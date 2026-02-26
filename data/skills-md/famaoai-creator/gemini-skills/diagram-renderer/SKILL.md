---
name: diagram-renderer
description: Converts diagram code (Mermaid, PlantUML) into image files (PNG/SVG). Useful for visualizing text-based architecture diagrams, flowcharts, and sequence diagrams.
status: implemented
category: Data & Content
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Diagram Renderer

## Overview

This skill acts as a rendering engine for text-based diagrams. It takes code (like Mermaid or PlantUML) as input and outputs high-quality image files.

## Capabilities

### 1. Brand-Themed Rendering

- **Palette Awareness**: Automatically looks up `knowledge/templates/themes/palettes/` for brand-specific colors.
- **Dynamic Styling**: Injects Mermaid `%%{init: ...}%%` directives to match the chart's colors with the overall project theme defined in `visual_harmony_guide.md`.

### 2. Multi-Format Output

2.  **PlantUML to Image** (Planned):
    - Future support for `.puml` files.

## Usage

```bash
# Render a Mermaid file to PNG
node scripts/render.cjs input.mmd output.png

# Render specific format (svg, pdf)
node scripts/render.cjs input.mmd output.svg
```

## Dependencies

- `@mermaid-js/mermaid-cli` (Requires Puppeteer/Chromium)

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
