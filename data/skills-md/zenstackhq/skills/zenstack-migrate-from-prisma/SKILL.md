---
name: zenstack-migrate-from-prisma
description: Migrate an existing Prisma project to ZenStack V3. Use when replacing Prisma/@prisma/client with ZenStack, converting schema.prisma to ZModel, swapping PrismaClient for ZenStackClient, updating generate/migrate scripts, mapping Prisma custom generators and client extensions, or keeping Prisma migrate tooling working.
---

# Migrating from Prisma to ZenStack V3

ZenStack V3 is designed as a drop-in upgrade path for Prisma: it keeps a Prisma-compatible query API
and a schema language (ZModel) that is a superset of the Prisma schema. Most apps migrate with
mechanical changes and no query rewrites. Supported databases: **PostgreSQL, MySQL, SQLite**.

For general setup/CLI details see `zenstack-project-setup`; for the client/dialect see
`zenstack-querying`; for schema syntax see `zenstack-schema-modeling`.

## At a glance

| Prisma | ZenStack V3 |
| ------ | ----------- |
| `prisma`, `@prisma/client` | `@zenstackhq/cli` (dev), `@zenstackhq/schema`, `@zenstackhq/orm` |
| `schema.prisma` | `zenstack/schema.zmodel` (Prisma schema is valid ZModel) |
| `prisma generate` | `zen generate` |
| `prisma db push` / `migrate dev` / `migrate deploy` | `zen db push` / `zen migrate dev` / `zen migrate deploy` |
| `new PrismaClient()` | `new ZenStackClient(schema, { dialect })` |
| bundled DB engine | you install a DB driver (`pg` / `mysql2` / `better-sqlite3`) |

## Step 1 — Swap dependencies

```bash
npm uninstall prisma @prisma/client
npm install @zenstackhq/schema @zenstackhq/orm
npm install --save-dev @zenstackhq/cli
```

ZenStack does **not** bundle a database engine — install the driver for your database:

| Database   | Install |
| ---------- | ------- |
| PostgreSQL | `npm install pg` + `npm install -D @types/pg` |
| MySQL      | `npm install mysql2` |
| SQLite     | `npm install better-sqlite3` + `npm install -D @types/better-sqlite3` |

> `@zenstackhq/cli` has a peer dependency on `prisma`, which is installed automatically when needed
> for migration commands (ZenStack's migrate commands wrap Prisma Migrate).

## Step 2 — Move and rename the schema

Move `schema.prisma` → `zenstack/schema.zmodel`. **No edits are required** — every valid Prisma
schema is valid ZModel. Optional cleanup:

- Drop the `generator client { ... }` block (no effect in ZenStack — code gen is driven by
  `zen generate`).
- The `datasource` block is kept; its `url` is used by the migration engine (the ORM runtime gets
  its connection from the driver/dialect instead).
- If you used Prisma's multi-file/multi-schema feature, merge files using ZModel `import`
  statements.

Run **`zen check`** to confirm the converted schema is valid (syntax + semantics) before moving on.

Once moved, you can start adding ZenStack-only features that Prisma lacks — access policies
(`zenstack-access-control`), `@@delegate` polymorphism, typed JSON, mixins, computed fields
(`zenstack-schema-modeling`).

## Step 3 — Update the generate script

```json
{ "scripts": { "generate": "zen generate" } }
```

Run `zen generate` after every schema change, before using the client.

## Step 4 — Replace the client

Swap `new PrismaClient()` for `new ZenStackClient(schema, { dialect })`, supplying a Kysely dialect
for your driver (see `zenstack-querying` for all dialects). PostgreSQL example:

```ts
import { ZenStackClient } from '@zenstackhq/orm';
import { PostgresDialect } from '@zenstackhq/orm/dialects/postgres';
import { schema } from './zenstack/schema';
import { Pool } from 'pg';

export const db = new ZenStackClient(schema, {
    dialect: new PostgresDialect({
        pool: new Pool({ connectionString: process.env.DATABASE_URL }),
    }),
});
```

Your existing `findMany`/`create`/`update`/etc. calls keep working — the ORM API is
Prisma-compatible.

## Step 5 — Update type references

- Model types (e.g. `User`) — import from the generated `models`.
- Input/argument types (e.g. `UserCreateArgs`) — import from the generated `input`.

Most code relies on inferred types and needs no explicit imports.

## Step 6 — Update migration scripts

```json
{
  "scripts": {
    "db:push": "zen db push",
    "migrate:dev": "zen migrate dev",
    "migrate:deploy": "zen migrate deploy"
  }
}
```

Move your existing migration history from `prisma/migrations` to `zenstack/migrations` (ZenStack's
default location, next to `zenstack/schema.zmodel`). It continues to work unchanged since ZenStack
migrate wraps Prisma Migrate. See the `zenstack-db-migration` skill for the full migration workflow.

## Special case — Prisma custom generators

If you depend on Prisma custom generators (e.g. zod, ERD, type generators) that read a
`schema.prisma`, keep emitting one with the `@core/prisma` plugin and chain the commands:

```zmodel
plugin prisma {
    provider = '@core/prisma'
    output = './schema.prisma'
}
```

```json
{ "scripts": { "generate": "zen generate && prisma generate --schema=zenstack/schema.prisma" } }
```

## Mapping Prisma Client extensions

| Prisma extension | ZenStack equivalent |
| ---------------- | ------------------- |
| **Query** extension (intercept calls) | A runtime plugin via `db.$use(...)` with an `onQuery` hook |
| **Result** extension (computed fields) | `@computed` field in ZModel + the `computedFields` option on `ZenStackClient` (see `zenstack-schema-modeling`) |

## After migrating

Verify with: `zen generate` → typecheck → run your test suite / app. Then incrementally adopt
ZenStack's value-add features (access control, query builder escape hatch, auto CRUD APIs via
`zenstack-crud-server`).

> Already on **ZenStack V2**? Start here (V2 was Prisma-based), then apply the V2→V3 deltas in
> `zenstack-project-setup` (package renames, policy plugin, `post-update`/`before()`, types+mixins,
> grouped hooks).

## Reference docs

Full ZenStack documentation for this topic is bundled under [`references/`](references/):

- [migrate-prisma.md](references/migrate-prisma.md) — official "Migrating from Prisma" guide
