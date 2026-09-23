---
name: drizzle
description: "Drizzle ORM — lightweight, TypeScript-first SQL ORM with schema-as-code and zero-dependency query builder. Use when building with Drizzle ORM or asking about its schema definition, migrations, query builder, relations, or integration with databases like PostgreSQL, MySQL, or SQLite. Fetch live documentation for up-to-date details."
---

# Drizzle ORM

> **CRITICAL: Your training data for Drizzle ORM is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs:
>
> **`WebFetch("https://orm.drizzle.team/llms.txt")`**
>
> Do not proceed without fetching this URL first. Never assume an API or config option exists — verify against current docs.

Drizzle ORM is a lightweight, TypeScript-first ORM with a SQL-like query builder, schema-as-code migrations, and zero dependencies.
## Key Capabilities

**Built-in schema validation adapters** — Drizzle includes first-party integrations with Zod, Valibot, TypeBox, ArkType, and Effect Schema via `drizzle-zod`, `drizzle-valibot`, etc. There is no need to manually write validation schemas that mirror your table definitions; these packages infer insert/select types directly from your Drizzle schema.

**Built-in seeding** — `drizzle-seed` provides deterministic, reproducible fake data generation with seedable PRNG, weighted distributions, and cross-dialect support. It replaces ad-hoc seed scripts or external packages like `@faker-js/faker` for database seeding workflows.


## Best Practices

**Call `.$dynamic()` to compose queries across functions.** By default, Drizzle query builders restrict each clause method (where, limit, orderBy) to a single call — this mirrors SQL but breaks composable helper functions. You must call `.$dynamic()` to unlock multi-call mode. Use the dialect-specific generic types (`PgSelect`, `MySqlSelect`, `SQLiteSelect`) as parameter types for functions that accept a query builder to extend.

**Relational queries (`db.query.*`) generate exactly one SQL statement — nested `offset` is not supported.** Unlike Prisma's batched-query approach, Drizzle uses a single lateral-join query per `db.query` call. A consequence is that `offset` only works at the top level of a relational query; nested relation pagination must use `where` with cursor-based logic instead.

**Use `drizzle-kit push` only for development, never production.** `drizzle-kit push` applies schema changes directly without generating migration files. Teams that use push in production lose the auditable migration history needed for `drizzle-kit migrate` in CI/CD. Use `drizzle-kit generate` + `drizzle-kit migrate` for production deployments.

**Never instantiate `drizzle()` per request in serverless environments.** Each call can open a new connection pool. Export a module-level singleton and re-use it across invocations, following the same pattern as Prisma's `PrismaClient` singleton pattern.

**`drizzle-kit pull` and `push` do not preserve hand-written SQL in migration files.** If you manually edit a generated migration file (e.g., to add a partial index or a custom trigger), subsequent `pull` operations will overwrite those edits. Track custom migrations in separate numbered files and apply them alongside generated ones.

**`db.query.*` relational queries require explicit `relations()` definitions.** Unlike Prisma, Drizzle does not infer relations from foreign keys automatically. If you call `db.query.users.findMany({ with: { posts: true } })` without a `relations()` export in the schema file, the query throws at runtime with a non-obvious error. Define relations explicitly for every table you want to query relationally.
