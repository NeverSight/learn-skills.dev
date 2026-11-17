---
name: backend-patterns
description: Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes.
origin: ECC
---

# Backend Development Patterns

Backend architecture patterns and best practices for scalable server-side applications.

## When to Activate

- Designing REST or GraphQL API endpoints
- Implementing repository, service, or controller layers
- Optimizing database queries (N+1, indexing, connection pooling)
- Adding caching (Redis, in-memory, HTTP cache headers)
- Setting up background jobs or async processing
- Structuring error handling and validation for APIs
- Building middleware (auth, logging, rate limiting)

## Pattern Index

| Area | Patterns | Reference |
|------|----------|-----------|
| Data access | Repository, service layer, middleware | `reference/data-and-caching.md` |
| Database | Query optimization, N+1 prevention, transactions | `reference/data-and-caching.md` |
| Caching | Redis caching layer, cache-aside | `reference/data-and-caching.md` |
| Auth | JWT validation, role-based access control | `reference/auth-and-jobs.md` |
| Rate limiting | In-memory sliding window limiter | `reference/auth-and-jobs.md` |
| Background jobs | In-process queue pattern | `reference/auth-and-jobs.md` |
| Errors | Centralized handler, retry with backoff | `reference/errors-logging.md` |
| Logging | Structured JSON logging | `reference/errors-logging.md` |

## API Design

> **REST conventions (URL structure, HTTP methods, status codes, pagination, filtering, versioning, error response format) live in the `api-design` skill — the canonical REST reference. Read it for endpoint design.** This skill covers the *server-side implementation* of those endpoints (repositories, services, caching, auth enforcement, error handling).

## Core Conventions

### Layered architecture
- **Repository pattern** abstracts data access behind an interface (`findAll`, `findById`, `create`, `update`, `delete`); swap implementations (Supabase, cache-wrapped) without touching business logic.
- **Service layer** holds business logic and depends on repository interfaces, never the storage details.
- **Middleware** wraps handlers as higher-order functions for cross-cutting concerns (auth, logging, rate limiting). Compose via wrappers like `withAuth(handler)`.

### Database
- **Select only needed columns** — never `select('*')` in hot paths.
- **Prevent N+1** — batch-fetch related rows and join in memory with a `Map`, instead of querying per-row in a loop.
- **Transactions** for multi-write operations; wrap in a DB function/RPC so rollback is automatic on error.

### Caching
- **Cache-aside**: check cache, on miss fetch from DB and populate cache with a TTL (e.g. `setex(key, 300, ...)`); invalidate explicitly on writes.
- Decorate a repository (`CachedMarketRepository`) to keep caching transparent to callers.

### Auth & authorization
- Validate JWTs at the boundary; throw a typed `ApiError(401, ...)` on missing/invalid tokens.
- **Role-based access control** via a `role → permissions` map; gate handlers with `requirePermission(...)` HOFs.

### Errors & resilience
- **Centralized error handler** maps typed errors (`ApiError`, `ZodError`) to status codes; unexpected errors log server-side and return a generic 500 (never leak internals).
- **Retry with exponential backoff** for transient upstream failures (1s, 2s, 4s).

### Async & observability
- Offload slow work to a **background queue** instead of blocking the request; return `202`/queued immediately.
- **Structured JSON logging** with request-scoped context (`requestId`, `method`, `path`, `userId`).
- **Rate limit** by IP or user with a sliding window; return `429` when exceeded.

## Quick Reference

```typescript
// Cache-aside
const cached = await redis.get(key)
if (cached) return JSON.parse(cached)
const row = await db.find(id)
await redis.setex(key, 300, JSON.stringify(row))

// Auth guard
const user = await requireAuth(request)        // throws ApiError(401)
if (!hasPermission(user, 'delete')) throw new ApiError(403, '...')

// Centralized error response
catch (error) { return errorHandler(error, request) }

// Offload to queue (non-blocking)
await indexQueue.add({ marketId })
```

## Reference Files

- `reference/data-and-caching.md` — read when implementing repositories, service layers, middleware, query optimization, transactions, or Redis/cache-aside caching.
- `reference/auth-and-jobs.md` — read when implementing JWT validation, role-based access control, rate limiting, or background job queues.
- `reference/errors-logging.md` — read when building centralized error handling, retry/backoff, or structured logging.
- `api-design` skill — read for REST endpoint design conventions (URLs, status codes, pagination, versioning, error format).

**Remember**: Backend patterns enable scalable, maintainable server-side applications. Choose patterns that fit your complexity level.
