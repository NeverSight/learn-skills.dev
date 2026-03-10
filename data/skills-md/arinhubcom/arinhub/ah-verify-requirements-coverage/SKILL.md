---
name: ah-verify-requirements-coverage
description: Use this skill to verify requirements coverage when using the "ah" prefix. Use when asked to "ah verify requirements coverage", "ah verify requirements coverage issue 42", "ah verify requirements coverage PR 123", or "ah verify requirements coverage PR 123, issue 42". Verify that a PR or local changes fully implement requirements from a linked GitHub issue.
argument-hint: "PR number or URL (e.g., 123, #456, https://github.com/owner/repo/pull/789), or issue number for local changes (e.g., issue #42)"
---

# Verify Requirements Coverage

Verify that a pull request or local changes fully implement the requirements described in a GitHub issue. Extracts the issue reference, analyzes the diff against the issue description, and produces a coverage report.

## Input

- **PR number or URL** (optional): The pull request identifier. Accepts:
  - Number: `123`
  - Hash-prefixed: `#123`
  - Full URL: `https://github.com/owner/repo/pull/123`
  - If omitted, verifies local changes instead.
- **Issue number** (optional): An issue number can be provided to check coverage against (e.g., `issue #42`). Works in both remote and local modes. In remote mode, this overrides automatic issue detection from the PR body.
- **Diff file path** (optional): Path to a pre-existing diff file (e.g., passed by `ah-review-code`). If provided, skip fetching the diff in Step 7 and read this file instead.

## Procedure

### 1. Determine Review Target

- **Remote PR**: If the user provides a PR number or URL (e.g., "Verify PR #123"), target that remote PR. Set `MODE=remote`.
- **Local Changes**: If no specific PR is mentioned, or if the user asks to "verify my changes" or "do my changes cover the issue", target the current local changes (staged and unstaged). Set `MODE=local`.

### 2. Resolve Identifier

**If `MODE=remote`:**

Extract the PR number from the user input. Strip any `#` prefix or parse the number from a URL.

```
PR_NUMBER=<extracted number>
```

**If `MODE=local`:**

Determine the current branch name and base branch for identification and diffing.

```bash
BRANCH_NAME=$(git branch --show-current | tr '/' '-')

# Determine the base (source) branch using this priority:
# 1. If an open/draft PR exists for the current branch, use its base branch.
# 2. Fall back to the repository's default branch.
# 3. Last resort: "main".
BASE_BRANCH=$(gh pr view --json baseRefName -q '.baseRefName' 2>/dev/null || gh repo view --json defaultBranchRef -q '.defaultBranchRef.name' 2>/dev/null || git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
BASE_BRANCH=${BASE_BRANCH:-main}

# Find the point where the current branch diverged from the base branch.
MERGE_BASE=$(git merge-base "${BASE_BRANCH}" HEAD)
```

### 3. Fetch Metadata

**If `MODE=remote`:**

Gather PR details including body and linked issues. Resolve the repository owner and name for later use in API calls.

```bash
PR_META=$(gh pr view $PR_NUMBER --json number,title,body,baseRefName,headRefName,files,url)
PR_BODY=$(echo "$PR_META" | jq -r '.body')

# Resolve repository owner and name for API calls (e.g., GraphQL in Step 4).
REPO_OWNER=$(gh repo view --json owner -q '.owner.login')
REPO_NAME=$(gh repo view --json name -q '.name')
```

**If `MODE=local`:**

Gather the list of changed files on the branch (committed and unstaged tracked changes) relative to the base branch. Note: untracked files (new files not yet `git add`-ed) are not included.

```bash
git diff --name-only "${MERGE_BASE}"
```

### 4. Extract Linked Issue Number

**If `MODE=remote`:**

Determine the related issue using these methods in priority order:

**Method A -- User-provided issue number:** If the user explicitly provided an issue number (e.g., "verify PR 123, issue #42"), use that directly. Skip Methods B–D.

**Method B -- Closing keywords in PR body:**

Search `$PR_BODY` (from Step 3) for GitHub closing keywords followed by an issue reference:

- `closes #N`, `fixes #N`, `resolves #N` (and their variants: `close`, `closed`, `fix`, `fixed`, `resolve`, `resolved`)
- Full URL references: `closes https://github.com/owner/repo/issues/N`

**Method C -- GitHub linked issues API:**

```bash
gh api graphql \
  -F owner="$REPO_OWNER" \
  -F repo="$REPO_NAME" \
  -F pr_number=$PR_NUMBER \
  -f query='
    query($owner: String!, $repo: String!, $pr_number: Int!) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $pr_number) {
          closingIssuesReferences(first: 10) {
            nodes { number title }
          }
        }
      }
    }
  ' --jq '.data.repository.pullRequest.closingIssuesReferences.nodes'
```

**Method D -- Issue reference in PR body:**

If Methods A–C yield no results, scan `$PR_BODY` for any `#N` pattern or issue URL that is not a closing keyword reference. After extracting candidate numbers, verify each is an actual issue (not a PR) by checking for the absence of a `pull_request` key:

```bash
# Returns empty if $N is a PR, returns the issue number if it is an issue.
gh api "repos/${REPO_OWNER}/${REPO_NAME}/issues/$N" --jq 'select(.pull_request == null) | .number'
```

**If `MODE=local`:**

Determine the related issue using these methods in priority order:

**Method A -- User-provided issue number:** If the user explicitly provided an issue number (e.g., "verify my changes against issue #42"), use that directly.

**Method B -- Branch name convention:** Extract an issue number from the branch name if it follows a convention like `feature/42-description`, `fix/42`, `issue-42-description`, `42-description`, `jj/42-description`, etc.

```bash
# Extract the first standalone number (2+ digits) that appears after a slash or dash
# boundary (or at the start), followed by a dash, slash, or end of string.
# Matches: feature/42-desc, fix/42, issue-42-desc, 42-desc, jj/42-desc
# Skips: feature/v2-add-auth (single digit after letter), release/1.0 (version-like)
ISSUE_NUMBER=$(git branch --show-current | grep -oP '(?:^|[/-])\K\d{2,}(?=[-/]|$)' | head -1)
```

**No issue found:** If no linked issue can be determined, inform the user and stop. Do not guess or fabricate an issue number.

```
ISSUE_NUMBER=<extracted number>
```

If multiple issues are found, process each one and produce a separate coverage report per issue.

### 5. Fetch Issue Details

Retrieve the full issue description:

```bash
gh issue view $ISSUE_NUMBER --json number,title,body,labels
```

### 6. Extract Requirements from Issue

Parse the issue body and title to identify discrete, testable requirements. Look for:

- Checklist items (`- [ ]` or `- [x]`)
- Numbered steps or acceptance criteria
- Explicit behavioral descriptions ("should", "must", "when X then Y")
- UI changes, API changes, or data model changes mentioned
- Edge cases or error handling requirements
- Non-functional requirements (performance, security, accessibility)

Produce a numbered list of requirements:

```
R1: <requirement description>
R2: <requirement description>
...
```

If the issue body is vague or contains no clear requirements, use the issue title and any available context to infer the expected behavior. Flag inferred requirements clearly.

### 7. Fetch Diff

**If a diff file path was provided as input**, read the diff from that file instead of fetching it. Skip the commands below and proceed to Step 8.

**If `MODE=remote`:**

Get the full diff for the pull request:

```bash
gh pr diff $PR_NUMBER
```

Also review the list of changed files from Step 3 to understand the scope of changes.

**If `MODE=local`:**

Diff from the merge base (resolved in Step 2) to the current working tree. This captures all changes on the feature branch — both committed and unstaged tracked changes — relative to the base branch. Note: untracked files (new files not yet `git add`-ed) are not included.

```bash
git diff "${MERGE_BASE}"
```

Also review the list of changed files from Step 3 to understand the scope of changes.

### 8. Analyze Coverage

For each requirement from Step 6, determine whether the diff addresses it:

- **Covered**: The diff contains code changes that directly implement the requirement
- **Partially covered**: The diff addresses some aspects but misses edge cases or details
- **Not covered**: No code changes in the diff relate to this requirement

Use evidence from the diff to justify each assessment. Do not speculate -- base judgments on actual code changes.

Calculate the coverage percentage: `coverage = (fully covered count / total requirements) × 100`, rounded to the nearest integer. Partially covered requirements do **not** count toward the covered total -- they are treated the same as "Not covered" for the percentage calculation, but are still distinguished in the report table.

### 9. Produce Report

Set `TARGET` label based on mode:
- `MODE=remote`: `PR #<PR_NUMBER>`
- `MODE=local`: `branch ${BRANCH_NAME}`

Generate the report using the coverage analysis from Step 8.

**If all requirements are covered (100% coverage):**

```
## Requirements Coverage: 100%

All requirements from issue #<ISSUE_NUMBER> are implemented in <TARGET>.

### Requirements
| # | Requirement | Status |
|---|-------------|--------|
| R1 | <description> | Covered |
| R2 | <description> | Covered |

### Summary
<2-3 sentences confirming full coverage, highlighting key implementation decisions>
```

**If any requirements are missing or partially covered:**

```
## Requirements Coverage: <percentage>%

<TARGET> does not fully implement issue #<ISSUE_NUMBER>.

### Requirements
| # | Requirement | Status | Notes |
|---|-------------|--------|-------|
| R1 | <description> | Covered | |
| R2 | <description> | Not covered | <what is missing> |
| R3 | <description> | Partially covered | <what is incomplete> |

### Missing Implementation
<For each uncovered or partially covered requirement, describe specifically what code changes are needed to complete the implementation>

### Summary
<2-3 sentences describing the overall gap between the issue requirements and the current implementation>
```

### 10. Report to User

Present the coverage report from Step 9. Include:

- The issue number and title for context
- `MODE=remote`: the PR URL for reference; `MODE=local`: the branch name and list of changed files
- The coverage percentage
- Clear next steps if coverage is incomplete

## Important Notes

- Never fabricate requirements that are not present or implied in the issue
- If the issue lacks acceptance criteria, clearly state which requirements were inferred from context
- Do not evaluate code quality -- this skill only checks implementation completeness against the issue description
- For issues with sub-tasks or linked child issues, only evaluate the requirements in the specific linked issue
- When multiple issues are linked, report coverage for each issue separately
- In `MODE=local`, the diff comes from `git diff "${MERGE_BASE}"` (all committed and unstaged tracked changes on the branch relative to the base branch; untracked files are not included) instead of a PR diff. The issue must be provided by the user or extracted from the branch name — if neither yields a result, inform the user and stop
