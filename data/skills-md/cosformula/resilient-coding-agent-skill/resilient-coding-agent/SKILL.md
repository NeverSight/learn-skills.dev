---
name: resilient-coding-agent
description: "Run long-running coding agents (Codex, Claude Code, etc.) in tmux sessions that survive orchestrator restarts, with automatic resume on interruption."
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: [tmux]
      anyBins: [codex, claude, opencode, pi]
---

# Resilient Coding Agent

Long-running coding agent tasks (Codex CLI, Claude Code, OpenCode, Pi) are vulnerable to interruption: orchestrator restarts, process crashes, network drops. This skill decouples the coding agent process from the orchestrator using tmux, and leverages agent-native session resume for recovery.

**Placeholders:** `<task-name>` and `<project-dir>` are filled in by the orchestrator. `<task-name>` must match `[a-z0-9-]` only. `<project-dir>` must be a valid existing directory.

**Temp directory:** Each task uses a secure temp directory created with `mktemp -d`. Store this path as `<tmpdir>` and use it for all task files (prompt, events, session ID, done marker). This avoids predictable filenames and symlink/race conditions. Example: `TMPDIR=$(mktemp -d)` produces something like `/var/folders/xx/.../T/tmp.aBcDeFgH`.

**Prompt safety:** Task prompts are never interpolated into shell commands. Instead, write the prompt to a temp file using the orchestrator's `write` tool (no shell involved), then reference it with `"$(cat $TMPDIR/prompt)"` inside the tmux command. The shell treats command substitution output inside double quotes as a single literal argument, preventing injection. This depends on the orchestrator's `write` tool not invoking a shell; OpenClaw's built-in `write` tool meets this requirement.

**Sensitive output:** tmux scrollback and event log files may contain secrets or API keys from agent output. On shared machines, restrict file permissions (`chmod 600`) and clean up temp directories after task completion.

## Prerequisites

This skill assumes the orchestrator is already configured to use coding agent CLIs (Codex, Claude Code, etc.) for coding tasks instead of native sessions. If the orchestrator is still using `sessions_spawn` for coding work, configure it to prefer coding agents first (e.g., via AGENTS.md or equivalent). See the `coding-agent` skill for setup.

## When to Use This

Use this pattern when:
- The task is expected to take **more than 5 minutes**
- The orchestrator might restart during execution
- You want fire-and-forget execution with completion notification

For quick tasks under 5 minutes, running the agent directly is fine.

## Start a Task

Create a tmux session with a descriptive name. Use the agent prefix (`codex-`, `claude-`, etc.) for easy identification.

### Codex CLI

```bash
# Step 1: Create secure temp directory
TMPDIR=$(mktemp -d)
chmod 700 "$TMPDIR"

# Step 2: Write prompt to file (use orchestrator's write tool, not echo/shell)
# File: $TMPDIR/prompt

# Step 3: Launch in tmux (pass TMPDIR via env)
tmux new-session -d -s codex-<task-name> -e "TASK_TMPDIR=$TMPDIR"
tmux send-keys -t codex-<task-name> 'cd <project-dir> && set -o pipefail && codex exec --full-auto --json "$(cat $TASK_TMPDIR/prompt)" | tee $TASK_TMPDIR/events.jsonl && echo "__TASK_DONE__"' Enter

# Step 4: Capture this task's Codex session ID; resume --last is unsafe with concurrent tasks.
# Uses jq for reliable JSON parsing (falls back to grep if jq unavailable).
until [ -s "$TMPDIR/codex-session-id" ]; do
  if command -v jq &>/dev/null; then
    jq -r 'select(.thread_id) | .thread_id' "$TMPDIR/events.jsonl" 2>/dev/null | head -n 1 > "$TMPDIR/codex-session-id"
  else
    grep -oE '"thread_id":"[^"]+"' "$TMPDIR/events.jsonl" 2>/dev/null | head -n 1 | cut -d'"' -f4 > "$TMPDIR/codex-session-id"
  fi
  sleep 1
done
```

### Claude Code

```bash
# Create secure temp directory and write prompt to $TMPDIR/prompt first
TMPDIR=$(mktemp -d) && chmod 700 "$TMPDIR"
tmux new-session -d -s claude-<task-name> -e "TASK_TMPDIR=$TMPDIR"
tmux send-keys -t claude-<task-name> 'cd <project-dir> && claude -p "$(cat $TASK_TMPDIR/prompt)" && echo "__TASK_DONE__"' Enter
```

### OpenCode / Pi

```bash
# Create secure temp directory and write prompt to $TMPDIR/prompt first
TMPDIR=$(mktemp -d) && chmod 700 "$TMPDIR"

# OpenCode
tmux new-session -d -s opencode-<task-name> -e "TASK_TMPDIR=$TMPDIR"
tmux send-keys -t opencode-<task-name> 'cd <project-dir> && opencode run "$(cat $TASK_TMPDIR/prompt)" && echo "__TASK_DONE__"' Enter

# Pi (separate temp dir)
TMPDIR=$(mktemp -d) && chmod 700 "$TMPDIR"
tmux new-session -d -s pi-<task-name> -e "TASK_TMPDIR=$TMPDIR"
tmux send-keys -t pi-<task-name> 'cd <project-dir> && pi -p "$(cat $TASK_TMPDIR/prompt)" && echo "__TASK_DONE__"' Enter
```

### Completion Notification (Optional)

Chain a notification command after the agent so you know when it finishes. Use `;` before `echo "__TASK_DONE__"` so the marker prints even if the notification command fails:

```bash
# Generic: touch a marker file
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat $TASK_TMPDIR/prompt)" && touch $TASK_TMPDIR/done; echo "__TASK_DONE__"' Enter

# macOS: system notification
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat $TASK_TMPDIR/prompt)" && osascript -e "display notification \"Task done\" with title \"Codex\""; echo "__TASK_DONE__"' Enter

# OpenClaw: system event (immediate wake)
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat $TASK_TMPDIR/prompt)" && openclaw system event --text "Codex done: <task-name>" --mode now; echo "__TASK_DONE__"' Enter
```

## Monitor Progress

```bash
# Check if the session is still running
tmux has-session -t codex-<task-name> 2>/dev/null && echo "running" || echo "finished/gone"

# Read recent output (last 200 lines)
tmux capture-pane -t codex-<task-name> -p -S -200

# Read the full scrollback
tmux capture-pane -t codex-<task-name> -p -S -
```

Check progress when:
- The user asks for a status update
- You want to proactively report milestones

## Health Monitoring

For long-running tasks, use an active monitor loop instead of only checking on demand.

Periodic check flow:
1. Run `tmux has-session -t <agent-task>` to confirm the tmux session still exists.
2. Run `tmux capture-pane -t <agent-task> -p -S -<N>` to capture recent output.
3. Detect likely agent exit by checking the last `N` lines for:
   - Shell prompt returned (for example, a line ending in `$ `, `% `, or `> `)
   - Exit indicators (`exit code`, `status <non-zero>`, `exited`)
   - No completion marker (`__TASK_DONE__`)
4. If crash is detected, run the agent-native resume command in the same tmux session.

Use a done marker in your start command so the monitor can distinguish normal completion from crashes:

```bash
tmux send-keys -t codex-<task-name> 'cd <project-dir> && codex exec --full-auto "$(cat $TASK_TMPDIR/prompt)" && echo "__TASK_DONE__"' Enter
```

For Codex tasks, save the session ID to `$TMPDIR/codex-session-id` when the task starts (see **Codex CLI** above). The monitor reads that file to resume the exact task session.

The orchestrator should run this check loop periodically (every 3-5 minutes, via cron or a background timer). On consecutive failures, double the interval (3m, 6m, 12m, ...) and reset when the agent is running normally. Stop after 5 hours wall-clock.

## Recovery After Interruption

For automated crash detection and retries, use **Health Monitoring** above.
Keep this section as a manual fallback when you need to intervene directly:

```bash
# Codex (prefer explicit session ID from $TMPDIR/codex-session-id)
tmux send-keys -t codex-<task-name> 'codex exec resume <session-id> "Continue the previous task"' Enter

# Claude Code
tmux send-keys -t claude-<task-name> 'claude --resume' Enter

# OpenCode
tmux send-keys -t opencode-<task-name> 'opencode run "Continue"' Enter

# Pi: no native resume; re-run the task prompt manually
```

## Cleanup

After a task completes, kill the tmux session:

```bash
tmux kill-session -t codex-<task-name>
```

List all coding agent tmux sessions:

```bash
tmux list-sessions 2>/dev/null | grep -E '^(codex|claude|opencode|pi)-'
```

## Naming Convention

Tmux sessions use the pattern `<agent>-<task-name>`:

- `codex-refactor-auth`
- `claude-review-pr-42`
- `codex-bus-sim-physics`

Keep names short, lowercase, hyphen-separated.

## Checklist

Before starting a long task:

1. Pick tmux over direct execution (if task > 5 min)
2. Name the tmux session with the agent prefix
3. Optionally chain a completion notification
4. Tell the user: task content, tmux session name, estimated duration
5. Monitor via `tmux capture-pane` on request

## Limitations

- tmux sessions do not survive a **machine reboot** (tmux itself is killed). For reboot-resilient tasks, the coding agent's native resume (`codex exec resume <session-id>`, `claude --resume`) is the recovery path.
- Interactive approval prompts inside tmux require manual `tmux attach` or `tmux send-keys`. Use `--full-auto` / `--yolo` / `-p` flags when possible.
