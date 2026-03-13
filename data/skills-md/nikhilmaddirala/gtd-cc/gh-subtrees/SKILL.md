---
name: gh-subtrees
description: Subtree publishing and project graduation. Publish monorepo changes to standalone GitHub repos, graduate projects from lab to production.
---

# gh-subtrees

## Overview

The monorepo uses git-sync to auto-commit and sync `main` every 2 minutes across machines (see your git-sync or auto-commit configuration). This means the commit history on `main` is not meaningful -- it's full of auto-commits like "vault backup: 2024-06-06 09:03:02".

This skill syncs monorepo subtrees with standalone GitHub repos using clean, rewritten commit history. The sync process uses rsync to copy the monorepo subtree into a worktree checked out from the remote, then the AI writes clean commit messages based on the diff and monorepo history. It also handles pulling genuine remote additions back into the monorepo.

```
monorepo main (messy git-sync auto-commits)
├── 40-code/41-subtrees/gtd-cc/      ──sync──→  github.com/.../gtd-cc (clean history)
├── 40-code/41-subtrees/my-project/  ──sync──→  github.com/.../my-project (clean history)
└── ...
```


## Sub-skills

CRITICAL: You MUST load the appropriate sub-skill from the `sub-skills/` directory based on user intent.

- **subtrees-status.md**: Diagnose subtree remote configuration and sync status
  - Triggers: "subtree status", "subtree health", "check subtrees", "subtree setup"

- **sync.md**: Sync subtree between monorepo and standalone GitHub repo
  - Triggers: "sync", "publish", "push to remotes", "pull from remote"

- **graduate.md**: Move project from lab to production with GitHub repo
  - Triggers: "graduate", "move to production", "publish new project"


## Process

1. Determine user intent from their request
2. Load the appropriate sub-skill from `sub-skills/`
3. Execute the sub-skill process
4. Verify expected outcome was achieved


## Resources

- **scripts/subtrees-status.sh**: Subtree sync diagnostic (discovers subtrees, fetches remotes, compares content)
- **sub-skills/**: Workflow-specific instructions for each operation


## Conventions

- Every dir in `40-code/41-subtrees/` is a subtree (convention-over-configuration)
- Remote naming: `remote-<dirname>` (e.g., `remote-gtd-cc`)
- Remote URLs stored in `40-code/41-subtrees.yaml` (git remotes are local config and don't travel with the repo)
- Sync is always pull-then-push; monorepo is source of truth for content
- Always get user approval before destructive operations
