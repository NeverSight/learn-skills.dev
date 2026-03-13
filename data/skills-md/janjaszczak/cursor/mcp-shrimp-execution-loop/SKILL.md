---
name: mcp-shrimp-execution-loop
description: Combine Shrimp task tracking with execution loops (plan → execute → verify → update status). Use for multi-step deliveries where progress tracking matters.
compatibility: Requires Shrimp Task Manager MCP.
allowed-tools: MCP(*) Bash(*) Read
---

# mcp-shrimp-execution-loop

## Procedure
1. Create tasks (or load existing).
2. For each task:
   - Execute minimal change
   - Verify (test/lint/run)
   - Update task status + notes
3. Stop at acceptance criteria.

## Output
- Current status snapshot + next task.
