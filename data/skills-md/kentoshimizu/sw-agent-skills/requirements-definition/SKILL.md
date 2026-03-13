---
name: requirements-definition
description: "Canonical requirement baseline workflow after evidence collection. Use when elicitation evidence is ready and must be synthesized into a traceable, testable requirement baseline; do not use for prioritization or implementation slicing."
---

# Requirements Definition

## Overview
Use this skill to convert validated evidence into a stable requirement baseline with traceability and ownership.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared Requirements Contract
- Governance contract:
  - `references/requirements-governance-contract.md`
- Manifest field guide:
  - `references/manifest-field-guide.md`
- Optional validator (if repository enforces manifest validation):
  - `python3 scripts/validate_requirements_contract.py --manifest <path/to/manifest.json>`

## Templates And Assets
- Requirement baseline checklist:
  - `assets/requirements-baseline-checklist.md`
- Valid sample manifests:
  - `assets/rqm-def-manifest.valid.json`
  - `assets/rqm-cmp-manifest.valid.json`

## Inputs To Gather
- Elicitation evidence with source references.
- Product goals, constraints, and operating assumptions.
- Architecture and compliance constraints.

## Deliverables
- Canonical `REQ-*` baseline.
- Scope and out-of-scope decisions.
- Traceability map (requirement -> evidence).
- Decision/open-issue log with owners.

## Workflow
1. Translate evidence into atomic requirement statements.
2. Link every requirement to supporting evidence.
3. Separate functional requirements and quality constraints.
4. Validate baseline using `assets/requirements-baseline-checklist.md`.
5. Publish baseline and unresolved decision items.

## Quality Standard
- Each requirement is atomic, testable, and source-traceable.
- Scope boundaries are explicit.
- Ownership and validation method are defined.

## Failure Conditions
- Stop when conflicting requirements lack decision authority.
- Stop when mandatory constraints are not represented.
- Escalate when baseline cannot be approved due to unresolved contradictions.
