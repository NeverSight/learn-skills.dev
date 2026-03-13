---
name: prisma-expand-contract
description: Safe database schema migrations using the expand-and-contract pattern with Prisma ORM. Use when renaming columns/tables, changing column types, adding non-nullable columns, or any schema change requiring zero-downtime deployment.
---

# Prisma Expand-and-Contract Migrations

Safe, zero-downtime database schema changes with Prisma ORM.

## When to Use

- Renaming columns or tables in production
- Changing column types (e.g., `String` to `Enum`)
- Adding non-nullable columns to tables with existing data
- Splitting or merging tables
- Any schema change that could break running instances during deployment

## The Pattern

Split destructive changes into three phases across multiple deployments:

```
EXPAND              MIGRATE             CONTRACT
Add new structure → Copy data,       → Remove old structure
                    update code
    Deploy 1          Deploy 2            Deploy 3
```

**Why:** During deployment, old and new application versions run simultaneously. Direct renames or type changes break old instances immediately.

## Core Principles

1. **Never remove in the same deploy as you add** - Old code must continue working
2. **Make changes additive first** - Add new columns/tables before removing old
3. **Code handles both states** - During transition, read from new, write to both
4. **Data migration between deploys** - Not during schema migration
5. **Cleanup is separate** - Remove old structures only after all code uses new

## Prisma Tools for Renames

### @map (Column-Level)

Maps Prisma field to different database column:

```prisma
model User {
  displayName String @map("user_name") // Prisma: displayName, DB: user_name
}
```

### @@map (Table-Level)

Maps Prisma model to different database table:

```prisma
model Account {
  id String @id
  @@map("users") // Prisma: Account, DB: users
}
```

**Note:** `@map`/`@@map` only work for code-level renames. For actual data migration, use full expand-and-contract.

### @default (Safe Non-Nullable Addition)

For new columns where a default makes sense:

```prisma
model User {
  createdAt DateTime @default(now())  // Safe to add directly
  isActive  Boolean  @default(true)   // Safe to add directly
}
```

## Common Scenarios

| Scenario | Approach |
|----------|----------|
| Rename column | Add new → backfill → make required → remove old |
| Change type (String→Enum) | Add enum column → backfill mapping → switch reads → remove string |
| Add non-nullable column | Add nullable → backfill → make required |
| Rename table | Create new table → copy data → migrate code → drop old |
| Split table | Add related table → copy data → update code → remove old fields |

For detailed step-by-step implementations, see [SCENARIOS.md](SCENARIOS.md).

## Anti-Patterns

### Direct Column Rename
```prisma
// DON'T: Breaks running instances immediately
model User {
  displayName String // Was: userName
}
```

### Remove and Add in Same Migration
```prisma
// DON'T: Old code fails during deployment
model User {
  // Removed: userName
  displayName String // Added
}
```

### migrate dev in Production
```bash
# DON'T: Can cause data loss
npx prisma migrate dev

# DO: Use migrate deploy
npx prisma migrate deploy
```

### Non-Nullable Without Backfill
```prisma
// DON'T: Migration fails if nulls exist
model User {
  email String // Changed from String?
}
```

## Quick Reference

```bash
npx prisma migrate dev --name name    # Development: create + apply
npx prisma migrate deploy             # Production: apply pending
npx prisma migrate status             # View migration status
```

For deployment checklists and rollback strategies, see [CHECKLISTS.md](CHECKLISTS.md).

## Additional Resources

- [Prisma Expand and Contract Pattern](https://www.prisma.io/dataguide/types/relational/expand-and-contract-pattern)
- [Prisma Production Deployment](https://www.prisma.io/docs/guides/deployment/deploy-database-changes-with-prisma-migrate)
