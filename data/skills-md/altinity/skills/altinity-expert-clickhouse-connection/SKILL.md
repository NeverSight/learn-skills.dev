---
name: altinity-expert-clickhouse-connection
description: Should be used when doing clickhouse analysis and diagnostics review before any altinity-expert-clickhouse skill to test clickhouse connection and set general rules
---

## Connection mode

Decide connection mode first and verify connectivity then:
```sql
select
    hostName() as hostname,
    version() as version,
    getMacro('cluster') as cluster_name,
    formatReadableTimeDelta(uptime()) as uptime_human,
    getSetting('max_memory_usage') as max_memory_usage,
    (select value from system.asynchronous_metrics where metric = 'OSMemoryTotal') as os_memory_total
```

### MCP mode 

Try to use MCP server with clickhouse in the name.
If multiple ClickHouse MCP servers are available, ask the user which one to use.
When executing queries by the MCP server, push a single SQL statement to the MCP server (no multy query!)

### Exec mode (clickhouse-client)

- if MCP is unavailable, try to run `clickhouse-client`. Don't rely on env vars. On failure, ask how to run it properly.
- Prefer running queries from a `.sql` file with `--queries-file` and forcing JSON output (`-f JSON`) when capturing results to files.

## Cluster selection for `clusterAllReplicas('{cluster}', ...)`

- Verify from the query results above if a cluster_name (cluster macro var) is not empty. If defined - leave macro as-is.
- if not, ask the user to choose from: `SELECT DISTINCT cluster FROM system.clusters where not is_local` and replace `'{cluster}'` placeholders in the queries in all `.sql` files.
- if the query above returns nothing, consider single-server mode and automatically rewrite `clusterAllReplicas('{cluster}', system.<table>)` → `system.<table>` before execution.

## Timeframe default for logs/errors

- If the user explicitly provides a timeframe in the initial prompt, use it exactly.
- Otherwise always default to **last 24 hours**:

```sql
-- Use this pattern for system.*_log tables and system.errors time filters:
-- WHERE event_time >= now() - INTERVAL 24 HOUR
```
- never expend time window without an explicit user prompt. If needed, ask user to extend time window

## Schema-safe rule 

- If a query fails with `UNKNOWN_IDENTIFIER`, run `DESCRIBE TABLE system.<table>` and drop/adjust only the missing columns.
- If a query fails with `UNKNOWN_TABLE`, skip that query and note the table is disabled or unavailable (e.g., `system.part_log`, `system.detached_parts`).

## Report Output 

In all reports, always provide a header with information:
- Connection mode used: MCP or clickhouse-client
- cluster name (or “no cluster / single node”)
- clickhouse version
- time window used for analysis

