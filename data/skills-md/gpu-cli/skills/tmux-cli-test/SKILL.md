---
name: tmux-cli-test
description: Test CLI applications interactively using tmux sessions. Use when testing TUI apps (ratatui dashboard, interactive prompts), verifying CLI command output, testing keyboard navigation, or validating terminal rendering. Launches commands in tmux, waits on conditions (never sleeps), captures frames, sends keypresses, and asserts on output. Specifically designed for gpu-cli but works with any CLI. Use this skill when asked to test, verify, or QA any terminal-based UI or CLI command flow.
---

# tmux CLI Testing

Test CLI applications by running them in tmux sessions, waiting for conditions, sending input, and asserting on output. Never sleep - always wait on a condition.

## Helpers

Source the helper script for all primitives:

```bash
source .claude/skills/tmux-cli-test/scripts/tmux_helpers.sh
```

### Quick Reference

| Function | Purpose |
|----------|---------|
| `tmux_start <session> <cmd>` | Launch command in detached tmux session |
| `tmux_kill <session>` | Kill session |
| `tmux_is_alive <session>` | Check if session is running |
| `tmux_capture <session>` | Get pane text |
| `tmux_capture_ansi <session>` | Get pane text with ANSI codes |
| `tmux_wait_for <session> <text> [timeout]` | Poll until text appears |
| `tmux_wait_for_regex <session> <pattern> [timeout]` | Poll until regex matches |
| `tmux_wait_gone <session> <text> [timeout]` | Poll until text disappears |
| `tmux_wait_exit <session> [timeout]` | Poll until process exits |
| `tmux_send <session> <keys...>` | Send keys (tmux key names) |
| `tmux_type <session> <text>` | Type literal text |
| `tmux_assert_contains <session> <text> [label]` | Assert text present |
| `tmux_assert_not_contains <session> <text> [label]` | Assert text absent |
| `tmux_assert_matches <session> <pattern> [label]` | Assert regex matches |
| `tmux_send_and_wait <session> <keys> <text> [timeout]` | Send then wait |
| `tmux_test <session> <cmd> <ready_text> <fn>` | Full lifecycle test |

### Configuration

Override defaults before calling functions:

```bash
TMUX_TEST_POLL_INTERVAL=0.3  # seconds between polls
TMUX_TEST_TIMEOUT=30         # max wait seconds
TMUX_TEST_WIDTH=120          # terminal columns
TMUX_TEST_HEIGHT=30          # terminal rows
```

## Workflow

Every test follows this pattern:

```
1. Start session with command
2. Wait for ready signal (text appearing)
3. Interact (send keys, wait for responses)
4. Assert on captured output
5. Kill session
```

### Minimal Example

```bash
source .claude/skills/tmux-cli-test/scripts/tmux_helpers.sh

tmux_start "test-help" "./crates/target/debug/gpu --help"
tmux_wait_for "test-help" "Usage:" 10
tmux_assert_contains "test-help" "run"
tmux_assert_contains "test-help" "dashboard"
tmux_kill "test-help"
```

### Using tmux_test for Lifecycle

```bash
test_help_page() {
    local s="$1"
    tmux_assert_contains "$s" "run" "help shows run command"
    tmux_assert_contains "$s" "dashboard" "help shows dashboard command"
    tmux_assert_not_contains "$s" "ERROR" "no errors in help"
}

tmux_test "help-test" "./crates/target/debug/gpu --help" "Usage:" test_help_page
```

## GPU CLI Patterns

### Testing the Dashboard (TUI)

```bash
source .claude/skills/tmux-cli-test/scripts/tmux_helpers.sh
TMUX_TEST_WIDTH=140
TMUX_TEST_HEIGHT=35

GPU_BIN="./crates/target/debug/gpu"

tmux_start "dash" "$GPU_BIN dashboard"
tmux_wait_for "dash" "Pods" 15

# Verify panels rendered
tmux_assert_contains "dash" "Pods" "pods panel visible"
tmux_assert_contains "dash" "Jobs" "jobs panel visible"

# Navigate with keys
tmux_send "dash" j
tmux_send "dash" j
tmux_wait_for "dash" "▶" 5  # selection cursor

# Switch panel
tmux_send "dash" Tab
tmux_wait_for_regex "dash" "Jobs.*selected" 5

# Open help overlay
tmux_send "dash" '?'
tmux_wait_for "dash" "Help" 5
tmux_assert_contains "dash" "Keybindings" "help shows keybindings"

# Close help
tmux_send "dash" Escape
tmux_wait_gone "dash" "Keybindings" 5

# Quit
tmux_send "dash" q
tmux_wait_exit "dash" 5
```

### Testing Interactive Prompts

```bash
tmux_start "init" "$GPU_BIN init"
tmux_wait_for "init" "project" 10

# Type project name
tmux_type "init" "my-test-project"
tmux_send "init" Enter

# Wait for next prompt
tmux_wait_for "init" "GPU" 10

# Select GPU with arrow keys
tmux_send "init" j j Enter
tmux_wait_for "init" "provider" 10

tmux_kill "init"
```

### Testing Command Output

```bash
tmux_start "status" "$GPU_BIN status"
tmux_wait_for_regex "status" "(No active|Pod)" 10

FRAME=$(tmux_capture "status")
if echo "$FRAME" | grep -q "No active"; then
    echo "No pods running - expected for cold test"
elif echo "$FRAME" | grep -q "Pod"; then
    tmux_assert_matches "status" "Pod.*READY\|ACTIVE" "pod in valid state"
fi

tmux_wait_exit "status" 15
```

### Testing Error Handling

```bash
tmux_start "bad-cmd" "$GPU_BIN run --nonexistent-flag"
tmux_wait_for_regex "bad-cmd" "error|Error|unknown" 10
tmux_assert_not_contains "bad-cmd" "panic" "no panics on bad input"
tmux_wait_exit "bad-cmd" 5
```

### Testing Long-Running Commands with Ctrl-C

```bash
tmux_start "run-job" "$GPU_BIN run python -c 'import time; time.sleep(3600)'"
tmux_wait_for "run-job" "Running" 30

# Interrupt
tmux_send "run-job" C-c
tmux_wait_for_regex "run-job" "cancel|interrupt|stopped" 10
tmux_wait_exit "run-job" 10
```

## Docker Containers

For testing CLI apps running inside Docker containers (e.g., FTR testing), source the Docker helpers:

```bash
source .claude/skills/tmux-cli-test/scripts/tmux_docker_helpers.sh
TMUX_DOCKER_CONTAINER="gpu-ftr-alex-chen-001"
# TMUX_DOCKER_SESSION="test"  # default, override if needed
```

Set `TMUX_DOCKER_CONTAINER` once, then all `docker_tmux_*` calls route through `docker exec` to that container. Same API as the local helpers but without session/container args:

| Function | Purpose |
|----------|---------|
| `docker_tmux_send <keys...>` | Send tmux keys |
| `docker_tmux_type <text>` | Type literal text |
| `docker_tmux_capture` | Get pane text |
| `docker_tmux_capture_ansi` | Get pane text with ANSI codes |
| `docker_tmux_wait_for <text> [timeout]` | Poll until text appears |
| `docker_tmux_wait_regex <pattern> [timeout]` | Poll until regex matches |
| `docker_tmux_wait_gone <text> [timeout]` | Poll until text disappears |
| `docker_tmux_assert_contains <text> [label]` | Assert text present |
| `docker_tmux_assert_not_contains <text> [label]` | Assert text absent |
| `docker_tmux_assert_matches <pattern> [label]` | Assert regex matches |
| `docker_tmux_send_and_wait <keys> <text> [timeout]` | Send then wait |

### Docker Example

```bash
source .claude/skills/tmux-cli-test/scripts/tmux_docker_helpers.sh
TMUX_DOCKER_CONTAINER="gpu-ftr-alex-chen-001"

docker_tmux_send "gpu dashboard" Enter
docker_tmux_wait_for "Pods" 15
docker_tmux_capture
docker_tmux_send j
docker_tmux_send "?"
docker_tmux_wait_for "Help" 5
docker_tmux_assert_contains "Keybindings" "help shows keybindings"
docker_tmux_send Escape
docker_tmux_wait_gone "Help" 5
docker_tmux_send q
```

## Writing Tests Inline

When no helper script is needed (quick one-off checks), use tmux commands directly:

```bash
# Start
tmux new-session -d -s test -x 120 -y 30 "./crates/target/debug/gpu dashboard"

# Poll for ready (inline wait loop)
for i in $(seq 1 100); do
    tmux capture-pane -t test -p | grep -q "Pods" && break
    sleep 0.3
done

# Assert
FRAME=$(tmux capture-pane -t test -p)
echo "$FRAME" | grep -q "Pods" && echo "PASS" || echo "FAIL"

# Cleanup
tmux send-keys -t test q
tmux kill-session -t test 2>/dev/null
```

## Anti-Patterns

| Bad | Good | Why |
|-----|------|-----|
| `sleep 3` | `tmux_wait_for s "Ready"` | Sleeps are flaky and slow |
| `sleep 5 && tmux capture-pane` | `tmux_wait_for s "expected" && tmux_capture s` | Condition, not duration |
| Hardcoded binary path | `GPU_BIN=./crates/target/debug/gpu` | Easy to switch debug/release |
| No cleanup on failure | `tmux_test` or explicit `tmux_kill` | Leftover sessions break next run |
| `grep -q` without timeout loop | `tmux_wait_for` | Text may not be rendered yet |
| Checking `.len()` of TUI text | Check display content only | Unicode width != byte length |

## Debugging Failed Tests

When a test fails, capture the frame for diagnosis:

```bash
# Capture what's actually on screen
tmux_capture "session-name"

# Save to file for comparison
tmux_capture_to_file "session-name" "/tmp/failed-frame.txt"

# Capture with colors to verify styling
tmux_capture_ansi "session-name"
```

## Session Naming Convention

Use descriptive, prefixed session names to avoid collisions:

```
gpu-test-dashboard
gpu-test-init
gpu-test-run-basic
gpu-test-status
gpu-test-error-handling
```
