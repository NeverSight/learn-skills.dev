---
name: git-worktree
description: Manage git worktrees for parallel development. Use when the user wants to work on multiple branches simultaneously, create isolated environments for features/fixes, or clean up completed worktrees.
disable-model-invocation: true
---

# Git Worktree Manager

## Overview

This skill provides a unified interface for managing git worktrees, enabling isolated parallel development. Worktrees allow you to have multiple branches checked out simultaneously in separate directories.

**Key features:**
- Automatic `.env` file copying from main repo to new worktrees
- Unified storage in `.worktrees/` directory
- Cleanup of merged and stale worktrees

## When to Use This Skill

- Creating isolated environments for feature development
- Working on multiple branches simultaneously
- Reviewing PRs without stashing current work
- Cleaning up completed feature branches

## Critical: Always Use the Manager Script

**Always use the worktree-manager.sh script** rather than raw `git worktree` commands. The script handles:
- Automatic `.env` file copying to new worktrees
- Consistent storage in `.worktrees/` directory
- Proper `.gitignore` management

## Core Commands

All operations use the unified `worktree-manager.sh` script:

```bash
bash scripts/worktree-manager.sh <command> [options]
```

### Create Worktree

```bash
worktree-manager.sh create <branch-name> [source-branch]
```

Creates a new worktree in `.worktrees/<branch-name>`. If the branch exists, it checks it out. If not, creates a new branch from the source (defaults to main/master).

### List Worktrees

```bash
worktree-manager.sh list
```

Shows all worktrees with their branch, commit, and status (clean/dirty/missing).

### Switch Worktree

```bash
worktree-manager.sh switch <branch-name|path>
```

Provides information for switching to a worktree by branch name or path.

### Cleanup Worktrees

```bash
worktree-manager.sh cleanup [--force]
```

Identifies and removes:
- Worktrees with merged branches
- Worktrees with deleted remote branches
- Missing worktree directories

Use `--force` to skip confirmation prompt.

### Copy Environment Files

```bash
worktree-manager.sh copy-env [worktree-path|branch-name]
```

Copies `.env*` files (excluding `.env.example`) from the main repo to a worktree. Useful for:
- Adding env files to existing worktrees created before this feature
- Refreshing env files after main repo changes

If run inside a worktree without arguments, copies to current location.

## Storage

Worktrees are stored in `.worktrees/` within the repository root. This directory is automatically added to `.gitignore`.

## Example Workflow

```bash
# Start new feature
worktree-manager.sh create feature-auth

# Work in the new worktree
cd .worktrees/feature-auth

# List all worktrees
worktree-manager.sh list

# When done, clean up
worktree-manager.sh cleanup
```

## Troubleshooting

### Missing .env files in existing worktrees

If you have existing worktrees created before the automatic env copying feature:

```bash
bash scripts/worktree-manager.sh copy-env feature-branch
```

Or from within the worktree directory:

```bash
bash scripts/worktree-manager.sh copy-env
```
