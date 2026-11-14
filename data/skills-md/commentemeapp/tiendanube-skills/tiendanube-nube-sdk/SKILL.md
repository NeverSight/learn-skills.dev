---
name: tiendanube-nube-sdk
description: "Apply when building or migrating a Tiendanube / Nuvemshop app that runs code in the storefront or checkout with NubeSDK: the App(nube) entry point inside a Web Worker, nube.on, send, render, clearSlot, getState and getBrowserAPIs, storefront, checkout, fixed, custom and dynamic section slots, components in JSX or declarative form, config:set flags, cart validation and the cart:before_update gate, styling with styled(), StyleSheet and theme tokens, async storage, the Script resource and its Partners Portal settings, DevTools and Local Mode, open FTP theme copies without slots, and the re-homologation of apps already published. Use for converting a legacy DOM or jQuery script, choosing a slot, or debugging a script that does not load."
license: MIT
compatibility: "Tiendanube / Nuvemshop storefront and checkout scripts built with @tiendanube/nube-sdk-types, nube-sdk-ui and nube-sdk-jsx (create-nube-app templates), plus the Admin API 2025-03 Script resource. Not for apps embedded in the Admin or for theme JavaScript written by the merchant."
metadata:
  author: commente.me
  version: "0.1.0"
---

# NubeSDK: storefront and checkout scripts

## When this skill applies

Use this skill when an app puts code or UI in front of shoppers: in the storefront (home, product, category, search, cart, register) or in the checkout (start, payment, success).

- Scaffolding a script with `npm create nube-app@latest` and writing the `App(nube)` entry point
- Choosing a slot and rendering components into it, or reacting to cart, shipping, payment and order events
- Validating the cart, gating cart mutations, or adding items and coupons from the app
- Migrating a legacy script that uses `document`, `window`, jQuery or the `LS` object
- Registering the script in the Partners Portal, associating it with stores through `POST /scripts`, and shipping a version
- Explaining why an app works on the demo store but not on a merchant's store, or preparing re-homologation

Do not use this skill for:

- Screens that run inside the merchant Admin (use `tiendanube-admin-apps`)
- OAuth tokens and the install webhook that triggers script association (use `tiendanube-oauth-apps` and `tiendanube-webhooks`)
- Editing theme templates for their own sake (use `tiendanube-themes`); only the slot markup is covered here

## Decision rules

- Any app that injects scripts into the storefront or the checkout needs NubeSDK, private apps included. Apps that only call the API or only live in the Admin do not.
- The checkout already requires NubeSDK: the **Uses Nube SDK** flag is always on for checkout scripts. There is no window in which a legacy script runs in checkout.
- Pick the template by output: **Minimal** for event-only apps (tracking, validation), **Minimal with UI** for the declarative functions, **Minimal with UI in JSX** for anything with a real interface.
- Read data with `nube.getState()` at startup, and from the state passed to each listener afterwards. Change state only through `nube.send(event, modifier)`; the modifier returns a partial state that is merged. Pass a function to `nube.render()` when the UI depends on state, and re-render from the relevant event (`cart:update`, `shipping:update`, `location:updated`).
- Use the predefined slots first; `custom_*` slots only where you control the theme (open FTP or a fork), dynamic section slots only through runtime discovery. In repeatable slots (product grid items, the cart `before_line_item`), give each rendered element `key={product.id}` (or the line item id) so it lands in the right card; never use the array index.
- Prefer fixed slots (`corner_*`, `edge_*`, `bar_*`, `modal_content`) for overlays: they exist on every page where the SDK runtime is mounted. `bar_*_sticky` pushes content; `bar_top` and `bar_bottom` cover it.
- Style with theme tokens (`theme.color.accent`, `theme.border.radius`) instead of hex values, so the UI follows each store's theme.
- Use `fetch` for HTTP (the target must allow CORS), `asyncLocalStorage` / `asyncSessionStorage` for persistence, and `navigate("/path")` for same-domain navigation only.
- Keep scripts **auto installed** unless they need per-store data that lives outside the platform; manual scripts must be associated with every store through `POST /scripts`, and a `409` there means the association already exists (inspect it with `GET /scripts`).
- Leave the script on `onfirstinteraction`. `onload` needs prior approval for storefront scripts and is refused when the PageSpeed mobile score drops more than 10%.

## Hard constraints

### Constraint: Never touch the DOM; talk to the page through the SDK

The script runs in a Web Worker. `document`, `window`, `localStorage`, jQuery, React DOM and the theme's globals do not exist there.

**Why this matters**

Homologation rejects apps that use `document`, `window`, jQuery or direct DOM manipulation, and the code simply throws in the worker. Each app is isolated so it cannot break the store or other apps.

**Detection**

`document.`, `window.`, `querySelector`, `innerHTML`, `useJquery`, `LS.` or `localStorage.` in the bundle; an IIFE or `DOMContentLoaded` handler as the entry point.

**Correct**

```tsx
const renderPoints = (nube: NubeSDK) =>
	nube.render("after_line_items", (state) => (
		<Text>{`Acme points for this cart: ${Math.floor(state.cart.prices.total)}`}</Text>
	));

export function App(nube: NubeSDK) {
	renderPoints(nube);
	nube.on("cart:update", () => renderPoints(nube));
}
```

**Wrong**

```javascript
(function () {
	const el = document.createElement("div");
	el.innerHTML = "Acme points: " + LS.cart.subtotal / 100;
	document.querySelector(".js-cart-total").after(el);
})();
```

### Constraint: Send every config flag your app needs in a single config:set

`config:set` replaces the whole app config. Any flag left out of a call is reset to `false`.

**Why this matters**

`cart:validate` is ignored unless `has_cart_validation` is true, and `cart:before_update` is only dispatched when `handle_cart_before_update` is true. A second `config:set` that repeats only one flag silently switches the other feature off.

**Detection**

More than one `config:set` in the codebase, or a call that omits a flag another module relies on.

**Correct**

```typescript
nube.send("config:set", () => ({
	config: { has_cart_validation: true, handle_cart_before_update: true, disable_shipping_more_options: false }
}));
```

**Wrong**

```typescript
nube.send("config:set", () => ({ config: { handle_cart_before_update: true } }));
nube.send("config:set", () => ({ config: { has_cart_validation: true } }));
```

### Constraint: Answer each cart:before_update once, within 5 seconds, and guard your own re-adds

The gate is storefront only and fail-open: no answer within 5 seconds, or any value other than `proceed: false`, lets the mutation through. One `proceed: false` from any opted-in app cancels it.

**Why this matters**

An event that arrives before the listener exists is replayed only once, and the 5 second clock keeps running. Mutations the app sends itself (`cart:add`, `cart:remove`) go through the same gate and are also broadcast back to the sender, so an app that cancels and re-adds without a guard cancels its own re-add forever.

**Detection**

`nube.on("cart:before_update", ...)` registered after an `await`; a handler that can return without sending `cart:before_update:result`; a cancel-and-re-add flow with no record of pending self adds.

**Correct**

```typescript
const ACME_BLOCKED_PRODUCT_ID = 123;

export function App(nube: NubeSDK) {
	// first line of App: the single config:set with handle_cart_before_update: true
	nube.on("cart:before_update", (state) => {
		const p = state.eventPayload as { request_id?: string; item?: { product_id: number | null } } | null;
		if (!p?.request_id) return;
		const proceed = p.item?.product_id !== ACME_BLOCKED_PRODUCT_ID;
		nube.send("cart:before_update:result", () => ({
			eventPayload: { request_id: p.request_id, proceed, reason: proceed ? undefined : "acme_blocked" }
		}));
	});
}
```

**Wrong**

```typescript
export async function App(nube: NubeSDK) {
	const rules = await fetch("https://api.acme.example/rules").then((r) => r.json());
	nube.on("cart:before_update", (state) => {
		if (rules.block) nube.send("cart:before_update:result", () => ({ eventPayload: { proceed: false } }));
	});
}
```

### Constraint: Never hardcode a dynamic section slot, and check that a slot exists

Dynamic slot names end with a section instance id generated when the page is built. Static slot coverage also varies by theme, and `custom_*` slots exist only where a theme declares them.

**Why this matters**

A hardcoded `before_dynamic_section_<name>_<id>` works on one page of one store. On sectionable themes (Ipanema, Zenit Flex) every home section is dynamic, so static `before_section_*` slots do not exist at all. Discovery returns nothing in the Patagonia theme and in checkout; there, use the documented static slots.

**Detection**

A literal string with a long numeric suffix passed to `render`; `before_section_*` slots used with no fallback; a `custom_` name that breaks the lowercase snake_case rule.

**Correct**

```tsx
export async function App(nube: NubeSDK) {
	const dynamics = await nube.api.getAvailableSlots().getDynamic();
	const target = dynamics.find((s) => s.sectionType === "product-list" && s.type === "before_dynamic_section");
	if (target) nube.render(target, [<Text key="acme-deal">Acme deals below</Text>]);
}
```

**Wrong**

```tsx
nube.render("before_dynamic_section_single-shelf_1782228052519", <Text>Acme deals below</Text>);
```

### Constraint: For a published app, migrate in order and keep the legacy fallback

Re-homologation applies to App Store apps that inject scripts. Its order is fixed: CDN migration, then NubeSDK adaptation, then the request. Both scripts (legacy and NubeSDK) stay configured until Nuvemshop coordinates the retirement of the fallback.

**Why this matters**

Requests opened out of order, with the app still in dev mode, without a reachable demo store or without the rollout store list, are closed and must be opened again. The fallback covers stores the rollout has not reached and open FTP stores whose theme has no slots.

**Detection**

The legacy script disabled before the rollout ended; a request without APPID, demo store URL, 10 to 20 production stores or a technical contact; the same behavior running twice on an SDK-enabled store.

**Correct**

```text
1. Assets served from the CDN, migrated version live and stable
2. NubeSDK script with "Uses Nube SDK", bundle uploaded, development mode off
3. Legacy script still configured; no behavior runs twice where the SDK is active
4. Request: APPID, demo store URL with access, 10-20 rollout stores, technical contact
5. Monitor the initial stores and report errors at once (stage 3 is the partner's)
```

**Wrong**

```text
Legacy script disabled; request opened with the script in development mode and no rollout stores.
```

## Preferred pattern

The JSX template has `src/main.tsx` (exports `App`), `tsup.config.js` (ESM, minified, `dist/main.min.js`), Biome and Vitest. `npm run dev` serves `http://localhost:8080/main.min.js` (tsup watch plus a static server with CORS). Point the script's development URL there, or connect it with DevTools Local Mode. `npm run build` produces the bundle you upload in the script's **Version** section.

```tsx
import { Box, Text } from "@tiendanube/nube-sdk-jsx";
import type { NubeSDK } from "@tiendanube/nube-sdk-types";
import { styled, theme } from "@tiendanube/nube-sdk-ui";

const Card = styled(Box)`
	padding: 12px;
	border-radius: ${theme.border.radius};
	background-color: ${theme.color.main.background};
`;

function renderBanner(nube: NubeSDK) {
	nube.render("before_main_content", (state) => (
		<Card>
			<Text>{`Acme: ${String(state.cart?.items?.length ?? 0)} item(s) in your cart`}</Text>
		</Card>
	));
}

export function App(nube: NubeSDK) {
	nube.send("config:set", () => ({
		config: { has_cart_validation: true, handle_cart_before_update: false, disable_shipping_more_options: false }
	}));
	renderBanner(nube);
	nube.on("cart:update", ({ cart }) => {
		renderBanner(nube);
		const validation =
			cart.items.length > 0 ? { status: "success" } : { status: "fail", reason: "Acme needs one item" };
		nube.send("cart:validate", () => ({ cart: { validation } }));
	});
	nube.getBrowserAPIs().asyncLocalStorage.setItem("acme_seen", "1", 3600); // per-app key, TTL in seconds
}
```

Map legacy code to events, not clicks: a click on Buy becomes `cart:update`, a shipping choice becomes `shipping:update`, the thank-you page becomes `order:update`. Use `checkout:ready` with `location.page.data.step` (`start`, `payment`) to know where the shopper is in checkout.

For a store with open FTP opened before May 11, 2026, the theme copy has no slots. Add `{{ component('nubesdk-slot', { type: "before_main_content" }) }}` as the first element of `<body>` in `layouts/layout.tpl` (it renders `#nubesdk-root` and `#nubesdk-runtime`, without which the SDK does not boot), then the other slots, in both the AJAX cart and the full-page cart template, with `pick: item.id` on `before_line_item`.

## Common failure modes

- Expecting a script that works with DevTools Local Mode or development mode to reach shoppers. They get the uploaded bundle, and for App Store apps production activation follows homologation and a gradual rollout run by Nuvemshop.
- Treating `POST /scripts` success or an OAuth token as proof the SDK runs. Activation is per app and store pair; a test store also needs the SDK tag.
- Trying to hide native elements, inject JSON-LD into `head`, replace search results, run GTM or add UI inside the payment data form. None is possible; the Customization API covers a fixed list of targets, and analytics go through the Analytics API.
- Using deprecated slot names (`before_add_to_cart_pdp`, `cart_line_item_top`, `before_start_checkout_button`). They are redirected for now but may be removed.
- Calling `navigate` with an absolute or external URL; routes must start with `/`.
- Reading `cart.total`: totals live under `cart.prices` (`subtotal`, `total`), in the store's base currency.

## Review checklist

- [ ] No `document`, `window`, jQuery, `LS` or synchronous storage in the bundle
- [ ] `App(nube)` registers time-sensitive listeners before any `await`
- [ ] One `config:set` with every flag the app needs; every `cart:before_update` gets exactly one answer, and self-issued adds are guarded
- [ ] Slots exist on the targeted pages and themes; dynamic slots are discovered, repeatable slots are keyed
- [ ] Colors and radii come from theme tokens; script has **Uses Nube SDK**, `onfirstinteraction`, uploaded version and development mode off
- [ ] Manual scripts are associated with every store; published apps follow re-homologation with the fallback kept
- [ ] Tested with NubeSDK DevTools (Apps, Components, Events, Logs) on a store with the SDK tag

## Related skills

- [`tiendanube-admin-apps`](../tiendanube-admin-apps/SKILL.md): Admin iframe apps, homologation and publication
- [`tiendanube-oauth-apps`](../tiendanube-oauth-apps/SKILL.md): installing the app and getting the token used by `POST /scripts`
- [`tiendanube-webhooks`](../tiendanube-webhooks/SKILL.md): the install event that triggers script association
- [`tiendanube-themes`](../tiendanube-themes/SKILL.md): theme templates, FTP workflow and custom slots
- [`tiendanube-rest-api`](../tiendanube-rest-api/SKILL.md): the Script resource and the rest of the Admin API

## Reference

- [NubeSDK](https://nuvemshop.dev/en-US/apps/nube-sdk/overview.md): Web Worker isolation and the `nube` API surface
- [Getting Started](https://nuvemshop.dev/en-US/apps/nube-sdk/getting-started.md): templates, scripts, Partners Portal setup, troubleshooting and deploy
- [Script Structure](https://nuvemshop.dev/en-US/apps/nube-sdk/script-structure.md): `NubeSDK` type, `on`, `off`, `send`, `render`, `clearSlot`, config options
- [Overview (slots)](https://nuvemshop.dev/en-US/apps/nube-sdk/slots/overview.md): slot types, fixed slots, z-index order, modal and fullscreen behavior
- [Storefront Slots](https://nuvemshop.dev/en-US/apps/nube-sdk/slots/storefront-slots.md): slot list, theme coverage, keyed grid rendering, deprecated aliases
- [Checkout Slots](https://nuvemshop.dev/en-US/apps/nube-sdk/slots/checkout-slots.md): checkout and success page slots
- [Custom Slots](https://nuvemshop.dev/en-US/apps/nube-sdk/slots/custom-slots.md): `custom_` naming rules and type validation
- [Dynamic Section Slots](https://nuvemshop.dev/en-US/apps/nube-sdk/slots/dynamic-slots.md): per-page instance ids and discovery
- [Available Slots](https://nuvemshop.dev/en-US/apps/nube-sdk/api/available-slots.md): `getAvailableSlots()` and where it is not available
- [Events](https://nuvemshop.dev/en-US/apps/nube-sdk/events/overview.md): event table and checkout-only or storefront-only events
- [Cart Events](https://nuvemshop.dev/en-US/apps/nube-sdk/events/cart.md): `cart:validate`, the `cart:before_update` handshake, self-add guard
- [State](https://nuvemshop.dev/en-US/apps/nube-sdk/state/overview.md): reading and modifying state
- [Overview (components)](https://nuvemshop.dev/en-US/apps/nube-sdk/components/overview.md): component catalog
- [Best Practices (styling)](https://nuvemshop.dev/en-US/apps/nube-sdk/styling/best-practices.md): theme tokens, `styled()` and `StyleSheet`
- [Browser APIs](https://nuvemshop.dev/en-US/apps/nube-sdk/browser-apis.md): async storage with TTL, `navigate`, `fetch` and CORS
- [DevTools](https://nuvemshop.dev/en-US/apps/nube-sdk/devtools.md): panels, temporary block, storage keys, Local Mode
- [Migration Guide](https://nuvemshop.dev/en-US/apps/nube-sdk/migration-guide.md): known limitations and legacy to SDK mapping
- [Finished Migrating: What's Next?](https://nuvemshop.dev/en-US/apps/nube-sdk/after-migration.md): rollout, coexistence, private apps
- [Frequently asked questions about NubeSDK](https://nuvemshop.dev/en-US/apps/nube-sdk/faq.md): dates, activation per store, `409` on association
- [Implementing NubeSDK on stores with open FTP](https://nuvemshop.dev/en-US/apps/nube-sdk/ftp-themes.md): slot markup, `before_main_content`, `pick`, two carts
- [Scripts](https://nuvemshop.dev/en-US/api/resources/2025-03/script.md): script form, events, auto install, versions, statuses, `/scripts` endpoints
- [NubeSDK Re-homologation](https://nuvemshop.dev/en-US/apps/publish/homologation/nube-sdk-rehomologation.md): prerequisites, four stages, closed requests
- `nube-sdk/packages/create-nube-app/templates/minimal-ui-jsx/src/main.tsx` ([GitHub](https://github.com/TiendaNube/nube-sdk/blob/bff8d7b0f4f7df3bef962e270c74038b1a63f7f4/packages/create-nube-app/templates/minimal-ui-jsx/src/main.tsx)): entry point and `styled()` usage
- `nube-sdk/packages/create-nube-app/templates/minimal-ui-jsx/tsup.config.js` ([GitHub](https://github.com/TiendaNube/nube-sdk/blob/bff8d7b0f4f7df3bef962e270c74038b1a63f7f4/packages/create-nube-app/templates/minimal-ui-jsx/tsup.config.js)): ESM minified build to `.min.js`
- `nube-sdk/packages/types/src/main.ts` ([GitHub](https://github.com/TiendaNube/nube-sdk/blob/bff8d7b0f4f7df3bef962e270c74038b1a63f7f4/packages/types/src/main.ts)): `NubeSDKState` and listener signatures
- `nube-sdk/packages/types/src/domain.ts` ([GitHub](https://github.com/TiendaNube/nube-sdk/blob/bff8d7b0f4f7df3bef962e270c74038b1a63f7f4/packages/types/src/domain.ts)): `AppConfig` flags
