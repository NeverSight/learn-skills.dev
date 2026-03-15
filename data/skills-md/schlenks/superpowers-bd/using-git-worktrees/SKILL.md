---
name: using-git-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Directory Selection Process

Follow this priority order:

1. **Check existing directories** -- Use `.worktrees/` or `worktrees/` if present (`.worktrees/` wins if both exist)
2. **Check CLAUDE.md** -- Use any worktree directory preference specified there
3. **Ask user** -- Offer `.worktrees/` (project-local) or `~/.config/superpowers/worktrees/<project>/` (global)

See `references/directory-selection.md` for full bash commands and ask-user flow.

## Safety Verification

For project-local directories only (not needed for global):

1. **Check gitignore** -- `git check-ignore -q .worktrees` to verify directory is ignored
2. **Add if needed** -- Add to `.gitignore` if not ignored
3. **Commit** -- Commit the `.gitignore` change before proceeding

See `references/safety-verification.md` for full verification protocol.

## Creation Steps (Task-Tracked)

**Create 6 native tasks, each blocked by the previous (non-skippable sequence):**

1. **Select worktree directory location** -- Check existing dirs, CLAUDE.md, or ask user
2. **Verify gitignore for project-local directory** -- Run `git check-ignore`, add to `.gitignore` if needed
3. **Create worktree** -- `git worktree add <path> -b <branch>`
4. **Install dependencies** -- Auto-detect project type, run appropriate install command
5. **Run baseline tests** -- Capture output showing pass/fail; ask user if tests fail
6. **Worktree ready** -- Report location and test status; only complete if tests passed

See `references/creation-steps.md` for full TaskCreate blocks, bash commands, and setup detection.

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md -> Ask user |
| Directory not ignored | Add to .gitignore + commit |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |
| Done with worktree | Use ExitWorktree tool (2.1.72+) |

## Common Mistakes

- **Skipping ignore verification** -- worktree contents pollute git status. Always `git check-ignore` first.
- **Assuming directory location** -- follow priority: existing > CLAUDE.md > ask.
- **Proceeding with failing tests** -- report failures, get permission first.
- **Hardcoding setup commands** -- auto-detect from project files instead.

## Integration

**Called by:** brainstorming (after design), any skill needing isolated workspace
**Pairs with:** finishing-a-development-branch (cleanup), executing-plans / subagent-driven-development (work happens here)
**Cleanup:** ExitWorktree tool (2.1.72+) — see Quick Reference and `references/creation-steps.md` section 6.

## Reference Files

- `references/directory-selection.md`: full priority order with bash commands and ask-user flow
- `references/safety-verification.md`: full gitignore verification protocol with commands
- `references/creation-steps.md`: full TaskCreate blocks, bash commands, and setup detection
- `references/example-workflow.md`: annotated example of complete worktree setup workflow
- `references/red-flags.md`: Never/Always lists for quick self-check

<!-- compressed: 2026-02-11, original: 541 words, compressed: 481 words -->
