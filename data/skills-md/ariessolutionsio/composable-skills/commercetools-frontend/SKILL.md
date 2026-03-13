---
name: commercetools-frontend
description: Production-tested patterns for commercetools storefronts — Next.js, React, PDP/PLP, cart, checkout, SEO, and performance from a Platinum partner with 50+ live implementations.
---

# commercetools Frontend & Storefront Development

## Two Development Paths

This skill covers **two distinct approaches** to building storefronts on commercetools:

| Approach | When to Use | Key File |
|----------|-------------|----------|
| **commercetools Frontend** (hosted) | Using Studio for business users, extensions, components (tastics), data sources | [references/ct-frontend-extensions.md](references/ct-frontend-extensions.md) |
| **Headless with Next.js/React** | Custom storefront with full control, App Router, Server Components | [references/storefront-architecture.md](references/storefront-architecture.md) |
| **B2B Storefront** | Business units, permissions, approval workflows, quotes, purchase lists | [references/b2b-frontend.md](references/b2b-frontend.md) |

Both approaches share patterns for product pages, cart/checkout UI, and performance/SEO. B2B patterns layer on top of either approach.

## How to Use This Skill

1. Identify which approach you are using (commercetools Frontend or headless Next.js)
2. Load the relevant architecture file first
3. Then load the page-type-specific reference for your current task
4. Reference files contain correct/incorrect code pairs, checklists, and pitfall warnings

**Progressive loading -- only load what you need:**

- Using commercetools Frontend extensions, data sources, actions? Load `references/ct-frontend-extensions.md`
- Using commercetools Frontend components, Studio, renderer? Load `references/ct-frontend-components.md`
- Building a headless Next.js storefront? Load `references/storefront-architecture.md`
- Building product listing pages (PLP, filtering, pagination)? Load `references/product-listing-pages.md`
- Building product detail pages (PDP, variants, product cards)? Load `references/product-detail-pages.md`
- Building cart UI? Load `references/cart-ui.md`
- Building checkout flows? Load `references/checkout-ui.md`
- Optimizing frontend performance (images, LCP, code splitting)? Load `references/frontend-performance.md`
- Optimizing SEO (structured data, meta tags, sitemap)? Load `references/frontend-seo.md`
- Building a B2B storefront (business units, quotes, approvals)? Load `references/b2b-frontend.md`

## CRITICAL Priority

| Pattern | File | Impact |
|---------|------|--------|
| Data fetching strategy (SSR vs SSG vs ISR) | [references/storefront-architecture.md](references/storefront-architecture.md) | Wrong strategy causes stale prices, slow pages, or API quota exhaustion |
| Cart state management & optimistic updates | [references/cart-ui.md](references/cart-ui.md) | Race conditions cause quantity bugs, lost items, broken checkout |
| Extension timeout limits (8s max) | [references/ct-frontend-extensions.md](references/ct-frontend-extensions.md) | Slow extensions fail silently, breaking pages for all users |
| Image optimization & LCP | [references/frontend-performance.md](references/frontend-performance.md) | Unoptimized product images destroy Core Web Vitals scores |
| B2B permission-gated UI | [references/b2b-frontend.md](references/b2b-frontend.md) | Missing permission checks expose admin actions to unauthorized users |

## HIGH Priority

| Pattern | File | Impact |
|---------|------|--------|
| Server Components for product data | [references/storefront-architecture.md](references/storefront-architecture.md) | Client-side fetching leaks API credentials and doubles load time |
| PLP pagination & filtering | [references/product-listing-pages.md](references/product-listing-pages.md) | N+1 queries on listing pages cause 3-10s load times |
| Checkout flow & payment integration | [references/checkout-ui.md](references/checkout-ui.md) | Missing error states cause silent payment failures |
| Component schema design (tastics) | [references/ct-frontend-components.md](references/ct-frontend-components.md) | Bad schemas make components unusable for business users in Studio |
| SEO structured data for products | [references/frontend-seo.md](references/frontend-seo.md) | Missing structured data means no rich results in Google |
| Locale routing & currency formatting | [references/storefront-architecture.md](references/storefront-architecture.md) | Wrong i18n setup breaks prices, URLs, and search indexing |
| B2B quote lifecycle & approval flows | [references/b2b-frontend.md](references/b2b-frontend.md) | Quote cart consumption and approval rejection side effects break B2B checkout |

## MEDIUM Priority

| Pattern | File | Impact |
|---------|------|--------|
| Product variant selection UI | [references/product-detail-pages.md](references/product-detail-pages.md) | Confusing variant selectors reduce conversion |
| Faceted search UI patterns | [references/product-listing-pages.md](references/product-listing-pages.md) | Slow or broken filters frustrate shoppers |
| commercetools Checkout integration | [references/checkout-ui.md](references/checkout-ui.md) | Misconfigured Checkout SDK blocks payment completion |
| Code splitting & bundle size | [references/frontend-performance.md](references/frontend-performance.md) | Oversized bundles increase Time to Interactive |
| Data source extension patterns | [references/ct-frontend-extensions.md](references/ct-frontend-extensions.md) | Redundant API calls from multiple components on a page |
| Studio page management & publishing | [references/ct-frontend-components.md](references/ct-frontend-components.md) | Wrong page folder structure breaks dynamic routing |
| B2B business unit & store scoping | [references/b2b-frontend.md](references/b2b-frontend.md) | Missing BU/store context causes cross-tenant data leaks |
| B2B purchase lists & quick order | [references/b2b-frontend.md](references/b2b-frontend.md) | Wrong Wishlist API mapping breaks purchase list CRUD |

## Common Frontend Anti-Patterns (Quick Reference)

| Anti-Pattern | File | Consequence |
|-------------|------|-------------|
| Fetching product data client-side | [references/storefront-architecture.md](references/storefront-architecture.md) | Exposes API credentials, no SSR benefits, poor SEO |
| Using `getServerSideProps` for static catalog pages | [references/storefront-architecture.md](references/storefront-architecture.md) | Every page visit hits the API, wastes quota, slow TTFB |
| Not implementing optimistic cart updates | [references/cart-ui.md](references/cart-ui.md) | UI freezes on every add-to-cart, feels broken |
| Loading all product images at full resolution | [references/frontend-performance.md](references/frontend-performance.md) | 5-10MB page weight, failed Core Web Vitals |
| Fetching all product attributes when you need 3 | [references/product-detail-pages.md](references/product-detail-pages.md) | 5-10x response payload, slower rendering |
| Building search from scratch instead of using Product Search API | [references/product-listing-pages.md](references/product-listing-pages.md) | Poor relevance, no faceting, slow queries |
| Missing error boundaries around commerce data | [references/storefront-architecture.md](references/storefront-architecture.md) | One failed API call crashes the entire page |
| Hardcoding locale/currency instead of using routing | [references/storefront-architecture.md](references/storefront-architecture.md) | Broken multi-market support, wrong prices |

## MCP Complement

Use this skill for storefront patterns, then use the [Developer MCP](https://docs.commercetools.com/sdk/mcp/developer-mcp) to look up field names and schemas, and the [Commerce MCP](https://docs.commercetools.com/sdk/mcp/commerce-mcp) for CRUD operations.
