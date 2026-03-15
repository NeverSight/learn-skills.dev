---
name: tidbx-nextjs
description: Build and deploy Next.js (App Router) apps that connect to TiDB. Covers Route Handlers (app/api/*/route.ts), Node vs Edge runtime selection for database access, environment variable handling, and production-safe DB patterns on Vercel/serverless. Prefer Prisma/Kysely integration, with optional mysql2 for minimal examples. Includes guides and TypeScript templates.
---

# TiDB Next.js Integration

Set up a Next.js app (App Router) that connects to TiDB, with clear guidance on where database code can run (Node runtime) and how to avoid common serverless pitfalls.

## What is different about Next.js (vs plain Node scripts)

- Full-stack framework: UI and server code live in one project.
- Server/client split: database code must stay server-side (route handlers, server components, server actions).
- Multiple runtimes: some routes can run on Edge; TCP database clients must run on Node runtime.
- File-based routing: API endpoints are files like `app/api/*/route.ts`.

## When to use this skill

- Build a new Next.js app that reads/writes TiDB
- Add TiDB to an existing Next.js App Router project
- Deploy to Vercel (or other serverless platforms) and avoid connection/caching/runtime issues
- Decide between Prisma/Kysely vs direct mysql2

## Key decisions (recommended defaults)

1. Prefer an ORM/query builder for application code:
   - Prisma ORM: `tidbx-prisma`
   - Kysely query builder: `tidbx-kysely`
2. Use a direct driver (`mysql2`) only for minimal demos or when you need raw SQL without an ORM.
3. Run TCP database clients in the Node.js runtime (not Edge).

## TiDB Cloud pool settings (mysql2)

- If you use a connection pool against TiDB Cloud, set the pool idle timeout to <= 300s (e.g. `idleTimeout: 300_000`).
- Keep the pool small in serverless environments (often `connectionLimit: 1` is enough per function/container).

## Available guides

- `guides/quickstart.md` -- create a Next.js app and add TiDB (Prisma-first; mysql2 alternative)
- `guides/troubleshooting.md` -- runtime/env/caching/connection issues

## Quick examples

- "Add a /api/health route that queries TiDB" -> route handler + pooled connection
- "Use Prisma in Next.js and deploy to Vercel" -> prisma singleton + route handlers
- "My route handler fails on Vercel Edge" -> force Node runtime or switch to serverless HTTP driver

## Templates

- `templates/route-handler-mysql2.ts` -- App Router Route Handler that queries TiDB with mysql2 (Node runtime)
- `templates/tidb-mysql2-pool.ts` -- mysql2 pool helper with TLS and serverless-friendly defaults
- `templates/prisma-client.ts` -- PrismaClient singleton for Next.js (dev hot reload safe)
- `templates/route-handler-prisma.ts` -- Route Handler using Prisma ($queryRaw + CRUD)

## Related skills

- `tidbx-prisma` -- Prisma ORM (models + migrations + typed client)
- `tidbx-kysely` -- Kysely (typed query builder)
- `tidbx-serverless-driver` -- TiDB Cloud serverless HTTP driver (for edge-like runtimes)
- `tidbx` -- provision/manage TiDB Cloud clusters

---

## Workflow

I will:
1. Confirm your Next.js routing mode (App Router) and runtime target (Node serverless vs Edge)
2. Confirm your TiDB deployment (TiDB Cloud vs self-managed) and endpoint type (public vs private)
3. Recommend Prisma/Kysely by default, unless you explicitly want mysql2
4. Generate the minimal files (route handler + db client helper) and env vars to get you running
