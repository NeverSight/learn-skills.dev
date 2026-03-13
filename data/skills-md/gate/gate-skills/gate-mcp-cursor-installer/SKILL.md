---
name: gate-mcp-cursor-installer
description: One-click installer for Gate MCP and Skills in Cursor. Installs Gate MCP servers (main/dex/info/news, selectable) and all skills from the gate-skills repository. Installs all MCPs + all skills by default; skills are always fully installed.
---

# Gate One-Click Installer (MCP + Skills)

Use this skill when the user says "one-click install Gate", "install Gate MCP and skills", "install gate-mcp", etc.

## Resources

| Type | Name | Endpoint / Config |
|------|------|-------------------|
| MCP | Gate (main) | `npx -y gate-mcp`, see [gate-mcp](https://github.com/gate/gate-mcp) |
| MCP | Gate Dex | https://api.gatemcp.ai/mcp/dex, fixed x-api-key |
| MCP | Gate Info | https://api.gatemcp.ai/mcp/info |
| MCP | Gate News | https://api.gatemcp.ai/mcp/news |
| Skills | gate-skills | https://github.com/gate/gate-skills (installs all under skills/) |

## Behavior Rules

1. **Default**: When the user does not specify which MCPs to install, install **all MCPs** (main, dex, info, news) + **all gate-skills**.
2. **Selectable MCPs**: Users can choose to install only specific MCPs (e.g. main only, dex only, etc.); follow the user's selection.
3. **Skills**: Unless `--no-skills` is passed, always install **all** skills from the gate-skills repository's **skills/** directory.

## Installation Steps

### 1. Confirm User Selection (MCPs)

- If the user does not specify which MCPs -> install all: main, dex, info, news.
- If the user specifies "only install xxx" -> install only the specified MCPs.

### 2. Write Cursor MCP Config

- Config file: `~/.cursor/mcp.json` (Windows: `%APPDATA%\Cursor\mcp.json`).
- If it already exists, **merge** into the existing `mcpServers`; do not overwrite other MCPs.
- Config details:
  - **Gate (main)**: `command: npx`, `args: ["-y", "gate-mcp"]`
  - **Gate-Dex**: `url` + `transport: streamable-http` + `headers["x-api-key"]` fixed as MCP_AK_8W2N7Q + `headers["Authorization"]` = `Bearer ${GATE_MCP_TOKEN}`
  - **Gate-Info / Gate-News**: `url` + `transport: streamable-http`

### 3. Install gate-skills (all)

- Pull all subdirectories under **skills/** from https://github.com/gate/gate-skills and copy them to `~/.cursor/skills/` (or the corresponding directory for the current environment).
- Add `--no-skills` when using the script to install MCP only without skills.

### 4. Post-Installation Prompt

- Inform the user of the installed MCP list and "all gate-skills have been installed" (unless --no-skills was used).
- Prompt to restart Cursor.
- **Getting API Key**: If the user uses Gate (main) for spot/futures trading, prompt them to visit https://www.gate.com/myaccount/profile/api-key/manage to create an API Key and set `GATE_API_KEY` and `GATE_API_SECRET`.
- **Gate-Dex Authorization**: If Gate-Dex was installed and a query returns an authorization required message, prompt the user to first open https://web3.gate.com/ to create or bind a wallet, then the assistant will return a clickable Google authorization link for the user to complete OAuth.

## Script

Use the **scripts/install.sh** in this skill directory for one-click installation.

- Usage:  
  `./scripts/install.sh [--mcp main|dex|info|news] ... [--no-skills]`  
  Installs all MCPs when no `--mcp` is passed; pass multiple `--mcp` to install only specified ones; `--no-skills` installs MCP only.
- The DEX x-api-key is fixed as `MCP_AK_8W2N7Q` and written to mcp.json.

After downloading this skill from GitHub, run from the repository root:  
`bash scripts/install.sh`  
Or (MCP only):  
`bash scripts/install.sh --no-skills`
