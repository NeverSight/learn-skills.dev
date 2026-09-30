---
name: backend-perf
description: Backend and database performance checklist. Use when writing or reviewing any backend endpoint, service, or DB query, when adding a WHERE clause or index, or when a query rewrite is proposed. Triggers on "endpoint is slow", "N+1", "race condition".
---

# Backend performance checklist

I walk every check below against the code in hand and state a verdict on each one. Applied, clean, or not applicable and why. A check I did not name is a check I did not run.

Checks marked `[pg]` are PostgreSQL-specific. I skip them on other stores rather than translating them.

- **Parallel async**. Independent async calls run together in `Promise.all`, never awaited one by one.
- **N+1 queries**. No query inside a sequential `for` or `for await` loop. Batch with `IN` clauses or a join instead. `Promise.all(items.map(q => oneQuery(q)))` over a few index-friendly queries runs in parallel and is not a sequential N+1. Cap the fan-out: an unbounded items list gets an explicit bound or concurrency limit, since N parallel queries still open N connections. Keep the parallel shape unless `EXPLAIN` shows the batched join runs faster, because batching often defeats the per-row index.
- **Pagination counts**. Count and rows come from one query: a `count(*) OVER ()` window or a single CTE, not a separate `COUNT(*)` next to the data query.
- **Index coverage** `[pg]`. Every production `WHERE` clause needs a matching index. `similarity(col, ...)`, `@@ to_tsvector(...)`, or `LIKE '%pattern%'` needs the matching `gin (col gin_trgm_ops)` or `gin (to_tsvector('lang', col))` index in the same PR, or a one-line comment citing the ADR or issue that accepts the sequential scan. Prefer the indexable `%` operator over a raw `similarity() > threshold` comparison, but only with a matching threshold: `%` tests against the session `pg_trgm.similarity_threshold` (default 0.3), so set it to the query's threshold and confirm result-set equivalence, and EXPLAIN-verify that the planner picks the index.
- **STABLE function reuse** `[pg]`. `pg_trgm.similarity` and `ts_rank` are STABLE, not IMMUTABLE, so PostgreSQL does not reliably memoize duplicate calls in one SELECT. A value needed twice, for example once in the projection and once in `GREATEST(...)`, is computed once in a `WITH ... AS MATERIALIZED` CTE. A plain subquery alias does not guarantee this. The planner can flatten it and evaluate per row.
- **Select only needed columns**. List endpoints name their columns instead of selecting the whole row.
- **Reuse fetched rows**. A row fetched for an ownership check is the row the handler returns. No second fetch by id.
- **EXPLAIN before rewriting** `[pg]`. Any query restructure, batching, joining, indexing, or replacement of parallel-N with batched-1 ships `EXPLAIN (ANALYZE, BUFFERS)` numbers for current versus proposed shape on representative data. Keep the faster shape. A rewrite that looks faster in the diff can run 10-100× slower on real data.
- **Race conditions**. When 2+ writers can touch one row, use a transaction. Async completion order is not source order. Order explicitly with `await` or `Promise.all` instead of relying on accidental serialization. A check plus a write that must stay atomic uses `SELECT ... FOR UPDATE` on `[pg]` or a unique constraint, not application-level locking.
