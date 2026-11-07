---
name: add-i18n
description: Add internationalization to a Buildpad app the way the Next.js App Router guide prescribes — locale-prefixed routes (app/[lang]), Accept-Language negotiation inside the existing auth middleware, server-loaded dictionaries handed to client pages through an I18nProvider, a LanguageSwitcher built on SelectDropdown, DaaS field-label translations via VForm's locale prop, and Directus-style content translations (a languages collection plus <collection>_translations junctions with optional per-locale workflow). Use when the user says add i18n, internationalization, internationalisation, localization, translations, multilingual, multi-language, bilingual, locale, language switcher, RTL, or wants content or UI in more than one language.
argument-hint: "[locales e.g. en id ar] [--default en] [--cwd path/to/project]"
---

# Add Internationalization

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

Internationalization in a Buildpad app is **two layers keyed by one locale**:

| Layer | What it translates | Where it lives | Who edits it |
| --- | --- | --- | --- |
| **UI strings** | App chrome: navigation, buttons, login form, empty states, validation | `lib/i18n/dictionaries/<locale>.json` in the repo | Developers, at build time |
| **Content** | Records editors author: article titles, product descriptions | DaaS: a `languages` collection + one `<collection>_translations` junction per translated collection | Editors, in the app / DaaS admin |

The `[lang]` route segment is the single source of truth for both. Middleware negotiates it once, the root layout loads the dictionary for it, pages query DaaS content for it. A third, smaller layer — **DaaS field and collection display names** — already exists (`daas_fields.translations`) and only needs the `[lang]` value threaded into `VForm`'s `locale` prop.

> **Read [buildpad-reference](../buildpad-reference/SKILL.md) before generating any `.tsx`.** The LanguageSwitcher and every translated page must use Buildpad components — no raw Mantine.

## CRITICAL Rules

1. **Never edit strings inside `components/ui/*`.** Those files are Copy & Own; every edited file diverges its checksum and turns the next `buildpad upgrade` into a manual merge. Pass the overrides the components already accept (`translations` on `ListM2M`, `loadingText`/`noItemsText` on `VTable`, `locale` on `VForm`) and record the remaining English chrome as a known gap (see [Known Limits](#known-limits)).
2. **Never put content in dictionaries or UI strings in DaaS.** Dictionaries ship with the app; content lives in translation rows. Mixing them breaks both editing and deployment.
3. **One locale list.** `lib/i18n/config.ts` is the only place locale codes are declared. The `languages.code` values in DaaS **must match it exactly** (`id` ≠ `id-ID`) or content queries silently return nothing.
4. **Never use `special: ["translations"]` on DaaS today.** The read path understands it, but the item writer has no nested-write branch for it, so translation rows submitted through the parent form are silently dropped. Use `special: ["o2m"]` — [content-translations reference](references/content-translations.instructions.md) explains the recipe and why.
5. **`/api/*` is never locale-prefixed.** Every fetch layer in a Buildpad app uses absolute `/api` paths; leave them alone.
6. **Locale negotiation happens only in middleware.** Reading `headers()` or `cookies()` inside a page or layout to detect locale forces dynamic rendering and duplicates the redirect logic.
7. **`I18nProvider` goes in the root `app/[lang]/layout.tsx`** — it holds only the static dictionary and locale, so the Bug 22 rule (no auth-bearing providers in the root layout) does not apply. `DaaSProviderWrapper` stays in `app/[lang]/(authenticated)/layout.tsx`.

## Prerequisites Check

```bash
node --version && pnpm --version && npx --version
ls buildpad.json middleware.ts proxy.ts app/layout.tsx 2>/dev/null
ls -d app/\[lang\] 2>/dev/null && echo "ALREADY LOCALE-PREFIXED"
```

- Requires Node.js v24 LTS and pnpm v10+ (see [add-buildpad](../add-buildpad/SKILL.md)).
<!-- buildpad-backend: supabase -->
- The app must be CLI-scaffolded (`buildpad.json` present) with the Supabase middleware installed (`lib/supabase/middleware.ts`). Next.js 16 apps may name the root middleware `proxy.ts` instead of `middleware.ts` — the same changes apply to whichever file exists.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- The app must be CLI-scaffolded (`buildpad.json` present) with the session middleware installed (`lib/supabase/middleware.ts`). On an Engine project the Supabase client in that file keeps the user's Engine sign-in session fresh and reads no data. Next.js 16 apps may name the root middleware `proxy.ts` instead of `middleware.ts` — the same changes apply to whichever file exists.
<!-- /buildpad-backend -->
- **Decide the shape first.** If `app/[lang]/` already exists (apps generated by a CLI that ships locale routing by default), skip Step 2 and Step 3's restructure and only add locales, dictionaries, and content translations. Otherwise this is a **retrofit**: it edits CLI-owned files (`middleware.ts`, `lib/supabase/middleware.ts`, `app/layout.tsx`, every page under `app/`), each of which will show as modified on `buildpad status`. Tell the user this before starting.
<!-- buildpad-backend: supabase -->
- DaaS MCP tools (`schema`, `collections`, `fields`, `items`, `permissions`) must be reachable for the content layer — see [daas-platform](../daas-platform/SKILL.md).
- DaaS CORS must use explicit origins (the LanguageSwitcher persists the choice with a credentialed call).
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- The Engine's MCP tools (`schema`, `collections`, `fields`, `items`, `permissions`) must be reachable for the content layer, and so must the Engine's API with an administrator's session, for the settings the MCP tools do not keep (Step 7) — see [daas-platform](../daas-platform/SKILL.md).
- On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere.
<!-- /buildpad-backend -->

```bash
pnpm add negotiator @formatjs/intl-localematcher server-only
pnpm add -D @types/negotiator
```

## Decision Tree

<!-- buildpad-backend: supabase -->
```
What does the user need?
├── UI in several languages                → Steps 1–6 (always)
├── Editors author content per language    → + Step 7 (content translations)
│     ├── Publish each language separately → + Group B on the junction (Step 7c)
│     └── One lifecycle for all languages  → Group B stays on the parent only
├── Tenant-specific locales (multitenancy) → + Group C on junctions (Step 7d)
└── Main app + micro-apps                  → + Step 8 (locale propagation)
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
```
What does the user need?
├── UI in several languages                → Steps 1–6 (always)
├── Editors author content per language    → + Step 7 (content translations)
│     ├── Publish each language separately → + Group B on the junction (Step 7c)
│     └── One lifecycle for all languages  → Group B stays on the parent only
├── Locales per scope (below the tenant)   → + Group C on junctions (Step 7d)
└── Main app + micro-apps                  → + Step 8 (locale propagation)
```
<!-- /buildpad-backend -->

## Step 1 — Locale config

Create `lib/i18n/config.ts` from the [locale-routing reference](references/locale-routing.instructions.md#1-locale-config). It exports `locales`, `defaultLocale`, `localeMeta` (display name + `ltr`/`rtl`), `LOCALE_COOKIE`, and the helpers `hasLocale`, `getLocaleFromPathname`, `stripLocale`, `localeHref`. Everything else imports from here.

## Step 2 — Middleware

Two files change; both are in the reference:

<!-- buildpad-backend: supabase -->
- **`middleware.ts` (or `proxy.ts`)** — before calling `updateSession`, redirect any non-`/api` request whose first segment is not a locale to `/<negotiated-locale>/<path>`, preserving the query string and using `publicOrigin(request)` for the absolute `Location`. Negotiation order: `NEXT_LOCALE` cookie → `Accept-Language` (Negotiator + `@formatjs/intl-localematcher`) → `defaultLocale`. The redirect returns **before** the Supabase client is created, so no refreshed session cookie is lost.
- **`lib/supabase/middleware.ts`** — compare `publicRoutes` against `stripLocale(pathname)` and redirect unauthenticated users to `/<locale>/login` instead of `/login`. Without this every locale-prefixed request bounces to an unprefixed `/login` that no longer exists.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- **`middleware.ts` (or `proxy.ts`)** — before calling `updateSession`, redirect any non-`/api` request whose first segment is not a locale to `/<negotiated-locale>/<path>`, preserving the query string and using `publicOrigin(request)` for the absolute `Location`. Negotiation order: `NEXT_LOCALE` cookie → `Accept-Language` (Negotiator + `@formatjs/intl-localematcher`) → `defaultLocale`. The redirect returns **before** the session client is created, so no refreshed session cookie is lost.
- **`lib/supabase/middleware.ts`** — compare `publicRoutes` against `stripLocale(pathname)` and redirect unauthenticated users to `/<locale>/login` instead of `/login`. On an Engine project the public routes are `/login` and `/api/auth` only, and `/auth/pending-access` when XAppHub sign-in is installed: there is no sign-up page, and XAppHub sign-in's callback, the only OAuth callback route there, lies under `/api/auth`. Without this every locale-prefixed request bounces to an unprefixed `/login` that no longer exists.
<!-- /buildpad-backend -->

## Step 3 — Route tree

Move every page and layout under `app/[lang]/`; leave `app/api/**`, `app/globals.css`, `app/design-tokens.css`, and `public/` where they are. The [retrofit map](references/locale-routing.instructions.md#3-route-tree-retrofit-map) lists every CLI-scaffolded target and its new location.

`app/[lang]/layout.tsx` becomes the root layout (there must be no `app/layout.tsx` left behind). It is the **only server component in a Buildpad app** — every scaffolded page is `'use client'` — so it is where `generateStaticParams()`, `notFound()` for unknown locales, `<html lang={lang} dir={direction}>`, Mantine's `DirectionProvider`, and `<I18nProvider>` all live.

## Step 4 — Dictionaries and provider

```
lib/i18n/
├── config.ts            # Step 1
├── negotiate.ts         # Step 2
├── types.ts             # Dictionary = typeof en.json
├── dictionaries.ts      # getDictionary(locale) — import 'server-only'
├── dictionaries/
│   ├── en.json          # { "app": {...}, "buildpad": {...} }
│   └── id.json
├── provider.tsx         # 'use client' — I18nProvider, useI18n(), t(), formatDate(), formatNumber()
├── navigation.ts        # useLocaleRouter(), useSwitchLocale()
└── content.ts           # Step 7 — translation query helpers
```

The Next.js guide keeps dictionaries in Server Components. Buildpad pages are client components, so the layout loads the dictionary on the server and hands it to `I18nProvider`; pages call `useI18n()`. The dictionary therefore ships to the client — acceptable for an authenticated admin app; keep dictionaries to UI strings only so they stay small.

Dictionary shape — two namespaces:

- `app.*` — your pages (`app.login.submit`, `app.nav.content`, …).
- `buildpad.*` — what the Buildpad components can accept today: `buildpad.listM2M` is passed straight into `ListM2M`'s `translations` prop (same `{placeholder}` interpolation convention), `buildpad.table.loading` / `buildpad.table.noItems` into `VTable`.

Every locale file must have the same keys; `types.ts` derives `Dictionary` from `en.json`, so a missing key in `id.json` is a type error in `dictionaries.ts`.

## Step 5 — Locale-aware navigation

Replace every hardcoded route literal with `useLocaleRouter()` (drop-in for `useRouter()` whose `push`/`replace` prefix the locale) or `localeHref(locale, path)` for `<Link href>`. Scaffolded offenders, all of which the retrofit must touch:

| File | Literal | Replacement |
| --- | --- | --- |
| `app/[lang]/login/page.tsx` | `router.push('/')` after sign-in | `router.push('/')` via `useLocaleRouter()` |
| `components/layout/AuthenticatedShell.tsx` | `DEFAULT_NAV_ITEMS` hrefs, active-item matching on `pathname` | `localeHref(locale, item.href)`; match on `stripLocale(pathname)` |
| `app/[lang]/content/layout.tsx` | ``router.push(`/content/${collection}`)`` | `useLocaleRouter().push(...)` |
| every `app/[lang]/**/page.tsx` | `router.push('/users/...')`, `/roles/...`, `/content/...` | `useLocaleRouter()` |
| `window.location.href = "/api/auth/logout"` | — | unchanged (API path) |

`isModuleActive`-style `pathname.startsWith('/content')` checks must compare against `stripLocale(pathname)`.

## Step 6 — LanguageSwitcher

<!-- buildpad-backend: supabase -->
`components/LanguageSwitcher.tsx` is a `SelectDropdown` (`choices` from `localeMeta`, `allowNone={false}`) whose `onChange` calls `useSwitchLocale()`. That hook writes the `NEXT_LOCALE` cookie the middleware reads and pushes the same route under the new prefix. Optionally persist the choice to the user's DaaS profile: DaaS lets a user `PATCH /api/users/me` with `language` (the column exists, default `en-US`), so mirror the direct-DaaS call pattern from `lib/buildpad/hooks/useUsers.ts`. Mount the switcher in the `AuthenticatedShell` header (pass it through a `'use client'` wrapper, as the shell's docs describe for `navItems`) and on the login page.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
`components/LanguageSwitcher.tsx` is a `SelectDropdown` (`choices` from `localeMeta`, `allowNone={false}`) whose `onChange` calls `useSwitchLocale()`. That hook writes the `NEXT_LOCALE` cookie the middleware reads and pushes the same route under the new prefix. Optionally persist the choice to the user's Engine profile: the Engine lets a user `PATCH /api/users/me` with `language`. Send that call with the signed-in user's access token as `Authorization: Bearer <access token>`, from the app's own server route or through the SDK; the Engine accepts no cookie session on its data API. Mount the switcher in the `AuthenticatedShell` header (pass it through a `'use client'` wrapper, as the shell's docs describe for `navItems`) and on the login page.
<!-- /buildpad-backend -->

## Step 7 — Content translations (optional)

<!-- buildpad-backend: supabase -->
Full payloads and SQL mirrors are in the [content-translations reference](references/content-translations.instructions.md). The recipe, per translated collection:

- **7a. `languages` collection** (once per project): `code` (unique, = `lib/i18n/config.ts`), `name`, `direction`, `sort`, plus Group A audit fields. Seed one row per locale via the `items` tool. Not scoped — languages are global.
- **7b. `<collection>_translations` junction**: the translatable fields moved off the parent, Group A audit fields, then two M2O fields created with the `fields` tool — `<collection>_id` with `options.corresponding_field: "translations"` (DaaS auto-creates the `translations` alias on the parent as `interface: list-o2m`, `special: ["o2m"]`, and sets `one_field`) and `languages_code` with `options.related_field: "code"`. Mirror both tables in a Supabase migration, including `UNIQUE (<collection>_id, languages_code)`, which the MCP schema cannot express.
- **7c. Per-locale publish**: add Group B (`workflow_instance`, `workflow_state`) to the **junction** and create a `daas_wf_assignment` for the junction collection. The workflow engine keys instances by `(collection, item_id)`, so every translation row gets its own lifecycle with no DaaS changes. Group B on the parent alone would publish every language at once. Then follow [create-workflow](../create-workflow/SKILL.md).
- **7d. Scope**: if the parent carries `resource_uri`, the junction must too (Group C), then [manage-scope](../manage-scope/SKILL.md).
- **7e. Permissions**: RLS is applied automatically when the collections are created, but policy permissions are not. Grant `read` on `languages` and the junction to the app policy, and `create`/`update`/`delete` on the junction to editor policies; nested writes through `parent.translations` are enforced on the junction, so finish with [relational-permissions](../relational-permissions/SKILL.md).
- **7f. Queries**: DaaS parses Directus's `deep` parameter but the items service ignores it, so you cannot ask for "the article with only its `id` translation". Query the junction directly — `filter={"<collection>_id":{"_eq":id},"languages_code":{"_in":[lang, defaultLang]}}` — and pick with `pickTranslation()` from `lib/i18n/content.ts`, which falls back to the default locale. The backend never falls back for you.
- **7g. Field labels**: set `meta.translations: [{ "language": "id", "translation": "Judul" }]` on fields via the `fields` tool and pass `locale` to `VForm`.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Full payloads are in the [content-translations reference](references/content-translations.instructions.md). On an Engine project there is no SQL file: the Engine's API is the only place the structure is defined. The recipe, per translated collection:

- **7a. `languages` collection** (once per project): `code` (unique, = `lib/i18n/config.ts`), `name`, `direction`, `sort`, plus Group A audit fields. Create it with `POST /api/collections` and its fields inline, with an administrator's session, so that `is_unique` and the defaults are kept; then seed one row per locale via the `items` tool. Not scoped — languages are global.
- **7b. `<collection>_translations` junction**: the translatable fields moved off the parent and Group A audit fields, created the same way; then two M2O fields created with the `fields` tool — `<collection>_id` with `options.corresponding_field: "translations"` (the Engine creates the `translations` alias on the parent, `special: ["o2m"]`, and sets `one_field`) and `languages_code` with `options.related_field: "code"`. The unique pair `(<collection>_id, languages_code)` goes through the Engine's schema migration routes (`GET /api/schema/snapshot`, `POST /api/schema/diff`, `POST /api/schema/apply`). There is no SQL file.
- **7c. Per-locale publish**: add Group B (`workflow_instance`, `workflow_state`) to the **junction** and create a workflow assignment for the junction collection (`POST /api/workflow-assignments`). The workflow engine keys instances by `(collection, item_id)`, so every translation row gets its own lifecycle. Group B on the parent alone would publish every language at once. Then follow [create-workflow](../create-workflow/SKILL.md).
- **7d. Scope**: if the parent carries `resource_uri`, the junction must too (Group C), then [manage-scope](../manage-scope/SKILL.md). On an Engine project the project is one tenant. Every scope hierarchy begins below the project's tenant node: create no scope type without a parent and no scope item without a parent. Scope types, items and collection settings are managed through `/api/scope/types`, `/api/scope/items` and `/api/scope/collection-config` with an administrator's session; the MCP `scope` tool, served to an administrator only, assigns a role to a user at a scope (`assign_user_role`) and registers a collection as tenanted (`create_config`, the body of `POST /api/scope/collection-config`).
- **7e. Permissions**: on an Engine project nothing is granted when a collection is created. Grant `read` on `languages` and the junction to the app policy, and `create`/`update`/`delete` on the junction to editor policies; nested writes through `parent.translations` are checked on the junction as if the user wrote its rows directly, so finish with [relational-permissions](../relational-permissions/SKILL.md).
- **7f. Queries**: the Engine ignores Directus's `deep` parameter, so you cannot ask for "the article with only its `id` translation". Query the junction directly — `filter={"<collection>_id":{"_eq":id},"languages_code":{"_in":[lang, defaultLang]}}` — and pick with `pickTranslation()` from `lib/i18n/content.ts`, which falls back to the default locale. The backend never falls back for you.
- **7g. Field labels**: set `meta.translations: [{ "language": "id", "translation": "Judul" }]` on fields via the `fields` tool and pass `locale` to `VForm`.

On an Engine project collections, fields, relations, roles, policies and permissions are created through the Engine's API (`/api/collections`, `/api/fields/:collection`, `/api/relations`, `/api/roles`, `/api/policies`, `/api/access`, `/api/permissions`) or its MCP tools `collections`, `fields`, `relations`, `roles`, `policies`, `access` and `permissions`. Access is roles, policies and permissions: a permission belongs to a policy, and a policy is attached to a role or a user. The MCP `collections` and `fields` tools keep a field's name, type and `meta` but not its `schema` block (default, not-null, length): set those through `POST /api/fields/:collection` with an administrator's session.
<!-- /buildpad-backend -->

> Verify every field name with `mcp_daas_schema` before writing a filter. A wrong name in `filter` or `sort` is a silent 500.

## Step 8 — Micro-apps (if [add-microapp](../add-microapp/SKILL.md) or [add-microfrontend](../add-microfrontend/SKILL.md) is in use)

Host-to-iframe state travels only through query params (`allowedParams`) and the one host-to-child message `SET_AUTH`; path segments are never synced. Run this skill in **each** micro-app, then in the host interpolate the locale into the iframe `path` (``path={`/${locale}/users`}``) — a locale switch reloads the iframe, which is acceptable. For live switching add a `SET_LOCALE` message modeled on `SET_AUTH`. The micro-app's auth-bridge redirect (`window.location.href = '/content'`) must become locale-aware. Details in the [locale-routing reference](references/locale-routing.instructions.md#8-micro-app-locale-propagation).

## Testing Requirements

Playwright (`tests/e2e/i18n.spec.ts`, `tests/api/translations.spec.ts`), all of which must pass:

- `/` and `/login` redirect to `/<locale>/...` chosen from `Accept-Language` (`browser.newContext({ locale: 'id-ID' })`), preserving the query string.
- A `NEXT_LOCALE` cookie wins over `Accept-Language`.
- `/xx/login` returns 404; `/api/items/...` is never redirected.
- Unauthenticated `/id/content` redirects to `/id/login` (locale preserved).
- The switcher navigates from `/en/content/articles?page=2` to `/id/content/articles?page=2` and sets the cookie.
- `<html lang>` and `dir` match the route; page chrome renders the locale's dictionary strings.
- Content: a translation row per language is created through the parent's `translations` field and read back; the fallback returns the default locale when a translation is missing; per-locale `workflow_state` transitions do not affect sibling locales.

## Post-Generation Validation (MANDATORY)

```bash
# 1. Buildpad-First: no raw Mantine in generated pages/components
grep -rn "from '@mantine/form'\|from '@mantine/dates'\|<TextInput\|<NumberInput\|<Select \|<Switch \|<Checkbox \|<DatePicker\|<Dropzone" app/ components/ 2>/dev/null

# 2. Locale-unaware navigation (must go through useLocaleRouter / localeHref)
grep -rn "router\.\(push\|replace\)(['\"\`]/\|href=['\"]/" app/ components/ --include=*.tsx | grep -v "/api/"

# 3. Hardcoded language / locale-less formatting
grep -rn 'lang="en"' app/
grep -rn "toLocaleDateString()\|toLocaleString()\|toLocaleTimeString()\|Intl\.\(DateTimeFormat\|NumberFormat\)('en" app/ components/ lib/ --include=*.ts --include=*.tsx | grep -v components/ui/

# 4. Dictionary parity + build
pnpm tsc --noEmit && pnpm build
npx @buildpad/cli@latest status --cwd /path/to/project
```

Matches in checks 1–3 must be fixed before the work is complete (hits inside `components/ui/*` are expected — see Known Limits). `buildpad status` will list the CLI-owned files this retrofit modified; report that list to the user.

## Known Limits

- **Component chrome stays English until Buildpad UI ships an i18n provider.** `CollectionList`, `CollectionForm`, `FileManager`, `UsersManager`, `Upload`, and most interfaces have hardcoded strings with no override props. Do not patch them; log the gap. (Tracked as Phase 2 of the Buildpad UI i18n plan.)
- **Dates and numbers inside `components/ui/*`** use the browser locale, not the URL locale. Use `formatDate`/`formatNumber` from `useI18n()` in your own code.
- **RTL**: setting `dir` on `<html>` and Mantine's `DirectionProvider` is the extent of support; component CSS is not RTL-audited. Do not add an RTL locale to `languages` unless the user accepts this.
- **Not in scope**: translating the DaaS admin app itself, form-builder definitions authored at runtime, email templates (DaaS mail is a raw transport — callers own the copy), `hreflang`/localized sitemaps for the authenticated tree (only public pages such as `/[lang]/login` benefit; add `alternates.languages` there if the user wants it).
- **DaaS gaps that a skill cannot fix**: no `deep` filter on nested reads, no `translations` interface or junction wizard in the admin. The `o2m` recipe is the supported path until DaaS implements the Directus `translations` field type end to end.

## Related

- [add-buildpad](../add-buildpad/SKILL.md) — the CLI and the Copy & Own rules this skill must respect.
- [create-collection](../create-collection/SKILL.md) — Group A/B/C field groups reused by the translation junctions.
- [create-workflow](../create-workflow/SKILL.md) — per-locale publish lifecycles.
- [relational-permissions](../relational-permissions/SKILL.md) — permissions on the translation junctions.
- [manage-scope](../manage-scope/SKILL.md) — multi-tenant locales.
- [add-microapp](../add-microapp/SKILL.md) / [add-microfrontend](../add-microfrontend/SKILL.md) — locale propagation across iframes.
- [buildpad-reference](../buildpad-reference/SKILL.md) — component catalog.

## References

- [Locale routing](references/locale-routing.instructions.md) — config, middleware, `[lang]` layout, dictionaries, provider, navigation, switcher, micro-apps.
- [Content translations](references/content-translations.instructions.md) — `languages` + junction MCP payloads, SQL mirrors, permissions, queries, per-locale workflow.
- [DaaS MCP tools](../daas-platform/references/daas-mcp-tools.instructions.md) — exact tool payload formats.
