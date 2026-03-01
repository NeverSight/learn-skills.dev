---
name: feature-branch
description: >-
  Create a feature branch worktree as a sibling of the current project directory.
  TRIGGER when: user asks to create a branch, start a feature branch, or set up a worktree.
  Examples: "create a branch called add-user-export", "set up a worktree for fix-search".
  DO NOT TRIGGER when: user just wants to switch branches, view issues, or implement code.
allowed-tools: Bash, Read, AskUserQuestion
---

Create a feature branch in a new git worktree, as a sibling directory of the current project.

## Steps

1. Take the branch name from the argument. If none provided, ask the user — never generate a name.

2. Fetch the latest main:
   - `git fetch origin main`

3. Create the worktree:
   - `git worktree add ../<branch-name> -b <branch-name> origin/main`
   - This creates `../<branch-name>/` alongside the current project directory

4. Confirm to the user:
   - Show the branch name
   - Show the worktree path
