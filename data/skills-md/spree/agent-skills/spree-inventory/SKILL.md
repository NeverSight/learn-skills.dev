---
name: spree-inventory
description: Use when working with stock in Spree 6 — StockLevel counters (count_on_hand, allocated_count, reserved_count, incoming_count, available/purchasable), stock locations (kind, pickup_enabled, returns_enabled), stock movements and their kinds, checkout stock reservations and their expiry job, backorders, inventory tracking on/off, bulk stock sync from an ERP/WMS (bulk_upsert), stock transfers, suppliers, purchase orders and stock receipts, the spree:stock:recount_levels task, and stock_level events. Common phrasings include "stock count is wrong", "oversold", "sync inventory from ERP", "update stock via API", "reserve stock at checkout", "stock reservation expired", "backorder", "restock", "move stock between warehouses", "purchase order", "receive a delivery", "incoming stock", "StockItem", "count_on_hand", "out of stock".
---

# Spree Inventory

Stock is tracked **per variant per location**. A variant has no single stock count — it has a `Spree::StockLevel` (`sl_`) at each `Spree::StockLocation` (`sloc_`) that carries it. Every change is a `Spree::StockMovement` (`sm_`) that names its cause.

Coming from 5.x (`Spree::StockItem`, stock decremented at order completion, `Spree::StockMovement` with a bare signed quantity)? The alias `Spree::StockItem = Spree::StockLevel` exists until 6.1 — write new code against `StockLevel`. See **spree-upgrade-5-to-6**.

## The counters

| Column / method | Meaning | Written by |
|---|---|---|
| `count_on_hand` | Physically on the shelf | `received`, `adjusted` and `shipped` movements only |
| `allocated_count` | Promised to placed orders not yet shipped | `allocated` (+), `released` / `shipped` (−) movements |
| `reserved_count` | Held by carts in checkout | Reservation create/update/destroy (counter cache) |
| `incoming_count` | On a purchase order marked ordered or a transfer in transit, not yet received | PO / transfer workflows |
| `available_count` (method) | `count_on_hand − allocated_count` | derived |
| `purchasable_count` (method) | `available_count − reserved_count` | derived |
| `backorderable` | May sell past zero | admin / API |

**Placing an order does not reduce `count_on_hand`.** `Spree::Orders::Complete` allocates each fulfillment's units (`allocated` movement → `allocated_count` up). Stock physically leaves only when the fulfillment ships (`Spree::Fulfillments::Fulfill` → `shipped` movement: on hand down, allocation retired). Canceling releases the allocation (`released`) — including units added by editing a placed order, because edits adjust the existing fulfillments in place (`Spree::OrderInventory`) instead of rebuilding them. Overselling shows up as `allocated_count > count_on_hand`, never a negative shelf count. So "the website still shows 10 on hand after I sold 3" is correct — look at `available_count`.

`reserved_count` and `incoming_count` are cached counters. If they drift (manual SQL, crashed jobs), recompute them — the task also sweeps expired reservations and prints every corrected row:

```bash
spree rake spree:stock:recount_levels        # classic: bin/rake spree:stock:recount_levels
```

(Service: `Spree.stock_level_recount_service`.)

Availability for shoppers is computed for you: Store API variants expose `in_stock` and `purchasable` (in stock or backorderable), already net of allocations and other shoppers' reservations. In Ruby, `Spree::Stock::Quantifier.new(variant).can_supply?(qty)` / `total_on_hand` does the same arithmetic; `variant.in_stock?`, `variant.purchasable?`, `variant.backorderable?`. `StockLevel` scopes: `in_stock`, `out_of_stock`, `low_stock(threshold)` (store `preferred_low_stock_threshold`, default 5), `with_incoming`, `with_reserved`, and the ransackable `with_stock_status`.

## Stock locations

| Attribute | Notes |
|---|---|
| `name`, `code`, `active`, `default` | Inactive locations are skipped for new allocations |
| `kind` | `warehouse`, `store`, `fulfillment_center` (`StockLocation::KINDS`, the built-in options) |
| address fields (`country_code`, `state_code`, `city`, `postal_code`, …) | Rates origin, proximity |
| `backorderable_default` | Default `backorderable` for new stock levels here |
| `propagate_all_variants` | On create, builds a stock level for every variant **of the location's store** (a seller's location: only that seller's variants); new variants get levels at such locations too |
| `pickup_enabled` | Customers can collect here (pickup delivery methods) |
| `returns_enabled` | Returns may be received here (see spree-returns) |

Which locations may source a product is decided by its delivery profile's origin groups and the channel's served locations (spree-fulfillment), not by the stock level alone.

Programmatic moves — always through the location, which records the movement and updates counters under a row lock:

```ruby
location.restock(variant, 10, purchase_order, unit_cost: 12.5) # 'received'
location.adjust(variant, -2, reason: 'damaged')                 # 'adjusted' — reason required
location.allocate(variant, 1, fulfillment)                      # 'allocated' (core calls this)
location.release(variant, 1, fulfillment)                       # 'released'  (core calls this)
location.unstock(variant, 1, fulfillment)                       # 'shipped'   (core calls this)
location.stock_level_or_create(variant)
```

Never `stock_level.update!(count_on_hand: …)` or `update_column` — it skips the movement ledger (no audit trail), backorder filling and the variant touch that busts caches.

## Stock movements

`Spree::StockMovement::KINDS = %w[received allocated shipped released adjusted]`. `allocated`/`shipped`/`released` are written positive (the kind carries the direction); `received`/`adjusted` keep their sign; `adjusted` requires a `reason` (conventional values in `StockMovement::ADJUSTMENT_REASONS`: `manual_adjustment correction count received return_restock damaged theft_or_loss promotion_or_donation inventory_feed`, free text also accepted). Movements point at their cause (fulfillment, return, transfer, purchase order, stock receipt) and received purchase-order stock carries `unit_cost`. Movements are an immutable ledger — correct mistakes with a new `adjusted` movement.

## Reservations during checkout

A `Spree::StockReservation` (`res_`) is a short hold on a stock level for a cart line item:

| Moment | What happens |
|---|---|
| Cart enters checkout (gets an email or ship address) | `Spree::StockReservations::Reserve` holds every tracked, non-backorderable, non-preorder line; fails with insufficient stock |
| Cart edited while in checkout (items added/changed, address updated) | Re-reserve / `Extend` pushes `expires_at` forward |
| Cart leaves checkout | `Release` |
| Cart completes | `Orders::Complete` releases the holds and allocates the fulfillments' units instead |
| Abandoned | Expire; `reserved_count` returns |

Store settings: `preferred_stock_reservations_enabled` (default true) and `preferred_stock_reservation_ttl_minutes` (default 10). Reservations never touch `count_on_hand`.

**Schedule the expiry job yourself.** Spree ships `Spree::StockReservations::ExpireJob` but doesn't run it. With Solid Queue (default) add it to `config/recurring.yml`; with Sidekiq use sidekiq-cron:

```yaml
# config/recurring.yml (Solid Queue)
production:
  expire_stock_reservations:
    class: Spree::StockReservations::ExpireJob
    schedule: every minute
```

Without it, expired holds still stop counting at read time, but rows and `reserved_count` linger until the next recount.

## Backorders

A `backorderable` level can sell past zero: the order is accepted and its fulfillment items are `backordered`. When stock arrives (`count_on_hand` increases), backordered units at that location are filled first — oldest order first — then the remainder becomes available. `Fulfillments::Fulfill` refuses a fulfillment holding backordered units unless `force: true`. Backorderable lines are not reserved at checkout.

## Tracking on/off

`variant.should_track_inventory?` is `variant.track_inventory? && store.preferred_track_inventory_levels`. Untracked variants are always purchasable and their movements don't change counters (except `adjusted`). Use it for services, made-to-order goods and digital products.

## Admin API (permission keys `read_stock` / `write_stock`)

```bash
GET   /api/v3/admin/stock_levels?q[stock_location_id_eq]=sloc_…&q[with_stock_status][]=low_stock
PATCH /api/v3/admin/stock_levels/sl_…            { "count_on_hand": 150, "reason": "count" }   # absolute
PATCH /api/v3/admin/stock_levels/sl_…            { "adjustment": -2, "reason": "damaged" }      # relative
POST  /api/v3/admin/stock_levels/bulk_upsert     { "stock_levels": [ { "variant_id": "variant_…", "stock_location_id": "sloc_…", "count_on_hand": 40, "backorderable": false } ] }
GET   /api/v3/admin/stock_movements?q[stock_level_variant_id_eq]=variant_…
GET   /api/v3/admin/stock_reservations
      /api/v3/admin/stock_locations                (CRUD)
```

`count_on_hand` and `adjustment` are mutually exclusive. **Use `bulk_upsert` for ERP/WMS feeds**, not a loop of PATCHes: it takes absolute (`count_on_hand`) or relative (`adjustment`) rows, last write wins per (variant, location), creates missing levels, records one `adjusted` movement per change with reason `inventory_feed`, and runs in one transaction — an unreadable row fails the whole batch rather than half-applying. Sending `"stock_levels": []` is a no-op; omitting the key is a 422. In Ruby: `Spree.stock_level_bulk_upsert_service.call(rows: [...])` (IDs are internal integers there) and `Spree.stock_level_correct_service.call(stock_level:, count_on_hand: | adjustment:, reason:)`.

TypeScript: `adminClient.stockLevels.list/update/bulkUpsert(...)`, `adminClient.stockMovements.list(...)`.

If stock truth lives in an external system, keep syncing a local snapshot (bulk upsert) — **the read path stays local**. For live checks at decision points (add to cart, reserve, complete) there is an inventory provider contract: `Spree::InventoryProvider::Base#stock_levels_for(variant, stock_location:)` returning unsaved StockLevel rows, registered in `Spree.inventory_providers` and selected by `store.preferred_inventory_provider` (default `'internal'`) with a failure policy. See spree-providers.

## Stock transfers (moving stock you own)

`Spree::StockTransfer` (`st_`) — statuses `draft → ready_to_ship → in_transit → partially_received / received / over_received`, or `canceled`. Items `Spree::StockTransferItem` (`sti_`, `quantity_shipped`).

- Units leave the source (a `shipped` movement caused by the transfer) and count as `incoming` at the destination **when marked in transit**, not when drafted.
- Destination availability rises only when a **stock receipt** counts them in.
- Canceling after departure requires `on_in_transit: 'restock'` (back to source) or `'write_off'`.
- `close` settles a short delivery (`closed_short_at` + reason); nothing moves.

Workflows (`Spree.stock_transfer_*_workflow`): `Create`, `Update`, `MarkReady`, `MarkInTransit` (hooks `validate`, `before_unstock`, `after_mark_in_transit`; `force:`), `Receive` (`validate`, `before_restock`, `after_receive`), `Cancel`, `MarkDraft`, `Close`.

API: `/api/v3/admin/stock_transfers` (CRUD; create with `source_location_id`, `destination_location_id`, `items: [{ variant_id, quantity_shipped }]`) + `PATCH mark_ready | mark_in_transit | mark_draft | close | cancel`, and `POST …/stock_transfers/:id/stock_receipts`.

## Purchase orders and suppliers (buying stock in)

`Spree::Supplier` (`sup_`) is a per-store address book. `Spree::PurchaseOrder` (`po_`) — `draft → ordered → partially_received / received / over_received`, or `canceled`; items `Spree::PurchaseOrderItem` (`poi_`, `quantity_ordered`, `unit_cost`); `expected_at`, `cancel_by` (calendar dates; nothing auto-cancels). Marking ordered adds to `incoming_count`; ordered stock is never available until received. Received units land as `received` movements carrying `unit_cost`. CSV export/import of POs is supported.

Workflows (`Spree.purchase_order_*_workflow`): `Create`, `Update`, `MarkOrdered`, `Receive` (`validate`, `before_restock`, `after_receive`), `Cancel`, `MarkDraft`, `Close` — each with a `validate` hook, e.g. `purchase_orders.mark_ordered.validate` for an approval limit.

API (permission keys `read_purchasing` / `write_purchasing` — deliberately separate from `write_stock`): `/api/v3/admin/suppliers` (CRUD), `/api/v3/admin/purchase_orders` (CRUD; create with `supplier_id`, `destination_location_id`, `expected_at`, `cancel_by`, `items: [{ variant_id, quantity_ordered, unit_cost }]`) + `PATCH mark_ordered | mark_draft | close | cancel`, `POST …/purchase_orders/:id/stock_receipts`.

## Stock receipts

Both documents are received the same way: each physical delivery is a `Spree::StockReceipt` (`sr_`) with a `reference` (packing slip) and per-line `Spree::StockReceiptItem` (`sri_`) counts:

```json
{ "reference": "DN-4471",
  "items": [{ "id": "poi_…", "quantity_accepted": 58, "quantity_rejected": 2, "rejection_reason": "damaged" }] }
```

`id` is the PO/transfer line (`poi_…` / `sti_…`). Counts are this delivery's, not running totals. Omit `items` to receive everything outstanding intact. `rejection_reason`: `damaged`, `wrong_item`, `expired`, `other`. Refused PO units are still owed by the supplier; refused transfer units have "arrived" (the trip is over).

## Events

`stock_level.created/.updated/.deleted` (legacy `stock_item.*` names are dual-emitted until 6.1), `stock_movement.*`, `stock_reservation.*`, `stock_transfer.*` (+ `draft`, `ready_to_ship`, `shipped`, `partially_received`, `received`, `over_received`, `canceled`), `purchase_order.*` (+ `draft`, `ordered`, `partially_received`, `received`, `over_received`, `canceled`), `stock_receipt.*`, `supplier.*`. A `stock_level.updated` subscriber is the usual hook for back-in-stock notifications or pushing counts to a marketplace channel — compute availability from the payload/record, and remember counter-only writes (allocation/reservation) also touch the level.

## Gotchas

- Scope everything to the store: `Spree::StockLevel.for_store(store)`, `store.stock_locations` — never unscoped `Spree::StockLevel.all` in a multi-store app.
- Don't mutate counters directly (`update_column(:count_on_hand, …)`, `increment!(:reserved_count)`); use `restock`/`adjust`/services or the API. If you did, run `spree:stock:recount_levels` (fixes reserved/incoming only — on hand/allocated are the ledger's job; fix those with an `adjust`).
- "In stock" in admin lists and `StockLevel.in_stock` subtract reservations; `StockLevel#in_stock?` / `available_count` don't. Pick the figure that matches the question.
- Jobs, rake tasks and console scripts must set `Spree::Current.store` — `Spree::Store.default` can be nil and store preferences (reservation TTL, tracking, low-stock threshold) read through it.
- Registering custom stock splitters belongs in `Rails.application.config.after_initialize` (core reassigns `Spree.stock_splitters` there) — see spree-fulfillment.

## Testing

Factories: `:stock_location`, `:stock_location_with_items`, `:stock_level`, `:stock_movement`, `:stock_reservation`, `:stock_transfer`, `:stock_transfer_item`, `:purchase_order`, `:purchase_order_item`, `:stock_receipt`, `:stock_receipt_item`, `:supplier`. Set stock with `location.stock_level_or_create(variant).set_count_on_hand(10)` or `location.restock(variant, 10)` rather than raw column writes, so the counters and ledger stay consistent in specs.

## Where to read further

- `node_modules/@spree/docs/dist/developer/core-concepts/inventory.md`
- `node_modules/@spree/docs/dist/developer/deployment/background_jobs.md` (scheduling `ExpireJob`)
- `node_modules/@spree/docs/dist/user/inventory/stock-levels.md`, `stock-transfers.md`, `purchase-orders.md`, `suppliers.md`
- Related skills: spree-fulfillment (allocation → shipping, routing, splitters), spree-returns (restocking), spree-checkout (when carts enter checkout), spree-providers, spree-events-webhooks, spree-performance.
