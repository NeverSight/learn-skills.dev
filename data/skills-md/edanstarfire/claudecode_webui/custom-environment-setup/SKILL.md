---
name: custom-environment-setup
description: Project-specific environment setup for issue workflows. Calculates test ports and provides initialization context for minions.
---

# Custom Environment Setup

## Purpose

This is a **project-specific custom skill** called by generic workflow skills at defined checkpoints.
It provides environment configuration specific to this project (claudecode_webui).

Generic workflow skills invoke this skill if it exists; if absent, the workflow continues without project-specific environment setup.

## Input

- `issue_number` (from $1 argument): The issue number being worked on

## Output

When invoked, this skill should set the following environment variables/context for the caller:

### Port Calculation

- **Backend Port** = 8000 + (issue_number % 1000)
- **Vite Port** = 5000 + (issue_number % 1000)

Examples:
- Issue #42 -> Backend: 8042, Vite: 5042
- Issue #372 -> Backend: 8372, Vite: 5372
- Issue #1234 -> Backend: 8234, Vite: 5234

### Initialization Context Fragment

Return this context fragment for inclusion in minion initialization:

```
Test Server Configuration:
- Backend Port: ${BACKEND_PORT} (8000 + issue_number % 1000)
- Backend Host: 0.0.0.0 (required for network-accessible dev server)
- Vite Port: ${VITE_PORT} (5000 + issue_number % 1000)
- Data Directory: Default (data/) - DO NOT use --data-dir flag
```

### Status Display Context

For `/status_workers`, provide:
- Port range info: Backend ports 8000-8999, Vite ports 5000-5999
- How to check running servers:
  ```bash
  # Check backend ports
  lsof -i :8000-8999 2>/dev/null | grep LISTEN

  # Check vite ports
  lsof -i :5000-5999 2>/dev/null | grep LISTEN
  ```

## Usage by Generic Skills

Generic workflow skills call this skill like:

```
Invoke custom-environment-setup skill with issue_number=$1
```

The skill returns port configuration and any project-specific init context.
If this skill does not exist, the generic workflow proceeds without port/environment configuration.
