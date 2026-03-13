---
name: review-pr
description: Orchestrate a comprehensive PR review with AI code review, PR comment analysis, findings evaluation, and optional finalization. Use when the user asks to "review PR", "review pull request", "review this PR", "check PR before merging", or "full PR review".
---

# Review PR

Orchestrate a PR review by running code review, fetching PR comments, evaluating all findings together, and optionally finishing with `/finalize`.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Code review and PR comments
2. Confirm implementation
3. Finalize implementation

## Step 1: Code Review and PR Comments

Run the `/review-code` skill to review the feature branch against the base branch. Pass any PR comments as additional findings.

Fetch PR comments by running the `/fetch-pr-comments` skill. Include the unresolved comments as additional findings for the `/review-code` evaluation step.

## Step 2: Confirm Implementation

After the code review summary, use `AskUserQuestion` to ask whether to proceed with finalization:

- **Proceed** — continue to Step 3
- **Skip** — stop here, leave changes as-is for manual review

## Step 3: Finalize Implementation

Run the `/finalize` skill.

## Rules

- If any phase fails, run the `/investigate` skill to diagnose the failure, apply the suggested fix, and retry. If investigation cannot identify a root cause, stop and report with investigation findings. Do not skip ahead.
