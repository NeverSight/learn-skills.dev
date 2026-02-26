---
name: diagrams
version: 1.0.0
description: Generate visual flow diagrams, architecture diagrams, and system maps as SVG/PNG. Use when the user asks for flowcharts, user flow diagrams, architecture diagrams, system diagrams, interaction maps, or any visual diagram. Supports ELK JSON layout engine with automatic rendering to SVG.
---

# Diagrams

Generate diagrams from structured JSON → SVG (and optionally PNG).

## Quick Start

1. **Install elkjs** in the target directory (if not already present):
   ```bash
   cd <project>/docs/diagrams && npm init -y && npm install elkjs
   # Set "type": "module" in package.json
   ```

2. **Write ELK JSON** files describing the diagram (see schema below)

3. **Render:**
   ```bash
   # Single file
   node <skill-dir>/scripts/render-elk.mjs diagram.json output.svg

   # Batch: all .json files in a folder → svg/ subfolder
   node <skill-dir>/scripts/render-elk.mjs --dir <folder>

   # Batch + PNG (macOS only, uses sips)
   node <skill-dir>/scripts/render-elk.mjs --dir <folder> --png
   ```

4. **Embed in markdown:**
   ```markdown
   ![Diagram Title](diagrams/svg/my-diagram.svg)
   ```

## ELK JSON Schema

```json
{
  "id": "root",
  "title": "Diagram Title (rendered as heading)",
  "layoutOptions": {
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    "elk.spacing.nodeNode": "30",
    "elk.layered.spacing.nodeNodeBetweenLayers": "40",
    "elk.padding": "[top=40,left=20,bottom=20,right=20]"
  },
  "children": [
    {
      "id": "node1",
      "width": 220,
      "height": 45,
      "labels": [{"text": "Node label for ELK layout"}],
      "label": "📦 Display label (rendered in SVG)",
      "color": "core",
      "subtitle": "Optional second line"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "sources": ["node1"],
      "targets": ["node2"],
      "labels": [{"text": "Yes", "width": 25, "height": 14}],
      "edgeColor": "#10B981",
      "dashed": true
    }
  ]
}
```

### Node Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Required. Unique identifier |
| `width` | number | Node width in px (default 120) |
| `height` | number | Node height in px (default 40) |
| `labels` | array | `[{text}]` — used by ELK for layout calculation |
| `label` | string | Display text rendered in SVG (supports emoji). Falls back to `id` |
| `color` | string | Color key from palette (see below) |
| `subtitle` | string | Smaller text below the label |
| `fontSize` | number | Label font size (default 13) |
| `children` | array | Nested nodes — makes this a container |
| `containerColor` | string | Color key for container background |

### Edge Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Required. Unique identifier |
| `sources` | string[] | Source node id(s) |
| `targets` | string[] | Target node id(s) |
| `labels` | array | `[{text, width, height}]` — edge labels |
| `edgeColor` | string | Hex color (default `#64748B`) |
| `dashed` | boolean | Dashed line style |
| `strokeWidth` | number | Line thickness (default 1.5) |

### Color Palette

8 semantic colors. Every node maps to one. A legend auto-renders at the bottom of each SVG.

| Key | Color | Meaning | Use For |
|-----|-------|---------|---------|
| `action` | 🔵 Blue | **System action** | Steps the app performs — API calls, DB writes, cron triggers |
| `external` | 🟢 Teal | **External service** | Third-party APIs — Google, Twilio, Stripe, Resend |
| `decision` | 🩷 Pink | **Decision point** | Yes/no branches, if/else, conditional checks |
| `user` | 🟠 Orange | **User action** | Things the user does — clicks, inputs, reviews |
| `success` | 🟢 Green | **Positive outcome** | Done, confirmed, created, visible |
| `negative` | 🔴 Red | **Negative outcome** | Canceled, error, failed, not built |
| `neutral` | ⚫ Gray | **Neutral / info** | Starting points, labels, inactive, informational |
| `data` | 🟡 Amber | **Data / artifact** | Records, drafts, outputs, intermediate data |

Set `"legend": false` on the root graph to hide the auto-legend.

### Layout Options

Common `layoutOptions` values:

- `elk.direction`: `DOWN` (default), `RIGHT`, `LEFT`, `UP`
- `elk.algorithm`: `layered` (default, best for flowcharts), `force`, `stress`
- `elk.spacing.nodeNode`: Space between sibling nodes (px)
- `elk.layered.spacing.nodeNodeBetweenLayers`: Space between layers (px)
- `elk.padding`: `[top=N,left=N,bottom=N,right=N]`

## Design Tips

- **Sizing:** 200-280px wide for most nodes. 45px tall for single-line, 55px for two-line labels.
- **Decision nodes:** Use `context` (pink) color for yes/no branching.
- **Edge labels:** Keep short (Yes/No/Error). Set `width`/`height` for proper positioning.
- **Containers:** Add `children` array to a node. Use `containerColor: "step"` for a light blue group.
- **Manual trips vs automated:** Use `dashed: true` on edges for alternative/optional paths.
- **Title:** Set `title` on the root graph for a rendered heading above the diagram.
- **Emoji in labels:** Supported and encouraged for visual scanning.

## Gotchas

- **Container layout:** ELK's layered algorithm with nested containers in `RIGHT` direction can produce overlapping layouts. Prefer `DOWN` for containers, or flatten to a non-container layout if horizontal.
- **`labels` vs `label`:** `labels` (array) is what ELK uses for layout spacing. `label` (string) is what gets rendered in the SVG. Always set both — `labels[0].text` should approximate the display label length for correct sizing.
- **`package.json` must have `"type": "module"`** for the ESM import to work.
- **elkjs must be installed locally** in the directory where you run the script. It's not global.

