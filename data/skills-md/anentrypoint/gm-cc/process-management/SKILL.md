---
name: process-management
description: >-
  PM2 process management for all running applications. Enforces: pre-check for
  running processes before start, watch enabled, autorestart disabled, lifecycle
  cleanup when done. Use for all servers, workers, agents, background processes.
  Triggers: start server, run application, background process, pm2, keep alive,
  process manager, daemon, monitor logs.
---

# Process Management — PM2

All applications MUST run through PM2. Direct invocations (node, bun, python) are forbidden for any process that produces output or has a lifecycle.

## Installation (First Time Only)

Check if PM2 is installed:

```bash
pm2 --version
```

If command not found, install globally:

```bash
npm install -g pm2
```

Verify installation:

```bash
pm2 --version        # should print version number
pm2 ping             # should respond "pong"
```

## Pre-Start Check (MANDATORY)

Before starting any process, check what is already running:

```bash
pm2 jlist
```

- `online` → already running, use `pm2 logs <name>` to observe
- `stopped` → use `pm2 restart <name>`
- Not in list → proceed to start

Never start a duplicate process. Always check first.

## Start a Process

```bash
# CLI (quick)
pm2 start app.js --name myapp --watch --no-autorestart

# With interpreter
pm2 start script.py --interpreter python3 --name worker --watch --no-autorestart

# From ecosystem config (preferred for reproducibility)
pm2 start ecosystem.config.cjs
```

## Ecosystem Config (Standard Template)

`autorestart: false` — process stops on crash, no automatic recovery
`watch: true` — restarts on file changes in watched directories only

```javascript
// ecosystem.config.cjs
module.exports = {
  apps: [{
    name: "myapp",
    script: "src/index.js",
    watch: ["src", "config"],
    watch_delay: 1000,
    autorestart: false,
    ignore_watch: [
      "node_modules",
      ".git",
      "logs",
      "*.log",
      ".pm2",
      "public",
      "uploads"
    ],
    watch_options: {
      followSymlinks: false,
      usePolling: false
    },
    log_date_format: "YYYY-MM-DD HH:mm:ss",
    out_file: "./logs/out.log",
    error_file: "./logs/error.log"
  }]
};
```

## Log Viewing

```bash
pm2 logs <name>                      # stream live (Ctrl+C to stop)
pm2 logs <name> --lines 100          # last 100 lines then stream
pm2 logs <name> --err                # errors only
pm2 logs <name> --out                # stdout only
pm2 logs <name> --nostream --lines 200  # dump without follow
pm2 logs --json                      # structured JSON output
pm2 flush                            # clear all log files
```

Log files: `~/.pm2/logs/<name>-out.log` / `<name>-error.log`
Windows path: `C:\Users\<user>\.pm2\logs\`

## Lifecycle Management

```bash
pm2 list                    # view all processes and status
pm2 jlist                   # JSON output for scripting
pm2 info <name>             # detailed process info
pm2 stop <name>             # stop (keeps in list)
pm2 restart <name>          # restart
pm2 delete <name>           # stop + remove from list
pm2 delete all              # remove all processes
pm2 ping                    # check if PM2 daemon is alive
```

**When work is complete: always `pm2 delete <name>` to clean up orphaned processes.**

Stopping a watched process: `pm2 stop` while watch is active restarts on next file change.
To fully halt: `pm2 delete <name>` (removes it entirely).

## Windows vs Linux

### File Watching

| Environment | Config |
|---|---|
| Linux native | `usePolling: false` (inotify kernel events) |
| WSL watching `/mnt/c/...` | `usePolling: true, interval: 1000` |
| Windows native | `usePolling: false` (ReadDirectoryChangesW) |
| Network / NFS / Docker volumes | `usePolling: true, interval: 1000` |

Linux inotify exhaustion fix (symptom: watch silently stops working):
```bash
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
```

### Windows: npm Scripts and .cmd Wrappers

PM2 cannot spawn `.cmd` shims (npm, npx, etc.) directly — they require `cmd.exe`.

```javascript
// ecosystem.config.cjs — Windows npm script
{
  name: "myapp",
  script: "npm",
  args: "start",
  interpreter: "cmd",
  interpreter_args: "/c"
}
```

For globally installed CLIs, find the real `.js` entry point:
```bash
# Linux/macOS
cat "$(which myapp)" | head -5

# Windows PowerShell
Get-Command myapp | Select-Object -ExpandProperty Source
```
Point `script` at the resolved `.js` file — never at the `.cmd` wrapper.

### Terminal Suppression on Windows (CRITICAL)

All code that spawns subprocesses MUST use `windowsHide: true` to prevent popup windows.

```javascript
// ❌ WRONG - will show popup windows on Windows
spawn('node', ['script.js']);

// ✅ CORRECT - hides windows, safe for all platforms
spawn('node', ['script.js'], { windowsHide: true });
```

Applies to all subprocess execution:
- `child_process.spawn()` → `{ windowsHide: true }`
- `child_process.exec()` → `{ windowsHide: true }`
- `child_process.execFile()` → `{ windowsHide: true }`
- `child_process.fork()` → `{ silent: true }` (alternative for fork)

PM2-started processes automatically hide windows. Code-spawned subprocesses must explicitly set this. Forgetting creates visible popups during automation—unacceptable UX.

### Windows 11+ wmic Error

PM2 uses `wmic` for process stats — removed in Windows 11+.
Symptom: `Error: spawn wmic ENOENT` in `~/.pm2/pm2.log`.
Fix: `npm install -g pm2@latest`. App processes continue working despite the error.

### Persistence on Reboot

| Platform | Method |
|---|---|
| Linux | `pm2 startup && pm2 save` (auto-detects systemd/upstart/openrc) |
| Windows | [pm2-installer](https://github.com/jessety/pm2-installer) (Windows Service) |

```bash
pm2 save        # snapshot current process list to ~/.pm2/dump.pm2
pm2 resurrect   # restore saved list after manual daemon restart
```
