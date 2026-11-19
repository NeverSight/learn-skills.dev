---
name: descope-fga-schema
description: Author, edit, or apply a Descope FGA schema using the ReBAC/ABAC DSL. Use this skill whenever the user asks to create a new FGA schema, modify an existing one, add types/relations/permissions/conditions, review an authorization model, or apply schema changes to a Descope project. Trigger even if the user says things like "set up authorization", "define roles and permissions", "add team-based access", "make this endpoint check FGA", or "update my authz model" — these almost always mean an FGA schema change.
---

# FGA DSL Authoring

Help the user design and apply Descope FGA schemas. The workflow is: understand the requirement → draft the DSL → validate via dry run → show the user + any data loss warnings → get confirmation → apply.

## MCP Setup — check first, stop if missing

**Before doing anything else**, check whether the Descope Management MCP is connected by looking for tools whose names contain `FGASchema` or `DryRunSchema` (e.g. `mcp__descope__DryRunSchema`). The exact prefix depends on how the user installed the MCP, but the operation IDs are `DryRunSchema`, `CreateFGASchema`, and `GetFGASchema`.

**If the tools are not found:** output only the message below, then end your turn. Do not generate a schema, do not say "here's what I'll apply once connected", do not do any design work, do not continue:

> The Descope Management MCP is required. If not yet installed, install and authorize it, then restart your AI agent and re-run `/descope-fga-schema`. See https://docs.descope.com/mcp/mcp-server#connecting for setup instructions.
> If already installed, it may need authorization. Authorize the Descope MCP, then restart your AI agent and re-run `/descope-fga-schema`.

**If the tools are found:** call `GetFGASchema` immediately as a connectivity probe before doing any other work. If this call returns an authorization error, output only the message below and end your turn:

> The Descope MCP is installed but not authorized. Authorize it, restart Claude Code, and re-run `/descope-fga-schema`.

All FGA operations go through MCP tool calls — never make raw HTTP requests yourself.

Once connected, use the `GetFGASchema` tool to read the current schema before editing — always do this when the user asks to modify an existing schema.

## Grammar

Every schema begins with exactly:
```
model AuthZ 1.0
```
No other name or version is accepted by the API.

Full structure:
```
model AuthZ 1.0

[constraint <Name>[:<Kind>][(args...)]]*
[condition <Name>(<param type, ...>) { <CEL bool expr> }]*

type <TypeName>
  [relation <name>: <TypeRef> [| <TypeRef>]* [with <condExpr>]]*
  [permission <name>: <expr> [with <condExpr>]]*
```

Keywords: `model` `type` `relation` `permission` `condition` `constraint` `with`

Operators:
- Permission expr: `|` union, `&` intersect, `-` subtract. Mix operators with parens: `a | (b - c)`
- Set arrow: `relation.permission` — walks a stored relation to reach the subject's own permissions (e.g. `parent.can_view`)
- Target set: `Type#relation` — see dedicated section below
- `with` clause (relations and permissions): `&` AND, `|` OR, `!` NOT, parens: `with A & (B | !C)`. Conditions are evaluated at **check time** — `with` gates whether the relation or permission counts during evaluation. Only one `with` clause is allowed per relation or permission definition — combine multiple conditions inside it with `&`/`|`/`!`.

**No comments** — the DSL parser has no comment token.

Naming: **PascalCase** for Types, Conditions, Constraints. **snake_case** for relations and permissions.

## Target Set Pattern (`Type#relation`)

When a relation should be held by members of a group (e.g. "any member of this Team"), put `Type#relation` directly in the relation definition. This stores individual member subjects — the right granularity for permission checks.

The indirect way — storing the group itself and deriving membership via a permission — produces correct relation expansion, but it introduces a `contributor_team` relation with no semantic meaning of its own. The only meaningful entity is the individual member. The target set syntax is more concise and directly expresses the intent.

**Avoid (extra relation with no semantic value):**
```
type Repository
  relation contributor_team: Team
  permission contributor: contributor_team.member
```

**Prefer (concise, direct):**
```
type Repository
  relation contributor: Team#member
```

You can mix direct subjects with target set subjects: `relation editor: User | Team#member`

## ABAC Anti-Patterns to Avoid

### Never use a "blocked" relation + subtraction to express a condition

`with` conditions are evaluated at **check time** — when a permission check is made against the context passed in the request. Relations are always stored unconditionally; the condition only affects whether the relation counts during permission evaluation.

The `blocked` relation + subtraction pattern is wrong because it requires manually maintaining a separate set of `blocked` edges in the DB for every excluded user. It's the wrong tool: use `with !Condition` on the relation that grants access instead — it is evaluated automatically at check time with no extra stored relations.

```
// NEVER do this — requires maintaining a separate "blocked" edge per user in the DB
relation creator: User
relation blocked: User with NorthKorea
permission can_delete: creator - blocked

// Right — condition evaluated automatically at check time; no extra edges
relation creator: User with !NorthKorea
permission can_delete: creator
```

### Don't write custom CEL when a built-in constraint covers it

A custom `condition` that checks a numeric range is just reinventing `NumRange` (or `NumAtLeast`/`NumAtMost`). Built-in constraints are more concise, less error-prone, and form a common vocabulary that makes schemas easier for both humans and agents to read and reason about. Use them.

**Wrong:**
```
condition DuringBusinessHours(seconds_since_midnight int) { seconds_since_midnight >= 32400 && seconds_since_midnight < 61200 }
```

**Right:**
```
constraint BusinessHours:NumRange(32400, 61200)
```

(Use a named alias when you want a descriptive name for the constraint.)

## Relations vs Permissions

A **relation** adds an edge to the pure relations graph. A **permission** is a derived rule that reuses existing relations — it adds edges only in the ReBAC graph without introducing new pure-graph edges. Fewer pure-graph edges means less to iterate during checks and a higher chance of cache hits across all checks in the schema, so permissions are more concise and keeping the pure graph lean tends to improve overall check performance as the system scales. Prefer satisfying a requirement with a permission whenever possible. Only introduce a new relation when a direct stored link is truly needed.

When a permission is a strict superset of another, express it by referencing the narrower permission rather than repeating its expansion. This keeps schemas concise and makes the access hierarchy self-documenting — a reader immediately sees that `can_admin` implies `can_write`, which implies `can_read`.

**Avoid (repeats relations across permissions):**
```
permission can_admin: owner
permission can_write: owner | editor
permission can_read: owner | editor | viewer
```

**Prefer (each permission builds on the previous):**
```
permission can_admin: owner
permission can_write: can_admin | editor
permission can_read: can_write | viewer
```

## Built-in Constraints

Use built-in constraints before reaching for custom CEL.

| Constraint | Runtime params (zero-arg form) | Hardcoded form |
|---|---|---|
| `IpRange` | `ip ipaddress, ip_range string` | `IpRange("10.0.0.0/8")` |
| `IpList` | `ip ipaddress, allowed_ips list` | `IpList("1.2.3.4","5.6.7.8")` |
| `DateExpiryEpochSeconds` | `now_epoch_seconds int, expiry_epoch_seconds int` | `DateExpiryEpochSeconds(1735689600)` |
| `StringMatchRegex` | `str string` | `StringMatchRegex("^admin_.*")` (regex required) |
| `NumAtLeast` | `num double, min int` | `NumAtLeast(18)` |
| `NumAtMost` | `num double, max int` | `NumAtMost(100)` |
| `NumRange` | `num double, min int, max int` | `NumRange(0,100)` (min ≤ max) |
| `BoolCheck` | `bool bool, expected bool` | `BoolCheck(true)` |
| `GeoCountry` | `country_code string, allowed_countries list` | `GeoCountry("US","GB")` (ISO 3166-1 alpha-2) |
| `IntList` | `int int, allowed_ints list` | `IntList(1,2,3)` |
| `LabelList` | `label string, allowed_labels list` | `LabelList("foo","bar")` |

**Multiple constraints of the same kind:** You cannot declare the same constraint kind more than once without a named alias — the alias is required to distinguish them. Named aliases share the same runtime param names as the original kind (the alias only changes the constraint's identifier, not its params). This is fine when both constraints operate on the same parameter. If you need two constraints that operate on genuinely different parameters, use a custom CEL condition with a unique param name instead:
```
// Two GeoCountry constraints sharing the same country_code param — alias required, shared param is intentional
constraint FiveEyes:GeoCountry("US","GB","CA","AU","NZ")
constraint Sanction:GeoCountry("KP","IR","SY","RU")

// Need a second IP check with a different param name? Use a custom condition
condition OfficeNetwork(office_ip ipaddress, office_range string) { office_ip.in_cidr(office_range) }
```

**Custom CEL** — only when no built-in covers the logic, or when alias-based param separation isn't enough:
```
condition InNetwork(user_ip ipaddress, allowed_range string) { user_ip.in_cidr(allowed_range) }
```
CEL param types: `int`, `string`, `bool`, `double`, `list`, `ipaddress`. Body must return `bool`. Avoid nested `exists` — the evaluator enforces a cost limit.

## Edit-Safety Protocol

When editing an existing schema, first read the current schema with `GetFGASchema` so you have the real state.

- If the user asks to add something already present, tell them exactly what exists and stop — don't silently overwrite.
- Removing an entire **type** or a **relation definition** from the schema will cause all relation tuples of that type or relation to be permanently deleted from the database. **Editing the target type(s) of a relation definition is equivalent to deleting it and recreating it** — the same data loss risk applies. Always confirm with the user and make sure they understand the impact before proceeding.
- **Exception: editing only the `with` condition of a relation does NOT delete tuples.** Relations are stored unconditionally; the condition is evaluated at check time. Changing `with CondA` to `with CondB` on an otherwise unchanged relation preserves all existing tuples — they simply start being evaluated against the new condition. This is safer than a full relation edit, but still requires caution: callers relying on the old condition's behavior will get different access results after the change.
- Removing or editing a **permission** deletes no relation tuples, but any downstream permissions or checks that depended on it will silently stop working. Confirm with user.
- Adding a new type, relation, or permission is generally safe.

## Validation and Apply Workflow

Follow this sequence every time you generate or edit a DSL:

### Step 1 — Dry run

Use the `DryRunSchema` MCP tool with the proposed DSL. This validates the schema and reports what data would be deleted if applied.

- On error: the schema is invalid. Read the error message, fix the DSL, retry. Cap at 5 iterations — if still failing, stop and show the user the last error.
- On success: continue to Step 2.

The response contains:
```json
{
  "deletesPreview": {
    "hasDeletes": true,
    "relations": ["folder#viewer", "doc#editor"],
    "types": ["LegacyRole"]
  }
}
```

### Step 2 — Show the user

Present:
1. The full proposed DSL (formatted in a code block)
2. If `hasDeletes` is true — a clear warning listing every relation type and namespace type that will be **permanently deleted** from the database

Example warning:
> **Warning: applying this schema will permanently delete all stored relations of these types:**
> - `folder#viewer`
> - `doc#editor`
>
> This cannot be undone. Confirm to proceed.

If `hasDeletes` is false, just show the schema and ask for confirmation.

### Step 3 — Get confirmation

End your turn after Step 2. Do not call `CreateFGASchema` in the same turn as `DryRunSchema` — the user must see the schema and any deletion warnings before you proceed. Wait for the user to reply with explicit approval ("yes", "apply", "go ahead", etc.).

### Step 4 — Apply

Before calling `CreateFGASchema`, verify all three of the following are true:
- You showed the full DSL in a code block in a prior turn (not in this turn)
- You surfaced all deletion warnings from the dry-run response (or confirmed `hasDeletes` was false)
- The user's most recent message is an explicit approval in response to your confirmation prompt

If any of these are not true, do not call `CreateFGASchema`. Go back to Step 2 instead.

When all three are confirmed, call `CreateFGASchema` with the same DSL from the dry run. Confirm success to the user.

The reason this gate matters: `CreateFGASchema` is irreversible. Relation tuples deleted by a schema change cannot be recovered. Skipping confirmation is never safe, even when the change looks minor.

## Examples

### Basic ReBAC with hierarchy

```
model AuthZ 1.0

type User

type Folder

type Doc
  relation owner: User
  relation parent: Folder
  permission can_view: owner | parent.owner
  permission can_edit: owner
```

### Group membership via target set

```
model AuthZ 1.0

type User

type Team
  relation member: User

type Repository
  relation owner: User
  relation contributor: User | Team#member
  permission can_push: owner | contributor
  permission can_read: can_push
```

### ABAC: time-gated access

```
model AuthZ 1.0

constraint ShiftHours:NumRange

type User

type PatientRecord
  relation viewer: User with ShiftHours
  relation owner: User
  permission can_view: viewer | owner
```

### Reused constraint kind with aliases — and `with` on a permission

```
model AuthZ 1.0

constraint FiveEyes:GeoCountry("US","GB","CA","AU","NZ")
constraint Sanction:GeoCountry("KP","IR","SY","RU")
constraint OfficeOnly:IpRange("10.0.0.0/8")

type User

type Resource
  relation allowed: User with FiveEyes & !Sanction
  relation owner: User
  permission can_access: allowed
  permission can_delete: owner with OfficeOnly
```

`allowed` carries geo-gating on the relation — it applies to every permission that uses `allowed`. `can_delete` uses `with` on the permission itself so the IP restriction scopes only deletion, not access.

### Nested permissions with `with` — conditions stack

```
model AuthZ 1.0

constraint BusinessHours:NumRange(32400, 61200)
constraint OfficeNetwork:IpRange("10.0.0.0/8")

type User

type Document
  relation reader: User
  permission can_read: reader with BusinessHours
  permission can_edit: can_read with OfficeNetwork
```

`can_edit` requires both `BusinessHours` (from `can_read`) **and** `OfficeNetwork` (from `can_edit`'s own `with`). Both conditions must be true at check time — `with` clauses on nested permissions accumulate.
