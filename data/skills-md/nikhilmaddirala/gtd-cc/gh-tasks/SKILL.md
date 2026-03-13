---
name: gh-tasks
description: Issue-driven development with worktree isolation. Create issues, plan implementations, work in worktrees, review PRs, and merge with clean squash history.
---

# gh-tasks

## Overview

Issue-driven development pipeline for this monorepo with three modes of operation:

**Daily edits** - Small changes happen directly on `main`

**Focused work** - Features and fixes use issue-linked worktrees with draft PRs:
```
new → plan → work → review → merge
 │                              │
 └──────────────────────────────┘
        (via status dashboard)
```

**Automated pipeline** - End-to-end execution via orchestrate sub-skill

### Workflow paths

| Path | When to use | Sub-skills |
|------|-------------|------------|
| Quick | Simple bug fix | `new` → `work` → `merge` |
| Standard | Most features | `new` → `work` → `review` → `merge` |
| Full | Complex work | `new` → `plan` → `work` → `review` → `merge` |
| Automated | Well-defined tasks | `orchestrate` (handles all stages) |

### Key principles

- Airtight tracking: one issue = one worktree = one draft PR = one branch
- Status visibility: dashboard shows all active work at a glance


## Sub-skills

CRITICAL: You MUST load the appropriate sub-skill from the `sub-skills/` directory based on user intent.

### Pipeline (in order)

- **new.md**: Create a GitHub issue for focused work
  - Triggers: "new issue", "create issue", "new task"

- **plan.md**: Research codebase and create implementation plan
  - Triggers: "plan", "research", "design approach", "analyze options"

- **work.md**: Create worktree, implement changes, create draft PR
  - Triggers: "work on", "implement", "start coding", "create worktree"

- **review.md**: Review PR for correctness, post findings
  - Triggers: "review", "check PR", "analyze changes"

- **merge.md**: Merge PR, cleanup worktree/branch, close issue
  - Triggers: "merge", "finish", "done", "complete"

- **rebase.md**: Squash-rebase feature branch onto main
  - Triggers: "rebase", "make mergeable", "update branch", "sync with main"

### Utilities

- **setup.md**: Bootstrap repo labels and configuration
  - Triggers: "setup labels", "create labels", "bootstrap repo", "configure labels"

- **tasks-status.md**: Dashboard of worktrees, issues, PRs, and next actions
  - Triggers: "status", "dashboard", "show active work", "what am I working on"

- **orchestrate.md**: Automated end-to-end pipeline
  - Triggers: "orchestrate", "auto", "end-to-end", "fully automated"

- **worktree-sync.md**: Sync worktrees from remote branches across machines
  - Triggers: "sync worktrees", "sync all worktrees", "update worktrees", "fetch all branches"


## Process

1. Determine user intent from their request
2. Load the appropriate sub-skill from `sub-skills/`
3. Execute the sub-skill process
4. Verify expected outcome was achieved


## Resources

- **sub-skills/**: Workflow-specific instructions
- **scripts/**: Standalone CLI tools matching each sub-skill
- **templates/**: Output format templates for issues, plans, and reviews


## Guidelines

- Airtight tracking: one issue = one worktree = one draft PR = one branch
- Always get user approval before destructive operations


## Appendix

### Scripts

| Script | Sub-skill | Usage |
|--------|-----------|-------|
| `setup-labels.sh` | setup | `./setup-labels.sh [--dry-run\|--delete]` |
| `work.sh` | work | `./work.sh <issue-number>` |
| `merge.sh` | merge | `./merge.sh <pr-number>` |
| `rebase.sh` | rebase | `./rebase.sh [worktree-path]` |
| `tasks-status.sh` | tasks-status | `./tasks-status.sh` |
| `monorepo-worktree-sync` | worktree sync | `monorepo-worktree-sync` (auto-runs every 2 min) |

### Templates

| Template | Purpose |
|----------|---------|
| `issue.md` | Goal/Context/Acceptance criteria format for issues |
| `plan.md` | Implementation plan format (appended to issue body) |
| `review.md` | PR review comment format with blockers/nice-to-haves |
