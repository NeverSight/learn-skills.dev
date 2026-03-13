---
name: feature-flag-strategy
description: "Feature flag lifecycle governance workflow for safe rollout, blast-radius control, and cleanup discipline. Use when feature rollout needs runtime controls (targeting, staged exposure, kill-switch policy, ownership, and retirement lifecycle) and those rules are not yet explicit; do not use for statistical experiment design and analysis."
---

# Feature Flag Strategy

## Overview
Use this skill to manage feature flags as controlled release instruments, not permanent complexity.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Lifecycle decision rules:
  - `references/flag-lifecycle-decision-rules.md`
- Targeting and blast-radius guidance:
  - `references/flag-targeting-risk-guidance.md`

## Templates And Assets
- Flag catalog template:
  - `assets/feature-flag-catalog-template.csv`
- Rollout plan template:
  - `assets/flag-rollout-plan-template.md`
- Retirement checklist:
  - `assets/flag-retirement-checklist.md`

## Inputs To Gather
- Rollout objective, user segments, and release risk tolerance.
- Blast-radius constraints and required kill-switch latency.
- Operational/compliance constraints and on-call readiness.
- Flag platform capabilities, dependency behavior, and telemetry coverage.

## Deliverables
- Flag definition with owner, type, kill-switch, and expiry.
- Rollout plan with progression gates and rollback policy.
- Lifecycle decision record including retirement criteria.
- Verification evidence for targeting and disable behavior.

## Workflow
1. Decide whether a flag is warranted using `references/flag-lifecycle-decision-rules.md`.
2. Register flags in `assets/feature-flag-catalog-template.csv` with ownership and expiry.
3. Define rollout and rollback using `assets/flag-rollout-plan-template.md`.
4. Validate targeting safety using `references/flag-targeting-risk-guidance.md`.
5. Retire flags using `assets/flag-retirement-checklist.md` once control is no longer needed.

## Quality Standard
- Every flag has owner, kill-switch, and retirement date.
- Rollout and rollback criteria are measurable and pre-defined.
- Targeting rules are auditable and operationally safe.
- Retired flags are removed from code paths, not just disabled.

## Failure Conditions
- Stop when flags lack ownership, expiry, or safe disable paths.
- Stop when targeting rules create unbounded or opaque blast radius.
- Escalate when accepted rollout risk exceeds policy thresholds.
