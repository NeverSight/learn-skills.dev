---
name: nestjs
description: "Build and evolve NestJS backends with correct DI/module boundaries, request lifecycle hygiene (pipes/guards/interceptors/filters), validation + serialization, OpenAPI, and testing. Use when adding or refactoring NestJS endpoints/modules and needing deterministic steps, output contracts, and verification gates."
metadata:
  category: language
---
# NestJS Pro

This skill is NestJS-specific. It does not assume a particular database, ORM, or hosting environment.

## Use this skill when

- Creating or refactoring a NestJS service (modules/providers/controllers)
- Designing request lifecycle behavior (auth, validation, logging, errors)
- Adding endpoints with clean DTOs, OpenAPI docs, and reliable tests
- Debugging dependency injection issues or cross-module coupling

## Do not use this skill when

- The service is not NestJS (use the stack-specific skill instead)
- You only need generic architecture guidance without NestJS specifics

## Required inputs

- Target NestJS repository or file paths
- Desired endpoint or module behavior
- Auth requirements and error/response expectations
- Existing test runner/commands (if available)

## Workflow (Deterministic)

1) Identify the surface
- Decide whether this is a new endpoint, cross-cutting behavior, or module refactor.
- Output: a short scope statement listing endpoints/modules affected.

2) Lock boundaries
- Decide the owning module and whether a new module is required.
- If multiple modules need the same provider, extract a shared module and export only necessary providers.
- Output: module ownership + export list.

3) Define contracts
- DTOs: request/response shapes, validation rules, serialization rules.
- Errors: failure cases, status codes, payload shape.
- Output: DTO list + error map.

4) Plan the request pipeline
- Choose global vs route-scoped wiring for pipes/guards/interceptors/filters.
- If behavior is cross-cutting, prefer global or module-scoped providers.
- Output: pipeline plan (what runs where).

5) Implement
- Update modules/providers/controllers and wire the pipeline pieces.
- Output: file list + brief change summary.

6) Verify
- Unit tests for providers and e2e tests for routes.
- Include at least one negative test per endpoint (validation/authz/error mapping).
- If no automated tests exist, provide manual checks with expected status codes.
- Output: test commands or manual checks + expected status codes.

## Common pitfalls

- Leaking providers across modules without explicit exports.
- Missing global ValidationPipe, leading to DTOs not enforcing rules.
- Using class-transformer without enabling serialization options.
- Inconsistent error shape when filters are not applied.
- Forgetting to document DTOs with Swagger decorators.

## Output Contract (Always)

- What changed (modules/providers/controllers) and why the boundary is correct
- Request lifecycle behavior (what runs in pipes/guards/interceptors/filters)
- DTO validation/serialization rules
- Verification steps (tests or manual curl + expected status codes)

**Reporting format**
- Scope
- Contracts
- Pipeline
- Changes
- Verification

## Examples

**Example request**
"Add a POST /projects endpoint with DTO validation and Swagger docs. Ensure auth guard and add an e2e test."

**Example response outline**
- Scope: `ProjectsModule`, `ProjectsController`, `ProjectsService`
- Contracts: `CreateProjectDto`, validation rules, error map
- Pipeline: `AuthGuard` on controller, `ValidationPipe` global
- Changes: list of files touched
- Verification: `npm run test:e2e -- projects`, expected `201` and `400`

## Scripts

- `scripts/nestjs_audit.sh`: read-only audit for common NestJS hygiene issues.
  - Requirements: `rg` (ripgrep) installed locally.
  - Usage: run from the root of a NestJS project repository.
  - Verification: report findings; no files are modified.

## References (Optional)

- `references/README.md` (index of NestJS deep-dive notes)
- `references/implementation-playbook.md`
