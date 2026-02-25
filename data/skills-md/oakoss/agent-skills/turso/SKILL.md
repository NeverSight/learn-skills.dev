---
name: turso
description: |
  Turso edge-hosted SQLite platform built on libSQL (open-source SQLite fork). Covers @libsql/client SDK, embedded replicas with local sync, multi-database per-tenant architecture, platform API for database provisioning, schema migrations, vector search with F32_BLOB, batch operations, interactive transactions, and encryption at rest.

  Use when connecting to Turso databases, configuring embedded replicas, provisioning databases via the platform API, implementing per-tenant database isolation, performing vector similarity search, or integrating libSQL with Drizzle ORM.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://docs.turso.tech'
user-invocable: false
---

# Turso

## Overview

Turso is an edge-hosted SQLite platform built on libSQL, an open-source fork of SQLite. It provides globally distributed databases with embedded replicas for local-first reads, a platform API for programmatic database management, and native vector search. Use Turso for edge-deployed applications needing low-latency reads, per-tenant database isolation, or offline-capable embedded replicas. Avoid when you need a traditional relational database with complex joins across tenants or require PostgreSQL-specific features.

## Quick Reference

| Pattern                 | API / Command                               | Key Points                                         |
| ----------------------- | ------------------------------------------- | -------------------------------------------------- |
| Remote client           | `createClient({ url, authToken })`          | Connect to Turso cloud database                    |
| Local file client       | `createClient({ url: 'file:local.db' })`    | Pure local SQLite via libSQL                       |
| Embedded replica        | `createClient({ url, syncUrl, authToken })` | Local reads, remote sync                           |
| Manual sync             | `client.sync()`                             | Pull latest changes from remote                    |
| Periodic sync           | `syncInterval: 60` in client config         | Auto-sync interval in seconds                      |
| Execute query           | `client.execute({ sql, args })`             | Positional `?` or named `$param` args              |
| Batch operations        | `client.batch([...statements], mode)`       | Atomic multi-statement execution                   |
| Interactive transaction | `client.transaction('write')`               | Multi-step logic with commit/rollback              |
| Encryption at rest      | `encryptionKey` in client config            | Encrypts local database file                       |
| Vector insert           | `vector32('[0.1, 0.2, ...]')`               | Store embeddings as F32_BLOB columns               |
| Vector search           | `vector_distance_cos(col, vector32(...))`   | Cosine similarity, ORDER BY distance ASC           |
| Vector index            | `libsql_vector_idx(col, 'type=diskann')`    | DiskANN index for efficient nearest-neighbor       |
| Create database (CLI)   | `turso db create <name>`                    | Provision new database                             |
| Create database (API)   | `POST /v1/organizations/{org}/databases`    | Programmatic provisioning for multi-tenant         |
| Generate token (CLI)    | `turso db tokens create <name>`             | Auth tokens with optional read-only and expiration |
| Drizzle integration     | `drizzle(createClient({ url, authToken }))` | Use `drizzle-orm/libsql` driver                    |
| In-memory database      | `createClient({ url: ':memory:' })`         | Ephemeral database for testing                     |

## Common Mistakes

| Mistake                                             | Correct Pattern                                                           |
| --------------------------------------------------- | ------------------------------------------------------------------------- |
| Using `syncUrl` without `authToken`                 | Embedded replicas require both `syncUrl` and `authToken`                  |
| Forgetting `client.sync()` before reads             | Call `sync()` or set `syncInterval` to keep replica current               |
| Using `vector_distance_cos` without a vector index  | Create a `libsql_vector_idx` index for efficient similarity search        |
| Hardcoding auth tokens in source code               | Use environment variables for `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` |
| Using interactive transactions for simple batches   | Use `client.batch()` for atomic multi-statement operations                |
| Not closing transactions on error                   | Always call `transaction.close()` in a `finally` block                    |
| Creating one database for all tenants               | Use multi-database per-tenant isolation for SaaS workloads                |
| Passing raw arrays as vector values                 | Wrap vectors with `vector32()` SQL function or pass as `Float32Array`     |
| Using `ORDER BY distance DESC` for nearest neighbor | Cosine distance: smaller is closer, use `ORDER BY distance ASC`           |

## Delegation

> If the `drizzle-orm` skill is available, delegate ORM schema definition, query building, relations, and migration patterns to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s drizzle-orm -a claude-code -y`
>
> If the `local-first` skill is available, delegate architecture decisions, sync engine comparisons, and conflict resolution strategies to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s local-first -a claude-code -y`
>
> If the `pglite` skill is available, delegate PGlite-specific patterns for comparison with Turso embedded replicas.

- **Database provisioning**: Use `Task` agent for multi-tenant setup automation
- **Vector search tuning**: Use `Explore` agent to research embedding models and dimensions
- **Code review**: Delegate to `code-reviewer` agent

## References

- [Client SDK setup, connection modes, and configuration](references/client-sdk.md)
- [Embedded replicas, sync strategies, and offline mode](references/embedded-replicas.md)
- [Batch operations and interactive transactions](references/transactions.md)
- [Vector search, embeddings, and similarity queries](references/vector-search.md)
- [Multi-database per-tenant architecture and platform API](references/multi-tenant.md)
- [CLI commands and database management](references/cli-management.md)
- [Drizzle ORM integration with libSQL driver](references/drizzle-integration.md)
- [Schema migrations and database operations](references/schema-migrations.md)
