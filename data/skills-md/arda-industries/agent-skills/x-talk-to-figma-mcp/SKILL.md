---
name: x-talk-to-figma-mcp
description: Reliable workflow for using the local TalkToFigma MCP server (Cursor ↔ Figma plugin via WebSocket relay).
---

This workspace includes a local MCP server ("TalkToFigma") that talks to a Figma plugin via a local WebSocket relay.

## Mental model

- **Figma plugin** connects to a local WebSocket server (default `localhost:3055`) and joins a channel (by default: `cursor`).
- **TalkToFigma MCP server** connects to the same WebSocket server and joins the same channel.
- **Cursor** calls MCP tools; the MCP server forwards commands to the plugin; the plugin applies them to the open Figma file.

If any of the 3 pieces isn't running/connected, tool calls will fail or appear to do nothing.

## One-time setup

### 1. Add the MCP server to Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "TalkToFigma": {
      "command": "bun",
      "args": [
        "/Users/audaciousaspen/brain/git/personal/cursor-talk-to-figma-mcp/src/talk_to_figma_mcp/server.ts"
      ],
      "disabled": false
    }
  }
}
```

Restart Cursor or reload MCP servers. Confirm TalkToFigma shows as connected (green dot) in Cursor Settings → MCP.

### 2. Install the Figma plugin (local development plugin)

In Figma:
1. Click **Plugins → Development → Import plugin from manifest...**
2. Select: `~/brain/git/personal/cursor-talk-to-figma-mcp/src/cursor_mcp_plugin/manifest.json`

This registers the plugin locally. You only need to do this once per machine.

## Per-session startup

### 1. Start the WebSocket relay

```bash
cd ~/brain/git/personal/cursor-talk-to-figma-mcp
bun socket
```

Keep this running in a terminal. It listens on port 3055.

### 2. Run the plugin in Figma

1. Open the Figma file you want to work with
2. Click **Plugins → Development → Cursor MCP Plugin**
3. Confirm the plugin panel shows: "Connected to server on port 3055 in channel: cursor"

## Preconditions (must be true before using tools)

- The WebSocket relay is running (`bun socket`)
- In Figma, the plugin is open and shows **Connected** to port `3055` in channel `cursor`
- In Cursor, the MCP server **TalkToFigma** is enabled/connected (green dot)

## First step: join the channel

Always join the channel before sending commands (or when reconnecting):

- Tool: `join_channel`
- Args: `channel: "cursor"` (or whatever the plugin is using)

## Creating a "hello world" rectangle (example)

- Tool: `create_rectangle`
- Args:
  - `x`, `y`, `width`, `height` (required)
  - `name` (optional)

Typical example:
- `x: 100`, `y: 100`, `width: 240`, `height: 120`, `name: "hello world"`

## Adding centered text inside a rectangle (reliable workflow)

There isn't a single "center text in shape" command, so do it deterministically:

1) **Find the rectangle bounds**
- Tool: `get_nodes_info`
- Args: `nodeIds: ["<RECT_ID>"]`
- Use `absoluteBoundingBox` → `{ x, y, width, height }`

2) **Create the text**
- Tool: `create_text`
- Args (minimum):
  - `x`, `y` (temporary; can be top-left of the rectangle)
  - `text: "hello world"`
- Optional but useful:
  - `fontSize` (e.g. 24)
  - `fontWeight` (e.g. 600)
  - `name` (e.g. `"hello world label"`)

3) **Measure the text**
- Tool: `get_nodes_info`
- Args: `nodeIds: ["<TEXT_ID>"]`
- Use its `absoluteBoundingBox` → `{ width, height }`

4) **Move the text to center**
- Tool: `move_node`
- Args:
  - `nodeId: "<TEXT_ID>"`
  - `x: rectX + (rectW - textW)/2`
  - `y: rectY + (rectH - textH)/2`

This produces a visually centered result without guessing.

## Debugging checklist (fast)

- If calls fail with "must join channel" or timeouts:
  - Run `join_channel` again (use the plugin's channel name).
- If calls succeed but nothing changes in Figma:
  - Confirm the plugin panel still shows connected to the same port and channel.
  - Confirm you're editing the intended file/page in Figma.
- If Cursor can't see the tools or they error immediately:
  - Check Cursor MCP settings: TalkToFigma enabled/connected.
  - Restart the MCP server and/or Cursor if it's stuck.

