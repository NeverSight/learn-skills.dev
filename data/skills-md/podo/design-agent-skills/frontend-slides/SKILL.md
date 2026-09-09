---
name: frontend-slides
description: |
  Create animation-rich HTML presentations from scratch or convert PPT/PPTX into
  polished web slides. Produces self-contained HTML files with smooth transitions,
  custom layouts, and presenter-friendly controls.
triggers:
  - "frontend slides"
  - "HTML slides"
  - "web presentation"
  - "animated slides"
  - "HTML presentation"
  - "convert PPT to HTML"
das:
  category: presentations
  upstream: "https://github.com/zarazhangrui/frontend-slides"
  upstream_path: "SKILL.md"
  version: latest
  install: true
---

# frontend-slides

> Catalogue stub — full skill: [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides)

## Decision tree

1. **Is the full skill already installed?**
   Check whether the skill at this location still has a `das:` block:
   - Global: `grep -q "^das:" ~/.agents/skills/frontend-slides/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/frontend-slides/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke it and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   To detect scope:
   ```bash
   [ -e ~/.agents/skills/frontend-slides ] && echo "global" || echo "project"
   ```

   **Global** (installed with `-g`):
   ```bash
   npx skills add zarazhangrui/frontend-slides --skill frontend-slides -g -y
   ```

   **Project** (installed without `-g`):
   ```bash
   npx skills add zarazhangrui/frontend-slides --skill frontend-slides -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.


## Invoke after install

- Skill name: `frontend-slides`
- Trigger phrases: "frontend slides", "HTML slides", "web presentation", "animated slides"

## What it does

Creates animation-rich, self-contained HTML presentations from scratch or by converting existing PPT/PPTX files into polished web slides. Supports smooth transitions, custom layouts, speaker notes, and keyboard/touch navigation. Output is a single HTML file — no build step required.
