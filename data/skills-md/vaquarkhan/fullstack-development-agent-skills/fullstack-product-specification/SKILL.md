---
name: fullstack-product-specification
description: Define fullstack product changes with clear UI journeys, API contracts, domain model updates, non-functional requirements, and release constraints. Use this before implementation when work spans frontend and backend.
disable-model-invocation: true
---

# Fullstack Product Specification

## Use When

- Work spans UI and backend in one delivery slice
- Requirements are unclear, conflicting, or incomplete
- Teams need a shared source of truth before coding

## Workflow

1. Capture business outcome, user roles, and success metrics.
2. Define journeys and states for each persona (happy path, empty, error, denied).
3. Specify API contracts, including request and response schemas, errors, and versioning.
4. Define domain and persistence impact (new entities, migration, indexing, retention).
5. Set non-functional requirements (latency, throughput, accessibility, security, auditability).
6. Record rollout strategy, migration or backfill needs, and rollback criteria.

## Required Checks

- Feature brief includes testable acceptance criteria
- API contract draft covers errors, versioning, and examples
- UI state matrix covers loading, empty, error, and success
- Data model or migration impact documented with rollback owner
- Rollout and rollback note approved before build

## Required Artifacts

- Feature brief with acceptance criteria
- API contract draft (OpenAPI, JSON Schema, or equivalent)
- UI state matrix covering loading, empty, error, and success
- Data model or schema change note
- Rollout and rollback note with decision owner

## Red Flags

- Requirements only describe UI visuals without behavior rules
- Backend assumptions are embedded in frontend code comments only
- API errors and edge cases are not defined
- No migration story for schema or contract changes

## Decision Framework

- If requirements are UI-only, force API and data impact review before build starts.
- If the change touches auth or money flow, require security and failure-mode scenarios.
- If migration is needed, choose expand-migrate-contract unless a stronger alternative is justified.
- If performance SLO is unknown, add a baseline measurement task before implementation.

## Common Rationalizations And Rebuttals

- "We can define API later once UI is done." -> This causes rework and contract drift; lock minimal API shape early.
- "Edge cases can wait for QA." -> Undefined error behavior becomes production bugs; specify it now.
- "Rollback is obvious." -> Rollback often fails with data changes; document exact rollback conditions and steps.

## Evidence Pack

- Approved feature brief with acceptance criteria and owner
- API contract diff with backward-compatibility note
- UI state matrix covering all critical transitions
- Data migration note with rollback decision point
- NFR checklist with explicit SLO targets

## Exit Criteria

- Acceptance criteria are testable and implementation-neutral
- Contract compatibility strategy is documented
- UI and backend ownership boundaries are explicit
- Release risk and rollback path are approved
