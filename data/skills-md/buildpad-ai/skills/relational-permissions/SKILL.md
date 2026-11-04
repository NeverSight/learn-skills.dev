---
name: relational-permissions
description: Configure permissions on junction and child collections so that nested relational writes (M2M, O2M, M2A) are enforced at every level — not just the parent. Use when setting up write access for collections that participate in relational fields, or when debugging silent no-ops on nested mutations.
argument-hint: "[parent collection] [relation type] [child/junction collection]"
---

# Relational Permissions

<!-- backend-gate:begin v1 -->
**Establish the backend first.** A Buildpad project's backend is either the Buildpad Engine or
Supabase, and some parts of this file hold for one of them only. Before you act on anything in
this file, find the backend with these steps, in order, and stop at the first step that answers:

1. Read `.buildpad/project.json` at the project root. If it is JSON and its field `backend` is
   `"engine"` or `"supabase"`, that is the backend. If `.buildpad/backend-answer.json` names the
   other backend, tell the developer the two files disagree, and follow `.buildpad/project.json`.
2. Otherwise read `.buildpad/backend-answer.json` in the same way; if its `backend` is
   `"engine"` or `"supabase"`, that is the backend.
3. If a folder named `supabase` at the project root holds a file named `config.toml`, or holds a
   folder named `migrations` that holds a file whose name ends in `.sql`, the backend is Supabase.
4. Otherwise ask the developer once: "Is this project's backend the Buildpad Engine or
   Supabase?" Write the answer to `.buildpad/backend-answer.json` as
   `{"buildpadBackendAnswer": 1, "backend": "engine"}` or
   `{"buildpadBackendAnswer": 1, "backend": "supabase"}`, and ask the developer to commit that
   file. Do not add it to `.gitignore`. Never write `.buildpad/project.json`.

To find the backend, do not open an environment file (`.env`, `.env.*`) or an MCP configuration
file, and do not call a tool that returns project credentials.

Then follow only the parts for that backend. A part starts at a line that holds only a comment
whose text is `buildpad` + `-backend: engine` or `buildpad` + `-backend: supabase`, and ends at the
next line that holds only a comment whose text is `/buildpad` + `-backend`. A comment that merely
mentions a backend is not a part. A file whose first line, after any front matter, holds only a
comment whose text is `buildpad` + `-backend-file: engine` (or `supabase`) holds for that backend
only, and so does every file in a folder named `engine-only` or `supabase-only`. Skip the other
backend's parts and copy no code from them; everything else holds for both. On an Engine project, when this file says that
something is not available, tell the developer so and stop: do not build a substitute.
<!-- backend-gate:end -->

Configure permission enforcement for nested relational writes so that create/update/delete operations on junction and child collections are gated by the same two-layer model as top-level collections.

## Why This Matters

When a client sends a PATCH to a parent collection with nested relational data:

```json
PATCH /api/items/cmp_catalogues/:id
{
  "catalogue_services": {
    "create": [{ "service_id": "...", "quantity": 1 }],
    "delete": ["junction-row-id"]
  }
}
```

The platform checks permission on `cmp_catalogues` (the parent). Without relational permission enforcement, the write to `cmp_catalogue_services` (the junction table) would execute **without any permission check** — any user with `update` on the parent could freely create/delete junction rows.

With relational permissions enabled, the platform also checks:
- `create` on `cmp_catalogue_services` (for the `create` block)
- `delete` on `cmp_catalogue_services` (for the `delete` block)

---

## Two-Layer Enforcement Model

<!-- buildpad-backend: supabase -->
```
Request with nested relational data
│
├─ Layer 1: Gate Check (boolean)
│  "Does the user have ANY permission for this action on this child collection?"
│  → 403 if no → abort
│
└─ Layer 2: Item-Level Filter
   "Which specific rows can the user touch?"
   → Resolved from daas_permissions.permissions JSONB
   → Applied as WHERE clause on UPDATE/DELETE
   → Applied as validation/fields/presets on INSERT
```

<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```
Request with nested relational data
│
├─ Layer 1: Gate Check (boolean)
│  "Does the user have ANY permission for this action on this child collection?"
│  → 403 if no → abort, nothing written
│
└─ Layer 2: Item-Level Filter
   "Which specific rows can the user touch?"
   → Resolved from the child collection's permission rule
   → Proved inside the write for UPDATE/DELETE: a row outside the rule → 403
   → Field allowlist checked on INSERT
```

<!-- /buildpad-backend -->
<!-- buildpad-backend: supabase -->
### Layer 1 — Gate Check

Uses `check_permission_with_scope` (scope-aware) or `check_permission` (flat). Returns true/false. Cached per request.

### Layer 2 — Item-Level Filter

| Operation | How applied |
|---|---|
| UPDATE | Filter merged into WHERE clause — non-matching rows unchanged |
| DELETE | Filter merged into WHERE clause — non-matching rows kept |
| Nullify (O2M deselect) | Same as UPDATE |
| INSERT | `fields` (allowlist), `validation` (pre-check), `presets` (server defaults) |
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Layer 1 — Gate Check

The Engine resolves the user's verdict for every child collection and action the request touches, at the request's scope, before it writes anything. On an Engine project this enforcement is unconditional: there is no warn mode and nothing to switch on.

### Layer 2 — Item-Level Filter

| Operation | How applied |
|---|---|
| UPDATE | The row must match the `update` rule, checked under a lock before it is written; a row outside it refuses the whole request (403) |
| DELETE | The same, with the `delete` rule |
| Link / unlink (O2M select, deselect) | Needs `update` on the child, and the row must match the `update` rule |
| INSERT | `fields` (allowlist, the foreign key included). Presets and validation are not applied on an Engine project |

The whole request is one transaction: when any row is refused, nothing is written.
<!-- /buildpad-backend -->

---

## Setup Steps

### Step 1 — Identify the child/junction collections

<!-- buildpad-backend: supabase -->
For each relational field on the parent collection, identify the target table:

| Relation type | Target table |
|---|---|
| M2M | Junction table (from `daas_relations.many_collection` where `junction_field` is set) |
| O2M | Child table (from `daas_relations.many_collection`) |
| M2A | Junction table + each target collection in `one_allowed_collections` |

Use MCP to query:

```json
{
  "method": "tools/call",
  "params": {
    "name": "read_items",
    "arguments": {
      "collection": "daas_relations",
      "query": {
        "filter": { "one_collection": { "_eq": "cmp_catalogues" } }
      }
    }
  }
}
```

### Step 2 — Create permissions on the child/junction collection

For each action the user needs on the child collection, create a `daas_permissions` row under the appropriate policy:

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_item",
    "arguments": {
      "collection": "daas_permissions",
      "item": {
        "policy": "<policy-uuid>",
        "collection": "cmp_catalogue_services",
        "action": "create",
        "fields": ["catalogue_id", "service_id", "quantity", "unit_price"],
        "presets": {
          "user_created": "$CURRENT_USER"
        },
        "permissions": null,
        "validation": null
      }
    }
  }
}
```

Repeat for `update` and `delete` as needed:

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_item",
    "arguments": {
      "collection": "daas_permissions",
      "item": {
        "policy": "<policy-uuid>",
        "collection": "cmp_catalogue_services",
        "action": "delete",
        "permissions": {
          "user_created": { "_eq": "$CURRENT_USER" }
        }
      }
    }
  }
}
```

<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
For each relational field on the parent collection, identify the target collection:

| Relation type | Target collection |
|---|---|
| M2M | Junction collection (a relation whose `meta.junction_field` is set) |
| O2M | Child collection (the relation whose `related_collection` is the parent) |
| M2A | Junction collection + each target collection in `meta.one_allowed_collections` |

Use the MCP `relations` tool to read the relations (it is for administrators):

```json
{
  "name": "relations",
  "arguments": {
    "action": "read"
  }
}
```

Keep the rows that touch the parent: a row whose `related_collection` is the parent (its `meta.one_field` names the parent's alias field), and a row whose `collection` is the parent (an M2O of the parent).

### Step 2 — Create permissions on the child/junction collection

For each action the user needs on the child collection, create a permission rule under the appropriate policy with the MCP `permissions` tool. The Engine keeps one rule per policy, collection and action.

```json
{
  "name": "permissions",
  "arguments": {
    "action": "create",
    "data": {
      "policy": "<policy-uuid>",
      "collection": "cmp_catalogue_services",
      "action": "create",
      "fields": ["catalogue_id", "service_id", "quantity", "unit_price"],
      "permissions": null
    }
  }
}
```

Repeat for `update` and `delete` as needed:

```json
{
  "name": "permissions",
  "arguments": {
    "action": "create",
    "data": {
      "policy": "<policy-uuid>",
      "collection": "cmp_catalogue_services",
      "action": "delete",
      "permissions": {
        "user_created": { "_eq": "$CURRENT_USER" }
      }
    }
  }
}
```

On an Engine project presets and validation are not applied, so the rules carry neither: `user_created` is filled by its `user-created` special, and every other value comes from the request.

<!-- /buildpad-backend -->
<!-- buildpad-backend: supabase -->
### Step 3 — Verify with the audit endpoint

```
GET /api/utils/audit-relational-permissions
```

This returns a report of all junction/child collections that are missing permissions for roles with parent access. After your setup, the child collection should no longer appear in the gap report.

### Step 4 — Enable enforcement

Set the environment variable:

```
ENFORCE_RELATIONAL_PERMISSIONS=true
```

⚠️ In warn mode (`false`, default), violations are logged but not blocked. Switch to `true` only after all permissions are seeded.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Step 3 — Verify with the users' own tokens

Sign in as a user who holds the policy and send the nested write (`PATCH /api/items/cmp_catalogues/:id` with the `create`/`delete` blocks): it answers 200. Sign in as a user who holds `update` on the parent but no rule on `cmp_catalogue_services`: the same request answers 403, naming the action and the child collection, and nothing is written.

### Step 4 — Nothing to enable

On an Engine project enforcement is unconditional: there is no warn mode and no setting to switch.
<!-- /buildpad-backend -->

---

<!-- buildpad-backend: supabase -->
## Filter Rule Constraints

🔴 **CRITICAL:** Not all filter patterns work on child/junction mutation queries. When writing `permissions` JSONB rules for child collections, use only the patterns marked ✅ below.

### Supported (use these)

| Pattern | Example |
|---|---|
| Scalar operators | `{ "status": { "_eq": "active" } }` |
| `_in` / `_nin` | `{ "type": { "_in": ["A", "B"] } }` |
| `_null` / `_nnull` | `{ "deleted_at": { "_null": true } }` |
| String operators | `{ "name": { "_starts_with": "TMP-" } }` |
| `_between` / `_regex` | `{ "sort": { "_between": [1, 100] } }` |
| `_and` / `_or` (scalar only) | `{ "_and": [{ "status": { "_eq": "draft" } }, { "user_created": { "_eq": "$CURRENT_USER" } }] }` |
| `$CURRENT_USER` / `$CURRENT_POLICIES` | `{ "user_created": { "_eq": "$CURRENT_USER" } }` |

### Unsupported — do NOT use on child collections

| Pattern | Why | Impact if used |
|---|---|---|
| `_has` (relation existence) | PostgREST UPDATE/DELETE don't support `!inner` joins | Filter silently ignored — wider access than intended |
| Dot-notation (`owner.status`) | Same as `_has` — requires embedded-resource joins | Filter silently ignored |
| `_some` / `_none` | Not implemented in filter translator | Operator silently skipped — wider access |
| `_or` mixing scalar + relational | Relational branch silently dropped | Partial enforcement only |
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Filter Rule Constraints

On an Engine project a child or junction rule is proved inside the statement that writes the row, so every filter the Engine accepts is enforced, relational ones included. A filter it cannot apply is refused with an error, never skipped.

### Supported (use these)

| Pattern | Example |
|---|---|
| Scalar operators | `{ "status": { "_eq": "active" } }` |
| `_in` / `_nin` | `{ "type": { "_in": ["A", "B"] } }` |
| `_null` / `_nnull` | `{ "deleted_at": { "_null": true } }` |
| String operators | `{ "name": { "_starts_with": "TMP-" } }` |
| `_between` / `_regex` | `{ "sort": { "_between": [1, 100] } }` |
| `_and` / `_or` | `{ "_and": [{ "status": { "_eq": "draft" } }, { "user_created": { "_eq": "$CURRENT_USER" } }] }` |
| `$CURRENT_USER`, `$CURRENT_USER.<field>`, `$CURRENT_ROLE`, `$NOW` | `{ "user_created": { "_eq": "$CURRENT_USER" } }` |
| One relation deep: a dot-notation key, or `_has` | `{ "owner.status": { "_eq": "active" } }` |

### Refused — do NOT use

| Pattern | What the Engine does |
|---|---|
| `$CURRENT_POLICIES`, `$CURRENT_ROLES` | Refuses the rule: it does not resolve them |
| A path through two relations (`owner.team.status`) | Refuses the rule |
| `_some` / `_none` | Refuses the rule |
| Nested-object form (`{ "owner": { "status": { ... } } }`) | Refuses the rule as an unknown operator |
<!-- /buildpad-backend -->

---

<!-- buildpad-backend: supabase -->
## Nesting Depth Limit

Relational writes are processed **one level deep**. Nested relational fields inside a child record payload are **not recursively processed**.

```
✅ parent → child (1 level)
❌ parent → child → grandchild (2 levels — grandchild ignored)
```

To mutate deeper levels, issue separate API calls for each level.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Nesting Depth Limit

Relational writes are processed up to **three relations deep**. A many-to-many that creates its far-side row uses two of them.

```
✅ parent → child (1 level)
✅ parent → junction → far side (2 levels)
✅ parent → child → grandchild → great-grandchild (3 levels)
❌ a fourth level — the request is refused (400), naming the field
```

Rows of the Engine's own collections (`daas_*`) are never written through a relational field: write them through their own routes. A nested write goes through `POST` or `PATCH /api/items/:collection`; the MCP `items` tool refuses one. One request may write only a limited number of related items, and more is refused with 413.
<!-- /buildpad-backend -->

---

## Common Patterns

<!-- buildpad-backend: supabase -->
### Full junction access scoped to current user

```json
{
  "action": "create",
  "collection": "catalogue_services",
  "fields": ["catalogue_id", "service_id", "quantity", "unit_price"],
  "presets": { "user_created": "$CURRENT_USER" }
}
```
```json
{
  "action": "delete",
  "collection": "catalogue_services",
  "permissions": { "user_created": { "_eq": "$CURRENT_USER" } }
}
```

### O2M child with field restriction + validation

```json
{
  "action": "create",
  "collection": "order_items",
  "fields": ["product_id", "quantity", "unit_price"],
  "validation": { "quantity": { "_gte": 1, "_lte": 100 } },
  "presets": { "user_created": "$CURRENT_USER" }
}
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Full junction access scoped to current user

```json
{
  "action": "create",
  "collection": "catalogue_services",
  "fields": ["catalogue_id", "service_id", "quantity", "unit_price"]
}
```
```json
{
  "action": "delete",
  "collection": "catalogue_services",
  "permissions": { "user_created": { "_eq": "$CURRENT_USER" } }
}
```

### O2M child with field restriction

```json
{
  "action": "create",
  "collection": "order_items",
  "fields": ["product_id", "quantity", "unit_price"]
}
```

On an Engine project `validation` is not applied: check values such as `quantity` in the application, or in a stored filter hook (see the `hooks-extensions` skill), before they are written.
<!-- /buildpad-backend -->

### Read-only junction (user cannot modify relations)

Do not create any `create`/`update`/`delete` permission on the junction collection. The gate check will reject all mutation attempts.

---

## References

- [Create RBAC Skill](../create-rbac/SKILL.md)
- [Grant Module Access Skill](../grant-module-access/SKILL.md)
- [Manage Scope Skill](../manage-scope/SKILL.md)
