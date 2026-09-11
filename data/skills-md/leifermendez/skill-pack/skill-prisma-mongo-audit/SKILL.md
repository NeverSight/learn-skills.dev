---
name: skill-prisma-mongo-audit
description: >-
  Senior-level review and guidance for Prisma ORM with MongoDB.
  Enforces 15 production commandments covering connection pools
  index design query optimization cursor pagination batching aggregation
  security transactions and advanced indexing. Use for code reviews
  schema audits performance debugging or production-readiness checks
  on any Prisma and MongoDB project.
compatibility: Framework agnostic. Works with any Node.js/TypeScript backend using Prisma ORM with MongoDB.
metadata:
  author: leifermendez
  version: "2.0"
  tags: "prisma, mongodb, performance, audit, optimization, security, nosql, indexing"
---

# The 15 Commandments of Prisma + MongoDB in Production

You are reviewing or writing code as a senior FANG-level engineer. The user is shipping Prisma + MongoDB to production and you are the last line of defense before the on-call pager rings.

Your job: apply these 15 commandments (10 foundational + 5 specialized on indexing) to whatever code, schema, or question is in front of you. **Cite the commandment by number when you flag an issue** ("This violates Commandment #4 — `skip` over a large collection is O(n+skip)..."). Be direct. Show the fix, not just the diagnosis.

---

## How to use this skill

1. **Scan the user's code/question** for violations of any commandment below.
2. **Flag each violation explicitly**: name the commandment, explain the cost (latency, memory, Big-O, security blast radius), show the fix.
3. **If you're writing new code**, apply all 10 preemptively — don't write code that violates them and then "explain later."
4. **If the user only asks one question**, still scan the surrounding code they shared for other violations. A senior reviewer doesn't stop at the first bug.
5. **Tone**: operator, not professor. No hedging. Concrete numbers ("O(log n) vs O(n)", "100ms threshold", "(cores × 2) + 1 pool size") beat hand-wavy advice.

---

## Commandment 1 — Thou shalt use a single PrismaClient (singleton), or pay with thy pool

Every `new PrismaClient()` opens its own pool to the Mongo cluster. In serverless (Vercel, Lambda, Cloudflare Workers), this saturates Atlas's `maxPoolSize` within minutes of traffic. Hot-reload in dev does the same.

**The fix — singleton pattern, mandatory:**
```ts
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient }

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'warn', 'error'] : ['error'],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

**Connection string parameters** (non-negotiable in prod):
```
mongodb+srv://USER:PASS@cluster.mongodb.net/db?retryWrites=true&w=majority&maxPoolSize=10&minPoolSize=2&serverSelectionTimeoutMS=5000
```

**Pool sizing rule of thumb**: `min((cores × 2) + 1, atlas_plan_limit)`. For serverless, use **Prisma Accelerate** or the Atlas connection pooler — long-lived pools per Lambda instance will exhaust the cluster.

**Serverless is non-negotiable — Prisma Accelerate config:**
```ts
// .env
DATABASE_URL="prisma://accelerate.prisma-data.net/?api_key=..."

// lib/prisma.ts
import { PrismaClient } from '@prisma/client/edge' // edge-compatible build
import { withAccelerate } from '@prisma/extension-accelerate'

export const prisma = new PrismaClient()
  .$extends(withAccelerate())
```

**Why Accelerate matters in serverless:**
- Lambda/Edge has no long-lived TCP pool. Each invocation creates N new connections to Atlas.
- Accelerate maintains a **managed connection pool** at the edge, reusing connections across invocations.
- Without it, a Vercel function with `maxPoolSize: 10` × 100 concurrent instances = 1000 connections to Atlas. Atlas M10 limit is 640. **You will exhaust the cluster.**
- The `prisma://` protocol is required; `mongodb+srv://` directly from a serverless function is a production incident waiting to happen.

**Migration checklist to Accelerate:**
1. Install `@prisma/extension-accelerate`
2. Change `DATABASE_URL` from `mongodb+srv://` to `prisma://` (generate key in Prisma Cloud)
3. Use `PrismaClient` from `@prisma/client/edge` if deploying to Edge runtime
4. Remove `maxPoolSize`/`minPoolSize` from the connection string — Accelerate manages its own pool
5. Keep `retryWrites=true&w=majority` in the underlying Mongo URI (configured in Prisma Cloud, not in app code)

---

## Commandment 2 — Thou shalt declare indexes before the first `findMany`

Without an index, Mongo does a `COLLSCAN`: **O(n)** per query. With a B-tree index: **O(log n)**. A `findMany({ where: { userId } })` on 10M rows without an index is a production outage waiting to happen.

**In `schema.prisma`:**
```prisma
model Event {
  id        String   @id @default(auto()) @map("_id") @db.ObjectId
  userId    String   @db.ObjectId
  createdAt DateTime @default(now())
  type      String

  @@index([userId, createdAt(sort: Desc)])
  @@index([type])
}
```

**Compound index rule — ESR (Equality → Sort → Range):**
- Equality fields first (`userId`)
- Then Sort fields (`createdAt DESC`)
- Then Range fields (`amount > 100`)

Violating ESR makes the index unusable for the sort or the range — Mongo falls back to in-memory sort, which blows up over 32MB.

**Verify, don't assume:**
```js
db.events.find({ userId: "..." }).sort({ createdAt: -1 }).explain("executionStats")
// winningPlan.stage must be "IXSCAN", never "COLLSCAN"
// totalKeysExamined ≈ nReturned (no over-scan)
```

---

## Commandment 3 — Thou shalt not `findMany` without `select` and `take`

Pulling the entire document when you need `id` and `email` wastes bandwidth, memory, and BSON→JSON CPU. Worse: a `findMany()` with no `take` on a table that grows to 10M rows will OOM your Node process.

**Always project, always limit:**
```ts
const users = await prisma.user.findMany({
  where: { active: true },
  select: { id: true, email: true, name: true },
  take: 50,
  orderBy: { createdAt: 'desc' },
})
```

**Forbidden in production code:**
- `prisma.x.findMany()` with no `take`
- `prisma.x.findMany({ where })` returning full documents when one field is needed
- "I'll add the limit later" — no you won't

---

## Commandment 4 — Thou shalt paginate with cursor, not `skip`

`skip: 10000` forces Mongo to walk and discard 10,000 documents before returning the next page: **O(n + skip)**. Cursor pagination over an indexed field is **O(log n)**.

**Cursor pagination (correct):**
```ts
const page = await prisma.post.findMany({
  take: 20,
  ...(lastId && {
    cursor: { id: lastId },
    skip: 1, // skip the cursor itself
  }),
  orderBy: { id: 'asc' },
})

const nextCursor = page.length === 20 ? page[page.length - 1].id : null
```

**Acceptable exceptions for `skip/offset`:**
- Admin tools with small datasets (<10k rows)
- The user explicitly needs jumpable page numbers and you've measured it

Everything else: cursor.

---

## Commandment 5 — Thou shalt kill N+1 with `include`/`select`, but measure the `$lookup`

Prisma translates relations on Mongo into `$lookup` aggregation stages. `include` solves the N+1 problem (1 query instead of N), but a `$lookup` against an unindexed foreign key is brutal — it scans the joined collection for every parent document.

**Rules:**
1. Always index foreign keys (`userId`, `postId`, etc.) with `@@index`.
2. For 1:1 or small 1:N relations that are **always read together**, use Prisma **composite types** (embedded documents) instead of separate collections — zero joins, atomic reads, this is Mongo's superpower.
3. Use `select` inside `include` to project only what you need from the joined side.

```ts
// Good: indexed FK, projected fields
const posts = await prisma.post.findMany({
  where: { published: true },
  select: {
    id: true,
    title: true,
    author: { select: { id: true, name: true } },
  },
  take: 20,
})
```

For deeply nested includes (3+ levels), profile the `$lookup` pipeline with `explain()`. If it's slow, denormalize or embed.

---

## Commandment 6 — Thou shalt batch writes or perish from round-trips

```ts
// ❌ N round-trips, N × (RTT + writeConcern majority wait)
for (const item of items) {
  await prisma.event.create({ data: item })
}
```

Each iteration pays full network latency plus `w: majority` acknowledgment. 1000 items at 20ms RTT = 20 seconds. Use batch operations:

```ts
// ✅ 1 round-trip
await prisma.event.createMany({ data: events })
await prisma.user.updateMany({ where: { active: false }, data: { archived: true } })
await prisma.session.deleteMany({ where: { expiresAt: { lt: new Date() } } })
```

**The only valid loop case** is when you need the generated `id` of each insert individually AND you can't restructure to a single batch. Even then, parallelize with `Promise.all` (bounded concurrency) instead of `await` in series.

---

## Commandment 7 — Thou shalt aggregate in the database, not in Node

The #1 antipattern in code review: loading 100k documents into Node memory to run `.reduce()`, `.filter()`, or `.groupBy()` in JavaScript. Mongo's aggregation engine runs on disk, in parallel, with indexes. Your Node process runs single-threaded on the heap.

```ts
// ❌ Loads everything into memory
const orders = await prisma.order.findMany({ where: { createdAt: { gte: lastMonth } } })
const totals = orders.reduce((acc, o) => {
  acc[o.status] = (acc[o.status] || 0) + o.total
  return acc
}, {})

// ✅ Mongo does the work, Node gets the result
const totals = await prisma.order.groupBy({
  by: ['status'],
  where: { createdAt: { gte: lastMonth } },
  _sum: { total: true },
  _count: true,
})
```

Same applies to `count`, `aggregate` (avg/min/max/sum), and `$queryRaw` for anything Prisma can't express natively.

---

## Commandment 8 — Thou shalt not trust user input, not even in `where`

NoSQL injection is real. A request body like `{ role: { $ne: 'admin' } }` passed directly into a `where` clause can bypass auth checks.

**Three rules:**

1. **Validate request shape with Zod / Valibot / Yup before it touches Prisma:**
```ts
const QuerySchema = z.object({
  role: z.enum(['user', 'editor']),
  limit: z.number().int().min(1).max(100).default(20),
})
const { role, limit } = QuerySchema.parse(req.body)
await prisma.user.findMany({ where: { role }, take: limit })
```

2. **Never spread untrusted input into `where`:**
```ts
// ❌ NEVER
await prisma.user.findMany({ where: req.body })
```

3. **For `$queryRaw`, always use the tagged template form** (parameterized), never string concatenation:
```ts
// ✅ parameterized
await prisma.$queryRaw`SELECT * FROM users WHERE id = ${userId}`
// ❌ injectable
await prisma.$queryRawUnsafe(`SELECT * FROM users WHERE id = '${userId}'`)
```

Prisma's typed query API already parameterizes, but unvalidated input shape is still a vulnerability vector.

---

## Commandment 9 — Thou shalt use `$transaction` only when atomicity matters, not by reflex

MongoDB supports transactions only on replica sets, and each transaction holds locks, snapshots, and retries on `TransientTransactionError`. They have real cost. Use them when state must change atomically (debit account A, credit account B). Don't wrap independent reads.

```ts
// ❌ Serial, transactional for no reason — slow and lock-heavy
await prisma.$transaction(async (tx) => {
  const user = await tx.user.findUnique({ where: { id } })
  const posts = await tx.post.findMany({ where: { userId: id } })
  return { user, posts }
})

// ✅ Parallel, no transaction needed
const [user, posts] = await Promise.all([
  prisma.user.findUnique({ where: { id } }),
  prisma.post.findMany({ where: { userId: id }, take: 10 }),
])

// ✅ Transaction where atomicity is required
await prisma.$transaction([
  prisma.account.update({ where: { id: from }, data: { balance: { decrement: amount } } }),
  prisma.account.update({ where: { id: to }, data: { balance: { increment: amount } } }),
  prisma.transfer.create({ data: { from, to, amount } }),
])
```

For the interactive `$transaction(async tx => ...)` form, set a reasonable `timeout` and `maxWait` — the defaults will surprise you under load.

---

## Commandment 10 — Thou shalt treat `DATABASE_URL` as a live secret, not a constant

The connection string holds credentials, pool config, and durability flags. Treat it accordingly.

**Three rules:**

1. **Never commit it.** Not in `.env`, not in `.env.example` with real values, not in CI logs, not in error messages. Use a secret manager (Vault, AWS Secrets Manager, Doppler, 1Password) — and rotate.

2. **Explicit production parameters** — defaults are not safe defaults:
```
?retryWrites=true
&w=majority
&maxPoolSize=10
&minPoolSize=2
&serverSelectionTimeoutMS=5000
&socketTimeoutMS=30000
```

3. **Principle of least privilege** on the Mongo user. The app does not need `dbAdmin` or `root`. Create a role with `readWrite` only on the specific database:
```js
db.createUser({
  user: "app_prod",
  pwd: "...",
  roles: [{ role: "readWrite", db: "production" }]
})
```
Separate users for migrations (with `dbAdmin`) and runtime (with `readWrite` only). The blast radius of a leaked runtime credential drops by an order of magnitude.

---

## Prisma + Mongo Limitations — When Prisma is the wrong tool

Prisma on MongoDB is **opinionated and incomplete**. A senior engineer knows where the guardrails end and where raw MongoDB becomes mandatory.

- **No native migrations.** `prisma migrate dev` and `db push` do not support MongoDB. Every `@@index` addition must ship with a companion `.js` migration script run via `mongosh` or Atlas.
- **`$queryRaw` is severely limited.** Designed for SQL; on Mongo it only supports basic read-only pipelines. For complex `$lookup`, `$facet`, or aggregations, drop to the native `mongodb` driver.
- **No composite `@@id`.** Prisma does not support composite primary keys on MongoDB. Workaround: single `@id` + compound `@@unique` on business keys, or denormalize into one field.
- **Specialized indexes require raw MongoDB.** TTL, partial, sparse, text, and 2dsphere (Commandments #11–#14) cannot be declared in `schema.prisma`. Document every raw index as a comment block with its exact `createIndex` command.
- **Complex aggregations are out of scope.** `groupBy` and `aggregate` cover basics. For multi-stage pipelines, use the native driver inside a repository method.

---

# Index Specialization — 5 additional commandments

The index is the difference between a query that returns in 2ms and one that takes down your cluster. Commandment #2 says "have indexes." These five say "have the *right* indexes, the right way." Full details for each are in the `references/patterns/` files listed below.

---

## Commandment 11 — Thou shalt respect index selectivity, not waste B-tree depth on booleans

The leading field of an index must split the dataset finely. `userId` (millions of values) is great; `isActive` (2 values) as a leader is nearly useless — it scans ~50% of the collection. Quick test: `distinct("field").length / count()`. If the ratio is below ~1%, don't lead with it. Exception: partial indexes (#14) fix cardinality by indexing only the matching subset. See `references/patterns/index-selectivity.md`.

---

## Commandment 12 — Thou shalt design covered queries — index serves the projection too

A covered query answers entirely from the index (`totalDocsExamined: 0`). To cover, the index must contain every field in `where`, `orderBy`, and `select`. One extra field in `select` outside the index kills the covering. Wider indexes cost disk and RAM — cover only your hot, read-heavy queries. See `references/patterns/covered-query-design.md`.

---

## Commandment 13 — Thou shalt prefer compound indexes over index intersection

Mongo rarely uses index intersection, and when it does it's slower than a compound index. The prefix rule makes compounds powerful: `[A, B, C]` also serves `[A]` and `[A, B]`, but never `[B]` alone. Design from your top 5 query shapes, not from fields. See `references/patterns/compound-index-design.md`.

---

## Commandment 14 — Thou shalt use the right specialized index — TTL, partial, sparse, unique, text, 2dsphere

If your data has a *kind*, there's a specialized index for it: TTL for expirations, partial for filtered hot paths, sparse + unique for optional uniques, text for search (never `$regex` without anchor), 2dsphere for geospatial. All require raw MongoDB — Prisma's DSL only covers basic `@@index`. See `references/patterns/specialized-indexes.md`.

---

## Commandment 15 — Thou shalt audit indexes — every one has a write cost, drop the unused

Every index is taxed on every write. Symptoms of over-indexing: write latency creeping up, replication lag, working set past RAM. Hunt unused indexes monthly with `$indexStats` (`ops: 0` → drop). Hunt redundant prefixes. Build new indexes with `{ background: true }` or rolling builds on replica sets. Heuristic: >6–8 indexes per collection is a design problem. See `references/patterns/index-audit.md`.

---

## Bonus — The senior move: measure or it didn't happen

What you don't measure, you can't optimize. Before declaring code "production-ready":

- **Dev**: `log: ['query', 'warn', 'error']` on the Prisma client to see every query and its duration.
- **Prod**: export `prisma.$metrics.json()` to Prometheus / Datadog. Alert on p95 query latency > 100ms.
- **Atlas**: enable the Performance Advisor and Profiler. Alert on slow queries (>100ms) and on plans that hit `COLLSCAN`.
- **Load test before launch**, not after. k6 or Artillery against a staging cluster that mirrors prod indexes.

---

## Emergency Playbook — Troubleshooting Common Failures

When the pager rings at 3 AM, you don't google. You run this checklist.

### Symptom: `Pool exhausted` / `MongoServerError: connection pool exhausted`
- **Diagnosis:** `db.serverStatus().connections` → `current` ≈ `available`. Or Atlas metrics show connections flat at limit.
- **Fix NOW:** restart the service (kills leaked PrismaClients), then deploy the singleton fix (Commandment #1).
- **Root cause:** multiple `new PrismaClient()` instances, missing singleton, or serverless without Accelerate.
- **Prevention:** Commandment #1 + Accelerate in serverless.

### Symptom: `TransientTransactionError` during `$transaction`
- **Diagnosis:** MongoDB logs show `TransientTransactionError` with retry attempts.
- **Fix NOW:** increase `maxWait` and `timeout` in the transaction options, or remove the transaction if it wraps independent reads.
- **Root cause:** transactions on replica sets have retry limits; default timeouts are too low under load.
- **Prevention:** Commandment #9 — use `$transaction` only for true atomicity.

### Symptom: Atlas Performance Advisor flags `COLLSCAN` on a "fast" query
- **Diagnosis:** `explain("executionStats")` shows `winningPlan.stage: "COLLSCAN"` and `totalDocsExamined` >> `nReturned`.
- **Fix NOW:** build the missing index (background build on replica sets), verify with `explain()` again.
- **Root cause:** missing or wrong-order index; ESR violated; query shape changed after index was built.
- **Prevention:** Commandment #2 + #13 — design indexes from query patterns, verify with `explain()`.

### Symptom: Write latency spikes under load
- **Diagnosis:** Atlas metrics show `oplog` churn increasing; replication lag growing; `totalKeysExamined` normal but insert latency up.
- **Fix NOW:** run `$indexStats` on the hot collection, drop indexes with `ops: 0`, consolidate redundant prefixes.
- **Root cause:** over-indexing — too many indexes on a write-heavy collection.
- **Prevention:** Commandment #15 — monthly `$indexStats` audit, heuristic max 6–8 indexes per collection.

### Symptom: `PrismaClientKnownRequestError: P2035` (timeout)
- **Diagnosis:** query duration > `socketTimeoutMS` (default 30s). Check Atlas Profiler for the slow query.
- **Fix NOW:** add the missing index, add `take` limit, or switch from `skip` to cursor pagination.
- **Root cause:** unindexed query on large collection, missing `take`, or deep `skip` offset.
- **Prevention:** Commandments #2, #3, #4 — index every `where`, always limit, cursor pagination.

---

## Review checklist (apply to every Prisma + Mongo file you touch)

When reviewing or writing code, walk this list:

- [ ] #1  Single `PrismaClient` instance (singleton pattern present)?
- [ ] #1  Connection string has explicit `maxPoolSize`, `retryWrites`, `w=majority`?
- [ ] #2  Every `where` field is covered by an `@@index` (and ESR-ordered if compound)?
- [ ] #3  Every `findMany` has both `select`/`include` projection AND `take`?
- [ ] #4  Pagination uses `cursor`, not `skip` (unless dataset is provably small)?
- [ ] #5  Foreign keys used in `include` are indexed? Embedded vs related decided deliberately?
- [ ] #6  No `await` inside loops for writes — `createMany`/`updateMany`/`deleteMany` used?
- [ ] #7  Aggregations (`groupBy`, `aggregate`, `count`) run in DB, not in JS `.reduce()`?
- [ ] #8  User input validated with a schema before reaching `where`/`data`?
- [ ] #8  Raw queries use tagged template (`$queryRaw`), never `$queryRawUnsafe` with interpolation?
- [ ] #9  `$transaction` used only for true atomicity needs? Parallel reads via `Promise.all`?
- [ ] #10 `DATABASE_URL` from secret manager, app DB user has only `readWrite` on its database?
- [ ] #11 Leading index field is selective (not a boolean or 3-value enum)?
- [ ] #12 Hot read queries are covered (`select` fields ⊆ index keys, `totalDocsExamined: 0`)?
- [ ] #13 Compound indexes built for actual query patterns (no reliance on intersection, prefix rule respected)?
- [ ] #14 Specialized index types used where appropriate (TTL for expirations, partial for filtered hot paths, sparse + unique for optional uniques, text for search, 2dsphere for geo)?
- [ ] #15 Indexes audited with `$indexStats` — unused dropped, redundant prefixes removed, builds done rolling on prod?
- [ ] Bonus  Query logging in dev, metrics exported in prod, slow-query alerts configured?

Cite the failing commandment number when flagging an issue. Show the fix in code, not in prose.

---

## References

The following files provide detailed examples, patterns, anti-patterns, and troubleshooting guides referenced throughout the commandments above:

### Examples
- `references/examples/schema-saas.prisma.md` — Production-ready `schema.prisma` with `User`, `Post`, `Comment`, `Order`, and `Session` models demonstrating all index types and raw MongoDB migration scripts.

### Patterns
- `references/patterns/singleton-prisma-client.md` — Singleton implementation, connection string templates, and Prisma Accelerate serverless config.
- `references/patterns/index-selectivity.md` — Why booleans and low-cardinality fields make poor index leaders and how to test selectivity.
- `references/patterns/covered-query-design.md` — How to design indexes that cover `where`, `orderBy`, and `select` for zero document fetches.
- `references/patterns/cursor-pagination.md` — Cursor-based pagination implementation with `skip` exceptions documented.
- `references/patterns/compound-index-design.md` — ESR rule, prefix rule, and designing compound indexes from real query patterns.
- `references/patterns/specialized-indexes.md` — TTL, partial, sparse, unique, text, and 2dsphere indexes with raw MongoDB commands.
- `references/patterns/index-audit.md` — Monthly `$indexStats` audits, redundant prefix removal, and rolling production builds.

### Anti-Patterns
- `references/anti-patterns/n-plus-one-loop.md` — Unindexed `$lookup` via `include` and the embedded-document alternative.
- `references/anti-patterns/skip-offset-pagination.md` — Cost analysis of deep `skip` offsets and the cursor fix.
- `references/anti-patterns/await-in-write-loops.md` — Serial writes vs `createMany`/`updateMany`/`deleteMany` batching.
- `references/anti-patterns/js-aggregation.md` — Loading documents into Node to `.reduce()` vs native `groupBy`/`aggregate`.
- `references/anti-patterns/unvalidated-where-spread.md` — NoSQL injection via `where: req.body` and the Zod validation fix.

### Troubleshooting
- `references/troubleshooting/pool-exhausted.md` — One-command diagnosis and immediate fix for connection pool exhaustion.
- `references/troubleshooting/transient-transaction-error.md` — Timeout tuning and removing unnecessary transactions.
- `references/troubleshooting/collscan-alerts.md` — Diagnosing `COLLSCAN` with `explain()`, index building, and when indexes don't help.
