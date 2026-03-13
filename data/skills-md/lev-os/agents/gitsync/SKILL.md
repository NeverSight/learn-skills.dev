---
name: gitsync
description: Fast git sync with project codes - add, commit, pull (no rebase), push
trigger: /sync, gitsync, "sync repos", "git sync", "push all"
---

# gitsync

Fast parallel git sync across repos with project code resolution.

## Quick Reference

```bash
# By project code
/sync naac lev clawd chezmoi    # Sync named projects
/sync all                        # Sync all dirty repos
/sync all --dry-run              # Preview what would sync

# By path
/sync ~/proj1 ~/proj2            # Sync specific paths
/sync .                          # Sync current directory

# Options
--dry-run                        # Preview without changes
```

## Project Codes

The registry at `~/.claude/skills/gitsync/projects.json` maps codes to paths:

| Code | Path |
|------|------|
| `naac` | ~/k/apps/production/naac |
| `lev` | ~/lev |
| `clawd` | ~/clawd |
| `chezmoi` | ~/.local/share/chezmoi |
| `dotfiles` | ~/.dotfiles |
| `leviathan` | ~/digital/leviathan |
| `clawdbot` | ~/.clawdbot |

## Output Key

| Symbol | Meaning |
|--------|---------|
| **b** | bd flush (daemon running) |
| **B** | bd sync (no daemon) |
| **C** | Committed |
| **P** | Pulled |
| **U** | Pushed |
| **.** | Skipped (nothing to do) |
| **D** | Dirty (dry-run only) |

## What It Does

1. **Resolves project codes** → paths via registry
2. **For each target:**
   - `git add .`
   - `git commit -m "sync MM-DD HH:MM"` (if dirty)
   - `git pull --no-rebase`
   - `git push`
3. **Discovers and syncs:**
   - All git worktrees
   - All submodules (recursive)

## Sync All Mode

`/sync all` scans all registered projects and syncs those with uncommitted changes.

```bash
/sync all              # Sync all dirty repos
/sync all --dry-run    # List dirty repos without syncing
```

## Agent Integration

When the script exits with code 1 (conflicts detected), the agent MUST:

### Step 1: Analyze Conflicts
```bash
# For each conflicted repo reported by gitsync:
cd <conflicted-repo>
git status --porcelain | grep "^UU"  # List conflicted files
git diff --name-only --diff-filter=U  # Alternative
```

### Step 2: Present Action Dashboard
Use AskUserQuestion with these options:

```
header: "Merge Conflict"
question: "How should I resolve conflicts in <repo>?"
options:
  - "Accept ours (keep local changes)"
  - "Accept theirs (take remote changes)"
  - "Smart merge (launch subagent)"
  - "Skip (I'll handle manually)"
```

### Step 3: Execute Resolution

**Accept ours:**
```bash
git checkout --ours .
git add .
git commit -m "resolve: accept local changes"
git push
```

**Accept theirs:**
```bash
git checkout --theirs .
git add .
git commit -m "resolve: accept remote changes"
git push
```

**Smart merge (subagent):**
```
Launch Task agent with subagent_type="code-refactoring:code-reviewer"
Prompt: "Analyze and resolve merge conflicts in <repo>.
         Show me the conflicts, explain what each side changed,
         and propose a merged solution that preserves both intents."
```

### Step 4: Re-run Sync
After resolution, re-run `gitsync <repo>` to complete the push.

## Conflict Resolution (Manual)

If conflicts detected:

```bash
cd <conflicted-repo>
git status                    # see conflicts
git checkout --ours <file>    # take local
git checkout --theirs <file>  # take remote
git add . && git commit       # complete merge
```

Then re-run `/sync` to continue.

## Execution

```bash
~/.claude/skills/gitsync/scripts/gitsync.sh [codes|paths...] [--dry-run]
```

## Installation

```bash
ln -sf ~/.claude/skills/gitsync/scripts/gitsync.sh ~/.claude/bin/gitsync
```

## Technique Map

- **Identify scope** — Determine what the skill applies to before executing.
- **Follow workflow** — Use documented steps; avoid ad-hoc shortcuts.
- **Verify outputs** — Check results match expected contract.
- **Handle errors** — Graceful degradation when dependencies missing.
- **Reference docs** — Load references/ when detail needed.
- **Preserve state** — Don't overwrite user config or artifacts.

## Technique Notes

Skill-specific technique rationale. Apply patterns from the skill body. Progressive disclosure: metadata first, body on trigger, references on demand.

## Prompt Architect Overlay

**Role Definition:** Specialist for gitsync domain. Executes workflows, produces artifacts, routes to related skills when needed.

**Input Contract:** Context, optional config, artifacts from prior steps. Depends on skill.

**Output Contract:** Artifacts, status, next-step recommendations. Format per skill.

**Edge Cases & Fallbacks:** Missing context—ask or infer from workspace. Dependency missing—degrade gracefully; note in output. Ambiguous request—clarify before proceeding.
