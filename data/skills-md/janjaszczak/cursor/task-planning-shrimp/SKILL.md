---
name: task-planning-shrimp
description: Plan, split, and track multi-step work using Shrimp Task Manager MCP (or equivalent). Use for multi-file refactors, migrations, or any work that benefits from task tracking.
compatibility: Requires Shrimp Task Manager MCP server configured and reachable.
allowed-tools: MCP(*)
metadata:
  intent: Don’t force planning when the user wants a single command.
---

# task-planning-shrimp

## Activation gate (anti-noise)
Activate if:
- Multi-step change, multiple files, long refactor, migration, or user explicitly asks for plan/task breakdown.

Skip if:
- Single command answer or short Q&A.

## Procedure
1. Create a concise task tree:
   - Parent: objective
   - Children: file-level tasks
   - Leaves: atomic steps with acceptance checks
2. Mark dependencies and “blocking” items.
3. Keep tasks small (≤30–60 min each for a mid).
4. Update status as work progresses.

## Output
- Link/IDs of created tasks + immediate next task to execute.
