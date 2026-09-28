---
name: design-debt-audit
description: |
  Identify, categorize, and prioritize accumulated design inconsistencies and structural
  problems. Debt taxonomy, audit process, Severity×Frequency/Effort scoring, debt register.
triggers:
  - "design debt audit"
  - "design debt triage"
  - "UI inconsistency audit"
  - "design debt register"
das:
  type: skill
  category: design-review
  upstream: "https://github.com/Owl-Listener/designer-skills"
  upstream_path: "design-ops/skills/design-debt-audit/SKILL.md"
  version: latest
---

# design-debt-audit

> Catalogue stub — full skill: [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills)

## Decision tree

1. **Is the full skill already installed?**
   - Global: `grep -q "^das:" ~/.agents/skills/design-debt-audit/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/design-debt-audit/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/design-debt-audit ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add Owl-Listener/designer-skills --skill design-debt-audit -g -y
   ```

   **Project:**
   ```bash
   npx skills add Owl-Listener/designer-skills --skill design-debt-audit -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.

## What it does

Owls design-debt-audit skill: a debt taxonomy (visual / structural / accessibility / documentation / implementation), a 5-step audit process, a Severity×Frequency/Effort prioritization score, and a living debt register. Turns "the UI feels inconsistent" into a triaged, remediable backlog. Nearby public skills cover register lifecycle or code debt but lack Owl’s taxonomy + scoring.

## When NOT to use

- Codebase/technical debt (not design) → a code-quality skill
- Live accessibility violations → use `wcag-audit-patterns`
