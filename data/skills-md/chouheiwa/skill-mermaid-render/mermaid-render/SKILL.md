---
name: mermaid-render
description: "Render Mermaid diagrams to SVG/PNG/PDF with optional hand-drawn (sketch) style. Supports all diagram types, multiple output formats, custom themes, CJK text, Markdown input, and batch processing."
---

# Mermaid Render

Render Mermaid diagrams to SVG/PNG/PDF. Supports standard Mermaid output as well as hand-drawn (sketch) style via svg2roughjs — identical to Mermaid Live Editor's hand-drawn mode.

By default, hand-drawn style is **enabled**. Use `--no-handdrawn` for standard Mermaid output.

## When to Use This Skill

1. User asks to "render", "visualize", or "generate" a Mermaid diagram
2. User provides .mmd files or Mermaid code blocks and needs output images
3. User wants to "create a flowchart/sequence/state/class/ER diagram"
4. User needs to extract and render diagrams from a Markdown document
5. User wants to "batch process" a directory of .mmd files
6. User mentions "hand-drawn", "sketch", or "rough" style — keep default or add `--pencil-filter`
7. User wants clean/standard Mermaid output (no hand-drawn) — use `--no-handdrawn`

## ⚠️ Path Resolution (Important)

All scripts are located in the same directory as this SKILL.md. Before running any script, you **must** determine the actual path of this file and derive the script directory from it.

**Rule:** Replace every `$SKILL_DIR` placeholder in this document with the absolute path of the directory containing this SKILL.md file.

Example: if this file is at `/path/to/mermaid-render/SKILL.md`, then `$SKILL_DIR` = `/path/to/mermaid-render`.

```bash
SKILL_DIR="<absolute path to the directory containing this SKILL.md>"
```

---

## Quick Start

### Standard Mermaid output (no hand-drawn)

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input diagram.mmd \
  --output diagram.svg \
  --no-handdrawn
```

### Hand-drawn style (default)

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input diagram.mmd \
  --output diagram.svg
```

### Output as PNG (high resolution)

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input diagram.mmd \
  --output diagram.png \
  --scale 2
```

### Output as PDF

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input diagram.mmd \
  --output diagram.pdf \
  --pdf-fit
```

### Extract and render from Markdown

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input document.md \
  --output ./output-dir
```

### Batch render

```bash
node "$SKILL_DIR/scripts/batch.mjs" \
  --input-dir ./diagrams \
  --output-dir ./output
```

---

## Workflow

**Step 1: What does the user want?**
- **Render existing Mermaid code** → Save as .mmd file, use render.mjs
- **Extract diagrams from Markdown** → Pass .md file directly
- **Create a new diagram** → Refer to templates in `$SKILL_DIR/assets/example_diagrams/`
- **Batch process** → Use batch.mjs

**Step 2: Choose output style**
- Default (hand-drawn) — sketch/rough style via svg2roughjs, same as Mermaid Live Editor
- `--no-handdrawn` — clean standard Mermaid output, no sketch effect

**Step 3: Choose output format**
- `svg` — Vector, ideal for web and docs (default)
- `png` — Bitmap, ideal for embedding and sharing (use --scale for resolution)
- `pdf` — Ideal for printing (use --pdf-fit for auto-sizing)

**Step 4: Choose theme**
- `default` — Mermaid default theme
- `neutral` — Neutral tones, good for documentation
- `dark` — Dark theme
- `forest` — Green theme

**Step 5: Render**
```bash
node "$SKILL_DIR/scripts/render.mjs" -i input.mmd -o output.svg --theme neutral
```

---

## Options

### render.mjs

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | Input file (.mmd or .md) | required |
| `-o, --output` | Output file (.svg/.png/.pdf) | required |
| `-e, --format` | Output format: svg, png, pdf | inferred from extension |
| `-t, --theme` | Mermaid theme | `default` |
| `--bg` | Background color | `transparent` |
| `-w, --width` | Page width | `800` |
| `-H, --height` | Page height | `600` |
| `-s, --scale` | Scale factor (affects PNG resolution) | `1` |
| `-c, --config` | Mermaid JSON config file | none |
| `-C, --css` | Custom CSS file | none |
| `--pdf-fit` | Fit PDF to diagram size | off |
| `--icon-packs` | Icon packs, comma-separated | none |
| `--font` | Font family for hand-drawn mode | `Comic Sans MS, cursive` |
| `--pencil-filter` | Enable pencil filter effect (hand-drawn only) | off |
| `--randomize` | Enable per-element randomization (causes variable hachure density) | off |
| `--seed` | Random seed | none |
| `--roughness` | Roughness level (hand-drawn only) | rough.js default |
| `--bowing` | Bowing level (hand-drawn only) | rough.js default |
| `--hachure-gap` | Gap between hachure lines in px (smaller = denser) | `2` |
| `--fill-weight` | Width of hachure lines in px | `1.5` |
| `--no-handdrawn` | Skip hand-drawn conversion, output raw Mermaid SVG | off |

### batch.mjs

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input-dir` | Input directory | required |
| `-o, --output-dir` | Output directory | required |
| `-e, --format` | Output format: svg, png, pdf | `svg` |
| `-t, --theme` | Mermaid theme | `default` |
| `--bg` | Background color | `transparent` |
| `-s, --scale` | Scale factor (affects PNG resolution) | `1` |
| `--font` | Font family (hand-drawn mode) | `Comic Sans MS, cursive` |
| `--pencil-filter` | Enable pencil filter effect | off |
| `--randomize` | Enable per-element randomization | off |
| `--seed` | Random seed | none |
| `--roughness` | Roughness level | rough.js default |
| `--bowing` | Bowing level | rough.js default |
| `--hachure-gap` | Gap between hachure lines in px | `2` |
| `--fill-weight` | Width of hachure lines in px | `1.5` |
| `--no-handdrawn` | Skip hand-drawn conversion | off |
| `--concurrency` | Max parallel renders | `3` |

---

## Examples

### Flowchart — standard style

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input "$SKILL_DIR/assets/example_diagrams/flowchart.mmd" \
  --output flowchart.svg \
  --no-handdrawn
```

### Flowchart — hand-drawn style

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input "$SKILL_DIR/assets/example_diagrams/flowchart.mmd" \
  --output flowchart.svg
```

### Sequence diagram (high-res PNG, neutral theme)

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input "$SKILL_DIR/assets/example_diagrams/sequence.mmd" \
  --output sequence.png \
  --scale 2 --theme neutral
```

### State diagram (auto-fit PDF)

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input "$SKILL_DIR/assets/example_diagrams/state.mmd" \
  --output state.pdf \
  --pdf-fit --theme dark
```

### Extract all diagrams from Markdown

```bash
# Single code block → single output file
node "$SKILL_DIR/scripts/render.mjs" -i doc.md -o diagram.svg

# Multiple code blocks → output to directory (auto-named doc-1.svg, doc-2.svg, ...)
node "$SKILL_DIR/scripts/render.mjs" -i doc.md -o ./output-dir
```

### Custom Mermaid config

```bash
# config.json: { "theme": "neutral", "flowchart": { "curve": "basis" } }
node "$SKILL_DIR/scripts/render.mjs" \
  --input diagram.mmd \
  --output diagram.svg \
  --config config.json
```

### Custom CSS

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input diagram.mmd \
  --output diagram.svg \
  --css custom.css
```

### Icon packs

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input diagram.mmd \
  --output diagram.svg \
  --icon-packs @iconify-json/logos
```

### Reproducible hand-drawn output (fixed seed)

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input diagram.mmd \
  --output diagram.svg \
  --seed 42 --no-randomize
```

### Pencil filter effect

```bash
node "$SKILL_DIR/scripts/render.mjs" \
  --input diagram.mmd \
  --output diagram.svg \
  --pencil-filter
```

---

## Creating diagrams from user requirements

**Step 1: Identify diagram type**
- Process / workflow → `graph TD` or `flowchart LR`
- API / interaction → `sequenceDiagram`
- State / lifecycle → `stateDiagram-v2`
- Object model → `classDiagram`
- Database → `erDiagram`
- Timeline → `timeline`
- Gantt / project → `gantt`
- Mind map → `mindmap`

**Step 2: Create .mmd file**
Refer to templates in `$SKILL_DIR/assets/example_diagrams/`.

**Step 3: Render and iterate**
```bash
node "$SKILL_DIR/scripts/render.mjs" -i diagram.mmd -o preview.svg
# Edit diagram.mmd based on feedback, re-render
```

---

## Features

### Mermaid rendering
- All Mermaid diagram types supported (flowchart, sequence, state, class, ER, timeline, gantt, mindmap, etc.)
- Output SVG / PNG / PDF
- Markdown input support (auto-extracts mermaid code blocks)
- CJK (Chinese/Japanese/Korean) text auto-optimization
- Custom Mermaid config and CSS
- Icon pack support (Iconify)
- Custom themes: default, neutral, dark, forest

### Hand-drawn style (default, disable with --no-handdrawn)
- Identical to Mermaid Live Editor hand-drawn mode (powered by svg2roughjs)
- Custom node colors (style directives) preserved
- Pencil filter effect
- Roughness and bowing controls
- Reproducible output via seed parameter

## Dependencies

- Node.js 18+
- puppeteer, svg2roughjs, and @mermaid-js/mermaid-cli (all installed via `npm install`)

## Troubleshooting

### mmdc not found
```
❌ @mermaid-js/mermaid-cli not found
```
**Fix:** `npm install`

### puppeteer install fails
Puppeteer needs to download Chromium. Ensure network access. Manual install:
```bash
cd "$SKILL_DIR" && npm install
```

### Mermaid syntax errors
Validate syntax at https://mermaid.live/ before rendering.

---

## File structure

### scripts/
- `render.mjs` — Single-file renderer (SVG/PNG/PDF, Markdown input)
- `batch.mjs` — Batch renderer

### assets/
- `example_diagrams/flowchart.mmd` — Flowchart template
- `example_diagrams/sequence.mmd` — Sequence diagram template
- `example_diagrams/state.mmd` — State diagram template
