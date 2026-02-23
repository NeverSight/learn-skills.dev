---
name: altinity-expert-clickhouse-ingestion
description: Diagnose ClickHouse INSERT performance, batch sizing, part creation patterns, and ingestion bottlenecks. Use for slow inserts and data pipeline issues.
---

## Diagnostics

Run all queries from the file checks.sql and analyze the results.

## Problem-Specific Investigation

### Insert with MV Overhead - Correlate by Query ID

When inserts feed materialized views, slow MVs cause insert delays. To correlate a slow insert with its MV breakdown:

```sql
-- Correlate slow insert with MV breakdown (requires query_id)
select
    view_name,
    view_duration_ms,
    read_rows,
    written_rows,
    status
from system.query_views_log
where query_id = '{query_id}'
order by view_duration_ms desc
```

### Kafka Consumer Exception Drill-Down (Targeted)

Use this only for problematic Kafka tables to avoid noisy output.

```sql
-- Filter to a specific Kafka table when lag is observed
select
    hostName() as host,
    database,
    table,
    consumer_id,
    is_currently_used,
    dateDiff('second', last_poll_time, now()) as last_poll_age_s,
    dateDiff('second', last_commit_time, now()) as last_commit_age_s,
    num_messages_read,
    num_commits,
    length(assignments.topic) as assigned_partitions,
    length(exceptions.text) as exception_count,
    exceptions.text[-1] as last_exception
from clusterAllReplicas('{cluster}', system.kafka_consumers)
where database = '{db}'
  and table = '{kafka_table}'
order by is_currently_used desc, last_poll_age_s desc
limit 50
```

## Ad-Hoc Query Guidelines

### Required Safeguards

```sql
-- Always limit results
limit 100

-- Always time-bound
where event_date = today()
-- or
where event_time > now() - interval 1 hour

-- For query_log, filter by type
where type = 'QueryFinish'  -- completed
-- or
where type like 'Exception%'  -- failed
```

### Useful Filters

```sql
-- Filter by table
where has(tables, 'database.table_name')

-- Filter by user
where user = 'producer_app'

-- Filter by insert size
where written_rows > 1000000  -- large inserts
where written_rows < 100      -- micro-batches
```
