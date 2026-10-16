---
name: spree-returns
description: Use when working with post-purchase flows in Spree 6 — returns (money back), exchanges (different items), and claims (damaged / missing / wrong item, refund or replacement without the goods coming back). Covers Spree::Return / Spree::Exchange / Spree::Claim, their statuses and workflows, return windows per market and staff overrides, custom return policy via the returns.create.validate hook, receiving and restocking (resellable), refunds to the original payment vs store credit, prepaid return labels, return and claim reasons, events, and the Store/Admin API endpoints. Common phrasings include "RMA", "return window", "30-day returns", "final sale items can't be returned", "restock returned items", "refund a return", "store credit refund", "exchange for a different size", "item arrived damaged", "send a replacement", "return label", "ReturnAuthorization", "CustomerReturn", "Reimbursement".
---

# Spree Returns, Exchanges & Claims

Three separate records, each with its own lifecycle, all hanging off a placed `Spree::Order`:

| Record | Prefix / number | What happened | Outcome |
|---|---|---|---|
| `Spree::Return` | `ret_` / `RET…` | Customer sends items back | Money back |
| `Spree::Exchange` | `exch_` / `EX…` | Customer sends items back | Different items (price difference settled) |
| `Spree::Claim` | `claim_` / `CLM…` | Arrived damaged, never arrived, wrong item | Refund, replacement, or both — goods usually not returned |

Keep them apart: don't model "arrived smashed" as a return you immediately mark received — use a claim, so damage is reportable. Coming from 5.x (`ReturnAuthorization` → `CustomerReturn` → `Reimbursement`, `ReturnItem`)? Those are gone; see **spree-upgrade-5-to-6**.

## Models

```
Order
  ├── Return (ret_)        status, stock_location, reason (ReturnReason rar_), memo, received_at, refunded_at, created_by
  │     ├── ReturnLineItem (rli_)   fulfillment_item + line_item + variant; quantity (announced), received_quantity, resellable, pre_tax_amount
  │     ├── refunds (Spree::Refund, originator: return) / store_credits (originator: return)
  │     ├── ShippingLabel × n       prepaid return postage
  │     └── Delivery × n            inbound tracking
  ├── Exchange (exch_)     status, stock_location, reason (ReturnReason)
  │     └── ExchangeLineItem (eli_) fulfillment_item + line_item; original_variant → new_variant; price_difference
  └── Claim (claim_)       status, resolution, reason (ClaimReason clr_)
        └── ClaimLineItem (cli_)    line_item + variant; quantity, description, images, send_replacement,
                                     replacement_variant, refund_amount
```

- Returns and exchanges reference **fulfillment items** (units that shipped), not cart line items. Claims reference **line items** (the goods may never have arrived).
- All three are store-scoped (`SingleStoreResource`), carry `metadata` and custom fields, and record who acted (`created_by`, approver, refunder).
- Reasons are store-owned vocabularies: `Spree::ReturnReason` (used by returns and exchanges) and `Spree::ClaimReason`. Seeds create a default set per store (claim reasons such as "Arrived damaged", "Never arrived", "Wrong item sent"); merchants add their own.

## Statuses

String `status` columns via `has_status` — no state machine, transitions are workflows:

| Record | Flow | Cancel allowed from |
|---|---|---|
| Return | `requested` → `approved` → `received` → `refunded`, or `canceled` | `requested`, `approved` |
| Exchange | `requested` → `approved` → `received` → `fulfilled`, or `canceled` | `requested`, `approved` |
| Claim | `open` → `approved` → `resolved`, or `denied` / `canceled` | `open`, `approved` (deny only from `open`) |

## Workflows

Every transition is a `Spree::Workflow` resolved through `Spree.<key>` (swap via `Spree.dependencies`, see spree-dependencies). Every one has a leading `validate` hook.

| Record | Workflow (DI key) | Arguments | Hooks |
|---|---|---|---|
| Return | `return_create_workflow` → `Spree::Returns::Create` | `order:, items: [{ fulfillment_item:, quantity: }], stock_location:, reason:, memo:, created_by:` | `validate`, `after_create` |
| | `return_approve_workflow` → `Returns::Approve` | `return_record:, approver:` | `validate`, `after_approve` |
| | `return_receive_workflow` → `Returns::Receive` | `return_record:, items: [{ return_line_item:, quantity:, resellable: }], received_by:` | `validate`, `before_restock`, `after_receive` |
| | `return_refund_workflow` → `Returns::Refund` | `return_record:, amount:, refund_method: 'original_payment', refunder:` | `validate`, `before_refund`, `after_refund` |
| | `return_cancel_workflow` → `Returns::Cancel` | `return_record:, reason:` | `validate`, `after_cancel` |
| | `return_purchase_label_workflow` → `Returns::PurchaseLabel` | `return_record:` | `validate`, `after_purchase_label` |
| Exchange | `exchange_create_workflow` → `Exchanges::Create` | `order:, items: [{ fulfillment_item:, new_variant:, quantity: }], …` | `validate`, `after_create` |
| | `exchange_approve_workflow`, `exchange_receive_workflow`, `exchange_cancel_workflow` | as returns | `validate`, `after_*` (+ `before_restock` on receive) |
| | `exchange_fulfill_workflow` → `Exchanges::Fulfill` | `exchange:, refund_method: 'store_credit', refunder:` | `validate`, `before_settle`, `after_fulfill` |
| Claim | `claim_create_workflow` → `Claims::Create` | `order:, items: [{ line_item:, quantity:, description:, send_replacement:, replacement_variant:, refund_amount: }], reason:, memo:, created_by:` | `validate`, `after_create` |
| | `claim_approve_workflow`, `claim_deny_workflow`, `claim_cancel_workflow` | | `validate`, `after_*` |
| | `claim_resolve_workflow` → `Claims::Resolve` | `claim:, resolution:, refund_method: 'store_credit', amount:, replacement_line_item_ids:, resolver:` | `validate`, `before_settle`, `after_resolve` |

Hook keys follow the class name: `returns.create.validate`, `returns.receive.before_restock`, `exchanges.fulfill.before_settle`, `claims.resolve.after_resolve`, etc.

```ruby
result = Spree.return_create_workflow.call(
  order: order,
  items: [{ fulfillment_item: order.fulfillment_items.find_by_prefix_id!('fi_…'), quantity: 1 }],
  reason: store.return_reasons.first, # or nil
  created_by: current_admin           # nil = customer self-service (window enforced)
)
result.success? ? result.value : result.error
```

Creation guards (all three): the order must be completed and not canceled, items non-empty; returns/exchanges also refuse quantities above what is still returnable — units on non-canceled earlier returns **and** exchanges count against each other (`Spree::Returns::ReturnableQuantity`), as do units named twice in one request. Claims are bounded the same way per line item: units already covered by `open`/`approved`/`resolved` claims can't be claimed again (denied or canceled claims free them).

## Return policy: window, overrides, custom rules

Core ships exactly one policy rule: `Spree::Returns::EligibilityValidator`, registered on **both** `returns.create.validate` and `exchanges.create.validate`.

- The window is `market.preferred_return_window_days` (default 30; `nil` = no limit), falling back to the `Spree::Market` default when the order has no market. It is measured from `order.completed_at` (placement), not delivery.
- It is **skipped when `created_by` is present** — staff (Admin API, and the Seller API) opening a return are treated as an override, attributable through `created_by`. Store API (customer) returns are always checked.
- `withdrawal_period_days` (default 14, EU floor) on the market is a separate statutory notice value — it doesn't gate return creation.
- The legacy `Spree::Config.return_eligibility_number_of_days` is deprecated and read by nothing.

Replace or extend the rule with your own handler. Core registers its validator **before** application initializers run, so the swap works at the top level of `config/initializers/spree.rb`:

```ruby
# app/services/my_store/return_policy.rb
module MyStore
  class ReturnPolicy
    def call(workflow) # Spree::Returns::Create or Spree::Exchanges::Create
      return if workflow.created_by.present? # keep the staff override

      order = workflow.order
      window = order.market&.preferred_return_window_days || 30
      delivered_at = order.fulfillments.maximum(:delivered_at) || order.completed_at
      workflow.reject!("Returns are accepted for #{window} days after delivery") if delivered_at < window.days.ago

      final_sale = workflow.items.any? do |item|
        item[:fulfillment_item].variant.product.get_custom_field('policy.final_sale')&.value == 'true'
      end
      workflow.reject!('Final-sale items cannot be returned') if final_sale
    end
  end
end

# config/initializers/spree.rb
%w[returns.create.validate exchanges.create.validate].each do |key|
  Spree.hooks.unregister(key, 'Spree::Returns::EligibilityValidator')
  Spree.hooks.register(key, 'MyStore::ReturnPolicy')
end
```

Handlers are registered as class-name strings (reload-safe), instantiated with no arguments and called with the workflow. `workflow.reject!(message)` adds a base error and fails the workflow; the API renders it as a 422 like a model validation error. The same pattern gates any later step — e.g. `returns.refund.validate` to require manager approval above an amount, or `claims.resolve.validate` to require photos on `claim_line_items.images`. There is no "eligible but needs manual review" state; model that with your own status (`Spree::Return.add_status`, in `to_prepare`) or metadata.

## Receiving and restocking

`Returns::Receive` (and `Exchanges::Receive`) takes what the warehouse actually counted. Omit `items` to receive everything as announced and resellable. Per line: `received_quantity` is recorded, and **only `resellable` units are restocked** — `stock_location.restock(variant, qty, return)` writes a `received` stock movement caused by the return at the return's stock location. Non-resellable units are recorded but never re-enter stock. Use `before_restock` to route damaged goods elsewhere or override resellability.

Where goods come back to: the return's `stock_location` — passed explicitly (`stock_location_id`, admin only), otherwise the location that shipped the items if it has `returns_enabled`, else the seller's returns location, else `store.returns_location`, else whatever shipped them / the store default.

A delivery reporting arrival on a return's inbound parcel **never** receives the return — arrival is not inspection.

## Refunds and settlement

- `Returns::Refund` requires status `received`. `amount` defaults to (and is capped by) `refundable_total` — only units that actually arrived are owed (`refund_total - refunded_total`). `refund_method` is `'original_payment'` (default for returns) or `'store_credit'` (`Spree::RefundMethods::METHODS`).
- **A returned or claimed unit is worth what the customer paid after discounts**, not its list price: `LineItem#discounted_amount_for(units)` (the line's `discounted_amount` pro-rated, rounded to the currency, never negative) backs `ReturnLineItem#default_pre_tax_amount` and `ClaimLineItem#paid_amount`. A coupon, promotion or manual discount on the line is not paid back, and a free gift sent back is worth zero.
- **A return owed nothing** (`refundable_total` zero, e.g. only a free gift came back) is closed by calling `Returns::Refund` with no amount (or `0`). It moves to `refunded` with no refund row, store credit, tax credit or refund email; `return.refunded` still publishes. Zero on a return that is still owed money fails with `refund_amount_required`, a negative amount with `refund_amount_negative`, more than owed with `refund_exceeds_balance`.
- Store credit is an internal ledger write inside the transaction (`Spree::StoreCredit`, originator = the return); gateway refunds run as an `external_step` after it, split across the order's refundable payments (`Spree::Refund` rows, originator = the return). Tax is credited through the tax provider afterwards (`refund_tax`).
- **One refundable balance per order.** Every refund path (returns, exchanges, claims — gateway or store credit) goes through `Spree::Refunds::OrderPayments`, which locks the order and caps the amount at what its payments can still refund **minus store credit already issued against the order** (`refunded_order`). Exceeding it fails with `refund_exceeds_paid`, so two post-sale records on one order can't each pay out the full amount.
- `refunded_total` counts refunds **and** store credits. So does the order's `payment_status`: store credit issued by a return, exchange or claim refund carries `refunded_order_id`, and the order moves to `partially_refunded` / `refunded` just like a gateway refund.
- Exchanges: `Exchanges::Fulfill` builds replacement fulfillments (via `Spree::Stock::Coordinator`) and allocates stock. If the replacements are cheaper (`price_difference` negative) it credits the difference **for the units actually received** (not the requested quantity) — `'store_credit'` by default or `'original_payment'`. If they cost more, the balance is **left for the merchant to collect** — core never silently charges a stored card.
- Claims: `Claims::Resolve` with `resolution` one of `refund`, `replacement`, `refund_and_replacement` (`Spree::Claim::RESOLUTIONS`); requires `approved`. Refund defaults to `'store_credit'` and the claim total (sum of line `refund_amount`s), capped at the sum of the lines' `paid_amount` (exposed on claim line items in the API; over it fails `refund_exceeds_paid`); replacements become new fulfillments on the original order (the customer doesn't place a second order). `replacement_line_item_ids` at resolve time overrides what was flagged at creation.
- Returns and claims update the order's `payment_status` through `Spree::Orders::UpdateStatuses`; don't write it.

## Prepaid return labels

`POST /api/v3/admin/orders/:order_id/returns/:id/labels` with no body buys postage through the carrier account the outbound parcel used (`Returns::PurchaseLabel` → the fulfillment provider's `purchase_label(return)`), booked from the customer back to the return's stock location, and mints an inbound `Spree::Delivery`. With `file` (signed blob id) + `tracking_number` it records a label bought elsewhere. Customers download it from `GET /api/v3/store/orders/:order_id/returns/:id/label`. Canceling a return refunds an unused prepaid label.

## API

Store API (order owner — customer JWT or order token), self-service open + view only:

```bash
POST /api/v3/store/orders/:order_id/returns   { "items": [{ "fulfillment_item_id": "fi_…", "quantity": 1 }], "reason_id": "rar_…", "memo": "Too small" }
GET  /api/v3/store/orders/:order_id/returns[/:id][/label]
POST /api/v3/store/orders/:order_id/claims    { "items": [{ "line_item_id": "li_…", "quantity": 1, "description": "Arrived cracked" }], "reason_id": "clr_…" }
GET  /api/v3/store/orders/:order_id/claims[/:id]
```

TypeScript: `client.orders.returns.create(orderId, …)`, `client.orders.claims.create(orderId, …)`.

Admin API — gated by `read_orders` / `write_orders` (returns are part of the orders permission resource):

| Endpoint | Notes |
|---|---|
| `…/admin/orders/:order_id/returns` (index/show/create/update) | create: `items[{fulfillment_item_id, quantity}]`, `reason_id`, `stock_location_id`, `memo`; update edits `memo`, `reason_id`, `stock_location_id`, `metadata` only |
| `PATCH …/returns/:id/approve` · `/receive` · `/refund` · `/cancel` | receive: `items[{return_line_item_id, quantity, resellable}]`; refund: `amount`, `refund_method`; cancel: `reason` |
| `…/returns/:id/labels` (+ `download`, `refund`) | prepaid postage |
| `…/admin/orders/:order_id/exchanges` + `approve` · `receive` · `fulfill` · `cancel` | create items: `fulfillment_item_id`, `new_variant_id`, `quantity`; fulfill: `refund_method` |
| `…/admin/orders/:order_id/claims` + `approve` · `resolve` · `deny` · `cancel` | create items: `line_item_id`, `quantity`, `description`, `send_replacement`, `replacement_variant_id`, `refund_amount`; resolve: `resolution`, `refund_method`, `amount`, `replacement_line_item_ids` |
| `GET /api/v3/admin/returns`, `/exchanges`, `/claims` | cross-order lists; Ransack e.g. `q[status_eq]=approved`, `q[created_at_gt]=…` |
| `/api/v3/admin/return_reasons`, `/claim_reasons` | CRUD |

Admin SDK: `adminClient.orders.returns.{create,approve,receive,refund,cancel}`, `.returns.labels.*`, `adminClient.orders.exchanges.{approve,receive,fulfill,cancel}`, `adminClient.orders.claims.{approve,resolve,deny,cancel}`, `adminClient.returns.list(...)`.

## Events

`return.requested`, `return.approved`, `return.received`, `return.refunded`, `return.canceled`; `exchange.requested/.approved/.received/.fulfilled/.canceled`; `claim.opened/.approved/.resolved/.denied/.canceled`; plus lifecycle `*.created/.updated/.deleted` for each. All reach webhooks. The optional `spree_emails` gem sends `Spree::ReturnMailer` mail (e.g. the refund email on `return.refunded`). Removed: `reimbursement.*`, `return_authorization.*`, `return_item.*`, `customer_return.*`.

## Gotchas

- Don't transition by `update!(status: …)` — you skip restocking, refunds, events and hooks. Always call the workflow.
- The return window counts from order placement. If your policy counts from delivery (common, and EU withdrawal does), write your own validator (above) — `fulfillment.delivered_at` is populated from carrier webhooks or `mark_delivered`.
- Staff/seller-created returns bypass the window by design. If your policy must apply to staff too, don't early-return on `created_by` in your handler.
- `Returns::Refund` only runs from `received`; a return is refunded once. Split tenders are handled inside that one refund (it spreads across payments), not by calling it twice.
- Exchange balances owed by the customer are not charged automatically — collect them yourself (e.g. in an `exchanges.fulfill.after_fulfill` hook or a manual payment).
- The replacement fulfillment, its packing slip and the dashboard's Exchanges card name the **replacement** variant (`new_variant`), not the original.
- Units an exchange or claim sends are filed under the original line item with `FulfillmentItem#replacement = true` (built through `Spree::Fulfillments::Replacements`). Order edits count only bought units, so changing that line's quantity adds or removes paid goods and leaves the replacement alone. Replacement units shipped on earlier 6.0 betas were not flagged and aren't backfilled.
- Claims don't restock anything — nothing comes back. If goods do come back, open a return too.
- Always scope lookups through the order/store (`order.fulfillment_items.find_by_prefix_id!`) — never `Spree::FulfillmentItem.find(params[:id])`.

## Testing

Factories: `:return`, `:approved_return`, `:received_return`, `:return_line_item`, `:exchange`, `:approved_exchange`, `:received_exchange`, `:claim`, `:approved_claim`, `:return_reason`, `:claim_reason`, plus `:completed_order_with_totals` / `:fulfillment`. Test your policy handler by calling the workflow and asserting `result.failure?` + `result.error` messages, not by invoking the handler in isolation only. Set `Spree::Current.store` in non-request specs.

## Where to read further

- `node_modules/@spree/docs/dist/developer/core-concepts/returns-exchanges-claims.md`
- `node_modules/@spree/docs/dist/developer/customization/workflows.md` (hooks, `reject!`)
- `node_modules/@spree/docs/dist/developer/core-concepts/store-credits-gift-cards.md`, `payments.md`
- Related skills: spree-workflows, spree-fulfillment (labels, deliveries, replacements), spree-inventory (restock movements), spree-payments (refunds), spree-events-webhooks, spree-upgrade-5-to-6.
