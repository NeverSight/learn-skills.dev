---
name: api-error-handling
description: API failure-contract design for status mapping, stable error codes, retryability semantics, and traceable error payloads across sync and async transports. Trigger when error behavior, retry semantics, or debuggability fields change in specs or source, or when those rules remain implicit. Do not use for full resource/schema modeling or version-channel policy definition.
---

# API Error Handling

## Scope Boundaries
- Use when API error taxonomy, response schemas, and status mapping are being created or changed.
- Use proactively when failure handling is implicit, inconsistent, or incident learning needs to be codified in the contract.
- Use proactively when error payload or status-mapping diffs are detected without explicit retry/backoff policy.
- Use when retry/backoff behavior affects client correctness or operational stability.
- Do not use for transport-independent incident handling policy; use `incident-postmortem` or runbook skills.
- Do not use for storage internals; use `db-*`.

## Goal
Deliver machine-actionable error contracts that are stable across versions.

## Shared API Contract (Canonical)
- Use `../api-design-rest/references/api-governance-contract.md` as the canonical contract.
- Optional consistency checks (only if your repository enforces manifest validation):
  - `python3 ../api-design-rest/scripts/validate_api_contract.py --manifest <path/to/manifest.json>`
- Reuse valid API error templates in `../api-design-rest/assets/`.
- Use threshold derivation reference:
  - `../api-design-rest/references/threshold-derivation-framework.md`
- Do not add local error-ID formats or local lifecycle variants.

## Implementation Templates
- Error catalog template:
  - `../api-design-rest/assets/api-error-catalog-template.yaml`

## Inputs
- Existing API status and error behavior
- Consumer retry and fallback assumptions
- Security/privacy constraints for error payload fields

## Outputs
- Error taxonomy with stable error codes and ownership
- Status-to-error mapping table by scenario
- Standard error payload schema with trace correlation and retry semantics

## Workflow
1. Define error categories (validation, authorization, conflict, dependency, internal).
2. Map each category to transport status and retry guidance (`retryable`, backoff expectations).
3. Define stable error code registry and deprecation policy for retired codes.
4. Define payload fields for client actionability and operator triage (including trace identifiers).
5. Align error behavior across sync/async/realtime transports when a domain is multi-transport.
6. Verify contract behavior with representative failure scenarios.
7. Validate artifact compliance against the canonical API contract.

## Quality Gates
- Error codes are stable, unique, and documented with owner.
- Status mapping is deterministic and consistent across endpoints.
- Error payload excludes sensitive internal details but preserves debugging context.
- Operational runbooks and alert correlations reference the published error model.

## Failure Handling
- Stop when clients cannot determine retry vs non-retry behavior from contract.
- Stop when status mapping varies for the same error class without explicit policy.
- Escalate when compatibility impact on existing consumers is unresolved.
