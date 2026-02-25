---
name: github-cli
description: GitHub CLI workflows for issues, labels, and PRs with proper linking, base branch handling, and structured descriptions
license: MIT
compatibility: opencode
metadata:
  scope: global
  tools: gh
---

# GitHub CLI Workflows

## Prerequisites

Ensure `gh` is authenticated:

```bash
gh auth status
```

## Issues

### Create Issue

```bash
gh issue create --title "Brief descriptive title" --body "$(cat <<'EOF'
## Summary
One-paragraph description of what needs to be done and why.

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
Additional context, links, or considerations.
EOF
)" --label "label1,label2"
```

**Issue Title Conventions:**

- Start with action verb: Add, Fix, Update, Remove, Refactor, Implement
- Be specific: "Add user authentication" not "Auth stuff"
- Keep under 72 characters

### Read Issues

```bash
# List open issues
gh issue list

# List with filters
gh issue list --label "bug" --assignee "@me"

# View specific issue
gh issue view 123

# View with comments
gh issue view 123 --comments
```

### Update Issue

```bash
# Add labels
gh issue edit 123 --add-label "priority:high,scope:mls"

# Remove labels
gh issue edit 123 --remove-label "needs-triage"

# Change title
gh issue edit 123 --title "New title"

# Add to milestone
gh issue edit 123 --milestone "v1.0"

# Assign
gh issue edit 123 --add-assignee "@me"
```

### Close Issue

```bash
# Close with reason
gh issue close 123 --reason completed

# Close as not planned
gh issue close 123 --reason "not planned"
```

## Labels

### Create Label

```bash
gh label create "scope:feature-name" --description "Features for X" --color "0052CC"
```

**Label Naming Conventions:**

- Use prefixes with colon: `scope:`, `priority:`, `type:`, `status:`
- Lowercase with hyphens: `scope:user-auth`
- Common prefixes:
  - `type:bug`, `type:feature`, `type:refactor`, `type:docs`
  - `priority:high`, `priority:medium`, `priority:low`
  - `scope:mls`, `scope:post-mls`
  - `status:blocked`, `status:in-review`

### List Labels

```bash
gh label list
```

### Update Label

```bash
gh label edit "old-name" --name "new-name" --description "Updated description" --color "FF0000"
```

### Delete Label

```bash
gh label delete "label-name" --yes
```

## Pull Requests

### Determine Base Branch

**CRITICAL: Always verify the correct base branch before creating a PR.**

```bash
# Check current branch
git branch --show-current

# See what branch you branched from
git log --oneline --graph -10

# List remote branches
git branch -r

# Common base branches: main, master, develop, release/*
```

### Create PR (Closing Issues)

**PRs MUST reference issues they implement using closing keywords.**

```bash
gh pr create \
  --base develop \
  --title "Add user authentication" \
  --body "$(cat <<'EOF'
## Summary
Brief description of what this PR does.

## Changes
- Change 1
- Change 2
- Change 3

## Closes
Closes #123
Closes #124

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] No regressions

## Screenshots
(if applicable)
EOF
)"
```

**Closing Keywords (any of these work):**

- `Closes #123`
- `Fixes #123`
- `Resolves #123`

**PR Title Conventions:**

- Match the issue title or summarize the change
- Use imperative mood: "Add feature" not "Added feature"
- Keep under 72 characters

### Create PR from Issue

When implementing an issue, reference it properly:

```bash
# Get issue details first
gh issue view 123

# Create branch named after issue
git checkout -b 123-add-user-auth

# After commits, create PR
gh pr create \
  --base main \
  --title "Add user authentication" \
  --body "$(cat <<'EOF'
## Summary
Implements user authentication with JWT tokens.

## Closes
Closes #123

## Changes
- Added auth middleware
- Added login/logout endpoints
- Added JWT token generation

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
EOF
)"
```

### Read PRs

```bash
# List open PRs
gh pr list

# View specific PR
gh pr view 456

# View PR diff
gh pr diff 456

# View PR checks
gh pr checks 456

# View PR comments
gh api repos/{owner}/{repo}/pulls/456/comments
```

### Update PR

```bash
# Change title
gh pr edit 456 --title "New title"

# Add reviewers
gh pr edit 456 --add-reviewer "username1,username2"

# Add labels
gh pr edit 456 --add-label "ready-for-review"

# Change base branch
gh pr edit 456 --base develop
```

### Merge PR

```bash
# Merge (creates merge commit)
gh pr merge 456 --merge

# Squash merge (single commit)
gh pr merge 456 --squash

# Rebase merge
gh pr merge 456 --rebase

# Delete branch after merge
gh pr merge 456 --squash --delete-branch
```

### Close PR Without Merging

```bash
gh pr close 456
```

## Complete Workflow Example

### Feature Development Flow

```bash
# 1. Create issue
gh issue create \
  --title "Add dark mode toggle" \
  --label "type:feature,scope:mls" \
  --body "$(cat <<'EOF'
## Summary
Add a dark mode toggle to user settings.

## Requirements
- [ ] Toggle switch in settings
- [ ] Persist preference
- [ ] Apply theme immediately

## Acceptance Criteria
- [ ] User can toggle dark mode
- [ ] Preference persists across sessions
EOF
)"
# Returns: Created issue #167

# 2. Create feature branch
git checkout -b 167-add-dark-mode

# 3. Make changes and commit
git add .
git commit -m "Add dark mode toggle component"

# 4. Push and create PR
git push -u origin 167-add-dark-mode

gh pr create \
  --base main \
  --title "Add dark mode toggle" \
  --body "$(cat <<'EOF'
## Summary
Adds dark mode toggle to user settings with persistent preferences.

## Closes
Closes #167

## Changes
- Added DarkModeToggle component
- Added theme context provider
- Added localStorage persistence

## Testing
- [x] Unit tests added
- [x] Manual testing completed
EOF
)"

# 5. After review, merge
gh pr merge --squash --delete-branch
```

## Tips

### Batch Operations

```bash
# Close multiple issues
for i in 101 102 103; do gh issue close $i; done

# Add label to multiple issues
for i in 101 102 103; do gh issue edit $i --add-label "wontfix"; done
```

### JSON Output for Scripting

```bash
# Get issue data as JSON
gh issue view 123 --json number,title,labels,state

# List PRs as JSON
gh pr list --json number,title,headRefName,baseRefName
```

### Check Repo Context

```bash
# Verify which repo you're working with
gh repo view --json nameWithOwner
```
