---
name: pylon
description: Build real full-stack apps with Pylon — schema, policies, server functions, server-rendered React (SSR), sync, and one-command deploy. Agent-native and production-grade. Use when the user is working in a Pylon project or asks to build with Pylon/Pylonsync.
---

# Pylon — the agent-native full-stack framework

You are helping build a real application on **Pylon** (pylonsync.com), an agent-native full-stack framework written in Rust with a TypeScript SDK. **Pylon renders your React frontend AND runs your backend** — schema, live queries, auth, server functions, jobs, search, and native server-side rendering, all on one port. It's a Rust server that runs your TypeScript and SSR on Bun. SQLite by default or Postgres. It's production infrastructure, not a sandbox: real auth, row-level policies, and one-command deploy — build like it ships. This skill gives you the shape, conventions, and gotchas to build Pylon apps correctly.

**Scaffold a new app with `npm create @pylonsync/pylon@latest my-app`** — the default template (`barebones`) is the smallest full-stack SSR app that runs: one entity, a live list, optimistic create. **Building an actual product? `--template saas`** — marketing landing, multi-tenant dashboard (orgs, members, tenant-scoped data), first-run onboarding wizard, pricing page, auth (password, email code, Google, reset) and Stripe billing with a trial already wired. **Shipping a mobile app? `--template mobile`** — an Expo Router app with guest-first onboarding, Sign in with Apple / Google / email code, a RevenueCat paywall (`@pylonsync/revenuecat`), offline sync, EAS build profiles, and `STORE.md`, the App Store submission checklist; the backend lives in `apps/api` and also serves the app's public website (landing page, `/support`, `/privacy`, `/terms`, copy in `lib/site.ts`), so the privacy-policy URL both stores demand is live on the same host as the API from the first deploy. `npm create @pylonsync/pylon@latest --help` lists the rest (crm, helpdesk, shop, chat, …). Needs **no global install**: `@pylonsync/cli` ships as a devDependency, so `npm run dev` runs the server. Prefer this. `pylon init` (needs the global CLI) scaffolds a **backend-only** app by default — add `--frontend nextjs|react|tanstack` to pair a separate frontend host. Global CLI install: `curl -fsSL https://www.pylonsync.com/install.sh | bash` (Windows: `powershell -c "irm https://www.pylonsync.com/install.ps1 | iex"`). **Bun ≥ 1.0 must be on PATH** — the Rust server spawns Bun to run your TypeScript + SSR.

## Authoritative references

This skill is a starting point, not the ceiling. When the user asks something this skill doesn't cover — a specific error code, an edge case, a feature not discussed below — fetch the source of truth:

- **Full docs index + concept map:** <https://docs.pylonsync.com/llms.txt> — fetch this first for a condensed overview of every doc page with links.
- **Docs site:** <https://docs.pylonsync.com/> — human docs covering Get started, Core concepts, Auth, Plugins, Clients, Cloud, Operations, and Compare-vs-X pages.
- **Source of truth for APIs:** <https://github.com/pylonsync/pylon/tree/main/packages> — the actual `@pylonsync/sdk`, `@pylonsync/functions`, `@pylonsync/react`, `@pylonsync/react-native`, `@pylonsync/next`, and the Swift SDK at `packages/swift/`. When in doubt about a method name or signature, read the source, not your training data.
- **Working example apps:** <https://github.com/pylonsync/pylon/tree/main/examples> — full apps covering CRM, ERP, chat, 3D, dashboards, plus `examples/swift-todo` for the iOS/macOS SDK.
- **Stack0 Cloud:** <https://cloud.stack0.dev> — managed Pylon. Same binary, same APIs, no infra to run.
- **This skill file (latest):** <https://www.pylonsync.com/pylon-skill.md> — re-fetch if the user reports the skill is out of date.

**Rule:** if you're about to use an API name or pattern you're not 100% sure exists, fetch the source or docs first. The SDK aliases the common naming variants (see the type table below), but anything outside that table that sounds plausible (`v.money()`, `v.enum()`, `v.timestamp()`) is probably hallucinated. (`db.useAggregate`, `db.useReactiveQuery`, `db.useSearch`, `useRoom`, `useShard` ARE real — see the realtime hooks below.)

## When to use this skill

Use this skill whenever:
- The user's project has a `pylon.manifest.json`, `app.ts` importing from `@pylonsync/*`, or a `functions/` directory next to an `app.ts`.
- The user's Swift project imports `PylonClient`, `PylonSync`, `PylonRealtime`, or `PylonSwiftUI`.
- The user says "Pylon", "Pylonsync", "realtime backend", or asks to build a live-syncing feature.
- The user runs `pylon dev`, `pylon init`, `pylon deploy`, `pylon codegen`, or another `pylon` CLI command.
- The user mentions Stack0 Cloud, `cloud.stack0.dev`, or `pylon deploy --target cloud`.

## Core mental model

A Pylon app is five things, all served on one port (a Rust server that runs your TypeScript and SSR on Bun):

1. **Entities** — typed tables declared in `app.ts` via the `@pylonsync/sdk` DSL. Pylon auto-migrates your database (SQLite by default, or Postgres via `DATABASE_URL`) to match.
2. **Policies** — row-level access rules evaluated as string expressions. Live alongside entities.
3. **Functions** — server TypeScript in `functions/*.ts`. Three flavors: `query`, `mutation`, `action`. RPC-called by the client.
4. **Live queries** — `db.useQuery(...)` in React subscribes to results. Pylon restreams diffs on every relevant mutation.
5. **SSR frontend** — your React app under `app/`, server-rendered by the SAME binary. Next-style file routing (`app/**/page.tsx`), `<Link>`/`<Image>`, `metadata`/`generateMetadata`, `loading.tsx`/`error.tsx`/`not-found.tsx`, `sitemap.ts`/`robots.ts`. No separate Next.js host, no `/api` proxy, one shared session on every request. (Headless/native-only apps can skip the frontend; the backend works on its own.)

## Directory convention (full-stack SSR app — the default)

```
my-app/
  app.ts                 # schema + policies + manifest — ENTRY POINT
  functions/             # server functions, one per file, default-exported
    createX.ts
  app/                   # SSR frontend — Next-style file routing, server-rendered
    layout.tsx           #   root layout (wraps every page)
    page.tsx             #   route "/"
    globals.css          #   Tailwind v4 entry; Pylon compiles + injects it
    blog/
      page.tsx           #   route "/blog"
      [slug]/page.tsx    #   dynamic route "/blog/:slug"
    sitemap.ts           #   served at /sitemap.xml (optional)
    robots.ts            #   served at /robots.txt (optional)
  components/            # your components (see the layering table below)
    ui/                  #   shadcn primitives — button, card, input, label,
                         #   select, badge, table, textarea
  components.json        # shadcn config — `bunx shadcn@latest add <name>` works
  lib/utils.ts           # `cn` (clsx + tailwind-merge)
  public/                # static assets served verbatim at the root; a real file
                         #   beats [param]/catch-all route matches (≥0.3.381),
                         #   static route paths beat files — Next semantics
  package.json           # deps: @pylonsync/sdk, @pylonsync/functions, @pylonsync/react, @pylonsync/client, react, react-dom
                         #   + @pylonsync/cli as a devDependency (so `npm run dev` needs no global install)
  pylon.manifest.json    # GENERATED — never edit by hand
```

`pylon dev` watches `app.ts` + `functions/` + `app/` and regenerates the manifest, recompiles Tailwind, and live-reloads the browser on every save. The manifest's routes are discovered from `app/**` by `discoverAppRoutes()` in `app.ts` (see the scaffold). One server serves the SSR HTML, the hydration JS, the API, and the WebSocket — same origin.

(A backend-only app omits `app/` and just ships `app.ts` + `functions/`. Older apps may pair a separate Vite/Next frontend with `@pylonsync/react` + `init()`/`configureClient()` against the Pylon URL — still supported, but native SSR is the default and avoids the second host + the `/api` proxy.)

## Schema (`app.ts`)

Every Pylon app has an `app.ts` that imports from `@pylonsync/sdk`, declares entities + policies, and calls `buildManifest`.

```ts
import { entity, field, policy, buildManifest, discoverAppRoutes, discoverFunctions } from "@pylonsync/sdk";

const User = entity(
  "User",
  {
    email: field.string().unique(),
    name: field.string(),
    createdAt: field.datetime(),
  },
  {
    indexes: [{ name: "by_email", fields: ["email"], unique: true }],
  },
);

const Message = entity(
  "Message",
  {
    roomId: field.id("Room"),
    authorId: field.id("User"),
    body: field.richtext(),
    sentAt: field.datetime(),
  },
  {
    indexes: [
      { name: "by_room_time", fields: ["roomId", "sentAt"], unique: false },
    ],
  },
);

const messagePolicy = policy({
  name: "message_public_read",
  entity: "Message",
  allowRead: "true",
  allowInsert: "auth.userId == data.authorId",
  allowUpdate: "auth.userId == existing.authorId",
  allowDelete: "auth.userId == existing.authorId",
});

const fns = await discoverFunctions();     // walks functions/*.ts

const manifest = buildManifest({
  name: "my-app",
  version: "0.1.0",
  entities: [User, Message],
  policies: [messagePolicy],
  queries: fns.queries,
  actions: fns.actions,
  routes: await discoverAppRoutes(),   // full-stack SSR: enumerates app/**/page.tsx (a backend-only app can pass routes: [])
});

console.log(JSON.stringify(manifest, null, 2));
```

**The last line is required** — `pylon dev` runs `bun run app.ts` and captures stdout as the manifest. Top-level `await` works because Bun runs `app.ts` as an ES module.

**`discoverFunctions()` is what puts your `functions/*.ts` in the manifest** (pylon ≥ 0.4.7). They are callable at `POST /api/fn/<name>` either way — the router loads them independently — but a manifest built with `queries: []` / `actions: []` reports an app with **zero** endpoints, so `/api/manifest`, the OpenAPI spec, and `pylon codegen` all silently under-report. It mirrors the runtime loader exactly (top-level `.ts`/`.js`, name = basename, default export with a `type` and a `handler`) and excludes `internal: true` functions, which aren't externally callable. Mutations and actions both land in `actions` — the manifest's split is read vs write — with `fnType` preserving which was which.

### Field types — EXACT API

```ts
field.string()        // TEXT
field.int()           // INTEGER 64-bit
field.float()         // REAL 64-bit
field.bool()          // 0/1 stored as INTEGER; field.boolean() alias also works
field.datetime()      // ISO-8601 string
field.richtext()      // long-form text
field.json()          // arbitrary JSON value (object/array/scalar), parsed-on-read
field.id("OtherEntity") // FK to another entity's id column
```

`field.json()` hands back the PARSED value on every read path (entity API,
`serverData`, `ctx.db`, sync events) — never a string to `JSON.parse`
yourself. Codegen types it `unknown` (narrow with your own row type). On CRDT
entities the whole value is one LWW register; not searchable, not
encryptable. The matching arg validator is `v.json()`.

**Modifiers (chainable):**
- `.optional()` — nullable
- `.unique()` — implicit unique index on one column
- `.default(value)` — static insert-time default (e.g. `field.bool().default(false)`)
- `.defaultNow()` — datetime defaults to insert time (e.g. `createdAt: field.datetime().defaultNow()`)
- `.owner()` — stamps the field with `auth.userId` on insert and **rejects a forged value** (403 `OWNER_MISMATCH`); also locked on update. Use for `authorId`/`buyerId`/`createdBy` so optimistic `db.insert` stays secure. Guests count (their stable guest id is stamped).
- `.serverOnly()` — never serialized in HTTP responses (secrets, `passwordHash`, `stripeCustomerId`). Still readable inside functions via `ctx.db.*`.
- `.syncOmit()` — stripped from REPLICATION only (snapshots, delta events, WS fanout, reconcile fetches); direct reads (`db.get`, lists, queries, SSR `serverData`) keep it. For heavy-but-not-secret columns — multi-KB JSON blobs, render plans, generated markdown — that would otherwise stream into every browser's replica on every sync. The replica row simply lacks the column; fetch by id when a detail view needs it. Declare such fields `.optional()` so the replica-row type is honest.
- `.max(n)` — string/richtext only: reject values over `n` characters with `400 FIELD_TOO_LONG` on every write path (entity API, sync push, `ctx.db`, CRDT edits). Put one on every user-writable text field; without it a guest can store up to the 10 MB body cap and every client syncs it. Per-caller limits in a policy: `data.bio == null || len(data.bio) <= 280` (`len` of null is null, which denies, so allow null explicitly on optional fields).
- `.readonly()` — settable on insert, rejected on client update (closes IDOR-via-PATCH).
- `entity(name, fields, { audit: true })` — every insert/update/delete lands in the audit log (actor, tenant, row id, changed field names; not values).
- `entity(name, fields, { retention: { field: "createdAt", after: "365d", hold: "legalHold" } })` — hourly job deletes expired rows (audited as `retention.delete`); omit `after` to treat `field` as a per-row expiry time (per-tenant periods).
- `.encrypted()` — AEAD-encrypted at rest (needs `PYLON_ENCRYPTION_KEY`; rotate by moving the old key to `PYLON_ENCRYPTION_PREVIOUS_KEYS` — a background pass re-encrypts, `POST /api/admin/encryption/rotate` runs one now).
- `.crdt("text")` — upgrade string/richtext to LoroText for collaborative merge

`field.enum(["pending", "paid", "failed"])` also exists (stored as a string with allowed-values metadata so codegen emits a precise literal union). Note: there is **no `v.enum()`** validator counterpart — validate an enum arg with `v.union(v.literal("pending"), v.literal("paid"), ...)` or a plain `v.string()`.

**Common mistakes to avoid:**
- Both `field.float()` / `field.number()` work (same type). Both `field.bool()` / `field.boolean()` work. Pick whichever reads better.
- `field.id()` without an entity argument **is invalid** — always pass the target entity name.
- Scalar fields are LWW by default. Use `field.richtext()` or `.crdt("text")` when concurrent text edits should merge.

### Indexes

Declare composite indexes in the options block. Live queries use indexed columns for fast fan-out — **index the filter columns you'll query on.**

```ts
{
  indexes: [
    { name: "by_user", fields: ["userId"], unique: false },
    { name: "by_user_created", fields: ["userId", "createdAt"], unique: false },
  ],
}
```

### Replication — `sync: false` for append-only tables

Entities default to **`sync: true`**: bulk-snapshotted and delta-streamed into
every signed-in browser's local replica. That default is right for the working
set a page renders from, and **wrong for anything that grows forever.**

```ts
const UsageWindow = entity(
  "UsageWindow",
  { projectId: field.id("Project"), periodStart: field.datetime(), requests: field.int() },
  {
    indexes: [{ name: "by_project_period", fields: ["projectId", "periodStart"], unique: true }],
    sync: false,   // read it through a function, not the replica
  },
);
```

**Rule: if the table is append-only, or no component reads it via
`db.useQuery`, set `sync: false`.** Typical: usage/metering rollups, audit and
event logs, billing history, job runs, notifier cursors, anything server-only.

**When you still want it live, scope it instead of disabling it.** `sync`
takes an object — the middle setting between "every row you can read" and
"nothing":

```ts
const Message = entity(
  "Message",
  { roomId: field.id("Room"), body: field.richtext(), sentAt: field.datetime() },
  {
    indexes: [{ name: "by_room_time", fields: ["roomId", "sentAt"], unique: false }],
    sync: { where: "data.roomId == auth.tenantId", limit: 5_000 },
  },
);
```

- `where` is the SAME expression language as policies (`exists(...)` included),
  evaluated per row per caller.
- **Rolling time window** — the right scope for append-only, timestamp-shaped
  data that must stay live (analytics events, activity feeds):
  `sync: { where: 'data.sentAt >= ago("30d")' }`. The replica and every
  catch-up stay bounded no matter how big the table grows; the periodic
  reconcile sweep evicts rows as they age out of the window. Older rows stay
  reachable through direct reads and queries. Combine with `limit` as the
  hard ceiling.
- It is applied **on top of** the read policy, never instead of it. A scope
  only ever REMOVES rows from a replica, so getting one wrong is a
  missing-data bug, never a leak — and a malformed one denies rather than
  falling back to replicating everything.
- `limit` is a hard per-client ceiling that survives snapshot pagination.
  Belt to `where`'s braces.
- A row that **leaves** scope is pushed as a DELETE, so replicas evict it
  instead of holding a copy that never updates again.
- Replication only. Direct reads (`/api/entities/X`, `/api/search/X`) are
  unscoped, same promise as `sync: false` — so an archive view or admin report
  still sees everything its policy allows.

`sync: false` keeps the entity out of the replica **only**. Policies, direct
reads (`/api/entities/X`), `db.useSearch`, and `ctx.db.*` inside functions are
all unchanged — so serve it with a query/action that returns the window the UI
actually renders (`limit: 168`, not the whole table).

Write a `sync: false` entity with a mutation (`ctx.db.insert/update/delete`) or
`/api/entities/X`, never through the client replica (`db.insert` in the sync
engine): no change is echoed back for it, so an optimistic row would vanish on
the next reconcile. `/api/sync/push` refuses such a write with
`ENTITY_NOT_SYNCED`.

Why it matters: the replica bootstrap walks a synced table **one cursor page at
a time, sequentially** — page N+1 needs page N's last id, so cold-start latency
is `rows / pageSize × round-trip`. A real app shipped a per-project-per-hour
rollup with the default on; a page load became ~100 chained requests at ~95ms,
about ten seconds of loading, for data no component read. It is invisible on
day one and unbearable by month three, so decide when you declare the entity.

## Policies

Policies are boolean string expressions. They guard direct `/api/entities/*` access (and sync). Server functions bypass policies — trust yourself to check inside handlers.

**Default-deny is the headline rule: an entity with NO registered policy refuses EVERY request** (`_default_deny`). This is the deliberate fix for the "forgot to lock the table" footgun — a new entity is invisible until you write its policy. For an intentionally-public entity, be explicit: `policy({ entity: "X", allowRead: "true" })`.

**Bindings available in expressions:**
- `auth.userId` — `string | null`
- `auth.isAdmin` — `boolean` (true for the `admin` role / admin token / Studio cookie)
- `auth.tenantId` — `string | null` (the selected org, for multi-tenant apps)
- `data.*` — the row: incoming payload on insert; the **stored row** on read/delete; on update, see below
- `existing.*` — synonym for `data.*`; use whichever reads clearer
- `now` — current UTC time as an ISO-8601 string, for time windows
- `ago("30d")` — the instant that long before `now`, for ROLLING windows (`data.createdAt >= ago("30d")`). Units `s/m/h/d/w`, compound allowed (`"1d12h"`); a bad duration fails at boot, not silently at eval

Roles are checked with the **`auth.hasRole("x")` / `auth.hasAnyRole("a", "b")` functions** — there is **no `auth.roles` array and no `auth.email`** binding in policy expressions. (The SSR page `auth` prop and the session DO expose roles/email; the policy evaluator does not.)

**Actions:**
- `allowRead` — applied to query results; unmatched rows are filtered out silently.
- `allowInsert` / `allowUpdate` / `allowDelete` — reject the op with `POLICY_DENIED` if false.
- **`allowUpdate` runs twice: on the stored row, then on the row after the write** (stored row + patched fields). Both must pass. With `auth.tenantId == data.orgId`, a member can edit their org's rows but a patch of `{ orgId: "<other org>" }` is denied. This applies to every client write path: `PATCH /api/entities`, `/api/sync/push`, `/api/link`, `/api/unlink`, and CRDT pushes. A state change the rule forbids for the new row (`data.status == "draft"` and an edit that publishes) is denied too; do that change in a server function.
- `allowDelete` runs on the stored row.
- **Omitted actions default to deny.**

**Operators — the COMPLETE set (the policy language is deliberately tiny):**
```
==  !=                              // equality
<   <=   >   >=                     // ordering (numbers; timestamps if both are ISO-8601; else lexicographic)
&&  ||  !                           // boolean logic
true  false  null                  // literals
42   -3   4.5                       // numeric literals (int / float / negative)
"string"  'string'                 // string literals (either quote)
auth.hasRole("admin")              // role check
auth.hasAnyRole("admin", "owner")  // any-of role check
ago("30d")                         // timestamp <duration> before now (s/m/h/d/w)
len(data.bio)                      // string length in characters (not a string → null → deny-safe)
exists(Entity where field == <expr> [and field == <expr>]*)   // correlated subquery
```
Ordering is **deny-safe**: comparing null, booleans, or a number against a non-numeric string is always false (so an unresolvable `data.publishAt <= now` denies). Still **no `in`, no `ends_with`/`starts_with`, no arithmetic (`+ - * /`).** Membership ("is the user in this org?") is `exists(...)`, not `in`. String prefix/suffix matching still belongs in a function.

**Typical patterns:**

```ts
// Public read, author-only write
policy({
  name: "post_public",
  entity: "Post",
  allowRead: "true",
  allowInsert: "auth.userId == data.authorId",
  allowUpdate: "auth.userId == existing.authorId",
  allowDelete: "auth.userId == existing.authorId",
});

// Member-of-org — membership lives in a join entity, checked with exists()
// NOTE: `Document` must actually HAVE an `orgId` field — see below.
policy({
  name: "doc_members",
  entity: "Document",
  allowRead: "exists(OrgMember where orgId == existing.orgId and userId == auth.userId)",
  allowInsert: "exists(OrgMember where orgId == data.orgId and userId == auth.userId)",
  allowUpdate: "exists(OrgMember where orgId == existing.orgId and userId == auth.userId)",
});

// Admin-only
policy({
  name: "audit_admin",
  entity: "AuditLog",
  allowRead: "auth.isAdmin",          // or: auth.hasRole("admin")
});

// Multi-tenant row scoping
policy({
  name: "ticket_tenant",
  entity: "Ticket",
  allowRead: "auth.tenantId == existing.orgId",
  allowInsert: "auth.tenantId == data.orgId",
});
```

**Tenant-scoped reads make org switching SLOW.** `auth.tenantId == data.orgId`
means the visible set changes on every org switch, so the sync engine must
wipe the replica and re-bootstrap from zero (blank dashboard for seconds).
For apps where users belong to multiple orgs, prefer MEMBERSHIP-scoped reads
— `allowRead: "exists(OrgMember where orgId == data.orgId and userId ==
auth.userId)"` — then the replica is valid across all the user's orgs at
once, and passing `resetOnTenantFlip: false` in the engine/provider config
makes an org switch instant: no wipe, no re-pull, the UI just filters by the
live `tenantId` (a background reconcile picks up rows of orgs joined since
the last snapshot). Do NOT set that flag with tenant-scoped reads — it would
keep stale rows across switches. Writes and functions may keep using
`auth.tenantId` either way.

```ts

// Time window: published posts are public; scheduled ones stay hidden until their time
policy({
  name: "post_published",
  entity: "Post",
  allowRead: "data.publishAt <= now || auth.userId == data.authorId",
});

// Threshold: only show rows at or above a priority
policy({
  name: "ticket_priority",
  entity: "Ticket",
  allowRead: "data.priority >= 3",
});
```

**Read policies run PER ROW. `exists(...)` in one is a query per row.**

A tenant gate like

```ts
allowRead: `auth.tenantId == data.orgId && (
  exists(Subscription where referenceId == data.orgId and status == "active") ||
  exists(Subscription where referenceId == data.orgId and status == "trialing")
)`
```

is evaluated against **every row** of a snapshot, a cursor page, and a list —
so on a synced stat table it becomes thousands of identical subqueries per
page load. The runtime memoizes `exists(...)` within a single scan, which
collapses that to one query per distinct question, but the shape still costs
more than it looks:

- Put the cheap, data-independent test FIRST (`auth.userId != null &&
  exists(...)`) — `&&` short-circuits, so a failing gate never runs the
  subquery.
- Gate on something already ON the row where you can. `data.orgId ==
  auth.tenantId` needs no subquery at all.
- A subscription/plan check is per-ORG, not per-row. Prefer denying the whole
  entity via a function, or stamping the row, over re-asking per row.
- Pair an expensive policy with `sync: false` or a `sync` scope, so the
  expression isn't run across a whole growing table on every connect.

**Gotcha: a policy that names a field the entity doesn't have denies
everything, silently.** An unresolvable reference is null, and null fails
closed — `exists(OrgMember where orgId == data.orgId ...)` on an entity keyed
`projectId` (no `orgId`) matches nothing, for everyone, forever. There is no
error and no warning: it reads exactly like a working membership check, and the
symptom is "the table looks empty" rather than "access denied".

Failing closed is the right default — the alternative leaks reads on a typo —
but it means **you must check the field exists on THAT entity** when you copy a
policy between entities. This shipped in a real app and stayed unnoticed
because the one page that displayed the data read it through a function
(functions bypass policies), so nothing appeared broken.

## Functions (`functions/*.ts`)

Three flavors, all default-exported. The **filename** becomes the RPC name — `functions/createIssue.ts` is callable at `POST /api/fn/createIssue`.

### Auth levels — read this before you write a public/pre-login feature

Every `query` / `mutation` / `action` carries an `auth` level. **The default is `"user"`.** The router enforces it *before* your handler runs — a caller who doesn't meet the bar gets a typed rejection and the handler never executes. The four levels:

| `auth:` | Who can call it | Use for |
|---|---|---|
| `"user"` **(default)** | A real signed-in user. **Guest sessions are REJECTED.** | Everything behind login. `ctx.auth.userId` narrows to `string`. |
| `"guest"` | Guest sessions (`/api/auth/guest`) **and** signed-in users | Pre-login state: carts, public demos, "try it before signing up". |
| `"public"` | Anyone, including fully unauthenticated | Webhook receivers, healthchecks, landing-page form submits. |
| `"admin"` | `ctx.auth.isAdmin === true` | Ops endpoints. |

**THE gotcha (this bites everyone): a guest session cannot call a default (`auth: "user"`) function.** If you mint a guest with `POST /api/auth/guest` and then `callFn("addToCart", …)`, the call fails with `401 AUTH_REQUIRED` ("requires a session — sign in or POST /api/auth/guest first") **unless that function declares `auth: "guest"`**. Public demos, pre-login carts, and anonymous "kick the tires" flows must set `auth: "guest"` (or `"public"`) on **every** function they call. Forgetting this is the #1 reason a scaffolded public demo returns 401s.

```ts
export default mutation({
  auth: "guest",                 // guest sessions AND users may call this
  args: { sku: v.string() },
  async handler(ctx, args) { /* ctx.auth.userId may be null — check it */ },
});
```

### Validators — EXACT API

Import from `@pylonsync/functions`:

```ts
v.string()
v.int()
v.number() / v.float()     // 64-bit float (both names work)
v.boolean() / v.bool()     // boolean (both names work)
v.datetime()               // ISO-8601 string
v.richtext()               // richtext string
v.id("Entity")
v.optional(v.string())
v.array(v.string())
v.literal("open")    // exact string/number/bool
v.object({ k: v.string() })
v.union(v.literal("a"), v.literal("b"))   // discriminated union / enum-of-literals
v.null()
v.any()
```

`v.float()` and `v.number()` are aliases for the same 64-bit float validator. Use whichever matches your `field.*` choice.

### Mutation pattern

```ts
// functions/createIssue.ts
import { mutation, v } from "@pylonsync/functions";

export default mutation({
  args: {
    teamId: v.id("Team"),
    title: v.string(),
    description: v.optional(v.string()),
    priority: v.optional(v.int()),
  },
  // `auth: "user"` is the default — the framework rejects BOTH anon
  // AND guest callers BEFORE the handler runs, so `ctx.auth.userId` is
  // `string` (not nullable) here. Use `auth: "guest"` for pre-login
  // callers, `auth: "public"` for webhooks/healthchecks.
  async handler(ctx, args) {
    const id = await ctx.db.insert("Issue", {
      teamId: args.teamId,
      title: args.title,
      description: args.description ?? null,
      priority: args.priority ?? 0,
      authorId: ctx.auth.userId,
      createdAt: new Date().toISOString(),
    });

    return { id };
  },
});
```

### Query pattern

```ts
// functions/listIssues.ts
import { query, v } from "@pylonsync/functions";

export default query({
  args: { teamId: v.id("Team") },
  async handler(ctx, args) {
    return ctx.db.query("Issue", { teamId: args.teamId });
  },
});
```

Queries are **live** when called from the React hook — the client subscribes and re-runs on relevant mutations.

### Action pattern (side effects — emails, external HTTP)

```ts
// functions/sendInvite.ts
import { action, v } from "@pylonsync/functions";

export default action({
  // Default `auth: "user"` — anon POSTs to this endpoint never reach
  // the handler. CRITICAL for actions: policies don't gate them, so
  // a forgotten auth check on an action that calls Stripe/Resend/etc.
  // = open vulnerability. `auth: "public"` for webhook receivers only.
  args: { email: v.string(), orgId: v.id("Org") },
  async handler(ctx, args) {
    // Built-in transactional email — no HTTP call, uses the runtime's
    // PYLON_EMAIL_* provider (sendgrid / resend / stack0 / webhook):
    await ctx.email.send(args.email, "Invite", "You're invited!");
    // Options form adds HTML + base64 attachments (contentType passes
    // through verbatim, so `text/calendar; method=REQUEST` invites work):
    // await ctx.email.send({ to, subject, text, html?, attachments? });
    // (Or hit an external HTTP API directly with fetch(...) + ctx.env.KEY.)
    return { ok: true };
  },
});
```

**Actions have NO `ctx.db`.** They're for external I/O and are non-transactional. To read/write data from an action, call a registered function: `ctx.runQuery("listX", args)` / `ctx.runMutation("createX", args)` (each runs in its own transaction). Use mutations for atomic multi-row writes.

### `ctx` surface (inside handlers)

**The three ctx shapes are NOT the same.** In particular an `action` has **no `ctx.db`**, and a `query` ctx has no `error`/`scheduler`/writes. Don't reach for a field the flavor doesn't have.

```ts
// ---- On EVERY ctx (query / mutation / action) ----
ctx.auth.userId       // string | null  (narrows to string when auth: "user"/"admin")
ctx.auth.isAdmin      // boolean
ctx.auth.tenantId     // string | null  (selected org)
ctx.auth.roles        // string[] (exact active-org/session role slugs)
await ctx.auth.elevate({ admin: true, reason: "..." })  // async — promote AFTER you verify a webhook/HMAC
ctx.env               // Record<string,string> — secrets / env (same values as process.env)
ctx.requireMember(orgId, { role })     // assert org membership/role — throws (UNAUTHENTICATED / MISSING_ORG / FORBIDDEN), fails closed
// NOTE: there is NO ctx.auth.email on the handler ctx.
// Need the email? -> const u = await ctx.db.get("User", ctx.auth.userId)  (query/mutation only)

// ---- query ctx — ctx.db is a READ-ONLY reader (no error, no scheduler, no writes) ----
ctx.db.get(entity, id)                 // => row | null
ctx.db.list(entity)                    // => row[]
ctx.db.query(entity, filter)           // => row[]   filter: { field: value, $gt, $lt, $in, $like, $order, $limit }
ctx.db.lookup(entity, field, value)    // => row | null
ctx.db.search(entity, spec)            // => { hits, facetCounts, total }  (needs `.search({...})` on the entity)
ctx.db.paginate(entity, { cursor, numItems })

// ---- mutation ctx — ctx.db ALSO has writes (transactional); + error, scheduler, llm, rooms, stream, connections ----
ctx.db.insert(entity, data)            // => id (string)
ctx.db.update(entity, id, patch)       // => boolean (true if the row existed)
ctx.db.delete(entity, id)              // => boolean
ctx.db.link(entity, id, relation, targetId) / ctx.db.unlink(entity, id, relation)
ctx.db.advisoryLock(key)               // serialize a TOCTOU-prone quota/uniqueness check
throw ctx.error("CODE", "message")     // typed error → rolls the tx back
ctx.scheduler.runAfter(delayMs, "fnName", args)   // enqueue delayed call; returns the job id
ctx.scheduler.cancel(jobId)                       // { cancelled } — false if it already started/finished
ctx.audit.log({ action: "lead.export", entity, entityId, meta })  // append-only audit event; actor/tenant from session
ctx.audit.list({ entity, entityId, action, beforeId, limit })  // actions only; caller's tenant (admins: any)
ctx.scheduler.runAt(unixMs, "fnName", args)       // enqueue at a wall-clock time (Unix ms, e.g. new Date(iso).getTime())

// ---- action ctx — NO ctx.db. Read/write via runQuery/runMutation; + email, error, scheduler, llm, rooms, stream ----
ctx.runQuery("fnName", args)           // read by invoking a registered query
ctx.runMutation("fnName", args)        // write by invoking a registered mutation (own tx)
ctx.agents.run("agentName", { input, as: { userId, admin? }, context?, runId? })  // run an agent() as that user; internal or admin (elevated) callers only
ctx.email.send(to, subject, body)      // transactional email via PYLON_EMAIL_* provider
ctx.email.send({ to, subject, text, html?, attachments? })  // options form: HTML + base64 attachments
throw ctx.error("CODE", "message")
ctx.request?.rawBody / ctx.request?.headers   // raw HTTP request (verify Stripe/GitHub webhook sigs)
ctx.request?.url                              // full public URL (Twilio signs it)
return ctx.response({ status, contentType, headers, body })  // raw reply from /api/webhooks/<name> (TwiML, empty 200)

// ---- mutation + action: LLM, streaming, server push ----
await ctx.llm.complete(request)         // request: { messages, system?, tools?, model?, max_tokens?, temperature? }
await ctx.llm.stream(request, onEvent, { signal? })  // same request; onEvent fires per delta, resolves with the SAME assembled response. signal aborts → rejects LLM_CANCELLED + closes the provider connection
ctx.stream.write(text)                  // SSE chunk → the caller (db.streamFn). RESUMABLE: buffered server-side under a stream id
await ctx.rooms.broadcast(room, topic, data)    // → EVERY subscriber of a presence room; => { delivered: boolean }
```

`ctx.llm` (provider-abstracted completions), `ctx.rooms` (server-originated push), and `ctx.connections` (per-user OAuth tokens) are on **mutation + action** ctx only — never on `query` (reactive purity: a subscribed query must be a pure function of its `ctx.db` reads, and a reactive re-run would re-bill the LLM / re-broadcast the event).

**Streaming LLM output.** `ctx.llm.stream` calls `onEvent` for each event as the provider emits it, then resolves with the same response `complete` returns — so you stream text out AND still branch on `stop_reason`:

```ts
// functions/agent.ts
const tools = [{
  name: "get_order",
  description: "Look up an order by id.",
  input_schema: { type: "object", properties: { orderId: { type: "string" } }, required: ["orderId"] },
}];

export default action({
  args: { question: v.string() },
  timeout: 300,   // idle seconds: each stream event resets it; total run capped
                  // at 10x. Default PYLON_FN_CALL_TIMEOUT is 30s (Cloud: 300s).
  async handler(ctx, args) {
    const messages: { role: "user" | "assistant"; content: string | any[] }[] = [
      { role: "user", content: args.question },
    ];
    for (let turn = 0; turn < 10; turn++) {   // ALWAYS bound the loop
      const res = await ctx.llm.stream({ messages, tools }, (e) => {
        if (e.type === "text_delta") ctx.stream.write(e.text);
      });
      messages.push({ role: "assistant", content: res.content });  // keep tool_use blocks verbatim
      if (res.stop_reason !== "tool_use") return { turns: turn + 1 };
      const results = [];
      for (const b of res.content) {
        if (b.type !== "tool_use") continue;
        const out = await ctx.runQuery("getOrder", { id: (b.input as any).orderId });
        results.push({ type: "tool_result", tool_use_id: b.id, content: JSON.stringify(out) });
      }
      messages.push({ role: "user", content: results });
    }
    throw ctx.error("AGENT_LOOP_LIMIT", "tool loop did not converge");
  },
});
```

Events: `text_delta {text}` | `tool_use_start {id, name}` | `tool_input_delta {partial_json}` | `done {stop_reason, usage}`. Tool arguments arrive as raw JSON fragments — concatenate, parse ONCE at the end (a single fragment is not valid JSON). Same auth gate and model allowlist as `complete`.

**SSE only when the handler streams (≥0.3.380).** `POST /api/fn/:name` with `Accept: text/event-stream` answers as SSE only if the handler actually calls `ctx.stream.write`; a handler that returns without streaming gets plain JSON (the raw return value), same as a JSON-only call. This makes MCP-over-an-action work out of the box — MCP clients advertise SSE on every POST but only parse plain JSON or default-type SSE events, so a non-streaming MCP handler now just works.

**`ctx.stream.write` vs `ctx.rooms.broadcast`.** `ctx.stream.write` streams to the one client holding the HTTP response — and every fn stream is RESUMABLE (≥0.4.22): the host buffers frames under a stream id (`X-Pylon-Stream-Id` header) with `id:` sequence lines, `streamFn` auto-reconnects to `GET /api/fn-streams/<id>?since=<cursor>` on a drop, `onStreamId` + `resumeStream(id)` survive a full page reload and deliver the final result even after the handler finished. Buffers are in-memory (default 4MB/stream, 1h retention after completion) — resume survives disconnects, not server restarts. `ctx.rooms.broadcast(room, topic, data)` reaches every CURRENTLY-CONNECTED subscriber of the presence room (second device, live dashboards, jobs with no HTTP caller) but does NOT replay missed messages. `{ delivered: false }` means the room had no members — a no-op, not an error. Doing both in one handler is normal. Clients join with `useRoom(roomId, userId)` and read pushes via `getSync().subscribeRoomMessages(roomId, (m) => ...)`; server broadcasts arrive with an empty `m.from`.

**`ctx.files.signedUrl(fileId, { ttlSecs })` (≥0.4.1)** — `GET /api/files/<id>` serves only the file's owner (or an unscoped admin). For authorized cross-user reads (an organizer reviewing a member's upload), a server function mints a short-lived signed path: `await ctx.files.signedUrl(fileId, { ttlSecs: 300 })` → `/api/files/<id>?sig=<hmac>&exp=<unix>`, anonymously fetchable (works in `<img src>`). ttl defaults 300s, capped at 24h. Available on query/mutation/action ctx. WHO gets a URL is your function's job — gate the mint with `ctx.requireMember`. Invalid/expired signatures fall through to the normal owner check; nothing becomes enumerable.

**Functions bypass policies** — a `mutation`/`action` that reads or writes another tenant's
rows without re-checking membership is an IDOR. Use `ctx.requireMember(orgId, { role })` (it
looks up the membership row and throws `UNAUTHENTICATED`/`FORBIDDEN`) rather than trusting
`args` or a client-supplied id.

`ctx.error` exists on **mutation/action** ctx but **not on query ctx** — a `query` handler that needs to signal "forbidden" should return a discriminated result (`{ authorized: false }`) rather than throw, or a plain throw will reach the client as a stripped generic `HANDLER_ERROR`.

### Typed errors

Always throw via `ctx.error(code, message)`. Canonical codes:
`UNAUTHENTICATED`, `POLICY_DENIED`, `NOT_FOUND`, `INVALID_ARGS`, `RATE_LIMITED`, `CONFLICT`, `INTERNAL`.
`ctx.error` returns the Error; it does not throw. Write `throw ctx.error(...)`. A handler that
`return`s the Error is still rejected by the runtime (an Error has no JSON shape, so it is
treated as thrown), but only `throw` also rolls a mutation's transaction back.

## React client (live data)

In a **full-stack SSR app you do NOT call `init`/`configureClient`** — the runtime wires the client to its own origin and injects the session on every render. Just import `db` / `callFn` and use them. `db.useQuery` is a live WebSocket subscription that updates on every relevant write.

(Only a **standalone** Vite/Next frontend needs manual wiring: `init({ baseUrl, appName })` + `configureClient({ baseUrl, appName })` once at mount, where `appName` matches `manifest.name`.)

### Live query

```tsx
import { db } from "@pylonsync/react";

function MessageList({ roomId }: { roomId: string }) {
  const { data: messages, loading } = db.useQuery("Message", { where: { roomId } });
  if (loading) return null;
  return (
    <ul>
      {messages.map((m) => <li key={m.id}>{m.body}</li>)}
    </ul>
  );
}
```

Filter keys must be indexed columns for performant fan-out.

`loading` drops as soon as there are rows to show, including rows from a warm local cache that this session has not confirmed with the server. `synced` (on `useQuery` / `useQueryOne`) is true once the engine completed a pull in this session; it resets on an org or account switch and stays false offline. Gate empty states, counts, and billing UI on `synced` so a stale partial cache never reads as complete.

### Calling functions

```tsx
import { callFn } from "@pylonsync/react";

async function onSend(roomId: string, body: string) {
  const { id } = await callFn("sendMessage", { roomId, body });
  return id;
}
```

`callFn`, `db.fn`, and `useMutation` all reach the same endpoint and all keep your replica current: the response's `X-Pylon-Change-Seq` header triggers a one-shot pull when the call produced changes the replica hasn't seen. **On pylon < 0.4.7 the exported `callFn` skipped that**, so your own write didn't show up until something else refreshed — if you're pinned below 0.4.7, use `db.fn` instead. Passing an explicit `{ token }` still bypasses the replica by design: that's a call as a different identity, and its results must not land in this user's data.

### Realtime hooks beyond `db.useQuery`

`db.useQuery` is the workhorse, but the React SDK ships a full realtime surface. Pick the right primitive:

| You want | Hook | Notes |
|---|---|---|
| Live list of one entity, filtered | `db.useQuery("E", { where: {...} })` | Cached in the local replica; filters offline/sort locally for free. **The cross-tab-reliable primitive.** |
| One row by id, live | `db.useQueryOne("E", id)` | |
| Live pagination | `db.useInfiniteQuery("E", { pageSize })` | each page is its own subscription |
| Server-side join / computed / aggregate value, live | `db.useReactiveQuery("fnName", args)` | Convex-style: a `query()` handler that auto-re-runs when its dep set changes. **See the footgun below.** |
| Live count / sum / avg / groupBy | `db.useAggregate(...)` | |
| Live full-text + faceted search | `db.useSearch("E", { query, filters, facets, sort, pageSize })` | re-runs on every keystroke AND every matching write; needs `.search({...})` on the entity |
| Optimistic write with a "ghost" row | `db.useMutation("fnName")` / `db.useEntity` | inserts locally instantly; server broadcast reconciles in place. `db.insert` / `update` / `delete` (and `useEntity`'s) reject with `MutationRejectedError` (`code`, `message`) after rolling the row back when the server refuses the write, so catch it to show "not sent"; they resolve when the server applies the write or queues it offline |
| Presence / cursors / typing / broadcast | `useRoom(roomId, userId, { initialPresence })` | ephemeral — `peers`, `setPresence(data)`, `broadcast(topic, data)`. NOT persisted. Receive relayed messages via `getSync().subscribeRoomMessages(roomId, cb)`. |
| Server-generated output (agent tokens, job progress) pushed to everyone watching live | server side: `ctx.rooms.broadcast(room, topic, data)` | ephemeral, live-only (no replay on reconnect); client joins with `useRoom` + `subscribeRoomMessages` |
| Server-generated output streamed back to the ONE client that called | server side: `ctx.stream.write(text)` | client reads with `db.streamFn(fn, args)`. RESUMABLE — a dropped connection auto-reconnects from its cursor; persist `onStreamId` + `resumeStream(id)` to survive a reload |
| Authoritative multiplayer sim (game/MMO tick loop) | `useShard(shardId, { subscriberId, token })` | `{ snapshot, tick, send, connected }`. The server-side sim (`SimState` tick loop) is defined in Rust (`crates/realtime`); `useShard`/`connectShard` are the TS client. |
| Connection/sync state for a status indicator | `useSyncStatus()` / `useSession()` | |
| The signed-in user's OAuth profile picture (≥0.4.2) | `useSession()` → `session.avatarUrl`; also `avatar_url` on `GET /api/auth/me`, `/api/auth/session`, and the org-members listing | Captured from the provider's `picture`/`avatar_url` claim on every OAuth login; `null` for password/magic users — keep the initials fallback. |

**Cross-tab realtime footgun (important).** For state that must update across *all* a user's tabs (a live counter, availability, "N slots left"), use **`db.useQuery` over a PII-free projection/aggregate entity** — NOT `db.useReactiveQuery`. Reactive server queries behave as leader-tab-only in practice (a follower tab's reactive subscription may never deliver its initial result), whereas entity sync (`db.useQuery`) reaches every tab. The pattern: keep your sensitive table `allowRead: "false"` (deny-all), and have the mutation also maintain a small public-read projection entity (e.g. `WaitlistStat { count }`, `BookedSlot { serviceId, startsAt }`) with `allowRead: "true"` + client writes denied. Subscribe the UI to the projection.

```tsx
// Live counter that updates in every tab — db.useQuery over a public projection
const { data: stat } = db.useQuery("WaitlistStat");   // allowRead:"true", count maintained server-side
const count = stat[0]?.count ?? 0;

// Presence (cursors / typing) — ephemeral, not stored
const room = useRoom(`doc:${docId}`, userId, { initialPresence: { cursor: 0 } });
room.peers.map((p) => <Cursor key={p.user_id} x={p.data.cursor} />);
room.setPresence({ cursor: caretPos });
```

Use `db.useReactiveQuery` for **server-side joins / computed values rendered in one (leader) view** (a feed that joins Post→User, a dashboard rollup) — it's the right tool there. Just don't lean on it for cross-tab fan-out of a shared scalar.

### Session / auth bootstrap (guest fallback pattern)

```tsx
import { storageKey } from "@pylonsync/react";

async function ensureGuest(): Promise<string> {
  const BASE_URL = import.meta.env.VITE_PYLON_URL ?? "http://localhost:4321";
  let token = localStorage.getItem(storageKey("token"));
  let userId = localStorage.getItem(storageKey("user"));
  if (!token || !userId) {
    const res = await fetch(`${BASE_URL}/api/auth/guest`, { method: "POST" });
    const body = await res.json();
    token = body.token;
    userId = body.user_id;
    localStorage.setItem(storageKey("token"), token);
    localStorage.setItem(storageKey("user"), userId);
  }
  return userId;
}
```

The response is `{ guest: true, token, user_id }`. **Minting a guest is only half of it** — every function this guest then calls must declare `auth: "guest"` (or `"public"`). A guest token against a default `auth: "user"` function still returns `401 AUTH_REQUIRED`. See "Auth levels" above.

## Server-side rendering (full-stack frontend)

Pylon natively server-renders React from the same server that runs your backend (the Rust server spawns Bun to execute the render) — Next-style, but no Next. Routes are files under `app/`.

### Routing & components

- `app/page.tsx` → `/`, `app/blog/page.tsx` → `/blog`, `app/blog/[slug]/page.tsx` → `/blog/:slug`, `app/docs/[...slug]/page.tsx` → catch-all, `[[...slug]]` → optional catch-all.
- `app/layout.tsx` wraps every page (nest `layout.tsx` per segment for sub-layouts).
- Route groups: a `(group)` directory is stripped from the URL — `app/(marketing)/pricing/page.tsx` still serves `/pricing`. A `layout.tsx` inside the group wraps only that group's pages, so one section gets its chrome (marketing nav + footer) while routes outside it (`/login`, `/dashboard`) render bare. Prefer this over URL-sniffing in the root layout.
- **A page is a server component by default** (runs only on the server — no JS shipped). Add `"use client"` at the top of a file to make it (and its tree) an interactive island that hydrates in the browser. Proven pattern: a thin server `page.tsx` (for metadata + auth) that renders one `"use client"` view containing the interactive UI.
- **Compose small components; don't grow one giant page.** A page that fetches, formats, and renders in one file can't be tested without standing up the whole app, and an agent extending it has one huge file to edit. Split along the data boundary:

  | Layer | Contains | How it's tested |
  |---|---|---|
  | `lib/*.ts` | pure functions — formatting, grouping, derivation. No React, no `db`. | direct unit tests, no DOM, no mocks |
  | `components/*.tsx` | presentational. Data arrives as **props**; writes go out through **callbacks**. Never calls `db.useQuery` itself. | `render(<C {...fixtures} />)` — no mocking, because there's no data layer to mock |
  | `app/**/page.tsx` + one `"use client"` container | the **only** place that touches `db` / `callFn`. Fetch, then hand plain data down. | `pylon verify`, or a container test that mocks just this boundary |

  Keeping the data boundary in exactly one module is what makes everything below it trivially testable. The `create-pylon` starters are generated in this shape — read one for a worked example.

- **Build on the UI kit that's already there.** Scaffolded apps ship `components/ui/` with shadcn primitives (`button`, `card`, `input`, `label`, `select`, `badge`, `table`, `textarea`), `lib/utils.ts` (`cn`), and a configured `components.json`. Use them, and style with the semantic tokens (`bg-background`, `bg-card`, `text-muted-foreground`, `border`) rather than hardcoded palette classes like `bg-zinc-50` — a raw `<input>` or a fixed color renders as an unstyled control next to the kit and breaks dark mode.

  Need a primitive that isn't there (dialog, dropdown, tabs, popover, …)? Add it rather than hand-rolling:

  ```sh
  bunx shadcn@latest add dialog     # npx if you're on Node
  ```

  `components.json` is preconfigured (new-york, zinc, `@/components/ui`), so the component lands with the right imports and tokens.

- The page receives props: `{ pathname, host, params, searchParams, auth, response, serverData }` — type them with `PageProps<{ slug: string }>` from `@pylonsync/react` instead of hand-rolling. **`pathname` is the PATH only** (`/blog/hello`), never the query — the router strips the query before the render and hands it over already parsed as `searchParams`. So read a query parameter from `searchParams.next`, NEVER `new URL(props.pathname).searchParams.get("next")`, which compiles and returns null on every request. (`url` is the same value under the old name and is deprecated.) `auth` is `{ user_id, is_admin, tenant_id, roles }` resolved from the shared session. `host` is the request host, lowercased, when the server trusts it (its own URL, `PYLON_TRUSTED_HOSTS`, or a ready customer domain attached with `ctx.domains`), else `""` — it is part of the SSR cache key, so a platform app can pick the customer from it and stay cacheable. **The request's `headers` and `cookies` are intentionally NOT props** — they're server-only and stripped from the hydration payload (a session cookie must never reach client JS), so reading them in a component body would hydrate-mismatch. Read request-derived data through `serverData` or a server function.

```tsx
// app/blog/[slug]/page.tsx  (server component)
import type { Metadata, PageAuth } from "@pylonsync/react";

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  return { title: `Post: ${params.slug}`, description: "…" };
}

export default function PostPage({ params, auth }: { params: { slug: string }; auth?: PageAuth }) {
  return <Article slug={params.slug} signedIn={Boolean(auth?.user_id)} />;
}
```

### Loading data during the server render (`serverData`)

A server component reads the DB during render through the `serverData` prop — a **read-only, policy-gated** handle (same store + policy gate as a query's `ctx.db`). Await it with React 19 `use()` inside `<Suspense>`; resolved values are replayed into the hydration payload so the client doesn't re-fetch. Writes are rejected (`SSR_WRITE_FORBIDDEN`) — mutations belong in functions.

```tsx
import { use, Suspense } from "react";
import type { PageProps } from "@pylonsync/react";

export default function Page({ serverData }: PageProps) {
  return (
    <Suspense fallback={<Skeleton />}>
      <PostList promise={serverData.list<Post>("Post")} />
    </Suspense>
  );
}
function PostList({ promise }: { promise: Promise<Post[]> }) {
  const posts = use(promise);
  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

`serverData` has `get` / `list` / `lookup` / `query` / `queryGraph` / `paginate` / `search` (same read shapes as `ctx.db`). For live, client-updating data prefer a `"use client"` island with `db.useQuery` instead.

**`serverData.fn(name, args)` (≥0.3.385)** — run a registered **query** function during SSR with the page's own auth (anonymous on public pages): `use(serverData.fn<Session[]>("getPublicSchedule", { eventId }))`. Use it when the safe public projection lives in a gated query (published-only rows, stripped fields) instead of open row policies — the query stays the single source of truth for SSR and client. Results replay through the hydration payload like other serverData reads. Mutations/actions are rejected (`FN_TYPE_MISMATCH`). Calling it on a signed-in request opts the render out of shared SSR caching (the query may read `ctx.auth`); anonymous renders stay cacheable.

### Navigation, images, metadata

- `import { Link, Image } from "@pylonsync/react"` — `<Link href>` = client-side nav; `<Image src width height>` = a built-in optimizer (emits `srcset`; pass `priority` for LCP).
- **`<Image>` `quality` and `w` are allowlists, not ranges.** An off-list value snaps to the nearest allowed one and the server logs it (`pylon dev` prints to the console) — the image renders, but NOT at the value you asked for. Bounding the set is what stops anyone minting unlimited cache entries.
  - `quality`: **50, 75, 90** (default 75). `quality={80}` is the usual mistake — it silently becomes 75.
  - `w`: `16,32,48,64,96,128,256,384` + `640,750,828,1080,1200,1920,2048,3840`.
  - `format`: `avif`, `webp`, `jpeg` — not snapped (no meaningful "nearest" codec); anything else falls back to `Accept` negotiation. Never SVG: rejected as input and output, it can carry script.
  - Need other values? Set `PYLON_IMAGE_QUALITIES` / `PYLON_IMAGE_DEVICE_SIZES` / `PYLON_IMAGE_IMAGE_SIZES` / `PYLON_IMAGE_FORMATS` (comma-separated). Prefer picking an allowed value over widening the list.
- SEO: `export const metadata: Metadata = {…}` (static) or `export async function generateMetadata(props)` (dynamic — keep it cheap, e.g. params→title). Fields: `title`, `description`, `canonical`, `robots`, `openGraph`, `twitter`, `icons`. Colocate `opengraph-image.png` / `icon.png` / `favicon.ico` next to a route and they're auto-wired.

### Code splitting

Every page is its own entry chunk, sharing one chunk with React + the runtime. That handles many routes; it does nothing for **one route with a heavy dependency**. A page that statically imports an editor puts the whole editor in its entry — and since `<Link>` warms sibling routes on sight, that weight lands on the first load of every page in the section, for a component most visitors never open.

`dynamic()` moves it behind a real `import()`: its own chunk, deliberately left out of the route's modulepreload set, fetched only when something renders it.

```tsx
import { dynamic } from "@pylonsync/react";

const Composer = dynamic(() => import("./Composer"), {
  loading: () => <ComposerSkeleton />,
});

// …then render <Composer /> behind whatever opens it.
```

Call it at **module level**, never inside a render — a `dynamic()` per render is a new component type each time and remounts the subtree. `ref` reaches the loaded component, so a deferred `forwardRef` editor still exposes its imperative handle.

`ssr` defaults to **false**, the opposite of Next, and deliberately: a Pylon page hydrates once after the whole document streams, so the safe contract is that the server HTML and the first client render are identical, which `ssr: false` guarantees by rendering the fallback in both. It's also the only mode that removes bytes from the first load — an `ssr: true` component must be in the client bundle before hydration, so it saves nothing and exists for organizing code, not weight.

Note the name collision: the route-segment export `export const dynamic = "force-static" | "force-dynamic"` is a **cache directive**, unrelated to this loader. Same word, different thing, both inherited from Next.

**Deferring one component isn't enough on its own.** `dynamic()` removes weight only if nothing else in the route imports the same library statically — a sibling component doing `import { H1, TEXT } from "@react-email/editor/ui"` drags the whole thing back in eagerly, and the only symptom is a heavy chunk in the route's preload set, which looks like a bundler bug. Check with `grep -o 'import[( ]*"[^"]*<chunk>[^"]*"'` against the built entry: a paren means deferred, no paren means something still imports it eagerly.

### File conventions (all optional, walked up from the page dir)

- `loading.tsx` → the route's pending state, in both directions: the Suspense fallback the SSR stream flushes first (set `export const streaming = true` on a page for progressive streaming), and what the client router paints over the page area when a `<Link>` navigation runs longer than ~100ms. Faster navigations swap straight to content, so it never flashes.
- `error.tsx` → error boundary; `not-found.tsx` → 404 boundary (call `notFound()` to trigger).
- `sitemap.ts` → `/sitemap.xml`, `robots.ts` → `/robots.txt`. Default export, **may be async** (enumerate dynamic pages from the DB). Types `Sitemap` / `Robots` from `@pylonsync/react`:

```ts
// app/sitemap.ts
import type { Sitemap } from "@pylonsync/react";
export default async function sitemap(): Promise<Sitemap> {
  const posts = await getPosts();
  return [
    { url: "https://x.com/", changeFrequency: "weekly", priority: 1 },
    ...posts.map((p) => ({ url: `https://x.com/blog/${p.slug}`, lastModified: p.updatedAt })),
  ];
}
// app/robots.ts → export default () => ({ rules: { userAgent: "*", allow: "/" }, sitemap: "https://x.com/sitemap.xml" })
```

### Client hooks & response control

- `import { useRouter, useSearchParams, usePathname, useParams, redirect, notFound } from "@pylonsync/react"` — for `"use client"` components.
- The `response` prop shapes the HTTP reply from a server component: `response.setStatus(404)`, `response.redirect("/login")`, `response.notFound()`, `response.setHeader(...)`, `response.setCookie(...)`.
- **Never `window.location` for in-app navigation** — use `<Link>` or `useRouter().push/replace`. A full document load tears down the sync engine and rebuilds it: fresh multi-tab election, fresh WebSocket, fresh initial pull, plus a flash of the old page. It's invisible when it works, so it shows up as "why is every login doing four pulls". The ONE case where a hard load is correct is an identity change — after login/logout you WANT a new document so SSR renders under the new session and the replica resets for the new user (this is why the templates' auth forms call `window.location.assign`). Redirecting inside an effect (`window.location.replace` in a landing page) is the common wrong version.

### Caching (SSR output cache)

Pages are **dynamic by default**. Two opt-ins make a render shareable (a hit skips the Bun render entirely):

- **Anonymous cache** — `export const revalidate = 60` (seconds). Stored + reused for ALL anonymous visitors. Cached ONLY if the render never read per-request identity — reading `props.auth`, setting a cookie via `response.setCookie`, a non-200, or streaming opts it out. (Request headers/cookies aren't page props, so there's nothing to accidentally read there.) `export const dynamic = "force-static"` caches until the next deploy; `"force-dynamic"` never caches. Use for fully public pages.
- **Auth-bucketed cache** — `export const cache = "auth-bucketed"` + `export const revalidate = 60`. Caches TWO identity-free shells keyed on whether the request is signed in. Read `props.session.exists` (a binary signed-in bit, **never** identity) to render a signed-in vs signed-out shell and still get a per-bucket hit. Reading real `props.auth` still opts out (output would be identity-specific).
  - **Purity contract:** an `auth-bucketed` page MUST be a pure function of its props. NEVER stash request data (auth/cookies/headers, or values derived from them) in module/global scope and render it on a later request — that leaks across users (same rule as Next: no request data in module scope).
  - CDN: bucket responses are browser-`private` by default (the origin still skips the render). A shared-CDN hit requires the operator to set `PYLON_SSR_BUCKET_CDN=1` after adding a CDN cache-key rule on session-cookie presence.

To show signed-in nav on a cacheable page, read `props.session.exists` (bucketed) — do NOT read `props.auth` server-side (that makes the render dynamic). Resolve full identity client-side after hydration.

**"Why isn't my page caching?"** → run `pylon diagnostics` or open the dev HUD; it reports the exact verdict + reason per route (see "Running the app").

### Performance

Ordered by how much they actually cost. The first two are where nearly all real
latency lives; the rest matter once those are clean.

**1. Don't serialize waterfalls.** `serverData` reads are promises — start them
all, then await together. Awaiting one before creating the next turns two 50ms
reads into 100ms:

```tsx
// Waterfall: the second read doesn't start until the first resolves.
const org = use(serverData.get("Organization", id));
const members = use(serverData.query("OrgMember", { orgId: id }));

// Parallel: both in flight, one wait.
const [org, members] = use(
  Promise.all([
    serverData.get("Organization", id),
    serverData.query("OrgMember", { orgId: id }),
  ]),
);
```

Independent sections should be separate `<Suspense>` boundaries so a slow one
streams in without blocking the rest — that's what `export const streaming =
true` is for.

**2. Ship less to the client.** Resolved `serverData` is replayed into the
hydration payload so the client doesn't re-fetch — which means over-fetching in
a server component inflates the HTML for every visitor. Select the fields the UI
renders; don't pass whole rows into a `"use client"` island to use two of them.

**3. Never keep mutable state in module scope.** The SSR runner is warm and
import-caches route modules, so a module-level variable persists **across
requests and across users**. This is the same purity contract as the
`auth-bucketed` cache, and it's a correctness bug before it's a performance one.

**4. Prefer `db.useQuery` to per-component `callFn`.** The synced replica already
dedupes and updates live; N components each calling `callFn` on mount is N
round-trips for data the client usually already has.

**5. Client-render hygiene** — the usual React rules, and the two that bite most:
never define a component inside another component (it remounts the whole subtree
every render), and derive values during render instead of syncing them in an
effect.

For the full catalogue — bundle analysis, memoization, hydration, SVG and DOM
detail — use Vercel's `react-best-practices` skill
(<https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices>);
70 rules ranked by impact. It's Next-flavoured, so read `next/dynamic` as a
plain `import()` and server actions as Pylon functions.

## Running the app

```bash
# One port — a Rust server serves the SSR frontend, the API, and the WebSocket (it runs your TypeScript on Bun).
pylon dev
```

That's it — no second terminal for the UI. `pylon dev` watches `app.ts` + `functions/` + `app/`, recompiles Tailwind, and live-reloads the browser. (A backend-only app runs the same `pylon dev`.) The first run creates `.pylon/dev.db` (SQLite) and auto-migrates. Set `DATABASE_URL=postgres://...` to target Postgres instead — the adapter is chosen at startup, and all schema/policy/function/SSR code is identical either way.

In production, use `pylon start` instead of `pylon dev`. Same server, no file watcher, blocks on the server thread so a fatal error exits the process and lets the supervisor (systemd / Docker / Fly init) restart cleanly. Two ways to run it:

- `pylon start app.ts` runs the source. The server needs the project and its `node_modules`.
- `pylon build` writes a production artifact to `dist/` (server bundle, client bundle, `public/`, manifest), and `pylon start dist` runs it with no source tree and no `node_modules`. Data paths (`PYLON_DB_PATH`, default `pylon.db`) resolve outside `dist/`. Browser targets, polyfills, CSS targets, and server externals go in `buildManifest({ build: { target, polyfill, css, server: { external }, include } })`. `pylon build --compile` also copies the `pylon` and `bun` binaries into `dist/bin/`. Docs: https://docs.pylonsync.com/operations/build

### Debugging — the dev HUD + `pylon diagnostics` (read this when iterating)

`pylon dev` surfaces the framework's hidden decisions so you don't guess. Same data, three ways:

- **Dev HUD** — a floating overlay (bottom-left, in the browser) showing each page's cache verdict + WHY, render mode + timing, sync connection + offline-outbox depth, and client error count.
- **`pylon diagnostics`** (machine-readable, for agents) — prints recent SSR renders: verdict (`cacheable` / `bucketed` / `dynamic`), the reason, and render time per route. `--json` for raw; `--port` if not 4321.
- **`GET /_pylon/dev/diagnostics`** — the JSON ring the CLI + HUD read.
- **`pylon dev` stdout** — one `[pylon:dev] SSR <route> → <verdict> · <ms> — <reason>` line per render.

When a page won't cache, returns no data, or is slow, check these FIRST — the verdict reason names the exact cause (e.g. "read props.auth", "not opted in", "the render set a cookie"). Dev-only; absent in prod.

### Design mode (for design tools)

Set `PYLON_DESIGN_MODE=1` with `pylon dev` to get a static, source-mapped render of any page for a design canvas. Dev-only; every part 404s in prod.

- **`PYLON_DESIGN_MODE=1`** — the SSR runner stamps every DOM element under `app/`, `components/` and `.design/` with `data-pylon-src="app/x/page.tsx:12:8"` (file, 1-based line, column of the `<`). Components are not stamped; browser bundles are unchanged.
- **`X-Pylon-Design: 1`** request header — the page renders with no hydration tail (no `__PYLON_DATA__`, no module script), no dev HUD, no live-reload snippet, the stylesheet inlined with no size cap, and `<base href="http://127.0.0.1:<port>/">` first in `<head>` so relative assets resolve inside a `srcdoc` iframe. Response is `Cache-Control: no-store` and never written to the SSR cache.
- **`GET /_pylon/dev/render?component=<rel module path>&layouts=<csv>&path=<url path>`** — render a module that is not a route (for example `.design/variants/v1`) with the given layout chain, as a design render. `component` and `layouts` are project-relative paths without extension and must exist inside the project. `path` defaults to `/`. Requires `Authorization: Bearer <PYLON_DEV_FILE_API_TOKEN>` when that env is set.
- **`X-Pylon-Design-Viewer: <userId>` or `anon`** — render as that user (their most recent session's org, roles, admin flag), so pages that redirect anonymous visitors still render. Only on design renders, and only with `PYLON_DEV_FILE_API_TOKEN` set and sent; otherwise 401.

## Deployment

Production env vars to set:

```bash
PYLON_DB_PATH=/data/pylon.db
PYLON_FILES_DIR=/data/uploads
PYLON_SESSION_DB=/data/sessions.db
PYLON_CORS_ORIGIN=https://your-web-ui.vercel.app   # EXACT origin — "*" refused in prod
PYLON_DEV_MODE=false
```

Scaffolding:

```bash
pylon deploy                     # default — actual hosted deploy to Stack0 Cloud
pylon deploy --target fly        # Dockerfile + fly.toml
pylon deploy --target docker     # Dockerfile
pylon deploy --target compose    # docker-compose.yml + Dockerfile
pylon deploy --target workers    # Cloudflare wrangler.toml (experimental)
pylon deploy --target systemd    # VPS unit file
pylon deploy --target manifest   # just regenerate manifest + client bindings
```

For Fly.io the common pattern is a 1GB volume mounted at `/data` with `auto_stop_machines = "stop"` — idle machines sleep and wake on request.

### CLI ops surface (Stack0 Cloud)

Once logged in (`pylon login`, or via the dashboard's "Hand off to your coding agent" card → `pylon login --code XXXX-XXXX`), the CLI covers every dashboard operation. Use these instead of clicking through `cloud.stack0.dev` for anything scripted.

```bash
pylon whoami                             # account + cloud + active project
pylon projects list                     # all projects you can see
pylon projects create my-app            # create + provision a project, set it as context
pylon projects use my-app               # set current project for this dir
pylon secrets list / set KEY=v / rm KEY / import .env
pylon logs --limit 100                   # last N request-log rows, then exit
pylon logs tail                          # 2s-polling stream (never exits — use --limit instead)
pylon status                             # uptime / requests / jobs / WS clients
pylon restart --yes                      # cycle the machines, same code
pylon deployments list / logs [<id>] / rollback <id> --yes
pylon domains list / add HOST / verify HOST / rm HOST
pylon db list / backup / restore <id> --yes
pylon data entities / list <E> / get <E> <id>
pylon members list / invite EMAIL [role]
pylon billing                            # plan, month-to-date + projected charge
pylon billing upgrade                    # move the org to Pro (Stripe checkout)
```

Every command accepts `--json` for piping to `jq`. Project context resolves from `--project` flag → `$PYLON_PROJECT` → `.pylon/project` file → interactive picker. The `.pylon/project` file is what `pylon projects use` writes; subsequent commands in that directory tree auto-target.

**Start with `pylon whoami`** when a command targets the wrong thing. It reports the account, the cloud origin, and which project is active *and where that slug came from* — a `.pylon/project` inherited from a parent directory is the usual culprit. It also flags a slug that resolves locally but names no project on the account.

**Destructive commands refuse to run unattended without `--yes`**: `restart`, `deployments rollback`, `db restore`, `secrets rm`, `domains rm`. Under `--json` or a non-TTY there is no prompt to answer, so the command errors out instead — pass `--yes` in scripts.

**API docs.** The server generates an OpenAPI **3.1** spec from the manifest and serves it at `GET /api/openapi.json`; `pylon codegen openapi` writes the same document to `pylon.openapi.json` without booting anything. Point Mintlify, Scalar, or Redoc at either. Every query/mutation/action appears at its real endpoint, `POST /api/fn/<name>`, with `auth: "public"` functions marked as needing no credentials; `internal: true` ones are omitted because they aren't externally callable. The spec is **admin/dev-only by default** — it enumerates your whole surface — so set `PYLON_OPENAPI_PUBLIC=true` if you want hosted docs to fetch it anonymously. A spec with entities but no functions means `app.ts` isn't calling `discoverFunctions()`.

**The runtime version comes from package.json** (pylon ≥ 0.4.8). The Rust binary and the `@pylonsync/*` packages ship from one release and talk to each other over the function protocol, which carries no version handshake — so a mismatch surfaces as a confusing runtime error, not "version mismatch". A cloud deploy therefore boots the machine on the runtime matching the version the build installed: change the dependency, `pylon deploy`, done. There is no runtime to bump. `pylon runtime` shows what a project is on and still moves it explicitly when you need a binary-only change without a rebuild; a machine pinned to an image *digest* is left alone, since that's an explicit choice.

**Two different "update" commands, don't mix them up.** `pylon update` bumps every `@pylonsync/*` dependency in the project's package.json files. `pylon upgrade` (pylon ≥ 0.4.6) updates the **pylon binary itself** to the latest release — `pylon upgrade --check` reports without changing anything. A CLI installed by npm or cargo is left alone; upgrade prints the command that manages it. Before 0.4.6, `pylon upgrade` opened a Stripe checkout; that is `pylon billing upgrade` now.

**`pylon restart`** (pylon ≥ 0.4.5) cycles the running process on the code already deployed. Reach for it when the app is wedged or crash-looping — `pylon deploy` rebuilds for no reason and `deployments rollback` ships older code. A stopped machine is started rather than restarted, and multi-region projects cycle one region at a time. Exits non-zero if any region failed to come back, so a script won't move on from a half-recovered app. Requires org owner or admin.

**Project creation** (pylon ≥ 0.3.317): `pylon projects create <slug> [--name <name>] [--org <org-slug>] [--region iad] [--db sqlite|postgres] [--no-wait]`. Creates the project, waits for the Fly machine to provision (~30–60s; Postgres adds a managed-DB provision), pins it as the local context, and prints the live `https://<slug>.stack0.app` URL — so login → create → deploy runs end-to-end without the dashboard. `--org` is only needed when the account belongs to multiple orgs. On older CLI versions (or if the account has no org yet), create the project in the dashboard and run `pylon projects use <slug>` instead.

### Multi-machine (horizontal scaling)

One machine is the recommended shape (a single machine serves thousands of rps with a CDN in front) — scale up first. When you do need more than one machine (pylon ≥ 0.3.315):

```bash
DATABASE_URL=postgres://…          # entities, auth, sync, jobs, workflows
PYLON_CLUSTER_BUS=redis://…        # self-hosted realtime fanout
```

Postgres provides shared entities, auth state, sync state, jobs, and workflows. Workers claim jobs and workflows with short leases. Another machine can recover work after a lease expires. Execution is at least once, so job and workflow handlers must be idempotent. During a rolling release, each machine claims only jobs that have a local handler.

Redis relays WS/SSE change events, presence, and CRDT frames for self-hosted deployments. Pylon Cloud configures its built-in relay and does not add Redis to the project. Boot-time DDL is serialized across machines. One elected scheduler adds each cron fire to the shared queue. SQLite mode is single-machine by definition.

Known per-machine semantics (documented, not bugs): rate-limit counters are per machine (N machines ≈ N× the configured limit — set PYLON_RATE_LIMIT_MAX accordingly), and the SSR output cache is per machine (put a CDN in front).

Keeping a project current: `pylon update` bumps every @pylonsync/* dependency (workspace members included, `workspace:*` pins untouched) to the latest release and reinstalls — then `pylon verify`.

## Gotchas & rules

- **Type names** — schema (`field.*`) and validator (`v.*`) both accept two naming conventions so you don't have to remember which camp a given API belongs to:

  | Type | Schema (`@pylonsync/sdk`) | Validator (`@pylonsync/functions`) |
  |---|---|---|
  | string | `field.string()` | `v.string()` |
  | integer | `field.int()` | `v.int()` |
  | float | `field.float()` or `field.number()` | `v.float()` or `v.number()` |
  | boolean | `field.bool()` or `field.boolean()` | `v.bool()` or `v.boolean()` |
  | datetime | `field.datetime()` | `v.datetime()` or `v.string()` |
  | richtext | `field.richtext()` | `v.richtext()` or `v.string()` |
  | FK id | `field.id("X")` | `v.id("X")` |

  What still **doesn't exist**: `v.money()`, `v.enum()`, `v.timestamp()`. When in doubt, source is at <https://github.com/pylonsync/pylon/tree/main/packages>.
- **Every function file must `export default`** the `mutation()/query()/action()` result. Named exports are ignored.
- **`functions/*.ts` file names are the RPC names.** `functions/create-issue.ts` would be called as `create-issue` — prefer camelCase to match JS identifier conventions.
- **Generated files** (`pylon.manifest.json`, `pylon.client.ts`) are rebuilt on every `pylon dev` invocation. Never edit by hand.
- **Workspace deps** in examples use `workspace:*` — if you scaffold outside the Pylon monorepo, replace with the published version.
- **Dev mode is generous by default** (CORS `*`, rate limits raised). Production requires explicit `PYLON_CORS_ORIGIN` — `*` is rejected.
- **Policies filter silently on read** but throw `POLICY_DENIED` on write. If a list query returns fewer rows than expected, check read policies.
- **Live queries need indexes** on filter columns. A `db.useQuery("Message", { where: { roomId } })` with no index on `roomId` will still work but scale O(N) per change.
- **Always call `ctx.error(code, msg)`** instead of throwing plain `Error` — plain errors become generic `HANDLER_ERROR` on the client with the real message stripped.

## Quick decision guide

| User wants | You write |
|---|---|
| A new table | New `entity(...)` in `app.ts` + matching `policy(...)` + `buildManifest({ entities: [...], policies: [...] })` |
| A list in the UI | `db.useQuery("Entity", { where: {...} })` — make sure the `where` keys are indexed |
| A live counter / availability across tabs | `db.useQuery` over a public-read projection entity the mutation maintains — NOT `useReactiveQuery` |
| A server-side join / computed value, live | `db.useReactiveQuery("fnName", args)` (leader-view; see footgun) |
| Live full-text search | `db.useSearch("Entity", { query, facets })` + `.search({...})` on the entity |
| Presence / cursors / typing | `useRoom(roomId, userId)` — ephemeral, not persisted |
| An AI chat / agent that streams its answer | `action()` with `ctx.llm.stream(req, (e) => ctx.stream.write(e.text))` + `db.streamFn` on the client (auto-resumes on disconnect; `onStreamId` + `resumeStream` survive reloads); set `timeout:` when a tool call can be silent past the idle timeout (30s default; each stream event resets it) |
| Agent output fanned to every CONNECTED watcher (second device, no HTTP caller) | `ctx.rooms.broadcast(room, topic, data)` from the mutation/action; live-only, no replay — persist the stream id for gap-proof delivery |
| Multiplayer game / tick sim | `useShard(shardId, { subscriberId })` |
| A form submission / write | A `mutation()` in `functions/X.ts` + `await callFn("X", args)` in the component (or `db.useMutation` for optimistic UI) |
| Auth-gated functions | `auth: "user"` is the default on every `query` / `mutation` / `action`. Anon AND guest callers get `401 AUTH_REQUIRED` before the handler runs. `auth: "guest"` for pre-login callers (carts, public demos), `auth: "public"` for webhooks/healthchecks, `auth: "admin"` for ops. CRITICAL on actions — policies don't gate them. The same gate applies on `/api/webhooks/<name>` and to `db.useReactiveQuery` subscriptions (which also accept only `query` functions), so a webhook receiver must declare `auth: "public"` and verify the provider's signature itself. |
| Access rules | `policy({ allowRead: "...", allowInsert: "..." })` — not middleware, not function guards |
| Email / external API | `action()` (not `mutation()`) |
| A one-shot deferred job | `ctx.scheduler.runAfter(delayMs, "fnName", args)` (or `runAt(unixMs, ...)` — Unix ms, not an ISO string) inside a mutation/action |
| A recurring job | a **cron**: `cron("0 * * * *", "fnName")` (import `cron` from `@pylonsync/sdk`) in `buildManifest({ crons: [...] })`; point it at an `internal: true` function |
| An LLM agent with tools + a persistent conversation | **`agent()`** — default-export `agent({ system, tools: { name: { description, args: {v...}, handler(ctx, input) } }, model?, maxSteps? })` from `functions/<name>.ts` (import `agent` from `@pylonsync/functions`). Compiles to a streaming action: call with `streamFn("<name>", { input, runId? })`. The framework runs the tool loop, validates tool args, streams tokens + `event: tool` frames, and persists every turn into the injected synced entities `AgentRun`/`AgentMessage` (owner-scoped; clients can't write them). Live transcript on any device: `useAgentRun(runId)`; token-level tail from another device: `resumeStream(run.streamId)`. Continue a conversation by passing `runId`. Sending while it generates QUEUES the message (`queued: true`) and the loop folds it in at its next turn boundary, so a chat composer never has to be disabled. Stop a run with `cancelAgentRun(agentName, runId)` (or `{ runId, cancel: true }`) — durable on the run row, so it reaches a loop on another machine; within ~2s it aborts a model response in flight (the provider stops generating) or a running tool's `ctx.signal`. `maxSteps` defaults to 64 per invocation. Failures mark the run `failed` with the error on the row. Requires a signed-in caller (auth "user" default) + a configured LLM provider. Webhooks/jobs have no user: from an `internal: true` or admin (elevated) action call `ctx.agents.run("<name>", { input, as: { userId, admin? }, context?, runId? })` — the run belongs to that user, and every tool handler gets `(ctx, input, run)` with `run.context` = the server-set context (stored on `AgentRun.context`), so tools find their conversation without smuggling ids through the title. Never mint a session over loopback for this. |
| A multi-step process that must survive restarts (onboarding sequence, agent pipeline with approval gates, dunning) | a **durable workflow**: default-export `workflow(name, async (wf, ctx) => {...})` (import `workflow` from `@pylonsync/functions`) from a file in `workflows/` (sibling of `functions/`). `wf.step(name, fn)` runs exactly once (replayed from its recorded output after that); `wf.sleep("24h")` and `wf.waitForEvent(name)` pause without burning compute. Start from app code with `await ctx.workflows.start("name", input)` (mutations/actions; returns `{id}` immediately), deliver events with `ctx.workflows.sendEvent(id, event, data)` (buffered when the run isn't waiting yet, so none are lost); `wf.waitForEvent(name, { timeout: "60s" })` resolves `null` on timeout; `ctx.workflows.start(name, input, { key })` keeps one active run per key; `ctx.workflows.list({ key, status: "active" })` + `ctx.workflows.cancel(id, { reason })` stop runs from code; the admin HTTP routes (`POST /api/workflows/start`, `/api/workflows/<id>/event`) drive the same engine for operators. RULE: the step/sleep/waitForEvent call sequence must be deterministic across replays — branch on `wf.input` and step outputs only, and give steps unique names. |
| Deploy | `pylon deploy --target fly` then `fly deploy . --config fly.toml` |

### Agent tooling — verify, policy dry-runs, MCP (pylon ≥ 0.3.313)

Three commands exist specifically so you can check your own work:

```bash
# Prove the app actually serves: boots it on a free port (or targets a
# running one with --url), checks /health, GETs every static route, and
# fetches every referenced JS/CSS asset (catches "renders but ships no
# hydration/styles"). Exit 0 only when nothing failed. --json for machine output.
pylon verify
pylon verify --url https://myapp.stack0.app

# Deploy. WAITS for the build by default, prints status transitions, and dumps
# the build log if it fails — so a non-zero exit means the deploy really failed,
# not just that queuing worked. Ctrl-C is safe; the build keeps running.
pylon deploy
pylon deploy --no-wait          # fire-and-forget (CI that tracks status elsewhere)

# Same, plus walk the live URL with the `pylon verify` checks once it flips:
pylon deploy --verify

# Dry-run a policy expression with the PRODUCTION evaluator before you
# ship it — allow/deny + the exact comparison that failed. Exit 0=allow, 1=deny.
pylon policy test 'auth.userId == data.ownerId' --auth userId=u1 --row '{"ownerId":"u2"}'
# An update rule: --row is the stored row, --patch the write. Checks both rows.
pylon policy test 'auth.tenantId == data.orgId' --auth userId=u1,tenantId=t1 \
  --row '{"orgId":"t1"}' --patch '{"orgId":"t2"}'
```

And a running app can be attached directly to your tool loop over MCP:

```bash
claude mcp add pylon -- pylon mcp --url http://localhost:4321
```

which exposes `pylon_schema` (entities/policies/routes/functions), `pylon_list` / `pylon_get` (entity reads — row policies apply, no extra authority), `pylon_call` (functions), `pylon_policy_test`, and `pylon_verify`.

Per-route CSS strategy: `export const inlineCss = true` on a page inlines the compiled stylesheet into that route's SSR `<head>` (kills the render-blocking round trip — right for cold-traffic landing pages); `false` forces the cached `<link>` (right for logged-in pages, where the immutable sheet is fetched once and free forever). Unset defers to `PYLON_SSR_INLINE_CSS`. Sheets over 32KB always link.

Dev-mode failures are disclosed where you'll see them: unhandled function errors return `Internal handler error (dev): <message> [at <file:line>]` in the HTTP response (prod stays masked), and a failed Tailwind compile paints a red banner on every page instead of silently serving unstyled.

## Before you finish a task

- Run `bun run app.ts` in the project root — if it errors, the manifest won't build and `pylon dev` will fail silently on function load.
- Run `pylon verify` — it boots the app and fails on any route/asset that doesn't serve. This is the cheap end-to-end check; don't skip it.
- Run `pylon lint` — flags wide-open dev policies (`allow*: "true"`) and other policy smells before they ship. Tighten what it reports.
- **Test in tiers, cheapest first.** Tier 1: pure helpers in `lib/` (milliseconds, no DOM). Tier 2: components with fixture props via `@testing-library/react` (happy-dom is preloaded through `bunfig.toml`). Tier 3: functions/policies through `pylon policy test` and `pylon verify`. If a component is hard to test, it's usually because it fetches its own data — lift that to the container.
- Run `pylon test` — discovers `*.test.ts` / `*.test.tsx` under `tests/` (or `functions/`) and runs them with Bun's test runner (`import { test, expect } from "bun:test"`).
- If you added a function, verify it's discoverable by opening the project and checking that `pylon dev` logs list your new function name in the `Loaded N functions` output.
- If you changed an entity, schema auto-migration runs — but destructive changes (dropping a required column) will refuse to apply without bumping `manifest.version`.
- If you wrote or changed a policy, dry-run it: `pylon policy test '<expr>' --auth ... --row ...` for both the allow case AND the deny case.

## Beyond the React quickstart — what's available

This skill focused on the React/TS happy path. Pylon has more — fetch the docs page when these come up:

### Auth (`/auth/*` in the docs)
- **Magic codes** (`/api/auth/magic/send` + `/verify`) — recommended sign-in flow. 6-digit, 10-min expiry, throttled.
- **Email + password** (`/api/auth/password/register` + `/login`) — Argon2id-hashed.
- **OAuth** — Google + GitHub built in (`/api/auth/login/:provider` + `/callback/:provider`). CSRF-protected via state tokens.
- **Sessions** — opaque 256-bit tokens, 30-day default. `/api/auth/refresh`, `/sessions` GET/DELETE for management.
- **Trusted server-side mint** — `POST /api/auth/sessions/trusted-mint`. HMAC-signed (`X-Pylon-Trusted-Signature: hex(HMAC_SHA256(PYLON_TRUSTED_SECRET, ts + "." + body))`), ±5min freshness window. Reach for this when another trusted system (Stripe Checkout, custom IdP) has verified the email and you want to skip the magic-link roundtrip. Opt-in: 404 unless `PYLON_TRUSTED_SECRET` is set.
- **RBAC** — roles on the session; `auth.hasRole('x')` in policies. `admin` role bypasses everything.
- **Multi-tenant** — `auth.tenantId` from `/api/auth/select-org`; row-scoped policies via `data.orgId == auth.tenantId`.
- **API keys** — via the `api_keys` plugin, scoped + rotatable + Argon2-hashed.

### Plugins (`/plugins/*` in the docs)
Built-ins, declared in `manifest.plugins`:
- **Security**: `rate_limit`, `cors`, `csrf`, `net_guard` (SSRF defense), `totp`, `jwt`, `api_keys`, `session_expiry`, `password_auth`
- **Data hygiene**: `validation`, `slugify`, `timestamps`, `computed`, `cascade`, `versioning`, `soft_delete`, `tenant_scope`, `organizations`
- **Search & AI**: `search` (FTS5 + facets — configured on the entity via `.search({...})`, not the plugin list), `ai_proxy`
- **Integrations**: `file_storage` (S3/R2/Stack0), `cache`, `cache_client` (Redis), `email`, `webhooks`, `stripe`, `feature_flags`, `audit_log`

**npm plugins** (imported, not declared in `manifest.plugins`): `@pylonsync/stripe` (web billing: checkout, portal, webhook, plan limits, trials), `@pylonsync/revenuecat` (native in-app purchases: the RevenueCat webhook and a server-verified `syncEntitlements` action write one `RcEntitlement` row per user + entitlement that syncs to every device; `syncEntitlements` accepts guests by default (`syncAuth: "user"` to require an account); app code gates with `hasEntitlement(rows, "pro")` from **`@pylonsync/revenuecat/client`** — the package root imports `@pylonsync/functions` and breaks Metro/browser bundles). Native sign-in for mobile apps: `POST /api/auth/native/apple|google` verifies a platform id_token against the provider's JWKS (audiences from `PYLON_APPLE_NATIVE_CLIENT_IDS` / `PYLON_GOOGLE_NATIVE_CLIENT_IDS`); `@pylonsync/react-native` exposes `nativeSignIn`, `guestSession`, `sendEmailCode`/`verifyEmailCode`, `signOut`, `deleteAccount`. **Account deletion:** `DELETE /api/auth/account` removes the User row and Pylon's auth rows only. Declare `auth({ onDeleteAccount: "deleteMyData" })` and write that function (`internal: true`, args `{ userId }`, runs as the user) to delete the app's own rows; a throw aborts the deletion. **Mobile session boot:** call `init()` (`@pylonsync/react-native`) before anything reads `db.sync`, and read `useSession().resolved` — `userId` is null until `/api/auth/me` answers, which is not "signed out".

**Vector search is a field type, not a plugin.** Declare `embedding: field.vector(1536)` (always server-only; dims must match the embedding model), fill it with `ctx.llm.embed(texts)` (OpenAI `text-embedding-3-small` by default when `OPENAI_API_KEY` is set; `PYLON_EMBEDDINGS_PROVIDER=voyage` + `VOYAGE_API_KEY` for Voyage), and query with `ctx.db.vectorSearch("Doc", { field: "embedding", vector, limit, metric?, filter? })` — exact k-NN, cosine default, hits `{id, score, doc}` best-first with vector fields stripped from `doc`. HTTP: `POST /api/vector-search/<Entity>`. Ctx rules compose the usual way: `vectorSearch` lives on `ctx.db` (queries + mutations; actions have no `ctx.db`), and `embed` is NOT available in queries (reactive re-runs re-bill). Standard flow: action embeds → `ctx.runQuery` a query that searches, or `ctx.runMutation` to store the vector. Do NOT put `vector_search` in `manifest.plugins`; that key does nothing.

**Not implemented — do NOT declare this.** `mcp` appears in the roadmap catalog (`pylon plugins list`) but has no implementation behind it; putting it in `manifest.plugins` does nothing. For MCP, use the CLI's `pylon mcp` (see above) — it is not a manifest plugin.

### Clients (`/clients/*` in the docs)
- `@pylonsync/sdk` — schema DSL + manifest builder
- `@pylonsync/react` — hooks (covered in this skill)
- `@pylonsync/react-native` — Expo SQLite-backed offline replica
- `@pylonsync/next` — Server Actions, RSC data fetching, middleware auth
- `@pylonsync/sync` — sync engine standalone (Vue, Svelte, Solid, vanilla)
- `@pylonsync/loro` — Loro CRDT integration for collaborative editing
- **Swift SDK** at `packages/swift/` — `PylonClient`, `PylonSync`, `PylonRealtime`, `PylonSwiftUI`. iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, Linux. Codegen via `pylon codegen client --target swift`.

### Stack0 Cloud
Managed Pylon at `cloud.stack0.dev`. Same binary, same APIs.
- `pylon login` → `pylon projects create <slug>` → `pylon deploy`
- Custom domains via `pylon domains add`
- Environment vars via `pylon env set/list/unset`
- Includes: managed Postgres, TLS, magic-link email, OAuth (your creds), file storage, Studio, logs/metrics
- Pricing: usage-based, no monthly minimums; free tier covers small projects

### Stack0 Analytics — the relay is a FUNCTION, not a route
Hosted at `analytics.stack0.dev`. No package to install; a script tag plus one HTTP endpoint. Full code: https://www.stack0.dev/docs/sdk/analytics

The bare tag (`<script defer src="https://analytics.stack0.dev/track.js" data-site="SITE_KEY">`) only works on a site with no server of your own. **Anywhere you control the server — which includes every Pylon app — relay through your own origin**, or the Analytics CORS allowlist refuses the browser's preflight and the install looks exactly like "no traffic yet".

Do NOT reach for the Next.js recipe. `/api/fn/*` is Pylon's own namespace, so `app/api/fn/ingestEvent/route.ts` is never matched, and there is no `next.config.js` to rewrite in.
- `functions/ingestEvent.ts` — an `action` with `auth: "public"` that forwards `ctx.request.rawBody` to `https://analytics.stack0.dev/api/fn/ingestEvent` and returns the upstream JSON **verbatim** (`track.js` reads `visitorId` off it). Only actions get `ctx.request`. Forward `rawBody`, not `args` — the beacon carries fields your arg list does not declare. Copy `user-agent`, `x-forwarded-for`, and your edge's geo headers (`cf-ip*` or `x-vercel-ip-*`) or every visitor lands at their country's centre.
- Name it `ingestEvent` and `track.js` derives the path itself; any other name needs `data-endpoint`, whose value must contain `/api/fn/` or it is read as an origin.
- `app/rt/track.js/route.ts` — a `RawRouteHandler` that fetches and caches `track.js`, so an ad blocker that knows the Analytics host does not take it out. Load it as `<script defer src="/rt/track.js" data-site="SITE_KEY" />` from `app/layout.tsx`.
- `stack0Analytics()` is a **browser global** and Pylon renders on the server: call it from an event handler or effect, never during a render. A no-JS `<Form>` + route handler has no client code left to run, so POST the event from the handler.
- Never send `revenueCents`, `currency` or `customerId` through `ingestEvent` — the site key is public and cannot authenticate money. Revenue arrives by Stripe webhook to `/api/fn/stripeRevenue`.

### Stack0 Feedback — a script tag and a guest session
Hosted at `feedback.stack0.app`. Boards, votes, comments, roadmaps, changelogs. Full API: https://www.stack0.dev/docs/sdk/feedback

- Embed: `<script src="https://feedback.stack0.app/widget.js" data-project="SLUG" defer></script>`, straight into `app/layout.tsx`. Pylon server-renders it, so you write no client code.
- **There is no API key and no MCP server.** Public reads take no credential: POST JSON to `/api/fn/portalView` `{ slug }`, `portalPostView`, `portalRoadmapView`, `portalChangelogView`, `similarPosts`. An unknown, unpublished or archived portal returns `null`.
- Writing on someone's behalf takes a session, not a key: `POST /api/auth/guest` returns `{ token }`, then send `authorization: Bearer <token>` to `submitPost`, `toggleVote`, `addComment`. Call `similarPosts` first and vote on a match rather than filing a duplicate.
- Reading your own board from your own app is a plain `fetch` inside a normal query.

### Compare-vs-X pages
If the user asks "Pylon vs Convex/Supabase/Firebase/Colyseus/Playroom/Nakama", point them at `/compare/<vendor>` in the docs — each page has a structured comparison with sources.

## Swift / iOS / macOS specifics

When the user is in a Swift project (Xcode, `Package.swift`, `*.swift` files):

- **Install** via SPM: `.package(url: "https://github.com/pylonsync/pylon-swift.git", from: "0.3.0")`
- **Auth**: `try await client.startMagicCode(email:)` then `try await client.verifyMagicCode(email:code:)`
- **Sync**: `await SyncEngine(config: cfg, client: client, persistence: SQLitePersistence(...))`, then `await engine.start()`
- **Mutations**: `try await engine.insert("Todo", ["title": .string("x")])` (optimistic, queued, idempotent). Throws `MutationRejectedError` (`code`, `message`) after rolling back when the server rejects the write; returns when the server applies it or queues it offline.
- **SwiftUI**: `@StateObject var todos = PylonQuery<Todo>(engine: engine, entity: "Todo")` — `todos.rows` re-renders on change
- **CRDTs**: `PylonLoroDoc(entity:rowId:)` then `await crdtDoc.attach(to: engine)` — uses `loro-swift` internally
- **Codegen**: `pylon codegen client manifest.json --target swift --out PylonGenerated.swift` produces typed structs + `PylonClient` extensions
- **Linux**: works via `FoundationNetworking`; needs `apt-get install libsqlite3-dev`

The Swift SDK is at full TS-sync parity — same wire format, same crash-safety, same offline behavior. CRDT logic is shared with TS via the same Rust Loro core.

Reference example: `examples/swift-todo/` is a complete SwiftUI iOS/macOS app.
