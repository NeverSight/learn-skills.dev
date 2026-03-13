---
name: create-pr
description: Create a Pull Request from the current branch. Syncs upstream main/master, updates current branch, handles fork remotes intelligently, and generates PR title/description from diff and commits. Respects PR templates if present. REQUIRES Must be in a git repository with gh CLI available.
---

# Create PR Skill

Create a Pull Request from the current branch with intelligent remote detection and PR content generation.

## Prerequisites Check (MUST verify first)

Before proceeding, verify:

```bash
# 1. Check if in a git repository
git rev-parse --is-inside-work-tree

# 2. Check if gh CLI is available and authenticated
gh auth status

# 3. Check current branch is not main/master
CURRENT_BRANCH=$(git branch --show-current)
DEFAULT_BRANCH=$(git remote show origin | grep 'HEAD branch' | cut -d' ' -f5)
if [ "$CURRENT_BRANCH" = "$DEFAULT_BRANCH" ]; then
  echo "ERROR: Cannot create PR from default branch"
  exit 1
fi

# 4. Check for uncommitted changes (warn user if any)
git status --porcelain
```

If checks fail, STOP and inform the user:

- Not in git repo → "This skill requires a git repository. Please navigate to a git project."
- gh not authenticated → "Please run `gh auth login` first."
- On default branch → "You are on the default branch. Please checkout a feature branch first."
- Uncommitted changes → "You have uncommitted changes. Please commit or stash them first."

## Input

The user may optionally provide:
- Target base branch (defaults to main/master)
- Draft mode flag
- Specific reviewers

## Workflow

### Step 1: Detect Repository Configuration

```bash
# Get all remotes
git remote -v

# Get current branch name
CURRENT_BRANCH=$(git branch --show-current)

# Detect default branch (main or master)
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name')

# Get repository info
gh repo view --json owner,name,isFork,parent
```

### Step 2: Identify Upstream and Fork Remotes

Determine the remote configuration:

```bash
# List all remotes with their URLs
git remote -v

# Check if this repo is a fork
IS_FORK=$(gh repo view --json isFork -q '.isFork')

# If it's a fork, get parent info
if [ "$IS_FORK" = "true" ]; then
  PARENT_OWNER=$(gh repo view --json parent -q '.parent.owner.login')
  PARENT_NAME=$(gh repo view --json parent -q '.parent.name')
fi
```

**Remote Classification Logic**:

| Scenario | Upstream Remote | Push Remote |
|----------|-----------------|-------------|
| Single remote (origin) | origin | origin |
| Fork: origin=fork, upstream=parent | upstream | origin |
| Fork: origin=parent, fork remote exists | origin | fork remote |
| Multiple remotes, one is fork | non-fork remote | fork remote |

**Detection Algorithm**:

```bash
# Get current user's GitHub username
CURRENT_USER=$(gh api user -q '.login')

# For each remote, check if it belongs to current user
for remote in $(git remote); do
  REMOTE_URL=$(git remote get-url $remote)
  # Extract owner from URL (handles both HTTPS and SSH)
  REMOTE_OWNER=$(echo "$REMOTE_URL" | sed -E 's/.*[:/]([^/]+)\/[^/]+\.git$/\1/' | sed 's/\.git$//')

  if [ "$REMOTE_OWNER" = "$CURRENT_USER" ]; then
    FORK_REMOTE=$remote
  else
    UPSTREAM_REMOTE=$remote
  fi
done

# Default fallback
UPSTREAM_REMOTE=${UPSTREAM_REMOTE:-origin}
FORK_REMOTE=${FORK_REMOTE:-origin}
```

### Step 3: Sync Upstream Default Branch

```bash
# Fetch latest from upstream
git fetch $UPSTREAM_REMOTE $DEFAULT_BRANCH

# Update local default branch
git checkout $DEFAULT_BRANCH
git pull $UPSTREAM_REMOTE $DEFAULT_BRANCH

# Return to feature branch
git checkout $CURRENT_BRANCH
```

### Step 4: Update Current Branch with Upstream

```bash
# Rebase current branch onto latest default branch
git rebase $UPSTREAM_REMOTE/$DEFAULT_BRANCH

# If rebase fails, inform user
if [ $? -ne 0 ]; then
  echo "Rebase failed. Please resolve conflicts manually."
  git rebase --abort
  exit 1
fi
```

### Step 5: Push Branch to Remote

Check if branch exists on remote and push:

```bash
# Check if branch exists on the push remote
REMOTE_BRANCH_EXISTS=$(git ls-remote --heads $FORK_REMOTE $CURRENT_BRANCH | wc -l)

if [ "$REMOTE_BRANCH_EXISTS" -eq 0 ]; then
  # Branch doesn't exist, push with upstream tracking
  git push -u $FORK_REMOTE $CURRENT_BRANCH
else
  # Branch exists, force push (after rebase) with lease for safety
  git push --force-with-lease $FORK_REMOTE $CURRENT_BRANCH
fi
```

**Important**: Always use `--force-with-lease` instead of `--force` for safety.

### Step 6: Gather PR Content Information

```bash
# Get all commits between default branch and current branch
git log $UPSTREAM_REMOTE/$DEFAULT_BRANCH..HEAD --pretty=format:"%h %s%n%b" --no-merges

# Get the diff summary
git diff --stat $UPSTREAM_REMOTE/$DEFAULT_BRANCH..HEAD

# Get the full diff for analysis
git diff $UPSTREAM_REMOTE/$DEFAULT_BRANCH..HEAD

# Get list of changed files
git diff --name-only $UPSTREAM_REMOTE/$DEFAULT_BRANCH..HEAD
```

### Step 7: Check for PR Template

```bash
# Check for PR template in common locations
PR_TEMPLATE=""
for template_path in \
  ".github/pull_request_template.md" \
  ".github/PULL_REQUEST_TEMPLATE.md" \
  "docs/pull_request_template.md" \
  "PULL_REQUEST_TEMPLATE.md"; do
  if [ -f "$template_path" ]; then
    PR_TEMPLATE="$template_path"
    break
  fi
done

# Also check for template directory
if [ -z "$PR_TEMPLATE" ] && [ -d ".github/PULL_REQUEST_TEMPLATE" ]; then
  # Use default template if exists
  if [ -f ".github/PULL_REQUEST_TEMPLATE/default.md" ]; then
    PR_TEMPLATE=".github/PULL_REQUEST_TEMPLATE/default.md"
  fi
fi

# Read template content if found
if [ -n "$PR_TEMPLATE" ]; then
  cat "$PR_TEMPLATE"
fi
```

### Step 8: Generate PR Title and Description

**Title Generation Rules**:

1. If single commit: Use commit message subject line
2. If multiple commits: Summarize the overall change
3. Follow conventional commit format if project uses it: `<type>(<scope>): <description>`
4. Keep under 72 characters

**Description Generation**:

If PR template exists, fill in the template sections:

| Common Template Section | How to Fill |
|------------------------|-------------|
| `## Summary` / `## Description` | Summarize changes from commits and diff |
| `## Changes` / `## What` | List key changes from diff |
| `## Why` / `## Motivation` | Extract from commit bodies or infer from changes |
| `## Testing` | List test files changed or suggest manual testing |
| `## Screenshots` | Leave placeholder if UI changes detected |
| `## Checklist` | Leave checkboxes for user to complete |
| `Fixes #` / `Closes #` | Extract issue references from commits |

If no template, generate structured description:

```markdown
## Summary

[2-3 sentences summarizing what this PR does]

## Changes

- [Key change 1]
- [Key change 2]
- [Key change 3]

## Testing

[How the changes were tested or should be tested]

---
[Any issue references found in commits]
```

### Step 9: Create the Pull Request

```bash
# Determine the base repository for the PR
if [ "$IS_FORK" = "true" ]; then
  # For forks, create PR against parent repo
  BASE_REPO="$PARENT_OWNER/$PARENT_NAME"
  gh pr create \
    --repo "$BASE_REPO" \
    --base "$DEFAULT_BRANCH" \
    --head "$CURRENT_USER:$CURRENT_BRANCH" \
    --title "$PR_TITLE" \
    --body "$PR_BODY"
else
  # For non-forks, create PR in same repo
  gh pr create \
    --base "$DEFAULT_BRANCH" \
    --head "$CURRENT_BRANCH" \
    --title "$PR_TITLE" \
    --body "$PR_BODY"
fi
```

**Use HEREDOC for body to preserve formatting**:

```bash
gh pr create --title "$PR_TITLE" --body "$(cat <<'EOF'
## Summary

[Generated summary here]

## Changes

- Change 1
- Change 2

EOF
)"
```

### Step 10: Report Results

After PR creation, provide:

```bash
# Get PR URL and details
gh pr view --json url,number,title,state
```

## Output Format

---

### PR Created Successfully

**PR**: #[NUMBER] - [TITLE]
**URL**: [PR_URL]
**Base**: [BASE_BRANCH] ← **Head**: [HEAD_BRANCH]
**Remote**: Pushed to `[FORK_REMOTE]`

#### Summary

[Brief description of what the PR contains]

#### Files Changed

| File | Changes |
|------|---------|
| `path/to/file.ts` | +[additions] -[deletions] |

#### Next Steps

- [ ] Review the PR description and edit if needed
- [ ] Add reviewers if required
- [ ] Wait for CI checks to pass
- [ ] Address any review comments

---

## Error Handling

| Situation | Action |
|-----------|--------|
| No commits ahead of base | "No changes to create PR. Your branch is up to date with [base]." |
| Rebase conflicts | "Rebase failed due to conflicts. Please resolve manually and re-run." |
| Push rejected | "Push failed. Check if you have write access to the remote." |
| PR already exists | "A PR already exists for this branch: [URL]. Opening existing PR." |
| No remote access | "Cannot access remote. Check your authentication with `gh auth status`." |
| Fork detection failed | "Could not determine fork relationship. Please specify the target repo." |

## Advanced Options

### Draft PR

```bash
gh pr create --draft --title "$PR_TITLE" --body "$PR_BODY"
```

### Add Reviewers

```bash
gh pr create --reviewer "user1,user2" --title "$PR_TITLE" --body "$PR_BODY"
```

### Add Labels

```bash
gh pr create --label "enhancement,needs-review" --title "$PR_TITLE" --body "$PR_BODY"
```

### Link to Issue

If commits reference issues (e.g., "Fixes #123"), automatically add to PR body:

```bash
# Extract issue references from commits
ISSUES=$(git log $UPSTREAM_REMOTE/$DEFAULT_BRANCH..HEAD --pretty=format:"%B" | grep -oE "(Fixes|Closes|Resolves) #[0-9]+" | sort -u)
```

## Important Notes

1. **Safety First**: Always use `--force-with-lease` instead of `--force` when pushing after rebase
2. **Fork Awareness**: Automatically detect and handle fork workflows
3. **Template Respect**: Always check for and use PR templates when available
4. **Conventional Commits**: If project uses conventional commits, follow the format
5. **Issue Linking**: Preserve issue references from commit messages
6. **Review Before Submit**: Show generated title/description for user approval before creating PR
