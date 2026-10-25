---
name: merge-readiness-check
description: "Verifies from evidence whether a change meets its merge preconditions and returns ready or not ready with the blockers, without merging. Use when a change has completed review and someone is about to merge it. Not for performing reviews or for the merge itself."
disable-model-invocation: true
---

# Merge Readiness Check

## Purpose
Check, item by item and from evidence, that a change may be merged, and return a decision a human can act on. The check never merges and never bypasses a required check or rule.

## When to use
- Use when: reviews of a change are complete and a merge is being considered, or a change was repaired and approvals must be confirmed again.
- Do not use when: reviews are still running, or the task is to perform or reconcile a review (use the review skills or `review-reconciliation`).

## Inputs
- Required: the change's current head revision, test evidence, the review reports and their revisions, the reconciled findings, the target branch, and the change's risk level.
- Optional: the status of required checks and approval rules on the target (for example required passing checks or required reviews), recorded human approvals, the execution record, and post-merge checks.
- Assumptions: the change may be tracked in any hosting or review system, or in a file; "change record" means wherever it is tracked. Read the target branch from project configuration or the change record; never assume it is the default branch.

## Process
1. Take the head revision from the change itself, not from a report.
2. Walk the checklist in the [merge checklist](templates/merge-checklist.md), marking each item Met, Not met, or Cannot verify, with the evidence.
3. Treat any item that cannot be verified as not met. Do not infer it from the other items.
4. Return ready only when every item is Met. Otherwise return not ready and list each blocker with what would clear it.
5. After a merge a human performed, run the post-merge items and report any that fail.

## Rules and heuristics
- Required: tests pass, with evidence linked. Never accept or report a passing result that was not shown.
- Required: the head revision equals the revision both reviews examined. A newer revision needs re-review at the tier the repair requires, unless a diff-only check covers it.
- Required: both reviews are PASS, each bound to a revision, either the head revision or the approved revision that a recorded Tier A check extends to the head revision, and the second reviewer did not see the first reviewer's output before its initial report.
- Required: the builder and the reviewers are independent, as the process requires. Variants or versions of one model family, or one family used through different tools, are not independent.
- Required: no Moderate or Major finding is unresolved, and every repair was re-reviewed at the correct tier.
- Required: both review reports are attached to the change record together, after both reviews finished.
- Required: the change targets the correct branch, and required checks and approval rules pass. Never recommend bypassing a required check or rule.
- Required: a high-risk change has a recorded human approval. The requester, not this check, approves it.
- Recommended: name the single most important blocker first.

## Checks
- Every checklist item has a status and evidence, or is marked Cannot verify.
- The decision follows from the statuses with no override.
- Each blocker names what would clear it.

## Output
Return the completed merge checklist, the decision (ready or not ready), the blockers ordered by importance, the human approvals still needed, and, after a merge, the post-merge results. Use the [merge checklist](templates/merge-checklist.md).

## Completion criteria
- The decision is ready only if every item is Met, and not ready otherwise.
- Every unverifiable item is reported as such, not assumed.
- No merge was performed and no required check or rule was bypassed.
