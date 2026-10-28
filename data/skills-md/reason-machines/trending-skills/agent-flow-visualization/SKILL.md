---
name: agent-flow-visualization
description: VS Code extension for real-time visualization of Claude Code agent orchestration as interactive node graphs
triggers:
  - visualize claude code agents
  - debug agent tool calls
  - see agent execution graph
  - monitor claude code sessions
  - agent flow vscode extension
  - watch agents think and branch
  - trace agent tool call chains
  - configure claude code hooks for visualization
---

# Agent Flow

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Agent Flow is a VS Code extension that provides real-time visualization of Claude Code agent orchestration. It renders agent execution as an interactive node graph, showing tool calls, branching, subagent coordination, and timing — turning Claude Code's black-box execution into a transparent, debuggable flow.

## Installation

### Via VS Code Marketplace

1. Open VS Code Extensions (`Cmd+Shift+X`)
2. Search for **Agent Flow** by simon-p
3. Click Install

Or install directly: [marketplace.visualstudio.com/items?itemName=simon-p.agent-flow](https://marketplace.visualstudio.com/items?itemName=simon-p.agent-flow)

### Requirements

- VS Code 1.85 or later
- Claude Code CLI installed and accessible
- Node.js (for Claude Code)

## Quick Start

```
# 1. Open Command Palette
Cmd+Shift+P (Mac) / Ctrl+Shift+P (Win/Linux)

# 2. Run the command
> Agent Flow: Open Agent Flow

# 3. Start a Claude Code session in your workspace
# Agent Flow auto-detects it and begins streaming
```

Or use the keyboard shortcut:
- **Mac**: `Cmd+Alt+A`
- **Win/Linux**: `Ctrl+Alt+A`

## Commands

| Command | Description |
|---------|-------------|
| `Agent Flow: Open Agent Flow` | Open visualizer in current editor column |
| `Agent Flow: Open Agent Flow to Side` | Open in a side editor column |
| `Agent Flow: Connect to Running Agent` | Manually connect to a specific agent session |
| `Agent Flow: Configure Claude Code Hooks` | Set up Claude Code hooks for live event streaming |

## Configuration

Settings available in VS Code settings (`settings.json`):

```jsonc
{
  // Path to a JSONL event log file to watch/replay
  "agentVisualizer.eventLogPath": "/path/to/agent-events.jsonl",

  // Auto-open the visualizer when an agent session starts
  "agentVisualizer.autoOpen": true,

  // Development server port (0 = production mode, use built assets)
  "agentVisualizer.devServerPort": 0
}
```

### Auto-Open on Agent Start

```jsonc
// settings.json
{
  "agentVisualizer.autoOpen": true
}
```

## Claude Code Hooks Setup

Agent Flow uses Claude Code's hook system for zero-latency event streaming. Hooks are configured automatically on first open, but you can reconfigure manually.

### Automatic Configuration

Run from Command Palette:
```
> Agent Flow: Configure Claude Code Hooks
```

### Manual Hook Configuration

If you need to configure hooks manually, Agent Flow starts a local HTTP server that receives events. The hooks forward Claude Code lifecycle events (tool calls, responses, session start/end) to the extension.

Claude Code hooks are configured in `~/.claude/settings.json` or project-level `.claude/settings.json`:

```jsonc
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "curl -s -X POST http://localhost:PORT/hook -H 'Content-Type: application/json' -d @-"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "curl -s -X POST http://localhost:PORT/hook -H 'Content-Type: application/json' -d @-"
          }
        ]
      }
    ]
  }
}
```

> Agent Flow manages this configuration automatically — prefer using the command palette command.

## JSONL Event Log Mode

For replaying past sessions or watching log files generated outside VS Code:

```jsonc
// settings.json
{
  "agentVisualizer.eventLogPath": "${workspaceFolder}/logs/agent-session.jsonl"
}
```

Agent Flow tails the file and visualizes events as they arrive. Use this for:
- Post-hoc debugging of agent runs
- Sharing agent execution recordings with teammates
- CI/CD pipeline agent monitoring

### JSONL Event Format

Each line in the log file is a JSON event object:

```jsonl
{"type":"session_start","sessionId":"abc123","timestamp":"2026-03-21T10:00:00Z","model":"claude-opus-4-5"}
{"type":"tool_use","sessionId":"abc123","toolName":"bash","input":{"command":"ls -la"},"timestamp":"2026-03-21T10:00:01Z"}
{"type":"tool_result","sessionId":"abc123","toolName":"bash","output":"total 48\n...","timestamp":"2026-03-21T10:00:02Z"}
{"type":"message","sessionId":"abc123","role":"assistant","content":"I can see the files...","timestamp":"2026-03-21T10:00:03Z"}
```

## Multi-Session Support

Agent Flow tracks multiple concurrent Claude Code sessions with tabs. Each session gets its own visualization canvas.

```
# Start multiple Claude Code sessions in different terminals
# Each appears as a separate tab in Agent Flow
# Click tabs to switch between session graphs
```

## Interactive Canvas Features

### Navigation
- **Pan**: Click and drag on empty canvas
- **Zoom**: Scroll wheel / pinch gesture
- **Select node**: Click any agent or tool call node to inspect details
- **Reset view**: Double-click empty canvas

### Node Types in the Graph

| Node Type | Visual | Description |
|-----------|--------|-------------|
| Agent/Subagent | Circle | Claude instance making decisions |
| Tool Call | Rectangle | Individual tool invocation (bash, read_file, etc.) |
| Tool Result | Rectangle (dashed) | Output returned from tool |
| Branch | Diamond | Decision point spawning subagents |
| Return | Arrow | Subagent returning result to parent |

### Panels

- **Timeline**: Chronological view of all events with durations
- **Transcript**: Full message history between agent and tools
- **File Heatmap**: Which files received the most attention

## Contributing / Development Setup

```bash
git clone https://github.com/patoles/agent-flow
cd agent-flow
npm install

# Build the extension
npm run build

# Watch mode for development
npm run watch

# Run with dev server (hot reload)
# Set in settings: "agentVisualizer.devServerPort": 3000
npm run dev
```

### Extension Structure

```
agent-flow/
├── src/
│   ├── extension.ts          # VS Code extension entry point
│   ├── hookServer.ts         # HTTP server receiving Claude Code hook events
│   ├── sessionManager.ts     # Manages multiple agent sessions
│   ├── webviewProvider.ts    # Webview panel management
│   └── logWatcher.ts         # JSONL file tail watcher
├── webview/
│   ├── src/
│   │   ├── App.tsx           # Main React app
│   │   ├── Graph.tsx         # Node graph canvas (likely D3 or React Flow)
│   │   ├── Timeline.tsx      # Timeline panel
│   │   └── Transcript.tsx    # Message transcript panel
│   └── package.json
└── package.json              # Extension manifest
```

## Common Patterns

### Pattern: Debug a Failing Agent Run

1. Open Agent Flow (`Cmd+Alt+A`)
2. Run your Claude Code command that's failing
3. Watch the graph — look for:
   - Red/error nodes indicating failed tool calls
   - Unexpected branching
   - Loops (agent retrying the same tool)
4. Click the failed tool node to inspect input/output
5. Check the Timeline panel for which tool call took unexpectedly long

### Pattern: Replay a Saved Session

```bash
# Save Claude Code output to JSONL during a run
# (depends on your Claude Code version/config)
claude --output-format jsonl > session-$(date +%s).jsonl

# Point Agent Flow at it
```

```jsonc
// .vscode/settings.json (project-level)
{
  "agentVisualizer.eventLogPath": "./logs/session-1234567890.jsonl"
}
```

### Pattern: Auto-Visualize All Agent Sessions

```jsonc
// settings.json
{
  "agentVisualizer.autoOpen": true
}
```

Now every time a Claude Code session starts in your workspace, Agent Flow opens automatically.

### Pattern: Side-by-Side Coding and Visualization

```
# Open Agent Flow to side so you can code and watch simultaneously
Cmd+Shift+P > Agent Flow: Open Agent Flow to Side
```

This opens the visualizer in a split editor, keeping your code files accessible in the main editor group.

## Troubleshooting

### Agent Flow doesn't detect my Claude Code session

1. Verify Claude Code is running in the same workspace folder
2. Check that hooks are configured: run `Agent Flow: Configure Claude Code Hooks`
3. Verify the hook server is running — look for "Agent Flow hook server listening" in the Output panel (`View > Output > Agent Flow`)
4. Try `Agent Flow: Connect to Running Agent` to manually specify the session

### Hooks aren't forwarding events

```bash
# Test the hook server manually
curl -X POST http://localhost:PORT/hook \
  -H 'Content-Type: application/json' \
  -d '{"type":"test","sessionId":"test123"}'
```

Check VS Code Output panel for the correct PORT value.

### Graph is empty / not updating

1. Check `agentVisualizer.eventLogPath` — if set, Agent Flow reads from file instead of hooks
2. Clear the setting if you want live hook-based streaming:
   ```jsonc
   { "agentVisualizer.eventLogPath": "" }
   ```
3. Reload VS Code window (`Cmd+Shift+P > Developer: Reload Window`)

### Extension not loading

```bash
# Check VS Code version meets requirement
code --version
# Must be 1.85 or later

# Check extension is enabled
# Extensions panel > search "Agent Flow" > verify enabled
```

### Multiple sessions showing in wrong tabs

Each session is identified by a unique session ID from Claude Code. If sessions are merging incorrectly, check that each `claude` process is started fresh (not reusing an existing session ID).

## Resources

- [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=simon-p.agent-flow)
- [Demo Video](https://www.youtube.com/watch?v=Ud6eDrFN-TA)
- [GitHub Repository](https://github.com/patoles/agent-flow)
- [CraftMyGame](https://craftmygame.com) — the project that inspired Agent Flow
- [License: Apache 2.0](https://github.com/patoles/agent-flow/blob/main/LICENSE)
