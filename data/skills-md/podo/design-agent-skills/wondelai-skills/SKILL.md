---
name: wondelai-skills
description: |
  Design skills derived from seminal books including Refactoring UI, The Design
  of Everyday Things, Inspired (Marty Cagan), JTBD, Hook Model, Design Sprint,
  and Lean UX. Available as individual skills (refactoring-ui,
  design-everyday-things, microinteractions, lean-ux, design-sprint).
triggers:
  - "wondelai"
  - "Refactoring UI skill"
  - "Design of Everyday Things"
  - "microinteractions skill"
  - "Lean UX skill"
  - "Hook Model skill"
  - "Design Sprint skill"
das:
  type: package
  category: design-review
  upstream: "https://github.com/wondelai/skills"
  version: latest
  install: false
---

# wondelai-skills

> Catalogue stub — full package: [wondelai/skills](https://github.com/wondelai/skills)

## Decision tree

1. **Is the skill already installed?** Check `~/.design-agent-skills/skills/` for wondelai skill directories (e.g. `refactoring-ui`, `lean-ux`).
   - Yes → invoke the relevant skill and proceed
   - No → go to step 2

2. **Shell access?** Yes → install below. No → show user the command (Claude Code: send with `!` as a chat message — add `-g` for global or omit for project-only).

## Install command

```bash
npx skills add wondelai/skills
```

> This installs the full suite. Individual skills from this package include: `refactoring-ui`, `design-everyday-things`, `microinteractions`, `lean-ux`, `design-sprint`. Check `ls ~/.design-agent-skills/skills/` after install.

## Invoke after install

- Skill names: `refactoring-ui`, `design-everyday-things`, `microinteractions`, `lean-ux`, `design-sprint`
- Triggers: "Refactoring UI skill", "Design of Everyday Things", "microinteractions skill", "Lean UX skill", "Design Sprint skill"

## What it does

A curated suite of design methodology skills drawn from foundational books. Brings frameworks from Refactoring UI (visual polish heuristics), The Design of Everyday Things (affordances, feedback, mental models), Inspired by Marty Cagan (product design thinking), Jobs To Be Done, the Hook Model (habit-forming product design), Design Sprint (5-day design process), and Lean UX (hypothesis-driven design) into your workflow.

## When NOT to use

- Code implementation — these are design thinking and methodology skills, not code-generation skills
- Component-level visual design — use `color-expert`, `design-tokens-skill`, or `ui-craft`
- Figma execution — use `work-with-design-systems` or `claude2figma`
