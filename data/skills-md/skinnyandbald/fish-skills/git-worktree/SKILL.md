---
name: git-worktree
description: "Manages Git worktrees for isolated parallel development. Creates worktrees in .github/worktrees/ with symlinked .env files."
---

# Git Worktree Manager

Manage isolated Git worktrees for parallel development, following project conventions.

## Quick Reference

| Command | Description |
|---------|-------------|
| `create <name> [base]` | Create worktree with symlinked .env |
| `list` | List all worktrees |
| `cleanup` | Remove inactive worktrees |
| `switch <name>` | Switch to a worktree |

## CRITICAL: Always Use the Manager Script

**NEVER call `git worktree add` directly.** Always use the script.

```bash
# CORRECT
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh create feature-name

# WRONG - Never do this directly
git worktree add .github/worktrees/feature-name -b feature-name develop
```

The script handles:
1. Symlinks `.env` file (not copy) from project root
2. Ensures `.github/worktrees/` is in `.gitignore`
3. Creates consistent directory structure at `.github/worktrees/`

## CRITICAL: Create the Worktree, Then STOP

**After creating a worktree, STOP.** Do NOT implement anything in the current session. Do NOT `cd` into the worktree and keep working.

Your job in this session is ONLY:
1. Create the worktree
2. Show the user the copy-paste command from the script output
3. **STOP and tell the user to run that command in a new terminal**

All planning, brainstorming, and implementation happens in the **new** Claude Code instance inside the worktree — NOT here.

**Why:** Claude Code's working directory and statusline are set at **launch time**. If you work here after creating a worktree, auto-compact will lose the worktree context and revert to the main repo mid-work.

## Project Conventions

- **Default base branch:** `develop` (not `main`)
- **Symlinks** for `.env` files, not copies — single source of truth
- **Worktree directory:** `.github/worktrees/`

## Commands

### `create <branch-name> [from-branch]`

Creates worktree in `.github/worktrees/<branch-name>`. Defaults to branching from `develop`.

```bash
# Create from develop (default)
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh create feature/pipeline-steps

# Create from specific branch
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh create hotfix/auth main
```

**What happens:**
1. Checks if worktree exists
2. Creates `.github/worktrees/` directory if needed
3. Updates base branch from remote
4. Creates worktree and branch
5. **Symlinks `.env` from project root**
6. Verifies symlink
7. **Outputs a copy-paste command** to launch Claude Code in the worktree

### `list` or `ls`

```bash
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh list
```

Shows:
- Worktree name and branch
- Current worktree marked with `*`
- Main repo status

### `switch <name>` or `go <name>`

```bash
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh switch feature/pipeline-steps
```

### `cleanup` or `clean`

Removes inactive worktrees interactively.

```bash
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

**Safety:** Won't remove current worktree.

## Workflow Examples

### Feature Development

```bash
# 1. Create worktree from develop
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh create feature/auth-system

# Script output:
#   ━━━ Launch Claude Code in this worktree ━━━
#   cd /path/to/.github/worktrees/feature-auth-system && claude
#   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 2. CLAUDE STOPS HERE. Tells user to copy-paste the command above into a new terminal.
#    DO NOT continue with any work in this session.

# 3. User pastes command → new Claude Code instance starts in the worktree
#    User brainstorms, plans, and implements in that fresh session

# 4. When done, cleanup from main repo
cd "$(git rev-parse --show-toplevel)"
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

### PR Review in Isolation

```bash
# Create worktree from PR branch
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh create pr-42-auth-fix origin/pr-branch

# CLAUDE STOPS HERE. Tells user to copy-paste the launch command into a new terminal.

# Cleanup after review
cd "$(git rev-parse --show-toplevel)"
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

## Directory Structure

```text
project-root/
├── .env                              # Source of truth
├── .github/
│   └── worktrees/                    # All worktrees live here
│       ├── feature-auth/
│       │   ├── .env -> ../../..      # Relative symlink to root .env
│       │   ├── src/
│       │   └── ...
│       └── feature-pipeline/
│           ├── .env -> ../../..      # Relative symlink to root .env
│           └── ...
└── .gitignore                        # Includes .github/worktrees
```

## Troubleshooting

### "Worktree already exists"

Switch to it instead:

```bash
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh switch <name>
```

### "Cannot remove worktree: it is current"

Return to main repo first:

```bash
cd "$(git rev-parse --show-toplevel)"
bash ~/.claude/skills/git-worktree/scripts/worktree-manager.sh cleanup
```

### Symlink broken?

Recreate manually from the worktree directory:

```bash
cd .github/worktrees/<name>
rm .env
# Compute relative path to project root .env
GIT_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
ln -s "$(python3 -c "import os; print(os.path.relpath('$GIT_ROOT/.env', '$(pwd)'))")" .env
ls -la .env  # Verify
```

## Why a New Terminal?

Claude Code's CWD and statusline are set at launch. If you `cd` into a worktree from an existing session, the statusline stays wrong, and auto-compact causes Claude to revert to the main repo.

The script outputs a copy-paste command that:
1. `cd`s to the worktree
2. Launches a **new** `claude` instance

This ensures correct statusline and stable context throughout the session.
