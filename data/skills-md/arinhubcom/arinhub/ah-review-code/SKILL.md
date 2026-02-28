---
name: ah-review-code
description: Use this skill to review code when using the "ah" prefix. Use when asked to "ah review code" or "ah review code 123". Review code for correctness, maintainability, and adherence to project standards. Supports local branch changes and remote Pull Requests (by ID or URL).
argument-hint: "PR number or URL (e.g., 100, #456, https://github.com/owner/repo/pull/789), or omit for local changes"
---

# Code Reviewer

Orchestrate a comprehensive code review by running multiple review strategies in parallel, merging and deduplicating findings into a review file. Supports both remote PRs and local branch changes.

## Input

- **PR number or URL** (optional): Accepts `123`, `#123`, or full URL. If omitted, reviews local changes.

## Procedure

### 1. Determine Review Target

- **Remote PR**: If the user provides a PR number or URL (e.g., "Review PR #123"), target that remote PR. Set `MODE=pr`.
- **Local Changes**: If no specific PR is mentioned, or if the user asks to "review my changes", target the current local file system changes (staged and unstaged). Set `MODE=local`.

### 2. Resolve Identifier and Repository

```sh
REVIEWS_DIR=~/.agents/arinhub/code-reviews
```

**If `MODE=pr`:**

```sh
MODE=pr
PR_NUMBER=<extracted from user input>
REPO_NAME=$(basename -s .git "$(git remote get-url origin)")
REVIEW_ID=${MODE}-${REPO_NAME}-${PR_NUMBER}
REVIEW_FILE=${REVIEWS_DIR}/code-review-${REVIEW_ID}.md

# Get the PR branch name, base branch, URL, and title from PR metadata (single API call).
PR_META=$(gh pr view ${PR_NUMBER} --json headRefName,baseRefName,url,title)
PR_BRANCH=$(echo "$PR_META" | jq -r '.headRefName')
PR_BASE=$(echo "$PR_META" | jq -r '.baseRefName')
PR_URL=$(echo "$PR_META" | jq -r '.url')
PR_TITLE=$(echo "$PR_META" | jq -r '.title')
```

**If `MODE=local`:**

```sh
MODE=local
REPO_NAME=$(basename -s .git "$(git remote get-url origin)")
BRANCH_NAME=$(git branch --show-current | tr '/' '-')
REVIEW_ID=${MODE}-${REPO_NAME}-branch-${BRANCH_NAME}
REVIEW_FILE=${REVIEWS_DIR}/code-review-${REVIEW_ID}.md

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

**Collision avoidance:** Check whether a review file or any subagent files for this `REVIEW_ID` already exist. If so, append a sequential number suffix to produce a unique `REVIEW_ID`.

```bash
BASE_REVIEW_ID=${REVIEW_ID}

if compgen -G "${REVIEWS_DIR}/code-review-${BASE_REVIEW_ID}.md" > /dev/null 2>&1 || \
   compgen -G "${REVIEWS_DIR}/subagent-*-${BASE_REVIEW_ID}.md" > /dev/null 2>&1; then
  N=1
  while compgen -G "${REVIEWS_DIR}/code-review-${BASE_REVIEW_ID}-${N}.md" > /dev/null 2>&1 || \
        compgen -G "${REVIEWS_DIR}/subagent-*-${BASE_REVIEW_ID}-${N}.md" > /dev/null 2>&1; do
    N=$((N + 1))
  done
  REVIEW_ID=${BASE_REVIEW_ID}-${N}
  REVIEW_FILE=${REVIEWS_DIR}/code-review-${REVIEW_ID}.md
fi
```

### 3. Initialize Review File

**If `MODE=pr`:**

Create the review file with a header:

```markdown
# PR Review: ${REPO_NAME} #${PR_NUMBER}

**Date:** <current date>
**Repo:** ${REPO_NAME}
**Branch:** ${PR_BRANCH}
**Base Branch:** ${PR_BASE}
**PR Number:** ${PR_NUMBER}
**PR Title:** ${PR_TITLE}
**PR Link:** ${PR_URL}

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

**If `MODE=pr`:**

```bash
DIFF_FILE=~/.agents/arinhub/diffs/diff-${REVIEW_ID}.diff

# Save the current branch so we can return to it after the review.
ORIGINAL_BRANCH=$(git branch --show-current)

# Stash any uncommitted local changes to prevent data loss during checkout.
STASH_MSG="ah-review-code: auto-stash ${REVIEW_ID}"
git stash --include-untracked -m "${STASH_MSG}"

gh pr diff ${PR_NUMBER} > ${DIFF_FILE}

# Check out the PR branch to ensure the working tree reflects the PR code
# for subagents that require it (e.g., react-doctor).
# If checkout fails, restore stashed changes and abort the review.
if ! gh pr checkout ${PR_NUMBER}; then
  STASH_INDEX=$(git stash list | grep -m1 "${STASH_MSG}" | sed 's/stash@{\([0-9]*\)}.*/\1/')
  [ -n "$STASH_INDEX" ] && git stash pop stash@{$STASH_INDEX}
  echo "ERROR: Failed to check out PR #${PR_NUMBER}. Review aborted."
  exit 1
fi
```

**If `MODE=local`:**

Diff from the merge base (resolved in Step 2) to the current working tree. This captures all changes on the feature branch — both committed and uncommitted — relative to the source branch. Note: untracked files (new files not yet `git add`-ed) are not included in the diff. To include new files in the review, stage them first with `git add -N <file>` (intent-to-add) before running the review.

```bash
DIFF_FILE=~/.agents/arinhub/diffs/diff-${REVIEW_ID}.diff

# Diff from the merge base to the current working tree.
# BASE_BRANCH and MERGE_BASE were resolved in Step 2.
git diff "${MERGE_BASE}" > "${DIFF_FILE}"
```

No checkout is needed in local mode — the working tree already contains the changes.

### 5. Detect React Code

Spawn a lightweight subagent (use fast model) to analyze `${DIFF_FILE}` and determine whether the changes contain React code. The subagent must read the diff file and return `HAS_REACT=true` or `HAS_REACT=false`.

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

Each subagent writes to its own dedicated file:

```
SUBAGENT_FILE=~/.agents/arinhub/code-reviews/subagent-<agent-name>-${REVIEW_ID}.md
```

Where `<agent-name>` is one of: `code-reviewer`, `octocode-roast`, `pr-review-toolkit`, `react-doctor`.

Before launching the subagents, read the issue format specification from [issue-format.md](references/issue-format.md) and embed its full content directly into each subagent prompt. This ensures subagents have the format regardless of the current working directory.

Every subagent prompt must include the following shared context:

> The working tree is checked out on the branch that contains the changes under review. A diff file at `${DIFF_FILE}` contains all the changes to review. Do not switch branches, run `gh pr checkout`, or modify the working tree. Do not submit any review.
>
> **Output:** Write your findings to `${SUBAGENT_FILE}` (your dedicated output file). Use the issue format specification embedded in your prompt above.

**Delegation rule (applies to ALL subagents A–D):** Each subagent's sole job is to invoke its assigned skill and return whatever the skill produces. Do NOT perform the analysis yourself. Do NOT write review logic, diagnostic logic, or generate findings manually. Each skill contains its own methodology — delegate to it completely.

- If `HAS_REACT=true`: spawn **four** subagents (A, B, C, D).
- If `HAS_REACT=false`: spawn **three** subagents (A, B, C) — skip Subagent D.

#### Subagent A: code-reviewer

- **File:** `~/.agents/arinhub/code-reviews/subagent-code-reviewer-${REVIEW_ID}.md`
- **Invoke:** `/code-reviewer`

#### Subagent B: octocode-roast

- **File:** `~/.agents/arinhub/code-reviews/subagent-octocode-roast-${REVIEW_ID}.md`
- **Invoke:** `/octocode-roast`
- **Extra Arguments:** add `code review`

#### Subagent C: pr-review-toolkit

- **File:** `~/.agents/arinhub/code-reviews/subagent-pr-review-toolkit-${REVIEW_ID}.md`
- **Invoke:** `/pr-review-toolkit:review-pr`
- **Extra Arguments:** add `all parallel`

#### Subagent D: react-doctor (only if `HAS_REACT=true`)

- **File:** `~/.agents/arinhub/code-reviews/subagent-react-doctor-${REVIEW_ID}.md`
- **Invoke:** `/react-doctor`
- **Extra Output:** add full diagnostic report in the subagent's response for merging into the final review file

### 7. Merge and Deduplicate Issues

Read all subagent output files (`~/.agents/arinhub/code-reviews/subagent-*-${REVIEW_ID}.md`) and deduplicate:

1. Parse each agent section (identified by `### <agent-name>` headings) into individual issues.
2. For each issue, create a fingerprint from: `file path` + `line number range` + `concern type` (e.g., security, correctness, performance, maintainability, style — inferred from the issue description).
3. Two issues are duplicates if they share the same file, overlapping line ranges (within ±5 lines), and address the same concern type (use semantic comparison of descriptions, not exact string matching).
4. When duplicates are found, keep the most detailed/actionable version.
5. Tag each kept issue with its source(s): `[code-reviewer]`, `[octocode-roast]`, `[pr-review-toolkit]`, `[react-doctor]`, or combination if multiple agents found it.
6. Transform each issue's `**File:**` field from the plain path in issue-format into the linked format used in review-format: combine the file path with the `**Line(s):**` value to produce a markdown link — e.g., `**File:** [`path/to/file.ts:42`](/absolute/path/to/file.ts#L42)` for single lines or `**File:** [`path/to/file.ts:42-50`](/absolute/path/to/file.ts#L42-L50)` for ranges.

### 8. Write Issues to Review File

Append deduplicated issues to the review file, grouped by severity. Use the format defined in [review-format.md](references/review-format.md).

### 9. React Health Report

**Skip this step if `HAS_REACT=false`.**

Follow the instructions in [react-health-report.md](references/react-health-report.md).

### 10. Verify Requirements Coverage

Spawn a subagent to execute the `/ah-verify-requirements-coverage` skill. The subagent's sole job is to invoke the skill and return its output.

- **Invoke:** `/ah-verify-requirements-coverage`
- **CRITICAL:** Do NOT perform requirements verification yourself. Do NOT write verification logic or analyze coverage manually. The skill contains its own methodology — delegate to it completely and return whatever it produces (full requirements coverage report in markdown format).

**If `MODE=pr`:** Pass PR `${PR_NUMBER}` and `${DIFF_FILE}` as arguments to the skill. If a linked issue number was identified during the review (e.g., from PR body or metadata), pass it as well to avoid redundant API lookups. The skill will resolve the linked issue on its own if no issue number is provided.

**If `MODE=local`:** Pass `${DIFF_FILE}` as an argument to the skill. The skill will attempt to extract the linked issue number from the branch name (e.g., `feature/42-description`, `fix/42`, `issue-42-description`). If no issue can be determined, the skill will skip coverage verification and report that no linked issue was found.

Append the returned coverage report to the end of the review file under a new section:

```markdown
## Requirements Coverage

<coverage report content from ah-verify-requirements-coverage>
```

### 11. Submit PR Review

**Skip this step if `MODE=local`.**

**Wait for Step 10** — do not proceed until the Verify Requirements Coverage subagent has completed and its report has been appended to the review file.

Follow the instructions in [submit-pr-review.md](references/submit-pr-review.md).
The subagent returns an **Issues Table** — append it to the end of `${REVIEW_FILE}`.

### 12. Restore Working Tree

**Skip this step if `MODE=local`.**

Follow the instructions in [restore-working-tree.md](references/restore-working-tree.md).

### 13. Report to User

**If `MODE=pr`:**

Present a summary:

- Path to the review file
- Total issues found (by severity)
- Requirements coverage percentage with one-line summary (if available)
- Whether the review was submitted successfully
- The PR URL for reference
- Present the **Issues Table** (returned by the `ah-submit-code-review` subagent in Step 11)

**If `MODE=local`:**

Present the review file (`${REVIEW_FILE}`) content to the user and a summary:

- Path to the review file
- Total issues found (by severity)
- Requirements coverage percentage with one-line summary (if available)
- Branch name and list of changed files reviewed

## Important Notes

- Review subagents run in parallel to minimize total review time (three or four, depending on whether the changes contain React code).
- The `react-doctor` subagent is only launched when the diff contains `.tsx`/`.jsx` files or React imports. This avoids unnecessary React diagnostics on non-React changes.
- The review file is the single source of truth — all findings are merged there before submission.
- Deduplication uses semantic comparison: if two agents flag the same concern on the same code, only one entry is kept.
- The review file persists at `~/.agents/arinhub/code-reviews/` for future reference and audit.
- If a subagent fails or times out, proceed with results from the remaining agents and note the failure in the review file.
- The diff file persists at `~/.agents/arinhub/diffs/` and is shared read-only across all subagents. The PR branch checkout happens once in Step 4 before subagents launch — no subagent should run `gh pr checkout` or switch branches on its own.
- In `MODE=local`, step 12 (Submit PR Review) is skipped — the review is output only to the review file and presented to the user. Step 11 (Verify Requirements Coverage) runs if a linked issue can be determined from the branch name or user input.
