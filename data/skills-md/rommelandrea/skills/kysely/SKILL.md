---
name: kysely
description: >
  Best practices for Kysely, the type-safe TypeScript SQL query builder.
  Use when writing queries, defining database types, creating migrations,
  or integrating Kysely with PostgreSQL, MySQL, or SQLite.
metadata:
  version: "1.2.0"
  tags: kysely, typescript, sql, postgres, mysql, sqlite, query-builder, database, type-safe
---

## When to use

Use this skill when you need to:
- Build type-safe SQL queries with Kysely
- Define database interfaces and column types
- Write and run Kysely migrations
- Handle transactions, error recovery, and connection pooling
- Load related data efficiently (JSON aggregation, avoiding N+1)
- Use raw SQL safely within Kysely
- Test code that uses Kysely

## How to use

Read individual rule files for detailed explanations and code examples:

- [rules/setup.md](rules/setup.md) - Installation, dialect config, database interface
- [rules/type-safety.md](rules/type-safety.md) - Database types, codegen, Generated, ColumnType
- [rules/select-queries.md](rules/select-queries.md) - SELECT patterns, joins, subqueries, CTEs
- [rules/insert-update-delete.md](rules/insert-update-delete.md) - DML operations, returning, upserts
- [rules/transactions.md](rules/transactions.md) - Transaction patterns, isolation levels, error recovery
- [rules/migrations.md](rules/migrations.md) - Migration setup, up/down, schema builder API
- [rules/raw-sql.md](rules/raw-sql.md) - sql template tag, parameterization, sql.raw dangers
- [rules/relations.md](rules/relations.md) - JSON aggregation, jsonArrayFrom, N+1 prevention
- [rules/error-handling.md](rules/error-handling.md) - Error types, constraint violations, executeTakeFirstOrThrow
- [rules/performance.md](rules/performance.md) - Connection pooling, pagination, batch operations
- [rules/testing.md](rules/testing.md) - Integration tests, transaction isolation, mocking
- [rules/plugins.md](rules/plugins.md) - CamelCasePlugin, custom plugins, ParseJSONResultsPlugin

## Core principles

- **Type safety end-to-end**: Define database interfaces, let Kysely infer query result types
- **Narrow selects**: Select only the columns you need — avoid `selectAll()`
- **Parameterized queries**: Always use the `sql` template tag — never concatenate user input
- **Single instance**: Create one `Kysely` instance per database, reuse it everywhere
- **Thin abstraction**: Kysely compiles to SQL 1:1 — learn the SQL it generates
- **Expression builder first**: Prefer `eb` callbacks over raw SQL for type-safe dynamic expressions
