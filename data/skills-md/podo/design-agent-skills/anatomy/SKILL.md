---
name: anatomy
description: |
  Build carefully crafted, interactive isometric SVG figures that explain a technical idea
  as a real physical object — a machine whose moving parts are the concept — framed in a card
  with a title, hint and live readout. Use for isometric illustrations, explanatory figures
  for docs or blog posts, and interactive explainers of how a system, algorithm or component
  works. Optionally adds WebGL shaders, true 3D, or a printable A4 PDF.
triggers:
  - "isometric illustration"
  - "anatomy figure"
  - "interactive explainer"
  - "explainer diagram"
  - "technical illustration"
das:
  type: skill
  category: diagrams
  upstream: "https://github.com/wheresryan22/anatomy"
  upstream_path: "SKILL.md"
  version: latest
---

# anatomy

> Catalogue stub — full skill: [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/anatomy/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/anatomy/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `anatomy`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/anatomy ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add wheresryan22/anatomy --skill anatomy -g -y
   ```

   **Project:**
   ```bash
   npx skills add wheresryan22/anatomy --skill anatomy -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **License:** MIT
<!-- das:install:end -->

## Invoke after install

- Skill name: `anatomy`
- Trigger phrases: "isometric illustration", "anatomy figure", "interactive explainer"

## What it does

Invents and draws a real object whose mechanism *is* the idea being explained, instead of boxes and arrows. One line of prompt ("explain how an LRU cache evicts entries, interactive") yields a self-contained interactive figure: dozens to hundreds of solid parts, one isometric camera looking down at 30°, four-tone shading, painter's order solved per frame, one lit accent part, and a live readout whose numbers come from the same small model that drives the motion.

Work happens in a fixed order — size the figure (Figure / Hero / Epic), collect the real numbers into a model, invent the object, list 40+ parts, plan the world, build geometry once, paint back to front, frame it, make it live, then audit it with screenshots at 4×. Output is framework-free TypeScript that writes SVG and HTML, React/Next.js components, or a printable A4 PDF (poster, drawing, handout). Opt-in keywords in the prompt add WebGL shaders (`WebGL`) or true 3D (`3D`), and it respects `prefers-reduced-motion` with keyboard and pointer interaction.

Six worked examples ship with it, from a ~300-line dial gauge up to a full turbofan engine, and the agent opens the closest one before starting. Expect 30–90 minutes for a normal figure; a Hero is 2–4 hours.

## When NOT to use

- Structural or flow diagrams where the boxes-and-arrows abstraction *is* the point (use `excalidraw-diagram`, or `hand-drawn-diagrams` for a rough sketch look)
- Anything that has to come back in seconds: this skill optimises for detail over speed and will not trade parts for turnaround
- Abstract data charts and infographics (use `antvis-chart-skills`), or 3D scenes that are art rather than explanation (use `threejs-claude-skill-package` or `shader-dev`)
