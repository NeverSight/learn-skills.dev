---
name: github-pull-request-review
version: 1.0.1
description: Comprehensive GitHub pull request review using the gh CLI. Reviews PR diffs against linked issues, repo conventions, and codebase context. Checks for bugs, security risks, style consistency, and goal alignment. Runs available lint, type-check, and test commands. Produces a prioritized report with an approve/block verdict. Use this skill whenever the user asks to "review a PR", "check PR #123", "audit a pull request", "is this PR ready to merge", "review this pull request", "what do you think of PR #N", "code review", "look at this PR", or any request involving evaluating GitHub code changes before merge.
---

# PR Review Workflow

Follow these phases in order. The user provides a PR number (e.g., `#123` or `123`). The repo must be cloned locally and `gh` must be authenticated.

## Phase 1 — Gather Context

1. **Fetch PR metadata:**
   ```bash
   gh pr view <PR> --json title,body,baseRefName,headRefName,state,labels,milestone,author,reviewRequests,reviews,additions,deletions,changedFiles
   ```

2. **Fetch PR comments** (PR-level discussion):
   ```bash
   gh api --paginate repos/{owner}/{repo}/issues/{pr_number}/comments --jq '.[] | {body, user: .user.login, created_at}'
   ```

3. **Fetch inline review comments** (code-level — the issues endpoint above does NOT include these):
   ```bash
   gh api --paginate repos/{owner}/{repo}/pulls/{pr_number}/comments --jq '.[] | {path, line, body, user: .user.login}'
   ```
   Auto-detect `{owner}/{repo}` with: `gh repo view --json nameWithOwner --jq .nameWithOwner`

4. **Fetch the diff:**
   ```bash
   gh pr diff <PR>
   ```
   If the diff exceeds 50 files, list changed files first with `gh api --paginate repos/{owner}/{repo}/pulls/{pr}/files --jq '.[].filename'` and read them individually.

5. **Extract linked issues** from the PR body. Parse patterns: `Fixes #N`, `Closes #N`, `Resolves #N`, `Related to #N`, or bare `#N`. For each:
   ```bash
   gh issue view <N> --json title,body,comments,labels,state
   ```

6. **Check CI status:**
   ```bash
   gh pr checks <PR>
   ```
   If any checks failed, fetch logs: `gh run view <RUN_ID> --log-failed`

You may also run `scripts/fetch-pr-context.sh <PR_NUMBER>` to automate steps 1-6.

## Phase 2 — Understand Repo Conventions

Read each file if it exists:
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CODEOWNERS`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `README.md` (project overview and architecture)
- `AGENTS.md` or `CLAUDE.md` (agent-specific instructions)

Detect linter/formatter configs to understand style expectations:
- `.eslintrc*`, `biome.json`, `.prettierrc*`, `pyproject.toml`, `ruff.toml`, `.rubocop.yml`, `.golangci.yml`, etc.

Read CI workflow files (`.github/workflows/*.yml`) to understand existing automated checks.

## Phase 3 — Analyze the Code Changes

Review the diff against these priorities. See [references/review-checklist.md](references/review-checklist.md) for detailed guidance.

1. **Goal alignment** — Does the PR achieve what the linked issue(s) describe? Missing requirements? Scope creep?
2. **Bugs and logic errors** — Off-by-one, null handling, race conditions, missing edge cases, broken error handling.
3. **Security risks** — Only HIGH-confidence findings. Trace data flow from source to sink. See the checklist for common false positives to avoid.
4. **Codebase consistency** — Compare against surrounding code, not abstract ideals. Naming, file organization, import patterns, architecture.
5. **Test coverage** — New paths tested? Existing tests updated? Obvious untested edge cases?
6. **Performance** — N+1 queries, unbounded loops, missing pagination, large memory allocations.
7. **Documentation** — Public APIs documented? Complex algorithms explained? Breaking changes noted?

## Phase 4 — Run Available Checks

Detect available commands by running `scripts/detect-repo-checks.sh` or manually inspecting `package.json`, `Makefile`, `pyproject.toml`, and CI workflow files.

Run in this order (stop if a step fails catastrophically):
1. **Lint** (e.g., `npm run lint`, `ruff check .`, `golangci-lint run`)
2. **Type-check** (e.g., `npx tsc --noEmit`, `mypy .`, `pyright`)
3. **Tests** — prefer running only tests relevant to changed files when possible

**Guardrails:**
- Do NOT run commands that could modify state (deploy, migrate, publish, seed).
- If unsure what a command does, skip it and note it in the report.
- If no checks are available, note this and move on.

## Phase 5 — Produce the Report

Generate a structured report. See [references/report-format.md](references/report-format.md) for the full template.

```
## PR Review: #<number> — <title>
### Summary
### Verdict: ✅ APPROVE / ⚠️ APPROVE WITH COMMENTS / ❌ REQUEST CHANGES
### Blocking Issues (must fix before merge)
### Non-blocking Issues (should fix)
### Positive Observations
### Checks (table: Lint, Type-check, Tests, CI)
### Context (linked issues, files changed, additions/deletions)
```

**Rules:**
- Rank blocking issues by severity: security > bugs > logic > breaking changes.
- Every issue must reference a specific file and line.
- If nothing significant is found, say so — do not invent issues.
- Include positive feedback for well-written code.

## Phase 6 — Post Review on GitHub (only if user requests)

If the user asks to post the review on the PR:
- APPROVE: `gh pr review <PR> --approve --body "<summary>"`
- REQUEST CHANGES: `gh pr review <PR> --request-changes --body "<report>"`
- APPROVE WITH COMMENTS: `gh pr review <PR> --comment --body "<report>"`

You may use `scripts/post-review-comment.sh <PR> <verdict> <body_file>`.

**Always confirm with the user before posting.**

## References

- [references/review-checklist.md](references/review-checklist.md) — Detailed review checklist by category
- [references/report-format.md](references/report-format.md) — Report template with good/bad finding examples
- [references/gh-cli-reference.md](references/gh-cli-reference.md) — gh CLI commands and API endpoints cheat sheet
