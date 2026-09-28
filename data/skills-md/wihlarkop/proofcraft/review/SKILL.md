---
name: review
description: >-
  Review a code or change diff against intended behavior, repository standards, and relevant risk
  domains. Use for explicit PR/diff/design review. Default to read-only unless fixes are
  requested. Validate suspicious findings before reporting them, compose only concerns touched by
  the diff, and prioritize actionable evidence-backed issues instead of speculative commentary.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# Review

Review the intended change, not the entire software universe.

## Entry

Default to read-only review. Modify code only when the user explicitly asks for fixes or the active workflow has already authorized remediation.

## Workflow

1. Understand intended behavior from the request/spec/plan and inspect the actual diff.
2. Determine which risk domains the diff truly touches. Compose only those specialist concerns.
3. Check correctness, compatibility, failure behavior, tests/evidence, and repository conventions at the affected boundaries.
4. Validate suspicious findings in surrounding code or direct evidence before reporting them.
5. Prioritize material, actionable findings. Distinguish blockers from improvements and avoid style churn already covered by automated tooling.

A green test suite is evidence, not proof that the implementation matches the intended contract.

## Outputs

A concise set of prioritized findings with file/location/evidence where available, plus an explicit no-material-findings result when appropriate.

## Stop

Stop when the material diff and relevant risk domains have been reviewed. Do not invent findings to fill a quota or launch unrelated refactoring.
## Reference Guide

Load only the references needed for the current task:

- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [reality check](references/_shared/orchestration/reality-check.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [diff discipline](references/_shared/engineering/diff-discipline.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
