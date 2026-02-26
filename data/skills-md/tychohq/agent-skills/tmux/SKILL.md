---
name: tmux
slug: tmux-controller
version: 1.0.0
description: Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.
metadata:
  { "openclaw": { "emoji": "🧵", "os": ["darwin", "linux"], "requires": { "bins": ["tmux"] } } }
---

# tmux Skill

Use tmux only when you need an interactive TTY. Prefer exec background mode for long-running, non-interactive tasks.

## Default Server — No Custom Sockets

**Always use the default tmux server.** Do NOT use `-S` custom sockets. The user needs to `tmux attach` easily without knowing obscure socket paths.

## Session Naming

**Convention:** `oc-${project}-${feature}` (e.g. `oc-knowhere-date-range-picker`, `oc-deck-auth-flow`)

- `oc-` prefix = OpenClaw-managed, avoids collision with user sessions
- Easy to find: `tmux ls | grep oc-`

## Quickstart

```bash
SESSION=oc-myproject-feature

tmux new-session -d -s "$SESSION" -c ~/projects/myproject
tmux send-keys -t "$SESSION" 'claude --dangerously-skip-permissions' Enter
tmux capture-pane -p -J -t "$SESSION" -S -200
```

After starting a session, tell the user:

```
To monitor: tmux attach -t $SESSION
```

## Targeting panes and naming

- Target format: `session:window.pane` (defaults to `:0.0`).
- Keep names short; avoid spaces.
- Inspect: `tmux list-sessions`, `tmux list-panes -a`.

## Sending input safely

- Prefer literal sends: `tmux send-keys -t target -l -- "$cmd"`.
- Control keys: `tmux send-keys -t target C-c`.
- For interactive TUI apps like Claude Code/Codex, **do not** append `Enter` in the same
  `send-keys`. These apps may treat a fast text+Enter sequence as paste/multi-line input
  and not submit. Send text and `Enter` as separate commands with a small delay:

```bash
tmux send-keys -t target -l -- "$cmd" && sleep 0.1 && tmux send-keys -t target Enter
```

## Watching output

- Capture recent history: `tmux capture-pane -p -J -t target -S -200`.
- Attaching is OK; detach with `Ctrl+b d`.

## Spawning processes

- For python REPLs, set `PYTHON_BASIC_REPL=1` (non-basic REPL breaks send-keys flows).

## Orchestrating Coding Agents (Codex, Claude Code)

tmux excels at running multiple coding agents in parallel:

```bash
# Create sessions in different worktrees
tmux new-session -d -s oc-project-fix1 -c ~/projects/project-fix1
tmux new-session -d -s oc-project-fix2 -c ~/projects/project-fix2

# Launch agents
tmux send-keys -t oc-project-fix1 'claude --dangerously-skip-permissions' Enter
tmux send-keys -t oc-project-fix2 'codex --full-auto' Enter

# Send a prompt (text + Enter separated by delay)
tmux send-keys -t oc-project-fix1 -l -- "Fix the date picker styling." && sleep 0.1 && tmux send-keys -t oc-project-fix1 Enter

# Poll for completion (check if shell prompt returned)
for sess in oc-project-fix1 oc-project-fix2; do
  if tmux capture-pane -p -t "$sess" -S -3 | grep -q "❯"; then
    echo "$sess: DONE"
  else
    echo "$sess: Running..."
  fi
done

# Get full output
tmux capture-pane -p -t oc-project-fix1 -S -500
```

**Tips:**

- Use separate git worktrees for parallel fixes (no branch conflicts)
- `bun install` / `pnpm install` first before running agents in fresh clones
- Check for shell prompt (`❯` or `$`) to detect completion
- Codex needs `--yolo` or `--full-auto` for non-interactive fixes

## Cleanup

- Kill a session: `tmux kill-session -t "$SESSION"`.
- Kill all OpenClaw sessions: `tmux ls -F '#{session_name}' | grep '^oc-' | xargs -n1 tmux kill-session -t`.
