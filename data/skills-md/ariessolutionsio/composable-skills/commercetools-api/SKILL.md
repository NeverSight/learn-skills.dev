---
name: commercetools-api
description: Production-tested patterns for commercetools cart/checkout, orders, payments, B2B, promotions, extensions, and subscriptions from a Platinum partner with 50+ live implementations.
---

# commercetools API Development

**Progressive loading — only load what you need:**

- Setting up the SDK or client? Load `references/sdk-setup.md`
- Building cart or checkout? Load `references/cart-checkout.md`
- Working with orders? Load `references/order-management.md`
- Managing customers? Load `references/customer-management.md`
- Setting up extensions or subscriptions? Load `references/extensions-subscriptions.md`
- Implementing discounts? Load `references/promotions-pricing.md`
- Building B2B features? Load `references/b2b-patterns.md`
- Implementing search? Load `references/search-discovery.md`
- Optimizing performance? Load `references/performance.md`
- Code review or debugging? Load `references/anti-patterns.md`

**MUST load the relevant reference file** before writing commercetools API code. For SDK client setup, always start with `references/sdk-setup.md`.

## CRITICAL Priority

| Pattern | File | Impact |
|---------|------|--------|
| Optimistic concurrency & version handling | [references/sdk-setup.md](references/sdk-setup.md) | Every update/delete fails without correct version tracking |
| Cart lifecycle & freeze before payment | [references/cart-checkout.md](references/cart-checkout.md) | Price changes during checkout cause order failures |
| Payment flow — never reuse/delete Payments | [references/cart-checkout.md](references/cart-checkout.md) | Lost audit trail, double charges, PSP inconsistencies |
| Extension timeout constraints (2s / 10s) | [references/extensions-subscriptions.md](references/extensions-subscriptions.md) | Entire API call fails on timeout — affects all clients |
| Discount stacking & sort order | [references/promotions-pricing.md](references/promotions-pricing.md) | Unexpected pricing, revenue loss, customer complaints |
| Direct Discounts block Discount Codes | [references/promotions-pricing.md](references/promotions-pricing.md) | Codes silently stop working when Direct Discounts exist |

## HIGH Priority

| Pattern | File | Impact |
|---------|------|--------|
| Client setup & auth flows | [references/sdk-setup.md](references/sdk-setup.md) | Wrong setup causes auth failures and token leaks |
| Order state machines & returns | [references/order-management.md](references/order-management.md) | Invalid state transitions, incomplete fulfillment |
| Customer auth & email verification | [references/customer-management.md](references/customer-management.md) | Broken sign-up/login, unverified accounts |
| Subscription idempotency & ordering | [references/extensions-subscriptions.md](references/extensions-subscriptions.md) | Duplicate side effects, stale data overwrites |
| Business unit hierarchies & permissions | [references/b2b-patterns.md](references/b2b-patterns.md) | Security gaps, broken approval workflows |
| Product Search API vs Query API | [references/search-discovery.md](references/search-discovery.md) | 10-100x slower queries on large catalogs |
| N+1 queries & reference expansion | [references/performance.md](references/performance.md) | Cascading latency on listing pages |

## MEDIUM Priority

| Pattern | File | Impact |
|---------|------|--------|
| Tax mode configuration | [references/cart-checkout.md](references/cart-checkout.md) | Failed order creation from incomplete tax data |
| Approval rules & quote lifecycle | [references/b2b-patterns.md](references/b2b-patterns.md) | Blocked B2B purchasing workflows |
| Connect application patterns | [references/extensions-subscriptions.md](references/extensions-subscriptions.md) | Deployment failures, resource constraint issues |
| Pagination & query optimization | [references/performance.md](references/performance.md) | Slow page loads, unnecessary API load |
| Customer groups & address management | [references/customer-management.md](references/customer-management.md) | Wrong pricing tiers, address data issues |
| Faceting & search performance | [references/search-discovery.md](references/search-discovery.md) | Slow search responses, poor relevance |

## Common Anti-Patterns (Quick Reference)

| Anti-Pattern | File | Consequence |
|-------------|------|-------------|
| Creating a client per request | [references/anti-patterns.md](references/anti-patterns.md) | Memory leaks, token exhaustion |
| Not batching update actions | [references/anti-patterns.md](references/anti-patterns.md) | Version conflicts under load |
| Using /products instead of /product-projections | [references/anti-patterns.md](references/anti-patterns.md) | 2x response payload size |
| Polling instead of Subscriptions | [references/anti-patterns.md](references/anti-patterns.md) | Wasted API quota, delayed detection |
| Ignoring ConcurrentModification errors | [references/anti-patterns.md](references/anti-patterns.md) | Silent data loss, corrupt state |
| Expanding all references "just in case" | [references/anti-patterns.md](references/anti-patterns.md) | Bloated responses, slow queries |
| Creating empty carts for every visitor | [references/anti-patterns.md](references/anti-patterns.md) | Millions of unused cart resources |
| Not monitoring Subscription health | [references/anti-patterns.md](references/anti-patterns.md) | Silent notification failures for 7 days |

## MCP Complement

Use this skill to understand the _right pattern_, then use the [Developer MCP](https://docs.commercetools.com/sdk/mcp/developer-mcp) to look up exact field names and schemas, and the [Commerce MCP](https://docs.commercetools.com/sdk/mcp/commerce-mcp) for CRUD operations.
