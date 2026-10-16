---
name: spree-order-totals
description: Use when the user is working with money on a Spree 6 cart or order — how `total` is built, the typed money rows (`Spree::TaxLine`, `Spree::Discount`, `Spree::Fee`), totals columns (`item_total`, `discount_total`, `delivery_total`, `fee_total`, `included_tax_total` vs `additional_tax_total`, `adjustment_total`, `amount_due`), `Spree::Carts::RecalculateTotals`, custom adjusters (`Spree.adjusters`), fees and customs duties, manual discounts and fees on placed orders, or rendering an order summary. Common phrasings include "order total is wrong", "totals don't add up", "tax counted twice", "add a surcharge / handling fee / gift wrap fee", "add a custom fee", "where are adjustments", "Spree::Adjustment missing", "recalculate order totals", "edit a placed order's discount", "why did my discount disappear", "display_total", "money as string", "duties".
---

# Spree Order Totals

A cart's or order's `total` is assembled from **typed money rows** — there is no polymorphic `Spree::Adjustment`. Each kind of money has its own table, its own denormalized sum on the purchase, and a single workflow that keeps them consistent.

> Coming from 5.x adjustments? See `spree-upgrade-5-to-6` (`spree:migrate_adjustments_to_typed_rows`).

## The formula

```
total = item_total + delivery_total + adjustment_total
adjustment_total = (all discount rows) + fee_total + additional_tax_total
```

| Column (Cart & Order) | What it holds |
|---|---|
| `item_total` | Σ line item `amount` (price × quantity), before discounts/tax |
| `delivery_total` | Σ fulfillment `cost` (the selected delivery rates) |
| `discount_total` | Σ **promotion** discount rows (negative) — manual discounts are *not* in it (see Gotchas) |
| `fee_total` | Σ fee rows (always ≥ 0), duties included |
| `additional_tax_total` | Σ tax lines with `included: false` — added on top |
| `included_tax_total` | Σ tax lines with `included: true` — **already inside** prices; informational |
| `adjustment_total` | discounts + fees + additional tax |
| `total` | What the customer pays |
| `payment_total` | Captured payments minus refunds |
| `tax_total` (method) | `included_tax_total + additional_tax_total` |
| `amount_due` (method) | `max(total − payment_total − applied store credit, 0)` |

Line items and fulfillments carry their own per-adjustable columns (`discount_total`, `included_tax_total`, `additional_tax_total`, `adjustment_total`, `taxable_adjustment_total` = discounts, `non_taxable_adjustment_total` = fees, `pre_tax_amount`) so per-line math and returns don't need to re-query rows.

Placed marketplace orders also carry `commission_amount_total` / `commission_tax_total` / `commission_total` — charged to the seller, **never** part of `total` (see `spree-marketplace`).

## The typed rows

All three include `Spree::TypedAdjustmentLine`: dual `cart_id` / `order_id` owner (exactly one — read `row.owner`), `label`, `amount` (+ `display_amount`), `metadata`.

| Model (prefix) | Attaches to (exactly one…) | Kinds | Sign | Written by |
|---|---|---|---|---|
| `Spree::TaxLine` (`tl_`) | line item, fulfillment, **or fee** | — (`included` true/false, `taxability_reason`) | ≥ 0 | The tax provider only (see `spree-taxes`) |
| `Spree::Discount` (`disc_`) | line item **or** fulfillment | `promotion`, `manual` | ≤ 0 | Promotion adjuster; admin (`manual`) |
| `Spree::Fee` (`fee_`) | line item, fulfillment, **or neither** (order-level) | `surcharge`, `handling`, `gift_wrap`, `cod`, `payment`, `duty` (extensible) | ≥ 0 | Adjusters, integrations, admin |

- **No order-level discount rows.** An order-wide promotion or manual discount is spread across line items by largest-remainder over each line's discounted base — which is what makes a partial return refund the right share without guessing.
- Rows **snapshot their provenance**: a discount keeps `code`, `value`, `value_type` (promotion FKs nullify on delete); a tax line keeps `rate`, `label`, `provider_id`, jurisdiction; a duty fee keeps its HS code / origin / rate in `metadata`. Never re-derive a placed order's money from today's catalog.
- Fees are taxable by default (tax lines point at `fee_id`); `duty` fees are excluded from the taxable set.
- Credits are never negative fees — create a discount.

## `Spree::Carts::RecalculateTotals` — the single seam

Everything that changes money ends in this workflow (`Spree.cart_recalculate_totals_workflow`; order twin `Spree.order_recalculate_totals_workflow` = `Spree::Orders::RecalculateTotals`). `cart.recalculate_totals!` is the shortcut.

```
reset caches → total_quantity → item_total / delivery_total / payment_total
  → [unless money-frozen] regenerate rows:
       Spree.adjusters.each { |a| a.adjust(cart) }          # promotions, your fees/discounts
       run_hooks :set_tax_line_context                      # carts.recalculate_totals.set_tax_line_context
       cart.tax_provider.estimate(cart, **cart.tax_estimate_inputs, context:)
  → fold rows into per-line and purchase columns → total → one update_columns
```

Two-pass by design: adjusters persist the discounted base first, then tax is estimated on it.

**What triggers it — writes, not steps.** Item add/upsert/remove (via `Spree::Carts::Recalculate`, which also rebuilds delivery proposals and re-activates promotions), address or market change (`recalculate_for_address_change!` also re-prices items), delivery-rate selection, coupon/gift card/store credit apply/remove, payments, cart merge, and **once more inside the completion lock** — the charged total is never trusted from an earlier request. Reading a cart doesn't recalculate (except the Store API `GET` backfilling missing delivery proposals).

Every Store API write returns the full cart with fresh totals; storefronts never call a "recalculate" endpoint.

### The promotion adjuster is winner-only

`Spree::Adjusters::Promotion` evaluates every eligible promotion on every recalculation and **persists only the winner per competition group**: line-level actions compete per line item, fulfillment actions per fulfillment, order-level actions order-wide (winner distributed across lines). Most negative amount wins; ties go to the newest action. Losing candidates simply aren't written, so they "reinstate" automatically when they become best. It also deletes any `kind: 'promotion'` row it didn't write this pass. Details: `spree-promotions`.

## Money freeze after placement

For a **placed** order (`completed?`) — or when called with `resum_only: true` (seller-split child drafts) — the workflow **skips row regeneration**: no adjusters, no promotion competition, no tax estimation. It only re-sums the rows the order already has. Consequences:

- Today's promotions and tax rates never rewrite last week's order.
- Custom adjusters don't run on placed orders.
- Post-placement money changes go through explicit services that write rows, then re-sum:

| Change | Service | Admin API |
|---|---|---|
| Manual discount (flat/percent, one line or distributed) | `Spree::Orders::Discounts::Create/Update/Destroy` | `POST/PATCH/DELETE /api/v3/admin/orders/:id/discounts` |
| Fee | `Spree::Orders::Fees::Create/Update/Destroy` | `/api/v3/admin/orders/:id/fees` |
| Items / attributes | `Spree::Orders::Update` (`items: [...]`), `Orders::UpdateItem`, `Orders::AddItem` | `PATCH /api/v3/admin/orders/:id`, `/api/v3/admin/orders/:id/items` |
| Tax lines | — (provider-written) | `GET /api/v3/admin/orders/:id/tax_lines` (read-only) |

```ruby
Spree::Orders::Discounts::Create.call(order: order, label: 'Price match', value: '15', value_type: 'flat')
Spree::Orders::Fees::Create.call(order: order, attributes: { label: 'Handling', kind: 'handling', amount: 2.5 })
```

Each of these services re-sums and then calls `order.update_statuses!`, because no event announces a moved total. A paid order that gains a fee reads `partially_paid`, and one cut below what was paid reads `overcharged` (`amount_due` floors at zero, so only the status says a refund is owed). A custom service that edits a placed order's money must make the same call. `Orders::Update` is all-or-nothing: if any item change in the request is refused, no line, quantity or address change is saved.

Only `manual` discounts are editable — touching a `promotion` row fails (`422` via the API). Because tax is not re-estimated on a placed order, a manual discount does **not** reduce already-charged tax; handle tax corrections through your tax provider / a return.

## Custom fees and discounts: adjusters

An adjuster owns a family of rows and is re-run on every (unfrozen) recalculation. Contract: subclass `Spree::Adjusters::Base`, implement idempotent `update` (write the rows that should exist, delete the ones that shouldn't). `order` is the cart (or draft order); `order.fees` / `order.discounts` attach to the right owner automatically.

```ruby
# server/app/models/my_app/adjusters/gift_wrap.rb
module MyApp
  module Adjusters
    class GiftWrap < Spree::Adjusters::Base
      PRICE = BigDecimal('4.99')

      def update
        wrapped = order.line_items.select { |li| li.metadata['gift_wrap'].present? }

        order.fees.where(kind: 'gift_wrap').where.not(line_item_id: wrapped.map(&:id)).delete_all
        wrapped.each do |li|
          order.fees.find_or_initialize_by(kind: 'gift_wrap', line_item_id: li.id)
               .update!(label: 'Gift wrapping', amount: PRICE * li.quantity)
        end
      end
    end
  end
end
```

```ruby
# server/config/initializers/spree.rb — MUST be after_initialize:
# core assigns Spree.adjusters = [Spree::Adjusters::Promotion] in its own after_initialize,
# which would wipe anything appended earlier.
Rails.application.config.after_initialize do
  Spree.adjusters << MyApp::Adjusters::GiftWrap
  Spree::Fee::KINDS << 'insurance' unless Spree::Fee::KINDS.include?('insurance') # custom fee kind (validated, not frozen)
end
```

Custom **discounts** from an adjuster must use `kind: 'manual'` (`Spree::Discount::KINDS` is frozen to `promotion`/`manual`) and attach to a line item or fulfillment. Don't write `kind: 'promotion'` rows — the promotion adjuster deletes rows it didn't create.

Fees written by an adjuster are taxed in the same pass (the provider runs after adjusters).

## Duties

A customs duty is a `Spree::Fee` with `kind: 'duty'`, written by a landed-cost integration (typically an adjuster). Rules:

- Not in the default taxable set (`purchase.taxable_items` excludes duties) — import VAT, if any, is written by the duty provider itself as a tax line against the duty fee.
- Snapshot the inputs (HS code, origin, rate) in the fee's `metadata`; never recompute a placed order's duty.
- Variants carry `hs_code`, `country_of_origin` (manufacture, not ship-from), `customs_description`.

## Rendering totals (Store API / SDK)

Money is a **string** (`"135.60"`) plus a pre-formatted `display_*` twin (`"$135.60"`). Render `display_*`; if you must do math, use a decimal library or integer cents — never JS floats.

```typescript
cart.display_item_total      // items
cart.display_discount_total  // negative
cart.display_delivery_total
cart.display_fee_total       // cart.fees[] for line-by-line (label, kind, display_amount)
cart.display_tax_total       // safe single tax line (included + additional)
cart.display_total
cart.display_amount_due      // after gift cards / store credit
```

- Building your own subtotal? Add **`additional_tax_total` only** — never `included_tax_total` (it's inside the prices already). The #1 European-storefront bug.
- List fees between subtotal and total; they're already in `total`, don't add them again. Show `duty` fees under their own label.
- Store API `cart.discounts` / `order.discounts` is a **per-applied-promotion summary** (`name`, `code`, `amount`, `display_amount`, `promotion_id`), not the typed `Spree::Discount` rows; typed rows are on the Admin API (`adminClient.orders.discounts`).
- Gift cards and store credit are payments, not discounts — they reduce `amount_due`, not `total`.
- With hidden prices (gated B2B guests) money attributes serialize as `null`.

## Gotchas

- **`discount_total` counts only `promotion` rows.** Manual discounts (and custom adjuster discounts) are in `adjustment_total` and `total` but not in `discount_total`. If your summary shows `discount_total` + `total`, a manual discount looks like a missing amount — show `item_total + delivery_total + fee_total + additional_tax_total − total` as "Discounts", or list `Spree::Discount` rows.
- **Never write totals columns directly** (`update_column(:total, …)`) — the next recalculation overwrites them. Write rows, then call `recalculate_totals!` / the order services.
- **Never create `TaxLine` rows by hand.** They're replace-all per item by the provider; yours vanish on the next estimate.
- **Changing items unapplies gift cards and checkout store credit** (`Spree::Carts::Recalculate`) — re-apply after edits. A plain totals recalculation (delivery, discounts, tax moving) keeps the gift card and resizes its payment to the new total instead.
- An adjuster that raises aborts the whole recalculation (and the customer's add-to-cart). Keep external calls out of adjusters or rescue inside.
- Don't read `row.order` during checkout — use `row.owner`.

## Where to read further

- `node_modules/@spree/docs/dist/developer/core-concepts/order-totals.md`, `discounts.md`, `fees.md`
- `node_modules/@spree/docs/dist/developer/how-to/custom-promotion.md` — custom adjusters
- Related skills: `spree-taxes`, `spree-promotions`, `spree-checkout`, `spree-returns`, `spree-pricing`
- Source: `spree/core/app/workflows/spree/carts/recalculate_totals.rb`, `spree/core/app/models/spree/adjusters/`, `spree/core/app/models/spree/{tax_line,discount,fee}.rb`
