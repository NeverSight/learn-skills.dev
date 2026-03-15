---
name: beads
description: Use when working with the beads (bd) CLI for issue tracking, managing epics and tasks, handling dependencies, or starting/ending coding sessions with persistent work tracking
---

# Beads (bd) Usage Rules

## First-Time Setup

**If `bd` command is not found**, tell the user:

> Run: `curl -fsSL https://raw.githubusercontent.com/schlenks/superpowers-bd/main/scripts/setup-beads-local.sh | bash`
> This installs beads, initializes stealth mode, and adds git worktree support. For team use (shared `.beads/`), use `bd init` without `--stealth`.

## TL;DR

```bash
bd ready                    # What can I work on?
bd update <id> --claim      # I'm starting this
bd close <id>               # I'm done with this
```

**Critical rules:**
- Never use semicolons in `--acceptance` (triggers permission prompts)
- Never use `bd edit` (opens interactive editor)
- Dolt auto-commits after each write command (default config) — no manual sync needed

## Permission Avoidance (Critical)

- Never use semicolons in `--acceptance`: `;` pattern triggers prompts. Use commas or `$'...\n...'`
- Use `--body-file` for multi-line content: newlines break pattern matching. Write to temp file first
- Never delete temp files with `rm`: triggers permission prompts. Leave for human cleanup

## Issue Operations

- Create epic: `bd create --silent --type epic "Title" --body-file temp/desc.md -p 1`
- Create child task: `bd create --silent --parent <epic-id> "Title" --body-file temp/desc.md -p 2`
- Add dependencies: `--deps "id1,id2"` (comma-separated, no spaces)
- View issue: `bd show <id>`
- Update issue: `bd update <id> --status=in_progress`
- Claim issue: `bd update <id> --claim` (sets assignee + in_progress atomically)
- Close issue: `bd close <id>`
- Close multiple: `bd close <id1> <id2> <id3>`
- Close with reason: `bd close <id> --reason "explanation"`
- Add comment: `bd comments add <id> "comment text"`
- Add comment from file: `bd comments add <id> -f temp/comment.md`

## Query Commands

- Ready work (no blockers): `bd ready`
- Blocked work: `bd blocked`
- Search issues: `bd search --query "text" --status open`
- List with filters: `bd list --status open --type task --priority-max 2`
- View dependency graph: `bd graph <id>`
- Check stale issues: `bd stale --days 14`
- Lint issues: `bd lint --status open`

## Maintenance Commands

- Health check: `bd doctor`
- Auto-fix issues: `bd doctor --fix`
- Cleanup old issues: `bd cleanup`
- Prime AI context: `bd prime`
- Database info: `bd info`

## Key Flags

- `--silent`: output only ID (for scripting)
- `--json`: output in JSON format
- `--quiet`: suppress non-essential output
- `--type`: bug, feature, task, epic, chore, merge-request, molecule, gate
- `--parent <id>`: create as child of epic
- `-d "text"`: single-line description (prefer `--body-file` for multi-line)
- `--body-file <path>`: read description from file
- `-p N`: priority 0-4 (0=critical, 4=backlog)
- `--deps "id1,id2"`: dependencies (blocked by these)
- `--acceptance "..."`: acceptance criteria (no semicolons!)
- `--external-ref "ref"`: external link (e.g., "sc-1234")
- `-l "label1,label2"`: labels (comma-separated)

## Session End Protocol

```bash
bd create "Remaining work" -d "..." -p 2   # 1. File remaining work
bd close <completed-ids>                    # 2. Close completed (unblocks dependents)
git status                                  # 3. Check what changed
git add <files>                             # 4. Stage code changes
git commit -m "..."                         # 5. Commit changes
# Dolt auto-commits after each bd write command — no manual sync needed
```

## Integration with Skills

- `superpowers-bd:plan2beads`: convert markdown plan to epic with child tasks
- `superpowers-bd:writing-plans`: create plans with `Depends on:` and `Files:` sections
- `superpowers-bd:subagent-driven-development`: parallel execution with dependency awareness

## Reference Files

- `references/acceptance-and-multiline.md`: writing acceptance criteria or multi-line descriptions
- `references/bd-edit-and-sandbox.md`: encountering bd edit usage or sandbox errors
- `references/dependency-management.md`: creating dependencies, fixing deadlocks, verifying dep structure
- `references/workflow-patterns.md`: running autonomous work loops, checking status values
- `references/session-end-details.md`: auto-commit behavior and ephemeral branch handling
- `references/sync-workflow.md`: Dolt persistence commands, auto-commit config, backup/export
- `references/troubleshooting.md`: database sync issues, worktree limitations, merge conflicts
- `references/parallel-execution-safety.md`: dispatching parallel subagents, epic scoping, priority values, ID format

<!-- compressed: 2026-02-11, original: 891 words, compressed: 645 words -->
