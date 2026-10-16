---
name: spree-taxes
description: Use when the user is configuring or extending tax in Spree 6 — tax categories (`tax_code`), tax rates by `country_code`/`state_code`, VAT-inclusive vs added-on pricing (`included_in_price`, market `tax_inclusive`), per-market tax providers and `Spree.default_tax_provider`, writing a custom tax provider (`estimate`/`commit`/`void`/`refund`), `Spree::TaxLine` rows, the `carts.recalculate_totals.set_tax_line_context` hook, B2B tax identifiers (VAT numbers) and exemption certificates, or connecting Avalara/an external tax engine. Common phrasings include "tax not calculated", "tax is zero", "VAT included in price", "EU VAT", "US sales tax", "tax per state", "integrate Avalara / TaxJar / Stripe Tax", "custom tax calculation", "tax exempt customer", "reverse charge", "VAT number at checkout", "tax on shipping", "tax on fees".
---

# Spree Taxes

Tax in Spree 6 is three separate decisions:

1. **What is sold** → `Spree::TaxCategory` on the product/variant (copied to line items).
2. **Where it goes** → the purchase's tax address (ship address by default) and its **market**.
3. **Who computes it** → the market's **tax provider**, falling back to `Spree.default_tax_provider` (default `Spree::TaxProvider::Internal`, which reads `Spree::TaxRate` rows).

Whatever computes it, the output is always the same: `Spree::TaxLine` rows on the cart/order, folded into `included_tax_total` / `additional_tax_total` by `Spree::Carts::RecalculateTotals` (see `spree-order-totals`).

> Coming from 5.x zones and `Spree::Calculator::DefaultTax`? Tax zones and tax adjustments are gone — see `spree-upgrade-5-to-6`.

## Tax categories

`Spree::TaxCategory` — store-scoped; `name`, `is_default` (one default per store; items with no category use it), `tax_code` (the code an external engine knows it by, e.g. an Avalara tax code). Products/variants reference one; line items snapshot `tax_category_id`. Delivery methods can carry a category for shipping tax; fees without one use the store default.

## Tax rates (Internal provider)

`Spree::TaxRate` (`tax_…`, store-scoped, soft-deleted) has **no zone** — it names its jurisdiction by ISO code:

| Field | Meaning |
|---|---|
| `amount` | Decimal fraction — `0.2` = 20% (`amount_percentage` reads/writes `20`) |
| `country_code` / `state_code` | Where it applies. `nil` country = everywhere; `nil` state = whole country |
| `tax_category` | What it applies to |
| `included_in_price` | `true` = VAT-style, already inside the price; `false` = added on top |
| `name` / `show_rate_in_label` | Label snapshotted onto tax lines (`"VAT 20%"`) |

```ruby
store = Spree::Current.store
standard = Spree::TaxCategory.default(store)
Spree::TaxRate.create!(name: 'VAT', amount: 0.20, country_code: 'DE', tax_category: standard, included_in_price: true)
Spree::TaxRate.create!(name: 'CA sales tax', amount: 0.0725, country_code: 'US', state_code: 'CA', tax_category: standard)
```

Admin API: `/api/v3/admin/tax_categories`, `/api/v3/admin/tax_rates` (`adminClient.taxRates.create({ …, country_code: 'GB', tax_category_id: 'taxcat_…' })`).

Matching: `TaxRate.for_store(store).for_jurisdiction(country, state)` — every rate for the item's category whose country/state match (or are nil) applies, so a country-wide `US` rate and a `US`/`CA` rate both tax a California address. The Internal provider declares `unsupported_capabilities`: `us_local_tax`, `reverse_charge`, `oss_thresholds`, `proportional_delivery_tax` — beyond simple country/state rates, use an external engine.

### Tax address

`purchase.tax_address` is the ship address when the store preference `tax_using_ship_address` is true (default), else the bill address. `purchase.tax_country` falls back to the market's default country, then the store's — which is what lets an inclusive market show real prices before any address exists.

## Included vs added-on

- **`included_in_price` (per rate)** drives the math: included tax is backed out of the gross (`pre_tax_amount` is stored on the item) and lands in `included_tax_total`; additional tax lands in `additional_tax_total` and increases `total`.
- **`Spree::Market#tax_inclusive`** is the market's declaration that its prices are quoted tax-inclusive — exposed on the Store API market so storefronts label prices ("incl. VAT"). Keep it consistent with the rates you configure for that market's countries.
- Cross-border VAT restatement: when a VAT-inclusive price is shown to a customer in another country, `Spree::VatPriceCalculation` removes home VAT and adds the destination's — **only with the Internal provider** (external engines keep no rate rows; use a geo-scoped price list instead, see `spree-pricing`).
- In summaries, never add `included_tax_total` to anything — it's already inside the prices. `tax_total` = included + additional is the safe single line.

## Tax providers

```ruby
cart.tax_provider   # => market&.tax_provider_instance || Spree.default_tax_provider.new
```

- `Spree::Market#tax_provider` is a class-name string, validated against `Spree.tax_providers` (Admin API: `PATCH /api/v3/admin/markets/:id { tax_provider: 'MyTax::Provider' }`; `GET /api/v3/admin/tax_providers` lists installed ones with availability and unsupported capabilities).
- `Spree.default_tax_provider` returns a **class** (accepts a class or string): `Spree.default_tax_provider = 'MyTax::Provider'`.
- Providers are stateless, instantiated fresh per call, no constructor args. Credentials live in a `Spree::Integration` the provider reads at runtime; override `self.available_for_store?(store)` to require it.

### The provider contract (`Spree::TaxProvider::Base`)

| Method | When | Must |
|---|---|---|
| `estimate(owner, items = nil, tax_date:, tax_identifier:, exemptions:, context:)` | Every unfrozen recalculation (cart, draft order); never on placed orders | **Replace-all per item**: delete the items' existing tax lines, write fresh ones — one row per treatment, zero-amount included. `items: nil` = `owner.taxable_items` (line items, fulfillments, non-duty fees). Raise if it can't compute. |
| `commit(order)` | After placement, outside any transaction (`Carts::Complete` finalize) | Be **idempotent** — completion replays; key the filing on the order |
| `void(order)` | Order cancellation | Reverse the committed document |
| `refund(order, return_items, amount:, tax_date:)` | Return refund | Credit no more tax than `amount` actually refunded |
| `service_tax_rate(address:, store:)` | Marketplace commission invoicing | Return a fraction or `nil` (no opinion) |
| `self.unsupported_capabilities` | Admin market pairing | Declare what you can't do (symbols) |
| `self.display_name`, `self.available_for_store?(store)` | Admin | Presentation / gating |

### Writing one

```ruby
# server/app/models/my_tax/provider.rb
module MyTax
  class Provider < Spree::TaxProvider::Base
    def self.display_name = 'MyTax'
    def self.unsupported_capabilities = %i[reverse_charge]

    def estimate(owner, items = nil, tax_date: nil, tax_identifier: nil, exemptions: [], context: {})
      items ||= owner.taxable_items
      return if items.empty?

      quote = MyTax::Client.quote(owner, items, tax_date:, vat_id: tax_identifier&.value, **context)

      items.group_by(&:class).each do |klass, group|
        fk = { Spree::LineItem => :line_item_id, Spree::Fulfillment => :fulfillment_id, Spree::Fee => :fee_id }.fetch(klass)
        Spree::TaxLine.where(fk => group.map(&:id)).delete_all        # replace-all
      end

      owner_key = owner.is_a?(Spree::Order) ? :order : :cart
      quote.lines.each do |line|
        Spree::TaxLine.create!(
          owner_key => owner, line.item_fk => line.item_id,
          amount: line.tax, rate: line.rate, label: line.label,
          included: false, provider_id: 'mytax',
          taxability_reason: line.reason,                     # e.g. 'standard_rated', 'reverse_charge'
          country_code: line.country, state_code: line.state,
          data: { jurisdictions: line.breakdown }             # provider payload, free-form
        )
      end
    end

    def commit(order)
      MyTax::Client.commit(document_code: order.number)       # idempotent by order number
    end

    def void(order) = MyTax::Client.void(document_code: order.number)
  end
end
```

```ruby
# server/config/initializers/spree.rb
Spree.default_tax_provider = 'MyTax::Provider'  # optional fallback for markets naming none (string: no autoload at boot)

Rails.application.config.after_initialize do
  Spree.tax_providers << MyTax::Provider        # selectable per market; app/ classes can't be referenced during boot
end
```

`TaxLine.taxability_reasons` is a class attribute (`standard_rated`, `reduced_rated`, `zero_rated`, `reverse_charge`, `intra_community_supply`, `export`, `customer_exempt`, `product_exempt`, `not_collecting`, `not_subject_to_tax`); add your own with `Spree::TaxLine.taxability_reasons += ['my_reason']`.

Keep network I/O fast and failure-aware: `estimate` runs inside cart writes and inside the completion lock. A raise aborts the recalculation.

### Feeding extra data: `set_tax_line_context`

Anything a provider needs that the typed inputs don't carry (customer usage codes, channel, a quote ID) comes from context handlers. Every handler's returned hash is merged and passed as `context:`.

```ruby
module MyApp
  class AvalaraEntityUseCode
    def call(workflow)
      code = workflow.cart.customer&.metadata&.dig('entity_use_code')
      code ? { entity_use_code: code } : {}
    end
  end
end

Spree.hooks.register('carts.recalculate_totals.set_tax_line_context', 'MyApp::AvalaraEntityUseCode')
# Admin draft-order edits use the twin key: 'orders.recalculate_totals.set_tax_line_context'
```

Don't use context for exemptions or the buyer's VAT number — those are typed inputs (below).

## TaxLine rows

`Spree::TaxLine` (`tl_`): owner (cart or order), exactly one of `line_item` / `fulfillment` / `fee`, `amount`, `rate`, `label`, `included`, `tax_rate` (nil for external), `provider_id`, `taxability_reason`, `country_code` / `state_code`, `data` (JSON). Snapshots — rates edited or deleted later don't change placed orders.

- Written **only** by the provider. Admin API `GET /api/v3/admin/orders/:id/tax_lines` is read-only.
- Copied verbatim from cart to order at completion (no re-estimate); placed orders are money-frozen.
- Tax on delivery → rows on fulfillments; tax on fees → rows on the fee (`fee_id`); duties aren't in the default taxable set.

## B2B: tax identifiers and exemptions

**Tax identifiers** (`Spree::TaxIdentifier`, `txi_`, `kind` + `value`, e.g. `eu_vat` / `NL123456789B01`) can belong to a customer, a company (legal entities only), or a cart (checkout-time override). Resolution: `cart.resolved_tax_identifier` → cart override → company (nearest legal-entity ancestor — never borrowed from a parent) → customer; within each, verified beats most recent. At completion the resolved one is **copied** onto the order (`source`: `override`/`company`/`customer`) and becomes read-only. No identifier = consumer sale (safe default).

- Store API: `GET/PUT/DELETE /api/v3/store/carts/:cart_id/tax_identifier` (PUT needs both `kind` and `value`; re-costs the cart). No SDK helper yet — use `client.request('PUT', \`/carts/${id}/tax_identifier\`, { body: { kind, value }, spreeToken })`.
- Admin: `/api/v3/admin/companies/:id/tax_identifiers` (+ `validate`), `/api/v3/admin/customers/:id/tax_identifiers`.
- Validators per kind: `Spree.tax_identifier_validators['au_abn'] = 'MyApp::AbnValidator'` (subclass `Spree::TaxIdentifiers::Validator::Base`: `self.valid_format?` on save, `call(tax_identifier:)` for registry checks in `Spree::TaxIdentifiers::ValidateJob`). The built-in `eu_vat` validator is **format-only** — plug in a VIES/registry validator if you need verification. Status: `pending`/`verified`/`unverified`/`unavailable`/`unsupported`.
- Reverse charge from a VAT ID is a provider capability — the Internal provider ignores `tax_identifier`.

**Exemptions**: `Spree::TaxExemptionCertificate` on a company legal entity, scoped by `country_code`/`state_code`, counted only when `active` (verified and unexpired). `Spree::Tax::ResolveExemptions` (`Spree.tax_resolve_exemptions_service`) turns them into `Spree::TaxExemption` value objects (`reason_code`, `certificate_number`, jurisdiction, `item_overrides`) passed as `exemptions:`. Exempt items get zero-amount lines with `taxability_reason: 'customer_exempt'`. Swap the service to read certificates from elsewhere (e.g. Avalara's certificate store). See `spree-b2b`.

## Avalara and other engines

Tax engines plug in as a provider class registered in `Spree.tax_providers` and selected per market. For Avalara, see `node_modules/@spree/docs/dist/integrations/tax/avalara.md` — check it describes the provider-based setup for your Spree version before following admin-UI steps. Map `TaxCategory#tax_code` to the engine's product codes and set a freight code on delivery methods' categories.

## Gotchas

- **Tax is zero** → no `TaxRate` matches: wrong store, category mismatch (item uses a category with no rate; items without one use the store's `is_default` category), or no tax address yet on an added-on market. Check `Spree::TaxRate.for_store(cart.store).for_jurisdiction(cart.tax_country&.iso, cart.tax_address&.state_code)`.
- Tax not updating after an admin edit of a placed order — correct: placed orders never re-estimate.
- Creating/editing `TaxLine`s by hand — overwritten on the next estimate. Change rates, categories, or the provider.
- Market `tax_provider` must be a registered class name; a gem's provider must be appended to `Spree.tax_providers` or market validation fails.
- `commit` not idempotent → duplicate documents when completion replays.
- Set `Spree::Current.store` in jobs/console — rates and default categories are per store.

## Where to read further

- `node_modules/@spree/docs/dist/developer/core-concepts/taxes.md`, `companies.md`, `markets.md`, `order-totals.md`
- `node_modules/@spree/docs/dist/developer/customization/workflows.md` — context hooks
- Related skills: `spree-order-totals`, `spree-b2b`, `spree-providers`, `spree-pricing`, `spree-checkout`
- Source: `spree/core/app/models/spree/tax_provider/{base,internal}.rb`, `spree/core/app/models/concerns/spree/purchase/taxation.rb`
