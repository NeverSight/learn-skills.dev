---
name: shopify-hydrogen
description: "Core Shopify Hydrogen APIs — createHydrogenContext, cart handler, CartForm, caching strategies, pagination, SEO, variant selection, analytics, and CSP."
---

# Shopify Hydrogen

Hydrogen is Shopify's opinionated stack for headless commerce, built on React Router v7. It provides utilities, handlers, and components for building storefronts on top of the Shopify Storefront API.

**All exports come from `@shopify/hydrogen`**, which re-exports everything from `@shopify/hydrogen-react`.

> Source: https://github.com/Shopify/hydrogen/tree/main/packages/hydrogen/src

## Live Documentation

Run these from this skill's own folder; the paths below are relative to the skill root.

For the most up-to-date Hydrogen API docs, use the search script:

```bash
node scripts/search_shopify_docs.mjs "<query>"
```

This queries Shopify's developer docs (`shopify.dev`) directly and returns the latest API references, code examples, and guides for Hydrogen.

**Examples:**
```bash
node scripts/search_shopify_docs.mjs "createHydrogenContext"
node scripts/search_shopify_docs.mjs "CartForm actions"
node scripts/search_shopify_docs.mjs "caching strategies"
node scripts/search_shopify_docs.mjs "getSeoMeta"
node scripts/search_shopify_docs.mjs "Pagination component"
```

For offline/cached reference, see the [references/](#references) folder below.

---

## Key Concepts (Quick Reference)

### createHydrogenContext

The single entry point to set up all Hydrogen services in `server.ts`. Creates and wires together `storefront`, `customerAccount`, and `cart`.

- Required env vars: `PUBLIC_STORE_DOMAIN`, `PUBLIC_STOREFRONT_API_TOKEN`, `PRIVATE_STOREFRONT_API_TOKEN`, `PUBLIC_STOREFRONT_ID`, `PUBLIC_CUSTOMER_ACCOUNT_API_CLIENT_ID`, `SHOP_ID`
- Returns: `{ storefront, customerAccount, cart }`

### Caching Strategies

| Strategy | maxAge | staleWhileRevalidate | Use for |
|----------|--------|----------------------|---------|
| `CacheNone()` | — | — | User-specific or real-time data |
| `CacheShort()` | 1s | 9s | Frequently changing data |
| `CacheLong()` | 1hr | 23hr | Stable data (shop info, menus) |
| `CacheCustom({...})` | custom | custom | Fine-grained control |

### Cart Handler

`createCartHandler` provides all cart operations: `get`, `create`, `addLines`, `updateLines`, `removeLines`, `updateDiscountCodes`, `addGiftCardCodes`, `updateBuyerIdentity`, `updateNote`, `setMetafields`, and more.

### CartForm

Form component for cart mutations. Uses `CartForm.ACTIONS` enum (`LinesAdd`, `LinesUpdate`, `LinesRemove`, `DiscountCodesUpdate`, etc.) and submits via React Router's `useFetcher`.

### useOptimisticCart

Applies pending cart mutations locally for instant UI feedback. Requires `selectedVariant` in `LinesAdd` inputs.

### Pagination

`getPaginationVariables(request, { pageBy })` + `<Pagination connection={...}>` component. GraphQL query must include `pageInfo { hasPreviousPage hasNextPage startCursor endCursor }`.

### SEO

`getSeoMeta(...)` generates React Router `meta` arrays. Supports `title`, `titleTemplate`, `description`, `url`, `media`, `jsonLd`, `robots`, `alternates`. `jsonLd` is concatenated across routes.

### Sitemaps

`getSitemapIndex` + `getSitemap` — two-level sitemap generation. Requires Storefront API 2024-10+.

### Content Security Policy

`createContentSecurityPolicy({ shop: { checkoutDomain, storeDomain } })` returns `{ nonce, header, NonceProvider }`.

---

## References

For offline/cached reference when the search script is unavailable:

| File | Contents |
|------|----------|
| [references/01-setup.md](references/01-setup.md) | Full `server.ts` setup, env vars, session, `createHydrogenContext` options |
| [references/02-caching.md](references/02-caching.md) | Cache strategies, `AllCacheOptions` type, `generateCacheControlHeader` |
| [references/03-cart.md](references/03-cart.md) | Cart route setup, `CartForm` examples, `useOptimisticCart` patterns |
| [references/04-ssr-performance.md](references/04-ssr-performance.md) | SSR bundle diet (worker inlines dynamic imports — `resolveId` stub pattern), bundle audit, TTFB measurement methodology |
