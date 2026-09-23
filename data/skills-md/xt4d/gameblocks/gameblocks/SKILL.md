---
name: gameblocks
description: Use when building or revising browser-based 3D games with GameBlocks modules, especially for coordinate systems, actor motion, camera rigs, collision-aware movement, gameplay state, and world building.
---

# GameBlocks

Use GameBlocks as source material before inventing 3D game systems from scratch.

## Workflow

- Use `modules/math/WorldBasis.js` as the single source of truth for gameplay-space coordinates, forward/right/up axes, planar movement, heading, and control-signal transforms.
- Review `summary.md` and select modules that can support the game implementation. Prioritize existing modules whenever possible, especially for motion controllers and camera rigs.
- Copy each selected module into the target project's source directory while preserving its relative directory structure so imports continue to work. If a selected module fully satisfies the game design requirements, reuse it as-is. If it only partially satisfies the requirements, adapt it from the existing implementation instead of rewriting it from scratch.
- Create `gameblocks_usage.md` documenting the selected modules, their purpose, reuse/adaptation status, key changes, and game integration.