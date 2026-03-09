---
name: custom-test-process
description: Project-specific test process. Starts backend/vite servers, runs pytest, and verifies health endpoints for claudecode_webui.
allowed-tools: [Bash, Skill]
---

# Custom Test Process

## Purpose

This is a **project-specific custom skill** called by the Builder workflow to run the full test cycle.
It handles starting servers, running tests, and verifying health endpoints specific to this project (claudecode_webui).

Generic workflow skills invoke this skill if it exists; if absent, the test step is skipped.

## When Called

The Builder invokes this skill from its working directory (the worktree). Environment variables (ports) come from `custom-environment-setup`.

## Input

Environment from `custom-environment-setup`:
- `BACKEND_PORT`: Backend server port (8000 + issue_number % 1000)
- `VITE_PORT`: Vite dev server port (5000 + issue_number % 1000)

## Test Lifecycle

This skill owns the full test lifecycle in a single invocation:

### 1. Start Backend Server

**CRITICAL:** Unset the `CLAUDECODE` environment variable before starting the backend. The Claude Agent SDK includes an undocumented safety check that prevents it from running inside another Claude Code instance. Since the builder agent runs inside Claude Code, this env var is inherited by child processes. Our application launches its own Claude Code SDK instances, so if `CLAUDECODE` is set, those SDK sessions will halt prematurely.

```bash
env -u CLAUDECODE uv run python main.py --host 0.0.0.0 --debug-all --port ${BACKEND_PORT} &
```

Wait for server to be ready:
```bash
# Wait up to 30 seconds for backend
for i in $(seq 1 30); do
    curl -s http://localhost:${BACKEND_PORT}/health > /dev/null 2>&1 && break
    sleep 1
done
```

### 2. Start Frontend Dev Server (if frontend changed)

**CRITICAL:** Set `VITE_BACKEND_PORT` so the vite dev server proxies to the correct per-issue backend port instead of the default 8001:

```bash
cd frontend && VITE_BACKEND_PORT=${BACKEND_PORT} npm run dev -- --port ${VITE_PORT} &
```

The `VITE_BACKEND_PORT` environment variable is read by `vite.config.js` to configure the proxy target. Without this, the frontend would proxy requests to port 8001 (the default) instead of the issue-specific backend port.

### 3. Run Unit Tests

```bash
uv run pytest src/tests/ -v
```

### 4. Verify Health Endpoints

```bash
# Check backend health
curl -s http://localhost:${BACKEND_PORT}/health

# Check frontend (if started)
curl -s http://localhost:${VITE_PORT}
```

### 5. Leave Servers Running

**CRITICAL:** Do NOT stop servers after testing. Leave them running for user review.
The `custom-cleanup-process` skill handles stopping servers later.

## Test Verification

- Server starts without errors
- Health endpoint returns success
- Unit tests pass
- No regressions introduced

## Usage by Generic Skills

The Builder workflow calls this skill like:

```
Invoke custom-test-process skill
```

The skill uses port information from the environment (provided by custom-environment-setup).
It may use the `process-manager` skill internally for process management.
If this skill does not exist, the generic workflow skips the test step.
