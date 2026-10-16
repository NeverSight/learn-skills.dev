---
name: spree-providers
description: Use when connecting Spree 6 to an external system through a provider contract — a tax engine, carrier rate shopping, a WMS/3PL or label provider, a payment gateway, a search engine (Meilisearch, Typesense, Algolia), seller payouts, digital downloads/license keys, SSO/OpenID Connect or a custom JWT issuer, OpenTelemetry/APM, or an ERP/PIM/DAM. Common phrasings - "custom tax provider", "Avalara", "delivery rate provider", "EasyPost", "fulfillment provider", "custom payment method", "search provider", "payout provider", "digital asset provider", "SSO", "Okta/Entra login", "Spree::Integration", "store credentials for a provider", "Spree.integrations", "which registry do I append to". A map of every plug-in point - base class, registration call, where it is selected, and the doc to read.
---

# Spree Providers — Plugging External Systems In

Spree 6 connects external systems through **provider contracts**: a base class you subclass, a registry you append to, and a place where the merchant (or config) picks it. Every contract has a built-in default that uses Spree's own data, so connecting nothing changes nothing. You never fork or decorate the core flow.

> Paths below use the `server/` prefix of a `create-spree-app` project; on a classic Rails app drop it.

## The map

| Concern | Base class | Register | Selected by | Default |
|---|---|---|---|---|
| Tax | `Spree::TaxProvider::Base` | `Spree.tax_providers << MyTax` | `market.tax_provider`, else `Spree.default_tax_provider =` | `Spree::TaxProvider::Internal` |
| Delivery rates | `Spree::DeliveryRateProvider::Base` | `Spree.delivery_rate_providers << MyRates` | `delivery_method.rate_provider` | `…::Internal` (calculator), `…::Freight` |
| Fulfillment / labels / WMS | `Spree::FulfillmentProvider::Base` | `Spree.fulfillment_providers << MyWms` ⚠ after_initialize | `delivery_method.fulfillment_provider` | `…::Manual`, `Digital`, `Pickup`, `PickupPoint` |
| Payments | `Spree::PaymentMethod` (or `Spree::Gateway`) + `Spree::PaymentSession` STI | `Spree.payment_methods << MyGateway` ⚠ after_initialize | Payment method records (Settings → Payments) | Check, StoreCredit, Bogus |
| Search | `Spree::SearchProvider::Base` | `Spree.search_provider = 'My::Provider'` (one global) | — | `Spree::SearchProvider::Database` |
| Seller payouts | `Spree::PayoutProvider::Base` | `Spree.payout_providers << MyPayouts` | store preference `payout_provider`, else `Spree.default_payout_provider` | `Spree::PayoutProvider::System` |
| Digital deliverables | `Spree::DigitalAssetProvider::Base` | `Spree.digital_asset_providers << 'My::Provider'` | `digital_asset.provider_type` | `…::File` |
| Auth strategies (SSO, external JWT) | `Spree::Authentication::Strategies::BaseStrategy` / `OidcStrategy.configure(...)` | `Spree.{store,admin,seller}_authentication_strategies.add(:key, klass)` ⚠ after_initialize | Login request (`provider` param) | `:email` (`EmailPasswordStrategy`) |
| Credentials for any of the above | `Spree::Integration` | `Spree.integrations << 'My::Integration'` ⚠ after_initialize | Per store, Settings → Integrations | — |
| Observability | — (gem) | `gem 'spree_opentelemetry'` + `OTEL_*` env | — | dormant |

**Transactional email is not a provider.** Spree sends it over plain SMTP configured by `SMTP_*` env vars for the whole deployment, not per store in the admin, and there's no provider gem to install. Any SMTP service works (Resend, Postmark, SendGrid, Mailgun and Amazon SES have setup guides). Use the STARTTLS port (587); an implicit-TLS port such as 465 won't connect. Spree doesn't process bounces or complaints, so handle those with the provider's own webhooks. See `spree-deployment`.

Related plug-in points that are not "providers" but work the same way: `Spree.order_routing.rules` / `.strategies` (base `Spree::OrderRoutingRule`, `Spree::OrderRouting::Strategy::Base`), `Spree.stock_splitters` ⚠, `Spree.number_generators[:order] = 'My::Numbers'`, `Spree.promotions.rules` / `.actions` ⚠, `Spree.adjusters` ⚠, `Spree.tracking_carriers['my_courier'] = { name:, url: }` ⚠. See `spree-fulfillment`, `spree-promotions`, `spree-order-totals`.

**Coming soon (roadmap, interfaces may change):** ERP inventory sync, PIM pricing feeds, externally hosted DAM media. Core already ships `Spree::PricingProvider::Base` / `Spree::InventoryProvider::Base` with `Spree.pricing_providers` / `Spree.inventory_providers` and store preferences `pricing_provider` / `inventory_provider` (default `'internal'`), but the docs mark them roadmap — don't build production integrations on them without checking the current source.

## ⚠ Registration timing

Core **assigns** `payment_methods`, `fulfillment_providers`, `integrations`, `stock_splitters`, `adjusters`, `promotions.actions`, `tracking_carriers` and the three authentication registries inside its own `config.after_initialize`. Anything appended before that — at the top of `config/initializers/spree.rb`, or in `to_prepare` (which runs before `after_initialize` at boot) — is silently wiped. The other provider registries are seeded early and concatenated, so any point works for them. Uniform rule: **register every provider inside `after_initialize`.**

```ruby
# server/config/initializers/spree.rb
Rails.application.config.after_initialize do
  Spree.integrations << 'MyApp::AcmeIntegration'
  Spree.delivery_rate_providers << MyApp::AcmeRates
  Spree.fulfillment_providers << MyApp::AcmeFulfillment
  Spree.payment_methods << MyApp::AcmeGateway
end

Spree.search_provider = 'MyApp::SearchProvider::Typesense'   # plain assignment, any time
```

In a gem, use `config.after_initialize` in the engine (see `spree-extensions`). Symptom of getting it wrong: the provider is missing from the dashboard picker, or saving fails with "must be registered"/inclusion errors — registries double as validation allowlists (`delivery_method.rate_provider`, `market.tax_provider`, `digital_asset.provider_type`, `integration.type` are all validated against them).

## Credentials: `Spree::Integration`

Per-store credentials never go in ENV — a multi-store or marketplace app has a different account per store. Ship an integration:

```ruby
module MyApp
  class AcmeIntegration < Spree::Integration
    preference :api_key, :password          # :password = masked on read, guarded on write
    preference :test_mode, :boolean, default: true

    def self.integration_group = 'shipping'  # gallery grouping

    # Called when the merchant activates it; false blocks activation with the message.
    def can_connect?
      client.ping
      true
    rescue StandardError => e
      self.connection_error_message = e.message
      false
    end

    def client = @client ||= Acme::Client.new(api_key: preferred_api_key)
  end
end
```

Providers link to it with `def self.integration_class = 'MyApp::AcmeIntegration'` (delivery rate, fulfillment, pricing, inventory providers include `Spree::IntegrationBackedProvider`): availability per store is derived from it, and `integration` returns the store's active row. Tax and payout providers override `self.available_for_store?(store)` themselves.

## Contract cheat-sheet

**Tax** (`spree-taxes`) — `estimate(owner, items = nil, tax_date:, tax_identifier:, exemptions:, context:)` writes `Spree::TaxLine` rows with replace-all semantics per item; `commit(order)`, `void(order)`, `refund(order, return_items, amount:, tax_date:)` are no-ops unless you have a remote ledger. Class-level `display_name`, `available_for_store?`, `unsupported_capabilities`. Providers are stateless, built with no args.

**Delivery rates** (`spree-fulfillment`) — `estimates(package)` → array of `Spree::DeliveryRateProvider::Estimate.new(cost:, currency:, carrier:, service_level:, estimated_delivery_date:, metadata:)`, or single-quote `estimate(package)`. `nil`/`[]` hides the method. **Never raise** — rescue, `Rails.error.report`, return `[]`. `cost` is pre-tax. Cache per request with `Spree::Current.provider_cache[key] ||=`. Optional `self.service_catalog(integration)` → `ServiceCatalog.listing/none/unavailable`. `book`/`release` exist but core doesn't call them yet.

**Fulfillment** — class predicates `generates_labels?`, `digital?`, `pickup?`; instance `can_fulfill?`, `auto_fulfill?`, `requires_address?`, `serves_location?(delivery_method, stock_location)`, `purchase_label(owner)`, `refund_label(label)`, `create_fulfillment(fulfillment)` (idempotent), `cancel_fulfillment`, `tracking_url`, `documents`. Label-generating providers buy the label before the fulfillment is marked shipped. Reference implementation: `spree_easypost` (`SpreeEasyPost::DeliveryRateProvider`, `SpreeEasyPost::FulfillmentProvider`, `SpreeEasyPost::Integration`).

**Payments** (`spree-payments`) — subclass `Spree::PaymentMethod`, implement payment-session methods with a matching `Spree::PaymentSession` STI subclass (and optionally `Spree::PaymentSetupSession`), handle webhooks. Reference: `SpreeStripe::Gateway`.

**Search** — `search_and_filter(scope:, query:, filters:, sort:, page:, limit:)`, `filters(...)`, `index(product)`, `remove(product)`, `remove_by_id(prefixed_id)`, `index_batch(documents)`, `reindex(scope)`, `self.indexing_required?`. Document shape comes from `Spree::Dependencies.search_product_presenter` (the `spree_meilisearch` gem registers `SpreeMeilisearch::ProductPresenter`). Meilisearch: `gem 'spree_meilisearch'`, `MEILISEARCH_URL` / `MEILISEARCH_API_KEY`, `Spree.search_provider = 'SpreeMeilisearch::SearchProvider'`, then `spree task search:reindex`.

**Payouts** (`spree-marketplace`) — `transfer!(seller_transfer)`, `pay!(seller_payout)` (store your id in `reference`, don't mark completed — confirm via webhook and `Spree.seller_payout_complete_workflow`), `reverse!(seller_transfer)`; onboarding `onboarding_url`, `onboarded?`, `onboarding_state`, `onboarding_message`; class `display_name`, `reference_system`, `requires_payout_account?`, `available_for_store?`. Don't override `provider_key`. Raise `Spree::Core::AmbiguousGatewayError` on timeouts, `Spree::Core::GatewayError` on definite failures. Reference: `SpreeStripe::PayoutProvider` (Stripe Connect).

**Digital assets** — `deliver(digital_link, expires_in:)` returns `Spree::DigitalDelivery.new(redirect_url:)` or `.new(inline_value:, content_type:)`; blank = refused without spending the customer's download allowance. Per-asset settings via `setting :pool_name, :string` (rendered as a dashboard form); `self.requires_attachment?` false for minted deliverables.

**SSO / external identity** (`spree-auth-permissions`) — OpenID Connect is in core:

```ruby
Rails.application.config.after_initialize do
  Spree.admin_authentication_strategies.add(
    :entra,
    Spree::Authentication::Strategies::OidcStrategy.configure(
      issuer: 'https://login.microsoftonline.com/<tenant>/v2.0',
      client_id: ENV['ENTRA_CLIENT_ID'],
      client_secret: ENV['ENTRA_CLIENT_SECRET'],
      redirect_uri: 'https://shop.example.com/api/v3/admin/auth/callback/entra',
      label: 'Microsoft Entra ID'
    )
  )
end
```

Works for any OIDC issuer (Okta, Google Workspace, Keycloak, Auth0). Remove password login with `.remove(:email)`. For a non-OIDC JWT issuer, subclass `BaseStrategy` (`authenticate`, `provider`, `success(user)`, `failure(msg)`, `find_or_create_user_from_oauth`).

**Observability** (`spree-deployment`, `spree-performance`) — `gem 'spree_opentelemetry'`, set `OTEL_SERVICE_NAME` + `OTEL_EXPORTER_OTLP_ENDPOINT`; `OTEL_SDK_DISABLED=true` turns it off. Spans for every workflow run/step/hook, event dispatch, webhook delivery and gateway call. Tweak with `SpreeOpenTelemetry.configure { |c| c.use/skip/with_sdk }`. Sentry works as the exporter (`OTEL_TRACES_EXPORTER=none`).

## Gotchas

- **Rate and fulfillment providers must never break checkout.** Their calls run inside workflows — rescue vendor errors and degrade (hide the option, fall back) rather than raise, except where the contract says to raise gateway errors.
- **Tax providers fail closed.** If `estimate` can't compute complete `Spree::TaxLine` rows, raise — the recalculation (or completion) aborts instead of placing an order with missing tax. Only fall back (e.g. to `Spree::TaxProvider::Internal`) if the fallback writes a full, auditable set of tax lines.
- **Stateless providers.** They're instantiated with no arguments (delivery rate providers get the `delivery_method`); anything request-specific arrives as a parameter. Don't memoize per-store data on the class.
- **Class names in registries survive dev reloads** — core re-resolves `delivery_rate_providers` / `fulfillment_providers` on reload; string entries (`'My::Provider'`) are the most reload-safe form where a registry accepts them.
- **Removing a gem** leaves rows pointing at unregistered classes. Those rows survive (validation runs on change only), and a store whose payout provider disappears falls back to the built-in one — but clean up delivery methods/markets that reference it.
- **Inbound provider webhooks run in the record's store.** `POST /api/v3/webhooks/{payments,payouts}/:payment_method_id` and `/webhooks/fulfillments/:integration_id` look the payment method / integration up by prefixed ID alone (no API key or store header), set `Spree::Current.store` to its store, and `Spree::Payments::HandleWebhookJob` does the same. Your signature check against that record's own secret is the only authentication — never skip it, and raise rather than return when no secret is configured. Also enforce the provider's freshness rule there (signed timestamp + tolerance, e.g. Stripe's 5-minute window in `construct_event`); core's payment handling is idempotent on the payment, but any handler you write must stay idempotent on its provider's stable key (event or object ID) so a redelivery is a no-op.
- **Tax provider ≠ tax rates.** The internal provider uses zones/rates; an external engine replaces the calculation per market. Placed orders are money-frozen — the provider's `commit`/`refund` handle the remote ledger.

## Where to read further

- Overview: `node_modules/@spree/docs/dist/developer/providers/overview.md`
- How-tos: `node_modules/@spree/docs/dist/developer/how-to/{custom-delivery-rate-provider,custom-payment-method,custom-search-provider,custom-digital-asset-provider,custom-api-authentication,custom-order-routing,custom-stock-splitter,custom-document-numbers}.md`
- Providers: `node_modules/@spree/docs/dist/developer/providers/{fulfillment,payouts,sso,observability,erp,pim,dam}.md`
- Integrations catalog: https://spreecommerce.org/docs/integrations (payments: Stripe, Adyen, PayPal, Razorpay; marketplace: Stripe Connect; shipping: EasyPost; tax: Avalara; search: Meilisearch; marketing/analytics: Klaviyo, GA, GTM) — setup guides under `node_modules/@spree/docs/dist/integrations/<category>/<name>.md`
- Related skills: `spree-extensions`, `spree-taxes`, `spree-fulfillment`, `spree-payments`, `spree-marketplace`, `spree-auth-permissions`, `spree-customization`
