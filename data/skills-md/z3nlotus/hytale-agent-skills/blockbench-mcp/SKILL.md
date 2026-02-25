---
name: blockbench-mcp
description: Setting up Model Context Protocol (MCP) integration between Blockbench and Claude AI for AI-assisted 3D modeling. Use when configuring BlockbenchMCP, connecting Claude to Blockbench, troubleshooting MCP connection issues, or enabling AI-powered model creation and manipulation.
---

# Blockbench MCP Integration

Connect Blockbench to Claude AI via Model Context Protocol for AI-assisted 3D modeling.

## Overview

BlockbenchMCP enables Claude to directly interact with and control Blockbench, allowing:
- AI-assisted 3D model creation
- Texture application and manipulation
- Real-time model modifications
- Automated modeling operations

**Repository**: [github.com/enfp-dev-studio/blockbench-mcp](https://github.com/enfp-dev-studio/blockbench-mcp)

## Prerequisites

- **Blockbench** 4.0 or newer
- **Node.js** 18.0 or newer
- **pnpm** package manager

## Installation

### Step 1: Install pnpm

```bash
npm install -g pnpm
```

### Step 2: Clone and Build

```bash
git clone https://github.com/enfp-dev-studio/blockbench-mcp.git
cd blockbench-mcp
pnpm install
pnpm build
```

### Step 3: Build the Blockbench Plugin

```bash
cd apps/mcp-plugin
pnpm build
```

### Step 4: Install Plugin in Blockbench

1. Open Blockbench
2. Go to **File → Plugins → Load Plugin from File**
3. Select plugin from `apps/mcp-plugin/dist/`
4. Enable by checking "MCP Plugin"

---

## Configuring MCP Client

### Option A: Antigravity (Recommended for this workspace)

Antigravity has native MCP support! Configure it directly in your workspace:

**Method 1: Via UI**
1. In Antigravity, go to **Agent Session → MCP Servers → Manage MCP Servers**
2. Add a new MCP server with the blockbench configuration

**Method 2: Via Config File**

Create `.mcp.json` in your workspace root (`e:\Hytale Modding\.mcp.json`):

```json
{
  "mcpServers": {
    "blockbench": {
      "command": "node",
      "args": [
        "C:/path/to/blockbench-mcp/apps/mcp-server/dist/index.js"
      ]
    }
  }
}
```

Replace `C:/path/to/blockbench-mcp` with your actual installation path.

After configuration, Claude in Antigravity will have direct access to Blockbench tools!

---

### Option B: Claude Desktop

Add to Claude Desktop config:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "blockbench": {
      "command": "node",
      "args": [
        "/path/to/blockbench-mcp/apps/mcp-server/dist/index.js"
      ]
    }
  }
}
```

---

## Usage

### Starting the Connection

1. In Blockbench, open **View → Panels**
2. Find "MCP Plugin" panel
3. Click **"Connect to MCP Server"**
4. Plugin listens on **port 9999**

### Capabilities

Once connected, Claude can:
- Get model and project information
- Create, delete, and modify block models
- Apply textures and materials
- Execute custom modeling operations
- Track command history in real-time

### Example Prompts for Claude

```
"Create a simple sword model with proper proportions"
"Add a crossguard to the existing sword model"
"Create a chest model with opening animation"
"Generate a pickaxe tool with different material variants"
"Show me the current model structure and elements"
"Create a character head with facial features"
```

## Architecture

```
Claude AI ← MCP Protocol → MCP Server ← Socket.IO → Blockbench Plugin
```

- **Socket.IO** for real-time communication
- **WebSocket** on port 9999
- **JSON-based** commands with type/payload structure
- **Event-driven** architecture

## Project Structure

```
blockbench-mcp/
├── apps/
│   ├── mcp-server/     # MCP server (Node.js)
│   └── mcp-plugin/     # Blockbench plugin
└── packages/
    └── shared/         # Shared TypeScript types
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection issues | Ensure Blockbench plugin running, MCP server configured |
| Port conflicts | Port 9999 in use - close conflicting apps |
| Plugin not loading | Verify build successful, Blockbench version compatible |
| Command timeouts | Simplify requests, break into smaller steps |
| No tools in Antigravity | Check .mcp.json path is correct, restart Antigravity |
| No hammer icon in Claude Desktop | Restart Claude Desktop after config change |
