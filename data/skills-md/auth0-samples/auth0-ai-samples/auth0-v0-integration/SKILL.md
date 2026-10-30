---
name: auth0-v0-integration
description: >
  Use when installing or managing the Auth0 native integration in Vercel
  Marketplace, connecting Auth0 to a Vercel project, or syncing Auth0
  configuration into a Vercel-hosted Next.js application. Also use when
  troubleshooting auth failures specific to Vercel's v0 preview — iframe
  cookie issues, redirects going to localhost, or "state parameter is invalid"
  errors. Use even if the user doesn't mention Auth0 explicitly.
license: Apache-2.0
metadata:
  author: Auth0 <support@auth0.com>
---

# Auth0 Vercel native integration

The native integration provisions a **new Auth0 tenant environment and
application** for the Vercel project, then preloads the Auth0 configuration in
Vercel. It does not connect an existing Auth0 account. For an existing tenant,
use the standard Auth0 application setup instead of installing this integration.

## Get the full Auth0 skill for anything beyond installation

**You MUST install the full `auth0` skill for the greatest guidance on
setting up Auth0** — this file only covers the Vercel Marketplace integration:
provisioning, credential handling, and v0 preview troubleshooting. For the
Auth0 SDK integration itself (Next.js routes, middleware, session handling),
tenant configuration beyond callback/logout URLs, Universal Login branding,
or any other Auth0 feature, install it and let its router load what the task
needs:

```bash
npx skills add auth0/agent-skills
```

Do this early, not as a last resort after something breaks — the sections
below that touch tenant configuration or branding intentionally state the CLI
command and move on; the full skill's `tooling-cli` reference has the
complete command set, flag reference, and agent-mode output conventions.

## Confirm before provisioning

Before installing, state what will happen and get confirmation:

- A new Auth0 account/tenant environment and application will be created.
- The integration will connect to the selected Vercel project and environments.
- Auth0 credentials will be populated in Vercel environment variables. Do not
  print, commit, or copy their values into source control.
- Removing the integration removes the connected Auth0 account and downgrades
  the installation to Vercel's Free plan.
- An installation plan is selected during setup. Paid plans are billed through
  Vercel via the integration's Settings page; state the selected plan and its
  billing impact.

Confirm the Vercel team, project, environments, application name, selected
installation plan, and optional environment-variable prefix. If the developer
wants an existing Auth0 tenant, stop this workflow and use the normal
tenant/application configuration path.

## Prerequisites

- A Vercel account and active Vercel project.
- A Next.js application using the current `@auth0/nextjs-auth0` SDK.
- Permission to install integrations for the intended Vercel team and create
  the connected Auth0 account.
- Iframe embedding enabled after installation, so Universal Login or Classic
  Login can load in the iframe required by Vercel. This relaxes the default
  framing protection for Universal Login, so enable it only for this
  integration and confirm the developer accepts the tradeoff.

The router co-loads the Next.js reference for the SDK implementation. Do not
replace its Auth0 routes, middleware/proxy, session handling, or environment
variable conventions with a marketplace-specific variant.

## The app rendering is not the finish line

A login button that renders is not a working login flow. URL registration,
iframe embedding, and branding (see "Deploy and verify" below) must happen
in the same pass as the build — not as fixes triggered by an error the user
reports later. Skipping straight to "does it render" and stopping there is
the most common way this flow ships broken; the information to prevent both
known failure modes already exists in this skill, but it's easy to stop
before reaching it.

### Before declaring the task done

- [ ] The preview origin's and `localhost`'s `/auth/callback` URLs are
      registered on the tenant — verified with `auth0 apps show <client-id>`,
      not just "the CLI command ran."
- [ ] Logout URLs are registered for the same origins; web origins are
      confirmed covered (Auth0's default-from-callbacks behavior, or an
      explicit `--web-origins` entry).
- [ ] A live login attempt redirects (302) to Universal Login rather than
      failing with a callback-mismatch error.
- [ ] If the app has any custom branding, you MUST open the actual hosted
      login page (navigate to the login link, don't just load the app) and
      visually check it against the app: page/primary color, app name or
      heading copy, and logo all match — not just "the branding API call
      returned 200" or "the app's login button renders."

## Deploy and verify

Do all five of these in one pass, in order, every time:

1. Follow the co-loaded Next.js reference to install `@auth0/nextjs-auth0`,
   configure `Auth0Client`, add the proxy/middleware, and add login/logout UI.
2. Pin `APP_BASE_URL` (see "Use the generated configuration safely" below) —
   not the per-deployment hashed URL, which changes every publish. Then
   register the matching callback and logout URLs on the Auth0 application
   now, in this same pass — see "Register callback and logout URLs" — do
   not wait for a login attempt to fail first. The integration populates
   localhost and callback URLs initially; update them with the CLI when the
   canonical domain or callback path changes:

   ```bash
   auth0 apps update <client-id> \
     --callbacks "https://<canonical-domain>/auth/callback" \
     --logout-urls "https://<canonical-domain>"
   ```

3. Enable iframe embedding for the intended origins now if the app runs in
   Vercel's embedded preview — see "Login page won't frame" under "Auth0 in
   the v0 preview" for the tenant setting, origin scoping, and dashboard
   path (not yet a CLI flag). Don't wait for the framed login to fail first;
   set this alongside the callback/logout URLs in step 2.
4. **Apply Universal Login branding now if the app has any custom design** —
   this is not optional polish and not a fix for a user complaint; it's part
   of the same build pass as steps 1-3. Do not leave the default Auth0
   branding on a login page that's supposed to look like part of the app.
   At minimum, set the primary/page background color and button/input
   border radius to match the app; pull the values from the app's own
   theme/CSS rather than guessing. Use the full `auth0` skill's branding
   guidance for the exact CLI/Management API calls (`auth0 branding ...`,
   or `PATCH /api/v2/branding` and `PUT /api/v2/branding/themes/default`) —
   see "Getting `AUTH0_*` into the chat's shell" below; fall back to the
   dashboard only if project linking genuinely isn't possible.

   **`logo_url` must resolve to a permanent, publicly fetchable URL** — Auth0
   fetches it server-side, and two origins that look reachable are not:
   - The v0 preview origin is session-gated, so pointing `logo_url` at it is
     a silent no-op — Auth0 fails to fetch it while the request that *set*
     `logo_url` still returns 200.
   - The app's own `public/` path is not safe either, even once deployed:
     the v0 preview origin returns a redirect (302) for `public/` assets
     instead of serving the file, so a logo referenced from that path fails
     to load while every Auth0-side branding check still passes.

   Host the logo on a permanent public CDN URL instead (e.g. Vercel Blob
   created with `access: 'public'`), or skip the logo in preview and set it
   once deployed to a public production URL. When a logo "won't appear,"
   trust the live DOM's `img.src` and a direct `curl` of that URL over a
   headless screenshot — screenshots can cache a stale or placeholder
   render and make a broken `logo_url` look fine. Re-check all branding
   after any tenant reconnect — see "Callback mismatch / login fails after
   reconnecting the integration" in Troubleshoot.
5. Deploy to the selected Vercel Production environment and verify with a
   real login attempt — not just that the page renders. Complete login,
   callback, session, protected-route, and logout checks on the deployed
   URL. **If the app has custom branding, open the login link in an actual
   browser session** (e.g. the Playwright MCP tools, or a manual click-through)
   **and visually compare the rendered hosted login page against the app** —
   page/primary color, app name or heading copy, and logo. A Management API
   200 or a config file diff does not confirm this; only the rendered page
   does. (For a logo that specifically won't appear, prefer a direct `curl`
   of the live `img.src` over a screenshot — see step 4 — since a headless
   screenshot can cache a stale render and hide a broken `logo_url`.) Run
   through the pre-completion checklist above
   before calling this done.

## Install the native integration

### Vercel Marketplace

1. In Vercel, open **Integrations** → **Browse Marketplace** and find
   **Auth0** under Native Integrations.
2. Select **Install**, choose the installation plan, and continue.
3. Name the Auth0 application and create it. Vercel creates the dedicated
   Auth0 tenant environment and application; wait for completion.
4. Select **Connect Project**, choose the Vercel project and target
   environments, enter a variable prefix only if the project requires one, and
   connect.
5. Open the integration's **Getting Started** page and follow its generated
   quickstart.

The Vercel CLI can start the same provisioning flow from the project directory.
Pass `--no-env-pull` so the CLI does not run `vercel env pull` automatically
after provisioning — pulling secrets is a separate, deliberate step below, run
only after confirming `.env.local` is ignored:

```bash
vc i auth0 --no-env-pull
```

Do not treat `vc i auth0` as read-only. It provisions a resource, so run it
only after the developer confirms the target team and project.

## Configure the tenant with the Auth0 CLI

**Before touching tenant config, verify:** decode the running app's login
`redirect_uri` to confirm which tenant/client it uses → confirm that
`client_id` matches the credentials in hand → mint a Management API token
(below) to prove the M2M credentials actually work → only then make changes.
Skipping this and configuring the wrong tenant, or configuring correctly but
with M2M credentials that don't actually work (placeholder values, wrong
environment), is the most common failure mode here.

If the failure was reported by a user rather than reproduced directly (a
published app rejecting logins), you can't decode `redirect_uri` from your
own request — instead pull the tenant's logs
(`GET /api/v2/logs?q=type:f` — `type:f` is the failed-login event type) and
read the `redirect_uri` off the matching failed event. This also confirms
which environment/tenant is actually failing before you change anything.

Reconnecting the integration is destructive to prior tenant config — it
provisions a **new** tenant and application client, so treat any reconnect as
"redo tenant setup," not "resume it."

Once the integration completes, an M2M grant lets you configure the
provisioned tenant directly instead of routing every change through the Auth0
dashboard. **Prefer the CLI for tenant configuration** — callback/logout URLs,
iframe embedding, application settings — and fall back to the dashboard only
where noted below.

```bash
auth0 login --domain <tenant>.auth0.com --client-id "$AUTH0_MANAGEMENT_API_CLIENT_ID" --client-secret "$AUTH0_MANAGEMENT_API_CLIENT_SECRET"
```

Use the M2M client ID/secret the integration provisioned (do not print or log
the secret). This is the same machine-login pattern the CLI uses for any
non-interactive environment — see the full `auth0` skill's `tooling-cli`
reference for every command and flag.

If `vercel env pull` isn't returning the `AUTH0_*` values, check project
linking before assuming the M2M grant isn't available — see "Getting
`AUTH0_*` into the chat's shell" below; it's almost always the wrong Vercel
project, not a missing grant. If no M2M grant is available yet, try
`auth0 login` (interactive device-code) next. As a last resort, only if you
try and cannot get M2M, the CLI, or correct project linking working in the
v0 VM/preview, register/configure by hand in the Auth0 dashboard — see
"Register callback and logout URLs" below.

### The M2M credentials are named after the Management API

The integration provisions a Management API M2M client and exposes it under
these exact Vercel env var names:

- `AUTH0_MANAGEMENT_API_CLIENT_ID`
- `AUTH0_MANAGEMENT_API_CLIENT_SECRET`

Use them verbatim. Do not invent or assume `AUTH0_CLIENT_M2M_ID` /
`AUTH0_CLIENT_M2M_SECRET` — those names don't exist in what the integration
provisions, and guessing at them wastes a round-trip discovering `env pull`
never populated them. Confirm the token actually mints before doing anything
else; the audience must be the tenant's own Management API:

```bash
curl -s --request POST \
  --url "https://$AUTH0_DOMAIN/oauth/token" \
  --data grant_type=client_credentials \
  --data "client_id=$AUTH0_MANAGEMENT_API_CLIENT_ID" \
  --data "client_secret=$AUTH0_MANAGEMENT_API_CLIENT_SECRET" \
  --data "audience=https://$AUTH0_DOMAIN/api/v2/"
```

A successful response returns an `access_token`. Anything else — including
`access_denied` — means the credentials, the audience, or the environment
they came from is wrong; see the next two sections before assuming it's a bad
secret.

### Getting `AUTH0_*` into the chat's shell: it's project linking, not a hard limitation

Management tasks (callback/logout URLs, branding, tenant/client config) can
and should be done with the `auth0` CLI in the shell. If `vercel env pull`
only returns `VERCEL_OIDC_TOKEN` and none of the `AUTH0_*` values
it is likely the shell is linked to the wrong Vercel project.

Verified working sequence (Development environment):

1. Confirm `.env.local` is gitignored and untracked before pulling (fail
   closed if not — see the check above).
2. Install the `auth0` CLI if it isn't already present in the sandbox (not
   preinstalled).
3. `vercel link` to the integration's actual project. Verify by project ID
   (`prj_...`), not name alone — there may be 2-3 near-identical project
   names.
4. `vercel env pull .env.local --environment=development`, then load the
   values into the shell (`source`/`export`).
5. Optionally confirm with the token-mint `curl` above.
6. `auth0 login --domain "$AUTH0_DOMAIN" --client-id "$AUTH0_MANAGEMENT_API_CLIENT_ID" --client-secret "$AUTH0_MANAGEMENT_API_CLIENT_SECRET"` —
   the CLI does its own client-credentials exchange; don't pass it a
   pre-minted token. Confirm with `auth0 tenants list`.

Gotchas:

- A "Could not store to keyring" / `dbus-launch not found` warning on login
  is harmless in a headless sandbox — the token stays in-session; re-login
  when it expires.
- `.env.local` now holds real client secrets. Keep it gitignored/untracked,
  and delete it when the management session is done if you don't want
  secrets at rest.
- A newly-added env var needs a dev-server restart to reach `process.env` in
  the running app — and it must exist on the right project **and** the right
  environment (a Production-only var won't reach the Development preview).

Default to this CLI path. If `vercel link` truly cannot reach the
integration's project (not just "env pull looked empty" — verify the project
ID first), the last resort is the dashboard, not app code — see "Register
callback and logout URLs" for the manual steps.

### Only the development environment has working M2M credentials

Each Vercel environment (Production/Preview/Development) gets its own Auth0
**tenant** and application client. Development additionally gets a real,
authorized M2M client for the Management API. **Production and Staging only
get placeholder `AUTH0_MANAGEMENT_API_CLIENT_ID`/`_SECRET` values** — dummy
strings, not a provisioned-but-unauthorized client. Always verify with the
token-mint `curl` above rather than assuming either way.

For CLI or Management API work against the running v0 preview: pull the
Development environment's values (`vercel env pull .env.local
--environment=development`), verify the token mints, then configure the
tenant/application client that Development points at — that's what the v0
preview actually runs against.

### If you need CLI/Management API access for Production or Staging

If the token-mint check fails, don't guess at a fix — walk through creating a
real M2M client for that environment and wiring it in:

1. In the Auth0 dashboard, switch to the Production/Staging tenant (top-left
   tenant switcher).
2. Go to **Applications → Applications → Create Application**, choose
   **Machine to Machine Applications**, name it (e.g. `v0-management-prod`),
   and authorize it against the **Auth0 Management API** with the scopes you
   need — at minimum `read:clients`, `update:clients`, `read:branding`,
   `update:branding`.
3. Open the new application's **Settings** tab and copy its **Client ID** and
   **Client Secret**.
4. Set those two values as `AUTH0_MANAGEMENT_API_CLIENT_ID` and
   `AUTH0_MANAGEMENT_API_CLIENT_SECRET` on the Vercel project, scoped to that
   specific environment, replacing the placeholder values. This is the
   developer's call, since it means putting Production/Staging Management
   API access in the agent's hands — ask rather than assume. Do this either:
   - directly in the Vercel project's environment variable settings
     themselves, or
   - if the developer is willing to grant the agent access, by pasting the
     Client ID/Secret into the v0 chat and having the agent save them as env
     vars on that environment through its own tooling — don't have the agent
     print, log, or echo the secret back once saved.
5. Re-run the token-mint `curl` against that environment to confirm before
   relying on it.

## Use the generated configuration safely

The integration preloads Auth0 credentials in the Vercel project. Its
quickstart exposes values such as `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`,
`AUTH0_DOMAIN`, and `AUTH0_SECRET`; retrieve them through Vercel rather than
copying secrets from a dashboard or committing a `.env.local` file.

If you set a variable prefix when connecting the project, Vercel names the
managed values `[prefix]_AUTH0_DOMAIN`, `[prefix]_AUTH0_CLIENT_ID`, and so on,
but the `@auth0/nextjs-auth0` SDK only reads the unprefixed default names.
Prefer connecting with no prefix. If a prefix is required, map the prefixed
values back to the standard names in your app before constructing `Auth0Client`
(or pass them explicitly to the constructor).

First confirm `.env.local` is both untracked and git-ignored so the pull cannot
write real client secrets into a tracked file. Stop if either check fails. Then
link the checkout and pull the values:

```bash
# BEFORE pulling any secrets: fail if .env.local is tracked or not ignored.
if git ls-files --error-unmatch -- .env.local >/dev/null 2>&1 \
   || ! git check-ignore --no-index --quiet -- .env.local; then
  echo ".env.local must be untracked and git-ignored before pulling secrets"
  exit 1
fi

# Link the local checkout to the intended Vercel project, then pull local-only values.
vercel link
# For the v0 preview, pull DEVELOPMENT (see "Only the development environment
# has working M2M credentials" above). For a deployed Production app, pull
# --environment=production.
vercel env pull .env.local --environment=development
```

> **The v0 preview runtime does NOT auto-inject the project's Vercel env
> vars** — the dev server only sees `.env.local`. If `process.env.AUTH0_DOMAIN`
> is undefined at request time, the SDK falls back to a header-based domain
> resolver that throws `DomainResolutionError` on every route. `vercel env ls`
> showing the vars proves nothing about the runtime; only a request that
> actually reads `process.env` proves it.

> **Confirm which Vercel project the chat actually runs on** — see "Getting
> `AUTH0_*` into the chat's shell" below for why a differently-named or
> similarly-named sibling project is the most common cause of "the vars
> exist but the app can't see them."

For local development the current Next.js SDK also needs `APP_BASE_URL`; set it
to your local URL (e.g. `http://localhost:3000`) in `.env.local`, and keep the
canonical production URL configured for the deployed environment.

**In the v0 preview, set `appBaseUrl` explicitly to `V0_RUNTIME_URL` — never
rely on the SDK inferring it from the request.** Behind the preview's proxy,
the inbound request's host header is the internal dev-server host, not the
public preview origin, so header-based inference produces a `redirect_uri`
that never matches what's registered on the tenant. This is the single
biggest cause of `"redirect_uri is not in the list of allowed callback URLs"`.

```ts
const auth0 = new Auth0Client({
  appBaseUrl: process.env.V0_RUNTIME_URL ?? process.env.APP_BASE_URL,
});
```

`V0_RUNTIME_URL` is only set inside the v0 preview; it's absent in
Production. Don't assume the SDK's inference is safe there either — Vercel's
inferred host on a real deployment is the per-deployment hashed URL (e.g.
`myapp-qrfarr7z6-team.vercel.app`), which changes on every publish and can
never stay registered on the tenant. Pin `APP_BASE_URL` explicitly to the
stable production alias (`VERCEL_PROJECT_PRODUCTION_URL`, or the custom
domain if one is set) instead: confirm the stable alias → set it as
`APP_BASE_URL` on the Production environment → redeploy → register that one
stable URL (see "Deploy and verify" step 2). This keeps `redirect_uri`
deterministic across publishes instead of drifting with every deploy.
Verify by inspecting the actual `redirect_uri` on the login redirect, not
just that the page compiles — see "Redirect goes to localhost" below for the
same check applied to the localhost-fallback failure mode.

The native-integration quickstart's own walkthrough only wires up the
Production environment. Preview and Development are provisioned automatically
too, but may still need non-Auth0 variables added or scoped manually before
testing.

## Manage the integration

Use the CLI for application-level changes (callback/logout URLs, grant types,
metadata) once the M2M grant is available — see `auth0 apps update --help`.

Use the Vercel project **Integrations** tab → **Auth0** → **Manage** for
Vercel-side operations the CLI has no access to: rotating the credentials
Vercel injects, editing the localhost/callback parameters Vercel tracks
separately, setting allowed environments, changing the installation plan, or
removing the integration. Use the Auth0 Dashboard for anything CLI-unsupported,
such as Universal Login customization.

Before rotating secrets or changing callback URLs, identify every deployment
that consumes the affected variables and plan a redeploy. After rotation,
confirm the new variables are present in the intended Vercel environment and
that login works before removing the old secret from dependent systems.

## Troubleshoot

| Symptom | Check | Resolution |
|---|---|---|
| Marketplace flow creates a different tenant than expected | Native-integration behavior | Expected: it creates a dedicated new Auth0 tenant environment. Use standard Auth0 setup for an existing tenant. |
| Local app has missing Auth0 variables, or `vercel env pull` only returns `VERCEL_OIDC_TOKEN` | Vercel project link and environment selection | Verify you're linked to the integration's own dedicated project by ID (`prj_...`), not a similarly-named sibling or the default v0 project. Run `vercel link` for that project, then `vercel env pull .env.local --environment=development`; keep the file out of Git. See "Getting `AUTH0_*` into the chat's shell." |
| Production works but Preview fails | Variable scope | Add or scope the required non-Auth0 variables deliberately; the generated quickstart's walkthrough only covers wiring up Production, even though Preview/Development are each provisioned automatically. |
| Login/callback fails or doesn't render, despite following "The app rendering is not the finish line" | Should be prevented by that workflow — treat as a diagnostic gap, not a new bug | Pull the tenant's failed-login logs (see "Configure the tenant with the Auth0 CLI") for the actual rejected `redirect_uri`/reason, then fix per "Deploy and verify" steps 2-3. |
| Integration removal has unexpected account impact | Removal warning | Stop and confirm the removal: deleting the integration removes the connected Auth0 account and downgrades the Vercel installation. |
| No M2M grant available yet | Integration provisioning stage, or wrong Vercel project linked | Check project linking first — see "Getting `AUTH0_*` into the chat's shell." If genuinely no grant, try `auth0 login` (interactive) next. Only as a last resort hand-edit the dashboard; see "Register callback and logout URLs." |
| `DomainResolutionError` on every route | `process.env.AUTH0_DOMAIN` missing at request time | The preview runtime doesn't auto-inject project env vars; pull into `.env.local` (Development environment) and confirm the value is present. Harden `middleware.ts` to skip Auth0 handling when config is absent so the site degrades instead of 500ing. |
| Token request returns `access_denied` (or fails to mint) for the Management API | Using Production/Staging's placeholder M2M values, which aren't a real client | Use the Development environment's M2M credentials for preview work, or create a real M2M client for that environment and wire in its Client ID/Secret (see "If you need CLI/Management API access for Production or Staging"). Don't assume it's a wrong secret — verify with a token-mint request first. |
| Login/signup click does nothing; server log shows only `GET /` | Auth button uses `window.open()`, blocked by the sandboxed iframe | Use a real `<a target="_blank">` anchor (via base-ui's `render` prop, not `asChild`). |
| Callback mismatch / login fails after reconnecting the integration | Reconnect provisioned a NEW tenant + application client | Re-register callback/logout/web-origin URLs and re-apply branding on the CURRENT client. Decode the live login `redirect_uri` and `client_id` to confirm which client is actually in use. |
| Every route returns a blank/empty 200 body with no console output, unrelated to Auth0 | Dev server wedged by a burst of rapid file writes | Restart the dev server before debugging further — this is a stuck process, not a code bug, and is common right after a round of rapid edits during setup. |

## Auth0 in the v0 preview

The v0 preview runs your app inside a cross-site iframe on an HTTPS origin that
is neither localhost nor a `VERCEL_URL`. Three common auth failures all trace
back to that fact. Keep these in mind and the flow works the first time.

### 1. Redirect goes to localhost ("localhost refused to connect")

The SDK builds its login/callback redirect from a base-URL setting that
defaults to `localhost`. In the preview, `VERCEL_URL` and
`VERCEL_PROJECT_PRODUCTION_URL` are unset, so anything relying on them falls
back to localhost. Set `appBaseUrl` explicitly to `V0_RUNTIME_URL` — see
"Use the generated configuration safely" above for why inference is a trap
here and the exact snippet. Verify by inspecting the actual `redirect_uri` on
the login redirect, not just that the page compiles.

### 2. State cookie dropped ("The state parameter is invalid")

The SDK stores a short-lived transaction/state cookie during the redirect and
reads it back on the callback. Default `SameSite=Lax` cookies are not sent on
the cross-site callback inside the iframe, so validation fails. When the framed
preview must remain authenticated, set the session cookie to
`SameSite=None; Secure`. Keep the transaction cookie at `SameSite=Lax` for
the top-level callback. Use `SameSite=None; Secure` for the transaction
cookie only when the callback uses an iframe or `form_post`. Document
independent CSRF protection for the cross-site session cookie. Keep plain
`localhost` HTTP on the safe defaults, since `Secure` cookies can't be set over
HTTP.

### 3. Login page won't frame ("This content is blocked")

Hosted login pages may send frame-busting headers when iframe embedding is not
enabled. First restrict the allowed iframe origins to the intended Vercel
URLs, then enable the setting — it's a tenant flag not yet exposed as a CLI
flag: **Auth0 Dashboard → Settings → Advanced → Allow Cross-Origin
Authentication**. Enabling it relaxes clickjacking protection, so scope the
origins first. If embedding isn't viable, open authentication in a top-level
context instead.

Make the login (and logout) navigation break out of the iframe using a real
anchor, not a programmatic `window.open(...)`. The v0 preview iframe is
sandboxed, so a script-initiated `window.open` is silently swallowed by the
popup blocker — the click appears to do nothing, and the server log shows only
`GET /` with no `/auth/*` request ever arriving. A real `<a target="_blank">`
click is a user-initiated navigation, so the sandbox and popup blocker let it
through:

```jsx
<a href="/auth/login" target="_blank" rel="noopener noreferrer">Log in</a>
<a href="/auth/logout" target="_blank" rel="noopener noreferrer">Log out</a>
```

v0's default `Button` is `base-ui`, which composes via a `render` prop, not
Radix's `asChild` — passing `asChild` throws `"React does not recognize the
asChild prop"`:

```jsx
<Button render={<a href="/auth/login" target="_blank" rel="noopener noreferrer" />}>Log in</Button>
```

After login completes in the top-level context, the framed preview needs a
refresh to pick up the new session cookie.

### Register callback and logout URLs

Callback/logout URLs are required application settings configured on the tenant,
not in the app and MUST be configured appropriately. Once an M2M grant is available, use the CLI:

```bash
auth0 apps update <client-id> \
  --callbacks "https://<project>.v0.build/auth/callback,http://localhost:3000/auth/callback" \
  --logout-urls "https://<project>.v0.build" \
  --web-origins "https://<project>.v0.build,http://localhost:3000"
```

Non-Vercel origins are never auto-synced, so register them explicitly. The one
that gets the preview working is the app's **stable v0 preview URL**
(`V0_RUNTIME_URL`, e.g. `https://<project>.v0.build`) — it stays constant
across rebuilds, so registering it once is what makes login succeed in the
preview. (Per-deployment Vercel URLs change every build and aren't worth
registering by hand.) Also register `localhost` for local dev.

By default, Auth0 allows every registered callback URL as a web origin too,
so `--web-origins` is often redundant with `--callbacks`. Pass it explicitly
anyway when an origin needs CORS/Cross-Origin Authentication access without
also being a callback path (or to be unambiguous rather than rely on the
default) — see the checklist above.

**No M2M grant yet, or the CLI isn't available in the chat's shell:** see
"Getting `AUTH0_*` into the chat's shell" above before touching the
dashboard — most cases are project-linking, not a missing grant. Only once
that's ruled out is manual dashboard editing the right move, and even then
treat it as a last resort, not the default:

1. In the Auth0 dashboard, pick the tenant the app's env vars point at
   (top-left tenant switcher — there may be separate Development/Staging/
   Production tenants).
2. Go to **Applications → Applications** and open the app's client (the
   integration names it "Created By Vercel"; match it by Client ID if unsure).
3. On the **Settings** tab, add to the comma-separated lists (use the stable
   v0 preview origin):
   - **Allowed Callback URLs**: the full callback path, e.g.
     `https://<project>.v0.build/auth/callback` (add `http://localhost:3000/auth/callback`
     too for local dev).
   - **Allowed Logout URLs**: the origin the user returns to, e.g.
     `https://<project>.v0.build`.
   - **Allowed Web Origins**: usually unnecessary — Auth0 allows every
     registered callback URL as a web origin by default. Add the origin here
     explicitly only if it needs CORS/Cross-Origin Authentication access
     without being a callback path.
4. **Save Changes** at the bottom. Give the exact origin — Auth0 matches these
   URLs exactly, so a missing entry is what causes callback/logout rejections.

Whichever path registered the URLs, re-verify them after any integration
reconnect or resync — the Vercel Auth0 integration auto-syncs real Vercel
deployment domains and owns the `AUTH0_*` env vars, so it can overwrite
hand-edited or script-edited callback lists without warning. Confirm with
`auth0 apps show <client-id>` or the dashboard before assuming a prior
registration still holds.
