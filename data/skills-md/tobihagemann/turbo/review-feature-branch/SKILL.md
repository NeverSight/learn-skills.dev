---
name: review-feature-branch
description: Orchestrate a comprehensive feature branch review with AI code review, findings evaluation, and optional finalization. Use when the user asks to "review feature branch", "review branch against main", "run full review", "check my branch before merging", or "review everything on this branch".
---

# Review Feature Branch

Orchestrate a feature branch review by running code review, evaluating findings, and optionally finishing with `/finalize`.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Code review
2. Confirm implementation
3. Finalize implementation

## Step 1: Code Review

Run the `/review-code` skill to review the feature branch against the base branch.

## Step 2: Confirm Implementation

After the code review summary, use `AskUserQuestion` to ask whether to proceed with finalization:

- **Proceed** — continue to Step 3
- **Skip** — stop here, leave changes as-is for manual review

## Step 3: Finalize Implementation

Run the `/finalize` skill.

## Rules

- If any phase fails, run the `/investigate` skill to diagnose the failure, apply the suggested fix, and retry. If investigation cannot identify a root cause, stop and report with investigation findings. Do not skip ahead.
