---
name: pytest-workflow
description: "Pytest verification workflow for Python changes with deterministic fixtures, explicit case strategy, and CI-ready evidence. Use when Python modules need executable pytest evidence before merge; do not use for browser-level E2E or non-Python test tooling decisions."
---

# Pytest Workflow

## Overview
Use this skill to design pytest suites that are fast enough for daily feedback and stable enough for CI gates.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Trigger examples:
  - `references/trigger-and-examples.md`
- Fixture boundary rules:
  - `references/fixture-boundary-rules.md`
- Determinism rules:
  - `references/pytest-determinism-rules.md`

## Templates And Assets
- Test plan template:
  - `assets/pytest-test-plan-template.md`
- Fixture stability checklist:
  - `assets/pytest-fixture-stability-checklist.md`
- Command profile template:
  - `assets/pytest-command-profile-template.md`

## Inputs To Gather
- Python modules and behaviors at risk.
- Fixture graph, dependency seams, and isolation constraints.
- Marker strategy and CI runtime/cost limits.
- Known flaky paths (async timing, shared state, environment coupling).

## Deliverables
- Pytest test strategy and case matrix.
- Fixture and parametrization policy.
- Local-fast and CI-full command profiles.
- Residual risk and follow-up actions.

## Workflow
1. Build case strategy with `assets/pytest-test-plan-template.md`.
2. Apply fixture rules from `references/fixture-boundary-rules.md`.
3. Validate determinism using `references/pytest-determinism-rules.md`.
4. Define execution profiles in `assets/pytest-command-profile-template.md`.
5. Finalize with `assets/pytest-fixture-stability-checklist.md`.

## Quality Standard
- Fixtures are explicit, scoped, and deterministic.
- Case coverage includes happy/edge/failure paths.
- Command profiles are reproducible across local and CI.

## Failure Conditions
- Stop when fixture design causes hidden shared state behavior.
- Stop when test determinism cannot be achieved for critical flows.
- Escalate when runtime cost blocks practical feedback loops.
