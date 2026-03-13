---
name: git-cherry-pick-hotfix
description: "Select and apply minimal hotfix commits across branches via cherry-pick with dependency risk control. Use when urgent fixes must be propagated without pulling unrelated changes; do not use for CI workflow design or application behavior implementation."
---

# Git Cherry Pick Hotfix

## Overview
Use this skill to backport urgent fixes quickly while controlling dependency spillover and regression risk.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Dependency decision rules:
  - `references/cherry-pick-dependency-rules.md`

## Templates And Assets
- Hotfix cherry-pick plan:
  - `assets/hotfix-cherry-pick-plan-template.md`
- Verification checklist:
  - `assets/hotfix-verification-checklist.md`

## Inputs To Gather
- Source fix commit hashes and dependency notes.
- Target branch constraints and release timeline.
- Verification scope for target environment.
- Rollback expectations for failed backport.

## Deliverables
- Cherry-pick plan with dependency analysis.
- Source-to-target commit mapping record.
- Post-pick verification evidence.
- Rollback notes if target behavior diverges.

## Workflow
1. Build plan in `assets/hotfix-cherry-pick-plan-template.md`.
2. Validate dependency scope using `references/cherry-pick-dependency-rules.md`.
3. Apply minimal commit set in dependency-safe order.
4. Resolve conflicts and run target-branch verification.
5. Finalize with `assets/hotfix-verification-checklist.md`.

## Quality Standard
- Picked commits are minimal and intent-preserving.
- Hidden dependencies are explicitly documented.
- Target branch behavior matches fix objective.
- Rollback path exists before production rollout.

## Failure Conditions
- Stop when backport requires broad dependency migration.
- Stop when target branch cannot satisfy fix prerequisites.
- Escalate when behavior diverges from source assumptions after pick.
