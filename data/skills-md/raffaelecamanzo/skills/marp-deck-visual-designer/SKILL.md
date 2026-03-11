---
name: marp-deck-visual-designer
description: Transform a MARP presentation plan into concrete visual and layout decisions, including generating Mermaid diagrams when explicitly planned. Use only when a deck-plan.md already exists.
---

# Marp Visual Designer

## Purpose

Translate an existing **presentation plan** into **visual and layout execution** for a MARP deck.

This skill:
- Preserves slide intent and ordering
- Defines concrete layouts drawn from the deck template's full pattern library
- Materializes planned visuals as **Mermaid diagrams** or **Excalidraw drawings**, choosing the best fit for each visual

This skill must **not**:
- Re-plan the deck
- Modify key messages
- Add or remove slides
- Introduce new concepts

The presentation plan is authoritative.

---

## Inputs

- `planning/deck-plan.md` — produced by `marp-deck-planner`
- `.marp/references/deck-template.md` — **mandatory reference**: defines every available layout pattern, class name, HTML structure, and content budget. Read this in full before assigning any layout.

---

## Output format

Produce a single Markdown file saved as: `planning/deck-visual-design.md`

Use `--` as a separator between slides, mirroring the plan order exactly.

---

## Slide structure

For each slide, output:

- `## Title`
- `## Layout`
- `## Content placement`
- *(optional)* `## Image`

Section divider slides must contain only:
- `## Section`
- `## Layout`

---

## Workflow

### 0. Read the deck template (mandatory first step)

Before making any layout decisions, read `.marp/references/deck-template.md` in full.

This document is the authoritative source for:
- Every available CSS class and layout pattern
- Valid class token combinations
- HTML structure required for each pattern
- Content budgets per pattern (bullets, cards, columns)

**Bullet lists are the layout of last resort.** Only use a single-column bullet list when no pattern in the deck template fits the content. For every slide, actively look for a richer match:

| Content type | Preferred pattern |
|---|---|
| 4 parallel findings / insights | `insight-cards` (2×2 grid) |
| 3 items with number + label + desc | `numbered-cards` |
| 3–5 horizontal steps | `timeline-steps` |
| 3 sequential phases with connectors | `phase-cards` |
| 4–6 stacked label + description rows | `feature-layers` |
| Table of contents | `toc-rows` |
| 2 contrasting blocks | `columns two-col duo` or `columns compare split-panels` |
| Text + diagram / image | `visual-split` |
| Text + supporting stat or quote | `highlight-layout` with `highlight-box` |
| Large single callout | `hero` with `impact-list` |
| Data grid / comparison table | HTML `<table>` |
| 6 focus areas | `labs-grid` |

When a richer pattern fits, **use it** — do not fall back to bullets.

---

### 1. Preserve structure and sequence

- Follow the exact slide order from the plan
- Do not rename, merge, or split slides
- Section slides remain section slides

---

### 2. Define layout explicitly

In `## Layout`, specify:

- Slide class tokens first (required), using this exact line format:
  - `Slide class: content ...` (e.g., `Slide class: content visual-split no-top-accent`)
- Layout type drawn from the deck template (not freeform description)
- Relative proportions where applicable (e.g. 60/40 split)
- Visual hierarchy (primary vs secondary areas)

Use concrete, MARP-compatible class names from `.marp/references/deck-template.md`.

Avoid abstract or aesthetic-only language.

---

### 3. Place content intentionally

In `## Content placement`, describe:

- Which deck-template pattern is used and its HTML container class
- Where each content block is placed within that pattern
- Grouping of items into cards, rows, columns, or callouts
- Emphasis rules (highlight, takeaway, footer note)

Do **not** rewrite or extend content.

---

### 4. Materialize visuals

If the corresponding slide in the plan includes a `## Image` section:

#### 4.1 Decide visual realization

Before creating any file, choose the format using this rubric:

**Use Mermaid when:**
- The visual is a sequential flow, process, or state machine
- The structure maps cleanly to flowchart/graph node-edge semantics
- Hierarchical or directional relationships are the core meaning
- Examples: pipeline steps, architecture dependency graphs, sequence diagrams

**Use Excalidraw when:**
- The visual is a hub-and-spoke or organic network without a dominant direction
- Ideas don't map to Mermaid's defined diagram types (no clean source→target edges)
- Spatial arrangement or grouping conveys meaning (e.g., clusters, proximity)
- Freeform sketch aesthetic matches the content better than a strict graph
- Examples: team/lab organization charts, ecosystem maps, conceptual overviews

---

#### 4.2 Generate Mermaid diagrams (when applicable)

If the planned visual is best represented as a diagram:

- Create a Mermaid diagram source file: `diagrams/<diagram-name>.mmd`
- The diagram must directly reflect the planned visual description
- Keep diagrams minimal and readable

##### Mermaid styling (mandatory)

All Mermaid renders use the shared deck config:
- `.marp/references/mermaid-config.json`

Rules:
- Do not rely on Mermaid default colors.
- Keep diagrams mostly neutral with a single accent (the config sets this).
- Use additional `classDef` styling only when needed for meaning, and keep it consistent with the mermaid config palette:
  - Primary border / line color: `#da291c` (SO accent / red-500)
  - Text: `#3d3935` (merlin)
  - Muted: `#716b5d` (merlin-600)

##### Diagram rules (mandatory)

- Choose the slide class first, then design the diagram to fit:
  - Default: `visual-split`
  - If the rendered PNG aspect ratio is `> 2.8`: add `image-wide`
  - If the rendered PNG aspect ratio is `< 0.8`: add `image-tall`
- Target diagram aspect ratio around **1.1 to 2.6** when possible (easiest fit in `visual-split`).
- Keep **one** diagram/image per slide unless a grid layout is explicitly planned.
- Keep labels short:
  - Aim for **<= 4 words per line**
  - Force line breaks for long text (use `<br/>` in Mermaid labels)
- Flow direction:
  - Prefer `flowchart TB` for **4+ nodes**
  - Use `LR` only when left-to-right meaning is essential
- Avoid long single-lane chains; split into compact groups/subgraphs to reduce extreme width.
- For loop diagrams, use compact cyclic shapes instead of stretched horizontal loops.

After writing the `.mmd` file:
- Render the diagram:
  - Prefer: `task mermaid-file FILE=diagrams/<diagram-name>.mmd`
  - Or rebuild all diagrams: `task mermaid`
- Validate the rendered PNG dimensions before deck render:
  - `task mermaid-check-file FILE=diagrams/<diagram-name>.mmd`
  - If the diagram is too flat/tall, adjust the `.mmd` structure first (direction, grouping, label breaks), then re-render.

- Reference the generated image in `## Image` as: `images/<diagram-name>.png`

Rules:
- Diagram names must be deterministic and descriptive
- One diagram per slide unless explicitly required
- Do not generate diagrams for decorative purposes

If the visual is not diagrammatic, describe it without generating files.

---

#### 4.3 Generate Excalidraw drawings (when applicable)

If the decision rubric in 4.1 selects Excalidraw:

##### File naming
- Create: `diagrams/<diagram-name>.excalidraw`
- Name must be deterministic and descriptive (lowercase, hyphens)

##### Export tool
`task excalidraw-file` renders with `node .marp/scripts/render-excalidraw.js` using
`@napi-rs/canvas` (Node 18+). No Docker dependency.

> **Prerequisite — `package.json` must exist in the project root.**
> `task excalidraw-file` runs `npm install` before every render. If the project has
> no `package.json`, the install silently fails (exit 254) and no PNG is produced.
>
> Before running `task excalidraw-file` for the first time, check for the file:
>
> ```bash
> ls package.json 2>/dev/null || echo "missing"
> ```
>
> If missing, create it:
>
> ```json
> {
>   "name": "deck-builder",
>   "version": "1.0.0",
>   "private": true,
>   "dependencies": {
>     "@napi-rs/canvas": "^0.1.65"
>   }
> }
> ```
>
> Then run `npm install` once manually before invoking the task.
> Subsequent `task excalidraw-file` calls will reuse the installed module.

##### Valid JSON structure
The `.excalidraw` file must be valid JSON matching schema version 2:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "marp-visual-designer",
  "elements": [ ... ],
  "appState": {
    "gridSize": 20,
    "gridStep": 5,
    "gridModeEnabled": false,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

##### Element authoring rules

**Shapes** — use `rectangle` for most nodes; use `ellipse` only when the node is a true radial hub with spokes going in all directions.

Required properties for both:
`id`, `type`, `x`, `y`, `width`, `height`, `angle: 0`, `strokeColor`, `backgroundColor`, `fillStyle: "solid"`, `strokeWidth`, `roughness: 0`, `opacity: 100`, `groupIds: []`, `isDeleted: false`, `boundElements: [...]`, `locked: false`

**Text labels** — one `text` element per shape, with `containerId` pointing to the parent:
- `x`, `y`, `width`, `height` must **exactly match** the parent shape
- Required extra: `text`, `fontSize: 14`, `fontFamily: 1`, `textAlign: "center"`, `verticalAlign: "middle"`, `containerId: "<shape-id>"`, `originalText: "<same as text>"`, `lineHeight: 1.25`
- The parent shape's `boundElements` must include `{"type": "text", "id": "<text-id>"}`
- Multi-line text: use a literal newline character `\n` in the JSON string value

**Arrows** — for static export, always use **null bindings** with explicit coordinate `points`:
- `startBinding: null`, `endBinding: null`
- `startArrowhead: null`, `endArrowhead: "triangle_outline"`
- `points` is an array of `[dx, dy]` offsets relative to the arrow's own `x, y` — the first point is always `[0, 0]`
- For a straight arrow from A-right to B-left: set arrow `x, y` to A's right-center; `points: [[0, 0], [gap, 0]]`
- For an elbowed connector (e.g. row-wrap): use a 4-point path:
  `points: [[0, 0], [0, down], [left_offset, down], [left_offset, down + drop]]`
  where `down` is the midpoint vertical and `left_offset` is negative (moving left)

Required properties: `id`, `type`, `x`, `y`, `width`, `height`, `angle: 0`, `strokeColor`, `backgroundColor: "transparent"`, `fillStyle: "solid"`, `strokeWidth: 2`, `roughness: 0`, `opacity: 100`, `groupIds: []`, `isDeleted: false`, `boundElements: []`, `locked: false`, `points`, `startBinding`, `endBinding`, `startArrowhead`, `endArrowhead`

**Grouping**: assign same string to `groupIds` array for all elements in a logical group

##### Brand color palette (must follow)
| Use | Color |
|---|---|
| Primary hub / main concept | stroke `#da291c`, fill `#ffffff`, strokeWidth `3` |
| Secondary nodes / cards | stroke `#716b5d`, fill `#f4f4f2`, strokeWidth `2` |
| Accent element (e.g. terminal / outcome node) | stroke `#e35205`, fill `#ffffff`, strokeWidth `2` |
| Text | `#3d3935` |
| Flow arrows (same-row) | stroke `#3d3935` |
| Elbowed inter-row connector | stroke `#da291c` |
| Background | `#ffffff` |

##### Aspect-ratio prediction (use before exporting)

`.marp/scripts/render-excalidraw.js` uses fixed `PADDING = 24px` each side and `scale = 2×`. Use these exact formulas to predict the exported PNG size before you export:

```
content_width  = max(element.x + element.width)  − min(element.x)   [all non-arrow elements]
content_height = max(element.y + element.height) − min(element.y)    [all non-arrow elements]

exported_width  = (content_width  + 48) × 2   [exact: PADDING=24 each side, 2× scale]
exported_height = (content_height + 48) × 2   [exact: same]

predicted_ratio = (content_width + 48) / (content_height + 48)
                  [the ×2 cancels; ratio is scale-independent]
```

**Design rule**: target `predicted_ratio` in **1.8–2.4** for a comfortable `visual-split` fit
(well inside the 1.1–2.6 safe band). The formula is exact — no rounding error. With the
recommended `inter_row_gap ≈ 1.4 × node_height` starting point, a 3+3 two-row layout at
150×75 px nodes naturally produces ratio ≈ 1.81, which is within the target band on
the first attempt.

##### Spatial layout guidance

- **Single-row chain** (up to 4 nodes): place nodes left-to-right with 20–30px gaps; straight arrows between them.
- **Multi-row chain** (5+ nodes or when single-row ratio would be > 2.6): split into 2 rows of equal or near-equal length.
  - Row 1: y = 30; row 2: y = 30 + node_height + inter_row_gap
  - Choose `inter_row_gap` so `predicted_ratio` lands in 1.8–2.4:
    `inter_row_gap ≈ (1.4 × node_height)` is a reliable starting point
  - Connect row 1 last node to row 2 first node with a red elbowed arrow:
    - Start at bottom-center of last node in row 1
    - End at top-center of first node in row 2
    - Midpoint: `down = inter_row_gap / 2` from the start
  - Center row 2 horizontally when it has fewer nodes than row 1
- **Hub-and-spoke**: place hub at center; spokes radiate to ~160px radius; use `ellipse` for the hub.
- Allocate **140–160px width × 70–80px height** per node as baseline.

##### Export and validation
After writing the `.excalidraw` file:
1. Predict the ratio using the formula above; adjust layout if needed before exporting.
2. Export: `task excalidraw-file FILE=diagrams/<diagram-name>.excalidraw`
3. Validate actual PNG dimensions: `task mermaid-check-file FILE=diagrams/<diagram-name>.excalidraw`
   - The validation script reads PNG IHDR bytes regardless of source format.
4. If actual ratio is outside target: adjust `inter_row_gap` or node positions, then re-export.

Reference the generated image in `## Image` as: `images/<diagram-name>.png`

Rules:
- Diagram names must be deterministic and descriptive
- One diagram per slide unless explicitly required
- Do not generate diagrams for decorative purposes

---

### 5. Respect MARP constraints

All layouts and visuals must be compatible with:
- Static Markdown slides
- CSS-based theming
- PDF / HTML export

Avoid:
- animations
- interactivity
- layered or dynamic visuals

---

## Section divider slides

For section slides:

- Provide only minimal layout guidance, such as:
- "Centered section title, full slide"
- "Minimal divider, no additional elements"

No visuals or diagrams for section slides.

---

## Quality checks (mandatory)

Before finalizing:

- `.marp/references/deck-template.md` was read before any layout was assigned
- No slide uses a bullet list where a deck-template pattern would fit better
- Mermaid vs Excalidraw decision is justified by content structure, not preference
- Slide order exactly matches the plan
- No new information or interpretation is introduced
- Diagrams strictly reflect planned visuals
- All generated diagrams are referenced correctly
- Output is immediately usable for MARP deck production
- PDF QA: if labels are hard to read at normal zoom, fix diagram structure first (not only CSS)

The result must be **execution-ready**, not exploratory.
