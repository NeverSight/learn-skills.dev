---
name: brand-design-md
description: |
  Fetches exact design tokens (colors, type weights, letter-spacing) for 62 world-class brands
  including Stripe, Linear, Apple, Figma, Notion, and Nike at runtime, then applies them to
  your project.
triggers:
  - "brand tokens"
  - "brand design"
  - "match Stripe design"
  - "62 brands"
  - "brand-design-md"
das:
  type: skill
  category: design-systems
  upstream: "https://github.com/zephyrwang6/brand-design-md"
  upstream_path: "SKILL.md"
  version: latest
  install: true
---

# brand-design-md

> Catalogue stub — full skill: [zephyrwang6/brand-design-md](https://github.com/zephyrwang6/brand-design-md)

## Decision tree

1. **Is the full skill already installed?**
   Check whether the skill at this location still has a `das:` block:
   - Global: `grep -q "^das:" ~/.agents/skills/brand-design-md/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/brand-design-md/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke it and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   To detect scope:
   ```bash
   [ -e ~/.agents/skills/brand-design-md ] && echo "global" || echo "project"
   ```

   **Global** (installed with `-g`):
   ```bash
   npx skills add zephyrwang6/brand-design-md --skill brand-design-md -g -y
   ```

   **Project** (installed without `-g`):
   ```bash
   npx skills add zephyrwang6/brand-design-md --skill brand-design-md -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.


## Invoke after install

- Skill name: `brand-design-md`
- Trigger phrases: "brand tokens", "brand design", "match Stripe design", "62 brands", "brand-design-md"

## What it does

At runtime, fetches the precise design tokens — primary and accent colors, type weights, letter-spacing, border-radius, and shadow values — for any of 62 documented world-class brands including Stripe, Linear, Apple, Figma, Notion, Vercel, Airbnb, and Nike. Once fetched, applies those tokens to the current project's CSS variables or Tailwind config so the output accurately reflects the chosen brand's visual language. Useful for building demos, pitch materials, or brand-matched prototypes quickly without manual research.

## When NOT to use

- When you need to develop a custom brand identity from scratch (this skill matches existing brands, not creates new ones)
- When none of the 62 brands match your target (use `design-consultation` to build a bespoke system)
- When brand token accuracy is legally or contractually sensitive (always verify tokens against official brand guidelines)
