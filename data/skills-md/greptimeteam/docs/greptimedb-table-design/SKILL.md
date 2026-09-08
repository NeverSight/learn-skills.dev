---
name: greptimedb-table-design
description: Guide for designing a GreptimeDB table schema for performance, and for improving an existing table. Covers primary key, append-only vs deduplication + merge mode, indexes (inverted/skipping/fulltext), wide vs multiple tables, and partitioning. Use when the user asks how to model a table, choose a primary key, pick an index, partition for scale, or improve a schema that already exists. Triggers on phrases like "design table", "表设计", "schema design", "建表", "primary key", "主键", "which index", "选索引", "partition table", "分区/分表", "append-only", "merge mode", "improve my schema". For server config tuning use greptimedb-performance-tuning; to find a bottleneck first use greptimedb-performance-diagnosis.
---

# GreptimeDB Table Design

Help the user design a table schema for performance, or improve an existing one. The schema
is the most impactful performance decision in GreptimeDB. This skill has two entry points —
**a new table** (every lever is open) and **an existing table** (most key decisions are baked
in at creation; only some things can be altered).

For server-level config (caches, write buffer, WAL) see `greptimedb-performance-tuning`. To
diagnose why a query/write is slow before redesigning, see `greptimedb-performance-diagnosis`.

Ask up front: **is this a new table or an existing one?** and the **GreptimeDB version**.

To run the SQL in this guide (`CREATE TABLE`, `ALTER TABLE`, `SHOW CREATE TABLE`,
`INSERT ... SELECT`), use any of: the `greptimedb-mcp-server` `execute_sql` tool if available;
a **MySQL** or **PostgreSQL** client; the built-in
[GreptimeDB Dashboard](https://docs.greptime.com/getting-started/installation/greptimedb-dashboard/);
or (Enterprise) the [Management Console](https://docs.greptime.com/enterprise/console-ui/).

## The workflow

### Phase 1. Understand how GreptimeDB stores and reads data

Read the design guide; the rest of this skill builds on these ideas:
https://docs.greptime.com/user-guide/deployments-administration/performance-tuning/design-table/

Key facts:

- Rows are stored sorted by `(primary key, timestamp)`. Rows sharing a primary key form one
  time series, stored contiguously — making single-series scans cheap and improving
  compression.
- A scan prunes in stages: **time range** → **row-group min/max stats** → **index** → read &
  filter. The leading primary-key column gets the most benefit from row-group pruning; there
  is no global primary-key index, so deep-key or high-cardinality point lookups need an index.
- Non-append-only tables **merge and deduplicate** by `(primary key, timestamp)` at scan time;
  append-only tables skip this and are faster.

### Phase 2. New table — make the decisions

Understand the data (cardinality of each column), the common queries (filters, GROUP BY,
ORDER BY), and whether updates/deletes are needed. Then decide:

**Primary key (tags).**

- Optional. An append-only table without a primary key (sorted by time) is a fine baseline.
- Set one when most queries benefit from its ordering, or you need to deduplicate/delete by
  it.
- Lead with the **most frequently filtered, most selective low-cardinality** column
  (`namespace`, `cluster`, `region`, `application`). Keep it to **≤5 columns**; a long key
  slows inserts and grows memory.
- Use short strings/integers; avoid `FLOAT`/`DOUBLE`/`TIMESTAMP` as tags.
- For high-cardinality columns (`trace_id`, `span_id`, `user_id`), prefer a **skipping index**
  over adding them to the primary key — add them to the key only when you must order or
  deduplicate by them.

**Append-only vs deduplication.**

- `append_mode = 'true'` — keep every row, no dedup/delete. Fastest; ideal for logs/traces.
- Default (deduplicating) — one row per `(primary key, timestamp)`, with `merge_mode`:
  `last_row` (default, faster) or `last_non_null` (update individual fields, keeps latest
  non-null). Make sure the primary key uniquely identifies a series so distinct rows aren't
  merged.

**Indexes** (optional; add when a filter is common and not already fast enough):

| Index | Best for |
|---|---|
| Inverted (`INVERTED INDEX`) | Filtering low-cardinality columns; supports `=`, `<`, `<=`, `>`, `>=`, `IN`, `BETWEEN`, `~` |
| Skipping (`SKIPPING INDEX`) | Precise filtering of high-cardinality columns; equality only; low storage/memory overhead |
| Full-text (`FULLTEXT INDEX`) | Tokenized text search in unstructured message bodies |

Primary key and index are complementary: the primary key gives ordering/locality and enables
dedup; an index targets selective filters ordering can't cover. A query can use both.

**Wide vs multiple tables.** Put metrics collected together in one wide table (better
throughput and compression). Use separate tables for logically distinct data (different
schema, columns, or TTL). For Prometheus remote-write, the metric engine handles this
automatically.

**Partitioning** — only when one node can no longer serve the table (disk, CPU, memory, or
ingestion limits). Choose partition columns that are evenly distributed, stable, and appear in
common query filters. For non-append-only tables, **partition columns must be a subset of the
primary key** (dedup happens within a partition).

Example append-only logs table:

```sql
CREATE TABLE http_logs (
  access_time  TIMESTAMP TIME INDEX,
  application  STRING,
  remote_addr  STRING,
  http_status  STRING,
  http_method  STRING INVERTED INDEX,
  http_refer   STRING,
  user_agent   STRING,
  request_id   STRING SKIPPING INDEX,
  request      STRING,
  PRIMARY KEY (application)
) WITH ('append_mode' = 'true');
```

### Phase 3. Existing table — what you can and cannot change

Be explicit about the constraints. The highest-impact choices are fixed at `CREATE`:

**Not alterable** (require recreating the table):

- Primary key
- `merge_mode`

**Alterable on a live table:**

- Add/drop **indexes** via `ALTER TABLE`. Explain that this only affects newly flushed data:
  the index is built for SST files produced by subsequent flushes and is not added to existing
  SST files (see the data-index guide).
- `append_mode` can change from `false` to `true`, but not from `true` back to `false`:

  ```sql
  ALTER TABLE my_table SET 'append_mode' = 'true';
  ```

- Existing unpartitioned tables can be repartitioned with
  `ALTER TABLE ... PARTITION ON COLUMNS`, and partitioned tables can be adjusted with
  `SPLIT PARTITION` / `MERGE PARTITION`. Repartitioning requires a distributed cluster,
  shared object storage, and GC enabled.
- `sst_format` → `flat` (only needed when upgrading from an old `primary_key`-format version):

  ```sql
  ALTER TABLE my_table SET 'sst_format' = 'flat';
  ```

- `compaction.twcs.time_window`, `TTL`, and other table options via `ALTER TABLE ... SET`.

**When a baked-in choice is wrong** (e.g. wrong primary key, wrong `merge_mode`, or need to
switch from append-only back to deduplicating mode), the path is to **create a new table with the
right schema and migrate**:

```sql
CREATE TABLE my_table_v2 ( ... corrected schema ... );
INSERT INTO my_table_v2 SELECT ... FROM my_table;
-- verify, then switch writes/reads to my_table_v2 and drop the old table
```

Confirm the time range and row volume before migrating large tables, and consider migrating in
time-window chunks.

## Escalation

If you're unsure whether a schema change will help, recommend benchmarking on the user's own
dataset (a baseline table without extra indexes is a good control). When still unclear, collect
context (`SHOW CREATE TABLE`, representative queries with `EXPLAIN ANALYZE VERBOSE`, cardinality
estimates, version) and open an issue or discussion at
https://github.com/GreptimeTeam/greptimedb.

## Reference

1. Design your table schema:
   https://docs.greptime.com/user-guide/deployments-administration/performance-tuning/design-table/
2. Data index (types, ALTER to add/drop indexes):
   https://docs.greptime.com/user-guide/manage-data/data-index/
3. CREATE TABLE (append-only, merge mode, SST format, compaction options):
   https://docs.greptime.com/reference/sql/create/
4. Table sharding / partitioning:
   https://docs.greptime.com/user-guide/deployments-administration/manage-data/table-sharding/
5. GreptimeDB Dashboard (run SQL from a web UI):
   https://docs.greptime.com/getting-started/installation/greptimedb-dashboard/
6. GreptimeDB Enterprise Management Console (SQL, metrics, logs):
   https://docs.greptime.com/enterprise/console-ui/
