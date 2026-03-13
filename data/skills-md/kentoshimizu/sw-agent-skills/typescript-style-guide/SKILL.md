---
name: typescript-style-guide
description: "Style, review, and refactoring standards for TypeScript codebases. Trigger when `.ts`, `.tsx`, `.d.ts`, or `tsconfig*.json` files are created, changed, or reviewed and TS-specific quality rules (type safety, narrowing, async/error handling, module boundaries) must be enforced. Do not use for JavaScript-only modules that are outside TypeScript type-check scope. In mixed JS/TS repositories, this skill owns `tsconfig`-scoped modules. For shared JS/TS configuration files (for example `package.json`, shared lint/test config), run together with `javascript-style-guide` when both JS and TS artifacts change in the same pull request."
---

# Typescript Style Guide

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

Apply this checklist when writing or reviewing TypeScript code.

## Trigger Reference

- Use `references/trigger-matrix.md` as the canonical trigger and co-activation matrix.
- Resolve skill activation from changed files with `python3 scripts/resolve_style_guides.py <changed-path>...` when automation is available.
- Validate trigger matrix consistency with `python3 scripts/validate_trigger_matrix_sync.py`.

## Architecture and boundaries
## Quality Gate Reference

- Use `references/quality-gate-command-matrix.md` for CI check-only vs local autofix command mapping.

1. Keep modules focused and dependency direction explicit.
2. Separate domain logic from adapters (HTTP, DB, queue, storage).
3. Keep controllers/route handlers thin and orchestration-light.
4. Encapsulate external APIs behind typed client abstractions.

## Naming and structure

1. Use descriptive names with consistent casing (`camelCase`, `PascalCase`, `UPPER_SNAKE_CASE`).
2. Keep functions small and single-purpose.
3. Replace magic numbers with named constants and units (`POLL_INTERVAL_MS`).
4. Avoid deep nesting; prefer guard clauses.

## Type safety and data modeling

1. Use strict compiler options (`strict`, `noImplicitAny`, `noUncheckedIndexedAccess` when possible).
2. Prefer explicit `type`/`interface`/discriminated unions over loose object bags.
3. Avoid `any`; use `unknown` plus narrowing when dynamic input is unavoidable.
4. Model boundary contracts with explicit request/response types.
5. Treat `object` and broad `Record<string, unknown>` as temporary boundary types, not domain model types.
6. Prefer parser/type-guard refinement over `as Foo` casts; repeated casts are usually a contract-design smell.
7. Use `satisfies` for config/static objects to preserve literal precision without unsafe widening.

## Runtime validation and error handling

1. Validate untrusted input at boundaries with runtime schemas (`zod`, equivalent).
2. Use specific error classes/codes and map them intentionally at boundaries.
3. Avoid broad catches that swallow failures.
4. Propagate failures explicitly (recover/retry/rethrow/log) with context.
5. Do not implement fallback logic that masks root causes by default.

## Configuration and environment

1. Parse configuration once at startup and expose typed config objects.
2. Fail startup when required environment variables are missing.
3. Do not hardcode fallback defaults for required environment variables.
4. Keep secrets outside source control and logs.

## Security and compliance

1. Treat all external input as untrusted and validate aggressively.
2. Prevent injection/XSS/SSRF via context-aware encoding and allow-lists.
3. Enforce auth/authz checks near entry points and sensitive operations.
4. Avoid logging secrets or personal data.

## Performance and scalability

1. Avoid repeated expensive computations and unbounded async fan-out.
2. Use streaming/pagination for large payloads.
3. Bound retries and concurrency with named limits.
4. Profile before optimizing and verify gains with measurements.

## Testing and verification

1. Add unit tests for domain logic and integration tests for boundaries.
2. Cover edge cases: invalid schema, timeout, cancellation, retry exhaustion.
3. Add regression tests for each bug fix.
4. Document manual verification where automation is not available.

## Observability and operations

1. Emit structured logs with request/correlation IDs.
2. Track latency, error rate, and dependency metrics.
3. Keep error responses stable and actionable.
4. Add safeguards for timeout, retry, and circuit-breaking behavior.

## CI required quality gates (check-only)

1. Run formatter check (`prettier --check .`, or project equivalent).
2. Run lint checks (`eslint . --max-warnings=0`).
3. Run type check (`tsc --noEmit`).
4. Run automated tests (`pnpm test`/`npm test`/project equivalent).

## Optional autofix commands (local)

1. Run `prettier --write .` to apply formatting.
2. Run `eslint . --fix` for safe lint autofixes, then re-run check-only gates.
