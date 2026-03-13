---
name: api-versioning
description: API version lifecycle governance for breaking-change classification, deprecation windows, migration planning, and support matrix management across internal and external consumers. Trigger when contract diffs may break consumers (for example required-field removal, semantic change, or channel change), when deprecation/sunset planning is required, or when multiple consumer cohorts must be supported in parallel. Do not use for first-pass endpoint/schema design.
---

# API Versioning

## Scope Boundaries
- Use when compatibility policy, deprecation lifecycle, or version transition strategy is in scope.
- Use proactively when API diffs alter semantics, required fields, response shape, or transport guarantees.
- Use when internal and external consumers have different support windows or migration constraints.
- Do not use for first-pass endpoint/schema design without change impact context.
- Do not use for storage internals; use `db-*`.

## Goal
Deliver explicit compatibility governance so consumers can migrate without surprises.

## Shared API Contract (Canonical)
- Use `../api-design-rest/references/api-governance-contract.md` as the canonical contract.
- Optional consistency checks (only if your repository enforces manifest validation):
  - `python3 ../api-design-rest/scripts/validate_api_contract.py --manifest <path/to/manifest.json>`
- Use API versioning templates in `../api-design-rest/assets/` as baseline.
- Use transport decision reference:
  - `../api-design-rest/references/transport-selection-matrix.md`
- Use threshold derivation reference:
  - `../api-design-rest/references/threshold-derivation-framework.md`
- Do not redefine breaking-change criteria, approval roles, or deprecation gates locally.

## Implementation Templates
- Versioning policy template:
  - `../api-design-rest/assets/api-versioning-policy-template.md`

## Inputs
- Current API surface and consumer adoption distribution
- Change classification (additive vs breaking)
- Regulatory, support-window, and migration constraints
- Audience split (`internal`, `external`, `both`) and transport mix (`rest`, `graphql`, `grpc`, `websocket`, `sse`, `queue`)

## Outputs
- Versioning policy (channel, semantics, compatibility guarantees)
- Deprecation and sunset plan with migration guidance
- Compatibility matrix linking producer versions and tested consumers

## Workflow
1. Classify changes using explicit breaking-change criteria from the canonical contract.
2. Choose version channel (URI/header/media-type/schema tag) and publish scope boundaries.
3. Split migration path for internal and external consumers when support windows differ.
4. Define deprecation timeline and migration artifacts for affected consumers.
5. Update compatibility matrix and ensure contract tests cover supported versions.
6. Verify runbook and monitoring updates for dual-version operation periods.
7. Validate artifact compliance against the canonical API contract.

## Quality Gates
- Breaking changes include explicit migration plan and minimum deprecation window.
- Compatibility matrix is current for all supported consumer groups.
- Deprecation communication and sunset criteria are documented.
- Rollback and incident procedures are defined for version cutover periods.

## Failure Handling
- Stop when breaking changes are proposed without migration path or deprecation evidence.
- Stop when supported consumer versions are unknown.
- Escalate when legal/compliance support windows cannot be met.
