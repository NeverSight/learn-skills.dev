---
name: visit-logger
description: >
  Log who opened what, from where and on what, server-side in a Next.js App
  Router app: an IP, edge-geolocation and parsed-browser fingerprint for every
  real page view of a shared resource and for lifecycle moments (sign-in link
  requested, account created, signed in), stored in Postgres/Supabase or
  Firestore, grouped into sittings, with first-open announcements and admin
  history panels. Use when: (1) sales, success or an owner must know whether and
  when someone opened a demo, proposal, quote, report or shared link, (2) a
  "signed up from" location and device is wanted at sign-up, (3) the user
  mentions: visit log, visitor tracking, log visits to the database, geolocation
  headers, x-vercel-ip-city, x-forwarded-for, cf-ipcountry, user agent parsing,
  userAgent(), isBot, device type, "who opened the link", "customer opened the
  demo" Slack ping, visit history, last seen, sign-up location. Carries the
  page-view filter that drops prefetches and Server Actions, bot detection for
  what the framework's list misses, NULL-safe repeat-visitor matching, the
  per-visitor announcement throttle, truncation-honest summaries, and the
  Supabase first-sign-in trap. Next.js App Router on Vercel or Cloudflare; the
  store is a seam. Not product analytics, not client-side tracking, not a
  consent manager.
---

# Visit logger: who opened it, from where, on what

A visit log answers a sales question, not an analytics one: *did this person
open the thing we sent, when, from where, and on what?* One row per real page
view, attributed to a resource and, when known, to a person, plus a row at each
lifecycle moment worth a fingerprint. The insight that shapes the module is that
**a request is not a visit**. Prefetches, assets, mail scanners, staff previews
and reloads all arrive as requests. Every rule here exists to filter them out
before anyone gets told "the customer opened it".

Written by the engineer who has shipped this module. The earlier
implementation it was audited against was a visit log on a sales site, behind
the shared links a team sends customers and on its sign-in routes.
[provenance.md](references/provenance.md) is the ledger: what the audit changed
and how the templates verify it, what was kept deliberately, and what was
designed here and has never run in production.

## When to use

- A shared demo, proposal, quote or report must show who opened it and when,
  and notify someone the first time; a sign-up should record where and on what.
- An existing visit log needs auditing: false "opened" pings, a wrong
  first-opened date, visitors counted twice.

## When NOT to use

| Instead of this | Use |
|---|---|
| Anonymous traffic, funnels, dashboards | Vercel Web Analytics, PostHog, Plausible. This logs *attributed* visits to specific resources |
| Clicks, scroll depth, time on page | a client analytics SDK. This is server-side and sees requests only |
| Cookie consent / ePrivacy banner | the host's consent manager. This sets no cookies, but an IP is still personal data |
| Blocking bots or fraud | Vercel BotID / WAF, Cloudflare Bot Management. `isBot` here labels; it never blocks |
| Gating the whole site | `site-pin-gate`; gating one resource is the host's auth or token layer |

## Architecture

```
request --> route handler / Server Component (the host authorises the viewer)
             |
             +- isPageView(headers)? .. no ...> serve, log nothing
             |    prefetch, <Link> prefetch, iframe, asset, Server Action
             |
             +- describeVisitor(request, edge)  synchronous: IP, geo, UA, isBot
             |
             +- after() ......................> response already sent
                  recordPageVisit(store, visit)
                    +- bot or internal .> insert only, never announce
                    +- readPriorVisits .> assessVisit: first? new visitor? back?
                    +- insert ..........> announce(assessment, fingerprint)?

admin page --> readVisitSummary --> groupVisitsIntoSessions --> <VisitHistory>
           --> readVisitorEvents / findOriginEvent ---------> <VisitorActivity>
```

## Critical facts

1. **A request is not a visit.** Only document navigations and App Router
   client navigations count. Browser prefetch and prerender, `<Link>`
   prefetches, mail previews, iframes, assets and Server Actions are dropped
   before a fingerprint is taken.
2. **The framework's `isBot` is a crawler list.** Next's `userAgent().isBot`
   passes headless Chrome, curl, python-requests and requests with no user
   agent at all, which are the clients that follow links in emails.
3. **Geolocation is only as good as the edge you trust.** Vercel overwrites
   `x-forwarded-for`; behind Cloudflare in front of Vercel it holds Cloudflare's
   address; self-hosted it is whatever the client sent. Region is an ISO 3166-2
   code, not a name. Cloudflare's UTF-8 city names arrive decoded as Latin-1.
4. **`eq` never matches NULL.** A visitor with no IP or no user agent is "new"
   on every page view unless matched with `IS NULL`, and the announcement
   throttle quietly stops working.
5. **A bounded read cannot know the first visit.** Past the limit, ask for it
   separately and show the counts as a lower bound.
6. **Supabase creates the user when the link is requested.** `created_at` is
   not the first sign-in; `email_confirmed_at` is.

## Hard rules

> **Never let tracking touch the response.** Read the fingerprint
> synchronously, defer the store, the write and the announcement with
> `after()`, and never throw from the write path.

> **Never announce a bot or an internal visit, and never let one count as a
> prior visit.** A staff preview must not swallow the customer's first-open
> ping.

> **Never trust `x-forwarded-for` off the platform that overwrites it.** Pick
> the `EdgeHeaders` adapter for the edge the request really came through.

> **Never grant the tables to client roles.** The server alone reads and writes
> tracking rows. Revoke explicitly: Supabase's default privileges grant every
> new table to `anon`.

> **Never render a failed read as an empty history.** "Could not load" and
> "Not opened yet" are different facts to the person deciding whether to call.

> **Never store an IP without a purpose and a retention period.** Ship the
> purge with the table, and say so in the privacy policy.

## Quick start

Every template is copied as written: the rename is the only edit, and the host's
code (the sender, the access check) goes in files of its own. The package
registry is not an external service; install what the templates import.

1. Probe the host, fill the seams, confirm the rename (unattended: apply it and
   list it as an assumption). The subject comes only from the host's
   authorisation, never the query string: [adaptation.md](references/adaptation.md).
2. Copy the types and the fingerprint, pick the edge adapter: [fingerprint.md](references/fingerprint.md).
3. Create the tables or the Firestore indexes: [data-model.md](references/data-model.md).
4. Copy the rules, the write and read paths, and one store: [rules.md](references/rules.md),
   [recording.md](references/recording.md), [stores.md](references/stores.md).
5. Call it from the resource's route or page, and from sign-in:
   [capture.md](references/capture.md).
6. Add the history panels to the admin page: [admin-ui.md](references/admin-ui.md).
7. Schedule retention, write the erasure path: [operations.md](references/operations.md).
8. `npm i -D vitest`, copy the three suites unchanged, wire `vitest run` to
   `npm test`: 56 tests. Never convert them: [testing.md](references/testing.md).
9. Hand over in the final report, all six: migration, purge, privacy line, edge,
   env names, scanner limit: [operations.md](references/operations.md).

## Reference directory

| Scenario | Trigger keywords | Reference |
|---|---|---|
| Fitting it into an app | seam, rename, host probe, Vercel, Cloudflare, self-hosted, strings, i18n | [adaptation.md](references/adaptation.md) |
| What one request tells you | describeVisitor, x-forwarded-for, x-vercel-ip-city, cf-ipcity, userAgent, isBot, headless, Sec-Fetch-Dest, prefetch, rsc | [fingerprint.md](references/fingerprint.md) |
| Tables, columns, indexes, access | page_visits, visitor_events, migration, RLS, REVOKE, anon, Firestore indexes | [data-model.md](references/data-model.md) |
| What counts, when to announce | session window, sitting, first visit, new visitor, throttle, signed up from, origin event | [rules.md](references/rules.md) |
| Writing and reading | recordPageVisit, after(), trackPageVisit, readVisitSummary, truncated, failed, Slack, announce | [recording.md](references/recording.md) |
| Backends | Supabase, supabase-js, service role, Firestore, firebase-admin, NULL, memory store | [stores.md](references/stores.md) |
| Where to call it | route handler, Server Component, headers(), sign-in, magic link, auth callback, signInWithOtp, email_confirmed_at | [capture.md](references/capture.md) |
| The admin panels | visit history, activity, badge, bot row, "first opened", duration | [admin-ui.md](references/admin-ui.md) |
| Running it | GDPR, retention, purge, erasure, pg_cron, handover, .env.example, mail scanner, Safe Links, internal traffic, debugging | [operations.md](references/operations.md) |
| Proving it | vitest, bun test, npm test, test cases, fixtures | [testing.md](references/testing.md) |
| What the audit changed and why | provenance, defect, audit, kept deliberately, upgrading an existing log | [provenance.md](references/provenance.md) |

Part of the [Timerise Skills](https://github.com/timerise-ai/skills) index, which lists the sibling skills.
