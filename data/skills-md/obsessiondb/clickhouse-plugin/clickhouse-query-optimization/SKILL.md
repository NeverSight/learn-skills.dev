---
name: clickhouse-query-optimization
description: "20+ optimization rules for ClickHouse queries. Load when writing queries, debugging slow queries, fixing memory errors, or optimizing JOINs. Achieves 10-100x faster queries, 90% less memory usage."
---

# ClickHouse Query Optimization

Load when writing, debugging, or optimizing ClickHouse queries.

## Goals

- 10-100x faster query execution
- 90%+ reduction in memory usage
- Eliminate full table scans (read <1% of data)
- JOINs that complete in milliseconds instead of minutes

## Reference Documentation

- [Query Optimization](https://clickhouse.com/docs/optimize/query-optimization)
- [PREWHERE](https://clickhouse.com/docs/optimize/prewhere)
- [JOINs](https://clickhouse.com/docs/best-practices/minimize-optimize-joins)
- [Dictionaries](https://clickhouse.com/docs/sql-reference/dictionaries)
- [Query Settings](https://clickhouse.com/docs/operations/settings/query-level)

**Search terms:** query optimization, PREWHERE, JOIN, dictionary, EXPLAIN, performance, slow query, memory limit, timeout, full table scan, dictGet, query cache, DELETE, UPDATE, mutation, aggregation, GROUP BY, COUNT DISTINCT, uniq, query_log

## Critical Rules

### [CRITICAL]

1. **Filter on ORDER BY prefix columns.** Queries that skip the prefix scan the entire table.
2. **Avoid SELECT *.** Only select columns you need.
3. **Always check EXPLAIN indexes=1.** Verify index usage and row estimates before optimizing.

### [HIGH]

4. **Use PREWHERE for selective filters.** Reduces I/O before main WHERE clause.
5. **Prefer dictionaries over JOINs.** For key-value lookups on tables <10M rows.
6. **Use IN subqueries for existence checks.** Faster than JOIN when you don't need columns from the other table.

### [MEDIUM]

7. **Limit JOINs when possible.** Each JOIN increases complexity exponentially.

## Querying basics: ORDER BY, indexes and PREWHERE

### ORDER BY

The `ORDER BY` clause in table definition determines query performance. ClickHouse stores data sorted by these columns and uses a sparse primary index to skip irrelevant data.

**How it works:**

- Data is divided into granules (default 8192 rows), can vary
- Primary index stores first value of each granule for ORDER BY columns
- Queries filtering on ORDER BY prefix in exact order or a prefix of it skip entire granules

```sql
-- Table: ORDER BY (tenant_id, event_date, user_id)

-- FAST: Filters on ORDER BY prefix (left to right)
WHERE tenant_id = 1                              -- Uses index
WHERE tenant_id = 1 AND event_date = '2024-01-15' -- Uses index
WHERE tenant_id = 1 AND event_date >= '2024-01-01' AND user_id = 123 -- Uses index

-- SLOW: Skips columns or filters only on later columns
WHERE event_date = '2024-01-15'                  -- Skips tenant_id, full scan
WHERE user_id = 123                              -- Skips tenant_id and event_date, full scan
```

**Key insight:** Always filter on the leftmost ORDER BY columns first for best performance.

### Indexes

Skip indexes (data skipping indexes) help when filtering on columns NOT in ORDER BY:

```sql
-- Table has ORDER BY (tenant_id, event_date, user_id)
-- But you need to query by session_id

-- Add bloom filter index
ALTER TABLE events
ADD INDEX idx_session session_id TYPE bloom_filter(0.01) GRANULARITY 4;

-- Now this query can skip granules instead of full scan
SELECT * FROM events WHERE session_id = 'abc123';
```

**Check if index is used:**

```sql
EXPLAIN indexes = 1
SELECT * FROM events WHERE session_id = 'abc123';

-- Look for "Skip" section showing granules skipped
```

**Common index types:**

- `bloom_filter` - High-cardinality columns (UUIDs, session IDs)
- `minmax` - Range queries on numeric/date columns
- `set(N)` - Low-cardinality columns (<N unique values)

### PREWHERE vs WHERE

| Clause   | When columns are read               | Use for                            |
| -------- | ----------------------------------- | ---------------------------------- |
| PREWHERE | Before other columns                | Small columns, selective filters   |
| WHERE    | After all selected columns are read | Large columns, complex expressions |

````sql
-- Small status column in PREWHERE, large error_message in WHERE
SELECT * FROM events
PREWHERE status = 'error'
WHERE error_message LIKE '%timeout%';

## Column Selection

### Always Specify Columns

```sql
-- BAD: Reads all columns from disk
SELECT * FROM events WHERE user_id = 123;

-- GOOD: Reads only needed columns
SELECT event_time, event_type, properties
FROM events
WHERE user_id = 123;
````

### Full Example

```sql
-- Table definition
CREATE TABLE events (
    tenant_id UInt32,
    event_date Date,
    user_id UInt64,
    status LowCardinality(String),    -- 4 bytes per row
    error_message String,              -- 500 bytes avg per row
    payload String                     -- 2KB avg per row
) ENGINE = MergeTree()
ORDER BY (tenant_id, event_date, user_id);

-- Table has 100M rows across 12,000 granules (8192 rows each)
```

```sql
-- Query
SELECT user_id, error_message, payload
FROM events
PREWHERE tenant_id = 5 AND event_date = '2024-01-15' AND status = 'error'
WHERE error_message LIKE '%timeout%';
```

**Step 1: Primary index (granule filtering)**

```
Primary index stores first row of each granule:
  Granule 0:    tenant_id=1,  event_date=2024-01-01
  Granule 1:    tenant_id=1,  event_date=2024-01-01
  ...
  Granule 846:  tenant_id=5,  event_date=2024-01-14
  Granule 847:  tenant_id=5,  event_date=2024-01-15  ← Match
  Granule 848:  tenant_id=5,  event_date=2024-01-15  ← Match
  Granule 849:  tenant_id=5,  event_date=2024-01-15  ← Match
  Granule 850:  tenant_id=5,  event_date=2024-01-16
  ...

Result: Read 3 granules out of 12,000 (skip 99.97% of data)
```

> **Note:** Skip indexes work similarly—they allow ClickHouse to skip granules for columns not in ORDER BY. Both mechanisms achieve the same goal: read less data by eliminating irrelevant granules before touching the actual rows.

**Step 2: PREWHERE (column filtering within granules)**

```
For the 3 matching granules (24,576 rows):

  1. Read tenant_id column      →  98 KB   (4 bytes × 24,576)
  2. Read event_date column     →  98 KB   (4 bytes × 24,576)
  3. Read status column         →  98 KB   (4 bytes × 24,576)
  4. Filter: 1,247 rows match PREWHERE conditions

  5. Read user_id column        →  10 KB   (8 bytes × 1,247 rows only)
  6. Read error_message column  →  623 KB  (500 bytes × 1,247 rows only)
  7. Read payload column        →  2.4 MB  (2KB × 1,247 rows only)

Total read: ~3.3 MB
Without PREWHERE: ~62 MB (read all columns for all 24,576 rows)
```

**Step 3: WHERE (final filtering)**

```
Apply: error_message LIKE '%timeout%'
Result: 43 rows returned
```

### Impact

Reading fewer columns:

- Reduces disk I/O
- Improves compression efficiency
- Lowers memory usage

## JOIN Optimization

### Decision Tree

```
Need data from another table?
│
├─ Only filtering rows, don't need columns from other table?
│  Example: "Get orders, but only for premium users"
│  └─ Use IN subquery
│
├─ Need columns from other table?
│  Example: "Get orders WITH user name and email"
│  │
│  ├─ Small lookup table (<10M rows), staleness OK?
│  │  └─ Use Dictionary
│  │
│  └─ Need real-time data or large table?
│     └─ Use JOIN with filtered subqueries
│
└─ Same join needed on every query?
   └─ Denormalize at insert time
```

### Full Example: Dictionary vs JOIN

```sql
-- Tables
-- events: 500M rows, ORDER BY (tenant_id, event_date, user_id)
-- users: 2M rows (user_id, name, tier, country)

-- Task: Get user name and tier for today's events
```

**Slow: JOIN**

```sql
SELECT e.event_time, e.event_type, u.name, u.tier
FROM events e
JOIN users u ON e.user_id = u.user_id
WHERE e.tenant_id = 1 AND e.event_date = today();

-- Execution:
-- 1. Scan events: 850K rows
-- 2. Build hash table from users: 2M rows loaded into memory
-- 3. Probe hash table for each event row
-- Time: 3.2s, Memory: 890MB
```

**Fast: Dictionary**

```sql
-- Create once
CREATE DICTIONARY user_dict (
    user_id UInt64,
    name String,
    tier String
)
PRIMARY KEY user_id
SOURCE(CLICKHOUSE(TABLE 'users'))
LAYOUT(HASHED())
LIFETIME(300);

-- Query
SELECT
    event_time,
    event_type,
    dictGet('user_dict', 'name', user_id) AS name,
    dictGet('user_dict', 'tier', user_id) AS tier
FROM events
WHERE tenant_id = 1 AND event_date = today();

-- Execution:
-- 1. Scan events: 850K rows
-- 2. Dictionary lookup: O(1) hash lookup per row, already in memory
-- Time: 0.4s, Memory: 120MB
```

**Tradeoff:** Dictionaries are eventually consistent. `LIFETIME(300)` means data can be up to 5 minutes stale. For real-time accuracy, use JOIN. Always ask the user if this delay is acceptable before implementing a dictioary.

```sql
-- Check when dictionary was last updated
SELECT name, last_successful_update_time, loading_duration
FROM system.dictionaries;

-- Force immediate reload
SYSTEM RELOAD DICTIONARY user_dict;
```

### IN Subquery for Filtering

When you only need to filter (not fetch columns):

```sql
-- Get orders from premium users
SELECT *
FROM orders
WHERE user_id IN (
    SELECT user_id FROM users WHERE tier = 'premium'
);

-- NOT this (builds unnecessary hash table)
SELECT o.*
FROM orders o
JOIN users u ON o.user_id = u.user_id
WHERE u.tier = 'premium';
```

### When You Must JOIN

Filter both sides first, smaller table on the right:

````sql
SELECT e.event_time, u.name, u.email
FROM (
    SELECT event_time, user_id
    FROM events
    WHERE tenant_id = 1 AND event_date = today()
) e
JOIN (
    SELECT user_id, name, email
    FROM users
    WHERE active = 1
) u ON e.user_id = u.user_id;

## Query Analysis

### EXPLAIN Queries

```sql
-- Basic execution plan
EXPLAIN SELECT ...;

-- Show index usage (most useful)
EXPLAIN indexes = 1 SELECT ...;

-- Show execution pipeline
EXPLAIN PIPELINE SELECT ...;

-- Show query AST
EXPLAIN AST SELECT ...;
````

### Reading EXPLAIN indexes Output

```sql
EXPLAIN indexes = 1
SELECT count()
FROM events
WHERE tenant_id = 1 AND event_date = '2024-01-15';

-- Output interpretation:
-- ReadFromMergeTree
--   Indexes:
--     PrimaryKey
--       Keys: tenant_id, event_date
--       Condition: (tenant_id = 1) AND (event_date = '2024-01-15')
--       Parts: 5/120           <- 5 parts selected out of 120
--       Granules: 42/15000     <- 42 granules out of 15000 (good!)
```

### Find Slow Queries

```sql
-- Recent slow queries
SELECT
    query,
    query_duration_ms,
    read_rows,
    read_bytes,
    memory_usage
FROM system.query_log
WHERE type = 'QueryFinish'
  AND query_duration_ms > 1000
  AND event_date >= today() - 1
ORDER BY query_duration_ms DESC
LIMIT 20;

-- Queries with full table scans
SELECT
    query,
    read_rows,
    total_rows_approx
FROM system.query_log
WHERE type = 'QueryFinish'
  AND read_rows > 0.9 * total_rows_approx  -- Reading >90% of table
  AND event_date >= today() - 1
ORDER BY read_rows DESC
LIMIT 10;
```

### Profile Query Execution

```sql
-- Enable query profiling
SET log_queries = 1;
SET log_query_threads = 1;

-- Run your query
SELECT ...;

-- Check thread-level metrics
SELECT
    thread_name,
    sum(read_rows) AS rows,
    sum(read_bytes) AS bytes,
    max(peak_memory_usage) AS peak_memory
FROM system.query_thread_log
WHERE query_id = '<your-query-id>'
GROUP BY thread_name;
```

## Query Cache (22.8+)

Cache query results for repeated identical queries:

```sql
-- Enable query cache for a session
SET use_query_cache = 1;

-- Run query (first execution populates cache)
SELECT count(*), avg(amount)
FROM orders
WHERE order_date >= '2024-01-01';

-- Subsequent identical queries return cached result instantly
-- Cache invalidated automatically when underlying data changes
```

**Configuration:**

```sql
-- Set cache TTL (default: 60 seconds)
SET query_cache_ttl = 300;  -- 5 minutes

-- Minimum rows to cache (skip small results)
SET query_cache_min_query_runs = 2;  -- Cache after 2nd run

-- Check cache status
SELECT * FROM system.query_cache;
```

**Best for:**

- Dashboard queries hitting same data repeatedly
- Reports regenerated frequently
- Multi-tenant queries with shared dimensions
- Queries that do not need real-time data

Update rows without full table rewrite:

```sql
-- Update specific columns
ALTER TABLE events
UPDATE status = 'processed'
WHERE event_id = 12345;

-- Can update multiple columns
ALTER TABLE events
UPDATE
    status = 'cancelled',
    cancelled_at = now()
WHERE order_id IN (SELECT order_id FROM cancelled_orders);
```

**Limitations:**

- Cannot update columns in ORDER BY or PARTITION BY
- Uses mutations (async, check progress in system.mutations)

```sql
-- Check mutation progress
SELECT table, command, is_done, latest_fail_reason
FROM system.mutations
WHERE database = 'default'
ORDER BY create_time DESC;
```

## EXPLAIN ESTIMATE

Get row/byte estimates without running query:

```sql
-- Estimate data to be read
EXPLAIN ESTIMATE
SELECT * FROM events
WHERE tenant_id = 1 AND event_date = '2024-01-15';

-- Output shows:
--   estimated_rows
--   estimated_bytes
--   number of parts/granules to read
```

**Use for:**

- Validating filter effectiveness before running
- Cost comparison between query approaches
- Capacity planning

## Troubleshooting

**Always ask for user confirmation before applying schema changes (adding indexes, creating MVs, altering tables).**

### Memory Limit Exceeded

**Problem:** `Memory limit exceeded`, `DB::Exception: Memory limit exceeded`, query killed by OOM

**Diagnose:**

```sql
EXPLAIN indexes = 1 SELECT ...;  -- Check if filtering is effective
```

**Solutions:**

| Cause                     | Fix                                                           |
| ------------------------- | ------------------------------------------------------------- |
| High-cardinality GROUP BY | Use approximate: `uniqHLL12()` instead of `COUNT(DISTINCT)`   |
| Large aggregation         | Pre-aggregate with `AggregatingMergeTree` + Materialized View |
| Full table scan           | Add filters on ORDER BY columns (see below)                   |
| Too many columns          | Select only needed columns                                    |

```sql
-- BAD: Exact distinct on high cardinality
SELECT COUNT(DISTINCT user_id) FROM events;

-- GOOD: Approximate (2% error, 10x less memory)
SELECT uniqHLL12(user_id) FROM events;

-- BETTER: Pre-aggregate with MV (see clickhouse-materialized-views skill)
```

### Full Table Scan Despite Filters

**Problem:** Query reads all rows, slow despite WHERE clause, `Granules: N/N` in EXPLAIN

**Diagnose:**

```sql
EXPLAIN indexes = 1
SELECT * FROM events WHERE user_id = 123;
-- If "Granules: N/N" → index not used
```

**Solutions:**

| Cause                         | Fix                                              |
| ----------------------------- | ------------------------------------------------ |
| Filter not on ORDER BY prefix | Add ORDER BY columns to WHERE, or add skip index |
| Function on column            | Store computed column, filter on that            |
| OR across ORDER BY columns    | Rewrite as UNION ALL                             |
| Type mismatch                 | Match filter type to column type                 |

```sql
-- BAD: Function prevents index use
WHERE toDate(event_time) = '2024-01-15'

-- GOOD: Store date column, filter on it
WHERE event_date = '2024-01-15'

-- BAD: Skips ORDER BY prefix (tenant_id, event_date, user_id)
WHERE user_id = 123

-- GOOD: Include prefix columns
WHERE tenant_id = 1 AND event_date = today() AND user_id = 123

-- ALT: Add skip index if you can't change query
ALTER TABLE events ADD INDEX idx_user user_id TYPE bloom_filter(0.01) GRANULARITY 4;
```

### Slow JOINs

**Problem:** JOINs take minutes, high memory during JOIN, query hangs on JOIN step

**Solutions (in order of preference):**

| Approach           | When to Use                                         |
| ------------------ | --------------------------------------------------- |
| Dictionary         | Lookup table <10M rows, staleness OK                |
| IN subquery        | Only filtering, don't need columns from other table |
| Filter before JOIN | Must JOIN, but can reduce rows first                |
| Denormalize        | Same JOIN on every query                            |

```sql
-- BAD: JOIN builds hash table of entire users table
SELECT e.*, u.name FROM events e JOIN users u ON e.user_id = u.user_id;

-- GOOD: Dictionary lookup (see "Dictionary vs JOIN" section)
SELECT *, dictGet('user_dict', 'name', user_id) AS name FROM events;

-- GOOD: IN subquery when only filtering
SELECT * FROM events WHERE user_id IN (SELECT user_id FROM users WHERE tier = 'premium');

-- GOOD: Filter both sides before JOIN
SELECT e.*, u.name
FROM (SELECT * FROM events WHERE tenant_id = 1 AND event_date = today()) e
JOIN (SELECT user_id, name FROM users WHERE active = 1) u ON e.user_id = u.user_id;
```

### High Disk I/O

**Problem:** Queries slow with high `read_bytes`, disk wait times high, reading GBs for simple queries

**Solutions:**

| Cause               | Fix                                              |
| ------------------- | ------------------------------------------------ |
| Reading all columns | Select only needed columns                       |
| No early filtering  | Use PREWHERE on small, selective columns         |
| Missing skip index  | Add bloom_filter for high-cardinality lookups    |
| Poor compression    | Use appropriate codecs (see schema-design skill) |

```sql
-- BAD: Reads all columns, filters late
SELECT * FROM events WHERE status = 'error';

-- GOOD: PREWHERE filters before reading large columns
SELECT event_time, error_message
FROM events
PREWHERE status = 'error'
WHERE error_message LIKE '%timeout%';
```
