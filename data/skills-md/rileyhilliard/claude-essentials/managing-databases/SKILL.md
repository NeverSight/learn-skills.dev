---
name: managing-databases
description: Guides database architecture decisions for PostgreSQL, DuckDB, Parquet, PGVector, and Neo4j. Use when designing schemas, choosing storage strategies, optimizing queries, tuning maintenance, configuring vector search, modeling graph data, or diagnosing performance issues across OLTP, OLAP, similarity search, and graph workloads.
---

# Database Management

Decision guidance for PostgreSQL, DuckDB, Parquet, and Neo4j in hybrid storage architectures.

## Contents

- When to use which database
- PostgreSQL quick reference
- DuckDB quick reference
- Parquet quick reference
- PGVector quick reference
- Neo4j quick reference
- Cross-database conventions
- Performance debugging checklist

## When to use which database

| Workload                              | Use                       | Why                                 |
| ------------------------------------- | ------------------------- | ----------------------------------- |
| Transactional (CRUD, users, sessions) | PostgreSQL                | ACID, row-level locking, indexes    |
| Analytical (aggregations, scans)      | DuckDB                    | Columnar, vectorized, parallel      |
| Data storage/interchange              | Parquet                   | Compressed, columnar, portable      |
| Metadata + relationships              | PostgreSQL                | Foreign keys, constraints           |
| Ad-hoc exploration                    | DuckDB                    | Fast on Parquet, no ETL needed      |
| Time-series with point lookups        | PostgreSQL + partitioning | Partition pruning + indexes         |
| Time-series analytics                 | DuckDB on Parquet         | Scan performance                    |
| Vector similarity search              | PostgreSQL + PGVector     | HNSW/IVFFlat indexes, hybrid search |
| RAG / semantic search                 | PostgreSQL + PGVector     | Embeddings + metadata in same DB    |
| Graph traversals / relationships      | Neo4j                     | Native graph, index-free adjacency  |
| Pattern matching / fraud detection    | Neo4j                     | Multi-hop traversal, path finding   |
| Knowledge graphs / ontologies         | Neo4j                     | Flexible schema, relationship-first |

**Hybrid pattern example:**

- PostgreSQL: transactional data, relationships, users (metadata)
- DuckDB + Parquet: analytical content, aggregations, time-series

## PostgreSQL quick reference

**Use for:** Metadata, relationships, OLTP workloads, anything needing ACID.

**Key decisions:**

- Partition tables >100M rows or with retention requirements
- Index columns in WHERE/JOIN clauses, not everything
- Tune autovacuum for high-churn tables

See [references/postgres-architecture.md](references/postgres-architecture.md) for maintenance patterns.
See [references/postgres-querying.md](references/postgres-querying.md) for advanced query techniques.

## DuckDB quick reference

**Use for:** Analytics, aggregations, Parquet queries, data exploration.

**Key decisions:**

- Prefer Parquet files over CSV (10-100x faster)
- Let DuckDB auto-parallelize; don't micro-optimize
- For remote data, increase threads beyond CPU count

See [references/duckdb-architecture.md](references/duckdb-architecture.md) for storage and parallelism.
See [references/duckdb-querying.md](references/duckdb-querying.md) for DuckDB-specific SQL features.

## Parquet quick reference

**Use for:** Storing analytical data, data interchange, columnar compression.

**Key decisions:**

- Target 128MB-1GB file sizes
- Partition by low-to-moderate cardinality columns (date, region)
- Sort by columns used in filters for better pruning

See [references/parquet-architecture.md](references/parquet-architecture.md) for file design.
See [references/parquet-querying.md](references/parquet-querying.md) for query optimization.

## PGVector quick reference

**Use for:** Similarity search, RAG applications, semantic search, recommendations.

**Key decisions:**

- HNSW for low-latency, high-recall (default choice)
- IVFFlat for memory-constrained or batch-updated data
- Use iterative scan for filtered queries
- Consider hybrid search (vector + keyword) for 8-15% accuracy boost

See [references/pgvector-architecture.md](references/pgvector-architecture.md) for index configuration.
See [references/pgvector-querying.md](references/pgvector-querying.md) for hybrid search and filtering.

## Neo4j quick reference

**Use for:** Graph traversals, relationship-heavy queries, pattern matching, knowledge graphs.

**Key decisions:**

- Model around your queries, not your source data
- Promote properties to nodes when you need to traverse through shared values
- Use specific relationship types to avoid supernode bottlenecks
- Bound all variable-length paths (`[*1..5]`, never `[*]`)
- Use parameters in Cypher for execution plan caching

See [references/neo4j-architecture.md](references/neo4j-architecture.md) for data modeling, indexing, and maintenance.
See [references/neo4j-querying.md](references/neo4j-querying.md) for Cypher optimization and anti-patterns.

## Cross-database conventions

### Naming

| Convention             | Example                  | Applies to    |
| ---------------------- | ------------------------ | ------------- |
| snake_case tables      | `dataset_jobs`           | All           |
| snake_case columns     | `created_at`             | PG, DuckDB, Parquet |
| camelCase properties   | `createdAt`              | Neo4j         |
| PascalCase labels      | `:UserAccount`           | Neo4j         |
| Singular table names   | `dataset` not `datasets` | PostgreSQL    |
| Plural for collections | `datasets/` directory    | Parquet files |

### Normalization decisions

| Pattern             | When to normalize                 | When to denormalize             |
| ------------------- | --------------------------------- | ------------------------------- |
| Lookup tables       | PostgreSQL, changes frequently    | DuckDB/Parquet, static data     |
| Repeated values     | PostgreSQL, storage matters       | Parquet, compression handles it |
| Joins at query time | PostgreSQL, complex relationships | Parquet, pre-join for analytics |

### Timestamps

- Store as UTC always
- PostgreSQL: `TIMESTAMPTZ`
- Parquet: `TIMESTAMP` with `isAdjustedToUTC=true`
- DuckDB: reads both correctly

## Performance debugging checklist

### PostgreSQL slow query

1. Run `EXPLAIN (ANALYZE, BUFFERS)` on the query
2. Check for sequential scans on large tables
3. Verify indexes exist on filter/join columns
4. Check `pg_stat_user_tables` for bloat (dead tuples)
5. Review `work_mem` if seeing disk sorts

### DuckDB slow query

1. Check if reading CSV instead of Parquet
2. Verify not doing `SELECT *` on remote data
3. Check thread count matches workload
4. Look for unnecessary type conversions

### Parquet slow reads

1. Verify predicate pushdown is working (check query plan)
2. Check file sizes (too small = overhead, too large = no parallelism)
3. Confirm data is sorted by filter columns
4. Look for high-cardinality partition keys (too many small files)

### PGVector slow search

1. Verify index exists and is being used (EXPLAIN)
2. Check `ef_search` (HNSW) or `probes` (IVFFlat) settings
3. Enable iterative scan for filtered queries
4. Check if IVFFlat recall degraded (rebuild index if heavily updated)
5. Consider partial indexes for common filters

### Neo4j slow query

1. Run `PROFILE` on the query, read operators bottom-up
2. Look for `AllNodesScan` or `NodeByLabelScan` (missing index)
3. Check for `CartesianProduct` (disconnected MATCH patterns)
4. Verify parameters are used instead of literals (plan caching)
5. Check for unbounded variable-length paths
6. Monitor `page_cache.hit_ratio` (below 98% = need more page cache memory)
