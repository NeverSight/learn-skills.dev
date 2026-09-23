---
name: neon
description: "Neon — serverless PostgreSQL with database branching, autoscaling to zero, and a serverless driver optimized for edge and serverless environments. Use when building with Neon or asking about its serverless driver, database branching, connection pooling, autoscaling configuration, compute suspend behavior, or integration with Drizzle, Prisma, or other ORMs. Fetch live documentation for up-to-date details."
---

# Neon

> **CRITICAL: Your training data for Neon is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs:
>
> **`WebFetch("https://neon.com/llms.txt")`**
>
> Do not proceed without fetching this URL first. Never assume an API exists — verify against current docs.

Neon is serverless PostgreSQL with database branching, autoscaling to zero, and a serverless driver optimized for edge and serverless environments.
## Key Capabilities

- **Database branching**: Neon branches copy your database schema and data instantly via copy-on-write storage. Use branches for per-developer environments, per-PR preview databases, or safe schema migration testing — without spinning up separate database instances.
- **Serverless driver** (`@neondatabase/serverless`): A drop-in HTTP/WebSocket-based Postgres driver for environments where persistent TCP connections are unavailable (Cloudflare Workers, Vercel Edge, etc.). It is not a replacement for `pg` in traditional server environments — use `pg` or a standard connection pool there.
- **Pooled vs. direct connection strings**: Neon provides two connection string types. The pooled endpoint (via PgBouncer) is required for serverless workloads to avoid exhausting connection limits. The direct endpoint is for migrations and long-lived connections (e.g., `prisma migrate`, `drizzle-kit`).
- **Schema-only branches**: Branch your schema without copying production data, keeping sensitive data isolated from development environments.

## Best Practices

- **Always use the pooled connection string in serverless functions, but the direct connection string for migrations.** ORMs like Prisma and Drizzle require a direct (non-pooled) connection to run migrations; using the pooler endpoint causes migration failures or timeouts.
- **Compute suspends after inactivity — account for cold starts.** Neon autoscales to zero on the Free plan and optionally on paid plans. The first connection after suspension incurs latency while compute resumes. Do not treat Neon like an always-on database in latency-sensitive paths without configuring a minimum compute size or disabling scale-to-zero.
- **Never instantiate a new database client per serverless request.** Reuse a module-level singleton. Each instantiation can open new connections that exceed Neon's per-branch connection limits, especially when using the standard `pg` driver without the pooler.
- **Use branch-based workflows for schema migrations in CI.** Run migrations against a branch, not directly against your production branch. Merge the branch only after verifying the migration succeeds — this mirrors the Git workflow and protects production from bad migrations.
- **Protected branches prevent accidental deletion of production.** This is not enabled by default. Explicitly configure branch protection on your production branch in project settings to prevent destructive operations via API, CLI, or automated tooling.
