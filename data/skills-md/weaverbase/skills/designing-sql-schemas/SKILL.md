---
name: designing-sql-schemas
description: Use when writing or changing SQL schemas, table definitions, migrations, or queries, choosing PostgreSQL column types for JSON or timestamps, running database queries through an ORM or driver in an async app, building SQL from user input, or planning DROP, TRUNCATE, column removal, type changes, or bulk deletes.
---

# Designing SQL Schemas

## Overview

Choose database types and access patterns that preserve correctness, schema history, and async performance.

**Core principle:** Schema and data changes are hard to undo. Use types that preserve correctness, change applied schema only through new migrations, and obtain clear approval before destructive changes.

These rules apply to new or requested changes. Do not rewrite existing working schemas or queries solely to match them.

## When to Use

- Defining or altering tables, columns, or indexes.
- Writing or editing migration files.
- Choosing a PostgreSQL type for JSON data or timestamps.
- Writing queries with an ORM or database client inside an async API, worker, or event loop.
- Building a query that includes user-supplied values.
- Planning a change that could delete or reshape existing data.

## Quick Reference

| Topic | Do | Do not |
| --- | --- | --- |
| JSON columns (PostgreSQL) | `JSONB` | `JSON`, unless a specific compatibility constraint requires it |
| Timestamps that identify instants (PostgreSQL) | `TIMESTAMPTZ` | Timezone-less `TIMESTAMP` for an instant |
| Async apps | Async ORM methods and async database clients | Synchronous queries that block request handlers, workers, or event loops |
| Applied migrations | Add a new migration to change the schema | Edit or rewrite a migration that has already been applied |
| Destructive changes | Confirm the affected data and approved scope before dropping, truncating, or irreversibly rewriting | Run or write an unapproved destructive change on your own judgment |
| User-supplied values in SQL | Parameterized queries or ORM bindings | String-built SQL (concatenation, f-strings, template literals) |

## PostgreSQL types

### JSON

Use `JSONB` for JSON data in PostgreSQL. Avoid `JSON` unless a specific compatibility constraint requires it.

Good:

```sql
metadata JSONB NOT NULL DEFAULT '{}'::jsonb
```

Bad:

```sql
metadata JSON NOT NULL DEFAULT '{}'
```

### Timestamps

Use `TIMESTAMPTZ` for timestamps that identify instants, such as creation and expiration times. A local wall-clock value or schedule may deliberately use `TIMESTAMP` without time zone; define its timezone interpretation separately rather than treating it as an instant.

Good:

```sql
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
```

Bad:

```sql
created_at TIMESTAMP NOT NULL DEFAULT now()
```

## Async ORM and database queries

Use async ORM methods and async database clients in async applications, such as SQLAlchemy 2.0 async APIs or Prisma async calls. Avoid synchronous queries that block async request handlers, workers, or event loops. A handler that makes "only one" blocking call is still an event-loop hazard.

Good:

```python
async def get_order(session: AsyncSession, order_id: UUID) -> Order | None:
    result = await session.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()
```

Bad: a synchronous driver call inside an `async def` handler.

```python
async def get_order(order_id: UUID):
    with sync_engine.connect() as conn:  # blocks the event loop
        return conn.execute(text("SELECT * FROM orders WHERE id = :id"), {"id": order_id}).first()
```

## Migrations

- Add a new migration to change the schema. Never edit a migration that has already been applied: other environments have already run the old version and will silently diverge.
- Each migration should be a small, reviewable step. Do not combine unrelated schema changes in one file.
- If a previous migration was wrong, fix it forward with a new migration.

## Destructive changes

Before a schema or data change that could destroy data, confirm the affected data and approved scope: `DROP TABLE`, `DROP COLUMN`, `TRUNCATE`, `DELETE` or `UPDATE` without a narrow `WHERE`, narrowing a column type, or adding a constraint that existing rows may violate. Stop and report options if the consequences are unclear or not already approved. Also stop for unrequested or unclear database contract changes (renaming a column, changing a type). State what would be lost or broken, and propose a safer path such as an additive migration, a backfill, or a backup. Clear, specific approval in the task is sufficient; it does not authorize executing a destructive migration against an unspecified environment.

## Parameterized SQL

Pass user-supplied and other untrusted values as bound parameters, never by building SQL text from strings. Table and column names cannot be bound; pick them from a fixed allowlist in code.

Good:

```python
await session.execute(
    text("SELECT id, status FROM orders WHERE customer_id = :customer_id"),
    {"customer_id": customer_id},
)
```

Bad:

```python
await session.execute(text(f"SELECT id, status FROM orders WHERE customer_id = '{customer_id}'"))
```

## Common Mistakes

- Choosing `JSON` or timezone-less `TIMESTAMP` because it is "close enough", without a concrete compatibility reason.
- Using a synchronous database driver or blocking ORM call inside an async API or worker.
- Editing an applied migration instead of adding a new one.
- Writing a destructive migration, or running a bulk delete, without stopping to report what it would remove.
- Building SQL strings from request values.
- Assuming a user-supplied identifier (table, column, sort field) can be bound as a parameter instead of checking it against an allowlist.

## Red Flags

Stop and use the compliant form if you think:

- "Use PostgreSQL `JSON` or `TIMESTAMP` because it is close enough."
- "Use a synchronous database driver inside an async API or worker."
- "Just edit the old migration, it is only a small fix."
- "The drop is obviously safe, so no need to flag it."
- "The value comes from our own UI, so concatenating it into the query is fine."

| Rationalization | Response |
| --- | --- |
| "This async endpoint only does one blocking call." | Blocking calls in async paths are still event-loop hazards. Use async drivers and async ORM/database APIs. |
| "`TIMESTAMP` is close enough to `TIMESTAMPTZ`." | A timezone-less timestamp does not identify an instant on its own. Use `TIMESTAMPTZ` for instants unless a concrete constraint requires otherwise; it stores the instant, not the original timezone or offset. |
| "The legacy syntax still works, so it is fine." | Working code is not the same as current convention. Use modern database practices unless a real constraint requires otherwise. |
