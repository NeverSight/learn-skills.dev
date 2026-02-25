---
name: clickhouse-query-optimization
description: |
  Optimizes ClickHouse queries for speed and efficiency. Helps with primary key design, sparse indexes, data skipping indexes (minmax, set, bloom filter, ngrambf_v1), partitioning strategies, projections, PREWHERE optimization, approximate functions, and query profiling with EXPLAIN. Use when writing ClickHouse queries, designing table schemas, analyzing slow queries, or implementing analytical aggregations. Works with columnar OLAP workloads.
allowed-tools: Read, Grep, Bash
---

# ClickHouse Query Optimization

## Quick Start

Check your query plan:

```sql
EXPLAIN
SELECT user_id, COUNT()
FROM events
WHERE timestamp >= '2024-01-01'
GROUP BY user_id;
```

This shows which parts of the index are used, how many partitions are read, and the aggregation strategy.

## When to Use

- Write fast ClickHouse queries
- Design table schemas
- Analyze slow queries
- Add data skipping indexes
- Implement partitioning strategies
- Use projections for multiple access patterns

## Core Principles

### 1. Primary Key Design

The primary key defines **sort order** (not uniqueness). Order columns by **low → high cardinality**.

```sql
-- Good: country (low) → user_id → timestamp (high)
CREATE TABLE events (
    user_id UInt32,
    timestamp DateTime,
    country String
)
ENGINE = MergeTree()
ORDER BY (country, user_id, timestamp);
```

**Key principle**: Queries must filter on **primary key prefix** to use index.

```sql
-- ✅ Fast: Uses index (country first)
SELECT * FROM events WHERE country = 'US';

-- ❌ Slow: Skips index (missing country)
SELECT * FROM events WHERE user_id = 12345;
```

### 2. Data Skipping Indexes

For non-primary-key columns:

```sql
-- Numeric ranges
ALTER TABLE events ADD INDEX idx_duration session_duration TYPE minmax GRANULARITY 4;

-- Categorical (low cardinality)
ALTER TABLE events ADD INDEX idx_event_type event_type TYPE set(100) GRANULARITY 4;

-- String equality
ALTER TABLE events ADD INDEX idx_url url TYPE bloom_filter(0.01) GRANULARITY 4;

-- Substring search
ALTER TABLE logs ADD INDEX idx_message message TYPE ngrambf_v1(4, 512, 3, 0) GRANULARITY 1;
```

### 3. Partitioning for Lifecycle Management

```sql
CREATE TABLE events (
    timestamp DateTime,
    user_id UInt32
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (user_id, timestamp);

-- Drop old data instantly
ALTER TABLE events DROP PARTITION '202401';

-- Or use TTL
ALTER TABLE events MODIFY TTL timestamp + INTERVAL 90 DAY;
```

### 4. Projections for Multiple Access Patterns

```sql
-- Main table sorted by user_id
CREATE TABLE events (
    user_id UInt32,
    product_id UInt32,
    timestamp DateTime
)
ENGINE = MergeTree()
ORDER BY (user_id, timestamp);

-- Add projection for product queries
ALTER TABLE events ADD PROJECTION proj_by_product (
    SELECT *
    ORDER BY (product_id, timestamp)
);

ALTER TABLE events MATERIALIZE PROJECTION proj_by_product;

-- Both queries now fast:
SELECT * FROM events WHERE user_id = 12345;    -- Uses main table
SELECT * FROM events WHERE product_id = 789;   -- Uses projection
```

### 5. Query Optimization

**PREWHERE for Early Filtering:**

```sql
SELECT user_id, event_type, properties
FROM events
PREWHERE timestamp >= '2024-01-01' AND country = 'US'  -- Small columns first
WHERE event_type IN ('purchase', 'signup');             -- Complex logic
```

**Approximate Functions:**

```sql
-- 10-100x faster, ~2% error
SELECT uniq(user_id) FROM events;                   -- vs COUNT(DISTINCT)
SELECT topK(10)(product_id) FROM events;            -- Approximate top-K
SELECT quantile(0.95)(response_time) FROM events;   -- Approximate percentile
```

**Select Only Needed Columns:**

```sql
-- Bad: Reads all columns
SELECT * FROM events WHERE user_id = 12345;

-- Good: Columnar advantage
SELECT user_id, timestamp, event_type FROM events WHERE user_id = 12345;
```

### 6. Profile and Debug

```sql
-- View execution plan
EXPLAIN SELECT COUNT() FROM events WHERE country = 'US';

-- Check performance
SELECT
    query,
    query_duration_ms,
    read_rows,
    read_bytes
FROM system.query_log
WHERE query LIKE '%events%'
ORDER BY event_time DESC
LIMIT 1;
```

## Common Patterns

| Technique | Problem Solved | Impact | When to Use |
|-----------|----------------|--------|------------|
| **Primary Key Design** | Index doesn't cover queries | Foundation | Always (design first) |
| **Data Skipping Indexes** | Non-primary filtering slow | 10-100x | After primary key |
| **Partitioning** | Need to delete old data | Instant deletion | Time-series with retention |
| **Projections** | Multiple query patterns | 100-1000x | Different sort orders |
| **Query Syntax** | Large columns read unnecessarily | 2-10x | Per-query optimization |
| **Profiling** | Don't know why slow | Insight | When optimization unclear |

## Supporting Files

| File | Purpose |
|------|---------|
| [examples/examples.md](examples/examples.md) | Real-world optimization scenarios with metrics |
| [references/reference.md](references/reference.md) | Technical guides and decision trees |

## Requirements

- ClickHouse 21.4+
- Understanding of SQL and aggregation
- Knowledge of query patterns

## Integration Tips

1. Design tables first (use EXPLAIN before/after)
2. Monitor query_log (alert on > 100M rows read)
3. Profile inserts (more indexes = slower writes)
4. Test projections (use EXPLAIN to confirm optimizer choice)

## See Also

- **Examples**: [examples/examples.md](examples/examples.md) - E-commerce, user events, time-series
- **Reference**: [references/reference.md](references/reference.md) - Index selection matrix, EXPLAIN guide, TTL config
