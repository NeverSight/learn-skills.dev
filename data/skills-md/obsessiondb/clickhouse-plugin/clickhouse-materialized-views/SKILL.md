---
name: clickhouse-materialized-views
description: "10+ patterns for ClickHouse Materialized Views. Load when creating MVs for real-time aggregation, data transformation, or query optimization. Covers SummingMergeTree, AggregatingMergeTree, and common pitfalls."
---

# ClickHouse Materialized Views

Load when creating Materialized Views for real-time aggregation, ETL pipelines, or query optimization.

**Prerequisite:** Understand MergeTree engine variants in `clickhouse-schema-design` skill.

## Reference Documentation

- [Materialized Views](https://clickhouse.com/docs/materialized-view)
- [AggregatingMergeTree](https://clickhouse.com/docs/engines/table-engines/mergetree-family/aggregatingmergetree)
- [Altinity: MV Best Practices](https://kb.altinity.com/altinity-kb-schema-design/materialized-views/)

**Search terms:** materialized view, MV, real-time aggregation, AggregateFunction, -State, -Merge, SummingMergeTree, pre-aggregation, incremental

## Critical Rules

### [CRITICAL]

1. **MVs are triggers, not caches.** They process INSERT data, not query results.
2. **Use correct engine.** AggregatingMergeTree for complex aggregates, SummingMergeTree for simple counters.
3. **Query with -Merge functions or argMax.** Aggregation completes at query time, not insert time.
4. **Chained MVs see the pre-aggregated block, NOT the merged table state.** A downstream MV (A→B→C) receives the block just inserted into B's target table — already grouped by the upstream MV's SELECT, but not merged with existing data. This means each insert batch is processed independently and `-MergeState` is required when chaining AggregatingMergeTree MVs.

### [HIGH]

5. **MV sees INSERT only.** No backfill; existing data must be inserted manually.
6. **ORDER BY in target must match GROUP BY in MV.** Otherwise aggregation won't work properly.

### [MEDIUM]

7. **Avoid too many MVs on one source table when possible.** Each MV adds overhead to every INSERT.

## How Materialized Views Work

```
Source Table ──INSERT──► MV Transform ──► Target Table
                │
                └─ MV executes SELECT for each inserted block
```

**Key insight:** The MV's SELECT query runs on each INSERT batch. Results go to the target table. The MV does NOT query historical data.

## Pattern 1: Real-Time Counters (SummingMergeTree)

Best for simple sums and counts that need real-time updates.

```sql
-- Source: raw events
CREATE TABLE events (
    event_time DateTime,
    tenant_id UInt32,
    event_type String,
    user_id UInt64
) ENGINE = MergeTree()
ORDER BY (tenant_id, event_time);

-- Target: daily counters
CREATE TABLE daily_event_counts (
    date Date,
    tenant_id UInt32,
    event_type LowCardinality(String),
    event_count UInt64,
    unique_users UInt64
)
ENGINE = SummingMergeTree()
ORDER BY (tenant_id, date, event_type);

-- MV: transform inserts
CREATE MATERIALIZED VIEW daily_event_counts_mv
TO daily_event_counts AS
SELECT
    toDate(event_time) AS date,
    tenant_id,
    event_type,
    count() AS event_count,
    uniq(user_id) AS unique_users  -- WARNING: Not additive!
FROM events
GROUP BY date, tenant_id, event_type;
```

**Warning:** `uniq()` in SummingMergeTree is not accurate—sums don't equal unique counts. Use AggregatingMergeTree for unique counts.

## Pattern 2: Complex Aggregates (AggregatingMergeTree)

For accurate uniq, quantiles, or any non-additive aggregate.

```sql
-- Target: uses AggregateFunction types
CREATE TABLE user_metrics_agg (
    date Date,
    tenant_id UInt32,
    total_events AggregateFunction(sum, UInt64),
    unique_users AggregateFunction(uniq, UInt64),
    p95_duration AggregateFunction(quantile(0.95), Float32)
)
ENGINE = AggregatingMergeTree()
ORDER BY (tenant_id, date);

-- MV: use -State functions
CREATE MATERIALIZED VIEW user_metrics_mv
TO user_metrics_agg AS
SELECT
    toDate(event_time) AS date,
    tenant_id,
    sumState(1) AS total_events,
    uniqState(user_id) AS unique_users,
    quantileState(0.95)(duration_ms) AS p95_duration
FROM events
GROUP BY date, tenant_id;

-- Query: use -Merge functions
SELECT
    date,
    tenant_id,
    sumMerge(total_events) AS events,
    uniqMerge(unique_users) AS users,
    quantileMerge(0.95)(p95_duration) AS p95
FROM user_metrics_agg
WHERE tenant_id = 1
GROUP BY date, tenant_id;
```

**Key pattern:** `-State` to insert, `-Merge` to query.

## Pattern 3: Data Transformation Pipeline

Transform/enrich data as it arrives.

```sql
-- Source: raw JSON logs
CREATE TABLE raw_logs (
    timestamp DateTime,
    raw_json String
) ENGINE = MergeTree()
ORDER BY timestamp;

-- Target: parsed structured data
CREATE TABLE parsed_logs (
    timestamp DateTime,
    level LowCardinality(String),
    service LowCardinality(String),
    message String,
    trace_id String
)
ENGINE = MergeTree()
ORDER BY (service, timestamp);

-- MV: parse JSON on insert
CREATE MATERIALIZED VIEW parsed_logs_mv
TO parsed_logs AS
SELECT
    timestamp,
    JSONExtractString(raw_json, 'level') AS level,
    JSONExtractString(raw_json, 'service') AS service,
    JSONExtractString(raw_json, 'message') AS message,
    JSONExtractString(raw_json, 'trace_id') AS trace_id
FROM raw_logs;
```

## Pattern 4: Last Value Tracking (ReplacingMergeTree)

Track latest state per entity.

```sql
-- Target: latest user state
CREATE TABLE user_latest_state (
    user_id UInt64,
    last_seen DateTime,
    last_action LowCardinality(String),
    total_actions UInt64
)
ENGINE = ReplacingMergeTree(last_seen)
ORDER BY user_id;

-- MV: update on each event
CREATE MATERIALIZED VIEW user_state_mv
TO user_latest_state AS
SELECT
    user_id,
    max(event_time) AS last_seen,
    argMax(event_type, event_time) AS last_action,
    count() AS total_actions
FROM events
GROUP BY user_id;
```

**Query with argMax pattern (avoid FINAL on large tables):**

```sql
SELECT
    user_id,
    argMax(last_seen, last_seen) AS last_seen,
    argMax(last_action, last_seen) AS last_action,
    argMax(total_actions, last_seen) AS total_actions
FROM user_latest_state
WHERE user_id = 123
GROUP BY user_id;
```

## Backfilling Existing Data

MVs don't process existing data. Backfill manually:

```sql
-- Insert historical data into target table
INSERT INTO daily_event_counts
SELECT
    toDate(event_time) AS date,
    tenant_id,
    event_type,
    count() AS event_count,
    uniq(user_id) AS unique_users
FROM events
WHERE event_time < '2024-01-01'  -- Before MV was created
GROUP BY date, tenant_id, event_type;
```

## MV Management

### Check MV Status

```sql
-- List all MVs
SELECT name, engine, create_table_query
FROM system.tables
WHERE engine = 'MaterializedView';

-- Check target table size
SELECT
    table,
    formatReadableSize(sum(bytes_on_disk)) AS size,
    sum(rows) AS rows
FROM system.parts
WHERE active AND table = 'daily_event_counts'
GROUP BY table;
```

### Pause/Resume MV

```sql
-- Pause (stop processing inserts)
ALTER TABLE events DETACH MATERIALIZED VIEW daily_event_counts_mv;

-- Resume
ALTER TABLE events ATTACH MATERIALIZED VIEW daily_event_counts_mv;
```

### Modify MV

MVs cannot be altered. Drop and recreate:

```sql
DROP VIEW daily_event_counts_mv;
-- Optionally truncate target: TRUNCATE TABLE daily_event_counts;
CREATE MATERIALIZED VIEW daily_event_counts_mv TO daily_event_counts AS ...;
-- Backfill if needed
```

## Common Pitfalls

| Pitfall                                 | Problem                               | Solution                                                                                                                   |
| --------------------------------------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Using `uniq()` with SummingMergeTree    | Sums don't equal uniques              | Use AggregatingMergeTree with `uniqState/uniqMerge`                                                                        |
| Forgetting argMax or -Merge             | Incomplete aggregation results        | Use `argMax` pattern for Replacing/Collapsing, `-Merge` for Aggregating                                                    |
| No backfill after MV creation           | Missing historical data               | Manually INSERT historical aggregates                                                                                      |
| MV on wrong table                       | Inserts to wrong source ignored       | Ensure MV is on the table receiving INSERTs                                                                                |
| Too many MVs on one source              | Slow inserts                          | Consider fewer MVs or async processing                                                                                     |
| Assuming chain is cheaper than parallel | Wrong topology choice                 | Chain and parallel have nearly identical resource cost — choose topology based on query granularity needs, not performance |
| Chained MV reads final table state      | Wrong aggregation logic, missing data | Downstream MVs see the pre-aggregated block, not merged state — use `-MergeState` when chaining AggregatingMergeTree       |

## Decision Tree

```
Need to aggregate data at query time?
│
├─ Yes, and data changes frequently → Query raw data
│
├─ Yes, but queries are slow → Create MV
│  │
│  ├─ Simple sums/counts only?
│  │  └─ SummingMergeTree
│  │
│  ├─ Need uniq, quantile, or complex aggregates?
│  │  └─ AggregatingMergeTree with -State/-Merge
│  │
│  └─ Need latest value per key?
│     └─ ReplacingMergeTree with argMax pattern
│
└─ Need to transform/parse data on insert?
   └─ MV with regular MergeTree target
```

## Complete Example: Multi-Level Aggregation

Chain MVs when each level serves different query granularity (hourly → daily). The downstream MV sees the **pre-aggregated block** (output of the upstream MV's SELECT), not the merged table state — use `-MergeState` to handle partial aggregation states.

**Cost note:** Chain (A→B→C) vs parallel (A→B, A→C) topologies have nearly identical resource consumption. The bottleneck is total data written to target tables, not the topology. Choose based on query needs, not performance assumptions.

```sql
-- Level 1: Raw events (source)
CREATE TABLE events (...) ENGINE = MergeTree() ORDER BY ...;

-- Level 2: Hourly aggregates
CREATE TABLE hourly_stats (
    hour DateTime,
    tenant_id UInt32,
    events AggregateFunction(sum, UInt64),
    users AggregateFunction(uniq, UInt64)
) ENGINE = AggregatingMergeTree() ORDER BY (tenant_id, hour);

CREATE MATERIALIZED VIEW hourly_mv TO hourly_stats AS
SELECT
    toStartOfHour(event_time) AS hour,
    tenant_id,
    sumState(1) AS events,
    uniqState(user_id) AS users
FROM events GROUP BY hour, tenant_id;

-- Level 3: Daily aggregates (from hourly)
-- daily_mv receives the pre-aggregated block inserted into hourly_stats
-- (already grouped by hour/tenant with -State values), but NOT merged
-- with existing hourly_stats data. sumMergeState/uniqMergeState handles
-- this: merges partial -State values within the block, then re-wraps as -State.
CREATE TABLE daily_stats (
    date Date,
    tenant_id UInt32,
    events AggregateFunction(sum, UInt64),
    users AggregateFunction(uniq, UInt64)
) ENGINE = AggregatingMergeTree() ORDER BY (tenant_id, date);

CREATE MATERIALIZED VIEW daily_mv TO daily_stats AS
SELECT
    toDate(hour) AS date,
    tenant_id,
    sumMergeState(events) AS events,   -- Merge partial states from block, then re-State
    uniqMergeState(users) AS users
FROM hourly_stats GROUP BY date, tenant_id;
```

**Query any level:**

```sql
-- Fast daily query
SELECT date, sumMerge(events), uniqMerge(users)
FROM daily_stats WHERE tenant_id = 1 GROUP BY date;

-- Drill down to hourly
SELECT hour, sumMerge(events), uniqMerge(users)
FROM hourly_stats WHERE tenant_id = 1 AND toDate(hour) = today() GROUP BY hour;
```

## Troubleshooting

**Always ask for user confirmation before creating/modifying MVs or target tables.**

### Wrong Aggregation Results

**Problem:** Counts are too high, uniq values don't match raw data, aggregates seem doubled

**Diagnose:**

```sql
-- Compare MV result vs raw query
SELECT count() FROM target_table;
SELECT count() FROM source_table WHERE <same_filters>;

-- Check for duplicate keys in target
SELECT date, tenant_id, count() AS rows
FROM target_table
GROUP BY date, tenant_id
HAVING rows > 1;
```

**Solutions:**

| Cause                                      | Fix                                                                     |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| Using `uniq()` with SummingMergeTree       | Switch to AggregatingMergeTree with `uniqState`/`uniqMerge`             |
| Forgetting `-Merge` in query               | Always use `sumMerge()`, `uniqMerge()` for AggregatingMergeTree         |
| Forgetting `argMax` for ReplacingMergeTree | Use argMax pattern: `SELECT key, argMax(col, version) ... GROUP BY key` |
| Duplicate inserts to source                | Deduplicate source or use ReplacingMergeTree for target                 |

```sql
-- BAD: uniq in SummingMergeTree (sums don't work)
ENGINE = SummingMergeTree()
-- SELECT uniq(user_id) AS users  -- Wrong!

-- GOOD: AggregatingMergeTree with State/Merge
ENGINE = AggregatingMergeTree()
-- MV: uniqState(user_id) AS users
-- Query: uniqMerge(users)
```

### MV Not Updating / Missing Data

**Problem:** Target table not receiving new data, counts stuck at old values

**Diagnose:**

```sql
-- Check if MV is attached
SELECT name, engine FROM system.tables WHERE engine = 'MaterializedView';

-- Check target table recent data
SELECT max(date), count() FROM target_table;

-- Verify source table is receiving inserts
SELECT max(event_time), count() FROM source_table WHERE event_time > now() - INTERVAL 1 HOUR;
```

**Solutions:**

| Cause                            | Fix                                                   |
| -------------------------------- | ----------------------------------------------------- |
| MV detached                      | `ALTER TABLE source ATTACH MATERIALIZED VIEW mv_name` |
| MV on wrong source table         | Drop MV, recreate with correct source                 |
| Historical data not backfilled   | Manually INSERT aggregated historical data            |
| Inserts going to different table | Ensure app inserts to the MV's source table           |

```sql
-- Backfill historical data
INSERT INTO target_table
SELECT
    toDate(event_time) AS date,
    tenant_id,
    sumState(1) AS events,
    uniqState(user_id) AS users
FROM source_table
WHERE event_time < '2024-01-01'  -- Before MV existed
GROUP BY date, tenant_id;
```

### Slow Inserts After Adding MV

**Problem:** INSERT performance degraded after creating MV, insert latency increased

**Diagnose:**

```sql
-- Check MVs on this table
SELECT name, as_select FROM system.tables
WHERE engine = 'MaterializedView' AND as_select LIKE '%source_table%';

-- Check MV query complexity
EXPLAIN SELECT ... FROM source_table ...;  -- Use MV's SELECT query
```

**Solutions:**

| Cause                                      | Fix                                        |
| ------------------------------------------ | ------------------------------------------ |
| Too many MVs on one source                 | Consolidate MVs or use async inserts       |
| Complex MV query (JOINs, heavy transforms) | Simplify MV, move complexity to query time |
| MV target table has wrong ORDER BY         | Match target ORDER BY to MV's GROUP BY     |

```sql
-- Example: MV groups by (tenant_id, date)
-- Target table ORDER BY should match
CREATE TABLE target (...)
ENGINE = AggregatingMergeTree()
ORDER BY (tenant_id, date);  -- Matches GROUP BY in MV
```

### Target Table Growing Too Large

**Problem:** MV target table larger than expected, not aggregating properly

**Diagnose:**

```sql
-- Check rows per key (should be 1 after merge for same GROUP BY)
SELECT date, tenant_id, count() AS rows
FROM target_table
GROUP BY date, tenant_id
ORDER BY rows DESC
LIMIT 10;
```

**Solutions:**

| Cause                                                   | Fix                                                  |
| ------------------------------------------------------- | ---------------------------------------------------- |
| ORDER BY doesn't match GROUP BY                         | Recreate target with ORDER BY matching MV's GROUP BY |
| Background merges haven't run                           | Wait for automatic merge, or use argMax in query     |
| Wrong engine (MergeTree instead of Summing/Aggregating) | Recreate with correct engine                         |

```sql
-- ORDER BY must match GROUP BY columns for proper aggregation
-- MV: GROUP BY (tenant_id, date, event_type)
-- Target: ORDER BY (tenant_id, date, event_type)  -- Must match!
```
