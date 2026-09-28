---
name: marp-slides
description: |
  Marp presentation skill with 22 curated example decks, SVG charts, dashboard components,
  and dark/light themes. Teaches slide composition and visual quality patterns for
  Markdown-based presentations rendered with the Marp framework.
triggers:
  - "Marp"
  - "marp-slides"
  - "Marp presentation"
  - "robonuggets slides"
das:
  type: skill
  category: presentations
  upstream: "https://github.com/robonuggets/marp-slides"
  upstream_path: "SKILL.md"
  version: latest
  install: true
---

# marp-slides

> Catalogue stub — full skill: [robonuggets/marp-slides](https://github.com/robonuggets/marp-slides)

## Decision tree

1. **Is the full skill already installed?**
   Check whether the skill at this location still has a `das:` block:
   - Global: `grep -q "^das:" ~/.agents/skills/marp-slides/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/marp-slides/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke it and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   To detect scope:
   ```bash
   [ -e ~/.agents/skills/marp-slides ] && echo "global" || echo "project"
   ```

   **Global** (installed with `-g`):
   ```bash
   npx skills add robonuggets/marp-slides --skill marp-slides -g -y
   ```

   **Project** (installed without `-g`):
   ```bash
   npx skills add robonuggets/marp-slides --skill marp-slides -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.


## Invoke after install

Skill name: `marp-slides`, triggers: "Marp", "marp-slides", "Marp presentation", "robonuggets slides"

## What it does

Creates Marp Markdown presentations informed by 22 curated real-world example decks covering different content types and visual styles. Includes SVG-based chart components, dashboard-style layout components, and dark/light theme variants. The examples teach the skill correct slide composition: appropriate information density, visual hierarchy, and component reuse patterns.

## When NOT to use

- Animated or interactive slides — use revealjs-skill instead
- Vue-component developer presentations — use slidev-skill instead
- Quality-checking an existing Marp deck — use marp-slide-quality as a companion after creation
