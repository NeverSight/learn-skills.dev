---
name: spice-acceleration
description: Accelerate data locally for sub-second query performance. Use when enabling data acceleration, choosing an engine (Arrow, DuckDB, SQLite, Cayenne), configuring refresh modes, setting up retention policies, creating snapshots, adding indexes, or materializing datasets.
---

# Accelerate Data

Data acceleration materializes working sets of data locally, reducing query latency from seconds to milliseconds. Hot data gets materialized for instant access while cold data remains federated.

Unlike traditional caches that store query results, Spice accelerates entire datasets with configurable refresh strategies and the flexible compute of an embedded database.

## Enable Acceleration

```yaml
datasets:
  - from: postgres:my_table
    name: my_table
    acceleration:
      enabled: true
      engine: duckdb # arrow, duckdb, sqlite, cayenne, postgres, turso
      mode: memory # memory or file
      refresh_check_interval: 1h
```

## Choosing an Engine

| Use Case                                 | Engine     | Why                                                     |
| ---------------------------------------- | ---------- | ------------------------------------------------------- |
| Small datasets (<1 GB), max speed        | `arrow`    | In-memory, lowest latency                               |
| Medium datasets (1-100 GB), complex SQL  | `duckdb`   | Mature SQL, memory management                           |
| Large datasets (100 GB-1+ TB), analytics | `cayenne`  | Built on Vortex (Linux Foundation), 10-20x faster scans |
| Point lookups on large datasets          | `cayenne`  | 100x faster random access vs Parquet                    |
| Simple queries, low resource usage       | `sqlite`   | Lightweight, minimal overhead                           |
| Async operations, concurrent workloads   | `turso`    | Native async, modern connection pooling                 |
| External database integration            | `postgres` | Leverage existing PostgreSQL infra                      |

### Cayenne vs DuckDB

Choose **Cayenne** when datasets exceed ~1 TB, multi-file ingestion is needed, or point lookups are common.
Choose **DuckDB** when datasets are under ~1 TB, complex SQL (window functions, CTEs) is needed, or DuckDB tooling is beneficial.

## Supported Engines

| Engine     | Mode           | Status            |
| ---------- | -------------- | ----------------- |
| `arrow`    | memory         | Stable            |
| `duckdb`   | memory, file   | Stable            |
| `sqlite`   | memory, file   | Release Candidate |
| `cayenne`  | file           | Beta              |
| `postgres` | N/A (attached) | Release Candidate |
| `turso`    | memory, file   | Beta              |

## Refresh Modes

| Mode              | Description                                                    | Use Case                                  |
| ----------------- | -------------------------------------------------------------- | ----------------------------------------- |
| `full`            | Complete dataset replacement on each refresh                   | Small, slowly-changing datasets           |
| `append` (batch)  | Adds new records based on a `time_column`                      | Append-only logs, time-series data        |
| `append` (stream) | Continuous streaming without time column                       | Real-time event streams (Kafka, Debezium) |
| `changes`         | CDC-based incremental updates via Debezium or DynamoDB Streams | Frequently updated transactional data     |
| `caching`         | Request-based row-level caching                                | API responses, HTTP endpoints             |

```yaml
# Full refresh every 8 hours
acceleration:
  refresh_mode: full
  refresh_check_interval: 8h

# Append mode: check for new records from the last day every 10 minutes
acceleration:
  refresh_mode: append
  time_column: created_at
  refresh_check_interval: 10m
  refresh_data_window: 1d

# Continuous ingestion using Kafka
acceleration:
  refresh_mode: append

# CDC with Debezium or DynamoDB Streams
acceleration:
  refresh_mode: changes
```

## Common Configurations

### In-Memory with Interval Refresh

```yaml
acceleration:
  enabled: true
  engine: arrow
  refresh_check_interval: 5m
```

### File-Based with Append and Time Window

```yaml
datasets:
  - from: postgres:events
    name: events
    time_column: created_at
    acceleration:
      enabled: true
      engine: duckdb
      mode: file
      refresh_mode: append
      refresh_check_interval: 1h
      refresh_data_window: 7d
```

## Retention Policies

Prevent unbounded growth of accelerated datasets. Spice supports time-based and custom SQL-based retention:

### Time-Based Retention

```yaml
acceleration:
  enabled: true
  engine: duckdb
  retention_check_enabled: true
  retention_period: 30d
  retention_check_interval: 1h
```

### SQL-Based Retention

```yaml
acceleration:
  retention_check_enabled: true
  retention_check_interval: 1h
  retention_sql: "DELETE FROM logs WHERE status = 'archived'"
```

## Constraints and Indexes

```yaml
acceleration:
  enabled: true
  engine: duckdb
  primary_key: order_id # Creates non-null unique index
  indexes:
    customer_id: enabled # Single column index
    '(created_at, status)': unique # Multi-column unique index
```

## Snapshots

Bootstrap file-based accelerations from S3 or filesystem snapshots on startup. Dramatically reduces cold-start latency in distributed deployments.

```yaml
snapshots:
  enabled: true
  location: s3://my_bucket/snapshots/
  bootstrap_on_failure_behavior: warn # warn | retry | fallback
  params:
    s3_auth: iam_role
```

Per-dataset opt-in:

```yaml
acceleration:
  enabled: true
  engine: duckdb
  mode: file
  snapshots:
    enabled: true
```

Snapshot triggers vary by refresh mode:

- `refresh_complete`: After each refresh (full and batch-append modes)
- `time_interval`: On a fixed schedule (all refresh modes)
- `stream_batches`: After every N batches (streaming modes: Kafka, Debezium, DynamoDB Streams)

## Engine-Specific Parameters

### DuckDB

```yaml
acceleration:
  engine: duckdb
  mode: file
  params:
    duckdb_file: ./data/cache.db
```

### SQLite

```yaml
acceleration:
  engine: sqlite
  mode: file
  params:
    sqlite_file: ./data/cache.sqlite
```

## Memory Considerations

When using `mode: memory` (default), the dataset is loaded into RAM. Ensure sufficient memory including overhead for queries and the runtime. Use `mode: file` for duckdb, sqlite, turso, or cayenne to avoid memory pressure.

## Documentation

- [Data Acceleration](https://spiceai.org/docs/features/data-acceleration)
- [Data Accelerators](https://spiceai.org/docs/components/data-accelerators)
- [Refresh Modes](https://spiceai.org/docs/features/data-acceleration/data-refresh)
- [Retention](https://spiceai.org/docs/features/data-acceleration/data-refresh#retention-policy)
- [Constraints](https://spiceai.org/docs/features/data-acceleration/constraints)
- [Indexes](https://spiceai.org/docs/features/data-acceleration/indexes)
- [Snapshots](https://spiceai.org/docs/components/data-accelerators/snapshots)
