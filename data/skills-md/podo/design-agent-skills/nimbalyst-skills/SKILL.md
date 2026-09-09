---
name: nimbalyst-skills
description: |
  3 skills from Nimbalyst IDE: Excalidraw diagrams with MCP tool support,
  UI wireframe mockups alongside architecture diagrams, and data model design.
  Uses a custom skill registry at nimbalyst.com/skills.
triggers:
  - "Nimbalyst"
  - "nimbalyst excalidraw"
  - "nimbalyst mockup"
  - "nimbalyst data model"
das:
  category: diagrams
  upstream: "https://nimbalyst.com/skills"
  version: latest
  install: false
---

# nimbalyst-skills

> Catalogue stub — full package: [nimbalyst.com/skills](https://nimbalyst.com/skills)

## Decision tree

Run this for Nimbalyst IDE skill workflows:

1. **Is a Nimbalyst skill already installed?**
   Check: `~/.design-agent-skills/skills/excalidraw/SKILL.md` exists (from Nimbalyst registry).
   - Yes → invoke the specific skill by name and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
# Excalidraw with MCP tool support (add elements, arrows, frames, Mermaid import)
npx skills add nimbalyst/excalidraw

# UI wireframe mockups alongside architecture diagrams
npx skills add nimbalyst/mockup

# Data model design
npx skills add nimbalyst/datamodel
```

Note: Nimbalyst uses a custom skill registry. If the above fails, install directly from [nimbalyst.com/skills](https://nimbalyst.com/skills).

## Invoke after install

- `excalidraw` (nimbalyst) — "excalidraw with MCP", "interactive excalidraw"
- `mockup` — "UI mockup", "wireframe alongside architecture"
- `datamodel` — "data model design"

## What it does

Nimbalyst IDE's 3 skills with unique MCP-enhanced capabilities: Excalidraw with programmatic element manipulation via MCP tools (add shapes, arrows, frames, import from Mermaid), UI wireframing that co-generates architecture diagrams, and structured data model design.
