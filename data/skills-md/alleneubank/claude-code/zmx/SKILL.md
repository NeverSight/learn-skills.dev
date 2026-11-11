---
name: zmx
description: Use when starting dev servers, watchers, tilt, or any process expected to outlive the conversation. Provides zmx session management patterns for long-lived processes.
---

# zmx Process Management

## Session Rules

- Check `zmx list --short` before creating sessions — duplicates cause port conflicts and confusing output
- Derive session name from `git rev-parse --show-toplevel` — hardcoded names collide when multiple agent instances run concurrently
- Use `zmx run` to send commands without attaching — `zmx attach` blocks the agent's shell and makes it unresponsive
- Use separate sessions with a common project prefix for multiple processes

One project = one session prefix. Multiple processes = multiple sessions sharing the prefix.

## Session Naming

```bash
PROJECT=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" || basename "$PWD")
```

All subsequent examples assume `PROJECT` is set. Session names follow `${PROJECT}-<role>`:
- `myapp-server`, `myapp-tests`, `myapp-tilt`

## Starting Processes

```bash
SESSION="${PROJECT}-server"

# Idempotent: skip if already running
if ! zmx list --short 2>/dev/null | grep -q "^${SESSION}$"; then
  zmx run "$SESSION" 'npm run dev'
fi
```

For multiple processes, loop over name:command pairs:

```bash
for name_cmd in "server:npm run dev" "tests:npm run test:watch"; do
  name="${name_cmd%%:*}"
  cmd="${name_cmd#*:}"
  SESSION="${PROJECT}-${name}"
  if ! zmx list --short 2>/dev/null | grep -q "^${SESSION}$"; then
    zmx run "$SESSION" "$cmd"
  fi
done
```

## Sending Commands

```bash
# Run a command in a session (creates session if needed)
zmx run "${PROJECT}-main" 'cat README.md'

# Pipe via stdin
echo "ls -lah" | zmx r "${PROJECT}-main"
```

## Monitoring Output

```bash
zmx history "${PROJECT}-server"                              # full scrollback
zmx history "${PROJECT}-server" | tail -50                   # last 50 lines
zmx history "${PROJECT}-server" | rg -i "error|fail"         # check for errors
zmx history "${PROJECT}-server" | rg -i "listening|ready"    # check for ready
```

## Waiting for Completion

```bash
zmx wait "${PROJECT}-tests"                                  # block until done
zmx wait "${PROJECT}-build" "${PROJECT}-lint"                 # wait for multiple
```

## Lifecycle

```bash
zmx list                                                     # all sessions
zmx list --short                                             # names only
zmx kill "${PROJECT}-server"                                 # kill one session

# Kill all project sessions
zmx list --short 2>/dev/null | grep "^${PROJECT}-" | while read -r s; do
  zmx kill "$s"
done
```

## Isolation

- Only kill sessions matching the current project prefix — other agent instances may have their own sessions running
- Always verify the session name before kill operations

## When to Use zmx

| Scenario | Use zmx? |
|----------|----------|
| `tilt up` | Yes, always |
| Dev server (`npm run dev`, `rails s`) | Yes |
| File watcher (`npm run watch`) | Yes |
| Test watcher (`npm run test:watch`) | Yes |
| Database server | Yes |
| One-shot build (`npm run build`) | No |
| Quick command (<10s) | No |
| Need stdout directly in conversation | No |

## Polling for Readiness

```bash
for i in {1..30}; do
  if zmx history "${PROJECT}-server" 2>/dev/null | tail -20 | rg -q "listening|ready"; then
    echo "Server ready"
    break
  fi
  sleep 1
done
```
