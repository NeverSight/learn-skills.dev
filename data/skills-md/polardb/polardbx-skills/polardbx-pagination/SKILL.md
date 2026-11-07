---
name: polardbx-pagination
description: |
  Efficient pagination and large table traversal for PolarDB-X 2.0 Enterprise Edition. Recommends Keyset pagination (cursor pagination) over LIMIT M,N for deep pagination scenarios, provides per-shard traversal for extreme cases, includes index requirements and complete Java code examples.
  Use when implementing pagination queries, traversing large tables, exporting data in batches, or optimizing slow LIMIT M,N queries on PolarDB-X.
  Triggers: "分页查询", "deep pagination", "Keyset pagination", "大表遍历", "数据导出", "LIMIT优化", "分页性能", "cursor pagination", "游标分页", "翻页慢", "深翻页", "pagination query", "batch traversal", "LIMIT M N slow", "efficient paging"
metadata:
  version: 0.1.1
---

# PolarDB-X Efficient Pagination — Keyset Pagination & Large Table Traversal

Implement efficient pagination for PolarDB-X 2.0 Enterprise Edition (AUTO mode) that maintains constant performance regardless of page depth. Covers Keyset pagination strategies, per-shard traversal, index requirements, and production-ready Java code.

**Scope**: PolarDB-X 2.0 Enterprise Edition + AUTO mode database only.

## Why LIMIT M, N Fails for Deep Pagination

- **Standalone DB cost**: O(M+N) — must scan M rows before returning N rows.
- **Distributed DB cost**: O(M+N) × number of shards — each shard returns M+N rows to CN for merge-sort.
- **Result**: Performance degrades linearly as page number increases; unacceptable for large tables.

> For small data volumes with shallow pagination (< 1000 offset), `LIMIT M, N` is acceptable.

## Core Workflow

1. **Determine the pagination scenario**:
   - Does the table use New Sequence (AUTO mode default)? → Scenario A
   - Is the sort column potentially non-unique (time column, group sequence ID)? → Scenario B
   - Are there extreme stability requirements with many shards? → Per-shard traversal

2. **Select the pagination strategy** (see Quick Reference below).

3. **Verify cursor correctness and consistency**: use immutable keys that are globally unique as a tuple; handle nullable sort keys explicitly. Decide whether pages are best-effort live reads or an exact snapshot/export. Independent autocommit pages can miss late commits or updates behind the cursor.

4. **Verify index exists** for the sort columns (critical for performance).

5. **Generate code** with JDBC settings matching the chosen consistency model.

## Pagination Strategies Quick Reference

### Scenario A: New Sequence ID (AUTO mode default)

A globally unique ID defines a deterministic cursor order, but sequence allocation order does not imply commit-time order:

```sql
-- First batch
SELECT * FROM t1 ORDER BY id LIMIT 1000;

-- Subsequent batches (record last_id from previous batch)
SELECT * FROM t1 WHERE id > :last_id ORDER BY id LIMIT 1000;
```

Cost: O(N) constant, regardless of page depth.

### Scenario B: Sort Column May Have Duplicates (time columns, etc.)

Use an immutable, globally unique `(sort_column, id)` tuple as the cursor. The example assumes both fields are non-NULL; otherwise explicitly paginate the NULL segment or use an equivalent non-NULL sort key:

```sql
-- First batch
SELECT * FROM t1 ORDER BY gmt_create, id LIMIT 1000;

-- Subsequent batches (record last_gmt_create and last_id)
SELECT * FROM t1
WHERE (gmt_create, id) > (:last_gmt_create, :last_id)
ORDER BY gmt_create, id LIMIT 1000;
```

PolarDB-X supports tuple comparison `(col1, col2) > (?, ?)` and can leverage composite indexes.

### Per-Shard Traversal (Advanced)

For extreme scenarios (many shards, relaxed ordering):

```sql
-- 1. Get topology
SHOW TOPOLOGY FROM t1;

-- 2. Paginate within each shard using HINT
/*+TDDL:NODE('partition_name')*/
SELECT * FROM t1 WHERE (gmt_create, id) > (?, ?)
ORDER BY gmt_create, id LIMIT 1000;
```

## Index Requirements

| Sort Method | Required Index |
|-------------|---------------|
| `ORDER BY id` | Primary key (usually exists) |
| `ORDER BY gmt_create, id` | `(gmt_create, id)` composite index |
| `ORDER BY c1, gmt_create, id` (with `WHERE c1 = ?`) | `(c1, gmt_create, id)` composite index |

```sql
-- Create composite index for pagination
ALTER TABLE t1 ADD INDEX idx_page (gmt_create, id);
```

## Method Comparison

| Method | Performance | Applicable Scenarios | Notes |
|--------|-------------|---------------------|-------|
| `LIMIT M, N` | O(M+N), degrading | Shallow pagination, small data | Even worse in distributed systems |
| Keyset (id) | O(N), constant | Traverse in ID order | Requires globally unique ID; not commit-time order |
| Keyset (sort_col, id) | O(N), constant | Sort columns with possible duplicates | Requires composite index |
| Per-shard traversal | O(N), constant | Many shards, relaxed ordering | Requires SHOW TOPOLOGY + HINT |
| Batch Tool | Internally optimized | Data export | Dedicated tool |

## Java JDBC Settings

| Parameter | Value | Reason |
|-----------|-------|--------|
| `netTimeoutForStreamingResults` | `0` | Avoid streaming read timeouts |
| `socketTimeout` | As needed (ms) | Avoid long queries being disconnected |
| `setFetchSize` | `Integer.MIN_VALUE` | Enable streaming reads (avoid OOM) |
| `autocommit` | `true` for best-effort live browsing | Avoid long transactions; pages do not share a snapshot |

For exact exports, define a stable snapshot or quiesce writes; if using change capture, reconcile changes against the chosen snapshot boundary. A maximum-ID watermark alone does not catch late commits with smaller IDs. Do not promise omission-free traversal from independent page reads.

## Best Practices

1. **Never use LIMIT M,N for deep pagination** on large tables — cost grows linearly.
2. **Always create composite indexes** matching your ORDER BY columns.
3. **Use tuple comparison** `(col, id) > (?, ?)` for non-unique sort columns — PolarDB-X supports this natively.
4. **Choose autocommit by consistency requirements**: use `autocommit=true` for best-effort live browsing; for exact exports, use an appropriate snapshot/export strategy and assess long-transaction costs.
5. **Use streaming reads** (`fetchSize = Integer.MIN_VALUE`) to avoid loading entire result sets into memory.
6. **Consider Batch Tool** for pure data export scenarios — it has built-in PolarDB-X optimizations.

## Reference

| Reference | Description |
|-----------|-------------|
| [references/pagination-best-practice.md](references/pagination-best-practice.md) | Complete pagination guide: all scenarios, per-shard traversal details, full Java code example, Batch Tool, FAQ |
