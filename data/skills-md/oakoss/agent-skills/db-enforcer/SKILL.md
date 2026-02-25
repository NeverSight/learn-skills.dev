---
name: db-enforcer
description: 'Enforces database integrity for PostgreSQL and Prisma systems. Use when designing schemas, writing migrations, or configuring Row-Level Security. Use for type-safe SQL, naming alignment, constraint validation, zero-trust RLS policies, UUIDv7 primary keys, and zero-downtime deployments.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# DB Enforcer

## Overview

Enforces data integrity and architectural consistency between the TypeScript application layer and the PostgreSQL persistence layer. Prevents type drift by ensuring CHECK constraints mirror TypeScript types, migrations are generated before applying changes, and Row-Level Security protects every table.

**When to use:** Schema design, migration planning, RLS policy authoring, Prisma model mapping, constraint auditing, zero-downtime deployments.

**When NOT to use:** Application-level business logic, frontend state management, non-PostgreSQL databases. For full RLS auditing, performance tuning, and compliance validation, use the `database-security` skill instead.

## Quick Reference

| Pattern               | API/Tool                            | Key Points                                           |
| --------------------- | ----------------------------------- | ---------------------------------------------------- |
| Type-to-DB sync       | `prisma migrate dev --create-only`  | Generate SQL before applying changes                 |
| Naming alignment      | `@map` / `@@map`                    | snake_case in SQL, camelCase in TS                   |
| Primary keys          | `DEFAULT uuidv7()`                  | Sequential, globally unique, fast indexing (PG 18+)  |
| Virtual columns       | `GENERATED ALWAYS AS (...) VIRTUAL` | Zero disk cost, computed on read (PG 18+)            |
| Temporal uniqueness   | `EXCLUDE USING gist`                | Prevent overlapping ranges natively                  |
| NOT VALID constraints | `ADD CONSTRAINT ... NOT VALID`      | Add constraints without table locks                  |
| TypedSQL              | `prisma.$queryRawTyped()`           | Type-safe raw SQL via `.sql` files                   |
| Relation emulation    | `relationMode = "prisma"`           | Integrity in FK-less environments (GA since 4.8.0)   |
| Soft deletes          | Prisma `$extends`                   | Cross-cutting concern via client extensions          |
| RLS standard          | `(select auth.uid()) = user_id`     | Default own-data access policy with initPlan caching |
| Team RLS              | `EXISTS` subquery                   | Permission checks via join tables                    |
| Column-level security | PostgreSQL Views                    | Hide sensitive columns from public APIs              |

## Synchronization Protocol

Every schema modification MUST follow these steps:

1. **Type-to-DB Verification**: When adding an enum or union in TS, verify the equivalent CHECK constraint in SQL
2. **Migration-First Generation**: Generate SQL migrations using `prisma migrate dev --create-only` BEFORE applying
3. **Naming Alignment**: Enforce snake_case in SQL and camelCase in TS via explicit `@map`/`@@map` directives
4. **Integrity Audit**: Run `prisma validate` and check for missing indices on relation scalars
5. **RLS Verification**: Confirm every new table has RLS enabled with appropriate policies
6. **Lock Assessment**: Evaluate whether migration requires `CREATE INDEX CONCURRENTLY` or `NOT VALID` patterns

## PostgreSQL Version Requirements

Several patterns in this skill require specific PostgreSQL versions:

| Feature            | Minimum Version | Fallback                                      |
| ------------------ | --------------- | --------------------------------------------- |
| `uuidv7()`         | PostgreSQL 18   | `gen_random_uuid()` (UUIDv4) via `pgcrypto`   |
| Virtual columns    | PostgreSQL 18   | `STORED` generated columns (PG 12+)           |
| `EXCLUDE USING`    | PostgreSQL 9.0  | Application-level overlap checks              |
| `NOT VALID`        | PostgreSQL 9.1  | Schedule constraint addition during downtime  |
| `security_invoker` | PostgreSQL 15   | Use `security_definer` with restricted grants |

## Common Mistakes

| Mistake                                                  | Correct Pattern                                                                       |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Running SQL changes manually without migrations          | Generate numbered migrations with `prisma migrate dev --create-only` before applying  |
| Using auto-increment or raw IDs exposed in URLs          | Use UUIDv7 for globally unique, non-enumerable identifiers                            |
| Skipping CHECK constraints on enums or unions            | Add database-level CHECK constraints that mirror TypeScript types                     |
| Mixing snake_case and camelCase without explicit mapping | Use `@map` and `@@map` to enforce snake_case in SQL and camelCase in TypeScript       |
| Tables without Row-Level Security policies               | Apply RLS policies to every table, defaulting to `(select auth.uid()) = user_id`      |
| DROP or RENAME column in a single deployment             | Use expand-and-contract: add new column, dual-write, backfill, switch reads, drop old |
| Adding NOT NULL to large tables with full lock           | Add column as NULL first, backfill, then add NOT NULL with NOT VALID                  |
| Creating indices without CONCURRENTLY                    | Use `CREATE INDEX CONCURRENTLY` in raw SQL migrations to avoid table locks            |
| Using `auth.uid()` directly in RLS without subselect     | Wrap in `(select auth.uid())` to trigger initPlan caching                             |
| Assuming `uuidv7()` works on all PG versions             | Verify PostgreSQL 18+; fall back to `gen_random_uuid()` on older versions             |

## Naming Conventions

Prisma models use camelCase in TypeScript and must map to snake_case in PostgreSQL:

| Layer      | Convention  | Enforced By              |
| ---------- | ----------- | ------------------------ |
| TypeScript | camelCase   | Prisma model field names |
| PostgreSQL | snake_case  | `@map` / `@@map`         |
| Enums      | UPPER_SNAKE | CHECK constraints        |
| Indices    | snake_case  | `idx_table_column`       |

## Deployment Pipeline

Migrations follow a strict pipeline order:

1. `prisma migrate dev --create-only` -- generate and review SQL locally
2. `prisma validate` -- verify schema consistency
3. Apply to staging/preview database and run integration tests
4. `prisma migrate deploy` -- apply in CI/CD pipeline to production
5. Monitor for lock contention and query plan regressions

## Relationship to Other Skills

- **`database-security`**: Covers full RLS auditing, PGAudit configuration, Supabase-specific patterns, Convex auth guards, and compliance validation. Use `database-security` for in-depth policy review and access simulation. Use `db-enforcer` for schema design and migration patterns that include RLS as part of the integrity workflow.

## Delegation

- **Audit existing schema for missing constraints or indices**: Use `Explore` agent
- **Plan a zero-downtime migration strategy for production databases**: Use `Plan` agent
- **Execute a full schema refactor with type alignment and RLS setup**: Use `Task` agent
- **Review RLS policies for bypasses and performance issues**: Use `database-security` skill

## References

- [PostgreSQL integrity patterns, UUIDv7, virtual columns, and temporal constraints](references/postgres-integrity.md)
- [Prisma architecture, TypedSQL, extensions, and edge-first patterns](references/prisma-architecture.md)
- [Migration safety protocols, destructive changes, and rollback strategies](references/migration-safety.md)
- [Row-Level Security, column-level security, and audit logging](references/rls-security.md)
