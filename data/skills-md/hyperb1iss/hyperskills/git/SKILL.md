---
name: git
description: Use this skill for complex git operations including rebases, merge conflict resolution, cherry-picking, branch management, or repository archaeology. Activates on mentions of git rebase, merge conflict, cherry-pick, git history, branch cleanup, git bisect, worktree, force push, or complex git operations.
---

# Git Operations

Advanced git workflows and conflict resolution.

## Decision Trees

### Conflict Resolution Strategy

| Situation                                        | Strategy                                                           |
| ------------------------------------------------ | ------------------------------------------------------------------ |
| Lock file conflict (pnpm-lock, Cargo.lock, etc.) | **Never merge manually.** Checkout theirs, regenerate.             |
| SOPS encrypted file                              | Checkout theirs, run `sops updatekeys`, re-add.                    |
| Simple content conflict                          | Resolve manually, prefer smallest diff.                            |
| Large structural conflict                        | Consider `--ours`/`--theirs` + manual reapply of the smaller side. |

### Rebase vs Merge

| Situation                                  | Use                                         |
| ------------------------------------------ | ------------------------------------------- |
| Feature branch behind main                 | `git rebase origin/main`                    |
| Shared branch (others have it checked out) | **Never rebase.** Merge only.               |
| Cleaning up messy commits before PR        | `git rebase -i` with squash/fixup           |
| Already pushed and others pulled           | **Never rebase.** Use `git revert` instead. |

### Undo Operations

| What happened                                 | Fix                                       |
| --------------------------------------------- | ----------------------------------------- |
| Wrong commit message (not pushed)             | `git commit --amend`                      |
| Last commit was wrong (keep changes staged)   | `git reset --soft HEAD~1`                 |
| Last commit was wrong (keep changes unstaged) | `git reset HEAD~1`                        |
| Already pushed bad commit                     | `git revert <hash>` (creates new commit)  |
| Need to recover something lost                | `git reflog` then `git checkout HEAD@{N}` |

## Lock File Conflicts

**Always regenerate, never manually merge:**

```bash
# pnpm
git checkout --theirs pnpm-lock.yaml && pnpm install && git add pnpm-lock.yaml

# npm
git checkout --theirs package-lock.json && npm install && git add package-lock.json

# Cargo
git checkout --theirs Cargo.lock && cargo generate-lockfile && git add Cargo.lock

# SOPS encrypted files
git checkout --theirs secrets.yaml && sops updatekeys secrets.yaml && git add secrets.yaml
```

## Archaeology

```bash
# Find when a string was added/removed
git log -S "search string" --oneline

# Blame specific lines
git blame -L 10,20 <file>

# Find commits touching a function
git log -L :functionName:file.js

# Binary search for a bug introduction
git bisect start && git bisect bad HEAD && git bisect good v1.0.0
```

## Safety Rules

1. **Never rebase shared branches**
2. **`--force-with-lease`** not `--force` (prevents overwriting others' work)
3. **Regenerate lock files** -- never merge them
4. **Backup branch before destructive ops:** `git branch backup-$(date +%Y%m%d-%H%M%S)`
5. **Never commit large binaries** -- use Git LFS
