---
name: stigg-widgets
description: Use when integrating Stigg's drop-in UI components — paywall / pricing table, customer portal, checkout, and the credit widgets (balance, utilization, usage chart, grants table, auto-recharge status, auto-recharge configuration). Triggers include "Stigg paywall", "pricing table", "customer portal", "Stigg checkout", "credits widget", "credit balance widget", "Paywall component", "CustomerPortal component", "render Stigg widget", "widget designer", "client-side security", "stigg widgets storybook". Skip for headless gating logic — use stigg-entitlements.
---

# Stigg Widgets — Drop-In UI

Stigg ships pre-built React components (with Next.js SSR support since v0.2.1) and a vanilla-JS client SDK for the most common pricing / billing UI surfaces. These are the canonical way to render paywalls, customer portals, checkout, and credit-balance UIs without rebuilding them. Vue and Embed SDKs also exist — see [docs.stigg.io](https://docs.stigg.io); the patterns below apply.

## Before You Start

Per the umbrella `stigg` skill: **search first.** Widget props evolve; the **Storybook is the live source of truth**.

### How to read the Storybook from an agent

The Storybook at `https://widgets.stigg.io/` is JavaScript-rendered (a basic HTTP fetch returns only the title). **But it exposes a machine-readable index** — `GET https://widgets.stigg.io/index.json` returns the full list of story IDs (pattern `widgets-<component>--<variant>`). Fetch that index whenever the user references widgets, then supplement with the per-widget docs pages under `docs.stigg.io/documentation/snap-in-widgets/<widget>` for props and snippets.

Full agent recipe — discovery workflow, story-ID categories, per-widget canonical doc paths, why a basic WebFetch only returns the title: `references/storybook.md`.

## Widgets at a Glance

| Widget | Use for | Reference |
|---|---|---|
| **Paywall / Pricing Table** | Public pricing page or in-app upgrade prompt | `references/paywall.md` |
| **Customer Portal** | In-app self-service: subscription, usage, billing, plan picker | `references/customer-portal.md` |
| **Checkout** | Cart-like in-app payment experience | `references/checkout.md` |
| **Credits widgets** (Balance, Utilization, Usage Chart, Grants Table, Auto-Recharge Status, Auto-Recharge Configuration) | Customer-facing credit-pool UI | `references/credit-widgets.md` |

## Setup

All widgets live inside a `<StiggProvider>` (React) or its equivalent in other framework SDKs. Use the **publishable key** (`client-`), never a server key.

```tsx
import { StiggProvider } from '@stigg/react-sdk';

export function App() {
  return (
    <StiggProvider apiKey="<STIGG_CLIENT_API_KEY>" customerId="<LOGGED_IN_CUSTOMER_ID>">
      <NestedComponents />
    </StiggProvider>
  );
}
```

Next.js: same — `@stigg/react-sdk` supports SSR, no separate package. Vanilla JS: `@stigg/js-client-sdk`. Vue: `@stigg/vue-sdk` follows the same provider shape — see docs.stigg.io.

> **Production setup must include client-side security hardening** (HMAC SHA256 signed customer tokens). Configure under the publishable key's detail panel. See `stigg-api/references/auth.md`.

## Composition: Customer Portal + Paywall

The `CustomerPortal` component supports composition — pass the `Paywall` as a slot / prop:

```tsx
<CustomerPortal
  paywallComponent={<Paywall />}
  theme={...}
  textOverrides={...}
/>
```

This wires up the portal's "Plan picker" section using the same paywall config.

## Composition: Modular Customer Portal

If the default portal layout doesn't fit your app, compose its sections individually under `CustomerPortalProvider`:

```tsx
import {
  CustomerPortalProvider,
  CustomerUsageData,
  PaymentDetailsSection,
  // SubscriptionsOverview, AddonsList, Promotions, InvoicesSection, ...
} from '@stigg/react-sdk';

function App() {
  return (
    <CustomerPortalProvider theme={...} textOverrides={...}>
      <CustomerUsageData />
      <PaymentDetailsSection />
    </CustomerPortalProvider>
  );
}
```

## Theming

Two paths:

1. **No-code Widget Designer** in the Stigg app — colors, typography, layout. Non-engineering owners can tune.
2. **Code-level theming** — `theme={...}` prop on each component, plus custom CSS targeting the documented stigg-prefixed classes (e.g. `stigg-payment-details-section-layout`, `stigg-{plan.id}`, `stigg-compatible-addon-{addon.id}`, `stigg-entitlement-feature-{feature.id}`).

Both can be combined. Re-fetch the docs for the current full CSS-class list.

## Text Overrides

Default copy can be overridden via `textOverrides`:

```tsx
const textOverrides = {
  manageSubscription: 'Manage',
  usageTabTitle: 'Usage',
  addonsTabTitle: 'Add-ons',
  promotionsTabTitle: 'Promotions',
  paywallSectionTitle: 'Plans',
  // ...
};

<CustomerPortal textOverrides={textOverrides} paywallComponent={<Paywall />} />
```

The full key list is in the docs — search `text overrides` if you need a specific one.

## Multi-Tenant (Multi-Active Subscriptions)

For products that allow multiple subscriptions per customer (workspaces / projects), pass `resourceId` everywhere — to `Paywall`, `CustomerPortal`, `Checkout`, and credit widgets:

```tsx
<Paywall resourceId="workspace-abc" onPlanSelected={({ plan, customer }) => { ... }} />

<CustomerPortal
  resourceId="workspace-abc"
  paywallComponent={<Paywall resourceId="workspace-abc" />}
/>
```

You also call `stigg.setResource('workspace-abc')` (and `clearResource()` when leaving the context) on the JS client so entitlement checks scope correctly.

## Picking a Renderer for the Paywall

Stigg's `Paywall` exposes the customer's intent via `onPlanSelected`. Branch on `intentionType`:

```tsx
<Paywall
  onPlanSelected={({ plan, intentionType }) => {
    switch (intentionType) {
      case SubscribeIntentionType.START_TRIAL:
        // provision trial subscription
        break;
      case SubscribeIntentionType.REQUEST_CUSTOM_PLAN_ACCESS:
        // redirect to a contact form
        break;
      case SubscribeIntentionType.UPGRADE_PLAN:
      case SubscribeIntentionType.DOWNGRADE_PLAN:
        // open the Checkout widget or your custom flow
        break;
    }
  }}
/>
```

## Cache Refresh

After your code performs an op that modifies the customer (provisioning, updating, granting), the cache on the JS client may briefly show stale data. The SDK exposes a refresh method — see the React / JS SDK page on cache refresh.

## When NOT to Use This Skill

- Headless gating in your backend (no UI) → `stigg-entitlements`.
- Modeling features / plans / add-ons → `stigg-pricing-modeling`.
- Provisioning / canceling subscriptions programmatically → `stigg-subscriptions`.
- Defining credit currencies / grants → `stigg-credits`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Embedding a server key in the widget setup | Always use the **publishable** key (prefix `client-`). It's read-only by design and safe to ship in browser bundles. |
| Skipping client-side security in production | The publishable key is publicly visible. Enable HMAC signed customer tokens. |
| Hard-coding plan names / prices in your app's UI | Use the widgets — they auto-reflect catalog changes. Hard-coded copies drift. |
| Forgetting `resourceId` on multi-active products | The widget targets the wrong subscription (or none). Pass it to every widget that takes it. |
| Trying to style the widget by overriding `<div>` selectors | Use the documented `stigg-*` CSS classes — they're stable and namespaced. |
| Composing the portal but forgetting to wrap in `CustomerPortalProvider` | The sub-sections won't have access to the customer / theme context. |
| Reading widget props from memory instead of the Storybook | Open `https://widgets.stigg.io/index.json` for the live story list, then the Storybook UI (in a browser) for prop tables. Re-confirm before authoring. |
| Trying to render the customer portal without an active subscription | Some sections (Plan picker / Paywall) work; others (Payment details / Invoices) require a paid sub or a connected billing provider. Surface that gracefully in your app. |
