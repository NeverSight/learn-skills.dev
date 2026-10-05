---
name: shopify-graphql-reference
description: Integrate Shopify-validated Storefront or Customer Account GraphQL into Vercel Shop. Use after Shopify AI Toolkit has supplied and validated an API operation, or when adapting existing GraphQL to the template's operation placement, fragments, domain transforms, locale flow, cache role, invalidation, and route architecture.
---

# Integrate Shopify GraphQL

Treat Shopify AI Toolkit as authoritative for Shopify documentation, schemas, fields, arguments, enum values, API versions, operation design, and validation. This skill owns only the Vercel Shop integration layer.

Read `references/REFERENCE.md` before editing.

## Delegate Shopify facts first

1. Choose the Shopify API:
   - Use Shopify AI Toolkit's Storefront GraphQL skill for catalog, search, menus, cart, and public metaobject reads.
   - Use its Customer skill for profiles, orders, addresses, and other authenticated customer data.
   - Use its custom-data skill first for metafields or metaobjects.
2. Search current Shopify documentation and validate the complete operation with that skill.
3. Do not copy schema snapshots, field catalogs, or generated API reference into this skill.
4. If Shopify AI Toolkit is unavailable, use official Shopify documentation and validation tooling; do not guess.

## Apply the Vercel Shop conventions

1. Inspect the consuming route before choosing cache behavior. Classify the read as static-shell content, request-time shared content, or private/request-scoped data.
2. Add the operation to `lib/shopify/operations/<resource>/server.ts` in the closest resource domain as an uncached `fetch*` function with no `next/cache` import. Put the cache directive, `cacheLife`, and `cacheTag` calls in a `get*` wrapper in the consuming domain's `lib/<domain>/server.ts` (for example `lib/product/server.ts`, `lib/collections/server.ts`, `lib/policies/server.ts`). Keep pure transforms in `lib/shopify/transforms/<resource>/index.ts`, named shared contracts in the owning domain's `types.ts`, and reusable fragment documents in their resource domain. Import implementations and types directly; do not add barrels or forwarding exports.
3. Wrap documents in Hydrogen's `gql()` with a leading `#graphql` comment, keep them static, and use variables for dynamic values. Inference supplies types; Shopify AI Toolkit validates fields and arguments.
4. Reuse the smallest existing fragment that fits by passing it in the `gql(source, [FRAGMENT])` list. Extend a shared fragment only when multiple operations need the same selection.
5. Pass `locale` to `storefront.request` when Shopify localizes the result; never add `country` or `language` to `variables`.
6. Derive raw Shopify types from fragment documents with `ResultOf<typeof FRAGMENT>` under `lib/shopify/**`; transform catalog/account data into domain types before presentation. Cart types intentionally derive from Hydrogen handlers through `lib/cart/types.ts`.
7. Preserve cache tags and the existing webhook invalidation hierarchy. Do not cache mutations.
8. Never place carts in the Next.js data cache; cart reads are memoized per request via `getCart`, so cart mutations need no cache invalidation step.

## Revalidate both boundaries

1. Validate the final GraphQL document again with Shopify AI Toolkit after fragment and variable changes.
2. Run local lint, typecheck, focused tests, and affected commerce flows; run a build when the changed surface requires it. Exercise the operation against the store once; typecheck does not catch invalid fields.
3. Report separately:
   - Shopify validation performed;
   - Vercel Shop cache and route role;
   - domain transform and invalidation changes.

Do not present this skill as a Shopify schema source. Shopify AI Toolkit determines what Shopify supports; this skill determines how validated operations fit Vercel Shop.
