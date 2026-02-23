---
name: arinhub-code-reviewer
description: Review code for correctness, maintainability, and adherence to project standards. Supports local branch changes and remote Pull Requests (by ID or URL). Use when asked to "ah review code", "ah review code 123", or "ah review PR 123".
argument-hint: "PR number or URL (e.g., 100, #456, https://github.com/owner/repo/pull/789), or omit for local changes"
---

# Code Reviewer

Orchestrate a comprehensive code review by running multiple review strategies in parallel, merging and deduplicating findings into a review file. Supports both remote PRs and local branch changes.

## Input

- **PR number or URL** (optional): Accepts `123`, `#123`, or full URL. If omitted, reviews local changes.

## Procedure

### 1. Determine Review Target

- **Remote PR**: If the user provides a PR number or URL (e.g., "Review PR #123"), target that remote PR. Set `MODE=remote`.
- **Local Changes**: If no specific PR is mentioned, or if the user asks to "review my changes", target the current local file system changes (staged and unstaged). Set `MODE=local`.

### 2. Resolve Identifier and Repository

**If `MODE=remote`:**

Extract the PR number. Determine the repository name from git remote or the provided URL.

```sh
PR_NUMBER=<extracted number>
REPO_NAME=<repository name, e.g. "my-app">
REVIEW_FILE=~/.agents/arinhub/code-reviews/pr-code-review-${REPO_NAME}-${PR_NUMBER}.md

# Get the PR branch name and base branch from PR metadata (single API call).
PR_META=$(gh pr view ${PR_NUMBER} --json headRefName,baseRefName)
PR_BRANCH=$(echo "$PR_META" | jq -r '.headRefName')
PR_BASE=$(echo "$PR_META" | jq -r '.baseRefName')
```

**If `MODE=local`:**

Determine the repository name from git remote. Use the current branch name for identification, sanitizing slashes to dashes so file paths remain valid. Also determine the base branch and merge base for diffing.

```sh
REPO_NAME=<repository name>
BRANCH_NAME=$(git branch --show-current | tr '/' '-')
REVIEW_FILE=~/.agents/arinhub/code-reviews/local-code-review-${REPO_NAME}-${BRANCH_NAME}.md

# Determine the base (source) branch using this priority:
# 1. If an open/draft PR exists for the current branch, use its base branch
#    (handles custom targets like develop, release/*, etc.).
# 2. Fall back to the repository's default branch.
# 3. Last resort: "main".
BASE_BRANCH=$(gh pr view --json baseRefName -q '.baseRefName' 2>/dev/null || gh repo view --json defaultBranchRef -q '.defaultBranchRef.name' 2>/dev/null || git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
BASE_BRANCH=${BASE_BRANCH:-main}

# Find the point where the current branch diverged from the base branch.
MERGE_BASE=$(git merge-base "${BASE_BRANCH}" HEAD)
```

Create `~/.agents/arinhub/code-reviews/` and `~/.agents/arinhub/diffs/` directories if they do not exist.

### 3. Initialize Review File

**If `MODE=remote`:**

Create the review file with a header:

```markdown
# PR Review: ${REPO_NAME} #${PR_NUMBER}

**Date:** <current date>
**Repo:** ${REPO_NAME}
**Branch:** ${PR_BRANCH}
**Base Branch:** ${PR_BASE}
**PR Number:** ${PR_NUMBER}
**PR Link:** <PR URL>

## Issues

<!-- Issues from parallel review agents merged below. No duplicates. -->
```

**If `MODE=local`:**

Create the review file with a header:

```markdown
# Local Review: ${REPO_NAME} (${BRANCH_NAME})

**Date:** <current date>
**Repo:** ${REPO_NAME}
**Branch:** ${BRANCH_NAME}
**Base Branch:** ${BASE_BRANCH} (merge base: ${MERGE_BASE})

## Issues

<!-- Issues from parallel review agents merged below. No duplicates. -->
```

### 4. Prepare Diff and Working Tree

Save the diff to a shared file so subagents can read it. In remote mode, also check out the PR branch so tools that require a working tree (e.g., `react-doctor`) operate on the correct code.

**If `MODE=remote`:**

```bash
DIFF_FILE=~/.agents/arinhub/diffs/pr-diff-${REPO_NAME}-${PR_NUMBER}.diff

# Save the current branch so we can return to it after the review.
ORIGINAL_BRANCH=$(git branch --show-current)

# Stash any uncommitted local changes to prevent data loss during checkout.
git stash --include-untracked -m "arinhub-code-reviewer: auto-stash before PR checkout"

gh pr diff ${PR_NUMBER} > ${DIFF_FILE}

# Check out the PR branch to ensure the working tree reflects the PR code for subagents that require it (e.g., react-doctor).
gh pr checkout ${PR_NUMBER}
```

**If `MODE=local`:**

Diff from the merge base (resolved in Step 2) to the current working tree. This captures all changes on the feature branch — both committed and uncommitted — relative to the source branch.

```bash
DIFF_FILE=~/.agents/arinhub/diffs/local-diff-${REPO_NAME}-${BRANCH_NAME}.diff

# Diff from the merge base to the current working tree.
# BASE_BRANCH and MERGE_BASE were resolved in Step 2.
git diff "${MERGE_BASE}" > "${DIFF_FILE}"
```

No checkout is needed in local mode — the working tree already contains the changes.

### 5. Detect React Code

Spawn a subagent to analyze `${DIFF_FILE}` and determine whether the changes contain React code. The subagent must read the diff file and return `HAS_REACT=true` or `HAS_REACT=false`.

Set `HAS_REACT=true` if **any** of these conditions are found in the diff:

- **File extensions**: Changed files include `.tsx`, `.jsx`, or paths under common React directories (e.g., `components/`, `hooks/`, `pages/`)
- **React core imports**: `import ... from 'react'`, `import ... from "react"`, `require('react')`, `require("react")`
- **React DOM**: `import ... from 'react-dom'`, `import ... from 'react-dom/client'`
- **JSX syntax**: Diff hunks contain JSX elements (`<Component`, `<div`, `/>`, `React.createElement`)
- **React hooks**: Usage of `useState`, `useEffect`, `useRef`, `useMemo`, `useCallback`, `useContext`, `useReducer`, `useLayoutEffect`, or custom `use*` hooks
- **React ecosystem packages**: Imports from `react-router`, `react-hook-form`, `@tanstack/react-query`, `@tanstack/react-table`, `react-redux`, `zustand`, `jotai`, `recoil`, `next`, `@next/`, `styled-components`, `@emotion/`, or similar React-centric libraries

Otherwise set `HAS_REACT=false`.

### 6. Launch Parallel Review Subagents

Spawn subagents **in parallel** (do not wait for one to finish before starting the next). No subagent may submit a review — they only return findings.

Every subagent prompt must include the following shared context:

> The working tree is checked out on the branch that contains the changes under review. A diff file at `${DIFF_FILE}` contains all the changes to review. Do not switch branches, run `gh pr checkout`, or modify the working tree. Return a structured list of issues using the format defined in `references/issue-format.md`. Do not submit any review.

- If `HAS_REACT=true`: spawn **four** subagents (A, B, C, D).
- If `HAS_REACT=false`: spawn **three** subagents (A, B, C) — skip Subagent D.

#### Subagent A: code-reviewer

Invoke the `code-reviewer` skill.

#### Subagent B: octocode-roast

Invoke the `octocode-roast` skill with `code review` mode.

#### Subagent C: pr-review-toolkit

Invoke the `pr-review-toolkit:review-pr` command with `all parallel` mode.

#### Subagent D: react-doctor (only if `HAS_REACT=true`)

Invoke the `react-doctor` skill. Return the full `react-doctor` diagnostic report alongside the structured issues.

### 7. Merge and Deduplicate Issues

Collect issues from all subagents (three or four, depending on `HAS_REACT`) and deduplicate:

1. Parse each subagent's response into individual issues.
2. For each issue, create a fingerprint from: `file path` + `line number range` + `concern category`.
3. Two issues are duplicates if they share the same file, overlapping line ranges (within ±5 lines), and address the same concern (use semantic comparison, not exact string matching).
4. When duplicates are found, keep the most detailed/actionable version.
5. Tag each kept issue with its source(s): `[code-reviewer]`, `[octocode-roast]`, `[pr-review-toolkit]`, `[react-doctor]`, or combination if multiple agents found it.

### 8. Write Issues to Review File

Append deduplicated issues to the review file, grouped by severity. Use the format defined in [review-format.md](references/review-format.md).

### 9. React Health Report

**Skip this step if `HAS_REACT=false`.**

Follow the instructions in [react-health-report.md](references/react-health-report.md).

### 10. Verify Requirements Coverage

Spawn a subagent to verify requirements coverage using the `arinhub-verify-requirements-coverage` skill. Pass the diff file path (`${DIFF_FILE}`) so the subagent can read the diff directly without fetching it again. The subagent must return the full requirements coverage report in markdown format.

**If `MODE=remote`:** Pass PR `${PR_NUMBER}` and `${DIFF_FILE}` to the subagent. It will use the diff file for analysis and resolve the linked issue automatically.

**If `MODE=local`:** Pass `${DIFF_FILE}` to the subagent. The subagent will attempt to extract the linked issue number from the branch name (e.g., `feature/42-description`, `fix/42`, `issue-42-description`). If no issue can be determined, the subagent will skip coverage verification and report that no linked issue was found.

Append the returned coverage report to the end of the review file under a new section:

```markdown
## Requirements Coverage

<coverage report content from arinhub-verify-requirements-coverage>
```

### 11. Submit PR Review

**Skip this step if `MODE=local`.**

Follow the instructions in [submit-pr-review.md](references/submit-pr-review.md).

### 12. Restore Working Tree

**Skip this step if `MODE=local`.**

Follow the instructions in [restore-working-tree.md](references/restore-working-tree.md).

### 13. Report to User

**If `MODE=remote`:**

Present a summary:

- Path to the review file
- Total issues found (by severity)
- PR coverage percentage
- Whether the review was submitted successfully
- The PR URL for reference

**If `MODE=local`:**

Present the review file (`${REVIEW_FILE}`) content to the user and a summary:

- Path to the review file
- Total issues found (by severity)
- Requirements coverage percentage (if available)
- Branch name and list of changed files reviewed

## Important Notes

- Review subagents run in parallel to minimize total review time (three or four, depending on whether the changes contain React code).
- The `react-doctor` subagent is only launched when the diff contains `.tsx`/`.jsx` files or React imports. This avoids unnecessary React diagnostics on non-React changes.
- The review file is the single source of truth — all findings are merged there before submission.
- Deduplication uses semantic comparison: if two agents flag the same concern on the same code, only one entry is kept.
- The review file persists at `~/.agents/arinhub/code-reviews/` for future reference and audit.
- If a subagent fails or times out, proceed with results from the remaining agents and note the failure in the review file.
- The diff file persists at `~/.agents/arinhub/diffs/` and is shared read-only across all subagents. The PR branch checkout happens once in Step 4 before subagents launch — no subagent should run `gh pr checkout` or switch branches on its own.
- In `MODE=local`, step 11 (Submit PR Review) is skipped — the review is output only to the review file and presented to the user. Step 10 (Verify Requirements Coverage) runs if a linked issue can be determined from the branch name or user input.
