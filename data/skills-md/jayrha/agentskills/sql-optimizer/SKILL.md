---
name: sql-optimizer
description: Diagnoses and fixes slow SQL queries using EXPLAIN/EXPLAIN ANALYZE plan reading, index design, query rewrites, statistics, and schema-aware tuning across PostgreSQL, MySQL/MariaDB, SQL Server, Oracle, and SQLite. Use this skill when a user says a query is slow, times out, "takes forever", needs an index, asks to "optimize this SQL", "why is this query slow", "read this EXPLAIN plan", "add an index", "reduce query cost", "fix a full table scan / seq scan", "N+1 query", "tune the database", or pastes a query plan and asks what is wrong.
license: MIT
---

# SQL Optimizer

## Overview
This skill turns "this query is slow" into a concrete, evidence-driven fix. It reads execution
plans, identifies the dominant cost, proposes the smallest effective change (index, rewrite,
schema, or config), and verifies the improvement with before/after measurements.

Keywords: slow query, EXPLAIN, EXPLAIN ANALYZE, query plan, seq scan, full table scan, index,
covering index, composite index, query rewrite, sargable, N+1, timeout, high cost, cardinality,
statistics, ANALYZE, query tuning, database performance, PostgreSQL, MySQL, SQL Server, Oracle, SQLite.

Golden rule: **measure, change one thing, measure again.** Never guess. Never add an index
without reading the plan first.

## Process
Follow these steps in order. Do not skip step 1 or 2.

1. **Gather context.** Identify: the engine + version, the exact query (with real-ish parameters,
   not placeholders), table row counts, existing indexes, and how the query is run (ORM? prepared
   statement? batch?). If any are missing, ask or inspect the schema. See
   `references/dialect-cheatsheet.md` for how to collect each per engine.

2. **Capture the real plan.** Run the engine's analyze form to get *actual* timing and row counts,
   not just estimates:
   - PostgreSQL: `EXPLAIN (ANALYZE, BUFFERS, VERBOSE, FORMAT TEXT) <query>;`
   - MySQL 8+/MariaDB: `EXPLAIN ANALYZE <query>;` (or `EXPLAIN FORMAT=JSON`)
   - SQL Server: `SET STATISTICS IO, TIME ON;` + Actual Execution Plan
   - Oracle: `EXPLAIN PLAN FOR ...; SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);` then `DBMS_XPLAN.DISPLAY_CURSOR(FORMAT=>'ALLSTATS LAST')`
   - SQLite: `EXPLAIN QUERY PLAN <query>;`
   Wrap writes (UPDATE/DELETE) in a transaction you roll back, or test on a SELECT-shaped copy.

3. **Find the dominant cost.** Read the plan bottom-up / inner-most-first. Locate the node with
   the largest `actual time` × `loops` (PostgreSQL) or highest cost/rows. Compare **estimated vs
   actual rows** — a large mismatch (>10x) means stale statistics or a bad predicate estimate.
   Use the diagnosis table in `references/plan-reading.md`.

4. **Classify the problem** into one of these buckets, then apply the matching fix:
   - Full/sequential scan on a large table with a selective filter → add/repair an index (step 5).
   - Index exists but unused → non-sargable predicate, type mismatch, or wrong column order (step 6).
   - Huge row estimate mismatch → refresh statistics (`ANALYZE` / `UPDATE STATISTICS`), then re-plan.
   - Expensive sort/hash/aggregate spilling to disk → covering/composite index or more work_mem.
   - Nested loop with high `loops` → likely N+1 or missing join index; consider batching or a join.
   - Returning/scanning far more rows than needed → add LIMIT, narrow SELECT list, prefilter.

5. **Design indexes deliberately.** Apply the column-ordering rules (equality → range → sort →
   include) in `references/indexing-guide.md`. Prefer one well-ordered composite/covering index
   over many single-column ones. Estimate write/storage cost before recommending.

6. **Rewrite the query to be sargable and minimal.** Remove functions on indexed columns, fix
   implicit casts, replace `OR` with `UNION ALL` or `IN` where it unlocks an index, turn correlated
   subqueries into joins, push filters down, and select only needed columns. Patterns are in
   `references/rewrite-patterns.md`.

7. **Verify.** Re-run the analyze form. Confirm: lower actual total time, scan replaced by index
   seek/scan, estimate≈actual, no disk spill. Report before/after numbers. If no improvement,
   revert the change (especially indexes) — do not leave dead indexes behind.

8. **Document.** Produce a short report: problem, root cause, change made, before/after timing,
   and any trade-offs (write amplification, storage). Use `templates/optimization-report.md`.

Optionally run `python3 scripts/explain_analyzer.py plan.json` to auto-flag seq scans, row
mis-estimates, and disk spills from a PostgreSQL `FORMAT JSON` plan.

## Decision Framework: which lever to pull
- **Cheapest first.** Statistics refresh (free, instant) → query rewrite (no schema change) →
  index (write cost) → schema change (migration) → config (`work_mem`, etc., affects everyone).
- **Selectivity test.** An index helps only if the predicate returns a small fraction of rows
  (rule of thumb: < ~5-10% for a non-covering index). For low-selectivity filters a scan is correct.
- **Read vs write balance.** Every index slows INSERT/UPDATE/DELETE and costs storage. On
  write-heavy tables, justify each index.
- **One change at a time.** Bundling changes makes attribution impossible.

## Best Practices
- Always test with realistic parameter values and on data volumes close to production.
- Prefer `EXPLAIN ANALYZE` (actuals) over plain `EXPLAIN` (estimates) when safe to execute.
- Make predicates sargable: `WHERE col = ?` not `WHERE fn(col) = ?`; range on dates not `YEAR(col)`.
- Order composite index columns: equality predicates first, then the range/sort column.
- Use covering indexes (INCLUDE / extra key columns) to enable index-only scans on hot queries.
- Keep the SELECT list narrow; avoid `SELECT *` in hot paths.
- Refresh statistics after big data loads before blaming the planner.
- For ORMs, look for N+1: one query per row in a loop → use eager loading / a single join.
- Name indexes meaningfully and record why they exist.

## Common Pitfalls
- Adding an index without reading the plan — it may never be used or may not help.
- Trusting estimated rows when actuals differ wildly (stale stats).
- Wrapping an indexed column in a function or casting it, killing index use.
- Leading-column violation: a composite index `(a,b)` cannot serve a query filtering only on `b`.
- Over-indexing: many redundant indexes crush write throughput.
- `OR` across different columns preventing index use (rewrite to `UNION ALL`).
- Optimizing a query that runs once instead of the one that runs millions of times — profile first.
- Testing on tiny dev data where every plan looks fine; scans only hurt at scale.
- Forgetting parameter sniffing / plan caching differences between literal and bound values.

## Bundled Files
- `references/plan-reading.md` — how to read each engine's plan, node-by-node diagnosis table.
- `references/indexing-guide.md` — index types, column ordering, covering indexes, selectivity.
- `references/rewrite-patterns.md` — before/after sargable rewrites and anti-patterns.
- `references/dialect-cheatsheet.md` — per-engine commands to collect plans, stats, and metadata.
- `scripts/explain_analyzer.py` — flags problems in a PostgreSQL JSON plan (stdlib only).
- `examples/slow-query-walkthrough.md` — a full worked diagnosis from plan to verified fix.
- `templates/optimization-report.md` — fill-in report template for handing off the result.
