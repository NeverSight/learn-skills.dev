---
name: fastapi-service-development
description: "FastAPI service development workflow for production-grade Python APIs. Use when FastAPI service behavior (path operations, dependency injection, request/response models, validation, async execution, OpenAPI exposure) must be implemented or revised; do not use for repository-wide architecture governance or release management policy."
---

# Fastapi Service Development

## Overview
Use this skill to build FastAPI services with explicit schema contracts, controlled dependency lifecycles, and predictable async runtime behavior.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Dependency lifecycle guidance:
  - `references/fastapi-dependency-lifecycle-guidance.md`
- Schema contract guidance:
  - `references/fastapi-schema-contract-guidance.md`

## Templates And Assets
- Router implementation starter:
  - `assets/fastapi-router-template.py`
- Error response shape template:
  - `assets/fastapi-error-model-template.json`
- Service verification checklist:
  - `assets/fastapi-service-checklist.md`

## Inputs To Gather
- Endpoint definitions and request/response schema requirements.
- Dependency injection graph and external service dependencies.
- Authentication, validation, and observability requirements.
- Async I/O boundaries and expected latency constraints.
- Internal service DTO contracts to avoid untyped `dict[str, Any]` propagation.

## Deliverables
- Endpoint map with typed request/response models.
- Dependency and lifecycle management plan.
- Error contract and exception handling policy.
- Verification checklist and test focus areas.

## Workflow
1. Define Pydantic models and endpoint contracts first.
2. Separate routers, service logic, and infrastructure adapters.
3. Convert boundary payloads to explicit domain input/output models before service-layer execution.
4. Manage shared resources using `references/fastapi-dependency-lifecycle-guidance.md`.
5. Implement exception mapping with `assets/fastapi-error-model-template.json`.
6. Validate behavior and docs with `assets/fastapi-service-checklist.md`.

## Quality Standard
- All endpoints expose explicit typed schemas.
- Dependency scope and teardown behavior are deterministic.
- Error responses are stable and machine-parseable.
- OpenAPI output reflects actual runtime behavior.
- Internal logic minimizes runtime casts by using precise models at boundaries.

## Failure Conditions
- Stop when schema contracts are ambiguous or loosely typed.
- Stop when async request paths contain hidden blocking I/O.
- Escalate when dependency lifecycle cannot be managed safely.
