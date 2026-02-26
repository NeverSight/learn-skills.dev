---
name: flipswitch-status
description: Shows an overview of all feature flags with on/off status per environment, targeting rules, and rollout indicators. Use when checking the current state of feature flags or when the user asks about flag status across environments.
disable-model-invocation: true
allowed-tools: AskUserQuestion mcp__flipswitch__authenticate mcp__flipswitch__list_organizations mcp__flipswitch__list_projects mcp__flipswitch__flag_overview
---

Show an overview of feature flags in a Flipswitch project.

**UX rule**: Whenever you need to ask the user to choose between options (e.g. selecting an organization or project), use the `AskUserQuestion` tool to present a selection UI instead of asking in plain text.

## Instructions

### 0. Verify MCP Server Configuration

Call `mcp__flipswitch__authenticate` as a connectivity check.

- **If successful**: ✅ MCP server is configured. Proceed to step 1.
- **If it fails with "tool not found" or similar**: ❌ MCP server is NOT configured. Run this in your terminal:
  ```
  claude mcp add --scope user --transport http flipswitch https://mcp.flipswitch.io/mcp
  ```
  Then restart Claude Code and retry this skill.
- **If it fails with a network error**: ⚠️ MCP server is configured but unreachable. Check your internet connection.

### 1. Authenticate
Call `mcp__flipswitch__authenticate`. If not authenticated, follow the device flow (show URL and code, then call `mcp__flipswitch__authenticate` again to confirm).

### 2. Select organization and project
1. Call `mcp__flipswitch__list_organizations`. If only one, use it. Otherwise, ask the user.
2. Call `mcp__flipswitch__list_projects` with the selected org. If only one, use it. Otherwise, ask the user.

### 3. Get flag overview
Call `mcp__flipswitch__flag_overview` with the org and project IDs. This returns a table with:
- Each flag's on/off status per environment
- `[T]` indicator for flags with targeting rules
- `[R]` indicator for flags with rollout/variants

### 4. Display results
Show the table returned by `mcp__flipswitch__flag_overview` directly to the user. The tool already formats it as a markdown table with a legend.
