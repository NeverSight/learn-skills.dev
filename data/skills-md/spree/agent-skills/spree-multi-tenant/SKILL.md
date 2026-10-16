---
name: spree-multi-tenant
description: Use when building a SaaS / multi-tenant platform on Spree 6 with the Enterprise `spree_multi_tenant` gem — many isolated merchants on one deployment, each with its own stores, catalog, customers and orders. Covers licensing and install (`spree_enterprise:install`, `spree_multi_tenant:install`), `Spree::Tenant` and row-level `tenant_id` isolation, `SpreeMultiTenant::Base`, `with_tenant` / `without_tenant`, console tenant context, `insert_all`/`upsert_all` pitfalls, background jobs, `Spree.root_domain`, cookie domain and host authorization, global staff vs per-tenant customers. Common phrasings include "multi-tenant Spree", "SaaS on Spree", "each merchant gets a subdomain", "tenant isolation", "records leaking between tenants", "set the tenant in the console", "Blocked hosts lvh.me".
---

# Multi-Tenant (SaaS) Spree

> **Enterprise only.** Multi-tenancy ships in the licensed `spree_enterprise` + `spree_multi_tenant` gems (private Keygen gem source). It is not part of open-source Spree. Confirm with Spree which gem release supports your Spree 6 version before planning around it.

## Multi-tenant vs multi-store vs marketplace

| Need | Use |
|---|---|
| Many independent merchants, fully isolated data, one deployment (Shopify-style SaaS) | **Multi-tenant** (this skill) |
| One merchant running several storefronts that share a catalog/customers | Multiple `Spree::Store`s (+ `spree_multi_store` for cross-store sharing) — see `spree-data-model` |
| Many sellers listing products under **one** shared storefront | Marketplace — see `spree-marketplace` |

## How isolation works

- `Spree::Tenant` is the top-level record. Creating a tenant creates its store and runs Spree's seeds (countries, zones, tax categories…).
- **Row-level tenancy**: every tenanted table has a `tenant_id` column. The gem is built on `acts_as_tenant`.
- The gem sets `Spree.base_class` to `SpreeMultiTenant::Base`, so every Spree model that inherits from `Spree.base_class` is tenanted automatically. `SpreeMultiTenant::Base` also makes `spree_base_uniqueness_scope` return `[:tenant_id]`, so uniqueness validations (slugs, codes, SKUs) are per tenant.
- While a tenant is current, **all reads add `WHERE tenant_id = ?` and all writes set `tenant_id`** automatically.
- The current tenant is resolved per request from the host: tenant subdomain (`store1.example.com`) or a custom domain → store → `store.tenant_id`. Available as `current_tenant` in controllers and `SpreeMultiTenant.current_tenant` elsewhere.
- One tenant can own several stores. `Spree::Store.default` returns the default store of the *first* tenant — never rely on it in tenant-aware code.
- **Staff (admin users) are global** and can be invited to many tenants. **Customers are per tenant** — the same email can register at two tenants.
- Isolation applies to the Admin API, Store API and dashboard alike.

## Install (summary)

1. Set `KEYGEN_ACCOUNT_ID` and `KEYGEN_LICENSE_KEY` in the server environment (and CI, staging, production **build** environments).
2. `spree eject` if you use the Docker CLI flow (gems must be installed into your own image).
3. Add to `server/Gemfile`:

   ```ruby
   source "https://license:#{ENV['KEYGEN_LICENSE_KEY']}@rubygems.pkg.keygen.sh/#{ENV['KEYGEN_ACCOUNT_ID']}" do
     gem 'spree_enterprise'
     gem 'spree_multi_tenant'
   end
   ```

4. Docker only: pass the Keygen values to **every** `bundle install` in `server/Dockerfile` as BuildKit secrets (`RUN --mount=type=secret,id=keygen_license_key,env=KEYGEN_LICENSE_KEY ...`) and declare the secrets in both compose files. Never use `ARG`/`ENV` — that bakes the license into image layers.
5. `spree bundle install` (or `bundle install`), then:

   ```bash
   spree generate spree_enterprise:install && spree generate spree_multi_tenant:install
   # classic: bin/rails g spree_enterprise:install && bin/rails g spree_multi_tenant:install
   ```

   This copies + runs migrations, wraps the Spree engine mount in `config/routes.rb` with domain constraints (and mounts the tenant app on the app subdomain), includes `SpreeMultiTenant::CustomerUserConcern` in the customer model, and changes the admin user's parent to `Spree::Base`.

## Post-install configuration

```ruby
# server/config/initializers/spree.rb
Spree.root_domain = ENV.fetch('SPREE_ROOT_DOMAIN', 'lvh.me')
```

```bash
# server/.env
SPREE_ROOT_DOMAIN=lvh.me   # local dev — NOT localhost (browsers reject localhost as a cookie domain)
COOKIE_TLD_LENGTH=2        # labels in the root domain: example.com=2, shop.example.co.uk=3
```

- `COOKIE_TLD_LENGTH` scopes the session cookie to the parent domain so staff stay signed in across `app.<root>` and tenant subdomains. Symptom when wrong: logged out between subdomains, `ActionController::InvalidAuthenticityToken`.
- Host authorization: allow the root domain or requests die with "Blocked hosts":

  ```ruby
  # server/config/environments/development.rb (and production equivalent)
  if (root_domain = ENV['SPREE_ROOT_DOMAIN']).present?
    config.hosts << ".#{root_domain}"
  end
  ```

- Customer model: after the generator adds `SpreeMultiTenant::CustomerUserConcern`, **remove Devise's `:validatable`** from the customer model — it enforces globally-unique emails; the concern re-validates per tenant. Don't add other Devise modules. The admin user model keeps `:validatable` (staff emails are global).
- `config/initializers/spree_multi_tenant.rb`:

  ```ruby
  SpreeMultiTenant::Config[:app_subdomain] = 'app'   # app.example.com — signup at /tenants/new
  SpreeMultiTenant::Config[:mail_from_name] = ENV.fetch('MAIL_FROM_NAME', 'Your SaaS')
  SpreeMultiTenant::Config[:mail_from_address] = ENV.fetch('MAIL_FROM_ADDRESS', "support@#{Spree.root_domain}")
  ```

  `mail_from_*` is used for staff-facing mail (invitations, exports). Customer emails use the tenant store's name and set `Reply-To` to the store's email.

## Writing tenant-aware code

### New models

Tenanted models inherit from `SpreeMultiTenant::Base` (automatic if you use `Spree.base_class`) and need a `tenant_id` column. Don't declare `belongs_to :tenant` — the gem does.

```bash
spree generate model Spree::Brand tenant:references name:string --parent SpreeMultiTenant::Base
```

If you use `spree generate api_resource` / `spree:model`, add the `tenant_id` column and index yourself, and include `tenant_id` in any unique DB index (`[:tenant_id, :slug]`).

### Forcing / escaping tenant context

```ruby
SpreeMultiTenant.with_tenant(tenant) do
  # everything here is scoped to tenant
end

SpreeMultiTenant.without_tenant do
  # cross-tenant: platform billing, global reports, maintenance
end
```

Console / `rails runner` / rake tasks start with **no** tenant:

```ruby
SpreeMultiTenant.current_tenant = Spree::Store.find_by(code: 'my_store').tenant
Spree::Current.store = Spree::Store.find_by(code: 'my_store')  # Spree 6 code also expects a current store
```

### Provisioning a new merchant's store

Seed it inside the tenant with `Spree::Seeds::StoreResources.call(store: store)` (per-store seeds — channels, roles, payment methods, API keys, … — without touching other stores), then `Spree::Stores::ProvisionDefaults.call(store:, country:)` for the country-shaped defaults (market, warehouse, delivery zones, pickup). Optional demo data: `Spree::SampleData::LoadJob.perform_later(store.id)`. See `spree-data-model`.

### Background jobs

Jobs enqueued while a tenant is current run in that tenant's context. Jobs enqueued outside one (cron/recurring jobs, `without_tenant` blocks) must iterate tenants explicitly:

```ruby
Spree::Tenant.find_each do |tenant|
  SpreeMultiTenant.with_tenant(tenant) { MyApp::NightlySyncJob.perform_later }
end
```

## Gotchas

- **`insert_all` / `upsert_all` / raw SQL bypass tenancy** — set `tenant_id` on every row yourself or you create orphaned/cross-tenant rows.
- `Spree::Store.default` / `Spree::Store.first` in tenant code returns the wrong tenant's store — use `current_store` / `Spree::Current.store`.
- Unique DB indexes without `tenant_id` make the second tenant's "same" slug/SKU fail at the DB level even though validations pass.
- `localhost` for local dev breaks cookies; use `lvh.me` or `localtest.me`.
- Keygen credentials missing in the Docker **build** step (not just runtime) → `bundle install` 401s.
- Tenanted records (including webhook endpoints) are only visible inside their tenant; a subscriber or job doing cross-tenant work must use `without_tenant` deliberately.
- Third-party extensions that write with `insert_all` or define their own base class may need a `tenant_id` migration and decorator — test each extension with two tenants.

## Where to read further

- `node_modules/@spree/docs/dist/developer/multi-tenant/quickstart.md`
- `node_modules/@spree/docs/dist/developer/multi-tenant/core-concepts.md`
- `node_modules/@spree/docs/dist/developer/multi-tenant/configuration.md`
- https://spreecommerce.org/pricing (Enterprise license)
- Related skills: `spree-data-model` (stores, channels), `spree-marketplace`, `spree-deployment`, `spree-security`
