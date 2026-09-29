---
name: activerecord-tenanted
description: Expert guidance for SQLite-per-tenant Rails apps using the Basecamp activerecord-tenanted gem. Use when adding multi-tenancy, tenant databases, GlobalRecord, ApplicationRecord.with_tenant, Current.tenant, Current.account, shard swapping, db/global_migrate, or per-tenant SQLite. Do not use for Nebula-style acts_as_tenant row scoping or Fizzy same-database path tenancy.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(bin/rails generate*), Bash(bin/rails db:*), Bash(bin/rails test:*), Bash(bin/rails test)
---

# activerecord-tenanted (SQLite per tenant)

One SQLite file per tenant via the Basecamp [`activerecord-tenanted`](https://github.com/basecamp/activerecord-tenanted) gem. Identity, sessions, and the tenant row live in a **global** database. Product data lives in `storage/tenants/{env}/{tenant_key}/main.sqlite3`.

This is the Herald / Cortex / Innkeeper model. It is **not**:

- **Nebula `acts_as_tenant`** — one database, `workspace_id` on every row
- **Fizzy path tenancy** — one database, `Current.account` + `SCRIPT_NAME` URL prefix

If the app already uses `acts_as_tenant` or Fizzy-style account slugs in a shared schema, do not introduce this gem.

## Philosophy

1. **Two base classes, two databases.** `GlobalRecord` never sees tenant data. `ApplicationRecord` never sees identities.
2. **No tenanted query without a tenant.** `User.find` outside `with_tenant` / `Current.tenant=` is a bug, even in jobs and rake tasks.
3. **The URL (or Current) chooses the shard.** The gem's default subdomain resolver is wrong for path-based apps — disable it.
4. **Jobs re-enter the tenant.** Active Job does not magically carry the shard. Pass a global id (account/tenant/project) and wrap `perform` in `with_tenant`.

## What Goes Where

| Global (`GlobalRecord`) | Tenanted (`ApplicationRecord`) |
|-------------------------|----------------------------------|
| Identity, Session, MagicLink | The actual product records |
| Tenant / Account | User (Cortex/Innkeeper — in-tenant profile) |
| Membership (Identity ↔ tenant) | Everything else in that workspace |
| JoinCode, API tokens | Active Storage blobs (when `tenanted_rails_records` is on) |

Herald keeps `Project` global (so slugs/API keys exist before a shard is selected) and stores releases/subscribers in the account tenant. Cortex/Innkeeper put almost all product tables in the tenant DB. Both are fine — pick one and stay consistent.

## Step 1: Gem + database.yml

```ruby
# Gemfile
gem "activerecord-tenanted"
```

```yaml
# config/database.yml — every environment
primary:
  adapter: sqlite3
  database: storage/tenants/<%= Rails.env %>/%{tenant}/main.sqlite3
  tenanted: true
  max_connection_pools: 50
global:
  adapter: sqlite3
  database: storage/<%= Rails.env %>.sqlite3
  migrations_paths: db/global_migrate
queue:
  adapter: sqlite3
  database: storage/<%= Rails.env %>_queue.sqlite3
  migrations_paths: db/queue_migrate
# cache + cable the same way
```

`%{tenant}` is the gem's placeholder. `database_tasks: false` on `primary` is optional (Herald sets it so Rails doesn't try to dump a single primary schema).

Migrations:

- `db/global_migrate/` — Identity, Tenant/Account, Membership, Session. Run once.
- `db/migrate/` — tenanted tables. The gem runs these **per tenant**.

```bash
bin/rails db:migrate          # tenanted
bin/rails db:migrate:global    # global — check the gem's task name in the app
```

## Step 2: Two abstract classes

```ruby
# app/models/application_record.rb
class ApplicationRecord < ActiveRecord::Base
  primary_abstract_class
  tenanted
end

# app/models/global_record.rb
class GlobalRecord < ActiveRecord::Base
  self.abstract_class = true
  connects_to database: { writing: :global, reading: :global }
end
```

New model: if it is a person, session, or the tenant row itself → `GlobalRecord`. If it is data inside a workspace → `ApplicationRecord`. Getting this wrong is the #1 bug.

## Step 3: Disable subdomain resolver + default tenant

Path-based apps (all of ours) must not use the gem's subdomain resolver:

```ruby
# config/initializers/tenanted.rb
Rails.application.configure do
  config.active_record_tenanted.tenant_resolver = ->(request) { nil }
  config.active_record_tenanted.default_tenant =
    Rails.env.local? ? "#{Rails.env}-tenant" : nil
  config.active_record_tenanted.tenanted_rails_records = true
  config.active_record_tenanted.connection_class = "ApplicationRecord"
end
```

**Production `default_tenant` must be `nil`.** Otherwise boot can fail with `ARTENANT not set`, or worse, every request shares one leftover shard. Locally a named default tenant lets console/tests boot.

`tenanted_rails_records = true` stores Active Storage / Action Text in the tenant DB with prefixed keys. Pair with the `active-storage-multitenant` skill.

## Step 4: Current swaps the shard

```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :identity, :session
  attribute :tenant  # or :account — pick one name and use it everywhere
  attribute :user

  def tenant=(tenant)
    super
    return if ActiveRecord::Base.shard_swapping_prohibited?

    ApplicationRecord.current_tenant =
      tenant ? tenant.external_id : ActiveRecord::Tenanted::Tenant::UNTENANTED_SENTINEL
  end
end
```

Herald uses `Current.account=` and `account.tenant_key` (`"account-#{id}"`). Cortex/Innkeeper use `Current.tenant=` and `tenant.external_id`. Same mechanism.

Reset on request end (Cortex):

```ruby
resets do
  next if ActiveRecord::Base.shard_swapping_prohibited?
  ApplicationRecord.current_tenant = ActiveRecord::Tenanted::Tenant::UNTENANTED_SENTINEL
end
```

## Step 5: Resolve tenant from the URL

Do this in a controller concern, not the gem resolver:

```ruby
module TenantScoping
  extend ActiveSupport::Concern

  included do
    before_action :set_current_tenant
    before_action :set_current_user
  end

  def set_current_tenant
    record = Tenant.find_by(external_id: params[:tenant_external_id])
    Current.tenant = record if record
  end

  def set_current_user
    return unless Current.identity && Current.tenant
    Current.user = User.find_by(identity_id: Current.identity.id)
  end
end
```

Routes nest under the tenant key (`/:tenant_external_id/...` or a project slug that loads Account). Unauthenticated pages (sign-in, webhooks from vendors) skip this and wrap only the tenanted work.

Create the tenant database when the Tenant/Account is created:

```ruby
after_create :provision_tenant_database

def ensure_tenant_database!
  ApplicationRecord.create_tenant(tenant_key) unless database_exists?
rescue ActiveRecord::Tenanted::TenantExistsError
  # parallel tests / retries
end
```

## Step 6: Jobs, rake, console

```ruby
def perform(tenant_external_id, record_id)
  ApplicationRecord.with_tenant(tenant_external_id) do
    Current.tenant = Tenant.find_by(external_id: tenant_external_id)
    Record.find(record_id).do_work
  end
end
```

Never serialize a tenanted Active Record as a GID and expect `perform` to load it — the job runs untenanted. Pass the **global** tenant key plus the record id.

Rake / one-off:

```ruby
Tenant.find_each do |tenant|
  ApplicationRecord.with_tenant(tenant.external_id) do
    puts Project.count
  end
end
```

Public inbound webhooks with no tenant in the URL: iterate tenants (Innkeeper) or look up a global token that points at a tenant, then `with_tenant`. Don't query `User` at the top of the job.

## Tests

Every test that touches tenanted models must set a tenant. Use a helper:

```ruby
def with_tenant(tenant = tenants(:acme), &block)
  ApplicationRecord.with_tenant(tenant.external_id, &block)
end
```

Integration tests: hit a URL that includes the tenant prefix so `TenantScoping` runs. Don't stub `Current.tenant` and then assert on HTTP — the shard won't match the request.

## Anti-Patterns

1. **`acts_as_tenant :workspace` in an app that's already tenanted** — two tenancy systems. Nebula is the other model; don't mix.
2. **Putting Identity or Session on ApplicationRecord** — those tables must survive switching shards.
3. **`User.find` in a job without `with_tenant`** — silent empty results or `TenantNotSet`.
4. **Leaving the subdomain resolver on** — path-based apps resolve the wrong tenant or none.
5. **`default_tenant` in production** — every process shares one database file.
6. **Assuming integer PKs in tenant DBs** — our tenanted tables are UUIDs. See `uuid-primary-keys`.
7. **Creating blobs without a current tenant** — "Cannot generate a Blob key without a tenant." Use `with_tenant` and the Active Storage skill.

## Related

- Identity vs User, memberships, join codes: `identity-membership`
- Tenanted Active Storage / Lexxy: `active-storage-multitenant`
- Outbound webhooks that run in a tenant: `outgoing-webhooks`
- Passwordless sign-in (global Identity): `magic-link-auth`

See [reference.md](reference.md) for database.yml, Herald vs Cortex naming, and shard-swap gotchas.
