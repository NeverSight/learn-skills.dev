---
name: build-shop
description: Build or adapt a Shopify storefront with Vercel Shop source-backed patterns. Use when creating, redesigning, refactoring, or reviewing storefront routes, commerce data, rendering, caching, streaming, navigation, cart, account, mutations, product cards, media, loading states, or when applying Vercel Shop outside the template.
---

# Build with Vercel Shop

Build the shop around commerce truth first: what product or collection is being shown, what the customer has selected, what can be bought now, what price is authoritative, and what state belongs in the URL, Shopify, the server cache, or the browser. Use Vercel Shop's template as the reference implementation, but adapt the behavior to the current storefront instead of copying files blindly.

## Ground the work in source

1. Read the project's `AGENTS.md`, the target route, its view contract, and every operation it calls.
2. If the Vercel Shop template source is available, inspect it before relying on this prose:
   - Template rules: `AGENTS.md`
   - Route/layout shell: `app/layout.tsx`, `app/page.tsx`
   - Shopify boundary: `lib/shopify/storefront/server.ts`, `lib/shopify/operations/`, `lib/shopify/transforms/`, `lib/product/types.ts`, `lib/customer/types.ts`
   - Next.js cache boundary: `lib/<domain>/server.ts` cached `get*` wrappers around the uncached `fetch*` operations
   - Shared UI layout primitives: `components/ui/container.tsx`, `components/ui/page.tsx`, `components/ui/sections.tsx`
   - Public source fallback: [template source](https://github.com/vercel/shop)
3. Use the docs to orient before editing unfamiliar areas:
   - [Documentation index](https://vercel.shop/llms.txt)
   - [Route reference](https://vercel.shop/docs/reference/routes)
   - [Shopify integration docs](https://vercel.shop/docs/shopify)
   - [API boundary docs](https://vercel.shop/docs/reference/storefront-api)
4. Read the local Next.js documentation under `node_modules/next/dist/docs/` for any API being changed. This template may use newer Cache Components and prefetch behavior than model knowledge.
5. Preserve existing cache directives, promises, invalidation tags, auth gates, redirects, metadata, and `notFound()` behavior unless the task explicitly changes the domain behavior.

## Hydrogen ownership

The template uses the framework-agnostic Hydrogen preview SDK, not Hydrogen's React Router application framework. Next.js owns routing, rendering, public-data caching, and invalidation. Hydrogen owns commerce state and protocols; the template supplies presentation and framework adapters. Use Hydrogen's cart provider/forms/handlers rather than rebuilding cart state or hydration. Cart types are handler-derived; catalog/account presentation uses domain transforms. Read the installed SDK guidance and verify adapter behavior before changing these boundaries.

## Organize code by domain and execution context

Organize `lib/` by domain, then use only the context files that domain needs:

- `index.ts` contains universal implementation safe for server and client imports; it is never a re-export barrel.
- `server.ts` contains server-side implementation; keep it out of client import graphs.
- `request.ts` contains code that takes the `Request` or `Headers` explicitly, such as Hydrogen handlers and session cookies; the root `proxy.ts` and Route Handlers import it. It never imports `next/cache`, `next/headers`, `next/navigation`, or `react`, which load the App Router runtime into the proxy; `server.ts` may import it.
- `client.ts` is a `"use client"` boundary for browser interaction, not an HTTP transport wrapper.
- `action.ts` is a `"use server"` entry point whose exports use a verb plus `Action` suffix. Server Actions are public endpoints: each export parses every argument with a module-private `zod` schema, `z.strictObject` for objects, before any other work, and returns its usual failure result when parsing fails.
- `types.ts` owns named shared contracts; consumers import types directly rather than through `server.ts` or `action.ts`.

Subdivide large domains with the same context filenames. Put Shopify transports in their API domain's `server.ts` and pure transforms in `index.ts`, even when all current callers run on the server. Do not add descriptive sibling files, flat root implementation modules, empty entry points, forwarding exports, or barrels.

Keep storefront models in their owning domain's `types.ts`, such as `lib/product/types.ts`, `lib/collections/types.ts`, and `lib/customer/types.ts`. Shared use does not change ownership: primitives live in `lib/money/types.ts`, `lib/media/types.ts`, and `lib/pagination/types.ts`. Types-only domains need no `index.ts` or re-export barrel. Keep SDK-specific contracts under `lib/shopify/` and handler-derived cart contracts in `lib/cart/types.ts`. Component props stay with their component; small private implementation types may stay local. Generated artifacts keep generator-owned paths and names.

## Copy and deployment defaults

The default storefront uses inline component copy and reusable content functions in `lib/content/index.ts`. Keep copy server-first, pass primitive labels to UI primitives and client leaves, and keep interactive copy in its consuming leaf and import shared content functions only when needed. Do not add a custom `t()` parser, a full browser catalog, or next-intl for a single deployment.

`shopConfig.localization` explicitly sets `{ country: "US", language: "EN", locale: "en-US" }`; country/language configure commerce requests and locale configures formatting. Currency comes from Shopify. Clean URLs and one deployment are the default; `lib/i18n/` and a Server Component locale resolver are absent. Operation locale/cache inputs may still be intentional. Preserve existing next-intl, catalogs, localized routes, and custom commerce behavior in upgraded installations. Use `enable-i18n` for copy/routing or `enable-shopify-markets` for regional commerce rather than coupling the two implicitly.

## Shop Agent boundaries

Shop Agent, customer authentication, and BotID are disabled by default. Preserve the installation's feature settings; a storefront redesign or localization change must not enable them implicitly.

For assistant changes, read the installed Eve docs starting at `node_modules/eve/docs/README.md`, then only the guide relevant to the task. Preserve Next.js deployment through `withEve` and the conditional plugin list passed to `withShopConfig` in `next.config.ts`.

Eve owns `/eve/v1/*`. Next.js prepares the browser cart through `/api/agent/session`; do not add another chat route or internal commerce HTTP bridge. Tool schemas and execution belong in `agent/tools/`, shared execution helpers in `agent/lib/`, and browser state, presentation helpers, and shared result types in `lib/agent/`. Keep Next.js request/cache APIs out of Eve's runtime imports. Use shared uncached catalog operations and Hydrogen cart handlers directly, with cart identity bound from the browser cookie rather than model arguments.

Preserve confirmed-mutation signals and Hydrogen reconciliation; restored messages must not replay cart writes or reopen the drawer. Do not claim exactly-once writes, conversation ownership, or server-history deletion on Clear. For conversation changes, check multiple search turns, visible results, and cumulative usage. For session controls, check restoration, Stop/Clear recovery, and failures. Mitigate abuse and cost with BotID, rate limits, and Gateway spending controls rather than per-session token caps. Distinguish browser/live-store evidence from mocks and build checks.

## Route the work

Read `references/rendering-architecture.md` for every route. Then read only the route references that apply:

- Commerce behavior and end-to-end flows: `references/commerce-flows.md`
- Home and marketing routes: `references/home.md`
- Collection and search routes: `references/plp-search.md`
- Product routes: `references/pdp.md`
- Cart and authenticated account routes: `references/cart-account.md`
- Cart provider, bootstrap, optimistic state, and mutations: `references/cart-provider.md`

## Model the route

Write down the route as five layers before editing, using commerce nouns instead of generic component names:

1. **Route orchestration** — resolve handles, locale, selected options, filters, pagination, redirects, metadata, auth, and real 404s.
2. **Data operation** — fetch Shopify data, transform provider types into shop domain types, and own cache scope, tags, and invalidation names.
3. **Server composition** — render the stable catalog shell first and place independent sections like recommendations, facets, reviews, and account/cart details behind granular boundaries.
4. **Client island** — own only selection, optimistic intent, browser APIs, effects, and event handlers: variant pickers, galleries, filter controls, carts, and forms.
5. **Mutation boundary** — use server actions, which parse their input with a `zod` schema first, for app-owned mutations and Hydrogen's proxy handlers for browser cart mutations. Return canonical Shopify state and warnings; invalidate public domain caches only when applicable. Let Hydrogen reconcile cart state without a parallel optimistic reducer.

For each layer's full ownership boundary, see the responsibility table in `references/rendering-architecture.md`. For every dependency, classify it as cacheable shell content, request-time shared content, request-time personalized content, or client-only state. Draw an edge only when one result genuinely requires another. Start all other work concurrently.

## Storefront gotchas

- Product selection must round-trip through direct visits, links, refreshes, and client navigation, then drive media, price, availability, add-to-cart payloads, and canonical links.
- Collection/search URLs are the source of truth for browsing. Empty results, unavailable facets, and back/forward navigation are not optional states.
- Cart UI must keep confirmed Shopify state separate from pending optimistic intent so concurrent mutations, bootstrap, errors, and warnings cannot double-apply or disappear.
- Customer, account, cart identity, and authorization state must never leak into shared product, collection, menu, page, or recommendation caches.
- Missing images, deleted products, sold-out variants, empty collections, partial Shopify failures, and disabled auth are normal storefront cases. Represent them deliberately.

## Keep the Shopify boundary explicit

Use the installed Shopify AI Toolkit for Shopify API documentation, schema facts, operation design, and validation. Invoke its API-specific skill before adding or changing Storefront or Customer Account GraphQL. For metafields or metaobjects, use its custom-data skill first.

Use `shopify-graphql-reference` only after Shopify validation to apply Vercel Shop conventions: operation placement, domain transforms, cache role, locale flow, invalidation, and route integration. Never treat this architecture skill as a substitute for authoritative Shopify validation.

Shopify returns rich text (`body`, `contentHtml`, `descriptionHtml`) as staff and apps saved it. Pass it through `sanitizeShopifyHtml` from `lib/shopify/html/server.ts` in the `fetch*` operation that returns it, and render it only under an `oxlint-disable-next-line react/no-danger` directive that names the sanitizer, such as `-- Product descriptions pass through sanitizeShopifyHtml when fetched.`

## Prevent blocking

1. Keep route identity, stable headings, primary media, selected price/availability, and likely LCP content in the earliest shell the data contract permits.
2. Resolve route identity early only when it is required for correctness or shell coherence.
3. Pass request-dependent promises downward unawaited. Resolve them in the smallest component that needs them and place Suspense there.
4. Use sibling boundaries for independent work. Do not put the whole page behind the slowest Shopify request.
5. Give every visible fallback the same outer geometry as its resolved content.
6. Keep components server-rendered by default. Do not move reads into client effects or internal HTTP endpoints.
7. Keep cache policy in the data layer and personalized data out of shared caches.
8. Treat prefetching as a traffic-versus-latency decision, not a default fix for blocking architecture.

## Use a browser feedback loop

For visible storefront changes, close the loop in a real browser before calling the work done. Use the agent's built-in browser when available; otherwise use the standalone `agent-browser` CLI.

1. Start the local storefront and open each affected route: `agent-browser open http://localhost:3000/...`.
2. Capture the current state: `agent-browser wait --load networkidle`, `agent-browser snapshot`, and `agent-browser screenshot --full`.
3. Exercise the commerce interaction through the UI: variant selection, filtering, pagination, add/update/remove cart, auth redirects, or the changed control.
4. Re-snapshot after every navigation or DOM change before reusing element refs.
5. Repeat on mobile and desktop viewports when layout, media, overlays, filters, cart, or primary actions changed.
6. Iterate on the implementation until the browser outcome matches the intended commerce behavior. If `agent-browser` is unavailable, say so and report the fallback checks used.

## Verify the architecture

Run the static hotspot scan from the skill directory:

```bash
node scripts/audit-storefront.mjs <storefront-root>
```

Treat its output as review prompts, not measurements. Then:

1. Run targeted lint, typecheck, tests, and affected flows available in the current environment.
2. Test direct visits, client navigations, back/forward navigation, and URL round-trips for the routes changed.
3. Verify that non-critical Shopify work does not delay the shell, primary media, selected price/availability, or primary interaction.
4. Run every affected flow in `references/commerce-flows.md`, including failure, empty, sold-out, and missing-media states.
5. Inspect failed requests, layout shifts, LCP discovery, hydration, and interaction behavior when relevant.
6. Require a production build only when build, prerendering, caching, bundling, deployment behavior, or release readiness is in scope.
7. Use bundle analysis or deployed field data only for an explicit performance investigation when those tools and data are available. Do not request them as routine completion work or claim measured improvement from code inspection.

Report the final layer boundaries, blocking dependencies, cache ownership, and remaining risks.
