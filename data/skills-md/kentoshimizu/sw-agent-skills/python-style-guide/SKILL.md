---
name: python-style-guide
description: "Style, review, and refactoring standards for Python codebases with strong typing, explicit error handling, and maintainable module boundaries. Use when Python artifacts are created, changed, or reviewed and Python-specific quality rules must be enforced."
---

# Python Style Guide

## Overview
Use this skill to review and improve Python code for correctness, readability, and production reliability.

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
- Typing and boundary rules:
  - `references/typing-and-boundary-rules.md`

## Templates And Assets
- Python review checklist:
  - `assets/python-review-checklist.md`
- Refactor plan template:
  - `assets/python-refactor-plan-template.md`

## Inputs To Gather
- Changed modules and impacted boundaries.
- Typing and data-modeling risk hotspots.
- Error/config/security constraints.
- CI and runtime quality gate expectations.

## Deliverables
- Risk-prioritized review findings.
- Refactor plan with validation strategy.
- Merge readiness decision with residual risks.

## Workflow
1. Confirm trigger fit and impacted Python artifacts.
2. Plan changes via `assets/python-refactor-plan-template.md`.
3. Review with `assets/python-review-checklist.md` and project gates.
4. Apply improvements for typing, boundaries, and failure visibility.
5. Execute required checks and publish residual-risk ownership.

## Review And Refactor Checklist

### Architecture and module boundaries
1. Keep modules cohesive and focused on one responsibility.
2. Isolate side effects (I/O, network, DB) behind clear interfaces.
3. Keep orchestration layers thin and move business rules into domain modules.
4. Avoid circular imports by keeping dependency direction explicit.

### Naming and code structure
1. Follow PEP 8 naming conventions (`snake_case`, `PascalCase`, `UPPER_CASE` constants).
2. Write small functions with explicit inputs/outputs.
3. Replace magic numbers with named constants including units (`REQUEST_TIMEOUT_SECONDS`).
4. Add short comments only where intent is non-obvious.

### Typing and data modeling
1. Add type hints for public functions, methods, and complex locals.
2. Prefer explicit models (`dataclass`, `TypedDict`, Pydantic model) over loose dicts.
3. Avoid `Any` unless unavoidable and justified inline.
4. Define precise protocols/interfaces for pluggable dependencies.
5. Avoid `dict[str, Any]` and `object` for domain payloads when structure is known.
6. Convert untyped external input into explicit models once at the boundary, then keep inner layers strongly shaped.
7. Treat repeated `typing.cast(...)` usage as a signal to redesign the underlying type contract.

### Error handling and control flow
1. Raise specific exception types with actionable messages.
2. Catch exceptions intentionally at boundaries and preserve causal chains.
3. Avoid broad `except Exception` unless rethrowing after required cleanup/logging.
4. Do not suppress failures with silent fallback logic by default.

### Configuration and environment
1. Parse and validate configuration at startup.
2. Fail startup when required environment variables are missing.
3. Do not hardcode fallback defaults for required environment variables.
4. Keep secrets in secret managers or injected environment, never in code.

### Security and compliance
1. Validate untrusted input at boundaries.
2. Use parameterized DB queries; never build SQL with string concatenation.
3. Avoid unsafe deserialization and command execution with unchecked input.
4. Redact secrets and sensitive fields from logs.

### Performance and efficiency
1. Measure bottlenecks before optimizing (`cProfile`, tracing, metrics).
2. Avoid N+1 data access patterns and repeated expensive computation.
3. Stream large datasets instead of loading everything into memory.
4. Use bounded retries/backoff with named constants.

### Testing and verification
1. Add unit tests for core logic and integration tests for boundaries.
2. Cover edge cases: invalid data, timeout, retry exhaustion, concurrency hazards.
3. Add regression tests for every bug fix.
4. Document manual verification when automation cannot cover behavior.

### Observability and operations
1. Use structured logs with trace/request IDs.
2. Emit metrics for latency, throughput, and errors.
3. Normalize exception-to-error response mapping at API boundaries.
4. Ensure alertable signals exist for critical failure paths.

## CI required quality gates (check-only)
1. Run `uv run ruff format --check .`.
2. Run `uv run ruff check .`.
3. Run `uv run mypy .` (or project type checker equivalent).
4. Run `uv run pytest -q`.

## Optional autofix commands (local)
1. Run `uv run ruff format .`.
2. Run `uv run ruff check --fix .`, then re-run checks.

## Failure Conditions
- Stop when boundary contracts remain ambiguous after review.
- Stop when required configuration or typing guarantees are missing.
- Escalate when unresolved defects threaten correctness or operability.
