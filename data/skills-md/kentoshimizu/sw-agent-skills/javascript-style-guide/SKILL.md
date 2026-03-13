---
name: javascript-style-guide
description: "Style, review, and refactoring standards for JavaScript codebases with explicit runtime contracts, safe async behavior, and maintainable module boundaries. Use when `.js`, `.jsx`, `.mjs`, or `.cjs` artifacts are created, changed, or reviewed and JS-specific quality rules must be enforced. Do not use for `.ts`, `.tsx`, `.d.ts`, or `tsconfig*.json`-owned code. For shared JS/TS config files, run together with `typescript-style-guide` when both JS and TS artifacts change in the same pull request."
---

# Javascript Style Guide

## Overview
Use this skill to review and improve JavaScript code for runtime safety, readability, and operational stability.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Trigger Reference
- Use `references/trigger-matrix.md` as the canonical trigger and co-activation matrix.
- Resolve skill activation from changed files with `python3 scripts/resolve_style_guides.py <changed-path>...` when automation is available.
- Validate trigger matrix consistency with `python3 scripts/validate_trigger_matrix_sync.py`.

## Quality Gate Reference
- Use `references/quality-gate-command-matrix.md` for CI check-only vs local autofix command mapping.

## Shared References
- Runtime safety and validation rules:
  - `references/runtime-safety-and-validation-rules.md`

## Templates And Assets
- JavaScript review checklist:
  - `assets/javascript-review-checklist.md`
- Refactor planning template:
  - `assets/javascript-refactor-plan-template.md`

## Inputs To Gather
- Changed modules and boundary responsibilities.
- Runtime assumptions (Node/browser/jsdom), async patterns, and side effects.
- Validation/security requirements for external inputs.
- CI/lint/test constraints and operational expectations.

## Deliverables
- Risk-prioritized review findings.
- Refactor plan with explicit behavior-preservation strategy.
- Verification plan for functional and operational confidence.
- Residual-risk log with follow-up ownership.

## Workflow
1. Confirm trigger fit and impacted JS artifacts.
2. Create/update plan using `assets/javascript-refactor-plan-template.md`.
3. Review code with `assets/javascript-review-checklist.md` and project gates.
4. Refactor to improve boundaries, validation, and failure transparency.
5. Re-run check-only quality gates and targeted runtime verification.
6. Publish merge decision with unresolved-risk ownership.

## Review And Refactor Checklist

### Architecture and boundaries
1. Keep modules focused and small; avoid cross-layer leakage.
2. Separate pure domain logic from side effects (I/O, network, storage).
3. Keep entry points thin and delegate behavior to reusable services.
4. Encapsulate third-party integrations behind adapter modules.

### Naming and code structure
1. Use clear, intent-revealing names for functions and variables.
2. Prefer `const`; use `let` only when mutation is required.
3. Replace magic numbers with named constants including units (`RETRY_DELAY_MS`).
4. Keep functions single-purpose and avoid deeply nested branching.

### Data shapes and validation
1. Define explicit data contracts with schema validators (`zod`, `yup`, or equivalent).
2. Avoid untyped, ambiguous object bags for domain-critical paths.
3. Validate external payloads at boundaries before business logic executes.
4. Keep serialization/deserialization logic centralized.
5. Parse once at the boundary and pass validated domain objects inward; avoid repeated shape checks in inner layers.
6. If the same cast/shape-fix appears in multiple call sites, replace it with an explicit named contract and mapper.
7. Use narrow JSDoc typedefs or schema-derived types for core payloads instead of broad `object`/`Record` placeholders.

### Async behavior and error handling
1. Prefer `async/await` over mixed promise chains.
2. Throw and handle specific error classes with clear operational meaning.
3. Avoid blanket catch blocks that swallow failures.
4. Propagate errors intentionally (recover/retry/rethrow/log).
5. Do not add fallback logic that hides root-cause failures by default.

### Configuration and environment
1. Validate required environment variables at process startup.
2. Fail fast if required configuration is missing.
3. Do not hardcode fallback defaults for required environment variables.
4. Keep secrets out of source control and logs.

### Security and compliance
1. Treat all external input as untrusted; validate and sanitize it.
2. Prevent injection attacks by parameterizing queries and escaping output contexts.
3. Enforce auth/authz at API boundaries.
4. Avoid logging secrets, tokens, or PII.

### Performance and efficiency
1. Avoid repeated expensive operations in loops; cache intentionally.
2. Bound concurrency for bulk async operations.
3. Stream or paginate large payloads.
4. Profile hot paths before optimization.

### Testing and verification
1. Add unit tests for core logic and integration tests for boundary modules.
2. Cover edge cases: empty input, invalid schema, timeout, retry exhaustion.
3. Add regression tests for bug fixes.
4. Document manual verification steps when automated tests are missing.

### Observability and operations
1. Use structured logs with request/correlation IDs.
2. Emit metrics for latency, throughput, and error rates.
3. Normalize error codes and statuses for incident response.
4. Add operational safeguards for retries, circuit breaking, and timeouts.

## CI Required Quality Gates (check-only)
1. Run `prettier --check .` (or project equivalent).
2. Run `eslint . --max-warnings=0`.
3. Run test suite (`npm test`/`pnpm test`/project equivalent).
4. Reject changes that weaken validation, security, or failure visibility.

## Optional Autofix Commands (local)
1. Run `prettier --write .` to apply formatting.
2. Run `eslint . --fix` for safe lint autofixes, then re-run check-only gates.

## Failure Conditions
- Stop when runtime-critical data boundaries are not explicitly validated.
- Stop when async/error behavior masks failures or loses root cause.
- Escalate when quality gates fail on security, reliability, or correctness-critical paths.
