---
name: claude2figma
description: |
  Four-skill enforcement layer for design system compliance in Figma: ensures
  components are instances of master components, and colors/fonts/spacing/radii
  bind to Figma variables and styles. Every canvas write is auto-verified for
  token compliance.
triggers:
  - "claude2figma"
  - "Figma token compliance"
  - "Figma variables enforcement"
  - "design system Figma"
  - "senlindesign"
  - "Figma design system enforcement"
das:
  type: package
  category: figma-code
  upstream: "https://github.com/senlindesign/claude2figma"
  version: latest
  install: false
---

# claude2figma

> Catalogue stub — full package: [senlindesign/claude2figma](https://github.com/senlindesign/claude2figma)

## Decision tree

1. **Is the skill already installed?** Check `~/.design-agent-skills/skills/` for `claude2figma` or related skill directories.
   - Yes → invoke and proceed
   - No → go to step 2

2. **Shell access?** Yes → install below. No → show user the command (Claude Code: send with `!` as a chat message — add `-g` for global or omit for project-only).

## Install command

```bash
npx skills add senlindesign/claude2figma
```

## Invoke after install

- Skill name: `claude2figma`
- Triggers: "claude2figma", "Figma token compliance", "Figma variables enforcement", "design system Figma"

## What it does

An enforcement layer comprising four skills that ensure every Figma canvas write complies with your design system. Verifies that placed components are instances of master components (not detached), and that all color, typography, spacing, and border-radius values are bound to Figma variables and styles rather than raw values. Auto-verifies compliance after every canvas operation.

## When NOT to use

- Reading or auditing existing Figma designs — use `figma-official-skills` (Figma MCP)
- Code-to-design without a token-based design system
- Token architecture outside Figma — use `design-tokens-skill`
