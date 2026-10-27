---
name: freemius-customer-portal
description:
  Build the Freemius Customer Portal in a React app — a self-service surface
  where a signed-in user manages their subscription (upgrade / change plan),
  cancels (with a churn-reducing retention coupon), edits billing information,
  and views payments & downloads invoices. Use when adding an "Account",
  "Billing", "Manage subscription", or "Invoices" page. Covers the React Starter
  Kit Customer Portal component and the SDK's headless portal processor
  (`freemius.customerPortal`); server-side checkout/entitlement sync is
  `freemius-core`.
---

# Freemius Customer Portal

Give a signed-in user one page to manage everything post-purchase:
subscriptions, upgrades, cancellation (with a retention offer), billing details,
and invoices — without your app reimplementing any billing logic.

Source: React Starter Kit Customer Portal component
<https://freemius.com/help/documentation/saas-sdk/react-starter/components/#customer-portal-component>

> **Framework note.** The route examples in this Skill are written for Hono, but
> the SDK's portal processor works with any framework supporting Web-Standard
> `Request`/`Response` routing — adapt the thin route to the app's real HTTP
> framework. The React Starter Kit `CustomerPortal` component targets **React
> 19+ with shadcn UI + Tailwind** (install via
> `npx shadcn@latest add https://shadcn.freemius.com/all.json`); if the app
> doesn't use shadcn/React, use it as a **reference** implementation.

> **Sandbox.** While validating, keep the processor's `isSandbox` wired to the
> dedicated `FREEMIUS_SANDBOX` env var (**never** `NODE_ENV`) so it matches the
> checkout's sandbox mode — sandbox is a checkout mode with test credit cards,
> owned by `freemius-core`.

## Golden rules (do not violate)

1. **The portal is headless and server-driven.** The SDK ships a
   `PortalRequestProcessor`: your backend exposes **one** endpoint
   (`GET|POST /api/portal`) and the SDK handles data retrieval _and_ every
   action behind signed, per-action URLs. The component never calls Freemius
   directly.
2. **Actions are token-signed.** Portal data arrives with pre-signed action URLs
   (cancel, coupon, billing-update, invoice). The component just hits those
   URLs; the SDK verifies the token server-side. You only supply the
   authenticated user's identity. (Upgrade is the exception — it goes through a
   server-built license-upgrade checkout (`setLicenseUpgradeByKey`), which
   avoids the double-subscription / renewing-license 500 pitfalls.)
3. **Identity is your job; everything else is the SDK's.** The processor's
   `getUser` resolves the Freemius user from your session (e.g. by email). All
   Freemius credentials stay server-side.
4. **Cancellation should try to retain first.** If a renewal-cancellation coupon
   is available, offer it before completing the cancellation.

## The one endpoint

```ts
// src/server/services/freemius/portal.ts
import { freemius, IS_SANDBOX } from './client';
import { env } from '../../env';

const PORTAL_ENDPOINT = `${env.publicAppUrl}/api/portal`;

export async function processPortalRequest(
  request: Request,
  email: string
): Promise<Response> {
  const processor = freemius.customerPortal.request.createProcessor({
    portalEndpoint: PORTAL_ENDPOINT, // must match the public URL the browser hits
    isSandbox: IS_SANDBOX,
    getUser: async () => {
      const fsUser = await freemius.api.user.retrieveByEmail(email);
      return fsUser?.id ? { id: String(fsUser.id), email } : { email };
    },
  });
  return processor(request); // dispatches by ?action= and verifies tokens
}
```

```ts
// src/server/routes/portal.ts — route stays thin: auth, then delegate.
portalRoute.on(['GET', 'POST'], '/', requireUser, async (c) =>
  processPortalRequest(c.req.raw, c.get('user').email)
);
```

The processor dispatches on the `?action=` query param:

| Method | `?action=`                         | Result                                           |
| ------ | ---------------------------------- | ------------------------------------------------ |
| GET    | `portal_data`                      | subscriptions + billing + payments + signed URLs |
| POST   | `billing`                          | update billing information                       |
| POST   | `subscription_cancellation`        | cancel renewal (+ optional feedback)             |
| POST   | `subscription_cancellation_coupon` | apply the retention coupon                       |
| GET    | `invoice`                          | stream the invoice PDF                           |

See [references/headless-endpoint.md](references/headless-endpoint.md).

## The component

Port `CustomerPortal` as editable shadcn/ui-style React source. It fetches
`?action=portal_data` once and renders four sections, each driven by signed URLs
baked into that data:

| Section             | What the user does                                                                                                                                                          | Reference                                                                        |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Subscription        | See current plan; upgrade via a server-built **license-upgrade checkout** (`setLicenseUpgradeByKey`) — the robust path (avoids double-subscription / renewing-license 500s) | [references/subscription-and-upgrade.md](references/subscription-and-upgrade.md) |
| Cancellation        | Cancel renewal — disclaimer → retention coupon → feedback                                                                                                                   | [references/cancellation-and-coupon.md](references/cancellation-and-coupon.md)   |
| Billing             | Edit business name / tax id / address                                                                                                                                       | [references/billing.md](references/billing.md)                                   |
| Payments & invoices | View payment history, download invoice PDFs                                                                                                                                 | [references/payments-and-invoices.md](references/payments-and-invoices.md)       |

## Quick start (frontend)

```tsx
import { CustomerPortal } from './react-starter/components/customer-portal';
import { PORTAL_ENDPOINT, portalFetch } from './api';

// portalFetch attaches the auth header; the component does the rest.
<CustomerPortal endpoint={PORTAL_ENDPOINT} fetcher={portalFetch} />;
```

```tsx
// Loading portal data:
const res = await fetcher(`${endpoint}?action=portal_data`);
const data = (await res.json()) as PortalData;
// data.subscriptions.{primary,active,past}, data.billing, data.payments,
// data.cancellationCoupons — each carries signed action URLs.
```

## Mental model

```
Frontend <CustomerPortal>               Backend (one endpoint)                Freemius
  GET  /api/portal?action=portal_data ─▶ processPortalRequest()
  { subscriptions, billing, payments, ◀─ freemius.customerPortal.request
    + signed action URLs }                .createProcessor() → getUser()
  POST <signed cancelRenewalUrl> ───────▶ processor verifies token ──────────▶ cancel renewal
  POST <signed couponUrl> ──────────────▶ processor verifies token ──────────▶ apply coupon
  POST <signed billing updateUrl> ──────▶ processor verifies token ──────────▶ update billing
  GET  <signed invoiceUrl> ─────────────▶ processor verifies token ──────────▶ invoice PDF
  GET  /api/checkout/upgrade ───────────▶ license.retrieve + checkout.create()
  { link } ◀──────────────────────────── .setLicenseUpgradeByKey(secret_key) ─▶ plan-change
                                          .getLink() — browser navigates ─────▶ checkout
```

> ⚠️ The upgrade path is the server-built license-upgrade checkout above. And
> **don't use `checkout.create({ licenseId })`** for it: that option 500s for
> actively-renewing licenses (the SDK internally calls a payment-method-update
> endpoint that rejects `expiration: null` licenses as "lifetime"). Fetch the
> license server-side and use `setLicenseUpgradeByKey(license.secret_key)`
> instead. See
> [references/subscription-and-upgrade.md](references/subscription-and-upgrade.md).

## Dashboard configuration (hand to the human)

- **Product → Coupons** → create a renewal-cancellation (retention) coupon so
  `cancellationCoupons` is populated and the wizard can offer it.
- The webhook + redirect setup that keeps the local entitlement in sync is owned
  by `freemius-core`; upgrades/cancellations arrive there as webhook events
  (`license.plan.changed`, `license.cancelled`, …).

## Post-action sync (how changes reach your app)

Portal actions change state **at Freemius first**; your local
`user_fs_entitlement` mirror catches up in two ways:

- **Immediately in the portal UI** — re-fetch `?action=portal_data` after any
  action (it reads live Freemius data).
- **In your entitlement mirror** — via `freemius-core`'s webhooks
  (`license.plan.changed` on upgrade, `license.cancelled`/expiry on
  cancellation). ⚠️ After setting or changing the webhook URL in the Dashboard,
  allow **~5 minutes for it to propagate** — events fired before the URL is
  active are never delivered (not retro-sent). See `freemius-core` →
  `references/webhooks.md` (and `freemius-troubleshooting` for the missed-event
  symptom).
