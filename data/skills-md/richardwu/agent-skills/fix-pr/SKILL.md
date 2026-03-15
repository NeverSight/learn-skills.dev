---
name: fix-pr
description: "Fix issues on the current PR: address bot (eg Claude Code, CodeRabbit, or custom GHA) review comments and fix failing CI checks. Use when asked to fix PR, fix review comments, fix CI, or fix checks. Triggers on: fix pr, fix review, fix ci, fix checks, fix failing checks."
user-invocable: true
---

# Fix PR

Fixes the current PR by addressing bot review comments and failing CI checks. Runs in a loop until everything is green.

---

## Prerequisites

- You must be on a branch that has an open PR
- The repo remote is on GitHub (uses `gh` CLI)

---

## Step 1: Identify the PR

Run:
```
gh pr view --json number,headRefName,url
```

If no PR is found for the current branch, tell the user and stop.

---

## Step 2: Fix Loop

Repeat the following loop. Each iteration is called a "round". Track what you fix in each round for the final summary.

### 2a. Wait for CI checks to settle

Poll CI status until all checks have completed (no `PENDING` or `IN_PROGRESS` states):

```
gh pr checks {pr_number} --json name,state
```

Poll every 30 seconds. If checks haven't settled after 10 minutes, tell the user and stop.

While waiting, print a brief status update each poll (e.g. "Waiting for CI... 3/6 checks complete").

### 2b. Wait for bot review (if applicable)

After CI settles, check if there's a bot code review check (e.g. `claude-review`). If so, wait for the bot to post its review comment.

Count existing bot comments:
```
gh api repos/{owner}/{repo}/issues/{pr_number}/comments --jq '[.[] | select(.user.type == "Bot")] | length'
```

If the bot review check passed but no **new** bot comment appeared since your last push (track the comment count from before your push), poll every 15 seconds for up to 5 minutes for a new comment to appear.

If no bot review check exists, skip this step.

### 2c. Fetch bot review comments

Get reviews from bots on the PR:
```
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews --jq '.[] | select(.user.type == "Bot") | {id: .id, user: .user.login, body: .body, state: .state}'
```

Also fetch issue-level comments from bots:
```
gh api repos/{owner}/{repo}/issues/{pr_number}/comments --jq '.[] | select(.user.type == "Bot") | {id: .id, body: .body, user: .user.login}'
```

Only consider the **latest** comment from each bot (by id). Ignore older comments from the same bot — they relate to previous iterations.

### 2d. Parse actionable issues from bot reviews

From the latest bot review comments, identify actionable bugs and issues. Ignore:
- Style nitpicks and suggestions that are not bugs
- Comments that are purely informational
- Comments on code that is not part of this PR's changes
- Issues marked as resolved or "✅" in the review

Focus on:
- Actual bugs flagged (🔴 or similar severity markers)
- Security issues
- Logic errors
- Missing error handling that could cause crashes

### 2e. Check user exclusions

The user may specify bugs NOT to fix when invoking this skill (e.g. `/fix-pr skip US-033 skeleton issue`). If the user specified exclusions, match them against the identified issues and skip those.

Present the list of issues you plan to fix to the user before proceeding. Format:
```
Round N — Found M issues:
1. [file:line] Description of issue (source: bot-name / CI check-name)
2. [file:line] Description of issue
   (skipped - user excluded)

Fixing M issues...
```

### 2f. Fix failing CI checks

Check which CI checks failed:
```
gh pr checks {pr_number} --json name,state
```

For each failing check, determine the type from the CI workflow (`.github/workflows/ci.yml`):
- **lint**: `bunx biome ci .` — fix lint/format issues
- **typecheck**: `bunx tsc --noEmit` — fix type errors
- **test**: `bun run test` — fix failing tests
- **build**: `bun run build` — fix build errors
- **validate-i18n**: `bun run validate:i18n` — fix missing i18n keys

Reproduce and fix locally:
1. **lint** failures: Run `bunx biome ci .` to see errors, then `bunx biome check --write .` to auto-fix. Manually fix the rest.
2. **typecheck** failures: Run the failing tsc command, read errors, fix type issues.
3. **test** failures: Run `bun run test`, read test files and source code, fix issues.
4. **build** failures: Run `bun run build`, read errors, fix them.
5. **validate-i18n** failures: Run `bun run validate:i18n`, add missing keys.

After fixing, re-run the same command to verify it passes before moving on.

### 2g. Fix bot review issues

Read each affected file, understand the context, and apply fixes. Follow the project's existing patterns and conventions (check CLAUDE.md or AGENTS.md).

### 2h. Commit and push

After all fixes for this round are applied:

1. Stage the changed files (use specific file names, not `git add -A`)
2. Commit with a descriptive message following the repo's commit style:
   ```
   fix: address PR review feedback

   - [describe each fix briefly]
   ```
3. Push to the current branch
4. Record the bot comment count before this push (for step 2b next round)

### 2i. Check if done

If there were **no failing CI checks** and **no actionable bot review issues** in this round, exit the loop and go to Step 3.

If this is round 3 or higher, stop looping — tell the user the remaining issues and ask for guidance.

---

## Step 3: Summary

Print a summary table of everything fixed across all rounds:

```
## Fix PR Summary

| Round | Source | Issue | File | Status |
|-------|--------|-------|------|--------|
| 1 | CI: lint | Formatting error in workspaces.ts | convex/functions/workspaces.ts | ✅ Fixed |
| 1 | claude[bot] | Missing membership status check | convex/functions/workspaces.ts:454 | ✅ Fixed |
| 2 | CI: typecheck | Type error from previous fix | convex/functions/workspaces.ts:351 | ✅ Fixed |
| - | claude[bot] | Use Doc<"users"> instead of inline type | convex/functions/workspaces.ts:353 | ⏭️ Skipped (style nit) |

All checks passing. PR is ready for review.
```

Include:
- Every issue encountered (fixed, skipped, or excluded)
- The source (which bot or CI check)
- The file and line where relevant
- Status: ✅ Fixed, ⏭️ Skipped (with reason), 🚫 Excluded (user requested)

---

## Important Notes

- Do NOT fix issues the user explicitly excluded
- Do NOT make unrelated changes or refactors while fixing
- If a review comment is ambiguous or you're unsure how to fix it, ask the user
- If a CI check failure is unrelated to this PR's changes (e.g. flaky test, pre-existing issue), tell the user rather than attempting a fix
- Always verify fixes locally before committing (re-run the failing command)
- Max 3 rounds to avoid infinite loops — escalate to user after that
