---
name: altinity-expert-clickhouse-kafka
description: Diagnose ClickHouse Kafka engine health, consumer status, thread pool capacity, and consumption issues. Use for Kafka lag, consumer errors, and thread starvation.
---

## Diagnostics

Run all queries from the file checks.sql and analyze the results.

---

## Interpreting Results

### Consumer Health

Check if consumers are stuck by comparing exception time vs activity times:

- `last_exception_time >= last_poll_time` OR `last_exception_time >= last_commit_time` → consumer stuck on error, not progressing
- Otherwise → consumer healthy

The `exceptions` column is a tuple of arrays with matching indices — `exceptions.time[-1]` and `exceptions.text[-1]` give the most recent error.

### Thread Pool Capacity

- `kafka_consumers > mb_pool_size` → thread starvation — consumers waiting for available threads
- Fix: increase `background_message_broker_schedule_pool_size` (default: 16)
- Sizing: total Kafka + RabbitMQ/NATS consumers + 25% buffer

### Slow Materialized Views (Poll Interval Risk)

- MV avg duration > 30s → consumer may exceed `max.poll.interval.ms` and get kicked from the group
- MV executions with error status → likely consumer rebalances (consumer kicked, MV interrupted mid-batch)
- **Most common root cause for slow MVs:** multiple `JSONExtract` calls re-parsing the same JSON blob
- **Fix:** rewrite to one-pass `JSONExtract(json, 'Tuple(...)') AS parsed` + `tupleElement()` — see [troubleshooting.md](troubleshooting.md)

### Pool Utilization Trends (12h)

- Sustained high values near pool size → capacity pressure
- Spikes correlating with lag → temporary overload
- Flat zero → Kafka consumers may not be active

---

## Advanced Diagnostics

For deeper investigation, run queries from advanced_checks.sql:

- **Consumer exception drill-down** — filter to a specific problematic Kafka table
- **Consumption speed measurement** — snapshot-based rate calculation
- **Topic lag via rdkafka_stat** — total lag per table and per-partition breakdown
- **Broker connection health** — connection state, errors, disconnects

**Important:** `rdkafka_stat` is **not enabled by default** in ClickHouse. It requires `<statistics_interval_ms>` in the Kafka engine settings. See advanced_checks.sql for setup instructions.

---

## Common Issues

For troubleshooting common errors and configuration guidance, see [troubleshooting.md](troubleshooting.md):

- Topic authorization / ACL errors
- Poll interval exceeded (slow MV / JSON parsing optimization)
- Thread pool starvation
- Parsing errors / dead letter queue
- Data loss with multiple materialized views
- Offset rewind / replay
- Parallel consumption tuning

---

## Cross-Module Triggers

| Finding | Load Module | Reason |
|---------|-------------|--------|
| Slow MV inserts | `altinity-expert-clickhouse-ingestion` | Insert pipeline analysis |
| High merge memory | `altinity-expert-clickhouse-merges` | Merge patterns |
| Query-level issues | `altinity-expert-clickhouse-reporting` | Query optimization |
| Schema concerns | `altinity-expert-clickhouse-schema` | Table design |

---

## Settings Reference

| Setting | Scope | Notes |
|---------|-------|-------|
| `background_message_broker_schedule_pool_size` | Server | Thread pool for Kafka/RabbitMQ/NATS consumers (default: 16) |
| `kafka_num_consumers` | Table | Parallel consumers per table (limited by cores) |
| `kafka_thread_per_consumer` | Table | Required for parallel inserts (`= 1`) |
| `kafka_handle_error_mode` | Table | `stream` (21.6+) or `dead_letter` (25.8+) |
| `max_poll_interval_ms` | librdkafka | Max time between polls before consumer is kicked (default: 300s) |
| `statistics_interval_ms` | librdkafka | Enable rdkafka_stat collection (disabled by default) |
