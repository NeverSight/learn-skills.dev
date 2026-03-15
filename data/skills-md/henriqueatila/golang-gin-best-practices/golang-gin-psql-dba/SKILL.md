---
name: golang-gin-psql-dba
description: "PostgreSQL DBA and architect skill for Go Gin APIs. Covers schema design decisions, migration impact analysis, index strategy, query optimization, partitioning, connection pool sizing, and the PostgreSQL extension ecosystem (ParadeDB, pgvector, PostGIS, TimescaleDB). Use when designing schemas, analyzing migration safety, choosing indexes, optimizing queries, selecting extensions, or making any PostgreSQL architecture decision. This is the 'how to think' complement to golang-gin-database's 'how to connect.' Also activate when the user mentions EXPLAIN ANALYZE, lock levels, zero-downtime migration, full-text search, vector embeddings, geospatial queries, time-series data, or database performance tuning."
license: MIT
metadata:
  author: henriqueatila
  version: "1.0.0"
---

# golang-gin-psql-dba — PostgreSQL DBA / Architect

Make PostgreSQL architecture decisions for Go Gin APIs. Schema design, migration safety, index strategy, query optimization, and extension selection. Uses raw SQL via sqlx — for ORM patterns, see the **golang-gin-database** skill.

## When to Use

- Designing a new PostgreSQL schema (tables, types, constraints, naming)
- Evaluating whether an ALTER TABLE is safe to run on a live database
- Choosing the right index type for a query pattern
- Reading EXPLAIN ANALYZE output and fixing slow queries
- Sizing connection pools or tuning autovacuum
- Selecting a PostgreSQL extension (search, vectors, geospatial, time-series)
- Deciding on partitioning strategy

**golang-gin-psql-dba vs golang-gin-database:** golang-gin-database covers GORM/sqlx wiring, repository pattern, and migrations tooling (golang-migrate). golang-gin-psql-dba covers the PostgreSQL decisions *behind* those patterns — what data types to pick, which index to create, how to ALTER TABLE safely, and when to reach for an extension.

## Schema Design Quick Rules

| Rule | Do | Don't |
|---|---|---|
| Primary keys | `id UUID DEFAULT gen_random_uuid()` or `id BIGINT GENERATED ALWAYS AS IDENTITY` | `SERIAL` (legacy) |
| Timestamps | `TIMESTAMPTZ` with `DEFAULT now()` | `TIMESTAMP` (no timezone) |
| Booleans | `NOT NULL DEFAULT false` | Nullable booleans (three-valued logic) |
| Money | `NUMERIC(19,4)` | `FLOAT`, `REAL`, `DOUBLE PRECISION` |
| Status/enum | `TEXT` + `CHECK` constraint, or PostgreSQL `ENUM` type | Free-text strings |
| Naming | `snake_case`, plural table names (`users`), singular columns | `camelCase`, `PascalCase` |
| Soft delete | `deleted_at TIMESTAMPTZ` (nullable) | Boolean `is_deleted` |
| Foreign keys | Always `ON DELETE` clause (CASCADE, SET NULL, or RESTRICT) | Omitting ON DELETE |

For complete schema design patterns (normalization, multi-tenancy, audit trails): see [references/schema-design.md](references/schema-design.md).

## Index Selection Decision Tree

| Query Pattern | Index Type | Example |
|---|---|---|
| Equality (`=`), range (`<`, `>`, `BETWEEN`) | **B-tree** (default) | `CREATE INDEX idx_users_email ON users (email)` |
| Full-text search (`@@`, `tsvector`) | **GIN** | `CREATE INDEX idx_posts_search ON posts USING gin (search_vector)` |
| JSONB containment (`@>`), array overlap (`&&`) | **GIN** | `CREATE INDEX idx_meta ON products USING gin (metadata jsonb_path_ops)` |
| Geometric / spatial / range types | **GiST** | `CREATE INDEX idx_loc ON stores USING gist (location)` |
| Large table, monotonic column (timestamp, id) | **BRIN** | `CREATE INDEX idx_events_ts ON events USING brin (created_at)` |
| Trigram similarity (`%`, `LIKE '%foo%'`) | **GIN + pg_trgm** | `CREATE INDEX idx_name_trgm ON users USING gin (name gin_trgm_ops)` |
| High-dimensional vectors (embeddings) | **HNSW** or **IVFFlat** (pgvector) | `CREATE INDEX idx_embed ON items USING hnsw (embedding vector_cosine_ops)` |
| IP ranges, text ranges | **SP-GiST** | `CREATE INDEX idx_ip ON logs USING spgist (ip_range)` |

**Rules of thumb:**
- Default to B-tree. Only switch when B-tree cannot serve the query pattern.
- Partial indexes (`WHERE active = true`) reduce size and maintenance for filtered queries.
- Covering indexes (`INCLUDE (col)`) let the planner do index-only scans.
- Never index columns with very low cardinality (e.g., boolean) alone — combine in composite indexes.

For deep dive on each index type with EXPLAIN ANALYZE: see [references/index-strategy.md](references/index-strategy.md).

## Migration Safety Quick Guide

Every `ALTER TABLE` acquires a lock. The lock level determines whether reads and writes are blocked.

| Operation | Lock Level | Safe Online? | Notes |
|---|---|---|---|
| `ADD COLUMN` (nullable, no default) | `AccessExclusiveLock` | **Yes** — fast metadata change | Safest column addition |
| `ADD COLUMN ... DEFAULT x` (PG 11+) | `AccessExclusiveLock` | **Yes** — fast since PG 11 | Pre-PG11: rewrites table |
| `ADD COLUMN ... NOT NULL DEFAULT x` (PG 11+) | `AccessExclusiveLock` | **Yes** — fast since PG 11 | Same as above |
| `DROP COLUMN` | `AccessExclusiveLock` | **Yes** — fast metadata mark | Data remains until VACUUM |
| `ALTER COLUMN SET NOT NULL` | `AccessExclusiveLock` | **Slow** — full table scan | Use `NOT VALID` constraint instead |
| `ALTER COLUMN TYPE` | `AccessExclusiveLock` | **Slow** — full table rewrite | Create new column + backfill instead |
| `ADD CONSTRAINT ... FOREIGN KEY` | `ShareRowExclusiveLock` | **Slow** — validates all rows | Use `NOT VALID` then `VALIDATE` separately |
| `CREATE INDEX` | `ShareLock` | **Blocks writes** | Use `CONCURRENTLY` instead |
| `CREATE INDEX CONCURRENTLY` | `ShareUpdateExclusiveLock` | **Yes** | Takes longer but doesn't block |
| `DROP INDEX` | `AccessExclusiveLock` | **Blocks all** | Use `CONCURRENTLY` |

**Zero-downtime pattern for NOT NULL:**

```sql
-- Step 1: Add constraint as NOT VALID (fast, no scan)
ALTER TABLE users ADD CONSTRAINT users_email_not_null
    CHECK (email IS NOT NULL) NOT VALID;

-- Step 2: Validate in a separate transaction (scans, but allows writes)
ALTER TABLE users VALIDATE CONSTRAINT users_email_not_null;
```

**Always set `lock_timeout` in migration scripts:**

```sql
SET lock_timeout = '5s';
-- If the lock can't be acquired in 5s, the migration fails instead of blocking all traffic.
```

For complete zero-downtime patterns (column rename, type change, backfill): see [references/migration-impact-analysis.md](references/migration-impact-analysis.md).

## Extension Selection Guide

| Need | Extension | Maturity | Reference |
|---|---|---|---|
| Full-text BM25 search | **ParadeDB (pg_search)** | Growing (production-ready) | [paradedb-full-text-search.md](references/paradedb-full-text-search.md) |
| Vector similarity (embeddings) | **pgvector** | Mature | [pgvector-embeddings.md](references/pgvector-embeddings.md) |
| Geospatial queries | **PostGIS** | Very mature | [postgis-geospatial.md](references/postgis-geospatial.md) |
| Time-series data | **TimescaleDB** | Mature | [timescaledb-time-series.md](references/timescaledb-time-series.md) |
| Cron jobs inside PostgreSQL | **pg_cron** | Mature | [extensions-toolkit.md](references/extensions-toolkit.md) |
| Table partitioning management | **pg_partman** | Mature | [extensions-toolkit.md](references/extensions-toolkit.md) |
| Fuzzy string matching (`LIKE '%x%'`) | **pg_trgm** | Core contrib | [extensions-toolkit.md](references/extensions-toolkit.md) |
| Encryption / hashing | **pgcrypto** | Core contrib | [extensions-toolkit.md](references/extensions-toolkit.md) |
| Audit logging | **pgAudit** | Mature | [extensions-toolkit.md](references/extensions-toolkit.md) |

**Decision shortcuts:**
- Need search? Start with PostgreSQL built-in `tsvector` + GIN. If you need BM25 ranking, fuzzy, or hybrid search → ParadeDB.
- Need AI/ML embeddings? → pgvector with HNSW index.
- Need lat/lng distance queries? → PostGIS. Use `geography` type for global lat/lng, `geometry` for local projected data.
- Need IoT / metrics / time-bucketed aggregation? → TimescaleDB.

## EXPLAIN ANALYZE Cheat Sheet

```go
// helper: run EXPLAIN ANALYZE from Go and log the plan
func ExplainQuery(ctx context.Context, db *sqlx.DB, query string, args ...any) (string, error) {
    row := db.QueryRowContext(ctx, "EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) "+query, args...)
    var plan string
    if err := row.Scan(&plan); err != nil {
        return "", fmt.Errorf("explain: %w", err)
    }
    return plan, nil
}
```

**5 things to look for in the output:**

| Signal | What It Means | Fix |
|---|---|---|
| `Seq Scan` on large table | Missing index or planner ignoring it | Add index; check `random_page_cost` |
| `actual rows=` ≫ `rows=` (estimated) | Stale statistics | `ANALYZE tablename;` |
| `Buffers: shared hit=0 read=N` | Cold cache, high I/O | Increase `shared_buffers`; warm cache |
| `Sort Method: external merge` | `work_mem` too low for sort | Increase `work_mem` for session |
| `Nested Loop` with large outer | Planner underestimating join size | Check stats; consider `SET enable_nestloop = off` to test |

For full performance tuning (pg_stat_statements, autovacuum, bloat, monitoring): see [references/query-performance.md](references/query-performance.md).

## Connection Pool Sizing

**Formula (per backend process):**

```
max_connections = (core_count * 2) + effective_spindle_count
```

For SSDs: `core_count * 2 + 1` is a practical starting point (e.g., 4 cores → 9 connections).

**Go application pool settings:**

```go
sqlDB.SetMaxOpenConns(25)          // Match PgBouncer pool_size or PostgreSQL max_connections budget
sqlDB.SetMaxIdleConns(5)           // Keep some warm connections ready
sqlDB.SetConnMaxLifetime(5 * time.Minute)  // Recycle to balance load across replicas
sqlDB.SetConnMaxIdleTime(1 * time.Minute)  // Close idle connections faster in low-traffic periods
```

**PgBouncer guidance:**
- Use **transaction** pooling mode (default) — releases connection back to pool after each transaction
- Set `pool_size` per database to match your PostgreSQL `max_connections` budget for that app
- Set `reserve_pool_size = 5` for burst handling
- Don't use session pooling with connection-pool-aware Go drivers (pgx already pools)

## Partitioning Strategy

| Strategy | When to Use | Example |
|---|---|---|
| **RANGE** | Time-series, date-based queries | `PARTITION BY RANGE (created_at)` |
| **LIST** | Known, fixed categories | `PARTITION BY LIST (region)` |
| **HASH** | Even distribution, no natural range | `PARTITION BY HASH (user_id)` |

**Rules:**
- Partition when a single table exceeds ~50–100M rows or you need fast bulk deletes (drop partition)
- Always include the partition key in WHERE clauses — otherwise the planner scans all partitions
- Use **pg_partman** for automated partition creation and retention
- Partitioned tables support indexes, constraints, and foreign keys (PostgreSQL 12+)

```sql
CREATE TABLE events (
    id         BIGINT GENERATED ALWAYS AS IDENTITY,
    tenant_id  UUID NOT NULL,
    event_type TEXT NOT NULL,
    payload    JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE events_2026_01 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE events_2026_02 PARTITION OF events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
```

## Reference Files

Load these for deeper detail:

- **[references/schema-design.md](references/schema-design.md)** — Naming conventions, data type selection, normalization, constraints, soft delete patterns, multi-tenancy, audit trails, complete schema example
- **[references/migration-impact-analysis.md](references/migration-impact-analysis.md)** — Lock hierarchy, safe vs unsafe ALTER TABLE, zero-downtime patterns for every operation, batched backfill, NOT VALID constraints, lock_timeout strategy, migration checklist
- **[references/index-strategy.md](references/index-strategy.md)** — B-tree, GIN, GiST, BRIN, SP-GiST, partial, expression, covering indexes, index maintenance, EXPLAIN ANALYZE deep dive, complete example
- **[references/query-performance.md](references/query-performance.md)** — pg_stat_statements setup, autovacuum tuning, bloat detection, planner statistics, work_mem, connection pool sizing, read replicas, monitoring Go helper
- **[references/extensions-toolkit.md](references/extensions-toolkit.md)** — pg_cron, pg_partman, pg_trgm, pg_stat_statements, pgcrypto, uuid-ossp, pgAudit, extension management in migrations
- **[references/paradedb-full-text-search.md](references/paradedb-full-text-search.md)** — BM25 search, pg_search setup, queries, fuzzy/autocomplete, hybrid search with pgvector, analytics, Go integration
- **[references/pgvector-embeddings.md](references/pgvector-embeddings.md)** — Vector types, IVFFlat vs HNSW, similarity queries, Go integration with pgvector-go, capacity planning
- **[references/postgis-geospatial.md](references/postgis-geospatial.md)** — geometry vs geography, spatial types, GiST indexes, distance/KNN/bounding box/point-in-polygon queries, Go integration
- **[references/timescaledb-time-series.md](references/timescaledb-time-series.md)** — Hypertables, time_bucket, continuous aggregates, compression, retention, downsampling, Go integration
- **[references/row-level-security.md](references/row-level-security.md)** — RLS setup, policy types, PERMISSIVE vs RESTRICTIVE, multi-tenant session variable pattern, Gin middleware, Go repository integration, performance, testing with testcontainers, common pitfalls
- **[references/backup-and-recovery.md](references/backup-and-recovery.md)** — pg_dump/pg_restore, pg_basebackup, WAL archiving, PITR, backup validation, managed DB backups, disaster recovery checklist
- **[references/replication-and-ha.md](references/replication-and-ha.md)** — Streaming replication, logical replication, read/write splitting in Go, replication lag monitoring, Patroni HA, pg_auto_failover, managed HA, application resilience

## Cross-Skill References

- For GORM/sqlx repository implementations and migrations tooling: see the **golang-gin-database** skill
- For testing database queries with testcontainers: see the **golang-gin-testing** skill
- For PostgreSQL Docker setup and Kubernetes StatefulSets: see the **golang-gin-deploy** skill
- For handler patterns that call repository methods: see the **golang-gin-api** skill
