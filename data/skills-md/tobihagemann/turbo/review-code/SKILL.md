---
name: review-code
description: Run AI code review and evaluate findings. Delegates to `/peer-review` for the review and `/evaluate-findings` for triage. Use when the user asks to "review code", "code review", "review my changes", or wants a reviewed and evaluated set of findings.
---

# Review Code

Run AI code review and evaluate findings.

## Step 1: Peer Review

Run the `/peer-review` skill. Pass the appropriate context:

- **Uncommitted changes**: `--uncommitted`
- **Against a base branch**: `--base <branch>`
- **Specific commit**: `--commit <sha>`

Default to reviewing against the repository's default branch (detect via `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`). If the caller specifies a different base, use that.

Capture the full review output.

## Step 2: Evaluate Findings

Run the `/evaluate-findings` skill on the review output.

If there are additional findings to include (e.g., PR comments passed in by the caller), combine them with the review output before evaluation.

If zero actionable findings survive evaluation, report that the code looks clean.

## Rules

- If the peer review tool is not available or returns malformed output, report the error and stop.
- Process findings in file order to minimize context switching.
