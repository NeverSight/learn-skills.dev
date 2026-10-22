---
name: spree-fulfillment
description: Use when working with how Spree 6 gets goods to the customer — fulfillments (`ful_`), delivery methods, delivery zones, delivery profiles and origin groups, delivery rates, calculators and carrier rate providers (EasyPost, freight), order routing and stock splitters, partial fulfillment and splitting, shipping labels, tracking/deliveries, carrier tracking webhooks, pickup and digital delivery. Common phrasings include "shipping method", "no delivery rates at checkout", "ship from the nearest warehouse", "custom shipping calculator", "live carrier rates", "mark as shipped", "partial shipment", "tracking number", "carrier webhook", "click and collect", "3PL / WMS integration", "fulfillment stuck unfulfilled", "add a fulfillment status", "fulfillment.fulfilled event", "Spree::Shipment". Returns/exchanges/claims live in spree-returns; stock counts, reservations and transfers in spree-inventory.
---

# Spree Fulfillment

A **fulfillment** (`Spree::Fulfillment`, prefix `ful_`, number `F…`) is one batch of items going to the customer by one delivery method from one stock location — a parcel, a download, or an order waiting at a pickup counter. A cart/order gets one fulfillment per (stock location × delivery profile × splitter output); the customer picks a delivery rate per fulfillment.

Coming from 5.x (`Shipment`, `ShippingMethod`, `StockItem`, shipment state machine)? Constant aliases exist until 6.1, but see **spree-upgrade-5-to-6** — don't write new code against the old names.

## The model graph

```
Cart / Order
  └── Fulfillment (ful_)                 status: unfulfilled → fulfilled → delivered | canceled
        ├── stock_location (sloc_)        where it ships from
        ├── FulfillmentItem (fi_) × n     line_item + variant + quantity; status on_hand/backordered/shipped/returned
        ├── DeliveryRate (dr_) × n        the options offered; one has selected: true
        │     └── DeliveryMethod (dm_)    what the customer picks ("Standard", "Express", "Collect in store")
        ├── Delivery (dlv_) × n           each consignment/parcel: tracking_number, carrier, status
        ├── ShippingLabel (lbl_) × n      postage bought (purchased) or recorded (uploaded)
        └── TaxLine / Discount / Fee      delivery money rows (see spree-order-totals)

Product ──> DeliveryProfile (fp_)        how a product ships: DeliveryProfiles::Shipping | ::Digital
              ├── DeliveryOriginGroup (og_) × n   a named set of stock locations ("EU warehouse")
              ├── DeliveryZone (dz_) × n          where: DeliveryZoneMember (dzm_) country | state | postal_code
              └── DeliveryMethod × n              belongs_to profile + origin group, optional zone
                    ├── calculator                 how much (when priced internally)
                    ├── rate_provider              where the price comes from (default Internal)
                    ├── fulfillment_provider       how it's dispatched (Manual | Digital | Pickup | PickupPoint | carrier gem)
                    └── DeliveryMethodRule (dmrule_) × n   eligibility, AND-ed

PackageType (pkgtype_)                    box/envelope/carton/pallet/container — tare + dimensions for quotes
```

Things to internalize:

- **Every fulfillment has exactly one owner** — `cart_id` during checkout, `order_id` after placement. Read `fulfillment.owner`, never assume `.order`.
- **Delivery type comes from the method's fulfillment provider class**, not a string column: `delivery_method.digital?`, `.pickup?`, `.pickup_point?`, `.requires_address?`. The API exposes `fulfillment_type` (`shipping | digital | pickup | pickup_point`) on the fulfillment.
- **The delivery profile decides what a product can use.** A digital profile only accepts digital providers; a shipping profile accepts everything else. Origin groups narrow which locations may source the product — the coordinator never packs a product from a location its profile doesn't cover.
- `cart.delivery_step_required?` is `line_items.any? && !digital?` — an all-digital cart skips delivery. `shipping_address_required?` asks the selected methods (or the profiles, before a method is chosen) — a shipping profile offering only pickup needs no address.
- **Delivery zones are delivery-only.** Tax zones are separate (spree-taxes).

## Statuses

`Spree::Fulfillment` uses `has_status :unfulfilled, :fulfilled, :delivered, :canceled` — a string `status` column, no state machine. Statuses describe what *the merchant* did with the parcel and only move forward:

| Status | Meaning |
|---|---|
| `unfulfilled` | Still with you |
| `fulfilled` | Handed over (carrier, pickup counter, or download made available); `fulfilled_at` set |
| `delivered` | Customer has it; `delivered_at` set (from the carrier's scan, not webhook arrival) |
| `canceled` | Won't be sent. Final — there is no resume |

Payment/backorder readiness is **not** a status. It is checked by `Spree::Fulfillments::Fulfill` at the moment you ship, and returns a reason (`order_not_paid`, `backordered_units`, `insufficient_stock_on_hand`, `order_draft`). Staff pass `force: true` to ship against an unpaid invoice or past a backorder (never past a draft order). `can_fulfill?` / `can_cancel?` are phrased negatively ("not already gone out"), so custom pre-handover statuses stay fulfillable.

Carrier truth lives on each **`Spree::Delivery`** (`Spree::Delivery::STATUSES`: `pending pre_transit in_transit out_for_delivery available_for_pickup delivered return_to_sender failure unknown`) and never moves the fulfillment backwards. The fulfillment becomes `delivered` when every consignment has arrived. `tracking` / `tracking_url` on the fulfillment summarize the first delivery.

The order rolls this up into `order.fulfillment_status` (written only by `Spree::Orders::UpdateStatuses`): `unfulfilled`, `partial`, `fulfilled`, `delivered`, `backorder`, `canceled`. Don't write it yourself.

## Transitions are workflows

Never `update!(status: 'fulfilled')`. Call the workflow through its DI key so apps can swap it:

| Action | Workflow (`Spree.<key>`) | Hooks |
|---|---|---|
| Ship (whole or partial) | `fulfillment_fulfill_workflow` → `Spree::Fulfillments::Fulfill` | `validate`, `after_fulfill` |
| Confirm receipt | `fulfillment_mark_delivered_workflow` → `Fulfillments::MarkDelivered` | `validate`, `after_mark_delivered` |
| Cancel | `fulfillment_cancel_workflow` → `Fulfillments::Cancel` | `validate`, `after_cancel` |
| Manual/3PL fulfillment on a placed order | `fulfillment_create_workflow` → `Fulfillments::Create` | `validate`, `get_provider_data`, `after_create` |
| Edit (tracking, rate, location) | `fulfillment_update_workflow` → `Fulfillments::Update` | |
| Buy a label ahead of dispatch | `fulfillment_purchase_label_workflow` → `Fulfillments::PurchaseLabel` | |
| Carrier tracking update | `delivery_update_tracking_workflow` → `Deliveries::UpdateTracking` | `validate`, `after_update_tracking` |

```ruby
result = Spree.fulfillment_fulfill_workflow.call(
  fulfillment: fulfillment,
  items: [{ line_item: line_item, quantity: 1 }], # omit to ship everything
  tracking: '1Z999AA10123456784',                # becomes the primary Spree::Delivery
  notify_customer: true,
  force: false
)
result.value # the fulfillment that actually shipped — for a partial ship, the NEW split-off one
```

What `Fulfill` does, in order: `validate` hook → guards → split off requested units (via `Fulfillments::Create`, cost 0) → record tracking → buy a label if the provider `generates_labels?` and none is active (failure is reported, parcel still ships) → `provider.create_fulfillment` → unstock allocated units (`shipped` movements) → mark items `shipped` + fulfillment `fulfilled` + publish `fulfillment.fulfilled` → capture payments whose method charges on dispatch → roll up order statuses.

**Manual fulfillments** (mirroring a 3PL or courier back into Spree): `POST /api/v3/admin/orders/:order_id/fulfillments` with `stock_location_id`, `items: [{ item_id: 'li_…', quantity }]`, optional `tracking`, `delivery_method_id`, `cost`, `status`, `metadata`. Units move out of their current fulfillments (restock/unstock when locations differ); emptied sources are destroyed and their cost carries over. Quirk: the only accepted `status` value is the legacy `'shipped'` (registers it already fulfilled); anything else fails `invalid_status`.

**Splitting without shipping**: `PATCH …/fulfillments/:id/split` takes `variant_id`, `quantity`, optional `stock_location_id` (moves units to a new fulfillment, possibly at another location) and returns every fulfillment on the order.

## Gating and custom stages

Gate handover with a validate hook — handlers receive the workflow and call `reject!`:

```ruby
# config/initializers/spree.rb
Spree.hooks.register('fulfillments.fulfill.validate') do |flow|
  work_order = MyApp::WorkOrder.find_by(fulfillment_id: flow.fulfillment.id)
  flow.reject!('Still in production') unless work_order&.completed?
end
```

Hook keys are `<workflow key>.<hook>` where the workflow key is the class name minus `Spree::`, underscored and dotted (`Spree::Fulfillments::Fulfill` → `fulfillments.fulfill`). Unknown keys fail boot when eager loading.

Add a real status only when staff filter by it, reports group by it, or webhooks should fire on it:

```ruby
# config/initializers/spree.rb — to_prepare so it survives dev reloads
Rails.application.config.to_prepare do
  Spree::Fulfillment.add_status('in_production', after: 'unfulfilled')
end
```

That gives `in_production?`, `.in_production` and a valid value. Moving into it is your own `Spree::Workflow` (see spree-workflows); core fulfill/cancel keep working on it. Statuses are additive only — never remove a core one.

## Rates: calculators vs rate providers

Every `DeliveryMethod` has a `rate_provider` (class name string, validated against `Spree.delivery_rate_providers`) and a calculator:

| Need | Use |
|---|---|
| Arithmetic on what's in the parcel (flat, per item, % of item total, price sack, flexi, free for digital) | A **calculator** — built-ins under `Spree::Calculator::Shipping::*` |
| A price that comes from outside Spree (carrier API, aggregator, contract rate card service) | A **rate provider** — `Spree::DeliveryRateProvider::Base` subclass |
| "Quoted after review" (pallets, containers) | `Spree::DeliveryRateProvider::Freight` — returns an `unpriced` rate carrying the freight summary |
| "Only offer this when …" (order value, weight, volume, company buyer, channel, excluded products) | A **DeliveryMethodRule** on the method, not calculator thresholds (the calculator `minimum_*`/`maximum_*` preferences are deprecated) |

Default provider is `Spree::DeliveryRateProvider::Internal` (prices via the calculator). Amount-based calculators carry a `currency` preference — a calculator whose currency doesn't match the order contributes nothing (no conversion). Create one method or calculator per currency you sell in. Rate-provider estimates in another currency are dropped by `Spree::Stock::Estimator` for the same reason.

Custom calculator:

```ruby
class MyApp::Calculator::DimensionalWeight < Spree::ShippingCalculator
  preference :rate_per_kg, :decimal, default: 0
  preference :currency, :string, default: -> { Spree::Store.default&.default_currency }

  def self.description = 'Dimensional weight'

  def supports_currency?(currency) = currency.casecmp?(preferred_currency)

  def compute_package(package)
    package.weight * preferred_rate_per_kg # nil hides the method
  end
end

# config/initializers/spree.rb — core ASSIGNS this list in after_initialize, so append there
Rails.application.config.after_initialize do
  Spree.calculators.shipping_methods << MyApp::Calculator::DimensionalWeight
end
```

Custom carrier rate provider (full contract, service catalog and testing in `references/provider-contracts.md`):

```ruby
module SpreeAcme
  class DeliveryRateProvider < Spree::DeliveryRateProvider::Base
    def self.integration_class = 'SpreeAcme::Integration' # hidden/refused until connected
    def self.requires_address? = true                        # it quotes real shipments

    def estimates(package)
      integration.client.rates(from: package.stock_location, to: package.order.ship_address, weight: package.weight).map do |q|
        Spree::DeliveryRateProvider::Estimate.new(
          cost: q.amount, currency: q.currency, carrier: q.carrier,
          service_level: q.service, estimated_delivery_date: q.eta, metadata: { quote_id: q.id }
        )
      end
    rescue SpreeAcme::Error => e
      Rails.error.report(e, source: 'acme.rating')
      [] # never raise into checkout — an empty array hides the method
    end
  end
end

Rails.application.config.after_initialize do
  Spree.integrations << 'SpreeAcme::Integration'
  Spree.delivery_rate_providers << SpreeAcme::DeliveryRateProvider
end
```

`cost` is pre-tax; Spree applies tax afterwards. The reference implementation is the `spree_easypost` gem (`SpreeEasyPost::DeliveryRateProvider` + `SpreeEasyPost::FulfillmentProvider` + `SpreeEasyPost::Integration`).

## Fulfillment providers (dispatch, labels, 3PL/WMS)

`delivery_method.fulfillment_provider` (default `Spree::FulfillmentProvider::Manual`; also `Digital`, `Pickup`, `PickupPoint`) owns the outbound mechanics. A WMS/3PL/carrier integration subclasses `Spree::FulfillmentProvider::Base` and implements `create_fulfillment(fulfillment)` (return `{ tracking_number:, tracking_url: }` optionally) and `cancel_fulfillment(fulfillment)`; label-generating carriers also override `self.generates_labels?`, `purchase_label(owner)` (owner is a `Fulfillment` or a `Return`), `refund_label(label)`, and optionally `tracking_url(delivery)`, `documents(owner)`, `can_fulfill?(fulfillment)`. Register in `after_initialize`: `Spree.fulfillment_providers << MyProvider` (core assigns that list too).

**Carrier tracking webhook**: Spree owns `POST /api/v3/webhooks/fulfillments/:integration_id` (prefixed integration ID, no API key). The integration is looked up by ID alone and the request runs in the integration's own store (`Spree::Current.store = integration.store`), so one URL per integration works for every store. Your `Spree::Integration` subclass implements `parse_webhook_event(raw_post, headers)`: verify the signature (raise `Spree::Integration::WebhookSignatureError` → 401, also when no secret is configured), return `{ tracking_code:, tracking_status:, estimated_delivery_at:, delivered_at:, details: }` or `nil` to ignore (→ 200). The controller finds the `Spree::Delivery` in the integration's store by tracking number and runs `Deliveries::UpdateTracking`; a `delivered` status confirms receipt on the fulfillment. Map unknown carrier statuses to `'unknown'`.

## Order routing and stock splitters

Two layers decide how items become fulfillments:

1. **Which stock locations** — order routing. `Spree::OrderRouting::Strategy::Rules` (default) walks the channel's `Spree::OrderRoutingRule` rows (`PreferredLocation`, `MinimizeSplits`, `DefaultLocation`; lower rank wins, `nil` abstains). Custom rule: subclass `Spree::OrderRoutingRule`, implement `rank(order, locations)` returning one `LocationRanking` per location, register via `Spree.order_routing.rules << MyRule`, create a row per channel. Custom strategy: subclass `Spree::OrderRouting::Strategy::Base`, implement `for_allocation` (returns `Spree::Stock::Package`s) plus `for_sale(fulfillment:)`, `for_release`, `for_cancellation`; register via `Spree.order_routing.strategies << MyStrategy`, select with `store.preferred_order_routing_strategy` / `channel.preferred_order_routing_strategy` (unregistered values fall back to Rules).
2. **How one location's allocation is broken into packages** — splitters. Default chain `Spree.stock_splitters = [Splitter::DeliveryProfile, Splitter::Backordered]`; `Splitter::Weight` (class-level `threshold`, default 150) is opt-in. Custom: subclass `Spree::Stock::Splitter::Base`, implement `split(packages)` and always end with `return_next(packages)`.

**Know where routing actually applies.** Storefront checkout builds fulfillments with `Cart#rebuild_fulfillments!`, which calls `Spree::Stock::Coordinator` directly — it respects delivery-profile origin groups, the channel's served locations and the splitter chain, but **does not consult the routing strategy or routing rules**. `Carts::Complete` copies the cart's fulfillments onto the order. The routing strategy runs in `Order#rebuild_fulfillments!` — admin draft-order create/update (`Spree::Orders::BuildFulfillments`, a no-op once the order is placed) and `OrderInventory` changes on placed orders. Editing a placed order's items never rebuilds its fulfillments — `Spree::OrderInventory` adjusts them in place, so the allocations made at placement stay on rows that cancel/ship can still release. The strategy's `for_sale`/`for_release`/`for_cancellation` are part of the contract but core does not call them today (Rules implements them as no-ops) — do post-allocation side effects in fulfillment workflow hooks or `fulfillment.*` subscribers instead. Claim/exchange replacements also use the Coordinator. To change which warehouse storefront carts ship from, use delivery profiles/origin groups, channel stock locations, or a decorator on the Coordinator — not a routing rule alone.

```ruby
# Splitters are assigned by core in after_initialize — append there, not in to_prepare
Rails.application.config.after_initialize do
  Spree.stock_splitters << MyApp::Stock::Splitter::Refrigerated
end
```

## Pickup, digital, freight

- **Pickup**: methods with `FulfillmentProvider::Pickup` serve pickup-enabled stock locations (`GET /api/v3/store/delivery_methods/:id/pickup_locations`); `PickupPoint` asks a pickup point provider (`…/pickup_points?latitude=&longitude=`). Pickup orders are closed out with mark-delivered.
- **Digital**: assign the product the store's digital delivery profile. The `Digital` fulfillment provider auto-fulfills on placement and grants `Spree::DigitalLink`s (event `digital_link.downloaded`). Deliver something other than an uploaded file via a `Spree::DigitalAssetProvider::Base` subclass (`deliver(digital_link, expires_in:)`), registered in `Spree.digital_asset_providers`.
- **Freight**: methods on the `Freight` rate provider bounded by `volume_rule` / `company_rule`; rates come back `unpriced: true`, display "Quoted after review", sort after priced rates, and checkout still completes.

## API surface

- Store: `PATCH /api/v3/store/carts/:cart_id/fulfillments/:id` with `selected_delivery_rate_id`; rates are on `cart.fulfillments[].delivery_rates`.
- The choice survives item changes. Every recalculation rebuilds the proposals (`rebuild_fulfillments!`), and the rebuild carries each stock location's selected rate over (same carrier service, else same method, else the estimator's default) and prices it for the new contents. Only a destination change (`Address::DESTINATION_FIELDS`: address lines, city, state, postal code, country) resets to the default rate; a phone or name edit keeps it. A placed order's delivery isn't re-priced by a rebuild.
- Admin — permission keys: `read_/write_fulfillments` for the fulfillments endpoints (nested labels/deliveries sit under `*_orders`), `*_delivery_methods` for methods/rules, `*_package_types`, `*_settings` for zones and profiles. Endpoints: `…/orders/:order_id/fulfillments` (index/show/create/update) + member `fulfill` (`items: [{ item_id, quantity }]`, `tracking`, `tracking_carrier`, `notify_customer`, `force`), `mark_delivered`, `cancel`, `split`; nested `labels` (create/destroy, `download`, `refund`) and `deliveries` (CRUD, `mark_delivered`). Setup: `delivery_methods` (+ `calculators`, `rate_providers`, `fulfillment_providers`, nested `rules`), `delivery_method_rules/types`, `delivery_zones`, `delivery_profiles` (+ `kinds`, nested `origin_groups`), `package_types`, `tracking_carriers`.
- Admin SDK: `adminClient.orders.fulfillments.{list,fulfill,markDelivered,cancel,split}`, `.labels.*`, `.deliveries.*`.

## Events

`fulfillment.created/updated/deleted`, `fulfillment.fulfilled` (metadata `notify_customer`), `fulfillment.delivered`, `fulfillment.canceled`; `delivery.created/updated/deleted`; `shipping_label.purchased/.refunded` (+ lifecycle); order-level `order.fulfilled`, `order.delivered`. There is no `fulfillment.resumed`. Use subscribers for WMS sync and emails (spree-events-webhooks).

## Troubleshooting

**No delivery rates at checkout** (cart shows a `delivery_unavailable` warning, fulfillment pruned):
- The product's delivery profile has no method whose zone (or origin group) covers the address / source location.
- A `DeliveryMethodRule` excludes the package (item total, weight, volume, company, channel).
- Calculator currency ≠ cart currency, or the calculator returned `nil`.
- The rate provider's integration isn't connected, it raised (check error reports), or it returned only foreign-currency estimates.
- Console: `Spree::Stock::Coordinator.new(cart).packages.map { |p| [p.stock_location.name, p.delivery_rates.map(&:name)] }`, or `Spree::Stock::Estimator.new(cart).delivery_rates(package, Spree::DeliveryMethod::BACKOFFICE)` to include admin-only methods.

**Fulfill returns 422**: read the error — unpaid (`force` or capture first), backordered units, not enough `count_on_hand` at the location (correct stock, or `force`), draft order, or your own `validate` hook.

**Ships from the wrong warehouse**: storefront carts ignore routing rules (see above) — check the product's delivery profile origin groups, the channel's stock locations, and `StockLevel` presence at each location.

**Tracking webhook does nothing**: the endpoint answers 200 for unknown tracking codes and `nil` events by design; 401 means signature verification failed; the integration must be active in the current store.

## Testing

Factories (spree_dev_tools / `spree/testing_support`): `:fulfillment`, `:fulfillment_item`, `:delivery_method`, `:free_delivery_method`, `:digital_delivery_method`, `:pickup_delivery_method`, `:delivery_zone`, `:delivery_zone_with_country`, `:delivery_profile`, `:digital_delivery_profile`, `:delivery_rate`, `:delivery`, `:stock_package`, `:cart_ready_for_delivery`, `:completed_order_with_totals`. Stub carrier clients — rate quoting runs on every checkout. Set `Spree::Current.store` in specs that build rates outside a request.

## Where to read further

- `node_modules/@spree/docs/dist/developer/core-concepts/fulfillments.md`, `delivery-setup.md`, `freight.md`, `calculators.md`
- `node_modules/@spree/docs/dist/developer/how-to/custom-delivery-rate-provider.md`, `custom-order-routing.md`, `custom-stock-splitter.md`, `sell-digital-products.md`, `custom-digital-asset-provider.md`
- `node_modules/@spree/docs/dist/developer/providers/fulfillment.md`; EasyPost setup: `node_modules/@spree/docs/dist/integrations/shipping/easypost.md`
- Deeper contracts: [`references/provider-contracts.md`](references/provider-contracts.md)
- Related skills: spree-inventory (stock levels, reservations, movements), spree-returns, spree-workflows (hooks, custom workflows), spree-providers, spree-checkout, spree-order-totals.
