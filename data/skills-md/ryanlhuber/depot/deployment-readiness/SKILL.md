---
name: deployment-readiness
description: "Decides from evidence whether a change is safe to release to a target environment, and what rollout, monitoring, and rollback it needs, without deploying. Use when a release, an environment move, or a high-risk change is about to go live. Not for merge decisions or early planning."
disable-model-invocation: true
---

# Deployment Readiness

## Purpose
Return a go or no-go for releasing a change to a named environment, with the blockers and the release controls required. Merge readiness and deploy readiness are separate questions; this answers only the second.

## When to use
- Use when: a change is about to be released, an environment is changing, or a high-risk change needs a release decision.
- Do not use when: the question is whether to merge (use `merge-readiness-check`), or the work is still being specified or built.

## Inputs
- Required: a change summary, the target environment, test results, and the rollback plan.
- Optional: migrations included, configuration and secrets changes, monitoring in place, known risks, and release timing.
- Assumptions: an item with no evidence is not met.

## Process
1. Confirm the scope, the target environment, and the exact revision to be released.
2. Check each area against evidence: tests, migrations and their order, configuration and secrets, observability, capacity, dependencies, and the rollback path.
3. Mark each item Met, Not met, or Cannot verify. Treat Cannot verify as Not met.
4. List blockers and what would clear each one.
5. Recommend a rollout shape matched to the risk, such as all at once, staged, or behind a switch, and the signals that would trigger a rollback.
6. Return go only when every required item is Met.

## Rules and heuristics
- Required: no release without a stated rollback posture. If rollback is impossible, say so and require the risk to be accepted by its owner.
- Required: missing monitoring on a risky change is a finding, not a note.
- Required: never deploy, and never report a result that was not shown.
- Recommended: scale the rollout caution to the blast radius of the change, not to the size of the diff.

## Checks
- The revision assessed is the revision to be released.
- Every item has a status and evidence.
- Rollback and monitoring are addressed explicitly.

## Output
Return: go or no-go, the checklist with statuses, blockers, the rollout plan, rollback notes, and monitoring checks.

## Completion criteria
- A person can act on the decision without asking what it was based on.
- Nothing is marked Met without evidence.
