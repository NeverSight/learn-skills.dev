---
name: dotnet-scaffold
description: Scaffold a new .NET solution, project, test project, or complete feature/entity/vertical slice (command, handler, endpoint, validation, tests) following repository conventions. Use when creating something new from scratch — new project, new test project, new entity, or CQRS/Vertical Slice feature. For engineering guidance on existing code use the dotnet skill, and for Aspire-specific workflows use the Aspire skill.
license: MIT
metadata:
  author: Timy
  version: "1.0"
---

# .NET Scaffolding

Use this workflow to scaffold a complete, working .NET solution, project, or feature. This skill owns the scaffolding workflow; when the `dotnet` skill is available, apply its engineering guidance rather than duplicating it here.

## Scope

Determine the scaffolding target:
1. **New solution/repository** — create solution structure, central build/package policies, and initial projects.
2. **New project** — add an application, worker, or test project to an existing solution.
3. **New feature/entity** — add a vertical slice or feature to an existing project.

Do not turn a feature request into a solution redesign. Greenfield archetypes and `assets/SliceTemplate/` apply **only** when the repository has no established convention. When working in an existing codebase, follow its existing conventions, architecture, and dependencies.

## Prerequisites

Automated scaffolding via `scripts/scaffold.cs` requires the **.NET 10 SDK or later** (for file-based C# apps and modern `slnx` solutions). Before executing, verify the installed SDK via `dotnet --version`. If running on an older SDK, stop and report the environment constraint to the user; do not guess or manually generate mismatched files.

## Workflow

### 1. Inspect Environment & Detect Architecture
Before generating code, inspect:
- Installed SDK version (`dotnet --version`) and project templates (`dotnet new list`).
- Existing target framework (`TargetFramework`) and language version (`LangVersion`).
- Solution layout and Central Package Management (`Directory.Packages.props`).
- **Detect Host Architecture:**
  - **Vertical Slice Architecture (VSA):** Single web project or features organized under `Features/` or `Endpoints/`.
  - **Clean Architecture (CA):** Multi-project layout containing `Domain`, `Application`, `Infrastructure`, `Api` / `Web`.
  - **Modular Monolith:** Independent module boundaries under `src/Modules/<ModuleName>/`.
  *Always adapt new feature code to match the host architecture. Never impose VSA on a Clean Architecture codebase or vice-versa.*

### 2. Scaffold Greenfield Solution
For a new solution, invoke the deterministic scaffolding script rather than re-deriving configuration:

```bash
dotnet run <path-to-skill>/scripts/scaffold.cs -- -n <SolutionName> -o <OutputDir> [--with-testcontainers]
```

The script automates:
- Modern XML solution creation (`dotnet new sln --format slnx`).
- Tooling configuration (`global.json` pinning SDK and Microsoft.Testing.Platform runner).
- Central Package Management (`Directory.Packages.props`) and build policies (`Directory.Build.props`).
- Web API and test projects referencing reusable templates in `assets/`.
- Dual-configuration verification (`dotnet build` and `dotnet test` in Debug and Release).

Reusable asset definitions reside in `assets/`:
- `Directory.Build.props`: Enforces central compiler warnings and active LTS (`net10.0`).
- `Directory.Packages.props`: Central package management skeleton.
- `global.json`: SDK feature band and MTP runner pin.
- `.editorconfig`: Standard .NET code formatting rules.
- `TestProject.csproj`: Canonical `MSTest.Sdk` test project template without inline versions.

### 3. Scaffold Test Project
When adding a test project to an existing solution:
- **Default Test Framework:** Current `MSTest.Sdk` (MTP-native, standalone executable). Reference `assets/TestProject.csproj`.
- **Alternative Framework:** `xUnit v3` for existing xUnit solutions.
- **Relational Persistence (Conditional):** Include `Testcontainers` (`Testcontainers.PostgreSql`, `Testcontainers.MsSql`) and `Respawn` **only** when the project uses relational persistence.
- **Docker Prerequisite:** Testcontainers requires a running Docker daemon. If Docker is unavailable in the environment, report this clearly in the verification summary; **never silently fall back to the EF Core in-memory provider** because in-memory providers do not enforce relational constraints, transactions, or SQL semantics.

### 4. Scaffold Feature / Slices

Generate complete feature slices conforming to the detected architecture:

#### A. Vertical Slice Architecture (VSA)
When working in a VSA project, use the slice pattern in `assets/SliceTemplate/`:
```text
Features/<Area>/<Action>/
├── <Action>Endpoints.cs   // Static MapGroup extension method; maps routes with TypedResults
├── <Action>Request.cs     // Input DTO / parameters (sealed record)
├── <Action>Handler.cs     // Domain / use-case execution with CancellationToken
└── <Action>Response.cs    // Output DTO with static From factory
```

#### B. Clean Architecture (CA)
When working in a Clean Architecture multi-project solution, distribute feature files across layer boundaries:
```text
src/<App>.Domain/Entities/<Entity>.cs                           // Domain entity & business invariants
src/<App>.Application/<Area>/<Action>/<Action>Command.cs       // Request DTO & Validator (FluentValidation)
src/<App>.Application/<Area>/<Action>/<Action>Handler.cs       // Use-case logic (injects DbContext or domain service)
src/<App>.Infrastructure/Persistence/Configurations/<Entity>Configuration.cs  // EF Core mapping
src/<App>.Api/Endpoints/<Area>/<Action>Endpoint.cs             // Minimal API route mapping with TypedResults
tests/<App>.Tests/Integration/<Area>/<Action>Tests.cs          // WebApplicationFactory + Testcontainers test
```

Key rules across all architectures:
- Endpoints return strongly typed results: `Results<Ok<TResponse>, ProblemHttpResult>` or `Results<Created<TResponse>, ProblemHttpResult>`.
- Request/Response types are sealed records with primary constructors.
- Propagate `CancellationToken` through all asynchronous operations.
- Inject `DbContext` or domain handlers directly; never wrap EF Core in generic repository layers.
- Do not call `.WithOpenApi()`; it is deprecated in .NET 10 (`ASPDEPR002`). ASP.NET Core built-in OpenAPI tracks endpoints automatically.
- Follow the dependency decision order in the `dotnet` skill and check the Commercial License Watchlist.

### 5. Verify
Always verify scaffolding with real commands:
1. Restore dependencies: `dotnet restore`
2. Build solution in both configurations: `dotnet build -c Debug` and `dotnet build -c Release`
3. Run tests: `dotnet test -c Debug` and `dotnet test -c Release`
4. Report any check that could not run.

## Strict 9-Point Feature Completeness Checklist

Every scaffolded feature must satisfy this checklist as a single complete unit before reporting completion:
- [ ] **1. Request/Response DTOs:** Sealed records with primary constructors; no domain entity leakage.
- [ ] **2. Validation:** Input validation (FluentValidation or DataAnnotations) handling edge cases.
- [ ] **3. Business Logic:** Dedicated handler or use case executing domain behavior cleanly.
- [ ] **4. Typed Minimal API Endpoint:** Route defined with typed results (`Results<Ok<T>, ProblemHttpResult>`).
- [ ] **5. Cancellation:** `CancellationToken` explicitly passed to all async methods and database calls.
- [ ] **6. Persistence:** Direct EF Core query/mapping without generic repository wrappers.
- [ ] **7. Error Handling:** Expected failures map explicitly to RFC 7807/9457 `ProblemDetails`.
- [ ] **8. OpenAPI:** Clean contract generated automatically (no deprecated `.WithOpenApi()`).
- [ ] **9. Integration Test:** At least one test using `WebApplicationFactory` and real database testing (`Testcontainers`).

## Reporting Contract

When scaffolding completes, output a structured report:
1. **Scaffolded Scope:** Type of artifact created (solution, project, or feature slice).
2. **Files Created / Modified:** Explicit list of created or altered files.
3. **Architecture & Dependency Decisions:** Selected frameworks, CPM additions, or deviations from repo defaults.
4. **Verification Results:** Logs and exit codes for `dotnet build` and `dotnet test` (Debug & Release).
5. **Environment Constraints / Follow-ups:** Any prerequisites (e.g., Docker for Testcontainers) or manual steps required.
