---
name: scm
description: >-
  Guide for effective source control management with Git following modern best practices.
  Covers branching strategies, commit hygiene, PR workflows, and team collaboration patterns.
  Triggers on "git", "source control", "version control", "branching", "merge", "rebase",
  "git workflow", "pull request", "commit message", "git history", "git conflict",
  "git stash", "git cherry-pick", "git bisect", "git blame", "git log", "git diff",
  "git reset", "git checkout", "git switch", "git restore", "git tag", "git remote",
  "git fetch", "git pull", "git push", "git branch", "conventional commits", "squash",
  "force push", "git hooks", "pre-commit", "commit-msg", "gitignore", "git submodule",
  "git worktree", "feature branch", "trunk based", "git flow", "github flow",
  "commit and push", "commit changes", "push changes", "push to remote",
  "commit this", "commit these", "make a commit", "create commit".
  PROACTIVE: MUST invoke when performing complex Git operations or setting up workflows.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ABOUTME: Source control management skill for Git best practices and workflows
# ABOUTME: Covers branching, commits, PRs, conflict resolution, and team collaboration

# Source Control Management (SCM) Skill

## Quick Reference

| Principle | Rule |
|-----------|------|
| Atomic Commits | One logical change per commit |
| Conventional Commits | `type(scope): description` format |
| Clean History | Rebase before merge for linear history |
| Branch Naming | `type/ticket-description` format |
| PR Size | < 400 lines of code changes |
| Never Force Push | To shared branches (main, develop) |

## 🔄 RESUMED SESSION CHECKPOINT

**When a session is resumed from context compaction, verify Git state:**

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION RESUMED - SCM SKILL VERIFICATION                   │
│                                                             │
│  Before continuing Git operations:                          │
│                                                             │
│  1. Was I in the middle of Git operations?                  │
│     → Check summary for "commit", "merge", "rebase"         │
│                                                             │
│  2. Current repository state:                               │
│     → Run: git status                                       │
│     → Run: git log --oneline -5                             │
│     → Run: git branch -vv                                   │
│                                                             │
│  3. Pending operations:                                     │
│     → Check for: .git/MERGE_HEAD (merge in progress)        │
│     → Check for: .git/rebase-merge (rebase in progress)     │
│     → Check for: .git/CHERRY_PICK_HEAD (cherry-pick)        │
│                                                             │
│  If operation was interrupted:                              │
│  → Complete or abort the pending operation                  │
│  → Verify working directory is clean                        │
│  → Ensure no uncommitted changes are lost                   │
└─────────────────────────────────────────────────────────────┘
```

## Branching Strategies

### Git Flow (Traditional)

```
main ─────●─────────────────●─────────────●──────
          │                 ↑             ↑
          │         merge   │     merge   │
          ↓                 │             │
develop ──●──●──●──●──●─────●──●──●──●────●──────
              │     ↑           │     ↑
              ↓     │           ↓     │
feature/xyz ──●──●──┘   feature/abc ──●──┘
```

**Use when:**
- Scheduled releases
- Multiple versions in production
- Formal QA process

**Branches:**
- `main`: Production code
- `develop`: Integration branch
- `feature/*`: New features
- `release/*`: Release preparation
- `hotfix/*`: Emergency fixes

### GitHub Flow (Simplified)

```
main ─────●───────●───────●───────●──────
          │       ↑       │       ↑
          ↓       │       ↓       │
feature ──●──●──●─┘ fix ──●──●────┘
```

**Use when:**
- Continuous deployment
- Small teams
- Rapid iteration

**Branches:**
- `main`: Always deployable
- `feature/*`, `fix/*`, `chore/*`: Short-lived branches

### Trunk-Based Development

```
main ─────●──●──●──●──●──●──●──●──●──────
          ↑     ↑     ↑     ↑     ↑
          │     │     │     │     │
          └─────┴─────┴─────┴─────┴── Small, frequent commits
```

**Use when:**
- Mature CI/CD pipeline
- Feature flags available
- High-trust team

## Branch Naming Convention

```
<type>/<ticket>-<brief-description>

Examples:
- feature/PROJ-123-user-authentication
- fix/PROJ-456-login-timeout
- chore/PROJ-789-update-dependencies
- docs/PROJ-012-api-documentation
- refactor/PROJ-345-extract-service
```

| Type | Purpose |
|------|---------|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `chore/` | Maintenance tasks |
| `docs/` | Documentation only |
| `refactor/` | Code restructuring |
| `test/` | Test additions |
| `hotfix/` | Emergency production fixes |

## Conventional Commits

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description | Triggers |
|------|-------------|----------|
| `feat` | New feature | Minor version bump |
| `fix` | Bug fix | Patch version bump |
| `docs` | Documentation only | No version bump |
| `style` | Formatting, no code change | No version bump |
| `refactor` | Code change, no feature/fix | No version bump |
| `test` | Adding/fixing tests | No version bump |
| `chore` | Build process, tooling | No version bump |
| `perf` | Performance improvement | Patch version bump |
| `ci` | CI configuration | No version bump |
| `build` | Build system changes | No version bump |
| `revert` | Revert previous commit | Varies |

### Examples

```bash
# Feature with scope
feat(auth): add OAuth2 login support

# Bug fix with body
fix(api): handle null response from payment gateway

The payment gateway occasionally returns null instead of
an error object. Added null check before processing.

Fixes #123

# Breaking change
feat(api)!: change user endpoint response format

BREAKING CHANGE: The /api/users endpoint now returns
a paginated response object instead of an array.

# Multiple footers
fix(security): upgrade vulnerable dependency

Reviewed-by: John Doe
Refs: CVE-2024-12345
```

## Commit Best Practices

### Atomic Commits

Each commit should:
- Represent ONE logical change
- Be independently revertable
- Pass all tests
- Have a clear, descriptive message

```bash
# BAD: Multiple unrelated changes
git add .
git commit -m "various fixes and updates"

# GOOD: Separate logical changes
git add src/auth/
git commit -m "feat(auth): implement password reset flow"

git add tests/auth/
git commit -m "test(auth): add password reset tests"

git add package.json package-lock.json
git commit -m "chore(deps): update authentication libraries"
```

### Interactive Staging

```bash
# Stage specific hunks
git add -p

# Stage specific files interactively
git add -i
```

### Commit Message Guidelines

**Subject line:**
- Max 50 characters
- Imperative mood ("add" not "added")
- No period at end
- Capitalize first word after type

**Body (optional):**
- Wrap at 72 characters
- Explain WHAT and WHY, not HOW
- Reference issues/tickets

```bash
# Use editor for complex commits
git commit

# Quick commit with message
git commit -m "fix(api): correct rate limit calculation"
```

## Merging vs Rebasing

### When to Merge

```bash
# Merge preserves history
git checkout main
git merge feature/user-auth --no-ff

# Creates merge commit:
# *   Merge branch 'feature/user-auth'
# |\
# | * feat: add login endpoint
# | * feat: add user model
# |/
# *   Previous commit on main
```

**Use merge when:**
- Preserving feature branch history is important
- Working with public/shared branches
- Team prefers merge commits

### When to Rebase

```bash
# Rebase creates linear history
git checkout feature/user-auth
git rebase main

# Results in linear history:
# * feat: add login endpoint
# * feat: add user model
# * Previous commit on main
```

**Use rebase when:**
- Cleaning up local commits before PR
- Updating feature branch with main
- Maintaining linear project history

### Interactive Rebase for Cleanup

```bash
# Squash, reorder, edit last 5 commits
git rebase -i HEAD~5

# In editor:
pick abc1234 feat: add user model
squash def5678 fix: typo in user model
pick ghi9012 feat: add login endpoint
reword jkl3456 feat: add logout endpoint
drop mno7890 WIP: debugging

# Commands:
# p, pick   = use commit
# r, reword = use commit but edit message
# e, edit   = use commit but stop for amending
# s, squash = meld into previous commit
# f, fixup  = like squash but discard message
# d, drop   = remove commit
```

## Pull Request Workflow

### Before Creating PR

```bash
# 1. Ensure branch is up to date
git fetch origin
git rebase origin/main

# 2. Run tests locally
npm test  # or equivalent

# 3. Check for linting issues
npm run lint  # or equivalent

# 4. Review your changes
git diff origin/main...HEAD
git log origin/main..HEAD --oneline
```

### PR Size Guidelines

| Size | Lines Changed | Review Time |
|------|---------------|-------------|
| XS | < 50 | Minutes |
| S | 50-200 | < 30 min |
| M | 200-400 | < 1 hour |
| L | 400-800 | Hours |
| XL | > 800 | Split required |

### PR Description Template

```markdown
## Summary
Brief description of changes (1-3 bullet points)

## Changes
- Added X feature
- Modified Y component
- Fixed Z bug

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if UI changes)
[Before/After screenshots]

## Related Issues
Closes #123
Refs #456
```

## Conflict Resolution

### Understanding Conflicts

```
<<<<<<< HEAD (current branch)
const timeout = 5000;
=======
const timeout = 10000;
>>>>>>> feature-branch (incoming changes)
```

### Resolution Strategies

```bash
# 1. Keep current branch version
git checkout --ours path/to/file

# 2. Keep incoming version
git checkout --theirs path/to/file

# 3. Manual resolution
# Edit file, then:
git add path/to/file
git rebase --continue  # or git merge --continue
```

### Prevention Strategies

- Pull/rebase frequently
- Keep branches short-lived
- Communicate about shared files
- Use code owners for critical paths

## Git Configuration

### Essential Configuration

```bash
# Identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Default branch
git config --global init.defaultBranch main

# Editor
git config --global core.editor "code --wait"

# Diff tool
git config --global diff.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff $LOCAL $REMOTE'

# Merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Auto-correct typos
git config --global help.autocorrect 10

# Prune deleted remote branches
git config --global fetch.prune true

# Default push behavior
git config --global push.default current
git config --global push.autoSetupRemote true
```

### Useful Aliases

```bash
# Add to ~/.gitconfig
[alias]
    # Status shortcuts
    st = status -sb

    # Log formats
    lg = log --oneline --graph --decorate -20
    lga = log --oneline --graph --decorate --all -20

    # Branch operations
    co = checkout
    cob = checkout -b
    br = branch -vv
    brd = branch -d

    # Commit shortcuts
    ci = commit
    ca = commit --amend
    can = commit --amend --no-edit

    # Diff shortcuts
    df = diff
    dfs = diff --staged

    # Undo operations
    unstage = reset HEAD --
    uncommit = reset --soft HEAD~1

    # Show recent branches
    recent = for-each-ref --sort=-committerdate refs/heads/ --format='%(refname:short) - %(committerdate:relative)'

    # Clean merged branches
    cleanup = "!git branch --merged | grep -v '\\*\\|main\\|master\\|develop' | xargs -n 1 git branch -d"
```

## Common Operations

### Undo Operations

```bash
# Undo last commit (keep changes staged)
git reset --soft HEAD~1

# Undo last commit (keep changes unstaged)
git reset HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Undo uncommitted changes to file
git checkout -- path/to/file

# Undo staged changes
git reset HEAD path/to/file

# Revert a pushed commit (creates new commit)
git revert <commit-sha>
```

### Stashing

```bash
# Stash current changes
git stash

# Stash with message
git stash save "WIP: feature description"

# Include untracked files
git stash -u

# List stashes
git stash list

# Apply most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Drop stash
git stash drop stash@{0}
```

### Cherry-Picking

```bash
# Apply single commit
git cherry-pick <commit-sha>

# Apply multiple commits
git cherry-pick <sha1> <sha2> <sha3>

# Apply range of commits
git cherry-pick <sha1>^..<sha2>

# Cherry-pick without committing
git cherry-pick -n <commit-sha>
```

### Bisect (Find Bug Introduction)

```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark known good commit
git bisect good <commit-sha>

# Git checks out middle commit; test and mark
git bisect good  # or bad

# When done
git bisect reset
```

## Safety Guidelines

### Never Do on Shared Branches

```bash
# NEVER force push to main/develop
git push --force origin main  # DANGEROUS

# NEVER rebase public branches
git rebase main  # on shared feature branch

# NEVER reset pushed commits
git reset --hard HEAD~3  # if already pushed
```

### Safe Alternatives

```bash
# Instead of force push, use:
git push --force-with-lease  # Fails if remote changed

# Instead of rebase on shared branch, use:
git merge origin/main

# Instead of reset pushed commits, use:
git revert <sha>
```

## Checklist

Before committing:
- [ ] Changes are atomic (one logical change)
- [ ] Commit message follows conventional format
- [ ] Tests pass locally
- [ ] No debug code or console.logs
- [ ] No secrets or credentials
- [ ] Branch is up to date with target

Before creating PR:
- [ ] Rebased on latest main/develop
- [ ] All commits have meaningful messages
- [ ] PR is appropriately sized (< 400 lines)
- [ ] Description explains what and why
- [ ] Related issues are linked
- [ ] CI checks pass

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `git add .` blindly | Commits unintended files | Use `git add -p` or specific files |
| "WIP" commits | Unclear history | Squash before merge |
| Force push to shared | Overwrites team work | Use `--force-with-lease` |
| Long-lived branches | Merge conflicts | Keep branches < 1 week |
| Large PRs | Slow reviews, bugs | Split into smaller PRs |
| Merge commits locally | Messy history | Rebase for updates |
| Ignoring CI failures | Broken main branch | Fix before merge |

## Additional Resources

- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
- [Oh Shit, Git!?!](https://ohshitgit.com/)
