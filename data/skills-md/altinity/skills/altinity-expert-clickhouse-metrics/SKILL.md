---
name: altinity-expert-clickhouse-metrics
description: Real-time monitoring of ClickHouse metrics, events, and asynchronous metrics. Use for load average, connections, queue monitoring, and resource saturation.
---

# Real-Time Metrics Monitoring

Real-time monitoring of ClickHouse metrics, events, and asynchronous metrics.

---

## Diagnostics

Run all queries from the file checks.sql and analyze the results.

---

## Ad-Hoc Query Guidelines

### Key Tables
- `system.metrics` - Current gauge values
- `system.events` - Cumulative counters since restart
- `system.asynchronous_metrics` - System-level metrics
- `system.metric_log` - Historical metrics
- `system.asynchronous_metric_log` - Historical async metrics

### Useful Patterns

```sql
-- Find metrics by pattern
select * from system.metrics where metric like '%pattern%'
select * from system.asynchronous_metrics where metric like '%pattern%'
select * from system.events where event like '%pattern%'
```

---

## Cross-Module Triggers

| Finding | Load Module | Reason |
|---------|-------------|--------|
| High memory metrics | `altinity-expert-clickhouse-memory` | Memory analysis |
| High replica delay | `altinity-expert-clickhouse-replication` | Replication issues |
| High parts count | `altinity-expert-clickhouse-merges` | Merge backlog |
| High load average | `altinity-expert-clickhouse-reporting` | Query analysis |
| High connections | `altinity-expert-clickhouse-reporting` | Connection analysis |

---

## Monitoring Recommendations

### Key Metrics to Alert On

| Metric | Warning | Critical |
|--------|---------|----------|
| `ReadonlyReplica` | - | > 0 |
| `Query` | > 75% max | > 90% max |
| `MemoryResident` | > 80% RAM | > 90% RAM |
| `MaxPartCountForPartition` | > parts_to_delay | > parts_to_throw |
| `ReplicasMaxAbsoluteDelay` | > 5 min | > 1 hour |
| `LoadAverage1` | > CPU count | > 2x CPU count |

### Prometheus/Grafana Export

ClickHouse exposes metrics at `:9363/metrics` in Prometheus format when enabled.