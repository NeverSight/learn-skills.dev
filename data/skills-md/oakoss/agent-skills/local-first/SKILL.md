---
name: local-first
description: |
  Local-first architecture decision framework for web applications. Covers when to go local-first vs server-based vs hybrid, sync engine selection (ElectricSQL, Zero, PowerSync, Replicache, LiveStore, Triplit), client-side storage options (IndexedDB, OPFS, SQLite WASM, PGlite), and conflict resolution strategies (LWW, CRDTs, server-wins, field-level merge).

  Use when deciding whether to adopt local-first architecture, choosing a sync engine, selecting client storage, or designing conflict resolution strategies.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
user-invocable: false
---

# Local-First

## Overview

Local-first is an architecture where the application reads and writes to a local database, with changes syncing to the server in the background. The local database is the source of truth for the UI, providing instant reads, offline support, and optimistic writes by default.

**When to use:** Collaborative apps needing offline support, latency-sensitive UIs where instant response matters, apps with unreliable network conditions, real-time multiplayer features, mobile apps with intermittent connectivity.

**When NOT to use:** Simple CRUD apps with reliable connectivity, server-authoritative workflows (payments, inventory), content-heavy sites with minimal interactivity, apps where data freshness from the server is critical on every render.

## Quick Reference

| Decision                | Options                                                 | Key Consideration                                      |
| ----------------------- | ------------------------------------------------------- | ------------------------------------------------------ |
| Architecture model      | Server-based, local-first, hybrid                       | Offline needs and latency tolerance drive the choice   |
| Read path               | Server fetch, local DB read, cache-then-network         | Local reads are instant; server reads block on network |
| Write path              | Server mutation, optimistic update, local-first write   | Local writes never fail; sync handles delivery         |
| Sync engine             | Electric, Zero, PowerSync, Replicache, LiveStore        | Postgres integration vs framework-agnostic             |
| Client storage          | IndexedDB, OPFS, SQLite WASM, PGlite                    | Capacity limits, query capability, browser support     |
| Conflict resolution     | LWW, CRDTs, server-wins, field-level merge              | Complexity vs correctness tradeoff                     |
| Data model              | Normalized tables, document store, CRDT documents       | Query patterns determine the best model                |
| Partial replication     | Shapes, subscriptions, query-based sync                 | Sync only what the client needs                        |
| Progressive enhancement | Server-first with local cache, full local-first         | Start simple, add local-first incrementally            |
| CQRS separation         | Separate read/write models, unified model               | Local-first naturally separates reads from writes      |
| Initial sync            | Full snapshot, incremental, progressive loading         | First-load performance vs completeness                 |
| Auth integration        | Token-based shape filtering, row-level security         | Security lives at the sync layer, not the client       |
| Schema evolution        | Additive migrations, versioned shapes                   | Local DB schema must evolve without data loss          |
| State management        | Replace React Query, coexist, hybrid approach           | Local-first can replace or complement server state     |
| Testing strategy        | Mock sync engine, test offline scenarios, seed local DB | Test both online and offline code paths                |

## Common Mistakes

| Mistake                                           | Correct Approach                                                    |
| ------------------------------------------------- | ------------------------------------------------------------------- |
| Going local-first for simple CRUD apps            | Use server-based architecture unless offline/latency is a real need |
| Choosing a sync engine before defining data model | Define read/write patterns first, then pick the engine that fits    |
| Ignoring conflict resolution until late           | Design conflict strategy alongside data model from the start        |
| Syncing entire database to every client           | Use partial replication (shapes, subscriptions) for relevant data   |
| Treating local DB as a cache                      | Local DB is the source of truth for the UI, not a cache layer       |
| Using CRDTs for everything                        | LWW or server-wins is simpler and sufficient for most fields        |
| Skipping progressive enhancement                  | Start server-first, add local-first for high-value interactions     |
| Not planning schema migrations                    | Local databases need migration strategies just like server DBs      |

## Delegation

> If the `electricsql` skill is available, delegate ElectricSQL setup, shapes, auth, and write patterns to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s electricsql -a claude-code -y`
> If the `realtime-sync` skill is available, delegate WebTransport, pub/sub, and CRDT implementation details to it.
> If the `tanstack-db` skill is available, delegate collection setup, live queries, and optimistic mutation patterns to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s tanstack-db -a claude-code -y`
> If the `tanstack-start` skill is available, delegate server function proxies and SSR integration to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s tanstack-start -a claude-code -y`

- **Architecture review**: Use `Plan` agent to evaluate local-first vs server-based tradeoffs
- **Sync engine comparison**: Use `Explore` agent to research current engine capabilities
- **Storage benchmarking**: Use `Task` agent to test storage options for specific data patterns

## References

- [Architecture patterns and decision framework](references/architecture-patterns.md)
- [Sync engine comparison and selection guide](references/sync-engines.md)
- [Client-side storage options and limits](references/client-storage.md)
- [Conflict resolution strategies](references/conflict-resolution.md)
- [Offline resilience patterns](references/offline-patterns.md)
- [Schema versioning and migration](references/schema-evolution.md)
- [Multi-tenant data governance patterns](references/multi-tenant.md)
- [Testing strategies for local-first apps](references/testing.md)
- [End-to-end encryption for synced data](references/encryption.md)
- [DevTools and debugging utilities](references/devtools-debugging.md)
- [Server-first to local-first migration guide](references/migration-guide.md)
