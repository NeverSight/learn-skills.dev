---
name: design-consultation
description: |
  Build a complete design system from scratch. Garry Tan's design consultation
  skill: systematic approach to establishing visual language, component library,
  spacing scale, and design tokens from first principles.
triggers:
  - "design consultation"
  - "design system from scratch"
  - "build design system"
  - "design language"
  - "visual language"
das:
  category: design-review
  upstream: "https://github.com/garrytan/gstack"
  upstream_path: "design-consultation/SKILL.md"
  version: latest
  install: true
---

# design-consultation

> Catalogue stub — full skill: [garrytan/gstack](https://github.com/garrytan/gstack/blob/main/design-consultation/SKILL.md)

## Decision tree

1. **Is the full skill already installed?**
   Check whether the skill at this location still has a `das:` block:
   - Global: `grep -q "^das:" ~/.agents/skills/design-consultation/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/design-consultation/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke it and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   To detect scope:
   ```bash
   [ -e ~/.agents/skills/design-consultation ] && echo "global" || echo "project"
   ```

   **Global** (installed with `-g`):
   ```bash
   npx skills add garrytan/gstack --skill design-consultation -g -y
   ```

   **Project** (installed without `-g`):
   ```bash
   npx skills add garrytan/gstack --skill design-consultation -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.


## Invoke after install

- Skill name: `design-consultation`
- Trigger phrases: "design consultation", "design system from scratch", "build design system"

## What it does

Garry Tan's (Y Combinator president) approach to building a complete design system from scratch. Establishes visual language, spacing scale, typography system, color tokens, and component library through a structured consultation process. Opinionated, systematic, and practical for early-stage products.
