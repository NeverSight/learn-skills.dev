---
name: syncing-mcp-servers
description: Synchronize MCP server configuration between VS Code (.vscode/mcp.json) and Copilot CLI (~/.copilot/mcp-config.json). Use when setting up Copilot CLI for the first time, when MCP servers are added or changed in the repo, or when a user reports missing MCP tools in CLI.
---

# Syncing MCP Servers

This skill ensures MCP server configurations stay in sync between VS Code (repo-level) and Copilot CLI (user-level).

## Why This Exists

VS Code and Copilot CLI use **different config files with different JSON formats** for MCP servers. Neither reads the other's config. This skill bridges that gap.

| Platform | Config File | Top-Level Key | Scope |
|----------|------------|---------------|-------|
| **VS Code** | `.vscode/mcp.json` | `"servers"` | Per-workspace (repo, checked into git) |
| **Copilot CLI** | `~/.copilot/mcp-config.json` | `"mcpServers"` | Per-user (global, all repos) |

## Format Differences

### VS Code format (`.vscode/mcp.json`)
```json
{
  "servers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--viewport-size=1024,768"]
    },
    "microsoftdocs": {
      "type": "http",
      "url": "https://learn.microsoft.com/api/mcp"
    }
  }
}
```

### CLI format (`~/.copilot/mcp-config.json`)
```json
{
  "mcpServers": {
    "playwright": {
      "type": "local",
      "command": "npx",
      "tools": ["*"],
      "args": ["@playwright/mcp@latest", "--viewport-size=1024,768"]
    },
    "microsoftdocs": {
      "type": "http",
      "url": "https://learn.microsoft.com/api/mcp"
    }
  }
}
```

### Key differences:
1. **Top-level key**: `"servers"` (VS Code) vs `"mcpServers"` (CLI)
2. **Local servers**: CLI requires `"type": "local"` — VS Code infers it from `"command"`
3. **Tool filtering**: CLI supports `"tools": ["*"]` (or specific tool names) — VS Code uses `"tools"` differently in its config
4. **Comments**: VS Code's `mcp.json` supports JSON with comments (JSONC) — CLI does not

## Workflow

### Step 1 — Read the source of truth

Read `.vscode/mcp.json` from the repo. This is the canonical config, maintained by the team and checked into git.

### Step 2 — Read the user's CLI config

Read `~/.copilot/mcp-config.json`. This may contain servers from other projects — **do not overwrite them**.

On Windows: `$env:USERPROFILE\.copilot\mcp-config.json`
On macOS/Linux: `~/.copilot/mcp-config.json`

The location can be overridden by the user via `--config-dir` flag or `XDG_CONFIG_HOME` env var. Check if either is set.

### Step 3 — Convert and merge

For each server in `.vscode/mcp.json`:

1. **Local servers** (have `"command"`): Add `"type": "local"` and `"tools": ["*"]` for CLI format
2. **HTTP servers** (have `"type": "http"`): Copy as-is — format is identical
3. **Skip** any server that already exists in the CLI config with matching `"command"` and `"args"` (or matching `"url"` for HTTP types)
4. **Warn** if an existing CLI server has the same name but different config — ask the user whether to overwrite

### Step 4 — Write the updated CLI config

Write the merged config back to `~/.copilot/mcp-config.json`. Preserve JSON formatting (2-space indent).

### Step 5 — Verify

Run `copilot --prompt "list available MCP tools" --allow-all-tools -p "run /mcp show and exit"` or instruct the user to run `/mcp show` in their next CLI session to confirm the servers are available.

## Important Rules

1. **Never delete** servers from the CLI config that aren't in the repo's VS Code config — the user may have servers from other projects
2. **Always back up** the CLI config before writing: copy to `mcp-config.json.bak`
3. **Strip comments** when reading VS Code's JSONC file — parse it as JSONC, not strict JSON
4. **Preserve user's existing servers** — merge, don't replace
5. **Report what changed** — list servers added, updated, or skipped

## Reverse Sync (CLI → VS Code)

If the user added new MCP servers via CLI (`/mcp add`) that should also be available in VS Code:

1. Read `~/.copilot/mcp-config.json` for any servers not in `.vscode/mcp.json`
2. Convert: remove `"type": "local"` and `"tools"` fields (VS Code infers these)
3. Add to `.vscode/mcp.json` under `"servers"` key
4. Preserve existing comments in the JSONC file — add new servers at the end of the `"servers"` block

## Future-Proofing

The CLI and VS Code MCP config formats may converge in the future. Before syncing:

1. **Check if CLI now reads `.vscode/mcp.json`** — look for a `.vscode/mcp.json` or `.github/copilot/mcp.json` entry in CLI docs or `copilot help` output
2. **Check if the top-level key has changed** — CLI may adopt `"servers"` or VS Code may adopt `"mcpServers"`
3. **Check for a unified config path** — a `.github/mcp.json` or similar repo-level config that both platforms read

If any of these converge, update this skill and simplify the sync process.

## Reference

- [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [CLI MCP docs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli#add-an-mcp-server)
- [Custom agents config (tools + MCP)](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- CLI flag: `--additional-mcp-config @<file-path>` — loads extra MCP config for one session without modifying `~/.copilot/mcp-config.json`
