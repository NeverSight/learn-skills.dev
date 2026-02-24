---
name: git
description: Git version control and GitHub CLI workflows for commits, branches, pull requests, and code reviews with professional commit message practices.
---
# Git and GitHub Workflow Skill

You are a Git and GitHub workflow specialist. This skill provides comprehensive guidance for version control, collaboration, and GitHub integration using git and the gh CLI.

## Core Principles

### Commit Messages

**IMPORTANT**: Use the git commit message writer agent for all commits.

**Commit message format**:
- Professional, human-written style
- **NO AI attribution**: Do not include "Generated with Claude Code" or "Co-Authored-By: Claude"
- Follow project conventions
- Clear, descriptive, focused on the "why" not just the "what"

### GitHub Access

Use `gh` CLI for all GitHub operations:
- Issues
- Pull requests
- Releases
- Repository management
- API access

## Git Fundamentals

### Repository Setup

```bash
# Initialize new repository
git init

# Clone existing repository
git clone <url>
git clone <url> <directory>

# Clone with specific branch
git clone -b <branch> <url>

# Clone with depth (shallow clone)
git clone --depth 1 <url>
```

### Basic Workflow

```bash
# Check status
git status

# View changes
git diff
git diff --staged
git diff <file>

# Stage changes
git add <file>
git add .
git add -p  # Interactive staging

# Commit changes
git commit -m "message"
# NOTE: Use commit message writer agent instead

# Push changes
git push
git push origin <branch>
git push -u origin <branch>  # Set upstream

# Pull changes
git pull
git pull --rebase  # Rebase instead of merge
```

### Branch Management

```bash
# List branches
git branch
git branch -a  # Include remote branches
git branch -r  # Remote branches only

# Create branch
git branch <name>
git checkout -b <name>  # Create and switch
git switch -c <name>    # Modern alternative

# Switch branches
git checkout <branch>
git switch <branch>     # Modern alternative

# Delete branch
git branch -d <branch>   # Safe delete
git branch -D <branch>   # Force delete

# Delete remote branch
git push origin --delete <branch>

# Rename branch
git branch -m <old-name> <new-name>
git branch -m <new-name>  # Rename current branch
```

### Viewing History

```bash
# View commit log
git log
git log --oneline
git log --graph --oneline --all
git log -p  # Show patches
git log --follow <file>  # Follow file history

# View specific commits
git show <commit>
git show <commit>:<file>

# Search commits
git log --grep="pattern"
git log --author="name"
git log --since="2 weeks ago"
```

### Undoing Changes

```bash
# Discard working directory changes
git checkout -- <file>
git restore <file>  # Modern alternative

# Unstage changes
git reset HEAD <file>
git restore --staged <file>  # Modern alternative

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Amend last commit
git commit --amend
# NOTE: Only use --amend when:
# 1. User explicitly requested amend OR
# 2. Adding edits from pre-commit hook

# Revert commit (creates new commit)
git revert <commit>
```

### Stashing

```bash
# Stash changes
git stash
git stash save "description"

# List stashes
git stash list

# Apply stash
git stash apply
git stash apply stash@{n}

# Apply and remove stash
git stash pop

# Drop stash
git stash drop stash@{n}

# Clear all stashes
git stash clear
```

### Remote Management

```bash
# List remotes
git remote -v

# Add remote
git remote add <name> <url>

# Change remote URL
git remote set-url <name> <url>

# Remove remote
git remote remove <name>

# Fetch from remote
git fetch
git fetch <remote>
git fetch --all

# Prune deleted remote branches
git remote prune origin
git fetch --prune
```

## Advanced Git Operations

### Rebasing

```bash
# Rebase current branch
git rebase <base-branch>
git rebase main

# Interactive rebase
git rebase -i HEAD~3  # Last 3 commits
git rebase -i <commit>

# Continue/abort rebase
git rebase --continue
git rebase --abort

# Rebase with autosquash
git commit --fixup <commit>
git rebase -i --autosquash <base>
```

**IMPORTANT**: Never use `git rebase -i` as it requires interactive input which is not supported.

### Merging

```bash
# Merge branch into current branch
git merge <branch>

# Merge without fast-forward
git merge --no-ff <branch>

# Merge with squash
git merge --squash <branch>

# Abort merge
git merge --abort
```

### Cherry-picking

```bash
# Cherry-pick commit
git cherry-pick <commit>

# Cherry-pick multiple commits
git cherry-pick <commit1> <commit2>

# Cherry-pick range
git cherry-pick <start>..<end>
```

### Tags

```bash
# List tags
git tag

# Create tag
git tag <name>
git tag -a <name> -m "message"  # Annotated tag

# Push tags
git push origin <tag>
git push origin --tags  # Push all tags

# Delete tag
git tag -d <name>
git push origin --delete <name>
```

## GitHub CLI (gh)

### Authentication

```bash
# Login to GitHub
gh auth login

# Check auth status
gh auth status

# Logout
gh auth logout
```

### Pull Requests

```bash
# Create PR
gh pr create
gh pr create --title "Title" --body "Description"
gh pr create --draft
gh pr create --base develop --head feature-branch

# Using heredoc for body (recommended)
gh pr create --title "Feature: Add new thing" --body "$(cat <<'EOF'
## Summary
- Added new feature
- Fixed related bug

## Test plan
- [ ] Run unit tests
- [ ] Test manually

EOF
)"

# List PRs
gh pr list
gh pr list --state open
gh pr list --state closed
gh pr list --author @me

# View PR
gh pr view
gh pr view 123
gh pr view --web  # Open in browser

# Check PR status
gh pr checks
gh pr checks 123

# Review PR
gh pr review
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please fix X"
gh pr review 123 --comment --body "Looks good!"

# Checkout PR
gh pr checkout 123

# Merge PR
gh pr merge
gh pr merge 123
gh pr merge 123 --squash
gh pr merge 123 --merge
gh pr merge 123 --rebase

# Close/reopen PR
gh pr close 123
gh pr reopen 123

# Comment on PR
gh pr comment 123 --body "Comment text"

# Edit PR
gh pr edit 123 --title "New title"
gh pr edit 123 --body "New description"
gh pr edit 123 --add-label bug
```

### Issues

```bash
# Create issue
gh issue create
gh issue create --title "Title" --body "Description"
gh issue create --label bug --label priority

# List issues
gh issue list
gh issue list --state open
gh issue list --assignee @me
gh issue list --label bug

# View issue
gh issue view 123
gh issue view 123 --web

# Edit issue
gh issue edit 123 --title "New title"
gh issue edit 123 --add-label bug
gh issue edit 123 --add-assignee @me

# Close/reopen issue
gh issue close 123
gh issue reopen 123

# Comment on issue
gh issue comment 123 --body "Comment text"
```

### Repository Management

```bash
# Create repository
gh repo create
gh repo create my-repo --public
gh repo create my-repo --private
gh repo create my-repo --clone

# Clone repository
gh repo clone owner/repo
gh repo clone owner/repo directory

# Fork repository
gh repo fork
gh repo fork owner/repo
gh repo fork --clone

# View repository
gh repo view
gh repo view owner/repo
gh repo view --web

# List repositories
gh repo list
gh repo list owner

# Archive repository
gh repo archive owner/repo
```

### Workflow Management

```bash
# List workflows
gh workflow list

# View workflow
gh workflow view
gh workflow view <workflow-id>

# Run workflow
gh workflow run <workflow>
gh workflow run <workflow> --ref branch-name

# List workflow runs
gh run list
gh run list --workflow=<workflow>

# View run details
gh run view
gh run view <run-id>

# Watch run
gh run watch <run-id>

# Re-run workflow
gh run rerun <run-id>
```

### GitHub API Access

```bash
# Make API request
gh api <endpoint>

# Get repository info
gh api repos/owner/repo

# Get PR comments
gh api repos/owner/repo/pulls/123/comments

# POST request
gh api repos/owner/repo/issues --field title="Title" --field body="Body"

# With jq for JSON processing
gh api repos/owner/repo | jq '.stargazers_count'
```

## Complete Workflows

### Workflow 1: Feature Development

```bash
# 1. Update main branch
git checkout main
git pull

# 2. Create feature branch
git checkout -b feature/new-thing

# 3. Make changes
# ... edit files ...

# 4. Stage and commit
git add .
# Use commit message writer agent for commit

# 5. Push to remote
git push -u origin feature/new-thing

# 6. Create PR
gh pr create --title "Add new feature" --body "Description"

# 7. Address review feedback
# ... make changes ...
git add .
# Use commit message writer agent
git push

# 8. Merge PR (when approved)
gh pr merge --squash
```

### Workflow 2: Fix Bug in Main

```bash
# 1. Create hotfix branch
git checkout main
git pull
git checkout -b hotfix/critical-bug

# 2. Fix the bug
# ... edit files ...

# 3. Commit and push
git add .
# Use commit message writer agent
git push -u origin hotfix/critical-bug

# 4. Create urgent PR
gh pr create --title "Fix: Critical bug" --body "Fixes #123"

# 5. Fast-track merge
gh pr merge --merge  # Keep commit history for hotfix
```

### Workflow 3: Update Branch with Main

```bash
# 1. Fetch latest changes
git fetch origin

# 2. Rebase on main (preferred)
git rebase origin/main

# Or merge main (alternative)
git merge origin/main

# 3. Resolve conflicts if any
# ... fix conflicts ...
git add .
git rebase --continue  # If rebasing
# Or: git commit if merging

# 4. Push (force push if rebased)
git push --force-with-lease
```

### Workflow 4: Review and Test PR

```bash
# 1. Checkout PR
gh pr checkout 123

# 2. Run tests
# ... test commands ...

# 3. Leave review
gh pr review --approve --body "LGTM! Tests pass."

# Or request changes
gh pr review --request-changes --body "Please fix X"

# 4. Return to your branch
git checkout feature/my-work
```

### Workflow 5: Clean Up After Merge

```bash
# 1. Switch to main
git checkout main

# 2. Pull latest
git pull

# 3. Delete local branch
git branch -d feature/old-feature

# 4. Delete remote branch (if not auto-deleted)
git push origin --delete feature/old-feature

# 5. Prune deleted remote branches
git fetch --prune
```

### Workflow 6: Release Management

```bash
# 1. Create release tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 2. Create GitHub release
gh release create v1.0.0 --title "v1.0.0" --notes "Release notes"

# With release assets
gh release create v1.0.0 --title "v1.0.0" dist/*.tar.gz

# 3. List releases
gh release list

# 4. View release
gh release view v1.0.0
```

## Best Practices

### Branch Naming

Use descriptive, categorized names:
- `feature/user-authentication`
- `fix/login-bug`
- `hotfix/critical-security-issue`
- `refactor/cleanup-api`
- `docs/update-readme`
- `test/add-integration-tests`

### Commit Guidelines

1. **Use commit message writer agent** for all commits
2. **Make atomic commits**: One logical change per commit
3. **Write clear messages**: Explain why, not just what
4. **Reference issues**: Include issue numbers when relevant
5. **Keep commits clean**: Avoid "WIP" or "fix typo" in main history

### Pull Request Practices

1. **Keep PRs focused**: One feature/fix per PR
2. **Write good descriptions**: Explain what, why, and how to test
3. **Update regularly**: Keep branch up to date with base
4. **Respond promptly**: Address review comments quickly
5. **Use draft PRs**: For work-in-progress feedback

### Git Configuration

```bash
# Set user info
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Set pull strategy
git config --global pull.rebase true

# Enable helpful colors
git config --global color.ui auto

# Set default editor
git config --global core.editor vim
```

## Common Patterns

### Pattern 1: Quick Fix on Current Branch

```bash
git add <fixed-files>
# Use commit message writer agent
git push
```

### Pattern 2: Sync Fork with Upstream

```bash
# Add upstream remote (once)
git remote add upstream <original-repo-url>

# Fetch and merge upstream changes
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### Pattern 3: Squash Commits Before Merge

```bash
# Interactive rebase to squash (locally)
git rebase -i HEAD~3

# Or use PR squash merge (preferred)
gh pr merge --squash
```

### Pattern 4: Find Who Changed a Line

```bash
# Blame file
git blame <file>
git blame -L 10,20 <file>  # Specific lines

# With gh
gh api repos/owner/repo/commits?path=<file> | jq '.[0]'
```

### Pattern 5: Bisect to Find Bug

```bash
# Start bisect
git bisect start
git bisect bad  # Current commit is bad
git bisect good <commit>  # Known good commit

# Test each commit git presents
# ... run tests ...
git bisect good  # or bad

# When found
git bisect reset
```

## Troubleshooting

### Issue: Merge Conflicts

```bash
# 1. See conflicted files
git status

# 2. Resolve conflicts in each file
# ... edit files ...

# 3. Mark as resolved
git add <resolved-files>

# 4. Continue operation
git rebase --continue  # If rebasing
git commit             # If merging
```

### Issue: Accidentally Committed to Wrong Branch

```bash
# 1. Create new branch from current state
git branch correct-branch

# 2. Reset current branch
git reset --hard HEAD~1

# 3. Switch to correct branch
git checkout correct-branch
```

### Issue: Pushed Sensitive Data

```bash
# 1. Remove from history
git filter-branch --tree-filter 'rm -f <file>' HEAD

# Or use BFG Repo-Cleaner (better)
# bfg --delete-files <file>

# 2. Force push (coordinate with team!)
git push --force

# 3. Rotate any exposed secrets immediately
```

### Issue: Need to Change Last Commit

```bash
# If not pushed yet
git commit --amend

# If already pushed (requires force push)
git commit --amend
git push --force-with-lease
```

**WARNING**: Only amend when:
1. User explicitly requested amend OR
2. Adding edits from pre-commit hook

Always check authorship before amending:
```bash
git log -1 --format='%an %ae'
```

### Issue: PR Has Conflicts

```bash
# Option 1: Rebase on base branch
git fetch origin
git rebase origin/main
git push --force-with-lease

# Option 2: Merge base branch
git fetch origin
git merge origin/main
git push

# Option 3: Use gh CLI
gh pr update-branch 123
```

## Git Safety Rules

1. **Never force push to main/master**: Warn user if requested
2. **Never skip hooks**: Don't use --no-verify unless explicitly requested
3. **Never run destructive commands**: Without user confirmation
4. **Always check before amending**: Verify authorship and push status
5. **Use --force-with-lease**: Instead of --force when needed

## Integration with Commit Message Writer

After validation and before committing:

```bash
# After all changes are ready
git add .
git status  # Review what will be committed
git diff --staged  # Review actual changes

# Then request commit using commit message writer agent
# Agent will:
# 1. Analyze changes
# 2. Draft professional commit message
# 3. Create commit with proper format
# 4. NO AI attribution (per CLAUDE.md)
```

## Quick Reference

```bash
# Status and info
git status
git log --oneline
git diff

# Branches
git checkout -b <branch>
git push -u origin <branch>
git branch -d <branch>

# Commits
git add .
# (use commit message writer)
git push

# Pull requests
gh pr create
gh pr list
gh pr checkout 123
gh pr merge --squash

# Issues
gh issue create
gh issue list
gh issue view 123

# Sync
git pull --rebase
git fetch --prune

# Cleanup
git branch -d <branch>
git push origin --delete <branch>
```

## Summary

**Primary directives:**
1. **Always use commit message writer agent** for commits
2. **Use gh CLI** for GitHub operations
3. **Follow branch naming conventions**
4. **Keep commits atomic and clear**
5. **Never include AI attribution** in commit messages
6. **Be careful with destructive operations**

**Most common commands:**
- `git status` - Check state
- `git checkout -b <branch>` - New branch
- `gh pr create` - Create PR
- `git pull --rebase` - Stay updated
- `gh pr merge --squash` - Merge PR
