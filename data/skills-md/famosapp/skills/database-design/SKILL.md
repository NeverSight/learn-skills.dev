---
name: database-design
description: |
  Design and review PostgreSQL schemas for this codebase: dual-key feature tables
  (`id` + `uuid`), soft or hard deletes by use case, indexes, JSONB, constraints,
  query performance (keyset pagination, EXPLAIN, anti-patterns), and TimescaleDB
  hypertables for append-only / time-series data. Includes critical / recommended /
  nit review checklist for migrations, sqlc queries, and PRs.

  Trigger when the user asks to design, create, alter, or review PostgreSQL
  tables, migrations, data types, foreign keys, indexes, partitioning,
  continuous aggregates, slow queries, pagination, sqlc queries, or OLTP /
  insert-heavy schemas. Pick mode from the conversation (schema_design,
  schema_review, migrate_evolve, query_tune, timescale).

  Keywords: PostgreSQL, schema, table design, dual-key, soft delete, hard delete,
  IDENTITY, UUID, FOREIGN KEY, indexes, JSONB, Timestamptz, TimescaleDB,
  hypertable, migration, golang-migrate, sqlc, schema review, query optimization,
  EXPLAIN, keyset pagination, tenant_id, critical, recommended, nit
version: 1.4.0
license: Apache-2.0
metadata:
  author: famosapp
  stack: postgresql-15+, golang-migrate, sqlc
  related_skills: make-it-clear, bruno-openapi, team-orch, git-full
  canonical_migration: 20260101000001_iam_core.up.sql
---

# PostgreSQL Database Design

Production schema design for this stack. **Non-negotiables override general
PostgreSQL advice.** Read the linked reference before inventing patterns.

**Announce when activating:**
`Using the database-design skill — mode: <mode>.`

## When to load which reference

| Need | Read |
|------|------|
| Which mode / vague “we need a database” | [modes.md](references/modes.md) |
| New feature / reference / junction table | [non-negotiable.md](references/non-negotiable.md), [dual-key-template.md](references/dual-key-template.md) |
| Soft vs hard delete | [deletes.md](references/deletes.md) |
| Types, CHECKs, FK actions | [data-types.md](references/data-types.md), [do-dont.md](references/do-dont.md) |
| Indexes, soft-delete, keyset | [indexing.md](references/indexing.md) |
| Query / EXPLAIN / pagination perf | [query-performance.md](references/query-performance.md) |
| sqlc Get/List/Create/Delete | [sqlc.md](references/sqlc.md) |
| golang-migrate up/down, expand/contract | [migrations.md](references/migrations.md) |
| Triggers, extensions, comments | [triggers-extensions.md](references/triggers-extensions.md) |
| JSONB columns / GIN | [jsonb.md](references/jsonb.md) |
| Events, metrics, audit, IoT | [timescaledb.md](references/timescaledb.md), [append-only.md](references/append-only.md) |
| Pitfalls & evolution | [gotchas.md](references/gotchas.md) |
| Review / PR feedback | [review-checklist.md](references/review-checklist.md) |
| Copy-paste DDL | [examples.md](references/examples.md) |

---

## Core rules

1. **Normalize to 3NF first.** Denormalize only for measured, high-ROI reads.
2. **Every API-facing entity uses the dual-key skeleton** — internal `id`, public `uuid`, timestamps, `extra`. Soft vs hard delete is chosen per table — see [deletes.md](references/deletes.md) and [dual-key-template.md](references/dual-key-template.md).
3. **Foreign keys reference `id` (BIGINT), never `uuid`.** Index every FK column manually.
4. **Name tables `{group}_{entity}`** (`iam_users`, `widget_widgets`). Columns `snake_case`, unquoted.
5. **Types:** `TEXT`, `BIGINT`, `BOOLEAN NOT NULL`, `TIMESTAMPTZ`, `NUMERIC` for money, `JSONB NOT NULL DEFAULT '{}'`. Prefer `TEXT` + `CHECK` over Postgres `ENUM`.
6. **Index access paths you query** — FK columns, hot filters/sorts, and keyset indexes. Soft-delete tables add partial live-row indexes; hard-delete tables use plain UNIQUE/keyset.
7. **Mint `uuid` in the application** (`pkg/random.UUID()` v7). No DB uuid default on feature tables — not `gen_random_uuid()`, not PG18 `uuidv7()`.
8. **Append-only / time-series** → skip full dual-key; use [append-only.md](references/append-only.md) or TimescaleDB [timescaledb.md](references/timescaledb.md).
9. **Tenancy (when the product is multi-tenant):** `tenant_id BIGINT` → parent `id`, never `tenant_uuid`. Filter in sqlc; RLS only if the product requires DB-enforced isolation.

---

## Non-negotiable

These are project law. Full contract: [non-negotiable.md](references/non-negotiable.md).

| Rule | Requirement |
|------|-------------|
| Dual-key | `id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY` + `uuid UUID UNIQUE NOT NULL` (app-supplied) |
| API surface | Clients see **only** `uuid`. Never expose `id` in URLs, DTOs, or JSON |
| FKs | `*_id BIGINT REFERENCES parent(id)` — never store parent uuid as FK |
| Deletes | Soft **or** hard by use case — pick deliberately ([deletes.md](references/deletes.md)). Soft: `deleted_at` + partial live indexes. Hard: omit `deleted_at`, use `DELETE` + FK `ON DELETE` |
| Timestamps | `created_at` / `updated_at` `TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP` |
| Metadata | `extra JSONB NOT NULL DEFAULT '{}'` — omit from list queries |
| Identity | `GENERATED ALWAYS AS IDENTITY` — never `SERIAL` / `BIGSERIAL` |
| UUID mint | App `pkg/random.UUID()` v7 — never `DEFAULT gen_random_uuid()` / `uuidv7()` on feature tables |
| Tenancy | `tenant_id BIGINT` FK to `id`; never store `tenant_uuid` as the tenant key |
| HTTP twin | Public REST sees **`uuid` only**; same-PR OpenAPI + Bruno if the table is API-facing |
| Strings | `TEXT` (+ optional `CHECK (length(...) <= n)`) — never `VARCHAR(n)` / `CHAR(n)` |
| Time | `TIMESTAMPTZ` — never bare `TIMESTAMP` |
| Money | `NUMERIC(p,s)` — never `FLOAT` / `MONEY` |
| Status enums | `TEXT NOT NULL CHECK (status IN (...))` — not `CREATE TYPE ... AS ENUM` |
| Updated_at | Trigger `set_updated_at()` + explicit `updated_at = now()` in UPDATE queries |
| Extensions (default) | Only `pgcrypto` and `citext` unless a feature proves need |

Canonical live reference: `20260101000001_iam_core.up.sql` (`iam_users`). Junction/child patterns: `iam_teams_tokens.up.sql`.

---

## PostgreSQL “Gotchas”

Summary — details in [gotchas.md](references/gotchas.md).

- Unquoted identifiers → lowercased. Use `snake_case` only.
- **UNIQUE allows multiple NULLs** unless `NULLS NOT DISTINCT` (PG15+).
- **PostgreSQL does not auto-index FK columns** — add them.
- No silent truncation: length/precision overflows **error**.
- Identity/sequence **gaps are normal** — never “fix” consecutive IDs.
- Heap storage: no clustered PK by default; row order ≈ insert order.
- MVCC: updates leave dead tuples — avoid hot wide-row churn; consider HOT/`fillfactor`.
- `CREATE INDEX CONCURRENTLY` cannot run inside a transaction (golang-migrate wraps migrations).
- Volatile defaults on new `NOT NULL` columns rewrite the table.
- Soft-delete tables: partial unique indexes enforce uniqueness among **live** rows only (`WHERE deleted_at IS NULL`). Soft delete is an UPDATE — FK `ON DELETE` does **not** fire.
- PG18 `uuidv7()` exists; this stack still **app-mints** `uuid` — no DB default.

---

## Data types

| Domain | PostgreSQL | Notes |
|--------|------------|-------|
| Internal PK / FK | `BIGINT GENERATED ALWAYS AS IDENTITY` / `BIGINT` | Never expose PK |
| External id | `UUID` | App-minted v7; UNIQUE; no PG18 `uuidv7()` default |
| Tenant FK | `BIGINT` | `tenant_id` → parent `id`; never `tenant_uuid` |
| String | `TEXT` | Bound with `CHECK`, not `VARCHAR` |
| Integer | `BIGINT` | Prefer over `INTEGER` unless range tiny |
| Boolean | `BOOLEAN NOT NULL` | Nullable only for meaningful tri-state |
| Instant | `TIMESTAMPTZ` | `now()` = tx start; `clock_timestamp()` = wall clock |
| Money / exact decimal | `NUMERIC(p,s)` | |
| Float (non-money) | `DOUBLE PRECISION` | Or `NUMERIC` if exact |
| Binary | `BYTEA` | |
| Metadata | `JSONB NOT NULL DEFAULT '{}'` | GIN only when queried |
| Enum-like | `TEXT` + `CHECK` or lookup table | Not Postgres ENUM |
| IP | `INET` | |
| Case-insensitive | `TEXT` + `LOWER(col)` index, or `CITEXT` sparingly | |

Full matrix, arrays, ranges, FTS, domains: [data-types.md](references/data-types.md).

---

## Tables and column types

### Feature / reference tables (default)

Clone the dual-key skeleton — keep `id`/`uuid` + timestamps + `extra`; **include
`deleted_at` only when soft delete is chosen**. Replace core columns only.

```sql
-- Soft-delete variant (durable API entities)
CREATE TABLE IF NOT EXISTS widget_widgets (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
    uuid UUID UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,              -- omit entirely for hard-delete tables
    -- core fields …
    name    TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    extra JSONB NOT NULL DEFAULT '{}'
);
```

Template + both delete modes: [dual-key-template.md](references/dual-key-template.md),
[deletes.md](references/deletes.md).

### Junction / child tables

May omit public `uuid` when not API-addressable. Still use BIGINT FKs, explicit
`ON DELETE`, and indexes on every FK. **Prefer hard delete** for junctions,
memberships, and tokens.

### Append-only / event tables

Internal, insert-heavy, keyed by `(time, entity_id)` — not dual-key. See [append-only.md](references/append-only.md). If TimescaleDB is available, follow [timescaledb.md](references/timescaledb.md).

### Table kinds

| Kind | Use |
|------|-----|
| Regular (default) | Durable OLTP feature data |
| `UNLOGGED` | Rebuildable cache/staging only |
| `TEMPORARY` | Session scratch |
| Hypertable | Insert-heavy time-series when TimescaleDB is enabled |

---

## DO and DON'T

| DO | DON'T |
|----|--------|
| Dual-key on API entities; pick soft **or** hard delete per table | Expose sequential `id` to clients |
| Soft: `deleted_at` + partial live indexes; Hard: real `DELETE` + FK actions | Assume soft delete fires `ON DELETE CASCADE` |
| FK → `parent(id)` + explicit index | FK on `uuid` or rely on implicit FK indexes |
| `TEXT` + `CHECK` for evolving status | Postgres `ENUM` for business statuses |
| `TIMESTAMPTZ`, `NUMERIC` for money | `TIMESTAMP`, `FLOAT`/`MONEY` for money |
| `GENERATED ALWAYS AS IDENTITY` | `SERIAL` / `BIGSERIAL` |
| App-mint UUID v7 before INSERT | DB `DEFAULT gen_random_uuid()` / `uuidv7()` on feature tables |
| `tenant_id BIGINT` → parent `id` | `tenant_uuid` as the tenant FK |
| Match indexes to delete mode | Unique constraints that block soft-delete key reuse |
| Index FK + hot WHERE/ORDER BY | Index every column “just in case” |
| `ON DELETE`/`ON UPDATE` explicit | Silent default without thinking |
| GIN on JSONB only when filtered | Default GIN on every `extra` |
| Business rules in service layer | Encode product logic only in triggers |
| Hypertables for proven insert-heavy time data | Full dual-key skeleton on event logs |

Complete list: [do-dont.md](references/do-dont.md).

---

## Critical / Recommended / Nits

Use when designing **or reviewing** schema. Full checklist:
[review-checklist.md](references/review-checklist.md).

Report as `path:line: <severity>: <problem>. <fix>.`

### Critical (block merge)

| Area | Fail if… |
|------|----------|
| Dual-key / API | Missing `id`+`uuid` on API entities; `id` leaked to clients/OpenAPI; FK on `uuid` |
| Identity | `SERIAL`/`BIGSERIAL`; DB `DEFAULT gen_random_uuid()` / `uuidv7()` on feature `uuid` |
| Types | Money as float/`MONEY`; bare `TIMESTAMP`; `VARCHAR`; evolving Postgres `ENUM` |
| Deletes | Mode undecided/mismatched; soft UNIQUE without partial; assumes soft fires `ON DELETE` |
| FKs | Missing FK index; missing `ON DELETE` on owned/destructive edges |
| Queries | Unparameterized SQL; `SELECT *` on wide/sensitive paths; function-wrapped hot `WHERE`; JSONB via `::text LIKE`; deep `OFFSET` pagination |
| Secrets | Plaintext tokens/keys; durable data on `UNLOGGED` |
| Migrations | No down; `CONCURRENTLY` inside transactional migrate; unsafe live rewrite |

### Recommended (should fix)

| Area | Prefer… |
|------|---------|
| Shape | `{group}_{entity}`; timestamps + `extra`; `TEXT`+`CHECK` for status; typed cols over JSONB bags |
| Deletes | Soft for durable API entities; hard for junctions/sessions/tokens; purge plan for tombstones |
| Indexes | Partial live + keyset (soft); plain keyset (hard); leftmost-prefix match; drop unused; covering when proven |
| Queries | Keyset pagination; `EXISTS`/JOIN over bad subqueries; batch writes; no N+1; `EXPLAIN (ANALYZE, BUFFERS)` on hot paths |
| JSONB / FTS | GIN only when filtered; generated col + B-tree for hot keys; language-qualified FTS; omit `extra` from lists |
| App sync | sqlc Get by `uuid` / JOIN on `id`; `set_updated_at` + explicit `updated_at = now()`; app cleanup when soft parent has hard children |
| Ops | `COMMENT` delete mode; avoid volatile defaults on large `NOT NULL` adds; upsert ≠ partial unique; `pg_stat_statements` |

### Nits (optional polish)

| Area | Nice to have… |
|------|----------------|
| Naming | `idx_`/`uidx_`/`trg_` conventions; consistent `{entity}` pluralization |
| SQL style | Project-consistent `now()` vs `CURRENT_TIMESTAMP`; `BIGINT` default; half-open time predicates; `FILTER` aggregates |
| DX | `COMMENT ON` for non-obvious CHECKs/JSONB keys; Timescale current APIs not deprecated names |
| Perf polish | Covering `INCLUDE`, tighter partial predicates, tombstone admin index, `fillfactor` only when measured |
| Observability | Note to verify with EXPLAIN on realistic volume |

---

## Examples

Minimal patterns live in [examples.md](references/examples.md):

1. Soft-delete feature table (`iam_users`-style)
2. Hard-delete feature / session-style table
3. Junction table (hard delete) with composite UNIQUE + FK indexes
4. Append-only events table
5. JSONB with generated stored column + B-tree
6. TimescaleDB hypertable sketch (when enabled)
7. sqlc Get/Create/SoftDelete by `uuid`

---

## Design workflow

1. Pick mode from the thread ([modes.md](references/modes.md)). Vague persistence ask → [make-it-clear](../make-it-clear/SKILL.md) first.
2. Classify table from the conversation: **feature** | **junction** | **append-only/time-series**.
3. Choose **soft or hard delete** via [deletes.md](references/deletes.md); document it.
4. Feature → clone dual-key skeleton (`deleted_at` only if soft); junction → FKs + UNIQUE (usually hard); events → append-only or Timescale.
5. Pick types from the mapping; add `NOT NULL` / `DEFAULT` / `CHECK`. Multi-tenant → `tenant_id BIGINT`, not `tenant_uuid`.
6. Declare FKs with explicit `ON DELETE`/`ON UPDATE`; index every FK.
7. Indexes: soft → partial live-row + keyset; hard → plain UNIQUE + keyset.
8. Attach `set_updated_at` trigger if `updated_at` exists.
9. `COMMENT ON` non-obvious tables/columns (include delete mode).
10. Emit golang-migrate up/down pair ([migrations.md](references/migrations.md)); sqlc Get/List/Create by `uuid` ([sqlc.md](references/sqlc.md)).
11. If API-facing: same-PR OpenAPI + Bruno use **`uuid` only** — [bruno-openapi](../bruno-openapi/SKILL.md).
12. Verify against [do-dont.md](references/do-dont.md) and
    [review-checklist.md](references/review-checklist.md) (critical → recommended → nits).
