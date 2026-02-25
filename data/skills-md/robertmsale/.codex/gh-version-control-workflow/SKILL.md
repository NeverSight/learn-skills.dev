---
name: gh-version-control-workflow
description: Run a disciplined GitHub workflow with git + gh using issues, issue-derived branches, worktrees, and PRs. Use when you need concurrent feature work, clear review boundaries, and issue-linked PRs instead of direct commits to integration branches.
---

# GH Version Control Workflow

## Overview
Use this workflow to move from direct commits on shared branches to issue-driven development:
- each unit of work starts from a GitHub issue
- each issue maps to a branch
- each branch gets its own worktree for concurrency
- each completed branch is proposed via a PR that links and closes its issue

## Preconditions
Run these checks first:

```bash
gh auth status
git remote -v
git fetch origin --prune
```

If auth is valid in `gh` but git over HTTPS fails, run:

```bash
gh auth setup-git
```

## Process

### 0) Ensure release tracker exists (`Version Bump: X.Y.Z`)
Before or during feature work for a planned release, find the open tracker issue for that target version.
Create it if missing, and reuse it if it already exists (avoid duplicate trackers).

```bash
TARGET_VERSION="<x.y.z>"
TRACKER_MATCHES="$(gh issue list \
  --state open \
  --json number,title \
  --limit 200 \
  --jq ".[] | select(.title == \"Version Bump: ${TARGET_VERSION}\") | .number")"
TRACKER_COUNT="$(printf '%s\n' "$TRACKER_MATCHES" | sed '/^$/d' | wc -l | tr -d ' ')"
if [[ "$TRACKER_COUNT" -gt 1 ]]; then
  echo "Multiple open trackers found for Version Bump: ${TARGET_VERSION}. Resolve duplicates first." >&2
  exit 1
fi
TRACKER_ISSUE="$(printf '%s\n' "$TRACKER_MATCHES" | head -n1)"
```

If empty, create:

```bash
cat > /tmp/version-bump-issue.md <<'EOF'
## Scope
Release tracker for v<x.y.z>.

## Candidate Issues
- (add issue references as `#<number>`)

## QA Checklist
- (add manual test instructions per issue)
EOF

TRACKER_URL="$(gh issue create \
  --title "Version Bump: ${TARGET_VERSION}" \
  --body-file /tmp/version-bump-issue.md \
  --label backlog \
  --assignee "@me")" || {
  echo "Failed to create tracker issue Version Bump: ${TARGET_VERSION}" >&2
  exit 1
}
TRACKER_ISSUE="$(printf '%s\n' "$TRACKER_URL" | awk -F/ 'END{print $NF}')"
if [[ -z "$TRACKER_ISSUE" ]]; then
  echo "Failed to parse tracker issue number from: $TRACKER_URL" >&2
  exit 1
fi
```

### 1) Create and triage issue
Create a scoped issue with acceptance criteria, assign owner, and apply labels.

```bash
gh issue create \
  --title "<short outcome>" \
  --body-file /tmp/issue-body.md \
  --label "<type>" \
  --assignee "@me"
```

Use labels to keep queue state explicit (`backlog`, `ready`, `in-progress`, `blocked`).
Use `--body-file` for multiline Markdown to avoid shell-escaping mistakes and literal `\n` text.

### 1b) Link issue into the version tracker
If the issue is intended for the current target release, reference it in the tracker issue.

```bash
cat > /tmp/version-bump-link.md <<'EOF'
Tracking issue #<issue-number> for v<x.y.z>.

Manual testing (draft, refine before QA handoff):
- <step 1>
- <step 2>
EOF

gh issue comment "$TRACKER_ISSUE" --body-file /tmp/version-bump-link.md
```

### 1c) Optional: split large work into sub-issues
For large efforts, create one parent issue and multiple child issues. Use sub-issues to parallelize work across agents.

`gh issue` does not currently expose parent/sub-issue flags directly, so use `gh api graphql`.

Get node IDs:

```bash
PARENT_ID="$(gh issue view <parent-issue-number> --json id --jq '.id')"
CHILD_ID="$(gh issue view <child-issue-number> --json id --jq '.id')"
```

Link child to parent:

```bash
gh api graphql \
  -f query='mutation($issueId:ID!,$subIssueId:ID!){addSubIssue(input:{issueId:$issueId,subIssueId:$subIssueId}){issue{number}}}' \
  -f issueId="$PARENT_ID" \
  -f subIssueId="$CHILD_ID"
```

List current sub-issues for a parent:

```bash
gh issue view <parent-issue-number> \
  --json number,title,subIssues \
  --jq '.subIssues[].number'
```

Reorder a sub-issue (move child before another sibling):

```bash
gh api graphql \
  -f query='mutation($issueId:ID!,$subIssueId:ID!,$beforeId:ID!){reprioritizeSubIssue(input:{issueId:$issueId,subIssueId:$subIssueId,beforeId:$beforeId}){issue{number}}}' \
  -f issueId="$PARENT_ID" \
  -f subIssueId="$CHILD_ID" \
  -f beforeId="<sibling-child-node-id>"
```

Unlink child from parent:

```bash
gh api graphql \
  -f query='mutation($issueId:ID!,$subIssueId:ID!){removeSubIssue(input:{issueId:$issueId,subIssueId:$subIssueId}){issue{number}}}' \
  -f issueId="$PARENT_ID" \
  -f subIssueId="$CHILD_ID"
```

Execution model:
- Create one branch/worktree/PR per child issue, not per parent issue.
- Keep the parent issue open until all child issues are closed and merged.

### 2) Derive branch from issue
Create a branch linked to the issue and based on the integration branch.

```bash
gh issue develop <issue-number> \
  --base <integration-branch> \
  --name "codex/issue-<issue-number>-<slug>"
```

Guidance:
- use `master` if your repo only has `origin/master`
- use `staging` only if `origin/staging` exists and is your integration branch

### 3) Create dedicated worktree
Keep each issue in its own directory so multiple branches can progress concurrently.

```bash
git worktree add ../<repo>-wt-<issue-number> codex/issue-<issue-number>-<slug>
```

Do implementation work in the worktree path, not in the primary checkout.

### 4) Bootstrap PR branch and publish
In the issue worktree:

```bash
git status
git commit --allow-empty -m "chore: bootstrap PR"
git push -u origin codex/issue-<issue-number>-<slug>
```

This creates a minimal remote branch state so PR-first/review tooling can run immediately without first-review special cases.

### 5) Open PR and link issue
Create a PR targeting the integration branch and include an auto-close reference.

```bash
gh pr create \
  --base <integration-branch> \
  --head codex/issue-<issue-number>-<slug> \
  --title "<type>: <summary>" \
  --body-file /tmp/pr-body.md
```

The `Closes #<issue-number>` line links the PR and auto-closes the issue on merge.
Prefer body files for `gh issue create`, `gh issue edit`, `gh pr create`, and `gh pr edit`.

### 5c) Implement and push normal commits
After the bootstrap PR exists, continue implementation with regular commits:

```bash
git status
git add -A
git commit -m "<type>: <summary>"
git push
```

Prefer multiple small commits for reviewability.

### 5a) Escaping-safe body files
Use heredocs to build Markdown bodies with real newlines:

```bash
cat > /tmp/issue-body.md <<'EOF'
## Why
<context>

## Acceptance Criteria
- <criterion 1>
- <criterion 2>
EOF
```

```bash
cat > /tmp/pr-body.md <<'EOF'
## Summary
- <change 1>
- <change 2>

Closes #<issue-number>
EOF
```

### 5b) Read review feedback (conversation + review summaries + inline code comments)
Before merging (or when doing post-merge follow-up), collect all PR feedback types:

```bash
# Top-level PR conversation + review summaries
gh pr view <pr-number> --json comments,reviews
gh pr view <pr-number> --comments
```

```bash
# Inline code review comments with file/line context
gh api repos/<owner>/<repo>/pulls/<pr-number>/comments --paginate
```

Notes:
- `gh pr view --comments` may not include every inline code remark.
- Inline review comments from the REST endpoint include `path`, `line`, and the full comment body.
- For quick triage, extract key fields only:

```bash
gh api repos/<owner>/<repo>/pulls/<pr-number>/comments --paginate \
  --jq '.[] | {path, line, body, html_url}'
```

### 6) Validate and merge
Use CLI checks and merge through PR:

```bash
gh pr checks --watch
gh pr merge --squash --delete-branch
```

After merge, update your integration branch locally:

```bash
git switch <integration-branch>
git pull --ff-only origin <integration-branch>
```

### 6a) Label auto-closed issues for QA
After merge, add the `qa` label to every issue auto-closed by the PR.

```bash
for issue in $(gh pr view <pr-number> --json closingIssuesReferences --jq '.closingIssuesReferences[].number'); do
  gh issue edit "$issue" --add-label qa
done
```

Optional verification:

```bash
gh issue view <issue-number> --json state,labels --jq '{state, labels:[.labels[].name]}'
```

### 6b) Add QA handoff comment to the version tracker
For each issue labeled `qa`, add a tracker comment with concrete manual testing steps.
This keeps release QA work centralized in the version bump issue.

```bash
cat > /tmp/version-bump-qa.md <<'EOF'
Issue #<issue-number> is merged and awaiting manual QA for v<x.y.z>.
PR: <https://github.com/<owner>/<repo>/pull/<pr-number>>

Manual testing:
- <step 1>
- <step 2>
- Expected result: <clear expected behavior>
EOF

gh issue comment "$TRACKER_ISSUE" --body-file /tmp/version-bump-qa.md
```

### 7) Mandatory local cleanup after merge
Always clean up branch/worktree after a PR is merged, whether merge happened via CLI or the GitHub web UI.

Verify PR merged:

```bash
gh pr view <pr-number> --json state,mergedAt,url
```

Then run cleanup using [$safe-worktree](/Users/robertsale/.codex/skills/safe-worktree/SKILL.md).
This avoids policy-blocked deletion commands and aggressively protects `main`/`master`.

Set inputs for `safe-worktree`:

```bash
REPO_ROOT="/path/to/repo"
INTEGRATION_BRANCH="<integration-branch>"
ISSUE_NUMBER="<issue-number>"
BRANCH="codex/issue-<issue-number>-<slug>"
WORKTREE_PATH="../<repo>-wt-<issue-number>"
DELETE_REMOTE="true"

/Users/robertsale/.codex/skills/safe-worktree/scripts/safe-worktree-cleanup \
  --repo-root "$REPO_ROOT" \
  --integration-branch "$INTEGRATION_BRANCH" \
  --issue-number "$ISSUE_NUMBER" \
  --branch "$BRANCH" \
  --worktree-path "$WORKTREE_PATH" \
  --delete-remote "$DELETE_REMOTE" \
  --allow-unmerged-delete false
```

## Guardrails
- Never commit directly to shared integration branches for feature work.
- Never open a PR without linking the issue in the body (`Closes #...`).
- Keep one issue per branch and one branch per worktree.
- Do not delete a worktree until its PR is merged or intentionally abandoned.
- Do not leave merged issue branches/worktrees on disk; cleanup is required.
- Use `safe-worktree` for cleanup; do not run branch/worktree deletion commands freehand.
- If an issue is in-scope for a release, it must be referenced in `Version Bump: X.Y.Z`.
- When adding `qa` to a closed issue, always add manual testing instructions to the version tracker.
- Do *not* work inside the base repo, always inside a worktree. Base repo must always have an integration branch checked out. Do not check out a worktree/issue branch.

## Command Reference
See `references/commands.md` for command templates and daily ops shortcuts.
