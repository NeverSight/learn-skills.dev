---
name: motion-design-skill
description: |
  Official LottieFiles motion design principles — timing curves, easing, choreography,
  Disney's 12 principles adapted for UI. Implementation-agnostic: works with CSS, GSAP,
  Framer Motion, Lottie. Supports 40+ agents.
triggers:
  - "motion design"
  - "animation principles"
  - "LottieFiles"
  - "Disney principles UI"
  - "timing curves"
das:
  type: package
  category: motion-animation
  upstream: "https://github.com/lottiefiles/motion-design-skill"
  version: latest
  install: false
---

# motion-design-skill

> Catalogue stub — full package: [lottiefiles/motion-design-skill](https://github.com/lottiefiles/motion-design-skill)

## Decision tree

1. **Is the package already installed?**
   Check: your agent's skills directory contains `motion-design-skill` with content beyond this stub.
   - Yes → invoke `motion-design-skill` and proceed
   - No → go to step 2

2. **Which agent are you on?**
   - Claude Code → `npx skills add LottieFiles/motion-design-skill` — or send `! npx skills add …` as a chat message (add `-g` for global, omit for project-only)
   - Cursor → `npx skills add LottieFiles/motion-design-skill`
   - Other → `npx skills add LottieFiles/motion-design-skill` or see [GitHub README](https://github.com/lottiefiles/motion-design-skill)

## Install command

```bash
npx skills add LottieFiles/motion-design-skill
```

## Invoke after install

- Skill name: `motion-design-skill`
- Trigger phrases: "motion design", "animation principles", "LottieFiles", "Disney principles UI", "timing curves"

## What it does

Official LottieFiles motion design principles skill. Covers timing curves, easing functions, animation choreography, and Disney's 12 classic animation principles adapted for UI contexts. Helps agents reason about when to animate, how to choose easing, how to sequence compound animations, and how to balance energy and weight in motion. Implementation-agnostic — the guidance applies equally to CSS transitions, GSAP, Framer Motion, Lottie, or any other animation toolchain. Supports 40+ AI coding agents.

## When NOT to use

- GLSL/shader-level animation (use `shader-dev`)
- Specific framework implementation (use `gsap-skills` or `framer-motion-skills`)
