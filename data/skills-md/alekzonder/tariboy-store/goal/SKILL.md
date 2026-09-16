---
name: goal
description: Use when an agent needs to understand or set its Tariboy Goal and AI usage attribution.
---

# Goal

The daemon selects the Goal shown in `runtime: goal` and automatically attributes AI usage to that Native Task and its top-level root. Use the `tasks` skill to read, create, and update the authoritative task.

If this iteration began without a Goal, create or claim the task first, then run `scripts/goal.sh set <TASK-KEY>`. The task must be active and assigned to this agent. The command output confirms selection for subsequent AI requests; the already-rendered `runtime: goal` block does not refresh during the iteration, and earlier unattributed requests remain unchanged.

A selected Goal remains daemon-owned and sticky across iterations until released. Neither another `goal.sh set` call nor merely starting a new iteration can replace it.
