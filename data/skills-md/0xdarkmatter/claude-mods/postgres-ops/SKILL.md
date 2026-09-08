---
name: postgres-ops
description: "PostgreSQL operations, optimization, and administration. Use for: schema design, index selection, query tuning with EXPLAIN ANALYZE, postgresql.conf configuration, backup and restore (pg_dump, pg_basebackup, WAL, PITR), vacuum and autovacuum tuning, connection pooling (pgBouncer, pgPool), replication (streaming, logical), partitioning, monitoring (pg_stat_statements, pg_stat_activity), JSONB operations, full-text search (tsvector, tsquery), row-level security (RLS), extensions (PostGIS, pg_trgm, timescaledb), GiST/GIN/BRIN indexes, materialized views, foreign data wrappers, LISTEN/NOTIFY."
license: MIT
allowed-tools: "Read Write Bash"
metadata:
  author: claude-mods
  related-skills: sql-ops, sqlite-ops, python-database-ops
---

# PostgreSQL Operations

Comprehensive PostgreSQL skill covering schema design through production operations.

## Quick Connection

```bash
# Standard connection
psql "postgresql://user:pass@localhost:5432/dbname"

# With SSL
psql "postgresql://user:pass@host:5432/dbname?sslmode=require"

# Environment variables (libpq)
export PGHOST=localhost PGPORT=5432 PGDATABASE=mydb PGUSER=myuser PGPASSWORD=secret
psql

# Connection pooling (pgBouncer default)
psql "postgresql://user:pass@localhost:6432/dbname"
```

```sql
-- Check current connection
SELECT current_database(), current_user, inet_server_addr(), inet_server_port();

-- Active connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
```

## Index Type Selection

```
What query pattern are you optimizing?
│
├─ Equality (WHERE col = val)
│  └─ B-tree (default, almost always right)
│
├─ Range (WHERE col > val, ORDER BY, BETWEEN)
│  └─ B-tree
│
├─ Array/JSONB containment (@>, ?, ?|, ?&)
│  └─ GIN
│
├─ Full-text search (@@)
│  └─ GIN with tsvector
│
├─ Geometric/range overlap (&&, <->)
│  └─ GiST
│
├─ Pattern matching (LIKE '%text%', similarity)
│  └─ GIN with pg_trgm (gin_trgm_ops)
│
├─ Large table, few distinct values, append-only
│  └─ BRIN (tiny index, good for timestamps)
│
└─ Exact equality only, no range/sort needed
   └─ Hash (rare - B-tree usually better)
```

### Quick Index Reference

| Index | Best For | Size | Write Cost |
|-------|----------|------|------------|
| B-tree | Equality, range, sort | Medium | Low |
| GIN | Arrays, JSONB, FTS, trigrams | Large | High |
| GiST | Geometry, ranges, FTS | Medium | Medium |
| BRIN | Correlated data (timestamps) | Tiny | Very low |
| Hash | Exact equality only | Medium | Low |

**Deep dive**: Load `./references/indexing.md` for composite, partial, expression, and covering index strategies.

## EXPLAIN ANALYZE Workflow

```sql
-- Step 1: Run with ANALYZE and BUFFERS
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;

-- Step 2: Read bottom-up. Find the slowest node.
-- Step 3: Check estimates vs actuals
--   actual rows=10000, rows=100  -> bad estimate, run ANALYZE
-- Step 4: Look for these red flags:
```

| Red Flag | Meaning | Fix |
|----------|---------|-----|
| `Seq Scan` on large table | No usable index | Add index matching WHERE/JOIN |
| `actual rows` >> `estimated rows` | Stale statistics | `ANALYZE tablename` |
| `Nested Loop` with high rows | O(n*m) join | Check join conditions, add index |
| `Sort` with `external merge` | work_mem too small | Increase `work_mem` for session |
| `Buffers: shared read` >> `hit` | Cold cache or table too large | Check `shared_buffers`, add covering index |
| `Hash Batch` > 1 | Hash join spilling to disk | Increase `work_mem` |

**Deep dive**: Load `./references/query-tuning.md` for plan node reference and optimization patterns.

## Workload Profiles

| Setting | OLTP | OLAP | Notes |
|---------|------|------|-------|
| `shared_buffers` | 25% RAM | 25% RAM | Same baseline |
| `work_mem` | 4-16 MB | 256 MB-1 GB | OLAP needs big sorts |
| `effective_cache_size` | 75% RAM | 75% RAM | Planner hint |
| `random_page_cost` | 1.1 (SSD) | 1.1 (SSD) | Lower for SSD |
| `max_parallel_workers_per_gather` | 2 | 4-8 | OLAP benefits more |
| `checkpoint_completion_target` | 0.9 | 0.9 | Spread checkpoint I/O |
| `wal_buffers` | 64 MB | 64 MB | -1 for auto |
| `maintenance_work_mem` | 512 MB | 1-2 GB | For VACUUM, CREATE INDEX |

**Deep dive**: Load `./references/config-tuning.md` for full postgresql.conf walkthrough and extension setup.

## Common Operations

### Backup & Restore

```bash
# Logical backup (single database)
pg_dump -Fc dbname > backup.dump

# Restore
pg_restore -d dbname backup.dump

# Parallel backup (faster for large DBs)
pg_dump -Fc -j4 dbname > backup.dump

# Base backup for PITR
pg_basebackup -D /backup/base -Ft -Xs -P
```

### Vacuum & Maintenance

```sql
-- Manual vacuum (reclaim space, update stats)
VACUUM (VERBOSE, ANALYZE) tablename;

-- Full vacuum (rewrites table, exclusive lock)
VACUUM FULL tablename;  -- CAUTION: locks table

-- Reindex without downtime
REINDEX INDEX CONCURRENTLY idx_name;

-- Update statistics only
ANALYZE tablename;
```

### Monitor Key Metrics

```sql
-- Slow queries (requires pg_stat_statements)
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;

-- Table bloat indicator
SELECT schemaname, relname, n_dead_tup, n_live_tup,
       round(n_dead_tup::numeric / NULLIF(n_live_tup, 0) * 100, 1) AS dead_pct
FROM pg_stat_user_tables WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Lock contention
SELECT pid, relation::regclass, mode, granted, query
FROM pg_locks JOIN pg_stat_activity USING (pid)
WHERE NOT granted;

-- Cache hit ratio (should be > 99%)
SELECT sum(heap_blks_hit) / NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0) AS ratio
FROM pg_statio_user_tables;
```

**Deep dive**: Load `./references/operations.md` for WAL archiving, PITR, autovacuum tuning, connection pooling.

## Data Types Quick Reference

| Type | Use When | Example |
|------|----------|---------|
| `JSONB` | Semi-structured data, flexible schema | `'{"tags": ["a","b"]}'::jsonb` |
| `ARRAY` | Fixed-type lists | `ARRAY['a','b','c']` |
| `tsrange` | Time periods, scheduling | `'[2024-01-01, 2024-12-31)'::tsrange` |
| `tsvector` | Full-text search | `to_tsvector('english', body)` |
| `uuid` | Distributed IDs | `gen_random_uuid()` |
| `inet`/`cidr` | IP addresses, networks | `'192.168.1.0/24'::cidr` |

**Deep dive**: Load `./references/schema-design.md` for normalization, constraints, RLS, generated columns, table inheritance.

## Gotchas & Anti-Patterns

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| `SELECT *` in production | Wastes bandwidth, blocks covering index scans | List columns explicitly |
| Function on indexed column (`WHERE UPPER(email) = ...`) | Prevents index use | Expression index: `CREATE INDEX ... ON (UPPER(email))` |
| `NOT IN (subquery)` with NULLs | Returns no rows if subquery has NULL | Use `NOT EXISTS` |
| Missing `ANALYZE` after bulk load | Planner uses stale row estimates | Run `ANALYZE tablename` |
| `VACUUM FULL` in production | Exclusive lock on entire table | Regular `VACUUM` + `pg_repack` |
| `LIMIT` without `ORDER BY` | Non-deterministic results | Always pair with `ORDER BY` |
| Offset pagination on large tables | Scans and discards rows | Keyset pagination: `WHERE id > last_id` |
| Too many indexes | Slows writes, wastes space | Audit with `pg_stat_user_indexes` |
| Single shared connection pool | Contention across services | Per-service pools via pgBouncer |
| `default_transaction_isolation = serializable` | Excessive serialization failures | Keep `read committed`, use explicit `SERIALIZABLE` where needed |

## Row-Level Security (RLS) Quick Start

```sql
-- Enable RLS on table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy: users see only their own rows
CREATE POLICY user_isolation ON documents
    USING (owner_id = current_setting('app.current_user_id')::int);

-- Policy: admins see everything
CREATE POLICY admin_access ON documents
    USING (current_setting('app.role') = 'admin');

-- Set context per request (from app layer)
SET app.current_user_id = '42';
SET app.role = 'user';
```

## Full-Text Search Quick Start

```sql
-- Add search column
ALTER TABLE articles ADD COLUMN search_vector tsvector
    GENERATED ALWAYS AS (to_tsvector('english', title || ' ' || body)) STORED;

-- Index it
CREATE INDEX idx_articles_fts ON articles USING gin(search_vector);

-- Search with ranking
SELECT title, ts_rank(search_vector, query) AS rank
FROM articles, to_tsquery('english', 'database & optimization') AS query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

## LISTEN/NOTIFY

```sql
-- Publisher
NOTIFY order_events, '{"order_id": 123, "status": "shipped"}';

-- Subscriber (in psql or app)
LISTEN order_events;

-- Check for notifications (app code)
-- Python: conn.poll(); conn.notifies
-- Node: client.on('notification', callback)
```

## Reference Files

Load these for deep-dive topics. Each is self-contained.

| Reference | When to Load |
|-----------|-------------|
| `./references/schema-design.md` | Designing tables, choosing types, constraints, RLS policies, JSONB modeling |
| `./references/indexing.md` | Choosing index types, composite/partial/expression indexes, index maintenance |
| `./references/query-tuning.md` | Reading EXPLAIN plans, pg_stat_statements, optimizing specific query patterns |
| `./references/operations.md` | Backup/restore, WAL/PITR, vacuum tuning, monitoring, connection pooling |
| `./references/replication.md` | Streaming/logical replication, failover, partitioning, FDW |
| `./references/config-tuning.md` | postgresql.conf settings, OLTP/OLAP profiles, extension setup |

## See Also

- `sql-ops` - Vendor-neutral SQL patterns (CTEs, window functions, JOINs)
- `sqlite-ops` - SQLite-specific patterns and operations
- `python-database-ops` - SQLAlchemy ORM and async database patterns
