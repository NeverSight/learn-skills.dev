---
name: excalidrawer
description: 'Code-first Excalidraw diagram generation with SVG and PNG export. Use when asked to "create a diagram", "draw a flowchart", "generate an architecture diagram", "export diagram to SVG", "export diagram to PNG", or "visualize a process". Produces .excalidraw, .svg, and .png files using the excalidrawer npm package — no browser required.'
---

# Excalidrawer

A diagram generation tool with built-in templates and a CLI. For supported diagram types, just provide JSON data and run the CLI. For custom diagrams, write a short JS script using the library API.

## Prerequisites

No install needed for template-based workflows — `npx` handles everything automatically.

Only install the npm package if you need the library API for custom scripts:

```bash
npm install excalidrawer
```

## Workflow: Template-Based (Preferred)

For supported diagram types (timeline, etc.), use the CLI directly — no script needed.

### Step 1: Identify the diagram type

Check if the request matches a built-in template:

| Type | Use for |
|------|---------|
| `timeline` | Project timelines, roadmaps, milestones |
| `architecture` | Layered system architecture, component diagrams |
| `flowchart` | Decision flows, process diagrams |
| `sequence` | Sequence / interaction diagrams, swimlane flows |

Run `npx excalidrawer types` to see all available types.

### Step 2: Create a JSON data file

Write a JSON file matching the template's schema (see Template Schemas below).

### Step 3: Run the CLI

```bash
npx excalidrawer generate --type <type> --input data.json --output ./path/to/output
```

CLI options:
- `--type, -t` — Diagram type (required)
- `--input, -i` — Input JSON file (reads stdin if omitted)
- `--output, -o` — Output path without extension (required)
- `--format, -f` — Comma-separated: `excalidraw,svg,png` (default: all three)
- `--seed, -s` — Seed for deterministic IDs

Examples:
```bash
# Generate all formats
npx excalidrawer generate -t timeline -i timeline.json -o docs/timeline

# Only SVG and PNG
npx excalidrawer generate -t timeline -i timeline.json -o docs/timeline -f svg,png

# Pipe from stdin
echo '{"title":"My Timeline","items":[...]}' | npx excalidrawer generate -t timeline -o out/timeline
```

## Template Schemas

### Architecture

Input JSON:
```json
{
  "title": "My System",
  "sections": [
    {
      "label": "Users",
      "color": "yellow",
      "items": [
        { "label": "Web User", "color": "yellow", "desc": "Browser-based access" },
        { "label": "API User", "color": "orange", "desc": "Programmatic access" }
      ]
    },
    {
      "label": "Services",
      "color": "blue",
      "items": [
        { "label": "Auth Service", "color": "blue" },
        { "label": "Data API",     "color": "green" }
      ]
    },
    {
      "label": "Storage",
      "color": "gray",
      "items": ["PostgreSQL", "Redis"]
    }
  ],
  "connections": [
    { "from": "Web User",     "to": "Auth Service" },
    { "from": "Auth Service", "to": "PostgreSQL",  "style": "dashed" }
  ]
}
```

Fields:
- `title` (string, optional) — Diagram title at the top
- `sections` (array) — Horizontal layers stacked top to bottom
  - `label` (string) — Section heading (e.g. "Users", "Interface", "Backend")
  - `color` (string, optional) — Section palette: `blue` `green` `yellow` `purple` `red` `orange` `gray`
  - `items` (array) — Boxes inside the section, laid out horizontally
    - Short form: `"Label string"`
    - Full form: `{ label, color?, desc? }`
    - `label` — Box title. Long labels auto-wrap within the box; box height grows to fit. Box width auto-sizes to the longest label across all sections, so one very long label widens every box.
    - `desc` (string, optional) — Small grey caption rendered below the box; use this for sub-details instead of cramming everything into the label
- `connections` (array, optional) — Arrows between items across sections
  - `from` / `to` — Must exactly match the item's `label` string
  - `label` (string, optional) — Text shown on the arrow
  - `style` — `"solid"` (default) or `"dashed"`

### Sequence

Input JSON:
```json
{
  "title": "OAuth Login Flow",
  "actors": [
    { "label": "User / CLI",      "color": "yellow" },
    { "label": "Local Client",    "color": "blue"   },
    { "label": "OAuth Server",    "color": "purple" }
  ],
  "steps": [
    {
      "actor": "User / CLI",
      "text":  "1. Run login command"
    },
    {
      "actor": "Local Client",
      "text":  "2. Start callback server\nlocalhost:PORT",
      "from":  "User / CLI",
      "arrow": ""
    },
    {
      "actor": "OAuth Server",
      "text":  "3. Show login page",
      "from":  "Local Client",
      "arrow": "GET /authorize"
    },
    {
      "actor": "User / CLI",
      "text":  "4. User authorizes",
      "from":  "OAuth Server",
      "arrow": "(page rendered)",
      "style": "dashed"
    },
    {
      "actor": "Local Client",
      "text":  "5. Receive token",
      "color": "green",
      "from":  "OAuth Server",
      "arrow": "200 OK token"
    }
  ]
}
```

Fields:
- `title` (string, optional) — Diagram title at the top, centered
- `actors` (array) — The participant columns, left to right
  - `label` (string) — Actor name, shown as column header; also used as reference key in steps
  - `color` (string, optional) — Header box color: `yellow` `blue` `purple` `orange` `green` `red` `gray`. Defaults to cycling through the palette.
- `steps` (array) — Events in chronological order, each occupying one row
  - `actor` (string) — Which actor column this step box belongs to (must match an actor `label`)
  - `text` (string) — Box content. Long text auto-wraps within the box; box height grows to fit. You can also use `\n` for explicit line breaks.
  - `color` (string, optional) — Override box color (e.g. `"green"` for a success/final step)
  - `from` (string, optional) — Source actor label. When set, draws a **horizontal arrow** from that actor's lifeline into this step box. The arrow Y is aligned to this box's center, ensuring perfect horizontal alignment.
  - `arrow` (string, optional) — Label shown above the arrow line. Use `""` for an unlabelled arrow.
  - `style` (string, optional) — Arrow style: `"solid"` (default) or `"dashed"` (for return/async flows)

### Flowchart

Input JSON:
```json
{
  "title": "Deployment Pipeline",
  "direction": "horizontal",
  "nodes": [
    { "id": "start", "label": "Push Code", "type": "start" },
    { "id": "build", "label": "Build & Test", "type": "process" },
    { "id": "check", "label": "Tests Pass?", "type": "decision" },
    { "id": "deploy", "label": "Deploy to Prod", "type": "process" },
    { "id": "done", "label": "Done", "type": "end" },
    { "id": "fix", "label": "Fix Errors", "type": "end" }
  ],
  "edges": [
    { "from": "start", "to": "build" },
    { "from": "build", "to": "check" },
    { "from": "check", "to": "deploy", "label": "Yes" },
    { "from": "check", "to": "fix", "label": "No" },
    { "from": "deploy", "to": "done" }
  ]
}
```

Fields:
- `title` (string, optional) — Diagram title
- `direction` (string, optional) — `"horizontal"` (default) or `"vertical"`
- `nodes` (array) — Diagram nodes
  - `id` (string) — Unique identifier, referenced by edges
  - `label` (string) — Display text. Long labels auto-wrap; node height grows to fit.
  - `type` (string, optional) — `"process"` (default, rectangle), `"decision"` (diamond), `"start"` / `"end"` (rounded), `"io"` (rectangle)
  - `color` (string, optional) — Override fill color
- `edges` (array) — Connections between nodes
  - `from` / `to` — Node `id` values
  - `label` (string, optional) — Text on the edge (e.g. "Yes" / "No")

### Timeline

Input JSON:
```json
{
  "title": "Project Timeline",
  "items": [
    {
      "label": "Milestone 1",
      "time": "Jan",
      "desc": "Description line 1\nline 2"
    },
    {
      "label": "Milestone 2",
      "time": "Mar",
      "desc": "Another description",
      "color": "#a5d8ff"
    }
  ]
}
```

Fields:
- `title` (string) — Diagram title displayed at top
- `items` (array) — Milestones in chronological order
  - `label` (string) — Milestone name (displayed in colored box)
  - `time` (string) — Time label (displayed near the axis)
  - `desc` (string) — Description text. Use `\n` for line breaks.
  - `color` (string, optional) — Box fill color. If omitted, cycles through: yellow → blue → green → purple → red → orange

## Workflow: Custom Script (Fallback)

For diagram types not covered by templates, write a JS script using the library API.

### Core API

```javascript
import {
  setSeed,            // setSeed(n) — set seed for deterministic IDs
  box,                // box(rid, tid, x, y, w, h, bg, text, fontSize?) → [rect, text]
  diamondBox,         // diamondBox(rid, tid, x, y, w, h, bg, text, fontSize?) → [diamond, text]
  arrow,              // arrow(id, x, y, points, extra?) → arrow element
  textEl,             // textEl(id, x, y, w, h, text, fontSize, extra?) → text element
  rect,               // rect(id, x, y, w, h, bg, extra?) → rectangle
  diamond,            // diamond(id, x, y, w, h, bg, extra?) → diamond shape
  ellipse,            // ellipse(id, x, y, w, h, bg, extra?) → ellipse shape
  colors,             // semantic color palette
  excalidraw,         // excalidraw(elements) → JSON string for .excalidraw file
  toSvg,              // toSvg(elements) → SVG string
  toPng,              // toPng(elements, scale?) → Promise<Buffer>
  wrapText,           // wrapText(text, maxWidth, fontSize) → wrapped string with \n
  estimateTextWidth,  // estimateTextWidth(text, fontSize) → pixel width estimate
  timeline,           // timeline(data, opts?) → elements array
  flowchart,          // flowchart(data, opts?) → elements array
  architecture,       // architecture(data, opts?) → elements array
  sequence,           // sequence(data, opts?) → elements array
} from 'excalidrawer';
```

### Color Palette

```javascript
colors.blue      // "#a5d8ff"  — info / process steps
colors.green     // "#b2f2bb"  — success / output
colors.yellow    // "#ffd43b"  — start / highlight
colors.purple    // "#d0bfff"  — AI / service layer
colors.red       // "#ffc9c9"  — external / warning
colors.orange    // "#ffec99"  — decision / human-in-loop
colors.gray      // "#e9ecef"  — secondary / misc

// Lighter section backgrounds
colors.bgBlue / colors.bgGreen / colors.bgYellow / colors.bgPurple

// Stroke accents
colors.strokeBlue / colors.strokeGreen / colors.strokeYellow / colors.strokeOrange
```

### Script Example

```javascript
import { writeFileSync } from "fs";
import { setSeed, box, arrow, textEl, colors, excalidraw, toSvg, toPng } from "excalidrawer";

setSeed(100000);
const CY = 150, BH = 56, BY = CY - BH / 2;

const elements = [
  textEl("title", 20, 12, 500, 28, "My Diagram", 22),
  ...box("s1", "s1t", 20, BY, 130, BH, colors.yellow, "Start", 15),
  arrow("a1", 150, CY, [[0,0],[40,0]]),
  ...box("s2", "s2t", 190, BY, 150, BH, colors.blue, "Process", 14),
];

writeFileSync("diagram.excalidraw", excalidraw(elements));
writeFileSync("diagram.svg", toSvg(elements));
writeFileSync("diagram.png", await toPng(elements, 2));
```

Run: `node diagram.mjs`

## Visual Design Guidelines

Follow these principles so diagrams feel readable and well-spaced:

### Labels
- **Long labels auto-wrap** — all templates automatically wrap text that exceeds the box width. Box heights grow to fit. No need to manually insert `\n` for line breaks.
- **Prefer concise labels** — shorter labels produce cleaner diagrams. The architecture template auto-widens every box to fit the longest label, so one very long label widens all boxes.
- **Use `desc` for secondary info** — put sub-details (URLs, tech stack, short notes) in the `desc` field, not in the label. `desc` renders as a small grey caption below the box and doesn't affect box sizing.

### Titles
- **Keep titles under ~60 characters** — the canvas width is driven by item count × box width. A very long title can exceed the auto-computed canvas width and appear clipped. Shorten or split into title + subtitle.

### Color usage
- Use color to encode meaning, not decoration:
  - `yellow` / `orange` → users, humans, external actors
  - `blue` → primary services, interface layer
  - `purple` → AI, ML, protocol layer
  - `green` → core logic, success state, data layer
  - `gray` → infrastructure, storage, secondary systems
  - `red` → warnings, external dependencies, risky paths
- Assign one color per architectural layer / role for visual consistency

### Connections
- Prefer direct vertical connections (same column) — they render as straight arrows
- Diagonal connections (different columns) render as L-shaped paths; avoid too many to prevent visual clutter

### Z-order (rendering layers)
When writing custom scripts, always control element order to avoid arrows obscuring text:
1. **Background rects** first (bottom layer)
2. **Arrows / connections** second (middle layer)
3. **Boxes, labels, desc text** last (top layer)

The `architecture` template handles this automatically. In custom scripts, use separate arrays and spread them in the right order:
```javascript
const bg = [], conn = [], fg = [];
// ... push elements into the right bucket ...
const elements = [...bg, ...conn, ...fg];
```

## Common Mistakes to Avoid

- **Do NOT** forget to spread `...box(...)` — it returns an array of two elements
- **Do NOT** reuse element IDs — use `setSeed()` with different values per diagram
- **Arrows**: `x, y` is the start point; `points` are relative offsets

## Export Format Decision

- Default to all three: `.excalidraw` + `.svg` + `.png`
- "for Markdown / GitHub" → `.svg`
- "for Lark / Notion / slides" → `.png`
- "I want to edit it" → `.excalidraw`

## References

- Package source: https://github.com/guohaonan-shy/excalidrawer
- Excalidraw element spec: https://github.com/excalidraw/excalidraw/blob/master/packages/excalidraw/element/types.ts
