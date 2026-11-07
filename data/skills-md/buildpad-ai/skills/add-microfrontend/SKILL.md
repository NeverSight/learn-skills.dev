---
name: add-microfrontend
description: "Compose independent Next.js micro-apps into one Main App with sandboxed iframes and a postMessage bridge. Supabase projects only for now: not yet available on an Engine project. Covers the host component, the message contract, auth token bridging, URL and scope syncing, sandbox flags, and CSP. Load add-microapp first to decide domain boundaries and bootstrap the repos, then load this skill to wire the composition. Use when the user says add-microfrontend, micro-frontend, iframe composition, or needs to embed an independent app in another app."
argument-hint: "[microapp name] [host route, e.g. /admin/users]"
---

# Add Micro-Frontend (Iframe Composition)

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

<!-- buildpad-backend: engine -->
Sharing one session between a host and its frames is not available on an Engine project yet. Tell the developer so and stop.
<!-- /buildpad-backend -->
<!-- buildpad-backend: supabase -->
> **Composition mode.** For micro-apps that are Next.js apps built and deployed by this
> project, [add-microfrontend-zones](../add-microfrontend-zones/SKILL.md) (Multi-Zones,
> one origin, no iframe) is the default — field-tested 2–4× faster to first paint and
> without the auth bridge. Use this skill when a micro-app is not a Next.js app, is
> third-party or untrusted code, or must render inside a page of another app.

This skill owns the **composition mechanism**: the host component, the bridge
protocol, auth and URL and scope syncing, sandbox flags, and CSP.

[add-microapp](../add-microapp/SKILL.md) owns domain boundaries, collection ownership,
RBAC, and repo bootstrap. Load it first. Come back here to wire the apps together.

All apps share **one** DaaS backend and **one** Supabase project. Each micro-app is a
standalone Next.js app with its own SSR, routing, and deployment. The browser composes
them.

## When to use iframes

Use this skill when at least two of these are true:

- Separate teams own separate parts of the product.
- Parts must deploy on their own schedule.
- A part must not be able to read the host DOM, CSS, or memory.
- A part already exists as a deployed app.

Do not use this skill when:

- One team owns everything. Use routes in a single app.
- The parts share layout, modals, or a scroll container. See the limits in
  [url-and-history](references/url-and-history.instructions.md).
- You want code reuse. Iframes share nothing. Use a package.
- The section is a widget, not a page.

The cost is real. Iframe composition adds an auth bridge, a message contract, echo
suppression, history rules, dialog limits, and two CSP headers. Isolation is complete;
complexity is not low. `add-microapp` without iframes is often the better answer.

## Critical Rules

1. Micro-apps load in `<iframe>` elements. The Main App owns layout, navigation, and
   the frame `src`.
2. The Main App must not read the frame DOM. The micro-app must not read
   `window.parent` DOM. All communication uses `postMessage`.
3. Copy `assets/shared/bridge-protocol.ts` and `assets/shared/mfe-cookies.ts` to every
   app. Do not retype message shapes or cookie names.
4. Every message handler must check `event.origin`, then `event.source`, then the
   `source` and `v` envelope fields.
5. The iframe `src` must depend on the micro-app origin and the route path only. It
   must never depend on the host query string.
6. The Main App owns token refresh. `SET_AUTH` carries `access_token` and `expires_at`.
   It must never carry `refresh_token`. When the host session is inside the renewal
   window, the host must call `refreshSession()` before answering — `getSession()`
   alone returns the same token and the frame asks again forever.
7. Each micro-app stores its own access token in its own cookie, on its own origin,
   with `SameSite=None; Secure; Partitioned`. The bridge is required on Amplify, on a
   custom domain, and in local development.
8. A micro-app validates the bridge token with `supabase.auth.getUser(token)` on every
   request (via `getMfeUser` in `lib/bridge/mfe-middleware.ts`). Never trust a local
   decode: only `getUser` observes a sign-out that happened in the Main App.
9. **Never overwrite a CLI-owned file.** Any file carrying an `@buildpad-origin`
   header belongs to the Buildpad CLI. It is restored by `npx buildpad upgrade` **and
   by any `buildpad add <library>`** — both rewrite owned files with no prompt, which
   is why every module install happens in Step 4a, before any merge. One documented
   exception: `components/layout/navigation.ts` carries the header but its own docblock
   says to edit it freely.
   The bridge merges into these files with the pinned edits in
   [auth-bridge](references/auth-bridge.instructions.md); it never replaces them.
   See "CLI-owned files" below.
10. The host sign-out control must `await logoutAllMicroapps()` before it triggers
    `/api/auth/logout`. The host cannot delete a cookie on a micro-app origin.
11. `SET_AUTH` must carry `resource_uri` on any project that uses `manage-scope` or
    `add-multitenancy`. Without it every micro-app call resolves at root scope and
    returns 403. On a project that uses neither, no scope cookie exists and no
    `X-Resource-Uri` header is expected — do not fabricate one.
12. Two token paths exist, and a module uses one of them. The CLI's ~16 Next proxy
    routes read `lib/api/auth-headers.ts` — pinned edit H1 covers those. A module whose
    hooks import `lib/buildpad/services/api-request.ts` calls DaaS **directly** from the
    browser and never touches H1 — pinned edit W1 is the only thing that authenticates
    it. Run
    `grep -rl "services/api-request" components lib` and
    `grep -rn "fetch('/api/" components lib` in the installed module, then apply both
    edits. The Users module is direct-call: H1 can be perfect while every users, roles,
    policies, and permissions call fails.
13. The sandbox attribute must omit `allow-modals` and `allow-top-navigation`. It must
    include `allow-popups`, `allow-downloads`, and
    `allow-storage-access-by-user-activation`. `allow-popups` is load-bearing for the
    Files module download, not only for OAuth — see
    [security](references/security.instructions.md).
14. Micro-app pages must not call `window.confirm`, `window.alert`, or
    `window.prompt` — including calls shipped by the CLI (audit for them in Step 4).
    Use Mantine `Modal` or `modals.openConfirmModal`.
15. A framed micro-app renders **content only**. The host owns all chrome, so the
    frame must show no sidebar, no header, no login form, and no sign-out control —
    double chrome also lets the user navigate the frame away from the section the
    host thinks is open. Pinned edit E1 skips `AuthenticatedShell` when the request
    arrives inside a frame; opened directly, the micro-app keeps its full shell. E1
    must decide from the bridge cookie, not from `Sec-Fetch-Dest` alone: an RSC fetch
    and `router.refresh()` re-render the same layout on the server with
    `Sec-Fetch-Dest: empty`, and a header-only test then mounts a second full shell.
16. All apps must use the same `NEXT_PUBLIC_BUILDPAD_DAAS_URL`,
    `NEXT_PUBLIC_SUPABASE_URL`, and `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
17. `NEXT_PUBLIC_HOST_ORIGIN` / `HOST_ORIGIN` are **reserved by the CLI's
    `lib/origin.ts`** and mean *this app's own* public origin. Never set them to
    another app's URL. The Main App's origin travels in
    `NEXT_PUBLIC_MICROAPP_URL_MAIN`, which bootstrap already writes into every
    `.env.local`. Localhost overrides go in `.env.development.local`, never
    `.env.local` — `next build` loads `.env.local`, so a localhost value there is
    baked into the production CSP.
18. Verify field names with `mcp_daas_schema` or `mcp_daas_fields` before you write any
    `sort`, `fields`, or `filter` parameter. A wrong name returns a 500 that is hard to
    trace through the frame.

## CLI-owned files

A Buildpad starter is not an empty Next.js app. `npx @buildpad/cli bootstrap` installs
components, auth routes, and middleware, and marks each file with an
`@buildpad-origin` header. `npx buildpad upgrade` restores them — interactively it
prompts on local changes, but with `--yes` or `--strategy=overwrite` (what a
non-interactive agent uses) it **silently reverts them**.

Before Step 3, run the preflight in every app:

```bash
grep -rl "@buildpad-origin" --include="*.ts" --include="*.tsx" app components lib middleware.ts 2>/dev/null
```

Files this skill touches, and how:

| Path | Owner | Action |
| --- | --- | --- |
| `lib/supabase/middleware.ts` | CLI | **Merge** — pinned edits M1–M3 in [auth-bridge](references/auth-bridge.instructions.md) |
| `middleware.ts` (root) | CLI | **Do not touch** — it sets `Cache-Control: private, no-store`, the only cache header on ~20 session routes |
| `app/api/auth/logout/route.ts` | CLI | **Merge** — pinned edit L1 (expire the three bridge cookies with `framedCookieOptions(0, …)`, never `delete()`). It has a GET handler the shell navigates to; never drop it |
| `app/login/page.tsx` | CLI | **Merge** — pinned edit P1 (wrap the form in `LoginBridge`) |
| `components/DaaSProviderWrapper.tsx` | CLI | **Merge** — pinned edit W1 (`useMfeToken` as second token source **and** the readiness gate) |
| `components/ui/file-manager/*`, `components/ui/users-management/*`, module hooks | CLI | **Do not touch** — installed by `buildpad add files-routes` / `add users-routes`. Wrap them; never edit them. This is why `search` cannot be URL-synced (Step 4) |
| `components/layout/AuthenticatedShell.tsx` | CLI | **Merge** (host only) — pinned edit S1 (`await logoutAllMicroapps()`). Micro-apps leave it untouched: E1 keeps it out of the frame entirely |
| `app/(authenticated)/layout.tsx` | CLI | **Merge** (micro-app) — pinned edit E1 (skip the shell when framed; content only inside the frame) |
| `lib/api/auth-headers.ts` | CLI | **Merge** — pinned edit H1 (read `mfe_access_token` before the session) |
| everything under `lib/bridge/`, `components/Microapp*`, `components/LoginBridge.tsx`, `config/app-urls.ts`, `next.config.ts`, the three bridge auth routes | this skill | **New files** — copy from `assets/` |

On every merged file, add one line under the CLI header:
`// ⚠️ LOCAL MODIFICATION (add-microfrontend): re-apply pinned edits after buildpad upgrade`.

## Architecture

```
Main App (host)                      Micro-App A            Micro-App B
┌───────────────────────────┐        ┌────────────┐         ┌────────────┐
│ AppShell: nav + layout    │        │ own SSR    │         │ own SSR    │
│ ┌───────────────────────┐ │        │ own routes │         │ own routes │
│ │ MicroappIframe        │◀┼───────▶│ own cookie │         │ own cookie │
│ │  postMessage bridge   │ │        └─────┬──────┘         └─────┬──────┘
│ └───────────────────────┘ │              │                      │
│ owns: session, refresh,   │              │                      │
│ scope, theme, navigation  │              │                      │
└─────────────┬─────────────┘              │                      │
              └─────────────────┬──────────┴──────────────────────┘
                                ▼
                    ┌───────────────────────┐
                    │ one DaaS backend      │──▶ Supabase (Auth + DB)
                    └───────────────────────┘
```

## Workflow

### Step 0: Discover the project context (always first)

Call `get_project_detail` on the platform MCP server. Take every URL and credential
from the response. Never ask the user for them.

Tool naming in this repo: platform tools have no prefix (`get_project_detail`). DaaS
tools use the `mcp_daas_*` prefix (`mcp_daas_schema`, `mcp_daas_cors-settings`).

Read `project.mainAmplifyUrl` (host origin), `project.daasUrl`,
`project.supabaseUrl`, `project.supabaseAnonKey`, and `microapps[]` (each with `name`
and `amplifyUrl`). The response may carry more fields than the documented schema
(`workers`, `messaging`, …) — the schema lists what these skills consume, not
everything the platform returns. When you enumerate origins (CSP, CORS), enumerate
what is actually present.

Stop and report to the user if `daasUrl`, `supabaseUrl`, or `mainAmplifyUrl` is null.
Do not continue with a placeholder.

Full response schema:
[add-microapp context discovery](../add-microapp/references/context-discovery.instructions.md).

### Step 1: Write `config/app-urls.ts` in every app

This file is committed to git. Amplify builds it with no console configuration.
The local-dev override for the Main App origin is `NEXT_PUBLIC_MICROAPP_URL_MAIN` —
bootstrap already writes the deployed value into every `.env.local` (Rule 17; never
`NEXT_PUBLIC_HOST_ORIGIN`). Put localhost overrides in `.env.development.local`
only: `next build` loads `.env.local`, and a localhost value there ends up inside
the production CSP header.

Generation rules and the failure modes:
[add-microapp app-urls config](../add-microapp/references/app-urls-config.instructions.md).

### Step 2: Install the bridge contract

Copy to `lib/bridge/` in the Main App **and** in every micro-app, unchanged:

| Copy from | Copy to |
| --- | --- |
| `assets/shared/bridge-protocol.ts` | `lib/bridge/bridge-protocol.ts` |
| `assets/shared/mfe-cookies.ts` | `lib/bridge/mfe-cookies.ts` |

### Step 3: Wire the host

New files (no collisions):

| Copy from | Copy to |
| --- | --- |
| `assets/host/useMicroappHost.ts` | `lib/bridge/useMicroappHost.ts` |
| `assets/host/MicroappIframe.tsx` | `components/MicroappIframe.tsx` |

Set the Main App login route in `useMicroappHost.ts` at the line marked `AGENT`.
Change nothing else.

**Route mapping.** `microapps[]` carries a `name` and an `amplifyUrl` — **no route**.
Four strings that look alike are independent; write the table before writing pages:

| Platform `name` | `MICROAPP_URLS` key | Local directory | Host page file | `path` prop |
| --- | --- | --- | --- | --- |
| `users-management` | `'users-management'` | whatever the repo is called | `app/(authenticated)/users/page.tsx` | that micro-app's `DEFAULT_AUTHENTICATED_ROUTE` |

The `path` prop must be a route that **exists in that micro-app** — read its
`DEFAULT_AUTHENTICATED_ROUTE` from its `config/app-urls.ts`, or verify a page file
exists at the path you choose. A wrong `path` does not error: it bounces through the
login bridge and looks like it works while every deep link is broken.

**Host pages** live in the authenticated route group — in a Buildpad starter that is
`app/(authenticated)/`, whose layout mounts `DaaSProviderWrapper` and the app shell.
A page outside it renders with no auth context and no chrome. The embedding page must
wrap the frame in `Suspense`: `useMicroappHost` reads `useSearchParams()`, and a
statically prerendered page without a boundary fails `next build`.

```tsx
// app/(authenticated)/users/page.tsx
import { Suspense } from 'react';
import { Skeleton } from '@mantine/core';
import { MicroappIframe } from '@/components/MicroappIframe';
import { MICROAPP_URLS } from '@/config/app-urls';

export default function UsersSectionPage() {
  return (
    <Suspense fallback={<Skeleton height="100%" width="100%" />}>
      <MicroappIframe
        src={MICROAPP_URLS['users-management']}
        path="/users"
        title="Users Management"
        // Derive this list from what the framed page really syncs (Step 4), never
        // from a generic default. A name the micro-app never sends is dead weight;
        // a name the micro-app sends and this list omits is dropped silently.
        allowedParams={['user']}
        // Inside Mantine AppShell.Main, subtract the header AND the shell padding.
        height="calc(100vh - 60px - 2 * var(--mantine-spacing-lg))"
      />
    </Suspense>
  );
}
```

Navigation in a hand-written shell must be a client component
(`<NavLink component={Link} …>` inside `'use client'`). The starter's
`AuthenticatedShell` handles nav itself — add the section items to it instead.

**Sign-out (pinned edit S1).** The starter's shell signs out with
`window.location.href = '/api/auth/logout'` — a GET navigation, not a POST fetch.
There is nothing to intercept after it runs, so the broadcast must come first, awaited:

```tsx
// components/layout/AuthenticatedShell.tsx — the sign-out onClick (CLI-owned; merge)
onClick={async () => {
  const { logoutAllMicroapps } = await import('@/lib/bridge/useMicroappHost');
  await logoutAllMicroapps();               // broadcast LOGOUT + 300 ms drain
  window.location.href = '/api/auth/logout'; // the CLI GET route, unchanged
}}
```

Call `broadcastScope(uri)` after a tenant switch (scope projects only).

### Step 4: Wire each micro-app

#### 4a. Install the domain module FIRST (before any file below)

**Order is not optional.** `buildpad add <library>` rewrites files it owns without a
prompt and without `--overwrite`: an observed `buildpad add api-routes` reverted six
already-merged files (E1, L1, P1, W1, H1, and `api/auth/user`), and
`add users-routes` silently replaced a local page. Install every module you need
**before** applying any pinned edit, or the CLI destroys your merges.

A micro-app whose domain matches a Buildpad module must scaffold that module instead
of hand-writing a page:

| Domain | Skill | Command |
| --- | --- | --- |
| files | [add-files](../add-files/SKILL.md) | `npx @buildpad/cli@latest add files-routes` |
| users, roles, policies | [add-users](../add-users/SKILL.md) | `npx @buildpad/cli@latest add users-routes` |
| workflow definitions, assignments, instances | [add-workflows](../add-workflows/SKILL.md) | `npx @buildpad/cli@latest add workflows-routes` |
| cron jobs, run history | [add-cron](../add-cron/SKILL.md) | `npx @buildpad/cli@latest add cron-routes` |
| AI chat, assistant (Chocolate Factory agent) | [add-ai-chat](../add-ai-chat/SKILL.md) | `npx @buildpad/cli@latest add ai-chat-routes` |

A hand-written placeholder page is acceptable ONLY when no module covers the domain.

CLI 1.11.1 installs group-aware — it writes `app/(authenticated)/files/…` directly and
records those paths in `buildpad.json`. Verify where the routes landed; move them under
`app/(authenticated)/` only if the CLI did not, and never by hand-editing
`buildpad.json`. Run the module's own required proxy routes step only if those routes
are genuinely missing — bootstrap already installs a large `api-routes` set, and
re-running it is what reverts merges.

The cost of skipping the module is measured, not theoretical. A placeholder exercises
the bridge and nothing else. The module is what carries downloads, modals, permission
gates, and the CLI's own dialogs, and each behaves differently inside the frame: the
Files row-menu download runs through `window.open` to a signed cross-origin URL and
needs `allow-popups` as well as `allow-downloads`; a Mantine confirm dialog stops being
modal at the frame edge; the module mounts its data fetches before the bridge token
exists (W1b). Six field trials on placeholder pages passed every gate in this skill
while the real modules were broken.

#### 4b. New files (no collisions)

| Copy from | Copy to |
| --- | --- |
| `assets/microapp/MicroappBridgeProvider.tsx` | `components/MicroappBridgeProvider.tsx` |
| `assets/microapp/LoginBridge.tsx` | `components/LoginBridge.tsx` |
| `assets/microapp/useQueryParamSync.ts` | `hooks/useQueryParamSync.ts` |
| `assets/microapp/useMfeToken.ts` | `lib/bridge/useMfeToken.ts` |
| `assets/microapp/mfe-middleware.ts` | `lib/bridge/mfe-middleware.ts` |
| `assets/microapp/set-session.route.ts` | `app/api/auth/set-session/route.ts` |
| `assets/microapp/token.route.ts` | `app/api/auth/token/route.ts` |

#### 4c. Merges into CLI-owned files

Apply these only AFTER 4a. Exact hunks in
[auth-bridge](references/auth-bridge.instructions.md), "Pinned edits":

1. **M1–M3** `lib/supabase/middleware.ts` — accept the bridge token as a second
   session source and gate `/api/auth/token`. Do **not** replace the file: it owns the
   `publicOrigin()` redirect, the Supabase cookie refresh, and the route table.
2. **L1** `app/api/auth/logout/route.ts` — expire the three bridge cookies inside
   `performLogout()`, before `signOut()`, using `framedCookieOptions(0, …)` — a bare
   `delete()` emits an unpartitioned Lax expiry that the cross-site frame rejects.
   Keep the GET handler and the OAuth SLO.
3. **P1** `app/login/page.tsx` — wrap the CLI form in `LoginBridge` (with `Suspense`).
4. **W1** `components/DaaSProviderWrapper.tsx` — add `useMfeToken()` as the framed
   token source alongside the Supabase path, **and gate the children on its `ready`
   flag**. Both halves are required. Without the gate the module mounts and fires its
   first DaaS fetches with no `Authorization` header, gets 401, and never retries —
   Users shows "Not authenticated" forever and Files shows an empty file list over a
   backend that holds files.
5. **H1** `lib/api/auth-headers.ts` — read `mfe_access_token` first, fall back to the
   Supabase session (this single edit fixes all ~16 CLI proxy routes). H1 covers the
   Next proxy routes only. A direct-call module needs W1 (Rule 12).
6. **E1** `app/(authenticated)/layout.tsx` — render content only when framed
   (Rule 15's implementation path): skip `AuthenticatedShell`, keep
   `DaaSProviderWrapper`. Standalone keeps the full shell. Decide from the bridge
   cookie; `Sec-Fetch-Dest` alone fails on every RSC re-render. Without this, the frame
   shows a second sidebar, header, and profile menu inside the host's — and its nav
   lets the user move the frame to a different page than the host section.

#### 4d. Then wire

- Mount `MicroappBridgeProvider` in the micro-app **root** layout, inside
  `MantineProvider`. A page that is not wrapped never reports that it loaded, and the
  host shows its error state.
- Add `DEFAULT_AUTHENTICATED_ROUTE` to `config/app-urls.ts` — the micro-app's first
  real route.
- **Wire the URL sync.** From buildpad-ui's URL-state release
  ([PR #154](https://github.com/buildpad-ai/ui/pull/154)), the list managers
  persist search/filter/sort/page (and Files' `folder`) in the frame's URL by
  default via `history.replaceState`, and `MicroappBridgeProvider`'s
  `OutboundUrlMirror` posts those writes to the host automatically — **module
  search now syncs with zero per-module wiring**. Two obligations remain:

  1. Reconcile the host allowlist. `pickParams()` filters both directions, so
     every parameter the module writes must be named in the host page's
     `allowedParams` or it is dropped silently:
     `['search', 'role', 'status', 'sort', 'page', 'folder', 'user', 'file']`
     covers the stock modules plus the row-click sync below.
  2. Detail-record sync stays a wrapper concern: drive `user`/`file` from
     `onUserClick`/`onFileClick` in a **new local file** rendered by the CLI
     page (the CLI page itself is `@buildpad-origin` — a one-line merge).

  On module versions **before** the URL-state release, module search is
  unsyncable — those managers hold `search`/`page`/`sort` in private
  `useState` inside `@buildpad-origin` files with no controlled prop, and
  Rule 9 forbids editing them. Do not scrape the frame DOM to fake it; take
  the upstream update instead.
- **Audit for native dialogs**:
  `grep -rn 'window\.\(confirm\|alert\|prompt\)' app components lib --include='*.tsx'`.
  The CLI's `rich-text-markdown.tsx` ships a `window.prompt` that is silently dead in
  the frame — replace the call or avoid that interface on framed pages (Rule 14).

### Step 5: Create the CSP headers

**A Buildpad starter ships no `next.config.ts` — create it.** These are complete
files. Two traps: the snippet must be a whole module (not a bare `headers()` method),
and `@/…` aliases do not resolve from the Next config loader — the import must be
**relative**. Never bake `localhost` into a production header: gate local origins on
`NODE_ENV`.

```ts
// Main App: next.config.ts (new file)
import type { NextConfig } from 'next';
import { MICROAPP_URLS } from './config/app-urls';

const dev = process.env.NODE_ENV === 'development';
const microappOrigins = Object.values(MICROAPP_URLS).map((u) => new URL(u).origin);
const frameSrc = ["'self'", ...microappOrigins, ...(dev ? ['http://localhost:3001', 'http://localhost:3002'] : [])];

const nextConfig: NextConfig = {
  async headers() {
    return [{
      source: '/:path*',
      headers: [{
        key: 'Content-Security-Policy',
        // frame-ancestors 'none': the host holds the real Supabase session and
        // must not be framable by anyone. frame-src limits what IT may embed —
        // it does nothing to stop it being embedded.
        value: `frame-ancestors 'none'; frame-src ${frameSrc.join(' ')}`,
      }],
    }];
  },
};
export default nextConfig;
```

```ts
// Micro-app: next.config.ts (new file)
import type { NextConfig } from 'next';
import { HOST_ORIGIN } from './config/app-urls';

const dev = process.env.NODE_ENV === 'development';
const ancestors = ["'self'", HOST_ORIGIN, ...(dev ? ['http://localhost:3000'] : [])];

const nextConfig: NextConfig = {
  async headers() {
    return [{
      source: '/:path*',
      headers: [{ key: 'Content-Security-Policy', value: `frame-ancestors ${ancestors.join(' ')}` }],
    }];
  },
};
export default nextConfig;
```

Verify after `pnpm build`: the resolved origins — and no `http://localhost` — appear in
`jq '.headers' .next/routes-manifest.json`.

### Step 6: Configure CORS (runnable)

The DaaS default (`cors_origins: ["*"]`, `cors_allow_credentials: false`) blocks
**every** credentialed browser call: the Fetch spec discards a credentialed response
carrying `Access-Control-Allow-Origin: *`. Fix it with the DaaS MCP tool
`mcp_daas_cors-settings` (wired in `.mcp.json`; REST equivalent
`PATCH /api/settings/cors`):

```json
{
  "action": "update",
  "cors_origins": ["<mainAmplifyUrl>", "<each microapps[].amplifyUrl>", "http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
  "cors_allow_credentials": true,
  "cors_allowed_headers": ["Content-Type", "Authorization", "Origin", "X-Requested-With", "Accept", "X-Resource-Uri"],
  "cors_max_age": 0
}
```

Verify:

```bash
curl -si -X OPTIONS "<daasUrl>/api/items/anything" -H "Origin: <mainAmplifyUrl>" -H "Access-Control-Request-Method: GET" | grep -i access-control
```

The response must echo the origin (not `*`) and include
`access-control-allow-credentials: true`.

### Step 7: Add the tests

The starters ship no test tooling. Install it, then copy the three assets:

```bash
pnpm add -D @playwright/test
pnpm exec playwright install chromium
```

| Copy from | Copy to (host app) |
| --- | --- |
| `assets/tests/playwright.config.ts` | `playwright.config.ts` |
| `assets/tests/auth.setup.ts` | `tests/auth.setup.ts` |
| `assets/tests/iframe-composition.spec.ts` | `tests/iframe-composition.spec.ts` |

Fill every value in the spec's `AGENT` block and the config's `webServer` array (one
entry per app — this composition needs three servers). Add `playwright/.auth/` and
`test-results/` to `.gitignore`. Run with real credentials:

```bash
TEST_EMAIL=... TEST_PASSWORD=... pnpm exec playwright test
```

**Never add a host route to `publicRoutes` to make a test pass** — `auth.setup.ts` +
`storageState` is the correct fix for tests landing on `/login`.

### Step 8: Deploy (gated)

`pnpm build` must pass **in every app you touched** before any push — Amplify runs the
same build, and a failure surfaces minutes later in a file unrelated to your change.
Then push each micro-app first, then the Main App. No console environment variable
changes are needed: the URLs live in `config/app-urls.ts`.

After the first deploy, verify the handshake **on the deployed origins**, not on
localhost — two localhost ports are the same *site*, so partitioned-cookie failures
(Safari, Incognito) are invisible locally.

## File Structure

```
main-app/
├── app/(authenticated)/{route}/page.tsx   # one page per micro-app, Suspense-wrapped
├── components/MicroappIframe.tsx
├── components/layout/AuthenticatedShell.tsx  # CLI-owned — pinned edit S1
├── config/app-urls.ts                     # committed
├── lib/bridge/{bridge-protocol,mfe-cookies,useMicroappHost}.ts
├── next.config.ts                         # NEW: frame-ancestors 'none' + frame-src
├── playwright.config.ts                   # NEW
└── tests/{auth.setup,iframe-composition.spec}.ts

{microapp}/
├── app/login/page.tsx                     # CLI-owned — pinned edit P1 (LoginBridge)
├── app/api/auth/logout/route.ts           # CLI-owned — pinned edit L1
├── app/api/auth/{set-session,token}/route.ts  # NEW
├── components/{MicroappBridgeProvider,LoginBridge}.tsx  # NEW
├── app/(authenticated)/layout.tsx         # CLI-owned — pinned edit E1 (no shell in frame)
├── components/DaaSProviderWrapper.tsx     # CLI-owned — pinned edit W1
├── config/app-urls.ts                     # committed: HOST_ORIGIN + DEFAULT_AUTHENTICATED_ROUTE
├── hooks/useQueryParamSync.ts             # NEW — and WIRED on the default route
├── lib/api/auth-headers.ts                # CLI-owned — pinned edit H1
├── lib/bridge/{bridge-protocol,mfe-cookies,mfe-middleware,useMfeToken}.ts  # NEW
├── lib/supabase/middleware.ts             # CLI-owned — pinned edits M1–M3
├── middleware.ts                          # CLI-owned — untouched
└── next.config.ts                         # NEW: frame-ancestors
```

## Before You Call It Done

Each item names its procedure — a box without evidence is not ticked.

- [ ] Every micro-app whose domain matches a Buildpad module renders that module, not a
      hand-written placeholder (Step 4, first bullet). A placeholder proves the bridge
      and nothing about the module.
- [ ] The frame shows real data. Record every DaaS response inside the frame and assert
      that **none** is 401 or 403. An empty list is not proof of an empty backend: the
      Files module swallows a 401 and renders "Drag files here" while files exist.
- [ ] The parameter the framed page syncs appears in the host `allowedParams`, and
      driving it in the frame updates the host URL while the frame `src` is unchanged
      (spec: *in-frame state reaches the host URL*). When the installed module exposes
      no controllable state, the gap is recorded and this box is marked N/A.
- [ ] A signed-in user reaches a micro-app section with no login form and no extra
      click (spec: *auth bridge signs the frame in*).
- [ ] Inside the frame the micro-app shows **no** sidebar, header, or profile menu;
      opened directly on its own origin it still shows the full shell (E1). Check this
      after a **fresh** host page load and after a host tenant switch, not only after a
      client-side navigation — an RSC re-render is what defeats a header-only E1.
- [ ] Renewal works without waiting an hour: overwrite `mfe_expires_at` to now+70 s
      and observe a second `set-session` round trip (spec: *token renewal*).
- [ ] Sign-out: `mfe_access_token` is present on the frame origin **before** the
      click and absent after (spec: *logout clears the micro-app cookie*).
- [ ] Scope projects only (Rule 11): a frame's `/api/items/*` call carries
      `X-Resource-Uri`. On other projects this box does not apply.
- [ ] `jq '.headers' .next/routes-manifest.json` shows the CSP with real origins and
      no `http://localhost` in a production build, in every app.
- [ ] The Step 6 `curl` echoes the origin and `access-control-allow-credentials: true`.
- [ ] `pnpm build` is green in every touched app.
- [ ] The deployed handshake was verified on the real cross-site origins, including
      once in Safari or an Incognito window (partitioned cookies).

## References

- [Bridge protocol and sequences](references/bridge-protocol.instructions.md)
- [Auth bridge: pinned edits, refresh, scope, sign-out](references/auth-bridge.instructions.md)
- [URL, history, layout limits](references/url-and-history.instructions.md)
- [Sandbox, CSP, cookies, message validation](references/security.instructions.md)
- [Troubleshooting](references/troubleshooting.instructions.md)
- [add-microapp](../add-microapp/SKILL.md) — domain boundaries and repo bootstrap
- [daas-platform](../daas-platform/SKILL.md) — DaaSProvider and CORS rules
- [authentication-proxy](../authentication-proxy/SKILL.md) — direct calls and proxy routes
<!-- /buildpad-backend -->
