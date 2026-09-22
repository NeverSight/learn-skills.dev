---
name: hydrogen-analytics-tracking
description: "End-to-end analytics & conversion tracking on Shopify Hydrogen — GTM, GA4 (browser + Measurement Protocol), Meta Pixel + CAPI, Google Ads, consent mode, CSP, Oxygen full-page cache. Real-world patterns from production deployments."
---

# Hydrogen Analytics & Tracking — Agent Skill

> Build a complete tracking pipeline on Shopify Hydrogen: client dataLayer → GTM → browser pixels, AND server `/api/track` → GA4 MP / Meta CAPI / Google Ads, with shared `event_id` for cross-side deduplication. Covers consent mode v2, CSP `strict-dynamic`, Oxygen full-page cache compatibility, and the surprising gotchas that bite every implementation.

This skill encodes hard-won lessons from production tracking work on Hydrogen storefronts. The reference files contain detailed implementations; this top page is the map.

---

## When to use this skill

You need this if you're:

- Implementing GA4 / Meta / Google Ads / TikTok tracking on Hydrogen and the default Hydrogen Analytics components aren't enough.
- Adding **server-side tracking** (Measurement Protocol, Conversions API) for resilience against ad-blockers and ITP.
- Debugging "event X is in GTM Preview but not in GA4 / Meta".
- Wiring up **conversion deduplication** between browser pixel and server CAPI.
- Setting up tracking on a Hydrogen storefront with **Weaverse** as the CMS layer.
- Investigating why **Oxygen full-page cache** is being disabled despite a correct `Oxygen-Cache-Control` header.

If you just want page_view + Hydrogen's built-in `<Analytics.Provider>` cart events forwarded to GA4 via GTM, the Shopify docs are enough. Come here when you need the full funnel.

---

## The mental model

### Three layers of tracking

| Layer | Where it runs | Strengths | Weaknesses |
|---|---|---|---|
| **Browser (GTM → pixels)** | `dataLayer.push()` → GTM tags → GA4, Meta Pixel, Google Ads, TikTok | Rich user context, fbp/fbc cookies, instant client-side ECommerce events | ITP, ad-blockers, page-navigation race conditions |
| **Server-side (`/api/track`)** | Hydrogen worker → GA4 MP, Meta CAPI, Google Ads Enhanced Conversions | Survives ad-blockers, runs even when client unloads, can be triggered by webhooks | Loses some context (no fbp without forwarding), needs IP + UA + match keys |
| **Vendor pipes you don't control** | Shopify "Google & YouTube" sales channel app, Shopify Customer Events Pixel | Works inside Shopify checkout (where merchant GTM can't go), Shopify-blessed | Limited customization, can DUPLICATE merchant GTM if same vendor set up twice |

**The combination matters.** A complete pipeline uses all three: GTM for storefront pages, server-side for resilience and dedup, vendor pipes for checkout pages (which Shopify Plus locks down).

### Dual-send + event_id dedup

The cornerstone pattern. Every trackable event:

1. **Generates a UUID `event_id` once** on the client.
2. **Pushes to `dataLayer`** with that `event_id` → GTM → browser pixels send the hit with `event_id` as the dedup key.
3. **POSTs to `/api/track`** via `navigator.sendBeacon` with the same `event_id` → server forwards to GA4 MP / Meta CAPI / Google Ads with the same key.
4. Each vendor's backend dedupes on `(event_name, event_id)` → exactly one count, not two.

```ts
function trackEvent({ event_name, custom_data, user_data }) {
  const event_id = crypto.randomUUID();

  // (1) Browser side
  window.dataLayer.push({ event: event_name, event_id, ...custom_data });

  // (2) Server side, same event_id
  const payload = { event_id, event_name, custom_data, user_data, consent };
  navigator.sendBeacon("/api/track", new Blob([JSON.stringify(payload)]));

  return event_id;
}
```

### Why sendBeacon, why not fetch?

Add-to-cart, begin_checkout, "Buy now" — these all trigger page navigation immediately after. A regular `fetch()` gets cancelled when the page unloads, losing the event. `sendBeacon` is the browser API designed exactly for this: the request is queued by the browser and guaranteed to be sent even after navigation. Fall back to `fetch(..., {keepalive: true})` if sendBeacon isn't available.

### Why event_id can't come from the server

If the server generates `event_id`, the browser already pushed its dataLayer event with a *different* (or no) id, and there's no way to backfill. Always generate client-side, send both directions with the same value.

---

## Experiment exposure (A/B tests)

A/B tests on a Weaverse storefront use [`@weaverse/experiments`](https://www.npmjs.com/package/@weaverse/experiments) — deterministic, project-level variant assignment. Exposure rides the **same** pipeline as every other event:

- **Segment downstream events by variant.** Pass the resolved assignments to `<Analytics.Provider customData={{ experiments: { '<id>': '<variant>' } }}>`. `customData` is merged into every event, so `add_to_cart` / `purchase` are already tagged with the variant — this is what measures conversion *impact*, not just impressions. No need to re-attach the experiment per event.
- **Fire an impression event.** Call `useAnalytics().publish('custom_experiment_viewed', { experimentId, variantId })` from the experiments `onExpose` callback, gated on `canTrack()`. Bridge `custom_experiment_viewed` → dataLayer/GA4 in your `<CustomAnalytics>` subscriber like any other custom event (`custom_` prefix required; call `ready()`).
- **Dedup.** Exposure is an impression, not a conversion, so the `event_id` dual-send is usually unnecessary. If you forward it to `/api/track`, reuse the storefront `trackEvent()` helper.

Server-side `getExperiments()` wiring lives in the `weaverse-hydrogen` skill (Multi-Project Architecture → A/B Testing).

---


## Reference files

Read these in order if you're implementing from scratch. Skip to the relevant one if you're debugging:

| Reference | Read if you're… |
|---|---|
| [`architecture.md`](./references/architecture.md) | Setting up the whole pipeline. Covers the dual-send pattern, dedup contract, vendor responsibilities, and how the pieces fit together. |
| [`gtm-meta-implementation.md`](./references/gtm-meta-implementation.md) | Wiring up GTM dataLayer pushes, GA4 Event tags, Meta CAPI forwarder. Real code patterns. |
| [`webhook-forwarding-via-builder.md`](./references/webhook-forwarding-via-builder.md) | **Weaverse-hosted storefronts:** how Shopify webhooks reach your storefront without leaking the multi-tenant app client secret. Uses the builder `WebhookForward` model + per-store signing secrets. |
| [`cart-attribute-stash.md`](./references/cart-attribute-stash.md) | Bridging the **webhook cookie gap**: how to get `_fbp` / `_fbc` / `gclid` / affiliate click IDs from the browser into the Shopify orders webhook. Covers the two cart entry paths (POST action AND `/cart/<id>:<qty>` loader) that both need stash logic. |
| [`oxygen-full-page-cache.md`](./references/oxygen-full-page-cache.md) | Configuring FPC, why `Set-Cookie` disables it, the `entry.server.tsx` strip trick. |
| [`csp-for-tracking.md`](./references/csp-for-tracking.md) | CSP directives that allow Google/Meta/Hotjar; nonce vs strict-dynamic; GTM Custom HTML tags and inline-script violations. |
| [`gotchas.md`](./references/gotchas.md) | The bugs that bite every implementation. Read this first if something isn't working. |

---

## Five things every Hydrogen tracking implementation gets wrong

1. **Using Hydrogen's `PRODUCT_ADD_TO_CART` analytics event for `add_to_cart`.** Hydrogen diffs cart state after revalidation and emits the event then. The timing is unreliable — events often miss GA4 DebugView entirely. **Fix:** fire `add_to_cart` directly from the button onClick handler via `sendBeacon` (it survives the form submit / navigation).

2. **Loading GTM after hydration via `<Script waitForHydration>`.** It hides GTM from Tag Assistant standalone scans and blocks the move to nonce-based `strict-dynamic` CSP. **Fix:** load `gtm.js` as a regular `<script async nonce={nonce}>` in `<head>`, with the inline `gtm.start` + Consent Mode v2 default-deny block before it.

3. **Pushing GA4-named events but configuring GTM triggers with legacy snake_case names** (or vice versa). After "Custom Event" renaming there's a coverage gap. **Fix:** match GTM trigger filters to whatever the storefront actually pushes today; do code + GTM in one coordinated change.

4. **Letting `<Analytics.ProductView>` gate on `selectedVariant`.** For combined listings or any product where the variant resolves after hydration, the analytics component never mounts and `view_item` doesn't fire. **Fix:** mount unconditionally with safe per-variant fallbacks.

5. **Treating "consent denied" as "send nothing".** Meta CAPI's relaxed pattern (LDU flag + ip/ua/fbp/fbc only, no hashed PII) recovers a large chunk of optimisation signal compliantly. GA4 Consent Mode v2 modeled conversions work the same way. **Fix:** in the server forwarder, when `ad_storage !== "granted"` drop hashed PII but still send the event with `data_processing_options: ["LDU"]`.

6. **Pasting a Liquid `dataLayer.push` snippet into Hydrogen.** Merchants often bring an existing theme snippet using Liquid tags (`{{ product.id }}`, `{{ collection.title }}`, `{{ product.price | money_without_currency }}`). **These do nothing in Hydrogen** — it's React/SSR, there is no Liquid at runtime, so the braces render as literal text or break. **Fix:** rebuild the same object from Hydrogen data and push it in JS. Liquid → Hydrogen mapping: `{{ product.id }}` → `product.id`, `{{ product.title }}` → `product.title`, `{{ product.price | money_without_currency }}` → `product.priceRange?.minVariantPrice?.amount` (a string, no currency symbol), `{{ collection.id/title }}` → `collection.id/title`.

7. **Expecting `select_item` / `view_item_list` from a built-in Hydrogen analytics event.** GA4 list events don't map to cart events. `select_item` is a **click** (user clicks a product card in a list) — fire it from the product card's `onClick` on the collection/PLP, where you already hold the product + collection + index. `view_item_list` is a **view** — push it from the `COLLECTION_VIEWED` subscriber in `app/components/root/custom-analytics.tsx`. Include `index` (list position) for GA4. Ensure the collection query returns `id`, `title`, `handle`, and `priceRange` so the values exist to push.

---

## The order to build it

If you're starting fresh on a new Hydrogen storefront:

1. **Hydrogen `<Analytics.Provider>` wired at root.** Subscribe to its events in a `<CustomAnalytics />` component. (See [`architecture.md`](./references/architecture.md))
2. **Inline `<head>` Consent Mode v2 default-deny block + dataLayer + gtm.start marker.**
3. **`gtm.js` external script with nonce, async, in `<head>` after the inline block.**
4. **`trackEvent()` helper** that pushes dataLayer + `sendBeacon('/api/track')` with shared `event_id`.
5. **`/api/track` server endpoint** that validates the payload, hashes PII server-side, fans out to GA4 MP + Meta CAPI + Google Ads forwarders.
6. **Shopify `orders/create` webhook** that maps the order to a `purchase` event with `event_id = "purchase_" + orderId` (deterministic for retries).
7. **Shopify "Google & YouTube" sales channel + Customer Events Pixel** for checkout-side events (Meta Pixel events, anything that needs to fire inside Shopify checkout where your GTM can't reach).
8. **GTM container** with one GA4 Event tag per dataLayer event, plus Meta Pixel + TikTok + Google Ads conversion tags as needed.
9. **CSP** updated to allow all vendor domains in `script-src`, `connect-src`, `img-src`. Use `strict-dynamic` + nonce.
10. **Oxygen full-page cache** opted in per route via `Oxygen-Cache-Control: public, max-age=N, ...` header. Strip `Set-Cookie` from cacheable responses in `entry.server.tsx`.

---

## Skill-level conventions

When working on a Hydrogen tracking implementation in this skill's scope:

- **Server code lives under `app/.server/tracking/`** (forwarders, validators, hash util, audit log).
- **Client helper at `app/utils/track-client.ts`** (exports `trackEvent`, consent listener, attribution capture).
- **dataLayer bridge at `app/components/root/custom-analytics.tsx`** (subscribes to Hydrogen `<Analytics.Provider>` events).
- **Inline Consent Mode + GTM bootstrap in `app/root.tsx` `<head>`**, with nonce.
- **CSP config at `app/weaverse/csp.ts`** (Weaverse projects) or wherever your storefront sets CSP.
- **Per-vendor forwarder modules at `app/.server/tracking/forwarders/{ga4,meta-capi,google-ads}.ts`** — each returns `{forwarder, ok, skipped?, reason?}` so the audit log can show why an event was dropped.

When a question is broader than a single vendor, prefer the reference doc that addresses the architectural layer rather than one vendor's docs.

---

## Live docs

Run these from this skill's own folder. The helpers ship inside the sibling
`shopify-hydrogen` skill, so `../shopify-hydrogen/scripts/` exists whenever the
whole pack is installed.

If you installed this skill on its own, that folder is absent and the commands
below fail with `MODULE_NOT_FOUND`. Add the helpers once:

```bash
npx skills add Weaverse/shopify-hydrogen-skills --skill shopify-hydrogen
```

The `references/` files in this skill remain a usable offline fallback if you
would rather not install it.

For up-to-date official sources:

```bash
# Shopify Hydrogen / Oxygen
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "oxygen full-page cache"
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "consent mode"
node ../shopify-hydrogen/scripts/search_shopify_docs.mjs "analytics provider"

# Weaverse (if using Weaverse CMS)
node ../shopify-hydrogen/scripts/search_weaverse_docs.mjs "csp"
```

Vendor docs (open in browser, no script):
- GA4 Measurement Protocol — https://developers.google.com/analytics/devguides/collection/protocol/ga4
- Meta Conversions API — https://developers.facebook.com/docs/marketing-api/conversions-api
- Google Ads Enhanced Conversions for Web — https://developers.google.com/google-ads/api/docs/conversions/enhanced-conversions-for-web
- Shopify "Customer Events" / Web Pixels — https://shopify.dev/docs/api/web-pixels-api
