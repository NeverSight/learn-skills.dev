---
name: identity-membership
description: Expert guidance for the Identity vs User split and tenant memberships in Rails. Use when adding users, workspaces, accounts, memberships, roles, join codes, invites, Current.identity, Current.user, or connecting magic-link auth to a tenant. Complements magic-link-auth and activerecord-tenanted. Not Nebula workspace members.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(bin/rails generate*), Bash(bin/rails db:*), Bash(bin/rails test:*), Bash(bin/rails test)
---

# Identity, User, Membership

A person who signs in is an **Identity**. A workspace they can enter is a **Tenant** (or Account). The join is **Membership**. Sessions hang on Identity, never on the tenant-scoped User.

This sits on top of `magic-link-auth`. In SQLite-per-tenant apps it also sits on `activerecord-tenanted`. Fizzy uses the same split in a single database.

## Philosophy

1. **Identity authenticates. Membership authorizes. User is the in-tenant person.** Mixing these is how you leak one customer's users into another shard.
2. **One email, many workspaces.** Don't create a second Identity when someone joins a second tenant.
3. **Create Membership globally, then the tenanted User inside `with_tenant`.** Order matters; a User without a Membership is an orphan.
4. **Join codes are shareable, not emailed magic links.** Different secret, different table.

## The records

```
Identity  (global)  email, sessions, magic links, access tokens
   │
   ├── Membership (global)  identity_id + tenant_id + role
   │
   └── User (tenanted, Cortex/Innkeeper)  identity_id + name + in-tenant role
```

Herald skips the tenanted User: `AccountMembership` on the global DB is enough because account members can see every project. Cortex/Innkeeper need a User **inside** the tenant DB for project assignments, comments, and audit actor.

Fizzy's User is the membership row in the same database (`users.identity_id` + `account_id`). Same idea, no shard.

## Step 1: Identity stays global

```ruby
class Identity < GlobalRecord
  has_many :sessions, dependent: :destroy
  has_many :magic_links, dependent: :destroy
  has_many :memberships, dependent: :destroy
  has_many :tenants, through: :memberships

  validates :email, presence: true, uniqueness: { case_sensitive: false }
  normalizes :email, with: ->(email) { email.downcase.strip }
end
```

Sign-in creates a Session for this Identity (`magic-link-auth`). It does **not** pick a tenant.

## Step 2: Membership is the join

```ruby
class Membership < GlobalRecord
  belongs_to :identity
  belongs_to :tenant  # or :account

  enum :role, { admin: "admin", member: "member" }, default: :member
  validates :identity_id, uniqueness: { scope: :tenant_id }
end
```

Roles live here for "can they enter this workspace at all." Finer ACL (board access, project assignments) lives on tenanted records.

Herald: `AccountMembership` with `owner` / `member`. Innkeeper adds `viewer`.

## Step 3: Tenanted User (when the workspace has a person record)

```ruby
class User < ApplicationRecord
  validates :identity_id, presence: true, uniqueness: true
  enum :role, { admin: "admin", member: "member" }

  def identity
    Identity.find_by(id: identity_id)
  end
end
```

No FK to `identities` — different database. Copy `role` from Membership at join time; don't treat the two roles as independent sources of truth.

## Step 4: Join in one method

```ruby
def join(tenant, name: nil, role: :member)
  was_new = false

  GlobalRecord.transaction do
    membership = memberships.find_or_create_by!(tenant: tenant) do |record|
      record.role = role
      was_new = true
    end

    ApplicationRecord.with_tenant(tenant.external_id) do
      User.find_or_create_by!(identity_id: id) do |user|
        user.role = membership.role
        user.name = name || email.split("@").first.titleize
      end
    end
  end

  was_new
end
```

Rescue `RecordNotUnique` and re-find — two tabs will race. Herald's `Account#add_member!` is the same idea without a tenanted User.

After magic-link verify, if `identity.tenants.none?`, send them to create-tenant / new-project. If they have tenants, send them to the last one or a picker.

## Step 5: Current

```ruby
# After cookie auth (global):
Current.identity = session.identity

# After TenantScoping:
Current.tenant = tenant
Current.user = User.find_by(identity_id: Current.identity.id)

def require_membership!
  redirect_to sign_in_path unless Current.user
end
```

`Current.user` is nil when the Identity is signed in but has no Membership in this tenant. That's a 403, not a sign-in loop.

Don't set `Current.user` from the session. The session doesn't know which tenant the URL selected.

## Step 6: Join codes

Shareable `XXXX-XXXX-XXXX` (Base58, no 0/O/I/l). Global table. One active code per tenant/project.

```ruby
class JoinCode < GlobalRecord
  belongs_to :tenant  # or :project / :account

  def redeem_if
    with_lock do
      increment!(:usage_count) if active? && yield
    end
  end
end
```

Redeem:

1. Load JoinCode by code (global).
2. If not signed in, stash the code in the session and send them through magic-link.
3. `identity.join(tenant)` then `redeem_if`.
4. Rate-limit the redeem endpoint.

Don't use a magic-link code as an invite. Don't increment usage until join succeeds.

## Anti-Patterns

1. **`has_many :sessions` on User** — logout/login is per person, not per workspace.
2. **`find_or_create_by(email:)` inside a tenant** — creates duplicate people; Identity is the uniqueness boundary.
3. **Authorizing with `Current.identity` only** — they might not be a member of this tenant.
4. **Creating User before Membership** — User in a shard with no global join row.
5. **Nebula `Member` on workspace** — different tenancy; don't copy that into an `activerecord-tenanted` app.
6. **Emailing the join code in the magic-link mailer** — two flows, two templates.

## Related

- Sign-in codes and session cookies: `magic-link-auth`
- Shard switching: `activerecord-tenanted`

See [reference.md](reference.md) for Herald vs Cortex/Innkeeper vs Fizzy, and test helpers.
