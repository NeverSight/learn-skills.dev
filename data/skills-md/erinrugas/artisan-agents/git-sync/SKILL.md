---
name: git-sync
description: >-
  Syncs local and remote branches safely. Use for fetch/pull/rebase/push workflows,
  conflict handling, and branch alignment before merge.
---

# Git Sync Skill

## When to Apply
- User asks to sync with remote.
- Branch is behind base branch.
- Pre-PR branch cleanup is needed.

## Workflow
1. Fetch latest refs.
2. Choose strategy:
   - Fast-forward pull when possible.
   - Rebase for linear history.
   - Merge when preserving branch topology is required.
3. Resolve conflicts and re-validate locally.
4. Push safely (`--force-with-lease` only after rebase when necessary).

## Safety
- Never force-push protected branches.
- Prefer explicit base branch in commands.
