---
name: express-backend-starter
description: Guides AI agents to scaffold and develop production-grade Node.js + Express backends with a clean, scalable folder structure and industry best practices. Use when user asks to "create a backend", "set up an API", "scaffold a Node project", "build an Express server", "create REST API", "backend folder structure", "API boilerplate", or starts a new Node.js/Express backend project. Covers JS and TS.
license: MIT
metadata:
  author: Hashim
  organization: Sitefusion.dev
  version: 1.0.0
---

# Backend Node + Express Development Skill

Expert guidance for building production-grade, API-only Node.js + Express backends. This skill ensures every new backend project starts with a clean architecture, consistent patterns, and security-first defaults — whether in JavaScript or TypeScript.

---

## Instructions

### Step 1: Confirm Project Basics

Before writing any code, clarify with the user:

1. **Language:** JavaScript or TypeScript?
2. **Database:** PostgreSQL, MySQL, MongoDB, or other?
3. **ORM/Query builder:** Prisma, Knex, Mongoose, raw driver?
4. **Auth strategy:** JWT or session-based?

If the user doesn't specify, default to: **TypeScript + PostgreSQL + Prisma + JWT**.

**Node Version: Require Node 24 LTS (Active LTS), preferably >=24.10.0** for non-experimental env-file support. Use `node --watch` for dev restarts and `--env-file-if-exists` for env loading — no `nodemon` or `dotenv` needed. For the full version/stability table and lifecycle guidance, see [node-version-guide.md](references/node-version-guide.md).

Pin the Node version in `.nvmrc` — e.g. `24` or a specific `24.x.y` (>=24.10.0 recommended).

### Step 2: Scaffold the Folder Structure

Always generate this folder structure. Adapt file extensions based on JS vs TS.

```
.
├─ src/
│  ├─ app/
│  │  ├─ app.(js|ts)                 # Express app: middleware stack + route mounting
│  │  └─ server.(js|ts)              # HTTP server start + graceful shutdown
│  ├─ config/
│  │  ├─ env.(js|ts)                 # Env var parsing + validation (fail fast on boot)
│  │  └─ index.(js|ts)               # Normalized config object (single source of truth)
│  ├─ routes/
│  │  ├─ index.(js|ts)               # Mount all versioned routers (e.g. /api/v1)
│  │  └─ v1/
│  │     ├─ health.routes.(js|ts)    # Health + readiness endpoints
│  │     └─ users.routes.(js|ts)     # Example resource module
│  ├─ controllers/
│  │  └─ users.controller.(js|ts)    # HTTP glue only (thin — no business logic)
│  ├─ services/
│  │  └─ users.service.(js|ts)       # All business logic and use-cases
│  ├─ repositories/
│  │  └─ users.repo.(js|ts)          # DB access only (queries, ORM calls)
│  ├─ db/
│  │  ├─ client.(js|ts)              # DB connection pool / Prisma client
│  │  ├─ migrations/                 # Database migration files
│  │  └─ seed/                       # Seed scripts for dev/test data
│  ├─ middlewares/
│  │  ├─ auth.(js|ts)                # Authentication middleware
│  │  ├─ error-handler.(js|ts)       # Global error handler (MUST be last middleware)
│  │  ├─ rate-limit.(js|ts)          # Rate limiting (global + per-route)
│  │  └─ request-id.(js|ts)          # Adds req.id for log correlation
│  ├─ validators/
│  │  └─ users.schema.(js|ts)        # Zod or Joi schemas for request validation
│  ├─ errors/
│  │  ├─ AppError.(js|ts)            # Custom error base class with status + code
│  │  └─ error-codes.(js|ts)         # Stable, documented error codes map
│  ├─ logging/
│  │  └─ logger.(js|ts)              # Structured logger (pino/winston) + secret redaction
│  ├─ utils/
│  │  ├─ async-handler.(js|ts)       # Wraps async controllers (no try/catch boilerplate)
│  │  └─ http-response.(js|ts)       # Standardized success/error response helpers
│  └─ types/                         # TS only: shared interfaces and type definitions
│
├─ tests/
│  ├─ unit/                          # Service + utility unit tests
│  ├─ integration/                   # Route + DB integration tests
│  └─ e2e/                           # Full flow end-to-end tests
│
├─ docs/
│  ├─ openapi.yaml                   # OpenAPI spec (recommended)
│  └─ runbook.md                     # Deploy, rollback, and ops notes
│
├─ scripts/                          # One-off scripts (backfills, maintenance)
├─ docker/                           # Dockerfile, docker-compose, local infra
├─ .github/workflows/                # CI pipeline config
├─ .env.example                      # Documented env var template
├─ .editorconfig
├─ .nvmrc                            # Pin Node version
├─ .eslintrc.* / eslint.config.*
├─ .prettierrc / prettier.config.*
├─ README.md
└─ package.json
```

CRITICAL rules:
- **One language per repo** — never mix JS and TS source files.
- For TS repos, compile to a `dist/` folder; never run raw `.ts` in production.
- Every new feature module replicates the same pattern: `routes → controller → service → repository → validator`.
- Keep `types/` for TS-only shared interfaces; omit for JS repos.

### Step 3: Follow the Request Flow

All requests MUST flow through these layers in order:

**Route → Controller → Service → Repository**

| Layer | Responsibility | Rules |
|---|---|---|
| **Routes** | Define URL paths + HTTP methods | Only call controllers. No logic. |
| **Controllers** | Parse/validate input, call service, format response | THIN — no business logic, no DB calls |
| **Services** | Business logic, permissions, orchestration | May call multiple repos. Owns transactions. |
| **Repositories** | Database queries only | Return domain objects, not raw DB rows |

NEVER skip layers. Controllers must NOT call repositories directly. Services must NOT write raw SQL.

### Step 4: Apply Security Defaults

Every backend MUST include these from day one:

1. **Helmet** — secure HTTP headers
2. **CORS** — explicit allowlist (never use `*` in production)
3. **Rate limiting** — global + stricter on auth routes (login, register)
4. **Body size limits** — prevent payload abuse
5. **Input validation** — validate params, query, and body on every endpoint using Zod or Joi
6. **Password hashing** — bcrypt or argon2 (NEVER store plaintext passwords)
7. **Secret redaction** — never log tokens, passwords, or API keys
8. **Auth consistency** — pick JWT or sessions and stick with one approach

### Step 5: Implement the Middleware Stack

Mount middleware in this exact order:

1. `request-id` — assigns unique ID to every request
2. Logger middleware — logs request start/end with request ID
3. `helmet` — security headers
4. `cors` — cross-origin policy
5. Body parsers (`express.json()`, `express.urlencoded()`) + size limits
6. Rate limiter
7. Auth middleware — only on protected routes
8. Routes — mount `/api/v1/*`
9. 404 handler — catch unmatched routes
10. Global error handler — MUST be last

### Step 6: Standardize API Responses

Use a consistent response shape across ALL endpoints:

```json
// Success
{
  "success": true,
  "data": { ... }
}

// Error
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "No user found with the given ID.",
    "details": null
  }
}
```

Use correct HTTP status codes:
- `400` — validation errors
- `401` — unauthenticated
- `403` — forbidden (authenticated but not authorized)
- `404` — resource not found
- `409` — conflict (duplicate, etc.)
- `429` — rate limited
- `500+` — server errors

### Step 7: Set Up Error Handling

- Create a custom `AppError` class extending `Error` with `statusCode`, `code`, and `isOperational` properties.
- Use an `async-handler` wrapper for all controller methods to catch rejected promises automatically.
- The global error handler middleware (LAST in the stack) catches everything:
  - Known `AppError` → return structured error with the appropriate status.
  - Unknown errors → log full stack trace, return generic 500 to client.
  - NEVER leak stack traces or internal details in production responses.
- Define stable error codes in `error-codes.(js|ts)` — clients depend on these, not message strings.

### Step 8: Configure Logging and Observability

- Use a structured JSON logger (`pino` recommended, `winston` acceptable).
- Attach `req.id` (request ID) to every log entry for correlation.
- Include response headers: `x-request-id`.
- Add health endpoints:
  - `GET /api/v1/health` — always returns `200` if process is alive.
  - `GET /api/v1/ready` — checks DB and external service connectivity.
- Redact any secrets, tokens, or passwords from all log output.

### Step 9: Configure Environment and Scripts

**Environment:**
- Validate ALL env vars on boot using the config module — crash immediately if required vars are missing.
- Centralize env access in `src/config/index.(js|ts)` — NEVER scatter `process.env.*` across the codebase.
- Provide `.env.example` documenting every required and optional variable.
- Do NOT install `dotenv` — use Node's built-in env loading instead.

**Package.json scripts** depend on your Node version. See [scripts-and-env.md](references/scripts-and-env.md) for the full 3-tier guide (Tier A: Node >=24.10.0 non-experimental, Tier B: Node 22.9+ experimental flags, Tier C: Node 20.12+ programmatic loading).

Quick reference (Tier A / recommended):
- JS dev: `node --watch --env-file-if-exists=.env src/app/server.js`
- TS dev: `tsc -w` in terminal 1, `node --watch --env-file-if-exists=.env dist/app/server.js` in terminal 2

Always include: `lint`, `format`, `test`, `test:watch`, `migrate`, `seed`

IMPORTANT: Do NOT add `nodemon`, `dotenv`, or `tsx` as dependencies.

### Step 10: Database Best Practices

- ALWAYS use migrations — never modify schema by hand in production.
- Use connection pooling with proper timeout configuration.
- Wrap multi-step writes in transactions.
- Index intentionally and monitor slow queries.
- Keep ALL database logic inside `repositories/` — services never write raw queries.
- Seed scripts go in `src/db/seed/` for reproducible dev/test data.

### Step 11: Testing Strategy

- **Unit tests** (`tests/unit/`) — test services, utilities, and pure logic in isolation.
- **Integration tests** (`tests/integration/`) — test routes with a real DB (use Docker).
- **E2E tests** (`tests/e2e/`) — test complete user flows end-to-end.
- Use `supertest` for HTTP assertions in integration tests.
- Use factories/fixtures for predictable, reproducible test data.
- Testing framework: `vitest` (preferred) or `jest`.
- **Zero-dependency alternative:** Node's built-in test runner (`node --test`) is stable since Node 20 and supports `describe`/`it` and assertions. Module mocking requires `--experimental-test-module-mocks`; coverage via `--experimental-test-coverage`. Vitest and Jest remain excellent for richer ecosystems.

### Step 12: Production Readiness

Before deploying, ensure:

1. **Graceful shutdown** — stop accepting requests, drain connections, close DB pool, stop background workers.
2. **Docker** — multi-stage build, non-root user, healthcheck wired to `/api/v1/health`.
3. **Stateless** — no in-memory state; use external stores (Redis, DB) for sessions/cache.
4. **12-Factor** — log to stdout/stderr, config via env vars, one codebase per deploy.
5. **CI pipeline** — lint → test → build (TS) → optional security scan → optional integration tests with Dockerized DB.
6. **Secrets** — use a secret manager in production; never commit `.env` files.

### Step 13: Naming Conventions

| Type | Pattern | Example |
|---|---|---|
| Routes | `*.routes.(js\|ts)` | `users.routes.ts` |
| Controllers | `*.controller.(js\|ts)` | `users.controller.ts` |
| Services | `*.service.(js\|ts)` | `users.service.ts` |
| Repositories | `*.repo.(js\|ts)` | `users.repo.ts` |
| Validators | `*.schema.(js\|ts)` | `users.schema.ts` |
| Errors | `AppError.(js\|ts)` | `AppError.ts` |
| Config | Descriptive names | `env.ts`, `index.ts` |

### Step 14: Recommended Dependencies

**Runtime:**
- `express` — web framework
- `helmet` — secure headers
- `cors` — cross-origin requests
- `zod` or `joi` — request validation
- `pino` or `winston` — structured logging
- DB driver: `pg`, `mysql2`, `mongoose`, or `prisma`

**NOT needed (handled by Node.js built-ins):**
- ~~`dotenv`~~ — use `--env-file-if-exists` (non-experimental in Node >=24.10.0) or `process.loadEnvFile()` (Node >=20.12.0)
- ~~`nodemon`~~ — use `node --watch` (stable since Node >=20.13.0)
- ~~`tsx`~~ — use `tsc -w` + `node --watch` (or native TS in Node >=22.18.0)

**Dev tooling:**
- `eslint` + `prettier` — code quality
- `vitest` or `jest` — test runner (or `node --test` for zero-dependency testing; coverage via `--experimental-test-coverage`)
- `supertest` — HTTP integration testing
- `husky` + `lint-staged` — git hooks (optional but recommended)
- `typescript` — compiler (TS repos only)

---

## Examples

### Example 1: New Backend Project

User says: "Create a new Express API for a task management app"

Actions:
1. Confirm: TypeScript, PostgreSQL, Prisma, JWT (or ask user preference)
2. Scaffold the full folder structure with `tasks` as the first resource module
3. Create `routes/v1/tasks.routes.ts`, `controllers/tasks.controller.ts`, `services/tasks.service.ts`, `repositories/tasks.repo.ts`, `validators/tasks.schema.ts`
4. Set up middleware stack in correct order
5. Configure env validation, logger, error handling
6. Add health endpoints
7. Create `package.json` with `node --watch` dev script and `--env-file-if-exists` for env loading — no nodemon or dotenv
8. Provide `.env.example`
9. Pin `24` in `.nvmrc` (Node 24 LTS)

### Example 2: Adding a New Feature Module

User says: "Add an orders feature to my API"

Actions:
1. Create the full module following the established pattern:
   - `routes/v1/orders.routes.(js|ts)`
   - `controllers/orders.controller.(js|ts)`
   - `services/orders.service.(js|ts)`
   - `repositories/orders.repo.(js|ts)`
   - `validators/orders.schema.(js|ts)`
2. Add migration for the orders table
3. Mount routes in `routes/v1/` index
4. Follow existing naming and response conventions

### Example 3: Backend Code Review

User says: "Review my Express backend structure"

Actions:
1. Check folder structure against the recommended layout
2. Verify the request flow (Route → Controller → Service → Repository)
3. Check for security defaults (helmet, cors, rate limiting, validation)
4. Verify error handling pattern (AppError, global handler, async wrapper)
5. Review middleware ordering
6. Flag any anti-patterns (business logic in controllers, raw SQL in services, scattered env access)

---

## Reference Files

- **Node version details**: See [node-version-guide.md](references/node-version-guide.md) for the full version/stability table, lifecycle guidance, watch flags, and native TypeScript details.
- **Script tiers and env loading**: See [scripts-and-env.md](references/scripts-and-env.md) for all 3 tiers of `package.json` scripts based on Node version.
- **Troubleshooting**: See [troubleshooting.md](references/troubleshooting.md) for common anti-patterns and the rationale behind `--env-file-if-exists`.
