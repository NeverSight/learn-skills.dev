---
name: backend-scaffold
description: Generate production-ready backend code with routes, data models, service layers, and validation. Use when scaffolding backend from specs.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/backend/scaffold/**), Task, WebSearch, AskUserQuestion, Edit(jaan-to/config/settings.yaml)
argument-hint: [backend-api-contract, backend-task-breakdown, backend-data-model]
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# backend-scaffold

> Generate production-ready backend code scaffolds from upstream specs — multi-stack, tech.md-adaptive.

## Context Files

- `$JAAN_CONTEXT_DIR/tech.md` - Tech stack context (CRITICAL — determines framework, DB, patterns)
  - Uses sections: `#current-stack`, `#frameworks`, `#constraints`, `#patterns`
- `$JAAN_CONTEXT_DIR/config.md` - Project configuration
- `$JAAN_TEMPLATES_DIR/jaan-to-backend-scaffold.template.md` - Output template
- `$JAAN_LEARN_DIR/jaan-to-backend-scaffold.learn.md` - Past lessons (loaded in Pre-Execution)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Upstream Artifacts**: $ARGUMENTS

Accepts 1-3 file paths or descriptions:
- **backend-api-contract** — Path to OpenAPI YAML (from `/jaan-to:backend-api-contract` output: `api.yaml`)
- **backend-task-breakdown** — Path to BE task breakdown markdown (from `/jaan-to:backend-task-breakdown` output)
- **backend-data-model** — Path to data model markdown (from `/jaan-to:backend-data-model` output)
- **Empty** — Interactive wizard prompting for each

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `backend-scaffold`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

Also read context files if available:
- `$JAAN_CONTEXT_DIR/tech.md` — Know the tech stack for framework-specific code generation
- `$JAAN_CONTEXT_DIR/config.md` — Project configuration

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_backend-scaffold`

> **Language exception**: Generated code output (variable names, code blocks, schemas, SQL, API specs) is NOT affected by this setting and remains in the project's programming language.

---

# PHASE 1: Analysis (Read-Only)

## Thinking Mode

ultrathink

Use extended reasoning for:
- Analyzing upstream artifacts to derive code structure
- Mapping API contract schemas to framework-native patterns
- Planning multi-stack generation strategy
- Identifying edge cases in input parsing

## Step 1: Validate & Parse Inputs

For each provided path:
- **backend-api-contract**: Read api.yaml, extract paths, schemas, error responses, security schemes
- **backend-task-breakdown**: Read markdown, extract task list, entity names, reliability patterns
- **backend-data-model**: Read markdown, extract table definitions, constraints, indexes, relations
- Report which inputs found vs missing; suggest fallback for missing (e.g., CRUD from backend-data-model if no API contract)

Present input summary:
```
INPUT SUMMARY
─────────────
Sources Found:    {list}
Sources Missing:  {list with fallback suggestions}
Entities:         {extracted entity names}
Endpoints:        {count from API contract}
Tables:           {count from data model}
Tasks:            {count from task breakdown}
```

## Step 2: Detect Tech Stack

Read `$JAAN_CONTEXT_DIR/tech.md`:
- Extract framework from `#current-stack` (default: Fastify v5+)
- Extract DB from `#current-stack` (default: PostgreSQL)
- Extract patterns from `#patterns` (auth, error handling, logging)
- If tech.md missing: ask framework/DB via AskUserQuestion

## Step 3: Clarify Architecture

AskUserQuestion for items not in tech.md:
- Project structure (monolith / modular monolith / microservice)
- Auth middleware pattern (JWT / API key / session / none)
- Error handling depth (basic / full RFC 9457 with error taxonomy)
- Logging (structured JSON pino / winston / none)

## Step 4: Plan Scaffold Structure

Present directory tree, file list, resource count:
```
SCAFFOLD PLAN
═════════════

STACK: {framework} + {database} + {orm}

PROJECT STRUCTURE
─────────────────
{directory tree showing all files to generate}

FILES ({count} total)
─────────────────────
{numbered list with file purpose}

RESOURCES ({count})
───────────────────
{resource list with operations}
```

---

# HARD STOP — Review Scaffold Plan

Use AskUserQuestion:
- Question: "Proceed with generating the scaffold?"
- Header: "Generate"
- Options:
  - "Yes" — Generate the scaffold code
  - "No" — Cancel
  - "Edit" — Let me revise the scope or architecture first

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Phase 2 Output — Flat folder (no nested subfolder)

All files in `$JAAN_OUTPUTS_DIR/backend/scaffold/{id}-{slug}/`:

```
{id}-{slug}/
├── {id}-{slug}.md                    # Main doc (setup guide + architecture)
├── {id}-{slug}-routes.ts              # Route handlers (all resources)
├── {id}-{slug}-services.ts            # Service layer (business logic)
├── {id}-{slug}-schemas.ts             # Validation schemas
├── {id}-{slug}-middleware.ts           # Auth + error handling middleware
├── {id}-{slug}-prisma.prisma          # ORM data model
├── {id}-{slug}-config.ts              # Package.json + tsconfig content
└── {id}-{slug}-readme.md              # Setup + run instructions
```

> File extensions adapt to detected stack (.ts for Node.js, .php for PHP, .go for Go).

## Step 6: Generate Content

Read `$JAAN_TEMPLATES_DIR/jaan-to-backend-scaffold.template.md` and populate all sections based on Phase 1 analysis.

If tech stack needed, extract sections from tech.md:
- Current Stack: `#current-stack`
- Frameworks: `#frameworks`
- Constraints: `#constraints`
- Patterns: `#patterns`

## Step 7: Quality Check

Validate generated output against checklist:
- [ ] All API endpoints from contract have route handlers
- [ ] All entities from data model have ORM models
- [ ] Validation schemas generated for all request bodies
- [ ] Error handler covers validation, ORM, and generic errors
- [ ] Service layer stubs exist for all business logic
- [ ] DB singleton + graceful disconnect configured
- [ ] No anti-patterns present in generated code

If any check fails, fix before preview.

## Step 8: Preview & Approval

Present generated output summary. Use AskUserQuestion:
- Question: "Write scaffold files to output?"
- Header: "Write Files"
- Options:
  - "Yes" — Write the files
  - "No" — Cancel
  - "Refine" — Make adjustments first

## Step 9: Generate ID and Folder Structure

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/id-generator.sh"
SUBDOMAIN_DIR="$JAAN_OUTPUTS_DIR/backend/scaffold"
mkdir -p "$SUBDOMAIN_DIR"
NEXT_ID=$(generate_next_id "$SUBDOMAIN_DIR")
slug="{project-name-slug}"
OUTPUT_FOLDER="${SUBDOMAIN_DIR}/${NEXT_ID}-${slug}"
```

Preview output configuration:
> **Output Configuration**
> - ID: {NEXT_ID}
> - Folder: `$JAAN_OUTPUTS_DIR/backend/scaffold/{NEXT_ID}-{slug}/`
> - Main file: `{NEXT_ID}-{slug}.md`

## Step 10: Write Output

1. Create output folder: `mkdir -p "$OUTPUT_FOLDER"`
2. Write all scaffold files to `$OUTPUT_FOLDER`
3. Update subdomain index:
```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/index-updater.sh"
add_to_index \
  "$SUBDOMAIN_DIR/README.md" \
  "$NEXT_ID" \
  "${NEXT_ID}-${slug}" \
  "{Project Title}" \
  "{Executive summary — 1-2 sentences}"
```

4. Confirm completion:
> Scaffold written to: `$JAAN_OUTPUTS_DIR/backend/scaffold/{NEXT_ID}-{slug}/`
> Index updated: `$JAAN_OUTPUTS_DIR/backend/scaffold/README.md`

## Step 11: Suggest Next Actions

> **Scaffold generated successfully!**
>
> **Next Steps:**
> - Copy scaffold files to your project directory
> - Run `npm install` (or equivalent) to install dependencies
> - Run `/jaan-to:dev-integration-plan` to plan integration with existing code
> - Run `/jaan-to:dev-test-plan` to generate test plan

## Step 12: Capture Feedback

Use AskUserQuestion:
- Question: "How did the scaffold turn out?"
- Header: "Feedback"
- Options:
  - "Perfect!" — Done
  - "Needs fixes" — What should I improve?
  - "Learn from this" — Capture a lesson for future runs

If "Learn from this": Run `/jaan-to:learn-add backend-scaffold "{feedback}"`

---

## Key Generation Rules — Node.js/TypeScript (Research-Informed)

- **Routing**: Use `@fastify/autoload` v6 for file-based route loading — register twice (plugins with `encapsulate: false`, routes encapsulated per resource); add `ignorePattern: /.*\.(?:schema|service)\.ts/` to prevent non-plugin files from being auto-loaded as routes
- **Type Provider**: Use `fastify-type-provider-zod` v6.1+ with `validatorCompiler`/`serializerCompiler` set once at app level; must call `withTypeProvider<ZodTypeProvider>()` on each encapsulated context (type providers don't propagate across encapsulation boundaries)
- **Prisma Singleton**: Use `globalThis` pattern to prevent connection pool exhaustion during hot-reload; conditional assignment based on `NODE_ENV`
- **Zod Schemas**: Define schemas in `.schema.ts` files, export `z.infer<>` types; derive from OpenAPI contract component schemas
- **Error Handler**: Use Fastify's `setErrorHandler` (NOT Express-style middleware) — use `hasZodFastifySchemaValidationErrors(error)` for 400 (NOT `instanceof ZodError` which fails across module boundaries), use `isResponseSerializationError(error)` for 500 serialization errors; map `PrismaClientKnownRequestError` P2002 → 409 (unique constraint), P2003 → 409 (foreign key), P2025 → 404 (not found), all others → 500; always set `Content-Type: application/problem+json`
- **RFC 9457 Fields**: `type` (URI), `title`, `status`, `detail`, `instance`; extension `errors[]` for validation details
- **Service Layer**: Plain exported functions importing the Prisma singleton — module caching acts as built-in singleton, making DI containers (tsyringe, inversify) unnecessary; testable via `vi.mock()`; callable from CRON jobs or queue consumers outside HTTP context; use Prisma `$transaction` for cross-service operations
- **Route Structure**: Collocated `index.ts` (routes) + `{resource}.schema.ts` (Zod) + `{resource}.service.ts` (logic) per resource
- **TypeScript**: Extend `fastify-tsconfig` v2 with `target: "ES2023"`, `module: "NodeNext"`, `strict: true`
- **Import Extensions**: With `"type": "module"` and `moduleResolution: "NodeNext"`, all imports MUST include `.js` extensions — `NodeNext` mirrors Node.js runtime behavior; never use `moduleResolution: "bundler"` for backends (allows vague imports that fail at runtime)
- **Env Vars**: Parameterize `DATABASE_URL`, `PORT`, `HOST`, `NODE_ENV`, `LOG_LEVEL`, `CORS_ORIGIN`
- **Env Validation**: Validate environment variables with Zod at startup — crash immediately on missing/invalid variables; use Node.js 20.6+ `--env-file=.env` flag for loading
- **Scripts**: `dev` (tsx watch), `build` (tsc), `start`, `lint`, `test`, `db:generate`, `db:migrate:dev`, `db:migrate:deploy`, `db:push`, `db:seed`, `db:studio`, `postinstall` (prisma generate)

## Multi-Stack Support (Research-Informed)

The skill reads tech.md `#current-stack` to determine which stack to generate:

| tech.md value | Framework | ORM/DB | Validation | Output |
|---------------|-----------|--------|------------|--------|
| Node.js / TypeScript | Fastify v5+ | Prisma | Zod + type-provider v6.1 | `.ts` files |
| PHP | Laravel 12 / Symfony 7 | Eloquent / Doctrine | Form Requests / Symfony Validator | `.php` files |
| Go | Chi / stdlib (Go 1.22+) | sqlc / GORM | go-playground/validator | `.go` files |

**PHP Stack (Laravel) — Key Patterns:**
- PSR-4 autoloading, single `public/index.php` entry point
- Route model binding + Form Requests for validation (`$request->validated()`, never `$request->all()`)
- Eloquent Active Record with `utf8mb4`, BIGINT PKs, JSON columns
- **Strictness in `AppServiceProvider::boot()`**: `preventLazyLoading()` (catches N+1), `preventSilentlyDiscardingAttributes()` (catches mass assignment typos), `preventAccessingMissingAttributes()`; in production, lazy loading violations log instead of throwing
- API Resources for response shaping (never expose raw models); use `whenLoaded()`, `whenCounted()`, conditional `when()` helpers
- Sanctum for auth (SPA cookies + API tokens); cookie auth requires `SANCTUM_STATEFUL_DOMAINS` and `supports_credentials: true`
- Pest 3/4 for testing with architecture presets (`arch()->preset()->laravel()`) and mutation testing (`--mutate`)
- RFC 9457 via `crell/api-problem` v3.8.0 (PHP ^8.3)
- Zero-downtime MySQL migrations: expand-contract pattern (add nullable → backfill → deploy → drop old); use `daursu/laravel-zero-downtime-migration` for large tables

**PHP Stack (Symfony) — Key Patterns:**
- API Platform v4.x: `#[ApiResource]` annotations for automatic CRUD REST APIs with OpenAPI documentation
- Doctrine Data Mapper ORM: entities are POPOs, persistence via EntityManager (better separation than Active Record)
- DTOs with `#[MapRequestPayload]` and Symfony Validator constraint attributes (`#[Assert\NotBlank]`, `#[Assert\Positive]`)
- JWT via `lexik/jwt-authentication-bundle` v3.2.0 with RS256 signing + `gesdinet/jwt-refresh-token-bundle` for refresh tokens

**Go Stack — Generation Rules:**
- **Routing**: Go 1.22+ `net/http.ServeMux` with method+wildcard patterns (`GET /users/{id}`, `r.PathValue("id")`); use Chi v5.2.x only for middleware grouping/subrouters; avoid gorilla/mux (archived 2023), Gin/Fiber (diverge from `net/http` idioms)
- **Structure**: Feature-based `internal/` packages (`internal/user/handler.go`, `service.go`, `repository.go`); avoid layer-based `internal/handlers/` anti-pattern (excessive cross-package imports); shallow hierarchies (1-2 levels)
- **DI**: Constructor injection with small interfaces (1-3 methods) defined at consumer site; accept interfaces, return structs; wire manually in `main.go`; manual DI preferred over Wire/Dig except for very large projects
- **Database**: sqlc generates type-safe Go code from annotated SQL queries (`-- name: GetUser :one`); golang-migrate for sequential numbered up/down migration files
- **Validation**: go-playground/validator v10 (v10.27.0) with struct tags (`validate:"required,email"`); single instance (caches struct info); `WithRequiredStructEnabled()` for v11 compatibility; `RegisterTagNameFunc()` for JSON field names
- **OpenAPI**: oapi-codegen v2 generates Go types, server interfaces, and request validation middleware; developers implement `ServerInterface`; YAML config with Chi/stdlib backend support
- **Error Handling**: RFC 9457 via custom `ProblemDetail` struct; `Content-Type: application/problem+json`
- **Testing**: Table-driven tests with `httptest.NewRecorder()` + `httptest.NewRequest()`; `t.Run()` subtests; `t.Parallel()` for concurrent execution
- **Docker**: Multi-stage builds → 10-20MB images using `distroless/static-debian12`; `CGO_ENABLED=0` for static binaries; `-ldflags="-s -w"` to strip debug info
- **Graceful Shutdown**: `signal.NotifyContext` with 10-second timeout, closing HTTP server and database connections

**WebSocket Support (Optional — all stacks):**
- **Go**: coder/websocket, Hub pattern for connection management
- **Node.js**: ws / Socket.IO
- **PHP**: Ratchet / Swoole
- Auth: ephemeral single-use token via query parameter (`ws://host/ws?ticket=abc123`); 30-second TTL, consumed on first use to prevent log-exposure attacks
- SSE handles 95% of real-time use cases — suggest SSE first; SSE works over standard HTTP, supports auto-reconnection, multiplexed over HTTP/2

## Test Framework & Mutation Tool Recommendations

When generating scaffold, include test framework and mutation tool recommendations based on detected stack:

| Stack | Test Framework | Mutation Tool | Config File |
|-------|---------------|---------------|-------------|
| Node.js/TS | Vitest | StrykerJS | `stryker.config.mjs` |
| PHP/Laravel | Pest | Infection | `infection.json5` |
| Go | testing + testify | go-mutesting | CLI flags |
| Python | pytest | mutmut | `setup.cfg` |

Add to generated README: "Run `/jaan-to:qa-test-mutate` to validate test suite effectiveness."

## Anti-Patterns to NEVER Generate

**All Stacks:** Business logic in route handlers, hardcoded secrets, missing `.gitignore`, no error handling

**Node.js:** Direct Prisma calls in handlers, multiple PrismaClient instances, `any` types, Express-style error middleware, missing response serialization schemas, `instanceof ZodError` (use v6 helpers), missing `.js` extensions in ESM imports, `moduleResolution: "bundler"` for backends

**PHP:** Fat controllers, N+1 queries, exposing raw Eloquent models, `env()` outside config files, `utf8` instead of `utf8mb4`, missing Eloquent strictness modes

**Go:** Generic package names (`utils/`), global database connections, ignoring errors, unlimited connection pool, goroutine leaks, layer-based `internal/handlers/` structure

## Package Dependencies (Research-Validated)

**Node.js/TypeScript:**
- **Production**: `fastify` ^5.7, `@fastify/autoload` ^6, `@fastify/cors` ^10, `@fastify/sensible` ^6, `@fastify/swagger` ^9, `@fastify/swagger-ui` ^5, `@prisma/client` ^6, `fastify-plugin` ^5, `fastify-type-provider-zod` ^6.1, `zod` ^3.24
- **Dev**: `typescript` ^5.6, `@types/node` ^22, `fastify-tsconfig` ^2, `prisma` ^6, `tsx` ^4, `vitest` ^2, `eslint` ^9

**Go:** `chi` v5.2.x (optional), `go-playground/validator` v10, `golang-migrate`, `sqlc`, `oapi-codegen` v2

**PHP (Laravel):** `laravel/sanctum`, `crell/api-problem` ^3.8, `pestphp/pest` ^3

**PHP (Symfony):** `api-platform/core` ^4, `lexik/jwt-authentication-bundle` ^3.2, `gesdinet/jwt-refresh-token-bundle`

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Multi-stack support via `tech.md` detection
- Template-driven output structure
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

- [ ] All API endpoints from contract have route handlers
- [ ] All entities from data model have ORM models (Prisma/Eloquent/Doctrine/sqlc)
- [ ] Validation schemas generated for all request bodies
- [ ] Error handler covers validation errors, ORM errors, and generic errors
- [ ] Service layer stubs exist for all business logic
- [ ] DB singleton + graceful disconnect configured
- [ ] Setup README is complete and actionable
- [ ] Output follows v3.0.0 structure (ID, folder, index)
- [ ] Index updated with executive summary
- [ ] User approved final result
