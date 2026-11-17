---
name: database-design
description: "Schema modeling and schema review: tables, keys, relationships, constraints, indexes, normalization. Use when designing a new schema or auditing an existing one for integrity and performance problems."
---

# Database Design

## Audit checklist (existing schema)

Go through every table. Report each finding with table, column, impact, fix.

- **Primary keys**: every entity table has one. `BIGINT identity` by default; UUID only when IDs must be opaque or generated client-side.
- **Foreign keys**: every reference is a real FK constraint, not just a column named `*_id`. FK columns are indexed (Postgres does not do this automatically).
- **NOT NULL**: applied wherever the domain requires a value. Nullable columns that are never null in practice are a smell.
- **UNIQUE / CHECK**: business rules (one email per user, status in a fixed set, quantity > 0) live in the database, not only in application code.
- **Indexes**: exist for frequent filters, sorts, joins. Flag unused or duplicate indexes (they slow writes).
- **Types**: money is `NUMERIC`, timestamps carry a time zone, strings are `TEXT` not `VARCHAR(255)` by habit.
- **JSON columns**: holding data that is actually structured and queried. Pull it into columns.
- **Soft deletes, audit columns, tenant_id**: present and consistent if the app needs them; indexed if filtered on.
- **N+1 risk**: ORM relations loaded in loops. Check query logs or ORM `include` usage.

## Design order (new schema)

1. List the entities and the questions the app will ask (access patterns).
2. Normalize to 3NF.
3. Add constraints immediately, not "later".
4. Index for the access patterns from step 1 and every FK.
5. Write the first migration. Denormalize only after measuring.

## Do not

- Default to PostgreSQL without asking; SQLite may be enough.
- Use `SELECT *` in application code.
- Store relations as arrays or comma-separated strings when a junction table is needed.
