---
name: laravel-database-optimization
description: Optimize Laravel database work across N+1 queries, indexes, selective columns, caching, pagination, large data, locks, and migrations.
tags:
  - laravel
  - php
---

# Laravel Database Optimization

Use this skill when improving query performance, reviewing migrations, debugging slow pages, or reducing memory and database load in Laravel apps.

This skill coordinates existing performance skills and adds an optimization workflow.

## Priority Order

1. Prove the bottleneck with logs, query inspection, profiling, `EXPLAIN`, tests, or realistic data volume.
2. Fix query shape before adding infrastructure: eager loading, constraints, selective columns, aggregates, pagination, and bounded datasets.
3. Add indexes that match actual filters, joins, sorts, and uniqueness rules.
4. Cache only stable or expensive work with explicit invalidation.
5. Review transaction scope, lock behavior, and retry strategy for write-heavy paths.
6. Plan migrations with production data size and lock risk in mind.

## Query Shape

- Prevent N+1 problems with intentional eager loading.
- Select only needed columns on hot paths, including constrained relationship columns.
- Use `withCount`, `withSum`, `exists`, subqueries, or aggregates instead of loading full relations for summaries.
- Avoid unbounded `all()`, broad `get()`, and collection-side filtering on large tables.
- Use cursor pagination or chunking for large ordered datasets and background processing.

## Indexes And Migrations

- Add indexes for foreign keys, common filters, common sort paths, and composite access patterns.
- Match composite index order to the real query pattern.
- Avoid adding indexes speculatively without a query path that needs them.
- For production-scale tables, plan additive and reversible migrations; ask before destructive changes.
- When altering existing columns, preserve existing attributes required by the database platform.

## Caching

- Cache expensive reads behind stable keys and short, intentional TTLs.
- Invalidate cache near the writes that change the underlying data.
- Use tags only when the configured cache store supports them.
- Do not cache user-specific or authorization-sensitive data without including the scope in the key.

## Transactions And Locks

- Keep transactions short and free of slow external calls.
- Use row locks only around data that must remain consistent during the write.
- Use retry logic for known deadlock-prone flows.
- Dispatch jobs, events, notifications, and file cleanup after commit when correctness depends on committed data.

## Related Skills

- `performance-eager-loading`
- `performance-select-columns`
- `performance-caching`
- `data-chunking-large-datasets`
- `migrations-and-factories`
- `database-transactions`
