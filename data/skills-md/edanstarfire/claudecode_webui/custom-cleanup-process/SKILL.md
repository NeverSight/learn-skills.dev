---
name: custom-cleanup-process
description: Project-specific cleanup process after issue completion. Stops test servers and cleans project-specific artifacts for claudecode_webui.
allowed-tools: [Bash, Skill]
---

# Custom Cleanup Process

## Purpose

This is a **project-specific custom skill** called by the `approve_issue` workflow to clean up project-specific resources.
It handles stopping test servers and cleaning artifacts specific to this project (claudecode_webui).

Generic workflow skills invoke this skill if it exists; if absent, the cleanup step is skipped (only generic cleanup like worktree removal runs).

## Input

- `issue_number` (from $1 argument): The issue number being cleaned up

## Cleanup Steps

### 1. Calculate Ports

- Backend Port = 8000 + (issue_number % 1000)
- Vite Port = 5000 + (issue_number % 1000)

### 2. Stop Test Servers

Use the `process-manager` skill pattern - find and kill by PID:

```bash
# Find and kill backend server
lsof -ti :${BACKEND_PORT} | xargs -r kill 2>/dev/null

# Find and kill vite server
lsof -ti :${VITE_PORT} | xargs -r kill 2>/dev/null
```

### 3. Verify Servers Stopped

```bash
lsof -i :${BACKEND_PORT} 2>/dev/null
lsof -i :${VITE_PORT} 2>/dev/null
```

Both should return no output.

### 4. Error Handling

- If servers are not found on expected ports, warn but continue (servers may have already been stopped)
- If kill fails, try `kill -9` as fallback
- Do NOT fail the overall cleanup if server stop fails

## Usage by Generic Skills

The `approve_issue` workflow calls this skill like:

```
Invoke custom-cleanup-process skill with issue_number=$1
```

The skill derives port numbers from the issue number and handles all project-specific cleanup.
It may use the `process-manager` skill internally for process management.
If this skill does not exist, the generic workflow proceeds with only generic cleanup (worktree removal, branch cleanup, etc.).
