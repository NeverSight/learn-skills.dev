---
name: add-microapp
description: Split an app into a Main App plus domain-focused micro-apps that share one DaaS backend. Covers domain boundaries, collection ownership, shared RBAC, cross-domain contracts, and repo bootstrap. Load this skill FIRST to decide the split, then load add-microfrontend-zones (Multi-Zones, the default for Next.js micro-apps) or add-microfrontend (iframe composition and the auth bridge) to wire the composition. Use when the user says add-microapp, microapp, service boundary, or needs to split a large app into domain-focused micro-apps.
argument-hint: "[service name] [domain, e.g. users, billing, analytics]"
---

# Add Microapp

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
Set up a **microapp architecture** where one **Main App** and multiple **micro-apps** all share a **single DaaS backend**. Each micro-app is a standalone Next.js application that owns a domain of collections within the shared DaaS. Micro-apps are composed at the client level via the iframe micro-frontend pattern.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Set up a **microapp architecture** where one **Main App** and multiple **micro-apps** all share a **single DaaS backend**: on an Engine project, the Engine. Each micro-app is a standalone Next.js application that owns a domain of collections within the shared backend. On an Engine project each app runs on its own address and the Main App links to the micro-apps: composing them into one page is not available on an Engine project yet (Rule 11).
<!-- /buildpad-backend -->

## Critical Rules

<!-- buildpad-backend: supabase -->
1. **Single Shared DaaS Backend**: All apps (Main App + micro-apps) connect to the **same** DaaS backend instance via the same `NEXT_PUBLIC_BUILDPAD_DAAS_URL`. There is only ONE DaaS backend. Collections for all domains live in this single instance.
2. **Shared Auth, Shared Data Layer**: All apps share the same Supabase Auth project AND the same DaaS backend. Authentication and data access go through the same infrastructure.
3. **Direct Calls for Components, Proxy Routes for Your Own Code**: Buildpad UI components (`CollectionList`, `VForm`) call DaaS **directly** from the browser through `DaaSProvider`, which supplies the `Authorization: Bearer <supabase-jwt>` and `X-Resource-Uri` headers. Hand-written fetches go through a Next.js proxy route in the same app. Do not generate `/api/items/[collection]/route.ts` unless the app has hand-written data calls. CORS for the direct path is handled on the DaaS side via `CORS_ORIGINS`. See [authentication-proxy](../authentication-proxy/SKILL.md).
4. **Collection-Based Domain Boundaries**: Each micro-app "owns" a logical domain of collections (e.g., Users service owns `profiles`, `roles`; Billing service owns `invoices`, `payments`). Ownership is a team/code convention — all collections physically live in the same DaaS instance. **Check every candidate domain against the module skills first — [add-files](../add-files/SKILL.md) and [add-users](../add-users/SKILL.md) — because the module may already provide the whole surface, and a hand-written page in its place leaves the real behaviour untested.**
5. **Independent Deployment**: Each micro-app deploys independently as a Next.js application. Schema changes in DaaS are shared — coordinate collection/field changes via the DaaS admin or MCP tools.
6. **Main App Is a Full App**: The Main App handles authentication, navigation, iframe composition, AND can have its own pages and collection data. It is not a thin shell.
7. **Shared Types via Contracts**: Cross-domain data access uses well-defined TypeScript interfaces. Publish shared types via a `packages/shared-types/` package or shared contract files.
8. **Backend-First Logic**: Use DaaS runtime extensions (filter/action hooks) for validation, audit logging, and business rules — not Next.js API routes. Extensions are configured once in the shared DaaS and apply regardless of which app triggers the request.
9. **Independent Testing**: Each micro-app has its own test suite (Playwright E2E + Vitest unit). Cross-service integration tests live in the Main App project.
10. **Shared RBAC**: Roles and permissions are managed centrally in the single DaaS backend. Each role defines access to specific collections. A user's roles (assigned via the `daas_user_roles` junction table) determine what they can do across ALL apps.
11. **Iframe Constraints Apply to Every Micro-App** (iframe composition only — under [add-microfrontend-zones](../add-microfrontend-zones/SKILL.md) Rules 11 and 14 do not apply): A framed micro-app cannot use native dialogs, cannot make a modal cover the host chrome (the overlay and the focus trap end at the frame edge, so one click in the host discards the dialog — route destructive confirmations to the host), and cannot rely on the host cookie — and it renders **content only**: the host owns the sidebar, header, and profile chrome, so the micro-app's own shell appears only when it is opened standalone (pinned edit E1). Design domains with that in mind. The rules and their fixes live in [add-microfrontend](../add-microfrontend/SKILL.md).
12. **No Function Props from Server Components (React 19)**: In Next.js 16 / React 19, you cannot pass functions as props from Server Components to Client Components. Avoid patterns like `<Anchor component={Link}>` in Server Components — use plain `<Link>` from `next/link` instead. The `component={...}` pattern is safe inside a `'use client'` component.
13. **Verify Field Names Against DaaS Schema**: Before writing any query, sort, or filter parameter, **always check the actual field names** in the DaaS schema using `mcp_daas_schema` or `mcp_daas_fields`. Do NOT assume field names — they may differ from common conventions (e.g., `created_at` vs `date_created`). Using a non-existent field in `sort` or `filter` causes a DaaS **500 error** with no helpful message, which is hard to debug through the proxy layer.
14. **Cross-Domain Auth Bridge (Amplify — always required)**: Supabase cookies cannot be shared between `*.amplifyapp.com` subdomains, so every micro-app needs the postMessage auth bridge. The bridge is owned by [add-microfrontend](../add-microfrontend/SKILL.md). Load that skill and copy the files it ships. Never send a refresh token across the bridge — see [auth-bridge](../add-microfrontend/references/auth-bridge.instructions.md).
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
1. **Single Shared DaaS Backend**: All apps (Main App + micro-apps) connect to the **same** Engine via the same `NEXT_PUBLIC_BUILDPAD_DAAS_URL`. There is only ONE backend. Collections for all domains live in this single instance. On an Engine project the data API's address is the Engine_URL, which both `NEXT_PUBLIC_BUILDPAD_DAAS_URL` and `NEXT_PUBLIC_SUPABASE_URL` hold. The Studio's address is an administration interface: send no data call to it.
2. **Shared Sign-In, Shared Data Layer**: All apps sign their users in against the same Engine AND use the same data API. On an Engine project the Supabase client is kept for sign-in only, and it points at the Engine_URL as well.
3. **Direct Calls for Components, Proxy Routes for Your Own Code**: Buildpad UI components (`CollectionList`, `VForm`) call the Engine **directly** from the browser through `DaaSProvider`, which supplies the `Authorization: Bearer <access token>` header (the signed-in user's access token) and the `X-Resource-Uri` header. Hand-written fetches go through a Next.js proxy route in the same app. Do not generate `/api/items/[collection]/route.ts` unless the app has hand-written data calls. On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere. See [authentication-proxy](../authentication-proxy/SKILL.md).
4. **Collection-Based Domain Boundaries**: Each micro-app "owns" a logical domain of collections (e.g., Users service owns `profiles`, `roles`; Billing service owns `invoices`, `payments`). Ownership is a team/code convention — all collections physically live in the same DaaS instance. **Check every candidate domain against the module skills first — [add-files](../add-files/SKILL.md) and [add-users](../add-users/SKILL.md) — because the module may already provide the whole surface, and a hand-written page in its place leaves the real behaviour untested.**
5. **Independent Deployment**: Each micro-app deploys independently as a Next.js application. Schema changes in the Engine are shared — coordinate collection/field changes through the Studio or the Engine's MCP tools (Step 9).
6. **Main App Is a Full App**: The Main App handles sign-in, navigation, AND can have its own pages and collection data. It is not a thin shell. On an Engine project it does not frame the micro-apps yet (Rule 11).
7. **Shared Types via Contracts**: Cross-domain data access uses well-defined TypeScript interfaces. Publish shared types via a `packages/shared-types/` package or shared contract files.
8. **Backend-First Logic**: Use event hooks stored in the Engine (filter and action hooks) for validation, audit logging, and business rules — not Next.js API routes. A hook is stored once in the shared Engine and applies regardless of which app triggers the request. Stored code runs in the Engine's runtime, which offers less than Node.js: see pattern 4 of [Cross-domain data access](references/cross-service-communication.instructions.md).
9. **Independent Testing**: Each micro-app has its own test suite (Playwright E2E + Vitest unit). Cross-service integration tests live in the Main App project.
10. **Shared RBAC**: Roles, policies and permissions are managed centrally in the single Engine. A permission belongs to a policy, and a policy is attached to a role or a user. A user's roles in the project's tenant (given with `POST /api/users/:id/roles` or in the Studio's Users module) determine what they can do across ALL apps.
11. **Composition Is Not Available on an Engine Project Yet**: Sharing one session between a host and the micro-apps it shows is not available on an Engine project yet: it waits on a change to the Engine. So iframe composition ([add-microfrontend](../add-microfrontend/SKILL.md)) and Multi-Zones ([add-microfrontend-zones](../add-microfrontend-zones/SKILL.md)) are not available on an Engine project yet. When the developer asks for micro-apps shown inside the Main App, tell them so and stop there: frame no micro-app and build no substitute. Each app is used on its own address.
12. **No Function Props from Server Components (React 19)**: In Next.js 16 / React 19, you cannot pass functions as props from Server Components to Client Components. Avoid patterns like `<Anchor component={Link}>` in Server Components — use plain `<Link>` from `next/link` instead. The `component={...}` pattern is safe inside a `'use client'` component.
13. **Verify Field Names Against the Schema**: Before writing any query, sort, or filter parameter, **always check the actual field names** with `mcp_daas_schema` or `mcp_daas_fields`. Do NOT assume field names — they may differ from common conventions (e.g., `created_at` vs `date_created`). A field that does not exist in `sort` or `filter` makes the request fail, and the error is hard to trace through the proxy layer.
14. **Cross-Domain Session Bridge — Not Available on an Engine Project Yet**: The cross-domain session bridge of [add-microfrontend](../add-microfrontend/SKILL.md) is not available on an Engine project yet (Rule 11). Write no bridge file and copy none of that skill's files.
<!-- /buildpad-backend -->

## Architecture

<!-- buildpad-backend: supabase -->
```
┌────────────────────────────────────────────────────────────────┐
│  Main App  (my-app)                                            │
│  - Auth (login/logout), session and token refresh              │
│  - Navigation & iframe composition                             │
│  - Own pages (dashboard, settings, etc.)                       │
│  - Components → shared DaaS directly                           │
└─────────┬──────────────────────┬───────────────────┬───────────┘
          │                      │                   │
          ▼                      ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Users App       │  │  Billing App     │  │  Analytics App   │
│  (micro-app)     │  │  (micro-app)     │  │  (micro-app)     │
│  ┌─────────────┐ │  │  ┌─────────────┐ │  │  ┌─────────────┐ │
│  │ Next.js App │ │  │  │ Next.js App │ │  │  │ Next.js App │ │
│  │ own cookie  │ │  │  │ own cookie  │ │  │  │ own cookie  │ │
│  └──────┬──────┘ │  │  └──────┬──────┘ │  │  └──────┬──────┘ │
└─────────┼────────┘  └─────────┼────────┘  └─────────┼────────┘
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                ▼
                  ┌──────────────────────────┐
                  │  Single DaaS Backend     │
                  │  (shared by ALL apps)    │
                  │                          │
                  │  Collections:            │
                  │  - profiles, roles       │  ← Users domain
                  │  - invoices, payments    │  ← Billing domain
                  │  - events, reports       │  ← Analytics domain
                  │  - settings, dashboard   │  ← Main App domain
                  └────────────┬─────────────┘
                               ▼
                  ┌──────────────────────────┐
                  │  Supabase                │
                  │  (Auth + single DB)      │
                  └──────────────────────────┘
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```
┌────────────────────────────────────────────────────────────────┐
│  Main App  (my-app)                                            │
│  - Sign-in (login/logout), session and token refresh           │
│  - Navigation, with links to each micro-app's address          │
│  - Own pages (dashboard, settings, etc.)                       │
│  - Components → the shared Engine directly                     │
└─────────┬──────────────────────┬───────────────────┬───────────┘
          │ link                 │ link              │ link
          ▼                      ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Users App      │  │  Billing App    │  │  Analytics App  │
│  (micro-app)    │  │  (micro-app)    │  │  (micro-app)    │
│  own address,   │  │  own address,   │  │  own address,   │
│  own sign-in    │  │  own sign-in    │  │  own sign-in    │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                ┌──────────────────────────┐
                │  Single Engine           │
                │  (shared by ALL apps)    │
                │  data API + sign-in,     │
                │  its own database        │
                │                          │
                │  Collections:            │
                │  - profiles, roles       │  ← Users domain
                │  - invoices, payments    │  ← Billing domain
                │  - events, reports       │  ← Analytics domain
                │  - settings, dashboard   │  ← Main App domain
                └──────────────────────────┘
```
<!-- /buildpad-backend -->

## Implementation Steps

### Step 0: Discover Project Context (MANDATORY — ALWAYS FIRST)

<!-- buildpad-backend: supabase -->
Before any code or configuration, call the `get_project_detail` platform MCP tool to auto-discover the full project context. **Never ask the user for URLs or credentials — they are all in the context.**

```json
// Call the platform MCP tool — no arguments needed
{ "name": "get_project_detail", "arguments": {} }
```

This returns:
- **`project.mainAmplifyUrl`** — Main App's deployed URL (the `HOST_ORIGIN` default in each micro-app's `config/app-urls.ts`; override via `NEXT_PUBLIC_MICROAPP_URL_MAIN`, never `NEXT_PUBLIC_HOST_ORIGIN` — that name is reserved by `lib/origin.ts`)
- **`project.supabaseUrl`**, **`project.supabaseAnonKey`**, **`project.supabaseServiceRoleKey`** — shared auth credentials
- **`project.daasUrl`** — shared DaaS backend URL
- **`project.mainGitUrl`**, **`project.mainGitToken`** — git credentials for cloning/pushing
- **`microapps[]`** — list of existing micro-apps with `name`, `gitUrl`, `amplifyUrl`

**Validation:** If any critical value (`daasUrl`, `supabaseUrl`, `mainAmplifyUrl`) is null, report it to the user with a specific remediation step. Do NOT proceed with placeholder values.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Before any code or configuration, call the `get_project_detail` platform MCP tool to auto-discover the full project context. **Never ask the user for URLs or credentials — they are all in the context.**

```json
// Call the platform MCP tool — no arguments needed
{ "name": "get_project_detail", "arguments": {} }
```

On an Engine project this returns:
- **`project.projectBackend`** — `"engine"`. If it names the other backend, tell the developer that the Platform and the backend established above disagree, and ask which holds before you go on
- **`project.mainAmplifyUrl`** — Main App's deployed URL (the `HOST_ORIGIN` default in each micro-app's `config/app-urls.ts`; override via `NEXT_PUBLIC_MICROAPP_URL_MAIN`, never `NEXT_PUBLIC_HOST_ORIGIN` — that name is reserved by `lib/origin.ts`)
- **`project.engineUrl`**, **`project.daasUrl`** — both the Engine_URL: the shared data API and sign-in address of every app
- **`project.projectTenantId`** — the project's tenant id
- **`project.tenantVariable`** — the name of the variable that carries the tenant id, `NEXT_PUBLIC_BUILDPAD_TENANT_ID`
- **`project.publicAnonKey`** — the fixed value for `NEXT_PUBLIC_SUPABASE_ANON_KEY` (not a secret)
- **`project.mainGitUrl`**, **`project.mainGitToken`** — git credentials for cloning/pushing
- **`microapps[]`** — list of existing micro-apps with `name`, `gitUrl`, `amplifyUrl`

The `project` object of an Engine project holds no Supabase address or key, no service-role key and no password: there is none to read.

**Validation:** If any critical value (`engineUrl`, `daasUrl`, `projectTenantId`, `mainAmplifyUrl`) is null, report it to the user with a specific remediation step. Do NOT proceed with placeholder values. Never stop because a Supabase value is absent: an Engine project has none.
<!-- /buildpad-backend -->

See [Context Discovery reference](references/context-discovery.instructions.md) for the full response schema and derivation rules.

### Step 1: Define Collection Domain Boundaries

Before creating any code, map out which collections belong to which app's domain. All collections live in the **same DaaS instance**:

| App / Domain | Collections                         | Owned By Team |
| ------------ | ----------------------------------- | ------------- |
| Main App     | `settings`, `dashboard_widgets`     | Core team     |
| Users        | `profiles`, `roles`, `preferences`  | Users team    |
| Billing      | `invoices`, `plans`, `payments`     | Billing team  |
| Analytics    | `events`, `reports`, `dashboards`   | Analytics team|

**Important**: Any app can _read_ any collection (subject to RBAC). Ownership means the team is responsible for that collection's schema, hooks, and business logic.

**Check each domain against the module skills before you plan any page.** Files maps to
[add-files](../add-files/SKILL.md) (`buildpad add files-routes`); users, roles, and
policies map to [add-users](../add-users/SKILL.md) (`buildpad add users-routes`);
workflow definitions, assignments, and instances map to
[add-workflows](../add-workflows/SKILL.md) (`buildpad add workflows-routes`); cron jobs
and their run history map to [add-cron](../add-cron/SKILL.md) (`buildpad add cron-routes`); an
AI chat or assistant maps to [add-ai-chat](../add-ai-chat/SKILL.md) (`buildpad add ai-chat-routes`).
Where a module exists, scaffold it and wrap it. Write a page by hand only for a domain no
module covers.

### Step 2: Create or Clone the Micro-App Project

Check if the microapp already exists in the `microapps[]` array from Step 0:

**If the microapp exists** (has `gitUrl`):
```bash
# Clone using the discovered git URL (includes credentials)
git clone {{microapp.gitUrl}} /path/to/{{microapp.name}}
cd /path/to/{{microapp.name}}
pnpm install
```

**If the microapp is new** — bootstrap it:
```bash
# Create the micro-app project
mkdir -p /path/to/{{serviceName}}-app
npx @buildpad/cli@latest bootstrap --cwd /path/to/{{serviceName}}-app
```

<!-- buildpad-backend: supabase -->
> The directory name is a local choice and is NOT the platform `microapps[].name` —
> existing repos may be called `<name>-starter`, `<name>-app`, or anything else.
> Config keys and env-var names always derive from the platform `name`; routes come
> from the micro-app's own `DEFAULT_AUTHENTICATED_ROUTE`. Write the mapping table
> from [add-microfrontend Step 3](../add-microfrontend/SKILL.md) before creating
> pages.

### Step 3: Auto-Configure Environment & URL Config (From Context — No User Input)

**ALL values come from the `get_project_detail` response.** Never use placeholder URLs.

Configuration is split in two:

- `.env.local` — infrastructure secrets (Supabase, DaaS). Also set in the Amplify console.
- `config/app-urls.ts` — application URLs, committed to git, available at build time.

Write both files for the Main App and for every micro-app. The file shapes, the
generation rules, and the failure modes are in one place:
[app-urls config](references/app-urls-config.instructions.md).

### Step 4: Auth Bridge for Cross-Domain Sessions (ALWAYS Required on Amplify)

On Amplify each app gets a different `*.amplifyapp.com` subdomain. `amplifyapp.com` is
a public suffix, so the browser treats each subdomain as a separate site and Supabase
cookies from the Main App are invisible to the micro-app. Without the bridge, the user
sees a login prompt in every micro-app section.

The bridge is owned by
[add-microfrontend](../add-microfrontend/SKILL.md). Load that skill and copy the files
it ships. Do not reimplement the bridge here.

Two rules matter while you bootstrap the repos:

1. Every micro-app needs `app/api/auth/set-session/route.ts`,
   `app/api/auth/logout/route.ts`, and `app/api/auth/token/route.ts`.
2. Every micro-app `config/app-urls.ts` needs `HOST_ORIGIN` and
   `DEFAULT_AUTHENTICATED_ROUTE`.

Full implementation and the security checklist:
[auth-bridge](../add-microfrontend/references/auth-bridge.instructions.md).

### Step 5: Configure Direct DaaS Access (Both Apps)

Buildpad UI components call DaaS directly from the browser. Hand-written fetches use a proxy route in the same app (Rule 3). Supply the DaaS URL and the Supabase JWT with `DaaSProvider`:

In a Buildpad starter the CLI already installs `components/DaaSProviderWrapper.tsx`
mounted from `app/(authenticated)/layout.tsx` — keep that. Never move the provider to
the root layout: root layouts never unmount, so a logout → login cycle delivers a
stale token (daas-platform Bug 22). The hand-rolled shape, for reference:

```typescript
// app/(authenticated)/layout.tsx-style wiring — NEVER app/layout.tsx (Bug 22)
import { DaaSProvider } from '@/lib/buildpad/services';
import { createBrowserClient } from '@supabase/ssr';

const supabase = createBrowserClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <DaaSProvider
          config={{
            url: process.env.NEXT_PUBLIC_BUILDPAD_DAAS_URL!,
            getToken: () => supabase.auth.getSession().then(({ data }) => data.session?.access_token ?? null),
          }}
        >
          {children}
        </DaaSProvider>
      </body>
    </html>
  );
}
```

DaaS CORS is a **settings singleton**, not env vars, and the default
(`cors_origins: ["*"]`, `cors_allow_credentials: false`) blocks every credentialed
browser call. Configure it with the runnable `mcp_daas_cors-settings` update in
[add-microfrontend Step 6](../add-microfrontend/SKILL.md) — origins must be explicit
and `cors_allow_credentials` must be `true`.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
> The directory name is a local choice and is NOT the platform `microapps[].name` —
> existing repos may be called `<name>-starter`, `<name>-app`, or anything else.
> Config keys and env-var names always derive from the platform `name`.

### Step 3: Auto-Configure Environment & URL Config (From Context — No User Input)

**ALL values come from the `get_project_detail` response.** Never use placeholder URLs.

Configuration is split in two:

- `.env.local` — infrastructure values: the Engine_URL, the fixed anon value and the project's tenant id. Also set in the Amplify console.
- `config/app-urls.ts` — application URLs, committed to git, available at build time.

On an Engine project the environment is: `NEXT_PUBLIC_SUPABASE_URL=<Engine_URL>`, `NEXT_PUBLIC_BUILDPAD_DAAS_URL=<Engine_URL>`, `NEXT_PUBLIC_SUPABASE_ANON_KEY=buildpad-engine-public-anon-key` (a fixed value that is not a secret; the Engine does not read it, the Supabase client needs one), and `NEXT_PUBLIC_BUILDPAD_TENANT_ID=<the project's tenant id>`. There is no service-role key on an Engine project: add none.

Write both files for the Main App and for every micro-app, with the same four values in each. The file shapes, the
generation rules, and the failure modes are in one place:
[app-urls config](references/app-urls-config.instructions.md).

### Step 4: Sharing the Session Across Apps (Not Available on an Engine Project Yet)

On an Engine project, sharing one session between the Main App and the micro-apps it
frames is not available yet: it waits on a change to the Engine. The cross-domain
session bridge and iframe composition
([add-microfrontend](../add-microfrontend/SKILL.md)), and Multi-Zones
([add-microfrontend-zones](../add-microfrontend-zones/SKILL.md)), are therefore not
available on an Engine project yet.

Write no bridge file and frame no micro-app in the Main App. If the developer asks for
the micro-apps inside the Main App, tell them that this is not available on an Engine
project yet and stop there; do not build a substitute. Each app is deployed on its own
address and signs its users in itself; the steps below hold for every app.

### Step 5: Configure Direct DaaS Access (Both Apps)

Buildpad UI components call the Engine directly from the browser. Hand-written fetches use a proxy route in the same app (Rule 3). On an Engine project the data API's address is the Engine_URL, which both `NEXT_PUBLIC_BUILDPAD_DAAS_URL` and `NEXT_PUBLIC_SUPABASE_URL` hold. The Studio's address is an administration interface: send no data call to it.

Supply the Engine_URL and the signed-in user's access token with `DaaSProvider`.
In a Buildpad starter the CLI already installs `components/DaaSProviderWrapper.tsx`
mounted from `app/(authenticated)/layout.tsx` — keep that. Never move the provider to
the root layout: root layouts never unmount, so a logout → login cycle delivers a
stale token (daas-platform Bug 22). The hand-rolled shape, for reference:

```typescript
// app/(authenticated)/layout.tsx-style wiring — NEVER app/layout.tsx (Bug 22)
import { DaaSProvider } from '@/lib/buildpad/services';
import { createBrowserClient } from '@supabase/ssr';

const supabase = createBrowserClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <DaaSProvider
          config={{
            url: process.env.NEXT_PUBLIC_BUILDPAD_DAAS_URL!,
            getToken: () => supabase.auth.getSession().then(({ data }) => data.session?.access_token ?? null),
          }}
        >
          {children}
        </DaaSProvider>
      </body>
    </html>
  );
}
```

On an Engine project both environment variables hold the Engine_URL, so the Supabase
client signs the user in against the Engine and `getToken` returns the Engine's access
token.

**Leave the cross-origin settings as they are.** On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere. The components send the user's
access token as `Authorization: Bearer`, never a cookie, so there is nothing to configure.
<!-- /buildpad-backend -->

In client components, use `useDaaSContext()` to get `buildUrl` and `getHeaders`:

```typescript
import { useDaaSContext } from '@/lib/buildpad/services';

export function OrdersList() {
  const { buildUrl, getHeaders } = useDaaSContext();

  useEffect(() => {
    fetch(buildUrl('/api/items/orders'), { headers: getHeaders() })
      .then(r => r.json())
      .then(data => setOrders(data.data));
  }, []);
}
```

<!-- buildpad-backend: supabase -->
### Step 6: Main App with Service Routing (Auto-Generated from Context)

Generate the service registry from the `microapps[]` returned by `get_project_detail`. **Do not hardcode service entries** — derive them dynamically. The registry imports URLs from the committed `config/app-urls.ts`:

```typescript
// my-app/lib/services.ts
// Auto-generated from get_project_detail → microapps[]
// URLs come from config/app-urls.ts (committed to git)

import { MICROAPP_URLS } from '@/config/app-urls';

export const MICRO_APPS = {
  // Example: if microapps[] contains { name: 'users-app', amplifyUrl: 'https://main.d123.amplifyapp.com' }
  'users-app': {
    url: MICROAPP_URLS['users-app'],
    label: 'Users',
    icon: 'users',
    routes: [
      { path: '/admin/users', microappPath: '/users', label: 'All Users' },
      { path: '/admin/users/roles', microappPath: '/roles', label: 'Roles' },
    ],
  },
  'billing-app': {
    url: MICROAPP_URLS['billing-app'],
    label: 'Billing',
    icon: 'credit-card',
    routes: [
      { path: '/admin/billing', microappPath: '/invoices', label: 'Invoices' },
      { path: '/admin/billing/plans', microappPath: '/plans', label: 'Plans' },
    ],
  },
} as const;
```

**Agent rule:** When generating `lib/services.ts`, iterate over the actual `microapps[]` array from context — do not use example entries. Import URLs from `config/app-urls.ts` rather than reading `process.env` directly.

`MicroappIframe` ships with [add-microfrontend](../add-microfrontend/SKILL.md). Copy it
from there. Do not write your own.

```typescript
// my-app/app/admin/users/page.tsx
import { MicroappIframe } from '@/components/MicroappIframe';
import { MICRO_APPS } from '@/lib/services';

export default function AdminUsersPage() {
  return (
    <MicroappIframe
      src={MICRO_APPS.users.url}
      path="/users"
      title="Users Management"
      // Derive this from what the framed page really syncs. A CLI module keeps
      // search/page/sort private, so those names cannot cross the boundary.
      // See add-microfrontend Step 4.
      allowedParams={['user']}
      height="calc(100vh - 100px)"
    />
  );
}
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Step 6: Main App with Service Routing (Auto-Generated from Context)

Generate the service registry from the `microapps[]` returned by `get_project_detail`. **Do not hardcode service entries** — derive them dynamically. The registry imports URLs from the committed `config/app-urls.ts`. On an Engine project the Main App uses it for navigation links only: each micro-app is opened on its own address.

```typescript
// my-app/lib/services.ts
// Auto-generated from get_project_detail → microapps[]
// URLs come from config/app-urls.ts (committed to git)

import { MICROAPP_URLS } from '@/config/app-urls';

export const MICRO_APPS = {
  // Example: if microapps[] contains { name: 'users-app', amplifyUrl: 'https://main.d123.amplifyapp.com' }
  'users-app': {
    url: MICROAPP_URLS['users-app'],
    label: 'Users',
    icon: 'users',
    routes: [
      { path: '/users', label: 'All Users' },
      { path: '/roles', label: 'Roles' },
    ],
  },
  'billing-app': {
    url: MICROAPP_URLS['billing-app'],
    label: 'Billing',
    icon: 'credit-card',
    routes: [
      { path: '/invoices', label: 'Invoices' },
      { path: '/plans', label: 'Plans' },
    ],
  },
} as const;
```

**Agent rule:** When generating `lib/services.ts`, iterate over the actual `microapps[]` array from context — do not use example entries. Import URLs from `config/app-urls.ts` rather than reading `process.env` directly. Each `path` is a real route of that micro-app.

The Main App's navigation links to each route on the micro-app's own address:

```typescript
// my-app/components/MicroappNav.tsx
import { MICRO_APPS } from '@/lib/services';

export function MicroappNav() {
  return (
    <nav>
      {Object.entries(MICRO_APPS).flatMap(([key, app]) =>
        app.routes.map((route) => (
          <a key={key + route.path} href={app.url + route.path}>
            {app.label}: {route.label}
          </a>
        )),
      )}
    </nav>
  );
}
```

Framing a micro-app inside a Main App page (`MicroappIframe` from [add-microfrontend](../add-microfrontend/SKILL.md)) is not available on an Engine project yet. If the developer asks for it, tell them so and stop for that part: write no frame page and build no substitute.
<!-- /buildpad-backend -->

### Step 7: Cross-Domain Data Access

Since all apps share the same DaaS backend, a micro-app can query **any collection** it has RBAC access to — even collections "owned" by another domain. No API-to-API calls needed:

```typescript
// billing-app needs to display user name on an invoice
// It queries the 'profiles' collection directly from the shared DaaS
// using buildUrl/getHeaders from DaaSProvider — no proxy needed

export async function getInvoiceWithUser(invoiceId: string) {
  // Both calls go directly to the same DaaS backend
  const { buildUrl, getHeaders } = useDaaSContext(); // or use buildApiUrl from services
  const invoice = await fetch(buildUrl(`/api/items/invoices/${invoiceId}`), { headers: getHeaders() }).then(r => r.json());
  const profile = await fetch(buildUrl(`/api/items/profiles/${invoice.data.user_id}`), { headers: getHeaders() }).then(r => r.json());

  return {
    ...invoice.data,
    user_display_name: profile.data.display_name,
  };
}
```

**When cross-domain access is common**, use DaaS **relational fields** to fetch related data in a single request:

```typescript
// Fetch invoice with related user profile in one DaaS call
const response = await fetch(
  buildUrl('/api/items/invoices/inv-001?fields=*,user_id.display_name,user_id.email'),
  { headers: getHeaders() }
);
// Returns invoice with nested user data — no extra API calls
```

### Step 8: Shared Type Contracts

Define shared interfaces for cross-domain data:

```typescript
// packages/shared-types/src/users.ts
export interface UserProfile {
  id: string;
  email: string;
  display_name: string;
  avatar_url: string | null;
  role: string;
}

// packages/shared-types/src/billing.ts
export interface Invoice {
  id: string;
  user_id: string;
  amount: number;
  status: 'draft' | 'sent' | 'paid' | 'overdue';
  created_at: string;
}
```

Publish as a shared package or copy to each app's `types/contracts/` directory.

<!-- buildpad-backend: supabase -->
### Step 9: DaaS Collections Setup (via MCP)

All collections are created in the **same DaaS instance** via MCP tools:

```json
// mcp_daas_collections -> action: create (all in SAME DaaS instance)

// Users domain
{ "collection": "profiles", "meta": { "icon": "person", "note": "User profiles — owned by Users team" } }
{ "collection": "roles", "meta": { "icon": "shield", "note": "User roles — owned by Users team" } }

// Billing domain
{ "collection": "invoices", "meta": { "icon": "receipt", "note": "Billing invoices — owned by Billing team" } }
{ "collection": "payments", "meta": { "icon": "credit_card", "note": "Payments — owned by Billing team" } }

// Analytics domain
{ "collection": "events", "meta": { "icon": "timeline", "note": "Analytics events — owned by Analytics team" } }
{ "collection": "reports", "meta": { "icon": "assessment", "note": "Reports — owned by Analytics team" } }
```

Use collection `meta.note` to document domain ownership.

### Step 10: Shared RBAC Configuration

Roles and permissions are defined once in the single DaaS backend and apply across all apps:

```json
// mcp_daas_roles -> action: create
{ "name": "admin", "description": "Full access to all collections" }
{ "name": "billing_manager", "description": "CRUD on billing collections, read-only on profiles" }
{ "name": "viewer", "description": "Read-only access to all collections" }

// mcp_daas_permissions -> action: create
// Admin: full access
{ "role": "admin", "collection": "profiles", "action": "read", "fields": ["*"] }
{ "role": "admin", "collection": "profiles", "action": "create", "fields": ["*"] }
{ "role": "admin", "collection": "invoices", "action": "read", "fields": ["*"] }
{ "role": "admin", "collection": "invoices", "action": "create", "fields": ["*"] }

// Billing manager: full billing, read-only profiles
{ "role": "billing_manager", "collection": "invoices", "action": "read", "fields": ["*"] }
{ "role": "billing_manager", "collection": "invoices", "action": "create", "fields": ["*"] }
{ "role": "billing_manager", "collection": "invoices", "action": "update", "fields": ["*"] }
{ "role": "billing_manager", "collection": "profiles", "action": "read", "fields": ["display_name", "email"] }
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Step 9: DaaS Collections Setup (via MCP)

On an Engine project collections, fields, relations, roles, policies and permissions are created through the Engine's API (`/api/collections`, `/api/fields/:collection`, `/api/relations`, `/api/roles`, `/api/policies`, `/api/access`, `/api/permissions`) or its MCP tools `collections`, `fields`, `relations`, `roles`, `policies`, `access` and `permissions`. Access is roles, policies and permissions: a permission belongs to a policy, and a policy is attached to a role or a user. The MCP `collections` and `fields` tools keep a field's name, type and `meta` but not its `schema` block (default, not-null, length): set those through `POST /api/fields/:collection` with an administrator's session.

All collections are created in the **same Engine** with the MCP `collections` tool, one call per collection:

```json
// mcp_daas_collections -> action: create (all in the SAME Engine)

// Users domain
{ "action": "create", "data": { "collection": "profiles", "meta": { "icon": "person", "note": "User profiles — owned by Users team" } } }
{ "action": "create", "data": { "collection": "roles", "meta": { "icon": "shield", "note": "User roles — owned by Users team" } } }

// Billing domain
{ "action": "create", "data": { "collection": "invoices", "meta": { "icon": "receipt", "note": "Billing invoices — owned by Billing team" } } }
{ "action": "create", "data": { "collection": "payments", "meta": { "icon": "credit_card", "note": "Payments — owned by Billing team" } } }

// Analytics domain
{ "action": "create", "data": { "collection": "events", "meta": { "icon": "timeline", "note": "Analytics events — owned by Analytics team" } } }
{ "action": "create", "data": { "collection": "reports", "meta": { "icon": "assessment", "note": "Reports — owned by Analytics team" } } }
```

Use collection `meta.note` to document domain ownership.

### Step 10: Shared RBAC Configuration

Roles, policies and permissions are defined once in the single Engine and apply across all apps. The rules live in a policy, and the policy is attached to a role:

```json
// mcp_daas_roles -> action: create
{ "action": "create", "data": { "name": "billing_manager", "description": "CRUD on billing collections, read-only on profiles" } }
{ "action": "create", "data": { "name": "viewer", "description": "Read-only access to all collections" } }

// mcp_daas_policies -> action: create (the rules of one role)
{ "action": "create", "data": { "name": "billing_manager", "description": "Full billing, read-only profiles" } }

// mcp_daas_access -> action: create (attach the policy to the role; use the ids the calls above returned)
{ "action": "create", "data": { "policy": "<billing_manager policy id>", "role": "<billing_manager role id>" } }

// mcp_daas_permissions -> action: create (each rule names its policy)
// Billing manager: full billing, read-only profiles
{ "action": "create", "data": { "policy": "<billing_manager policy id>", "collection": "invoices", "action": "read", "fields": ["*"] } }
{ "action": "create", "data": { "policy": "<billing_manager policy id>", "collection": "invoices", "action": "create", "fields": ["*"] } }
{ "action": "create", "data": { "policy": "<billing_manager policy id>", "collection": "invoices", "action": "update", "fields": ["*"] } }
{ "action": "create", "data": { "policy": "<billing_manager policy id>", "collection": "profiles", "action": "read", "fields": ["display_name", "email"] } }
```

Give the `viewer` role its own policy and read rules the same way. For full access to every
collection, attach a policy created with `"admin_access": true` instead of writing rules.
Give each user their role in the project's tenant: `POST /api/users/:id/roles` with
`role_id`, or the Studio's Users module.
<!-- /buildpad-backend -->

### Step 11: Add Tests

**Per-app tests (in each micro-app):**

```typescript
// users-app/tests/api/users.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Users App API', () => {
  test('GET /api/items/profiles returns profiles', async ({ request }) => {
    const response = await request.get('/api/items/profiles');
    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    expect(body.data).toBeDefined();
  });

  test('POST /api/items/profiles creates profile', async ({ request }) => {
    const response = await request.post('/api/items/profiles', {
      data: { display_name: 'Test User', email: 'test@example.com' },
    });
    expect(response.status()).toBe(200);
  });
});
```

<!-- buildpad-backend: supabase -->
**Cross-app integration tests (in Main App):**

```typescript
// my-app/tests/integration/cross-app.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Cross-App Integration', () => {
  test('Main App renders users micro-app iframe', async ({ page }) => {
    await page.goto('/admin/users');
    const iframe = page.locator('iframe[title="Users Management"]');
    await expect(iframe).toBeVisible();
  });

  test('Main App renders billing micro-app iframe', async ({ page }) => {
    await page.goto('/admin/billing');
    const iframe = page.locator('iframe[title="Billing"]');
    await expect(iframe).toBeVisible();
  });

  test('navigation switches between micro-apps', async ({ page }) => {
    await page.goto('/admin/users');
    let iframe = page.locator('iframe');
    let src = await iframe.getAttribute('src');
    expect(src).toContain('users');

    await page.click('a[href="/admin/billing"]');
    await page.waitForURL('/admin/billing');
    iframe = page.locator('iframe');
    src = await iframe.getAttribute('src');
    expect(src).toContain('billing');
  });
});
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
**Cross-app integration tests (in Main App):** each app answers on its own address, and the Main App links to it.

```typescript
// my-app/tests/integration/cross-app.spec.ts
import { test, expect } from '@playwright/test';
import { MICRO_APPS } from '@/lib/services';

test.describe('Cross-App Integration', () => {
  for (const [key, app] of Object.entries(MICRO_APPS)) {
    test(key + ' answers on its own address', async ({ request }) => {
      const response = await request.get(app.url + '/api/health');
      expect(response.ok()).toBeTruthy();
    });

    test('Main App links to ' + key, async ({ page }) => {
      await page.goto('/admin/dashboard');
      const link = page.locator('a[href^="' + app.url + '"]').first();
      await expect(link).toBeVisible();
    });
  }
});
```

`/api/health` is the health route each app exposes (see [Deployment topology](references/deployment-topology.instructions.md)).
<!-- /buildpad-backend -->

## File Structure (Multi-App Workspace)

<!-- buildpad-backend: supabase -->
```
workspace/
├── my-app/                          # Main App
│   ├── app/
│   │   ├── admin/
│   │   │   ├── layout.tsx           # AdminShell
│   │   │   ├── dashboard/page.tsx   # Main App's own page
│   │   │   ├── settings/page.tsx    # Main App's own page
│   │   │   ├── users/page.tsx       # → Users micro-app iframe
│   │   │   ├── billing/page.tsx     # → Billing micro-app iframe
│   │   │   └── analytics/page.tsx   # → Analytics micro-app iframe
│   │   ├── api/
│   │   │   └── auth/                # Auth routes (Supabase SSR cookies)
│   │   └── login/page.tsx           # Login page
│   ├── components/
│   │   └── MicroappIframe.tsx       # from add-microfrontend
│   ├── config/
│   │   └── app-urls.ts             # Deployed URLs (committed to git)
│   ├── lib/
│   │   ├── bridge/                  # from add-microfrontend
│   │   └── services.ts             # Micro-app registry (imports from config)
│   ├── .env.local                   # Infrastructure secrets only
│   └── tests/
│       └── integration/
│           └── cross-app.spec.ts
│
├── users-app/                        # Users Micro-App
│   ├── app/
│   │   ├── users/                   # Users pages
│   │   ├── roles/                   # Roles pages
│   │   ├── api/
│   │   │   └── auth/                # set-session, logout, token, user
│   │   ├── login/page.tsx           # renders LoginBridge
│   │   └── ...
│   ├── components/                  # MicroappBridgeProvider, LoginBridge
│   ├── config/
│   │   └── app-urls.ts             # HOST_ORIGIN + DEFAULT_AUTHENTICATED_ROUTE
│   ├── hooks/
│   │   └── useQueryParamSync.ts
│   ├── lib/bridge/                  # bridge-protocol.ts
│   ├── .env.local                   # Infrastructure secrets only
│   └── tests/
│
├── billing-app/                      # Billing Micro-App
│   ├── app/
│   │   ├── invoices/
│   │   ├── plans/
│   │   ├── api/
│   │   │   └── auth/
│   │   └── ...
│   │   └── ...
│   ├── config/
│   │   └── app-urls.ts             # Host origin URL (committed to git)
│   ├── .env.local                   # Infrastructure secrets only
│   └── tests/
│
├── analytics-app/                    # Analytics Micro-App
│   ├── ...
│   ├── config/
│   │   └── app-urls.ts             # Host origin URL (committed to git)
│   ├── .env.local                   # Infrastructure secrets only
│   └── tests/
│
└── packages/
    └── shared-types/                 # Shared TypeScript contracts
        └── src/
            ├── users.ts
            ├── billing.ts
            └── events.ts
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```
workspace/
├── my-app/                          # Main App
│   ├── app/
│   │   ├── admin/
│   │   │   ├── layout.tsx           # AdminShell (navigation links to the micro-apps)
│   │   │   ├── dashboard/page.tsx   # Main App's own page
│   │   │   └── settings/page.tsx    # Main App's own page
│   │   ├── api/
│   │   │   ├── auth/                # Sign-in routes (the app's own server routes)
│   │   │   └── health/route.ts      # Health check
│   │   └── login/page.tsx           # Login page
│   ├── components/
│   │   └── MicroappNav.tsx          # Links to each micro-app's own address
│   ├── config/
│   │   └── app-urls.ts             # Deployed URLs (committed to git)
│   ├── lib/
│   │   └── services.ts             # Micro-app registry (imports from config)
│   ├── .env.local                   # Infrastructure values only
│   └── tests/
│       └── integration/
│           └── cross-app.spec.ts
│
├── users-app/                        # Users Micro-App (own address, own sign-in)
│   ├── app/
│   │   ├── users/                   # Users pages
│   │   ├── roles/                   # Roles pages
│   │   ├── api/
│   │   │   ├── auth/                # Sign-in routes (the app's own server routes)
│   │   │   └── health/route.ts      # Health check
│   │   ├── login/page.tsx           # Login page
│   │   └── ...
│   ├── config/
│   │   └── app-urls.ts             # Main App URL (committed to git)
│   ├── .env.local                   # Infrastructure values only
│   └── tests/
│
├── billing-app/                      # Billing Micro-App
│   ├── app/
│   │   ├── invoices/
│   │   ├── plans/
│   │   ├── api/
│   │   │   └── auth/
│   │   └── ...
│   ├── config/
│   │   └── app-urls.ts             # Main App URL (committed to git)
│   ├── .env.local                   # Infrastructure values only
│   └── tests/
│
├── analytics-app/                    # Analytics Micro-App
│   ├── ...
│   ├── config/
│   │   └── app-urls.ts             # Main App URL (committed to git)
│   ├── .env.local                   # Infrastructure values only
│   └── tests/
│
└── packages/
    └── shared-types/                 # Shared TypeScript contracts
        └── src/
            ├── users.ts
            ├── billing.ts
            └── events.ts
```
<!-- /buildpad-backend -->

## Domain Ownership Matrix

<!-- buildpad-backend: supabase -->
| Concern            | Main App                   | Micro-App (each)           |
| ------------------ | -------------------------- | -------------------------- |
| Authentication     | Login/logout flows         | Session validation only    |
| Navigation         | Sidebar, header, tabs      | Internal routes only       |
| Layout             | AppShell wrapper           | Page content only          |
| Data collections   | Own domain collections     | Own domain collections     |
| API routes         | `/api/auth/*` (+ `/api/items/*` only for hand-written fetches) | `/api/auth/*` incl. `set-session`, `logout`, `token` (+ `/api/items/*` only for hand-written fetches) |
| DaaS backend       | Shared (same URL)          | Shared (same URL)          |
| Deployment         | Independent (Amplify)      | Independent (Amplify)      |
| Testing            | Integration + E2E          | Unit + API + E2E           |
| RBAC               | Managed centrally in DaaS  | Enforced by DaaS on every request |
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
| Concern            | Main App                   | Micro-App (each)           |
| ------------------ | -------------------------- | -------------------------- |
| Authentication     | Login/logout flows         | Its own login/logout, on its own address |
| Navigation         | Sidebar, header, tabs, links to the micro-apps | Internal routes only       |
| Layout             | AppShell wrapper           | Its own shell              |
| Data collections   | Own domain collections     | Own domain collections     |
| API routes         | `/api/auth/*` (+ `/api/items/*` only for hand-written fetches) | `/api/auth/*` (+ `/api/items/*` only for hand-written fetches) |
| DaaS backend       | Shared (same Engine_URL)   | Shared (same Engine_URL)   |
| Deployment         | Independent (Amplify)      | Independent (Amplify)      |
| Testing            | Integration + E2E          | Unit + API + E2E           |
| RBAC               | Managed centrally in the Engine | Enforced by the Engine on every request |
<!-- /buildpad-backend -->

## Deployment Automation

### Automated Deploy via Git Push

After scaffolding and configuring a microapp, deploy it by pushing to git. Amplify triggers a build on push to `main`:

```bash
# Inside the micro-app directory
cd /path/to/{{serviceName}}-app

# Initialize git if not already a repo
git init
git remote add origin {{microapp.gitUrl}}

# Commit and push to trigger Amplify deployment
git add .
git commit -m "feat: initial {{serviceName}} microapp scaffold"
git push -u origin main
```

<!-- buildpad-backend: supabase -->
### Update Main App After New Microapp

When adding a new microapp, the Main App needs:
1. A new entry in `config/app-urls.ts` with the microapp's Amplify URL as default
2. An entry in `lib/services.ts` for the new service (importing from config)
3. A new page under `app/admin/{{route}}/page.tsx` with `MicroappIframe`

```bash
# Update Main App
cd /path/to/main-app

# 1. config/app-urls.ts already updated with the new microapp URL
# 2. lib/services.ts already updated with the new service entry
# 3. New page already created

# Commit and push — Amplify builds with URLs baked into codebase
git add .
git commit -m "feat: add {{serviceName}} microapp integration"
git push origin main
```

**Agent rule:** After pushing, note that Amplify deployments take 2-5 minutes. No manual Amplify console env var changes are needed — the microapp URL is baked into `config/app-urls.ts` in the codebase.

### Amplify Environment Variables

Only **infrastructure variables** (Supabase, DaaS) need to be set in the Amplify console. These are set once when the Amplify app is created:

```
NEXT_PUBLIC_SUPABASE_URL        — set once at app creation
NEXT_PUBLIC_SUPABASE_ANON_KEY   — set once at app creation
SUPABASE_SERVICE_ROLE_KEY       — set once at app creation (Main App only)
NEXT_PUBLIC_BUILDPAD_DAAS_URL   — set once at app creation
```

App URLs (Main App URL, microapp URLs) live in committed `config/app-urls.ts` — NOT as Amplify env vars.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Update Main App After New Microapp

When adding a new microapp, the Main App needs:
1. A new entry in `config/app-urls.ts` with the microapp's Amplify URL as default
2. An entry in `lib/services.ts` for the new service (importing from config), so the navigation links to it

On an Engine project the Main App gets no page that frames the microapp: framing is not available on an Engine project yet (Step 6).

```bash
# Update Main App
cd /path/to/main-app

# 1. config/app-urls.ts already updated with the new microapp URL
# 2. lib/services.ts already updated with the new service entry

# Commit and push — Amplify builds with URLs baked into codebase
git add .
git commit -m "feat: add {{serviceName}} microapp integration"
git push origin main
```

**Agent rule:** After pushing, note that Amplify deployments take 2-5 minutes. No manual Amplify console env var changes are needed — the microapp URL is baked into `config/app-urls.ts` in the codebase.

### Amplify Environment Variables

Only **infrastructure variables** need to be set in the Amplify console: the same four in the Main App and in every micro-app. These are set once when the Amplify app is created:

```
NEXT_PUBLIC_SUPABASE_URL        — the Engine_URL (project.engineUrl), set once at app creation
NEXT_PUBLIC_BUILDPAD_DAAS_URL   — the Engine_URL (project.daasUrl), set once at app creation
NEXT_PUBLIC_SUPABASE_ANON_KEY   — the fixed value (project.publicAnonKey), set once at app creation
NEXT_PUBLIC_BUILDPAD_TENANT_ID  — the tenant id (project.projectTenantId), set once at app creation
```

On an Engine project the environment is: `NEXT_PUBLIC_SUPABASE_URL=<Engine_URL>`, `NEXT_PUBLIC_BUILDPAD_DAAS_URL=<Engine_URL>`, `NEXT_PUBLIC_SUPABASE_ANON_KEY=buildpad-engine-public-anon-key` (a fixed value that is not a secret; the Engine does not read it, the Supabase client needs one), and `NEXT_PUBLIC_BUILDPAD_TENANT_ID=<the project's tenant id>`. There is no service-role key on an Engine project: add none.

App URLs (Main App URL, microapp URLs) live in committed `config/app-urls.ts` — NOT as Amplify env vars.
<!-- /buildpad-backend -->

```yaml
# amplify.yml (included in every micro-app)
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - corepack enable
        - pnpm install --frozen-lockfile
    build:
      commands:
        - pnpm build
  artifacts:
    baseDirectory: .next
    files:
      - "**/*"
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*
```

## End-to-End Automated Workflow Summary

The complete agent workflow with zero user input for URLs/credentials:

<!-- buildpad-backend: supabase -->
```
1.  get_project_detail → discover all context (URLs, credentials, microapps)
2.  Validate critical values exist (daasUrl, supabaseUrl, mainAmplifyUrl)
3.  Check if microapp already exists in context
    ├── Exists → clone gitUrl, configure, continue development
    └── New → bootstrap project
4.  Auto-generate .env.local for infrastructure vars (no placeholders)
5.  Auto-generate config/app-urls.ts with deployed URLs (committed to git)
6.  Load add-microfrontend and copy the bridge files into every app
7.  Auto-generate lib/services.ts importing from config/app-urls.ts
8.  Create domain collections in DaaS via MCP
9.  Set up RBAC for cross-domain access
10. Set up DaaSProvider in (authenticated)/layout.tsx (URL + token + getHeaders)
11. Write tests
12. git push → Amplify deploys automatically
13. Update Main App with new service integration → push → deploy
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```
1.  get_project_detail → discover all context (URLs, tenant, microapps)
2.  Validate critical values exist (engineUrl, daasUrl, projectTenantId, mainAmplifyUrl)
3.  Check if microapp already exists in context
    ├── Exists → clone gitUrl, configure, continue development
    └── New → bootstrap project
4.  Auto-generate .env.local with the same four values in every app (no placeholders)
5.  Auto-generate config/app-urls.ts with deployed URLs (committed to git)
6.  Create domain collections in the Engine via MCP
7.  Set up roles, policies and permissions for cross-domain access
8.  Set up DaaSProvider in (authenticated)/layout.tsx (URL + token + getHeaders)
9.  Write tests
10. git push → Amplify deploys automatically
11. Add the new microapp URL to the Main App's config/app-urls.ts → push → deploy
```

Framing the micro-apps in the Main App, and the session bridge, are not available on an
Engine project yet (Step 4).
<!-- /buildpad-backend -->

## Key Differences from Multi-DaaS Architecture

| Aspect                    | Single Shared DaaS (this pattern)       | Multi-DaaS (NOT this pattern)            |
| ------------------------- | --------------------------------------- | ---------------------------------------- |
| DaaS instances            | 1 shared by all                         | 1 per service                            |
| `NEXT_PUBLIC_BUILDPAD_DAAS_URL` | Same everywhere                  | Different per service                    |
| Cross-domain data access  | Direct (same DaaS, RBAC-controlled)     | API-to-API calls between services        |
| RBAC                      | Centralized (one set of roles)          | Per-service (separate role sets)          |
| Schema coordination       | Shared — coordinate changes             | Independent — no coordination needed     |
| Relations between domains | DaaS relational fields work natively    | Not possible (separate databases)        |
| Complexity                | Lower (one backend to manage)           | Higher (N backends to manage)            |

## References

- [Context discovery & auto-configuration](references/context-discovery.instructions.md)
- [Service boundary patterns](references/service-boundaries.instructions.md)
- [Cross-domain data access](references/cross-service-communication.instructions.md)
- [App URL config (`config/app-urls.ts`)](references/app-urls-config.instructions.md)
- [Deployment topology](references/deployment-topology.instructions.md)
- [add-microfrontend](../add-microfrontend/SKILL.md) — iframe composition and the auth bridge

