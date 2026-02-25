---
name: pglite
description: |
  PGlite embeds PostgreSQL 17.4 in the browser and Node.js via WASM, under 3MB gzipped. Covers storage backends, queries, transactions, extensions (pgvector, pg_trgm, full-text search), live queries, React integration, multi-tab worker architecture, and Electric sync.

  Use when setting up PGlite, choosing storage backends, writing queries or transactions, configuring extensions, implementing live queries, integrating with React, managing multi-tab workers, or syncing with Electric.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://pglite.dev/docs'
user-invocable: false
---

# PGlite

## Overview

PGlite is a lightweight WASM build of PostgreSQL 17.4 that runs directly in the browser, Node.js, and Bun with no external dependencies. It provides a full Postgres query engine with extensions, transactions, COPY support, and listen/notify in under 3MB gzipped.

**When to use:** Local-first apps needing a real SQL engine, browser-based analytics, offline-capable PWAs, embedded Postgres for testing, prototyping without a server.

**When NOT to use:** High-concurrency server workloads (use native Postgres), apps requiring full Postgres replication, Safari OPFS storage (not supported), write-heavy multi-tab scenarios without leader election.

## Quick Reference

| Pattern              | API                                              | Key Points                    |
| -------------------- | ------------------------------------------------ | ----------------------------- |
| Create instance      | `PGlite.create(dataDir?, options?)`              | Awaits ready internally       |
| In-memory DB         | `PGlite.create()`                                | Default, ephemeral storage    |
| IndexedDB storage    | `PGlite.create('idb://dbname')`                  | Persists in browser           |
| OPFS storage         | `PGlite.create('opfs-ahp://dbname')`             | Worker only, no Safari        |
| Parameterized query  | `db.query<T>(sql, params)`                       | Returns `QueryResult<T>`      |
| Tagged template      | `db.sql\`SELECT ...\``                           | Auto-parameterized            |
| Multi-statement exec | `db.exec(sqlString)`                             | No params, returns void       |
| Transaction          | `db.transaction(async (tx) => {})`               | Full ACID, use tx.query       |
| Load extension       | `extensions: { vector }` in create               | Loaded at construction        |
| Live query           | `db.live.query(sql, params, cb)`                 | Re-runs on data change        |
| Incremental query    | `db.live.incrementalQuery(sql, params, key, cb)` | Diffs large result sets       |
| Live changes         | `db.live.changes(sql, params, key, cb)`          | Raw insert/update/delete ops  |
| React hook           | `useLiveQuery(sql, params)`                      | Returns `{ rows }` reactively |
| Multi-tab worker     | `PGliteWorker` + leader election                 | Single writer, multi reader   |
| Electric sync        | `syncShapeToTable(db, shape, table)`             | One-way read-only sync        |
| Dump data            | `db.dumpDataDir('gzip')`                         | Returns File blob             |
| Load data            | `PGlite.create({ loadDataDir: blob })`           | Restore from dump             |
| Listen/notify        | `db.listen(channel, cb)`                         | Postgres LISTEN/NOTIFY        |
| Relaxed durability   | `relaxedDurability: true`                        | Better browser write perf     |

## Common Mistakes

| Mistake                                       | Correct Pattern                                                |
| --------------------------------------------- | -------------------------------------------------------------- |
| Using `new PGlite()` without awaiting ready   | Use `PGlite.create()` which awaits internally                  |
| Using OPFS in main thread                     | OPFS-AHP requires a Web Worker context                         |
| Using OPFS on Safari                          | Safari lacks required OPFS APIs; use idb://                    |
| Querying outside transaction callback         | Pass `tx` from transaction callback, use `tx.query()`          |
| Forgetting extension in create options        | Extensions must be declared at `PGlite.create({ extensions })` |
| Multiple tabs writing without leader election | Use `PGliteWorker` with leader election for multi-tab          |
| Expecting Electric sync to be bidirectional   | Electric sync is read-only, one-way from server                |
| Using `live.query()` for large datasets       | Use `live.incrementalQuery()` for large result sets            |
| Not providing `key` to incremental query      | Incremental and changes queries require a unique key column    |
| Importing extensions without bundler support  | Extensions are WASM; ensure bundler handles `.wasm` assets     |

## Delegation

> If the `electricsql` skill is available, delegate Electric sync patterns, Shape configuration, and real-time replication to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s electricsql -a claude-code -y`
>
> If the `drizzle-orm` skill is available, delegate Drizzle + PGlite driver setup and schema management to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s drizzle-orm -a claude-code -y`
>
> If the `local-first` skill is available, delegate local-first architecture decisions and sync engine selection to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s local-first -a claude-code -y`

## References

- [Installation, storage backends, and configuration](references/setup.md)
- [Queries, transactions, COPY, listen/notify, and data import/export](references/queries-and-transactions.md)
- [Extensions: pgvector, pg_trgm, pgcrypto, full-text search, and more](references/extensions.md)
- [Live queries: reactive, incremental, and change-tracking](references/live-queries.md)
- [React integration: providers, hooks, and typed patterns](references/react-integration.md)
- [Multi-tab worker architecture and leader election](references/multi-tab-worker.md)
- [Electric sync: shapes, transactional sync, and persistence](references/electric-sync.md)
