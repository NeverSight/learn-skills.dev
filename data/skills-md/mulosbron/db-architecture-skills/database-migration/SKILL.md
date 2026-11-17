---
name: database-migration
description: "Changing a live database schema safely: zero-downtime column renames and type changes, backfills, rollbacks, moving between databases or ORMs. Read before writing any migration against a database that has data."
---

# Database Migration

## Rules

- Every migration has a tested rollback, or an explicit note that it is irreversible and why.
- One logical change per migration. Small steps, deployed often.
- Never run a dev-mode command (`prisma migrate dev`, `drizzle-kit push`) against production.
- Back up or snapshot before anything that touches existing rows.
- Backfills run in batches (a few thousand rows per transaction), never as one UPDATE over the whole table.
- Migrations are idempotent where possible (`IF NOT EXISTS`, guarded backfills).

## Zero-downtime pattern: expand, migrate, contract

Any rename or type change while the app is running follows the same four deploys:

1. **Expand**: add the new column or table alongside the old one. Nullable or with a constant default.
2. **Dual-write**: deploy application code that writes both old and new. Backfill old rows in batches.
3. **Switch reads**: deploy code that reads from the new column. Verify parity.
4. **Contract**: drop the old column in a later migration, once no code references it.

Shortcuts that break this: `ALTER TABLE ... RENAME COLUMN` on a live table, changing a type in place, adding a `NOT NULL` column with a volatile default (table rewrite, see `skills/postgresql/SKILL.md`).

## Postgres specifics

- `CREATE INDEX CONCURRENTLY` for indexes on live tables; it cannot run inside a transaction, so isolate it in its own migration.
- Add constraints as `NOT VALID`, then `VALIDATE CONSTRAINT` separately to avoid a long exclusive lock.
- Set `lock_timeout` (a few seconds) in migration sessions so a blocked DDL fails fast instead of queueing behind traffic.

## Cross-database or cross-ORM moves

Map types explicitly before anything else (`BIGINT identity` vs `AUTO_INCREMENT`, `TIMESTAMPTZ` vs `DATETIME`, `JSONB` vs `JSON`, boolean vs tinyint). Verify row counts and checksums per table after the copy. Keep the old system readable until the new one has run a full business cycle.
