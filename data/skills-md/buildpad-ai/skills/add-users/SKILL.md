---
name: add-users
description: Scaffold the Buildpad Users module — ready-made /users, /roles, and /policies admin pages (UsersManager/UserDetail, RolesManager/RoleDetail, PoliciesManager/PolicyDetail) with search, filters, role assignment, API tokens, and a per-collection permissions matrix. Backed by the useUsers/useRoles/usePolicies hooks. Use when the user says add users, user management, user admin, roles page, policies page, permissions matrix, or wants an access-control admin surface.
argument-hint: "[--cwd path/to/project]"
---

# Add the Users Module

A ready-made access-control admin surface installed via the Buildpad CLI (Copy & Own — the code is copied into your project). It manages three interdependent domains — **users**, **roles**, and **policies** — on top of the access-control APIs of the project's data service (the DaaS application on a Supabase project, the Buildpad Engine on an Engine project), so you never hand-build user tables, role editors, or permission matrices.

Six screens ship together:

- **`UsersManager`** — the `/users` list: search, role/status filters, pagination, permission-gated create/edit/delete.
- **`UserDetail`** — the `/users/[id]` page: profile fields, password rules, role assignment, API token generation/management (on an Engine project a static token is an MCP credential only), and a Policies tab.
- **`RolesManager`** — the `/roles` list with member counts.
- **`RoleDetail`** — the `/roles/[id]` page: icon, parent role hierarchy, scope-assignment rules, plus Users and Policies tabs.
- **`PoliciesManager`** — the `/policies` list with user/role attachment counts.
- **`PolicyDetail`** — the `/policies/[id]` page: access flags (`app_access`, `admin_access`, `delegate_access`) and a per-collection permissions matrix with a custom-permission editor.

## CRITICAL: Never Create These Manually

Like all Buildpad UI, the Users module is CLI-installed and owned as source. Do **not** hand-write `components/ui/users-management/*` or the `useUsers`/`useRoles`/`usePolicies`/`useAccess` hooks in `lib/buildpad/hooks/` — scaffold them. For app-level role gating, do **not** invent role-name checks either — see [grant-module-access](../grant-module-access/SKILL.md).

## Prerequisites Check

```bash
node --version && pnpm --version && npx --version
```

Requires Node.js v24 LTS and pnpm v10+ (see [add-buildpad](../add-buildpad/SKILL.md) for install guidance). The module **must** render under the authenticated layout (`buildpad init` generates `app/(authenticated)/` with a `DaaSProviderWrapper`) so `DaaSProvider` header injection (the signed-in user's session token) is in scope — the hooks call your `app/api/users/*`, `app/api/roles/*`, `app/api/policies/*`, `app/api/permissions/*`, and `app/api/collections/*` proxy routes.

**On a Supabase project, DaaS CORS must be configured first.** The managers fetch authenticated DaaS endpoints from the browser with `credentials: 'include'`. DaaS's default `cors_origins: ["*"]` is **incompatible** with credentialed requests — the browser blocks every preflight. Set explicit origins before mounting the module (see [daas-platform](../daas-platform/SKILL.md) "CORS must use explicit origins"). This is not Users-specific: it affects every authenticated Buildpad component.

**On an Engine project there is nothing to configure.** On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere.

## Installation

The Users module is **opt-in** — it is not part of `bootstrap`.

```bash
# 1. Add the module (copies app/users/, app/roles/, app/policies/ shells and
#    components/ui/users-management/, plus the access-control hooks)
npx @buildpad/cli@latest add users-routes --cwd /path/to/project

# 2. Add the data-API proxy routes it needs (if not already present)
npx @buildpad/cli@latest add api-routes --cwd /path/to/project
```

> The docs use the shorthand `buildpad add users-routes` when the CLI is installed globally; `npx @buildpad/cli@latest add …` is the equivalent no-install form used across these skills.

> **If the CLI command fails, `@buildpad/cli` IS published to npm** — verify with `npm view @buildpad/cli version` before assuming otherwise. The CLI fetches its registry from `raw.githubusercontent.com`, so confirm the environment can reach **both** npm and the GitHub raw CDN.

## The Routes

```
app/users/
├── page.tsx          # /users          — UsersManager list
└── [id]/page.tsx     # /users/[id]     — UserDetail profile + tokens + policies

app/roles/
├── page.tsx          # /roles          — RolesManager list
└── [id]/page.tsx     # /roles/[id]     — RoleDetail hierarchy + members + policies

app/policies/
├── page.tsx          # /policies       — PoliciesManager list
└── [id]/page.tsx     # /policies/[id]  — PolicyDetail flags + permissions matrix
```

## Usage

### List view — `UsersManager`

```tsx
// app/users/page.tsx
"use client";

import { useRouter } from "next/navigation";
import { UsersManager } from "@/components/ui/users-management";

export default function UsersPage() {
  const router = useRouter();
  return (
    <UsersManager
      onUserClick={(user) => router.push(`/users/${user.id}`)}
      onCreateUser={() => router.push("/users/new")}
    />
  );
}
```

| Prop | Purpose |
| ----------------- | ------------------------------------------------------ |
| `onUserClick`     | Open a user (e.g. navigate to the detail page)         |
| `onCreateUser`    | Handle the permission-gated create action              |
| `pageSize` / `pageSizeOptions` | Pagination control                        |
| `hideHeader`      | Embed the list without its own header chrome           |
| `usersCollection` | DaaS collection used for RBAC checks                   |

### Detail view — `UserDetail`

```tsx
// app/users/[id]/page.tsx
"use client";

import { use } from "react";
import { useRouter } from "next/navigation";
import { UserDetail } from "@/components/ui/users-management";

export default function UserDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  return (
    <UserDetail
      id={id}
      onBack={() => router.push("/users")}
      onDeleted={() => router.push("/users")}
      onPolicyClick={(policy) => router.push(`/policies/${policy.id}`)}
    />
  );
}
```

The roles and policies pages follow the identical pattern: `RolesManager`/`RoleDetail` (`onRoleClick`, `onUserClick`, `onPolicyClick` cross-navigation) and `PoliciesManager`/`PolicyDetail`. Wire the `on*Click` callbacks so the three domains link to each other.

### Supporting components (reuse anywhere)

`SystemPermissions` (per-collection CRUD-S matrix), `PermissionDetailModal` (tabbed custom-permission editor), `TokenInput` (static token with client-side generation; on an Engine project a static token is an MCP credential only: the Engine accepts it on its MCP endpoint `/api/mcp`, never on the data API), `SelectIcon`/`IconDisplay`, and the shared list chrome (`SearchInput`, `ListFooter`, `ListEmptyState`, `RowActionsMenu`).

## The Data Layer (reuse anywhere)

All six screens are thin wrappers over hooks from `@/lib/buildpad/hooks`:

```tsx
import { useUsers, useRoles, usePolicies, useAccess } from "@/lib/buildpad/hooks";
```

- **`useUsers()`** → `fetchUsers`, `getUser`, `createUser`, `updateUser`, `deleteUser`, `bulkUpdateUsers`, `fetchUserPolicies`, `attachUserPolicy`, `detachUserPolicy` (+ `loading`, `error`)
- **`useRoles()`** → role CRUD plus policy attach/detach, mirroring `useUsers`
- **`usePolicies()`** → policy CRUD; list rows include `userCount`/`roleCount`
- **`useAccess()`** → raw access to the `daas_access` junction when you need custom attachment logic

On an Engine project an administrator creates every user who signs in with a password, through the Engine's user API (`POST /api/users` with an administrator's session) or the Studio's Users module, and gives the user a role in the project's tenant (`POST /api/users/:id/roles` with `role_id`, or the Users module). A user's first XAppHub sign-in creates that user's account, which holds no role until an administrator gives it one in the same way. An administrator resets a user's password, in the Studio's Users module. So on an Engine project `createUser` works only for an administrator, and every user it creates is given a role in the project's tenant when it is created: an account that holds no role there is refused at sign-in.

## Access-Control Semantics (IMPORTANT)

- **`admin_access` on users and roles is computed, never written.** To make someone an admin, attach a policy whose `admin_access` flag is true — do not try to set a field on the user.
- Permissions come from policies OR-merged across a user's direct policies and role policies. The `PolicyDetail` matrix is the source of truth per collection.
- For **application-level** capability gating (hiding buttons/pages by capability), use Module-Level Access Keys via [grant-module-access](../grant-module-access/SKILL.md) — never role-name checks. For **data-level** permission design, see [create-rbac](../create-rbac/SKILL.md) and [relational-permissions](../relational-permissions/SKILL.md).

## Post-Install Validation

```bash
npx @buildpad/cli@latest status --cwd /path/to/project
npx @buildpad/cli@latest validate --cwd /path/to/project
cd /path/to/project && pnpm build
```

## Related

- [add-buildpad](../add-buildpad/SKILL.md) — the underlying CLI and low-level field widgets.
- [create-rbac](../create-rbac/SKILL.md) — designing the roles/policies/permissions model this module administers.
- [grant-module-access](../grant-module-access/SKILL.md) — app-level capability flags checked with `hasModuleAccess`.
- [manage-scope](../manage-scope/SKILL.md) — the scope rules (levels of data separation inside the project) that `RoleDetail` scope assignment builds on.
- [buildpad-reference](../buildpad-reference/SKILL.md) — full component catalog.
