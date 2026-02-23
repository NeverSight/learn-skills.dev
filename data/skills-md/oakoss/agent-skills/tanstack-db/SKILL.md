---
name: tanstack-db
description: 'TanStack DB reactive client-side database with live queries and optimistic mutations. Use when building reactive UIs with local-first data, sync engines, or optimistic updates. Use for tanstack-db, live queries, optimistic mutations, sync engine, reactive database, local-first.'
license: MIT
metadata:
  author: oakoss
  version: '1.3'
  source: 'https://tanstack.com/db/latest'
---

# TanStack DB

## Overview

TanStack DB is a reactive client store built on differential dataflow that extends TanStack Query with collections, live queries, and optimistic mutations. It normalizes data into typed collections, enables sub-millisecond cross-collection queries, and provides instant optimistic updates with automatic rollback on failure.

**When to use:** Reactive UIs needing local-first data, cross-collection joins with live updates, optimistic mutations with automatic sync, real-time sync via ElectricSQL or other backends, apps that outgrow TanStack Query's per-query caching model.

**When NOT to use:** Simple fetch-and-display (TanStack Query alone suffices), server-components-only apps, purely synchronous local state (useState/Zustand), GraphQL with normalized caching (Apollo/urql).

> TanStack DB is currently in **beta**. APIs may change between releases.

## Quick Reference

| Pattern             | API                                                         | Key Points                                            |
| ------------------- | ----------------------------------------------------------- | ----------------------------------------------------- |
| Create collection   | `createCollection(queryCollectionOptions({...}))`           | Define typed set of objects with `getKey`             |
| Live query (React)  | `useLiveQuery((q) => q.from({...}).where(...))`             | Auto-updates when underlying data changes             |
| Filter              | `.where(({ t }) => eq(t.field, value))`                     | Supports `eq`, `gt`, `lt`, `like`, `and`, `or`, `not` |
| Select fields       | `.select(({ t }) => ({ id: t.id, name: t.name }))`          | Project specific fields from collections              |
| Order results       | `.orderBy(({ t }) => t.field, 'asc')`                       | Sort ascending or descending                          |
| Join collections    | `.join({ b: collB }, ({ a, b }) => eq(...), 'inner')`       | Cross-collection joins with type safety               |
| Group and aggregate | `.groupBy(...).select(({ t }) => ({ count: count(t.id) }))` | Supports `count`, `sum`, `avg`, `min`, `max`          |
| Insert              | `collection.insert({ ...data })`                            | Optimistic insert, syncs via `onInsert` handler       |
| Update              | `collection.update(key, (draft) => { ... })`                | Immer-style draft mutation, syncs via `onUpdate`      |
| Delete              | `collection.delete(key)`                                    | Optimistic delete, syncs via `onDelete` handler       |
| Electric sync       | `electricCollectionOptions({ shapeOptions: {...} })`        | Real-time Postgres sync via ElectricSQL               |
| Live query coll.    | `liveQueryCollectionOptions({ query })`                     | Derived collection from live query definition         |
| Local storage       | `localStorageCollectionOptions({...})`                      | Persistent local data, syncs across tabs              |

## Sync Modes (v0.5+)

| Mode            | Behavior                                             | Use Case                          |
| --------------- | ---------------------------------------------------- | --------------------------------- |
| Eager (default) | Loads all records on collection init                 | Small datasets (< 1k rows)        |
| On-demand       | Loads only what queries request (predicate pushdown) | Large datasets, selective loading |
| Progressive     | Fast first paint, full dataset syncs in background   | Best of both, scales to 100k+     |

## Common Mistakes

| Mistake                                        | Correct Pattern                                             |
| ---------------------------------------------- | ----------------------------------------------------------- |
| Using TanStack Query directly for local state  | Use collections with live queries for reactive local data   |
| Forgetting `getKey` in collection config       | Always provide `getKey` to identify items uniquely          |
| Not providing persistence handlers             | Define `onInsert`/`onUpdate`/`onDelete` to sync with server |
| Using `useQuery` instead of `useLiveQuery`     | `useLiveQuery` provides reactive cross-collection queries   |
| Creating collections inside components         | Define collections at module scope, outside components      |
| Importing from `@tanstack/db` in React apps    | Import from `@tanstack/react-db` (re-exports core)          |
| Expecting automatic server sync without config | Collections require explicit persistence handlers for sync  |
| Not installing collection type package         | Install `@tanstack/query-db-collection` for REST API usage  |

## Delegation

> If the `tanstack-query` skill is available, delegate TanStack Query-specific patterns (query keys, cache invalidation, SSR) to it.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-query`
> If the `electricsql` skill is available, delegate ElectricSQL setup, shapes, auth proxy, and write patterns to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s electricsql -a claude-code -y`
> If the `local-first` skill is available, delegate architecture decisions, sync engine comparison, and conflict resolution to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s local-first -a claude-code -y`

- **Query pattern discovery**: Use `Explore` agent
- **Architecture review**: Use `Task` agent

## References

- [Setup, installation, and collection configuration](references/setup.md)
- [Live queries, filtering, joins, and aggregations](references/live-queries.md)
- [Optimistic mutations, persistence handlers, and sync patterns](references/mutations.md)
- [ElectricSQL integration, electric collections, and txid patterns](references/electricsql-integration.md)
