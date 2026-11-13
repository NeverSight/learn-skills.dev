---
name: dimensional-drawing
description: |
  Draw an Apple-style monochrome dimensional drawing of a UI component or physical product:
  one title block plus a dense sheet of plan, exploded and detail views where every
  dimension is a variable code with a formula table instead of a bare number. Use for a
  spec sheet, redline, anatomy drawing or component documentation; a second skill turns the
  finished sheet into a short motion film.
triggers:
  - "dimensional drawing"
  - "spec sheet"
  - "redline drawing"
  - "component anatomy drawing"
das:
  type: package
  category: visual-components
  upstream: "https://github.com/enesozturk/dimensional-drawing"
  version: latest
---

# dimensional-drawing

> Catalogue stub — full skill: [enesozturk/dimensional-drawing](https://github.com/enesozturk/dimensional-drawing)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   This package installs 2 skills (`dimensional-drawing`, `dimensional-drawing-motion`); checking the first.
   - Global: `f=~/.agents/skills/dimensional-drawing/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/dimensional-drawing/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `dimensional-drawing`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/dimensional-drawing ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add enesozturk/dimensional-drawing --skill dimensional-drawing dimensional-drawing-motion -g -y
   ```

   **Project:**
   ```bash
   npx skills add enesozturk/dimensional-drawing --skill dimensional-drawing dimensional-drawing-motion -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **Requires:** Playwright and ffmpeg, only for the headless motion renderer; the Claude artifact route needs neither
- **License:** MIT
<!-- das:install:end -->

## Invoke after install

- Skill name: `dimensional-drawing` (draws the sheet), `dimensional-drawing-motion` (animates a finished sheet)
- Trigger phrases: "dimensional drawing", "spec sheet", "redline drawing"

## What it does

Produces one self-contained HTML sheet in the style of Apple's accessory dimensional drawings: black line on white paper, greys only, a title block with DWG NO. / REV / SHEETS / SCALE / SOURCE and a notes block, then a single SVG sheet with a plan view, a shadow envelope, an exploded axonometric of the layer stack, nested-corner and radius details, and variable tables down the right.

The rules are what make it useful: draw **slots, never content** (lead box with an X, `TITLE SLOT · FLEX`, `CONTENT SLOT · FILL`), use **variable codes instead of numbers** (`H1`, `R2`, `E3`) with derived values as formulas (`R2 = R1 − B − S6 = 11`), stay **unbranded** unless asked, and mark anything absent from the source as `[TBD]` rather than inventing it. Two worked sheets (dialog, card) ship as a drawing kit to copy.

Its companion skill `dimensional-drawing-motion` animates a finished sheet into a roughly 11-second 1920×1080 film — lines drawing themselves, camera pulling back, layers lifting into exploded view — using Claude's Motion artifact type, or Playwright plus ffmpeg elsewhere.

## When NOT to use

- Diagrams that explain a mechanism rather than measure a component — `anatomy` draws interactive isometric figures and is the better fit for "how does this work"
- Flowcharts, architecture or quick sketch diagrams (use `excalidraw-diagram` or `hand-drawn-diagrams`)
- Reading dimensions out of Figma and keeping them in sync with code — `figma-official-skills` and `design-tokens-skill` own that
- Anything with real product photography, colour or branding: this skill is deliberately monochrome and unbranded
