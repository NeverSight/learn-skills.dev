---
name: vertical-slice-architecture
version: 1.0.0
description: Enforce Vertical Slice Architecture (VSA) when building applications in any language (Go, .NET/C#, Java, Kotlin, TypeScript, Python, etc.) and any type (web API, mobile backend, CLI, event-driven). Organize code by feature/use-case instead of technical layers. Each feature is a self-contained vertical slice with a single entry point that receives the router/framework handle and its dependencies. Use when the user says "vertical slice architecture", "VSA", "organizar por feature", "feature-based architecture", "slice architecture", or when building a new app or feature and the project already follows VSA conventions. Also use when reviewing or refactoring code to align with VSA principles.
---

# Vertical Slice Architecture

## Quick Reference: The 5 Rules

1. **One feature = one directory** containing handler, request/response types, validation, and tests
2. **One entry point per feature** — a setup/registration function that receives the router and dependencies. Name varies by convention (`Setup`, `RegisterRoute`, `Map`); the role is the invariant, not the name.
3. **Minimize coupling between slices, maximize coupling within a slice**
4. **No premature abstractions** — no shared repository/service layers until genuine duplication emerges across multiple slices
5. **Test each feature primarily through its entry point**, verifying outcomes (DB state, API calls, response). Platform/adapter tests are also encouraged.

## Project Structure

```
{project}/
  features/              # or internal/features/ (Go), Features/ (.NET)
    {domain}/            # orders/, users/, kvs/
      {operation}/       # create/, list/, delete/
        handler          # Single entry point + orchestration
        request/response # DTOs
        validator        # Input validation (optional)
        test             # Co-located integration test
        internal/        # Feature-private helpers (optional)
  platform/              # or Infrastructure/ — shared cross-cutting concerns
    middleware/           # Auth, error handling, idempotency
    database/            # Connection pooling, circuit breakers
    observability/       # Metrics, tracing, structured logging
    opqueue/             # Operation queues, outbox patterns (if needed)
  main                   # Composition root wires features + infrastructure
```

## Workflow: Adding a New Feature

1. Create directory: `features/{domain}/{operation}/`
2. Define the handler with a single exported setup function
3. Define request/response types (inline for simple cases)
4. Add validation logic
5. Register in the composition root (`main`)
6. Write integration test that calls the setup function, sends request, verifies outcomes

## Workflow: Adding Cross-Cutting Concerns

Place in `platform/` (not inside a feature). Examples:
- Auth middleware, error handling, request logging
- Database connection pooling, circuit breakers
- Idempotency middleware, operation queues, event notifications
- Observability (metrics, tracing, structured logging)

## Workflow: Extracting Shared Logic

Only extract when genuine duplication emerges across multiple slices (use judgment — the "3+ slices" heuristic is guidance, not a hard rule):
- Duplicate business rule: extract to a domain entity/value object
- Duplicate data access pattern: extract to a shared repository (only for that specific pattern)
- Duplicate HTTP helper: extract to `platform/httpx/`

## Key Decisions by Language

Detect the project's language/framework and consult the appropriate reference:
- **Patterns per language**: See [references/patterns-by-language.md](references/patterns-by-language.md) for Go, .NET, Java, TypeScript, Python
- **Testing per language**: See [references/testing.md](references/testing.md) for testcontainers, mock verification, integration test patterns
- **Core principles**: See [references/principles.md](references/principles.md) for detailed rules, anti-patterns, and shared domain model guidance

## Single Entry Point Contract

Every feature exposes one primary setup/registration function. Internal types stay private. The entry point name is conventional — the invariant is: **one public function per feature that wires the slice to the framework**.

| Language | Convention | Signature | DI mechanism |
|----------|-----------|-----------|--------------|
| Go | `Setup` or `RegisterRoute` | `func Setup(r gin.IRoutes, repo Repository)` | Explicit params |
| .NET | `Map` (static) | `static void Map(IEndpointRouteBuilder app)` | DI container resolves deps in handler |
| Java/Kotlin | `@RestController` class | Controller discovered by component scan | Spring DI (constructor injection) |
| TypeScript | `setup` | `function setup(router: Router, db: Database): void` | Explicit params |
| Python | `setup` | `def setup(router: APIRouter, db: Database) -> None` | Explicit params or `Depends()` |

**Exceptions**: Versioned APIs may have `SetupV1`/`SetupV2` wrappers sharing internal handler wiring. Frameworks with auto-discovery (Spring, NestJS) use the controller/module class itself as the entry point.

## Testing

See [references/testing.md](references/testing.md) for full testing strategy per language, including feature integration tests, platform/adapter tests, mock verification patterns, and test naming conventions.
