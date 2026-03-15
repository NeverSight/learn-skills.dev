---
name: antigravity-mcp
description: Use when Antigravity MCP is available locally and you want to query workspaces, check quota, run lightweight Antigravity asks, or generate images through the local antigravity-mcp-server.
---

# antigravity-mcp

Use the local Antigravity MCP server for lightweight asks, workspace inspection, and image generation.

## Features

- 🔌 **Direct MCP Connection** - Connects directly to antigravity-mcp-server
- 🖼️ **Image Generation** - Generate images via Antigravity AI
- 📊 **Code Analysis** - Analyze project code and architecture
- 🔄 **Async Support** - Full asyncio implementation
- 🛡️ **Error Handling** - Comprehensive error handling and logging

## Prerequisites

```bash
# 1. Antigravity MCP Server must be installed
ls ~/.config/antigravity-mcp/bin/antigravity-mcp-server

# 2. Python 3.8+ with asyncio
python3 --version  # >= 3.8
```

## Installation

```bash
# Skill is automatically discovered by OpenClaw
# Place in: ~/.agents/skills/antigravity-mcp/

# Verify installation
openclaw skills list | grep antigravity
```

## Usage

### Command Line

```bash
# Ping MCP server
python3 ~/.agents/skills/antigravity-mcp/scripts/antigravity_cli.py ping

# List available tools
python3 ~/.agents/skills/antigravity-mcp/scripts/antigravity_cli.py list-tools

# List known workspaces (prefers local registry)
python3 ~/.agents/skills/antigravity-mcp/scripts/antigravity_cli.py list-workspaces

# Check quota
python3 ~/.agents/skills/antigravity-mcp/scripts/antigravity_cli.py quota-status

# Ask Antigravity to generate/analyze
python3 ~/.agents/skills/antigravity-mcp/scripts/antigravity_cli.py ask \
  "生成一张太空猫咪的图片，穿着宇航服，背景是地球和星空"

# Specify output path for image tasks
python3 ~/.agents/skills/antigravity-mcp/scripts/antigravity_cli.py ask \
  "画一只可爱的猫" -o ~/Desktop/cat.png
```

### As OpenClaw Tool

```python
# In an OpenClaw conversation or script
from antigravity_mcp import AntigravityMCPClient

client = AntigravityMCPClient()
await client.connect()

# Generate image
result = await client.ask_antigravity(
    "生成一张架构图，展示微服务系统的数据流",
    output_path="/tmp/architecture.png"
)

await client.disconnect()
```

### Available Actions

| Action | Description | Example |
|--------|-------------|---------|
| `ask-antigravity` | Send prompt to Antigravity AI | Generate images, analyze code, answer questions |
| `antigravity-stop` | Stop running generation | Cancel long-running tasks |
| `ping` | Test connectivity | Check if server is ready |
| `list-workspaces` | List available workspaces | See available project contexts |
| `quota-status` | Check quota | Verify usage limits |
| `launch-antigravity` | Launch Antigravity | Start Antigravity with CDP |

## Architecture

```
┌─────────────────────────────────────────────┐
│         OpenClaw Agent / CLI                │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│   antigravity-mcp Skill (Python/Asyncio)    │
│   ┌─────────────────────────────────────┐   │
│   │  AntigravityMCPClient               │   │
│   │  ├─ connect()                       │   │
│   │  ├─ ask_antigravity()               │   │
│   │  ├─ list_tools()                    │   │
│   │  └─ disconnect()                    │   │
│   └─────────────────────────────────────┘   │
└──────────────────┬──────────────────────────┘
                   │ stdio (JSON-RPC)
┌──────────────────▼──────────────────────────┐
│   antigravity-mcp-server (binary)           │
└──────────────────┬──────────────────────────┘
                   │ CDP / WebSocket / HTTP
┌──────────────────▼──────────────────────────┐
│        Antigravity AI Service               │
│   (Image Generation, Code Analysis, etc.)   │
└─────────────────────────────────────────────┘
```

## Troubleshooting

### Server not found
```bash
# Check if antigravity-mcp is installed
ls ~/.config/antigravity-mcp/bin/antigravity-mcp-server

# If not found, install Antigravity app first
# (Antigravity should install MCP server automatically)
```

### Connection timeout
```bash
# Check if server is already running
ps aux | grep antigravity-mcp-server

# Check logs
tail ~/.config/antigravity-mcp/logs/latest.log
```

### Image generation fails
- Verify Antigravity app has necessary permissions
- Check quota status: use `quota-status` action
- Ensure prompt is not blocked by safety filters

## Contributing

This Skill is designed to be:
- **Modular**: Easy to extend with new actions
- **Maintainable**: Clear error handling and logging
- **Compatible**: Works with OpenClaw ecosystem

## License

MIT - OpenClaw Agent
