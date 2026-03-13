---
name: tanstack-db
description: Comprehensive React-focused guide for TanStack DB and community integrations (Dexie.js, PGLite). Use when writing or debugging code that uses @tanstack/react-db for live queries, optimistic mutations, or local-first synchronization.
---

# TanStack DB (React)

## Quick Start

TanStack DB is a local-first database and reactivity layer. For React applications, it provides `useLiveQuery` and optimistic mutations with sub-millisecond updates powered by `d2ts`.

## Core Guidelines

1. **Schemas Validate Client State**: Schemas are StandardSchema-compatible (Zod, Valibot, etc.). They validate client mutations, not server data. `TInput` must be a superset of `TOutput` for updates to work correctly.
2. **Dependency Arrays**: All query hooks require dependency arrays as the last argument, identical to `useEffect`. Include all external values. Omit to run on every render, or use `[]` for static queries.
3. **Conditional Queries**: To disable a query, return `undefined` or `null` from the callback.
4. **Router Preloading**: Preload data in your route loader (`await collection.preload()`), then consume it with `useLiveQuery` in the component.

## Advanced Topics

For deep dives into specific areas, consult the following references:

- **Collections & Schemas**: See [references/core-concepts.md](references/core-concepts.md) for collection types, sync modes (eager, on-demand, progressive), and schema constraints.
- **Queries & Hooks**: See [references/live-queries.md](references/live-queries.md) for the fluent SQL-like API, expression functions, `useLiveSuspenseQuery`, and query composition patterns.
- **Mutations & Transactions**: See [references/mutations.md](references/mutations.md) for optimistic updates, mutation merging, temporary ID handling, and direct `QueryCollection` writes.
- **Error Handling**: See [references/error-handling.md](references/error-handling.md) for specific error types (e.g., `DuplicateKeyError`, `SchemaValidationError`) and transaction states.
- **Community Integrations**: See [references/community-integrations.md](references/community-integrations.md) for Dexie.js (IndexedDB) and PGLite (WASM PostgreSQL + Drizzle ORM) adapters.