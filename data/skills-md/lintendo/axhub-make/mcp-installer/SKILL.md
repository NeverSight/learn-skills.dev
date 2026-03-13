---
name: mcp-installer
description: "Install and configure MCP servers across desktop and CLI clients (Claude, Cline, Windsurf, Cursor, VSCode, Gemini CLI, Codex, Trae, Antigravity, etc.) on macOS/Windows/Linux, preferring @smithery/cli when supported and otherwise performing manual JSON config updates and path discovery."
---

# MCP Installer

## Overview

Install MCP server configurations across multiple clients and OSes with a CLI-first workflow and a safe manual fallback.

## Workflow

### 1) Collect inputs

- Identify the target client ID and OS; use `references/clients.md` for the supported list and known paths.
- Gather MCP server definitions (name -> config object) and decide whether to override existing entries.
- If any provided MCP config includes secrets (for example fields like `key`, `token`, `apiKey`, `accessToken`, `secret`, `password`, or `Authorization`, or env vars like `*_KEY`, `*_TOKEN`), pause the install and ask the user to obtain/provide those values first. Only proceed once the user confirms they have the required credentials (or requests installing a placeholder and will fill it in later).

### 2) Prefer @smithery/cli (when supported)

- Run `npx @smithery/cli --help` and `npx @smithery/cli install --help` to confirm the exact syntax.
- Use the CLI install flow for the client ID; if the CLI rejects the client or fails, fall back to manual edits.

### 3) Manual install (JSON config fallback)

- Locate the config file path (see `references/clients.md`). If unknown, search standard config dirs for files like `mcp.json`, `mcp_config.json`, `claude_desktop_config.json`, or `cline_mcp_settings.json`.
- Read existing JSON and ensure a top-level `mcpServers` object exists.
- Merge servers: add new names; replace existing when override is true; preserve all other keys.
- Write JSON with 2-space indentation.

Example shape:

```json
{
  "mcpServers": {
    "example-server": {
      "command": "npx",
      "args": ["-y", "example-mcp@latest"],
      "env": {}
    }
  }
}
```

### 4) Verify and troubleshoot

- Restart the client and confirm the MCP servers appear.
- If writes fail on macOS, prompt for Full Disk Access and ensure the client app is closed before writing.
- For CLI-only clients (for example `claude-code`), use the client CLI help to locate its MCP install/config command.
- If Trae/Trae-CN installs fail due to permissions or other errors, generate a deep link and return it as a fallback.

### 5) Trae deep-link fallback

If `trae` or `trae-cn` cannot write to disk, generate a schema link for the user to open in Trae:

- `trae`: `trae://trae.ai-ide/mcp-import?type=${TYPE}&name=${NAME}&config=${BASE64_ENCODED_CONFIG}`
- `trae-cn`: `trae-cn://trae.ai-ide/mcp-import?type=${TYPE}&name=${NAME}&config=${BASE64_ENCODED_CONFIG}`

Rules:
- `TYPE` is the MCP transport type (for example `streamable-http`).
- `NAME` is the server name shown in Trae.
- `config` is the base64-encoded JSON config object for that server (no whitespace, UTF-8 bytes).

## References

- Use `references/clients.md` for client IDs, aliases, and known config paths.
