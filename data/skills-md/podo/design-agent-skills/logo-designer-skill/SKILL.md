---
name: logo-designer-skill
description: |
  Conducts a brand interview, proposes 3-5 distinct SVG logo concepts, refines the chosen
  direction, and exports PNGs at 16px-2048px. Requires resvg, Inkscape, or librsvg for
  PNG export.
triggers:
  - "logo design"
  - "SVG logo"
  - "brand mark"
  - "logo concepts"
  - "logo-designer"
das:
  type: package
  category: design-systems
  upstream: "https://github.com/neonwatty/logo-designer-skill"
  version: latest
  install: false
---

# logo-designer-skill

> Catalogue stub — full package: [neonwatty/logo-designer-skill](https://github.com/neonwatty/logo-designer-skill)

## Decision tree

1. **Is the package already installed?**
   Check: your agent's skills directory contains `logo-designer-skill` with content beyond this stub.
   - Yes → invoke `logo-designer-skill` and proceed
   - No → go to step 2

2. **Which agent are you on?**
   - Claude Code → `claude plugin add neonwatty/logo-designer-skill`
   - Cursor → `claude plugin add neonwatty/logo-designer-skill`
   - Other → `claude plugin add neonwatty/logo-designer-skill` or see [GitHub README](https://github.com/neonwatty/logo-designer-skill)

## Install command

```bash
claude plugin add neonwatty/logo-designer-skill
```

## Invoke after install

- Skill name: `logo-designer-skill`
- Trigger phrases: "logo design", "SVG logo", "brand mark", "logo concepts", "logo-designer"

## What it does

Runs a structured brand interview to capture values, audience, and visual direction before generating 3-5 distinct SVG logo concepts. After the user selects a direction, iterates through refinement rounds to tighten proportions, weight, and scalability. Exports final SVGs and PNGs across the full size spectrum from 16px favicon to 2048px high-res. PNG export requires one of resvg, Inkscape, or librsvg to be available in the environment.

## When NOT to use

- Full brand system design including color, type, and spacing guidelines (use `brand-design-md` to apply an existing brand's tokens)
- When PNG export tools (resvg, Inkscape, librsvg) are not available and raster output is required
- When the deliverable is a complete marketing or product UI rather than a standalone mark
