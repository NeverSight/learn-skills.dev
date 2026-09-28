---
name: nanobanan-ppt
description: |
  AI-powered PowerPoint generation with document analysis and styled image generation.
  Analyzes input documents, structures content into slides, and generates matching
  visual assets. Requires API credentials for image generation features.
triggers:
  - "NanoBanana"
  - "nanobanan ppt"
  - "AI PowerPoint"
  - "styled PPT"
  - "PPT with images"
  - "document to slides"
das:
  category: presentations
  upstream: "https://github.com/op7418/NanoBanana-PPT-Skills"
  upstream_path: "SKILL.md"
  version: latest
  install: true
---

# nanobanan-ppt

> Catalogue stub — full skill: [op7418/NanoBanana-PPT-Skills](https://github.com/op7418/NanoBanana-PPT-Skills)

## Decision tree

1. **Is the full skill already installed?**
   Check whether the skill at this location still has a `das:` block:
   - Global: `grep -q "^das:" ~/.agents/skills/nanobanan-ppt/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/nanobanan-ppt/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke it and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   To detect scope:
   ```bash
   [ -e ~/.agents/skills/nanobanan-ppt ] && echo "global" || echo "project"
   ```

   **Global** (installed with `-g`):
   ```bash
   npx skills add op7418/NanoBanana-PPT-Skills --skill nanobanan-ppt -g -y
   ```

   **Project** (installed without `-g`):
   ```bash
   npx skills add op7418/NanoBanana-PPT-Skills --skill nanobanan-ppt -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.


## Invoke after install

- Skill name: `nanobanan-ppt`
- Trigger phrases: "NanoBanana", "AI PowerPoint", "styled PPT", "document to slides"

## What it does

AI-powered PowerPoint generation that goes beyond text structure: analyzes input documents for content and tone, structures content into coherent slide decks, and generates styled images matched to the presentation theme. Output is a fully assembled .pptx with both content and visuals. Image generation requires external API credentials.

## When NOT to use

- Simple text-only slide generation → use `guizang-ppt` instead (no API deps)
- When you don't have image API credentials configured
