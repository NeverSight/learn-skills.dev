---
name: create-rbac
description: Set up complete role-based access control for DaaS applications including roles, policies, permissions, access entries, and dynamic filters. Supports patterns like own_items, role_hierarchy, and public_read. For multi-tenancy, use /manage-scope which handles scope-aware role assignment natively. Use when the user needs roles, permissions, access control, or security configuration.
argument-hint: "[collections] [roles] [pattern: own_items|role_hierarchy|public_read]"
---

# Create RBAC Configuration

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

Set up complete role-based access control using DaaS MCP tools.

## RBAC Entity Hierarchy

```
Role → Access → Policy → Permission (collection × action × filter)
```

## Setup Steps

### Step 1: Plan Permission Matrix

<!-- buildpad-backend: supabase -->
```
| Role   | Collection | Action | Fields | Filter                    | Presets                   |
|--------|-----------|--------|--------|---------------------------|---------------------------|
| Editor | articles  | create | *      | null                      | { user_created: $CUR_USER }|
| Editor | articles  | read   | *      | null                      | null                      |
| Author | articles  | update | *      | { user_created: $CUR_USER }| null                     |
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```
| Role   | Collection | Action | Fields | Filter                     |
|--------|-----------|--------|--------|----------------------------|
| Editor | articles  | create | *      | null                       |
| Editor | articles  | read   | *      | null                       |
| Author | articles  | update | *      | { user_created: $CUR_USER } |
```

On an Engine project a permission's `presets` and `validation` are stored but not applied on write, so the matrix has no presets column: `user_created` is filled by its `user-created` special, and every other value comes from the request. The Engine keeps one rule per policy, collection and action.
<!-- /buildpad-backend -->

### Step 2: Create Roles (via MCP)

```json
{
  "name": "roles",
  "arguments": {
    "action": "create",
    "data": { "name": "Editor", "icon": "edit" }
  }
}
```

<!-- buildpad-backend: supabase -->
#### Scope-Restricted Roles

Use `scope_config` to control where a role can be assigned:

```json
{
  "name": "roles",
  "arguments": {
    "action": "create",
    "data": {
      "name": "Branch Manager",
      "icon": "business",
      "scope_config": {
        "allowed_scopes": ["^/.*branch"],
        "validation_message": "{role_name} requires a branch scope"
      }
    }
  }
}
```

| `scope_config` value               | Effect                                |
| ---------------------------------- | ------------------------------------- |
| `null` (default)                   | No restrictions — assignable anywhere |
| `{ "allowed_scopes": [] }`         | **Locked** — cannot be assigned       |
| `{ "allowed_scopes": [".+"] }`     | Scoped only — requires `resource_uri` |
| `{ "allowed_scopes": ["^$"] }`     | Global only — no `resource_uri`       |
| `{ "allowed_scopes": ["^/org:"] }` | Pattern match on `resource_uri`       |

When reading roles, each includes a computed `assignable: boolean` based on the request's `X-Resource-Uri`.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
#### Scope-Restricted Roles

Use `scope_config` to control where a role can be assigned. On an Engine project every scope URI begins with the project's tenant node (`/<tenant-type-uuid>:<tenant-uuid>`), so every pattern starts with that segment:

```json
{
  "name": "roles",
  "arguments": {
    "action": "create",
    "data": {
      "name": "Branch Manager",
      "icon": "business",
      "scope_config": {
        "allowed_scopes": ["^/<tenant-type-uuid>:<tenant-uuid>/<branch-type-uuid>:"],
        "validation_message": "{role_name} requires a branch scope"
      }
    }
  }
}
```

| `scope_config` value                                                   | Effect                                     |
| ---------------------------------------------------------------------- | ------------------------------------------ |
| absent (default)                                                       | No restrictions — assignable anywhere      |
| `{ "allowed_scopes": [] }`                                             | **Locked** — cannot be assigned            |
| `{ "allowed_scopes": ["^/<tenant-type-uuid>:<tenant-uuid>/.+"] }`      | Scoped only — below the tenant node        |
| `{ "allowed_scopes": ["^/<tenant-type-uuid>:<tenant-uuid>/<org-type-uuid>:"] }` | Pattern match on `resource_uri`   |

A role takes `name`, `icon`, `description`, `ip_access`, `enforce_tfa`, `scope_config` and `parent`; `admin_access` and `app_access` belong on a policy, and the Engine refuses them on a role. An assignment outside the patterns is refused with `ROLE_SCOPE_MISMATCH`, and one of a locked role with `ROLE_SCOPE_LOCKED`.

When reading roles, each includes a computed `assignable: boolean` based on the request's `X-Resource-Uri`.
<!-- /buildpad-backend -->

### Step 3: Create Policies

```json
{
  "name": "policies",
  "arguments": { "action": "create", "data": { "name": "Editor Policy" } }
}
```

### Step 4: Link via Access

```json
{
  "name": "access",
  "arguments": {
    "action": "create",
    "data": { "policy": "<policy-id>", "role": "<role-id>" }
  }
}
```

### Step 5: Create Permissions

> ⚠️ **`data.action` is the permission action** (what access is granted: `read`/`create`/`update`/`delete`/`share`), not the tool operation. The top-level `action: "create"` is the CRUD operation. Always pass both.

```json
{
  "name": "permissions",
  "arguments": {
    "action": "create",
    "data": {
      "policy": "<policy-id>",
      "collection": "articles",
      "action": "read",
      "fields": ["*"]
    }
  }
}
```

## Scoped Role Assignments (Multi-tenancy / Hierarchy)

<!-- buildpad-backend: supabase -->
To grant a role that is only effective within a specific scope node (and its descendants), use the `scope` MCP tool instead of the `users` tool:

```json
// mcp_daas_scope -> action: assign_user_role
{
  "user_id": "<user-uuid>",
  "role_id": "<role-uuid>",
  "resource_uri": "/<type-uuid>:<item-uuid>"
}
```

This writes to `daas_user_roles.resource_uri`. The role is only evaluated when the user's active scope URI is equal to or a descendant of `resource_uri`. Global (cross-scope) roles use the `users` tool `add_roles` action (which sets `resource_uri: null`).
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
To grant a role that is only effective within a specific scope node (and its descendants), use the `scope` MCP tool. On an Engine project it takes its arguments under `assignment`:

```json
// mcp_daas_scope -> action: assign_user_role
{
  "action": "assign_user_role",
  "assignment": {
    "user_id": "<user-uuid>",
    "role_id": "<role-uuid>",
    "resource_uri": "/<tenant-type-uuid>:<tenant-uuid>/<type-uuid>:<item-uuid>"
  }
}
```

Through the API, with an administrator's session: `POST /api/users/:id/roles` with `{ "role_id": "<role-uuid>", "resource_uri": "<uri_path>" }` (it answers 201). The role is only evaluated when the user's active scope URI is equal to or a descendant of `resource_uri`. The MCP `users` tool only reads and updates users, so every role assignment goes through one of these two.
<!-- /buildpad-backend -->

See `/manage-scope` skill for full scope setup.

> **Lifecycle Events:** Role and policy assignment operations emit events: `daas_access.items.create/update/delete` (policy assignments), `daas_user_roles.items.create/delete` (role assignments). You can attach runtime extensions to react to permission changes (e.g., sending a welcome notification when a user is granted a role, or invalidating permission caches).

<!-- buildpad-backend: supabase -->
## Dynamic Variables for Filters

| Variable                           | Description       |
| ---------------------------------- | ----------------- |
| `$CURRENT_USER`                    | User's UUID       |
| `$CURRENT_USER.<field>`            | Field on user     |
| `$CURRENT_USER.<relation>.<field>` | Nested relation   |
| `$CURRENT_ROLE`                    | Primary role UUID |
| `$NOW`                             | Current timestamp |
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Dynamic Variables for Filters

| Variable                | Description                                   |
| ----------------------- | --------------------------------------------- |
| `$CURRENT_USER`         | User's UUID                                   |
| `$CURRENT_USER.<field>` | One column of the user's own record           |
| `$CURRENT_ROLE`         | One role UUID of the user                     |
| `$NOW`                  | Current timestamp                             |

On an Engine project a rule that uses any other variable is refused: `$CURRENT_ROLES`, `$CURRENT_POLICIES`, `$CURRENT_ROLE.<field>`, an adjusted `$NOW(...)`, and a path through a relation such as `$CURRENT_USER.<relation>.<field>`.
<!-- /buildpad-backend -->

## Common Filter Patterns

```json
// Own items only
{ "user_created": { "_eq": "$CURRENT_USER" } }

// Published OR own drafts
{ "_or": [{ "status": { "_eq": "published" } }, { "user_created": { "_eq": "$CURRENT_USER" } }] }

// Same organization
{ "organization": { "_eq": "$CURRENT_USER.organization" } }
```

## Security Principles

1. **Least privilege** — start with no access, grant only what's needed
2. **Defense in depth** — item-level AND field-level restrictions
3. **No hardcoded IDs** — always use dynamic variables
4. **Sensitive fields** — never expose password, token, secret fields
5. **Verify** — read back permissions and test with debug endpoint

<!-- buildpad-backend: supabase -->
## Required: Permissions Proxy Route

> ⚠️ **ALWAYS verify this route exists before testing RBAC.** If it's missing, `CollectionList` and `CollectionForm` fall back to empty permissions and silently grant full UI access to all users — making RBAC appear to have no effect. DaaS still enforces permissions server-side, but the UI won't reflect them.

Check whether `app/api/permissions/me/route.ts` exists. If not, create it:

```ts
// app/api/permissions/me/route.ts
import { type NextRequest, NextResponse } from "next/server";
import { getAuthHeaders, getDaaSUrl } from "@/lib/api/auth-headers";

export async function GET(request: NextRequest) {
  try {
    const daasUrl = getDaaSUrl();
    const headers = await getAuthHeaders();
    const searchParams = request.nextUrl.searchParams.toString();
    const url = `${daasUrl}/permissions/me${searchParams ? `?${searchParams}` : ""}`;

    const response = await fetch(url, {
      method: "GET",
      headers,
      cache: "no-store",
    });
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Proxy error";
    return NextResponse.json({ errors: [{ message }] }, { status: 500 });
  }
}
```

This route proxies `GET /permissions/me` from DaaS using the current user's JWT, so Buildpad components can resolve CRUD permissions without cross-origin requests.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Required: Permissions Proxy Route

> ⚠️ **ALWAYS verify this route exists before testing RBAC.** If it's missing, `CollectionList` and `CollectionForm` fall back to empty permissions and silently grant full UI access to all users — making RBAC appear to have no effect. The Engine still enforces permissions on every request, but the UI won't reflect them.

Check whether `app/api/permissions/me/route.ts` exists. If not, create it (this is the route the Buildpad CLI generates):

```ts
// app/api/permissions/me/route.ts
import { type NextRequest, NextResponse } from "next/server";
import { getAuthHeaders, getDaasUrl } from "@/lib/api/auth-headers";

export async function GET(request: NextRequest) {
  try {
    const daasUrl = getDaasUrl();
    const headers = await getAuthHeaders();
    const searchParams = request.nextUrl.searchParams.toString();
    const url = `${daasUrl}/api/permissions/me${searchParams ? `?${searchParams}` : ""}`;

    const response = await fetch(url, { headers, cache: "no-store" });
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Proxy error";
    return NextResponse.json({ errors: [{ message }] }, { status: 500 });
  }
}
```

This route forwards `GET /api/permissions/me` to the Engine with the signed-in user's access token as `Authorization: Bearer`, so Buildpad components can resolve CRUD permissions. The Engine answers `data` (the permissions), `isAdmin` and `moduleAccess`.

On an Engine project some files the Buildpad CLI generates cannot be used yet: `lib/supabase/admin.ts`, the OAuth callback and provider routes of the `external-oauth` module, the server-side enforcer and session modules, and `lib/module-access/enforce.ts`. Do not call them; check module access by forwarding the user's token to `GET <Engine_URL>/api/permissions/me` and reading `isAdmin` and `moduleAccess`. For XAppHub sign-in the CLI installs the `external-oauth-engine` module in place of `external-oauth`; its routes are used as the `add-external-oauth` skill says.
<!-- /buildpad-backend -->

## Required: Module-Level Access Keys (ALWAYS include with RBAC)

After setting up roles and policies, **always** register Module-Level Access Keys for every non-CRUD capability gate in the feature. Raw role name checks (`user.role === 'manager'`, `if (roleName === 'admin')`) are forbidden — every capability gate must go through this system.

### Step 1 — Register key(s)

<!-- buildpad-backend: supabase -->
```json
// mcp_daas_module_access_keys → action: "create"
// Optional: create a folder node first (key: null), then leaf keys under it
{
  "parent_id": "<folder-uuid-or-null>",
  "display_name": "Approve Tickets",
  "description": "Can approve or reject ticket submissions",
  "key": "tickets:approve",
  "sort": 10
}
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```json
// items tool → action: "create", collection: "daas_module_access_keys"
// Optional: create a folder node first (key: null), then leaf keys under it
{
  "name": "items",
  "arguments": {
    "action": "create",
    "collection": "daas_module_access_keys",
    "data": {
      "parent_id": "<folder-uuid-or-null>",
      "display_name": "Approve Tickets",
      "description": "Can approve or reject ticket submissions",
      "key": "tickets:approve",
      "sort": 10
    }
  }
}
```

On an Engine project keys are registered through the `items` tool on `daas_module_access_keys`, or by an administrator with the MCP tool `module_access_keys`.
<!-- /buildpad-backend -->

Key naming convention: `<domain>:<capability>` (e.g. `tickets:approve`, `dashboard:manager_stats`, `reports:export`).
The `system:` and `workflow:` prefixes are platform-reserved — use a project-specific prefix.

### Step 2 — Grant on policy

```json
// mcp_daas_policies → action: "update"
{
  "id": "<policy-uuid>",
  "data": {
    "module_access": {
      "tickets:approve": true
    }
  }
}
```

OR-merge semantics: the user gains the key if *any* of their effective policies sets it to `true`. Admin users bypass all checks.

### Step 3 — Check in React

```tsx
const { hasModuleAccess } = usePermissions();

// Gate UI elements
{hasModuleAccess('tickets:approve') && (
  <Button onClick={handleApprove}>Approve</Button>
)}

// Gate entire pages / sidebar nav items
if (!hasModuleAccess('dashboard:manager_stats')) {
  return <Text c="dimmed">Access denied.</Text>;
}
```

`hasModuleAccess` returns `true` for admins regardless of the policy map.

### Step 4 — Validate (no raw role checks)

After generating `.tsx` files, run:

```bash
grep -rn "role === \|roleName\|user\.role\|is_manager\|is_admin\|isManager\b" app/ components/ 2>/dev/null
grep -rn "detectAdminFromMe\|checkAdmin\|roleObj\.name === 'Administrator'\|admin_access\s*===\s*true\|\bisAdmin\b" app/ components/ 2>/dev/null
```

Any match that is NOT reading from `hasModuleAccess` must be replaced before proceeding.

### Step 5 — Capability Matrix Artifact (STOP-SHIP)

Before considering RBAC setup complete, produce a capability matrix in the response:

- key name (`domain:capability`)
- policy grants (`module_access` map)
- UI guard locations (`hasModuleAccess`)
<!-- buildpad-backend: supabase -->
- API guard locations (module_access OR-merge checks)
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- API guard locations (each server route that forwards the user's token to `GET <Engine_URL>/api/permissions/me` and reads `isAdmin` and `moduleAccess`)
<!-- /buildpad-backend -->

If this artifact is missing, RBAC work is incomplete.

---

## Required: E2E Tests

Create `tests/api/rbac-[app].spec.ts`:

- Test each role's allowed actions
- Test denied actions return 403
- Test item-level filtering works
- Test field-level restrictions

## References

- [RBAC setup guide](references/rbac-setup.instructions.md)
- [Permissions filtering](references/permissions-filtering.instructions.md)
- [Module access checklist](../../references/module-access-checklist.md)
