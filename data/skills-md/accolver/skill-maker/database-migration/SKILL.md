---
name: database-migration
description: Writes safe, reversible database migrations with rollback plans, data backup commands, zero-downtime deployment notes, and index impact analysis. Produces both up and down migration files with verification queries. Use when writing database migrations, schema changes, ALTER TABLE statements, adding indexes, or when the user needs to modify database structure.
---

# Database Migration

## Overview

Write safe, reversible database migrations that won't take down production.
Every migration gets a rollback plan, data backup commands, lock impact
analysis, verification queries, and a deployment runbook. The core principle:
**if you can't reverse it safely, don't ship it.**

## When to use

- When writing any database migration (schema change, ALTER TABLE, CREATE INDEX)
- When adding, removing, or modifying columns on production tables
- When renaming columns, tables, or constraints
- When adding or dropping indexes on large tables
- When the user says "migrate", "schema change", "alter table", or "add column"
- When modifying database structure that could affect running applications

**Do NOT use when:**

- Writing application queries (SELECT, INSERT, UPDATE for data operations)
- Designing a database schema from scratch (use a schema design skill)
- Performing data-only backfills with no schema change

## Workflow

### 1. Analyze the Schema Change

Before writing any SQL, understand the full impact:

- **What tables are affected?** Check row counts — a 100-row config table and a
  100M-row events table need completely different strategies.
- **What columns are involved?** Nullable vs NOT NULL, defaults, data types.
- **Who reads/writes this table?** Identify application code, background jobs,
  and reporting queries that touch the affected columns.
- **What database engine?** PostgreSQL, MySQL, and SQLite have different locking
  behaviors. Ask if not obvious.

Output: A brief impact summary stating table(s), estimated row count, and
affected consumers.

### 2. Assess Lock and Downtime Impact

Every ALTER TABLE acquires some form of lock. Classify the impact:

| Operation (PostgreSQL)                  | Lock Level         | Downtime Risk      |
| --------------------------------------- | ------------------ | ------------------ |
| ADD COLUMN (nullable, no default)       | ACCESS EXCLUSIVE   | Instant            |
| ADD COLUMN (with volatile default)      | ACCESS EXCLUSIVE   | **Blocks all**     |
| ADD COLUMN (with constant default, 11+) | ACCESS EXCLUSIVE   | Instant            |
| DROP COLUMN                             | ACCESS EXCLUSIVE   | Instant            |
| RENAME COLUMN                           | ACCESS EXCLUSIVE   | Instant            |
| ALTER COLUMN TYPE                       | ACCESS EXCLUSIVE   | **Rewrites table** |
| CREATE INDEX                            | SHARE lock         | **Blocks writes**  |
| CREATE INDEX CONCURRENTLY               | SHARE UPDATE EXCL. | Non-blocking       |
| ADD NOT NULL constraint                 | ACCESS EXCLUSIVE   | **Scans table**    |
| ADD CHECK constraint (NOT VALID)        | ACCESS EXCLUSIVE   | Instant            |
| VALIDATE CONSTRAINT                     | SHARE UPDATE EXCL. | Non-blocking       |

For MySQL, note that many ALTERs require a full table copy. Use
`pt-online-schema-change` or `gh-ost` for large tables.

Output: Lock classification and estimated duration for the table size.

### 3. Write the Up Migration

Write the forward migration SQL. Apply these safety rules:

- **Set a lock timeout** to avoid blocking the entire application:

  ```sql
  SET lock_timeout = '5s';
  ```

- **Use transactions** for DDL that supports it (PostgreSQL does, MySQL doesn't
  for most DDL).
- **Split large operations** into safe steps. Never combine a schema change with
  a large data backfill in the same transaction.
- **Add columns as nullable first**, then backfill, then add the NOT NULL
  constraint separately.
- **Create indexes concurrently** on large tables (PostgreSQL: `CONCURRENTLY`,
  MySQL: use online DDL or `gh-ost`).

Output: `migration.sql` — the up migration file.

### 4. Write the Down Migration (Rollback)

Every up migration MUST have a corresponding down migration. This is
non-negotiable.

- The rollback must undo the up migration completely.
- If the up migration added a column, the down drops it.
- If the up migration renamed a column, the down renames it back.
- If the up migration created an index, the down drops it.
- **Data loss warning**: If the rollback would lose data (e.g., dropping a
  column that was populated), document this explicitly.

Output: `rollback.sql` — the down migration file.

### 5. Add Data Backup Commands

Before any destructive or risky migration, provide backup commands:

```sql
-- Backup: full table snapshot
CREATE TABLE orders_backup_20260306 AS SELECT * FROM orders;

-- Backup: affected column only (for large tables)
CREATE TABLE orders_email_backup_20260306 AS
  SELECT id, email FROM orders;

-- Verify backup row count matches
SELECT
  (SELECT count(*) FROM orders) AS original,
  (SELECT count(*) FROM orders_backup_20260306) AS backup;
```

For very large tables, suggest `pg_dump` with table filtering instead of
`CREATE TABLE AS`.

Output: Backup commands included in the runbook.

### 6. Write Verification Queries

After the migration runs, how do you know it worked? Write queries that verify:

- **Schema is correct**: Column exists, has right type, right default, right
  constraints.
- **Data is intact**: Row counts match, no unexpected NULLs, values in expected
  range.
- **Application works**: Key queries still return expected results.

```sql
-- Verify column exists with correct type
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'orders' AND column_name = 'email';

-- Verify row count unchanged
SELECT count(*) FROM orders;

-- Verify no unexpected NULLs (after backfill)
SELECT count(*) FROM orders WHERE email IS NULL;
```

Output: Verification queries included in the runbook.

### 7. Create Deployment Runbook

Compile everything into a runbook that an on-call engineer can follow:

```markdown
## Migration Runbook: [description]

### Pre-flight

- [ ] Backup commands executed and verified
- [ ] Lock timeout set
- [ ] Off-peak deployment window confirmed
- [ ] Application code deployed (if dual-write needed)

### Execute

1. Run migration.sql
2. Verify with verification queries
3. Monitor error rates for 15 minutes

### Rollback (if needed)

1. Run rollback.sql
2. Verify rollback with verification queries
3. Restore from backup if data was lost

### Post-migration

- [ ] Remove old column/compatibility code (after soak period)
- [ ] Update documentation
- [ ] Close migration ticket
```

Output: `runbook.md` — the deployment runbook.

## Safety Checklist

Before considering any migration complete, verify:

- [ ] Up migration file written and tested
- [ ] Down migration (rollback) file written and tested
- [ ] Rollback reverses the up migration completely
- [ ] Data backup commands included
- [ ] Lock impact analyzed and documented
- [ ] Zero-downtime strategy confirmed (or downtime window documented)
- [ ] Verification queries written for post-migration checks
- [ ] Deployment runbook created with pre-flight, execute, rollback sections
- [ ] Large table operations use CONCURRENTLY or equivalent

## Common Migration Patterns

### Adding a non-nullable column with default (large table)

**Unsafe** — blocks reads and writes while rewriting the entire table:

```sql
ALTER TABLE orders ADD COLUMN status varchar(50) NOT NULL DEFAULT 'pending';
```

**Safe** — three-step approach:

```sql
-- Step 1: Add nullable column (instant, no rewrite)
ALTER TABLE orders ADD COLUMN status varchar(50);

-- Step 2: Backfill in batches (no lock held between batches)
UPDATE orders SET status = 'pending' WHERE status IS NULL AND id BETWEEN 1 AND 100000;
UPDATE orders SET status = 'pending' WHERE status IS NULL AND id BETWEEN 100001 AND 200000;
-- ... continue in batches

-- Step 3: Add NOT NULL constraint (after backfill complete)
ALTER TABLE orders ALTER COLUMN status SET NOT NULL;
ALTER TABLE orders ALTER COLUMN status SET DEFAULT 'pending';
```

### Renaming a column

**Unsafe** — breaks all application code instantly:

```sql
ALTER TABLE users RENAME COLUMN email TO email_address;
```

**Safe** — dual-write strategy:

```sql
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN email_address varchar(255);

-- Step 2: Backfill
UPDATE users SET email_address = email WHERE email_address IS NULL;

-- Step 3: Deploy app code that writes to BOTH columns
-- Step 4: Switch reads to new column
-- Step 5: Stop writing to old column
-- Step 6: Drop old column (in a later migration)
ALTER TABLE users DROP COLUMN email;
```

### Adding an index on a large table

**Unsafe** — blocks all writes for the duration:

```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

**Safe** — non-blocking:

```sql
CREATE INDEX CONCURRENTLY idx_orders_customer_id ON orders(customer_id);
```

Note: `CONCURRENTLY` cannot run inside a transaction. It takes longer but
doesn't block writes. For a 100M row table, expect 10-30 minutes depending on
hardware.

## Common Mistakes

| Mistake                                         | Fix                                                                                           |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------- |
| No rollback migration                           | Every up migration MUST have a down migration. No exceptions.                                 |
| No data backup commands                         | Include CREATE TABLE AS or pg_dump commands before destructive changes                        |
| Ignoring lock impact on large tables            | Always check row count and classify lock level before writing SQL                             |
| Using CREATE INDEX without CONCURRENTLY         | On tables > 1M rows, always use CONCURRENTLY (PostgreSQL) or online DDL                       |
| Adding NOT NULL column with default in one step | Split into: add nullable → backfill in batches → add constraint                               |
| Bare RENAME COLUMN in production                | Use dual-write strategy: add new → backfill → migrate reads → drop old                        |
| No verification queries                         | Write queries that confirm schema correctness and data integrity post-migration               |
| Missing deployment runbook                      | Create a step-by-step runbook with pre-flight, execute, rollback, and post-migration sections |
| Backfilling millions of rows in one UPDATE      | Batch updates (10k-100k rows per batch) to avoid long-running transactions                    |
| Running migrations during peak traffic          | Schedule for off-peak hours; set lock_timeout to fail fast if locks can't be acquired         |

## Key Principles

1. **Every migration must be reversible** — If you can't write a rollback that
   undoes the change, the migration is too risky. Restructure it into smaller,
   reversible steps. The only exception is dropping a column that was already
   emptied — and even then, document the data loss.

2. **Always include verification queries** — "It ran without errors" is not
   verification. Write queries that prove the schema is correct, data is intact,
   and the application still works. Run these after every migration AND after
   every rollback.

3. **Respect table size** — A migration that's instant on a 1,000-row dev table
   can lock production for 30 minutes on a 100M-row table. Always ask about row
   counts and adjust strategy accordingly. When in doubt, assume the table is
   large.

4. **Separate schema changes from data changes** — Never combine ALTER TABLE
   with a large UPDATE in the same transaction. Schema changes should be
   instant; data backfills should be batched. This prevents long-held locks and
   makes rollback simpler.

5. **Fail fast, don't block** — Set `lock_timeout` so migrations fail quickly if
   they can't acquire locks, rather than blocking all application queries while
   waiting. A failed migration you can retry is better than a blocked
   application.
