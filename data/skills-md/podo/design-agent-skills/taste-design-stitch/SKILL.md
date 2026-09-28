---
name: taste-design-stitch
description: |
  Apply design taste and aesthetic judgment to Google Stitch UI output. Elevates
  AI-generated Stitch interfaces beyond generic defaults with opinionated visual
  choices, spacing, and typographic refinement.
triggers:
  - "taste design"
  - "stitch taste"
  - "design taste stitch"
  - "improve stitch UI"
  - "stitch aesthetics"
das:
  category: interaction-polish
  upstream: "https://github.com/google-labs-code/stitch-skills"
  upstream_path: "plugins/stitch-utilities/skills/taste-design/SKILL.md"
  version: latest
  install: true
---

# taste-design-stitch

> Catalogue stub — full skill: [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills/blob/main/plugins/stitch-utilities/skills/taste-design/SKILL.md)

## Decision tree

1. **Is the full skill already installed?**
   Check whether the skill at this location still has a `das:` block:
   - Global: `grep -q "^das:" ~/.agents/skills/taste-design-stitch/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/taste-design-stitch/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke it and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   To detect scope:
   ```bash
   [ -e ~/.agents/skills/taste-design-stitch ] && echo "global" || echo "project"
   ```

   **Global** (installed with `-g`):
   ```bash
   npx skills add google-labs-code/stitch-skills --skill taste-design-stitch -g -y
   ```

   **Project** (installed without `-g`):
   ```bash
   npx skills add google-labs-code/stitch-skills --skill taste-design-stitch -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.


## Invoke after install

- Skill name: `taste-design-stitch`
- Trigger phrases: "taste design", "stitch taste", "improve stitch UI", "stitch aesthetics"

## What it does

Applies aesthetic judgment and design taste to Google Stitch UI output. Pushes generated interfaces past generic AI defaults — opinionated choices on spacing, typography, color, and visual hierarchy that make Stitch output feel crafted rather than computed. Part of Google Labs' official Stitch skills ecosystem.
