---
name: claude-peers-mcp
description: Enable multiple Claude Code instances to discover each other and exchange messages in real-time via a local broker daemon and MCP server.
triggers:
  - "set up claude peers"
  - "let my claude instances talk to each other"
  - "install claude-peers mcp"
  - "send messages between claude sessions"
  - "multi-agent claude communication"
  - "list all running claude instances"
  - "claude peers messaging setup"
  - "coordinate multiple claude code sessions"
---

# claude-peers-mcp

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

claude-peers is an MCP server that lets multiple Claude Code instances running on the same machine discover each other and exchange messages in real-time. A local broker daemon (SQLite + HTTP on `localhost:7899`) handles peer registration and message routing; each session's MCP server pushes inbound messages directly into the Claude channel so they appear instantly.

## Installation

### 1. Clone and install dependencies

```bash
git clone https://github.com/louislva/claude-peers-mcp.git ~/claude-peers-mcp
cd ~/claude-peers-mcp
bun install
```

### 2. Register as a global MCP server

```bash
claude mcp add --scope user --transport stdio claude-peers -- bun ~/claude-peers-mcp/server.ts
```

Adjust the path if you cloned elsewhere.

### 3. Launch Claude Code with the channel enabled

```bash
claude --dangerously-skip-permissions --dangerously-load-development-channels server:claude-peers
```

Add a shell alias to avoid typing it every time:

```bash
# ~/.bashrc or ~/.zshrc
alias claudepeers='claude --dangerously-load-development-channels server:claude-peers'
```

The broker daemon starts automatically on first use. No manual daemon management needed.

## Requirements

- [Bun](https://bun.sh) runtime
- Claude Code v2.1.80+
- claude.ai login (channels require it — API key auth does **not** work)

## Architecture

```
                    ┌───────────────────────────┐
                    │  broker daemon            │
                    │  localhost:7899 + SQLite  │
                    └──────┬───────────────┬────┘
                           │               │
                      MCP server A    MCP server B
                      (stdio)         (stdio)
                           │               │
                      Claude A         Claude B
```

- Each Claude Code session spawns its own `server.ts` MCP process over stdio
- MCP servers register with the broker and poll every second
- Inbound messages are pushed via the `claude/channel` protocol for instant delivery
- The broker auto-cleans dead peers and is localhost-only

## MCP Tools Reference

| Tool | Description |
|---|---|
| `list_peers` | Discover other Claude Code instances; scope: `machine`, `directory`, or `repo` |
| `send_message` | Send a message to a peer by ID — delivered instantly via channel push |
| `set_summary` | Set a description of what this instance is working on |
| `check_messages` | Manually poll for messages (fallback without channel mode) |

### Example prompts to Claude

```
List all peers on this machine
```

```
Send a message to peer abc123: "what files are you editing right now?"
```

```
Set your summary to: "refactoring the authentication module"
```

```
Check for any new messages from peers
```

## CLI Usage

Inspect and interact with the broker directly from the terminal:

```bash
cd ~/claude-peers-mcp

# Show broker status and all registered peers
bun cli.ts status

# List peers in a table
bun cli.ts peers

# Send a message into a specific Claude session
bun cli.ts send <peer-id> "your message here"

# Stop the broker daemon
bun cli.ts kill-broker
```

## Configuration

Set these environment variables before starting Claude Code:

| Variable | Default | Description |
|---|---|---|
| `CLAUDE_PEERS_PORT` | `7899` | Port the broker listens on |
| `CLAUDE_PEERS_DB` | `~/.claude-peers.db` | Path to the SQLite database |
| `OPENAI_API_KEY` | — | Enables auto-summary via `gpt-4o-mini` on startup |

```bash
export CLAUDE_PEERS_PORT=7899
export CLAUDE_PEERS_DB=~/.claude-peers.db
export OPENAI_API_KEY=$OPENAI_API_KEY  # optional — enables auto-summary
```

## Auto-Summary Feature

With `OPENAI_API_KEY` set, each instance generates a brief summary on startup describing what you're likely working on (based on working directory, git branch, recent files). Other peers see this in `list_peers` output. Without the key, Claude sets its own summary via `set_summary`.

## Common Patterns

### Cross-project coordination

Start two sessions in different project directories:

```bash
# Terminal 1 — in ~/projects/backend
claudepeers

# Terminal 2 — in ~/projects/frontend
claudepeers
```

Ask Claude in Terminal 1:
```
List peers scoped to machine, then ask the peer in the frontend project what API endpoints it needs
```

### Scope-filtered peer discovery

```
List peers scoped to repo
```
Shows only instances running in the same git repository — useful when you have worktrees or split terminals on the same codebase.

### Scripted message injection via CLI

```bash
# Inject a task into a running Claude session from a shell script
PEER_ID=$(bun ~/claude-peers-mcp/cli.ts peers | grep 'backend' | awk '{print $1}')
bun ~/claude-peers-mcp/cli.ts send "$PEER_ID" "run the test suite and report failures"
```

### Polling fallback (no channel mode)

If you launch without `--dangerously-load-development-channels`, Claude can still receive messages by calling `check_messages` explicitly:

```
Check for any new peer messages
```

## Troubleshooting

**Broker not starting**
```bash
# Check if something is already on port 7899
lsof -i :7899

# Kill a stuck broker and restart
bun ~/claude-peers-mcp/cli.ts kill-broker
# Then relaunch Claude Code
```

**Peers not appearing in `list_peers`**
- Ensure both sessions were started with `--dangerously-load-development-channels server:claude-peers`
- Confirm both use the same `CLAUDE_PEERS_PORT` (default `7899`)
- Run `bun cli.ts status` to verify the broker sees both registrations

**Messages not arriving instantly**
- Channel push requires claude.ai login; API key auth won't work
- Fall back to `check_messages` tool if channels are unavailable

**Auto-summary not generating**
- Verify `OPENAI_API_KEY` is exported in the shell where Claude Code was launched: `echo $OPENAI_API_KEY`
- The feature uses `gpt-4o-mini`; confirm your key has access

**Database issues**
```bash
# Reset the database entirely (all peers/messages lost)
rm ~/.claude-peers.db
bun ~/claude-peers-mcp/cli.ts kill-broker
```

**MCP server not found after registration**
```bash
# Verify registration
claude mcp list

# Re-register if missing
claude mcp add --scope user --transport stdio claude-peers -- bun ~/claude-peers-mcp/server.ts
```
