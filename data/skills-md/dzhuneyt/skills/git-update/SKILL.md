---
name: git-update
description: Safely update branch by fetching, checking for conflicts, stashing, rebasing, and restoring changes
allowed-tools: [Bash]
disable-model-invocation: true
---

Execute the following steps:
1. Check if current directory is a valid git repository
2. Fetch latest changes from remote
3. Check if working directory is clean (no local changes)
4. If clean: analyze safety and pull with rebase directly (skip stash operations)
5. If dirty: stash changes with `git stash push --include-untracked --keep-index` (preserves staging state)
6. Analyze if rebasing looks safe (check for potential conflicts by comparing commit histories)
7. If safe: pull with rebase, then restore stash if needed with `git stash pop`
8. If unsafe: abort and restore stash if needed with `git stash pop` to return to exact original state
9. Always provide exactly one sentence summary of the operation result

Safety checks:
- Use `git rev-parse --is-inside-work-tree` to verify git repository
- Look for divergent commit histories that could cause conflicts
- Check if remote has force-pushed (dangerous for rebase)
- Verify we're on a branch that can be safely rebased
- Use `git status --porcelain` to check for local changes efficiently
- Only stash/unstash if working directory is dirty

Stash safety rules:
- Use `git stash push --include-untracked --keep-index` to preserve staging state
- Always use `git stash pop` to restore, never `git stash apply`
- If stash pop fails due to conflicts, use `git reset --hard` and `git stash apply` then resolve
- Guarantee that abort scenarios restore files to their exact original state (staged files remain staged, unstaged files remain unstaged)
- Never proceed if stashing fails or if restoration would cause data loss

Rules:
- Preserve exact file states (staged/unstaged) through stash operations
- Only proceed with rebase if conflict probability is low
- Always restore original state on abort
- Output exactly one sentence summary at the end
- Zero tolerance for data loss
