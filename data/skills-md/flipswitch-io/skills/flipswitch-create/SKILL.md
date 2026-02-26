---
name: flipswitch-create
description: Creates a new feature flag in Flipswitch and generates evaluation code for the project's language. Use when adding a new feature flag or when the user asks to create a flag.
disable-model-invocation: true
argument-hint: "[flag name]"
allowed-tools: Read Glob AskUserQuestion mcp__flipswitch__authenticate mcp__flipswitch__list_organizations mcp__flipswitch__list_projects mcp__flipswitch__create_flag mcp__flipswitch__get_sdk_setup_snippet
---

Quickly create a new feature flag in Flipswitch.

**UX rule**: Whenever you need to ask the user to choose between options (e.g. selecting an organization, project, or language), use the `AskUserQuestion` tool to present a selection UI instead of asking in plain text.

## Arguments
The user may provide a flag name as an argument via `$ARGUMENTS`, e.g. `dark mode`. If no argument is given, ask the user for a flag name.

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

### 2. Parse the flag name
Take the user's input and:
- Use it as the human-readable **name** (e.g. "Dark Mode")
- Convert to kebab-case for the **key** (e.g. "dark-mode")

### 3. Select organization and project
1. Call `mcp__flipswitch__list_organizations`. If only one, use it. Otherwise, ask the user.
2. Call `mcp__flipswitch__list_projects` with the selected org. If only one, use it. Otherwise, ask the user.

### 4. Create the flag
Call `mcp__flipswitch__create_flag` with:
- The org and project IDs
- The generated key and name
- `flagValueType`: `Boolean` (unless the user specified a different type)

### 5. Generate evaluation snippet
Detect the project language (check for `package.json`, `go.mod`, etc.) and call `mcp__flipswitch__get_sdk_setup_snippet` to get the evaluation code for this specific flag key.

**For JavaScript projects**: Also determine the environment (web or server) using the same detection logic as in the setup skill. If uncertain, ask the user with `AskUserQuestion`.

### 6. Show results
Tell the user:
- Flag created: **{name}** (`{key}`)
- Show the evaluation code snippet for their language
- Link to dashboard: https://app.flipswitch.io
- Remind them the flag is disabled by default — they can enable it in the dashboard
