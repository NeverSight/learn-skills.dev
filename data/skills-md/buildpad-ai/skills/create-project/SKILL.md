---
name: create-project
description: Initialize a new Buildpad application (Next.js + Buildpad UI) on the Buildpad Engine or on Supabase. Creates the project foundation including scaffolding, authentication proxy, and test infrastructure, ready for spec-driven feature development. Use when the user wants to start a new project, create a new app, or bootstrap a DaaS application.
argument-hint: "[project name] [description]"
---

# Create DaaS Project

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

Initialize a new Data-as-a-Service application, ready for **spec-driven development**.

> **BEFORE generating ANY `.tsx` files** (pages, layouts, components), you MUST `read_file` the Buildpad component reference at `.github/skills/buildpad-reference/SKILL.md`. This loads the full 40+ component catalog with import paths and usage patterns. Skipping this step leads to raw Mantine usage violations.

## Architecture

<!-- buildpad-backend: supabase -->
DaaS apps use a **two-tier architecture**:

```
Frontend (Next.js) → DaaS Backend (DaaS-compatible API) → Supabase (PostgreSQL)
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
On an Engine project the app uses a **two-tier architecture**:

```
Frontend (Next.js) → Buildpad Engine (data API, sign-in and files, with its own database)
```

On an Engine project the data API's address is the Engine_URL, which both `NEXT_PUBLIC_BUILDPAD_DAAS_URL` and `NEXT_PUBLIC_SUPABASE_URL` hold. The Studio's address is an administration interface: send no data call to it.
<!-- /buildpad-backend -->

## Step 0: Verify Prerequisites (MANDATORY)

Before creating any project, **automatically check** that all required tools are installed:

```bash
node --version && pnpm --version && git --version && npx --version
```

| Tool    | Min Version | Install Guide                                                                                                                                     |
| ------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Node.js | v24 LTS     | https://nodejs.org/en/download — macOS: `brew install node@24`; Linux: `fnm install 24`; Windows: installer or `winget install OpenJS.NodeJS.LTS` |
| pnpm    | v10+        | https://pnpm.io/installation — `corepack enable && corepack prepare pnpm@latest --activate`                                                       |
| Git     | v2.30+      | https://git-scm.com/downloads — macOS: `xcode-select --install`; Linux: `sudo apt-get install git`; Windows: `winget install Git.Git`             |
| npx     | (bundled)   | Comes with Node.js — reinstall Node if missing                                                                                                    |

**If any tool is missing, install it before proceeding.** See [Prerequisites reference](references/prerequisites.instructions.md) for detailed installation instructions per OS.

> **Do NOT skip prerequisites.** Commands like `npx`, `pnpm dev`, and `create-next-app` will fail without them.

## Project Creation (Choose ONE approach)

### Recommended: Bootstrap (single command)

<!-- buildpad-backend: supabase -->
```bash
mkdir -p /path/to/my-project
npx @buildpad/cli@latest bootstrap --cwd /path/to/my-project
```

Bootstrap creates: Next.js skeleton + 40+ Buildpad components + installs ALL npm deps.

### Alternative: create-next-app + CLI add (empty directory only)

```bash
npx create-next-app@latest my-project --typescript --tailwind --eslint --app --src-dir=no --import-alias="@/*" --use-pnpm --turbopack
npx @buildpad/cli@latest add --all --with-api --cwd /path/to/my-project
cd /path/to/my-project && pnpm install
```

**Never mix both approaches.**
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```bash
mkdir -p /path/to/my-project
npx @buildpad/cli@latest bootstrap --cwd /path/to/my-project
```

Bootstrap creates: Next.js skeleton + 40+ Buildpad components + installs ALL npm deps.

### Alternative: create-next-app + CLI add (empty directory only)

```bash
npx create-next-app@latest my-project --typescript --tailwind --eslint --app --src-dir=no --import-alias="@/*" --use-pnpm --turbopack
npx @buildpad/cli@latest add --all --with-api --cwd /path/to/my-project
cd /path/to/my-project && pnpm install
```

**Never mix both approaches.**

On an Engine project some files the Buildpad CLI generates cannot be used yet: `lib/supabase/admin.ts`, the OAuth callback and provider routes of the `external-oauth` module, the server-side enforcer and session modules, and `lib/module-access/enforce.ts`. Do not call them; check module access by forwarding the user's token to `GET <Engine_URL>/api/permissions/me` and reading `isAdmin` and `moduleAccess`. For XAppHub sign-in the CLI installs the `external-oauth-engine` module in place of `external-oauth`; its routes are used as the `add-external-oauth` skill says.
<!-- /buildpad-backend -->

## Spec-Driven Development (MANDATORY)

This skill delivers the project **foundation**. Every feature after that follows the spec workflow (see the `spec-driven-development` skill): `requirements.md` → `design.md` → `tasks.md` in `.kiro/specs/<feature>/`, implemented task by task. In Kiro use native specs; in other IDEs use the `/buildpad-spec-*` skills.

## Foundation Deliverables

<!-- buildpad-backend: supabase -->
1. Project scaffolding (Next.js + TypeScript + Mantine v8)
2. Environment config (`.env.local` with Supabase + DaaS URLs)
3. Auth proxy routes (login, logout, user, callback) — installed by CLI
4. **`app/(authenticated)/layout.tsx`** with `DaaSProviderWrapper` + `ScopeProvider` (NOT in root layout)
5. **`DaaSProviderWrapper`** using `onAuthStateChange` (not `getSession`) + `getHeaders` wired to scope cookie
6. **Logout route** clears `daas_resource_uri` cookie
7. **DaaS CORS** configured with explicit origins + `cors_allow_credentials: true` + `X-Resource-Uri` in allowed headers
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
1. Project scaffolding (Next.js + TypeScript + Mantine v8)
2. Environment config (`.env.local` with the Engine values of "Required Environment Variables")
3. Auth proxy routes (login, logout, user) — installed by CLI. An OAuth callback route is a deliverable on an Engine project only when XAppHub sign-in is asked for: then the [add-external-oauth](../add-external-oauth/SKILL.md) skill adds it through the CLI's `external-oauth-engine` module. Sign-in with any other OAuth provider, and the Supabase client's code exchange, are not available there
4. **`app/(authenticated)/layout.tsx`** with `DaaSProviderWrapper` + `ScopeProvider` (NOT in root layout)
5. **`DaaSProviderWrapper`** using `onAuthStateChange` (not `getSession`) + `getHeaders` wired to scope cookie
6. **Logout route** clears `daas_resource_uri` cookie
7. **Cross-origin settings left as provisioned** — nothing to change (see "CORS Configuration")
<!-- /buildpad-backend -->
8. Base layout and navigation with Mantine provider
9. Test infrastructure (Playwright + Vitest)
10. README with setup instructions

## Post-Bootstrap Steps (MANDATORY — run after `bootstrap` every time)

> **Gap 9:** If the workspace had an existing `node_modules` (e.g. from `npm install`), bootstrap's internal install silently fails. Always run a clean install after bootstrap:

```bash
Remove-Item -Recurse -Force node_modules  # Windows
rm -rf node_modules                       # macOS/Linux
pnpm install
```

<!-- buildpad-backend: supabase -->
## DaaSProviderWrapper Pattern (REQUIRED)

> **Bug 19 + Bug 27:** Always use `onAuthStateChange`, NEVER `getSession` — `getSession` can return `null` before cookies are parsed, causing 401 on first mount. Also pass `token` as a sync prop AND only set `ready = true` when the token is non-null — `INITIAL_SESSION` can fire with `session = null` when the access token is expired and Supabase is performing a silent refresh.  
> **Bug 16:** Always wire `getHeaders` to forward the active scope cookie on every DaaS call.

```tsx
// components/DaaSProviderWrapper.tsx
"use client";
import { DaaSProvider } from "@/lib/buildpad/services/daas-context";
import { createClient } from "@/lib/supabase/client";
import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";

export function DaaSProviderWrapper({ children }: { children: ReactNode }) {
  const supabase = useMemo(() => createClient(), []);
  const [ready, setReady] = useState(false);
  const [tokenState, setTokenState] = useState<string | null>(null);
  const tokenRef = useRef<string | null>(null);

  useEffect(() => {
    // onAuthStateChange fires INITIAL_SESSION after cookies are fully parsed —
    // never use getSession() which can return null before cookie parsing finishes.
    // Only set ready when tok is non-null: INITIAL_SESSION can fire with null
    // session when the access token is expired and Supabase is doing a silent refresh.
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      const tok = session?.access_token ?? null;
      tokenRef.current = tok;
      setTokenState(tok);
      if (tok) setReady(true);
    });
    return () => subscription.unsubscribe();
  }, [supabase]);

  const config = useMemo(
    () => ({
      url: process.env.NEXT_PUBLIC_BUILDPAD_DAAS_URL ?? "",
      token: tokenState ?? undefined, // sync prop so DaaSProvider has token on first render
      getToken: async () => tokenRef.current,
      // Forward the active scope cookie on every DaaS call so scoped collections
      // return data for the correct tenant (required for scope-based RBAC)
      getHeaders: async () => {
        const raw = document.cookie
          .split("; ")
          .find((r) => r.startsWith("daas_resource_uri="))
          ?.split("=")[1];
        return raw ? { "X-Resource-Uri": decodeURIComponent(raw) } : {};
      },
    }),
    [tokenState],
  ); // re-create config when token refreshes

  if (!ready) return null; // block children until auth is fully initialised
  return <DaaSProvider config={config}>{children}</DaaSProvider>;
}
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## DaaSProviderWrapper Pattern (REQUIRED)

> **Bug 19 + Bug 27:** Always use `onAuthStateChange`, NEVER `getSession` — `getSession` can return `null` before cookies are parsed, causing 401 on first mount. Also pass `token` as a sync prop AND only set `ready = true` when the token is non-null — `INITIAL_SESSION` can fire with `session = null` when the access token is expired and the Supabase client is performing a silent refresh.  
> **Bug 16:** Always wire `getHeaders` to forward the active scope cookie on every DaaS call.

On an Engine project the Supabase client in this wrapper only holds and refreshes the signed-in user's session. `DaaSProvider` sends the session's access token to the Engine_URL as `Authorization: Bearer <access token>`; the Engine accepts no cookie session on its data API. A request with a session takes its tenant from the session, and `X-Resource-Uri` names the active scope inside the project's tenant.

```tsx
// components/DaaSProviderWrapper.tsx
"use client";
import { DaaSProvider } from "@/lib/buildpad/services/daas-context";
import { createClient } from "@/lib/supabase/client";
import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";

export function DaaSProviderWrapper({ children }: { children: ReactNode }) {
  const supabase = useMemo(() => createClient(), []);
  const [ready, setReady] = useState(false);
  const [tokenState, setTokenState] = useState<string | null>(null);
  const tokenRef = useRef<string | null>(null);

  useEffect(() => {
    // onAuthStateChange fires INITIAL_SESSION after cookies are fully parsed —
    // never use getSession() which can return null before cookie parsing finishes.
    // Only set ready when tok is non-null: INITIAL_SESSION can fire with null
    // session when the access token is expired and the client is doing a silent refresh.
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      const tok = session?.access_token ?? null;
      tokenRef.current = tok;
      setTokenState(tok);
      if (tok) setReady(true);
    });
    return () => subscription.unsubscribe();
  }, [supabase]);

  const config = useMemo(
    () => ({
      url: process.env.NEXT_PUBLIC_BUILDPAD_DAAS_URL ?? "", // the Engine_URL
      token: tokenState ?? undefined, // sync prop so DaaSProvider has token on first render
      getToken: async () => tokenRef.current,
      // Forward the active scope cookie on every DaaS call so scoped collections
      // return data for the active scope (required for scope-based RBAC)
      getHeaders: async () => {
        const raw = document.cookie
          .split("; ")
          .find((r) => r.startsWith("daas_resource_uri="))
          ?.split("=")[1];
        return raw ? { "X-Resource-Uri": decodeURIComponent(raw) } : {};
      },
    }),
    [tokenState],
  ); // re-create config when token refreshes

  if (!ready) return null; // block children until auth is fully initialised
  return <DaaSProvider config={config}>{children}</DaaSProvider>;
}
```
<!-- /buildpad-backend -->

**Authenticated layout structure** (Bug 22 — providers MUST NOT be in root layout):

```tsx
// app/(authenticated)/layout.tsx
import { DaaSProviderWrapper } from "@/components/DaaSProviderWrapper";
import { ScopeProvider } from "@/lib/contexts/ScopeContext";

export default function AuthenticatedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <DaaSProviderWrapper>
      <ScopeProvider>{children}</ScopeProvider>
    </DaaSProviderWrapper>
  );
}
```

<!-- buildpad-backend: supabase -->
## CORS Configuration (MANDATORY after project creation)

> **Bug 25 + Bug 17:** The DaaS default `cors_origins: ["*"]` + Buildpad's `credentials: 'include'` = every browser request blocked. Also `X-Resource-Uri` is not in the default allowed headers and must be added.

Run **immediately after project creation**, before wiring any frontend:

```json
// mcp_daas_cors-settings — action: update
{
  "cors_origins": [
    "http://localhost:3000",
    "http://localhost:3001",
    "<mainAmplifyUrl from get_project_detail>"
  ],
  "cors_allow_credentials": true,
  "cors_allowed_headers": [
    "Content-Type",
    "Authorization",
    "Origin",
    "X-Requested-With",
    "Accept",
    "X-Resource-Uri"
  ],
  "cors_max_age": 0
}
```

Never leave `cors_origins: ["*"]` in place — the browser will block every API call.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## CORS Configuration (nothing to change)

On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere.

There is no cross-origin step after project creation: the Engine's MCP tools hold no cross-origin setting, and the Studio's is left as it is. Send the user's access token as `Authorization: Bearer <access token>`, never a cookie session.
<!-- /buildpad-backend -->

## Buildpad-First Component Rule (MANDATORY — applies to ALL code generated during and after foundation setup)

**EVERY form, input, list, and filter component MUST use Buildpad.** The CLI bootstrap installs 40+ components — use them. Never fall back to raw Mantine form/input components.

| ❌ NEVER Use Directly                                   | ✅ ALWAYS Use Buildpad Instead                        |
| ------------------------------------------------------- | ----------------------------------------------------- |
| `<TextInput>` / `<Textarea>` from @mantine/core         | `Input`, `Textarea` from `@/components/ui`            |
| `<Select>` from @mantine/core                           | `SelectDropdown` from `@/components/ui`               |
| `<DatePicker>` / `<DateTimePicker>` from @mantine/dates | `DateTime` from `@/components/ui`                     |
| `<Switch>` / `<Checkbox>` from @mantine/core            | `Toggle`, `Boolean`, `SelectMultipleCheckbox`         |
| `<Dropzone>` from @mantine/dropzone                     | `Upload`, `Files`, `FileImage` from `@/components/ui` |
| `useForm` from @mantine/form                            | `VForm` or `CollectionForm` from `@/components/ui`    |
| Custom `<Table>` for collection data                    | `CollectionList` from `@/components/ui`               |
| Custom filter builder                                   | `FilterPanel` from `@/components/ui`                  |
| `<NumberInput>` from @mantine/core                      | `Input` (with type="number") from `@/components/ui`   |
| `<ColorInput>` from @mantine/core                       | `Color` from `@/components/ui`                        |

**Allowed raw Mantine**: `Stack`, `Group`, `Button`, `Modal`, `Table` (for non-collection data), `Tabs`, `Paper`, `Text`, `Title`, `Badge`, `ActionIcon`, `Menu`, `Loader`, `Alert`.

**When generating ANY `.tsx` file** (pages, components, forms, lists), check this table first. If the UI element has a Buildpad equivalent, you MUST use it.

### Quick Reference: Common Patterns

```tsx
// ✅ List page → CollectionList (NEVER custom table)
import { CollectionList } from "@/components/ui";
<CollectionList
  collection="tasks"
  enableSearch
  enableFilter
  enableCreate
  enableDelete
/>;

// ✅ Form page → CollectionForm (NEVER useForm)
import { CollectionForm } from "@/components/ui/collection-form";
<CollectionForm
  collection="tasks"
  onSuccess={(item) => router.push(`/tasks/${item.id}`)}
/>;

// ✅ Individual field → Buildpad component (NEVER raw Mantine input)
import { Input } from "@/components/ui/input";
import { SelectDropdown } from "@/components/ui/select-dropdown";
import { DateTime } from "@/components/ui/datetime";
import { Toggle } from "@/components/ui/toggle";
```

## Post-Generation Validation (MANDATORY)

After generating ANY `.tsx` files, run this check to catch Buildpad-First violations:

```bash
# Scan for forbidden raw Mantine form/input imports
grep -rn "from '@mantine/form'\|from '@mantine/dates'\|from '@mantine/dropzone'\|<TextInput\|<NumberInput\|<Select \|<Switch \|<Checkbox \|<DatePicker\|<Dropzone" app/ components/ 2>/dev/null
```

If any matches are found, **replace them with Buildpad equivalents before proceeding**.

## Critical Rules

- **Buildpad-First**: All UI components come from Buildpad CLI — never create custom Input, Select, DateTime, Toggle, File upload, or Relations
<!-- buildpad-backend: supabase -->
- **Auth via Proxy**: Login MUST call `/api/auth/login`, NEVER `supabase.auth.signInWithPassword()` directly
- **No Direct DaaS Calls from Browser**: All API calls go through Next.js API routes
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- **Auth via Proxy**: Login MUST call `/api/auth/login`, NEVER `supabase.auth.signInWithPassword()` directly. On an Engine project that server route names the tenant: it sends `X-Tenant-Id` with the value of `NEXT_PUBLIC_BUILDPAD_TENANT_ID`
- **Supabase client for sign-in only**: On an Engine project the Supabase client is kept for sign-in only. Password sign-in, session refresh, reading the signed-in user and sign-out work through it, and its default sign-out ends the user's sessions on every device. An account that holds no role in the project's tenant is refused at password sign-in. XAppHub sign-in also works through it while the project's XAppHub connector is connected: the application's server gives the ID token from XAppHub to `signInWithIdToken` with the provider `my-apps`, and ends the session of an account that holds no role yet (the `add-external-oauth` skill). Not available on an Engine project: sign-up; OAuth sign-in with any provider other than XAppHub; magic link and one-time code; password recovery; changing a password, an email or a profile through the Supabase client; the Supabase client's code exchange; and the Supabase administration API. The Platform's password-less handoff opens the Studio; it is not a way for an application to sign a user in.
- **User token on every data call**: On an Engine project every data call carries the signed-in user's access token as `Authorization: Bearer <access token>`, from the application's own server route or from the SDK. The Engine accepts no cookie session on its data API. The token in the project's MCP configuration is accepted only on the MCP endpoint `/api/mcp`: never send it, or any other administrator token, to the data API.
<!-- /buildpad-backend -->
- **NEVER create files manually** in `components/ui/` or `lib/buildpad/` — CLI only
- **DaaSProvider in authenticated layout only**: NEVER place `DaaSProviderWrapper` or `ScopeProvider` in the root `app/layout.tsx`. Always place them in `app/(authenticated)/layout.tsx` so they fully unmount on logout and remount fresh on next login (Bug 22)
- **Mantine components require `'use client'`**: ANY page or component that renders Mantine must have `'use client'` — Mantine compound components (`Table.Tbody`, `Modal`, `Tabs.Panel`) are `undefined` in React Server Components (Bug 10)

<!-- buildpad-backend: supabase -->
## Required Environment Variables

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_BUILDPAD_DAAS_URL=http://localhost:3000
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Required Environment Variables

On an Engine project the environment is: `NEXT_PUBLIC_SUPABASE_URL=<Engine_URL>`, `NEXT_PUBLIC_BUILDPAD_DAAS_URL=<Engine_URL>`, `NEXT_PUBLIC_SUPABASE_ANON_KEY=buildpad-engine-public-anon-key` (a fixed value that is not a secret; the Engine does not read it, the Supabase client needs one), and `NEXT_PUBLIC_BUILDPAD_TENANT_ID=<the project's tenant id>`. There is no service-role key on an Engine project: add none.

```env
NEXT_PUBLIC_SUPABASE_URL=<Engine_URL>
NEXT_PUBLIC_BUILDPAD_DAAS_URL=<Engine_URL>
NEXT_PUBLIC_SUPABASE_ANON_KEY=buildpad-engine-public-anon-key
NEXT_PUBLIC_BUILDPAD_TENANT_ID=<the project's tenant id>
```

Use the project's own Engine_URL and tenant id; if you do not have them, ask the developer. A local Engine runs on port 8080, so its Engine_URL is `http://localhost:8080`.
<!-- /buildpad-backend -->

## After the Foundation

Start the first feature spec: `/buildpad-discovery "<idea>"` or `/buildpad-spec-init "<feature description>"` (in Kiro, create a spec from the Specs panel).

## References

- [Prerequisites check](references/prerequisites.instructions.md)
- [Project creation details](references/project-creation.instructions.md)
- [Environment setup](references/environment.instructions.md)
