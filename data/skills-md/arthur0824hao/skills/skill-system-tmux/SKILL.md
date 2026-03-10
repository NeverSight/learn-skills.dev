---
name: skill-system-tmux
description: "Tmux execution support for long-running and persistent commands. Load this skill when you need to: (1) run commands expected to exceed tool timeout (over 60s), (2) start persistent servers or dev processes, (3) run TUI/interactive applications, (4) execute parallel isolated tasks in separate sessions, (5) run remote commands over SSH that must survive disconnection. Trigger phrases: 'run in background', 'start server', 'long-running', 'tmux session', 'keep running', 'persistent process', 'dev server', 'training script', 'git clone large repo', 'docker build'."
license: MIT
metadata:
  os: linux, macos
---

# Skill System Tmux

Route shell commands through tmux when they risk timeout, require persistence, or need interactive terminal access. This skill provides decision heuristics and session management conventions — not tmux tutorials.

## Decision Matrix

Use this matrix to decide: **direct bash** vs **tmux**.

| Condition | Route | Examples |
|---|---|---|
| Estimated time > 60s | tmux | `git clone <large>`, `npm install`, `docker build`, training scripts |
| Command does not self-terminate | tmux | `npm run dev`, `python app.py`, `jupyter notebook` |
| Requires TUI or interactive input | tmux | `vim`, `htop`, `pudb`, `claude` |
| Parallel isolated execution needed | tmux | Multiple agents, concurrent test suites |
| Remote execution over SSH | tmux | Commands that must survive connection drops |
| Atomic, non-interactive, fast (<30s) | direct bash | `ls`, `grep`, `git status`, `cat`, `mkdir` |
| Single-shot with expected output | direct bash | `python script.py` (fast), `git diff`, `npm test` (short) |

**Default: direct bash.** Only route to tmux when a condition above is met.

### Time Estimation Heuristics

Commands likely to exceed timeout:

- **Git operations**: `clone` (large repos), `push` (large payloads), `checkout` (>1GB working tree)
- **Package install**: `npm install`, `pip install` (many deps), `cargo build`
- **Build tools**: `docker build`, `make` (large projects), `webpack` (production builds)
- **Data processing**: Training scripts, preprocessing pipelines, large file transfers
- **CI/test suites**: Full test runs on large projects

## Session Naming Convention

Use project-context naming for human readability:

```
Format: {project}-{purpose}

Agent-created sessions (MANDATORY prefix):
  oc-{purpose}        # e.g., oc-audit, oc-verify, oc-render
  oc-{project}-{task}  # e.g., oc-skills-build, oc-subproject-test

User/infra sessions (no prefix required):
  skills-dev-server
  frontend-tests
  ml-training
  exp_runner
```

Rules:
- **Agent-created sessions MUST use `oc-` prefix** — enables bulk identification and cleanup
- Lowercase, hyphens for separators (not underscores)
- Include project context for multi-project environments
- Reuse well-known session names when they exist (e.g., `exp_runner`)
- Never create sessions with numeric-only names (e.g., `531`)

## Core Patterns

### Pattern 1: Fire and Forget (Background Task)

For long-running commands where you don't need real-time output:

```bash
# Kill any existing session with same name, then start fresh
tmux kill-session -t {session} 2>/dev/null || true
tmux new-session -d -s {session} bash -c '{command}'
```

Using `interactive_bash` tool:
```
tmux_command: new-session -d -s {session}
tmux_command: send-keys -t {session} "{command}" Enter
```

### Pattern 2: Persistent Server

For dev servers or processes that must keep running:

```
tmux_command: new-session -d -s {session}
tmux_command: send-keys -t {session} "{command}" Enter
```

Check if running later:
```
tmux_command: has-session -t {session}
```

### Pattern 3: Output Capture

Read what a tmux session has produced:

```
tmux_command: capture-pane -p -t {session}
```

For longer history (last 1000 lines):
```
tmux_command: capture-pane -p -t {session} -S -1000
```

### Pattern 4: Readiness Detection

After sending a command, poll to detect completion:

1. Capture the pane output
2. Look for shell prompt at end of output (regex: `/(\\$|>|#)\s*$/m`)
3. If prompt appears, command has finished
4. If no prompt after expected duration, assume still running or hung

### Pattern 5: Clean Shutdown

Always clean up sessions when done:

```
tmux_command: kill-session -t {session}
```

**Kill-before-new pattern** prevents zombie sessions:
```
tmux_command: kill-session -t {session}
# (ignore error if doesn't exist)
tmux_command: new-session -d -s {session}
```

### Pattern 6: Bulk Resource Reclaim

Reclaim all agent-created sessions and detect stale resources. Run this when:
- Machine feels sluggish or memory is high
- Before/after long agent work sessions
- User requests cleanup

**Step 1: Identify agent sessions**
```bash
tmux list-sessions -F '#{session_name} #{session_activity}' | grep '^oc-'
```

**Step 2: Kill all agent sessions**
```bash
tmux list-sessions -F '#{session_name}' | grep '^oc-' | xargs -I{} tmux kill-session -t {}
```

**Step 3: Detect stale non-agent sessions**

A session is likely stale if:
- Last activity > 6 hours ago AND no running foreground process
- Session has only an idle shell prompt (capture-pane shows just `$` or `╰─`)

```bash
# List sessions with last activity timestamp
tmux list-sessions -F '#{session_name} #{session_activity}'
# Compare #{session_activity} (epoch) against current time
# Capture pane of suspects to verify idle state
```

**Step 4: Reclaim orphaned processes**
```bash
# Find opencode processes whose parent tmux pane was killed
ps aux | grep opencode | grep -v grep
# Check if port is held by a zombie
lsof -i :{port} 2>/dev/null
# Force kill if needed (SIGTERM first, SIGKILL if unresponsive after 5s)
kill {pid} && sleep 5 && kill -0 {pid} 2>/dev/null && kill -9 {pid}
```

**Important**: Never kill sessions matching known infra patterns (`exp_runner`, `manager`, `preprocess`, `watcher`, `unified`) without explicit user confirmation.

## Integration with Agent Tools

### `interactive_bash` Tool

The primary interface. Pass tmux subcommands directly (without `tmux` prefix):

```
# Create session
tmux_command: new-session -d -s my-session

# Send command
tmux_command: send-keys -t my-session "npm run dev" Enter

# Read output
tmux_command: capture-pane -p -t my-session

# Kill session
tmux_command: kill-session -t my-session
```

### `bash` Tool with Timeout

For commands near the timeout boundary, prefer increasing `timeout` parameter over tmux:

```
bash(command="npm install", timeout=300000)  # 5 min timeout
```

Use tmux only when:
- Timeout cannot be reliably estimated
- Process must persist beyond the current tool call
- Interactive/TUI access is needed

## Anti-Patterns

| Don't | Do Instead |
|---|---|
| Route every command through tmux | Use direct bash for fast, atomic commands |
| Forget to kill sessions after use | Always clean up with `kill-session` |
| Use generic session names like `s1` | Use descriptive names: `project-purpose` |
| Create agent sessions without `oc-` prefix | Always prefix: `oc-audit`, `oc-verify`, `oc-build` |
| Poll capture-pane in tight loops | Use 1-2s intervals between polls |
| Start a new session without killing old one | Always kill-before-new for same session name |
| Send commands without clearing the line first | Send `C-u` before commands if line might have residual input |
| Leave sessions running after task completes | Run bulk reclaim (Pattern 6) at session end |

## Existing Project Conventions

This skill system's sibling projects use these established patterns:

- **Session name `exp_runner`**: Used for experiment execution (training, evaluation loops)
- **Watcher sessions**: Background monitors that wake agents via `tmux send-keys`
- **`machines.json` config**: `tmux_session` field defines per-machine session names
- **Kill-before-new**: Standard cleanup pattern used across all experiment scripts

When working in a project with existing tmux conventions, follow them. This skill provides defaults for projects without conventions.

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-tmux",
  "version": "1.0.0",
  "capabilities": ["tmux-route", "tmux-session-manage", "tmux-capture", "tmux-reclaim"],
  "effects": ["proc.exec"],
  "operations": {
    "route-command": {
      "description": "Decide whether a command should use direct bash or tmux, and execute accordingly.",
      "input": {
        "command": { "type": "string", "required": true, "description": "The shell command to execute" },
        "estimated_duration": { "type": "string", "required": false, "description": "Estimated duration: short (<30s), medium (30-120s), long (>120s)" }
      },
      "output": {
        "description": "Execution result or session name for tmux-routed commands",
        "fields": { "route": "string", "session": "string", "result": "string" }
      },
      "entrypoints": {
        "agent": "Apply decision matrix from SKILL.md, then execute via bash or interactive_bash"
      }
    },
    "manage-session": {
      "description": "Create, list, kill, or check tmux sessions.",
      "input": {
        "action": { "type": "string", "required": true, "description": "Action: create, kill, list, check, capture" },
        "session_name": { "type": "string", "required": false, "description": "Target session name" }
      },
      "output": {
        "description": "Session status or captured output",
        "fields": { "status": "string", "output": "string" }
      },
      "entrypoints": {
        "agent": "Use interactive_bash with appropriate tmux subcommand"
      }
    },
    "reclaim-resources": {
      "description": "Bulk cleanup of stale agent tmux sessions and orphaned processes. Kills all oc-* sessions, detects idle non-agent sessions, and reclaims zombie processes holding ports.",
      "input": {
        "scope": { "type": "string", "required": false, "description": "Scope: agent-only (default, kills oc-* only), all-stale (includes idle non-agent sessions with user confirmation)" }
      },
      "output": {
        "description": "Summary of killed sessions and processes",
        "fields": { "sessions_killed": "array", "processes_killed": "array", "ports_freed": "array" }
      },
      "entrypoints": {
        "agent": "Follow Pattern 6 (Bulk Resource Reclaim) in SKILL.md"
      }
    }
  },
  "stdout_contract": {
    "last_line_json": false,
    "note": "Agent-executed; uses interactive_bash tool for tmux operations."
  }
}
```
