---
name: add-microfrontend-zones
description: "Set up a micro-frontend architecture with Next.js Multi-Zones (path-based composition on one origin). Supabase projects only for now: not yet available on an Engine project. Creates a Main App (default zone) that routes path prefixes to independent Next.js micro-apps through rewrites, with one shared Supabase session cookie, one shared DaaS backend, the CLI's AuthenticatedShell rendered by every zone, and no iframes. Use this skill whenever the user asks for micro-frontends, microfrontends, multi-zones, zones, path-based composition, or wants independent Next.js apps under one domain — even if the user says \"iframe\". Use the add-microfrontend (iframe) skill only when a micro-app is not a Next.js app, is third-party or untrusted code, or must render inside a page of another app."
argument-hint: "[microapp name] [path prefix, e.g. /iam]"
---

# Add Micro-Frontend (Multi-Zones Composition)

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
Set up a **path-based composition** with Next.js Multi-Zones. The **Main App** is the default zone. Each **micro-app** is a separate Next.js application that owns one path prefix — a **zone**. The Main App routes requests for the prefix to the micro-app with `rewrites`. The browser sees one origin. All apps share one Supabase Auth instance, one session cookie, and one DaaS backend. There are no iframes and no `postMessage` bridges.

This skill is the default for Next.js micro-apps. The [`add-microfrontend`](../add-microfrontend/SKILL.md) skill (iframe composition) is the fallback. Read the next section before you start.

**Field-tested.** On 2026-09-04 this skill was applied to three live Buildpad projects (`@buildpad/cli` 1.11.1, Next.js 16.3.3): a Main App plus the `users-management` and `files-management` micro-apps that had been composed with the iframe skill. All eleven acceptance checks in `assets/tests/zones.spec.ts` passed on local production builds and again on the deployed Amplify origin, in Chromium and WebKit. Cold time-to-shell on the Users module: 0.7 s zones vs 2.9 s iframe on the same machine, and **0.54 s vs 2.33 s on the deployed origins** (Files 0.50 s vs 2.78 s); the conversion deleted 3,266 lines of bridge code. Every rule marked *(trial)* below exists because the first draft got it wrong.

## Choose the composition mode

| Situation | Mode | Skill |
| --- | --- | --- |
| The micro-app is a Next.js app that this project builds and deploys | Zones (default) | this skill |
| The micro-app is not a Next.js app, or the host is not a Next.js app | Iframe | `add-microfrontend` |
| The micro-app is third-party or untrusted code | Iframe | `add-microfrontend` |
| A widget from one app must render inside a page of another app | Iframe | `add-microfrontend` |
| One team builds and deploys all pages together | No micro-frontend. Use one app with route groups. | none |

Zones and iframes differ in one property: isolation. An iframe isolates the DOM, the CSS, the JS, and the cookies of a micro-app. A zone shares the origin with all other zones. A security bug in one zone is a security bug for the full origin. If a micro-app needs isolation from the Main App, use the iframe skill.

## Critical Rules

1. **One public origin.** The browser loads all zones from the Main App origin (`MAIN_APP_URL`). Users never see a micro-app URL. This is what makes the session cookie shared without a token bridge.
2. **One path prefix per zone.** Each micro-app owns one prefix, set as `basePath`. Next.js then serves the pages, the `/_next` assets, and the `public` files of the zone under that prefix. The Main App must not have a page under a prefix that a zone owns. **Buildpad route modules nest under the prefix** *(trial)*: `add users-routes` installs `/users`, `/roles`, `/policies`, `/module-access-keys` as sibling top-level routes; in a zone with `basePath: '/iam'` they are served at `/iam/users`, `/iam/roles`, … That is the URL scheme of a zone composition. Tell the user, and take the prefix from the user (short and meaningful: `/iam`, `/storage`, `/billing`).
3. **Route with rewrites in the Main App.** For each zone, the Main App adds two rewrite rules: `{{prefix}}` and `{{prefix}}/:path+`. The destination is the deployed URL of the zone plus the same path. No asset rewrite is necessary, because `basePath` puts the assets under the prefix. **Rewrites run after the Main App middleware** *(trial)*, so the Main App's session check sees every zone request — pages, RSC fetches and chunks alike. Rule 9 handles the chunks.
4. **Cross-zone links are `<a>` elements. In-zone links are `<Link>`.** `<Link>` prefetches and soft-navigates; across zones that pulls another app's RSC tree into this one. Use `ZoneLink` from `assets/shared/`; it selects the correct element from the public path.
5. **One session cookie, validated in every app.** Every app's middleware reads the shared Supabase cookie and validates it. No app has a `set-session` route, a token bridge, `MICROAPP_NEEDS_AUTH`, or `SET_AUTH`. Do not create them.
6. **Login and logout live in the Main App only.** A zone redirects an unauthenticated request to `${MAIN_APP_URL}/login?next=<public path>`. The shell's logout control calls `/api/auth/logout` on the public origin — which is the Main App's route from every zone — and the browser lands on `/login`. One `signOut()` ends the session for all zones, because all zones read the same cookie.
7. **Every app renders the same shell.** There is no live host page. Each app renders the CLI's `AuthenticatedShell` with pinned edit Z1 and an **identical `components/layout/navigation.ts`** of public paths — one entry per page, generated from each zone's installed modules *(trial)*, not one entry per zone. Regenerate the file in every app together.
8. **Never overwrite a CLI-owned file** *(trial)*. A `@buildpad/cli` app already ships `middleware.ts`, `lib/supabase/middleware.ts`, `AuthenticatedShell.tsx`, `navigation.ts`, `app/login/page.tsx` and `DaaSProviderWrapper.tsx`, each with an `@buildpad-origin` header. The zone composition merges into them with the six pinned edits in [pinned-edits](references/pinned-edits.instructions.md) and never replaces them. The greenfield files in Steps 4–6 are for apps that were not generated by the CLI. The one sanctioned free edit is `navigation.ts` (its own docblock says so).
9. **Exclude every zone's `_next/static` from the Main App middleware** *(trial)*. The stock matcher excludes only `/_next/static`; a zone's chunks live at `{{prefix}}/_next/static/…` and match it. Left alone, every zone chunk costs a Supabase round-trip and — because the CLI middleware stamps `Cache-Control: private, no-store` on everything it handles — can never be cached by the browser. Pinned edit Z-M2.
10. **Bare `/api/*` calls in a zone are answered by the Main App** *(trial)*. The browser resolves `fetch('/api/auth/user')` on the public origin, so the Main App's route answers. That is correct for the CLI's shared routes (auth, collections, items — the CLI generates the same ones in every app). A route that exists only in a zone must be called as `{{prefix}}/api/…`. A zone opened on its own domain 404s on bare calls; zone domains are not user-facing (Rule 1).
11. **Server Actions need `allowedOrigins`.** Behind the rewrite the request `Host` header is the zone domain and the `Origin` header is the public domain. Set `experimental.serverActions.allowedOrigins` to the public host in every app.
12. **Keep the CLI's `getUser()`** *(trial)*. `getClaims()` verifies locally only when the Supabase project signs with an asymmetric key; with the legacy HS256 secret it calls the Auth server exactly like `getUser()`. Check the token header (`alg`) before promising a saving, and treat key rotation as an optimisation, not a prerequisite. Every zone page load makes two sequential auth round-trips (Main App middleware, then zone middleware); measured at 90–450 ms each.
13. **Single shared DaaS backend and Supabase project.** All apps use the same `NEXT_PUBLIC_BUILDPAD_DAAS_URL`, `NEXT_PUBLIC_SUPABASE_URL`, and `NEXT_PUBLIC_SUPABASE_ANON_KEY`. Each app calls the DaaS backend directly with `Authorization: Bearer <supabase-jwt>`. Set `CORS_ORIGINS` in the DaaS `.env` to the public origin and the local dev origin only — zone domains are not browser origins.
14. **No iframes, no `postMessage`, no URL sync code.** The URL bar shows the real URL of the zone page. The browser history is the real history. Detail pages are routes again (`router.push('/users/<id>')`).
15. **`NEXT_PUBLIC_HOST_ORIGIN` means the public origin in every app** *(trial)*. The CLI's `lib/origin.ts` reads that name as "this app's own public origin"; under zones a zone's public origin *is* the Main App origin, so the two meanings coincide and the CLI's own redirect helpers (login bounce, logout, OAuth) point at the right place. Set it to `{{project.mainAmplifyUrl}}` in every zone's Amplify environment (Step 7); without it a zone behind the rewrite falls back to `x-forwarded-host`, which names the zone's own Amplify domain.
16. **Strip `basePath` before `router.replace`** *(trial)*. Buildpad's list managers persist search/sort/page through `useUrlListParams`, which hands the app-registered writer the browser path — `basePath` included — and `router.replace()` prepends `basePath` again. Pinned edit Z-W1; without it every search lands on `/iam/iam/users`.
17. **Group pages by navigation.** Navigation inside a zone is a soft navigation. Navigation between zones is a full page load (0.6 s to shell in the trial, plus one network hop deployed). Put pages that users visit together in the same zone.
18. **Independent deployments.** Each app has its own git repository and its own Amplify app. The Main App holds only the zone URLs and prefixes in `config/zones.json`. It never bundles micro-app code.
19. **No function props from Server Components (React 19 / Next.js 16).** Use plain `<Link href="...">` in Server Components. The `component={...}` pattern is safe only inside `'use client'` components.
20. **Verify field names against the DaaS schema.** All apps share one DaaS backend. Check field names with `mcp_daas_schema` or `mcp_daas_fields` before you write `sort`, `fields`, or `filter` parameters.

## Architecture

```
Browser sees ONE origin: https://main.d1234abcde.amplifyapp.com (or the custom domain)

┌───────────────────────────────────────────────────────────────────────┐
│  Main App (default zone)                     next.config.ts rewrites  │
│  /                    → own pages                                     │
│  /login, /api/auth/*  → own routes (the only login/logout)            │
│  /iam/*               → https://main.d5678fghij.amplifyapp.com/iam/*  │
│  /storage/*           → https://main.d9012klmno.amplifyapp.com/storage/* │
└──────────────────┬──────────────────────────────┬─────────────────────┘
                   ▼                              ▼
┌─────────────────────────────┐    ┌─────────────────────────────┐
│  users-management (zone)    │    │  files-management (zone)    │
│  basePath: /iam             │    │  basePath: /storage         │
│  /iam/users /iam/roles …    │    │  /storage/files             │
│  own SSR, middleware, shell │    │  own SSR, middleware, shell │
└──────────────┬──────────────┘    └──────────────┬──────────────┘
               └──────────────────┬───────────────┘
                                  ▼
                       ┌──────────────────┐
                       │  Single DaaS     │
                       │  Backend         │
                       └────────┬─────────┘
                                ▼
                       ┌──────────────────┐
                       │  Supabase        │
                       │  (Auth + DB)     │
                       └──────────────────┘
```

**Request flow for `GET /iam/users?search=john`:**

```
Browser → Main App origin
        → Main App middleware validates the session (redirects to /login?next=/iam/users if none)
        → Main App rewrite matches /iam/:path+
        → Main App proxies the request to the users-management URL (cookies included)
        → zone middleware validates the session again
        → zone SSR renders the page inside the shell
        → the response returns through the Main App to the browser
Browser → /iam/_next/static/...  (same route; skipped by the Main App middleware, cached immutable)
```

Compare with the iframe skill: one document, one React runtime, one SSR pass, and no auth handshake.

## CLI-owned files

Every file below carries an `@buildpad-origin` header. Rule 8 applies: merge with the pinned edit named here, never replace. The exact diffs are in [pinned-edits](references/pinned-edits.instructions.md).

| File | Main App | Zone |
| --- | --- | --- |
| `components/layout/AuthenticatedShell.tsx` | Z1 | Z1 (byte-identical) |
| `components/layout/navigation.ts` | replace content, keep header (Rule 7) | same content as the Main App |
| `lib/supabase/middleware.ts` | Z-M1h | Z-M1 |
| `middleware.ts` | Z-M2 | unchanged (its matcher is basePath-aware) |
| `app/login/page.tsx` | Z-P1 | unchanged; unreachable through the Main App, harmless |
| `components/DaaSProviderWrapper.tsx` | Z-W1 only if it hosts list managers | Z-W1 |
| `app/(authenticated)/layout.tsx`, `app/layout.tsx`, `app/api/auth/*`, `lib/api/auth-headers.ts`, module pages | stock | stock |

Skill-owned files (copy from `assets/`, never CLI-owned): `config/zones.json`, `config/app-urls.ts`, `lib/shell/ZoneLink.tsx`, `lib/shell/usePublicPathname.ts`, `next.config.ts`, the tests.

## Implementation Steps

### Step 0: Discover Project Context (MANDATORY — ALWAYS FIRST)

Call the `get_project_detail` platform MCP tool before any code or configuration. **Never ask the user for URLs or credentials. They are all in the context.**

```
{ "name": "get_project_detail", "arguments": {} }
```

Use these values:

- `project.mainAmplifyUrl` — the public origin (`MAIN_APP_URL`), until a custom domain exists
- `project.supabaseUrl`, `project.supabaseAnonKey`, `project.supabaseServiceRoleKey` — shared auth credentials
- `project.daasUrl` — shared DaaS backend URL
- `project.mainGitUrl`, `project.mainGitToken` — git credentials
- `project.daasAdminEmail`, `project.daasAdminPassword` — the account the Playwright suites sign in with (Step 9); pass them as `TEST_EMAIL` / `TEST_PASSWORD`, never print them
- `microapps[]` — existing micro-apps with `name`, `gitUrl`, `amplifyUrl`

**Choose the path prefix for each micro-app:**

1. If the user gave a prefix argument, use it.
2. Otherwise propose one short segment that names the domain (`users-management` → `/iam`, `files-management` → `/storage`, `billing-app` → `/billing`) and confirm it with the user. Module routes nest under it (Rule 2), so `/admin/users-management` would produce `/admin/users-management/users`; do not derive prefixes mechanically from the app name.
3. No two zones share a prefix, and no prefix is a parent of another prefix. The Main App must not have a page under any prefix.

**Validation:** If `daasUrl`, `supabaseUrl`, or `mainAmplifyUrl` is null, report it to the user with a remediation step. Do not continue with placeholder values.

See the [context discovery reference](../add-microapp/references/context-discovery.instructions.md) for the full response schema.

### Step 1: Generate `config/zones.json` and `config/app-urls.ts` (every app)

Copy `assets/shared/zones.json` into the Main App and into every zone and fill it. Only `ownPrefix` differs.

```json
{
  "mainAppUrl": "{{project.mainAmplifyUrl}}",
  "ownPrefix": "",
  "zones": [
    { "name": "{{microapp.name}}", "label": "{{Label}}", "prefix": "{{prefix}}", "url": "{{microapp.amplifyUrl}}" }
  ]
}
```

- Main App: `"ownPrefix": ""`. Zone: `"ownPrefix"` is the prefix of that zone, equal to `basePath`.
- `zones[]` lists every micro-app in the project, in every app.
- `url` is the deployed Amplify URL from `microapps[].amplifyUrl`. Never write `localhost` or a placeholder into this file.

Copy `assets/shared/app-urls.ts` to `config/app-urls.ts` unchanged. It exports `MAIN_APP_URL` (env override `NEXT_PUBLIC_HOST_ORIGIN`, then `zones.mainAppUrl`), `OWN_PREFIX`, `ZONES`, `LOGIN_PATH`, and `zoneFor(publicPath)`.

### Step 2: Configure the micro-app as a zone

Copy `assets/zone/next.config.ts` to the zone. It reads `zones.json`:

```ts
const nextConfig: NextConfig = {
  basePath: zones.ownPrefix,
  experimental: { serverActions: { allowedOrigins: [publicHost] } },
};
```

If the zone was composed with the iframe skill before, this **replaces** the iframe `next.config.ts` (its `frame-ancestors` CSP header goes with it).

Rules for `basePath`:

- Page files stay where the CLI put them. `app/(authenticated)/users/page.tsx` serves `{{prefix}}/users`.
- In-zone `<Link href>` and `router.push()` values are written without the prefix. Next.js adds `basePath`.
- `fetch('/api/...')` and `<a href>` values are resolved by the browser on the public origin (Rule 10).
- A file at `public/logo.png` is served at `{{prefix}}/logo.png`.
- If one zone must own paths that do not share one prefix, use `assetPrefix` instead of `basePath` and add a rewrite for `{{assetPrefix}}/:path+` in the Main App. This is rare. Prefer one prefix per zone.

### Step 3: Add the rewrites in the Main App

Copy `assets/host/next.config.ts` to the Main App. It generates the rules from `zones.json`, with a per-zone local override (`NEXT_PUBLIC_USERS_MANAGEMENT_URL` for a zone named `users-management`):

```ts
async rewrites() {
  return zones.zones.flatMap((zone) => {
    const origin = zoneUrl(zone);
    return [
      { source: zone.prefix, destination: `${origin}${zone.prefix}` },
      { source: `${zone.prefix}/:path+`, destination: `${origin}${zone.prefix}/:path+` },
    ];
  });
}
```

Notes:

- The Main App has no `basePath`. It is the default zone. If it hosted the iframe composition before, delete the iframe host pages under the prefixes first — a page shadows an `afterFiles` rewrite.
- Query strings pass through a rewrite unchanged.
- The rewrite carries the request cookies to the zone, and the `Set-Cookie` headers back to the browser. This is how a token refresh in a zone updates the shared cookie.
- Some hosting platforms change headers during a rewrite. Then the zone returns 400 or 503. In that case, move the routing to the middleware with `NextResponse.rewrite(new URL(...))`. The result is the same; `next.config.ts` rewrites are the first choice because they have lower latency.

### Step 4: Validate the session in every app

**CLI app (the normal case):** the app already has `middleware.ts` + `lib/supabase/middleware.ts` with the Supabase cookie refresh and `getUser()`. Apply the pinned edits:

- Zone: **Z-M1** — the unauthenticated redirect goes to `${MAIN_APP_URL}/login` with `next=${basePath}${pathname}${search}`.
- Main App: **Z-M1h** — the redirect carries `next=${pathname}${search}`; **Z-M2** — the matcher also excludes `.*/_next/static` and `.*/_next/image`.

Next.js 16 prints `The "middleware" file convention is deprecated. Please use "proxy" instead` for every CLI app. Leave it: `middleware.ts` is CLI-owned, and the codemod is the CLI's to run.

**Greenfield app (no `@buildpad-origin` files):** create `proxy.ts` (Next.js 16) with this shape. The matcher already contains the Rule 9 exclusions.

```ts
// proxy.ts (Main App and every zone)
import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';
import { LOGIN_PATH, MAIN_APP_URL } from '@/config/app-urls';

const PUBLIC_ROUTES = ['/login', '/api/auth', '/api/health'];
const isPublic = (p: string) => PUBLIC_ROUTES.some((r) => p === r || p.startsWith(`${r}/`));

export async function proxy(request: NextRequest) {
  let response = NextResponse.next({ request });
  const { pathname, search, basePath } = request.nextUrl; // pathname never contains basePath
  if (isPublic(pathname)) return response;

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value));
          response = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) => response.cookies.set(name, value, options));
        },
      },
    },
  );

  // getUser() validates against the Auth server. getClaims() is a local check
  // only with an asymmetric signing key (Rule 12). Never getSession() here.
  const { data, error } = await supabase.auth.getUser();
  if (error || !data?.user) {
    // The PUBLIC origin, never request.url: behind the rewrite that is the zone's own domain.
    const loginUrl = new URL(LOGIN_PATH, MAIN_APP_URL);
    loginUrl.searchParams.set('next', `${basePath}${pathname}${search}`);
    return NextResponse.redirect(loginUrl);
  }
  response.headers.set('Cache-Control', 'private, no-store, must-revalidate');
  return response;
}

export const config = {
  // The Main App's own assets AND every zone's assets under its prefix (Rule 9).
  matcher: ['/((?!_next/static|_next/image|favicon.ico|.*/_next/static|.*/_next/image).*)'],
};
```

Sign-out behaviour: `signOut()` in the Main App revokes the refresh token and clears the cookie on the shared origin. A zone request after that has no cookie and redirects to login. An access token that was already issued stays valid until it expires; keep the expiry short.

### Step 5: Login and logout in the Main App

The Main App keeps its CLI `/login` page and `/api/auth/*` routes. One pinned edit: **Z-P1** — after a successful sign-in, replace `router.push('/'); router.refresh()` with a hard navigation to the guarded `next` parameter:

```ts
const next = safeRelativePath(new URLSearchParams(window.location.search).get('next'), '/');
window.location.assign(next);
```

`safeRelativePath` is the CLI's own helper in `lib/origin.ts`; it rejects `//evil.example` and absolute URLs. The navigation must be hard: the target may live in another zone.

Logout needs no edit. The CLI shell's control does `window.location.href = "/api/auth/logout"`, which resolves on the public origin in every zone and lands on `/login`. Zones keep their own CLI `/api/auth/*` routes; through the Main App they are unreachable (the Main App's routes answer first), which is the intended state.

### Step 6: One shell in every app

Copy `assets/shared/ZoneLink.tsx` and `assets/shared/usePublicPathname.ts` to `lib/shell/` in the Main App and in every zone.

```tsx
// ZoneLink: give it a PUBLIC path, always with the zone prefix.
// Same zone  → <Link> without the prefix (Next.js adds basePath). Soft navigation.
// Other zone → <a> with the full path. Full page load.
```

**CLI app:** apply pinned edit **Z1** to `AuthenticatedShell.tsx` (imports `ZoneLink` and `usePublicPathname`; the nav loop renders `<ZoneLink>`; the active-state comparison uses the public pathname). Then write `components/layout/navigation.ts` from `assets/shared/navigation.ts`, identical in every app: one entry per page, public hrefs, the zone's module `navItems` with the prefix prepended, `Home` pointing at `/`. Keep the CLI header and the `buildpad:nav-insert` marker.

**Greenfield app:** render this layout in every app instead:

```tsx
// lib/shell/AppShellLayout.tsx
'use client';
import { AppShell, Button, Group, NavLink, Title } from '@mantine/core';
import { ZoneLink } from './ZoneLink';
import { usePublicPathname } from './usePublicPathname';

// AGENT: one entry per page, public paths, identical in every app.
const NAV_ITEMS = [{ label: 'Dashboard', href: '/dashboard' }, { label: 'Users', href: '/iam/users' }];

async function logout() {
  await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' });
  window.location.assign('/login'); // hard: the login page is in the Main App zone
}

export function AppShellLayout({ children }: { children: React.ReactNode }) {
  const current = usePublicPathname();
  return (
    <AppShell header={{ height: 60 }} navbar={{ width: 250, breakpoint: 'sm' }} padding="md">
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Title order={3}>My App</Title>
          <Button size="xs" variant="light" onClick={logout} data-testid="logout-button">Log out</Button>
        </Group>
      </AppShell.Header>
      <AppShell.Navbar p="md">
        {NAV_ITEMS.map((item) => (
          <NavLink key={item.href} label={item.label}
            active={current === item.href || current.startsWith(`${item.href}/`)}
            renderRoot={(props) => <ZoneLink href={item.href} {...props} />} />
        ))}
      </AppShell.Navbar>
      <AppShell.Main>{children}</AppShell.Main>
    </AppShell>
  );
}
```

When the shell design changes, regenerate it in every app. Write this rule in the project README. **Shared package option:** publish `lib/shell/` plus the shell as a private npm package once the copies start to drift; the generated module needs no infrastructure, so start with it.

### Step 6b: URL state under `basePath`

Apply pinned edit **Z-W1** to every zone's `DaaSProviderWrapper.tsx` (Rule 16). The Main App needs it only if it hosts list managers itself. Verify with the "query params stay in the real URL" check in Step 9: the address bar must read `{{prefix}}/users?search=…` with the prefix exactly once.

### Step 7: Environment files

Every app has the same infrastructure secrets. All values come from `get_project_detail`.

```
# .env.local (Main App and every zone) — also set in the Amplify console
NEXT_PUBLIC_SUPABASE_URL={{project.supabaseUrl}}
NEXT_PUBLIC_SUPABASE_ANON_KEY={{project.supabaseAnonKey}}
NEXT_PUBLIC_BUILDPAD_DAAS_URL={{project.daasUrl}}

# Main App only
SUPABASE_SERVICE_ROLE_KEY={{project.supabaseServiceRoleKey}}

# Every ZONE, in Amplify (Rule 15): the public origin, so the CLI's own redirects
# never fall back to the zone's Amplify domain.
NEXT_PUBLIC_HOST_ORIGIN={{project.mainAmplifyUrl}}
```

```
# .env.development.local (every app) — loaded by `next dev` only, never by `next build`
NEXT_PUBLIC_HOST_ORIGIN=http://localhost:3000
# Main App only: where the local zones run
NEXT_PUBLIC_USERS_MANAGEMENT_URL=http://localhost:3002
NEXT_PUBLIC_FILES_MANAGEMENT_URL=http://localhost:3001
```

If the apps came from the iframe skill, remove `NEXT_PUBLIC_MICROAPP_URL_MAIN` from the zones' `.env.development.local` — with both names present the CLI's `lib/origin.ts` would still see the right value, but the iframe branch of the same repo needs the old name and the two are easy to confuse.

DaaS `.env`:

```
CORS_ORIGINS={{project.mainAmplifyUrl}},http://localhost:3000
```

Only the public origin makes browser requests. Zone URLs are not browser origins.

### Step 8: Local development

Run every app on its own port. The Main App rewrites to the local zones.

| App | Port | Command | Test URL |
| --- | --- | --- | --- |
| Main App | 3000 | `npx next dev -p 3000` | `http://localhost:3000/iam/users` (through the rewrite) |
| users-management | 3002 | `npx next dev -p 3002` | `http://localhost:3002/iam/users` (direct) |
| files-management | 3001 | `npx next dev -p 3001` | `http://localhost:3001/storage/files` (direct) |

1. Set the `.env.development.local` values from Step 7.
2. Log in at `http://localhost:3000/login`.
3. Open `http://localhost:3000/iam/users`. The zone page must render inside the shell with no second login.

A direct zone URL has no session cookie and redirects to `http://localhost:3000/login?next=…`. That is correct behaviour. Direct zone URLs also 404 on bare `/api/*` calls (Rule 10); test through the Main App.

For production-like measurements build and start all three (`NEXT_PUBLIC_HOST_ORIGIN` and the zone URL overrides must be present **at build time** — `next build` does not read `.env.development.local`):

```bash
NEXT_PUBLIC_HOST_ORIGIN=http://localhost:3000 npx next build && npx next start -p 3002   # each zone
NEXT_PUBLIC_HOST_ORIGIN=http://localhost:3000 NEXT_PUBLIC_USERS_MANAGEMENT_URL=http://localhost:3002 \
  NEXT_PUBLIC_FILES_MANAGEMENT_URL=http://localhost:3001 npx next build && npx next start -p 3000   # Main App
```

### Step 9: Playwright tests (Main App)

Copy `assets/tests/playwright.zones.config.ts` to the Main App root and `assets/tests/auth.setup.ts` + `assets/tests/zones.spec.ts` to `tests/microfrontend/`. Fill the `AGENT` block at the top of the spec (two zones, their pages, the modules' test ids, the sidebar labels). Run:

```bash
pnpm add -D @playwright/test && pnpm exec playwright install chromium
TEST_EMAIL=… TEST_PASSWORD=… ZONES_BASE=http://localhost:3000 npx playwright test -c playwright.zones.config.ts
```

The suite proves, in order: no iframe; assets under the prefix and none from the Main App bundle; zone chunks cacheable through the Main App (Z-M2); identical shell with a full load across zones and a soft navigation inside one; one session for every zone; query params in the real URL, once-prefixed (Z-W1); detail views as real routes with working Back; an unauthenticated deep link bouncing to the Main App login with `next=`; the bounce landing in the other zone after sign-in (Z-M1h, Z-P1); logout from a zone ending the session everywhere.

Two gotchas the first draft of this suite had: `browser.newContext()` in `@playwright/test` inherits the project's `storageState`, so an "unauthenticated" context must pass `storageState: { cookies: [], origins: [] }` explicitly; and a module's table may carry no test id at runtime — wait for a rendered row (the trial used the Users module's `user-avatar` cell).

### Step 10: Build gate

`npx next build` must pass in every app before anything is pushed. Delete a stale `.next/` first if `tsc` complains about `.next/types/validator.ts` referencing routes that no longer exist (the iframe `set-session`/`token` routes leave one behind).

## File Structure (Main App)

```
my-app/                                    # Main App = default zone
├── app/
│   ├── (authenticated)/                   # CLI route group, own pages only
│   │   ├── layout.tsx                     # stock: DaaSProviderWrapper + AuthenticatedShell
│   │   └── page.tsx
│   ├── login/page.tsx                     # CLI page + pinned edit Z-P1
│   └── api/auth/...                       # the only login/logout in the project
├── components/
│   ├── DaaSProviderWrapper.tsx            # stock (Z-W1 only with own list managers)
│   └── layout/
│       ├── AuthenticatedShell.tsx         # CLI shell + pinned edit Z1
│       └── navigation.ts                  # identical in every app (assets/shared/navigation.ts)
├── config/
│   ├── zones.json                         # ownPrefix = ""
│   └── app-urls.ts                        # identical in every app
├── lib/
│   ├── shell/ZoneLink.tsx                 # identical in every app
│   ├── shell/usePublicPathname.ts
│   └── supabase/middleware.ts             # CLI + pinned edit Z-M1h
├── middleware.ts                          # CLI + pinned edit Z-M2
├── next.config.ts                         # assets/host/next.config.ts
├── playwright.zones.config.ts
└── tests/microfrontend/{auth.setup.ts,zones.spec.ts}
```

## File Structure (Zone)

```
users-management/                          # Zone: basePath /iam
├── app/
│   ├── (authenticated)/
│   │   ├── layout.tsx                     # stock
│   │   ├── users/page.tsx                 # CLI module page, serves /iam/users
│   │   ├── users/[id]/page.tsx            # serves /iam/users/:id
│   │   └── roles/, policies/, module-access-keys/
│   ├── login/page.tsx                     # stock CLI page; unreachable through the Main App
│   └── api/...                            # stock CLI routes; bare calls hit the Main App's (Rule 10)
├── components/
│   ├── DaaSProviderWrapper.tsx            # CLI + pinned edit Z-W1
│   └── layout/{AuthenticatedShell.tsx, navigation.ts}   # Z1; same nav as the Main App
├── config/{zones.json, app-urls.ts}       # ownPrefix = "/iam"
├── lib/shell/{ZoneLink.tsx, usePublicPathname.ts}
├── lib/supabase/middleware.ts             # CLI + pinned edit Z-M1
├── middleware.ts                          # stock
└── next.config.ts                         # assets/zone/next.config.ts
```

A zone has no `set-session` route, no `MicroappBridgeProvider`, no `LoginBridge`, no `useQueryParamSync`, and no `*-section.tsx` wrappers.

## Deployment

### Deploy a zone

Push to git. Amplify builds on push to `main`. Use the same `amplify.yml` as the iframe skill. Set `NEXT_PUBLIC_HOST_ORIGIN` in the zone's Amplify environment (Step 7).

### Update the Main App after a new zone

1. Add the zone to `config/zones.json` in the Main App.
2. Add the same entry to `config/zones.json` and the zone's pages to `navigation.ts` in every other app. The nav must show the new zone everywhere.
3. Push each app. The Main App build reads `zones.json` and generates the rewrites.

**Agent rule:** Amplify deployments take 2-5 minutes. No Amplify console change is necessary for a new zone beyond its own `NEXT_PUBLIC_HOST_ORIGIN`. The zone URLs are in `zones.json`.

### Production origin

**Option A — Amplify custom domain on the Main App (default).** Attach the custom domain to the Main App in the Amplify console. Set `mainAppUrl` in every `zones.json` to the custom domain, update `NEXT_PUBLIC_HOST_ORIGIN` in the zones, and update `CORS_ORIGINS`. Zones stay on their Amplify URLs. Zone traffic flows through the Main App compute: one extra hop, counted against the Main App compute quota.

**Option B — CloudFront path routing.** Use this when the extra hop is a measured problem. Create one distribution with the custom domain and one origin per Amplify app:

| Path pattern | Origin | Cache policy | Origin request policy |
| --- | --- | --- | --- |
| `/iam/_next/static/*` | users-management | CachingOptimized | none |
| `/iam*` | users-management | CachingDisabled | AllViewerExceptHostHeader |
| `/_next/static/*` | Main App | CachingOptimized | none |
| `*` (default) | Main App | CachingDisabled | AllViewerExceptHostHeader |

Do not forward the viewer `Host` header. Forward cookies and query strings. Keep the Main App rewrites in place; they are inactive behind CloudFront and keep the Main App Amplify URL usable on its own.

Amplify "Rewrites and redirects" 200 rules can also proxy a path to an external URL. They reach public targets only, and CloudFront drops some request headers on the way. Use them only if `next.config.ts` rewrites fail on Amplify.

Verified on Amplify (2026-09-04): `next.config.ts` rewrites from the Main App's compute reach the zone apps unchanged — a zone chunk requested through the Main App answers `200` with `cache-control: public, max-age=31536000, immutable` (`x-cache: Miss from cloudfront`, i.e. served by the rewrite), cookies and `Set-Cookie` pass through, and the login bounce lands on the public origin from a zone opened directly. Run `assets/tests/zones.spec.ts` against the deployed origin (`ZONES_BASE=https://…`, `--project chromium` and `--project webkit`) after every first deployment of a new zone.

### End-to-End Automated Workflow Summary

```
1. get_project_detail → discover context (URLs, credentials, microapps)
2. Validate daasUrl, supabaseUrl, mainAmplifyUrl
3. Choose a short prefix per micro-app with the user. Check for conflicts.
4. Check if the micro-app exists in microapps[]
   ├── Exists → clone gitUrl, restore any iframe-edited CLI files to stock, continue
   └── New → bootstrap the project
5. Generate config/zones.json + config/app-urls.ts in the zone and in the Main App
6. Zone: next.config.ts (basePath, allowedOrigins), pinned edits Z-M1, Z1, Z-W1, navigation.ts, lib/shell
7. Main App: next.config.ts (rewrites), pinned edits Z-M1h, Z-M2, Z1, Z-P1, navigation.ts, lib/shell
8. Set CORS_ORIGINS on the DaaS backend to the public origin
9. Playwright suite green on local production builds; next build green in every app
10. git push the zone → Amplify deploys (NEXT_PUBLIC_HOST_ORIGIN set in Amplify)
11. git push the Main App → Amplify deploys with the new rewrites; run the suite against the deployed origin
```

## Migration from `add-microfrontend` (iframe)

Do this **first**, before any zone edit: restore every CLI-owned file the iframe skill pinned back to stock (`git show <bootstrap-commit>:<path>`, or `npx @buildpad/cli add <origin> --overwrite`), then delete the iframe files, then apply the zone steps.

| Iframe skill artifact | Zones skill |
| --- | --- |
| Main App: `app/<section>/page.tsx` iframe host pages, `components/MicroappIframe.tsx`, `lib/bridge/*`, the iframe Playwright suites and configs | Delete. Rewrites replace the host pages. |
| Main App: `AuthenticatedShell.tsx` pinned edit S1 (logout broadcast) | Restore stock, then Z1. |
| Micro-app: `components/MicroappBridgeProvider.tsx`, `components/LoginBridge.tsx`, `hooks/useQueryParamSync.ts`, `lib/bridge/*` | Delete. |
| Micro-app: `app/api/auth/set-session/route.ts`, `app/api/auth/token/route.ts` | Delete. |
| Micro-app: `*-section.tsx` wrappers and `section-nav.ts` under `app/(authenticated)/` | Delete; the module pages go back to the CLI's `router.push('/users/<id>')` versions. |
| Micro-app: pinned edits M1–M4 (`lib/supabase/middleware.ts`), E1/E1b (`(authenticated)/layout.tsx`), L1 (`logout/route.ts`), H1 (`lib/api/auth-headers.ts`, `api/auth/user/route.ts`), P1 (`login/page.tsx`), W1 (`DaaSProviderWrapper.tsx`), the framed-logout edit in `AuthenticatedShell.tsx`, `MicroappBridgeProvider` in `app/layout.tsx` | Restore stock. Then Z-M1, Z1, Z-W1. |
| `next.config.ts` with `frame-ancestors` / `frame-src` CSP in both apps | Replace with `assets/host/` and `assets/zone/` versions. |
| `config/app-urls.ts` with `MICROAPP_URLS` / `HOST_ORIGIN` / `DEFAULT_AUTHENTICATED_ROUTE` | Replace with `zones.json` and the new `app-urls.ts`. |
| `NEXT_PUBLIC_MICROAPP_URL_MAIN` in `.env*` | `NEXT_PUBLIC_HOST_ORIGIN` (Rule 15). |
| `sandbox` attribute, `postMessage` origin checks, `allowedParams` lists | Delete. |
| Mantine modals instead of native dialogs (iframe Rule 12) | No longer necessary. Keep Mantine modals for a consistent UI. |

Add: `basePath` in each zone, rewrites in the Main App, `lib/shell/` in every app, `allowedOrigins` in every app, the identical `navigation.ts`.

## Tradeoffs to tell the user

- Navigation between zones is a full page load; inside a zone it is a soft navigation. Measured on production builds: shell visible in 0.6 s for a warm cross-zone switch, against 0.9 s for the iframe's soft navigation plus frame reload; rows arrive about 0.4 s later than in the iframe, whose host document persists.
- Cold loads are 2–4× faster than the iframe composition (Users 0.7 s vs 2.9 s to shell, Files 0.9 s vs 1.8 s), with one document instead of two or three and 40% fewer requests.
- One zone per URL. Two zones cannot render on one screen. Use the iframe skill for that case.
- The shell is generated into every app. A shell change needs a regeneration and a deploy of every app, or a shared npm package.
- Module URLs nest under the zone prefix (`/iam/users`, not `/users`).
- All zones share one origin. There is no DOM, CSS, or cookie isolation between zones. A security bug in one zone affects the full origin.
- A new zone needs a Main App deploy, because the rewrites are static.
- Zone traffic flows through the Main App compute until CloudFront path routing is in place, and every zone page load pays two middleware auth calls.

In return, each screen has one document, one React runtime, and one SSR pass. There is no auth handshake, and the URL and the history are real.

## Security Boundaries

| Boundary | Implementation |
| --- | --- |
| Routing | Main App rewrites. Only listed prefixes reach a zone. |
| Auth | One Supabase session cookie on one origin, validated by the middleware of the Main App and of the zone. |
| Login bounce | `next=` is a path only; `safeRelativePath` rejects off-origin targets (Z-P1). |
| Server Actions | `allowedOrigins` limited to the public host in every app. |
| Data | Single shared DaaS backend. Access controlled by RBAC and RLS. |
| CORS | `CORS_ORIGINS` limited to the public origin. |
| Isolation | None between zones. Same origin. Use the iframe skill when isolation is a requirement. |
| Deployment | Independent Amplify apps. Zone URLs are not user-facing. |

## References

- [Pinned edits for CLI-owned files](references/pinned-edits.instructions.md)
- [Next.js Multi-Zones guide](https://nextjs.org/docs/app/guides/multi-zones)
- [Next.js `with-zones` example](https://github.com/vercel/next.js/tree/canary/examples/with-zones)
- [Supabase `getClaims()`](https://supabase.com/docs/reference/javascript/auth-getclaims) and [JWT signing keys](https://supabase.com/docs/guides/auth/signing-keys)
- [Context discovery reference](../add-microapp/references/context-discovery.instructions.md)
- [`add-microfrontend` (iframe composition)](../add-microfrontend/SKILL.md) — the fallback mode
<!-- /buildpad-backend -->
