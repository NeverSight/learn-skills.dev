---
name: bigcommerce-api
description: BigCommerce API expert for building integrations, apps, headless storefronts, and automations. Full lifecycle - REST APIs, GraphQL Storefront, webhooks, authentication, app development, and multi-storefront. Use when working with BigCommerce platform APIs.
---

<essential_principles>

<principle name="api-versioning">
BigCommerce maintains V2 and V3 APIs concurrently. V3 is preferred for most operations:
- **Catalog, Customers, Carts**: Use V3 (better pagination, metafields support)
- **Orders**: V2 for CRUD operations, V3 for transactions/refunds
- **Customer Groups**: Still V2 only (V3 migration planned)

Always check which version supports your specific endpoint.
</principle>

<principle name="authentication-model">
BigCommerce uses OAuth exclusively for V3 APIs:
- **X-Auth-Token header**: REST APIs and GraphQL Admin
- **Bearer token**: GraphQL Storefront API
- **Store-level credentials**: Single store integrations
- **App-level credentials**: Marketplace apps (OAuth flow)
- **Account-level credentials**: Multi-store management

Never embed credentials in client-side code. Use environment variables.
</principle>

<principle name="rate-limits">
Respect rate limits to avoid blocking:
- **Standard REST API**: 20,000 requests/hour
- **Payments API**: 50 requests/4 seconds
- **B2B Edition**: 150 requests/minute
- **GraphQL**: Query complexity limits apply

Monitor headers: `X-Rate-Limit-Requests-Left`, `X-Rate-Limit-Time-Reset-Ms`
Implement exponential backoff with jitter for retries.
</principle>

<principle name="channel-awareness">
All storefronts and sales channels have a `channel_id`:
- Default storefront channel_id is always `1`
- MSF stores have multiple channels
- Products must be explicitly assigned to channels
- Orders, carts, and checkouts should specify channel_id

Always include channel_id when working with multi-storefront stores.
</principle>

</essential_principles>

<intake>
What would you like to do with BigCommerce APIs?

1. Build a new integration (REST API, webhooks, data sync)
2. Create a headless storefront (GraphQL Storefront, Next.js/Catalyst)
3. Develop a BigCommerce app (single-click app, marketplace)
4. Work with specific API (Catalog, Orders, Customers, Payments)
5. Debug an API issue (errors, authentication, rate limits)
6. Set up webhooks and event handling
7. Something else

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "integration", "sync", "connect" | `workflows/build-integration.md` |
| 2, "headless", "storefront", "next.js", "catalyst", "graphql" | `workflows/build-headless-storefront.md` |
| 3, "app", "marketplace", "single-click" | `workflows/build-app.md` |
| 4, "catalog", "orders", "customers", "payments", "specific" | `workflows/work-with-api.md` |
| 5, "debug", "error", "fix", "troubleshoot", "401", "422" | `workflows/debug-api-issue.md` |
| 6, "webhook", "webhooks", "events", "subscribe" | `workflows/setup-webhooks.md` |
| 7, other | Clarify intent, then route to appropriate workflow |

**After reading the workflow, follow it exactly.**
</routing>

<verification_loop>
After every API operation:

```bash
# 1. Check response status
# 200/201 = Success
# 4xx = Client error (check request)
# 5xx = Server error (retry with backoff)

# 2. Verify rate limit headers
X-Rate-Limit-Requests-Left: [remaining]
X-Rate-Limit-Time-Reset-Ms: [reset time]

# 3. For mutations, verify the change
GET the resource to confirm state
```

Report to user:
- "API call: [status]"
- "Rate limit remaining: [X]"
- "Data verified: [confirmation]"
</verification_loop>

<reference_index>

**Authentication & Security:**
- references/authentication.md - OAuth, tokens, scopes, credentials
- references/security-best-practices.md - API keys, PCI compliance, headers

**Core APIs:**
- references/catalog-api.md - Products, categories, brands, variants
- references/orders-api.md - Orders, shipments, transactions, fulfillment
- references/customers-api.md - Customers, addresses, groups, segments
- references/payments-api.md - Payment processing, gateways, checkout

**Storefront & Content:**
- references/graphql-storefront.md - GraphQL queries, carts, checkout
- references/widgets-scripts.md - Widgets API, Scripts API, content injection
- references/stencil-themes.md - Theme development, Handlebars, CLI

**Platform Features:**
- references/webhooks.md - Events, subscriptions, retry logic
- references/multi-storefront.md - MSF, channels, site routing
- references/headless-commerce.md - Next.js Commerce, Catalyst, React

**Development:**
- references/app-development.md - Single-click apps, Developer Portal
- references/rate-limits-pagination.md - Throttling, cursor pagination, batching
- references/error-handling.md - Status codes, troubleshooting, debugging

</reference_index>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| build-integration.md | Create data sync, connect external systems |
| build-headless-storefront.md | Next.js/Catalyst headless frontend |
| build-app.md | Single-click marketplace app |
| work-with-api.md | Use specific BigCommerce API |
| debug-api-issue.md | Fix errors and authentication problems |
| setup-webhooks.md | Configure webhook subscriptions |
</workflows_index>

<quick_reference>

**Base URLs:**
- REST API: `https://api.bigcommerce.com/stores/{store_hash}/v3/`
- Payments: `https://payments.bigcommerce.com/stores/{store_hash}/payments`
- GraphQL Storefront: `https://{store_domain}/graphql`
- OAuth Token: `https://login.bigcommerce.com/oauth2/token`

**Essential Headers:**
```
X-Auth-Token: {access_token}
Content-Type: application/json
Accept: application/json
```

**GraphQL Storefront Auth:**
```
Authorization: Bearer {storefront_token}
```

</quick_reference>
