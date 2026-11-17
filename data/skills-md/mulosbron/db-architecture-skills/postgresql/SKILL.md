---
name: postgresql
description: "PostgreSQL table design: type choices, PG-specific traps, constraints, index types, partitioning, JSONB. Read when writing or reviewing any Postgres schema, including through Prisma or Drizzle."
---

# PostgreSQL Table Design

## Core rules

- Primary key for every entity table: `BIGINT GENERATED ALWAYS AS IDENTITY`. UUID only when IDs must be opaque, client-generated or merged across systems; then `uuidv7()` (PG18+) or `gen_random_uuid()`. Append-only event/log tables may skip a PK.
- Normalize to 3NF first. Denormalize only for a measured, specific read path.
- `NOT NULL` wherever the domain requires a value. Defaults for common values.
- Index what you query: FK columns (not automatic!), frequent filters, sorts, join keys.

## Traps the model keeps falling into

- **Unquoted identifiers are lowercased.** Use `snake_case`; never quoted mixed-case names.
- **UNIQUE allows multiple NULLs.** Use `UNIQUE (...) NULLS NOT DISTINCT` (PG15+) when one NULL is the limit.
- **FK columns are not indexed automatically.** Add the index; it also prevents lock pile-ups on parent deletes.
- **CHECK passes NULL.** `CHECK (price > 0)` allows a NULL price. Pair with `NOT NULL`.
- **No silent coercion.** Overflowing `NUMERIC(2,0)` errors instead of rounding.
- **Sequences have gaps.** Normal. Do not try to make IDs consecutive.
- **Heap storage, no clustered index.** Row order on disk is insertion order; `CLUSTER` is one-off.
- **MVCC bloat.** Updates leave dead tuples. Avoid hot wide-row churn; split hot columns into their own table, use `fillfactor=90`.
- **Adding a NOT NULL column with a volatile default (`now()`, `gen_random_uuid()`) rewrites the table.** Constant defaults are instant.
- **`CREATE INDEX CONCURRENTLY` cannot run inside a transaction.**
- **Partitioned tables: no global UNIQUE.** The partition key must be part of every PK/UNIQUE.
- **Upsert needs an exact-matching UNIQUE index** on the `ON CONFLICT` target. Partial indexes do not qualify.

## Types

| Use | Type | Never |
|---|---|---|
| IDs | `BIGINT GENERATED ALWAYS AS IDENTITY` | `SERIAL` |
| Integers | `BIGINT` (or `INTEGER` when range is known) | |
| Money | `NUMERIC(p,s)` | `MONEY`, `REAL`, `DOUBLE PRECISION` |
| Strings | `TEXT` + `CHECK (length(col) <= n)` if a limit is needed | `VARCHAR(n)`, `CHAR(n)` |
| Timestamps | `TIMESTAMPTZ` | `TIMESTAMP`, `TIMETZ`, `TIMESTAMPTZ(0)` |
| Dates / durations | `DATE`, `INTERVAL` | |
| Booleans | `BOOLEAN NOT NULL` | nullable boolean unless tri-state is intended |
| Fixed small sets | `ENUM` only for truly stable sets (weekdays). Business statuses: `TEXT` + `CHECK` or lookup table | |
| Semi-structured | `JSONB` | `JSON` (only if key order must be preserved) |
| Tags, small lists | `TEXT[]` with GIN; junction table when it is really a relation | |
| Ranges / scheduling | `tstzrange`, `daterange` with GiST; `[)` bounds by default | |
| Case-insensitive match | expression index on `LOWER(col)`; `CITEXT` only for case-insensitive PK/UNIQUE | |
| Full-text | `TSVECTOR` with GIN; always pass the language: `to_tsvector('english', col)` | one-argument `to_tsvector` |
| Embeddings | `vector` (pgvector) | |

## Constraints

- FK: always state `ON DELETE` (`CASCADE`, `RESTRICT`, `SET NULL`). `DEFERRABLE INITIALLY DEFERRED` for circular references.
- `EXCLUDE USING gist (room_id WITH =, period WITH &&)` prevents double booking; CHECK cannot.
- Reusable validation: `CREATE DOMAIN email AS TEXT CHECK (VALUE ~ '^[^@]+@[^@]+$')`.
- Computed, indexable fields: `GENERATED ALWAYS AS (expr) STORED`.

## Indexes

- **B-tree** default. Composite: leftmost prefix rule; equality columns first, then range.
- **Covering**: `INCLUDE (cols)` for index-only scans.
- **Partial**: `WHERE status = 'active'` for hot subsets.
- **Expression**: `(LOWER(email))`; the query must use the identical expression.
- **GIN**: JSONB, arrays, full-text. **GiST**: ranges, geometry, exclusion. **BRIN**: huge append-only tables ordered by time.
- Insert-heavy tables: fewest indexes possible, `COPY` or multi-row INSERT, `UNLOGGED` for rebuildable staging.

## Partitioning

Only for very large tables (>100M rows) where queries filter on the partition key, or where whole partitions are dropped on a schedule. `RANGE` for time, `LIST` for discrete regions, `HASH` when no natural key. Declarative partitioning only; never inheritance. TimescaleDB automates time partitioning, retention and compression.

## JSONB

- Keep core relations in columns; JSONB holds optional or variable attributes.
- Default index: `CREATE INDEX ON t USING GIN (doc)`. Containment-only workloads: `GIN (doc jsonb_path_ops)` is smaller but loses `?` key-existence support.
- Equality or range on one scalar field: promote it to a generated column with a B-tree index instead of indexing the expression in queries.
- Constrain the shape: `CHECK (jsonb_typeof(doc) = 'object')`.

## Extensions worth suggesting

`pg_trgm` (fuzzy `LIKE '%x%'`), `pgvector`, `timescaledb`, `postgis`, `pgcrypto` (password hashing), `pgaudit`. Prefer `pgcrypto` over `uuid-ossp`.
