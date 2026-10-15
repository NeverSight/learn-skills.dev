---
name: agent-mesh
description: >-
  Universal inter-harness agent mesh orchestrator enabling asynchronous, peer-to-peer, and event-driven communication
  across Claude Code, Antigravity, OpenCode, Pi, Codex, and any ACP-compliant agent with live session visibility,
  git worktree isolation, and session leasing. Supports one-command setup via `mesh --init` or `mesh --install`,
  and clean removal via `mesh --uninstall`. Use whenever the user asks to coordinate multiple AI agent harnesses,
  have agents communicate across harnesses, run cross-agent workflows, view/attach to agent sessions live, or initialize the mesh.
license: MIT
compatibility: Requires Node 22+ (for built-in node:sqlite and native IPC) and Git. Works on Windows and POSIX.
metadata:
  version: 1.1.0
---

# Agent Mesh: Universal Inter-Harness Communication

`agent-mesh` connects heterogeneous coding agent harnesses into an asynchronous, observable agent mesh.

Instead of rigid 1-to-1 RPC relays, agents interact via an atomic local Broker daemon using asynchronous messaging, Git worktree isolation, and session leasing for live human inspection.

## Supported Harnesses & Tiers
- **Claude Code (`claude`)**: Continuous `stream-json` stdio or resume mode. Automatic plugin hooks via `hooks/hooks.json`.
- **Google Antigravity (`agy`)**: Headless print mode with project session resumption and strict JSON lifecycle hooks.
- **OpenCode (`opencode`)**: CLI run mode. *(Experimental: server mode endpoint not yet verified against `opencode serve`.)*
- **Pi (`pi`)**: RPC stdio mode (`pi --mode rpc`) or session resumption.
- **Codex (`codex`)**: `codex exec --json`. *(Experimental: event names pending verification against installed CLI version.)*
- **ACP Agents**: Any Agent Client Protocol-compliant agent via generic `AcpDriver`. *(Experimental: method names pending upstream ACP standard stabilization.)*
- **Declarative CLIs**: Aider, custom LLM CLIs via 30-line `resumeDriver`.

## Live Presence & MCP Per Harness

Presence (who is online, names, exit) comes from hooks/plugins plus a broker-side process scanner. Every harness
also has an optional, opt-in MCP shim (`mesh --init --mcp`, removed by `mesh --uninstall`) that gives agents the
tools `mesh_send`, `mesh_ask`, `mesh_inbox`, `mesh_status`; the Stop-hook/plugin inbox injection keeps working
without it. Sessions announced by both hooks and MCP collapse into one row and one start toast.

| Harness | Presence sources | MCP entry (opt-in) | MCP presence |
|---|---|---|---|
| `claude` | settings.json hooks, transcript rename watch | `~/.claude.json` / `.mcp.json` `mcpServers` | yes (parent = claude) |
| `antigravity` (`agy`) | hooks.json hooks, TUI scanner, conversation db poll | `~/.gemini/config/mcp_config.json` | yes (parent = agy) |
| `codex` | hooks.json hooks (run in the shared app-server), TUI scanner, thread db poll | `config.toml` `[mcp_servers.agent-mesh]` | tools only (servers are hosted by the daemon) |
| `opencode` | plugin (`opencode.json` `plugin`) | `opencode.json` `mcp` | yes |
| `pi` | extension (`~/.pi/agent/extensions`) | `~/.pi/agent/mcp.json` | yes |

**Mail delivery.** Claude/Codex receive queued mail on the next prompt (and at turn end), Antigravity before each
model call, OpenCode and Pi are woken while idle (plugin/extension inject a turn). An idle Claude/Codex/Antigravity
TUI cannot be woken: the mesh raises a "message waiting" toast and the mail is delivered at its next prompt.
Address a specific session with `--to <agent>@<session name or id prefix>`.

Adding a harness is one descriptor file in `src/harnesses/` plus a registry line; see `docs/ADAPTERS.md`
("How to add a harness"). Design notes, MCP spawn behaviour per harness and the Codex app-server study live there too.

## Quick Start CLI

```powershell
# 1. One-step initialization: auto-discovers all harnesses with skill installed and starts broker
node scripts/mesh.mjs --init

# Alternatively: assign specific harness names
node scripts/mesh.mjs --init agy,claude
node scripts/mesh.mjs --init opencode,pi,codex
node scripts/mesh.mjs --init --project codex,pi   # project-local scope

# 2. Check mesh status and active agent sessions
node scripts/mesh.mjs status

# 3. Diagnose hook and plugin installation across all harnesses (or targeted ones)
node scripts/mesh.mjs hooks doctor
node scripts/mesh.mjs hooks doctor claude,agy

# 4. Send a non-blocking question to an agent (or a specific live session)
node scripts/mesh.mjs ask --to claude "Can you analyze the memory usage in src/broker.mjs?"
node scripts/mesh.mjs ask --to claude@<session-uuid> "Targeted instruction for specific terminal"

# 5. Announce an interactive session (or let hooks handle it)
node scripts/mesh.mjs announce --harness claude --session <uuid> --pid <pid>

# 6. Inspect an agent's (or the human's) mailbox
node scripts/mesh.mjs inbox claude
node scripts/mesh.mjs inbox human-cli --delivered

# 7. View an agent's live event stream
node scripts/mesh.mjs watch claude

# 8. Interactively attach to an agent session (acquires lease)
node scripts/mesh.mjs attach opencode

# 9. Cleanly remove hooks and stop daemon (auto-discovers or targeted)
node scripts/mesh.mjs --uninstall
node scripts/mesh.mjs --uninstall pi,opencode
```

## Agent Identity, Session Discovery & Routing
Broker-driven agent turns run with `MESH_AGENT`, `MESH_HOPS`, and `MESH_CONVERSATION` set, and the
coalesced prompt embeds the mesh CLI path plus reply instructions. Agents reply by invoking the
CLI (`mesh reply --ticket <id> --to <peer> "..."`); the CLI inherits `MESH_AGENT`/`MESH_HOPS`
from the environment, so hop budgets survive across `ask` chains, not just reply chains.
Human interactive sessions announce themselves via hooks (`src/hooks/presence-hook.mjs` for Claude,
`src/hooks/agy-presence-hook.mjs` for Antigravity), allowing peer agents to route directly to live terminal windows without synthetic placeholder IDs.

## Architecture & Specifications
See [SPEC.md](SPEC.md) for complete Architecture Decision Records (ADR 001–008), data models, and delivery contracts.
