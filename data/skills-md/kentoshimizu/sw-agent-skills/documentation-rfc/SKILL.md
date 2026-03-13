---
name: documentation-rfc
description: "Author RFC documents for proposed technical changes with clear problem framing, options, tradeoffs, and decision path. Use when proposal alignment and review sign-off are needed before implementation; do not use for post-decision implementation-only docs."
---

# Documentation RFC

## Overview
Use this skill to produce decision-ready RFCs that let stakeholders review options with clear tradeoffs and risks.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Decision quality checks:
  - `references/rfc-decision-quality-checks.md`

## Templates And Assets
- RFC template:
  - `assets/rfc-template.md`
- Tradeoff matrix template:
  - `assets/rfc-tradeoff-matrix-template.csv`

## Inputs To Gather
- Problem statement and business/technical motivation.
- Constraints and non-goals.
- Candidate options and evaluation criteria.
- Risks, rollout implications, and decision timeline.

## Deliverables
- RFC with context, options, recommendation, and rationale.
- Tradeoff table and risk assessment.
- Open questions and decision dependencies.
- Review checklist and approval path.

## Quick RFC Skeleton
1. Problem and goals/non-goals.
2. Constraints and assumptions.
3. Options considered (including rejected options).
4. Recommendation and rationale.
5. Risks, rollout, and rollback considerations.
6. Open questions and required approvals.

## Quality Standard
- Problem framing is concrete and scope-bounded.
- Options are comparable with explicit criteria.
- Recommendation includes why alternatives were rejected.
- Risks and unknowns are clearly separated.

## Workflow
1. Define problem scope and success criteria.
2. Collect options and evaluation evidence.
3. Compare options with explicit tradeoff criteria in `assets/rfc-tradeoff-matrix-template.csv`.
4. Draft recommendation and risk treatment plan using `assets/rfc-template.md`.
5. Publish for review with clear decision deadlines.

## Failure Conditions
- Stop when recommendation lacks option comparison evidence.
- Stop when major risks/unknowns are hidden or untracked.
- Escalate when required approvers are missing for high-impact decisions.
