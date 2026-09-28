---
name: interfaces-that-feel
description: |
  An emotional-resonance lens for UI that is technically correct but flat. Translates
  a user’s felt state into specific copy, motion, and interaction changes.
triggers:
  - "interfaces that feel"
  - "emotional interface design"
  - "felt experience"
  - "make it feel human"
  - "emotional resonance UI"
das:
  type: skill
  category: interaction-polish
  upstream: "https://github.com/Owl-Listener/designer-skills"
  upstream_path: "interaction-design/skills/interfaces-that-feel/SKILL.md"
  version: latest
---

# interfaces-that-feel

> Catalogue stub — full skill: [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills)

## Decision tree

1. **Is the full skill already installed?**
   - Global: `grep -q "^das:" ~/.agents/skills/interfaces-that-feel/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/interfaces-that-feel/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/interfaces-that-feel ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add Owl-Listener/designer-skills --skill interfaces-that-feel -g -y
   ```

   **Project:**
   ```bash
   npx skills add Owl-Listener/designer-skills --skill interfaces-that-feel -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.

## What it does

Owls distinctive affective-design method: name the user’s felt state → find a physical-world analogue → extract a behavioral property (weight, resistance, recovery arc) → apply it to easing, delay, copy tone, or spacing. Includes a copy-voice-by-state table and emotional-timing principles. Bigger general UX skills exist, but none package this specific felt-state→property translation.

## When NOT to use

- You need raw motion engineering → use `gsap-skills` or `motion-design-skill`
- A broad design review → use `design-consultation` or `plan-design-review`
