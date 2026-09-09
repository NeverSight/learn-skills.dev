---
name: localization-design
description: |
  Design interfaces that survive translation, RTL scripts, and cultural difference.
  Per-language text-expansion table, full RTL mirroring rules, non-Latin typography,
  logical CSS properties, and cultural color/icon traps.
triggers:
  - "localization design"
  - "RTL layout design"
  - "text expansion design"
  - "internationalization design"
  - "right-to-left UI"
das:
  type: skill
  category: design-systems
  upstream: "https://github.com/Owl-Listener/designer-skills"
  upstream_path: "design-systems/skills/localization-design/SKILL.md"
  version: latest
---

# localization-design

> Catalogue stub — full skill: [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills)

## Decision tree

1. **Is the full skill already installed?**
   - Global: `grep -q "^das:" ~/.agents/skills/localization-design/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/localization-design/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/localization-design ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add Owl-Listener/designer-skills --skill localization-design -g -y
   ```

   **Project:**
   ```bash
   npx skills add Owl-Listener/designer-skills --skill localization-design -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.

## What it does

Owls best-in-class localization-design skill. Covers the failure modes generic agents miss: text-expansion budgets per language (German +35%, Finnish +40%), full RTL layout mirroring (what flips vs what does not), non-Latin script typography, `margin-inline-start`-style logical properties, and culturally loaded color/icon meanings. Web research found no public skill with deeper localization-*design* coverage.

## When NOT to use

- Pure string/i18n plumbing (use an i18n library, not a design skill)
- General accessibility audits → use `wcag-audit-patterns` or `fixing-accessibility`
