---
name: optimize-database
description: Perform complete database health, correctness, performance, reliability, and scalability audits across SQL, NoSQL, key-value, cache, search, and managed database systems. Detects the existing database and query layer, then checks indexes, query plans, schemas, constraints, relations, transactions, locks, pagination, pooling, caching, migrations, backups, observability, security, retention, replication, partitioning, and capacity. Use when diagnosing slow queries, reviewing an entire data layer, preparing for growth, reducing database cost, or safely optimizing production workloads.
---

# Database Optimization

Optimize any database technology without assuming MongoDB, PostgreSQL, MySQL, an ORM, or a particular hosting provider. Inspect evidence before making recommendations.

## First: detect the data layer

Search the repository for database drivers, ORM/query-builder packages, connection configuration, schemas/models, migrations, indexes, constraints, repositories, raw queries, transactions, seeds, caches, search systems, background jobs, analytics workloads, tests, deployment configuration, and monitoring.

Identify:

- database engines, versions, extensions, topology, hosting, and environment;
- drivers, ORM/query layer, versions, pooling, retry, and timeout configuration;
- schemas, relationships, constraints, indexes, migrations, and ownership;
- high-traffic read/write paths, data volume/growth, concurrency, latency, and throughput;
- replicas, partitions/shards, caches, queues, backup/restore, retention, and observability.

If a data layer exists, explain its current design, healthy choices, measured or evidenced problems, and an ordered safe improvement plan. If none exists, design the smallest suitable persistence approach from the product's consistency, query, scale, security, and operational requirements.

Do not upgrade a database, driver, or ORM silently. Check release notes, compatibility, migration requirements, and rollback before changing versions.

## Mandatory full audit

Check every applicable area, even when the request mentions only one slow query:

1. **Correctness and integrity** — types, nullability, uniqueness, foreign keys/references, validation, invariants, transactions, isolation, idempotency, and consistency.
2. **Indexes** — missing, unused, duplicate, overlapping, invalid, low-selectivity, oversized, write-heavy, foreign-key, compound order, covering, partial, expression, text, geospatial, TTL, and unique indexes.
3. **Queries and plans** — scans, selectivity, cardinality estimates, join strategy, sort/group operations, temporary work, N+1 calls, repeated queries, over-fetching, application-side filtering, and plan regressions.
4. **Access patterns** — real filters, sorts, joins/population, aggregations, writes, hot keys/rows, batch operations, and read/write amplification.
5. **Pagination and limits** — stable ordering, maximum limits, cursor/keyset strategy, large offsets, unbounded exports, and count-query cost.
6. **Schema and modeling** — normalization/denormalization, relationship ownership, document growth, row width, large fields, enums, temporal/history data, and multi-tenant boundaries.
7. **Concurrency** — transactions, isolation level, locks, deadlocks, optimistic/pessimistic control, race conditions, long-running work, and connection starvation.
8. **Connections** — pool sizing, leaks, timeouts, retries, backoff, prepared statements, proxy/serverless behavior, and graceful shutdown.
9. **Caching** — need, keys, TTL, invalidation, consistency, stampede protection, negative caching, memory limits, and failure fallback.
10. **Migrations** — backward compatibility, locks, table rewrites, online index creation, backfills, expand/contract rollout, validation, rollback, and deployment order.
11. **Operations** — slow-query logs, metrics, tracing, alerts, vacuum/analyze or equivalent maintenance, statistics, fragmentation/bloat, storage, and cost.
12. **Reliability** — backups, restore tests, point-in-time recovery, replication, failover, disaster recovery, RPO/RTO, and reconciliation.
13. **Growth** — retention, archival, partitioning/sharding, replicas, materialized views, queues, warehouse/search separation, capacity forecasts, and scaling thresholds.
14. **Security and privacy** — least privilege, credential storage/rotation, encryption, network access, tenant isolation, sensitive fields, audit logs, deletion/retention, and injection risks.

## Workflow

1. Establish a baseline using timings, throughput, resource use, query plans, slow-query logs, traces, or representative code and data.
2. Trace the complete request/job to every database and cache operation.
3. Rank bottlenecks by evidence and user impact instead of applying generic tuning.
4. Match indexes to real equality/range filters, joins, sort order, uniqueness, selectivity, and projection while accounting for writes and storage.
5. Fix query shape and data access before adding infrastructure. Select only needed fields, batch work, remove N+1 calls, enforce limits, and use stable cursor/keyset pagination where appropriate.
6. Check correctness, transactions, concurrency, and tenant/security boundaries before performance changes.
7. Add caching, replicas, partitions, search engines, queues, or sharding only when simpler fixes and measured requirements justify their operational cost.
8. Treat every schema, constraint, index, or data rewrite as a migration with staging evidence, rollout monitoring, and rollback/recovery.
9. Re-run the original measurements and report before/after evidence, tradeoffs, and remaining capacity limits.

## Safety

Never run destructive or irreversible database operations without explicit confirmation. This includes dropping data or indexes, truncation, unsafe deletes, column removal or rename, destructive type changes, migration resets, repartitioning, and blind production-cache flushes. Confirm the exact environment and target, verify a usable backup/restore path, test on representative staging data, assess locks and disk headroom, and prepare rollback steps first.

## Detailed guidance

Read [references/database-guide.md](references/database-guide.md) for database-specific index and query patterns, ORM advice, pooling, caching, migration and backup checklists, large-scale strategies, or the detailed review format. Search by heading and load only the sections relevant to the detected stack.

## Output

Lead with whether an existing data layer was found and summarize its engines, versions, topology, and query tools. Report findings by severity and measured or likely impact. For every recommendation, state evidence, expected benefit, tradeoff, safe rollout, rollback, and verification method. Include an index review even when no new index is recommended. Separate correctness/data-loss risks, security risks, performance bottlenecks, reliability gaps, capacity concerns, and speculative tuning.
