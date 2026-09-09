---
name: pm-skills
description: |
  55 production-ready PM skills organized around the Triple Diamond methodology: 26 phase
  skills (Discover through Iterate), 8 foundation skills (personas, OKRs, lean canvas),
  6 utility meta-skills, and 15 Design Sprint and Foundation Sprint methodology skills.
  Templates, workflows, and sample outputs included.
triggers:
  - "Triple Diamond"
  - "pm-skills"
  - "product-on-purpose"
  - "55 PM skills"
  - "Design Sprint methodology"
das:
  category: product-pm
  upstream: "https://github.com/product-on-purpose/pm-skills"
  version: latest
  install: false
---

# pm-skills

> Catalogue stub — full package: [product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills)

## Decision tree

1. **Is the package already installed?**
   Check: `~/.design-agent-skills/skills/pm-skills/SKILL.md` exists.
   - Yes → invoke the relevant PM skill and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
/plugin marketplace add product-on-purpose/pm-skills
```

## Invoke after install

- Skill name: `pm-skills`
- Trigger phrases: "Triple Diamond", "pm-skills", "product-on-purpose", "55 PM skills", "Design Sprint"

## What it does

Provides 55 structured PM skills organized by the Triple Diamond product development framework. The 26 phase skills cover each stage from Discovery through Iteration (problem framing, research synthesis, ideation, prototyping, validation, launch). The 8 foundation skills cover recurring artifacts like personas, OKR trees, and lean canvas. The 6 utility meta-skills handle cross-cutting concerns and skill lifecycle. The 15 sprint skills cover Design Sprint and Foundation Sprint facilitation. Worked sample outputs are bundled for reference.

## When NOT to use

- Single PRD generation — use deanpeters-pm-skills for a lighter workflow
- Marketing and CRO work — use coreyhaines-marketing instead
- UX research focus only — use phuryn-pm-skills instead
