---
name: fix-review
description: When the user asks to fix, address, or work on PR review comments — fetch review comments from a GitHub pull request and apply fixes to the local codebase. Requires gh CLI.
owner: chalk
version: "1.0.0"
metadata-version: "1"
allowed-tools: Bash, Read, Edit, Grep, Glob, Write
argument-hint: "[pr-number]"
---

# Fix PR Review Comments

Fetch review comments from a GitHub PR and apply fixes to the local codebase.

## Current PR context

!`gh pr view --json number,url,headRefName 2>/dev/null || echo "NO_PR_FOUND"`

## Step 1: Identify the PR

If the user provided a PR number as `$ARGUMENTS`, use that instead of the auto-detected PR above.

If no PR is found (output shows NO_PR_FOUND and no argument was given), stop and tell the user:
- There is no open PR for the current branch
- They need to either push and create a PR first, or provide a PR number

## Step 2: Verify gh CLI is available

```sh
gh --version 2>/dev/null || echo "GH_NOT_FOUND"
```

If `gh` is not installed, stop and tell the user to install it: https://cli.github.com

## Step 3: Fetch review comments

Fetch all inline review comments on the PR:

```sh
gh api repos/{owner}/{repo}/pulls/{number}/comments --paginate
```

Each comment object has these relevant fields:
- `path` — file path
- `line` (or `original_line`) — line number in the new file
- `body` — the comment text
- `diff_hunk` — surrounding diff context
- `user.login` — who posted it

## Step 4: Parse and classify comments

### Bot review comments (structured severity markers)

Look for severity markers in the comment `body`:
- `**🔴 Critical**` — Must fix. Production crash, security, data loss.
- `**🟠 High**` — Must fix. Significant bugs, logical flaws.
- `**🟡 Medium**` — Should fix. Tech debt, best practice deviation.
- `**🟢 Low**` — Optional. Nitpick, stylistic.
- `**✨ Praise**` — Skip. Positive feedback.

Also extract from the body:
- **Category** (e.g. `**✅ Correctness**`, `**🛡️ Security**`) — appears after severity on the first line
- **Comment text** — the main feedback paragraph
- **Why it matters** — appears in a blockquote starting with `💡 **Why it matters:**`
- **Code suggestion** — appears in a ` ```suggestion ` fenced block (GitHub's suggested change format)

### Human review comments (no severity markers)

If a comment has no structured severity markers, classify it as a **human comment**. Do NOT auto-fix these — list them separately for the user to address manually.

### Fallback: no bot comments found

If there are zero comments with severity markers, treat ALL comments as potentially actionable:
- Show them to the user in a summary table
- Ask which ones to address
- Only proceed with explicit user confirmation

## Step 5: Apply fixes

Sort bot comments by severity: Critical > High > Medium > Low.

For each comment (Critical, High, and Medium severity):
1. Read the file at `path`
2. Understand the issue described in the comment
3. If a `suggestion` block exists, use it as a strong hint — but verify it makes sense in context before applying blindly
4. Show the proposed fix to the user and ask for explicit confirmation before applying it.
5. If a comment is unclear or the fix would require broader refactoring beyond the scope, note it and skip

For Low severity: skip unless trivially fixable (one-line change).

For Praise: skip entirely.

## Step 6: Summary

After applying fixes, provide a summary table:

| Severity | File | Line | Status | Notes |
|----------|------|------|--------|-------|
| 🔴 Critical | path/to/file.ts | 42 | ✅ Fixed | Brief description |
| 🟠 High | path/to/other.ts | 17 | ⏭️ Skipped | Requires broader refactor |

Then list:
- **Skipped comments** with reasoning
- **Human feedback** (non-bot comments) that the user should address manually

## Rules

- Do NOT blindly apply suggestions without reading the surrounding code
- Do NOT modify files that weren't mentioned in review comments
- If there are no review comments on the PR, tell the user and stop
- Human review comments should be shown to the user but not auto-fixed — list them separately as "Human feedback to address"
- If `gh` CLI is not authenticated, tell the user to run `gh auth login`
