---
name: greptimedb-performance-tuning
description: Guide for tuning GreptimeDB server config and table options for better performance — cache sizing, write buffer, WAL, and ingestion throughput. Use when the user wants to speed up queries or writes, reduce object-store reads, fix write stalls/rejects, or right-size caches and the write buffer. Triggers on phrases like "tune performance", "性能调优", "increase cache", "调大缓存", "page cache / write cache", "write buffer", "写缓冲", "global_write_buffer_size", "disable WAL", "关闭 WAL", "improve write throughput", "提升写入吞吐", "batch writes". For schema/table changes (primary key, indexes, partitioning) use greptimedb-table-design; to first find the bottleneck use greptimedb-performance-diagnosis.
---

# GreptimeDB Performance Tuning

Apply **server config and table-option** changes to improve GreptimeDB performance. This
skill covers the live-tunable / deployment-level knobs. Schema-level decisions (primary key,
indexes, append-only, partitioning) live in `greptimedb-table-design`. If you don't yet know
*what* to tune, run `greptimedb-performance-diagnosis` first to find the bottleneck.

Read the source guide first when you need detail:
https://docs.greptime.com/user-guide/deployments-administration/performance-tuning/performance-tuning-tips/

## The workflow

### Phase 1. Identify the goal and version

Confirm what to optimize for (query latency, write throughput, or memory/disk footprint) and
ask for the **GreptimeDB version** — defaults and available options differ across versions.

To apply `ALTER` / table-option changes, run SQL via the `greptimedb-mcp-server` `execute_sql`
tool if available, a **MySQL**/**PostgreSQL** client, the built-in
[GreptimeDB Dashboard](https://docs.greptime.com/getting-started/installation/greptimedb-dashboard/),
or (Enterprise) the [Management Console](https://docs.greptime.com/enterprise/console-ui/).
Config-file (`toml`) changes require a restart. See defaults in
https://docs.greptime.com/user-guide/deployments-administration/configuration/.

### Phase 2. Cache sizing

Use `greptime_mito_cache_bytes{type="..."}` as the primary signal: if a cache sits near its
configured capacity, grow it; if it stays far below, shrink it and give the resource to a
cache under pressure. Use hit/miss/eviction as supporting signals.

```toml
[[region_engine]]
[region_engine.mito]
# Write cache (data files); `type` label is `file`.
write_cache_size = "10G"
# Percentage of write cache for index (puffin) files; `type` label `index`.
index_cache_percent = 20
# `type` label `sst_meta`.
sst_meta_cache_size = "128MB"
# `type` label `vector`.
vector_cache_size = "512MB"
# Pages of SST row groups; `type` label `page`.
page_cache_size = "512MB"
# Time series selector results (e.g. last_value()); `type` label `selector_result`.
selector_result_cache_size = "512MB"
# Flat range scan results; `type` label `range_result`.
range_result_cache_size = "512MB"
# Manifest files; `type` label `manifest`.
manifest_cache_size = "256MB"
```

Decision rules:

- **Check available memory and disk first, and leave headroom.** Size in-memory caches
  (`page`, `vector`, `*_result`, `sst_meta`, `manifest`) against free RAM and the node's
  memory limit so they don't trigger OOM; size the `write_cache_size` (disk) against free disk
  so it doesn't fill the volume. Grow incrementally and re-check resource usage rather than
  maxing caches out.
- Allocate **at least 1/10 of disk** to the write cache; prefer a large write cache with
  object storage.
- Allocate **at least 1/4 of memory** to `page_cache_size` if memory usage is under 20%.
- **Double** a cache if its hit ratio is below 50%.
- If `greptime_mito_cache_bytes{type="index"}` is full but `{type="file"}` is not, increase
  `index_cache_percent`.
- Only tune `index.staging_size` for index-search workloads where
  `greptime_mito_cache_bytes{type="index_staging"}` approaches capacity — not for every
  deployment.

### Phase 3. Ingestion throughput

- **Batching** — send multiple rows per request; ~1000 rows/batch is a good start, enlarge if
  latency and resources allow.
- **Write by time window** — out-of-order writes across time windows hurt performance. For
  backfilling a long time range, create the table in advance and set
  `compaction.twcs.time_window`.
- **Write buffer** — only after confirming (via diagnosis) that flush performance and write
  distribution are healthy, increase `region_engine.mito.global_write_buffer_size`
  (default: auto, ~1/8 OS memory, max 1GB). Increase gradually (2x–4x) and watch datanode
  memory. Leave `global_write_buffer_reject_size` unset to use the default 2x; set it manually
  (commonly 1.5x–2x, and it must exceed `global_write_buffer_size`) only if you want writes to
  fail earlier under memory pressure.

```toml
[[region_engine]]
[region_engine.mito]
global_write_buffer_size = "2GB"
# Optional. Leave unset unless you need a custom reject margin.
global_write_buffer_reject_size = "3GB"
```

If flush is slow or one region/datanode takes most writes, repartition instead — see
`greptimedb-table-design`.

### Phase 4. WAL and table options

- **Disable WAL** for replayable sources (e.g. Kafka) to boost write throughput. Unflushed
  data is not recoverable from GreptimeDB and must be replayed from the source.

  ```sql
  CREATE TABLE logs (
    message STRING,
    ts TIMESTAMP TIME INDEX
  ) WITH (skip_wal = 'true');
  ```

- **`append_mode`** and **`sst_format`** — append-only tables and the `flat` SST format
  improve scan performance. `flat` is the default; the only reason to set `sst_format='flat'`
  manually is upgrading from an old version whose default was the legacy `primary_key` format.
  These are schema-level concerns — see `greptimedb-table-design`.

## Escalation

If tuning doesn't help and the cause is unclear, collect context (relevant metrics including
`greptime_mito_cache_bytes`/hit/miss, `EXPLAIN ANALYZE VERBOSE` for query cases,
`SHOW CREATE TABLE`, version, logs) and open an issue or discussion at
https://github.com/GreptimeTeam/greptimedb. For self-monitoring users, use the
**`self-monitoring-export`** skill to export the incident data.

## Reference

1. Performance tuning tips:
   https://docs.greptime.com/user-guide/deployments-administration/performance-tuning/performance-tuning-tips/
2. Configuration (default cache and buffer sizes):
   https://docs.greptime.com/user-guide/deployments-administration/configuration/
3. CREATE TABLE (table options, `skip_wal`, `append_mode`, `sst_format`, compaction options):
   https://docs.greptime.com/reference/sql/create/
4. GreptimeDB Dashboard (run SQL from a web UI):
   https://docs.greptime.com/getting-started/installation/greptimedb-dashboard/
5. GreptimeDB Enterprise Management Console (SQL, metrics, logs):
   https://docs.greptime.com/enterprise/console-ui/
