---
name: open-pencil
description: Work with Figma .fig design files and the running OpenPencil editor — inspect structure, query nodes, analyze design tokens, export images/SVG/JSX, and modify designs programmatically. Use when asked to open, inspect, export, analyze, or edit .fig files, or to control the running OpenPencil app.
---

# OpenPencil

CLI and MCP server for .fig design files. Two modes of operation:

- **App mode** — connect to the running OpenPencil editor (omit the file argument)
- **Headless mode** — work with .fig files directly (pass a file path)

```bash
# App mode — operates on the document open in the editor
bun open-pencil tree

# Headless mode — operates on a .fig file
bun open-pencil tree design.fig
```

The app exposes an automation bridge on `http://127.0.0.1:7600` when running. The CLI auto-connects to it when no file path is provided.

## CLI Commands

### Inspect

```bash
# Document overview — pages, node counts, fonts
bun open-pencil info design.fig

# Node tree — shows hierarchy with types and sizes
bun open-pencil tree design.fig
bun open-pencil tree --page "Components" --depth 3  # app mode, specific page

# List pages
bun open-pencil pages design.fig

# Detailed node properties — fills, strokes, effects, layout, text
bun open-pencil node design.fig --id 1:23
bun open-pencil node --id 1:23  # app mode

# List design variables and collections
bun open-pencil variables design.fig
bun open-pencil variables --collection "Colors" --type COLOR
```

### Search

```bash
# Find by name (partial match, case-insensitive)
bun open-pencil find design.fig --name "Button"

# Find by type
bun open-pencil find --type FRAME                          # app mode
bun open-pencil find design.fig --type TEXT --page "Home"

# Combine filters
bun open-pencil find design.fig --name "Card" --type COMPONENT --limit 50
```

Node types: `FRAME`, `TEXT`, `RECTANGLE`, `ELLIPSE`, `VECTOR`, `GROUP`, `COMPONENT`, `COMPONENT_SET`, `INSTANCE`, `SECTION`, `LINE`, `STAR`, `POLYGON`, `SLICE`, `BOOLEAN_OPERATION`

### Export

```bash
# PNG (default)
bun open-pencil export design.fig -o hero.png
bun open-pencil export -o hero.png  # app mode — exports from running editor

# Specific node at 2x
bun open-pencil export design.fig --node 1:23 -s 2 -o button@2x.png

# JPG with quality
bun open-pencil export design.fig -f jpg -q 85 -o preview.jpg

# SVG
bun open-pencil export design.fig -f svg --node 1:23 -o icon.svg

# JSX (OpenPencil format — renderable back into .fig)
bun open-pencil export design.fig -f jsx -o component.jsx

# JSX (Tailwind — React component with Tailwind classes)
bun open-pencil export design.fig -f jsx --style tailwind -o component.tsx

# Page thumbnail
bun open-pencil export design.fig --thumbnail --width 1920 --height 1080

# Specific page
bun open-pencil export --page "Components" -o components.png
```

### Analyze

```bash
# Color palette — usage frequency, similar colors
bun open-pencil analyze colors design.fig
bun open-pencil analyze colors --similar --threshold 10  # app mode

# Typography — font families, sizes, weights
bun open-pencil analyze typography design.fig --group-by size

# Spacing — gap and padding values, grid compliance
bun open-pencil analyze spacing design.fig --grid 8

# Clusters — repeated patterns that could be components
bun open-pencil analyze clusters design.fig --min-count 3
```

### Eval (Figma Plugin API)

Execute JavaScript against the document using the full Figma Plugin API:

```bash
# Read-only — query the document
bun open-pencil eval design.fig -c 'figma.currentPage.findAll(n => n.type === "TEXT").length'

# App mode — modifies the live document in the editor
bun open-pencil eval -c '
  const buttons = figma.currentPage.findAll(n => n.name === "Button");
  buttons.forEach(b => { b.cornerRadius = 8 });
  buttons.length + " buttons updated"
'

# Modify and save to file
bun open-pencil eval design.fig -w -c '
  const texts = figma.currentPage.findAll(n => n.type === "TEXT");
  texts.forEach(t => { t.fontSize = 16 });
'

# Save to a different file
bun open-pencil eval design.fig -o modified.fig -c '...'

# Read code from stdin
echo 'figma.currentPage.children.map(n => n.name)' | bun open-pencil eval design.fig --stdin
```

The eval environment provides `figma` with the Figma Plugin API: `figma.currentPage`, `figma.createFrame()`, `figma.createText()`, `figma.getNodeById()`, etc.

### JSON Output

Every command supports `--json` for machine-readable output:

```bash
bun open-pencil info design.fig --json
bun open-pencil find --name "Button" --json  # app mode
bun open-pencil analyze colors design.fig --json
```

## MCP Server

### Stdio (Claude Desktop, Cursor)

Add to your MCP config:

```json
{
  "mcpServers": {
    "open-pencil": {
      "command": "npx",
      "args": ["openpencil-mcp"]
    }
  }
}
```

### HTTP (multi-session, remote)

```bash
export PORT=3100
export OPENPENCIL_MCP_AUTH_TOKEN=secret       # optional auth
export OPENPENCIL_MCP_CORS_ORIGIN="*"         # optional CORS
export OPENPENCIL_MCP_ROOT=/path/to/files     # restrict file access

npx openpencil-mcp-http
```

### MCP Workflow

1. **Open a file** — `open_file { path: "/path/to/design.fig" }` or `new_document {}`
2. **Query** — `get_page_tree`, `find_nodes`, `get_node`, `list_pages`, etc.
3. **Modify** — `render` (JSX), `set_fill`, `set_layout`, `create_shape`, etc.
4. **Save** — `save_file { path: "/path/to/output.fig" }`

### MCP Tools (86 total)

**Read (11):** `get_selection`, `get_page_tree`, `get_node`, `find_nodes`, `get_components`, `list_pages`, `switch_page`, `get_current_page`, `page_bounds`, `select_nodes`, `list_fonts`

**Create (7):** `create_shape`, `render`, `create_component`, `create_instance`, `create_page`, `create_vector`, `create_slice`

**Modify (19):** `set_fill`, `set_stroke`, `set_effects`, `update_node`, `set_layout`, `set_constraints`, `set_rotation`, `set_opacity`, `set_radius`, `set_min_max`, `set_text`, `set_font`, `set_font_range`, `set_text_resize`, `set_visible`, `set_blend`, `set_locked`, `set_stroke_align`, `set_text_properties`, `set_layout_child`

**Structure (16):** `delete_node`, `clone_node`, `rename_node`, `reparent_node`, `group_nodes`, `ungroup_node`, `flatten_nodes`, `node_to_component`, `node_bounds`, `node_move`, `node_resize`, `node_ancestors`, `node_children`, `node_tree`, `node_bindings`, `node_replace_with`, `arrange_nodes`

**Variables (11):** `list_variables`, `list_collections`, `get_variable`, `find_variables`, `create_variable`, `set_variable`, `delete_variable`, `bind_variable`, `get_collection`, `create_collection`, `delete_collection`

**Vector & Export (13):** `boolean_union`, `boolean_subtract`, `boolean_intersect`, `boolean_exclude`, `path_get`, `path_set`, `path_scale`, `path_flip`, `path_move`, `viewport_get`, `viewport_set`, `viewport_zoom_to_fit`, `export_svg`, `export_image`

**Analyze (7):** `analyze_colors`, `analyze_typography`, `analyze_spacing`, `analyze_clusters`, `diff_create`, `diff_show`, `eval`

**File (3):** `open_file`, `save_file`, `new_document`

### JSX Rendering (via `render` tool or `eval`)

Create entire component trees in one call:

```jsx
<Frame name="Card" w={320} h="hug" flex="col" gap={16} p={24} bg="#FFF" rounded={16}>
  <Text size={18} weight="bold">Title</Text>
  <Text size={14} color="#666">Description text</Text>
  <Frame flex="row" gap={8}>
    <Frame w={80} h={36} bg="#3B82F6" rounded={8} justify="center" items="center">
      <Text size={14} color="#FFF" weight="600">Action</Text>
    </Frame>
  </Frame>
</Frame>
```

**Elements:** `Frame`, `Rectangle`, `Ellipse`, `Text`, `Line`, `Star`, `Polygon`, `Vector`, `Group`, `Instance`

**Layout shorthands:**

| Prop | Meaning |
|------|---------|
| `w`, `h` | Width, height (number or `"hug"` / `"fill"`) |
| `flex` | `"row"` or `"col"` |
| `gap` | Item spacing |
| `p`, `px`, `py`, `pt`, `pr`, `pb`, `pl` | Padding |
| `justify` | `"start"`, `"center"`, `"end"`, `"between"` |
| `items` | `"start"`, `"center"`, `"end"` |
| `bg` | Fill color (hex) |
| `rounded` | Corner radius |
| `stroke`, `strokeWidth` | Stroke color and weight |
| `opacity` | 0–1 |
| `size`, `weight`, `font`, `color` | Text properties |

## Node IDs

Format: `session:local` (e.g., `1:23`). Get IDs from `find`, `tree`, or `node` commands.

## Tips

- Omit the file path to work with the document open in the running OpenPencil editor
- Start with `info` to understand the document structure
- Use `tree --depth 2` for a quick overview without overwhelming output
- Use `find --type COMPONENT` to discover reusable components
- Use `analyze colors --similar` to find near-duplicate colors to merge
- Export specific nodes with `--node` instead of full pages for faster results
- The `eval` command gives you the full Figma Plugin API for anything the CLI doesn't cover
- Use `--json` when piping output to other tools
- In app mode, `eval` modifications are reflected live in the editor
