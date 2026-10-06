---
name: gdb
description: "Debug and trace C/C++/Rust programs with the GNU Debugger (GDB) without blocking the agent. Use when you need to set tracepoints, inspect variables, or monitor a running process while staying responsive to the user."
---

# GNU Debugger (GDB) Skill

Non-blocking GDB debugging for AI agents. Trace live processes, set conditional
breakpoints, and inspect program state while the agent stays responsive and can
multitask.

## How It Works

Agents are single-threaded — if an agent runs GDB directly and waits for a breakpoint, it **blocks entirely**. It can't respond to the user, answer questions, or change strategy until the breakpoint fires (which may take a very long time).

This skill avoids that by running GDB in the **background** via a named pipe. The agent sends commands by writing to the pipe and reads results from a log file, so it never blocks. Instead of traditional breakpoints, it uses **`dprintf`** (dynamic printf) — a GDB feature that prints formatted output when hit and **automatically continues** execution without stopping.

This means the agent can:
1.  **Start** a debug session and immediately return to the user.
2.  **Sample** the log file periodically to report progress.
3.  **Multitask** (e.g., search the web, edit code) while the target process runs.
4.  **Interrupt** and modify tracepoints dynamically without killing the session.

The skill includes helper scripts that encapsulate all the pipe management, signal handling, and quoting logic — so any agent that can run shell commands can use it.

## Core Concepts

1.  **Background Execution**: GDB runs in the background. You interact with it by writing to its standard input (stdin).
2.  **Non-Blocking**: Use `dprintf` (dynamic printf) instead of `break`. This inserts a printf call and continues execution immediately.
3.  **Log Sampling**: GDB output is redirected to a file (`set logging file ...`). You read this file to see the trace.
4.  **Dynamic Updates**: proper interrupt handling is required to add/remove tracepoints on a running process.

## Prerequisites & Setup

### Requirements
- Linux OS
- `gdb-multiarch` (recommended) or `gdb`

### Installation
```bash
# Debian/Ubuntu
sudo apt-get update && sudo apt-get install -y gdb-multiarch

# Fedora/RHEL
sudo dnf install -y gdb

# Arch
sudo pacman -S gdb

# Verify
gdb-multiarch --version || gdb --version
```

- Target process is running.
- If remote: `gdbserver` running on target.

## Workflow

### 1. Start a Session (Universal Method)

This method works with **any agent** that can run shell commands, without needing special stdin handling.

**Recommended** — use the helper script:
```bash
./scripts/gdb_start.sh ./path/to/executable
# Creates: gdb_cmd_pipe (named pipe), .gdb_pid (PID file), trace.log (output)
```

**Manual method** (if you need more control):
1.  Create a Named Pipe (FIFO):
    ```bash
    mkfifo gdb_cmd_pipe
    ```
2.  Start GDB reading from the pipe:
    ```bash
    tail -f gdb_cmd_pipe | gdb-multiarch -q -x scripts/setup.gdb --args ./executable &
    echo $! > .gdb_pid
    ```

**Interaction Protocol:**
1.  **Send Commands**: `./scripts/gdb_send.sh "command"` (or `echo "command" > gdb_cmd_pipe`)
2.  **Interrupt**: `kill -INT $(cat .gdb_pid)`
3.  **Resume**: `./scripts/gdb_send.sh "continue"`

### 2. Configure Logging (The Easy Way)

Use the provided `scripts/setup.gdb` to automatically configure non-blocking logging.

```bash
# Start GDB with the setup script
gdb-multiarch -q -x scripts/setup.gdb -p <PID>
```

If you need to configure it manually (e.g., if you forgot `-x`):
```gdb
set pagination off
set logging file trace.log
set logging enabled on
```

### 3. Set Non-Blocking Tracepoints (`dprintf`)

Use `dprintf` to print variables or status without pausing the program.

Format: `dprintf <LOCATION>, "<FORMAT_STRING>", <ARGUMENTS>`

Examples:
```gdb
dprintf main.c:120, "Iteration %d, Value: %s\n", i, some_string
dprintf process_request, "Got request ID: %d\n", req->id
```

Send `continue` to let the process run while tracing:
```gdb
continue
```

### 4. Conditional Tracing

To trace only when a condition is true, use the helper script:
```bash
./scripts/gdb_trace.sh loop_function '"Hit 10: %d\n", iteration' 'iteration == 10'
```

Or manually via the pipe:
1.  Set the `dprintf`:
    ```bash
    ./scripts/gdb_send.sh 'dprintf loop_function, "Hit 10: %d\n", iteration'
    # Output in trace.log: Dprintf 2 at ...
    ```
2.  Apply the condition. Use `$bpnum` (GDB's convenience variable for the last breakpoint number).
    **Important**: Escape the `$` so the shell doesn't expand it:
    ```bash
    ./scripts/gdb_send.sh 'condition $bpnum iteration == 10'
    ```

### 5. Sampling the Trace

Read the log file to see what's happening.
```bash
tail -n 20 trace.log
```

### 6. Modifying Tracepoints (The Interrupt Pattern)

Use the helper script to replace all tracepoints in one call:
```bash
# Replaces all existing tracepoints with a new one:
./scripts/gdb_trace.sh new_func '"New trace: %d\n", x'

# Or clear all tracepoints without setting new ones:
./scripts/gdb_trace.sh --clear
```

**Manual method** (if you need finer control):
1.  **Interrupt** — `kill -INT $(cat .gdb_pid)`
2.  **Modify** — `./scripts/gdb_send.sh "delete"` then `./scripts/gdb_send.sh 'dprintf ...'`
3.  **Resume** — `./scripts/gdb_send.sh "continue"`

## Helper Scripts

The `scripts/` directory provides helper scripts that handle quoting, timing, and PID tracking.
Use these instead of raw `echo` commands — they save tokens and avoid shell quoting errors.

| Script | Purpose | Usage |
|--------|---------|-------|
| `gdb_start.sh` | Create pipe, start GDB, save PID | `./scripts/gdb_start.sh ./my_app` |
| `gdb_send.sh` | Send a single GDB command to the pipe | `./scripts/gdb_send.sh "info breakpoints"` |
| `gdb_trace.sh` | Interrupt + delete + set dprintf + continue | `./scripts/gdb_trace.sh func '"fmt\n"' 'cond'` |
| `gdb_trace.sh --clear` | Remove all tracepoints, keep running | `./scripts/gdb_trace.sh --clear` |
| `gdb_stop.sh` | Kill processes, wait, remove session files | `./scripts/gdb_stop.sh` |

## Example Session

Here is the complete workflow using the helper scripts. These are plain shell commands
that work with **any** agent (Cursor, Claude Code, Gemini CLI, Antigravity, Aider, etc.).

### 1. Start GDB
```bash
./scripts/gdb_start.sh ./demo_app
# Output: GDB started. PID=12345, pipe=gdb_cmd_pipe, log=trace.log
```

### 2. Set a conditional tracepoint
```bash
./scripts/gdb_trace.sh loop_function '"iteration=%d\n", iteration' 'iteration == 10'
```

### 3. Run the program
```bash
./scripts/gdb_send.sh "run"
```

### 4. Sample the trace
```bash
tail -n 20 trace.log
```

### 5. Modify the tracepoint dynamically
```bash
./scripts/gdb_trace.sh loop_function '"new trace: %d\n", iteration' 'iteration == 50'
```

### 6. Clear all tracepoints (keep process running)
```bash
./scripts/gdb_trace.sh --clear
```

### 7. Stop GDB and clean up
```bash
./scripts/gdb_stop.sh
# Kills GDB + target + tail feeder, waits for exit, removes session files.
```

## Agent Compatibility

The named pipe method was designed to work with **any agent** that can execute shell commands.
It requires only three primitives: (1) write to a file, (2) send POSIX signals, (3) read a file.

| Agent | Shell Tool | Background Commands | Notes |
|-------|-----------|---------------------|-------|
| Cursor | `Shell` | `block_until_ms: 0` or `&` | Stateful shell across calls |
| Claude Code | `bash` | `&` | Stateful shell |
| Gemini CLI | Shell | `&` | Similar to Claude Code |
| Antigravity | Shell/exec | `&` | Varies by config |
| Aider | Shell | `&` | May need `--yes` for non-interactive |

**Key design choice**: The helper scripts (`gdb_start.sh`, `gdb_send.sh`, `gdb_trace.sh`) encapsulate
all quoting and timing logic, so agents don't need to reason about shell escaping or sleep intervals.
Every agent calls the same scripts the same way.

## Limitations

1.  **Linux Only**: This workflow relies on POSIX signals (`SIGINT`) and Linux process management. It will not work on Windows.
2.  **Permissions (`ptrace`)**:
    *   Attaching to a running process (`-p PID`) often requires `sudo` or adjusting `/proc/sys/kernel/yama/ptrace_scope` (set to 0).
    *   **Workaround**: Start the process *via* GDB (`--args ./exe`) to avoid this.
3.  **Signal Handling**: If the target process masks `SIGINT`, interrupting it might be difficult. You may need to use `kill -STOP` / `kill -CONT` cautiously, but that stops GDB logic too.
4.  **Blind Spots**: Since you are not seeing `stdout` in real-time (only the log file), you might miss immediate errors if you don't check the log frequently.

## Common Pitfalls

These are real issues discovered in practice. Read them before starting a session.

### 1. Conditional tracepoint on a value that already passed
If the program has a monotonically increasing counter (e.g., `iteration++`) and you set
`condition $bpnum iteration == 20` after the counter is already at 50, **the tracepoint
will never fire**. The counter will never be 20 again.

**Fix**: Before setting a conditional tracepoint on a changing value, **interrupt and inspect
the current value first**. Then pick a target value that hasn't been reached yet.

```bash
# Interrupt, check current state, then set a future target
kill -INT $(cat .gdb_pid) && sleep 1
echo "frame 3" > gdb_cmd_pipe && sleep 0.5   # navigate to the right frame
echo "print counter" > gdb_cmd_pipe && sleep 1
tail -n 5 trace.log                           # read the value
# Now set condition for a value AHEAD of where the program is
```

### 2. Cleanup race: removing the pipe before GDB exits
If you delete `gdb_cmd_pipe` before GDB has finished processing `kill`/`quit` commands sent
through that pipe, GDB and its child processes will **linger as orphans**. The pipe is gone,
so GDB can no longer read commands and the `tail -f` feeder also hangs.

**Fix**: Use `./scripts/gdb_stop.sh` which kills processes first, waits for them to die,
and only then removes session files. Never `rm` the pipe as a first step.

### 3. Commands dropped after SIGINT
After sending `kill -INT` to GDB, it needs time to stop the inferior and return to the
`(gdb)` prompt. Commands sent too soon (e.g., 0.3s later) may be silently dropped.

**Fix**: Wait at least **1 second** after SIGINT before sending the next command. The helper
scripts (`gdb_trace.sh`) already account for this.

### 4. GDB cannot process commands while the inferior is running
In all-stop mode (the default), GDB blocks on the running inferior. Commands like
`info breakpoints` sent via the pipe are **queued but not executed** until the inferior stops.

**Fix**: Always **interrupt first**, then send your query command, read the log, and then
`continue`. Example:

```bash
kill -INT $(cat .gdb_pid) && sleep 1
./scripts/gdb_send.sh "info breakpoints"
sleep 1 && tail -n 10 trace.log
./scripts/gdb_send.sh "continue"
```

### 5. Log output appears delayed
GDB's logging (`set logging enabled on`) can buffer output. After a `dprintf` fires or a
command runs, the result may not appear in `trace.log` immediately.

**Fix**: Wait **1–2 seconds** before reading the log after sending a command. Don't assume
the log is broken just because it looks stale — check again after a brief delay.

## Agent Guidance (Reducing Tool Calls)

Follow these patterns to handle common GDB tasks in fewer round-trips.

### Before setting a conditional tracepoint on a running program
If the condition depends on a **changing value** (counter, timestamp, etc.), you MUST check
the current value first to avoid setting a condition that will never fire.
Do this in **one shell call**:

```bash
kill -INT $(cat .gdb_pid) && sleep 1 \
  && echo "frame 3" > gdb_cmd_pipe && sleep 0.5 \
  && echo "print counter" > gdb_cmd_pipe && sleep 1 \
  && tail -n 5 trace.log
```

Then set the tracepoint for a value **ahead** of the current one, and continue — again
in **one call**:

```bash
./scripts/gdb_trace.sh loop_function '"trace: %d\n", iteration' 'iteration == <FUTURE_VALUE>'
```

### Setting a tracepoint and immediately running
When the program hasn't been started yet (`run` not called), you can set the tracepoint
and run in **one call** since there's nothing to interrupt:

```bash
./scripts/gdb_trace.sh loop_function '"iteration=%d\n", iteration' 'iteration == 10' \
  && ./scripts/gdb_send.sh "run"
```

### Sampling the log after a tracepoint
Don't check the log immediately — give the program time to reach the tracepoint.
Estimate the wait from the loop interval and current position, then **combine the wait
and the read into one call**:

```bash
sleep 5 && tail -n 20 trace.log
```

### Inspecting state (interrupt + query + resume)
Batch all three steps into a **single shell call**:

```bash
kill -INT $(cat .gdb_pid) && sleep 1 \
  && ./scripts/gdb_send.sh "info breakpoints" \
  && sleep 1 && tail -n 15 trace.log \
  && ./scripts/gdb_send.sh "continue"
```

### Shutdown and cleanup
Always use the dedicated stop script — **one call** handles everything:

```bash
./scripts/gdb_stop.sh
```

## Best Practices

- **Use the helper scripts** instead of raw `echo` commands. They handle quoting, timing, and PID tracking.
- **Always use `gdb-multiarch`** if available (auto-detected by `gdb_start.sh`).
- **Trace lightly**: High-frequency tracepoints (e.g., inside tight loops) will slow down execution significantly.
- **Avoid blocking commands**: Never issue a GDB command that waits for user input (like `command` without `end`) unless you are sure you can provide it.
- **Check `trace.log` frequently**: Since stdout isn't visible in real-time, the log is your only window into the process.
- **Clean up with `gdb_stop.sh`**: Always use the stop script instead of manually removing files. It kills processes first, avoiding orphaned GDB/tail processes.
