---
name: altinity-expert-clickhouse-logs
description: Analyze ClickHouse system log table health including TTL configuration, disk usage, freshness, and cleanup. Use for system log issues and TTL configuration.
---

## Diagnostics

Run all queries from the file checks.sql and analyze the results.

## TTL Recommendations

| Log Table | Recommended TTL | Notes |
|-----------|----------------|-------|
| query_log | 7-30 days | Balance debugging vs disk |
| query_thread_log | Disable or 3 days | Very verbose |
| part_log | 14-30 days | Important for RCA |
| trace_log | 3-7 days | Large, mostly for debugging |
| text_log | 7-14 days | Important for debugging |
| metric_log | 7-14 days | Useful for trending |
| asynchronous_metric_log | 7-14 days | Low volume |
| crash_log | 90+ days | Rare, keep longer |


## KB articles
- https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-system-tables-eat-my-disk/
