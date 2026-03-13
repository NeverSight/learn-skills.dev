---
name: constructive-safegres
description: Safegres is Constructive's security protocol for expressing authorization as Authz* policy nodes (types + JSON configs). This skill defines each Authz* type, its config shape, semantics, and when to use it. No SQL and no SDK/grant/RLS steps.
compatibility: Node.js 22+, @constructive-io/sdk
metadata:
  author: constructive-io
  version: "1.0.0"
---

# Safegres (Authz* Security Protocol)

Safegres is the **protocol layer** behind Constructive authorization.

- Safegres is expressed as a **policy type** (e.g. `AuthzEntityMembership`) plus a **JSON config** (policy `data`).
- The system compiles these policy nodes into enforcement mechanisms (most notably **PostgreSQL RLS**), but Safegres itself is **not SQL**.

If you are writing automation that provisions security, treat Safegres as the **vocabulary of "what access means"**.

Related skills:
- **TypeScript SDK secure provisioning:** `constructive-security`
- **Relation provisioning:** `constructive-relations`
- **Data* modules (field generators):** `constructive-data-modules` -- defines each Data* nodeType, what fields it creates, and which Authz* policy it pairs with

---

## Core vocabulary (used in every Safegres policy)

### Actor
The **actor** is the authenticated user performing the query.

- `current_user_id()` (conceptually) = the actor's user id.
- In membership resolution tables you'll see this represented as `actor_id`.

### Entity
An **entity** is the scope a membership belongs to.

- For org/group memberships: `entity_id` identifies the org/group.
- For app memberships: membership is global, so there is typically **no per-row entity_id binding**.

### Membership types (scopes)
Safegres policies commonly take `membership_type`:

- `1` = App
- `2` = Org
- `3` = Group

This can be provided as an integer or a string name (resolved via the membership types module).

### Users ARE Organizations (personal orgs)
A key identity property:

- Every user also has an "org identity".
- Each user automatically has an org-level membership to themselves ("personal org").

This matters because an org-level membership check against a field like `owner_id` can often unify:
- "user owns it personally" and
- "org owns it and user is a member"

...under a single `AuthzEntityMembership` policy.

---

## The critical distinction: `AuthzMembership` vs `AuthzEntityMembership`

### `AuthzMembership` (UNBOUND)
**Meaning:** "Is the actor a valid member of *some scope* (app/org/group), optionally with a permission/admin flag?"

- It does **not** bind to any field on the row being accessed.
- Therefore it is primarily an **app-level gate**.

Typical correct uses:
- "Is this request coming from any authenticated/approved user?"
- "Is the actor a super app admin?"
- "Can the actor access a global administrative table that is not entity-scoped?"

Typical incorrect uses:
- Using `AuthzMembership(membership_type=2)` on an entity-scoped table and expecting it to mean "member of *this row's org*".
  - It does not.
  - It means "member of *any org*" (or, more precisely, "has at least one org membership row"), which is almost always too broad.

### `AuthzEntityMembership` (BOUND)
**Meaning:** "Does the actor have membership in the specific entity referenced by *this row's field*?"

- It binds membership evaluation to an `entity_field` on the protected row.
- It is the default choice for entity-scoped resources.

Rule of thumb:
- If your row has an `entity_id`, `organization_id`, or `owner_id` that should scope access: you almost always want **EntityMembership**, not Membership.

---

## Safegres policy node types (leaf types)

Below are the **14 leaf policy node types**.

Each policy is described as:
- **Intent**: what it's for
- **Config**: JSON shape (keys)
- **Semantics**: what it authorizes (in words)
- **Use when** / **Avoid when**

> Note: `AuthzComposite` exists as an *advanced meta-node* for boolean trees; see the section at the end.

---

### 1) `AuthzDirectOwner`

**Intent:** Direct personal ownership.

**Config:**
```json
{ "entity_field": "owner_id" }
```

**Semantics:** Authorize when the row's `{entity_field}` equals the actor's user id.

**Use when:**
- The row is owned by exactly one user, and ownership is represented directly on the row.

**Avoid when:**
- Ownership can be an organization (or user-as-org) and you want "org members can access." Prefer `AuthzEntityMembership` (org scope) instead.

---

### 2) `AuthzDirectOwnerAny`

**Intent:** Multi-owner OR logic.

**Config:**
```json
{ "entity_fields": ["sender_id", "receiver_id"] }
```

**Semantics:** Authorize when the actor id matches **any** of the fields.

**Use when:**
- A record has multiple relevant user id columns and any of them confer access.

---

### 3) `AuthzMembership`

**Intent:** **Unbound** membership gate (app/org/group), optionally permissioned.

**Config (minimal):**
```json
{ "membership_type": 1 }
```

**Config (permissioned):**
```json
{ "membership_type": 1, "permission": "admin_permissions" }
```

Optional keys (depending on policy needs):
- `permission` (string)
- `permissions` (string[])
- `is_admin` (boolean)
- `is_owner` (boolean)

**Semantics:** "The actor has at least one membership record in the given scope, optionally matching permission/admin flags."

**Use when:**
- App-level admin checks.
- Global feature gating.

**Avoid when:**
- Entity-scoped resources (anything that should be constrained by a row's field).

---

### 4) `AuthzEntityMembership`

**Intent:** **Bound** membership-to-row.

**Config (minimal):**
```json
{ "entity_field": "entity_id", "membership_type": 2 }
```

Optional keys:
- `permission` / `permissions`
- `is_admin` / `is_owner`

**Semantics:** "The actor is a member of the entity referenced by this row's `{entity_field}`."

**Use when:**
- Org-owned or group-owned resources.
- `owner_id` that may refer to either a user or an org (because users are orgs via personal orgs).

---

### 5) `AuthzRelatedEntityMembership`

**Intent:** Entity membership where the entity isn't directly on the protected row, but reachable via a join.

**Config (typical):**
```json
{
  "entity_field": "post_id",
  "membership_type": 2,
  "obj_schema": "public",
  "obj_table": "posts",
  "obj_field": "organization_id"
}
```

**Semantics:** "Look up the related row and authorize based on membership in the entity referenced there."

**Use when:**
- Protected rows reference another table (FK), and that related table carries `entity_id` / org id.

---

### 6) `AuthzPeerOwnership`

**Intent:** Peer visibility via shared entity membership (direct owner field on protected row).

**Config (typical):**
```json
{ "owner_field": "owner_id", "membership_type": 2 }
```

Optional keys:
- `permission` / `permissions`
- `is_admin` / `is_owner`

**Semantics (in words):**
- Find the entities (orgs/groups) the actor belongs to.
- Find **other users** who belong to those same entities.
- Allow access when the row's `{owner_field}` is one of those peer user ids.

**Use when:**
- "People in the same org can see each other's user-owned objects."

**Avoid when:**
- The owner is not directly on the protected row (then use `AuthzRelatedPeerOwnership`).

---

### 7) `AuthzRelatedPeerOwnership`

**Intent:** Peer visibility via shared entity membership **through a related table**.

**Config (typical):**
```json
{
  "entity_field": "message_id",
  "membership_type": 2,
  "obj_schema": "public",
  "obj_table": "messages",
  "obj_field": "sender_id"
}
```

Optional keys:
- `obj_ref_field` (defaults to `id`)
- `permission` / `permissions`
- `is_admin` / `is_owner`

**Semantics (in words):**
- Find peers of the actor (as in `AuthzPeerOwnership`).
- Join the related table where each peer is the related row's owner (`obj_field`).
- Allow access when the protected row's `{entity_field}` matches those related rows.

**Use when:**
- Protected row points at another object, and that object's owner is what should be peer-visible.

---

### 8) `AuthzOrgHierarchy`

**Intent:** Visibility via org hierarchy (manager/subordinate relationships).

**Config (typical):**
```json
{ "direction": "down", "anchor_field": "owner_id", "entity_field": "entity_id" }
```

**Semantics:** Authorize based on hierarchy closure relationships anchored at a user field (often `owner_id`).

**Use when:**
- Manager sees subordinate-owned records.
- Subordinate sees manager-owned records.

---

### 9) `AuthzTemporal`

**Intent:** Time-window constraints.

**Config (typical):**
```json
{ "valid_from_field": "valid_from", "valid_until_field": "valid_until" }
```

Either field can be omitted (at least one is required):
- `valid_from_field` only -> "accessible from this time onward" (open-ended future)
- `valid_until_field` only -> "accessible until this time" (open-ended past)
- Both -> classic time window

Additionally, a NULL column value in `valid_until` is treated as "no expiry" (`valid_until IS NULL OR valid_until > now()`), making the window dynamic per row.

Optional keys:
- `valid_from_inclusive` (default `true`)
- `valid_until_inclusive` (default `false`)

**Semantics:** Authorize only when "now" is within the configured time window. Omitting a field removes that boundary.

**Use when:**
- Scheduled content.
- Expiring invites.
- Open-ended "accessible after publish date" (use `valid_from_field` only).

> **Combination guidance:** `AuthzTemporal` answers *when* access is valid, not *who* has access. On its own it means "anyone can access within the time window." In practice, always combine it with an identity-based policy — either as a **restrictive** top-level policy (ANDed with a permissive identity policy) or inside an `AuthzComposite` `BoolExpr`.

> **Overlap with `AuthzPublishable`:** You could approximate published-content gating with `AuthzTemporal` (e.g. `valid_from_field: "published_at"` with no `valid_until_field`). However, `AuthzPublishable` additionally provides the `is_published` boolean toggle, which lets authors unpublish content independently of time. Use `AuthzPublishable` when you need an explicit on/off switch; use `AuthzTemporal` when access is purely time-driven.

---

### 10) `AuthzPublishable`

**Intent:** Draft/published gating.

**Config (default fields):**
```json
{}
```

Optional keys:
- `is_published_field` (default `"is_published"`)
- `published_at_field` (default `"published_at"`)
- `require_published_at` (default `true`)

**Semantics:** Authorize when a record is published (and, if `require_published_at=true`, when `published_at <= now`).

**Use when:**
- Public content that is only visible after publishing.

> **Combination guidance:** `AuthzPublishable` answers *whether content is published*, not *who* can see it. On its own it means "anyone can see published content." In practice, always combine it with an identity-based policy — either as a **restrictive** top-level policy (ANDed with a permissive identity policy like `AuthzEntityMembership`) or inside an `AuthzComposite` `BoolExpr`. See the "Permissive vs Restrictive policies in RLS" section for examples.

> **Overlap with `AuthzTemporal`:** The time component of `AuthzPublishable` (`published_at <= now`) is a subset of what `AuthzTemporal` can express. The key difference is the `is_published` boolean -- a deliberate on/off toggle that `AuthzTemporal` does not provide. If you only need time-window access with no manual toggle, `AuthzTemporal` is sufficient.

---

### 11) `AuthzMemberList`

> **Not recommended.** This policy relies on a UUID array column rather than a proper foreign-key relationship. It does not scale well and bypasses normal relational integrity. Prefer `AuthzEntityMembership` or `AuthzPeerOwnership` with proper FK-based membership tables when possible.

**Intent:** Actor is present in a UUID array column on the same row.

**Config:**
```json
{ "array_field": "member_ids" }
```

**Semantics:** Authorize when the actor id appears in `{array_field}`.

**Use when:**
- Legacy share lists stored as arrays (supported but not recommended for new designs).

---

### 12) `AuthzRelatedMemberList`

> **Not recommended.** Same concern as `AuthzMemberList` -- relies on a UUID array column in a related table rather than proper FK-based membership. Prefer FK-based policies when possible.

**Intent:** Actor is present in a UUID array column in a related table.

**Config (conceptual):**
```json
{
  "owned_schema": "public",
  "owned_table": "documents",
  "owned_table_key": "member_ids",
  "owned_table_ref_key": "document_id",
  "this_object_key": "id"
}
```

**Semantics:** "Follow a reference to a related row that contains an array of member ids."

**Use when:**
- Legacy membership lists stored as arrays in a related table (supported but not recommended for new designs).

---

### 13) `AuthzAllowAll`

> **WARNING: `AuthzAllowAll` is almost never what you want.** It grants unconditional access to every authenticated user for the specified privilege. Before using it, ask yourself: "Should literally every authenticated user be able to read/write this data?" If the answer is no (and it usually is), use a scoped policy like `AuthzDirectOwner` or `AuthzEntityMembership` instead.
>
> **Especially avoid `AuthzAllowAll` on junction tables.** When creating ManyToMany relations with security, match the junction table's policy to the parent tables' policies. If parents use `AuthzDirectOwner`, the junction should too. Using `AuthzAllowAll` on a junction table means any authenticated user can create/delete links between rows they don't own. See the `constructive-relations` skill for junction table security patterns.

**Intent:** Unconditional allow.

**Config:**
```json
{}
```

**Semantics:** Always authorizes.

**Legitimate use cases (rare):**
- Truly public reference data (e.g., a `countries` lookup table that any user should read)
- Public read-only access (combine with restrictive write policies)

**Common misuses:**
- Using `AuthzAllowAll` as a "just make it work" default -- this bypasses all access control
- Using `AuthzAllowAll` on junction tables when parent tables have scoped policies -- the junction should match the parents
- Using `AuthzAllowAll` for both read AND write on any table with user-generated content

---

### 14) `AuthzDenyAll`

**Intent:** Unconditional deny.

**Config:**
```json
{}
```

**Semantics:** Never authorizes.

**Use when:**
- Explicitly blocking a privilege.

---

## Advanced: `AuthzComposite` (meta-node, not a leaf type)

`AuthzComposite` lets you build a boolean expression tree (AND/OR/NOT) over Safegres nodes.

The `data` for an `AuthzComposite` is itself an AST node that the system recursively evaluates. It can be either a single Authz* leaf node or a `BoolExpr` combining multiple nodes.

**Single leaf node wrap** — delegates to one Authz* node:
```json
{
  "AuthzEntityMembership": {
    "entity_field": "owner_id",
    "membership_type": "Organization Member"
  }
}
```

**`BoolExpr` AND** — all conditions must pass:
```json
{
  "BoolExpr": {
    "boolop": "AND_EXPR",
    "args": [
      { "AuthzTemporal": { "valid_from_field": "publish_at" } },
      { "AuthzDirectOwner": { "entity_field": "owner_id" } }
    ]
  }
}
```

**`BoolExpr` OR** — any condition grants access:
```json
{
  "BoolExpr": {
    "boolop": "OR_EXPR",
    "args": [
      {
        "AuthzEntityMembership": {
          "entity_field": "owner_id",
          "membership_type": "Organization Member"
        }
      },
      {
        "AuthzMembership": {
          "membership_type": "App Member",
          "permission": "create_invites"
        }
      }
    ]
  }
}
```

**When to use `AuthzComposite`:**
- Genuinely nested boolean logic that cannot be expressed with separate top-level policies.
- Mixing AND/OR at different levels (e.g., `(A OR B) AND (C OR D)`).
- NOT expressions.
- Non-authz conditions in the same expression tree (e.g., column value checks combined with auth checks).

---

## Permissive vs Restrictive policies in RLS

When Safegres policies compile to PostgreSQL RLS, their interaction depends on whether they are **permissive** or **restrictive**:

- **Permissive** (default): Multiple permissive policies on the same table and privilege are **ORed** together. If **any** permissive policy passes, the row is accessible.
- **Restrictive** (`permissive := false`): Restrictive policies are **ANDed** with the result of permissive policies. **All** restrictive policies must pass *in addition to* at least one permissive policy.

**OR composition (permissive + permissive):**
"Owner OR org admin can see" — add two separate permissive policies. PostgreSQL automatically ORs them:

```
Policy 1 (permissive): AuthzDirectOwner { entity_field: "owner_id" }
Policy 2 (permissive): AuthzEntityMembership { entity_field: "organization_id", membership_type: 2, is_admin: true }

Effective rule: row.owner_id = actor OR actor is admin of row.organization_id
```

**AND composition (permissive + restrictive):**
"Org members can access, but only while the row's time window is active" — add membership as permissive and the time constraint as restrictive:

```
Policy 1 (permissive):  AuthzEntityMembership { entity_field: "entity_id", membership_type: 2 }
Policy 2 (restrictive): AuthzTemporal { valid_from_field: "starts_at", valid_until_field: "ends_at" }

Effective rule: actor is member of row.entity_id AND now() is within [starts_at, ends_at)
```

**3 policies (2 permissive + 1 restrictive):**
"Owner OR org member can access, but only if the row is published":

```
Policy 1 (permissive):  AuthzDirectOwner { entity_field: "owner_id" }
Policy 2 (permissive):  AuthzEntityMembership { entity_field: "organization_id", membership_type: 2 }
Policy 3 (restrictive): AuthzPublishable {}

Effective rule: (row.owner_id = actor OR actor is member of row.organization_id) AND row.is_published = true
```

**4 policies (2 permissive + 2 restrictive):**
"Owner OR org member can access, but only if published AND within the time window":

```
Policy 1 (permissive):  AuthzDirectOwner { entity_field: "owner_id" }
Policy 2 (permissive):  AuthzEntityMembership { entity_field: "organization_id", membership_type: 2 }
Policy 3 (restrictive): AuthzPublishable {}
Policy 4 (restrictive): AuthzTemporal { valid_from_field: "available_from", valid_until_field: "available_until" }

Effective rule: (P1 OR P2) AND R3 AND R4
             = (owner OR org member) AND is_published AND now() in time window
```

Notice the pattern: permissive/restrictive composition always produces `(P1 OR P2 OR ... Pn) AND R1 AND R2 AND ... Rm`. This is powerful but **limited to a single grouping shape**.

---

### When `AuthzComposite` is necessary

Permissive/restrictive composition cannot express arbitrary boolean groupings. Consider:

"Access is allowed if (org member AND published) OR (direct owner AND within time window)":

```
Desired: (AuthzEntityMembership AND AuthzPublishable) OR (AuthzDirectOwner AND AuthzTemporal)
```

This requires OR-ing two AND-groups — impossible with flat permissive/restrictive policies (which always produce a single `(any P) AND (all R)` shape). Use `AuthzComposite`:

```json
{
  "BoolExpr": {
    "boolop": "OR_EXPR",
    "args": [
      {
        "BoolExpr": {
          "boolop": "AND_EXPR",
          "args": [
            { "AuthzEntityMembership": { "entity_field": "organization_id", "membership_type": 2 } },
            { "AuthzPublishable": {} }
          ]
        }
      },
      {
        "BoolExpr": {
          "boolop": "AND_EXPR",
          "args": [
            { "AuthzDirectOwner": { "entity_field": "owner_id" } },
            { "AuthzTemporal": { "valid_from_field": "starts_at", "valid_until_field": "ends_at" } }
          ]
        }
      }
    ]
  }
}
```

**Prefer multiple top-level policies over `AuthzComposite` whenever possible.** They are simpler, easier to read, and easier to maintain. Reserve `AuthzComposite` for cases that genuinely require nested boolean trees like the one above.
