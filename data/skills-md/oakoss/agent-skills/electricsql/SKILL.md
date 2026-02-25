---
name: electricsql
description: |
  ElectricSQL real-time Postgres sync engine using Shapes for partial replication. Covers ShapeStream API, React hooks, where clause filtering, column selection, auth proxy patterns, and progressive write strategies from online-only to through-the-database.

  Use when setting up ElectricSQL, configuring Postgres sync, implementing shape-based data loading, building auth proxies for shapes, or choosing write patterns for local-first apps with Electric.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://electric-sql.com/docs'
user-invocable: false
---

# ElectricSQL

## Overview

ElectricSQL is a sync engine that streams partial replicas of Postgres data to local clients via Shapes. It handles the read path — syncing rows from Postgres to the client in real-time using logical replication. Writes flow back through your existing API; Electric syncs the confirmed state back to all connected clients.

**When to use:** Real-time sync from Postgres to client apps, local-first architectures needing live data from Postgres, replacing polling with streaming updates, apps using TanStack DB with Electric collections, multi-client collaborative apps backed by Postgres.

**When NOT to use:** Non-Postgres databases, apps needing client-to-server sync built into the engine (Electric handles reads only), simple REST CRUD with no real-time needs, apps that don't benefit from local data.

## Quick Reference

| Pattern             | API / Approach                                        | Key Points                                                |
| ------------------- | ----------------------------------------------------- | --------------------------------------------------------- |
| Shape request       | `GET /v1/shape?table=items&offset=-1`                 | Initial sync fetches full snapshot                        |
| Live updates        | `?live=true&handle=...&offset=...`                    | Long-poll for real-time changes after initial sync        |
| SSE streaming       | `?live=true&live_sse=true`                            | Persistent Server-Sent Events connection                  |
| Where clause        | `?where=status='active'`                              | SQL-style row filtering at the server                     |
| Parameterized where | `?where=user_id=$1&params[1]=abc`                     | SQL injection safe parameterized filtering                |
| Column selection    | `?columns=id,title,status`                            | Sync only needed columns to reduce bandwidth              |
| Full replica        | `?replica=full`                                       | Complete row data on updates and deletes                  |
| Changes only        | `?log=changes_only`                                   | Skip initial snapshot, receive only new changes           |
| ShapeStream (JS)    | `new ShapeStream({ url, params: { table } })`         | Low-level streaming client with auto-reconnect            |
| Shape (JS)          | `new Shape(stream)`                                   | Materializes stream into a Map of current values          |
| useShape (React)    | `useShape({ url, params: { table } })`                | React hook with loading/error states                      |
| Auth proxy          | Route shapes through your API server                  | Validate tokens, inject where clauses per user            |
| Docker setup        | `docker run -e DATABASE_URL=... electricsql/electric` | Single container, needs `wal_level=logical`               |
| Electric secret     | `ELECTRIC_SECRET=key` env var                         | Required for production; `ELECTRIC_INSECURE=true` for dev |

## Common Mistakes

| Mistake                                           | Correct Pattern                                                      |
| ------------------------------------------------- | -------------------------------------------------------------------- |
| Exposing Electric directly to the internet        | Put Electric behind an auth proxy that validates tokens              |
| Forgetting `wal_level=logical` in Postgres config | Required for logical replication; Electric will not start without it |
| Using Electric for writes                         | Electric is read-path only; writes go through your API               |
| Not returning `txid` from write handlers          | Return `{ txid }` so Electric can confirm sync completion            |
| Syncing entire tables to every client             | Use where clauses and column selection for partial replication       |
| Hardcoding shape URL in client code               | Use a proxy endpoint that adds auth and where clauses server-side    |
| Using `offset=-1` for every request               | Use `offset=-1` only for initial sync; use returned offset after     |
| Not handling `FetchError` 401 in ShapeStream      | Use `onError` callback to refresh tokens and retry                   |

## Delegation

> If the `local-first` skill is available, delegate architecture decisions and sync engine comparison to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s local-first -a claude-code -y`
> If the `tanstack-db` skill is available, delegate collection setup, live queries, and optimistic mutation patterns to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s tanstack-db -a claude-code -y`
> If the `tanstack-start` skill is available, delegate shape proxy implementation with server functions to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s tanstack-start -a claude-code -y`

- **Setup and deployment**: Use `Task` agent for Docker and Postgres configuration
- **Architecture review**: Use `Plan` agent for auth proxy and write pattern design

## References

- [Setup, Docker, and Postgres configuration](references/setup.md)
- [Shapes, ShapeStream, and React hooks](references/shapes-and-streams.md)
- [Authentication and security patterns](references/auth-and-security.md)
- [Write patterns from online to through-the-DB](references/write-patterns.md)
- [Observability and monitoring](references/monitoring.md)
- [Sync performance optimization](references/sync-performance.md)
- [Error handling, retry patterns, txid flow, and control messages](references/error-handling.md)
