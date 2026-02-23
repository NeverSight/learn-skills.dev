---
name: postgres-tuning
description: 'PostgreSQL 17/18+ performance tuning and optimization. Covers async I/O configuration, query plan forensics, index strategies, autovacuum tuning, vector search optimization, connection pooling, declarative partitioning, and practical query patterns. Use when diagnosing slow queries, configuring async I/O, tuning autovacuum, optimizing vector indexes, analyzing execution plans with EXPLAIN BUFFERS, configuring PgBouncer or connection pooling, setting up table partitioning, implementing cursor pagination, or optimizing queue processing.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# PostgreSQL Tuning

## Overview

Optimizes PostgreSQL 17/18+ performance across I/O, query execution, indexing, and maintenance. Covers the native AIO subsystem introduced in PostgreSQL 18 for throughput gains on modern storage, forensic query plan analysis with EXPLAIN BUFFERS (auto-included in PG18), B-tree skip scans for composite indexes, native UUIDv7 generation, and autovacuum tuning for high-churn tables.

**When to use:** Diagnosing slow queries, configuring async I/O, tuning shared_buffers and work_mem, optimizing indexes for write-heavy workloads, managing table bloat, pgvector HNSW tuning.

**When NOT to use:** Schema design (use a data modeling tool), application-level caching strategy, database selection decisions, ORM query generation.

**Key monitoring views:**

- `pg_stat_statements` — identifies slow query patterns by cumulative execution time
- `pg_stat_io` — granular I/O analysis by backend type, object, and context (PG16+)
- `pg_stat_checkpointer` — checkpoint frequency and timing (PG17+; previously in `pg_stat_bgwriter`)
- `pg_stat_user_tables` — dead tuple counts for bloat detection and autovacuum monitoring
- `pg_statio_user_tables` — buffer cache hit ratios per table
- `pg_aios` — in-progress AIO operations (PG18+)

## Quick Reference

| Pattern               | Configuration / Query                   | Key Points                                                                                         |
| --------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Async I/O             | `io_method = worker` or `io_uring`      | PG18 default is `worker`; `io_uring` Linux-only (kernel 5.1+, requires liburing build flag)        |
| I/O concurrency       | `io_max_concurrency` and `io_workers`   | `io_workers` defaults to 3; `io_max_concurrency` defaults to -1 (auto-calculated)                  |
| Forensic EXPLAIN      | `EXPLAIN (ANALYZE, BUFFERS, SETTINGS)`  | PG18 auto-includes BUFFERS with ANALYZE; target Shared Hit > 95%                                   |
| UUIDv7 primary keys   | `DEFAULT uuidv7()`                      | PG18 built-in; time-ordered, monotonic within a session; RFC 9562 compliant                        |
| B-tree skip scan      | Composite index on `(a, b)`             | PG18 skips leading column; works best with low-cardinality prefix and equality on trailing columns |
| Aggressive autovacuum | `autovacuum_vacuum_scale_factor = 0.01` | Triggers at 1% row change instead of default 20%                                                   |
| Shared buffers        | Start at 25% of RAM                     | Do not exceed 40% without benchmarking                                                             |
| work_mem tuning       | `SET work_mem = '64MB'` per session     | Prevents sort spills to disk; allocated per operator, not per query                                |
| BRIN index            | `CREATE INDEX USING brin(...)`          | 100x smaller than B-tree for physically ordered time-series data                                   |
| HNSW vector index     | `USING hnsw (col vector_cosine_ops)`    | Tune `m` (default 16) and `ef_construction` (default 64) for recall vs speed                       |
| GIN index             | `CREATE INDEX USING gin(...)`           | JSONB containment, full-text search, array operators; slower writes                                |
| Checkpoint tuning     | `checkpoint_timeout = 30min`            | Spread writes over 90% of timeout window to avoid I/O storms                                       |
| WAL compression       | `wal_compression = zstd`                | Available since PG15; reduces WAL I/O 50-70% for write-heavy workloads                             |
| Bloat detection       | `pg_stat_user_tables.n_dead_tup`        | Reindex concurrently if bloat > 30%                                                                |
| I/O monitoring        | `SELECT * FROM pg_stat_io`              | Watch `evictions` (cache too small) and `extends` (fast growth)                                    |
| Checkpoint monitoring | `pg_stat_checkpointer`                  | PG17+ moved checkpoint stats out of `pg_stat_bgwriter`                                             |

## Key Version Changes

**PostgreSQL 18:**

- Native async I/O via `io_method` parameter (reads only; writes remain synchronous)
- Built-in `uuidv7()` function with monotonic ordering within a session (RFC 9562)
- `uuidv4()` alias for `gen_random_uuid()` and `uuid_extract_timestamp()` for UUIDv7
- B-tree skip scan for composite indexes (equality on trailing columns, low-cardinality prefix)
- EXPLAIN ANALYZE auto-includes buffer statistics without specifying BUFFERS
- `pg_stat_io` gains byte-level columns (`read_bytes`, `write_bytes`, `extend_bytes`); `op_bytes` removed
- `effective_io_concurrency` default changed from 1 to 16
- AIO monitoring via `pg_aios` system view for in-progress I/O operations

**PostgreSQL 17:**

- Checkpoint statistics moved from `pg_stat_bgwriter` to `pg_stat_checkpointer`
- Column renames: `checkpoints_timed` to `num_timed`, `checkpoints_req` to `num_requested`
- `buffers_backend` and `buffers_backend_fsync` removed from `pg_stat_bgwriter` (now in `pg_stat_io`)

**PostgreSQL 15:**

- `wal_compression` expanded from boolean to support `pglz`, `lz4`, and `zstd` algorithms

## Common Mistakes

| Mistake                                                            | Correct Pattern                                                                                          |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Using `uuid_generate_v7()` or `gen_random_uuid()` for ordered keys | PG18 provides built-in `uuidv7()` for time-ordered UUIDs; pre-PG18 use `pg_uuidv7` extension             |
| Using `max_async_ios` as a configuration parameter                 | The correct PG18 parameter is `io_max_concurrency` (max concurrent I/O ops per process)                  |
| Querying `pg_stat_bgwriter` for checkpoint statistics on PG17+     | Checkpoint stats moved to `pg_stat_checkpointer` in PG17; columns renamed (`num_timed`, `num_requested`) |
| Using SELECT \* in high-frequency queries                          | Select only needed columns to reduce I/O and improve cache hit ratios                                    |
| Ignoring sequential scans on tables over 10k rows                  | Add targeted indexes on columns used in WHERE, ORDER BY, and JOIN clauses                                |
| Setting shared_buffers above 40% of RAM without testing            | Start at 25% and benchmark; excessive allocation causes OS page cache contention                         |
| Leaving autovacuum at default settings for high-churn tables       | Tune `autovacuum_vacuum_scale_factor` to 0.01 for tables with frequent UPDATE/DELETE                     |
| Over-indexing columns rarely used in queries                       | Every extra index slows UPDATE/INSERT and prevents HOT (Heap Only Tuple) updates                         |
| Expecting B-tree skip scan to work with range predicates           | PG18 skip scan only works with equality operators on trailing columns                                    |
| Ignoring "External Merge Disk" in query plans                      | Increase work_mem for specific sessions; it indicates sort spills to disk                                |
| Setting `io_method = io_uring` without verifying build flags       | PostgreSQL must be built with `--with-liburing` and requires Linux kernel 5.1+                           |
| Assuming PG18 AIO accelerates writes                               | AIO in PG18 only covers reads (seq scans, bitmap heap scans, VACUUM); writes remain synchronous          |

## Tuning Workflow

1. **Identify** slow queries from `pg_stat_statements` (sort by `total_exec_time`)
2. **Analyze** execution plans with `EXPLAIN (ANALYZE, BUFFERS, SETTINGS)`
3. **Check** buffer hit ratios via `pg_statio_user_tables` (target > 99%)
4. **Monitor** I/O patterns via `pg_stat_io` (watch evictions and disk reads)
5. **Optimize** with targeted indexes, work_mem adjustments, or query rewrites
6. **Verify** improvements by re-running EXPLAIN and comparing costs
7. **Maintain** with aggressive autovacuum settings for high-churn tables

## Delegation

- **Discover slow queries and I/O bottlenecks**: Use `Explore` agent to analyze pg_stat_statements, pg_stat_io, and slow query logs
- **Execute query plan analysis and index optimization**: Use `Task` agent to run EXPLAIN ANALYZE, create indexes, and verify performance improvements
- **Design database scaling and partitioning strategy**: Use `Plan` agent to architect sharding, partitioning, and replication topology

## References

- [Async I/O configuration and storage tuning](references/aio-tuning.md)
- [Query plan analysis and operator forensics](references/query-plan-analysis.md)
- [Indexing strategies and bloat management](references/indexing-and-bloat.md)
- [Connection pooling, partitioning, and query patterns](references/pooling-and-patterns.md)
