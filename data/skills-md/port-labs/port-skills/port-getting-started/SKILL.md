---
name: port-getting-started
description: "Set up Port and connect it to your coding agent: sign up for a Port account, install Port's MCP server, and optionally the Port CLI. Use when asked to 'get started with Port', 'set up Port', 'connect Port MCP', 'install the Port MCP server', 'how do I use Port from Claude Code/Cursor/VS Code', or before using any other skill in this repo for the first time."
license: MIT
compatibility: "Claude Code, Cursor, Codex CLI, GitHub Copilot, VS Code"
metadata:
  version: "1.0.0"
  author: port-labs
  repository: https://github.com/port-labs/port-skills
  tags: port,setup,mcp,onboarding,reference
  summary: Sign up for Port and connect its MCP server to your coding agent
---

# Getting started with Port

Every other skill in this repo produces correct Port config either way, but
without Port's MCP server connected, you're copying that config in by hand.
With it connected, the agent can read your live account and apply changes
directly. Do this once, first.

## Prerequisites

None. This is the first skill to run.

## How to get started

1. **Sign up for a Port account** at [app.port.io](https://app.port.io) if
   you don't have one yet.
2. **Find your Port region.** Check your Port app's base URL: if it
   contains `us`, you're on the US region; otherwise you're on EU.

   | Region | MCP server URL |
   |---|---|
   | EU | `https://mcp.port.io/v1` |
   | US | `https://mcp.us.port.io/v1` |

3. **Connect Port's MCP server** to your coding agent, using the URL for
   your region from the table above:

   | Client | How to connect |
   |---|---|
   | Cursor | [Install EU](cursor://anysphere.cursor-deeplink/mcp/install?name=port-eu&config=eyJ1cmwiOiJodHRwczovL21jcC5wb3J0LmlvL3YxIn0=) or add an MCP server manually with your region's URL |
   | Claude (claude.ai / Claude Desktop) | [Install from the Claude directory](https://claude.ai/directory/8f5edd1c-c876-465e-a5b9-cc8e6d27dcb7), then enter your region's MCP server URL when prompted |
   | VS Code | Add `port-eu` or `port-us` as an MCP server using the URL for your region |
   | Claude Code (CLI) | `claude mcp add --transport http port-eu https://mcp.port.io/v1` (or `port-us` / `https://mcp.us.port.io/v1`) |
   | Any other MCP-compatible agent | Point it at your region's URL, or follow the [manual install docs](https://docs.port.io/agent-management/port-mcp-server/installation) |

   This repo's own `.mcp.json` already ships both `port-eu` and `port-us`
   servers, so installing this plugin gets you both — disable whichever
   region doesn't apply to your account.

4. **Optional: install the [Port CLI](https://github.com/port-experimental/port-cli).**
   Beyond MCP, it covers day-to-day resource management from the terminal,
   and `port skills sync` pulls any skills your org has already configured
   in Port straight into your coding agent's skill directory.
5. **Once connected, prefer Port's own tools over guesswork.** Every skill
   in this repo notes where it can call Port's MCP tools directly (to read
   live state or apply a change) instead of just handing you config to
   copy in. If a skill doesn't cover something you need, search Port's
   documentation from inside the agent with the `search_port_knowledge_sources`
   MCP tool rather than guessing.

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| MCP server added but no Port tools show up | Most agents need a session restart after adding an MCP server | Restart the coding agent |
| The Cursor/VS Code install link does nothing when clicked | Some browsers block custom URI schemes by default | Use the [manual install docs](https://docs.port.io/agent-management/port-mcp-server/installation) instead |
| `claude mcp add` command not found | That command is Claude Code's own CLI, not Claude Desktop or claude.ai | Use the Claude directory link for Desktop/claude.ai instead |
| Tools work for one teammate but not another | Each person connected to the wrong region's server for their account | Re-check the Port app base URL and connect to that region's server instead |

## Quick reference

- Sign up: [app.port.io](https://app.port.io)
- MCP server URL (EU): `https://mcp.port.io/v1`
- MCP server URL (US): `https://mcp.us.port.io/v1`
- Manual install docs: [docs.port.io/agent-management/port-mcp-server/installation](https://docs.port.io/agent-management/port-mcp-server/installation)
- Port CLI: [github.com/port-experimental/port-cli](https://github.com/port-experimental/port-cli)
- Search Port's docs from inside a connected agent: the `search_port_knowledge_sources` MCP tool
