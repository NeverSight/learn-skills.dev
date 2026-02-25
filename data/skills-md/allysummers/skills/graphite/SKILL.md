---
name: graphite
description: |
  Use for Graphite CLI stacked PRs workflow in repos with .git/.graphite_repo_config.
  Triggers: graphite, stacked PRs, dependent PRs, chained PRs, PR stack, gt create,
  gt modify, gt submit, gt sync, gt restack, gt log, gt checkout, gt up, gt down,
  rebase my stack, fix stack conflicts, split PR, land my stack, merge stack,
  sync with main/trunk, reorder branches, fold commits, amend stack, move branch
  to different parent, stack out of date, update my stack. For repos WITHOUT
  .git/.graphite_repo_config, use standard git commands instead.
---
<!--
  Modified from claude-code-graphite by George Guimarães
  (https://github.com/georgeguimaraes/claude-code-graphite)
  Licensed under the Apache License, Version 2.0.
  Changes: Adapted from Claude Code plugin format to Cursor agent skill;
  updated MCP server references for Cursor.
-->

# Graphite Stacked PRs Workflow

**IMPORTANT:** This workflow applies ONLY to repositories with `.git/.graphite_repo_config`. For repositories without this file, use standard git commands (`git commit`, `git push`, etc.).

## Detection

Check for `.git/.graphite_repo_config` to determine if a repo uses Graphite:
- **File exists:** Use `gt` commands (this skill applies)
- **File does not exist:** Use standard `git` commands (this skill does NOT apply)

When Graphite is detected, use `gt` commands instead of `git` for all commit and branch operations.

## MCP Server

A Graphite MCP server may be available (requires Graphite CLI v1.6.7+). If the `graphite` MCP server is configured in your Cursor MCP settings, it provides tools to work with stacked PRs.

To set up, add the following to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "graphite": {
      "command": "gt",
      "args": ["mcp"]
    }
  }
}
```

## Planning Stacks (CRITICAL)

**Before writing any code, present the stack structure and ask for confirmation.**

When building a feature as a stack:

1. **Plan first** - break the work into logical, sequential PRs
2. **Use TodoWrite** - each todo item maps to one PR/`gt create`
3. **Present the structure** - show the user the planned stack:
   ```
   PR Stack for [Feature]:
   1. PR 1: [description] - [what it does]
   2. PR 2: [description] - [what it does]
   3. PR 3: [description] - [what it does]
   ```
4. **Ask for confirmation** - "Does this structure look good to proceed?"
5. **Only then start coding**

**IMPORTANT:** Each PR must be atomic and pass CI independently. Verify this before committing.

## Command Mapping

Use these `gt` commands instead of their git equivalents:

| Instead of | Use | Purpose |
|------------|-----|---------|
| `git commit` | `gt create -am "msg"` | Create new branch/PR with changes |
| `git commit --amend` | `gt modify -a` | Amend current PR |
| `git push` | `gt submit --no-interactive` | Submit current + all downstack branches |
| `git pull` | `gt sync` | Pull trunk, restack, clean merged |
| `git checkout` | `gt checkout <branch>` | Switch branches |
| `git rebase` | `gt restack` | Rebase stack (usually via `gt sync`) |

## When to Create vs Amend

**Use `gt create -am "message"`** when:
- Starting new work (new feature, new fix)
- The change is logically separate from current PR
- Building the next piece in a stack

**Use `gt modify -a`** when:
- Addressing PR review feedback
- Fixing something in the current PR
- Adding forgotten changes to current work

## Commit and PR Style

### Commit Messages

- Keep it brief and human
- No LLM fluff, no em dashes

### PR Body Descriptions

Write PR bodies that explain:
1. **What** changed
2. **Why** it changed
3. **The benefit** or purpose

Keep descriptions casual, concise, and human-like. Avoid corporate speak or overly formal language. Don't wrap long lines with line breaks (unlike git commits). Line breaks are fine for separating paragraphs.

Make sure to check if the repo uses a PR template by checking for the existence of `.github/pull_request_template.md`.

### After Submitting

When returning the PR URL to the user, use the **Graphite PR URL** (e.g., `https://app.graphite.dev/github/pr/...`), not the GitHub PR URL.

## Stack Philosophy

Each PR in a stack must be:
- **Atomic** - passes CI independently, no broken intermediate states
- **Small** - ideally under 250 lines changed
- **Focused** - one logical change per branch
- **Reviewable** - makes sense on its own (even if it depends on others)

### Stacking Frameworks

**Functional component stacks** — one PR per layer:
- Database changes first
- Backend logic next
- Frontend last

**Iterative improvement stacks** — ship and build on top:
- Basic implementation
- Error handling
- Tests
- Polish

**Refactor/change stacks** — separate cleanup from the fix:
- PR 1: Refactor the surrounding code
- PR 2: The actual bug fix or feature

**Version bumps/generated code stacks** — isolate boilerplate:
- PR 1: Version bump or code generation
- PR 2: Changes that use the updates

**Riskiness stacks** — isolate risky changes for easy revert:
- PR 1: Low-risk changes
- PR 2: High-risk change (easy to revert independently)

**Note:**
If something is too big to be done atomically in 1 PR, it _may_ be done in a stack of where the top of the stack (or a specific merge-point) passes CI, even if the PRs under it do not. This should rarely be used and should be used as a last resort. If something is split up because of its size for this reason, each PR should make sure to group changes into parts that are easiest to be reviewed together.

## Navigation

Move through the stack:

```bash
gt log          # View full stack with PR status
gt ls           # Abbreviated stack view
gt up           # Move up one branch (toward tip)
gt down         # Move down one branch (toward trunk)
gt top          # Jump to top of stack
gt bottom       # Jump to bottom of stack
gt checkout X   # Switch to specific branch
```

## Sync Workflow

Run `gt sync` regularly (at least daily) to:
1. Pull latest trunk changes
2. Restack all branches
3. Clean up merged branches

When `gt sync` encounters conflicts, it pauses for resolution. See conflict resolution below.

## Checkpointing

Use `gt create` as checkpoints during development without submitting yet. Once the work is in a good state, use `gt fold` to consolidate checkpoint branches into logical PRs before submitting. This prevents creating unnecessary PRs for intermediate work.

```bash
gt create -am "checkpoint: initial scaffolding"
# ... more work ...
gt create -am "checkpoint: wire up endpoints"
# ... ready to consolidate ...
gt fold                      # Merge current branch into its parent
```

If you over-fold, `gt split` can break a branch back apart.

## Submitting Work

Push changes with:

```bash
gt submit --no-interactive   # Submit current + all downstack branches (recommended)
gt submit --stack            # Submit current + all descendant branches
gt ss                        # Shorthand for --stack
```

Use `--no-interactive` to avoid prompts during submission.

**IMPORTANT:** If you make changes lower in the stack (e.g. via `gt modify`), use `gt submit --stack` instead of `gt submit`. Otherwise upstack PRs won't reflect the changes, and their GitHub diffs will be stale.

## Conflict Resolution

When `gt sync` or `gt restack` hits conflicts:

1. **Understand what conflicted** - check which branch and what files
2. **Check what each branch does** - use `gt log` and review the changes
3. **Auto-resolve obvious conflicts:**
   - Import order changes
   - Whitespace differences
   - Non-overlapping additions
4. **Ask about ambiguous conflicts:**
   - Same code modified differently
   - Deleted vs modified conflicts
   - Semantic conflicts (logic changes)

After resolving:
```bash
gt continue -a      # Stage all and continue restack
```

If stuck:
```bash
gt abort            # Abandon restack, return to previous state
```

For detailed conflict resolution patterns, see `references/conflict-resolution.md`.

## Reorganizing Stacks

Adjust stack structure when needed:

```bash
gt move --onto <branch>   # Move current branch to new parent
gt fold                   # Merge branch into its parent
gt split                  # Break branch into multiple
gt squash                 # Combine commits in branch to one
gt reorder                # Interactively reorder branches
```

## Collaboration

Work with others' stacks:

```bash
gt get <branch>           # Fetch someone's stack locally
gt track <branch>         # Start tracking existing git branch
```

## Quick Reference

See `references/cheatsheet.md` for a complete command reference.

## Common Workflows

### Building a Feature as a Stack

1. Plan the stack structure first (use TodoWrite)
2. Present to user and get confirmation
3. Implement each PR sequentially:

```bash
gt sync                                    # Get latest
gt create -am "feat: Add avatar upload API"
# ... verify it passes CI ...
gt create -am "feat: Add avatar display component"
# ... verify it passes CI ...
gt create -am "feat: Add avatar to user profile"
gt submit --no-interactive                 # Submit entire stack
```

### Addressing Review Feedback

```bash
gt checkout <branch-with-feedback>
# ... make fixes ...
gt modify -a                               # Amend changes
gt submit --no-interactive                 # Push updates (auto-restacks dependents)
```

### Daily Sync Routine

```bash
gt sync                                    # Pull, restack, clean
# Resolve any conflicts if prompted
gt continue -a                             # After resolving
```
