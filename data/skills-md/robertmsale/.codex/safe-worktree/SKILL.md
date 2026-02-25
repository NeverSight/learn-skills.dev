---
name: safe-worktree
description: Safely remove issue worktrees and branches with policy-aware fallbacks. Use for post-merge cleanup or abandoned issue cleanup when branch/worktree deletion commands may be blocked. Aggressively protects main/master and other integration branches, and when local branch-deletion safeguards are missing, proactively offer to install lightweight protection hooks first.
---

# Safe Worktree Cleanup

## Overview
Use this skill to clean up issue worktrees and branches without risking `main`/`master` or the active integration branch.

This workflow is built for Codex command-policy environments where commands like `git branch -d` or `git push origin --delete` may be rejected.

Important:
- Git can retain stale worktree registrations after manual folder removal.
- The helper script handles this automatically by running `git worktree prune` as part of normal cleanup.

## Use When
- A PR is merged and you need local/remote branch + worktree cleanup.
- An issue branch/worktree is intentionally abandoned and must be removed.
- Standard cleanup commands are being blocked by policy.

## Branch Protection Baseline
Before cleanup, check whether the repo already enforces local branch-deletion safeguards (for example, protected branch hooks in `core.hooksPath`).

If safeguards are missing, offer to install lightweight local hooks before branch cleanup:
- `pre-push` to block remote deletion pushes for protected branches.
- `reference-transaction` to block local branch deletion for protected branches.

Reference templates and install notes:
- `references/branch-protection-hooks.md`

## Required Inputs
- `REPO_ROOT`: repository path.
- `INTEGRATION_BRANCH`: usually `master` or `main`.
- `ISSUE_NUMBER`: numeric issue id.
- `BRANCH`: expected `codex/issue-<issue-number>-<slug>`.
- `WORKTREE_PATH`: expected issue worktree path.

## Hard Safety Rules
- Never delete protected branches: `main`, `master`, `develop`, `staging`, `production`.
- Never delete the integration branch.
- Never delete the currently checked out branch.
- By default, only delete branches matching `^codex/issue-[0-9]+-`.
- Refuse dangerous worktree paths (`/`, `.`, `$HOME`, or empty).
- Run destructive actions as separate commands, not one long chained command.

## Helper CLI (Deterministic)
Use the bundled helper instead of emitting inline scripts:

```bash
/Users/robertsale/.codex/skills/safe-worktree/scripts/safe-worktree-cleanup \
  --repo-root "/path/to/repo" \
  --integration-branch "master" \
  --issue-number "123" \
  --branch "codex/issue-123-some-slug" \
  --worktree-path "../repo-wt-123" \
  --delete-remote true \
  --allow-unmerged-delete false
```

Run `--help` for usage:

```bash
/Users/robertsale/.codex/skills/safe-worktree/scripts/safe-worktree-cleanup --help
```

## Deterministic Protections Implemented By Script
- Refuses protected branches: `main`, `master`, `develop`, `staging`, `production`.
- Refuses deleting integration branch or currently checked out branch.
- Refuses non-issue branch names by default (`^codex/issue-[0-9]+-`).
- Optionally enforces `--issue-number` branch match.
- Refuses dangerous worktree paths (`/`, `.`, `$HOME`, empty, repo root).
- Uses recoverable deletion fallback (`trash`) when `git worktree remove` cannot fully remove the directory.
- Runs `git worktree prune` by default (before and after worktree-path cleanup) to clear stale registrations automatically.
- Requires merged state unless `--allow-unmerged-delete true`.
- Uses policy-aware fallback deletes for local and remote refs.
- Fails non-zero if branch/worktree still exists after attempted cleanup.
