---
name: prisma-expert
description: "Prisma ORM: schema.prisma review, migrations, query patterns, connection pooling. Read when the project contains schema.prisma."
---

# Prisma

First read `prisma/schema.prisma`, `prisma/migrations/`, and check the provider and Prisma version in `package.json`. Combine with `skills/postgresql/SKILL.md` when the provider is Postgres.

## Rules

- `prisma migrate dev` is for local development only. Production runs `prisma migrate deploy`. Never `migrate reset` on anything shared.
- Every relation declares `onDelete` explicitly. Prisma's default is not always what the domain wants.
- Add `@@index` for every field used in `where` or `orderBy` that is not already `@id` or `@unique`. Prisma does not index relation scalar fields automatically.
- Use `select` to fetch only needed fields; `include` only the relations the caller uses. Deep `include` trees are the usual N+1 and over-fetch source.
- Paginate every list query (`take` + cursor). No unbounded `findMany`.
- Serverless or edge: a pooler (Prisma Accelerate, PgBouncer, Neon pooler) is mandatory; set `connection_limit` in the URL to a small number per instance.
- Inside `$transaction`, no external API calls and no long computation. Keep it short to avoid lock contention.
- Explicit join tables for many-to-many that need extra columns or indexes; implicit `@relation` only for the trivial case.
- `@@map` / `@map` to keep `snake_case` in the database while using camelCase in code.

## Audit checklist for an existing schema.prisma

- Models without `@id`, relations without `fields`/`references`, missing `onDelete`.
- Filtered fields without `@@index`; composite queries without composite indexes.
- `String` columns that should be `Decimal` (money) or `DateTime` with `@db.Timestamptz`.
- `Json` fields holding structured, queried data.
- `findMany` calls in loops or without `take` in the codebase.
