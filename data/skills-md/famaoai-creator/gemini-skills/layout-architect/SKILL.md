---
name: layout-architect
description: Converts visual designs (images/screenshots) into implementation code (CSS, Python-pptx, HTML). Use when recreating slide layouts or UI designs from images.
status: implemented
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Layout Architect

This skill specializes in **Visual Reverse Engineering**. It analyzes input images or brand guidelines and generates the precise code required to reproduce that design.

## Capabilities

1.  **Slide & Brand Reproduction**:
    - **Image to Marp CSS**: Creates custom themes for Markdown-to-slide conversion.
    - **Brand-to-Theme**: Translates research (colors, logos) into a Marp CSS file AND a shared color palette JSON in `knowledge/templates/themes/palettes/` following the `visual_harmony_guide.md`.
    - **Image to Editable PPTX**: Generates `python-pptx` scripts to build native PowerPoint slides with editable text and shapes.

2.  **UI Reproduction**:
    - **Image to Code**: Converts UI screenshots into HTML/Tailwind, React, or pure CSS.

## Workflow

### 1. Asset Extraction (If input is PPTX)

If the user provides a `.pptx` file instead of an image, first extract the media assets to "see" the design.

```bash
node layout-architect/scripts/extract_images.cjs <path_to_pptx> <output_dir>
```

### 2. Visual Analysis & Theming

Before writing code, analyze the brand assets and define the **Design System**.

- Refer to `knowledge/templates/themes/theme_design_guide.md` for standards on grid layouts and card styles.

## Best Practices

- **Accuracy**: Strive for pixel-perfect layout reproduction.
- **Maintainability**: Use variables/constants for colors and sizes.

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
