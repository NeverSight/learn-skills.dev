---
name: mcp-github-ops
description: Use GitHub MCP for issue/PR context, diffs, reviews, and automations. Use when the task references PR/issue numbers, review requests, or requires repo metadata beyond local git.
compatibility: Requires GitHub MCP configured (token/env in mcp.json).
allowed-tools: MCP(*) Bash(*)
---

# mcp-github-ops

## Procedure
1. Load issue/PR context (title, body, files changed).
2. Map to local branch/worktree if needed.
3. Produce actions: review notes, patch, or `/pr` command execution.

## Output
- Linked PR/issue context + recommended actions.
