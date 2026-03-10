---
name: source-control
description: "Git conventions for commit messages and workflow. Use for git commit, conventional commits, branch strategy, rebasing, merge conflicts, git workflow. Not for general code changes that happen to need a commit afterward."
allowed-tools: [mcp__acp__Bash]
---

# ABOUTME: Git conventional commit format and version control best practices
# ABOUTME: Commit message standards, branch strategies, workflow patterns

# Source Control

## Quick Reference

```bash
git commit -m "feat: add user authentication"
git checkout -b feat/user-auth
git fetch origin && git rebase origin/main
git stash && git stash pop
```

---

## Conventional Commits

**Format:** `<type>(<scope>): <subject>` (scope/body/footer optional)

| Type | Use |
|------|-----|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting |
| `refactor` | Code restructure |
| `perf` | Performance |
| `test` | Tests |
| `chore` | Maintenance |
| `ci` | CI/CD |
| `build` | Build system |
| `revert` | Revert commit |

**Rules:** Imperative mood, present tense, lowercase, no period, max 50 chars

```bash
# Good
git commit -m "feat(auth): add JWT validation"
git commit -m "fix: resolve race condition"

# Bad
git commit -m "Fixed stuff"      # Not conventional
git commit -m "Feat: Add thing"  # Capital letter
```

---

## Commit Process

1. **Check state:**
   ```bash
   git status && git diff HEAD && git branch --show-current && git log --oneline -5
   ```

2. **Verify NOT on main/master** (abort if so, unless authorized)

3. **Stage specific files** (never `git add -A`):
   ```bash
   git add <specific-files>
   ```

4. **Commit with conventional format:**
   ```bash
   git commit -m "<type>(<scope>): <subject>"
   ```

---

## Branch Naming

| Type | Pattern |
|------|---------|
| Feature | `feat/user-auth`, `feature/dashboard` |
| Fix | `fix/login-bug`, `bugfix/api-error` |
| Hotfix | `hotfix/security-patch` |
| Chore | `chore/update-deps` |

---

## Workflow

```bash
# Start feature
git checkout main && git pull origin main
git checkout -b feat/user-auth

# Keep up to date
git fetch origin && git rebase origin/main

# After PR merged
git checkout main && git pull
git branch -d feat/user-auth
```

| Use | When |
|-----|------|
| **Rebase** | Keep feature branch current, clean linear history |
| **Merge** | Integrate to main (via PR), preserve history |

---

## Recovery

| Situation | Command |
|---|---|
| Undo last commit (keep changes) | `git reset --soft HEAD~1` |
| Undo staged files | `git reset HEAD <file>` |
| Discard file changes | `git checkout -- <file>` |
| Recover deleted branch | `git reflog` then `git checkout -b <branch> <sha>` |
| Amend last commit | `git commit --amend -m "new message"` |
| Revert pushed commit | `git revert <sha>` |

---

## Conflicts

Resolve: `git status` to see conflicts, edit files to remove markers, `git add <resolved>`, then `git rebase --continue` (or `git merge --continue`). Use `git rebase --abort` to bail out.

---

## Hooks

**Pre-commit:** `.git/hooks/pre-commit` -- run linters, formatters, tests per language.

**Commit-msg:** Validate conventional format (commitlint, husky, lefthook).

---

## Best Practices

| DO | DON'T |
|----|-------|
| Conventional commits | Generic messages ("fix", "update") |
| Small, logical commits | Huge unrelated changes |
| Run tests before commit | Push broken code |
| Use branches | Commit to main directly |
| `--force-with-lease` | `--force` on shared branches |

---

## Resources

- https://www.conventionalcommits.org/
- https://git-scm.com/doc
- Tools: commitlint, husky, lefthook
