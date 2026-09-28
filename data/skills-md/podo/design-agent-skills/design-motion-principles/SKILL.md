---
name: design-motion-principles
description: |
  Motion and interaction design expert with two modes — build interactive
  components with purposeful motion, or audit existing animations for AI-slop
  patterns. Audit emits a branded HTML report with looping CSS demos per finding.
  Based on Emil Kowalski (restraint), Jakub Krehel (production polish), and
  Jhey Tompkins (creative experimentation) — lenses weighted to project context.
  Works with React, Framer Motion, CSS, and HTML.
triggers:
  - "add animation"
  - "audit animation"
  - "hover state"
  - "enter exit animation"
  - "motion review"
  - "AI slop motion"
  - "motion audit"
  - "purposeful motion"
  - "motion principles"
das:
  category: motion-animation
  type: package
  upstream: "https://github.com/kylezantos/design-motion-principles"
  version: latest
---

# design-motion-principles

> Catalogue stub — full skill: [kylezantos/design-motion-principles](https://github.com/kylezantos/design-motion-principles)  
> Type: package — install via `npx skills add` (SKILL.md alone is not sufficient; requires workflow files)

## When to use

Activate when the user wants to:
- Build interactive components with motion (transitions, hover states, micro-interactions, enter/exit animations)
- Audit existing UI motion for AI-slop patterns (pulsing indicators, hover-scale-on-everything, stagger-spam)
- Get motion guidance weighted across Emil Kowalski, Jakub Krehel, and Jhey Tompkins lenses

Do **not** activate for static layout, color, or typography work — route to a design-systems skill instead.

## How to install

```bash
npx skills add kylezantos/design-motion-principles
```

Works with Claude Code, Cursor, Windsurf, and other AI coding assistants.

## How to invoke after install

The skill detects mode from your request:

| You say | Mode |
|---------|------|
| "animate this", "add motion", "make it feel alive" | **Create** |
| "audit my animations", "review motion", "check for AI slop" | **Audit** |
| Ambiguous | Skill asks which mode |

Invoke the `design-motion-principles` skill and state your request.

## What it does

Two modes, three lenses weighted to project context:

| Mode | Output |
|------|--------|
| **Create** | Context discovery → lens weighting → component with motion baked in (React / Framer Motion / CSS / HTML) |
| **Audit** | Motion-gap analysis + anti-AI-slop checklist → branded HTML report with auto-looping CSS demos, or `--terminal` for inline markdown |

**Three lenses:**
- **Emil Kowalski** — Restraint and speed. "Should this animate at all?"
- **Jakub Krehel** — Production polish. "Is this subtle enough?"
- **Jhey Tompkins** — Creative experimentation. "What could this become?"

The productive tension between these three lenses — not one applied universally — is the point.
