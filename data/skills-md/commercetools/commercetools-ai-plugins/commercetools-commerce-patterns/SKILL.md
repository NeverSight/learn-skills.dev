---
name: commercetools-commerce-patterns
description: Surface-independent commerce domain logic — pricing models (customer groups, channel fallback, high-precision money), discount stacking (Product/Cart/Code/Direct/Groups), shipping predicates and cart score, tax modes, payment object modeling, Import API bulk patterns, and catalog architecture. Use for commerce-domain questions that are independent of surface (storefront, MC app, Connect).
when_to_use:
  - "Pricing models: customer group pricing, channel price fallback, high-precision money, limited-time pricing"
  - "Discount stacking order, Direct Discounts blocking Discount Codes, sortOrder semantics"
  - "Cart Discounts: Buy/Get, Discount Bundles, BOGO, spend thresholds, Discount Groups"
  - "Shipping predicates, cart score tiers, price functions, dynamic shipping rate calculation"
  - "Tax modes: Platform, External, ExternalAmount, Disabled — when to use each"
  - "Payment object modeling — PSP transaction states, interfaceId immutability, tax services"
  - "Import API: batch size limits, ordering guarantees, productDraftImport vs productVariantPatch"
  - "Catalog architecture: ProductType design, bundle patterns, item substitutes, inventory modeling"
  - "B2B order flows: Business Unit hierarchy, as-associate API, approval rules, quote lifecycle"
  - "Recurring orders: RecurrencePolicy, priceSelectionMode, recurringOrderScope"
  - "Implementing a spec/plan/tasks.md task annotated [SKILL: commercetools-commerce-patterns]"
  - "An implementation-plan step covering pricing, discounts, tax, shipping, catalog, or B2B domain modeling"
metadata:
  contentType: SKILL
  area:
    - Foundations
  docsSearch:
    products:
      - Composable Commerce
      - Checkout
      - Connect
      - InStore
      - AI Hub
---

## Workflow

When this skill is invoked, always follow these steps:

1. <!-- ct:docs-search:begin -->
   **Docs search (required, run first)** — The first time you use this skill in a session you must run this before answering. It gathers the latest verified documentation as your primary grounding, filtered to the products this skill covers. Use this script for documentation search while working with this skill; the Knowledge MCP covers everything else. Always confirm details against retrieved documentation rather than the skill text alone:

   ```bash
   node "<this skill's directory>/scripts/docs-search.mjs" \
     --query "<extract key terms from user's question>" \
     --app-name "<host app: claude-code, claude-chat, cursor, codex, copilot — or the host's own name>" \
     --model "<current-model>" \
     --commercetools-project-key "<if known>" \
     --commercetools-region "<if known>" \
     --limit 10
   ```

   Pass the commercetools project key and region (as in `api.{region}.commercetools.com`) only if already in your context; otherwise omit both. Never search files or ask the user for them.
   <!-- ct:docs-search:end -->

2. **Combine with skill references** — Cross-reference the analysis output with local references in `./references/` for complete context.

3. **Provide implementation guidance** — Synthesize the documentation with the specific integration mode the user is targeting.

### Optional scripts

**Fetch GraphQL schema** — Run this when you need context about a commercetools GraphQL query or mutation — for example, to inspect a resource's fields, types, and available operations before writing a query, or to verify a GraphQL query/mutation you have just generated against the real schema. It fetches the partial GraphQL SDL for a single commercetools resource:
  ```bash
  node scripts/graphql-schemata.mjs \
    --resource-name "<commercetools resource, e.g. Cart, Product, Order>" \
    --app-name "<host app: claude-code, claude-chat, cursor, codex, copilot — or the host's own name>" \
    --model "<current-model>"
  ```
  The output is the GraphQL SDL for that resource. If the resource name is not recognized, the script prints the list of valid resource names — pick the correct one and re-run. **Note:** the SDL may contain *stubbed types* — referenced resources rendered as stubs, with their real type name given in a comment. Fetch any you need separately by re-running this script with that type name as `--resource-name`.

**Fetch OpenAPI (REST) schema** — Run this when you need context about a commercetools REST endpoint, request/response payload, or update action — for example, to inspect a resource's REST operations before constructing a request, or to verify a REST request/payload you have just generated against the real specification. It fetches the partial OpenAPI specification for a single commercetools resource:
   ```bash
   node scripts/openApi-schemata.mjs \
     --resource-name "<commercetools resource, e.g. api-Cart-write, api-Customer-read, checkout-Application>" \
     --app-name "<host app: claude-code, claude-chat, cursor, codex, copilot — or the host's own name>" \
     --model "<current-model>"
   ```
   The output is the OpenAPI specification (YAML) for that resource. REST resources use a read/write-split naming form (e.g. `api-Cart-read`, `api-Cart-write`). If the resource name is not recognized, the script prints the list of valid resource names — pick the correct one and re-run. **Note:** the spec does not include reference-expansion schemas — fetch a referenced resource's schema separately by re-running this script with that resource as `--resource-name`.
## Key Takeaways

**Discount stacking follows a strict priority chain.** Product Discounts → Cart Discounts → Discount Codes → Direct Discounts. Direct Discounts on a cart **block all Discount Codes**. Never mix Direct Discounts and Discount Code flows on the same cart.

**sortOrder direction: higher value fires first.** For both Product Discounts and Cart Discounts, the discount with the highest `sortOrder` value (closest to 1) is applied first. `0.9` fires before `0.5`. For Product Discounts only one applies (no stacking); for Cart Discounts they stack by default unless `stackingMode: StopAfterThisDiscount` is set.

**Product Discounts cannot be used with external pricing.** If a project uses an external price source, Product Discounts are not applied. Use Cart Discounts for any promotional discounts when external pricing is active.

**Discount Groups bundle multiple cart discounts under one entity.** A Discount Group has its own `sortOrder` and a `"Best deal"` prioritization mode — only the cart discount from the group that gives the customer the greatest saving is applied. Use Discount Groups to manage large-scale campaigns (e.g., Black Friday) where deactivating dozens of individual discounts at once would otherwise be error-prone.

**Customer Group pricing is set on embedded prices, not at the customer level.** A buyer's Customer Groups are resolved at cart calculation time — the price with a matching `customerGroup` on the variant is selected. A Customer can carry multiple Customer Groups (via `customerGroupAssignments`, up to 500), and price resolution selects the best qualifying price across all assigned groups. For B2B buyers, assign Customer Groups directly to the buyer's customer record or via the Business Unit.

**Cart Score is the key to dynamic shipping rates.** Set the project's shipping rate input type to "Cart Score" in Merchant Center. Call `setShippingRateInput` with a `Score` type and an integer score. CT will look up the rate tier matching that score. The score must be a non-negative integer.

**Cart Score is not available in shipping predicates — copy it to a cart custom field.** The `score` is not directly queryable in predicates. Write the underlying value (e.g., distance in km) to a cart custom field. Write your shipping predicate against that custom field.

**Price functions turn cart score into a continuous rate.** Configure a `priceFunction` (e.g., `(x / 30)`) where `x` is the cart score. CT evaluates the function and sets the resulting amount as the shipping price, enabling rates that scale smoothly without enumerating every possible value.

**Use `taxMode: ExternalAmount` for most PSP/tax service integrations.** This mode lets your tax service calculate the exact tax amount per line item and pass it directly to CT, eliminating rounding discrepancies between CT's engine and external tax services (AvaTax, Vertex).

**CT records payment state; the PSP does the actual financial transaction.** The Payment object is a ledger. Use `addTransaction` update actions to track each PSP event (Authorization, Charge, Refund, Chargeback). Only set `state: "Success"` after confirmed PSP confirmation.

**`interfaceId` on a Payment is immutable once set.** This field links CT Payment to the PSP's identifier. Record it correctly the first time — there is no update path.

**Cart prices are snapshotted at order creation.** If a product price changes between cart creation and order creation, the cart holds the old price. Use the `recalculate` action on the cart to refresh prices before checkout.

**Business Units are the core B2B entity — all B2B operations run through them.** All B2B operations use the `as-associate` API chain (construction and scope in [references/as-associate-api.md](./references/as-associate-api.md)). Never use project-level cart/order APIs for B2B user-facing operations.

**The quote lifecycle has four entities: QuoteRequest → StagedQuote → Quote → Order.** A buyer creates a `QuoteRequest`; a sales rep creates a `StagedQuote` (working draft with negotiated prices); the `Quote` is the finalized offer; if accepted, the buyer converts it to an Order. Each step has its own state machine.

**`POST /orders` vs `POST /recurring-orders` produce fundamentally different results.** Calling `POST /orders` on a cart with recurring line items creates both a regular order (immediate) and a recurring order. Calling `POST /recurring-orders` creates only the recurring order. Use `/orders` for "subscribe and ship now" flow; use `/recurring-orders` for future-dated subscriptions.

**Cart discount `recurringOrderScope` controls whether a discount repeats.** Set `"NonRecurringOrdersOnly"` for one-time welcome promotions. Set `"AnyOrder"` for standing loyalty discounts that should apply on every recurrence cycle.

---

## Reference Index

### Pricing & Promotions

| Topic | Reference |
|-------|-----------|
| Discount stacking rules, sortOrder, Direct Discount blocking Discount Codes | [references/discount-fundamentals.md](references/discount-fundamentals.md) |
| Buy/Get cart discount — triggerPattern, targetPattern, excludeCount | [references/bundle-discounting.md](references/bundle-discounting.md) |
| Cart discount scenario cookbook — 12 named scenarios with full JSON | [references/cart-discount-scenarios.md](references/cart-discount-scenarios.md) |
| Fixed-price combo discount — buy N of X+Y at fixed combined price | [references/fixed-price-combo.md](references/fixed-price-combo.md) |
| "Any N of a set for one fixed total price" (no trigger item), and per-cart firing caps via `maxOccurrence` | [references/cart-discount-scenarios.md](references/cart-discount-scenarios.md) |
| Customer Group-based pricing — embedded price selection, group assignment | [references/customer-group-pricing.md](references/customer-group-pricing.md) |
| B2B customer group pricing — buyer-specific pricing via Customer Groups | [references/b2b-customer-group-pricing.md](references/b2b-customer-group-pricing.md) |
| High Precision Money — fractionDigits, currency configuration, rounding | [references/high-precision-money.md](references/high-precision-money.md) |
| Discount Groups and Promotion Prioritization — best-deal selection | [references/discount-groups.md](references/discount-groups.md) |
| Store credit & loyalty currency — external ledger pattern | [references/store-credit.md](references/store-credit.md) |
| Limited-time pricing — validFrom/validUntil on embedded prices | [references/limited-time-pricing.md](references/limited-time-pricing.md) |
| Discount code usage — code generation, redemption limits | [references/discount-code-usage.md](references/discount-code-usage.md) |

### Shipping & Fulfillment

| Topic | Reference |
|-------|-----------|
| Tiered rates, cart score setup, ScoreShippingRateInput | [references/tiered-rates-cart-score.md](references/tiered-rates-cart-score.md) |
| Shipping predicates — predicate syntax, custom field workaround | [references/shipping-predicates.md](references/shipping-predicates.md) |
| Price functions — priceFunction configuration, function syntax | [references/price-functions.md](references/price-functions.md) |
| Dynamic shipping costs — external calculation, setCustomShippingMethod | [references/dynamic-shipping-costs.md](references/dynamic-shipping-costs.md) |
| BOPIS shipping — multiple shipping methods, delivery group setup | [references/bopis-shipping.md](references/bopis-shipping.md) |

### Payments & Tax

| Topic | Reference |
|-------|-----------|
| Payments — Payment object model, transactions, PSP integration flow | [references/payments.md](references/payments.md) |
| Taxes — cart tax modes (Platform/External/ExternalAmount/Disabled) | [references/taxes.md](references/taxes.md) |
| Financing & installments — BNPL integration, CT payment modeling | [references/financing-options.md](references/financing-options.md) |

### B2B Order Flows

| Topic | Reference |
|-------|-----------|
| Custom Associate Roles — role definition, permission keys, assignment to BU | [references/custom-associate-roles.md](references/custom-associate-roles.md) |
| Business Unit hierarchy — parent/child BUs, inherited roles, store assignment | [references/business-unit-hierarchy.md](references/business-unit-hierarchy.md) |
| Approval rules — predicate design, approval flow lifecycle | [references/approval-rules.md](references/approval-rules.md) |
| Quote lifecycle — QuoteRequest, StagedQuote, Quote, Order conversion | [references/quote-lifecycle.md](references/quote-lifecycle.md) |
| as-associate API pattern — chain construction, scope | [references/as-associate-api.md](references/as-associate-api.md) |

### Recurring Orders

| Topic | Reference |
|-------|-----------|
| Recurring orders — RecurrencePolicy, priceSelectionMode, /orders vs /recurring-orders | [references/recurring-orders.md](references/recurring-orders.md) |

### Catalog & Import

| Topic | Reference |
|-------|-----------|
| Product data modeling — hierarchy, all 14 attribute types, Nested vs Custom Object | |
| Bundle product modeling — ProductType design, child SKU reference, BFF orchestration | [references/bundle-modeling.md](references/bundle-modeling.md) |
| Import API — containers, batching, async processing, delta imports | |
| Import API performance — 15M record pattern, container count, batch size | |
| Item substitutes — modeling substitute/replacement products | [references/item-substitutes.md](references/item-substitutes.md) |
| Inventory modeling — supply channels, inventory entries, backorder | |

---

## Priority Tiers

### CRITICAL

- **Direct Discounts block Discount Codes.** Never add a Direct Discount to a cart if the checkout flow expects users to enter discount codes.
- **sortOrder: higher value fires first** — for both Product Discounts and Cart Discounts. `0.9` is applied before `0.5`. This is a common misconception that causes incorrect promotion behavior.
- **Product Discounts do not work with external pricing.** If the project uses an external price source, switch all promotional discounts to Cart Discounts.
- **triggerPattern SKU predicates are ANDed across entries.** A single `CountOnLineItemUnits` entry can only match one SKU — add separate entries per bundle component.
- **Score must be set before shipping rate lookup.** `setShippingRateInput` must be called before checkout and before shipping rate totals are calculated. Calling it after order creation has no effect.
- **Shipping predicate failures are silent.** If a predicate syntax error exists, CT may silently return no methods or all methods. Always test predicate behavior explicitly with `GET /shipping-methods?cartId=<id>`.
- **All B2B writes MUST use the `as-associate` API chain.** Project-level `apiRoot.carts().*` does not enforce B2B permissions. This is a security requirement, not just a convention.
- **An Associate must have `CreateMyCarts` permission to add items to a cart as-associate.** Missing permissions result in a 403.
- **`POST /orders` creates both a regular order and recurring orders from a mixed cart.** Design the order confirmation flow to handle multiple order IDs.
- **A RecurrencePolicy cannot be deleted while in use.** Remove all line item and cart references before attempting deletion.
- **Never set a Payment transaction to `Success` before PSP confirmation.** Optimistic success marking creates reconciliation failures.
- **`interfaceId` on a Payment cannot be changed once set.** Record the PSP transaction identifier correctly on the first write.
- **Import API has no ordering guarantee.** Poll the first operation's status before submitting the second.
- **`productDraftImport` is destructive.** Any field not included in the draft is deleted.
- **Version conflicts (409 ConcurrentModification) require retry with the latest version.** Do NOT use the version from the failed request.

### HIGH

- **Customer Group pricing requires the customer to be logged in and have a customerGroup set.** Anonymous carts get the default price.
- **HighPrecisionMoney must be consistent across all prices in a cart.** Mixing centPrecision and highPrecision prices in the same cart/order causes calculation errors.
- **Discount Code `maxApplications` is global across all customers.** Use `maxApplicationsPerCustomer` for per-customer limits — they are separate fields.
- **Cart Score is not available in shipping predicates.** Copy the distance or weight value to a cart custom field before writing predicates against it.
- **Per-warehouse predicates need the warehouse key in a cart custom field.** The cart's assigned supply channel is not directly queryable in a shipping predicate.
- **StagedQuotes hold negotiated line item prices.** When converting a StagedQuote to a Quote, prices from the StagedQuote are locked in.
- **Approval Rules are evaluated at Order creation, not Cart creation.** Design the cart-to-order UX to set buyer expectations about the approval wait.
- **`priceSelectionMode` must be set intentionally per use case.** `"Fixed"` provides price guarantee; `"Dynamic"` always applies current catalog pricing.
- **`recurringOrderScope` on cart discounts defaults to applying on all orders.** Explicitly set `"NonRecurringOrdersOnly"` for introductory discounts.
- **Nested attributes are not searchable and cannot target discount predicates.** Use flat attribute types for any attribute that must appear in search filters or predicates.
- **Batch size for Import API is max 20 operations per request.** Always chunk.
- **Changing a ProductType attribute constraint after data exists requires a migration.** Plan attribute constraints during initial design.

### MEDIUM

- **`isActive` on a Cart Discount is a soft toggle.** Use this for scheduled campaigns rather than creating/deleting discounts.
- **Use `stackingMode: StopAfterThisDiscount`** to make a specific discount exclusive. Cart discounts stack by default.
- **Price rounding is configurable via `priceRoundingMode`** (on Cart/Order/Quote and as a Project default). Modes: `HalfEven` (banker's rounding — the default), `HalfUp`, `HalfDown`. Only `HalfDown` rounds `.5` in the customer's favor; align the mode with your ERP/tax system and budget margin accordingly for high-volume campaigns.
- **For unsupported discount scenarios, the pattern is an API Extension on cart/order** that calculates and injects a Direct Discount or custom line item.
- **`lineItemGrossTotal(categories.key = (...)) >= "X.XX USD"` is the pattern for category spend thresholds.** The currency string must be included in the value.
- **Price functions are evaluated server-side at rate lookup time.** Do not try to replicate the function in your frontend.
- **Quote negotiation supports multiple rounds.** Track negotiation rounds via custom fields on QuoteRequest if your business requires round history.
- **Customer Group assignment on the buyer's customer record is the simplest B2B pricing pattern.** All their carts inherit the group pricing automatically.
- **Order confirmation UX must handle multiple order IDs.** A single cart checkout with recurring items at different frequencies produces N+1 orders.
- **Standalone prices via Import API support `validFrom`/`validUntil`** for time-limited pricing without product republication.

