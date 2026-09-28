---
name: huashu-design
description: |
  HTML-native design skill producing magazine-grade typography, precise CSS Grid, animated
  prototypes with 20 design philosophies, 5-dimension self-review, and MP4 export.
  Agent-agnostic and works without external component libraries.
triggers:
  - "huashu"
  - "magazine typography"
  - "CSS Grid design"
  - "animated prototype"
  - "MP4 export"
das:
  type: skill
  category: design-systems
  upstream: "https://github.com/alchaincyf/huashu-design"
  upstream_path: "SKILL.md"
  version: latest
  install: true
---

# huashu-design

> Catalogue stub — full skill: [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)

## Decision tree

1. **Is the full skill already installed?**
   Check whether the skill at this location still has a `das:` block:
   - Global: `grep -q "^das:" ~/.agents/skills/huashu-design/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/huashu-design/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke it and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   To detect scope:
   ```bash
   [ -e ~/.agents/skills/huashu-design ] && echo "global" || echo "project"
   ```

   **Global** (installed with `-g`):
   ```bash
   npx skills add alchaincyf/huashu-design --skill huashu-design -g -y
   ```

   **Project** (installed without `-g`):
   ```bash
   npx skills add alchaincyf/huashu-design --skill huashu-design -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.


## Invoke after install

- Skill name: `huashu-design`
- Trigger phrases: "huashu", "magazine typography", "CSS Grid design", "animated prototype", "MP4 export"

## What it does

Produces publication-quality HTML/CSS designs with magazine-grade typography and precise CSS Grid layouts, drawing on 20 named design philosophies. Includes a built-in 5-dimension self-review loop that critiques its own output across readability, hierarchy, proportion, rhythm, and contrast before delivering. Supports animated interactive prototypes and MP4 export for sharing or presenting motion designs. Entirely agent-agnostic — no external component libraries or framework dependencies required.

## When NOT to use

- Non-HTML targets such as React Native, SwiftUI, or backend rendering (the skill is HTML/CSS native)
- When you need a pre-built component library or design system scaffold (use `shadcn-ui` or `design-consultation`)
