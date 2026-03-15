---
name: pocketbase-automation-and-hooks
description: Use when you specifically need advanced PocketBase hooks, realtime subscriptions, and file lifecycle automation details
---

# PocketBase Automation and Hooks (Advanced)

## Overview
Use this only for event-driven workflows. Default to `pocketbase-agent-orchestrator` for standard management tasks.

## Focus
- Hook behavior and side-effect control
- Realtime subscription lifecycle
- File validation, retention, and cleanup

## Minimal Workflow
1. Define event triggers and idempotency expectations.
2. Implement minimal deterministic hook logic.
3. Verify realtime lifecycle and reconnection handling.
4. Add observability and operations handoff.

## References
- [hooks-patterns.md](references/hooks-patterns.md)
- [realtime-patterns.md](references/realtime-patterns.md)
- [file-workflows.md](references/file-workflows.md)
