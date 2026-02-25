---
name: clickhouse-materialized-views
description: |
  Guides for implementing real-time data aggregation and transformation pipelines using ClickHouse materialized views. Use when building real-time dashboards, streaming analytics, metrics aggregation, event processing, or continuous data transformation. Covers incremental aggregation, State/Merge functions, chaining views, schema evolution, and troubleshooting streaming pipelines.
allowed-tools: Read, Bash, Glob, Grep
---

## Table of Contents

1. [Purpose](#purpose)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
   - [Aggregation Patterns](#aggregation-patterns)
   - [Destination Table Engines](#destination-table-engines)
   - [State/Merge Functions](#statemerge-functions)
   - [View Chaining](#view-chaining)
4. [Instructions](#instructions)
   - [Step 1: Choose Your Aggregation Pattern](#step-1-choose-your-aggregation-pattern)
   - [Step 2: Select the Right Destination Engine](#step-2-select-the-right-destination-engine)
   - [Step 3: Design Your Aggregation Query](#step-3-design-your-aggregation-query)
   - [Step 4: Implement State/Merge Functions](#step-4-implement-statemerge-functions-for-complex-aggregates)
   - [Step 5: Chain Views for Multi-Level Aggregation](#step-5-chain-views-for-multi-level-aggregation)
   - [Step 6: Handle Schema Evolution](#step-6-handle-schema-evolution-and-versioning)
   - [Step 7: Monitor Performance](#step-7-monitor-and-optimize-view-performance)
   - [Step 8: Backfill Historical Data](#step-8-backfill-historical-data)
5. [Examples & Patterns](#examples--patterns)
   - [Real-Time Dashboards](#real-time-dashboard-metrics)
   - [User Segmentation](#user-segmentation)
   - [Multi-Destination Routing](#multi-destination-routing)
   - [Complete Examples](#complete-examples)
6. [References](#references)
   - [Engine Comparison](#engine-comparison)
   - [State/Merge Functions Reference](#statemerge-functions-reference)
   - [Kafka Streaming Pipeline](#kafka-streaming-pipeline)
   - [Troubleshooting Guide](#troubleshooting-guide)
7. [Requirements](#requirements)

# ClickHouse Materialized Views Skill

## Purpose

Materialized views in ClickHouse are incremental triggers that automatically transform and aggregate incoming data in real-time. Unlike traditional databases, ClickHouse views process only new data as it arrives, enabling efficient streaming analytics, real-time dashboards, and continuous aggregation without scheduled batch jobs.

## When to Use This Skill

Use when asked to:
- Build real-time data aggregation pipelines ("create real-time metrics")
- Implement streaming analytics or continuous aggregation
- Create pre-aggregated tables for fast dashboard queries
- Set up automatic data transformation as events arrive
- Chain multi-level aggregations (hourly → daily → monthly)

Do NOT use when:
- Data is batch-processed infrequently (use scheduled jobs instead)
- Aggregation logic changes often (materialized views are harder to modify)
- Source data is small and queries are already fast

## Quick Start

**Create a simple real-time aggregation pipeline:**

```sql
-- Step 1: Create source table (raw events)
CREATE TABLE events (
    user_id UInt32,
    event_type String,
    timestamp DateTime,
    revenue Decimal(10, 2)
) ENGINE = MergeTree()
ORDER BY (user_id, timestamp);

-- Step 2: Create destination table (aggregated)
CREATE TABLE daily_revenue (
    date Date,
    total_revenue Decimal(18, 2),
    event_count UInt64
) ENGINE = SummingMergeTree()
ORDER BY date;

-- Step 3: Create materialized view (automatic aggregation)
CREATE MATERIALIZED VIEW daily_revenue_mv TO daily_revenue AS
SELECT
    toDate(timestamp) as date,
    SUM(revenue) as total_revenue,
    COUNT() as event_count
FROM events
GROUP BY date;

-- Now every INSERT into events automatically updates daily_revenue
INSERT INTO events VALUES (12345, 'purchase', '2024-01-15 10:30:00', 99.99);
SELECT * FROM daily_revenue;  -- Result: 2024-01-15 | 99.99 | 1
```

## Instructions

### Step 1: Choose Your Aggregation Pattern

Materialized views support three main patterns depending on your use case:

**Incremental Views (Most Common)**
- Process only new data as it arrives
- Best for streaming event data and continuous updates
- Use with `SummingMergeTree` for automatic deduplication

**Refreshable Views**
- Recalculate entire view on a schedule (e.g., hourly)
- Best for complex queries that need full recalculation
- Syntax: `CREATE MATERIALIZED VIEW ... REFRESH EVERY 1 HOUR AS ...`

**Populate-Based Views**
- Backfill existing data when view is created
- Warning: Can be expensive on large tables
- Syntax: `CREATE MATERIALIZED VIEW ... POPULATE AS ...`

See `examples/aggregation-patterns.md` for complete pattern examples.

### Step 2: Select the Right Destination Engine

The destination table engine determines how your aggregated data behaves:

**SummingMergeTree** (Simple Aggregates)
- Use when aggregating with COUNT, SUM, AVG
- Automatically sums columns during background merges
- No duplicate rows in final results
- Example: Hourly sales totals, daily revenue

**AggregatingMergeTree** (Complex Aggregates)
- Use with State/Merge functions for uniq, quantile, topK
- Stores intermediate aggregation states
- Combine with `uniqState()`, `quantileState()`, `topKState()` in views
- Query with `uniqMerge()`, `quantileMerge()`, `topKMerge()` functions
- Example: Unique user counts, percentile calculations

**ReplacingMergeTree** (Deduplication)
- Use when you need to replace/update existing rows
- Maintains version column to determine latest record
- Example: User profile updates, entity state snapshots

**MergeTree** (Raw Events)
- Use when storing raw events without aggregation
- No automatic deduplication
- Example: Event audit trail, raw clickstream data

See `references/engine-comparison.md` for detailed comparison.

### Step 3: Design Your Aggregation Query

Follow these principles:

**GROUP BY Cardinality**
- Keep cardinality moderate (not millions of unique combinations)
- Example: Good = `GROUP BY date, product_id` | Bad = `GROUP BY user_id, timestamp`

**ORDER BY for Query Patterns**
- Design ORDER BY for your most common query filters
- If queries filter by date first: `ORDER BY (date, product_id)`
- If queries filter by product first: `ORDER BY (product_id, date)`

**Include Necessary Columns**
- Include columns needed for post-aggregation filtering
- Store raw values alongside aggregates when needed for flexibility
- Example: Store `timestamp` and `revenue` along with hourly aggregates

**Use Conditional Aggregation**
- Use `countIf()`, `sumIf()`, `avgIf()` for event filtering
- Filter within the aggregation rather than in views
- Example: `countIf(event_type = 'purchase') as purchase_count`

See `examples/aggregation-patterns.md` for SQL patterns.

### Step 4: Implement State/Merge Functions for Complex Aggregates

When using `AggregatingMergeTree`, use special State/Merge function pairs:

**In Materialized View (State Functions)**
```sql
CREATE MATERIALIZED VIEW user_stats_mv TO user_stats AS
SELECT
    toDate(timestamp) as date,
    uniqState(user_id) as unique_users,
    quantileState(0.95)(response_time) as p95_latency
FROM events
GROUP BY date;
```

**In Queries (Merge Functions)**
```sql
SELECT
    date,
    uniqMerge(unique_users) as total_unique_users,
    quantileMerge(0.95)(p95_latency) as latency_p95
FROM user_stats
GROUP BY date;
```

Common function pairs:
- `uniq()` ↔ `uniqState()` / `uniqMerge()`
- `sum()` ↔ `sumState()` / `sumMerge()`
- `avg()` ↔ `avgState()` / `avgMerge()`
- `quantile(0.95)()` ↔ `quantileState(0.95)()` / `quantileMerge(0.95)()`
- `topK(10)()` ↔ `topKState(10)()` / `topKMerge(10)()`

See `references/state-merge-reference.md` for all function pairs.

### Step 5: Chain Views for Multi-Level Aggregation

Build hierarchical aggregations to reduce redundant computation:

```sql
-- Level 1: Raw events (source)
CREATE TABLE events (...) ENGINE = MergeTree() ORDER BY (user_id, timestamp);

-- Level 2: Hourly aggregation
CREATE TABLE hourly_stats (...) ENGINE = SummingMergeTree() ORDER BY (hour, product_id);
CREATE MATERIALIZED VIEW hourly_stats_mv TO hourly_stats AS
SELECT
    toStartOfHour(timestamp) as hour,
    product_id,
    COUNT() as event_count,
    SUM(revenue) as total_revenue
FROM events
GROUP BY hour, product_id;

-- Level 3: Daily aggregation (chain from hourly, not raw events)
CREATE TABLE daily_stats (...) ENGINE = SummingMergeTree() ORDER BY (date, product_id);
CREATE MATERIALIZED VIEW daily_stats_mv TO daily_stats AS
SELECT
    toDate(hour) as date,
    product_id,
    SUM(event_count) as event_count,
    SUM(total_revenue) as total_revenue
FROM hourly_stats
GROUP BY date, product_id;
```

Benefits:
- Reduces redundant computation (don't re-process raw events for daily stats)
- Each level optimized for different query patterns
- Easier to debug and modify intermediate aggregations

### Step 6: Handle Schema Evolution and Versioning

When modifying aggregation logic:

```sql
-- Create new versioned view with updated schema
CREATE MATERIALIZED VIEW hourly_stats_v2_mv TO hourly_stats_v2 AS
SELECT
    toStartOfHour(timestamp) as hour,
    product_id,
    COUNT() as sales_count,
    SUM(revenue) as total_revenue,
    COUNT(DISTINCT user_id) as unique_customers  -- New column
FROM orders
GROUP BY hour, product_id;

-- Migrate queries gradually to v2
-- Then drop old view:
DROP VIEW hourly_stats_v1_mv;
DROP TABLE hourly_stats_v1;
```

Avoid ALTER TABLE on materialized view destinations when possible (can cause data loss).

### Step 7: Monitor and Optimize View Performance

**Check View Execution Performance**
```sql
SELECT
    view_name,
    elapsed,
    read_rows,
    memory_usage
FROM system.query_log
WHERE query_kind = 'MaterializedView'
  AND elapsed > 1
ORDER BY elapsed DESC;
```

**Common Performance Issues and Solutions**
- **High memory usage**: Reduce GROUP BY cardinality or add WHERE filters
- **Slow execution**: Simplify aggregation logic or chain views instead of complex single view
- **Data lag**: Increase `kafka_max_block_size` if consuming from Kafka

See `references/troubleshooting.md` for debugging guide.

### Step 8: Backfill Historical Data

When adding new views to existing data:

**Option 1: Direct Insert (Safest)**
```sql
-- Backfill historical data directly to destination
INSERT INTO hourly_stats
SELECT
    toStartOfHour(timestamp) as hour,
    product_id,
    COUNT() as sales_count,
    SUM(revenue) as total_revenue
FROM orders
WHERE date < '2024-01-01'
GROUP BY hour, product_id;
```

**Option 2: Use POPULATE (for empty tables)**
```sql
-- Only use if destination table is empty
CREATE MATERIALIZED VIEW hourly_stats_mv TO hourly_stats
POPULATE AS
SELECT ... FROM orders;
```

⚠️ Avoid `POPULATE` on large source tables (can be very slow).

## Examples & Patterns

The following patterns are common use cases for materialized views:

### Real-Time Dashboard Metrics

Pre-aggregate metrics to enable instant dashboard queries:
```sql
CREATE MATERIALIZED VIEW dashboard_metrics_mv TO dashboard_metrics AS
SELECT
    toStartOfHour(timestamp) as hour,
    COUNT() as total_events,
    uniq(user_id) as unique_users,
    countIf(event_type = 'purchase') as purchases
FROM events
GROUP BY hour;
```

### User Segmentation

Automatically segment users based on behavior:
```sql
CREATE MATERIALIZED VIEW user_segments_mv TO user_segments AS
SELECT
    user_id,
    COUNT() as event_count,
    SUM(revenue) as lifetime_value,
    CASE
        WHEN lifetime_value > 1000 THEN 'vip'
        WHEN lifetime_value > 100 THEN 'regular'
        ELSE 'casual'
    END as segment
FROM events
GROUP BY user_id;
```

### Multi-Destination Routing

Route data to multiple aggregations:
```sql
-- High-value orders
CREATE MATERIALIZED VIEW high_value_orders_mv TO high_value_orders AS
SELECT * FROM orders WHERE total_amount > 1000;

-- All orders
CREATE MATERIALIZED VIEW all_orders_mv TO all_orders AS
SELECT * FROM orders;
```

### Complete Examples

For comprehensive, production-ready examples covering real-world scenarios, see the [examples/](./examples/) directory:
- Real-time dashboards and metrics aggregation
- User segmentation and cohort analysis
- Funnel analysis and conversion tracking
- Time-series downsampling and rollups
- Kafka streaming pipelines with end-to-end examples

## Requirements

- ClickHouse 20.6+: Basic materialized views
- ClickHouse 21.9+: Refreshable materialized views
- ClickHouse 22.0+: Advanced State/Merge functions
- Python client (for querying views): `pip install clickhouse-driver`
- Kafka/Redpanda: For streaming pipelines (optional)

## References

### Engine Comparison

[references/engine-comparison.md](./references/engine-comparison.md) - Detailed comparison of ClickHouse table engines for materialized views:
- **SummingMergeTree vs AggregatingMergeTree**: When to use each for aggregation
- **ReplacingMergeTree**: For deduplication and entity updates
- **Engine characteristics**: Memory usage, merge behavior, query performance
- **Decision matrix**: Choosing the right engine for your use case

### State/Merge Functions Reference

[references/state-merge-reference.md](./references/state-merge-reference.md) - Complete reference for all State/Merge function pairs:
- Function pair mapping (State ↔ Merge)
- Supported aggregation functions
- Parameter specifications and usage
- Performance considerations
- Examples for each function

### Kafka Streaming Pipeline

[examples/kafka-streaming-pipeline.md](./examples/kafka-streaming-pipeline.md) - Real-world Kafka integration patterns:
- Consuming from Kafka with Kafka table engine
- Chaining materialized views with Kafka sources
- Error handling and data validation
- Complete end-to-end pipeline example
- Monitoring Kafka consumption in ClickHouse

### Aggregation Patterns

[examples/aggregation-patterns.md](./examples/aggregation-patterns.md) - SQL pattern examples and common scenarios:
- Real-time dashboards and metrics
- User segmentation and cohort analysis
- Funnel analysis and conversion tracking
- Time-series downsampling and rollups
- Copy-paste ready SQL examples

### Complex Aggregates with State/Merge

[examples/state-merge-aggregates.md](./examples/state-merge-aggregates.md) - Advanced aggregation techniques:
- Using uniq, quantile, and topK in views
- Multi-stage aggregation with State/Merge
- Accuracy vs performance tradeoffs
- Real-world performance tuning examples
- Working with approximate functions

### Troubleshooting Guide

[references/troubleshooting.md](./references/troubleshooting.md) - Comprehensive debugging guide for common issues:
- Performance problems and optimization strategies
- Data correctness and consistency issues
- Schema evolution and migration challenges
- Monitoring and health checks
- Common error messages and solutions
