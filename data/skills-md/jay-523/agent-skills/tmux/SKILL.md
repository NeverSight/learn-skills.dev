---
name: tmux
description: Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.
metadata:
  { "openclaw": { "emoji": "🧵", "os": ["darwin", "linux"], "requires": { "bins": ["tmux"] } } }
---

# tmux Session Control

Control tmux sessions by sending keystrokes and reading output. Essential for managing Claude Code sessions.

## When to Use

✅ **USE this skill when:**

- Monitoring Claude/Codex sessions in tmux
- Sending input to interactive terminal applications
- Scraping output from long-running processes in tmux
- Navigating tmux panes/windows programmatically
- Checking on background work in existing sessions

## When NOT to Use

❌ **DON'T use this skill when:**

- Running one-off shell commands → use `exec` tool directly
- Starting new background processes → use `exec` with `background:true`
- Non-interactive scripts → use `exec` tool
- The process isn't in tmux
- You need to create a new tmux session → use `exec` with `tmux new-session`

## Example Sessions

| Session                 | Purpose                     |
| ----------------------- | --------------------------- |
| `shared`                | Primary interactive session |
| `worker-2` - `worker-8` | Parallel worker sessions    |

## Common Commands

### List Sessions

```bash
tmux list-sessions
tmux ls
```

### Capture Output

```bash
# Last 20 lines of pane
tmux capture-pane -t shared -p | tail -20

# Entire scrollback
tmux capture-pane -t shared -p -S -

# Specific pane in window
tmux capture-pane -t shared:0.0 -p
```

### Send Keys

```bash
# Send text (doesn't press Enter)
tmux send-keys -t shared "hello"

# Send text + Enter
tmux send-keys -t shared "y" Enter

# Send special keys
tmux send-keys -t shared Enter
tmux send-keys -t shared Escape
tmux send-keys -t shared C-c          # Ctrl+C
tmux send-keys -t shared C-d          # Ctrl+D (EOF)
tmux send-keys -t shared C-z          # Ctrl+Z (suspend)
```

### Window/Pane Navigation

```bash
# Select window
tmux select-window -t shared:0

# Select pane
tmux select-pane -t shared:0.1

# List windows
tmux list-windows -t shared
```

### Session Management

```bash
# Create new session
tmux new-session -d -s newsession

# Kill session
tmux kill-session -t sessionname

# Rename session
tmux rename-session -t old new
```

## Sending Input Safely

For interactive TUIs (Claude Code, Codex, etc.), split text and Enter into separate sends to avoid paste/multiline edge cases:

```bash
tmux send-keys -t shared -l -- "Please apply the patch in src/foo.ts"
sleep 0.1
tmux send-keys -t shared Enter
```

## Claude Code Session Patterns

### Check if Session Needs Input

```bash
# Look for prompts
tmux capture-pane -t worker-3 -p | tail -10 | grep -E "❯|Yes.*No|proceed|permission"
```

### Approve Claude Code Prompt

```bash
# Send 'y' and Enter
tmux send-keys -t worker-3 'y' Enter

# Or select numbered option
tmux send-keys -t worker-3 '2' Enter
```

### Check All Sessions Status

```bash
for s in shared worker-2 worker-3 worker-4 worker-5 worker-6 worker-7 worker-8; do
  echo "=== $s ==="
  tmux capture-pane -t $s -p 2>/dev/null | tail -5
done
```

### Send Task to Session

```bash
tmux send-keys -t worker-4 "Fix the bug in auth.js" Enter
```

## Recipes

Reusable orchestration patterns for the `/parallel` and
`/parallel-research` skills. Reference these by name instead of
duplicating tmux logic.

### Recipe: Spawn N Agents in a tmux Session

Create a session with up to 4 panes per window, tiled layout.
Validates pane count before proceeding.

```bash
SESSION="myagents"
AGENTS=("agent-1" "agent-2" "agent-3" "agent-4" "agent-5")
PANES_PER_WINDOW=4

tmux new-session -d -s "$SESSION" -x 220 -y 55

pane_index=0
for agent in "${AGENTS[@]}"; do
  window_index=$((pane_index / PANES_PER_WINDOW))
  slot=$((pane_index % PANES_PER_WINDOW))

  if [[ $slot -eq 0 && $pane_index -gt 0 ]]; then
    # New window needed
    tmux new-window -t "$SESSION"
  elif [[ $slot -gt 0 ]]; then
    # Split within current window
    tmux split-window -t "$SESSION:$window_index"
    tmux select-layout -t "$SESSION:$window_index" tiled
  fi

  # Validate pane exists before sending
  if tmux list-panes -t "$SESSION:$window_index" -F '#{pane_index}' | grep -q "^${slot}$"; then
    tmux send-keys -t "$SESSION:$window_index.$slot" "echo 'launching $agent'" Enter
  else
    echo "ERROR: pane $SESSION:$window_index.$slot does not exist"
  fi

  pane_index=$((pane_index + 1))
done

# Final validation
tmux list-windows -t "$SESSION" -F "#{window_name}: #{window_panes} panes"
```

### Recipe: Wait for All Agents to Complete

Uses `wait-for-text.sh` to poll each pane for a completion marker.
Blocks until all agents finish or time out.

```bash
WAIT="$(dirname "$0")/scripts/wait-for-text.sh"
SESSION="myagents"
TIMEOUT=600  # seconds per agent
MARKER="COMPLETE"

# Build list of all pane targets
PANES=$(tmux list-panes -s -t "$SESSION" -F '#{window_index}.#{pane_index}')

all_done=true
for pane in $PANES; do
  target="$SESSION:$pane"
  if bash "$WAIT" -t "$target" -p "$MARKER" -T "$TIMEOUT" -i 5; then
    echo "Pane $target: DONE"
  else
    echo "Pane $target: TIMED OUT or FAILED"
    all_done=false
  fi
done

$all_done && echo "All agents complete." || echo "Some agents failed."
```

### Recipe: Health-Check Running Agents

Classify each pane into one of 4 states:

| State | Meaning | Detection |
|-------|---------|-----------|
| **DONE** | Agent finished successfully | `COMPLETE` marker found in pane output |
| **WORKING** | Agent still running | Process alive, no COMPLETE, no error patterns |
| **FAILED** | Agent crashed or hit an error | Process dead without COMPLETE, OR error patterns visible (rate limit, traceback, permission denied, "I'm blocked") |
| **UNKNOWN** | Pane not accessible | Pane doesn't exist or `capture-pane` failed |

**Quick version** (inline, for one-off checks):

```bash
SESSION="myagents"

for pane in $(tmux list-panes -s -t "$SESSION" -F '#{window_index}.#{pane_index}'); do
  target="$SESSION:$pane"
  dead=$(tmux display-message -t "$target" -p '#{pane_dead}')
  text=$(tmux capture-pane -p -J -t "$target" -S -50 2>/dev/null)
  pid=$(tmux display-message -t "$target" -p '#{pane_pid}')

  if printf '%s\n' "$text" | grep -q "COMPLETE"; then
    state="DONE"
  elif [[ "$dead" == "1" ]]; then
    state="FAILED (dead)"
  elif printf '%s\n' "$text" | grep -qE "rate limit|Traceback|permission denied|I'm blocked|Error:"; then
    state="FAILED (error)"
  else
    state="WORKING"
  fi

  echo "=== $target === $state (pid $pid)"
  printf '%s\n' "$text" | grep -v '^[[:space:]]*$' | tail -1 | sed 's/^/  /'
  echo ""
done
```

**Scripted version** (full diagnostics with summary and output file checks):

```bash
# Requires: skills/tmux/scripts/diagnose-agents.sh
DIAG="$HOME/Developer/personal_projects/agent-skills/skills/tmux/scripts/diagnose-agents.sh"

# Basic: check all panes in a session
bash "$DIAG" myagents

# With output file check
bash "$DIAG" research "research-agents/*/output.md"
bash "$DIAG" parallel "worktrees/*/run/output.md"
```

The script prints a per-pane report and a summary line
(`N working, N done, N failed, N unknown`). See
`scripts/diagnose-agents.sh` for the full implementation.

### Recipe: Safe Input to Interactive Sessions

When sending text to interactive TUIs (Claude Code, Codex), use `-l`
(literal) to prevent tmux from interpreting special characters, and
split the text from Enter to avoid paste/multiline edge cases.

```bash
# -l sends the string literally (no key-name interpretation)
# sleep gives the TUI time to process the input before Enter
tmux send-keys -t shared -l -- "Please fix the bug in src/auth.ts"
sleep 0.1
tmux send-keys -t shared Enter
```

**Why `-l`?** Without it, tmux interprets words like `Enter`, `Escape`,
`C-c` as special keys. If your prompt text contains these words,
they'll be executed as keystrokes instead of typed as text.

**Why separate Enter?** Interactive TUIs may have paste detection.
Sending text + Enter in one `send-keys` call can trigger multiline
paste mode, which many TUIs handle differently from single-line input.

**Why NOT `send-keys "$(cat file)"`?** Shell expansion of file contents
through `send-keys` breaks on quotes, backticks, `$`, and newlines.
For multi-line prompts, pipe through `claude -p` instead (see
`/parallel-research` Phase 4 launcher pattern).

## Notes

- Use `capture-pane -p` to print to stdout (essential for scripting)
- `-S -` captures entire scrollback history
- Target format: `session:window.pane` (e.g., `shared:0.0`)
- Sessions persist across SSH disconnects

