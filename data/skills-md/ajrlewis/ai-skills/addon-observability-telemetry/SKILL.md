---
name: addon-observability-telemetry
description: Use when a project needs production-grade logging, metrics, tracing, and health diagnostics; pair with architect-stack-selector and addon-human-pr-review-gate.
---

# Add-on: Observability Telemetry

Use this skill when a project needs to be diagnosable in production with structured telemetry instead of ad hoc console logging.
Prefer trusted, ecosystem-standard observability packages over custom logging utilities.
Use this as the shared observability policy layer, then pair it with the runtime-specific implementation add-on when available.

## Compatibility

- Works with all `architect-*` skills.
- Especially useful for `architect-python-uv-fastapi-sqlalchemy`, `architect-nextjs-bun-app`, and any queue or worker style runtime.
- Can be combined with `addon-deterministic-eval-suite` to make telemetry contracts testable.
- Prefer `addon-observability-python-structlog` for Python runtimes.
- Prefer `addon-observability-nextjs-pino` for Next.js or TypeScript server runtimes.

## Inputs

Collect:
- `TELEMETRY_MODE`: `logs-only` | `logs+metrics` | `logs+metrics+traces`.
- `TRACE_EXPORTER`: `otlp` | `stdout` | `none`.
- `LOG_FORMAT`: `json` | `logfmt`.
- `ERROR_TRACKING`: `yes` | `no` (default `yes`).
- `PII_REDACTION`: `strict` | `standard`.
- `LOG_BACKEND`: default to the runtime-standard package unless the user explicitly requests another option.

## Integration Workflow

1. Add telemetry artifacts:
```text
docs/OBSERVABILITY.md
src/{{MODULE_NAME}}/observability/logging.*
src/{{MODULE_NAME}}/observability/metrics.*
src/{{MODULE_NAME}}/observability/tracing.*
src/{{MODULE_NAME}}/api/routes/health.*
scripts/ops/check_health.*
```
- Copy and adapt this skill's bundled health-check script:
- `scripts/check_health.sh`
- Place the adapted result in the target project at `scripts/ops/check_health.sh` (or the runtime-equivalent script path).
- Treat `observability/logging.*` as package configuration and adapters only; do not implement a custom logger there.

2. Standardize event shape:
- use structured logs with request or run correlation IDs
- classify levels consistently (`info`, `warn`, `error`)
- emit explicit error codes for expected failures

3. Add runtime diagnostics:
- health and readiness checks for critical dependencies
- latency, error-rate, and throughput metrics
- trace spans around network, database, and LLM calls when tracing is enabled

4. Protect sensitive data:
- redact auth headers, secrets, and raw personal data
- document what fields may be logged
- keep sampling and retention decisions explicit

5. Select runtime-standard dependencies:
- Next.js or TypeScript server runtimes: prefer `addon-observability-nextjs-pino`. If that add-on is unavailable, still use `pino`; do not rely on ad hoc `console.log` in production request paths. `logging.ts` should configure serializers, redaction, correlation IDs, and child loggers only.
- Python services and workers: prefer `addon-observability-python-structlog`. If that add-on is unavailable, still use `structlog` for APIs and long-lived services. `loguru` is acceptable for smaller services or CLI-heavy workers when a simpler sink model is sufficient. Do not build a custom wrapper around `print` or bare stdlib logging as the primary production path.
- If metrics or traces are enabled, prefer official OpenTelemetry SDK or instrumentation packages instead of custom metric counters or tracing helpers.

## Required Template

### `docs/OBSERVABILITY.md`
```markdown
# Observability Contract

## Telemetry Mode
- logs+metrics

## Required Fields
- timestamp
- level
- message
- correlation_id

## Health Checks
- app process
- database
- external provider dependencies

## Redaction Policy
- Never log secrets, auth headers, or raw PII.
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Do not emit telemetry that leaks credentials, tokens, or full request bodies by default.
- Prefer one well-supported observability dependency over a dependency-free but hand-rolled logger.
- Keep `observability/logging.*` limited to configuring, adapting, and binding the chosen package; do not create a homemade logger implementation.
- Do not use raw `console.log` in production TypeScript or Next.js server code except in tests or local-only scripts.
- Do not use raw `print()` in production Python service code except for explicit CLI UX or local-only scripts.
- If the runtime already has a clear ecosystem default, use it unless the user explicitly requests an alternative and the tradeoff is documented.
- Use correlation IDs consistently across logs, metrics labels, and traces where supported.
- Prefer stable event names over free-form log spam.
- Missing health diagnostics for critical dependencies should be treated as incomplete.
- Keep observability dependencies bounded; avoid heavyweight infra by default, but do not treat "bounded" as "dependency-free."

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
test -f docs/OBSERVABILITY.md
rg -n "health|ready|trace|metric|correlation" src || true
rg -n "console\\.log" src || true
test -e scripts/ops/check_health.sh || test -e scripts/ops/check_health.ts || test -e scripts/ops/check_health.py || true
```

Manual checks:
- Health endpoint reports degraded status for dependency failures.
- Logs and traces include correlation identifiers without leaking secrets.
- `observability/logging.*` configures a real package (`pino`, `structlog`, `loguru`, or explicit user-approved equivalent) instead of implementing logging from scratch.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
