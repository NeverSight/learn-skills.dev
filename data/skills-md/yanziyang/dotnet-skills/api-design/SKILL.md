---
name: api-design
description: REST API design patterns for .NET / ASP.NET Core (net8.0–net10.0) including resource naming, status codes, ProblemDetails error responses, pagination, filtering, versioning, and rate limiting for production APIs. Use this skill whenever designing or reviewing ASP.NET Core endpoints (Minimal APIs or controllers), adding list endpoints, returning errors from an API, choosing status codes, or when the user mentions REST, endpoints, Web API, pagination, API versioning, or rate limits — even if they don't say "API design" explicitly.
metadata:
  origin: dotnet-skills
  targets: ASP.NET Core on .NET 8, 9, and 10
---

# API Design Patterns for .NET

Conventions and best practices for designing consistent, production-grade REST APIs with ASP.NET Core. Code samples use Minimal APIs on .NET 10; everything applies to .NET 8+ and controllers unless noted.

## When to Activate

- Designing new API endpoints (Minimal APIs or MVC controllers)
- Reviewing existing API contracts
- Adding pagination, filtering, or sorting to list endpoints
- Implementing error handling and validation responses
- Planning API versioning strategy
- Building public or partner-facing APIs

## Reference Files — Read Before Implementing

Read the matching reference file BEFORE writing code for that concern. Do not improvise these from memory:

| Task | Read |
|------|------|
| Error responses, exception handling, validation | [references/error-handling.md](references/error-handling.md) |
| Pagination, filtering, sorting, search | [references/pagination-filtering.md](references/pagination-filtering.md) |
| API versioning (Asp.Versioning setup, deprecation) | [references/versioning.md](references/versioning.md) |
| Rate limiting (policies, 429 responses, headers) | [references/rate-limiting.md](references/rate-limiting.md) |

## Resource Design

### URL Structure

```
# Resources are nouns, plural, lowercase, kebab-case
GET    /api/v1/users
GET    /api/v1/users/{id}
POST   /api/v1/users
PUT    /api/v1/users/{id}
PATCH  /api/v1/users/{id}
DELETE /api/v1/users/{id}

# Sub-resources for relationships
GET    /api/v1/users/{id}/orders
POST   /api/v1/users/{id}/orders

# Actions that don't map to CRUD (use verbs sparingly, always POST)
POST   /api/v1/orders/{id}/cancel
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
```

### Naming Rules

```
# GOOD
/api/v1/team-members          # kebab-case for multi-word resources
/api/v1/orders?status=active  # query params for filtering
/api/v1/users/123/orders      # nested resources for ownership

# BAD
/api/v1/getUsers              # verb in URL
/api/v1/user                  # singular (use plural)
/api/v1/team_members          # snake_case in URLs
/api/v1/TeamMembers           # PascalCase in URLs
```

Enforce lowercase URLs globally:

```csharp
builder.Services.Configure<RouteOptions>(options =>
{
    options.LowercaseUrls = true;
    options.LowercaseQueryStrings = true;
});
```

### Route Groups

Organize Minimal API endpoints with `MapGroup` so shared conventions (prefix, auth, filters, tags) are declared once:

```csharp
var users = app.MapGroup("/api/v1/users")
    .WithTags("Users")
    .RequireAuthorization();

users.MapGet("/", GetUsers);
users.MapGet("/{id:guid}", GetUser);
users.MapPost("/", CreateUser);
users.MapPut("/{id:guid}", UpdateUser);
users.MapDelete("/{id:guid}", DeleteUser);
```

Use route constraints (`{id:guid}`, `{id:int}`) so malformed IDs return 404 from routing instead of reaching your handler.

## HTTP Methods and Status Codes

### Method Semantics

| Method | Idempotent | Safe | Use For |
|--------|-----------|------|---------|
| GET | Yes | Yes | Retrieve resources; never mutate state |
| POST | No | No | Create resources, trigger actions |
| PUT | Yes | No | Full replacement of a resource |
| PATCH | No* | No | Partial update of a resource |
| DELETE | Yes | No | Remove a resource |

*PATCH can be made idempotent with proper implementation.

### Status Code Reference

```
# Success
200 OK                    — GET, PUT, PATCH (with response body)
201 Created               — POST (include Location header — use TypedResults.Created)
202 Accepted              — Long-running work queued (return status URL)
204 No Content            — DELETE, PUT (no response body)

# Client Errors
400 Bad Request           — Validation failure, malformed JSON
401 Unauthorized          — Missing or invalid authentication
403 Forbidden             — Authenticated but not authorized
404 Not Found             — Resource doesn't exist (also for others' resources, see below)
409 Conflict              — Duplicate entry, concurrency/state conflict
422 Unprocessable Entity  — Semantically invalid (valid JSON, bad data)
429 Too Many Requests     — Rate limit exceeded (include Retry-After)

# Server Errors
500 Internal Server Error — Unexpected failure (never expose details)
502 Bad Gateway           — Upstream service failed
503 Service Unavailable   — Temporary overload, include Retry-After
```

### Return TypedResults, Not Results

Always use `TypedResults` with a `Results<...>` union return type. The compiler then enforces which status codes the endpoint can return, and OpenAPI metadata is inferred automatically — no `[ProducesResponseType]` attributes needed:

```csharp
private static async Task<Results<Ok<UserResponse>, NotFound>> GetUser(
    Guid id, AppDbContext db, CancellationToken ct)
{
    var user = await db.Users
        .Where(u => u.Id == id)
        .Select(u => new UserResponse(u.Id, u.Email, u.Name, u.CreatedAt))
        .FirstOrDefaultAsync(ct);

    return user is null ? TypedResults.NotFound() : TypedResults.Ok(user);
}

private static async Task<Results<Created<UserResponse>, Conflict<ProblemDetails>>> CreateUser(
    CreateUserRequest request, AppDbContext db, CancellationToken ct)
{
    if (await db.Users.AnyAsync(u => u.Email == request.Email, ct))
    {
        return TypedResults.Conflict(new ProblemDetails
        {
            Title = "Email already registered.",
            Status = StatusCodes.Status409Conflict,
        });
    }

    var user = new User { Id = Guid.NewGuid(), Email = request.Email, Name = request.Name };
    db.Users.Add(user);
    await db.SaveChangesAsync(ct);

    var response = new UserResponse(user.Id, user.Email, user.Name, user.CreatedAt);
    return TypedResults.Created($"/api/v1/users/{user.Id}", response);
}
```

Rules:
- Accept a `CancellationToken` in every handler and pass it to all async calls.
- Never return entities directly — always project to response DTOs (records) so internal fields never leak.
- `404` vs `403`: when a user requests a resource owned by someone else, prefer `404` (avoids leaking existence). Use `403` only when it's not sensitive that the resource exists.

### Common Mistakes

```
# BAD: 200 for everything
{ "status": 200, "success": false, "error": "Not found" }

# GOOD: use HTTP status codes semantically; errors are ProblemDetails
HTTP/1.1 404 Not Found
Content-Type: application/problem+json

# BAD: 500 for validation errors        → use 400 with ValidationProblemDetails
# BAD: 200 for created resources        → use 201 + Location header
# BAD: catching exceptions per-endpoint → use global IExceptionHandler
```

## Request and Response Shape

### DTOs Are Records, JSON Is camelCase

```csharp
public sealed record CreateUserRequest(
    [property: Required, EmailAddress] string Email,
    [property: Required, StringLength(100, MinimumLength = 1)] string Name);

public sealed record UserResponse(Guid Id, string Email, string Name, DateTimeOffset CreatedAt);
```

- System.Text.Json web defaults already produce camelCase (`createdAt`) — do not override with snake_case for new APIs.
- Use `DateTimeOffset` (serialized as ISO 8601 with offset) for all timestamps; store and return UTC.
- Use `Guid` (or a ULID/string id) for public identifiers — never expose auto-increment integers on public APIs.
- Separate request and response DTOs per operation. Never reuse an EF entity as a DTO.

Configure enum serialization as strings once, globally:

```csharp
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.Converters.Add(new JsonStringEnumConverter(JsonNamingPolicy.CamelCase));
    options.SerializerOptions.DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull;
});
```

### Single Resource Response

Return the DTO directly (no envelope) — the status code carries success/failure:

```json
{
  "id": "0198c5f3-...",
  "email": "alice@example.com",
  "name": "Alice",
  "createdAt": "2026-07-09T10:30:00+00:00"
}
```

### Collection Response

Always wrap collections in a paged envelope — never return a bare JSON array (can't add metadata later without a breaking change). See [references/pagination-filtering.md](references/pagination-filtering.md) for the `PagedResponse<T>` implementation.

```json
{
  "items": [ { "id": "...", "name": "Alice" } ],
  "page": 1,
  "pageSize": 20,
  "totalCount": 142,
  "totalPages": 8
}
```

### Error Response

All errors — validation, not found, conflicts, crashes — use RFC 9457 `application/problem+json` via ASP.NET Core's built-in `ProblemDetails`. Never invent a custom error envelope. See [references/error-handling.md](references/error-handling.md) for full setup.

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "email": ["The Email field is not a valid e-mail address."],
    "name": ["The Name field is required."]
  }
}
```

## Validation

On .NET 10, enable built-in Minimal API validation — data annotations on request DTOs are validated automatically and return 400 `ValidationProblemDetails`:

```csharp
builder.Services.AddValidation();   // .NET 10+, validates [Required] etc. on minimal API parameters
```

On .NET 8/9, or for complex rules (cross-field, async, DB lookups), use FluentValidation with an endpoint filter. Full pattern in [references/error-handling.md](references/error-handling.md).

## Authentication and Authorization

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer();                       // config from appsettings "Authentication:Schemes:Bearer"

builder.Services.AddAuthorizationBuilder()
    .AddPolicy("Admin", policy => policy.RequireRole("admin"));

app.UseAuthentication();
app.UseAuthorization();
```

Apply auth at the group level; opt out explicitly for public endpoints:

```csharp
var api = app.MapGroup("/api/v1").RequireAuthorization();
api.MapGet("/health", () => Results.Ok()).AllowAnonymous();
api.MapDelete("/users/{id:guid}", DeleteUser).RequireAuthorization("Admin");
```

Always enforce resource-level ownership in the handler — role checks alone are not enough:

```csharp
private static async Task<Results<Ok<OrderResponse>, NotFound>> GetOrder(
    Guid id, ClaimsPrincipal principal, AppDbContext db, CancellationToken ct)
{
    var userId = Guid.Parse(principal.FindFirstValue(ClaimTypes.NameIdentifier)!);
    var order = await db.Orders
        .Where(o => o.Id == id && o.UserId == userId)   // ownership in the query itself
        .Select(o => new OrderResponse(o.Id, o.Total, o.Status))
        .FirstOrDefaultAsync(ct);

    return order is null ? TypedResults.NotFound() : TypedResults.Ok(order);
}
```

## OpenAPI

.NET 9+ has built-in OpenAPI document generation (no Swashbuckle needed):

```csharp
builder.Services.AddOpenApi();     // Microsoft.AspNetCore.OpenApi

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();              // serves /openapi/v1.json
}
```

Give every endpoint a name and summary so the generated spec is usable:

```csharp
users.MapGet("/{id:guid}", GetUser)
    .WithName("GetUser")
    .WithSummary("Get a user by id");
```

With `TypedResults` union return types, response status codes and schemas appear in the spec automatically.

## Program.cs Middleware Order

Middleware order matters. Use this order:

```csharp
var app = builder.Build();

app.UseExceptionHandler();      // global ProblemDetails for unhandled exceptions
app.UseStatusCodePages();       // ProblemDetails bodies for bare 404/405/415
app.UseHttpsRedirection();
app.UseRateLimiter();
app.UseAuthentication();
app.UseAuthorization();

// ... MapGroup / endpoints ...

app.Run();
```

## API Design Checklist

Before shipping a new endpoint, verify every item:

- [ ] URL follows conventions (plural nouns, kebab-case, lowercase, no verbs)
- [ ] Route constraints on parameters (`{id:guid}`)
- [ ] Correct HTTP method and status codes (`201` + Location for creates, `204` for deletes)
- [ ] Handler returns `TypedResults` with a `Results<...>` union type
- [ ] Request/response are dedicated record DTOs — no EF entities on the wire
- [ ] Input validated (data annotations + `AddValidation()`, or FluentValidation filter)
- [ ] All errors are RFC 9457 ProblemDetails (no custom error envelope)
- [ ] List endpoints paginated with capped page size, wrapped in `PagedResponse<T>`
- [ ] `CancellationToken` accepted and propagated
- [ ] Authentication required (or `AllowAnonymous` is an explicit, deliberate choice)
- [ ] Ownership enforced in the query for user-scoped resources (404 for others' resources)
- [ ] Rate limiting policy applied
- [ ] No internal details leak (stack traces, SQL, entity fields)
- [ ] Endpoint has `WithName`/`WithSummary` for OpenAPI
