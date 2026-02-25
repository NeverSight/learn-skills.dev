---
name: excalidraw-design-guide
description: Load when drawing any Excalidraw diagram. Provides color palette (hex codes), sizing formulas to prevent text truncation, spacing rules to prevent overlaps, arrow styles, layout patterns, and diagram templates for architecture, flowchart, and ER diagrams. Use when asked to draw, visualize, diagram, or create any chart.
---

# Excalidraw Diagram Design Guide

## Color Palette

### Stroke Colors (borders & text)
| Name   | Hex     | Use for                    |
|--------|---------|----------------------------|
| Black  | #1e1e1e | Default text & borders     |
| Red    | #e03131 | Errors, warnings, critical |
| Green  | #2f9e44 | Success, approved, healthy |
| Blue   | #1971c2 | Primary actions, links     |
| Purple | #9c36b5 | Services, middleware       |
| Orange | #e8590c | Async, queues, events      |
| Cyan   | #0c8599 | Data stores, databases     |
| Gray   | #868e96 | Annotations, secondary     |

### Fill Colors (backgroundColor — pastel)
| Name         | Hex     | Pairs with stroke |
|--------------|---------|-------------------|
| Light Red    | #ffc9c9 | #e03131           |
| Light Green  | #b2f2bb | #2f9e44           |
| Light Blue   | #a5d8ff | #1971c2           |
| Light Purple | #eebefa | #9c36b5           |
| Light Orange | #ffd8a8 | #e8590c           |
| Light Cyan   | #99e9f2 | #0c8599           |
| Light Gray   | #e9ecef | #868e96           |
| White        | #ffffff | #1e1e1e           |

---

## Sizing Rules

- **Minimum shape**: width >= 120px, height >= 60px
- **Shape width formula**: `max(160, charCount * 11 + 40)` — the `+40` is mandatory padding, never skip it
- **Multi-word labels**: measure the longest single word: `max(160, longestWord * 11 + 80)`
- **Shape height**: 60px single-line, 80px two-line, 100px three-line labels
- **Font sizes**: body text >= 16, titles/headers >= 20, small labels >= 14
- **Padding**: at least 20px inside shapes for text breathing room
- **Arrow gap**: minimum 80px between connected shapes — closer = arrows overdraw the border
- **Consistent sizing**: same-role shapes = same dimensions

---

## Layout Patterns

- **Grid snap**: align to 20px grid for clean layouts
- **Spacing**: 40–80px gap between adjacent shapes
- **Flow direction**: top-to-bottom (vertical) or left-to-right (horizontal)
- **Hierarchy**: important nodes larger or higher; left-to-right = temporal order
- **Grouping**: cluster related elements; use background rectangles as zones
- **Tier layout**:
  - Tier 1 (y=50–130): Client apps / entry points
  - Tier 2 (y=200–280): Gateway / edge layer
  - Tier 3 (y=350–440): Services (spread wide: 160–200px apart)
  - Tier 4 (y=510–590): Data stores
  - Side panels: x < 0 or x > mainDiagramRight + 80

---

## Arrow Best Practices

### Binding (always use element IDs, not raw coordinates)
```json
{"type": "arrow", "x": 0, "y": 0, "start": {"id": "svc-a"}, "end": {"id": "svc-b"}}
```
Server auto-routes arrows to element edges using precise geometry.

### Line styles
- **Solid**: synchronous calls, direct dependencies
- **Dashed** (`"strokeStyle": "dashed"`): async flows, optional paths, events
- **Dotted** (`"strokeStyle": "dotted"`): weak dependencies, annotations

### Arrowheads
- `"endArrowhead": "arrow"` — default directed flow
- `"endArrowhead": "dot"` — data stores / database relationships
- `"endArrowhead": "bar"` — cardinality (ER diagrams)
- `"endArrowhead": "triangle"` — filled triangle (UML)
- `"endArrowhead": null` — plain line (undirected)
- `"startArrowhead"` mirrors the same options for bidirectional arrows

### Labels on arrows
Use `"label": {"text": "HTTP"}` — keep to 1–2 words. Long labels overlap shapes.

### Routing complex arrows (avoid crossings)
**Elbowed arrow** (right-angle routing — cleanest for architecture diagrams):
```json
{
  "type": "arrow", "x": 0, "y": 0,
  "start": {"id": "svc-a"},
  "end": {"id": "svc-b"},
  "elbowed": true
}
```

**Curved arc** (for arrows that need to arc over elements):
```json
{
  "type": "arrow", "x": 100, "y": 100,
  "points": [[0,0],[50,-40],[200,0]],
  "roundness": {"type": 2},
  "strokeColor": "#1971c2"
}
```

---

## Fill Styles (`fillStyle`)

Controls how shape interiors are rendered. Default is `"hachure"` (Excalidraw's signature sketchy look).

| Value | Appearance | Best for |
|-------|-----------|----------|
| `"solid"` | Flat solid color | Clean production diagrams |
| `"hachure"` | Diagonal hatching (default) | Sketchy/hand-drawn style |
| `"cross-hatch"` | Grid hatching | Emphasis, dense areas |
| `"dots"` | Dot pattern | Light texture, secondary elements |
| `"zigzag"` | Zigzag lines | Decorative, callouts |
| `"zigzag-line"` | Single zigzag | Borders/edges |

**Use `"solid"` for any diagram meant to look professional.** Only use `"hachure"` if you want the hand-drawn aesthetic intentionally.

```json
{"type": "rectangle", "fillStyle": "solid", "backgroundColor": "#a5d8ff", ...}
```

---

## Rounded Corners (`roundness`)

Add `"roundness": {"type": 3}` to rectangle and ellipse elements for rounded corners.

```json
{"type": "rectangle", "roundness": {"type": 3}, ...}
```

Omit `roundness` (or set to `null`) for sharp corners.

---

## Diagram Type Templates

### Architecture Diagram
```json
{
  "elements": [
    {
      "id": "zone-backend",
      "type": "rectangle",
      "x": 40, "y": 40, "width": 600, "height": 400,
      "backgroundColor": "#e9ecef", "strokeColor": "#868e96",
      "opacity": 40,
      "label": {"text": "Backend", "fontSize": 20}
    },
    {
      "id": "api-gw",
      "type": "rectangle",
      "x": 80, "y": 100, "width": 180, "height": 70,
      "strokeColor": "#9c36b5", "backgroundColor": "#eebefa",
      "label": {"text": "API Gateway"}
    },
    {
      "id": "auth-svc",
      "type": "rectangle",
      "x": 80, "y": 240, "width": 180, "height": 70,
      "strokeColor": "#1971c2", "backgroundColor": "#a5d8ff",
      "label": {"text": "Auth Service"}
    },
    {
      "id": "db",
      "type": "rectangle",
      "x": 80, "y": 380, "width": 180, "height": 70,
      "strokeColor": "#0c8599", "backgroundColor": "#99e9f2",
      "label": {"text": "Postgres"}
    },
    {"type":"arrow","x":0,"y":0,"start":{"id":"api-gw"},"end":{"id":"auth-svc"},"label":{"text":"JWT verify"}},
    {"type":"arrow","x":0,"y":0,"start":{"id":"auth-svc"},"end":{"id":"db"},"label":{"text":"SQL"},"strokeStyle":"dashed"}
  ]
}
```

### Flowchart
```json
{
  "elements": [
    {"id":"start","type":"ellipse","x":160,"y":40,"width":120,"height":60,
     "strokeColor":"#2f9e44","backgroundColor":"#b2f2bb","label":{"text":"Start"}},
    {"id":"step1","type":"rectangle","x":140,"y":160,"width":160,"height":60,
     "strokeColor":"#1971c2","backgroundColor":"#a5d8ff","label":{"text":"Validate Input"}},
    {"id":"decide","type":"diamond","x":140,"y":280,"width":160,"height":80,
     "strokeColor":"#e8590c","backgroundColor":"#ffd8a8","label":{"text":"Valid?"}},
    {"id":"end-ok","type":"ellipse","x":340,"y":290,"width":100,"height":60,
     "strokeColor":"#2f9e44","backgroundColor":"#b2f2bb","label":{"text":"Success"}},
    {"id":"end-err","type":"ellipse","x":0,"y":290,"width":100,"height":60,
     "strokeColor":"#e03131","backgroundColor":"#ffc9c9","label":{"text":"Error"}},
    {"type":"arrow","x":0,"y":0,"start":{"id":"start"},"end":{"id":"step1"}},
    {"type":"arrow","x":0,"y":0,"start":{"id":"step1"},"end":{"id":"decide"}},
    {"type":"arrow","x":0,"y":0,"start":{"id":"decide"},"end":{"id":"end-ok"},"label":{"text":"Yes"}},
    {"type":"arrow","x":0,"y":0,"start":{"id":"decide"},"end":{"id":"end-err"},"label":{"text":"No"}}
  ]
}
```

### ER Diagram
```json
{
  "elements": [
    {"id":"users","type":"rectangle","x":40,"y":100,"width":180,"height":120,
     "strokeColor":"#1971c2","backgroundColor":"#a5d8ff",
     "label":{"text":"users\n─────\nid: UUID\nname: text\nemail: text"}},
    {"id":"orders","type":"rectangle","x":300,"y":100,"width":180,"height":120,
     "strokeColor":"#9c36b5","backgroundColor":"#eebefa",
     "label":{"text":"orders\n──────\nid: UUID\nuser_id: UUID\ntotal: decimal"}},
    {"type":"arrow","x":0,"y":0,"start":{"id":"users"},"end":{"id":"orders"},
     "label":{"text":"1..N"},"endArrowhead":"arrow","startArrowhead":"dot"}
  ]
}
```

---

## Anti-Patterns to Avoid

1. **Overlapping elements** — always leave gaps; use `excalidraw distribute`
2. **Cramped spacing** — minimum 40px between shapes; 60px between diagram tiers
3. **Tiny fonts** — never below 14px; prefer 16+ for readability
4. **Raw arrow coordinates** — always use `start`/`end` binding to connect to shapes
5. **Too many colors** — limit to 3–4 fill colors per diagram
6. **Inconsistent sizes** — same-role shapes should have identical width/height
7. **No labels** — every shape and meaningful arrow needs descriptive text
8. **Flat layouts** — use background zones/groups to show hierarchy
9. **Side panels overlapping main diagram** — place at x < 0 or x > mainRight + 80
10. **Unchecked arrow crossings** — use `"elbowed": true` or route with waypoints
11. **Forgetting `fillStyle: "solid"`** — default is `"hachure"` (sketchy); always set `"fillStyle": "solid"` for clean diagrams

---

## Pre-Drawing Checklist

Before writing any JSON:
- [ ] Plan coordinate grid (tiers, x-positions, spacing)
- [ ] Calculate shape widths: `max(160, charCount * 11 + 40)`
- [ ] Assign IDs to all shapes that arrows will reference
- [ ] Choose 2–3 fill colors for semantic grouping
- [ ] Add `"fillStyle": "solid"` to every shape for a clean look
- [ ] Decide flow direction (vertical or horizontal)
- [ ] Run `excalidraw guide` for quick color/sizing reference
