---
name: altinity-expert-clickhouse-reporting
description: Diagnose ClickHouse SELECT query performance, analyze query patterns, identify slow queries, and find optimization opportunities. Use for query latency and timeout issues.
---

# Query Performance Analysis

Diagnose SELECT query performance issues, analyze query patterns, and identify optimization opportunities.

---

## Diagnostics

Run all queries from the file checks.sql and analyze the results.

---

## Query Optimization Hints

### Index Usage Check

```sql
-- Check if data skipping indices exist
select
    database,
    table,
    name as index_name,
    type,
    expr,
    granularity
from system.data_skipping_indices
where database = '{database}' and table = '{table}'
```

### Mark Count for Query

For a specific slow query, check how many marks (granules) were read:

```sql
select
    query_id,
    read_rows,
    selected_marks,
    selected_parts,
    formatReadableSize(read_bytes) as read_bytes,
    round(read_rows / nullIf(selected_marks, 0)) as rows_per_mark
from system.query_log
where query_id = '{query_id}'
  and type = 'QueryFinish'
```

**High `selected_marks`** relative to result = index not selective enough.

---

## Ad-Hoc Query Guidelines

### Required Safeguards
```sql
-- Always time-bound
where event_date >= today() - 1
-- or
where event_time > now() - interval 1 hour

-- Always limit
limit 100

-- Filter by type
where type = 'QueryFinish'  -- completed
where type like 'Exception%'  -- failed
```

### Useful Filters
```sql
-- By user
where user = 'analytics_user'

-- By query pattern
where query ilike '%SELECT%FROM my_table%'

-- By duration threshold
where query_duration_ms > 10000  -- > 10 seconds

-- By normalized hash (for specific query pattern)
where normalized_query_hash = 1234567890
```

---

## Cross-Module Triggers

| Finding | Load Module | Reason |
|---------|-------------|--------|
| High memory queries | `altinity-expert-clickhouse-memory` | Memory limits/optimization |
| Reading too many parts | `altinity-expert-clickhouse-merges` | Part consolidation |
| Poor index selectivity | `altinity-expert-clickhouse-schema` | Index/ORDER BY design |
| Cache misses | `altinity-expert-clickhouse-caches` | Cache sizing |
| MV slow | `altinity-expert-clickhouse-ingestion` | MV optimization |

---

## Settings Reference

| Setting | Scope | Notes |
|---------|-------|-------|
| `max_execution_time` | Query | Query timeout |
| `max_rows_to_read` | Query | Limit rows scanned |
| `max_bytes_to_read` | Query | Limit bytes scanned |
| `max_threads` | Query | Parallelism |
| `use_query_cache` | Query | Enable query result caching |
| `log_queries` | Server | Enable query logging |
| `log_queries_min_query_duration_ms` | Server | Log threshold |
