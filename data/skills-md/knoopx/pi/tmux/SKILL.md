---
name: tmux
description: Manages background processes, captures command output, and handles session multiplexing. Use when running long-running commands, capturing output from detached processes, or managing concurrent tasks in headless environments.
---

# tmux

Terminal multiplexer for background processes, output capture, and session management.

## Quick Reference

| Command                               | Description                       |
| ------------------------------------- | --------------------------------- |
| `tmux new -d -s name 'cmd'`           | Run command in background session |
| `tmux capture-pane -t name -p`        | Capture output from session       |
| `tmux send-keys -t name 'text' Enter` | Send input to session             |
| `tmux kill-session -t name`           | Terminate session                 |
| `tmux ls`                             | List all sessions                 |
| `tmux has -t name`                    | Check if session exists           |

## Running Background Processes

```bash
# Run command in new detached session
tmux new-session -d -s myserver 'python -m http.server 8080'

# With specific working directory
tmux new-session -d -s build -c /path/to/project 'make build'

# Keep session alive after command completes
tmux new-session -d -s task 'command; exec bash'

# Run only if session doesn't exist
tmux has -t myserver || tmux new-session -d -s myserver 'command'
```

## Capturing Output

```bash
# Capture visible output
tmux capture-pane -t mysession -p

# Capture entire scrollback history
tmux capture-pane -t mysession -p -S -

# Capture last N lines
tmux capture-pane -t mysession -p -S -100

# Save to file
tmux capture-pane -t mysession -p > output.txt

# Capture with escape sequences (colors)
tmux capture-pane -t mysession -p -e
```

## Sending Input

```bash
# Send text and Enter
tmux send-keys -t mysession 'echo hello' Enter

# Send without Enter
tmux send-keys -t mysession 'some-text'

# Send Ctrl+C
tmux send-keys -t mysession C-c
```

## Session Management

```bash
# List sessions
tmux list-sessions
tmux ls

# Kill specific session
tmux kill-session -t myserver

# Kill all sessions
tmux kill-server

# Check if session exists
tmux has -t mysession
```

## Wait for Completion

```bash
# Signal completion from command
tmux new-session -d -s job 'command; tmux wait-for -S job-done'

# Wait for signal
tmux wait-for job-done
```

## Common Patterns

### Development Servers

```bash
tmux new-session -d -s backend 'bun run backend'
tmux new-session -d -s frontend 'bun run frontend'
tmux new-session -d -s tests 'vitest --watch'
```

### Run and Capture Output

```bash
tmux new-session -d -s job 'command'
sleep 0.5
output=$(tmux capture-pane -t job -p)
echo "$output"
```

### Conditional Session

```bash
tmux has -t myserver || tmux new-session -d -s myserver 'command'
```

### Cleanup

```bash
tmux kill-session -t backend
tmux kill-session -t frontend
tmux kill-server  # Kill all
```

## Tips

- Use `tmux new-session -d` for background processes
- Use `tmux capture-pane -p -S -` for full scrollback
- Use `tmux has -t name` to check session existence
- Use `tmux kill-server` to clean up all sessions
- Use `-c /path` to set working directory
- Use `exec bash` to keep session alive after command
