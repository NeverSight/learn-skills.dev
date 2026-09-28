---
name: cloudai-threejs
description: |
  Three.js skills for creating interactive 3D elements and experiences on the web.
  Covers scene setup, geometries, materials, lighting, cameras, animations,
  and WebGL rendering best practices.
triggers:
  - "Three.js"
  - "threejs"
  - "3D web"
  - "WebGL 3D"
  - "3D scene"
  - "3D animation"
das:
  category: creative-3d
  upstream: "https://github.com/CloudAI-X/threejs-skills"
  version: latest
  install: false
---

# cloudai-threejs

> Catalogue stub — full package: [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills)

## Decision tree

Run this before any Three.js or 3D web development:

1. **Is the Three.js skill already installed?**
   Check: `~/.design-agent-skills/skills/threejs/SKILL.md` exists.
   - Yes → invoke `threejs` and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
npx skills add CloudAI-X/threejs-skills
```

## Invoke after install

- Skill name: check installed skill names with `ls ~/.design-agent-skills/skills/`
- Trigger phrases: "Three.js", "3D web", "WebGL 3D", "3D scene"

## What it does

Three.js skill suite for building interactive 3D elements and experiences on the web. Covers the complete Three.js pipeline: scene and renderer setup, geometries and materials, lighting rigs, camera controls, object animations, and WebGL performance best practices. Use for product visualizations, interactive backgrounds, and immersive web experiences.
