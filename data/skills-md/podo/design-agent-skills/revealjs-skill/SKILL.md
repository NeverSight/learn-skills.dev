---
name: revealjs-skill
description: |
  Generates professional Reveal.js presentations with themed designs, multi-column layouts,
  Chart.js data visualization, speaker notes, staggered animations, and PDF export.
  No build step required — outputs standalone HTML files.
triggers:
  - "Reveal.js"
  - "revealjs-skill"
  - "Reveal presentation"
  - "ryanbbrown slides"
das:
  category: presentations
  upstream: "https://github.com/ryanbbrown/revealjs-skill"
  version: latest
  install: false
---

# revealjs-skill

> Catalogue stub — full package: [ryanbbrown/revealjs-skill](https://github.com/ryanbbrown/revealjs-skill)

## Decision tree

1. **Is the package already installed?**
   Check: `~/.design-agent-skills/skills/revealjs-skill/SKILL.md` exists.
   - Yes → invoke `revealjs-skill` and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
/plugin marketplace add ryanbbrown/revealjs-skill
```

## Invoke after install

- Skill name: `revealjs-skill`
- Trigger phrases: "Reveal.js", "revealjs-skill", "Reveal presentation", "ryanbbrown slides"

## What it does

Generates professional Reveal.js presentations as standalone HTML files requiring no build tooling. Supports themed designs, multi-column slide layouts, embedded Chart.js data visualizations, speaker notes for presenter mode, staggered enter animations, and one-command PDF export via Reveal's print stylesheet. Best for visually rich, browser-displayed presentations with interactivity.

## When NOT to use

- Marp Markdown output — use marp-slides instead
- Slidev/Vue-component presentations — use slidev-skill instead
- PowerPoint/PPTX export — use guizang-ppt instead
- Quality scoring an existing Marp deck — use marp-slide-quality instead
