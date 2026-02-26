---
name: use-the-index-luke
description: Postgres query and index optimization workflow based on use-the-index-luke principles. Use for EXPLAIN analysis, index design, predicate rewrites, joins, sorting, and pagination tuning.
---

# Use the Index, Luke (Postgres)

## Purpose

Fix slow Postgres queries with an indexing-first workflow that balances read performance, write overhead, and operational risk.

## When to use

Use this skill when:

- Query latency or throughput regresses in Postgres.
- You need concrete index recommendations tied to an `EXPLAIN (ANALYZE, BUFFERS)` plan.
- You are tuning filters, joins, ORDER BY, GROUP BY, or pagination.

Do not use this skill for:

- Generic ORM cleanup without query-level evidence.
- Cache-first fixes when SQL execution is the bottleneck.

## Required inputs

Ask for:

- Exact SQL with representative bind values.
- Table DDL, row counts, and current indexes/constraints.
- `EXPLAIN (ANALYZE, BUFFERS)` from a production-like environment.
- Read/write mix (SELECT vs INSERT/UPDATE/DELETE rates).

If key inputs are missing, proceed with assumptions but label uncertainty clearly.

## Optimization workflow

### 1) Baseline and bottleneck

- Identify dominant plan cost: scans, sort/hash spill, nested loop amplification, or heap fetches.
- Record baseline metrics: total time, rows, shared/local reads, loops.

### 2) Predicate sargability review

- Prefer direct column predicates over wrapped expressions.
- Rewrite non-sargable filters (`func(col)`, arithmetic on column, optional-param OR chains).
- Keep type consistency (no implicit casts on indexed columns).
- Use half-open date/time ranges (`>= start AND < end`) for index-friendly filtering.

### 3) Index design

- Composite index order: equality columns first, then range, then ordering columns.
- Align index order with `ORDER BY` direction when avoiding sort is important.
- Use expression indexes when expression predicates are required (for example `lower(email)`).
- Use partial indexes for stable hot subsets.
- Prefer one good composite index over multiple single-column indexes for the same query path.
- Consider `INCLUDE` columns when index-only access can materially reduce heap visits.

### 4) Join strategy checks

- For nested loops, ensure an index exists on the inner-side join key.
- Verify join order/selectivity does not explode loop counts.
- For hash joins, reduce input cardinality early with selective filters/indexes.

### 5) Sorting, grouping, and pagination

- Match index keys to frequent `ORDER BY` patterns to avoid explicit sort.
- For high offsets, switch from OFFSET pagination to keyset/seek pagination.
- For GROUP BY-heavy queries, test whether index order can reduce sort work.

### 6) DML trade-off analysis

- Every added index increases write amplification and storage.
- Keep only indexes that pay for themselves under observed workload.
- Identify redundant/overlapping indexes before adding new ones.

### 7) Validate and rollout

- Re-run `EXPLAIN (ANALYZE, BUFFERS)` and compare against baseline.
- Confirm improvements under realistic concurrency, not only isolated runs.
- For large tables, prefer `CREATE INDEX CONCURRENTLY` and plan cleanup (`DROP INDEX CONCURRENTLY`) after verification.

## Output format

Return:

- Root-cause diagnosis from the plan.
- Proposed SQL rewrite(s), if needed.
- Proposed index change(s) with exact DDL.
- Expected impact, risks, and write-cost trade-offs.
- Validation plan and rollback notes.

## Postgres command quick reference

- `EXPLAIN (ANALYZE, BUFFERS) <query>;`
- `CREATE INDEX CONCURRENTLY idx_name ON table_name (...);`
- `DROP INDEX CONCURRENTLY idx_name;`
- `ANALYZE table_name;`

## Reference

- [Use The Index, Luke](https://use-the-index-luke.com/)
