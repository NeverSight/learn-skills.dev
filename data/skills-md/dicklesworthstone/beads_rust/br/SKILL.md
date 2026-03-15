---
name: br
description: >-
  Official skill for beads_rust (`br`), a local-first, dependency-aware issue
  tracker for AI agents. Use when creating issues, triaging backlogs, managing
  dependencies, finding ready work, updating status, or syncing to git via JSONL.
license: MIT
domain: project-management
role: specialist
scope: operations
output-format: commands
triggers:
  - br
  - beads
  - beads_rust
  - issue tracker
  - issue triage
  - backlog
  - dependencies
  - ready work
metadata:
  author: Dicklesworthstone
  version: 1.0.0
---

<!-- TOC: Critical Rules | Quick Workflow | Essential Commands | Dependencies | Sync | bv Integration | Agent Mail | Troubleshooting | References -->

# br -- Beads Rust Issue Tracker (Official Skill)

> **Non-invasive:** br NEVER runs git commands. Sync and commit are YOUR responsibility.

## Critical Rules for Agents

| Rule | Why |
|------|-----|
| **Binary is `br`** | NEVER `bd` (that is the old Go version) |
| **ALWAYS use `--json`** | Structured output for parsing; `--format toon` for reduced tokens |
| **NEVER run bare `bv`** | Blocks session in interactive TUI mode |
| **Sync is EXPLICIT** | `br sync --flush-only` exports DB to JSONL only |
| **Git is YOUR job** | br only touches `.beads/` -- you must `git add .beads/ && git commit` |
| **No cycles allowed** | `br dep cycles` must return empty |
| **Resolve actor at runtime** | Use `ACTOR="${BR_ACTOR:-assistant}"` and pass `--actor "$ACTOR"` |

## Quick Workflow

```bash
ACTOR="${BR_ACTOR:-assistant}"

# 1. Find work
br ready --json

# 2. Claim it
br update --actor "$ACTOR" <id> --status in_progress

# 3. Do work...

# 4. Complete
br close --actor "$ACTOR" <id> --reason "Implemented X"

# 5. Sync to git (EXPLICIT!)
br sync --flush-only
git add .beads/ && git commit -m "feat: X (<id>)"
```

## Essential Commands

### Issue Lifecycle

```bash
ACTOR="${BR_ACTOR:-assistant}"

br init                                              # Initialize .beads/ workspace
br create --actor "$ACTOR" "Title" -p 1 -t task      # Create issue (priority 0-4)
br q --actor "$ACTOR" "Quick note"                   # Quick capture (ID only output)
br show <id> --json                                  # Show issue details
br update --actor "$ACTOR" <id> --status in_progress # Update status
br update --actor "$ACTOR" <id> --priority 0         # Change priority
br close --actor "$ACTOR" <id> --reason "Done"       # Close with reason
br close --actor "$ACTOR" <id1> <id2> --reason "..."  # Close multiple at once
br reopen --actor "$ACTOR" <id>                      # Reopen closed issue
```

### Create Options

```bash
br create --actor "$ACTOR" "Title" \
  --priority 1 \             # 0-4 scale (0=critical, 4=backlog)
  --type task \              # task, bug, feature, epic, question, docs
  --assignee "user@..." \    # Optional assignee
  --labels backend,auth \    # Comma-separated labels
  --description "..."        # Detailed description
```

### Update Options

```bash
br update --actor "$ACTOR" <id> \
  --title "New title" \
  --priority 0 \
  --status in_progress \     # open, in_progress, closed
  --assignee "new@..." \
  --add-label reliability \
  --parent <parent-id> \
  --claim                    # Shorthand for claim-and-start
```

Bulk update (batch triage):
```bash
br update --actor "$ACTOR" <id1> <id2> <id3> --priority 2 --add-label triage-reviewed --json
```

### Querying (always use --json for agents)

```bash
br ready --json                      # Actionable work (no blockers)
br list --json                       # All issues
br list --status open --sort priority --json  # Filter and sort
br list --priority 0-1 --json        # Filter by priority range
br list --assignee alice --json      # Filter by assignee
br blocked --json                    # Show blocked issues
br search "keyword" --json           # Full-text search
br show <id> --json                  # Issue details with dependencies
br stale --days 30 --json            # Stale issues
br count --by status --json          # Count with grouping
```

### Dependencies

```bash
br dep add <child> <parent>          # child depends on parent
br dep add <id> <depends-on> --type blocks  # Explicit block type
br dep remove <child> <parent>       # Remove dependency
br dep list <id> --json              # List dependencies for issue
br dep tree <id> --json              # Show dependency tree
br dep cycles --json                 # Find circular deps (MUST be empty!)
```

**Critical:** `br dep cycles` must return empty. Circular dependencies break the dependency graph and make `br ready` unreliable.

### Labels

```bash
br label add <id> backend auth       # Add multiple labels
br label remove <id> urgent          # Remove label
br label list <id>                   # List issue's labels
br label list-all                    # All labels in project
```

### Comments

```bash
ACTOR="${BR_ACTOR:-assistant}"
br comments add --actor "$ACTOR" <id> --message "Triage note" --json
br comments list <id> --json
```

### Sync (EXPLICIT -- never automatic)

```bash
br sync --flush-only                 # Export DB to JSONL (before git commit)
br sync --import-only                # Import JSONL to DB (after git pull)
br sync --status                     # Check sync status
```

Workflow after making changes:
```bash
br sync --flush-only
git add .beads/ && git commit -m "Update issues"
```

Workflow after pulling:
```bash
git pull
br sync --import-only
```

### System and Diagnostics

```bash
br doctor                            # Full diagnostics
br stats --json                      # Project statistics
br config list                       # Show all configuration
br config get id.prefix              # Get specific value
br config set defaults.priority=1    # Set value
br where                             # Show workspace location
br version                           # Show version
br upgrade                           # Self-update (if enabled)
br lint --json                       # Lint issues for problems
```

## Priority Scale

| Priority | Meaning | Use numbers, not words |
|----------|---------|------------------------|
| 0 | Critical | Immediate action required |
| 1 | High | Important, do soon |
| 2 | Medium (default) | Normal priority |
| 3 | Low | When time permits |
| 4 | Backlog | Future consideration |

## Issue Types

`task`, `bug`, `feature`, `epic`, `question`, `docs`

## Output Formats

| Flag | Use case |
|------|----------|
| `--json` | Default for agents -- full structured data |
| `--format toon` | Token-optimized alternative for context-window-sensitive agents |
| (no flag) | Human-readable terminal output with colors |

## bv Integration

**CRITICAL:** Never run bare `bv` -- it launches interactive TUI and blocks.

```bash
# Always use --robot-* flags:
bv --robot-next                      # Single top pick + claim command
bv --robot-triage                    # Full triage with recommendations
bv --robot-plan                      # Parallel execution tracks
bv --robot-insights | jq '.Cycles'   # Check graph health (must be empty)
bv --robot-priority                  # Priority misalignment detection
bv --robot-alerts                    # Stale issues, blocking cascades
```

## Agent Mail Coordination

Use bead ID as thread_id for multi-agent coordination:

| Concept | Value |
|---------|-------|
| Mail `thread_id` | `bd-###` (the issue ID) |
| Mail subject | `[bd-###] ...` |
| File reservation `reason` | `bd-###` |
| Commit messages | Include `bd-###` for traceability |

```python
# 1. Reserve files for bead
file_reservation_paths(..., reason="bd-123")

# 2. Announce work in thread
send_message(..., thread_id="bd-123", subject="[bd-123] Starting...")

# 3. Do work...

# 4. Close bead and release
br close bd-123 --reason "Completed"
release_file_reservations(...)
```

## Session Ending Pattern

Before ending any work session:

```bash
git pull --rebase
br sync --flush-only
git add .beads/ && git commit -m "Update issues"
git push
git status  # MUST show "up to date with origin"
```

## Standard Agent Workflow (Full)

```bash
ACTOR="${BR_ACTOR:-assistant}"

# 1. Verify workspace
br where
br ready --json
br blocked --json
br list --status open --sort priority --json

# 2. Pick highest-priority ready work
br show <id> --json

# 3. Claim it
br update --actor "$ACTOR" <id> --status in_progress --claim

# 4. Do work...

# 5. Close with evidence
br close --actor "$ACTOR" <id> --reason "Implemented X in commit abc123"

# 6. Check queue impact
br ready --json
br blocked --json

# 7. Sync to git
br sync --flush-only
git add .beads/ && git commit -m "feat: X (<id>)"
git push
```

## Triage Decision Matrix

Classify each issue into exactly one category:

| Classification | Action |
|---------------|--------|
| `implemented` | Close with evidence (commit/PR/file/behavior) |
| `out-of-scope` | Close with explicit boundary reason |
| `needs-clarification` | Comment with specific unanswered questions |
| `actionable` | Keep open, correct status/priority/labels/deps |

During large triage efforts, checkpoint every few updates:
```bash
br ready --json
br blocked --json
```

## Anti-Patterns

- Running `br sync` without `--flush-only` or `--import-only`
- Forgetting sync before git commit
- Creating circular dependencies
- Running bare `bv` (blocks session)
- Assuming auto-commit behavior (br NEVER auto-commits)
- Inventing evidence for closure -- if unsure, comment instead
- Modifying unrelated issues during triage
- Adding speculative dependencies

## Storage Layout

```
.beads/
  beads.db        # SQLite database (primary storage)
  beads.db-shm    # SQLite shared memory (WAL mode)
  beads.db-wal    # SQLite write-ahead log
  issues.jsonl    # JSONL export (for git)
  config.yaml     # Project configuration
  metadata.json   # Workspace metadata
```

## Troubleshooting

```bash
br doctor                    # Full diagnostics
br dep cycles                # Must be empty
br config list               # Check settings
which br                     # Verify br is installed
```

**"Database locked"**: Check for other `br` processes with `pgrep -f "br "`.

**Worktree error** (`'main' is already checked out`):
```bash
git branch beads-sync main
br config set sync.branch beads-sync
```

**Verbose debugging:**
```bash
br -v list                   # Verbose
br -vv list                  # Debug
RUST_LOG=debug br list       # Detailed trace logs
```

## References

| Topic | File |
|-------|------|
| Command cookbook | [references/COMMANDS.md](references/COMMANDS.md) |
| Configuration details | [references/CONFIG.md](references/CONFIG.md) |
| Troubleshooting guide | [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) |
| Multi-agent integration | [references/INTEGRATION.md](references/INTEGRATION.md) |
