---
name: open-pencil-design-editor
description: AI-native open-source Figma alternative with CLI, MCP server, and Vue SDK for reading/writing .fig files programmatically.
triggers:
  - open pencil design editor
  - figma alternative open source
  - open fig files programmatically
  - design editor cli typescript
  - mcp server for figma files
  - ai design editor self-hosted
  - open pencil cli commands
  - figma file scripting automation
---

# OpenPencil Design Editor

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

OpenPencil is an open-source, AI-native design editor that reads and writes native Figma (`.fig`) files, provides a headless CLI, an MCP server for AI agents, and a Vue SDK for building custom editors. It is MIT-licensed and runs in the browser, as a desktop app (Tauri/macOS/Windows/Linux), or fully headlessly.

---

## Installation

### Web app (no install)
Visit [app.openpencil.dev/demo](https://app.openpencil.dev/demo).

### Desktop (macOS)
```sh
brew install open-pencil/tap/open-pencil
```
Or download from [releases](https://github.com/open-pencil/open-pencil/releases/latest).

### CLI
```sh
bun add -g @open-pencil/cli
```

### MCP server
```sh
bun add -g @open-pencil/mcp
```

### Local development
```sh
git clone https://github.com/open-pencil/open-pencil
cd open-pencil
bun install
bun run dev          # Web app at localhost:1420
bun run tauri dev    # Desktop (requires Rust)
```

---

## CLI Reference

The `open-pencil` CLI operates on `.fig` files headlessly. When the desktop app is running, omit the file argument to connect to the live canvas via RPC.

### Inspect file structure

```sh
# Print the full node tree
open-pencil tree design.fig

# Find nodes by type
open-pencil find design.fig --type TEXT
open-pencil find design.fig --type FRAME

# Get a specific node by ID
open-pencil node design.fig --id 1:23

# File metadata
open-pencil info design.fig
```

### XPath queries

```sh
# All frames
open-pencil query design.fig "//FRAME"

# Frames narrower than 300px
open-pencil query design.fig "//FRAME[@width < 300]"

# Text nodes whose name contains "Button"
open-pencil query design.fig "//TEXT[contains(@name, 'Button')]"

# Nodes with rounded corners
open-pencil query design.fig "//*[@cornerRadius > 0]"

# Text inside sections
open-pencil query design.fig "//SECTION//TEXT"
```

### Export

```sh
# PNG (default)
open-pencil export design.fig

# JPG at 2x scale, quality 90
open-pencil export design.fig -f jpg -s 2 -q 90

# SVG
open-pencil export design.fig -f svg

# WEBP
open-pencil export design.fig -f webp

# JSX with Tailwind v4 utility classes
open-pencil export design.fig -f jsx --style tailwind
```

Example Tailwind output:
```html
<div className="flex flex-col gap-4 p-6 bg-white rounded-xl">
  <p className="text-2xl font-bold text-[#1D1B20]">Card Title</p>
  <p className="text-sm text-[#49454F]">Description text</p>
</div>
```

### Design token analysis

```sh
open-pencil analyze colors design.fig
open-pencil analyze typography design.fig
open-pencil analyze spacing design.fig
open-pencil analyze clusters design.fig   # Repeated structures / component candidates
```

### Scripting with Figma Plugin API (`eval`)

```sh
# Read: count children on the current page
open-pencil eval design.fig -c "figma.currentPage.children.length"

# Read: get all text node contents
open-pencil eval design.fig -c "figma.currentPage.findAll(n => n.type === 'TEXT').map(n => n.characters)"

# Write: set opacity of all selected nodes (-w writes back to file)
open-pencil eval design.fig -c "figma.currentPage.selection.forEach(n => n.opacity = 0.5)" -w

# Write: rename all frames on the page
open-pencil eval design.fig -c "figma.currentPage.findAll(n => n.type === 'FRAME').forEach((f, i) => f.name = 'Frame ' + i)" -w

# Connect to the live running desktop app (no file arg)
open-pencil eval -c "figma.currentPage.name"
open-pencil tree
open-pencil export -f png
```

All commands support `--json` for machine-readable output:
```sh
open-pencil find design.fig --type TEXT --json
open-pencil analyze colors design.fig --json
```

---

## MCP Server

The MCP server exposes 90 tools (87 core + 3 file management) for AI agents to read and write `.fig` files.

### Stdio (Claude Code, Cursor, Windsurf)

```sh
bun add -g @open-pencil/mcp
```

Add to your MCP client config (e.g. `~/.claude/mcp.json` or Cursor settings):
```json
{
  "mcpServers": {
    "open-pencil": {
      "command": "openpencil-mcp"
    }
  }
}
```

### HTTP server (scripts, CI)

```sh
openpencil-mcp-http
# Listens at http://localhost:3100/mcp
```

### Claude Code desktop integration

1. Install the ACP adapter:
   ```sh
   npm i -g @zed-industries/claude-agent-acp
   ```
2. Add MCP permission to `~/.claude/settings.json`:
   ```json
   {
     "permissions": {
       "allow": ["mcp__open-pencil"]
     }
   }
   ```
3. Open the desktop app → `Ctrl+J` → select **Claude Code** from the provider dropdown.

### Agent skill (quick setup)

```sh
npx skills add open-pencil/skills@open-pencil
```

---

## AI Chat (Built-in)

- Open with `⌘J` (macOS) or `Ctrl+J` (desktop/web).
- 87 tools: create shapes, set fills/strokes, manage auto-layout, work with components and variables, boolean operations, token analysis, asset export.
- Bring your own API key — no backend or account required.

### Supported providers

Configure via the provider dropdown in the chat panel:

| Provider | Env var |
|---|---|
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Google AI | `GOOGLE_AI_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Any compatible endpoint | Custom base URL |

---

## Real-time Collaboration

No server, no account. Peer-to-peer via WebRTC.

1. Click the **Share** button (top-right).
2. Share the generated URL: `app.openpencil.dev/share/<room-id>`.
3. Peers see live cursors, selections, and edits.
4. Click a peer's avatar to follow their viewport.

---

## Project Structure

```
packages/
  core/     @open-pencil/core  — engine: scene graph, renderer, layout, codec
  cli/      @open-pencil/cli   — headless CLI
  mcp/      @open-pencil/mcp   — MCP server (stdio + HTTP)
  docs/     Documentation site
src/        Vue 3 app — components, composables, stores
desktop/    Tauri v2 (Rust + config)
tests/      E2E (188 tests) + unit (764 tests)
```

### Tech stack

| Layer | Technology |
|---|---|
| Rendering | Skia (CanvasKit WASM) |
| Layout | Yoga WASM (flex + CSS Grid) |
| UI | Vue 3, Reka UI, Tailwind CSS 4 |
| File format | Kiwi binary + Zstd + ZIP |
| Collaboration | Trystero (WebRTC P2P) + Yjs (CRDT) |
| Desktop | Tauri v2 |
| AI/MCP | Anthropic, OpenAI, Google AI, OpenRouter; MCP SDK; Hono |

---

## Development Commands

```sh
bun run dev        # Start web dev server (localhost:1420)
bun run tauri dev  # Start desktop app (requires Rust)
bun run check      # Lint + typecheck
bun run test       # E2E visual regression tests
bun run test:unit  # Unit tests
bun run format     # Code formatting
bun run tauri build  # Production desktop build
```

Desktop prerequisites: [Rust](https://rustup.rs/) + [Tauri v2 platform deps](https://v2.tauri.app/start/prerequisites/).

---

## Common Patterns

### Batch-rename all text nodes in a .fig file

```sh
open-pencil eval design.fig \
  -c "figma.currentPage.findAll(n => n.type === 'TEXT').forEach((t, i) => t.name = 'Text_' + i)" \
  -w
```

### Extract all colors as JSON

```sh
open-pencil analyze colors design.fig --json > colors.json
```

### Export every frame as PNG in CI

```sh
for id in $(open-pencil find design.fig --type FRAME --json | jq -r '.[].id'); do
  open-pencil export design.fig --id "$id" -f png -o "frames/$id.png"
done
```

### Query nodes matching a naming convention

```sh
# Find all nodes named with a "btn-" prefix
open-pencil query design.fig "//*[starts-with(@name, 'btn-')]"
```

### Connect an MCP client to a running desktop app

When the desktop app is open, the MCP stdio server can connect to the live canvas. No file path needed — all reads and writes go to the open document.

```json
{
  "mcpServers": {
    "open-pencil": {
      "command": "openpencil-mcp"
    }
  }
}
```

### Export a selection as Tailwind JSX programmatically

```sh
open-pencil export design.fig --id 1:23 -f jsx --style tailwind
```

---

## Troubleshooting

**`openpencil-mcp` not found after install**
- Ensure `bun`'s global bin dir is on your `PATH`: `export PATH="$HOME/.bun/bin:$PATH"`
- Or use `npx openpencil-mcp` as the MCP command value.

**Desktop app CLI connection fails**
- The desktop app must be running before issuing commands without a file argument.
- Check that no firewall rule blocks the local RPC socket.

**Tauri dev build errors**
- Install platform prerequisites: [v2.tauri.app/start/prerequisites](https://v2.tauri.app/start/prerequisites/)
- Ensure Rust is up to date: `rustup update`

**`.fig` file won't open**
- Confirm the file was exported from Figma (not a `.fig` backup or plugin artifact).
- Run `open-pencil info design.fig` to check if the codec can parse the header.

**AI chat returns no response**
- Verify your API key is set correctly in the provider settings panel.
- For OpenRouter, ensure your key has credits and the selected model is available.

**Collaboration peers not connecting**
- Both peers must use the exact same share URL (room ID is case-sensitive).
- WebRTC requires both peers to allow the browser/app through any firewall.

---

## Links

- Web app: [app.openpencil.dev/demo](https://app.openpencil.dev/demo)
- Documentation: [openpencil.dev](https://openpencil.dev)
- MCP tools reference: [openpencil.dev/reference/mcp-tools](https://openpencil.dev/reference/mcp-tools)
- Releases: [github.com/open-pencil/open-pencil/releases](https://github.com/open-pencil/open-pencil/releases/latest)
- License: MIT
