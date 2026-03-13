---
name: flipswitch-toggle
description: Enables or disables a feature flag in a specific environment. Use when changing a flag's state, turning on a feature for testing, or disabling a flag in production.
disable-model-invocation: true
argument-hint: "[flag name] [on/off]"
allowed-tools: AskUserQuestion mcp__flipswitch__authenticate mcp__flipswitch__list_organizations mcp__flipswitch__list_projects mcp__flipswitch__list_flags mcp__flipswitch__list_environments mcp__flipswitch__toggle_flag
---

Enable or disable a feature flag in a specific environment.

**UX rule**: Whenever you need to ask the user to choose between options (e.g. selecting an organization, project, flag, or environment), use the `AskUserQuestion` tool to present a selection UI instead of asking in plain text.

## Arguments
The user may provide arguments via `$ARGUMENTS`, e.g. `dark-mode on` or `dark-mode off`. Parse:
- The flag name or key (e.g. "dark-mode", "Dark Mode")
- The desired state: `on`/`enable`/`true` → enabled, `off`/`disable`/`false` → disabled

If no arguments are given, ask the user which flag to toggle and whether to enable or disable it.

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

### 3. Find the flag
Call `mcp__flipswitch__list_flags` with the org and project IDs. Match the user's input against flag keys and names (case-insensitive). If no match is found, show the available flags and ask the user to pick one.

### 4. Select environment
Call `mcp__flipswitch__list_environments` with the org and project IDs. If the user didn't specify an environment, ask which one. Default to "Development" if it exists and the user doesn't have a preference.

### 5. Production safety check
If the selected environment name contains "prod", "production", "live", or "main" (case-insensitive), you MUST warn the user before proceeding. Show a clear warning like:

> You are about to **enable/disable** flag `{key}` in **{environment name}**. This is a production environment and the change will affect live users. Are you sure?

Do NOT proceed until the user explicitly confirms. If they decline, abort.

### 6. Toggle the flag
Call `mcp__flipswitch__toggle_flag` with the org ID, project ID, flag ID, environment ID, and the desired `enabled` value.

### 7. Confirm
Tell the user:
- Flag **{name}** (`{key}`) is now **enabled/disabled** in **{environment name}**
- Link to dashboard: https://app.flipswitch.io
