---
name: coding-agent
description: >-
  Orchestrate Codex CLI and Claude Code as background assistants via tmux.
  Think of them as your team — delegate freely. Use when you want to: get a
  second opinion on your work; delegate research or context-heavy tasks; fan
  out work in parallel (map-reduce across agents); run the same instruction
  across many items; fix issues in parallel with worktrees; or build
  something end-to-end (research → plan → phased implementation → review).
  Triggers on: "run codex", "use claude on", "spawn an agent", "second
  opinion", "delegate", "fan out", "review my work", "build with agents".
allowed-tools: Bash, Read
argument-hint: "<task description>"
---

# Coding Agent

Orchestrate Codex CLI and Claude Code as background assistants via tmux.

Spawn agents liberally — if a task can be done independently by another agent, delegate it.

## Session Management

Use `remain-on-exit on` so the pane persists after the process exits — output stays capturable.

| Operation    | Command                                                  |
| ------------ | -------------------------------------------------------- |
| Start        | `tmux new-session -d -s NAME -c DIR "cmd" \; set remain-on-exit on` |
| Read output  | `tmux capture-pane -t NAME -p -S -` (full scrollback)   |
| Check status | `tmux display-message -t NAME -p '#{pane_dead}'` → `1` if exited |
| Exit code    | `tmux display-message -t NAME -p '#{pane_dead_status}'` |
| Send raw     | `tmux send-keys -t NAME "y"` (no Enter)                 |
| Send Ctrl-C  | `tmux send-keys -t NAME C-c`                            |
| Kill         | `tmux kill-session -t NAME`                              |
| List all     | `tmux list-sessions`                                     |

Use descriptive session names: `codex-auth-refactor`, `claude-fix-78`. Kill sessions after capturing output to avoid sprawl.

### Waiting for completion

All agents in this skill run as one-shot processes (`codex exec`, `claude -p`) that exit when done. Poll `pane_dead` to detect completion without wasted time:

```bash
while [ "$(tmux display-message -t NAME -p '#{pane_dead}')" != "1" ]; do sleep 1; done
# Now read: tmux capture-pane -t NAME -p -S -
# Exit code: tmux display-message -t NAME -p '#{pane_dead_status}'
```

For multi-turn conversations, prefer `resume` with an explicit session ID over keeping an interactive TUI session alive — each turn is a clean one-shot process, so the same `pane_dead` polling works every time. **Always pass the session ID explicitly** (`exec resume <ID>`, `--resume <ID>`) rather than using `--last` or `-c`, which can pick the wrong session when multiple agents run in parallel. See multi-turn examples below for how to capture and reuse the session ID.

## Codex CLI

Default model is configured in `~/.codex/config.toml`. **Requires a git repository** — use `--skip-git-repo-check` to override, or `DIR=$(mktemp -d) && git -C "$DIR" init` for scratch work.

Progress streams to stderr, final result to stdout — enables piping: `codex exec "..." | tee result.md`. Use `-` to pipe prompt from stdin: `cat spec.md | codex exec -`.

### Flags

| Flag                          | Effect                                     |
| ----------------------------- | ------------------------------------------ |
| `exec "prompt"`               | One-shot execution, exits when done        |
| `--full-auto`                 | Shortcut: `-a on-request` + `--sandbox workspace-write` (auto-approves in `exec` mode) |
| `--sandbox read-only`         | Read-only sandbox (default for `exec`). Also: `workspace-write`, `danger-full-access` |
| `--yolo`                      | No sandbox, no approvals (hidden alias for `--dangerously-bypass-approvals-and-sandbox`) |
| `--model, -m`                 | Override model for this run                |
| `--json`                      | JSONL stream of all events to stdout       |
| `-o <path>`                   | Write final message to file               |
| `--output-schema <path>`      | JSON Schema file — validates final response shape |
| `--image, -i <path>`          | Attach images to prompt (screenshots, diagrams). Repeatable |
| `--add-dir <path>`            | Grant write access to additional directories. Repeatable |
| `--skip-git-repo-check`       | Run outside a git repository               |
| `exec resume <SESSION_ID>`    | Continue an exec session by ID (pass a follow-up prompt after the ID) |

Top-level subcommands (not `exec` flags):

| Subcommand                    | Effect                                     |
| ----------------------------- | ------------------------------------------ |
| `fork <SESSION_ID>`           | Branch an interactive session into a new thread |

`--full-auto` vs `--yolo`: `--full-auto` runs in a `workspace-write` sandbox with model-driven approval — safe for most building tasks. `--yolo` removes all guardrails (no sandbox, no approvals). Prefer `--full-auto`; only use `--yolo` when the agent needs unrestricted system access (e.g., installing packages, modifying system files).

```bash
# One-shot
tmux new-session -d -s codex-task -c ~/project \
  "codex exec --full-auto 'Add error handling to API calls'" \; \
  set remain-on-exit on

# Read-only research (safe, no writes)
tmux new-session -d -s codex-research -c ~/project \
  "codex exec --sandbox read-only -o /tmp/codex-research.txt 'Analyze how auth tokens flow through this codebase'" \; \
  set remain-on-exit on

# Multi-directory access
tmux new-session -d -s codex-task -c ~/project \
  "codex exec --full-auto --add-dir ../shared-lib 'Update the API client to use the new shared auth module'" \; \
  set remain-on-exit on

# Multi-turn: extract session ID from pane, then resume with follow-up
tmux new-session -d -s codex-review -c ~/project \
  "codex exec --full-auto 'Review the auth module'" \; \
  set remain-on-exit on
# Wait, extract session ID from the pane header, then resume:
while [ "$(tmux display-message -t codex-review -p '#{pane_dead}')" != "1" ]; do sleep 1; done
SESSION_ID=$(tmux capture-pane -t codex-review -p -S - | grep "session id:" | awk '{print $NF}')
tmux kill-session -t codex-review
tmux new-session -d -s codex-review-2 -c ~/project \
  "codex exec resume --full-auto $SESSION_ID 'Now fix the issues you found'" \; \
  set remain-on-exit on

# Monitor
tmux capture-pane -t codex-task -p -S -
```

## Claude Code

### Flags

| Flag                                | Effect                             |
| ----------------------------------- | ---------------------------------- |
| `-p "prompt"`                       | Print mode — non-interactive, exits when done |
| `--allowedTools Bash Read Edit`     | Auto-approve specific tools without prompting (prefix matching: `Bash(git:*)`) |
| `--tools Bash Read Edit`            | Restrict which tools are *available* (agent cannot use unlisted tools at all) |
| `--dangerously-skip-permissions`    | Auto-approve all tool use (use with caution) |
| `--model sonnet`                    | Set model (`haiku` for cheap tasks, `opus` for complex ones, `sonnet` default) |
| `--output-format json`              | Structured output with session ID and metadata (`text`, `json`, `stream-json`) |
| `--append-system-prompt "..."`      | Add instructions while keeping default behavior |
| `--append-system-prompt-file path`  | Same, but load from file — ideal for batch patterns (write once, reuse per agent) |
| `--add-dir ../other-project`        | Add extra directories to agent's context |
| `--resume SESSION_ID`              | Continue a specific conversation by ID |
| `--no-session-persistence`          | Don't save session to disk (for throwaway agents) |

**Variadic flag gotcha:** `--allowedTools` and `--tools` are variadic — they consume all following positional arguments, including the prompt. When using them, place `--` before the prompt to terminate option parsing:

```bash
# WRONG — prompt gets swallowed as a tool name:
claude -p --allowedTools Bash Read Edit "Fix the bug"

# RIGHT — use -- to separate flags from the prompt:
claude -p --allowedTools Bash Read Edit -- "Fix the bug"

# ALSO RIGHT — pipe prompt via stdin:
echo "Fix the bug" | claude -p --allowedTools Bash Read Edit
```

`--allowedTools` vs `--tools`: `--tools` controls what's *available*. `--allowedTools` controls what's *auto-approved*. Use both for tight scoping: `--tools Bash Read --allowedTools Read` makes Bash available but still prompts, while Read is auto-approved.

Stdin is piped as context: `gh pr diff 130 | claude -p "Review this diff"`.

```bash
# One-shot (print mode)
tmux new-session -d -s claude-task -c ~/project \
  "claude -p 'Refactor the auth module'" \; \
  set remain-on-exit on

# Research with haiku
tmux new-session -d -s claude-research -c ~/project \
  "claude -p --model haiku 'Summarize how auth works in this codebase'" \; \
  set remain-on-exit on

# With allowedTools — note the -- before the prompt
tmux new-session -d -s claude-task -c ~/project \
  "claude -p --allowedTools Bash Read Edit -- 'Process src/auth/'" \; \
  set remain-on-exit on

# Batch pattern: instructions from file
tmux new-session -d -s claude-task -c ~/project \
  "claude -p --append-system-prompt-file /tmp/instructions.md 'Process src/auth/'" \; \
  set remain-on-exit on

# Multi-turn: capture session ID with --output-format json, then resume
# (Claude doesn't print session ID in its pane output, so JSON redirect is needed)
tmux new-session -d -s claude-review -c ~/project \
  "claude -p --output-format json 'Review the auth module' > /tmp/claude-review.json" \; \
  set remain-on-exit on
# Wait, extract session ID and readable result, then resume:
while [ "$(tmux display-message -t claude-review -p '#{pane_dead}')" != "1" ]; do sleep 1; done
SESSION_ID=$(jq -r '.session_id' /tmp/claude-review.json)  # requires jq
# Read the result: jq -r '.result' /tmp/claude-review.json
tmux kill-session -t claude-review
tmux new-session -d -s claude-review-2 -c ~/project \
  "claude -p --resume $SESSION_ID 'Now fix the issues you found'" \; \
  set remain-on-exit on

# Monitor
tmux capture-pane -t claude-task -p -S -
```

## Building with Coding Agents

For substantial features, tools, or scripts, use a phased pipeline. Each step is a separate agent session — you orchestrate the handoffs.

### 1. Research

Spawn an agent to investigate the problem space, explore relevant code, and gather context. Write findings to a file.

```bash
tmux new-session -d -s research -c ~/project \
  "codex exec --full-auto 'Research how auth tokens are handled in this codebase. Write findings to /tmp/research.md'" \; \
  set remain-on-exit on
```

### 2. Plan & spec

Feed the research to an agent tasked with producing a concrete plan and spec document.

```bash
tmux new-session -d -s plan -c ~/project \
  "claude -p --allowedTools Read Write -- 'Read /tmp/research.md. Create a detailed implementation plan and spec at /tmp/plan.md. Include phases, file changes per phase, and acceptance criteria.'" \; \
  set remain-on-exit on
```

### 3. Review the plan

Spawn a review agent (or use `resume` for a conversation) to challenge the plan, find gaps, and refine it.

```bash
tmux new-session -d -s plan-review -c ~/project \
  "claude -p --allowedTools Read Write -- 'Read /tmp/plan.md. Review it critically: are there gaps, risks, or missing edge cases? Update the plan with your suggestions.'" \; \
  set remain-on-exit on
```

### 4. Implement phase by phase

Split the plan into phases, then loop: **implement → review → fix → next phase**.

```bash
# Phase 1: implement
tmux new-session -d -s phase-1-impl -c ~/project \
  "codex exec --full-auto 'Read /tmp/plan.md. Implement Phase 1 only. Commit when done.'" \; \
  set remain-on-exit on

# Phase 1: review & fix
tmux new-session -d -s phase-1-review -c ~/project \
  "claude -p --allowedTools Bash Read Edit -- 'Read /tmp/plan.md. Review the Phase 1 implementation against the spec. Fix any issues. Commit when done.'" \; \
  set remain-on-exit on

# Repeat for Phase 2, 3, ...
```

### 5. Final review

Once all phases are complete, spawn a final agent to review the full implementation against the original spec.

```bash
tmux new-session -d -s final-review -c ~/project \
  "claude -p --allowedTools Bash Read -- 'Read /tmp/plan.md. Review the full implementation against this spec. Report what was completed, what diverged, and any remaining issues.'" \; \
  set remain-on-exit on
```

Wait for each step to complete before starting the next (see "Waiting for completion" above). Read results with `tmux capture-pane -t NAME -p -S -`.

## Parallel Issue Fixing

Use git worktrees to fix multiple issues concurrently:

```bash
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# --yolo here because pnpm install needs system writes outside the workspace sandbox.
# Use --full-auto when the task only needs workspace writes.
tmux new-session -d -s fix-78 -c /tmp/issue-78 \
  "pnpm install && codex exec --yolo 'Fix issue #78: <desc>. Commit and push.'" \; \
  set remain-on-exit on
tmux new-session -d -s fix-99 -c /tmp/issue-99 \
  "pnpm install && codex exec --yolo 'Fix issue #99: <desc>. Commit and push.'" \; \
  set remain-on-exit on

# After completion: push branches, create PRs, remove worktrees
```

## Rules

1. **Respect tool choice.** Use the agent the user asks for. Do not silently substitute your own edits when an agent fails — respawn or ask the user.
2. **Use `--full-auto` for building, vanilla for reviewing.** No approval flags needed for code review.

## Progress Updates

When spawning background agents, keep the user informed:

- 1 short message at launch (what's running, where).
- Update only on state changes: milestone reached, agent needs input, error hit, or agent finished.
- If you kill a session, say so immediately with the reason.
