---
name: teleport
description: Set up an app-to-web flow or experiment with the superwall framework's teleport — the shopper starts on a paywall or onboarding in the iOS app and finishes on the web, paying with Apple Pay through Stripe, and the app is credited on its own. Covers the recommended setup (`teleport.route` in config.ts, the Apple Pay gate with `useApplePay().available` and `router.push(route, { teleport:false })`, `teleport.fallbacks`, blocking prepaid cards), what buying a Stripe product inside the app does, direct Apple Pay checkout (not with Stripe Managed Payments), A/B testing teleport by paywall in a campaign, and a catalogue of setups and experiments (web pricing, discounts, failure rescue, abandonment offers, custom teleport screens, trial eligibility, `completion`, attribution). Use when the user asks to "set up app to web", "app-to-web experiment", "teleport", "send users to web checkout from the app", "sell on the web from iOS", "Stripe / Apple Pay from the app", or to test web checkout against the App Store. Needs the superwall-framework skill for everything else about the paywall.
user-invocable: true
---

# Teleport: app to web

App to web means the shopper starts in the iOS app and finishes on the web:
a paywall shown by SuperwallKit 4.18+ opens one of its routes in the
shopper's browser, they pay there with Apple Pay (Stripe), and the app is
credited without a restore. With the superwall framework this is one key,
`teleport`, in the paywall's `config.ts`; the same paywall runs on both
sides, so nothing is built twice. Everything about writing the paywall
itself (routes, hooks, layout, push and publish) is in the
`superwall-framework` skill; this skill is how to set up teleport well.

The framework is headless React: every screen, offer, branch and
fallback here is code the user owns, so anything they can describe they can
build. Treat the setup below as the baseline and
[references/experiments.md](references/experiments.md) as the menu of what
else is possible; offer from it.

These are **today's recommendations** (November 2026). They come from what
converts so far and may change; when the user's own results disagree, theirs
win. Say so when you hand a setup over.

## The rules

1. **Teleport through `teleport.route` in `config.ts`, always.** Name the
   route the web half opens on: `teleport: { route: "plan" }`. A paywall
   with `teleport.route` prepares that teleport and warms the web page the
   moment it opens, asks Apple about Apple Pay at the same time, and
   `superwall push` pre-renders the route so the browser paints it before
   any script runs. A route teleported only with
   `router.push(route, { teleport: true })` gets none of that and opens
   cold. Never hand-build a link or call `openExternalUrl` to reach the web.
2. **Send only shoppers with Apple Pay to the web.** App to web converts
   well when the shopper pays with a double click; typing a card in a
   browser does not. Read `useApplePay().available` and push the route with
   `{ teleport: applePay.available }`: `true` teleports, `false` pushes the
   same route in the app (`teleport: false` overrides `teleport.route`), so
   the page is still warmed and checked. `false` includes `checking`, the
   first moments before Apple answers; it is cached for the page, and the
   paywall asked when it opened, so by the shopper's tap it has almost
   always answered. Call `await checkApplePay()` instead when a tap must
   wait for the real answer (at most 1.5 s, never `checking`).
3. **In the app, sell store products; on the web, Stripe products.** The
   route pushed in the app (no Apple Pay) offers the App Store product;
   branch on `useDevice().host` (`"ios-sdk"` or `"android-sdk"` in an
   app, `"web-teleport"` on the teleport page), never on the URL.
   `purchase()` of a Stripe product inside the app teleports: to
   `teleport.route` with the tapped product preselected there
   (`useTeleport().productReference`), or, without `teleport.route`, to
   the route it was tapped on, cold. That is fine as a deliberate path,
   never as a side effect of the in-app branch.
4. **Map every Stripe product to a store product in `teleport.fallbacks`.**
   While the shopper is in the browser the app shows Superwall's teleport
   screen; `fallbacks` adds "Continue In-App Instead", which buys the store
   product. It is the way back for anyone who changes their mind.
5. **Use direct Apple Pay, and block prepaid cards:** `checkout: { mode:
   "applePay", prepaidCards: "block" }`. Direct Apple Pay opens Apple's own
   sheet on the tap, a double click and done; it converts better than
   Stripe's embedded card sheet (`"sheet"`), so never pick `"sheet"` for a
   teleport paywall. It is **not available with Stripe Managed Payments**: a
   Managed Payments session can't be paid with Apple Pay directly
   (`useApplePay(product).product.reason` is `session_unsupported`) and the
   shopper gets the card sheet instead. When the account uses Managed
   Payments, tell the user, recommend direct Apple Pay, and let them decide
   whether to set `managedPayments: false` in `checkout` for this paywall
   (they give up Stripe acting as merchant of record on it). Prepaid cards
   are how free trials are abused; `prepaidCards` holds on the card sheet,
   but Apple Pay itself can't be filtered by card type, so also add a Radar
   rule in the Stripe dashboard (see setup).
6. **A/B test with separate paywalls, not branches in one.** Each variant is
   its own paywall directory with its own `teleport.route`, attached as its
   own variant in a campaign. A flag inside one paywall that decides which
   route teleports loses the preparation, warm-up and pre-render for every
   route but the configured one.

## Worked example

The `teleport` example (`superwall create --example teleport`) is the full
flow; this is the shape with the rules above applied. `monthly` and `pro`
are Stripe products, `annual` the App Store one.

```ts
// paywalls/web-checkout/config.ts
import { definePaywall } from "superwall/config";

export default definePaywall({
  name: "Web checkout",
  teleport: { route: "plan", fallbacks: { monthly: "annual", pro: "annual" } },
  checkout: { mode: "applePay", prepaidCards: "block" },
  products: {
    monthly: "live:price_MONTHLY:7days-free",
    pro: "live:price_PRO:no-trial",
    annual: "pro_5999_year",
  },
});
```

```tsx
// paywalls/web-checkout/app/goal.tsx — in the app
import { useApplePay } from "superwall/hooks";
import { useRouter } from "superwall/navigation";

export default function Goal() {
  const router = useRouter();
  const applePay = useApplePay();

  return (
    <button
      type="button"
      onClick={() => {
        // Apple Pay set up: plan opens in the browser. Otherwise: plan, in the app.
        router.push("plan", { teleport: applePay.available });
      }}
    >
      Continue
    </button>
  );
}
```

```tsx
// paywalls/web-checkout/app/plan.tsx — on the web, or in the app without Apple Pay
import { useDevice, useProducts, usePurchase } from "superwall/hooks";

export default function Plan() {
  const { host } = useDevice();
  const { getProduct } = useProducts();
  const { purchase } = usePurchase();
  // In an app sell the store product: a Stripe purchase in the iOS app would
  // teleport again, and the Android app can't teleport at all.
  const inApp = host === "ios-sdk" || host === "android-sdk";
  const reference = inApp ? "annual" : "monthly";
  const product = getProduct(reference);

  return (
    <button type="button" onClick={() => void purchase(reference)}>
      {product?.variables.price ? `Subscribe for ${product.variables.price}` : "Subscribe"}
    </button>
  );
}
```

## Where to go next

| The job | Read |
| --- | --- |
| Set up app to web end to end: prerequisites, the paywall, products, the campaign, verifying on a device | [references/setup.md](references/setup.md) |
| Setups and experiments: A/B tests by paywall, web prices and discounts, email before the teleport, failure and abandonment rescue, a custom teleport screen, trial eligibility, `completion`, attribution, and more | [references/experiments.md](references/experiments.md) |
| Anything else about the paywall: routes, `useQueryState`, `useTeleport`, layout, push and publish | the `superwall-framework` skill |
