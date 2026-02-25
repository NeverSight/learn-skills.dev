---
name: cloudflare
description: 'Cloudflare Workers, KV, D1, R2, Pages, and Wrangler CLI. Use when deploying to the edge, configuring Workers, managing storage bindings, or setting up Cloudflare Pages.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: https://developers.cloudflare.com/workers
user-invocable: false
---

# Cloudflare

## Overview

Cloudflare Workers is a serverless edge compute platform that runs JavaScript, TypeScript, and WebAssembly on Cloudflare's global network. Workers use the ES modules format with `fetch`, `scheduled`, and `queue` event handlers, and access platform services (KV, D1, R2, Durable Objects) through environment bindings.

**When to use:** Edge-first APIs, low-latency global apps, serverless functions, static site hosting with Pages, key-value caching, relational data at the edge, object storage without egress fees.

**When NOT to use:** Long-running compute exceeding CPU time limits, workloads requiring persistent TCP connections, applications needing full Node.js API compatibility, large monolithic applications better suited to containers.

## Quick Reference

| Pattern               | API / Config                                         | Key Points                                   |
| --------------------- | ---------------------------------------------------- | -------------------------------------------- |
| Fetch handler         | `export default { fetch(request, env, ctx) }`        | Entry point for HTTP requests                |
| Scheduled handler     | `export default { scheduled(controller, env, ctx) }` | Cron triggers via `[triggers]` in config     |
| Environment variables | `env.VAR_NAME`                                       | Set in wrangler.toml or dashboard            |
| KV read/write         | `env.KV.get(key)` / `env.KV.put(key, value)`         | Eventually consistent, 25 MiB max value      |
| D1 query              | `env.DB.prepare(sql).bind(...params).all()`          | SQLite at the edge, prepared statements      |
| D1 batch              | `env.DB.batch([stmt1, stmt2])`                       | Atomic transaction, single round trip        |
| R2 upload             | `env.BUCKET.put(key, body)`                          | S3-compatible, no egress fees                |
| R2 download           | `env.BUCKET.get(key)`                                | Returns `R2ObjectBody` with `ReadableStream` |
| Durable Objects       | `env.DO.get(id)` then `stub.fetch(request)`          | Single-instance stateful coordination        |
| DO storage            | `this.ctx.storage.sql.exec(query)`                   | SQLite backend recommended for new DOs       |
| Pages deploy          | `wrangler pages deploy <dir>`                        | Static + Functions, auto-generated routes    |
| Worker deploy         | `wrangler deploy`                                    | Reads wrangler.toml for config               |
| Dev server            | `wrangler dev`                                       | Local development with bindings              |
| Secrets               | `wrangler secret put SECRET_NAME`                    | Encrypted, not in wrangler.toml              |
| Static assets         | `assets: { directory: "./dist" }`                    | Served without invoking Worker by default    |
| Workflows             | `export class MyWorkflow extends WorkflowEntrypoint` | Durable multi-step execution engine          |
| Hyperdrive            | `env.HYPERDRIVE.connectionString`                    | Connection pooling for external PostgreSQL   |
| Queues produce        | `env.QUEUE.send(message)`                            | Async message passing between Workers        |
| Config format         | `wrangler.jsonc` (recommended for new projects)      | JSON with comments; preferred over TOML      |

## Common Mistakes

| Mistake                                   | Correct Pattern                                               |
| ----------------------------------------- | ------------------------------------------------------------- |
| Accessing bindings as globals             | Access via `env` parameter in module format                   |
| Storing secrets in wrangler.toml          | Use `wrangler secret put` for encrypted values                |
| Using KV for strong consistency           | Use D1 or Durable Objects for consistent reads                |
| Not binding parameters in D1 queries      | Always use `.prepare().bind()` to prevent SQL injection       |
| Exceeding KV value size (25 MiB)          | Use R2 for objects larger than 25 MiB                         |
| Forgetting `await` on storage operations  | KV, D1, R2 methods are all async                              |
| Using `fetch()` without passing `signal`  | Pass `request.signal` for automatic cancellation              |
| Creating D1 database in Worker code       | Create with `wrangler d1 create`, bind in config              |
| Missing `compatibility_date` in config    | Always set to avoid breaking changes                          |
| Returning non-Response from fetch handler | Must return a `Response` object                               |
| Using `wrangler.toml` for new projects    | Use `wrangler.jsonc` for new projects; has better IDE support |
| Using KV for relational queries           | Use D1 for SQL queries; KV is key-value only                  |

## Delegation

- **Architecture review**: Use `Task` agent to evaluate edge vs origin patterns
- **Code review**: Delegate to `code-reviewer` agent
- **Storage selection**: Use `Explore` agent to compare KV vs D1 vs R2 vs DO

## References

- [Workers syntax, fetch handler, scheduled events, and bindings](references/workers.md)
- [KV, D1, R2, and Durable Objects storage APIs](references/storage.md)
- [Cloudflare Pages, functions, routes, and build configuration](references/pages.md)
- [Wrangler CLI, configuration, dev server, deploy, and secrets](references/wrangler.md)
