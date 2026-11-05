---
name: enable-analytics
description: Add Vercel Analytics, Vercel Speed Insights, and Google Tag Manager to the storefront.
---

# Enable Analytics

The current storefront includes support for Vercel Web Analytics and Vercel Speed Insights, with each integration disabled by default in `lib/config/index.ts`. This skill enables or adds those integrations and can also add Google Tag Manager using the recommended integration.

## Before you start

Ask the user two questions in order:

### 1. Do you need to add or change Vercel Analytics and/or Vercel Speed Insights?

- **Enable both** — page views, custom events, and Core Web Vitals
- **Analytics only** — page view and custom event tracking via `@vercel/analytics`
- **Speed Insights only** — Core Web Vitals monitoring via `@vercel/speed-insights`
- **Neither** — keep both integrations disabled

### 2. Do you want Google Tag Manager?

If yes, ask for the GTM container ID (e.g. `GTM-XXXXXX`). This will be stored in the `NEXT_PUBLIC_GTM_ID` environment variable.

Wait for the user to answer both questions before proceeding.

---

## Part A: Vercel Analytics and Speed Insights

If the storefront has `analytics` configuration in `lib/config/index.ts`, enable only the selected integrations. If the user selected neither, keep both integration gates disabled and skip the remaining steps in this section.

```ts
analytics: {
  shopify: {
    consent: { isEnabled: false, mode: "default-banner" },
    isEnabled: false,
  },
  speedInsights: { isEnabled: false },
  vercel: { isEnabled: false },
},
```

The `shopify` gate is separate: it controls Shopify storefront analytics and its consent integration. Standalone consent can be enabled separately through `shopify.consent.isEnabled`. Leave these settings alone unless the user asked about Shopify analytics or consent, and see Part D.

### A1. Install dependencies

For older storefronts without the integrations, install only the packages the user selected:

```bash
# Both
pnpm add @vercel/analytics @vercel/speed-insights

# Analytics only
pnpm add @vercel/analytics

# Speed Insights only
pnpm add @vercel/speed-insights
```

For older storefronts, create or update the root analytics component described below. Each library handles its own client-side behavior internally.

---

## Part B: Google Tag Manager

Skip this section if the user did not want GTM.

### B1. Install dependency

```bash
pnpm add @next/third-parties
```

### B2. Add environment variable

Add this row to the `# Optional` block of `.env.example`, keeping it alphabetical:

```bash
# NEXT_PUBLIC_GTM_ID="GTM-XXXXXX" # Set to load Google Tag Manager; leave unset to skip it.
```

Add `NEXT_PUBLIC_GTM_ID` to `turbo.json` `globalEnv`, keeping it alphabetical; Turborepo's strict mode hides undeclared variables from tasks and leaves them out of cache keys. Set the actual value in `.env.local` or in the Vercel dashboard under Environment Variables.

### B3. Add GTM to `components/analytics/index.tsx`

Import `GoogleTagManager` from `@next/third-parties/google`. Read `NEXT_PUBLIC_GTM_ID` in the analytics component and render `<GoogleTagManager gtmId={gtmId} />` only when the value exists. If the storefront extends `lib/config/index.ts` with a GTM integration gate, apply that gate inside the same component.

---

## Part C: Root analytics integration

### C1. Update `components/analytics/index.tsx`

Extend the existing root analytics component. Do not create a sibling `components/analytics.tsx`, which would shadow the directory import. Preserve the Shopify scripts gate: Shopify analytics, standalone consent, and WebMCP use the required numeric `NEXT_PUBLIC_SHOPIFY_SHOP_ID`. Build the ShopifyScripts props from configuration rather than making a shop-data request:

```tsx
import type { ShopifyScriptsI18n, ShopifyScriptsShop } from "@shopify/hydrogen";
import { GoogleTagManager } from "@next/third-parties/google";
import { Analytics } from "@vercel/analytics/next";
import { SpeedInsights } from "@vercel/speed-insights/next";

import { isShopifyScriptsEnabled, shopConfig } from "@/lib/config";

import { ShopifyScriptsTracker } from "./shopify-client";

export function AnalyticsComponents() {
  const gtmId = process.env.NEXT_PUBLIC_GTM_ID;
  const i18n: ShopifyScriptsI18n = {
    country: shopConfig.localization.country,
    language: shopConfig.localization.language,
  };
  const shop: ShopifyScriptsShop = {
    myshopifyDomain: process.env.NEXT_PUBLIC_SHOPIFY_STORE_DOMAIN as string,
    shopId: process.env.NEXT_PUBLIC_SHOPIFY_SHOP_ID as string,
    storefrontId: process.env.NEXT_PUBLIC_SHOPIFY_STOREFRONT_ID ?? "",
  };

  return (
    <>
      {shopConfig.analytics.vercel.isEnabled ? <Analytics /> : null}
      {shopConfig.analytics.speedInsights.isEnabled ? <SpeedInsights /> : null}
      {gtmId ? <GoogleTagManager gtmId={gtmId} /> : null}
      {isShopifyScriptsEnabled && <ShopifyScriptsTracker i18n={i18n} shop={shop} />}
    </>
  );
}
```

Remove imports for integrations the storefront does not support.

### C2. Update `app/layout.tsx`

Render the root analytics component near the end of `<body>`. The default has inline component copy, not a translation provider; in an already localized installation, preserve its scoped translation-provider boundaries:

```tsx
import { AnalyticsComponents } from "@/components/analytics";
```

```tsx
<body ...>
  {/* ... existing layout content and scoped providers ... */}
  <Suspense>
    <AnalyticsComponents />
  </Suspense>
</body>
```

Do not add next-intl or a root message catalog for analytics. In a customized localized storefront, preserve any required commerce locale prop and existing scoped providers; do not pass the complete catalog to a root `NextIntlClientProvider`. The root component remains mounted as the extension point for current and future analytics providers. Provider gates stay inside it so disabled integrations are not mounted.

## Part D: Shopify storefront analytics

Only make changes here if the user asked about Shopify analytics or consent.

The storefront sends page, product, collection, search, cart-view, and confirmed cart-change events through Hydrogen's analytics bus when Shopify scripts are enabled. Shopify analytics is disabled by default. Set the required `NEXT_PUBLIC_SHOPIFY_SHOP_ID` before building the storefront. Use the numeric Shopify shop ID, not the Headless storefront ID. To turn Shopify's built-in analytics destination and consent integration on, set `analytics.shopify.isEnabled` to `true` in `lib/config/index.ts`. To load Shopify consent without its analytics destination, set `analytics.shopify.consent.isEnabled` to `true`. WebMCP also loads Shopify scripts and consent without enabling the analytics destination.

Consent mode is set by `analytics.shopify.consent.mode` in `lib/config/index.ts` and defaults to `default-banner`, which renders Shopify's hosted privacy banner for visitors in regions that require consent. Use `custom-banner` when the storefront supplies its own consent UI. Do not ship `no-banner` in production unless consent is handled elsewhere, because visitors in those regions can never grant consent and their events are dropped.

Third-party analytics can subscribe through the same destination API, so consent gating and buffered replay remain centralized. Register destinations with `addAnalyticsDestination()` from `lib/analytics/client.ts`; do not publish cart-change events manually.

## Guardrails

- Keep root analytics providers and their gates in `components/analytics/index.tsx`; mount Shopify scripts when Shopify analytics, consent, or WebMCP is enabled.
- Always mount `<AnalyticsComponents />` from the root layout, even when every provider is disabled.
- The GTM container ID must come from `NEXT_PUBLIC_GTM_ID`, never hardcoded. The provider renders nothing if the env var is missing.
- Use `@next/third-parties/google` for GTM, not a manual `<script>` tag. The Next.js component handles script loading and performance optimization.
- Import paths: use `@vercel/analytics/next` and `@vercel/speed-insights/next` (the `/next` subpath), not the root package exports.
- Add `NEXT_PUBLIC_GTM_ID` to `.env.example` with a placeholder value so other developers know the variable exists.
