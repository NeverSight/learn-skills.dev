---
name: api-design-rest
description: Resource-oriented REST/OpenAPI contract design for URI/method semantics, idempotency, pagination, and HTTP status behavior. Trigger when REST contract diffs are detected in paths, methods, schemas, or status semantics, or when request-response transport choice is still unresolved before implementation. Do not use for GraphQL schema authoring, error-taxonomy-only changes, version lifecycle governance, or consumer-provider contract test implementation.
---

# API Design REST

## Scope Boundaries
- Use when REST resources, URI structures, and HTTP behavior are being designed or changed.
- Use proactively when route, method, status, or schema diffs appear in specs, manifests, or source.
- Use when request-response transport options are being compared and REST is a candidate.
- Do not use for GraphQL-first schema work; use `api-design-graphql`.
- Do not use for storage internals; use `db-*`.

## Goal
Deliver REST contracts that are stable, predictable, and operationally safe.

## Shared API Contract (Canonical)
- Use `references/api-governance-contract.md` as the primary reference for recommended structure.
- Optional consistency checks (only if your repository enforces manifest validation):
  - `python3 scripts/validate_api_contract.py --manifest <path/to/manifest.json>`
- Start from valid templates in `assets/`.
- Use transport decision reference:
  - `references/transport-selection-matrix.md`
- Use threshold derivation reference:
  - `references/threshold-derivation-framework.md`
- Do not define alternate ID formats, lifecycle states, or compatibility policies locally.

## Implementation Templates
- REST OpenAPI template:
  - `assets/openapi-rest-template.yaml`
- Queue/event API template:
  - `assets/asyncapi-queue-template.yaml`
- WebSocket contract template:
  - `assets/websocket-message-contract-template.yaml`
- SSE contract template:
  - `assets/sse-event-contract-template.yaml`

## Inputs
- Product behavior and consumer integration requirements
- Resource model candidates and domain invariants
- Security, compliance, and SLO constraints
- Interaction model candidates (`sync`, `async`, `streaming`, `bidirectional_realtime`)
- Transport options (`rest`, `graphql`, `grpc`, `websocket`, `sse`, `queue`)

## Outputs
- Resource map and endpoint matrix (`method`, `path`, `status`, `error`)
- Request/response schema contract including pagination and filtering rules
- Authorization, rate-limit, idempotency, and observability decisions

## Workflow
1. Model resources as nouns and define stable identifiers before endpoint naming.
2. Select interaction mode and primary transport with explicit rationale and rejected alternatives.
3. Define method semantics with explicit idempotency strategy for retry-sensitive writes.
4. Fix status and error semantics so clients can branch without string parsing.
5. Define naming conventions for paths, fields, and error codes.
6. Define authz scope, rate-limit policy, and trace/log fields for every operation class.
7. Derive threshold types and methods (latency, timeout, capacity, concurrency, retry, delivery).
8. Validate backward compatibility and publish deprecation/migration notes when behavior changes.
9. Validate the artifact against the canonical API contract before approval.

## Quality Gates
- URI and method choices follow resource-oriented conventions and HTTP semantics.
- Contract is backward compatible or includes approved version transition evidence.
- Error contract is machine-actionable and trace-correlated.
- Authz, rate-limit, and runbook updates are complete and reviewable.
- Decision context captures internal/external audience and sync/async/real-time transport rationale.
- Threshold derivation methods are explicit and tied to SLO/risk evidence.

## Failure Handling
- Stop when URI design leaks internal implementation or method semantics are inconsistent.
- Stop when compatibility impact is unknown.
- Escalate when required approvers or compliance evidence are missing.
