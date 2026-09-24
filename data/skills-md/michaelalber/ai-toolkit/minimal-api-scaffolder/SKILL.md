---
name: minimal-api-scaffolder
audience: team
description: >
  Scaffolds .NET 10 Minimal API endpoints with OpenAPI documentation, versioning strategies, and
  security patterns. Use when creating REST APIs, adding endpoints, setting up API projects, or
  configuring API infrastructure. Do NOT use when the project is controller-based MVC — use
  dotnet-vertical-slice for handler architecture instead.
---

# .NET 10 Minimal API Scaffolder

> "Minimal APIs are ideal for microservices and apps that want to include only the minimum files, features, and dependencies in ASP.NET Core."
> -- Microsoft Documentation

> "A good API is not just easy to use but also hard to misuse."
> -- Joshua Bloch

## Core Philosophy

This skill scaffolds and maintains Minimal API endpoints in .NET 10 projects with OpenAPI documentation, versioning, and security configured from the start. Every API begins with a clear contract, validated inputs, and documented responses.

**Non-Negotiable Constraints:**

1. **OpenAPI-First Design** — Every endpoint must have OpenAPI metadata: name, summary, request/response types, and status codes. No endpoint ships without `.WithName()`, `.WithSummary()`, and `.Produces<T>()`.
2. **Versioning from Day One** — API versioning is configured at project creation, not retrofitted. Every endpoint group includes a version segment. There is no "we'll add versioning later."
3. **Security by Default** — Groups default to `.RequireAuthorization()`. Anonymous access is an explicit opt-in via `.AllowAnonymous()`, never an implicit default.
4. **Convention over Configuration** — Every new endpoint group mirrors the established convention: group creation with tags, OpenAPI metadata, typed results, and FluentValidation integration.
5. **Typed Results, Not Raw Responses** — All handlers return `TypedResults` with explicit union return types (`Results<Ok<T>, NotFound, ValidationProblem>`). No raw `IResult`, no untyped `Results.Ok()`, no status code magic numbers.

## Domain Principles Table

| # | Principle | Description | Priority |
|---|-----------|-------------|----------|
| 1 | **Endpoint Grouping** | Related endpoints are organized into static extension method classes (e.g., `UsersEndpoints`). Each group maps a resource to a route prefix with shared tags, authorization, and OpenAPI settings. | Critical |
| 2 | **Request/Response Models** | All request and response types are C# records. Request models use `[AsParameters]` for GET queries. No anonymous objects, no `dynamic`, no `Dictionary<string, object>`. | Critical |
| 3 | **FluentValidation Integration** | Every mutating endpoint (POST, PUT, PATCH) injects and executes `IValidator<TRequest>` before processing. Validation is explicit in the handler, not hidden in middleware. | Critical |
| 4 | **OpenAPI Documentation** | Every endpoint declares `.WithName()`, `.WithSummary()`, `.Produces<T>()` for all possible status codes, and `.Accepts<T>()` for request bodies. | Critical |
| 5 | **Versioning Strategy** | The project chooses a versioning strategy at setup time and applies it consistently. URL versioning (`/api/v{version:apiVersion}/`) is the recommended default. | High |
| 6 | **Authorization Patterns** | Endpoint groups default to requiring authorization. Individual endpoints may override with specific policies or `.AllowAnonymous()`. Policies are defined in `Program.cs`. | Critical |
| 7 | **Rate Limiting** | Public and high-traffic endpoints configure rate limiting policies defined as named policies in `Program.cs` and applied with `.RequireRateLimiting()`. | High |
| 8 | **Error Handling** | Errors return RFC 7807 Problem Details via `TypedResults.Problem()` or `TypedResults.ValidationProblem()`. A global exception handler produces consistent `application/problem+json` responses. | High |
| 9 | **CORS Configuration** | CORS origins are explicitly configured per environment. Never use `AllowAnyOrigin()` in production. Production must whitelist specific origins loaded from configuration. | High |
| 10 | **Health Checks** | Every API project includes health check endpoints (`/health`, `/health/ready`, `/health/live`) mapped with `.AllowAnonymous()`. Database connectivity is included in readiness checks. | Medium |

## Knowledge Base Lookups

| Query | When to Call |
|-------|--------------|
| `search_knowledge("ASP.NET Core Minimal API endpoint group TypedResults .NET 10")` | At SCAFFOLD phase — confirms current Minimal API patterns and TypedResults syntax |
| `search_knowledge("ASP.NET Core API versioning URL header query string")` | During CONFIGURE phase — authoritative versioning strategies and setup |
| `search_knowledge("ASP.NET Core authentication JWT bearer authorization policy")` | During SECURE phase — confirms authentication pipeline and policy setup |
| `search_knowledge("OpenAPI Swagger ASP.NET Core endpoint metadata WithName Produces")` | During DOCUMENT phase — authoritative OpenAPI metadata decoration patterns |
| `search_knowledge("ASP.NET Core rate limiting policy RequireRateLimiting")` | When configuring rate limiting — confirms rate limiter registration and application |
| `search_knowledge("ASP.NET Core health checks ready live endpoints")` | When scaffolding health checks — confirms health check endpoint patterns |

Search before each scaffold phase. Generated code must use KB-confirmed API signatures — never training-data assumptions about .NET versioned APIs. Cite source paths in generated file headers.

## Workflow

The scaffold lifecycle flows: **CONFIGURE → SCAFFOLD → SECURE → DOCUMENT**. Each phase has a verification checklist before advancing to the next.

### Phase 1: CONFIGURE

Set up the project foundation before any endpoints are created.

- [ ] Create or verify `.csproj` with required packages (see `references/endpoint-patterns.md`)
- [ ] Configure `Program.cs` with service registrations: OpenAPI, versioning, FreeMediator, FluentValidation, DbContext
- [ ] Set up authentication and authorization pipeline
- [ ] Configure API versioning strategy (URL recommended)
- [ ] Register rate limiting policies
- [ ] Configure CORS for target environments

### Phase 2: SCAFFOLD

Create endpoint groups, request/response models, and validators.

- [ ] Create endpoint group static class with extension method pattern
- [ ] Define all CRUD operations with typed results
- [ ] Create request records for each mutating operation
- [ ] Create response DTOs for each query operation
- [ ] Implement FluentValidation validators for all request models
- [ ] Wire endpoint group into `Program.cs` via `api.Map{Resource}Endpoints()`

### Phase 3: SECURE

Apply authorization, rate limiting, and CORS to all endpoints.

- [ ] Apply `.RequireAuthorization()` to endpoint groups
- [ ] Define and apply specific policies for sensitive operations
- [ ] Apply rate limiting to public-facing or high-traffic endpoints
- [ ] Verify CORS is configured for all consuming origins
- [ ] Add health check endpoints with anonymous access
- [ ] Verify authentication middleware is in the pipeline

### Phase 4: DOCUMENT

Ensure every endpoint is fully documented via OpenAPI metadata.

- [ ] Verify every endpoint has `.WithName()` and `.WithSummary()`
- [ ] Verify every endpoint declares all `.Produces<T>()` responses
- [ ] Add `.WithDescription()` for complex endpoints
- [ ] Test Swagger UI renders correctly for all versions
- [ ] Verify versioned Swagger docs are accessible
- [ ] Confirm request/response schemas appear in OpenAPI spec

## State Block Format

```
<api-scaffold-state>
mode: SCAFFOLD
project_name: MyApp.Api
dotnet_version: net10.0
endpoints_created: [UsersEndpoints]
versioning_strategy: url
auth_configured: true
openapi_configured: true
last_action: Scaffolded UsersEndpoints with full CRUD
next_action: Create OrdersEndpoints group
</api-scaffold-state>
```

## Output Templates

```markdown
## API Project: [Name] | .NET 10 | Versioning: [URL/Header/Query] | Auth: [JWT/Azure AD]
Packages: Swashbuckle, Asp.Versioning.Http, FluentValidation, FreeMediator

## Endpoint Group: [Resource]
Base Path: /api/v{version}/[resource] | Auth: Required | Rate Limited: [Yes/No]
| Method | Path | Name | Request Type | Response Type | Auth Override |
| GET / | GET /{id} | POST / | PUT /{id} | DELETE /{id} |
Error responses: 400 Validation | 401 Auth | 403 Forbidden | 404 Not Found | 500 Server Error
```

Full templates (Project Setup Checklist with packages, Endpoint Group Report with request/response schemas, Validation Report, API Documentation Summary): `references/endpoint-patterns.md`

## AI Discipline Rules

**Always add FluentValidation to mutating endpoints.** Every POST, PUT, and PATCH handler must inject `IValidator<TRequest>`, call `ValidateAsync()` before any business logic, and return `TypedResults.ValidationProblem(validation.ToDictionary())` on failure. The return type must be a union type — `Results<Created<T>, ValidationProblem>` — not raw `IResult`. Never rely on model binding validation alone.

**Never create endpoints without OpenAPI metadata.** Every endpoint must have `.WithName("OperationId")`, `.WithSummary("brief description")`, `.Produces<T>(statusCode)` for every possible response, and `.Accepts<T>()` for request bodies. An endpoint without this metadata is invisible to API consumers and tooling.

**Always configure CORS explicitly per environment.** Never use `AllowAnyOrigin()` outside development. Origins must be loaded from configuration, not hardcoded. Apply CORS in the middleware pipeline before authentication. Allow credentials only when specific origins are listed.

**Use TypedResults with union return types.** All handlers must return `TypedResults` with explicit union types declared in the method signature (`Results<Ok<UserDto>, NotFound>`). No raw strings, magic status codes, or untyped `IResult` in endpoint bodies.

**Enforce structural versioning and one group per resource.** Version segments must appear in the route template — use `app.NewVersionedApi()` with `.HasApiVersion()` on groups. One `Map{Resource}Endpoints()` extension method per resource, called from a single location in `Program.cs`. When a breaking change occurs, create a new version-specific endpoint class; never add conditional logic inside an existing handler.

## Anti-Patterns Table

| # | Anti-Pattern | Problem | Correct Approach |
|---|-------------|---------|------------------|
| 1 | **Fat Program.cs** | All registrations and middleware in one massive file | Extract endpoint groups to static extension classes |
| 2 | **Endpoints Without Validation** | Request data flows directly to business logic without validation | Always inject and call `IValidator<T>` in mutating endpoints |
| 3 | **Missing OpenAPI Tags** | Endpoints appear ungrouped in Swagger UI, making the API undiscoverable | Apply `.WithTags()` at group level, `.WithName()`/`.WithSummary()` on every endpoint |
| 4 | **Hardcoded CORS Origins** | Origins embedded in `Program.cs` cannot change per environment | Load origins from `appsettings.json` or environment variables |
| 5 | **No Versioning Strategy** | API changes break existing clients with no migration path | Configure versioning at project creation; use URL versioning as default |
| 6 | **Mixing Controllers and Minimal APIs** | Two routing systems in one project create confusion about conventions | Choose one approach per project |
| 7 | **Returning Raw Strings** | `Results.Ok("success")` provides no type safety and no OpenAPI schema | Use `TypedResults.Ok(typedObject)` with strongly typed response records |
| 8 | **Catch-All Exception Handlers in Endpoints** | `try/catch` in every handler duplicates error handling logic | Use global exception handler middleware; let exceptions propagate |
| 9 | **Anonymous Endpoints by Default** | Forgetting `.RequireAuthorization()` leaves endpoints publicly accessible | Apply auth at the group level; `.AllowAnonymous()` as explicit opt-in |
| 10 | **Inline Lambda Handlers** | Complex logic inside `MapGet("/", async (ctx) => {...})` is untestable | Extract handlers to named static methods; inject dependencies as parameters |

## Error Recovery

**Project already has controllers**: Do NOT convert existing controllers in place. Create a `Features/` directory alongside existing `Controllers/`. Configure both `app.MapControllers()` and minimal API groups in `Program.cs`. Migrate one resource at a time — create the minimal API endpoint group, verify it works, then deprecate the controller. Ask the developer before mixing paradigms; a gradual migration is acceptable, a hybrid architecture with no migration plan is not.

**Conflicting versioning approaches** (URL in some places, header in others): Identify the dominant strategy already in use. Configure `ApiVersionReader.Combine()` to support existing clients during migration. Standardize all new endpoints on URL versioning. Document the canonical approach. Never remove a working version reader without a client migration plan.

**OpenAPI generation failures** (Swagger UI fails or shows missing schemas): Check for endpoints missing `.Produces<T>()` — Swashbuckle cannot infer response types from minimal APIs. Verify all response types are public records (internal types are invisible). Check for duplicate `.WithName()` values (operation IDs must be unique). Inspect `/swagger/v1/swagger.json` directly for schema errors. Verify `app.UseSwagger()` and `app.UseSwaggerUI()` are in the correct pipeline order.

**Rate limiting not taking effect**: Verify `app.UseRateLimiter()` is in the pipeline after routing and before auth. Confirm rate limiter policy names match the names used in `.RequireRateLimiting("PolicyName")`. Test under load with `bombardier` or `hey`. Verify the `OnRejected` handler returns 429 responses.

## Integration with Other Skills

| Skill | Integration Point | When to Use |
|-------|-------------------|-------------|
| **dotnet-vertical-slice** | Feature architecture for handlers behind endpoints | Scaffold CQRS handlers, commands, queries, and validators that endpoint groups delegate to |
| **dotnet-architecture-checklist** | Review scaffolded API projects | Run after scaffolding to verify architectural best practices |
| **test-scaffold** | Generate API integration tests | Create test classes exercising endpoints via `WebApplicationFactory<Program>` |
| **dotnet-security-review** | Security audit of API configuration | Verify JWT configuration, authorization policies, CORS settings, and rate limiting |
| **ef-migration-manager** | Database setup for API data access | Use when endpoints need new entities or schema changes |

References: `references/endpoint-patterns.md` (full endpoint group templates, request models, validators, OpenAPI patterns, error handling) | `references/versioning-strategies.md` (URL/header/query versioning with deprecation) | `references/security-patterns.md` (authorization, rate limiting, CORS, health checks, JWT setup)
