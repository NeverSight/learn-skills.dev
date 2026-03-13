---
name: read-only-gh-pr-review
description: Review backend pull requests for correctness, security, performance, maintainability, and test coverage using GitHub CLI plus local repository inspection. Use when asked to review service-layer/API/database changes, audit backend branch diffs, summarize backend risk, or produce actionable must-fix/should-fix feedback.
compatibility: Requires GitHub CLI (gh), an authenticated GitHub account, and network access.
---

# PR Review (Backend, GitHub CLI)

## Overview

Review backend pull requests end-to-end using local code analysis and GitHub CLI API calls. Report only actionable, high-signal findings.

## Tool Constraints

- Use only: `SemanticSearch`, `WebSearch`, `Grep`, `LS`, `Glob`, `Read`, `Shell`, `GitHub CLI`.
- **Before any `gh` command**, source the read-only environment script to enable security enforcement:
  ```bash
  source "<SKILL_DIR>/scripts/activate-gh-readonly.sh"
  ```
  Replace `<SKILL_DIR>` with the absolute path to this skill directory.
- After sourcing, use `gh` commands directly—they are intercepted by the read-only wrapper.
- Verify CLI auth first with `gh auth status`. If not authenticated, ask the user to run `gh auth login`.
- Enforce strict read-only mode at all times.
- Never attempt any write operation, including comments, reviews, edits, assignments, merges, closes, reopens, or API mutations.
- If a requested command is blocked by the wrapper, do not try alternatives that can mutate state.
- The read-only wrapper blocks `command gh` and other bypass attempts.

## Workflow

1. Enable read-only environment.
   - Source the environment script: `source "<SKILL_DIR>/scripts/activate-gh-readonly.sh"`
   - All subsequent `gh` commands in this shell session are now protected.
2. Prepare review context.
   - Confirm identity and auth: `gh auth status`, `gh api user`.
   - Resolve repository owner/name from the current repo or pass `-R <OWNER>/<REPO>`.
3. Resolve the target PR.
   - Use `gh pr view <PR_NUMBER> [--json <fields>]` when PR number is known.
   - Otherwise shortlist with `gh pr list [flags]` and pick the target PR.
4. Sync local repository to the latest PR branch code.
   - Fetch the latest remote state for the PR head branch before reviewing code.
   - Example flow:
     - Get head branch name from PR metadata (`headRefName`).
     - Run `git fetch --prune origin <HEAD_BRANCH>`.
     - Review files from `FETCH_HEAD` or check out a local review branch from it.
5. Gather full PR evidence before judging.
   - Metadata: `gh pr view <PR_NUMBER> [--json <fields>]`
   - Diff: `gh pr diff <PR_NUMBER> [--patch|--name-only]`
   - Changed files: `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/files --paginate`
   - Reviews: `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/reviews --paginate`
   - Checks: `gh pr checks <PR_NUMBER> [--json <fields>]`
   - Comments:
     - `gh pr view <PR_NUMBER> --comments`
     - `gh api repos/<OWNER>/<REPO>/issues/<PR_NUMBER>/comments --paginate`
     - `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments --paginate`
6. Inspect changed backend code deeply.
   - Read all high-risk touched files locally (`Read`, `Grep`) and correlate with diff hunks.
   - Prioritize request handlers/controllers, business services, authorization logic, database queries, migrations, background jobs, and queue/event handlers.
   - Verify idempotency, transaction safety, concurrency behavior, retry behavior, and backward compatibility for public API contracts.
   - Use `gh api repos/<OWNER>/<REPO>/contents/<PATH>?ref=<REF>` when exact remote content is needed (content is usually base64 in `.content`).
7. Apply review checklist with risk-first ordering.
   - Use `references/review-checklist.md`.
   - Cover security, correctness, data integrity, API compatibility, performance, and test sufficiency before style concerns.
8. Produce actionable review output.
   - Report only issues that are likely defects, regressions, or maintainability risks.
   - Include exact `file:line`, impact, and concrete fix guidance.
   - End with residual risk and missing validation/testing assumptions.
   - Return findings in chat only; do not write any comment or review back to GitHub.

## Response Format

Use this section order:

1. `Critical Issues (Must Fix)`
2. `Important Issues (Should Fix)`
3. `Suggestions (Consider)`
4. `Good Practices Noted`

For each issue, use:

```text
Issue: <brief description>
Location: <file:line>
Severity: <Critical|High|Medium|Low>
Problematic Code: <snippet or precise behavior>
Suggestion: <specific fix>
Example: <optional patch-style snippet>
```

## GitHub CLI API Equivalents

Use command mappings in `references/github-cli-map.md`.

## Review Tone

- Be constructive and specific.
- Explain impact and rationale.
- Assume positive intent.
- Prefer concise, high-confidence feedback.
