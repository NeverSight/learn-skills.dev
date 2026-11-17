---
name: drizzle-orm-expert
description: "Drizzle ORM: schema.ts review, drizzle-kit migration workflow, relational queries, serverless drivers. Read when the project contains drizzle.config.ts."
---

# Drizzle ORM

First read `drizzle.config.ts`, the schema files it points to, and the `drizzle/` migrations folder. Combine with `skills/postgresql/SKILL.md` for the Postgres dialect.

## Rules

- `drizzle-kit push` is for local development only; it can drop data. Production runs `drizzle-kit generate` then `drizzle-kit migrate`, with the SQL committed.
- Pass the whole schema to the client: `drizzle(client, { schema })`. Without it `db.query.*` is undefined and relational queries silently do not exist.
- Define `relations()` for every FK you want to traverse with `with`. Drizzle does not infer relations from `references()`.
- Use `db.query.*` with `with` for nested reads instead of looping `select`s (N+1).
- Indexes live in the schema (`index().on(...)`, `uniqueIndex()`), including every FK column. Review that they exist.
- Derive types with `InferSelectModel` / `InferInsertModel`; no hand-written interfaces that drift.
- Serverless and edge: one client per module scope, using the serverless driver for the platform (`@neondatabase/serverless`, `@libsql/client`, `@planetscale/database`). Never a new connection per request.
- MySQL has no `RETURNING`; read `insertId` from the result instead.
- Prepared statements (`.prepare()`) for hot queries in production.

## Audit checklist for an existing Drizzle schema

- Columns named `*_id` without `references()`.
- FK columns without an index.
- `timestamp()` without `{ withTimezone: true }`; `varchar` where `text` is meant; `real`/`doublePrecision` for money.
- Missing `.notNull()` on required fields; missing `relations()` for tables queried together.
- `push` appearing in deploy scripts.
