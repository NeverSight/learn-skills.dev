---
name: api-contract-testing
description: "Consumer-provider contract testing and release-gate design for compatibility matrices, contract assertions, and CI blocking rules across versions and transports. Trigger when API contract diffs are detected but compatibility evidence is missing or stale (contract test pass, consumer-impact mapping, or compatibility matrix update), or when multiple consumers, versions, or transports must be protected by automated gates. Do not use for first-pass API interface design."
---

# API Contract Testing

## Scope Boundaries
- Use when API compatibility must be continuously validated between producers and consumers.
- Use proactively when schema/endpoint/protocol diffs exist but executable compatibility evidence is missing.
- Use when compatibility judgment is currently human-only and needs codified CI gates.
- Do not use for API schema design from scratch; use `api-design-*`.
- Do not use for end-to-end UI validation.

## Goal
Catch contract drift before deployment impacts consumers.

## Shared API Contract (Canonical)
- Use `../api-design-rest/references/api-governance-contract.md` as the canonical contract.
- Optional consistency checks (only if your repository enforces manifest validation):
  - `python3 ../api-design-rest/scripts/validate_api_contract.py --manifest <path/to/manifest.json>`
- Use API contract-testing templates in `../api-design-rest/assets/`.
- Use transport decision reference:
  - `../api-design-rest/references/transport-selection-matrix.md`
- Keep compatibility states and approval gates aligned with the canonical contract.

## Implementation Templates
- Contract test matrix template:
  - `../api-design-rest/assets/api-contract-test-matrix-template.yaml`

## Inputs
- Provider API specification and implementation
- Consumer expectations and critical integration cases
- Versioning and deprecation policy constraints
- Transport mix and interaction modes under test (`sync`, `async`, `streaming`, `bidirectional_realtime`)

## Outputs
- Executable contract test suite definition
- Compatibility matrix by version and consumer
- Release gate criteria for contract compliance

## Workflow
1. Select high-risk consumer-provider interactions and define version scope.
2. Encode executable contracts for success and failure semantics.
3. Build compatibility matrix coverage across supported producer versions and transport modes.
4. Include internal and external consumer classes when both are supported.
5. Enforce CI blocking for incompatible changes on protected branches.
6. Publish failing contracts with impacted consumers, owner, and rollback advice.
7. Validate artifact compliance against the canonical API contract.

## Quality Gates
- Critical contracts are executable and version-scoped.
- CI blocks on incompatible contract changes.
- Failure reports identify impacted consumers clearly.
- Deprecation paths include migration guidance and consumer ownership.
- Consumer matrix remains current as new integrations are added.

## Failure Handling
- Stop integration/deployment gates when compatibility-breaking changes are unapproved.
- Stop integration/deployment gates when required consumer coverage is missing for supported versions.
- Escalate when contract ownership is ambiguous.
