---
name: vercel-skills
description: |
  4 official Vercel skills for web design guidelines, component building, React
  performance, and composition patterns. Enforces 100+ Web Interface Guidelines
  and accessible, composable component APIs.
triggers:
  - "Vercel skill"
  - "web design guidelines"
  - "building components"
  - "React best practices"
  - "composition patterns"
  - "Web Interface Guidelines"
das:
  category: official-suites
  upstream: "https://github.com/vercel-labs/skills"
  version: latest
  install: false
---

# vercel-skills

> Catalogue stub — full package: [vercel-labs/skills](https://github.com/vercel-labs/skills)

## Decision tree

Run this before using Vercel skill workflows:

1. **Is a Vercel skill already installed?**
   Check: `~/.design-agent-skills/skills/building-components/SKILL.md` exists (representative skill).
   - Yes → invoke the specific skill by name and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → install the specific skill below, then invoke it
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
# Review UI code against 100+ Web Interface Guidelines
npx skills add vercel-labs/web-design-guidelines

# Build accessible, composable, themeable UI components
npx skills add vercel-labs/building-components

# React/Next.js performance optimization
npx skills add vercel-labs/react-best-practices

# React component composition and reusable patterns
npx skills add vercel-labs/composition-patterns
```

> Note: `web-design-guidelines` may be a stale listing — verify install before use.

## Invoke after install

- `web-design-guidelines` — "web design guidelines", "UI review"
- `building-components` — "build component", "accessible component", "composable API"
- `react-best-practices` — "React performance", "Next.js optimization"
- `composition-patterns` — "composition patterns", "reusable React patterns"

## What it does

Vercel's official skill collection: enforces 100+ Web Interface Guidelines in UI code review, guides accessible and composable component architecture, optimizes React/Next.js performance, and establishes reusable component composition patterns.
