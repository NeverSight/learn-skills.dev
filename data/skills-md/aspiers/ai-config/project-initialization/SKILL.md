---
name: project-initialization
description: Initialize a project with AI agent rules and documentation. Use when setting up a new repository for AI agent collaboration.
---

# Project Initialization

Improve the results of running the `/init` command to create AI agent rules.

## When to Use This Skill

Use this skill when:
- Setting up a new repository for AI agent collaboration
- Neither `CLAUDE.md` nor `AGENTS.md` exists
- The `/init` command has been run but needs improvement
- You want AI agent rules to be discoverable by multiple agents

## Goal

The `/init` command creates `CLAUDE.md`, but this is only useful for Claude Code.
This skill ensures the same file contents are discoverable and readable by
multiple AI agents looking in different places.

This follows the standard documented at: https://agent-rules.org/

## Process

Perform the following steps:

1. **Check existing files**: Verify if `CLAUDE.md` and/or `AGENTS.md` exist

2. **Handle new project**: If neither file exists, first run Claude's `/init` process to generate initial content

3. **Rename if needed**: If only `CLAUDE.md` exists, rename it to `AGENTS.md`

4. **Create symlinks**: Generate symlinks so different agents can find the rules:
   - `CLAUDE.md` → points to `AGENTS.md`

5. **Fix unsafe `git push` commands**: Scan all agent instruction files
   (`AGENTS.md`, `CLAUDE.md`, and any other files they reference) for
   bare or underspecified `git push` invocations that could
   accidentally push to the wrong branch. This is a common problem
   with instructions added by tools like beads.

   **What to look for**: any `git push` that does NOT specify both
   a remote and a refspec, e.g.:
   - `git push` (no arguments at all)
   - `git push origin` (remote but no refspec)
   - `git push --force` (flags but no remote/refspec)

   **Why this matters**: a bare `git push` relies on the upstream
   tracking branch configuration. If you're on a feature branch
   that happens to track `main`, `git push` will push your feature
   commits directly to `main`. Using `git push origin HEAD` is much
   safer because it pushes the current branch to a remote branch of
   the same name, preventing accidental pushes to trunk branches.

   **How to fix**: replace bare `git push` with
   `git push origin HEAD`. Preserve any flags that were present,
   e.g. `git push --force` → `git push origin HEAD --force`.

   **Edge cases to handle**:
   - Lines inside code blocks (` ``` `) and inline code (`` ` ``)
   - Lines in checklists like `[ ] 6. git push  (push to remote)`
   - Comments after the command, e.g. `git push  # deploy`
   - Multiple occurrences in the same file
   - Do NOT modify lines that already specify both remote and
     refspec (e.g. `git push origin main`,
     `git push origin HEAD`)

6. **Verify**: Confirm the symlinks work by checking file accessibility

## Context

- Existing files: `ls CLAUDE.md AGENTS.md`

## Example Commands

```bash
# Check existing files
ls -la CLAUDE.md AGENTS.md

# Rename if needed
mv CLAUDE.md AGENTS.md

# Create symlinks
ln -s AGENTS.md CLAUDE.md

# Verify
cat CLAUDE.md
```

### Fixing unsafe `git push`

Search agent instruction files for bare `git push`:

```bash
# Find bare git push commands in agent files
grep -n 'git push' AGENTS.md CLAUDE.md .beads/context/*.md
```

Example transformations:

| Before | After |
|--------|-------|
| `git push` | `git push origin HEAD` |
| `git push --force` | `git push origin HEAD --force` |
| `git push origin` | `git push origin HEAD` |
| `[ ] 6. git push` | `[ ] 6. git push origin HEAD` |

Leave these unchanged (already safe):

| Already safe |
|--------------|
| `git push origin HEAD` |
| `git push origin main` |
| `git push origin HEAD --force` |
| `git push -u origin HEAD` |

## Result

After this process:
- `AGENTS.md` contains the authoritative AI agent rules
- `CLAUDE.md` is a symlink to `AGENTS.md`
- Multiple AI agents can discover and read the same rules
- All `git push` commands in agent instructions explicitly
  specify remote and refspec to prevent accidental pushes
  to trunk branches
