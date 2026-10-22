---
name: spree-auth-permissions
description: Use when the user is working on who can sign in to Spree 6 and what they may do — staff roles and permission keys, secret-key scopes, registering permission scopes for an extension, 403 errors with `required_permission` / `required_scope`, storefront ownership rules (`Spree::Storefront::AccessPolicy`), custom login strategies (SSO, OIDC, Auth0/Okta/Entra/Firebase), JWT audiences, or swapping the customer/admin user class. Common phrasings include "Spree roles", "staff permissions", "add a role", "read_orders permission", "Spree.permissions.register_scope", "API key scopes", "403 Missing permission", "who can see this order", "SSO for the dashboard", "OIDC login", "custom authentication strategy", "Spree.customer_class", "admin_user_class", "CanCanCan in Spree 6". Spree 6.
---

# Spree Auth & Permissions

Spree 6 has three principals and each has its own way of being authorized:

| Principal | Authenticates with | Authorized by |
|---|---|---|
| **Staff** (`Spree.admin_user_class`, default `Spree::AdminUser`) | JWT (`aud: admin_api`) from `POST /api/v3/admin/auth/login` | Permission keys held by their **roles on the current store** |
| **Integration** (server-to-server) | Secret key `sk_…` in `X-Spree-Api-Key` | The key's **scopes** (same keys as roles) |
| **Customer** (`Spree.customer_class`, default `Spree::Customer`) | Publishable key `pk_…` + optional JWT (`aud: store_api`) | **Ownership**: scoped queries plus `Spree::Storefront::AccessPolicy` |

Marketplace sellers are a fourth surface (`/api/v3/seller`, JWT `aud: seller_api` + `X-Spree-Seller-Id`) — see `spree-marketplace`.

Two rules sit under everything in this skill:

1. **Keys gate *kinds* of records, never *which* rows.** `write_orders` means "may write orders", and the controller's scoped query (`current_store.orders`, `current_seller.products`, `current_user.wishlists`) decides which orders. If you add a controller, you own the scoping.
2. **Record-state rules belong on models and workflows**, not in permissions. "A placed order can't be deleted" must bind secret keys too, and secret keys never go through roles.

## Staff roles are data

A `Spree::Role` belongs to what it governs (`resource`: a `Spree::Store` for back-office staff, a `Spree::Seller` for a seller's team) and carries a flat list of permission keys in `permissions` (JSON array). There are no permission-set classes and no Ruby role definitions.

- Keys look like `read_<resource>` / `write_<resource>`. **`write_x` implies `read_x`** (`Spree.permissions.expand_keys`).
- **Granting and removing roles are bounded the same way.** Only a holder of the `admin` role can grant or remove `admin`; everyone else can grant or remove only roles whose keys they hold themselves; and a store always keeps at least one admin (`403` "The store must keep at least one admin."). Assigning an empty role list is a removal too.
- Every store has one protected `admin` role meaning "everything in this store". It can't be renamed, edited or deleted, and it ignores its `permissions` list (it gets `can :manage, :all`).
- Role names are unique per owner, so two stores can both have "Manager".
- A role with staff or pending invitations attached can't be deleted.
- `mutable: false` makes a role read-only in the dashboard.

### Managing roles

Pick whichever matches how the rest of the store is managed:

- **Dashboard:** Settings → Roles (the permission picker is rendered from the catalog).
- **Admin API:** `/api/v3/admin/roles` (CRUD), `/api/v3/admin/permissions` (the grantable catalog). Both need `read_staff` / `write_staff`.

  ```bash
  spree api post /roles -d '{"name":"Support","permissions":["read_orders","read_customers"]}'
  ```

  ```ts
  await adminClient.roles.create({
    name: 'Fulfillment staff',
    permissions: ['read_orders', 'write_fulfillments', 'read_products'],
  })
  ```

- **Seeds** (`db/seeds.rb`) — a role must have a `resource`:

  ```ruby
  store = Spree::Store.default
  role = Spree::Role.find_or_initialize_by(name: 'support', resource: store)
  role.update!(permissions: %w[read_orders read_customers write_customers])

  admin = Spree.admin_user_class.find_by!(email: 'agent@example.com')
  admin.add_role('support', store)   # looks the role up by name + resource
  ```

Unknown keys, or keys not grantable to the role's audience, fail validation — you can't save a store role holding `write_seller_profile`.

To invite staff: Settings → Users → Invite, or `adminClient.invitations.create({ email, role_id })` (publishes `invitation.created`, which sends the email). `role_id` is **required** — an invitation never defaults to the admin role — and the caller must be allowed to grant that role. Invitation listings don't include the acceptance link (it carries the token that creates the account): fetch it on demand with `adminClient.invitations.acceptanceLink(id)` → `GET /api/v3/admin/invitations/:id/acceptance_link`, which needs `write_staff` plus the right to grant the invitation's role (sellers: `sellers.invitations.acceptanceLink(sellerId, id)` / Seller API `invitations.acceptanceLink(id)`). Resending an invitation rotates its token, so an earlier link stops working. To create an admin locally: `spree user create` (gets the `admin` role on the default store).

## The permission catalog

The full list of core keys, grouped the way the pickers show them, is in `spree-api-v3/references/scopes.md`. Discover it at runtime with `GET /api/v3/admin/permissions`; secret-key scopes come from `Spree::ApiKey.known_scopes` (every staff-grantable key plus `read_all` / `write_all`).

Worth knowing:

- Money-adjacent areas are separate resources: `payments`, `refunds`, `gift_cards`, `store_credits` aren't covered by `orders`. "Can see orders but not refund" needs no special handling.
- Staff management is `read_staff` / `write_staff` (`/admin_users`, `/invitations`, `/roles`).
- `api_keys` and `webhooks` are split out from `settings` because they're sensitive. A caller holding `write_api_keys` can only mint keys with scopes it already holds.
- Custom-field **values** follow their parent resource (`write_products` covers product custom fields). Definitions are `settings`.
- Exports have no scope of their own. Each export type needs the read key of the resource it exports. Imports need the write key.
- `read_dashboard` has no write key.

### Registering a scope for your extension

```ruby
# config/initializers/spree.rb (or your engine's initializer)
Spree.permissions.register_scope(:reviews, group: :catalog, resources: -> {
  [SpreeReviews::Review]
})
```

Signature: `register_scope(name, group:, resources:, write: true, audiences: [:store], read_only_for: [])`.

- `group` picks the section in the pickers: `:analytics`, `:orders`, `:catalog`, `:customers`, `:sellers`, `:loyalty`, `:marketing`, `:settings`, `:access`, or your own. Rows show in registration order.
- `resources` is a lambda returning CanCanCan subjects (classes or symbols). It resolves lazily, so load order doesn't matter.
- `write: false` registers a read-only scope (only `read_<name>`).
- `audiences` lists **every** audience whose roles may hold the keys. The default is `[:store]` (staff). `%i[store seller]` also opens it to marketplace seller roles. If you leave `:store` out, the scope disappears from the staff picker, from `read_all`/`write_all`, and from mintable secret keys.
- `read_only_for: %i[seller]` gives that audience only the read key.
- The name `all` is reserved (raises `ArgumentError`). Re-registering a name replaces it; `Spree.permissions.unregister_scope(:name)` removes it.
- Never open `settings`, `staff` or `api_keys` to another audience.

Localize the picker labels under `spree.permissions_catalog.resources.<name>.label` / `.description`.

Then declare the scope on your Admin API controller:

```ruby
module Spree
  module Api
    module V3
      module Admin
        class ReviewsController < ResourceController
          scoped_resource :reviews        # index/show → read_reviews; everything else → write_reviews

          protected

          def model_class = SpreeReviews::Review
          def serializer_class = SpreeReviews::Api::V3::Admin::ReviewSerializer
          def resource_permitted_attributes = %i[rating body status]
        end
      end
    end
  end
end
```

The `spree:api_resource` generator (see `spree-resource`) emits both halves: `scoped_resource :reviews` on the Admin controller, and the matching `register_scope` line appended to `config/initializers/spree.rb` (`--permission-group` picks the group, default `catalog`), plus a label in `config/locales/spree_reviews.en.yml`. Hand-written controllers need both too — a `scoped_resource` without a registered scope means only `read_all`/`write_all` keys and the `admin` role can reach the endpoint, other staff are denied, and no key can be minted with `read_reviews`.

## How the gate works (Admin API)

Every Admin API controller declares `scoped_resource :name`. Controllers that authorize some other way call `skip_scope_check!`, optionally with `only:` or `jwt_only: true`. A controller that declares neither raises `MissingScopedResource` when a request hits it, so the check fails closed. For each request:

1. The action maps to `read_` (`index`, `show`, plus anything in the controller's `read_actions`) or `write_` (everything else, including custom member actions like `cancel`).
2. **Secret key:** `current_api_key.has_scope?("write_orders")`, or 403:
   ```json
   { "error": { "code": "access_denied", "message": "API key lacks scope: write_orders",
                "details": { "required_scope": "write_orders" } } }
   ```
3. **JWT staff:** the user's expanded role keys on the current store (`Spree::Ability#permission_keys`), or 403 with `"details": { "required_permission": "write_orders" }`. The `admin` role passes everything.
4. Behind the gate, keys compile into CanCanCan rules for record-level checks. A 403 **without** `required_permission` means the user holds the key but a record-level rule refused the action.

If a request carries both a JWT and a secret key, the JWT wins and the user's roles apply. A staff user with no role on the requested store is rejected even with a valid token.

**Embedded data is gated too.** An endpoint is gated on its own key, but `?expand=` segments that pull in records of another kind are dropped unless the caller holds their read key (`orders`→`read_orders`, `payments`/`payment_splits`→`read_payments`, `customer(s)`→`read_customers`, `gift_card(s)`→`read_gift_cards`, `store_credit(s)`→`read_store_credits`), and gift card codes are masked for callers without `read_gift_cards`. In your own Admin controllers, use `holds_permission?('read_x')` (it mirrors the gate for both JWT staff and secret keys) before serializing data another permission guards.

`GET /api/v3/admin/me` returns `permission_keys` (flat list) and the CanCanCan rule dump that the dashboard mirrors for UI gating. **Hiding a button in the UI is not authorization.** The API gate is the only enforcement.

### Secret-key specifics

- Scopes are **immutable** once a key is created. To change what an integration can do, mint a new key and revoke the old one.
- A publishable key can be bound to one channel (`channel_id`, also immutable). A bound key sets the request's channel on the server, and a conflicting `X-Spree-Channel` header is rejected.
- Mint keys with the minimum scopes: `spree api-key create --type secret --scopes read_orders,write_fulfillments`.

### About `Spree::Ability` and `ability_class`

CanCanCan is still used **behind** the key gate for record-level rules. Every staff ability — JWT staff on the Admin API, sellers on the Seller API, imports and exports — is built from `Spree.ability_class` (`Spree::Dependencies.ability_class`, default `Spree::Ability`). When you need rules the permission catalog can't express, swap it:

```ruby
# app/models/my_app/ability.rb
module MyApp
  class Ability < Spree::Ability
    def initialize(user, options = {})   # keep this signature
      super                              # options[:store]; options[:resource] = the seller on the Seller API
      cannot :destroy, Spree::Order      # add can/cannot rules AFTER super
    end
  end
end

# config/initializers/spree.rb
Spree::Dependencies.ability_class = 'MyApp::Ability'
```

What it does **not** change:

- **The key gate runs first.** A custom ability can refuse records the key allows (a 403 without `required_permission`), but it can't let a request through that lacks the permission key.
- **Secret API keys never consult it** — they use `Spree::ApiKeyAbility`, gated only by scopes.
- **The no-seller `GET /api/v3/seller/me` answer** is always built from core `Spree::Ability`, so rules you add don't leak into it.
- **The Store API** — customers aren't authorized with CanCanCan at all (see below).

For narrowing what a listing returns, changing the scoped query is often simpler than an ability rule. State rules ("can't refund a canceled order") belong on the model or workflow.

## Storefront authorization (Store API)

Customers never hold roles, and the Store API doesn't use CanCanCan. Access is ownership, enforced two ways:

1. **Scoped queries.** Every store controller reads through the store and the owner, e.g. `storefront_access_policy.scope(Spree::Wishlist.for_store(current_store))`.
2. **`Spree::Storefront::AccessPolicy`**, a single object with `readable?(record, token:)`, `writable?(record, token:)` and `scope(relation, token:)`:
   - Default: the caller owns the record (`record.customer_id == user.id`). Guests own nothing.
   - Carts, orders and order groups: the owner by JWT **or** whoever holds the guest token (`X-Spree-Token`). Writes are refused once the cart or order is completed.
   - Companies (B2B): members with standing on the node or one of its ancestors.
   - Denials raise `Spree::Storefront::AccessDenied`, which renders as 403 `access_denied`.

For a custom customer-owned resource, follow the core pattern:

```ruby
class Spree::Api::V3::Store::SavedListsController < Spree::Api::V3::Store::ResourceController
  prepend_before_action :require_authentication!

  protected

  def scope
    storefront_access_policy.scope(MyApp::SavedList.for_store(current_store))
  end

  def model_class = MyApp::SavedList
  def serializer_class = MyApp::Api::V3::SavedListSerializer
  def resource_permitted_attributes = %i[name]
end
```

Swap the policy only when access has to go **beyond the owner** (company-wide purchase visibility, shared wishlists). Subclass it and call `super`:

```ruby
# app/models/my_app/company_access_policy.rb
class MyApp::CompanyAccessPolicy < Spree::Storefront::AccessPolicy
  def scope(base, token: nil)
    return base.where(company_id: approver_company_ids) if base.klass <= Spree::Order && approver?
    super
  end
end

# config/initializers/spree.rb
Spree::Dependencies.storefront_access_policy_class = 'MyApp::CompanyAccessPolicy'
```

Don't use the policy for action vetoes like approval-required or spending limits. Those are checkout workflow `validate` hooks (see `spree-workflows`, `spree-b2b`). `/customers/me/*` stays owner-only by design.

## Authentication strategies (login providers)

Login is pluggable per surface. The `provider` field of `POST …/auth/login` picks a strategy from a registry. If it's omitted, `email` (password) is used.

| Surface | Registry | User class | JWT `aud` | Refresh token |
|---|---|---|---|---|
| Store API | `Spree.store_authentication_strategies` | `Spree.customer_class` | `store_api` | in the response body |
| Admin API | `Spree.admin_authentication_strategies` | `Spree.admin_user_class` | `admin_api` | HttpOnly cookie at `/api/v3/admin/auth` |
| Seller API | `Spree.seller_authentication_strategies` | `Spree.admin_user_class` | `seller_api` | HttpOnly cookie at `/api/v3/seller/auth` |

Each surface accepts only its own audience, so a customer token can't be replayed against the Admin API. Spree issues HS256 JWTs with `iss: spree`. The signing secret resolves from `Spree::Api::Config[:jwt_secret_key]` (env `SPREE_JWT_SECRET_KEY`), then credentials `jwt_secret_key`, then `JWT_SECRET_KEY`, then `secret_key_base`. Lifetimes: customer JWT 1 hour (`jwt_expiration`), admin JWT 5 minutes (`admin_jwt_expiration`), refresh token 30 days.

### Built-in OIDC (staff SSO)

`Spree::Authentication::Strategies::OidcStrategy` is a redirect strategy that works with any OpenID Connect issuer (Entra ID, Okta, Google Workspace, Keycloak, Auth0):

```ruby
# config/initializers/spree.rb
Rails.application.config.after_initialize do
  Spree.admin_authentication_strategies.add(
    :entra,
    Spree::Authentication::Strategies::OidcStrategy.configure(
      issuer: "https://login.microsoftonline.com/#{ENV['ENTRA_TENANT_ID']}/v2.0",
      client_id: ENV['ENTRA_CLIENT_ID'],
      client_secret: ENV['ENTRA_CLIENT_SECRET'],
      redirect_uri: 'https://shop.example.com/api/v3/admin/auth/callback/entra',
      label: 'Microsoft Entra ID'
    )
  )
  # Optional: SSO-only staff login
  # Spree.admin_authentication_strategies.remove(:email)
end
```

The dashboard lists providers from `GET /api/v3/admin/auth/providers` and completes login at `GET /api/v3/admin/auth/callback/:provider`. **Staff accounts are never auto-provisioned.** A known identity logs in. An existing account whose email matches a *verified* email claim adopts the identity. Everyone else is rejected. Leave `trust_unverified_email: false` unless the IdP's directory owns the email addresses.

### Custom strategy (third-party JWT, Firebase, Cognito, …)

```ruby
# app/models/my_app/auth/external_jwt_strategy.rb
class MyApp::Auth::ExternalJwtStrategy < Spree::Authentication::Strategies::BaseStrategy
  def provider = 'external_idp'

  def authenticate
    payload = verify_with_jwks(params[:token])   # pin algorithms, verify iss + aud
    user = find_or_create_user_from_oauth(
      provider: provider,
      uid: payload.fetch('sub'),
      info: { email: payload['email'], first_name: payload['given_name'], last_name: payload['family_name'] }
    )
    success(user)
  rescue JWT::DecodeError, KeyError
    failure(Spree.t('api.unauthorized'))
  end

  private

  # Yours to implement — BaseStrategy has no JWT helper. Uses the `jwt` gem.
  def verify_with_jwks(token)
    jwks = JWT::JWK::Set.new(MyApp::Auth.fetch_jwks) # cache the issuer's JWKS
    JWT.decode(token, nil, true, algorithms: ['RS256'], jwks: jwks,
               iss: ENV['IDP_ISSUER'], verify_iss: true,
               aud: ENV['IDP_AUDIENCE'], verify_aud: true).first
  end
end

# config/initializers/spree.rb
Rails.application.config.after_initialize do
  Spree.store_authentication_strategies.add(:external_idp, MyApp::Auth::ExternalJwtStrategy)
end
```

- `BaseStrategy` gives you `params`, `request_env`, `user_class`, `success(user)`, `failure(msg)`, `find_user_by_email`, and `find_or_create_user_from_oauth(provider:, uid:, info:, tokens: {})`. The last one maps `provider + uid` to a user through `Spree::UserIdentity`.
- Password-style strategies implement `authenticate`. Redirect strategies define `def self.kind = :redirect` (plus `self.label` for the button) and implement `authorization_url(state:)` and `callback`. The admin surface has the callback route.
- Registries support `add(key, klass)` (overwrites, which is also how you replace `:email`), `remove(key)`, `[key]`, `keys`.
- **Register inside `Rails.application.config.after_initialize`.** Core reassigns the strategy registries in its own `after_initialize`, which wipes anything added at the top level of an initializer or in `to_prepare`. `Spree::UserIdentity` validates `provider` against the keys of the store, admin **and seller** strategy registries, so a missing registration fails on first login.
- `access_token` / `refresh_token` passed in `tokens:` are stored on the identity and **encrypted at rest** (Active Record encryption, `support_unencrypted_data: true` so pre-encryption rows stay readable) — but only when encryption keys are configured; otherwise plaintext. See `spree-security`.
- The third-party token is used **once**, at login. After that the client uses Spree's JWT. Don't try to accept foreign tokens on protected endpoints.
- **Any code that checks a password must go through the lockout.** Wrap it in `Spree::Authentication::Lockout.check(user) { user.valid_password?(pw) }` → `:locked` / `:valid` / `:invalid` (misses count, a hit clears the counter; limits are `Spree::Config[:max_failed_login_attempts]` / `[:lockout_duration]`). Core uses it for login, current-password confirmation and invitation acceptance by an existing account — a password check outside it is an unthrottled guessing oracle.
- Link by email only if the IdP guarantees `email_verified`. Linking on an unverified email lets an attacker take over the account.

## Custom user classes

```ruby
# config/initializers/spree.rb
Spree.customer_class = 'MyApp::Customer'     # String, never the Class
Spree.admin_user_class = 'MyApp::StaffUser'
```

- Customers default to `Spree::Customer` (table `spree_customers`, `cust_` IDs). Staff default to `Spree::AdminUser` (`adm_` IDs). A custom class includes `Spree::CustomerMethods` / `Spree::AdminUserMethods` respectively.
- In code, always go through `Spree.customer_class` / `Spree.admin_user_class`. `Spree.user_class` is a deprecated alias for `customer_class`.
- Customer lifecycle events are named `user.*`. Staff users (`Spree::AdminUser`) publish no lifecycle events.

## Gotchas

- **`Spree::Role.find_or_create_by!(name: 'support')` fails** — roles belong to a resource (the store, or a seller). Create them through the owner: `store.roles.find_or_create_by!(name: 'support').update!(permissions: %w[read_orders read_customers])`.
- `Spree.permissions.assign(...)` and permission-set classes (`Spree::PermissionSets::*`) no longer exist. `assign` raises `PermissionSetsRemovedError`. Coming from 5.x? See `spree-upgrade-5-to-6`.
- New Admin controller returns 500 `MissingScopedResource`: declare `scoped_resource :x` or `skip_scope_check!`.
- A staff member gets 403 with `required_permission` even though the role "looks right": check the role is on **this** store (the `X-Spree-Store-Id` / host) and the key is spelled exactly (`write_fulfillments`, not `write_shipments`).
- A secret key 403s on `/admin_users`: that endpoint needs `read_staff`, which is not part of `settings`.
- A custom admin controller that uses `Spree::Order.find(params[:id])` instead of the store-scoped `scope` leaks data across stores regardless of keys.
- Staff password reset (`POST /api/v3/admin/auth/password_resets`) honors `redirect_url` only when it is on the dashboard's own origin (`Spree::Stores::DashboardUrl`) and the account is staff of that store; otherwise the email links to `<dashboard>/reset-password`. Allowed Origins don't widen this.
- Admin/seller refresh cookies are `SameSite=None; Secure` over HTTPS. A cross-origin dashboard also needs its origin in Settings → Allowed Origins (see `spree-security`).

## Where to read further

- Staff & roles: `node_modules/@spree/docs/dist/developer/core-concepts/staff-roles.md`
- Permission catalog and extension scopes: `node_modules/@spree/docs/dist/developer/customization/permissions.md`
- Custom login strategy: `node_modules/@spree/docs/dist/developer/how-to/custom-api-authentication.md`
- Identity & SSO: `node_modules/@spree/docs/dist/developer/providers/sso.md`
- Admin API auth: `node_modules/@spree/docs/dist/api-reference/admin-api/authentication.md`
- Source: `spree/core/lib/spree/core/permission_configuration.rb`, `spree/core/lib/spree/core/permissions/default_catalog.rb`, `spree/api/app/controllers/concerns/spree/api/v3/scoped_authorization.rb`, `spree/core/app/models/spree/storefront/access_policy.rb`
- Related skills: `spree-api-v3` (scopes list, error envelopes), `spree-security`, `spree-marketplace` (seller audience), `spree-b2b` (company access), `spree-dashboard` (UI permission gating).
