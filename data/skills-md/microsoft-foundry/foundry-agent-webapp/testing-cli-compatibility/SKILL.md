---
name: testing-cli-compatibility
description: Validate that Copilot CLI can see all repo skills, MCP servers, and custom instructions. Use when setting up CLI for the first time, after adding skills, or to diagnose CLI issues.
---

# Testing CLI Compatibility

Validates that the standalone [Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli) works correctly with this repo's skills and MCP servers.

## Quick Start

```powershell
# Run all tests (including MCP)
./deployment/scripts/test-cli-compatibility.ps1

# Skip MCP server tests (faster, no tool approval needed)
./deployment/scripts/test-cli-compatibility.ps1 -SkipMcp
```

## What It Tests

| # | Test | What It Checks |
|---|------|----------------|
| 1 | **CLI Version** | `copilot` command is installed and responds |
| 2 | **Custom Instructions** | `.github/copilot-instructions.md` is loaded (identifies project name) |
| 3 | **Skills** | All `.github/skills/*/SKILL.md` files are visible (count auto-detected) |
| 4 | **MCP Servers** | `playwright` and `microsoftdocs` servers are connected |

## Prerequisites

1. **Copilot CLI installed**: `npm install -g @anthropic-ai/copilot-cli` or via GitHub
2. **Authenticated**: Run `copilot login` if not already logged in
3. **MCP servers synced**: Run the `syncing-mcp-servers` skill first if MCP tests fail

## How It Works

The script uses `copilot -p "<prompt>" -s --no-auto-update` to invoke the CLI in non-interactive mode:

- `-p` — Single prompt, exits after response
- `-s` — Silent mode, output only the agent response (no stats)
- `--no-auto-update` — Skip update check for faster execution
- `--allow-all-tools` — Used only for MCP test (needs tool access)

Each test sends a prompt asking the CLI to list what it can see, then validates the response against expected values.

## When to Run

- After adding or modifying skills in `.github/skills/`
- After syncing MCP servers with the `syncing-mcp-servers` skill
- When a user reports CLI issues (missing agents, skills, or tools)
- As a smoke test after CLI updates (`copilot update`)

## Manual Testing

If the script isn't available, you can test manually:

```powershell
# Check version
copilot --version

# Test custom instructions
copilot -p "What project is this repo for?" -s

# Test skills
copilot -p "List all custom skills" -s

# Test MCP (needs --allow-all-tools)
copilot -p "List all MCP servers" -s --allow-all-tools
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `copilot` not found | Install CLI or add to PATH |
| Custom instructions not loaded | Ensure you're in the repo directory |
| Agents missing | No custom agents expected — this repo uses skills + copilot-instructions only |
| Skills missing | Check `.github/skills/*/SKILL.md` files exist with valid frontmatter |
| MCP servers not connected | Run `syncing-mcp-servers` skill to sync `.vscode/mcp.json` → `~/.copilot/mcp-config.json` |
