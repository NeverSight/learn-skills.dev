---
name: cc-use
description: >
  Supervise and manage an inner Claude Code instance running in tmux.
  Use this skill when you need to delegate implementation work to an inner Claude
  while focusing on task planning, progress monitoring, and end-to-end acceptance testing.
  Ideal for long-running tasks that would otherwise exhaust a single Claude's context window.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
---

# cc-use: Claude Code Supervisor Skill

You are an **outer Claude** acting as a supervisor. You delegate implementation work to an **inner Claude** running inside a tmux session, while you focus on planning, monitoring, and verification.

## Why This Exists

A single Claude session accumulates all file reads, edits, command outputs, and debugging iterations in its context window. A typical bug fix might consume 50k+ tokens on implementation details alone. This skill offloads that work to an inner Claude, so:

- **Inner Claude**: handles implementation details (reads files, writes code, runs tests). Its context fills up with code-level details, and can be restarted fresh when needed.
- **Outer Claude (you)**: only sees high-level status summaries. Your context grows slowly, enabling you to manage much longer workflows.

### Context isolation principle

Inner Claude's tool calls (Read, Edit, Bash outputs) **never enter your context**. You monitor via screen-diff: comparing tmux snapshots and only seeing incremental changes. A monitoring cycle that waits 5 minutes typically adds only ~20-50 tokens to your context.

When the inner Claude's context fills up, you restart it with a fresh session and re-send a brief task prompt. The inner Claude picks up where it left off with a clean window. This makes the overall workflow length **no longer bounded by context limits**.

### Your role

Think of yourself as a **tech lead**, not an implementer:
- You define goals, design task prompts, set constraints
- You monitor progress without micromanaging
- You verify results like a real user (black-box, end-to-end)
- You manage environment, context lifecycle, and coordination
- You do NOT read source code, edit files, or debug — that's inner Claude's job

## Helper Scripts

All tmux operations are provided via a dispatcher script at `.cc-use/cc` (symlinked during Phase 1 init).

Call commands as `.cc-use/cc <command> [args...]`:

| Command | Purpose |
|---------|---------|
| `.cc-use/cc launch <session> <project_dir> <state_dir> [perm_flags]` | Create tmux session and start claude |
| `.cc-use/cc stop <session>` | Gracefully exit claude and kill session |
| `.cc-use/cc restart <session> [perm_flags]` | Restart claude (for config changes), restores window size |
| `.cc-use/cc send <session> "prompt text"` | Send prompt (flattened to single line), handles long text |
| `.cc-use/cc send_file <session> <file>` | Send prompt from file |
| `.cc-use/cc cmd <session> "/command"` | Send a slash command |
| `.cc-use/cc glance <session> [lines]` | Quick screen capture from bottom (default 40 lines) |
| `.cc-use/cc scroll <session> <page> [page_size]` | Page through scrollback: page 0=bottom, 1=one page up, etc. (default 30 lines/page) |
| `.cc-use/cc read_conversation <project_dir> [last_n]` | Read last N complete assistant messages from JSONL transcript (Tier 3) |
| `.cc-use/cc read_tools <project_dir> [last_n]` | Show tool calls + text summary for last N messages (quick activity overview) |
| `.cc-use/cc watch <session> <state_dir> [...]` | Full monitoring: outputs incremental diffs + Tier 0. Use after sending a task |
| `.cc-use/cc watch <session>` | Quiet mode: just waits for idle, outputs only "IDLE after Xs". Use for startup/menu wait |
| `.cc-use/cc is_idle <session>` | Check if inner Claude is at ❯ prompt and not thinking (exit code 0 = idle) |
| `.cc-use/cc wait_shell <session> [max_iter]` | Wait for claude to exit to shell |
| `.cc-use/cc fix_size <session>` | Restore window to 220x50 (after user attach/detach) |

## Directory Structure

You operate from the `.cc-use/` directory inside the user's project:

```
my-project/
├── .cc-use/                          # Your working directory
│   └── state/
│       ├── session-info.json         # tmux session config and permission mode
│       ├── last-screen.txt           # Last captured tmux screen (for diff monitoring)
│       └── env-changes.md            # Track environment modifications for rollback
├── CLAUDE.md                         # Project's own instructions (for inner Claude)
└── (project files...)
```

## Workflow

### Phase 1: Initialize

1. **First-time setup**: Ask the user which permission mode to use for the inner Claude:
   - `--dangerously-skip-permissions` (fully autonomous, only in isolated environments)
   - Default mode (inner Claude will pause for permission prompts; user must approve in tmux)
   - `--allowedTools "Tool1" "Tool2"` (whitelist specific tools)

2. **Create state directory, derive session name, and set up dispatcher**:
   ```bash
   mkdir -p .cc-use/state
   ln -sf "${CLAUDE_SKILL_DIR}/scripts/cc-use" .cc-use/cc
   project_dir="$(cd .. && pwd)"
   session_name="cc-use-$(basename "$project_dir")"
   ```
   Write `session-info.json` with the session name, permission mode, and project path.

3. **Understand the project**: Read `../CLAUDE.md` if it exists, but remember — that file contains instructions for the inner Claude's development work, not directives for you.

### Phase 2: Launch Inner Claude

```bash
.cc-use/cc launch "$session_name" "$project_dir" "$(pwd)/state" "--dangerously-skip-permissions"
```

Wait for Claude to be ready, then send the task prompt:
```bash
.cc-use/cc watch "$session_name" && .cc-use/cc send "$session_name" "Your task description here"
```

For long prompts, write to a file first:
```bash
cat > /tmp/cc-use-prompt.txt <<'PROMPT'
## Task: Fix the auth bug
### Goal
...
PROMPT
.cc-use/cc send_file "$session_name" /tmp/cc-use-prompt.txt
```

### Phase 3: Monitor and Steer (Core Loop)

Repeat this cycle until the goal is achieved:

#### Step 1: Watch for inner Claude to finish

```bash
.cc-use/cc watch "$session_name" "$(pwd)/state"
```

This is a **single Bash call** that monitors via screen-diff:
- Every 10s, captures the tmux screen and compares with the previous snapshot
- **Large changes (>5 new lines)**: inner Claude is busy — stays silent, continues watching
- **Small changes (≤5 new lines)**: outputs only the new lines to you (incremental, no repeat)
- **No change for 3 consecutive checks + ❯ visible**: exits with IDLE status

**The output you receive is a concatenation of:**
1. Incremental diffs (small changes observed during monitoring)
2. A status line: `IDLE after Xs`, `STUCK after Xs`, or `TIMEOUT after Xs`
3. Tier 0: a few lines of inner Claude's actual output (UI decoration filtered out)

Note: Some incremental diffs may be Claude Code UI refreshes (progress timers, spinner changes) rather than meaningful content — this is normal noise. Typical context usage: ~20-50 tokens per cycle.

#### Step 1b: Progressive reading (expand only if needed)

`.cc-use/cc watch` already gives you Tier 0 (last 3 lines) on exit. Only expand if that's not enough:

| Tier | What | When to use | Context cost |
|------|------|-------------|-------------|
| **0** | Auto from `.cc-use/cc watch` (filtered, up to 8 lines) | Always — shows inner Claude's last response summary | ~10 tokens |
| **1** | `.cc-use/cc glance "$session" 10` | Need a quick summary of what happened | ~15 tokens |
| **2** | `.cc-use/cc scroll "$session" 0` then `1`, `2`... | Scroll up page by page (30 lines each, no overlap) | ~45 tokens/page |
| **3** | `.cc-use/cc read_conversation "$project_dir"` or `.cc-use/cc read_tools "$project_dir"` | Need full assistant response or activity overview (JSONL parsing) | varies |

**Tier 2 example — scrolling up like a human:**
```bash
.cc-use/cc scroll "$session" 0     # page 0: most recent 30 lines
# not enough? scroll up:
.cc-use/cc scroll "$session" 1     # page 1: previous 30 lines (no overlap with page 0)
.cc-use/cc scroll "$session" 2     # page 2: even further back
```

**Rule: start from Tier 0, only go deeper if information is insufficient.** Most monitoring cycles only need Tier 0 or 1.

#### Step 2: Decide next action

| Situation | Action |
|-----------|--------|
| Inner Claude completed a step successfully | Send next instruction or move to verification |
| Inner Claude is going in the wrong direction | `.cc-use/cc send "$session" "correction..."` |
| Inner Claude hit an error it can't resolve | Analyze the error, send guidance |
| A milestone is reached | Run verification yourself (tests, browser checks) |
| Inner Claude's context is getting full | `.cc-use/cc cmd "$session" "/compact focus on ..."` |
| Goal is fully achieved | Move to Phase 4 (Acceptance) |

**WARNING — Command accumulation**: Always check idle state before sending. If you send commands while inner Claude is busy, they queue and fire in rapid succession.

```bash
.cc-use/cc is_idle "$session_name" && .cc-use/cc send "$session_name" "Next instruction..."
```

### Phase 4: Acceptance Testing

**Core principle: Black-box, end-to-end testing. You are the user, not a developer.**

Verify like a real user — interact with the actual system using real data and real environments. Do NOT read source code. You MAY read documentation, README, API docs to understand expected behavior.

**4.1: Issue reproduction FIRST** (for bug fixes) — reproduce the bug end-to-end before checking the fix.

**4.2: End-to-end verification** — use real environments, real data, real interactions. Avoid mocks. Do NOT let inner Claude write code-level tests (unit tests, test scripts that import internal modules) as a substitute for real E2E testing.

**4.3: For Claude Code plugin/skill/MCP development** — you MUST test by actually using the plugin/skill/MCP through Claude Code, not by writing Node.js scripts that import internal code. See @references/acceptance-testing.md for specific methods (`--plugin-dir`, `--add-dir`, `.mcp.json`, `/mcp`, `/reload-plugins`).

**4.4: Edge case coverage** — test boundary conditions end-to-end: empty/null inputs, large inputs, invalid inputs, special characters, concurrent operations.

**4.5: Run existing test suite** (supplementary) — `pytest` / `npm test` / `cargo test` as a sanity check. Passing unit tests does NOT replace e2e verification.

See @references/acceptance-testing.md for detailed patterns and examples.

### Phase 5: Cleanup

```bash
.cc-use/cc stop "$session_name"
```

Then: report results to user, and check `.cc-use/state/env-changes.md` for any environment changes that need reverting.

## Managing Inner Claude's Context

| Command | How |
|---------|-----|
| Compress context | `.cc-use/cc cmd "$session" "/compact focus on <task>"` |
| Clear context | `.cc-use/cc cmd "$session" "/clear"` |
| Check context usage | `.cc-use/cc cmd "$session" "/context"` then `.cc-use/cc glance "$session" 20` |
| Switch model | `.cc-use/cc cmd "$session" "/model sonnet"` |
| Restart (config changed) | `.cc-use/cc restart "$session" "--dangerously-skip-permissions"` |

### What requires restart vs what doesn't:

| Change | Restart needed? |
|--------|----------------|
| Edit CLAUDE.md | No — dynamically loaded |
| Edit SKILL.md (via --add-dir) | No — hot-reloaded |
| `/reload-plugins` | No — reloads immediately |
| Add MCP server | **Yes** — `.cc-use/cc restart` |
| Change settings.json | **Yes** — `.cc-use/cc restart` |

## Delegation Discipline

**Do NOT do the inner Claude's job.** As the outer Claude, you should:

- ✅ Read inner Claude's output to understand progress
- ✅ Send instructions and corrections to inner Claude
- ✅ Read documentation, README, API docs, user guides (to understand expected behavior)
- ✅ Run end-to-end acceptance tests (real commands, browser interactions)
- ✅ Manage inner Claude's context and lifecycle
- ❌ Do NOT read project source code (let inner Claude do it)
- ❌ Do NOT edit project files directly (send instructions to inner Claude)
- ❌ Do NOT debug build errors yourself (tell inner Claude what you see)
- ❌ Do NOT configure project tooling (tell inner Claude to do it)
- ❌ Do NOT write or read unit tests / mock-based tests (that's inner Claude's domain)

**You are the user, not the developer.** During acceptance, treat the project as a black box: read its docs to understand what it should do, then verify by actually using it end-to-end with real data and real environments.

## Environment Change Tracking

Record system-level changes in `.cc-use/state/env-changes.md`. See @references/environment-management.md for format and rules.

**Always ask the user** before: installing global packages, modifying shell config, installing MCP servers, running sudo commands.

## Crafting Task Prompts for Inner Claude

Write clear, focused prompts. Include only what the inner Claude needs:

```
## Task: <name>

### Goal
<What to implement/fix — be specific about the deliverable>

### Context
<Only the background info needed for THIS task, not everything>

### Constraints
- Work within <specific directories/files>
- Do not modify <protected files>
- Use <specific tech stack/patterns>

### Done when
- <Testable completion criteria>
- <e.g., "all tests in tests/auth/ pass">
- <e.g., "the login page renders correctly at localhost:3000/login">
```

## References

For detailed guidance on specific topics, see:
- @references/tmux-operations.md — tmux commands and patterns
- @references/environment-management.md — environment tracking and rollback
- @references/acceptance-testing.md — verification strategies
- @references/cc-commands-guide.md — Claude Code slash commands reference
