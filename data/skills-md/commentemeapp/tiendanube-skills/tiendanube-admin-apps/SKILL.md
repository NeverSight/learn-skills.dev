---
name: tiendanube-admin-apps
description: "Apply when building, reviewing or publishing a Tiendanube / Nuvemshop app with a merchant-facing panel: integrated apps loaded in an Admin iframe through Nexo (connect, iAmReady, ACTION_NAVIGATE_SYNC, getSessionToken, ErrorBoundary) and built with the Nimbus design system, or external apps with their own panel. Covers the official Node and React templates, Developer Mode, design guidelines and UX writing, the homologation artifacts and design checklist, App Store publication data, private versus App Store distribution, and charging merchants with the billing model and the Billing API (plans, subscriptions, charges). Use for starting an Admin app, fixing an embedded app that never loads, preparing a homologation request, or wiring plan upgrades."
license: MIT
compatibility: "Tiendanube / Nuvemshop partner apps: React frontends with @tiendanube/nexo and @nimbus-ds packages, Node backends (Express template), Admin API 2025-03 Billing resource, Partners Portal. Not for storefront or checkout scripts."
metadata:
  author: commente.me
  version: "0.1.0"
---

# Admin apps, homologation and billing

## When this skill applies

Use this skill when the merchant uses your app through a screen: inside the store Admin (integrated) or on your own site (external), and when that app goes to the App Store.

- Scaffolding from the integrated template (Express API plus React frontend) or the external one
- Making an iframe app appear in the Admin: Nexo instance, readiness handshake, route sync
- Calling your backend from the iframe with the Nexo session token
- Building screens with Nimbus components, patterns and templates that pass the design checklist
- Preparing homologation: sequence diagram, demo video, demo account, FAQ document, publication data
- Choosing a billing model and managing plans, subscriptions and extra charges

Do not use this skill for:

- Scripts that run in the storefront or checkout (use `tiendanube-nube-sdk`)
- The OAuth code exchange and scopes in depth (use `tiendanube-oauth-apps`)
- Payment, shipping or ERP specific flows (use `tiendanube-shipping-payment-apps` or `tiendanube-erp-integration`)

## Decision rules

- **Integrated** when merchants should work inside the Admin: React is required, because Nexo connects the iframe and Nimbus, which is built for React, sets the interface standard. **External** when the app has its own panel: Nimbus is recommended, not required.
- **For Your Customers** (private) skips homologation and installs through `/admin/apps/{app_id}/authorize` on the store's Admin. **App Store** goes through homologation and publication. Either way, an app that injects scripts also needs NubeSDK.
- Start from the official templates (`tiendanube-app-native-template-node` with its React frontend for integrated apps, `tiendanube-app-standalone-template-node` for external ones); they ship OAuth installation and, for integrated apps, Nexo already wired.
- Test integrated apps with **Developer Mode** ("Test App" menu in the Admin, where you enter the app URL). It only exists on stores the Nuvemshop team enabled; request it.
- Every permission added or edited requires uninstalling and reinstalling the app to get a token with the new scope. Request only the scopes the app needs; the sequence diagram must match them.
- Use webhooks instead of polling, paginate every list call, send a `User-Agent` with app name and contact email, and respect the default rate limit of 2 requests per second per store and app (10 times more on the Next plan), reading the `x-rate-limit-*` headers.
- Page widths: 800px for forms, 1200px for tables and multi-column content. Replace tables with a Data List on mobile.
- One primary action per page (Button `primary`); page-level actions sit right-aligned in the Page header; local actions sit in their Card. More than two row actions collapse into an ellipsis icon button.
- Status of a condition uses Tag; a quantity uses Badge. Alert for problems that need action or async confirmation; Toast for informative feedback. Skeleton while a page loads, Spinner for a local action, Toast Progress for a task that changes page.
- Choose the billing model per country before requesting homologation: Free (no subscription, external billing allowed), One-time fee, or Monthly fee. Only Monthly fee creates subscriptions you manage with the Billing API. Prices and countries lock while the app is **In approval**.
- App Store name: up to 35 characters, no Tiendanube or Nuvemshop trademarks, starting with a unique term. Icon: 600x600 JPEG or PNG, no text, screenshots or photos, logo not touching the edges.

## Hard constraints

### Constraint: Complete the Nexo handshake and wrap the app in Nexo's ErrorBoundary

An integrated app must create the Nexo instance with its `clientId`, wait for `connect(nexo)`, call `iAmReady(nexo)`, and then keep a listener for `ACTION_NAVIGATE_SYNC`, which the Admin sends with the initial route right after the ready signal. `ErrorBoundary` from `@tiendanube/nexo` goes at the top of the tree.

**Why this matters**

The Admin shows a loading message until the iframe reports it is ready. Skipping `iAmReady`, or mounting the route sync component before it, leaves the merchant on the loader or on the wrong route. `connect` rejects after its timeout (3000 ms by default), so the rejection needs handling. The ErrorBoundary is mandatory for App Store publication: it dispatches `ACTION_LOG_ERROR` (URL, message, stack) and the Admin shows its own fallback instead of a broken iframe.

**Detection**

No `iAmReady` call; `syncPathname` or `nexo.suscribe(ACTION_NAVIGATE_SYNC, ...)` mounted before the connection resolves; `connect` without `.catch`; no `ErrorBoundary` from `@tiendanube/nexo`, or a homemade one; a hardcoded `clientId` that differs from the app id.

**Correct**

```tsx
const AcmeApp: React.FC = () => {
	const [connected, setConnected] = useState(false);
	useEffect(() => {
		connect(nexo)
			.then(() => {
				setConnected(true);
				iAmReady(nexo);
			})
			.catch(() => setConnected(false));
	}, []);
	if (!connected) return <AcmeSkeleton />;
	return (
		<ErrorBoundary nexo={nexo}>
			<BrowserRouter>
				<NexoSyncRoute>
					<AcmeRouter />
				</NexoSyncRoute>
			</BrowserRouter>
		</ErrorBoundary>
	);
};
```

**Wrong**

```tsx
const AcmeApp = () => (
	<BrowserRouter>
		<NexoSyncRoute>
			<AcmeRouter />
		</NexoSyncRoute>
	</BrowserRouter>
);
```

### Constraint: Authenticate iframe calls with the session token, never with the store access token

From the frontend, get a JWT with `getSessionToken(nexo)` for every request and send it as `Authorization: Bearer`. The backend verifies it with the app's client secret and looks up the store's access token on its side.

**Why this matters**

The session token identifies the logged-in store and is signed with the client secret. The Admin API access token grants the app's full scopes and must stay on the server. The Node template verifies with `SECRET_KEY`, which is `THE_SECRET` in Developer Mode and must be the app's client secret in production.

**Detection**

An access token in frontend code, local storage or a query string; a backend route without JWT verification; `SECRET_KEY` left as `THE_SECRET` in a production environment.

**Correct**

```ts
acmeApi.interceptors.request.use(async (config) => {
	const token = await getSessionToken(nexo);
	config.headers.Authorization = `Bearer ${token}`;
	return config;
});
// backend
passport.use(
	new JWTStrategy(
		{ jwtFromRequest: ExtractJWT.fromAuthHeaderAsBearerToken(), secretOrKey: process.env.SECRET_KEY },
		(payload, done) => done(null, storeRepository.findOne(payload.storeId) ?? false)
	)
);
```

**Wrong**

```ts
fetch(`https://api.acme.example/products?store=${storeId}&token=${accessToken}`);
```

### Constraint: Use Nimbus as published, without overrides

Build integrated screens with Nimbus templates first, patterns second, and components last, using only the properties documented in Storybook and the UI kit.

**Why this matters**

The design checklist marks the empty and initial state page, the error page, template customization limits, component assignments, customization limits, action prioritization, responsiveness and every UX writing item as mandatory. Overriding component styles is prohibited; a missing property is requested through a discussion in the Nimbus GitHub repository.

**Detection**

`className` or `style` used to restyle Nimbus components, CSS targeting their internals, a list screen with no empty state, a destructive action without a confirmation modal, or required fields not separated from fields labeled "(Optional)".

**Correct**

```tsx
<Page maxWidth="800px">
	<Page.Header title="Configure shipping labels" />
	<Page.Body>
		<Layout columns="1">
			<Layout.Section>
				<Card>
					<Input id="acme-sender" />
				</Card>
			</Layout.Section>
		</Layout>
	</Page.Body>
</Page>
```

**Wrong**

```tsx
<Button style={{ background: "#ff6600", borderRadius: 0 }}>Save</Button>
```

### Constraint: Change a merchant's plan only on an existing subscription, after the merchant chose it

Subscriptions are created by the platform at installation for apps with a monthly fee; there is no endpoint to create one. `PATCH .../subscriptions` switches the plan, and the merchant must choose the paid plan in your app first.

**Why this matters**

A Free listing has no subscription (GET returns `404`, not a zero-value subscription), so a PATCH cannot turn it paid. Changing a subscription price, or patching or deleting a plan, also rewrites charges that are not yet paid or waiting for payment. The App Store requires that merchants upgrade and downgrade without contacting support or reinstalling.

**Detection**

A PATCH sent on install or from an admin script; plan limits enforced only by Billing (it does not count usage; your backend must); charge webhooks handled without checking `app_id`.

**Correct** (the Billing page does not show the base URL; the `/2025-03/{store_id}` prefix is inferred from the other 2025-03 resources, so confirm it against a demo store)

```http
GET  /2025-03/{store_id}/concepts/app-cost/services/{app_id}/subscriptions
PATCH /2025-03/{store_id}/concepts/app-cost/services/{app_id}/subscriptions
Content-Type: application/json

{ "plan_id": "<plan the merchant just selected in the Acme plans screen>" }
```

**Wrong**

```http
PATCH /v1/{store_id}/concepts/app-cost/services/{app_id}/subscriptions

{ "amount_value": 0 }
```

### Constraint: Submit homologation only when the app is complete and the artifacts are ready

Homologation starts after all artifacts arrive, and publication data is filled in parallel in **Publication Data**.

**Why this matters**

Apps found incomplete or still in development are removed from the queue, and so are apps whose partner does not answer the team within 5 days or claims fixes that were not made. The team has up to 30 business days to answer after the artifacts arrive. ERP, payment and shipping apps also go through a scripted video demonstration checked against a checklist.

**Detection**

A request with no sequence diagram, a video that installs from the partner's panel instead of the authorize URL, a demo account still behind a paywall or approval step, no FAQ document, or missing privacy webhooks.

**Correct**

```text
- Sequence diagram of every Admin API call, with webhooks instead of polling
- Video: install via https://www.tiendanube.com/apps/{app_id}/authorize, sign-up, login,
  uninstall and reinstall, main features, any required setup
- Demo account past subscription and approval steps; FAQ document from the category template
- Privacy webhooks configured; billing model and listing filled per country
```

**Wrong**

```text
"Request homologation" clicked with the app half built, then no reply to the review team for a week.
```

## Preferred pattern

The integrated template splits `api/` (Express: `/auth/install` exchanges the code, JWT-protected routes, Admin API client) from `frontend/` (Vite, React, Nexo, Nimbus).

```tsx
// frontend/src/app/NexoClient.ts
const nexo = create({ clientId: import.meta.env.VITE_CLIENT_ID, log: true });

// frontend/src/app/NexoSyncRoute.tsx (rendered after iAmReady)
const NexoSyncRoute = ({ children }: { children: JSX.Element }) => {
	const { pathname } = useLocation();
	const navigate = useNavigate();
	useEffect(() => {
		syncPathname(nexo, pathname);
	}, [pathname]);
	useEffect(
		() =>
			nexo.suscribe(ACTION_NAVIGATE_SYNC, ({ path, replace }: NavigateSyncResponse) =>
				navigate(path, { replace: Boolean(replace) })
			),
		[navigate]
	);
	return children;
};
```

After installation, consume the OAuth `code` on the backend and send the merchant straight to sign-up or login, or to a landing page that separates existing customers from new ones. Never ask for the store URL, never run OAuth in a pop-up, and never display the code. Use `navigateHeader(nexo, { goTo: "/", text: "Back" })` for the Admin top bar and `getStoreInfo(nexo)` for store name, language and currency.

For paid plans: set the monthly base price in Publication Data, request Billing enablement with the app id (plus the demo store id for a test subscription), add the `read_subscriptions`, `write_subscriptions`, `write_charges` and `write_plans` scopes, and reinstall. Create extra charges with `POST /services/{app_id}/charges` one day before the subscription's `next_execution`, for the same period. Billing periods align to the 16th of the month, with proration on the first charge.

## Common failure modes

- Leaving the Redirect URL on the Partners Portal default, which sends merchants to the partner login after they accept.
- Adding a scope and testing with the old token instead of reinstalling.
- Allowing any site to frame the app; the publication rules require protecting iframes against external domains.
- Showing raw 404 or 500 pages; the app must be fully usable and the error page template is mandatory.
- Using Billing endpoints under `v1`; they exist only in `2025-03` (and `unstable`).
- Editing price or countries while **In approval**; ask support to return the app to **In development** first.
- Writing screen titles with the app's name or a final period; titles describe the task, ideally with a verb.
- Reading the publication guidelines' mentions of an "App Bridge" library or "theme app extensions" literally; every other page uses Nexo for embedded apps and NubeSDK slots for storefront code.
- Offering support only in one language while publishing in countries that speak another.

## Review checklist

- [ ] App type (integrated or external) and distribution (private or App Store) decided and documented
- [ ] Nexo: `connect` with `.catch`, `iAmReady`, route sync mounted after it, `ErrorBoundary` at the top
- [ ] Every backend call carries the session token; access tokens never leave the server
- [ ] Screens use Nimbus templates and patterns without overrides; empty, error and confirmation states exist
- [ ] Widths, action placement, status components and feedback follow the UX/UI concepts; texts follow UX writing
- [ ] Scopes are minimal, match the sequence diagram, and the app was reinstalled after changes
- [ ] Billing model set per country; plan changes go through PATCH on an existing subscription after the merchant chooses
- [ ] Homologation artifacts complete: diagram, video, demo account, FAQ document, privacy webhooks
- [ ] Publication Data filled: description in the required structure, icon, images per country, support channels

## Related skills

- [`tiendanube-nube-sdk`](../tiendanube-nube-sdk/SKILL.md): storefront and checkout scripts and their re-homologation
- [`tiendanube-oauth-apps`](../tiendanube-oauth-apps/SKILL.md): authorization code exchange, scopes and reinstall
- [`tiendanube-webhooks`](../tiendanube-webhooks/SKILL.md): privacy webhooks, `subscription/updated` and `charge/*` events
- [`tiendanube-rest-api`](../tiendanube-rest-api/SKILL.md): pagination, rate limits and the `User-Agent` header
- [`tiendanube-shipping-payment-apps`](../tiendanube-shipping-payment-apps/SKILL.md): apps with the extended homologation checklist
- [`tiendanube-erp-integration`](../tiendanube-erp-integration/SKILL.md): ERP apps and their scripted demonstration

## Reference

- [Overview](https://nuvemshop.dev/en-US/apps/admin/overview.md): app creation, distribution types, demo store, private install, permissions, ErrorBoundary requirement
- [Integrated Applications](https://nuvemshop.dev/en-US/apps/admin/integrated.md): actors, initialization flow, Developer Mode
- [External Applications](https://nuvemshop.dev/en-US/apps/admin/external.md): independent apps and Nimbus as a recommendation
- [App Templates](https://nuvemshop.dev/en-US/apps/admin/app-templates.md): integrated and external templates, React required for integrated apps
- [Nexo](https://nuvemshop.dev/en-US/apps/admin/nexo.md): instance, `connect`, `iAmReady`, route sync, session token, ErrorBoundary, actions and helpers
- [Frequently asked questions about the Admin and apps](https://nuvemshop.dev/en-US/apps/admin/faq.md): Redirect URL, reinstall after scope changes, loading issues
- [Use of Design Templates](https://nuvemshop.dev/en-US/apps/admin/design-guidelines/template-usage.md): empty, error, form, confirmation, settings and table templates
- [Components and Patterns](https://nuvemshop.dev/en-US/apps/admin/design-guidelines/component-usage.md): component assignments, form components, prohibited overrides
- [UX/UI Concepts](https://nuvemshop.dev/en-US/apps/admin/design-guidelines/concept-usage.md): actions, status, feedback, loading, tables, widths, forms
- [UX Writing Concepts](https://nuvemshop.dev/en-US/apps/admin/design-guidelines/ux-writing-usage.md): naming apps and screens, tone, text patterns
- [Overview (homologation)](https://nuvemshop.dev/en-US/apps/publish/homologation/overview.md): request steps, privacy webhooks, ERP, payments and shipping path
- [Requirements (homologation)](https://nuvemshop.dev/en-US/apps/publish/homologation/requirements.md): requirements by app type, sequence diagram, video, demo account
- [Design Requirements](https://nuvemshop.dev/en-US/apps/publish/homologation/checklist.md): priority and mandatory items of the design checklist
- [Homologation Process](https://nuvemshop.dev/en-US/apps/publish/homologation/async.md): asynchronous flow, 30 business days, action plan
- [Best Practices](https://nuvemshop.dev/en-US/apps/publish/homologation/guidelines.md): pagination, `User-Agent`, webhooks, scopes, rate limit
- [Publication Guidelines](https://nuvemshop.dev/en-US/apps/publish/guidelines.md): prohibited apps, setup flows, plan changes, name and icon rules, security, queue policy
- [Overview (publication)](https://nuvemshop.dev/en-US/apps/publish/app-publication/overview.md): artifacts and Publication Data in parallel
- [Requirements (publication)](https://nuvemshop.dev/en-US/apps/publish/app-publication/requirements.md): images, icon, description structure, FAQ templates, locked data
- [Landing Page](https://nuvemshop.dev/en-US/apps/publish/landing-page.md): post-install onboarding page
- [Pricing & Billing](https://nuvemshop.dev/en-US/apps/publish/pricing-billing.md): billing models, monthly setup, free listings, plan limits
- [Frequently asked questions about publishing and homologation](https://nuvemshop.dev/en-US/apps/publish/faq.md): login URL for Admin-only apps, timing, icon formats
- [Billing](https://nuvemshop.dev/en-US/api/resources/2025-03/billing.md): scopes, plans, subscriptions, billing cycle, charges, webhooks
- `tiendanube-app-native-template-react/src/app/App.tsx` ([GitHub](https://github.com/TiendaNube/tiendanube-app-native-template-react/blob/af3305c3292d53ba8810a7c434f6d2b4a1969fea/src/app/App.tsx)): handshake, ErrorBoundary and provider order
- `tiendanube-app-native-template-react/src/app/NexoSyncRoute/NexoSyncRoute.ts` ([GitHub](https://github.com/TiendaNube/tiendanube-app-native-template-react/blob/af3305c3292d53ba8810a7c434f6d2b4a1969fea/src/app/NexoSyncRoute/NexoSyncRoute.ts)): route sync with React Router
- `tiendanube-app-native-template-react/src/app/Axios/Axios.ts` ([GitHub](https://github.com/TiendaNube/tiendanube-app-native-template-react/blob/af3305c3292d53ba8810a7c434f6d2b4a1969fea/src/app/Axios/Axios.ts)): session token interceptor
- `tiendanube-app-native-template-react/src/pages/Products/Products.tsx` ([GitHub](https://github.com/TiendaNube/tiendanube-app-native-template-react/blob/af3305c3292d53ba8810a7c434f6d2b4a1969fea/src/pages/Products/Products.tsx)): Page and Layout patterns, 1200px table page, mobile list
- `tiendanube-app-native-template-node/api/.env.example` ([GitHub](https://github.com/TiendaNube/tiendanube-app-native-template-node/blob/201f0ff79a7f8d7e7e477c109fd0eb8a4af4692f/api/.env.example)): `SECRET_KEY` in Developer Mode and production
- `tiendanube-app-native-template-node/api/src/utils/passaport-strategy.ts` ([GitHub](https://github.com/TiendaNube/tiendanube-app-native-template-node/blob/201f0ff79a7f8d7e7e477c109fd0eb8a4af4692f/api/src/utils/passaport-strategy.ts)): JWT verification of the session token
- `tiendanube-app-native-template-node/api/src/features/auth/install-app.service.ts` ([GitHub](https://github.com/TiendaNube/tiendanube-app-native-template-node/blob/201f0ff79a7f8d7e7e477c109fd0eb8a4af4692f/api/src/features/auth/install-app.service.ts)): authorization code exchange on install
- `nimbus-design-system/packages/react/README.md` ([GitHub](https://github.com/TiendaNube/nimbus-design-system/blob/61996b1dfbfa4c774c207c745c0fe5f5fbcb59df/packages/react/README.md)): `@nimbus-ds/components` installation and usage
