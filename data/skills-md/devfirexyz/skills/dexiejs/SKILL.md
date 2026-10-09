---
name: dexiejs
description: Build and maintain Dexie.js data layers for IndexedDB-backed offline-first web applications. Use when tasks involve Dexie setup, schema/index design, CRUD/query implementation, transactions, live queries, migrations, or debugging in Vanilla JS, React, Next.js, TanStack Start, Svelte, or SvelteKit.
---

# Dexie.js

Implement Dexie as a production data layer, not as scattered table calls inside UI components.

## Workflow

1. Classify runtime and rendering mode
- Confirm whether the target code runs only in browser or can run on server too.
- Prevent Dexie usage on server runtimes in Next.js, TanStack Start, and SvelteKit.
- Load `references/framework-integration.md` before writing framework-specific code.

2. Design schema from query shapes
- List read queries first (filters, sorts, ranges), then derive indexes.
- Use compound and multi-entry indexes when queries require them.
- Keep key strategy explicit (`++id`, custom IDs, or compound primary key).
- Load `references/core-patterns.md` sections 2 and 3.

3. Implement one shared DB module
- Define Dexie instance once per app/package.
- Export typed table handles and data-layer helper functions.
- Keep transaction boundaries in the data layer.

4. Add reactive reads
- Use `liveQuery()` for framework-agnostic reactivity.
- In React, prefer `useLiveQuery` from `dexie-react-hooks`.
- In Svelte, consume `liveQuery` observables directly in components.

5. Add writes with invariants
- Use `db.transaction()` for multi-table consistency and read-modify-write logic.
- Avoid unrelated async APIs inside transactions unless deliberately wrapped with `Dexie.waitFor()`.

6. Plan upgrades before release
- Add new versions with `db.version(n).stores(...).upgrade(...)`.
- Make migration code idempotent and safe for partially-updated datasets.

7. Validate behavior
- Test cold start, reload persistence, and multi-tab updates.
- Test migration from previous schema with realistic data.
- Verify SSR/client boundaries are enforced in hybrid frameworks.

## Framework Routing

- Vanilla JS: shared DB module + `liveQuery().subscribe(...)`.
- React: `dexie-react-hooks` + colocated data hooks.
- Next.js: client boundaries (`'use client'`) or dynamic import with `ssr: false`.
- TanStack Start: treat loaders as isomorphic; gate Dexie with `createClientOnlyFn`.
- Svelte/SvelteKit: use `liveQuery`; in SvelteKit gate with `$app/environment` (`browser`).

Load `references/framework-integration.md` for templates.

## Output Contract

When using this skill, return:

- Runtime boundary strategy and why.
- Final schema and index rationale per query path.
- Data-layer API surface (read/write helpers and transaction rules).
- Reactive read strategy for the selected framework.
- Migration plan and rollback considerations.
- Remaining risks and targeted tests.

## References

- `references/core-patterns.md`
Core Dexie patterns: schema syntax, CRUD/query, transactions, migrations, reactivity, and performance.

- `references/framework-integration.md`
Framework implementations for Vanilla JS, React, Next.js, TanStack Start, Svelte, and SvelteKit.

- `references/troubleshooting.md`
Symptom-to-fix guide for SSR boundary leaks, stale live queries, transaction issues, and migration failures.
