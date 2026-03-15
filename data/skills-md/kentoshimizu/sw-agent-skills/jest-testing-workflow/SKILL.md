---
name: jest-testing-workflow
description: "Jest verification workflow for JavaScript/TypeScript codebases with deterministic tests, explicit mock boundaries, and actionable CI evidence. Use when JS/TS changes need executable Jest evidence before merge; do not use for browser-level E2E or language-agnostic policy design."
---

# Jest Testing Workflow

## Overview
Use this skill to design and run Jest suites that are stable, meaningful, and decision-ready for merge gates.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Trigger examples and expected deliverables:
  - `references/trigger-and-examples.md`
- Mock boundary decision rules:
  - `references/mock-boundary-decision-rules.md`
- Determinism rules:
  - `references/jest-determinism-rules.md`

## Templates And Assets
- Test plan template:
  - `assets/jest-test-plan-template.md`
- Command profile template:
  - `assets/jest-command-profile-template.md`
- Flake triage checklist:
  - `assets/jest-flake-triage-checklist.md`

## Inputs To Gather
- Change scope and affected JS/TS modules.
- Runtime assumptions (`node`/`jsdom`) and mock boundaries.
- CI constraints for runtime and coverage gates.
- Known flaky areas (async timers, shared state, external dependencies).

## Deliverables
- Jest test strategy with mock/timer/environment policy.
- Assertion matrix for happy, edge, and failure paths.
- Local-fast and CI-full command profiles.
- Residual flakiness risk log with owner and next action.

## Workflow
1. Clarify decision question and mandatory quality constraints.
2. Draft strategy using `assets/jest-test-plan-template.md`.
3. Decide mock boundaries with `references/mock-boundary-decision-rules.md`.
4. Define execution profiles in `assets/jest-command-profile-template.md`.
5. Stabilize async/timer behavior with `references/jest-determinism-rules.md`.
6. Run checks and close with `assets/jest-flake-triage-checklist.md`.

## Quality Standard
- Trigger fit and test depth are explicit.
- Mock strategy preserves behavior confidence for critical paths.
- Async/timer behavior is deterministic in local and CI runs.
- Evidence is reproducible with exact commands and artifacts.

## Failure Conditions
- Stop when mock strategy hides behavior that must be integration-visible.
- Stop when command profile is not reproducible across local/CI.
- Escalate when flakiness persists after deterministic controls.
