---
name: site-pin-gate
description: >
  Put a shared-PIN gate in front of an entire Next.js site from the
  proxy/middleware layer: one env var arms it, a self-contained unlock page
  sets an HMAC-derived HttpOnly cookie, and the app behind it stays untouched.
  Use when: (1) a pre-launch, staging, client-preview or investor-preview site
  must be hidden from the public and from crawlers without adding user
  accounts, (2) an existing PIN or password gate in middleware.ts or proxy.ts
  needs auditing, (3) the user mentions: site PIN, password-protect the site,
  access code, pre-launch gate, coming-soon lock, staging password, SITE_PIN,
  "hide the site behind a PIN", "lock the preview deployment", "temporary
  password page". Carries the return path resolved against the request origin,
  the 303 unlock redirect, the cookie token keyed by a server-side secret,
  constant-time comparisons, an attempt budget answering 429 with Retry-After,
  and the suite that holds them. Next.js App Router, proxy.ts or middleware.ts;
  the attempt store is a seam, so a shared store can replace the in-memory one.
  Not user authentication and not per-route authorization.
---

# Site PIN gate: one PIN in front of the whole site

A PIN gate is the smallest possible access control: one shared secret, one
cookie, zero user accounts. Its whole value is that the app behind it never
knows it exists. The insight that shapes this module is that **everything
dangerous lives in the two places the gate touches the outside world**: the
return path it redirects to, and the cookie it hands out. Everything else is a
form and a cookie check.

Written by the engineer who has shipped this module. The earlier implementation
it was audited against was a temporary gate on a marketing site kept private
ahead of its launch. The facts and rules below are what the behaviour contract
and the handler suite verify; `references/provenance.md` has the record.

## When to use

A public-by-default Next.js site that must be hidden for a while: before
launch, during a client or investor review, on a staging domain. Everyone who
should see it can be told one PIN. The gate sits in `proxy.ts` (Next 16) or
`middleware.ts` (Next 13 to 15) and is removed by unsetting one env var.

## When NOT to use

| Instead of this | Use |
|---|---|
| Real users with real accounts | the host's auth (Clerk, NextAuth, Supabase Auth); a shared PIN cannot be revoked for one person |
| Per-route or per-tenant authorization | the host's authorization layer; this gate is all-or-nothing by path matcher |
| Only preview deployments, on Vercel, for team members | Vercel Deployment Protection, which needs no code; see [operations.md](references/operations.md) |
| Protecting an API consumed by machines | an API key; a cookie and an HTML form are the wrong shape |

## Architecture

```
request --> proxy.ts / middleware.ts (the matcher decides what is even seen)
              |
              +- SITE_PIN unset ...........................> app (gate off)
              |
              +- cookie == HMAC(secret, pin) ..............> app
              |
              +- GET  /__unlock ..........> 303 /
              +- POST /__unlock  bad body > 400 gate page
              |                  over budget 429 gate page + Retry-After
              |                  wrong PIN . 401 gate page (return path kept)
              |                  right PIN . 303 safe return path + Set-Cookie
              |
              +- anything else ............> 401 gate page, no-store, noindex
```

## Critical facts

1. **An unset PIN is an open site, silently.** The most likely production
   failure is the env var set in one environment and not another. Smoke-test
   every environment; the check is one `curl`.
2. **The matcher is the security boundary.** Whatever it excludes is public.
   Build assets always are; the sitemap, `robots.txt`, OG images and `/api` are
   public only if you exclude them, and a pages-only matcher publishes the route
   list of an unlaunched site through `sitemap.xml`.
3. **The cookie is a bearer token derived from the PIN.** Rotating the PIN logs
   every browser out with no store to clear. Without `SITE_GATE_SECRET` it is a
   plain fingerprint of the PIN, and a leaked cookie is then a leaked PIN.
4. **The PIN's length is the real defence.** The attempt budget is per server
   instance and best-effort. A four-digit PIN is ten thousand requests.
5. **The gate page is self-contained by design.** The proxy runs before the
   app, with no stylesheet, no components and no i18n provider. Inline CSS and a
   strings table are not laziness.

## Hard rules

> **Never validate a return path with `startsWith('/')`.** `//evil.example`,
> `/\evil.example` and `/a/..//evil.example` all pass it and all leave the site.
> Resolve it against the request origin, compare origins, then check the result again.

> **Never answer a successful form POST with a 307.** The browser repeats the
> request with its method and body, so the PIN is posted again to the page it
> lands on, and once more through any locale redirect. Use 303.

> **Never put the PIN, or an unkeyed hash of it, in the cookie.** A cookie the
> operator can read is a cookie an operator's laptop can leak. Key the token
> with `SITE_GATE_SECRET`.

> **Never compare the PIN or the cookie with `===`.** Route both through a
> constant-time comparison of equal-length digests.

> **Never let `request.formData()` throw to the platform.** It rejects any body
> that is not form-encoded, and an unhandled rejection in the proxy is a stack
> trace instead of a rejected attempt. Answer 400.

> **Never choose the matcher by default, never gate `_next/static`, and never
> nest the unlock path in a locale or app route.** Exclusions are public, a
> crawler sees only the 401 anyway, and a colliding unlock path never renders.

## Invocation

| Invocation | Meaning |
|---|---|
| `/site-pin-gate` | Read the task, probe the host, ask for the PIN at step 4; unanswered, write no PIN anywhere |
| `/site-pin-gate 1111` | One bare token is **the PIN**: use it as `SITE_PIN`, do not ask |
| `/site-pin-gate uninstall` | Reserved word, never a PIN: remove the wiring, `lib/site-gate` and the env vars; the site goes public |
| `/site-pin-gate audit middleware.ts` | More than one token is a task, not a PIN |

Name the PIN back before writing it, so a single word meant as a topic
("staging") is not silently armed as one. Trimmed, it must be 1 to 128
characters: blank arms nothing, and the form caps its field at 128, so a longer
PIN is a gate no browser can open. Under eight characters is enumerable and
`1111` is ten thousand guesses against a per-instance, best-effort budget
(fact 4): use it, say what it is worth, and that rotating it is one deploy.

The PIN goes to `.env.local` and nowhere else: never a template, a test, a
commit or `.env.example`; deployed environments take theirs from the platform's
env store ([operations.md](references/operations.md)). `SITE_GATE_SECRET` is
not the argument's business: `openssl rand -hex 32`, never derived from the PIN.

`uninstall` is a launch, so confirm the site is meant to be public, then follow
*Uninstalling* in [operations.md](references/operations.md). To lock again
later, keep the code and unset `SITE_PIN` instead.

## Quick start

1. Probe the host and fill in the seam table: [adaptation.md](references/adaptation.md).
2. Copy the config, pure helpers and attempt store: [module.md](references/module.md).
3. Copy the page renderer and the handler, wire them into `proxy.ts` or
   `middleware.ts` with the default matcher verbatim; only a path the task names
   as public changes it: [handler.md](references/handler.md).
4. Set `SITE_PIN` (the invocation's PIN, if one was given) and
   `SITE_GATE_SECRET` per environment and run the smoke checks. Whatever you
   cannot set, hand over: unset `SITE_PIN` is an open site, and
   `SITE_GATE_SECRET` belongs wherever `SITE_PIN` is: [operations.md](references/operations.md).
5. Run the shipped tests unmodified; with no runner, `npm i -D vitest` (the
   package registry is not an external service): [testing.md](references/testing.md).

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Fitting this into an existing app | adapt, seam, proxy.ts, middleware.ts, matcher, next-intl, cookie name, unlock path, strings, Redis | [adaptation.md](references/adaptation.md) |
| Config, token, return path, budget | SITE_PIN, SITE_GATE_SECRET, HMAC, constantTimeEqual, safeReturnPath, open redirect, rate limit, x-forwarded-for | [module.md](references/module.md) |
| The behaviour contract, the page, the handler, the wiring | renderGatePage, createSiteGate, 303, 401, 429, formData, Set-Cookie, x-robots-tag, inline CSS | [handler.md](references/handler.md) |
| Running it in production | env per environment, PIN at invocation, .env.local, .env.example, Vercel, rotate PIN, kill switch, uninstall, remove the gate, launch, smoke test, sitemap, robots, noindex, OG image, /api, Deployment Protection, lock endpoint, multiple PINs | [operations.md](references/operations.md) |
| Proving it | vitest, bun test, NextRequest, test cases | [testing.md](references/testing.md) |
| The audit ledger: what changed, was kept and was added | provenance, defect, audit, kept deliberately, upgrading an existing gate | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
