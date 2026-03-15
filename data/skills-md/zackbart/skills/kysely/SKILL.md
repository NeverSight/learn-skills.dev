---
name: kysely
description: >
  Type-safe SQL query builder assistant for Kysely. Use this skill whenever the user is writing
  database queries with Kysely, setting up a Kysely database instance, defining Database types,
  writing migrations, or asking how to do SQL operations (SELECT, INSERT, UPDATE, DELETE, JOIN,
  CTE, MERGE, transactions) in Kysely. Also trigger when the user mentions kysely in their code,
  imports from 'kysely', has a Database interface with table types, or asks about type-safe SQL
  in TypeScript. Also trigger on common misspellings like "kaisley" and "kysley". Activate even
  if they just say "query builder" or "how do I do X in kysely" or paste code that uses
  selectFrom/insertInto/updateTable/deleteFrom patterns. This skill covers relations
  (jsonArrayFrom/jsonObjectFrom), expression builders, raw SQL via the sql tag, conditional
  queries, reusable helpers, schema management, migrations, execution pipeline/debugging, plugins,
  and all Kysely patterns.
---

# Kysely Query Builder

You are an expert at writing type-safe SQL queries with Kysely. Kysely is a type-safe TypeScript SQL query builder — it is NOT an ORM. It builds SQL based on what the developer writes and provides compile-time type checking.

## Core Principles

1. **Type safety first** — Always define proper Database interfaces. Use `Generated<T>` for auto-increment/default columns, `ColumnType<S, I, U>` for columns with different select/insert/update types.
2. **Kysely is not an ORM** — There are no model classes, no lazy loading, no relation definitions. Relations are handled via joins or JSON helper functions.
3. **Everything is an expression** — `Expression<T>` is the fundamental building block. Helpers should accept and return expressions for composability.
4. **The query builder is immutable** — Each method call returns a new builder. When building queries conditionally, reassign: `query = query.where(...)`.
5. **Dialect awareness** — Some features are dialect-specific (e.g., `returning` on PostgreSQL, `insertId` on MySQL/SQLite, `distinctOn` on PostgreSQL, `mergeInto` varies by dialect). Always consider which database the user targets.

## How to Use This Skill

When the user needs Kysely help, consult the reference files for detailed patterns:

- **`references/examples.md`** — Complete code examples for SELECT, WHERE, JOIN, INSERT, UPDATE, DELETE, MERGE, transactions, and CTEs
- **`references/recipes.md`** — Advanced patterns: relations, reusable helpers, data types, raw SQL, conditional selects, expressions, schemas, plugins, extending Kysely, introspection, and logging
- **`references/migrations.md`** — Migrator setup and production-safe migration flows (`migrateToLatest`, directional up/down, target migration, rollback all, error handling)
- **`references/execution.md`** — Query lifecycle internals and practical debugging/performance patterns (`compile`, `executeQuery`, `stream`, `explain`, plugins)

Read the relevant reference file section before generating code. The examples there are drawn directly from the official Kysely documentation and represent the canonical way to use each feature.

## Quick Reference

### Database Type Setup

```typescript
import { Kysely, Generated, ColumnType, Selectable, Insertable, Updateable } from 'kysely'

interface Database {
  person: PersonTable
  pet: PetTable
}

interface PersonTable {
  id: Generated<number>           // auto-increment, not needed on insert
  first_name: string
  last_name: string | null        // nullable column
  age: number
  created_at: ColumnType<Date, string | undefined, never>  // different types for select/insert/update
}

// Utility types for function signatures
type Person = Selectable<PersonTable>
type NewPerson = Insertable<PersonTable>
type PersonUpdate = Updateable<PersonTable>
```

### Common Operations at a Glance

| Operation | Pattern |
|-----------|---------|
| Select | `db.selectFrom('table').select([...]).where(...).execute()` |
| Insert | `db.insertInto('table').values({...}).executeTakeFirst()` |
| Update | `db.updateTable('table').set({...}).where(...).executeTakeFirst()` |
| Delete | `db.deleteFrom('table').where(...).executeTakeFirst()` |
| Join | `db.selectFrom('a').innerJoin('b', 'b.a_id', 'a.id').select([...])` |
| Transaction | `db.transaction().execute(async (trx) => { ... })` |
| CTE | `db.with('name', (qb) => qb.selectFrom(...).select([...])).selectFrom('name')` |
| Nested array | `jsonArrayFrom(eb.selectFrom('child').select([...]).whereRef(...)).as('children')` |
| Nested object | `jsonObjectFrom(eb.selectFrom('related').select([...]).whereRef(...)).as('item')` |
| Raw SQL | `` sql<Type>`expression with ${parameterized} values` `` |
| Conditional | `if (condition) { query = query.where(...) }` |

### Expression Builder

The expression builder (`eb`) is available via callbacks in most methods. It provides:

- `eb('column', 'op', value)` — binary comparison
- `eb.and([...])` / `eb.or([...])` — logical combinations
- `eb.not(expr)` / `eb.exists(subquery)` — negation and existence
- `eb.selectFrom(...)` — subqueries
- `eb.ref('column')` — column references
- `eb.val(value)` — parameterized values
- `eb.lit(value)` — literal values (embedded in SQL)
- `eb.fn.count(...)` / `eb.fn.avg(...)` / `eb.fn.max(...)` — aggregate functions
- `eb.fn('name', [...])` — call any database function

### Import Paths

```typescript
// Core
import { Kysely, sql, expressionBuilder } from 'kysely'

// Dialect-specific relation helpers
import { jsonArrayFrom, jsonObjectFrom } from 'kysely/helpers/postgres'   // or /mysql or /sqlite

// Plugins
import { ParseJSONResultsPlugin, CamelCasePlugin, DeduplicateJoinsPlugin } from 'kysely'
```

## Common Mistakes to Catch

- **Calling `.select()` before `.innerJoin()`** — The joined table's columns won't be available. Always join first, then select.
- **Forgetting `.as()` on complex selections** — Any expression that isn't a simple column reference needs a name via `.as('alias')`.
- **Using `returning` on MySQL** — MySQL doesn't support RETURNING. Use `insertId` from the result instead.
- **Expecting relations like an ORM** — There are no eager/lazy loading. Use `jsonArrayFrom`/`jsonObjectFrom` or explicit joins.
- **Mutating queries instead of reassigning** — The builder is immutable. `query.where(...)` returns a new query; it doesn't modify the existing one.
- **Not importing dialect-specific helpers** — `jsonArrayFrom` and `jsonObjectFrom` come from `kysely/helpers/postgres` (or `/mysql`/`/sqlite`), not from `kysely` directly.
- **JSON parsing issues** — If the database driver returns JSON columns as strings instead of objects, add `ParseJSONResultsPlugin` to the Kysely instance.
- **Using app DB types in migrations** — Migration callbacks should accept `Kysely<any>`, not your runtime app `Database` type.
- **Assuming migrations throw by default** — Migrator methods return a result set with `error`; always check it and fail explicitly.
