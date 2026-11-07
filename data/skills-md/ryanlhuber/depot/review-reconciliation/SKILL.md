---
name: review-reconciliation
description: "Combines independent review reports for one revision into a single deduplicated finding list with a blocking set, and chooses how much re-review a repair needs. Use when two or more reviews of a change are complete, or when a repair follows a failed review. Not for performing the reviews or for the final merge decision."
disable-model-invocation: true
---

# Review Reconciliation

## Purpose
Turn separate, independently produced review reports into one finding list the builder can act on, and decide how much re-review a repair requires, without weakening any reviewer's result.

## When to use
- Use when: every planned review of a revision is complete, or a repair has been made after a FAIL and the re-review scope must be chosen.
- Do not use when: a review is still in progress (do not show one reviewer's findings to another before its initial report), or the question is whether the change may merge (use `merge-readiness-check`).

## Inputs
- Required: each review report with its revision identifier, verdict, and findings; the approved specification; test results.
- Optional, for repairs: the repair diff, the revision that was reviewed, and the findings the repair addresses.
- Assumptions: reports were produced independently. If one reviewer saw another's output, note it on that report and reduce reliance on it.

## Process
1. Check that every report names the same revision. A report for another revision cannot count toward this one; list it as stale.
2. Merge duplicate findings by cause, keeping each source report and its evidence. Keep a finding that only one reviewer raised; mark it as unique to that reviewer.
3. Keep each finding's severity. If reports rate one cause differently, keep the higher severity and record the disagreement for the requester.
4. Build the blocking set: every unresolved Moderate or Major finding. All severities return to the builder unless the process says otherwise.
5. Order the fix list by severity, then dependency, and name any finding that needs the requester's decision.
6. For a repair, choose the re-review tier from the repair diff using the rules below, and record the approved revision, the repair revision, and the verified scope.
7. Complete the [consolidated findings](templates/consolidated-findings.md).

## Rules and heuristics
- Required: re-review tiers. Tier A is a diff-only check by the reviewer who raised the finding, allowed only for demonstrably non-behavioral changes such as comments and formatting. Tier B reruns both reviews for behavioral changes: logic, tests, security, accessibility, runtime behavior, and instructions an agent reads. Tier C is for major or uncertain changes: full reviews by both, plus tests.
- Required: any change to a file an agent reads as instructions (prompts, skill files, agent configurations, review prompts) is at least Tier B, never Tier A.
- Required: a Tier A check must name the approved revision, the repair revision, and the verified scope. If the scope cannot be established, do a full re-review. When unsure, use the stricter tier.
- Required: an approval is tied to one revision. A new revision invalidates earlier approvals unless a Tier A check covers it.
- Required: never drop, merge away, or downgrade a finding to reach a PASS. A concern without evidence stays in remaining uncertainty.
- Recommended: group findings by cause so one fix can close several.

## Checks
- Every report is for the stated revision or listed as stale.
- Each merged finding keeps its source reports, evidence, and severity.
- The blocking set equals the unresolved Moderate and Major findings.
- The re-review tier follows the rules and names its scope.

## Output
Return the consolidated findings: the revision, the verdicts received, the merged findings with sources, the blocking set, the ordered fix list, items needing a decision, disagreements between reviewers, and for a repair the chosen re-review tier. Use the [consolidated findings](templates/consolidated-findings.md).

## Completion criteria
- One list stands for all reports without losing any source or severity.
- The blocking set and the next review step are explicit.
- Every approval and re-review is tied to a named revision.
