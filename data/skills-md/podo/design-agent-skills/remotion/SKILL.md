---
name: remotion
description: |
  Create programmatic videos with React. Official Remotion skill package — compose video
  sequences using React components, animate with spring physics, and render to
  MP4/GIF. Ideal for product demos, explainers, and data-driven videos.
triggers:
  - "remotion"
  - "programmatic video"
  - "React video"
  - "video with React"
  - "animated video"
  - "render video"
das:
  type: package
  category: creative-3d
  upstream: "https://github.com/remotion-dev/skills"
  version: latest
  install: false
---

# remotion

> Catalogue stub — full package: [remotion-dev/skills](https://github.com/remotion-dev/skills)

> **Note:** Upstream restructured the single `remotion` skill into a package of focused
> sub-skills — `remotion-best-practices`, `remotion-create`, `remotion-render`,
> `remotion-captions`, `remotion-docs`, `remotion-interactivity`, `remotion-markup`,
> `remotion-saas`, `remotion-upgrade`, plus `mediabunny`. Install the package to get them all.

## Decision tree

1. **Is the package already installed?**
   Check: your agent's skills directory contains the `remotion-*` skills with content beyond this stub.
   - Yes → invoke the relevant `remotion-*` skill and proceed
   - No → go to step 2

2. **Which agent are you on?**
   - Claude Code → `npx skills add remotion-dev/skills` — or send `! npx skills add …` as a chat message (add `-g` for global, omit for project-only)
   - Cursor → `npx skills add remotion-dev/skills`
   - Other → `npx skills add remotion-dev/skills` or see [GitHub README](https://github.com/remotion-dev/skills)

## Install command

```bash
npx skills add remotion-dev/skills
```

> Installs all Remotion sub-skills. To install just one, append its name, e.g.
> `npx skills add remotion-dev/skills --skill remotion-best-practices`.

## Invoke after install

- Skill names: `remotion-best-practices`, `remotion-create`, `remotion-render`, `remotion-captions`, `remotion-docs`, `remotion-interactivity`, `remotion-markup`, `remotion-saas`, `remotion-upgrade`, `mediabunny`
- Trigger phrases: "remotion", "programmatic video", "React video", "animated video", "render video"

## What it does

Official Remotion skill package for creating programmatic videos with React. Compose video sequences as React components, animate with spring physics and interpolation, and render to MP4, WebM, or GIF. Sub-skills cover best practices, scaffolding new projects (`remotion-create`), rendering (`remotion-render`), captions, interactivity, markup, SaaS integration, and version upgrades. Best for product demos, data-driven visualizations, and explainer animations that require code-controlled precision.

## When NOT to use

- Simple CSS/JS animation without video export (use `gsap-skills` or `framer-motion-skills`)
- Non-React video pipelines (use `hyperframes` for HTML-to-video)
