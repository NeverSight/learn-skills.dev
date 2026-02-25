---
name: excalidraw
description: Control a live Excalidraw canvas via the `excalidraw` CLI. Use when an agent needs to (1) draw or lay out diagrams on a live canvas, (2) create/update/delete individual elements, (3) batch-create complex diagrams from JSON, (4) inspect the canvas with describe or screenshot, (5) export/import .excalidraw files, PNG, or SVG, (6) save/restore canvas snapshots, (7) align, distribute, group, lock, or duplicate elements, (8) convert Mermaid diagrams to Excalidraw elements, (9) share diagrams as encrypted excalidraw.com URLs. Requires a running canvas server (default http://localhost:3000).
---

# Excalidraw Skill

## Step 0: Setup

### Load companion skills when needed
- **Drawing or styling a diagram** → load `excalidraw-design-guide` (colors, sizing, anti-patterns)
- **Building a multi-element diagram or reviewing one** → load `excalidraw-workflow` (planning, progressive drawing, review checklist)
- **Just checking status, exporting, or a single command** → no companion skills needed

### Check if canvas is running
```bash
excalidraw status
```
Returns `{"status":"healthy","timestamp":"...","elements_count":N,"websocket_clients":N}` if running.

### Start canvas if not running
```bash
excalidraw serve --port 3000
```

> **Browser required for**: `viewport`, `screenshot`, and `mermaid` commands.
> These route through the browser tab via WebSocket — they return a 503 error if no browser has the canvas open.
> Open `http://localhost:3000` before using any of these commands.

### Install CLI (one-time)
```bash
bun add -g github:opencoredev/excalidraw-cli
```

### Global URL override
```bash
export EXCALIDRAW_URL=http://localhost:3000
```
All commands respect `EXCALIDRAW_URL`. Override per-command with `--url <url>`.

---

## ⚡ Draw Element by Element — Don't Make the User Wait

Create each element individually so the user sees every shape appear on canvas and can redirect if something is wrong.

```bash
excalidraw create --type rectangle --id svc-a --x 100 --y 100 --width 160 --height 60 --text "Service A" --stroke-color "#1971c2" --fill "#a5d8ff"
excalidraw viewport --fit

excalidraw create --type rectangle --id svc-b --x 100 --y 240 --width 160 --height 60 --text "Service B" --stroke-color "#2f9e44" --fill "#b2f2bb"
excalidraw viewport --fit

excalidraw create --type arrow --x 0 --y 0 --start svc-a --end svc-b
excalidraw viewport --fit
```

**Order**: zones/containers first → nodes one by one → arrows one by one → detail labels last.

**Rule**: your first tool call must be a draw command. Do not reason through the whole diagram before starting.

**`excalidraw batch` is best for** complete diagrams where all elements and their arrows are defined together — arrow bindings are computed across the whole set at once, which gives better geometry. For live incremental drawing, use individual `create` calls.

---

## Inline Self-Check (before EVERY create)

1. **Will the text fit?** `width = max(160, charCount * 11 + 40)`. Go wider when unsure — truncation looks worse than a wide box.
2. **Multi-word labels**: measure the longest single word: `max(160, longestWord * 11 + 80)`
3. **Shapes before arrows**: arrows bind to shapes by ID — the shape must exist first.
4. **Enough gap?** At least 60px between shapes, 80px between tiers.

**Fix immediately**: `excalidraw update <id> --width <wider>` before moving on.

### Arrow binding rules
- **Always `--start <id> --end <id>`** — never raw coordinates to connect shapes
- **Shapes first, arrows second** — every time, no exceptions
- Arrow passes through a box? Shapes too close, or arrow wasn't bound. Delete, increase gap, recreate with `--start`/`--end`.

### Quality gate (only when something looks off)
```bash
excalidraw describe   # spot-check IDs and positions
excalidraw viewport --fit
```

---

## Command Reference

### Server
```bash
excalidraw serve [--port 3000] [--host localhost]   # Start server (blocks)
excalidraw serve --port 3000 --host 0.0.0.0         # Bind to all interfaces
excalidraw status                                    # Health check
excalidraw stop                                      # Prints Ctrl+C instructions
```

### Create element — all flags
```bash
excalidraw create \
  --type <type> \          # rectangle | ellipse | diamond | arrow | text | line | freedraw (required)
  --x <n> --y <n> \        # Position (required)
  --width <n> --height <n> \
  --text "Label" \         # Shape label (stored as label.text) or text element content
  --id "my-id" \           # Custom ID — set this for any shape you'll reference with arrows
  --stroke-color "#1971c2" \
  --fill "#a5d8ff" \       # backgroundColor
  --stroke-width <n> \
  --stroke-style solid|dashed|dotted \
  --roughness <0-3> \      # 0 = sharp, 3 = very rough
  --opacity <0-100> \
  --font-size <n> \        # Text elements only
  --start <id> \           # Arrow: bind start to shape edge
  --end <id> \             # Arrow: bind end to shape edge
  --start-arrowhead arrow|bar|dot|triangle|none \
  --end-arrowhead arrow|bar|dot|triangle|none
```

### Update element
```bash
excalidraw update <id> --text "New" --stroke-color "#e03131"
excalidraw update <id> --x 200 --y 300 --width 220 --height 80
excalidraw update <id> --fill "#ffd8a8" --stroke-style dashed --opacity 80
```

### Read / delete
```bash
excalidraw get <id>
excalidraw query                   # All elements
excalidraw query --type rectangle  # Filter by type
excalidraw delete <id>
excalidraw clear                   # Remove all elements
excalidraw describe                # Human-readable summary of all elements
```

### Batch create (best for complete diagrams)
```bash
excalidraw batch diagram.json      # From file
cat diagram.json | excalidraw batch  # From stdin (also accepts bare array)
```

Batch JSON — full property set:
```json
{
  "elements": [
    {
      "id": "svc-a",
      "type": "rectangle",
      "x": 100, "y": 100, "width": 180, "height": 60,
      "label": {"text": "Service A"},
      "strokeColor": "#1971c2",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeStyle": "solid",
      "strokeWidth": 2,
      "roughness": 0,
      "opacity": 100,
      "roundness": {"type": 3}
    },
    {
      "id": "db",
      "type": "rectangle",
      "x": 100, "y": 240, "width": 180, "height": 60,
      "label": {"text": "Database"},
      "strokeColor": "#0c8599",
      "backgroundColor": "#99e9f2"
    },
    {
      "type": "arrow",
      "x": 0, "y": 0,
      "start": {"id": "svc-a"},
      "end": {"id": "db"},
      "label": {"text": "SQL"},
      "strokeStyle": "dashed",
      "endArrowhead": "arrow",
      "elbowed": true
    }
  ]
}
```

**Batch-only properties** (not exposed as CLI flags, only via batch JSON):
- `fillStyle`: `"hachure"` | `"solid"` | `"cross-hatch"` | `"dots"` | `"zigzag"` | `"zigzag-line"` — default is `"hachure"` (Excalidraw's sketchy fill); use `"solid"` for clean fills
- `roundness`: `{"type": 3}` for rounded corners on rectangles/ellipses
- `elbowed`: `true` on arrows for right-angle routing instead of curved

**Critical**: `"label": {"text": "..."}` for shapes. `"text": "..."` directly on `"type": "text"` elements only.

### Scene I/O
```bash
excalidraw export                            # Print .excalidraw JSON to stdout
excalidraw export --out scene.excalidraw     # Write to file
excalidraw import scene.excalidraw           # Import — replaces canvas (default)
excalidraw import scene.excalidraw --mode merge  # Merge with existing elements

excalidraw snapshot v1                       # Save named in-memory snapshot
excalidraw restore v1                        # Restore snapshot (clears canvas first)
```

> **Snapshots are in-memory** — they're lost when the server restarts, same as canvas state.
> Use `excalidraw export --out backup.excalidraw` before stopping the server.

### Viewport & screenshot (browser must be open)
```bash
excalidraw viewport --fit                    # Zoom to fit all elements
excalidraw viewport --element <id>           # Center on element
excalidraw viewport --zoom 1.5              # Set zoom level (1 = 100%)
excalidraw viewport --offset-x <n> --offset-y <n>  # Manual scroll offset

excalidraw screenshot                        # Capture PNG (base64 to stdout)
excalidraw screenshot --format svg --out diagram.svg
excalidraw screenshot --out check.png
```

### Layout
```bash
excalidraw align id1 id2 id3 --alignment left|right|center|top|bottom|middle
excalidraw distribute id1 id2 id3 --direction horizontal|vertical  # needs 3+
excalidraw group id1 id2 id3                # Assigns shared groupId; returns groupId
excalidraw ungroup <groupId>
excalidraw duplicate id1 id2 [--dx 20] [--dy 20]
excalidraw lock id1 id2                     # Prevent UI edits
excalidraw unlock id1 id2
```

### Export & sharing
```bash
excalidraw url                              # Encrypted excalidraw.com link (uploads scene)
excalidraw mermaid diagram.mmd              # Convert Mermaid → Excalidraw (browser required)
echo "graph TD; A-->B" | excalidraw mermaid
excalidraw guide                            # Print color palette, sizing, layout rules
```

---

## Element Types Reference

| Type      | Required fields       | Label syntax        | Notes                              |
|-----------|-----------------------|---------------------|------------------------------------|
| rectangle | x, y, width, height   | `label: {text}` | Use `roundness: {type:3}` for rounded |
| ellipse   | x, y, width, height   | `label: {text}` |                                    |
| diamond   | x, y, width, height   | `label: {text}` | Decision nodes in flowcharts       |
| text      | x, y, text            | `text: "..."` directly | Standalone labels/titles    |
| arrow     | x, y                  | `label: {text}` | Bind with `start`/`end` by ID      |
| line      | x, y, points          | —                   | Manual `[[x,y],[x,y]]` points array |
| freedraw  | x, y, points          | —                   | Freehand path                      |

---

## Common Patterns

### Architecture diagram
```json
{
  "elements": [
    {"id":"zone","type":"rectangle","x":40,"y":40,"width":500,"height":400,
     "backgroundColor":"#e9ecef","strokeColor":"#868e96","opacity":40,
     "fillStyle":"solid","label":{"text":"Backend"}},
    {"id":"api","type":"rectangle","x":80,"y":100,"width":200,"height":60,
     "strokeColor":"#1971c2","backgroundColor":"#a5d8ff","fillStyle":"solid",
     "roundness":{"type":3},"label":{"text":"API Gateway"}},
    {"id":"db","type":"rectangle","x":80,"y":260,"width":200,"height":60,
     "strokeColor":"#0c8599","backgroundColor":"#99e9f2","fillStyle":"solid",
     "roundness":{"type":3},"label":{"text":"Database"}},
    {"type":"arrow","x":0,"y":0,"start":{"id":"api"},"end":{"id":"db"},
     "label":{"text":"SQL"},"strokeStyle":"dashed"}
  ]
}
```

### Flowchart
```json
{
  "elements": [
    {"id":"start","type":"ellipse","x":160,"y":40,"width":120,"height":60,
     "strokeColor":"#2f9e44","backgroundColor":"#b2f2bb","fillStyle":"solid","label":{"text":"Start"}},
    {"id":"step1","type":"rectangle","x":140,"y":160,"width":160,"height":60,
     "strokeColor":"#1971c2","backgroundColor":"#a5d8ff","fillStyle":"solid","label":{"text":"Process Data"}},
    {"id":"decide","type":"diamond","x":140,"y":280,"width":160,"height":80,
     "strokeColor":"#e8590c","backgroundColor":"#ffd8a8","fillStyle":"solid","label":{"text":"Valid?"}},
    {"type":"arrow","x":0,"y":0,"start":{"id":"start"},"end":{"id":"step1"}},
    {"type":"arrow","x":0,"y":0,"start":{"id":"step1"},"end":{"id":"decide"}}
  ]
}
```

---

## Iterative Refinement Loop

```
excalidraw batch diagram.json
  → excalidraw describe           (verify IDs exist and positions look right)
  → excalidraw viewport --fit     (fit view)
  → excalidraw screenshot --out /tmp/check.png   (visual check)
  → [issues?] excalidraw update <id> --width 220
  → excalidraw screenshot --out /tmp/check2.png
  → [done] excalidraw export --out backup.excalidraw
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Canvas server unreachable` | Run `excalidraw status`; if error → `excalidraw serve` |
| `503 No frontend client connected` | Open `http://localhost:3000` in a browser tab first |
| Arrow floats instead of connecting | Create both shapes **before** the arrow; use `--start`/`--end` by ID |
| Label not showing | Shapes: `"label": {"text": "..."}` — not `"text": "..."` |
| Fill looks hatched/sketchy | Add `"fillStyle": "solid"` to your batch JSON elements |
| Elements lost after restart | `excalidraw export --out backup.excalidraw` before stopping |
| Snapshot missing after restart | Snapshots are in-memory; export instead for persistence |
| Arrow too curved | Use `"elbowed": true` in batch JSON for right-angle routing |
