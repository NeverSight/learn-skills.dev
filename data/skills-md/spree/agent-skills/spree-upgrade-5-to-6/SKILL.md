---
name: spree-upgrade-5-to-6
description: Use when upgrading a Spree 5.x application to Spree 6.0, or when fixing code that broke after that upgrade. Common phrasings include "upgrade to Spree 6", "migrate from 5.6 to 6.0", "Spree 6 breaking changes", "checkout_flow / state machine is gone", "Spree::Adjustment not found", "master variant removed", "PermissionSets NameError", "staff locked out after upgrade", "what replaced Shipment / Taxon / ReturnAuthorization / metafields", "spree_admin gem not found". Covers preconditions (5.6 first, Rails 8.1, Gemfile swaps, roles as data), the ordered 5.6 → 6.0 data backfills, grep recipes for code that must change, and the behavioral review checklist.
---

# Upgrading Spree 5.x → 6.0

Spree 6.0 is the breaking-change release. Cart and Order are separate models, state machines are gone (statuses + workflows), adjustments became typed rows (`TaxLine` / `Discount` / `Fee`), the master variant is gone, shipping became fulfillment/delivery, taxons became categories/collections, users became `Spree::Customer`, staff permissions became data, and the Rails admin, Rails storefront and API v2 were removed in favor of the React dashboard (`spree_dashboard`) and API v3.

The upgrade is: **preconditions → gems → migrations → backfills → code fixes → behavioral review.** Budget real time for the last two; the rake part is the easy part.

Generic mechanics (`spree upgrade` flags, `STEP=`, production release phase) are in the **spree-upgrade** skill. This skill is the 6.0-specific playbook.

## 1. Preconditions — do these before touching the Gemfile

- [ ] **Be on 5.6.x, fully upgraded.** The 6.0 manifest assumes the 5.6 schema. Land on 5.6 first (`spree upgrade --to 5.6`, or bump to `~> 5.6` and run `bundle exec rake spree:upgrade`). The 6.0 run also replays the 5.4→5.5 and 5.5→5.6 backfills, but that doesn't replace being on 5.6.
- [ ] **Rails 8.1.** `spree_core` 6.0 requires `rails >= 8.1, < 8.2`; Ruby ≥ 3.2. Do the Rails bump (and its own deprecations) as a separate commit if you can.
- [ ] **Back up the database** and rehearse on a restored copy. Several backfills rewrite money, stock and customer rows; measure how long they take.
- [ ] **Gemfile swaps:**
  - remove `spree_admin` and `spree_storefront` (gone — replaced by the React dashboard and the Next.js storefront);
  - add `spree_dashboard` (serves the admin at `/dashboard`) — skip it for API-only deployments;
  - add `spree_meilisearch` if `Spree.search_provider` points at Meilisearch;
  - every other `spree_*` extension (payments, i18n, your own) needs a 6.0-compatible release — check before you start, or `bundle update` won't resolve. `spree_stripe`, `spree_easypost` and `spree_meilisearch` now ship from the Spree monorepo in lock-step versions.
- [ ] **Action Text / Action Cable.** `spree_core` no longer requires them. If *your* code uses `has_rich_text`, Action Text helpers, or Action Cable, add `require 'action_text/engine'` / `require 'action_cable/engine'` to `config/application.rb`.
- [ ] **Widen the rich-text allowlist first, if needed.** Descriptions/notes are re-sanitized to what the dashboard editor emits (paragraphs, headings, inline formatting, code, blockquote, lists, links, images). Tables, `div`/`span`, inline `style` and arbitrary classes are stripped. If you need them, set `Spree::RichTextSanitizer.allowed_tags += %w[…]` / `allowed_attributes += %w[…]` in an initializer **before** `migrate_rich_text_to_columns` runs and before anything is saved under 6.0.
- [ ] **Recreate staff roles as data.** Permission sets are removed with no bridge. A pre-existing role row comes up with **no permissions** — staff holding it are locked out (fail closed). Seed them before deploying:
  ```ruby
  store.roles.find_or_create_by!(name: 'support').update!(permissions: %w[read_orders read_customers])  # roles belong to a store
  ```
  Keys are `read_<resource>` / `write_<resource>` from the catalog (`Spree::ApiKey.known_scopes` lists them).
- [ ] **Delete PermissionSets initializers.** `Spree::PermissionSets::*` raises `NameError` and `Spree.permissions.assign` raises at boot. Extensions register resources with `Spree.permissions.register_scope(:reviews, group: :catalog, resources: -> { [SpreeReviews::Review] })`.
- [ ] **Customer migration check (Devise apps).** `spree:upgrade:migrate_users_to_customers` copies `spree_users` into `spree_customers` and maps Devise's `encrypted_password` to `password_digest`. It only works if **no Devise pepper** was configured; with Devise no longer loaded it aborts until you pass `CONFIRM_NO_PEPPER=true`. Rows with blank/duplicate emails abort it too (`SKIP_INVALID_ROWS=true` to skip). Peppered/SSO/non-bcrypt installs keep a custom `Spree.customer_class` instead.
- [ ] **Initializer settings that moved to the store** (`track_inventory_levels`, `auto_capture`, `company`, …) are copied by `store_settings_backfill_from_config` — leave them in the initializer until that step has run, then remove them.
- [ ] **Enable Active Record encryption.** Spree 6 encrypts webhook signing secrets, gateway customer IDs and OAuth identity tokens — only when keys are configured. Make `config/application.rb` read them (inside the `Application` class):
  ```ruby
  %i[primary_key deterministic_key key_derivation_salt].each do |key|
    value = ENV["ACTIVE_RECORD_ENCRYPTION_#{key.upcase}"].presence ||
      credentials.dig(:active_record_encryption, key).presence
    config.active_record.encryption[key] = value if value
  end
  ```
  Keys only in credentials, without this, leave webhook secrets and gateway customer IDs plaintext (their `encrypts` checks `config.active_record.encryption`). Generate a separate set per environment (`spree encryption init` for dev `.env`, `spree encryption init --print` / `bin/rails db:encryption:init` for production), set them on the host **before** deploying, back them up, never change them. Existing plaintext webhook secrets and gateway customer IDs become unreadable once encryption is on: deploy first with `config.active_record.encryption.support_unencrypted_data = true` and `extend_queries = true`, run `[Spree::WebhookEndpoint, Spree::GatewayCustomer, Spree::UserIdentity].each { |m| m.find_each(&:encrypt) }`, then remove both settings. See `spree-security`.
- [ ] **Secret API keys minted with `settings`** lose `/admin_users`, `/invitations`, `/roles` — they now need `read_staff` / `write_staff`. Re-mint integration keys that manage staff.

## 2. Run the upgrade

```bash
# create-spree-app (ejected dev stack; Rails app in server/, older projects backend/)
spree upgrade
spree upgrade --plan              # after the gem bump: list every step

# classic Rails app / no CLI
bundle update
bundle exec rake spree:install:migrations && bin/rails db:migrate
DRY_RUN=1 bundle exec rake spree:upgrade
CONFIRM_NO_PEPPER=true bundle exec rake spree:upgrade
```

Production: deploy runs `db:migrate`, then the release phase runs `bundle exec rake spree:upgrade` (pass `CONFIRM_NO_PEPPER=true` there too if applicable). Take a maintenance window — in-flight checkouts are converted into carts by the backfills.

## 3. What the 5.6 → 6.0 manifest runs (in order)

From `spree_core/lib/spree/upgrades/5_6_to_6_0/manifest.yml`. All idempotent; re-run one with `spree upgrade --step <id>`.

| # | Step id | What it does |
|---|---|---|
| 1 | `consolidate_metadata` | Safety net: merges any leftover `public_metadata`/`private_metadata` pairs into the single `metadata` column |
| 2 | `migrate_media_class_names` | Rewrites stored `Spree::Asset`/`Spree::Image` class names to `Spree::Media` |
| 3 | `migrate_master_images_to_product_media` | Moves variant-pinned images onto the product gallery (enqueues jobs — let them drain) |
| 4 | `backfill_media_store_ids` | Gives every media row a `store_id` |
| 5 | `remove_master_variant` | Backfills `default_variant_id`, retires master variants |
| 6 | `migrate_taxons_to_categories_and_collections` | Automatic taxons → `Spree::Collection`; the rest stay `Spree::Category`; rewrites `Spree::Taxon*` strings |
| 7 | `backfill_library_media_placements` | Puts category/collection images into the media library |
| 8 | `migrate_users_to_customers` | `spree_users` → `spree_customers`, repoints `user_type` columns (see Devise pepper precondition) |
| 9 | `migrate_rich_text_to_columns` | Action Text bodies → text columns, sanitized |
| 10 | `migrate_shipping_to_delivery` | Shipment → fulfillment strings/statuses, fulfillment providers, `display_on` → `storefront_visible` |
| 11 | `migrate_delivery_profiles` | Shipping categories → store-owned delivery profiles |
| 12 | `migrate_fulfillment_statuses` | Remaps to `unfulfilled` / `fulfilled` / `delivered` |
| 13 | `migrate_deliveries` | Tracking numbers → `spree_deliveries` rows |
| 14 | `migrate_zones_to_delivery_zones` | Delivery-referenced zones → `Spree::DeliveryZone` |
| 15 | `migrate_country_state_codes` | Fills ISO `country_code`/`state_code` columns (countries/states are reference data now) |
| 16 | `migrate_promotion_option_value_rules` | Option-value promo rules → stable option value ids |
| 17 | `migrate_adjustments_to_typed_rows` | `spree_adjustments` → `TaxLine` / `Discount` / `Fee`; flags non-reconciling orders |
| 18 | `backfill_reason_store_ids` | Store-owns return/refund reasons |
| 19 | `migrate_returns` | ReturnAuthorization → `Spree::Return` / `Spree::Exchange` (aborts on failed rows; `SKIP_FAILED_ROWS=true`) |
| 20 | `migrate_stock_movements_to_typed_rows` | Types stock movements; re-allocates open fulfillments (stock now leaves at dispatch) |
| 21 | `backfill_delivery_and_stock_store_ids` | Store-owns delivery methods and stock locations |
| 22 | `migrate_tax_zones` | Tax rate zones → country/state on the rate |
| 23 | `backfill_tax_store_ids` | Store-owns tax rates/categories |
| 24 | `backfill_order_coupon_codes` | Fills the new `spree_orders.coupon_code` on historical placed orders |
| 25 | `backfill_order_markets` | Assigns default market to orders |
| 26 | `migrate_incomplete_orders_to_carts` | Incomplete orders → `Spree::Cart` (same token) |
| 27 | `migrate_calculator_bounds_to_delivery_method_rules` | FlatRate min/max bounds → `DeliveryMethodRule` |
| 28 | `store_settings_backfill_from_config` | Copies moved `Spree::Config` settings onto every store |
| 29 | `migrate_capture_methods` | `auto_capture` → `capture_method` on payment methods |
| 30 | `product_types_backfill` | Store-owns product types |
| 31 | `search_reindex` | Rebuilds indexing search providers (Meilisearch); no-op for the DB provider |
| 32 | `fold_store_credit_categories` | Store credit category → memo |
| 33 | `migrate_stripe_webhook_keys` | *(optional, `spree_stripe` only)* webhook secrets onto the gateway |
| 34 | `backfill_import_export_tenancy` | Gives imports a `store_id` (+ `seller_id`) |
| 35 | `backfill_custom_field_definition_stores` | Store-owns custom field definitions |
| 36 | `package_types` | Store default box → package type row |
| 37 | `migrate_external_receives_to_purchase_orders` | 5.x supplier receives → purchase orders; gives transfers a store/status |
| 38 | `backfill_actor_types` | Fills the new actor `*_type` columns (canceler, approver, created_by, …) with the admin user class; until it runs, old rows resolve with a deprecation warning |
| 39 | `recount_stock_levels` | Fills `reserved_count` / `incoming_count` |

Always trust `spree upgrade --plan` (run after the gem bump) over this table — the gem you install is the source of truth.

### Post-check: frozen orders

`migrate_adjustments_to_typed_rows` never changes money. Orders whose typed sums don't reconcile with stored totals are left untouched and flagged in `metadata` (the guide says `private_metadata` — that column is now `metadata`). Review each:

```ruby
# spree console
Spree::Order.where.not(completed_at: nil).find_each.select { |o| o.metadata['typed_adjustments_frozen'].present? }
  .map { |o| [o.number, o.metadata['typed_adjustments_frozen']] }
```

Reasons include `totals_do_not_reconcile` and return-authorization freezes (handled by `migrate_returns`).

## 4. Fix your code — grep recipes

Run these over `server/app server/config server/lib server/spec` (classic apps: `app config lib spec`), plus `apps/storefront`, `apps/dashboard` and any integration code. The full pattern → replacement table is in **[references/grep-recipes.md](references/grep-recipes.md)**. The hits that break boot or checkout first:

```bash
cd server   # or the app root
grep -rnE "checkout_flow|go_to_state|insert_checkout_step|remove_checkout_step|state_machine|before_transition|after_transition" app config lib
grep -rnE "PermittedAttributes|permitted_[[:alnum:]_]+_attributes" app config lib
grep -rnE "PermissionSets|permissions\.assign|ApiKey::SCOPES" app config lib
grep -rnE "Spree::Adjustment|\.adjustments\b|promo_total|ship_total|item_count" app config lib
grep -rnE "\.master\b|is_master|default_price|DefaultPrice|variant\.price\b|\.price =" app config lib
grep -rnE "finalize!|order\.completed|OrderUpdater|register_update_hook|\bresume!?\b" app config lib
grep -rnE "ReturnAuthorization|CustomerReturn|Reimbursement|ReturnItem" app config lib
grep -rnE "_service\s*=" config
```

Deprecated-but-working names (Shipment, ShippingMethod, Taxon, metafields, `firstname`, `Spree.user_class`, …) log `Spree::Deprecation` warnings — fix them now; they're removed in 6.1. Run the suite with deprecations visible and treat each warning as a to-do.

## 5. Behavioral review checklist

These don't raise — they change what happens. Walk through each.

- [ ] **Completed carts are read-only.** Post-checkout edits belong to the `Spree::Order`. Anything that mutated an order after completion through cart APIs must move to order-side admin services.
- [ ] **`line_item.order` may be nil.** LineItem, Fulfillment, Payment, TaxLine, Discount, Fee and StockReservation have `cart_id` + `order_id` (exactly one set). Use `#owner`.
- [ ] **Statuses are derived.** `payment_status` / `fulfillment_status` are written only by `Spree::Orders::UpdateStatuses`; direct assignment is overwritten. `payment_state`/`shipment_state`/`state` are read aliases until 6.1. Order filter: `q[status_eq]=placed`.
- [ ] **Placed orders are money-frozen.** Recalculation re-sums typed rows; it never regenerates them. Post-placement money edits go through `Spree::Orders::Discounts::*` / `Orders::Fees::*`.
- [ ] **5.x extensions call Order names on carts.** Gateway gems written when a cart was an incomplete order call `promo_total`, `item_count`, `shipments`, `user`, `available_payment_methods` … on `Spree::Cart`. Those deprecated names now warn and forward on Cart as well as Order until 6.1 (see the grep recipes). Watch the deprecation log and update the gem.
- [ ] **Free gifts don't count toward thresholds.** A `create_line_items` gift no longer counts toward `item_total` rules or the base of a percentage-off order discount, including its own promotion's threshold. "Spend over $100, get a gift" takes the gift back once the paid items fall to $100.
- [ ] **Cancel is final.** No `resume` for orders or fulfillments; `order.resumed` / `fulfillment.resumed` events are gone. A fully recalled order reads `fulfillment_status: unfulfilled`.
- [ ] **`Spree::Store.default` can be `nil`.** Set `Spree::Current.store` in jobs, rake tasks, seeds and tests that run outside a request; ensure a default store exists before creating store-scoped records.
- [ ] **`belongs_to` is required by default** in anything inheriting `Spree::Base` — including your own models. Add `optional: true` where blank is legitimate. The error reads "must exist", not "can't be blank" (fix assertions and clients parsing 422 `details`).
- [ ] **Storefront contract.** `requirements[]` entries carry `{ step, field, code, message }`; the delivery requirement is `field: 'delivery_method'`, `code: 'delivery_method_required'`. Rich-text reads return plain text plus `*_html` (`description_html`, `internal_note_html`) — hydrate editors from `*_html`. Cart `number` mirrors the prefixed `cart_` ID for one release.
- [ ] **Webhooks/events.** Subscribe to `order.placed` (`order.completed` is a deprecated alias until 6.1). `report.*`, `order.resumed`, `fulfillment.resumed` are removed. New: `return.*`, `exchange.*`, `claim.*`, `digital_asset.*`, `digital_link.downloaded`.
- [ ] **Rich-text allowlist** narrowed (see preconditions). Content is re-sanitized on next save.
- [ ] **Digital downloads** answer `302` to a short-lived signed URL (≤ 1 hour, `digital_asset_link_expire_time`). Clients must follow redirects. Customers now get a download-links email from `spree_emails` — suppress your own if you sent one.
- [ ] **Custom field definitions are store-scoped.** Multi-store installs end up with all definitions on the default store; recreate them per store. Product CSV columns use the `custom_field.` prefix (was `metafield.`) and `product_type` (was `shipping_category`).
- [ ] **Staff API permissions.** JWT staff pass the same per-controller gate as secret keys (403 with `details.required_permission`). Staff endpoints need `read_staff` / `write_staff`.
- [ ] **Store API authorization** no longer consults CanCanCan — customer access is ownership scoping plus `Spree::Storefront::AccessPolicy`. Move storefront `can` rules into an access-policy subclass or a workflow `validate` hook.
- [ ] **Countries and states are reference data** (plain objects from the `countries` gem, no `.where`/`.find`). Records name them by ISO `country_code` / `state_code`.
- [ ] **Stock leaves at dispatch**, not at placement (open fulfillments hold an allocation). Inventory reports built on `count_on_hand` alone will read differently.
- [ ] **Jobs.** New projects run Solid Queue inside Puma (Mission Control at `/jobs`). An upgraded app keeps its own `config.active_job.queue_adapter` — Sidekiq keeps working; just move any Spree recurring jobs into whatever scheduler you use.
- [ ] **SDK majors.** Bump `@spree/sdk` to 2.x in the storefront and `@spree/admin-sdk` to 1.x in integrations; replace the Rails admin customizations with `apps/dashboard` plugins (`spree add dashboard`).

## Gotchas

- **Don't reorder backfills.** Several steps depend on earlier ones (media before master-variant removal; taxons and customers before rich text; adjustments before carts and returns; returns before stock movements). The manifest order is load-bearing.
- **`migrate_users_to_customers` aborts by design** without `CONFIRM_NO_PEPPER=true` once Devise is gone. Confirm no pepper was used rather than forcing it.
- **Overriding a `*_service` DI key does nothing now.** Legacy writes like `Spree::Dependencies.carts_complete_service = 'MyComplete'` are stashed, not applied. Move to the `*_workflow` key (subclass the shipped workflow) or, better, a `Spree.hooks.register` handler — see **spree-dependencies** and **spree-workflows**.
- **`Spree::Product.additional_permitted_attributes << :x` raises `FrozenError`.** Use `+= [:x]`.
- **Legacy tables stay until 6.1** (`spree_adjustments`, return-authorization tables, `spree_state_changes`, `spree_log_entries`, `spree_users`, Action Text rows) as rollback sources. Export anything you want to keep before 6.1.

## Where to read further

- `node_modules/@spree/docs/dist/developer/upgrades/5.6-to-6.0.md` — the official guide (https://spreecommerce.org/docs/developer/upgrades/5.6-to-6.0)
- `references/grep-recipes.md` — full pattern → replacement table
- Related skills: **spree-upgrade**, **spree-workflows**, **spree-checkout**, **spree-order-totals**, **spree-fulfillment**, **spree-returns**, **spree-auth-permissions**, **spree-catalog**, **spree-pricing**, **spree-dashboard-plugins**, **spree-typescript-sdk**
