---
name: git-rebase-workflow
description: "Linearize local branch history with safe rebase practices before integration. Use when branch history cleanup is needed and rebase risks (conflicts, dropped commits, rewritten history impact) must be controlled; do not use for CI workflow design or application behavior implementation."
---

# Git Rebase Workflow

## Overview
Use this skill to clean local history for reviewability while avoiding unsafe rewrite on shared branches.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Rebase safety rules:
  - `references/rebase-safety-rules.md`

## Templates And Assets
- Rebase readiness checklist:
  - `assets/rebase-readiness-checklist.md`
- Conflict log template:
  - `assets/rebase-conflict-log-template.md`

## Inputs To Gather
- Branch divergence from target base.
- Branch sharing status and PR status.
- Force-push/rewrite policy constraints.
- Verification scope for rewritten commits.

## Deliverables
- Rebase execution notes with conflict rationale.
- Verification evidence for rewritten history.
- Push plan aligned to force-with-lease policy.

## Workflow
1. Confirm rebase eligibility using `assets/rebase-readiness-checklist.md`.
2. Fetch latest base and inspect commit divergence.
3. Rebase commits in logical sequence.
4. Record conflict resolutions in `assets/rebase-conflict-log-template.md`.
5. Verify behavior and push per `references/rebase-safety-rules.md`.

## Quality Standard
- Rebased commits preserve original behavioral intent.
- Rewrite policy is followed without exceptions.
- Conflict decisions are documented and test-verified.
- Resulting history is easier to review without hiding risk.

## Failure Conditions
- Stop when branch is shared or already under open PR policy constraints.
- Stop when rebase would rewrite protected/shared history.
- Escalate when rewrite exceptions are requested without approval.
