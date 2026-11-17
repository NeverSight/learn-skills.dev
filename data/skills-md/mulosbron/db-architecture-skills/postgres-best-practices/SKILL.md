---
name: postgres-best-practices
description: "Postgres and Supabase performance rules: missing or wrong indexes, connection pooling, RLS performance, locking, pagination, N+1, vacuum. Read when a Postgres query is slow or when reviewing queries and schema for performance."
---

# Postgres Best Practices (Supabase rule set)

Thirty rule files, each with a wrong and a right SQL example. Read only the files that match the problem.

| Problem area | Prefix | Start with |
|---|---|---|
| Slow queries, index choice | `rules/query-*` | `query-missing-indexes.md`, `query-composite-indexes.md` |
| Too many connections, serverless | `rules/conn-*` | `conn-pooling.md`, `conn-limits.md` |
| Row-Level Security, privileges | `rules/security-*` | `security-rls-performance.md` |
| Types, keys, FK indexes, partitioning | `rules/schema-*` | `schema-foreign-key-indexes.md` |
| Deadlocks, long transactions, queues | `rules/lock-*` | `lock-short-transactions.md`, `lock-skip-locked.md` |
| Pagination, upsert, batch insert, N+1 | `rules/data-*` | `data-pagination.md`, `data-n-plus-one.md` |
| Diagnosing | `rules/monitor-*` | `monitor-explain-analyze.md`, `monitor-pg-stat-statements.md` |
| JSONB, full-text | `rules/advanced-*` | |

`rules/_sections.md` lists every rule with a one-line summary.

## When auditing performance

1. Ask for or run `EXPLAIN (ANALYZE, BUFFERS)` on the slow query. Do not guess from the SQL alone.
2. Check `pg_stat_statements` for the top queries by total time if available.
3. Report each finding as: query, what the plan shows, rule file that applies, concrete fix.
