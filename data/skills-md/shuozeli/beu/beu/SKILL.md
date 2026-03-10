---
name: beu
description: >
  Persistent session-memory CLI for AI agent workflows. Provides journal,
  artifact, task, state, idea, and debug tracking across sessions and
  conversation compaction.
allowed-tools: "Read,Bash(beu:*)"
version: "0.1.0"
author: "Shuoze Li"
---

# beu -- Session Memory for AI Agents

You have access to `beu`, a persistent session-memory CLI. Use it to track work
across sessions and survive conversation compaction.

## When to Use beu

- Work spans multiple sessions or days
- Need to persist decisions, blockers, or context
- Tracking deliverables, tasks, or investigations
- Resuming after conversation compaction

## Session Protocol

```bash
beu resume              # Check checkpoint, blockers, focus items
beu journal open        # Start interaction ledger
# ... do work ...
beu check               # Verify docs are up to date (if configured)
beu pause "state desc"  # Save checkpoint before stopping
```

## Module Quick Reference

| Module | Purpose | Key Commands |
|--------|---------|--------------|
| journal | Interaction ledger | `open`, `log`, `note`, `summary`, `close` |
| artifact | Deliverable tracking | `add`, `status`, `list`, `show`, `changelog` |
| task | Work items + sprint view | `add`, `list`, `update`, `done`, `sprint`, `test-status` |
| state | Persistent memory | `set --category <C> <key> <value>`, `get`, `list`, `remove` |
| idea | Lightweight capture | `add`, `list`, `done`, `archive` |
| debug | Investigation tracking | `open`, `log`, `symptom`, `cause`, `resolve` |

## Test Status Tracking

Every task carries a `test_status` field that tracks the testing lifecycle:

```
planned -> designed -> implemented -> tested -> darklaunched -> launched
```

```bash
# View test pattern reference (unit, integration, systest, golden)
beu test patterns

# Update test status after writing tests
beu task test-status <id> implemented

# Mark tests as run and passing
beu task test-status <id> tested

# Filter tasks by test status
beu task list --test-status planned
```

Rules for agents:
- When adding a task for a new feature, `test_status` starts as `planned`.
- After deciding what tests to write (consult `beu test patterns`), set it to `designed`.
- After writing the tests, set it to `implemented`.
- After running the tests and confirming they pass, set it to `tested`.
- Include `beu task list --test-status planned` in the pre-pause checklist to catch untested work.

## Common Patterns

### Record a decision
```bash
beu state set --category decision "db-choice" "SQLite for simplicity"
```

### Track a blocker
```bash
beu state set --category blocker "ci-flaky" "Tests timeout on CI"
```

### Task workflow
```bash
beu task add "implement auth" --priority high --tag feature
beu task sprint                    # View sprint board
beu task update 1 --status in-progress
beu task done 1
```

### Test workflow
```bash
beu test patterns                  # See available test patterns
beu task test-status 1 designed    # Decided what tests to write
beu task test-status 1 implemented # Tests written
beu task test-status 1 tested      # Tests passing
beu task list --test-status planned # Find tasks still needing tests
```

### Debug investigation
```bash
beu debug open "connection timeout"
beu debug symptom conn-timeout "errors after 30s idle"
beu debug log conn-timeout "pool max_idle is 10s"
beu debug cause conn-timeout "idle timeout shorter than keepalive"
beu debug resolve conn-timeout
```

### Artifact tracking
```bash
beu artifact add design --type doc
beu artifact status design in-progress
beu artifact changelog design "added auth section"
```

## System Commands

```bash
beu status              # Project overview + enabled modules
beu progress            # Cross-module summary
beu events              # Recent event log
beu health              # Database integrity check
beu check               # Compliance gate (required docs)
beu export --all        # Export all data as JSON
beu update-rules        # Re-install latest skill files
```

## Configuration

`.beu/config.yml` controls which modules are active:

```yaml
modules:
  journal: true
  artifact: true
  task: true
  state: true
  idea: true
  debug: true

# Optional: override built-in test patterns
test_patterns:
  - key: property
    description: QuickCheck/proptest-based property testing.
```

Disabled modules return an error when their commands are invoked.

## Project Scoping

Use `-p <project>` to scope commands to a specific project within a shared
`.beu` database. Without the flag, the default project is used.

## Global Flags

- `--beu-dir <PATH>`: Override .beu directory location
- `-p, --project <ID>`: Project scope
- `-v, --verbose`: Detailed output
- `-q, --quiet`: Suppress non-essential output
