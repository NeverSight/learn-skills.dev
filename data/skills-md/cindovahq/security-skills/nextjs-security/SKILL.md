---
name: nextjs-security
description: Security review and secure-coding guidance for Next.js applications (App Router and Pages Router, Next.js 14.x to 16.x). Use when auditing or hardening a Next.js codebase, or when writing or changing Server Actions, Route Handlers, Pages API routes, middleware.ts or proxy.ts, Server and Client Components, caching (fetch cache, use cache, unstable_cache, ISR), next.config, environment variables, images config, or Auth.js, Clerk or Supabase auth integration. Triggers on next in package.json, a next.config.js/mjs/ts file, app/ or pages/ directories, or middleware.ts/proxy.ts. Covers Server Action authorization and IDOR, middleware and proxy bypass (CVE-2025-29927), React Server Components advisories (React2Shell, CVE-2025-55182), data leaking to Client Components, NEXT_PUBLIC_ secret exposure, cross-user cache leaks, CSRF and CORS, XSS (dangerouslySetInnerHTML, Markdown, JSON in script tags), SSRF and the image optimizer, open redirects, security headers and CSP, draft mode, dependencies, and fix verification.
license: Apache-2.0
metadata:
  author: Cindova Technologies
  homepage: https://github.com/cindovahq/security-skills
  version: "1.0.1"
  status: beta
  framework-versions: "Next.js 14.x (unsupported), 15.x (Maintenance LTS until 2026-10-21), 16.x (Active LTS)"
  last-verified: "2026-10-02"
---

# Next.js Security

Find, explain, fix and verify security issues in Next.js applications, and write Next.js code that doesn't introduce them.

All paths in this skill (`references/...`) are relative to the directory containing this `SKILL.md`.

## Modes

- **Review mode**: audit, security review, pentest prep, "is this secure?". Follow the workflow below and produce findings.
- **Build mode**: writing or modifying Next.js code. Apply the [build-mode guardrails](#build-mode-guardrails) to every change. Load only the reference for the area you are touching.

If the `appsec-review` skill is installed, it owns the overall methodology and report format. This skill supplies the Next.js-specific knowledge. If it is not installed, use the [evidence and reporting rules](#evidence-and-reporting-rules) below. Supabase Row Level Security and policies belong to the `supabase-security` skill. Generic Node.js server issues (Express, Fastify, custom servers) belong to the `nodejs-security` skill.

## The Next.js security model in one paragraph

Every `'use server'` function, every `route.ts` export and every `pages/api` file is a **public HTTP endpoint**, whether or not the UI links to it. Rendering a page or layout behind a login does not protect the Server Actions or Route Handlers it uses. `middleware.ts`/`proxy.ts` is an optimistic filter, not an authorization layer: matchers miss paths, and several advisories bypassed it outright. Authorization belongs next to the data, in a `server-only` Data Access Layer that every page, action and handler calls. Anything a Server Component passes to a Client Component, and anything an action returns, is serialized to the browser. Anything prefixed `NEXT_PUBLIC_` is compiled into client JavaScript.

## Review workflow

### 1. Confirm the stack and version

1. Confirm Next.js: `next` in `package.json`, a `next.config.{js,mjs,ts}`, and an `app/` and/or `pages/` directory (possibly under `src/`).
2. Read the **installed** version from the lock file (`package-lock.json` → `"node_modules/next"` → `"version"`, or `pnpm-lock.yaml`/`yarn.lock`/`bun.lock`), not the `package.json` range. Do the same for `react`, `react-dom`, and any auth library.
3. Note which routers are in use. App Router (`app/`) brings Server Components, Server Actions and the RSC protocol. Pages Router (`pages/`) brings `getServerSideProps` and `pages/api`. Many apps have both.
4. Note the request filter file: `middleware.ts` (deprecated in 16, still works) or `proxy.ts` (16+). Read its `config.matcher`.
5. Check support status and advisories. As of 2026-10-02, 16.x is Active LTS (latest 16.3.8), 15.x is Maintenance LTS until 2026-10-21 (latest 15.5.27; unsupported after that date), and 14.x and older are unsupported. Any version older than those patch releases is affected by published advisories. See `references/dependencies.md`.
6. Record the hosting model (Vercel, other managed platform, `next start`, standalone, custom server). Several advisories and the Host-header issues depend on it.

### 2. Map the attack surface

- **Server Actions:** every file or function with `'use server'`. Also files with a top-level `'use cache'`: their exports can be called from Client Components like Server Functions.
- **Route Handlers:** `app/**/route.{ts,js}` and each exported method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
- **Pages API routes:** `pages/api/**`. Data functions: `getServerSideProps`, `getStaticProps`.
- **Dynamic segments:** folders named `[param]`, `[...slug]`, `[[...slug]]` are user input.
- **Config-driven behavior:** `next.config.*` (`images`, `rewrites`, `redirects`, `headers`, `env`, `serverActions`, `productionBrowserSourceMaps`), `instrumentation.ts`, metadata image routes (`opengraph-image.tsx`).
- **Third-party auth:** `auth.ts` (Auth.js), `clerkMiddleware`, `@supabase/ssr` clients, webhook routes.

### 3. Review each area

Load the reference for each area as you reach it. Do not load all of them up front.

| Area | Reference | Start by looking for |
|---|---|---|
| Server Actions | `references/server-actions.md` | `'use server'` functions without auth/ownership checks, `formData` spread into DB writes, full rows returned, `.bind(` args |
| Route Handlers & API routes | `references/route-handlers-api.md` | `route.ts` exports without auth, cookie-auth `POST` handlers (CSRF), reflected `Access-Control-Allow-Origin`, webhooks, `pages/api` |
| Middleware / proxy | `references/middleware-proxy.md` | Auth only in `middleware.ts`/`proxy.ts`, matcher exclusions (`api`), layouts as auth gates, `NextResponse.next({ headers })` |
| Authentication & sessions | `references/authentication-sessions.md` | Cookie flags, custom JWT sessions, Auth.js `AUTH_SECRET`/`trustHost`/callbacks, Clerk `auth()`, Supabase `getSession()` on the server |
| Data exposure | `references/data-exposure.md` | Whole DB rows as props to `'use client'` components, `getServerSideProps` props, missing `server-only`, error details |
| Secrets & configuration | `references/secrets-config.md` | `NEXT_PUBLIC_` secrets, `next.config` `env`, source maps, committed `.env*`, `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY`, dev mode in prod |
| Caching | `references/caching.md` | `unstable_cache`/`'use cache'` keys missing the user or tenant, `force-cache` with credentials, ISR of personalized pages, unauthenticated revalidation, draft mode |
| Validation & injection | `references/validation-injection.md` | Unvalidated action args/params, `$queryRawUnsafe`, mass assignment, file paths from params, uploads |
| XSS | `references/xss.md` | `dangerouslySetInnerHTML`, Markdown/MDX renderers, `JSON.stringify` inside `<script>`, `next/script` inline code, SVG |
| SSRF & redirects | `references/ssrf-redirects.md` | `fetch(userUrl)`, `images.remotePatterns`, dynamic `rewrites` hosts, `redirect(`/`NextResponse.redirect(` with input, `next/og` |
| Security headers & CSP | `references/security-headers-csp.md` | `headers()` in config, nonce CSP in proxy, `poweredByHeader`, framing, HSTS |
| Dependencies | `references/dependencies.md` | Installed `next`/`react` versions vs advisory table, `npm audit`, lock files, EOL majors |
| Verification | `references/verification.md` | How to prove each finding and each fix |

### 4. Classify and report

Every finding needs evidence: file, line, the code or config, and the path from attacker-controlled input to the sensitive operation. Classify findings using the rules below.

### 5. Remediate and verify (when asked to fix)

Explain the issue before changing code. Make the smallest change that uses Next.js's own mechanism (a DAL check, a narrower matcher plus an in-handler check, a DTO, a cache key). Then verify using `references/verification.md`: the attack no longer works, legitimate use still works, and the same pattern isn't repeated elsewhere (search for siblings).

## High-signal patterns

These are **investigation signals, not findings**. Trace each one before reporting.

```text
# Entry points and authorization
'use server'   "use server"   'use cache' (file-level)   export async function (GET|POST|PUT|PATCH|DELETE)
pages/api/   getServerSideProps   middleware.ts   proxy.ts   config.matcher   (?!api   createRouteMatcher(
findUnique({ where: { id    findFirst({ where: { id    .delete({ where: { id    params.id   searchParams.get(
role: formData   Object.fromEntries(formData)   ...data   data: body   .bind(null,

# Data exposure
'use client' + props typed as User/Account/full model   return db.   return await prisma.   select: undefined
NEXT_PUBLIC_.*(SECRET|SERVICE_ROLE|PRIVATE|TOKEN|PASSWORD)   env: {  in next.config   productionBrowserSourceMaps: true

# Supabase / Auth.js / Clerk boundary
auth.getSession()  (server code)   SERVICE_ROLE   sb_secret_   createClient( in 'use client' files
trustHost   AUTH_SECRET   callbacks: { redirect   sameSite: 'none'   httpOnly: false

# Caching
unstable_cache(   'use cache'   cache: 'force-cache'   revalidate =   revalidatePath(   revalidateTag(   draftMode().enable
Cache-Control: public  +  Set-Cookie   dynamic = 'force-static'   generateStaticParams

# XSS
dangerouslySetInnerHTML   marked(   marked.parse(   rehype-raw   allowDangerousHtml   JSON.stringify( inside <script>
<Script ...>{`   beforeInteractive   dangerouslyAllowSVG   contentDispositionType: 'inline'

# SSRF / redirects / CORS
fetch(url   fetch(body.   remotePatterns   hostname: '**'   dangerouslyAllowLocalIP   destination: 'https://:
redirect(searchParams   NextResponse.redirect(new URL(next   callbackUrl   Access-Control-Allow-Origin   allowedOrigins
```

## Common false positives

Do not report these without further evidence:

- **Server Action forms without a CSRF token.** Next.js only runs actions for `POST` and rejects requests whose `Origin` host does not match `Host`/`X-Forwarded-Host` (plus `serverActions.allowedOrigins`). That is the framework's CSRF control. It is a finding only if `allowedOrigins` is too broad, the app is on an affected version (CVE-2026-27978, 16.0.1 to 16.1.6), or the action is reached some other way.
- **`href={user.url}` in App Router components.** The App Router renders with React 19, which replaces `javascript:` URLs in `href`/`src`/`action`/`formAction` on DOM elements with a URL that throws. Still report `javascript:` reaching `window.location`, `router.push`, `dangerouslySetInnerHTML` markup, or Pages Router apps on React 18.
- **`NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY` (or publishable key) in client code.** They are designed to be public. The protection is RLS (see the `supabase-security` skill). The service-role or secret key is the finding.
- **`dangerouslySetInnerHTML` on output of a real sanitizer** (DOMPurify / `isomorphic-dompurify`, `sanitize-html`) with a default or allow-list config, or on static content you control.
- **`react-markdown` without `rehype-raw`** and with the default `urlTransform`. It escapes HTML and drops `javascript:` links by default.
- **Prisma `$queryRaw` / `sql` tagged templates with `${value}` interpolation.** These are parameterized. `$queryRawUnsafe`/`$executeRawUnsafe` with string building is the finding.
- **Inline Server Action closures over server values.** Closed-over variables are encrypted with a per-build key. Still check the action re-authorizes; values passed via `.bind()` are *not* encrypted.
- **`fetch(..., { cache: 'force-cache' })` for public, non-personalized data** without `Authorization`/`Cookie` headers.
- **Missing CSRF protection on `route.ts` handlers that only accept bearer tokens or verify a webhook signature.**
- **`.env.example` / `.env.sample` with placeholder values**, and `.env*` files that are gitignored and not deployed.
- **Supabase auth cookies with `httpOnly: false`.** That is the `@supabase/ssr` default because the browser client must read the session. Hardening at most.
- **A logout or "dismiss banner" Server Action without an auth check.** No privilege is gained.

## Severity calibration

Common mis-ratings to avoid:

- **Missing auth inside a Server Action or Route Handler** is rated by what the endpoint does, not by whether the UI hides it. An unauthenticated admin action (change roles, delete users) is **Critical**. "The page is protected by middleware" does not lower it.
- **Middleware-only authorization on a version affected by CVE-2025-29927** (or a later bypass advisory) is a confirmed bypass of every protected route: rate it by the most sensitive route behind it, usually **Critical/High**.
- **Server data leaking through Client Component props or action return values** (password hashes, reset tokens, MFA secrets, other users' PII) is **High**, even though nothing visible renders it. The data is in the RSC payload.
- **A service-role/secret key or other privileged credential in a `NEXT_PUBLIC_` variable** that reaches a client bundle is **Critical**: it bypasses all authorization in the backing service.
- **Cross-user/cross-tenant cache leaks** are rated as data exposure (usually **High**), not as "caching misconfiguration".
- **Image optimizer allowing any host** alone is Medium (abuse, limited SSRF). Combined with `dangerouslyAllowSVG` served inline without CSP it becomes XSS on the app origin (**High**).
- **Open redirects** are Low/Medium alone. Raise them when they leak tokens (OAuth/magic-link callbacks) or chain into SSRF.

## Build-mode guardrails

When writing Next.js code, default to:

1. **Data Access Layer.** Put all DB/API access in `server-only` modules (`import 'server-only'`) that read the session themselves (`cookies()`/`auth()`/`getUser()`), check authorization, and return minimal DTOs.
2. **Every Server Action and Route Handler authenticates and authorizes on its own**, first thing, even if the page, layout or proxy already did. Scope lookups by owner/tenant (`where: { id, teamId: user.teamId }`).
3. **Validate every argument** of actions and handlers with a schema (zod, valibot). TypeScript types are not enforced at runtime. Accept IDs and changes, not whole objects. Allow-list writable fields; never pass `Object.fromEntries(formData)` or a request body straight to the ORM.
4. **Return only what the UI needs** from actions and handlers, and pass only needed fields to Client Components. Type client props narrowly.
5. **Secrets stay server-side.** Never prefix secrets with `NEXT_PUBLIC_`, never put them in `next.config` `env`, never import a privileged client (service role, admin SDK) from a `'use client'` module.
6. **Proxy/middleware is optional and optimistic.** If used, match broadly and still check in the DAL. Never authorize only by path matching.
7. **Cache only public data, or key it by user/tenant.** Never cache responses that read cookies or set `Set-Cookie` in a shared cache. Protect revalidation and draft-mode endpoints with a secret compared in constant time.
8. **No raw HTML from users.** If HTML is required, sanitize with DOMPurify server-side before `dangerouslySetInnerHTML`. Serialize data into `<script>` with an escaping serializer, or pass it as props instead.
9. **Outbound requests** to user-supplied URLs go through an allow-list. `images.remotePatterns` lists exact hosts with `protocol`, `pathname` and `search`. Redirect targets from input must be relative paths starting with a single `/`.
10. **Cookies** you set: `httpOnly: true`, `secure: true`, `sameSite: 'lax'` (or `strict`), explicit `path` and expiry.
11. **Headers:** set CSP (nonce-based in proxy if you can render dynamically), `frame-ancestors`, HSTS, `X-Content-Type-Options`, and `poweredByHeader: false`.
12. **Keep `next` on the latest patch of a supported major**, and add a test for each security boundary you write (another user gets 403/404, a forged action call fails).

## Evidence and reporting rules

Use these when `appsec-review` is not installed.

**Classification**

- **Confirmed**: the path from attacker input to impact is fully traced in code/config, or it was safely demonstrated.
- **Likely**: strong evidence, but one runtime condition (hosting model, CDN config, environment value, a check in code you can't see) could not be verified. Name it.
- **Hardening**: not demonstrably exploitable, but a stronger control is recommended.
- **Informational**: context with no direct security impact.

**Severity** follows impact × exploitability × required privileges × exposure. Do not raise severity because a scary keyword appears. Unauthenticated RCE, auth bypass and cross-tenant data access are Critical/High. Issues that need an admin account or an unusual configuration go down.

**Finding format**

```markdown
### [SEVERITY] Title — Confirmed|Likely|Hardening
- **Location:** `app/invoices/actions.ts:12` (`deleteInvoice`)
- **Evidence:** the exact code/config, and how attacker input reaches it
- **Impact:** what an attacker gains, and who the attacker must be
- **Preconditions:** auth level, configuration, hosting assumptions, installed version
- **Fix:** smallest Next.js-native change (code snippet)
- **Verify:** test or request that proves the fix
- **Refs:** CWE / OWASP / Next.js docs or advisory link
```

**Rules:** never invent files, routes, packages, versions or config values. Redact secrets (`SUPABASE_SERVICE_ROLE_KEY=****`). Say explicitly when runtime verification was not performed. Only test applications the user is authorized to assess, and use non-destructive checks.

## References

- Next.js data security guide: https://nextjs.org/docs/app/guides/data-security
- Next.js authentication guide: https://nextjs.org/docs/app/guides/authentication
- Next.js security advisories: https://github.com/vercel/next.js/security/advisories
- React security advisories: https://github.com/facebook/react/security/advisories
- Next.js support policy: https://nextjs.org/support-policy
- How to Think About Security in Next.js: https://nextjs.org/blog/security-nextjs-server-components-actions
- OWASP ASVS 5.0: https://owasp.org/www-project-application-security-verification-standard/
