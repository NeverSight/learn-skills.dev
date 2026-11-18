---
name: alera-orchestration
description: Dispatch, coordinate, and complete agent tasks through Alera orchestration.
metadata:
  version: 5
---

# Alera Orchestration

The runtime host owns lifecycle authority. Use its commands, not generic messages or arbitrary status edits, for completion, cancellation, gates, and ownership.

## Choose Your Role

- Dispatched worker (your terminal received an Alera dispatch): run `alera orchestration --json context` and read [worker](references/worker.md).
- Coordinator delegating tasks or planning a run: read [coordinator](references/coordinator.md).
- Following, controlling, or cleaning up a run: read [runs](references/runs.md).
- Stalled tasks, gates, cancellation, or ownership transfer: read [recovery](references/recovery.md).
- Questions, messages between agents, or terminal inspection: read [messaging](references/messaging.md).

Read only the references relevant to the current role. A worker completes exactly once with `alera orchestration complete --summary "..."`, then ends its turn and leaves the terminal available for reuse.

## Shared Constraints

Run inside an Alera terminal. `ALERA_TERMINAL_HANDLE` identifies the caller and `ALERA_WORKSPACE_ID` supplies the workspace default; `alera orchestration current` inspects both. Check `alera version --json` if compatibility is uncertain: commands that need a newer runtime host fail with a message to restart Alera.

Scope every task to its workspace and coordinator. A workspace holds at most one active run; tasks of a run must match its workspace and coordinator.

Honor prior explicit user authorization for the same scope without duplicate approval requests. Plan approval, stage gates, and stall gates are decisions for the user; never resolve them on the user's behalf or invent a user decision. Active workers ask the coordinator through `alera orchestration ask`, not a local user-input prompt.
