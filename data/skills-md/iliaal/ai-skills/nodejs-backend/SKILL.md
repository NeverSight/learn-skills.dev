---
name: nodejs-backend
description: >-
  Node.js backend patterns: layered architecture, TypeScript, validation, error
  handling, security, deployment. Use when building REST APIs, Express/Fastify
  servers, or server-side TypeScript.
---

# Node.js Backend

## Framework Selection

| Context | Choose | Why |
|---------|--------|-----|
| Edge/Serverless | Hono | Zero-dep, fastest cold starts |
| Performance API | Fastify | 2-3x faster than Express, built-in schema validation |
| Enterprise/team | NestJS | DI, decorators, structured conventions |
| Legacy/ecosystem | Express | Most middleware, widest adoption |

Ask user: deployment target, cold start needs, team experience, existing codebase.

## Architecture

```
src/
├── routes/          # HTTP: parse request, call service, format response
├── middleware/       # Auth, validation, rate limiting, logging
├── services/        # Business logic (no HTTP types)
├── repositories/    # Data access only (queries, ORM)
├── config/          # Env, DB pool, constants
└── types/           # Shared TypeScript interfaces
```

- Routes never contain business logic
- Services never import Request/Response
- Repositories never throw HTTP errors
- For scripts/prototypes: single file is fine — ask "will this grow?"

## TypeScript Rules

- Use `import type { }` for type-only imports — eliminates runtime overhead
- Prefer `interface` for object shapes (2-5x faster type resolution than intersections)
- Prefer `unknown` over `any` — forces explicit narrowing
- Use `z.infer<typeof Schema>` as single source of truth — never duplicate types and schemas
- Minimize `as` assertions — use type guards instead
- Add explicit return types to exported functions (faster declaration emit)
- Untyped package? `declare module 'pkg' { const v: unknown; export default v; }` in `types/ambient.d.ts`

## Validation

**Zod** (TypeScript inference) or **TypeBox** (Fastify native). Validate at boundaries only: request entry, before DB ops, env vars at startup. Use `.extend()`, `.pick()`, `.omit()`, `.partial()`, `.merge()` for DRY schemas.

## Error Handling

Custom error hierarchy: `AppError(message, statusCode, isOperational)` → `ValidationError(400)`, `NotFoundError(404)`, `UnauthorizedError(401)`, `ForbiddenError(403)`, `ConflictError(409)`

Centralized handler middleware:
- `AppError` → return `{ error: message }` with statusCode
- Unknown → log full stack, return 500 + generic message in production
- Async wrapper: `const asyncHandler = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);`

Codes: 400 bad input | 401 no auth | 403 no permission | 404 missing | 409 conflict | 422 business rule | 429 rate limited | 500 server fault

## API Design

- **Resources**: plural nouns (`/users`), max 2 nesting levels (`/users/:id/orders`)
- **Methods**: GET read | POST create | PUT replace | PATCH partial | DELETE remove
- **Versioning**: URL path `/api/v1/`
- **Response**: `{ data, pagination?: { page, limit, total, totalPages } }`
- **Errors**: `{ error: { code, message, details? } }`
- **Queries**: `?page=1&limit=20&status=active&sort=createdAt,desc`
- Return `Location` header on 201. Use 204 for successful DELETE with no body.

## Async Patterns

| Pattern | Use When |
|---------|----------|
| `async/await` | Sequential operations |
| `Promise.all` | Parallel independent ops |
| `Promise.allSettled` | Parallel, some may fail |
| `Promise.race` | Timeout or first-wins |

Never `readFileSync` / sync methods in production. Offload CPU work to worker threads (Piscina). Stream large payloads.

## Production Resilience

- **Caching**: Redis cache-aside for DB/API responses; in-memory LRU with TTL for hot paths. Always invalidate on writes.
- **Load shedding**: `@fastify/under-pressure` (or equivalent) — monitor event loop delay, heap, RSS; return 503 when thresholds exceeded.
- **Response schemas**: In Fastify, always define response schemas — enables `fast-json-stringify` for 2-3x faster serialization.

## Discipline

- For non-trivial changes, pause and ask: "is there a more elegant way?" Skip for obvious fixes.
- Simplicity first — every change as simple as possible, impact minimal code
- Only touch what's necessary — avoid introducing unrelated changes
- No hacky workarounds — if a fix feels wrong, step back and implement the clean solution

## References

- [TypeScript config](./references/typescript-config.md) — tsconfig, ESM, branded types, compiler performance
- [Security](./references/security.md) — JWT, password hashing, rate limiting, OWASP
- [Database & production](./references/database-production.md) — connection pooling, transactions, Docker, logging
