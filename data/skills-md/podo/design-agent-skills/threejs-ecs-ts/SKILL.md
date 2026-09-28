---
name: threejs-ecs-ts
description: |
  Three.js combined with Entity Component Systems (ECS) and TypeScript, adding structured
  game and interactive architecture patterns on top of Three.js rendering for complex
  interactive scenes with many independent objects.
triggers:
  - "Three.js ECS"
  - "entity component"
  - "threejs-ecs-ts"
  - "Nice Wolf Studio"
  - "3D game architecture"
das:
  category: creative-3d
  upstream: "https://github.com/Nice-Wolf-Studio/claude-skills-threejs-ecs-ts"
  version: latest
  install: false
---

# threejs-ecs-ts

> Catalogue stub — full package: [Nice-Wolf-Studio/claude-skills-threejs-ecs-ts](https://github.com/Nice-Wolf-Studio/claude-skills-threejs-ecs-ts)

## Decision tree

1. **Is the package already installed?**
   Check: `~/.design-agent-skills/skills/threejs-ecs-ts/SKILL.md` exists.
   - Yes → invoke `threejs-ecs-ts` and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
npx skills add Nice-Wolf-Studio/claude-skills-threejs-ecs-ts
```

## Invoke after install

- Skill name: `threejs-ecs-ts`
- Trigger phrases: "Three.js ECS", "entity component", "3D game architecture"

## What it does

Combines Three.js rendering with Entity Component System (ECS) architecture patterns in TypeScript, providing a structured approach to managing complex interactive 3D scenes. ECS separates data (components) from logic (systems) and entities (IDs), enabling scalable scenes with many independent objects such as game characters, simulations, or interactive installations. Ideal when scene complexity exceeds what simple object hierarchies can manage cleanly.

## When NOT to use

- Simple Three.js scenes without architectural complexity — use cloudai-threejs instead
- WebGPU-specific rendering features — use webgpu-claude-skill instead
- Architecture/BIM 3D workflows — use threejs-claude-skill-package instead
