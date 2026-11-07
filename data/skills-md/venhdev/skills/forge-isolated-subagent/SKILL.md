---
name: forge-isolated-subagent
description: "Delegate /forge implementation to a background subagent in an isolated worktree."
disable-model-invocation: true
---

# forge-isolated-subagent — Delegated Worktree Construction Pipeline

1. Execute `/worktree` to create `.agents/worktree/<branch>`.
2. Dispatch a background subagent (Role: `Forge Worker (<branch>)`) to execute `/forge` inside `.agents/worktree/<branch>`, seeded with target task/changeset specifications, acceptance criteria, and invariant boundaries.
