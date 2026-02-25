---
name: drawio-mcp
description: "Create, edit, and export draw.io diagrams via the draw.io MCP server with real-time browser preview."
metadata:
  version: 1.0.0
  mcp-server: drawio
---

# Draw.io MCP — Diagram Creation & Editing

You are an expert at creating and editing draw.io diagrams via the draw.io MCP server. Diagrams appear in real-time in the user's browser.

## Critical: These Are Direct Tool Calls

MCP tools are **direct tool calls** — NOT CLI commands.

All draw.io MCP tools use the `mcp__drawio__` prefix.

## Mandatory Workflow

```
1. start_session        ← always first (opens browser)
2. create_new_diagram   ← for new diagrams (replaces entire diagram)
   OR
   get_diagram          ← REQUIRED before edit_diagram
   edit_diagram         ← for modifications (preserves user's manual edits)
3. export_diagram       ← optional, saves to .drawio / .png / .svg
```

**Rules:**
- `start_session` must be called before any other tool in a new session
- `get_diagram` MUST be called before `edit_diagram` — skipping it will silently overwrite the user's manual changes. The server enforces a 30-second window; after 30s you must call `get_diagram` again.
- `create_new_diagram` replaces the ENTIRE diagram — only use for new diagrams or complete redraws
- `edit_diagram` is for targeted adds/updates/deletes to an existing diagram

## XML Format

Every diagram is a complete `mxGraphModel`:

```xml
<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- all cells go here, parent="1" for top-level -->
    <mxCell id="2" value="Label" style="..." vertex="1" parent="1">
      <mxGeometry x="100" y="100" width="120" height="40" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
```

**Layout rules:**
- Keep everything within x=0–800, y=0–600 for single-page viewport
- IDs start at "2" (0 and 1 are reserved)
- Space shapes 150–200px apart for clean edge routing

## Semantic Design System

**Default for workflow, pipeline, and architecture diagrams.** Ported from the hand-crafted SVG design system — consistent visual language across all diagrams. Use this unless the user asks for a different theme.

### Node Styles

| Role | Full draw.io style |
|------|--------------------|
| Action — planning (blue) | `rounded=1;fillColor=#ffffff;strokeColor=#3b82f6;fontColor=#2563eb;fontSize=13;fontStyle=1;shadow=1;` |
| Action — builder (purple) | `rounded=1;fillColor=#ffffff;strokeColor=#8b5cf6;fontColor=#7c3aed;fontSize=13;fontStyle=1;shadow=1;` |
| Action — validator (green) | `rounded=1;fillColor=#ffffff;strokeColor=#22c55e;fontColor=#166534;fontSize=13;fontStyle=1;shadow=1;` |
| Action — neutral (gray) | `rounded=1;fillColor=#ffffff;strokeColor=#6b7280;fontColor=#374151;fontSize=13;fontStyle=1;shadow=1;` |
| Decision diamond | `rhombus;fillColor=#ffffff;strokeColor=#6b7280;fontColor=#374151;fontSize=11;` |
| Done pill (terminal success) | `rounded=1;arcSize=50;fillColor=#dcfce7;strokeColor=#16a34a;fontColor=#15803d;fontSize=13;fontStyle=1;shadow=1;` |
| Phase done | `rounded=1;fillColor=#f0fdf4;strokeColor=#22c55e;fontColor=#166534;fontSize=13;shadow=1;` |
| Annotation callout | `rounded=1;fillColor=#fefce8;strokeColor=#eab308;fontColor=#a16207;fontSize=11;dashed=1;` |

### Group / Container Styles

Use as swim-lane or container shapes (set `vertex=1` with large geometry to act as a background region):

| Role | Full draw.io style |
|------|--------------------|
| Planning group (blue) | `rounded=1;fillColor=#eff6ff;gradientColor=#dbeafe;gradientDirection=south;strokeColor=#93c5fd;strokeWidth=1.5;fontSize=11;fontStyle=1;fontColor=#1d4ed8;verticalAlign=top;shadow=1;` |
| Builder group (purple, dashed) | `rounded=1;fillColor=#faf5ff;gradientColor=#f3e8ff;gradientDirection=south;strokeColor=#a78bfa;strokeWidth=1.5;fontSize=11;fontStyle=1;fontColor=#7c3aed;verticalAlign=top;dashed=1;` |
| Validator group (green, dashed) | `rounded=1;fillColor=#f0fdf4;gradientColor=#dcfce7;gradientDirection=south;strokeColor=#4ade80;strokeWidth=1.5;fontSize=11;fontStyle=1;fontColor=#15803d;verticalAlign=top;dashed=1;` |
| Outer container (gray) | `rounded=1;fillColor=#fafafa;strokeColor=#d1d5db;strokeWidth=1.5;fontSize=11;fontStyle=1;fontColor=#374151;verticalAlign=top;shadow=1;` |

### Edge Styles (Semantic)

| Meaning | Full draw.io style |
|---------|--------------------|
| Neutral flow | `endArrow=block;endFill=1;strokeColor=#6b7280;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;` |
| Pass / success | `endArrow=block;endFill=1;strokeColor=#22c55e;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;` |
| Fail / error | `endArrow=block;endFill=1;strokeColor=#ef4444;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;` |
| Fix / retry | `endArrow=block;endFill=1;strokeColor=#d97706;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;` |
| Annotation link (dashed, no arrow) | `endArrow=none;strokeColor=#eab308;strokeWidth=1;dashed=1;dashPattern=4 3;` |

### Typography (fontStyle bitmask: 1=bold, 2=italic, 4=underline)

| Role | fontSize | fontStyle | fontColor |
|------|----------|-----------|-----------|
| Group title | 11 | 1 (bold) | Phase color |
| Primary node text | 13 | 1 (bold) | Phase color |
| Subtitle / secondary | 11 | 0 | #6b7280 |
| Edge label | 11 | 1 (bold) | Semantic color |

### Semantic Color Reference

| Role | Fill | Stroke | Text |
|------|------|--------|------|
| Blue (planning) | `#ffffff` | `#3b82f6` | `#2563eb` |
| Purple (builder) | `#ffffff` | `#8b5cf6` | `#7c3aed` |
| Green (validator/pass) | `#ffffff` | `#22c55e` | `#166534` |
| Gray (neutral) | `#ffffff` | `#6b7280` | `#374151` |
| Red (fail) | — | `#ef4444` | `#dc2626` |
| Amber (fix/retry) | — | `#d97706` | `#d97706` |
| Yellow (annotation) | `#fefce8` | `#eab308` | `#a16207` |
| Done pill | `#dcfce7` | `#16a34a` | `#15803d` |

---

## Alternative Palettes

Use when the user explicitly requests a different visual style.

### Dark / Tech
```
nodes:   fillColor=#1e1e2e;strokeColor=#89b4fa;fontColor=#cdd6f4
accents: strokeColor=#a6e3a1 (green), #f38ba8 (red), #cba6f7 (purple)
```

### Pastel / Soft
```
nodes:   fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#333333
```

### Minimal / Mono
```
nodes:   fillColor=#ffffff;strokeColor=#333333;fontColor=#333333
edges:   endArrow=open;endSize=8;strokeColor=#333333
```

### Bold / AWS
```
header:  fillColor=#232F3E;strokeColor=#FF9900;fontColor=#ffffff
compute: fillColor=#FF9900;strokeColor=#FF9900;fontColor=#ffffff
```

### Vibrant / UI
```
primary:   fillColor=#6366f1;strokeColor=#4f46e5;fontColor=#ffffff;shadow=1
secondary: fillColor=#8b5cf6;strokeColor=#7c3aed;fontColor=#ffffff;shadow=1
```

## Common Shape Styles

| Shape | Style fragment |
|-------|----------------|
| Rounded rectangle | `rounded=1;` |
| Diamond (decision) | `rhombus;` |
| Pill (terminal) | `rounded=1;arcSize=50;` |
| Cylinder (database) | `shape=cylinder3;` |
| Circle | `ellipse;` |
| User/person | `shape=mxgraph.aws4.user;` |
| Cloud | `shape=mxgraph.aws4.cloud;` |
| Title text | `text;fontSize=16;fontStyle=1;align=center;` |

## Layout Rules (Critical — violations cause misaligned diagrams)

### 1. Center-align all nodes in a flow column

Every node in a vertical flow column **must share the same `center_x`**. Mixed center_x values cause orthogonal edges to jog horizontally, routing through text.

**Formula:** `node_x = center_x - node_width / 2`

For a container at `x=C_x, width=C_w`: `center_x = C_x + C_w / 2`

If subgroups inside the container have a fixed center (e.g. builder nodes at center_x=533), align ALL orchestrator nodes above/below them to that same center_x. Do not place orchestrator nodes at a different x and rely on routing to bridge the gap.

### 2. Edges between vertically-stacked nodes must be straight vertical

If source and target share the same `center_x`, use `exitX=0.5;exitY=1;entryX=0.5;entryY=0;` — the edge routes as a clean vertical line with no horizontal jog.

If they have different center_x values (unavoidable), add an explicit waypoint that steps horizontally **above** the entry node (at `y = target_top - 15`) so the jog happens in empty space, not through text:

```xml
<mxGeometry relative="1" as="geometry">
  <Array as="points">
    <mxPoint x="[target_center_x]" y="[target_top - 15]"/>
  </Array>
</mxGeometry>
```

### 3. Annotation boxes: vertical center must match the connector exit point

For horizontal dashed connectors to annotation boxes, the annotation's vertical center **must equal** the source element's exit y.

**Formula:** `annotation_y = source_center_y - annotation_height / 2`

Example: source diamond center_y=234, annotation height=72 → `annotation_y = 234 - 36 = 198`.

If the annotation y is wrong the connector angles — it will not be horizontal. Calculate this explicitly before placing annotations.

### 4. Loopback labels: use edge `value`, not rotated text cells

**Do NOT** use standalone `mxCell` text cells with `rotation=-90` as sidebar labels for loopback edges. They render as floating horizontal blocks, not clean sidebar annotations.

**Do:** Put the label as the edge `value` — it will appear near the midpoint of the edge in horizontal text, which is readable and unambiguous:

```xml
<mxCell id="e-fail" value="FAIL" style="...strokeColor=#ef4444;fontColor=#dc2626;fontSize=11;fontStyle=1;..." edge="1" ...>
```

For loopbacks with two semantic labels (e.g. "FAIL" on horizontal segment, "Fresh builder" on vertical), use the more important label as `value` and omit the secondary label.

## Edge Routing Rules

- Always specify `exitX`, `exitY`, `entryX`, `entryY` explicitly — never rely on auto-routing to pick correct connection points
- For bidirectional connections (A↔B), use **opposite sides** (exitY=0.3 / entryY=0.7)
- Never let multiple edges share the same path — offset using different exit/entry points
- Add `curved=1;` for smoother bends on complex routes

```xml
<!-- Example: clean vertical edge between aligned nodes -->
<mxCell id="e1" value="" style="endArrow=block;endFill=1;strokeColor=#6b7280;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;entryX=0.5;entryY=0;" edge="1" source="node-a" target="node-b" parent="1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- Example: edge stepping around text via waypoint -->
<mxCell id="e2" value="" style="endArrow=block;endFill=1;strokeColor=#22c55e;strokeWidth=1.5;edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;entryX=0.5;entryY=0;" edge="1" source="diamond" target="inner-node" parent="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="[inner_node_center_x]" y="[inner_node_top - 15]"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## edit_diagram Operations

```json
{ "operations": [
  { "operation": "add",    "cell_id": "new-1",  "new_xml": "<mxCell ...>" },
  { "operation": "update", "cell_id": "2",       "new_xml": "<mxCell ...>" },
  { "operation": "delete", "cell_id": "old-1" }
]}
```

Always use descriptive `cell_id` values (e.g. `"lambda-fn"`, `"api-gw"`) — not numeric IDs — for new cells to avoid collisions.

## Export

```
export_diagram({ path: "./diagram.drawio" })   ← XML (default)
export_diagram({ path: "./diagram.png" })       ← PNG (requires open browser tab)
export_diagram({ path: "./diagram.svg" })       ← SVG (requires open browser tab)
```

PNG/SVG export requires the browser tab to be open and the diagram loaded.

## Port & Session Notes

- MCP server uses port **6002** by default; auto-increments to 6003–6020 if occupied
- The next-ai-draw-io **desktop app** uses port **61337** in production — no conflict
- In dev mode (`npm run dev`) the desktop app also uses 6002 — conflict likely; set `PORT=6003` in MCP env
- The MCP server and the desktop app are **separate** — the MCP controls a browser-based draw.io embed, not the Electron window

## Configuration

| Env var | Default | Purpose |
|---------|---------|---------|
| `PORT` | `6002` | MCP embedded server port |
| `DRAWIO_BASE_URL` | `https://embed.diagrams.net` | draw.io embed source (for self-hosted) |

## Decision Tree

| User says | Action |
|-----------|--------|
| "Create a diagram" | `start_session` → `create_new_diagram` |
| "Add X to the diagram" | `get_diagram` → `edit_diagram` (add) |
| "Change / update X" | `get_diagram` → `edit_diagram` (update) |
| "Remove X" | `get_diagram` → `edit_diagram` (delete) |
| "Save / export" | `export_diagram` |
| Asks about style | Apply named palette from this skill; show options if unsure |

## Troubleshooting

### "No active session"
Call `start_session` first — the session resets on MCP server restart.

### Browser not updating
Check the browser URL contains `?mcp=<session-id>`. If the tab was closed, call `start_session` again to get a new URL.

### Port already in use
Set `PORT=6003` in the MCP server env config (`.mcp.json` or Claude Desktop config).

### edit_diagram rejected ("must call get_diagram first")
The 30-second window expired. Call `get_diagram` then retry `edit_diagram` immediately.

### PNG/SVG export returns "timed out"
The browser tab must be open with the diagram loaded. Navigate to the session URL, wait for the diagram to render, then retry.
