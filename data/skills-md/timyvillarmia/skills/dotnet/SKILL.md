---
name: dotnet
description: Engineering standards, architectural guidance, and validation workflows for modern .NET and C# development. Make sure to use this skill whenever building, modifying, debugging, reviewing, or architecting .NET/C# code or working with .cs, .csproj, .sln, or .slnx files—even if the user only mentions symptoms or ecosystem tools like ASP.NET Core Minimal APIs, OpenAPI, Native AOT, EF Core (DbContext), zero-downtime migrations, BackgroundService/channels, OpenTelemetry, Testcontainers/WebApplicationFactory, WolverineFx/MassTransit/outbox, multi-tenancy, concurrency, auth/security, rate limiting (AddRateLimiter), HybridCache, ResiliencePipeline, IOptions/ValidateOnStart, webhooks, performance, or NuGet dependency/license choices.
license: MIT
metadata:
  author: Timy
  version: "1.1.2"
---

# .NET Engineering

Use this skill as the default engineering guide for modern .NET work. It provides general .NET engineering principles, task classification, reference routing, dependency decisions, and validation. Repository-specific instructions, established conventions, and explicit task requirements take precedence.

## Target version

- Greenfield: default to `net10.0` (LTS) and C# 14.
- Existing repos: read `<TargetFramework>`/`<LangVersion>` in `.csproj`, `Directory.Build.props`, and `global.json` first. Do not use APIs or syntax newer than the target. Version labels like "(.NET 9+)" in references mark minimum versions.
- Lifecycle awareness: .NET 8 and .NET 9 reached EOL on November 10, 2026. Respect the repository's existing `<TargetFramework>` for code compatibility, but flag EOL target frameworks when reviewing or planning upgrades.

## Core principles

- Understand the repository before changing it.
- Prefer the simplest correct solution that satisfies the requirement.
- Preserve existing project conventions unless there is a concrete reason to change them.
- Prefer framework/platform capabilities before introducing custom infrastructure.
- Minimize unnecessary dependencies, not dependencies at all costs.
- Do not add a third-party dependency merely because a library exists.
- Do not implement security-sensitive primitives yourself merely to avoid a dependency.
- Prefer explicit behavior over magic, hidden conventions, and unnecessary abstraction.
- Optimize for correctness, maintainability, observability, and performance together.
- Measure performance before making optimization claims.
- Make surgical changes; avoid unrelated refactoring.

## Instruction precedence

When guidance conflicts, use this order:

1. Security and correctness constraints.
2. Explicit task requirements.
3. Repository/project-specific instructions and conventions.
4. Existing architectural decisions.
5. This skill and its references.
6. Personal/default technology preferences.
7. Agent preferences.

An existing dependency or architecture is not automatically wrong because it differs from a preferred default. Change it only when the task requires it or the benefit clearly justifies the migration cost.

## Classify the task

Before implementation, determine the smallest set of concerns involved:

| Task involves | Action |
|---|---|
| C# syntax, idioms, type-system design, async patterns, AOT, or modernization | Read `references/csharp.md` when the task depends on language behavior, source generators, or version-sensitive syntax |
| ASP.NET Core HTTP APIs, endpoints, OpenAPI, error handling | Read `references/api.md` when the task touches HTTP surface, status codes, problem details, exception handlers, or API contracts |
| Observability, OpenTelemetry, metrics, structured logs, health checks | Read `references/observability.md` when configuring tracing, metrics, LoggerMessage, data redaction, or health endpoints |
| Background work, hosted services, periodic jobs, channels | Read `references/hosted-services.md` when implementing BackgroundService, periodic timers, producer/consumer channels, or shutdown lifecycles |
| Architecture, boundaries, CQRS, Vertical Slice | Read `references/architecture.md` when the task changes structure, dependency direction, or module boundaries |
| EF Core, queries, modeling, transactions, migrations | Read `references/efcore.md` when the task touches DbContext, LINQ, persistence, outbox, or schema evolution |
| Zero-downtime migrations, schema evolution, lock-safe DDL | Read `references/database-migrations.md` when adding, modifying, or removing database columns or indexes in production |
| Distributed messaging, outbox pattern, WolverineFx, MassTransit, message brokers | Read `references/messaging.md` when publishing/consuming messages across processes, brokers, or outbox tables |
| Multi-tenancy, tenant isolation, global query filters | Read `references/multi-tenancy.md` when isolating tenant data, resolving tenant contexts, or isolating tenant caches |
| Application configuration, Options pattern, User Secrets, feature flags | Read `references/configuration.md` when binding `IOptions<T>`/`IOptionsSnapshot<T>`/`IOptionsMonitor<T>`, configuring `[OptionsValidator]`/`ValidateOnStart()`, handling env vars/User Secrets, or evaluating `Microsoft.FeatureManagement` |
| Caching, HybridCache, HTTP Output Caching, cache invalidation | Read `references/caching.md` when caching data or HTTP responses, configuring L1/L2 TTLs, preventing cache stampedes, or evicting by tag |
| Outbound HTTP resilience, ResiliencePipeline, retries, circuit breakers, timeouts | Read `references/resilience.md` when configuring `AddStandardResilienceHandler`, `AddResiliencePipeline`, retry/backoff policies, timeout budgets, or `Retry-After` handling |
| Testing, integration tests, Testcontainers, WebApplicationFactory, MTP | Read `references/testing.md` when designing, writing, repairing, or scaffolding tests |
| Concurrency, thread safety, locks, Parallel.ForEachAsync | Read `references/concurrency.md` when coordinating parallel tasks, async locks, or race conditions |
| A measured or suspected performance problem | Read `references/performance.md` when performance is a requirement; if the bottleneck is database/EF, also read `references/efcore.md` |
| Authentication, authorization, untrusted input, secrets | Read `references/security.md` when the task handles identity, access control, or attacker-reachable input |
| Reviewing a diff, PR, or completed change | Read `references/review.md` when reviewing rather than implementing |
| Finding evidence for packages, APIs, or version diffs | Search NuGet, inspect project packages, or use official documentation |
| .NET Aspire-specific workflow or current Aspire APIs | Use the official Aspire Agent Skill when available |

If a task crosses multiple areas, read only the smallest combination of references that covers the affected decisions. Do not load unrelated references merely because they exist.

## Before implementation

1. Inspect repository instructions and relevant agent guidance.
2. Identify the target .NET SDK, C# language version, frameworks, and package versions.
3. Locate application boundaries, entry points, tests, and affected code paths.
4. Understand existing architecture, dependency direction, and data flow.
5. Translate the task into concrete behavioral and technical requirements.
6. Classify the task and read only the relevant references.
7. Check whether the required capability already exists in the framework or an existing dependency.
8. For a new dependency, evaluate complexity, maintenance, security, performance, licensing, and whether a small explicit implementation would be sufficient.

Do not ask questions that repository inspection can answer.

## Scale the process to the task

Match investigation, implementation, and validation depth to scope, risk, and uncertainty.

- **Tiny change:** inspect the necessary context, make the smallest correct change, and run focused validation.
- **Normal feature:** inspect affected architecture, dependencies, call sites, and relevant tests; use applicable references.
- **Cross-cutting, security-sensitive, performance-sensitive, data-sensitive, or architectural change:** broaden investigation and validation proportionally.

Do not perform heavyweight architectural analysis or broad refactoring for a trivial change without a concrete reason.

## Gotchas and Anti-Patterns

Never generate these anti-patterns:
- **`async void`:** Swallows exceptions and cannot be awaited. Always return `Task` (or `ValueTask`) except in event handlers.
- **Sync-over-async blocking:** `Task.Result`, `.Wait()`, or `.GetAwaiter().GetResult()` cause thread exhaustion and deadlocks in ASP.NET contexts. Await all asynchronous calls.
- **`DateTime.Now` / `DateTime.UtcNow` in time-dependent logic:** Untestable and timezone-dependent when branching on deadlines, expirations, or schedules. Inject `TimeProvider` and use `FakeTimeProvider` in tests.
- **Direct `new HttpClient()`:** Causes socket exhaustion and ignores DNS rotation. Inject `IHttpClientFactory` or use configured typed clients.
- **Generic Repository over EF Core:** Wraps an already robust unit of work (`DbContext`) in redundant abstraction layers. Inject `DbContext` directly into handlers.
- **Exceptions for expected control flow:** Throwing exceptions for predictable outcomes (e.g., validation or not-found) incurs stack-trace overhead. Follow the repository's error model; in greenfield code, prefer a typed `Result` or `ErrorOr`.
- **Target framework vs Language version:** Target framework is not language version: verify `LangVersion` and SDK defaults independently before using newer C# syntax.
- **EF Core in-memory providers:** In-memory providers are not relational substitutes: do not claim relational behavior (constraints, transactions, concurrency) is verified without a relational provider. Use `Testcontainers`.
- **Startup migrations:** Racing migrations across multiple instances at startup risks deployment corruption. Prefer explicit migration scripts or isolated migration bundles.
- **`TypedResults` vs `IResult`/`Results`:** Follow the surrounding API's established return style; do not mix both without a reason.
- **Tenant/Role security:** Client-supplied tenant/role identifiers are not authorization proof: enforce scope server-side at the resource boundary.
- **Deprecated OpenAPI annotations:** Do not call `.WithOpenApi()`; it is deprecated in .NET 10 (`ASPDEPR002`). ASP.NET Core built-in OpenAPI tracks endpoints automatically.
- **`IConfiguration` injected into services or handlers:** String keys bypass startup validation and hide missing-config errors until runtime execution. Bind and validate strongly typed `IOptions<T>` with `ValidateOnStart()` instead.
- **Culture-sensitive parsing or formatting of machine data:** Ambient `CultureInfo.CurrentCulture` corrupts numbers and dates on non-US locales (e.g., `,` vs `.` decimal separators). Pass `CultureInfo.InvariantCulture` (or ISO 8601) for logs, protocols, and persistence.
- **Buffering large uploads with `IFormFile`:** Buffers entire files above 64 KB to memory or temp disk, risking memory/disk exhaustion DoS. Stream large payloads with `MultipartReader` or offload to presigned URLs.

## Modern C# and .NET

Use language and framework features supported by the repository's actual target version. Use newer syntax when it improves clarity, correctness, or maintainability—not merely because it is new. Do not rewrite stable code solely to adopt newer syntax unless modernization is part of the task.

For detailed language-feature guidance, use `references/csharp.md` when the task involves C# syntax, idioms, language-version decisions, type-system design, async patterns, or modernization.

Prefer framework-provided abstractions for common concerns. Examples include `TimeProvider` for testable time, `IHttpClientFactory`/HTTP resilience infrastructure for outbound HTTP, built-in validation/OpenAPI/problem-details facilities where they fit, and `Channel<T>` for in-process producer/consumer workflows.

Always verify version-sensitive APIs and behavior against the repository's actual target and installed packages before relying on them.

## API and application structure

For Minimal API applications, organize routing with native `MapGroup` static extension methods on `IEndpointRouteBuilder` (`Microsoft.AspNetCore.Routing`) rather than dumping route registrations into `Program.cs` or inventing reflection-based endpoint interfaces. This pattern avoids reflection scanning and is Native AOT-friendly.


When designing endpoints or reviewing `MapGroup` examples, read `references/api.md`. For `.slnx` XML solutions or .NET 10 file-based apps (`dotnet run app.cs` with `#:sdk`/`#:package`), inspect the entry file or `.slnx` before assuming a traditional `.sln`/`.csproj` layout.

## Configuration and hosted work

For application configuration, bind strongly typed `IOptions<T>` validated at startup with `[OptionsValidator]` and `ValidateOnStart()` rather than injecting `IConfiguration` into services. Read `references/configuration.md` for source precedence, options lifetimes, User Secrets, and feature flags.

For hosted/background work, account for cancellation, graceful shutdown, service lifetimes and scoped dependencies, exception behavior, retries, and overlap/concurrency requirements. Read `references/hosted-services.md` when designing background workers or pipeline channels. Follow the repository's established hosting pattern rather than introducing infrastructure without a concrete need.

## Implementation guidance

- Use modern idiomatic C# appropriate to the repository's language version.
- Prefer clear types, explicit contracts, small cohesive components, and dependency injection where it improves composition and testability.
- Use async APIs for asynchronous I/O; do not introduce blocking waits to hide asynchronous work.
- Pass `CancellationToken` through meaningful asynchronous boundaries.
- Treat logging, metrics, tracing, configuration, and health behavior as production concerns where applicable.
- Keep public API contracts deliberate and stable.
- Keep persistence concerns appropriate to the application's architecture; do not add generic abstractions over EF Core without a concrete benefit.
- Keep security decisions explicit and verify authorization at the resource boundary.
- Avoid premature abstractions, speculative extensibility, and ceremony without a demonstrated need.

For domain-specific implementation guidance, route to the relevant reference rather than expanding this skill with duplicate material.

## Dependency decisions

Use this decision order:

```text
Framework/platform capability
        ↓
Existing project dependency
        ↓
Small explicit implementation for simple, non-sensitive functionality
        ↓
New third-party dependency when its value justifies the added cost
```

Before adding a new dependency, consider complexity, reliability, ecosystem support, security, performance, licensing, and migration/lock-in cost.

### Commercial & Maintenance License Watchlist

Several prominent .NET libraries have migrated to commercial licenses or subscription fees. Do NOT blindly add or upgrade these packages in commercial or unverified codebases without explicit user authorization:

| Package | Version / Model | License / Condition | Recommended Action & Permissive Alternative |
|---|---|---|---|
| **MediatR** | $\ge$ 13.0 | Commercial (Lucky Penny dual license) | Prefer direct handler injection; for mediator pipelines use `Mediator.SourceGenerator` (MIT, source-generated, Native AOT) or `WolverineFx` (MIT). |
| **FluentAssertions** | $\ge$ 8.0 | Commercial (Xceed Software) | Prefer MSTest native assertions or xUnit `Assert`; for fluent assertions use `Shouldly` (BSD) or `AwesomeAssertions` (Apache 2.0). |
| **MassTransit** | $\ge$ 9.0 | Commercial | Use `WolverineFx` (MIT) or remain pinned on v8.x. |
| **AutoMapper** | $\ge$ 15.0 | Commercial | Use compile-time `Riok.Mapperly` (Apache 2.0) or static DTO factory methods (`UserResponse.From(entity)`). |
| **Polly / Polly.Core** | Future major (>Nov 2026) | Existing v8.x is Apache-2.0 / BSD-3 | Direct `Polly` v8.x is permissive; future post-2026 majors announced OSMF fee. Transitive usage via `Microsoft.Extensions.Http.Resilience` remains under Microsoft's package license. |

For a new dependency that is not already established by the repository, explain the trade-off and ask the user before adding it unless the task explicitly requested it or the repository requires it. Do not ask before using an existing dependency.

If execution is explicitly autonomous/headless and no user response is possible, do not silently introduce a new third-party dependency. Prefer an existing dependency or suitable framework capability when reasonable; otherwise stop at the dependency decision and report what is required, why it is justified, and what alternatives were considered.

Security-sensitive primitives are an explicit exception: prefer established framework/library implementations for cryptography, password hashing, token validation, OAuth/OIDC protocol behavior, and similar primitives rather than writing them yourself to save a dependency.

## Testing

Choose tests by the behavior and boundary being verified:

- Unit tests for pure domain/application logic, validators, and deterministic transformations.
- Integration tests (`WebApplicationFactory`) for HTTP routing, serialization, dependency injection, and authorization.
- Real database persistence tests (`Testcontainers`) for behavior that depends on real relational semantics.
- Contract tests when compatibility with external consumers is important.

Do not mock EF Core into behaving like a relational database, and do not use in-memory EF providers for relational verification because in-memory providers do not enforce relational constraints, transactions, or SQL semantics. Test risk and observable behavior. For detailed testing architecture, test framework selection, and Testcontainers setup, read `references/testing.md`.

## .NET Aspire

When a task involves .NET Aspire, use the official Aspire Agent Skill when it is installed and available in the environment. Do not duplicate Aspire-specific workflows, API details, resource configuration guidance, or current Aspire documentation in this skill.

This skill still applies to general .NET engineering decisions around an Aspire codebase: correctness, architecture, dependencies, C#, APIs, persistence, testing, security, and performance. The official Aspire skill owns Aspire-specific workflows and APIs.

If the official Aspire skill is unavailable, follow the repository's existing Aspire conventions and verify version-sensitive behavior against official Aspire documentation rather than relying on remembered APIs.

## Modern greenfield defaults

These are defaults for genuinely new projects or unconstrained features where the repository does not already establish a pattern. They are not universal rules and must not override existing project conventions.

- CQRS where separate command/query models provide value.
- Direct handler/use-case injection for Minimal APIs; in-process mediator only when cross-cutting pipeline behaviors justify the abstraction.
- A Result/ErrorOr-style result model for expected application failures.
- Static factory methods (`UserResponse.From(entity)`) and projection expressions (`UserResponse.Project`) on DTOs, or compile-time source-generated mappers (such as `Riok.Mapperly`).
- Native `MapGroup` static extension methods on `IEndpointRouteBuilder` for modular Minimal API route organization, returning `TypedResults` and using `builder.Services.AddValidation()` (.NET 10+) for boundary validation.
- Strongly typed `IOptions<T>` with `[OptionsValidator]` and `AddOptionsWithValidateOnStart` / `ValidateOnStart()` rather than injecting `IConfiguration`.
- Built-in OpenAPI (`builder.Services.AddOpenApi()`) paired with `Scalar.AspNetCore` for interactive API documentation in development.
- Built-in `AddRateLimiter` for endpoint abuse protection.
- `Guid.CreateVersion7()` (.NET 9+) for time-ordered database keys.
- `Microsoft.Extensions.Http.Resilience` (`AddStandardResilienceHandler()`) for client HTTP resilience and `Microsoft.Extensions.Resilience` (`AddResiliencePipeline()`) for non-HTTP resilience.
- `Microsoft.Extensions.Caching.Hybrid` (`HybridCache`) for high-performance multi-tier caching with stampede protection in .NET 9+.
- Current `MSTest.Sdk` (resolve version) as the primary test project default (MTP-native, native assertions); xUnit v3 as the supported alternative.
- Testcontainers for relational database and persistence testing.
- Fewer dependencies and explicit implementations for small, non-sensitive functionality.

For an existing project, follow its established architecture and dependencies. Do not introduce these defaults merely because they are preferred here.

## Validation

After changes, validate proportionally to risk using native, standalone CLI commands:

1. Format/analyze the affected project when appropriate:
   `dotnet format --verify-no-changes`
2. Build the smallest useful scope first, then the relevant solution when warranted:
   `dotnet build <project-or-sln> -c Debug`
3. Identify the SDK command mode and test framework before choosing focused-test syntax. Follow `references/testing.md` under **Running focused tests**.
   - Dual-configuration verification when relevant: `dotnet test -c Debug` and `dotnet test -c Release`
4. Verify API contracts, database behavior, migrations, or security behavior when affected.
5. Review the final diff for unintended changes, unnecessary complexity, and regressions.
6. If performance is relevant, compare measurements before and after.

When reporting validation results, use this structured contract:
- **Build:** Status (`Pass` / `Fail` / `Skipped`), configuration (`Debug` / `Release`), warnings count, errors count.
- **Tests:** Executed count, passed count, failed count, framework/runner used.
- **Unverified Checks:** Checks that could not be run (e.g., Docker/Testcontainers when Docker daemon is absent) and explicit reason.
- **Diff Review:** Summary of changes made and confirmation of no unintended edits.

Do not claim a change is verified when the relevant validation was not actually performed. Report checks that could not be run and why.

Routing reminder: re-check `Classify the task` above and load only the reference needed; do not load unrelated references.

If the task is primarily scaffolding a new solution, project, or complete feature, follow repository conventions and use this skill for general .NET engineering guidance.
