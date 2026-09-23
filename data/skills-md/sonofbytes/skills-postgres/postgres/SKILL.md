---
name: postgres
description: Use when designing, writing or changing anything that touches a PostgreSQL database in an application — choosing column types and keys, modelling entities, tenancy and state, writing constraints, adding or auditing indexes, writing queries (pagination, upserts, EXPLAIN), transactions and locking, job queues on SKIP LOCKED, full-text search, pgvector, partitioning, writing lock-safe migrations, roles and row-level security, connection pooling, server settings, backups, observability, and data-layer tests. Determines the Postgres major version, deployment shape and access layer (pgx, Npgsql/EF Core, sqlc) first, then routes to a sourced reference. Every rule cites official documentation or a recognised authority. For reviewing an existing database, use the postgres-quality-reviewer agent.
---

# PostgreSQL for Application Databases

This skill is the writing-side companion to the `postgres-quality-reviewer` agent. The agent
reviews; this skill tells you how to build it right the first time. Every reference file carries
its rules as "do X because Y [source]", and every source is listed in `SOURCES.md` with its
credibility tier. Nothing here needs web access at runtime.

Supported majors at time of writing: 14 (end of life 12 November 2026), 15, 16, 17, 18; 19 is in
beta. Rules that depend on a version carry a marker such as `[pg>=15]` or `[pg<=17]`;
`references/versions.md` is the matrix.

## Step 1 — Determine three things. Always.

**Do this before reading any reference file** and state the answers in your reply, so a wrong
inference is visible.

| Fact | Where to look, in order | Why it matters |
|---|---|---|
| **Postgres major version** | docs and `CLAUDE.md`; CI `services:` image; compose or Dockerfile `image:`/`FROM`; IaC (`engine_version`, `database_version`); a dump header `-- Dumped from database version`; a live `SELECT version()` on a test database only | features and defaults differ per major; never write `uuidv7()` for a 16 cluster |
| **Deployment shape** | a `postgres` service in compose = self-hosted container; RDS, Cloud SQL, Neon, Supabase, Azure hostnames = managed; `pgbouncer`, `-pooler`, port 6543 = pooled | managed services own settings and backups; poolers forbid session state |
| **Access layer** | `go.mod` (`jackc/pgx`), `*.csproj` (`Npgsql`, `EntityFrameworkCore`), `sqlc.yaml`, ORM config files | driver execution mode, error types, pool fields and scanning differ |

If the major version cannot be determined, **ask**. Do not default to the newest.

## Step 2 — Read the matching reference

| Task | Read |
|---|---|
| Choose column types, a primary-key strategy, enums vs lookup tables, jsonb boundaries | `references/types.md` |
| Foreign keys and ON DELETE, CHECK, unique and partial unique, exclusion constraints | `references/constraints.md` |
| Model an entity, tenancy, polymorphism, soft delete vs hard delete, state machines, history | `references/modelling.md` |
| Name tables, columns, indexes and constraints | `references/naming.md` |
| Add or audit an index; choose B-tree, GIN, GiST, BRIN | `references/indexing.md` |
| Change an existing query's ordering or predicate and name the index that serves it | `references/queries.md` then `references/indexing.md` |
| Write a query: pagination, upsert, N+1, CTEs, LATERAL, reading EXPLAIN | `references/queries.md` |
| Transactions, isolation, retries, locking, advisory locks, LISTEN/NOTIFY | `references/transactions.md` |
| A job queue on `SKIP LOCKED`, staged job drain, idempotency keys | `references/queues.md` |
| Full-text search, trigram search, pgvector, materialized views, CDC, vetting an extension | `references/capabilities.md` |
| Decide whether to partition, and partition DDL | `references/partitioning.md` |
| Write a migration: process, lock safety, tools, the schema guard | `references/migrations.md` |
| The safe sequence for a specific ALTER (add NOT NULL, change type, add index, rename) | `references/migration-recipes.md` |
| Roles and grants, authentication, TLS, injection, search_path, encryption, logging | `references/security.md` |
| Row-level security policies for multi-tenant tables | `references/rls.md` |
| Connection pool sizing, PgBouncer mode, what transaction pooling breaks | `references/pooling.md` then `references/drivers/<layer>.md` |
| Server settings, timeouts per role, vacuum, the container, collation | `references/operations.md` |
| Backups, point-in-time recovery, monitoring, health probes, tracing | `references/backup-and-observability.md` |
| Data-layer tests: fixtures, failure paths, concurrency, isolation, migrations | `references/testing.md` |
| Which major has a feature; end-of-life dates | `references/versions.md` |
| pgx (Go): pool config, exec mode, batching, scanning, error mapping | `references/drivers/pgx.md` |
| Npgsql and EF Core (.NET): pool, prepare, lazy loading, generated migrations | `references/drivers/npgsql.md` |
| sqlc: query files, slices, generated code boundaries | `references/drivers/sqlc.md` |

## Rules that hold everywhere

1. **Invariants in the database, policy in the application.** Uniqueness, referential integrity,
   non-null, non-overlap and closed value sets are constraints. Rules that change are code.
2. **Every value is a bound parameter.** Identifiers go through `format('%I')`. There is no third
   case.
3. **Tenant scope is an explicit parameter** on every scoped query; row-level security is defence
   in depth behind it, never the only fence.
4. **`timestamptz`, `text`, `bigint identity`, `jsonb`, `numeric`.** Never `timestamp`, `char(n)`,
   `serial`, `json`, `money` or floats for money.
5. **Every migration that takes a lock sets `lock_timeout`** and every index on a live table is
   built `CONCURRENTLY`.
6. **`SET LOCAL`, never `SET`,** for anything per-transaction, because the next checkout of a
   pooled connection is someone else.
7. **Tests run against a real Postgres** from the real migrations, and a constraint is unproven
   until a test has watched it reject a row.

## Instructions for Claude

- Resolve the three facts first; say what you resolved and from which file.
- Read only the references the task needs; `versions.md` when a marker is in doubt.
- When you write DDL, state the lock class of each statement and whether it can run inside a
  transaction. When you write a query, name the index that serves it.
- When a rule here conflicts with the project's own documented convention, the project wins;
  say so rather than silently following either.
- Reviewing an existing database is the agent's job: `Agent({ subagent_type:
  "postgres-quality-reviewer", ... })`.
