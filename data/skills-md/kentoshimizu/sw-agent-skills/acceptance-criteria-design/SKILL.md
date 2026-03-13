---
name: acceptance-criteria-design
description: "Design executable acceptance criteria for approved requirements by converting goals/specs into binary pass/fail checks with observable outcomes. Use when implementation handoff, QA validation, or release decisions need testable criteria for stable `REQ-*`/`NFR-*` baselines; do not use for requirement discovery, prioritization, or sprint slicing."
---

# Acceptance Criteria Design

## Overview
Use this skill to translate approved requirements into acceptance criteria that engineering and QA can execute without interpretation drift.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Inputs To Gather
- Approved requirements (`REQ-*`) and relevant non-functional requirements (`NFR-*`).
- Business intent, out-of-scope boundaries, and policy constraints.
- User-visible behaviors, system side effects, and error paths.
- Test environment capabilities and observability limits.

## Deliverables
- Acceptance criteria set with binary pass/fail expectations.
- Scenario matrix covering happy path, boundary, negative, and failure cases.
- Traceability map: requirement -> criterion -> verification method.
- Open ambiguity list that blocks objective verification.

## Quality Standard
- Each criterion is independently testable and yields one clear result.
- Each criterion states preconditions, action, expected observable outcome, and evidence source.
- Boundary values, invalid inputs, authorization errors, and integration failure behavior are covered when applicable.
- Criteria describe required behavior, not implementation detail.
- Overlap and contradiction across criteria are removed.

## Workflow
1. Normalize requirement intent and explicit assumptions.
2. Split requirements into observable behavior units.
3. Draft pass/fail criteria for normal, boundary, negative, and failure scenarios.
4. Define evidence sources (API response, UI state, logs, metrics, events) for each criterion.
5. Run ambiguity and overlap review; publish unresolved blockers.

## Failure Conditions
- Stop when requirement intent is unstable or contradictory.
- Stop when a criterion cannot be verified with available test/observability capabilities.
- Escalate when missing instrumentation prevents objective pass/fail judgment.
