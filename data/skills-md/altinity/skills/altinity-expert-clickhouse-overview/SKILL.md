---
name: altinity-expert-clickhouse-overview
description: Runs a quick overview of Clickhouse server health.
---

## Analyze

## Predefined SQL

Run reporting SQL queries from files in Skill directory:
- checks.sql 
- metrics.sql
- ddl_queue.sql

Inline SQL below (version/enablement sensitive):

### Detached Parts 

version-dependent: ClickHouse 23.8 does not have modification_time 

```sql
SELECT
  hostName() AS host,
  database,
  table,
  reason,
  count() AS detached_parts,
  formatReadableSize(sum(bytes_on_disk)) AS bytes,
  min(modification_time) AS first_detach,
  max(modification_time) AS last_detach
FROM system.detached_parts
GROUP BY host, database, table, reason
ORDER BY detached_parts DESC
LIMIT 100
```

### Text Log 
(may be disabled)

```sql
select event_date, level, thread_name, any(logger_name) as logger_name,
       message_format_string, count(*) as count
from   system.text_log
where  event_date > now() - interval 24 hour
  and level <= 'Warning'
group by all
order by level, thread_name, message_format_string
```

### Check Pools

```sql
WITH
    ['MergesAndMutations', 'Fetches', 'Move', 'Common', 'Schedule', 'BufferFlushSchedule', 'MessageBrokerSchedule', 'DistributedSchedule'] AS pool_tokens,
    ['pool', 'fetches_pool', 'move_pool', 'common_pool', 'schedule_pool', 'buffer_flush_schedule_pool', 'message_broker_schedule_pool', 'distributed_schedule_pool'] AS setting_tokens
SELECT
    extract(m.metric, '^Background(.*)Task') AS pool_name,
    m.active_tasks,
    pool_size,
    round(100.0 * m.active_tasks / pool_size, 1) AS utilization_pct,
    multiIf(utilization_pct > 99, 'Major', utilization_pct > 90, 'Moderate', 'OK') AS severity
FROM
(
    SELECT
        metric,
        value AS active_tasks,
        transform(extract(metric, '^Background(.*)PoolTask'), pool_tokens, setting_tokens, '') AS pool_key,
        concat('background_', lower(pool_key), '_size') AS setting_name
    FROM system.metrics
    WHERE metric LIKE 'Background%PoolTask'
) AS m
LEFT JOIN
(
    SELECT
        name,
        toFloat64OrZero(value) AS pool_size
    FROM system.server_settings
    WHERE name LIKE 'background%pool_size'
) AS s ON s.name = m.setting_name
WHERE pool_size > 0
ORDER BY utilization_pct DESC
```

On error and for clickhouse version <= 22.8 replace system.server_settings to system.settings 

## Report

Prepare a summary report based on the findings


## Routing Rules (Chain to Other Skills)

Based on findings, load specific modules:

- Replication lag/readonly replicas/Keeper issues → `altinity-expert-clickhouse-replication`
- High memory usage or OOMs → `altinity-expert-clickhouse-memory`
- Disk usage > 80% or poor compression → `altinity-expert-clickhouse-storage`
- Many parts, merge backlog, or TOO_MANY_PARTS → `altinity-expert-clickhouse-merges`
- Slow SELECTs / heavy reads in query_log → `altinity-expert-clickhouse-reporting`
- Slow INSERTs / high part creation rate → `altinity-expert-clickhouse-ingestion`
- Low cache hit ratios / cache pressure → `altinity-expert-clickhouse-caches`
- Dictionary load failures or high dictionary memory → `altinity-expert-clickhouse-dictionaries`
- Frequent exceptions or error spikes → include `system.errors` and `system.*_log` summaries below
- System log TTL issues or log growth → `altinity-expert-clickhouse-logs`
- Schema anti‑patterns (partitioning/ORDER BY/MV issues) → `altinity-expert-clickhouse-schema`
- High load/connection saturation/queue buildup → `altinity-expert-clickhouse-metrics`
- Suspicious server log entries → `altinity-expert-clickhouse-logs`
