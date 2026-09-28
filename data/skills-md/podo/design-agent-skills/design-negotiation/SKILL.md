---
name: design-negotiation
description: |
  Advocate for design quality, scope, and time with cross-functional partners using
  evidence and shared goals — not taste or authority.
triggers:
  - "design negotiation"
  - "design advocacy"
  - "defend design decisions"
  - "stakeholder pushback"
  - "design trade-off negotiation"
das:
  type: skill
  category: design-review
  upstream: "https://github.com/Owl-Listener/designer-skills"
  upstream_path: "designer-toolkit/skills/design-negotiation/SKILL.md"
  version: latest
---

# design-negotiation

> Catalogue stub — full skill: [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills)

## Decision tree

1. **Is the full skill already installed?**
   - Global: `grep -q "^das:" ~/.agents/skills/design-negotiation/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/design-negotiation/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/design-negotiation ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add Owl-Listener/designer-skills --skill design-negotiation -g -y
   ```

   **Project:**
   ```bash
   npx skills add Owl-Listener/designer-skills --skill design-negotiation -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.

## What it does

Owls design-negotiation skill: ready-to-use approaches for timeline compression, scope cuts made without design review, stakeholder overrides ("make the button red"), and headcount requests — each grounded in evidence (research, metrics, accessibility, precedent) rather than taste. Plus building long-term influence. Web research found NO public rival; the only matching file online is Owl’s own.

## When NOT to use

- One-off copy/wording help → use `ux-writing-skill`
- Pure PM prioritization frameworks → use `pm-skills`
