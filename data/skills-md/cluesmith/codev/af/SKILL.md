---
name: af
description: Agent Farm CLI — the tool for spawning builders, managing Tower, workspaces, and cron tasks. ALWAYS consult this skill BEFORE running any `af` command to get the exact syntax. This prevents wasting time guessing flags that don't exist. Use this whenever you need to spawn a builder, check status, send messages, clean up worktrees, manage Tower, or run cron tasks. If you're about to type `af` followed by anything, check here first.
---

# Agent Farm CLI

## af spawn

Spawns a new builder in an isolated git worktree.

```
af spawn [number] [options]
```

**The ONLY flags that exist:**

| Flag | Description |
|------|-------------|
| `--protocol <name>` | Protocol: spir, aspir, air, bugfix, tick, maintain, experiment. **Required for numbered spawns.** |
| `--task <text>` | Ad-hoc task (no issue number needed) |
| `--shell` | Bare Claude session |
| `--worktree` | Bare worktree session |
| `--amends <number>` | Original spec number (TICK only) |
| `--files <files>` | Context files, comma-separated. **Requires `--task`.** |
| `--no-comment` | Skip commenting on the GitHub issue |
| `--force` | Skip dirty-worktree and collision checks |
| `--soft` | Soft mode (AI follows protocol, you verify) |
| `--strict` | Strict mode (porch orchestrates) — this is the default |
| `--resume` | Resume builder in existing worktree |
| `--no-role` | Skip loading role prompt |

**There is NO `-t`, `--title`, `--name`, or `--branch` flag.** The branch name is auto-generated from the issue title.

**Examples:**
```bash
af spawn 42 --protocol spir           # SPIR builder for issue #42
af spawn 42 --protocol aspir          # ASPIR (autonomous, no human gates)
af spawn 42 --protocol air            # AIR (small features)
af spawn 42 --protocol bugfix         # Bugfix
af spawn 42 --protocol tick --amends 30  # TICK amendment to spec 30
af spawn 42 --protocol spir --soft    # Soft mode
af spawn 42 --resume                  # Resume existing builder
af spawn --task "fix the flaky test"  # Ad-hoc task (no issue)
af spawn 42 --protocol spir --force   # Skip dirty-worktree check
```

**Pre-spawn checklist:**
1. `git status` — worktree must be clean (or use `--force`)
2. Commit specs/plans first — builders branch from HEAD and can't see uncommitted files
3. `--protocol` is required for numbered spawns

## af send

Sends a message to a running builder.

```
af send [builder] [message]
```

| Flag | Description |
|------|-------------|
| `--all` | Send to all builders |
| `--file <path>` | Include file content |
| `--interrupt` | Send Ctrl+C first |
| `--raw` | Skip structured formatting |
| `--no-enter` | Don't press Enter after message |

```bash
af send 0042 "PR approved, please merge"
af send 0585 "check the test output" --file /tmp/test-results.txt
```

## af cleanup

Removes a builder's worktree and branch after work is done.

```
af cleanup [options]
```

| Flag | Description |
|------|-------------|
| `-p, --project <id>` | Builder project ID (no leading zeros: `585` not `0585`) |
| `-i, --issue <number>` | Cleanup bugfix builder by issue number |
| `-t, --task <id>` | Cleanup task builder (e.g., `task-bEPd`) |
| `-f, --force` | Force cleanup even if branch not merged |

```bash
af cleanup -p 585              # Clean up project 585
af cleanup -p 585 -f           # Force (unmerged branch)
```

**Note:** `af cleanup` uses plain numbers (`585`), not zero-padded (`0585`). But `af send` uses zero-padded IDs (`0585`).

## af status

```bash
af status                      # Show all builders and workspace status
```

No flags needed. Shows Tower status, workspace, and all active builders.

## af tower

```bash
af tower start                 # Start Tower on port 4100
af tower stop                  # Stop Tower
af tower log                   # Tail Tower logs
af tower status                # Check daemon and cloud connection status
af tower connect               # Connect to Codev Cloud
af tower disconnect            # Disconnect from Codev Cloud
```

There is NO `af tower restart` — use `af tower stop && af tower start`.

## af workspace

```bash
af workspace start             # Start workspace for current project
af workspace stop              # Stop workspace processes
```

`af dash` is a deprecated alias — use `af workspace` instead.

## af cron

```bash
af cron list                   # List all cron tasks
af cron status <name>          # Check task status
af cron run <name>             # Run immediately
af cron enable <name>          # Enable
af cron disable <name>         # Disable
```

There is NO `af cron add` — create YAML files in `.af-cron/` directly.

## Other commands

```bash
af open <file>                 # Open file in annotation viewer (NOT system open)
af shell                       # Spawn utility shell
af attach                      # Attach to running builder terminal
af rename <name>               # Rename current shell session
af architect                   # Start architect session in current terminal
```
