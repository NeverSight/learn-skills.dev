---
name: greptimedb-performance-diagnosis
description: Guide for diagnosing GreptimeDB performance problems — find the bottleneck behind a slow query, lagging or stalled ingestion, or high CPU/memory, then hand off to the right fix. Use when the user reports something is slow or resource-hungry and wants to know why. Triggers on phrases like "query is slow", "查询慢", "ingestion is slow", "写入慢", "write stall", "写入卡顿/被拒绝", "high CPU", "CPU 高", "high memory", "内存高/OOM", "EXPLAIN ANALYZE", "why is GreptimeDB slow", "性能排查/诊断". This skill diagnoses; apply fixes with greptimedb-performance-tuning and greptimedb-table-design.
---

# GreptimeDB Performance Diagnosis

Help the user find the **bottleneck** behind a GreptimeDB performance problem, then point
them at the right fix. This skill is the triage hub: it observes and concludes, it does not
apply tuning itself. Once the cause is clear, hand off to:

- `greptimedb-performance-tuning` — server config and table-option changes (caches, write
  buffer, WAL, batching).
- `greptimedb-table-design` — schema changes (primary key, indexes, append-only,
  partitioning).

Before going deep, ask for the **GreptimeDB version** and deployment mode (standalone or
cluster). Older versions may not expose some of the metrics below, and older Grafana
dashboards may lack some panels — you can supplement them from the
[grafana dashboards directory](https://github.com/GreptimeTeam/greptimedb/tree/main/grafana/dashboards),
where each panel's PromQL is the canonical source for the metric names used below.

**Running SQL and viewing metrics/logs.** To run the SQL in this guide (`EXPLAIN ANALYZE`,
`SELECT`, `SHOW CREATE TABLE`), use any of: the `greptimedb-mcp-server` `execute_sql` tool if
available; a **MySQL** or **PostgreSQL** client; or the built-in
[GreptimeDB Dashboard](https://docs.greptime.com/getting-started/installation/greptimedb-dashboard/).
**GreptimeDB Enterprise** users can use the
[Management Console](https://docs.greptime.com/enterprise/console-ui/), which also surfaces
metrics and logs.

## The workflow

### Phase 1. Make signals observable (only as needed)

Metrics dashboards are **not** a prerequisite. Many diagnoses need nothing but SQL:

- A **slow query** can be investigated immediately with `EXPLAIN ANALYZE VERBOSE` (Phase 3).
- Write distribution can be checked with `REGION_STATISTICS` (Phase 4).

Recommend setting up observability only when the symptom needs time-series metrics (write
pressure trends, cache hit ratios, CPU/memory over time):

1. Self-monitoring setup:
   https://docs.greptime.com/user-guide/deployments-administration/monitoring/cluster-monitoring-deployment/
2. Import the Grafana dashboards (standalone or cluster):
   https://github.com/GreptimeTeam/greptimedb/tree/main/grafana/dashboards

If the dashboard version is old and missing a panel, give the user the raw PromQL from the
phases below so they can add it.

### Phase 2. Classify the symptom

Route to the matching phase based on what the user reports:

| Symptom | Go to |
|---|---|
| A specific query is slow | Phase 3 |
| Ingestion is slow / latency high / writes stall or get rejected | Phase 4 |
| A node has high CPU or memory (cause unclear) | Phase 5 |
| Cache seems ineffective / lots of object-store reads | Phase 6 |

If the user is unsure, start from the broadest available signal (ingestion rate, request
latency, CPU/memory) and narrow down.

### Phase 3. Diagnose a slow query

Run the query with `EXPLAIN ANALYZE VERBOSE` (see access methods above):

```sql
EXPLAIN ANALYZE VERBOSE <SQL>;
```

`EXPLAIN ANALYZE` executes the query and reports per-stage runtime metrics; `VERBOSE` adds
scan-level metrics. When comparing repeated runs, remember the second run may be served from
cache — shift the time range slightly to keep the shape equivalent but avoid a fully cached
repeat.

Map common findings to causes and the fix skill:

| Finding in output | Likely cause | Fix |
|---|---|---|
| High `num_file_ranges`, many files < 1 row group | Many small SST files (backfill across windows, compaction pressure) | Tuning: `compaction.twcs.time_window`; Table-design: write/backfill by time window |
| High `scan_cost` **and** high `rows_precise_filtered` | Reads many rows then filters them out — missing a selective index | Table-design: add an index on the selective column |
| High `fetch_metrics.cache_miss` / `pages_to_fetch_store` / `store_fetch_elapsed` | Reading pages from object store instead of cache | Tuning: increase `write_cache_size` / `page_cache_size` |
| High `build_parts_cost` / `build_reader_cost` | Time spent building scan ranges/readers | Correlate with `num_file_ranges`, metadata cache misses |
| High `metadata_cache_metrics.metadata_load_cost` / `cache_miss` | SST metadata cache too small | Tuning: increase `sst_meta_cache_size` (check `greptime_mito_cache_bytes{type="sst_meta"}`) |

If the cause is still unclear, capture the **full** `EXPLAIN ANALYZE VERBOSE` output plus
`SHOW CREATE TABLE` and escalate (see [Escalation](#escalation)).

### Phase 4. Diagnose ingestion & write pressure

First check whether the write buffer is under pressure:

- `greptime_mito_write_buffer_bytes`
- `greptime_mito_write_stall_total`
- `greptime_mito_write_stalling_count`
- `greptime_mito_write_reject_total`

Stalls mean GreptimeDB is applying backpressure (global write buffer near
`global_write_buffer_size`, or a region temporarily not writable). A client error like
`Engine write buffer is full, rejecting write requests` means the reject threshold
(`global_write_buffer_reject_size`) was reached.

**Don't jump to raising the write buffer.** First find out *why* the buffer fills:

1. **Flush performance** — `greptime_mito_flush_elapsed`, plus
   `greptime_mito_flush_requests_total`, `greptime_mito_flush_bytes_total`,
   `greptime_mito_flush_file_total`. Datanode logs also help: search for
   `Successfully flush memtables` and divide `total_rows`/`total_bytes` by `cost` to estimate
   throughput. Slow flushes (e.g. ≥30s) or flush throughput below ingestion → the fix is
   partitioning/region distribution, not a bigger buffer.
2. **Write distribution** — `greptime_mito_write_rows_total` per datanode and
   `greptime_mito_handle_request_elapsed_bucket`; query
   [`REGION_STATISTICS`](https://docs.greptime.com/reference/sql/information-schema/region-statistics/)
   for `written_bytes_since_open` and `memtable_size`. If one region/datanode takes most of
   the load → repartition (Table-design).

Conclusion → fix:

- Flush slow or unbalanced load → **Table-design** (partitioning / region distribution).
- Flush fast but frequent under steady load → **Tuning** (increase `global_write_buffer_size`).

Also compare frontend protocol latency (`greptime_servers_http_requests_elapsed_bucket`,
`greptime_servers_grpc_requests_elapsed_bucket`, filter by `path`/`method`/`code`) against
datanode-side `greptime_mito_handle_request_elapsed_bucket` and
`greptime_mito_write_stage_elapsed_bucket` to locate whether the bottleneck is before or
inside the storage engine.

### Phase 5. Diagnose high CPU / memory

When a node has high CPU or memory and the cause is unclear, collect a profile from that
node and provide it to developers. Profiling is node-local — use the HTTP address of the
affected node (replace `127.0.0.1:4000`).

CPU flamegraph (collect while CPU is high):

```bash
curl -X POST -s 'http://127.0.0.1:4000/debug/prof/cpu?seconds=10&output=flamegraph' > greptime-cpu.svg
```

Memory flamegraph (collect while memory is high or growing):

```bash
curl -X POST -s 'http://127.0.0.1:4000/debug/prof/mem?output=flamegraph' > greptime-mem.svg
```

Notes:

- Memory profiling is Linux-only (not macOS/Windows) and requires heap profiling enabled.
  Official Docker images enable it by default; for self-built deployments start with
  `MALLOC_CONF=prof:true ./greptime ...`.
- Generating a flamegraph uses extra memory (parsing + symbolization in process) — be careful
  on a node near its memory limit.
- To find growing allocations, collect two `output=proto` profiles at different times and
  compare them.

See https://docs.greptime.com/reference/http-endpoints/#profiling-tools for the reference.
Attach the flamegraph/profile when escalating.

### Phase 6. Diagnose cache pressure

Use `greptime_mito_cache_bytes{type="..."}` as the primary signal: if a cache sits near its
configured capacity, it is under pressure. Supporting signals are `greptime_mito_cache_hit`,
`greptime_mito_cache_miss`, and `greptime_mito_cache_eviction` (all labeled by `type`). Cache
types include `file`, `index`, `sst_meta`, `page`, `vector`, `selector_result`,
`range_result`, `manifest`, and index-related caches.

A low hit ratio with high miss/eviction on a near-full cache → hand off to **Tuning** to
resize that specific cache.

## Escalation

When you cannot reach a confident conclusion, recommend the user collect context and open an
issue or discussion at https://github.com/GreptimeTeam/greptimedb. Gather, as relevant:

- Full `EXPLAIN ANALYZE VERBOSE` output (for query issues).
- Table schema (`SHOW CREATE TABLE`).
- GreptimeDB version and deployment mode.
- Relevant metrics (PromQL results or dashboard screenshots) and logs.
- CPU/memory flamegraphs for resource issues, plus the approximate time range and workload.

If the user runs GreptimeDB self-monitoring, use the **`self-monitoring-export`** skill to
export the logs/metrics for the incident window.

## Reference

1. Performance tuning tips (metrics tables, EXPLAIN findings):
   https://docs.greptime.com/user-guide/deployments-administration/performance-tuning/performance-tuning-tips/
2. EXPLAIN reference:
   https://docs.greptime.com/reference/sql/explain/
3. Self-monitoring deployment:
   https://docs.greptime.com/user-guide/deployments-administration/monitoring/cluster-monitoring-deployment/
4. Grafana dashboards (canonical source for metric names / PromQL):
   https://github.com/GreptimeTeam/greptimedb/tree/main/grafana/dashboards
5. HTTP profiling endpoints:
   https://docs.greptime.com/reference/http-endpoints/#profiling-tools
6. REGION_STATISTICS:
   https://docs.greptime.com/reference/sql/information-schema/region-statistics/
7. GreptimeDB Dashboard (run SQL from a web UI):
   https://docs.greptime.com/getting-started/installation/greptimedb-dashboard/
8. GreptimeDB Enterprise Management Console (SQL, metrics, logs):
   https://docs.greptime.com/enterprise/console-ui/
