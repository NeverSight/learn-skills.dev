---
name: design-lab
description: |
  Interactive design exploration environment: conducts design interviews,
  generates multiple UI variants, and refines designs through structured
  iterative feedback loops until the direction is confirmed.
triggers:
  - "design lab"
  - "design exploration"
  - "design variants"
  - "iterative design"
das:
  category: interaction-polish
  upstream: "https://github.com/0xdesign/design-plugin"
  upstream_path: "design-and-refine/skills/design-lab/SKILL.md"
  version: latest
  install: true
---

# design-lab

> Catalogue stub — full skill: [0xdesign/design-plugin](https://github.com/0xdesign/design-plugin)

## Decision tree

Run this before any exploratory design session:

1. **Is the full skill already installed?**
   Check: `~/.design-agent-skills/skills/design-lab/SKILL.md` exists AND does NOT contain a `das:` block.
   - Yes → invoke `design-lab` and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
npx skills add 0xdesign/design-plugin --skill design-lab
```

Or per-agent:
- Claude Code: `claude skills add 0xdesign/design-plugin`
- Cursor/OpenCode: `npx skills add 0xdesign/design-plugin --skill design-lab`

## Invoke after install

- Skill name: `design-lab`
- Trigger phrases: "design lab", "design exploration", "design variants", "iterative design"

## What it does

Runs an interactive design exploration session by first conducting a brief design interview to understand constraints and intent, then generating multiple distinct UI variants. Gathers structured feedback on each variant and iterates until a direction is confirmed and ready for implementation.
