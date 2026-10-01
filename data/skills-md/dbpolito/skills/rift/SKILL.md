---
name: rift
description: Create and switch to an isolated Rift-backed worktree. Use when asked to work in a new worktree, Rift workspace, or isolated checkout.
---

# Rift

1. Create one worktree with `rift.create`. Use a short task-based name when a useful name is apparent.
2. After creation succeeds, call `opencode.session_move` with the returned directory in a separate tool call.
3. Continue the original task from the moved session.

Do not create another worktree after moving the session. Do not substitute a manual Git worktree when Rift was requested; report the blocker if the Rift tools are unavailable.
