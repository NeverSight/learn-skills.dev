---
name: manage-scope
description: Set up and manage multi-tenancy or organizational data partitioning using the DaaS-native scope system. Use whenever the user needs tenant isolation, org-level access control, regional data partitioning, or any hierarchical data separation. This is the standard multi-tenancy approach for DaaS applications.
argument-hint: "[levels: e.g. tenant / region/branch] [use-case: multi-tenant|hierarchical|departmental]"
---

# Manage Scope

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

<!-- buildpad-backend: supabase -->
The DaaS **scope system** is the standard way to implement multi-tenancy and hierarchical data partitioning. Scopes live in built-in platform tables (`daas_scope_types`, `daas_scope_items`) and are enforced at the API and permission layers automatically — no junction tables, no custom FK columns on every collection.

> **MCP-First:** Use the `scope` MCP tool for all scope setup. SQL is only needed for custom Supabase RLS policies.

> **Lifecycle Events:** All scope operations emit events: `daas_scope_types.items.create/update/delete`, `daas_scope_items.items.create/update/delete`, `daas_scope_collection_config.items.create/update/delete`. You can attach runtime extensions to react to scope changes (e.g., provisioning resources when a new tenant is created).

---

## Critical Rules

1. **`uri_path` is immutable once assigned** — A scope item's `uri_path` is set on creation and baked into all user-role and access assignments. Never update it; delete and recreate if restructuring.
2. **Permission inheritance is upward-only** — A role granted at a parent scope is effective at all descendant scopes. The reverse is NOT true: a role at a child does NOT grant access at the parent.
3. **Data filter direction is configurable** — `inheritance_mode: "exact"` returns data assigned strictly to the active scope, `"down"` returns data for active scope + all descendants. Set per collection via `update_config`.
4. **Scope context is set by the frontend** — All API calls respect the `X-Resource-Uri` header or `daas_resource_uri` cookie. The backend never assumes a scope; if none is provided, `missing_uri_mode` on each collection decides the fallback.
5. **Scope-scoped access entries** — Assign `resource_uri` on `daas_access` records to restrict a policy to a specific scope node and its descendants. A `null` `resource_uri` means global (no scope restriction).
6. **Admin roles bypass scope** — System admins (`is_admin: true`) operate globally. Scope only affects regular user permission checks.

---

## Architecture

```
Scope Tree (types define levels, items are instances):

  daas_scope_types            daas_scope_items
  ─────────────────           ──────────────────────────────────────────
  id  name      level         id  type_id  name         uri_path
  ──  ────────  ─────         ──  ───────  ───────────  ──────────────────────────────────
  t1  Region    0             i1  t1       APAC         /<t1>:<i1>
  t2  Branch    1             i2  t1       EMEA         /<t1>:<i2>
                              i3  t2       Singapore    /<t1>:<i1>/<t2>:<i3>
                              i4  t2       London       /<t1>:<i2>/<t2>:<i4>

Permission Inheritance (upward propagation):
  Role assigned at /<t1>:<i1>  →  effective at /<t1>:<i1>/<t2>:<i3>  ✓
  Role assigned at /<t1>:<i1>/<t2>:<i3>  →  NOT effective at /<t1>:<i1>  ✗

Data Filtering (per collection):
  inheritance_mode: "exact"  → WHERE resource_uri = '<active>'
  inheritance_mode: "down"   → WHERE resource_uri LIKE '<active>%'

Scope Context Flow:
  ScopeSwitcher UI  →  daas_resource_uri cookie  →  API middleware
                                                 →  enforcePermission({ resourceUri })
                                                 →  getPermissionFilters(user, collection, resourceUri)
```

---

## Steps

### Step 1: Design the Hierarchy (Scope Types)

Define one or more scope types representing the levels of your hierarchy, in order from top to bottom.

**Via MCP — create a top-level type:**

```json
// mcp_daas_scope -> action: create_type
{
  "name": "Region",
  "description": "Top-level geographic region",
  "level": 0,
  "meta": {}
}
```

**Create a child level:**

```json
// mcp_daas_scope -> action: create_type
{
  "name": "Branch",
  "description": "Branch office within a region",
  "level": 1,
  "meta": {}
}
```

**Read all types (to get UUIDs for next steps):**

```json
// mcp_daas_scope -> action: read_types
{}
```

> **Tip:** For a flat tenant model (SaaS with no sub-levels), use a single type (e.g., `Tenant`) at `level: 0`.

---

### Step 2: Create Scope Items

Each scope item is a concrete instance (e.g., "APAC", "Singapore HQ"). Provide `parent_uri` when creating child items.

**Create a root item:**

```json
// mcp_daas_scope -> action: create_item
{
  "type_id": "<region-type-uuid>",
  "name": "APAC",
  "meta": {}
}
```

**Create a child item (scoped under APAC):**

```json
// mcp_daas_scope -> action: create_item
{
  "type_id": "<branch-type-uuid>",
  "name": "Singapore HQ",
  "parent_uri": "/<region-type-uuid>:<apac-item-uuid>",
  "meta": {}
}
```

**Read items to obtain `uri_path` values:**

```json
// mcp_daas_scope -> action: read_items
{
  "type_id": "<branch-type-uuid>"
}
```

The `uri_path` returned (e.g., `/<t1>:<i1>/<t2>:<i3>`) is used in all subsequent role assignments and access entries.

---

### Step 3: Assign Users to Roles in Specific Scopes

Use `assign_user_role` to grant a user a role that is effective only within that scope node and its descendants.

**Assign user to a role within Singapore HQ scope:**

```json
// mcp_daas_scope -> action: assign_user_role
{
  "user_id": "<user-uuid>",
  "role_id": "<branch-manager-role-uuid>",
  "resource_uri": "/<region-type-uuid>:<apac-uuid>/<branch-type-uuid>:<sgp-uuid>"
}
```

**Assign user to a global role (no scope restriction):**

```json
// mcp_daas_users -> action: add_roles
{
  "user_id": "<user-uuid>",
  "roles": ["<global-admin-role-uuid>"]
}
```

> `assign_user_role` writes to `daas_user_roles.resource_uri`. Global roles (null `resource_uri`) are managed through the `users` tool `add_roles` action.

**Read scoped role assignments:**

```json
// mcp_daas_scope -> action: read_user_roles
{
  "user_id": "<user-uuid>"
}
```

**Remove a scoped role assignment:**

```json
// mcp_daas_scope -> action: remove_user_role
{
  "user_id": "<user-uuid>",
  "role_id": "<branch-manager-role-uuid>",
  "resource_uri": "/<region-type-uuid>:<apac-uuid>/<branch-type-uuid>:<sgp-uuid>"
}
```

#### Role Scope Restrictions (`scope_config`)

Roles can restrict **where** they may be assigned using `scope_config`. When `scope_config.allowed_scopes` is set, any attempt to assign that role to a user is validated against the patterns.

| `scope_config` value | Meaning |
|---|---|
| `null` / absent | No restriction — role can be assigned at any scope |
| `{ "allowed_scopes": ["/<type>:<id>/*"] }` | Role can only be assigned at URIs matching any of the listed patterns (supports `*` wildcard segments) |
| `{ "allowed_scopes": [] }` | Role is **locked** — cannot be assigned to any user |

Validation occurs on `daas_users.items.create` and `daas_users.items.update` via a built-in platform hook (`lib/hooks/role-scope.ts`). It applies to:
- `assign_user_role` scope action
- `PATCH /api/users/:id` (role changes)
- `PATCH /api/items/daas_users/:id` (role changes)
- MCP `mcp_daas_users` → `update` action (role changes)

**Error codes on validation failure:**

| Code | Meaning |
|---|---|
| `ROLE_SCOPE_MISMATCH` | The assignment `resource_uri` does not match any pattern in `allowed_scopes` |
| `ROLE_SCOPE_LOCKED` | The role has `allowed_scopes: []` (empty array) — no assignments allowed |

**Checking assignability before assigning:**

When reading roles, the platform computes an `assignable` boolean field based on the current scope context. Use this to filter the role picker UI:

```json
// mcp_daas_roles -> action: list
{}
// Each role in the response includes:
// "assignable": true   — can be assigned at the current scope
// "assignable": false  — scope_config prevents assignment here
```

> **Tip:** Set `scope_config` via `mcp_daas_roles` → `create` or `update` action. See the [create-rbac skill](../create-rbac/SKILL.md) for examples.

---

### Step 4: Configure Collection Data Filtering

Each collection can be independently configured for how it behaves under scope context.

**Read current configs:**

```json
// mcp_daas_scope -> action: read_configs
{}
```

---

#### Scenario A — New collection (via Data Model UI or MCP)

Add the scope URI column as a **Many-to-One field** (type: `text`, related collection: `daas_scope_items`, related field: `uri_path`). Then call `scope: create_config` to register it.

**Via Data Model UI:**
In the field creation modal, select interface "Many to One", set type to `text`, choose related collection `daas_scope_items`, and select related field `uri_path`. Then run `create_config` below.

**Via MCP (two steps):**

```json
// Step 1 — create collection with scope column as M2O field
// mcp_daas_collections -> action: create
// IMPORTANT: resource_uri MUST be created with interface "list-m2o" and special ["m2o"].
// This causes the system to automatically:
//   • Add the FK constraint: resource_uri → daas_scope_items(uri_path)
//   • Insert the daas_relations metadata row
//   • Reload the PostgREST schema cache
// Creating it as a plain "input" string field skips all of this and breaks ?fields=resource_uri.*
{
  "collection": "orders",
  "meta": { "icon": "shopping_cart" },
  "fields": [
    { "field": "id", "type": "uuid", "schema": { "is_primary_key": true } },
    {
      "field": "resource_uri",
      "type": "string",
      "schema": { "is_nullable": true, "max_length": 1024 },
      "meta": {
        "interface": "list-m2o",
        "special": ["m2o"],
        "options": {
          "related_collection": "daas_scope_items",
          "related_field": "uri_path",
          "on_delete": "RESTRICT"
        },
        "note": "Scope URI for tenant filtering"
      }
    }
  ]
}
```

```json
// Step 2 — register scope config row
// mcp_daas_scope -> action: create_config
// The FK + daas_relations were already wired in Step 1.
// This call adds the daas_scope_collection_config row that tells the API middleware
// to apply scope filtering on reads/writes.
{
  "config_data": {
    "collection": "orders",
    "field_name": "resource_uri",
    "inheritance_mode": "exact",
    "missing_uri_mode": "strict"
  }
}
```

> The field can be named anything (e.g. `org_uri`, `tenant_uri`). `resource_uri` is just the convention.
> There is **no automatic wiring based on field name** — `create_config` must always be called explicitly.

---

#### Scenario B — Existing collection (add scope to it)

First add the scope URI column (if not present), then register it with `create_config`.

**If the column doesn't exist yet:**

Via Data Model UI: Add a new field with interface "Many to One", type `text`, related collection `daas_scope_items`, related field `uri_path`.

Via MCP fields tool:
```json
// mcp_daas_fields -> action: create
{
  "collection": "orders",
  "field": "resource_uri",
  "type": "text",
  "meta": {
    "interface": "list-m2o",
    "special": ["m2o"],
    "options": {
      "related_collection": "daas_scope_items",
      "related_field": "uri_path",
      "on_delete": "RESTRICT"
    }
  }
}
```

**Then register scope config:**

```json
// mcp_daas_scope -> action: create_config
// FK + daas_relations were already created by the fields tool above.
// This adds the scope config row that enables API middleware filtering.
{
  "config_data": {
    "collection": "orders",
    "field_name": "resource_uri",
    "inheritance_mode": "exact",
    "missing_uri_mode": "strict"
  }
}
```

---

#### Config Settings Reference

| Setting             | Values                     | Effect                                                                           |
| ------------------- | -------------------------- | ------------------------------------------------------------------------------- |
| `field_name`        | column name in collection  | Name of the TEXT column that stores the scope `uri_path` (usually `resource_uri`) |
| `inheritance_mode`  | `"exact"` \| `"down"`      | `exact` (default): strict match only; `down`: includes all descendant scope items |
| `missing_uri_mode`  | `"strict"` \| `"reject"`   | `strict` (default): no scope = treat as root; `reject`: block if no scope header |

#### Why the FK constraint matters

- Prevents orphaned `resource_uri` values when scope items are deleted
- `ON DELETE RESTRICT` blocks deleting a scope item that is still referenced by collection rows
- Enables API clients to request nested scope item data via M2O expansion: `?fields=resource_uri.name`

**Update config settings (after creation):**

```json
// mcp_daas_scope -> action: update_config
{
  "collection": "orders",
  "config_update": {
    "inheritance_mode": "down"
  }
}
```

---

### Step 5: Assign Policies to Specific Scopes

To restrict a policy to users operating within a given scope and its descendants, set `resource_uri` on the `daas_access` record.

**Assign a policy to a role only within a specific scope:**

```json
// mcp_daas_access -> action: create
{
  "role": "<branch-manager-role-uuid>",
  "policy": "<branch-data-read-policy-uuid>",
  "resource_uri": "/<region-type-uuid>:<apac-uuid>/<branch-type-uuid>:<sgp-uuid>"
}
```

**Assign a global policy (no scope restriction):**

```json
// mcp_daas_access -> action: create
{
  "role": "<global-viewer-role-uuid>",
  "policy": "<read-all-policy-uuid>"
}
```

> When `check_permission_with_scope` is called, it finds access entries where `resource_uri` is an ancestor-or-equal of the active scope URI. A null `resource_uri` always matches.

---

### Step 6: Frontend — Scope Selection & API Integration

The active scope is communicated to all API calls via the `daas_resource_uri` cookie or `X-Resource-Uri` header. See [Client-Side Scope Integration](references/scope-client.instructions.md) for full patterns.

#### Using the ScopeSwitcher Component

`ScopeSwitcher` is a pre-built component that calls `/api/scope/available` to show accessible scopes for the current user and sets the cookie on selection:

```tsx
import ScopeSwitcher from '@/components/ScopeSwitcher';

// Place in your header/navbar:
<ScopeSwitcher />
```

> **Bug 21 warning — NEVER add a "fallback to all tenants" path in the `/api/scope/available` proxy.**
> If DaaS returns non-200 and you fall back to fetching all rows from `daas_scope_items`, every user will see every tenant regardless of their assignments. This is a data leakage vulnerability. Surface the real DaaS error instead:
>
> ```ts
> // ✅ CORRECT — proxy DaaS directly, surface real errors
> const resp = await fetch(`${daasUrl}/api/scope/available`, { headers, cache: 'no-store' });
> return NextResponse.json(await resp.json(), { status: resp.status });
>
> // ❌ WRONG — dangerous fallback
> if (!resp.ok) {
>   const allScopes = await fetch(`${daasUrl}/api/items/daas_scope_items`); // returns ALL tenants
>   return NextResponse.json(await allScopes.json());
> }
> ```

#### ScopeProvider Context (app-wide scope state)

Wrap your layout with a `ScopeProvider` that reads the active scope from the cookie and exposes it to all components.

> **Bug 20:** The `ScopeProvider` must validate the stored cookie URI against the user's actual available scopes. If the URI isn't in the user's list (stale from a previous user's session), clear it. This is the second defensive layer after the logout route clears the cookie.

```tsx
// lib/contexts/ScopeContext.tsx
'use client';
import { apiRequest } from '@/lib/buildpad/services/api-request';
import { createContext, useContext, useEffect, useState } from 'react';

export interface ScopeItem {
  id: string;
  name: string;
  uri_path: string;
}

interface ScopeContextValue {
  resourceUri: string | null;
  activeTenant: ScopeItem | null;
  availableScopes: ScopeItem[];
  setResourceUri: (uri: string | null) => void;
  isLoading: boolean;
}

const ScopeContext = createContext<ScopeContextValue>({
  resourceUri: null, activeTenant: null, availableScopes: [],
  setResourceUri: () => {}, isLoading: true,
});

export function ScopeProvider({ children }: { children: React.ReactNode }) {
  const [resourceUri, setResourceUriState] = useState<string | null>(null);
  const [availableScopes, setAvailableScopes] = useState<ScopeItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const match = document.cookie.match(/(?:^|;\s*)daas_resource_uri=([^;]*)/);
    const cookieUri = match ? decodeURIComponent(match[1]) : null;

    apiRequest<{ data: ScopeItem[] }>('/api/scope/available')
      .then((data) => {
        const scopes = data.data ?? [];
        setAvailableScopes(scopes);

        // Validate the cookie against the user's actual scopes (Bug 20)
        const uriIsValid = cookieUri ? scopes.some(s => s.uri_path === cookieUri) : false;
        if (uriIsValid) {
          setResourceUriState(cookieUri);
        } else {
          if (cookieUri) document.cookie = 'daas_resource_uri=; path=/; max-age=0';
          const autoUri = scopes.length === 1 ? scopes[0].uri_path : null;
          if (autoUri) setResourceUri(autoUri);
        }
      })
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, []);

  const setResourceUri = (uri: string | null) => {
    if (uri) {
      document.cookie = `daas_resource_uri=${encodeURIComponent(uri)}; path=/; max-age=${30 * 24 * 3600}`;
    } else {
      document.cookie = 'daas_resource_uri=; path=/; max-age=0';
    }
    setResourceUriState(uri);
  };

  const activeTenant = availableScopes.find(s => s.uri_path === resourceUri) ?? null;
  return <ScopeContext.Provider value={{ resourceUri, activeTenant, availableScopes, setResourceUri, isLoading }}>{children}</ScopeContext.Provider>;
}

export const useScope = () => useContext(ScopeContext);
```

#### Clearing scope on logout (server-side — Bug 20)

The logout route must clear the cookie server-side so the next user doesn't inherit it:

```ts
// app/api/auth/logout/route.ts — inside performLogout:
cookieStore.delete('daas_resource_uri'); // REQUIRED — prevents 403 for next user
```

#### Making scoped API requests

The cookie is sent automatically on all same-origin requests. For explicit override or cross-origin:

```ts
// Cookie is auto-sent — no extra code needed for standard fetch
const res = await fetch('/api/items/orders', { credentials: 'include' });

// Explicit header override (overrides cookie if both present)
const res = await fetch('/api/items/orders', {
  headers: { 'X-Resource-Uri': resourceUri },
  credentials: 'include',
});
```

#### Handling 403 and scope-related errors

The API returns `403` when the user lacks permission in the active scope, and `400` when the scope URI is malformed or unrecognised.

```ts
// lib/api.ts — centralised fetch wrapper with scope error handling
async function scopedFetch(url: string, options?: RequestInit) {
  const res = await fetch(url, { credentials: 'include', ...options });

  if (res.status === 403) {
    const body = await res.json().catch(() => ({}));
    const code = body?.errors?.[0]?.extensions?.code;

    if (code === 'FORBIDDEN_SCOPE') {
      // User's role doesn't cover the active scope — redirect to scope selector
      window.location.href = '/select-scope';
      return;
    }
    throw new Error('Permission denied');
  }

  if (res.status === 400) {
    const body = await res.json().catch(() => ({}));
    const code = body?.errors?.[0]?.extensions?.code;

    if (code === 'INVALID_SCOPE') {
      // Stale or invalid scope cookie — clear it and reload
      document.cookie = 'daas_resource_uri=; path=/; max-age=0';
      window.location.reload();
      return;
    }
    throw new Error('Bad request');
  }

  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}
```

#### React error boundary for scope access denied

```tsx
// components/ScopeErrorBoundary.tsx — catch scope permission errors in UI
'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export function ScopeGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  useEffect(() => {
    const handler = (event: PromiseRejectionEvent) => {
      if (event.reason?.message === 'Permission denied') {
        router.push('/select-scope?error=access_denied');
      }
    };
    window.addEventListener('unhandledrejection', handler);
    return () => window.removeEventListener('unhandledrejection', handler);
  }, [router]);

  return <>{children}</>;
}
```

---

## Common Scenarios

### Scenario 1: Simple SaaS — each user belongs to one tenant

```
Scope types:  Tenant (level 0)
Scope items:  Acme Corp, Beta LLC, Gamma Inc
Assignment:   Each user gets a role at exactly one tenant URI
Config:       all collections: inheritance_mode=exact, missing_uri_mode=strict
```

Setup:
1. Create one scope type `Tenant` at `level: 0`
2. Create one scope item per customer
3. Assign each user `assign_user_role` at their tenant's `uri_path`
4. Configure all collections with `update_config` (`scope_field`, `exact`, `deny`)
5. Place `<ScopeSwitcher />` in header — users with one tenant never see the switcher

---

### Scenario 2: Regional hierarchy — managers see all branches under them

```
Scope types:  Region (level 0), Branch (level 1)
Scope items:  APAC → [Singapore, Sydney], EMEA → [London, Paris]
Assignment:   Regional manager at /<region>:<apac>
              Branch staff at /<region>:<apac>/<branch>:<sgp>
Config:       orders, tasks: inheritance_mode=down, missing_uri_mode=strict
```

Result:
- Singapore staff see only Singapore data
- APAC manager sees APAC + Singapore + Sydney data
- EMEA staff have no access to APAC data at all

---

### Scenario 3: Department isolation — HR, Finance, Engineering each see their own data

```
Scope types:  Department (level 0)
Scope items:  HR, Finance, Engineering
Assignment:   Cross-department admin at root (no resource_uri = global)
              Dept members assigned at their dept URI
Config:       documents, tickets: inheritance_mode=exact, missing_uri_mode=strict
              announcements: no scope config  (visible to all, no isolation)
```

---

### Scenario 4: Mixed — some collections scoped, some global

Not every collection needs scope filtering. Only configure `update_config` on collections that should be isolated. Collections without a config entry have no scope filtering — they return all data regardless of scope context.

```
Collections with scope config:   orders, tasks, documents
Collections without scope config: announcements, help_articles, categories
```

---

### Scenario 5: User onboarding — no scope assigned yet

When a new user logs in and has no `daas_user_roles` entries with `resource_uri`, `/api/scope/available` returns an empty list. Handle this in the frontend:

```tsx
// app/select-scope/page.tsx
'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SelectScopePage() {
  const [scopes, setScopes] = useState<{ id: string; name: string; uri_path: string }[]>([]);
  const router = useRouter();

  useEffect(() => {
    fetch('/api/scope/available', { credentials: 'include' })
      .then((r) => r.json())
      .then((data) => {
        const selectable = (data.data ?? []).filter((s: any) => s.selectable !== false);
        if (selectable.length === 1) {
          // Auto-select if only one option
          document.cookie = `daas_resource_uri=${encodeURIComponent(selectable[0].uri_path)}; path=/; max-age=${30 * 24 * 3600}`;
          router.replace('/');
        } else {
          setScopes(selectable);
        }
      });
  }, [router]);

  if (scopes.length === 0) {
    return <p>You have not been assigned to any scope. Contact your administrator.</p>;
  }

  return (
    <ul>
      {scopes.map((s) => (
        <li key={s.id}>
          <button onClick={() => {
            document.cookie = `daas_resource_uri=${encodeURIComponent(s.uri_path)}; path=/; max-age=${30 * 24 * 3600}`;
            router.push('/');
          }}>{s.name}</button>
        </li>
      ))}
    </ul>
  );
}
```

---

## Using `mcp_daas_items` with Scope

The `mcp_daas_items` tool accepts a `resource_uri` parameter that fully propagates scope through all CRUD operations, including cross-collection reads and writes via relations.

### What `resource_uri` enforces

| Operation | Effect |
| --------- | ------ |
| **read** | Filters results to items whose scope field matches `resource_uri` (exact or `down` depending on `inheritance_mode`) |
| **create** | Injects `resource_uri` into the scope-enabled field of the new record — client value is overridden |
| **nested O2M create** (inline `{ create: [...] }`) | Also injects `resource_uri` into each child record being created inline |
| **O2M relation read** | Child collection sub-queries are also filtered by `resource_uri` if the child is scope-enabled |
| **update** | Scope filtering applies when resolving which records to update |
| **Omit `resource_uri`** | No scope filtering — global/admin-level access |
| **`resource_uri: null`** | Root scope — only records with no scope assignment |

### Examples

Read orders scoped to a specific branch:
```json
// mcp_daas_items -> action: read
{
  "collection": "orders",
  "resource_uri": "/<region-type-uuid>:<apac-uuid>/<branch-type-uuid>:<sgp-uuid>",
  "query": { "filter": { "status": { "_eq": "pending" } } }
}
```

Create an order with O2M order_lines — both get `resource_uri` injected automatically:
```json
// mcp_daas_items -> action: create
{
  "collection": "orders",
  "resource_uri": "/<region-type-uuid>:<apac-uuid>/<branch-type-uuid>:<sgp-uuid>",
  "data": {
    "customer_name": "Acme Corp",
    "order_lines": {
      "create": [
        { "product": "Widget A", "qty": 3, "price": 100 }
      ]
    }
  }
}
```

> **Source of `resource_uri` in agent context:** The agent should read the user's active scope from the `daas_resource_uri` cookie value or from a prior `mcp_daas_scope` → `read_user_roles` call, then pass that `uri_path` as `resource_uri`.

---

- [Scope Management](references/scope-management.instructions.md) — Full MCP tool reference, resource URI format, collection config settings
- [Scope Permissions](references/scope-permissions.instructions.md) — Permission inheritance, enforcePermission internals, inheritance_mode / missing_uri_mode details
- [Client-Side Scope Integration](references/scope-client.instructions.md) — ScopeProvider, REST API patterns, 400/403 handling, onboarding flow
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
The Buildpad Engine's **scope system** is the standard way to separate data inside an Engine project: customers, regions, branches or departments, as one hierarchy. Scopes live in the Engine's own collections (`daas_scope_types`, `daas_scope_items`, `daas_scope_collection_config`) and the Engine enforces them on every request — no junction tables, no tenant filter on every permission.

On an Engine project the project is one tenant. Every scope hierarchy begins below the project's tenant node: create no scope type without a parent and no scope item without a parent. Scope types, items and collection settings are managed through `/api/scope/types`, `/api/scope/items` and `/api/scope/collection-config` with an administrator's session; the MCP `scope` tool, served to an administrator only, assigns a role to a user at a scope (`assign_user_role`) and registers a collection as tenanted (`create_config`, the body of `POST /api/scope/collection-config`).

> **API first:** sign in as an administrator and call these routes with that session's access token as `Authorization: Bearer`. The token in the project's MCP configuration is accepted only on the MCP endpoint: never send it to these routes.

---

## Critical Rules

1. **Customers are second-level nodes** — the project's tenant node is the first level of the tree. Each customer, region or department of the application is a node below it, of a scope type whose parent is the tenant's type (or a type below it).
2. **`uri_path` is composed by the Engine** — the Engine builds each node's `uri_path` from its ancestry, one `/<type-id>:<item-id>` segment per level, and refuses a `uri_path` sent by a client. It never changes: only a node's `name` and `sort` can be updated. To restructure, create new nodes and move the assignments.
3. **Role assignments reach downward** — a role assigned at a node is effective at that node and at every node below it. The reverse is NOT true: a role at a child does NOT grant access at the parent.
4. **Data filter direction is configurable** — `inheritance_mode: "exact"` returns rows assigned strictly to the active scope, `"down"` (the default) returns the active scope and all descendants. Set per collection in its scope collection setting.
5. **Every request names its scope** — the application sends `X-Resource-Uri: <uri_path>` with every request to a scoped collection. The Engine takes the scope from this header: a cookie on the app's origin never reaches it. Without the header, a user who does not reach every scope is refused with 403 `MISSING_SCOPE`; with `missing_uri_mode: "reject"`, everyone is.
6. **Deletes do not cascade** — a scope type or item that is still referenced (by child nodes, role assignments, access entries or rows of a scoped collection) is refused; remove or repoint each reference first. The tenant node itself cannot be deleted.
7. **Access entries can be scoped too** — an access entry with `resource_uri` gives its policy only at that node and below. A user must hold both ends at the active scope: the role assignment and the role's access entry.

---

## Architecture

```
Scope tree of an Engine project (types define levels, items are nodes):

  daas_scope_types                      daas_scope_items
  ───────────────────────────           ───────────────────────────────────────────────────────────
  id  name      parent_id               id  scope_type_id  name        uri_path
  ──  ────────  ─────────               ──  ─────────────  ──────────  ──────────────────────────────
  T   (tenant)  —                       p   T              (project)   /<T>:<p>
  t1  Region    T                       i1  t1             APAC        /<T>:<p>/<t1>:<i1>
  t2  Branch    t1                      i2  t1             EMEA        /<T>:<p>/<t1>:<i2>
                                        i3  t2             Singapore   /<T>:<p>/<t1>:<i1>/<t2>:<i3>
                                        i4  t2             London      /<T>:<p>/<t1>:<i2>/<t2>:<i4>

Role assignments (downward):
  Role assigned at /<T>:<p>/<t1>:<i1>           →  effective at /<T>:<p>/<t1>:<i1>/<t2>:<i3>  ✓
  Role assigned at /<T>:<p>/<t1>:<i1>/<t2>:<i3>  →  NOT effective at /<T>:<p>/<t1>:<i1>         ✗

Data filtering (per collection):
  inheritance_mode: "exact"  → rows whose scope field equals the active uri_path
  inheritance_mode: "down"   → rows at the active uri_path and at every node below it

Scope context flow:
  Scope switcher (app)  →  daas_resource_uri cookie (the app's own origin)
                        →  X-Resource-Uri header on every Engine request
                        →  the Engine checks the user's assignments, then confines the rows
```

---

## Steps

### Step 1: Find the Tenant Node, then Design the Hierarchy (Scope Types)

Read the project's tree first, with an administrator's session: `GET /api/scope/types` and `GET /api/scope/items`. Inside an Engine project they answer the project's own subtree. Note the tenant node's `id`, its `scope_type_id` and its `uri_path` (`/<tenant-type-id>:<tenant-id>`).

Then define one scope type per level, in order from top to bottom. Each type names the level above it in `parent_id`, starting from the tenant's type.

**Create the first level below the tenant — `POST /api/scope/types`:**

```json
{
  "name": "Region",
  "parent_id": "<tenant-type-id>",
  "sort": 1,
  "note": "Geographic region"
}
```

**Create a child level:**

```json
{
  "name": "Branch",
  "parent_id": "<region-type-id>",
  "sort": 2,
  "note": "Branch office within a region"
}
```

A type takes `name`, `parent_id`, `sort`, `icon` and `note`. A type without `parent_id` is refused: its nodes would be new tenants, which only the host creates.

> **Tip:** For a flat customer model (a SaaS with no sub-levels), use a single type (e.g., `Customer`) whose parent is the tenant's type.

---

### Step 2: Create Scope Items

Each scope item is a concrete node (e.g., "APAC", "Singapore HQ"). Every item names its type and its parent node; the parent must be of the type that the new item's type names as its parent.

**Create a first-level item under the tenant node — `POST /api/scope/items`:**

```json
{
  "name": "APAC",
  "scope_type_id": "<region-type-id>",
  "parent_item_id": "<tenant-node-id>"
}
```

**Create a child item (under APAC):**

```json
{
  "name": "Singapore HQ",
  "scope_type_id": "<branch-type-id>",
  "parent_item_id": "<apac-item-id>"
}
```

**Read items to obtain `uri_path` values:** `GET /api/scope/items`.

The `uri_path` the Engine composed (e.g., `/<tenant-type-id>:<tenant-id>/<region-type-id>:<apac-id>/<branch-type-id>:<sgp-id>`) is used in all subsequent role assignments and access entries.

---

### Step 3: Assign Users to Roles in Specific Scopes

Use `assign_user_role` to grant a user a role that is effective only within that scope node and its descendants. On an Engine project the tool takes its arguments under `assignment`.

**Assign user to a role within Singapore HQ scope:**

```json
// mcp_daas_scope -> action: assign_user_role
{
  "action": "assign_user_role",
  "assignment": {
    "user_id": "<user-uuid>",
    "role_id": "<branch-manager-role-uuid>",
    "resource_uri": "/<tenant-type-id>:<tenant-id>/<region-type-id>:<apac-id>/<branch-type-id>:<sgp-id>"
  }
}
```

**Through the API (administrator's session):**

- Assign: `POST /api/users/<user-uuid>/roles` with `{ "role_id": "<role-uuid>", "resource_uri": "<uri_path>" }` (answers 201).
- Read a user's assignments: `GET /api/users/<user-uuid>/roles`.
- Remove one: `DELETE /api/users/<user-uuid>/roles/<role-uuid>?resource_uri=<uri_path>`.

**A role for the whole project:** assign it at the tenant node's `uri_path`.

> The MCP `users` tool only reads and updates users: every role assignment goes through `assign_user_role` or `POST /api/users/:id/roles`.

#### Role Scope Restrictions (`scope_config`)

Roles can restrict **where** they may be assigned using `scope_config`. When `scope_config.allowed_scopes` is set, any attempt to assign that role to a user is validated against the patterns, which are regular expressions matched against the assignment's `resource_uri`. On an Engine project every `resource_uri` begins with the tenant node's segment, so every pattern starts with it.

| `scope_config` value | Meaning |
|---|---|
| absent | No restriction — role can be assigned at any scope |
| `{ "allowed_scopes": ["^/<tenant-type-id>:<tenant-id>/<branch-type-id>:"] }` | Role can only be assigned at URIs matching any of the listed patterns |
| `{ "allowed_scopes": [] }` | Role is **locked** — cannot be assigned to any user |

The check applies to every role assignment: the `scope` tool's `assign_user_role` and `POST /api/users/:id/roles`.

**Error codes on validation failure:**

| Code | Meaning |
|---|---|
| `ROLE_SCOPE_MISMATCH` | The assignment `resource_uri` does not match any pattern in `allowed_scopes` |
| `ROLE_SCOPE_LOCKED` | The role has `allowed_scopes: []` (empty array) — no assignments allowed |

**Checking assignability before assigning:**

When reading roles, the Engine computes an `assignable` boolean field for the scope the request names in `X-Resource-Uri`. Use this to filter the role picker UI:

```json
// GET /api/roles with X-Resource-Uri: <uri_path>
// Each role in the response includes:
// "assignable": true   — can be assigned at the current scope
// "assignable": false  — scope_config prevents assignment here
```

> **Tip:** Set `scope_config` via `mcp_daas_roles` → `create` or `update` action. See the [create-rbac skill](../create-rbac/SKILL.md) for examples.

---

### Step 4: Configure Collection Data Filtering

Each collection can be independently configured for how it behaves under scope context. Read the current settings with `GET /api/scope/collection-config` (administrator's session).

---

#### Scenario A — New collection

Add the scope URI column as a **Many-to-One field** to `daas_scope_items`, related field `uri_path`. Then register the collection's scope setting.

**Step 1 — create the collection, then the scope field** (see [create-collection](../create-collection/SKILL.md) for the collection itself):

```json
// mcp_daas_fields -> action: create
// The relation (foreign key to daas_scope_items.uri_path) comes from meta.options.
// The fields tool reads the field's name from data.field.
{
  "collection": "orders",
  "data": {
    "field": "resource_uri",
    "type": "string",
    "meta": {
      "interface": "list-m2o",
      "special": ["m2o"],
      "options": {
        "related_collection": "daas_scope_items",
        "related_field": "uri_path",
        "on_delete": "RESTRICT"
      },
      "note": "Scope URI for data separation"
    }
  }
}
```

**Step 2 — register the scope setting — `POST /api/scope/collection-config`:**

```json
{
  "collection": "orders",
  "field_name": "resource_uri",
  "inheritance_mode": "exact",
  "missing_uri_mode": "reject"
}
```

> The field can be named anything (e.g. `org_uri`, `customer_uri`); `resource_uri` is the default `field_name`.
> There is **no automatic wiring based on field name** — the collection is confined only once it is registered.

---

#### Scenario B — Existing collection (add scope to it)

First add the scope URI field (if not present) with the same `fields` payload as Scenario A, then register it with `POST /api/scope/collection-config`. Rows created before the field existed hold no scope; set each one's `resource_uri` (an administrator, with the `items` tool or `PATCH /api/items/<collection>/<id>`) before users rely on the filter.

---

#### Config Settings Reference

| Setting             | Values                     | Effect                                                                           |
| ------------------- | -------------------------- | ------------------------------------------------------------------------------- |
| `field_name`        | column name in collection  | The field that stores the scope `uri_path` (default `resource_uri`)             |
| `inheritance_mode`  | `"exact"` \| `"down"`      | `exact`: the active scope only; `down` (default): the active scope and every node below it |
| `missing_uri_mode`  | `"strict"` \| `"reject"`   | `strict` (default): a request without `X-Resource-Uri` is served only to a user who reaches every scope; `reject`: refused for everyone (`MISSING_SCOPE`) |

#### Why the FK constraint matters

- Prevents orphaned `resource_uri` values: a value must name an existing node
- `ON DELETE RESTRICT`, and the Engine's own reference check, refuse deleting a scope item that is still referenced by collection rows
- Enables API clients to request nested scope item data via M2O expansion: `?fields=resource_uri.name`

**Update settings (after creation) — `PATCH /api/scope/collection-config/orders`:**

```json
{
  "inheritance_mode": "down"
}
```

`DELETE /api/scope/collection-config/orders` removes the setting, and with it the collection's confinement.

---

### Step 5: Assign Policies to Specific Scopes

To restrict a policy to users operating within a given scope and its descendants, set `resource_uri` on the access entry.

**Assign a policy to a role only within a specific scope:**

```json
// mcp_daas_access -> action: create
{
  "data": {
    "role": "<branch-manager-role-uuid>",
    "policy": "<branch-data-read-policy-uuid>",
    "resource_uri": "/<tenant-type-id>:<tenant-id>/<region-type-id>:<apac-id>/<branch-type-id>:<sgp-id>"
  }
}
```

**Assign a policy without a scope restriction:**

```json
// mcp_daas_access -> action: create
{
  "data": {
    "role": "<global-viewer-role-uuid>",
    "policy": "<read-all-policy-uuid>"
  }
}
```

> The Engine counts an access entry when its `resource_uri` is the active scope or one of its ancestors; an entry with no `resource_uri` always counts. The role behind it must itself be assigned at or above the active scope.

---

### Step 6: Frontend — Scope Selection & API Integration

On an Engine project the data API serves no request without a session; only the sign-in, `GET /api/server/info` and the Engine's password routes are served without one (an application must not use them: on an Engine project an administrator resets a user's password). The requests that take their tenant from the header `X-Tenant-Id` are the password sign-in, XAppHub sign-in and anonymous reads of public files. A browser can send `X-Tenant-Id` to the Engine from another origin, without cookies or credentials: the Engine allows that header from any origin and allows no credentialed cross-origin request. Even so, the request that names the tenant is the sign-in made through the application's own server route, which sends `X-Tenant-Id` with the value of `NEXT_PUBLIC_BUILDPAD_TENANT_ID`. A public file shown in a browser is loaded through a signed URL from `/api/files/signed-url`, not by an anonymous read. A request without a session that names no tenant is served from the Engine's host plane, not from the project. A request with a session takes its tenant from the session.

Inside the project, the active scope travels in the `X-Resource-Uri` header. The app keeps the selection in its own `daas_resource_uri` cookie; that cookie is never sent to the Engine, so every data call adds the header — the SDK's calls and every server route that forwards a call. See [Client-Side Scope Integration](references/scope-client.instructions.md) for full patterns.

#### Using the ScopeSwitcher Component

`ScopeSwitcher` is a pre-built component that calls `/api/scope/available` to show accessible scopes for the current user and sets the cookie on selection:

```tsx
import ScopeSwitcher from '@/components/ScopeSwitcher';

// Place in your header/navbar:
<ScopeSwitcher />
```

> **Bug 21 warning — NEVER add a "fallback to all scopes" path in the `/api/scope/available` route.**
> If the Engine returns non-200 and you fall back to fetching all rows of `daas_scope_items`, users can see scopes they hold no assignment for. This is a data leakage vulnerability. Surface the real Engine error instead:
>
> ```ts
> // ✅ CORRECT — forward to the Engine with the user's token, surface real errors
> const headers = await getAuthHeaders(); // from '@/lib/api/auth-headers'
> const resp = await fetch(`${getDaasUrl()}/api/scope/available`, { headers, cache: 'no-store' });
> return NextResponse.json(await resp.json(), { status: resp.status });
>
> // ❌ WRONG — dangerous fallback: never read the scope items collection here
> ```

#### ScopeProvider Context (app-wide scope state)

Wrap your layout with a `ScopeProvider` that reads the active scope from the cookie and exposes it to all components.

> **Bug 20:** The `ScopeProvider` must validate the stored cookie URI against the user's actual available scopes. If the URI isn't in the user's list (stale from a previous user's session), clear it. This is the second defensive layer after the logout route clears the cookie.

```tsx
// lib/contexts/ScopeContext.tsx
'use client';
import { apiRequest } from '@/lib/buildpad/services/api-request';
import { createContext, useContext, useEffect, useState } from 'react';

export interface ScopeItem {
  id: string;
  name: string;
  uri_path: string;
}

interface ScopeContextValue {
  resourceUri: string | null;
  activeTenant: ScopeItem | null;
  availableScopes: ScopeItem[];
  setResourceUri: (uri: string | null) => void;
  isLoading: boolean;
}

const ScopeContext = createContext<ScopeContextValue>({
  resourceUri: null, activeTenant: null, availableScopes: [],
  setResourceUri: () => {}, isLoading: true,
});

export function ScopeProvider({ children }: { children: React.ReactNode }) {
  const [resourceUri, setResourceUriState] = useState<string | null>(null);
  const [availableScopes, setAvailableScopes] = useState<ScopeItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const match = document.cookie.match(/(?:^|;\s*)daas_resource_uri=([^;]*)/);
    const cookieUri = match ? decodeURIComponent(match[1]) : null;

    apiRequest<{ data: ScopeItem[] }>('/api/scope/available')
      .then((data) => {
        const scopes = data.data ?? [];
        setAvailableScopes(scopes);

        // Validate the cookie against the user's actual scopes (Bug 20)
        const uriIsValid = cookieUri ? scopes.some(s => s.uri_path === cookieUri) : false;
        if (uriIsValid) {
          setResourceUriState(cookieUri);
        } else {
          if (cookieUri) document.cookie = 'daas_resource_uri=; path=/; max-age=0';
          const autoUri = scopes.length === 1 ? scopes[0].uri_path : null;
          if (autoUri) setResourceUri(autoUri);
        }
      })
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, []);

  const setResourceUri = (uri: string | null) => {
    if (uri) {
      document.cookie = `daas_resource_uri=${encodeURIComponent(uri)}; path=/; max-age=${30 * 24 * 3600}`;
    } else {
      document.cookie = 'daas_resource_uri=; path=/; max-age=0';
    }
    setResourceUriState(uri);
  };

  const activeTenant = availableScopes.find(s => s.uri_path === resourceUri) ?? null;
  return <ScopeContext.Provider value={{ resourceUri, activeTenant, availableScopes, setResourceUri, isLoading }}>{children}</ScopeContext.Provider>;
}

export const useScope = () => useContext(ScopeContext);
```

#### Clearing scope on logout (server-side — Bug 20)

The logout route must clear the cookie server-side so the next user doesn't inherit it:

```ts
// app/api/auth/logout/route.ts — inside performLogout:
cookieStore.delete('daas_resource_uri'); // REQUIRED — prevents 403 for next user
```

#### Making scoped API requests

The Engine takes the scope from the `X-Resource-Uri` header. Send it with every request to a scoped collection — from a client component through the app's own routes, which forward it with the user's token:

```ts
// Client component → the app's own route (same origin)
const res = await fetch('/api/items/orders', {
  headers: { 'X-Resource-Uri': resourceUri },
});
```

```ts
// app/api/items/[collection]/route.ts — forward the scope with the user's token
const headers = await getAuthHeaders(); // Authorization: Bearer <access token>
const scope = request.headers.get('X-Resource-Uri');
if (scope) headers['X-Resource-Uri'] = scope;
const resp = await fetch(`${getDaasUrl()}/api/items/${collection}${request.nextUrl.search}`, { headers, cache: 'no-store' });
return NextResponse.json(await resp.json(), { status: resp.status });
```

A request to a scoped collection without the header is refused with 403 `MISSING_SCOPE` for any user who does not reach every scope.

#### Handling 403 and scope-related errors

The Engine answers `403` when the user lacks permission or the scope, and `400` when the scope URI names no node.

| HTTP | `extensions.code` | Meaning |
|---|---|---|
| `403` | `FORBIDDEN` | The user's roles at this scope do not grant the action on the collection |
| `403` | `FORBIDDEN_SCOPE` | The user holds no role assignment covering the requested scope |
| `403` | `MISSING_SCOPE` | No `X-Resource-Uri` on a scoped collection that needs one |
| `400` | `INVALID_SCOPE` | The `X-Resource-Uri` names no scope node (malformed, or a deleted node) |
| `401` | `UNAUTHENTICATED`, `TOKEN_INVALID`, `TOKEN_EXPIRED` | No valid session — sign in again |

```ts
// lib/api.ts — centralised fetch wrapper with scope error handling
async function scopedFetch(url: string, resourceUri: string | null, options?: RequestInit) {
  const res = await fetch(url, {
    ...options,
    headers: { ...(options?.headers as Record<string, string>), 'X-Resource-Uri': resourceUri ?? '' },
  });

  if (res.status === 403) {
    const body = await res.json().catch(() => ({}));
    const code = body?.errors?.[0]?.extensions?.code;

    if (code === 'FORBIDDEN_SCOPE' || code === 'MISSING_SCOPE') {
      // No scope, or one the user's roles don't cover — redirect to scope selector
      window.location.href = '/select-scope';
      return;
    }
    throw new Error('Permission denied');
  }

  if (res.status === 400) {
    const body = await res.json().catch(() => ({}));
    const code = body?.errors?.[0]?.extensions?.code;

    if (code === 'INVALID_SCOPE') {
      // Stale or invalid scope cookie — clear it and reload
      document.cookie = 'daas_resource_uri=; path=/; max-age=0';
      window.location.reload();
      return;
    }
    throw new Error('Bad request');
  }

  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}
```

#### React error boundary for scope access denied

```tsx
// components/ScopeErrorBoundary.tsx — catch scope permission errors in UI
'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export function ScopeGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  useEffect(() => {
    const handler = (event: PromiseRejectionEvent) => {
      if (event.reason?.message === 'Permission denied') {
        router.push('/select-scope?error=access_denied');
      }
    };
    window.addEventListener('unhandledrejection', handler);
    return () => window.removeEventListener('unhandledrejection', handler);
  }, [router]);

  return <>{children}</>;
}
```

---

## Common Scenarios

### Scenario 1: Simple SaaS — each user belongs to one customer

```
Scope types:  Customer (parent: the tenant's type)
Scope items:  Acme Corp, Beta LLC, Gamma Inc (each under the tenant node)
Assignment:   Each user gets a role at exactly one customer URI
Config:       all customer collections: inheritance_mode=exact, missing_uri_mode=reject
```

Setup:
1. Create one scope type `Customer` whose `parent_id` is the tenant's type
2. Create one scope item per customer, each with `parent_item_id` = the tenant node
3. Assign each user `assign_user_role` at their customer's `uri_path`
4. Register every customer collection with `POST /api/scope/collection-config` (`field_name`, `exact`, `reject`)
5. Place `<ScopeSwitcher />` in header — users with one customer never see the switcher

---


### Scenario 2: Regional hierarchy — managers see all branches under them

```
Scope types:  Region (parent: the tenant's type), Branch (parent: Region)
Scope items:  APAC → [Singapore, Sydney], EMEA → [London, Paris]
Assignment:   Regional manager at /<T>:<p>/<region>:<apac>
              Branch staff at /<T>:<p>/<region>:<apac>/<branch>:<sgp>
Config:       orders, tasks: inheritance_mode=down, missing_uri_mode=strict
```

Result:
- Singapore staff see only Singapore data
- APAC manager sees APAC + Singapore + Sydney data
- EMEA staff have no access to APAC data at all

---

### Scenario 3: Department isolation — HR, Finance, Engineering each see their own data

```
Scope types:  Department (parent: the tenant's type)
Scope items:  HR, Finance, Engineering
Assignment:   Cross-department admin at the tenant node /<T>:<p>
              Dept members assigned at their dept URI
Config:       documents, tickets: inheritance_mode=exact, missing_uri_mode=reject
              announcements: no scope setting  (visible to all, no isolation)
```

---

### Scenario 4: Mixed — some collections scoped, some global

Not every collection needs scope filtering. Only register a scope collection setting (`POST /api/scope/collection-config`) for collections that should be isolated. Collections without one have no scope filtering — they return all data regardless of scope context.

```
Collections with a scope setting:    orders, tasks, documents
Collections without a scope setting: announcements, help_articles, categories
```

---

### Scenario 5: User onboarding — no scope assigned yet

When a new user logs in and holds no role assignment at a scope, `/api/scope/available` returns an empty list. Handle this in the frontend:

```tsx
// app/select-scope/page.tsx
'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SelectScopePage() {
  const [scopes, setScopes] = useState<{ id: string; name: string; uri_path: string }[]>([]);
  const router = useRouter();

  useEffect(() => {
    fetch('/api/scope/available', { credentials: 'include' })
      .then((r) => r.json())
      .then((data) => {
        const selectable = (data.data ?? []).filter((s: any) => s.selectable !== false);
        if (selectable.length === 1) {
          // Auto-select if only one option
          document.cookie = `daas_resource_uri=${encodeURIComponent(selectable[0].uri_path)}; path=/; max-age=${30 * 24 * 3600}`;
          router.replace('/');
        } else {
          setScopes(selectable);
        }
      });
  }, [router]);

  if (scopes.length === 0) {
    return <p>You have not been assigned to any scope. Contact your administrator.</p>;
  }

  return (
    <ul>
      {scopes.map((s) => (
        <li key={s.id}>
          <button onClick={() => {
            document.cookie = `daas_resource_uri=${encodeURIComponent(s.uri_path)}; path=/; max-age=${30 * 24 * 3600}`;
            router.push('/');
          }}>{s.name}</button>
        </li>
      ))}
    </ul>
  );
}
```

---

## Using the MCP `items` Tool with Scope

On an Engine project the MCP `items` tool takes no scope argument: a `resource_uri` argument is not read. The tool acts with the reach of the project's MCP token, which is an administrator's, so it reads and writes rows of every scope.

To act inside one scope from an agent:

- **Create a row for a scope:** set the collection's scope field to the node's `uri_path` in the data you write; the Engine refuses a value that names no node.
- **Read a scope's rows:** filter on the scope field, for example `"resource_uri": { "_eq": "<uri_path>" }` (exact), or `"_starts_with"` for a node and its descendants.
- **Check what a user sees at a scope:** sign in as that user and call `GET /api/items/<collection>` with `X-Resource-Uri: <uri_path>`. Never send the MCP token to the data API.

A collection registered with `missing_uri_mode: "reject"` refuses every request that names no scope, so the MCP `items` tool cannot reach it: use the API with `X-Resource-Uri` and an administrator's session.

Read a user's assignments (to find the `uri_path` they work in) with `GET /api/users/<user-uuid>/roles` and an administrator's session.

---

- [Scope Management](references/engine-scope-management.instructions.md) — Full API reference for an Engine project: scope types, items, collection settings, role assignments, resource URI format
- [Scope Permissions](references/engine-scope-permissions.instructions.md) — How the Engine checks a scope on each request: assignments, access entries, `inheritance_mode` / `missing_uri_mode` details
- [Client-Side Scope Integration](references/scope-client.instructions.md) — ScopeProvider, REST API patterns, 400/403 handling, onboarding flow
<!-- /buildpad-backend -->
