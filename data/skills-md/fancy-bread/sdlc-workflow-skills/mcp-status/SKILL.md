---
name: mcp-status
description: MCP Status
disable-model-invocation: true
---

# MCP Status

## Overview
Check the authentication status of all configured Model Context Protocol (MCP) servers.

## Definitions

- **MCP server**: A configured Model Context Protocol server in Cursor (e.g. github, atlassian, ado, asdlc).
- **User-level MCP configuration**: The `mcpServers` section in `~/.cursor/mcp.json` (macOS/Linux) or `%USERPROFILE%\.cursor\mcp.json` (Windows), or configured via Cursor Settings → Features → Model Context Protocol.
- **Project-level MCP configuration**: Optional `mcpServers` in `.cursor/mcp.json` at the workspace root. When present, Cursor may merge or override with user-level config; discover from this file so status reflects project-configured servers. If the file is missing, skip (not an error).
- **Extension-exposed MCP**: An MCP server provided by a VS Code/Cursor extension (e.g. Agent Context Explorer / extension-ace). Tools may use prefixes like `mcp_<vendor>_*`. When the agent has access to such tools, include them in status and tag as source **(extension)**.

## Prerequisites

- **None required.** Run anytime to check status. If no MCP servers are configured, the command reports that.
- **MCP Tool Usage Standards**: MCP tool usage should follow best practices (check schema files, validate parameters, handle errors gracefully). These standards are documented in AGENTS.md §3 Operational Boundaries if AGENTS.md exists, but apply universally regardless.

## Purpose
MCP servers can disconnect or lose authentication after periods of inactivity. Use this command to verify all integrations are ready before starting work.

## Steps

1. **Discover configured MCP servers (user, project, extension)**
   - **User-level**: Read `~/.cursor/mcp.json` (macOS/Linux) or `%USERPROFILE%\.cursor\mcp.json` (Windows). Extract `mcpServers` keys. Tag each server as source **(user)**. If the file is not accessible, try common server names: `github`, `atlassian`, `ado`, `asdlc`, `user-github`, `user-atlassian`, `user-ado`, `user-asdlc`.
   - **Project-level**: If workspace root is available, read `.cursor/mcp.json` at workspace root. If the file exists, extract `mcpServers` keys and tag each as **(project)**. If a server name already appeared from user config, record both sources (e.g. "user, project") or report once with combined source. If the file is missing, skip (not an error).
   - **Extension-exposed**: When the agent has access to MCP tools from extensions (e.g. Agent Context Explorer; tool names use a prefix pattern such as `mcp_<vendor>_<suffix>`), treat each distinct extension server as one entry. Call one read-only tool per known extension server (e.g. extension-ace: list rules or list commands) and tag as **(extension)**. If no extension tools are available, skip (not an error).
   - Note: Server names in config may differ from tool prefixes (e.g. config has `github` but tools use `mcp_github_*`).

2. **Test each server connection**
   - For each discovered server (from any source), attempt to call one lightweight read-only tool to verify connectivity and authentication. Record the server's **source** (user / project / extension) with the result.
   - Use common tool patterns for known server types:
     - **github** / **user-github** → Try `list_commits` (may require owner/repo args) or `list_branches`
     - **atlassian** / **user-atlassian** → Try `getAccessibleAtlassianResources` or `atlassianUserInfo`
     - **ado** / **user-ado** → Try `core_list_projects`
     - **asdlc** / **user-asdlc** → Try `list_articles`
   - For unknown server types, try common tool names like `list_*`, `get_*`, or `*_info` with minimal or empty args.
   - Record success or failure for each server. Handle "server not found" vs "authentication error" vs "tool not found" differently.

3. **Report status**
   - Display results in a clear, formatted list. Group or label by source (User config, Project config, Extensions) so users see where each server comes from.
   - Show server name, authentication status, and source (e.g. "(user)", "(project)", "(extension)").
   - For disconnected servers, provide reconnection instructions (Cursor Settings → Features → Model Context Protocol).

## Tools

### Filesystem
- Read user MCP configuration: `~/.cursor/mcp.json` (macOS/Linux) or `%USERPROFILE%\.cursor\mcp.json` (Windows). Parse JSON to extract `mcpServers` keys.
- Read project MCP configuration: `.cursor/mcp.json` at workspace root (if present). Parse JSON to extract `mcpServers` keys. If file is missing, skip.

### MCP (per discovered server)
- **github** / **user-github** → Try `list_commits`, `list_branches`, or other read-only tools
- **atlassian** / **user-atlassian** → Try `getAccessibleAtlassianResources`, `atlassianUserInfo`
- **ado** / **user-ado** → Try `core_list_projects`
- **asdlc** / **user-asdlc** → Try `list_articles`
- **Extension-exposed** (e.g. extension-ace): Try a read-only tool such as list rules or list commands (no args or minimal args). Tag result as (extension).
- **Other servers**: Try common read-only tool patterns (`list_*`, `get_*`, `*_info`) with minimal or empty args
- Note: Tool names may be prefixed with `mcp_<server>_` or `mcp_user-<server>_` depending on configuration. Record source (user / project / extension) with each result.

## Expected Output

### All Connected (with sources)
```
🔌 MCP Server Status

User config:
  ✅ atlassian - Connected (user)
  ✅ github - Connected (user)

Project config:
  (none)

Extensions:
  ✅ extension-ace - Connected (extension)

All systems operational!
```

(When only user-level config exists and no extensions, output may show no "Project config" or "Extensions" sections, and servers with "(user)" or no source label for backward compatibility.)

### Some Disconnected
```
🔌 MCP Server Status

User config:
  ❌ atlassian - Needs authentication (user)
  ✅ github - Connected (user)

⚠️ Action Required:
1. Open Cursor Settings (Cmd+, or Ctrl+,)
2. Navigate to: Tools & MCP
3. Click "Connect" next to: atlassian
4. Run /mcp-status again to verify
```

## When to Use

- **Start of day** - Verify connections before beginning work
- **After inactivity** - MCP servers may disconnect after timeout
- **Before critical commands** - Ensure integrations are ready for commands like `/start-task`, `/create-task`, etc.
- **Troubleshooting** - When other commands fail with authentication errors

## Error Handling

If unable to discover MCP servers:
- If user config file is not accessible, try common server names as fallback
- If project `.cursor/mcp.json` is missing, skip (not an error)
- If no extension tools are available, skip extension section (not an error)
- If no servers respond, report that no MCP servers are configured or accessible
- Provide link to MCP setup documentation (e.g., `docs/reference/mcp-setup.md` if present, or general MCP setup instructions)

If a server test fails:
- **Server not found**: Server name doesn't exist in MCP configuration
- **Authentication error**: Server exists but needs reconnection/authentication
- **Tool not found**: Server exists but the tested tool isn't available (try a different tool)
- **Network/connection error**: Server unreachable or connection failed
- Provide specific guidance for each failure type, especially authentication errors which require user action

## Notes

- This command performs **read-only** operations only
- No data is modified or created
- Safe to run at any time
- Does not require any parameters or arguments

## Guidance

### Role
Act as a **developer** checking that MCP integrations are ready before running commands that depend on them.

### Instruction
Read the MCP configuration file (`~/.cursor/mcp.json` or Windows equivalent) to discover configured servers. For each server, attempt to call a lightweight read-only MCP tool to verify connectivity and authentication. Report connected / disconnected status; for disconnected servers, provide reconnection steps (Cursor Settings → Features → Model Context Protocol).

### Context
- MCP servers can disconnect or lose auth after inactivity. Use at start of day, after inactivity, or before critical commands.
- Discover servers from three sources: (1) user-level `mcp.json`, (2) project-level `.cursor/mcp.json` at workspace root when present, (3) extension-exposed MCPs when the agent has access to their tools. Report each server with its source (user / project / extension).
- If user config file is not accessible, try common server names and test connectivity. Missing project or extension config is not an error.
- **ASDLC patterns**: [Context Gates](asdlc://context-gates)
- **ASDLC pillars**: **Quality Control** (pre-flight validation for other commands)

### Examples

**ASDLC**: [Context Gates](asdlc://context-gates) — MCP checks act as an input gate before running commands that depend on them.

### Constraints

**Rules (Must Follow):**
1. **Operational Standards Compliance**: This command follows operational standards (documented in AGENTS.md if present, but apply universally):
   - **MCP Tool Usage**: Check schema files, validate parameters, handle errors gracefully
   - **AGENTS.md Optional**: Commands work without AGENTS.md. Standards apply regardless of whether AGENTS.md exists.
   - See AGENTS.md §3 Operational Boundaries (if present) for detailed standards
2. **Read-only Operations**: This command performs read-only operations only; no data is modified or created.
3. **Error Handling**: If a server test fails, distinguish authentication errors (needs reconnect) from other errors and provide specific guidance.
