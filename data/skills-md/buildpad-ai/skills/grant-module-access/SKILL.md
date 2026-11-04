---
name: grant-module-access
description: Grant application-level capability flags to users via DaaS Module-Level Access Keys. Keys such as `workflow:approve` or `system:logs` are registered in `daas_module_access_keys`, toggled on policies, and checked in React with `usePermissions().hasModuleAccess(key)` or in API routes with the OR-merge logic already built into the platform. Use when an application needs to gate a feature, page, or workflow command that is not tied to a collection CRUD operation.
argument-hint: "[key names to register] [policies/roles to grant them to]"
---

# Grant Module-Level Access

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

Add named capability flags to DaaS policies using the platform's built-in Module-Level Access system. No custom columns, no copied server utilities, no manual context wiring needed.

## Concept

DaaS has two independent permission dimensions:

| Dimension | Stored on | Controls |
|---|---|---|
| **Record-Level Access** | `daas_permissions` rows | Which collections a user can CRUD, and with what filters |
| **Module-Level Access** | `daas_policies.module_access` (JSONB) | Whether a user has a named application capability |

Module access keys live in `daas_module_access_keys` — a hierarchical registry. Each leaf key has a format like `workflow:approve` or `system:logs`. Folder nodes (`key = null`) group related keys in the UI.

**OR-merge semantics**: a user holds a key if *any* of their effective policies sets it to `true`. Admin users bypass all checks.

---

<!-- buildpad-backend: supabase -->
## Step 1: Register the Key(s)

Use the MCP `module_access_keys` tool (or the **Module Access Keys** page at `/module-access-keys`).

### Create a folder group (optional)

```json
{
  "name": "module_access_keys",
  "arguments": {
    "action": "create",
    "data": {
      "display_name": "Reporting",
      "description": "Reporting and analytics access",
      "key": null,
      "sort": 40
    }
  }
}
```

### Create leaf key(s)

```json
{
  "name": "module_access_keys",
  "arguments": {
    "action": "create",
    "data": {
      "parent_id": "<folder-uuid>",
      "display_name": "Export Reports",
      "description": "Download CSV/XLSX exports from the Reports page",
      "key": "reports:export",
      "sort": 10
    }
  }
}
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Step 1: Register the Key(s)

On an Engine project register keys with the MCP `items` tool on the collection `daas_module_access_keys`, as below. An administrator's agent may instead use the MCP tool `module_access_keys` (`create`, `read`, `update`, `delete`), which is listed and served to an administrator only.

### Create a folder group (optional)

```json
{
  "name": "items",
  "arguments": {
    "action": "create",
    "collection": "daas_module_access_keys",
    "data": {
      "display_name": "Reporting",
      "description": "Reporting and analytics access",
      "key": null,
      "sort": 40
    }
  }
}
```

### Create leaf key(s)

```json
{
  "name": "items",
  "arguments": {
    "action": "create",
    "collection": "daas_module_access_keys",
    "data": {
      "parent_id": "<folder-uuid>",
      "display_name": "Export Reports",
      "description": "Download CSV/XLSX exports from the Reports page",
      "key": "reports:export",
      "sort": 10
    }
  }
}
```
<!-- /buildpad-backend -->

Key format rules:
- Lowercase letters, digits, and `:`, `_`, `.`, `/`, `-` only
- Must start with a letter
- Globally unique across all keys
- Convention: `<domain>:<capability>` — e.g. `workflow:approve`, `system:logs`, `reports:export`

<!-- buildpad-backend: supabase -->
`system:` and `workflow:` namespaces contain platform-seeded keys. Use a project-specific prefix for application keys.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
The Engine seeds `system:logs`, `workflow:approve` and `workflow:reject`; the `system:` and `workflow:` namespaces are the platform's. Use a project-specific prefix for application keys.
<!-- /buildpad-backend -->

---

## Step 2: Grant the Key on a Policy

Use the MCP `policies` tool:

```json
{
  "name": "policies",
  "arguments": {
    "action": "update",
    "id": "<policy-uuid>",
    "data": {
      "module_access": {
        "reports:export": true
      }
    }
  }
}
```

Only keys set to `true` are granted. Keys set to `false` or absent are not granted.
Multiple policies held by a user are OR-merged — the user gains the key if *any* policy grants it.

Alternatively, toggle the key in the **Module-Level Access** tab of the Policy editor UI at `/policies/<id>`.

---

## Step 3: Check in React (Client Components)

`hasModuleAccess` is already wired into `PermissionsContext` — no code changes needed:

```tsx
import { usePermissions } from '@/lib/buildpad/hooks';

function ReportsPage() {
  const { hasModuleAccess } = usePermissions();

  return (
    <div>
      <ReportsTable />
      {hasModuleAccess('reports:export') && (
        <Button onClick={handleExport}>Export</Button>
      )}
    </div>
  );
}
```

`hasModuleAccess` returns `true` for admins regardless of the `module_access` map.

---

<!-- buildpad-backend: supabase -->
## Step 4: Check in API Routes (Server-Side)

Query `daas_policies.module_access` directly using the `get_user_policies` RPC:

```typescript
// app/api/reports/export/route.ts
import { createSupabaseServerClient } from '@/lib/supabase/server';

export async function GET() {
  const supabase = await createSupabaseServerClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return new Response('Unauthorized', { status: 401 });

  const { data: policyIds } = await supabase.rpc('get_user_policies', { user_id: user.id });
  const { data: policies } = await supabase
    .from('daas_policies')
    .select('module_access, admin_access')
    .in('id', policyIds ?? []);

  const isAdmin = policies?.some(p => p.admin_access);
  const canExport = isAdmin || policies?.some(
    p => (p.module_access as Record<string, boolean>)?.['reports:export'] === true
  );

  if (!canExport) return new Response('Forbidden', { status: 403 });

  // ... generate export
}
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Step 4: Check in API Routes (Server-Side)

On an Engine project some files the Buildpad CLI generates cannot be used yet: `lib/supabase/admin.ts`, the OAuth callback and provider routes of the `external-oauth` module, the server-side enforcer and session modules, and `lib/module-access/enforce.ts`. Do not call them; check module access by forwarding the user's token to `GET <Engine_URL>/api/permissions/me` and reading `isAdmin` and `moduleAccess`. For XAppHub sign-in the CLI installs the `external-oauth-engine` module in place of `external-oauth`; its routes are used as the `add-external-oauth` skill says.

```typescript
// app/api/reports/export/route.ts
import { getAuthHeaders, getDaasUrl } from '@/lib/api/auth-headers';

export async function GET() {
  const headers = await getAuthHeaders(); // the signed-in user's access token as Authorization: Bearer
  if (!headers.Authorization) return new Response('Unauthorized', { status: 401 });

  const res = await fetch(`${getDaasUrl()}/api/permissions/me`, { headers, cache: 'no-store' });
  if (!res.ok) return new Response('Unauthorized', { status: res.status });
  const { isAdmin, moduleAccess } = await res.json();

  // An administrator passes every gate.
  const canExport = isAdmin === true || moduleAccess?.['reports:export'] === true;
  if (!canExport) return new Response('Forbidden', { status: 403 });

  // ... generate export
}
```
<!-- /buildpad-backend -->

---

## Step 5: Gate Workflow Commands (optional)

<!-- buildpad-backend: supabase -->
If the capability controls a workflow state-machine transition, add `module_access_keys` to the command definition:

```json
{
  "name": "approve",
  "next_state": "approved",
  "policies": [],
  "module_access_keys": ["workflow:approve"],
  "actions": []
}
```

`policies` and `module_access_keys` are OR'd — the user may execute the command if they satisfy *either* list. Existing workflows with only `policies` are unaffected.

Two things to know when a key gates a workflow command (observed on DaaS 0.1.98 and Buildpad UI 3.0.0):

- **The transition endpoint has no administrator bypass.** Unlike `hasModuleAccess`, it reads the grant map only, so an administrator who does not hold the key is answered 403. Grant the key on the administrators' policy if they must be able to run the command.
- **`WorkflowButton` does not filter by module access keys.** It offers a key-gated command to every user and the server refuses the ones without the key. Expect that 403 in the UI, or filter the commands yourself with `hasModuleAccess`.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
If the capability controls a workflow state-machine transition, add `module_access_keys` to the command definition:

```json
{
  "name": "approve",
  "next_state": "approved",
  "policies": [],
  "module_access_keys": ["workflow:approve"],
  "actions": []
}
```

`policies` and `module_access_keys` are OR'd — the user may execute the command if they satisfy *either* list. Existing workflows with only `policies` are unaffected.

Two things to know when a key gates a workflow command:

- **An administrator passes every gate.** On an Engine project the transition endpoint lets an administrator run every command, as `hasModuleAccess` does.
- **`WorkflowButton` does not filter by module access keys** (observed on Buildpad UI 3.0.0). It offers a key-gated command to every user and the server refuses the ones without the key. Expect that 403 in the UI, or filter the commands yourself with `hasModuleAccess`.
<!-- /buildpad-backend -->

---

## Step 6: Gate Pages and Sidebar Nav (optional)

For pages that should be entirely inaccessible without the key, add a guard at the top of the page component and hide the sidebar nav item:

```tsx
// app/reports/page.tsx
'use client';
import { usePermissions } from '@/lib/buildpad/hooks';

export default function ReportsPage() {
  const { hasModuleAccess } = usePermissions();

  if (!hasModuleAccess('reports:export')) {
    return <Paper p="xl"><Text c="red">You do not have access to this page.</Text></Paper>;
  }

  return <ReportsContent />;
}
```

```tsx
// A client wrapper around AuthenticatedShell that filters the nav items it passes in
{hasModuleAccess('reports:export') && (
  <SidebarNavItem href="/reports" label="Reports" icon={<IconChartBar size={18} />} ... />
)}
```

`hasModuleAccess` already answers `true` for an administrator — do not add `isAdmin ||` in front of it. The check also fails closed while permissions load, so a gated item appears a moment after the page does rather than flashing in and out.

To gate a whole area that only administrators should see (no policy grants it), register a key, grant it on no policy, and check it the same way: administrators pass, everyone else does not, and the area can later be delegated by granting the key.

---

## Summary

<!-- buildpad-backend: supabase -->
| Step | Where | What |
|---|---|---|
| 1 | MCP `module_access_keys` / `/module-access-keys` UI | Register key in the platform catalogue |
| 2 | MCP `policies` / Policy editor UI | Toggle key `true` on the relevant policy |
| 3 | React component | `usePermissions().hasModuleAccess('key')` |
| 4 | API route | Query `daas_policies.module_access` via `get_user_policies` RPC |
| 5 | Workflow command JSON (optional) | Add `module_access_keys: ["key"]` |
| 6 | `LayoutShell.tsx` (optional) | Hide nav item unless key is granted |
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
| Step | Where | What |
|---|---|---|
| 1 | MCP `items` tool on `daas_module_access_keys` | Register key in the platform catalogue |
| 2 | MCP `policies` / Policy editor UI | Toggle key `true` on the relevant policy |
| 3 | React component | `usePermissions().hasModuleAccess('key')` |
| 4 | API route | Forward the user's token to `GET <Engine_URL>/api/permissions/me`; read `isAdmin` and `moduleAccess` |
| 5 | Workflow command JSON (optional) | Add `module_access_keys: ["key"]` |
| 6 | `LayoutShell.tsx` (optional) | Hide nav item unless key is granted |
<!-- /buildpad-backend -->

## Security Checklist

- [ ] Server-side check in every API route that performs a guarded action (UI checks are UX-only)
- [ ] Admin users (`admin_access: true`) bypass all module access checks — this is intended
- [ ] Key names follow the `<domain>:<capability>` convention and are globally unique
- [ ] Workflow commands use `module_access_keys` instead of bespoke policy IDs where possible

## Required Verification Tests (MANDATORY)

Run these checks whenever module keys are introduced or modified:

- [ ] Granted user can access the gated UI/action
- [ ] Ungranted user cannot see gated UI elements
- [ ] Ungranted user is blocked server-side (`403`) even if UI is bypassed
- [ ] Admin bypass behavior remains correct

If any test fails, treat the feature as incomplete.

## Additional Reference

- [Module access checklist](../../references/module-access-checklist.md)
