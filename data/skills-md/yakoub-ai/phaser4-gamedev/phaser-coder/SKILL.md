---
name: phaser-coder
description: This skill should be used when the user asks to implement Phaser 4 game code, create or edit scenes, add players, enemies, scoring, collectibles, movement, shooting, animations, input, physics behavior, game objects, or complete gameplay features in TypeScript.
version: 0.7.0
---

# Phaser 4 Coder

Use this skill for TypeScript-first Phaser 4 implementation work.

## Workflow

1. Read existing code before editing. Inspect `src/main.ts`, scene files, related objects/managers, shared constants, and asset keys.
2. Match existing naming, folder structure, scene key conventions, and state management patterns.
3. Use Phaser 4 APIs only. Avoid removed Phaser 3 APIs such as `Phaser.Geom.Point`, `Phaser.Math.PI2`, `Phaser.Structs`, and deprecated texture generation patterns.
4. Prefer typed constants/enums for scene keys, registry keys, event names, asset keys, and animation keys.
5. Write complete runnable code. Avoid placeholder TODOs unless the user explicitly asks for a scaffold.
6. After non-trivial edits, run `npx tsc --noEmit` when the project has TypeScript configured.

## Implementation Defaults

- Use class-based scenes extending `Phaser.Scene`.
- Use Arcade Physics for typical platformer/top-down/shooter mechanics unless Matter.js is clearly required.
- Use object pooling for bullets, enemies, particles, and frequent temporary objects.
- Put shared types under `src/types/` and reusable game objects under `src/objects/` or the existing local equivalent.
- Gate debug affordances behind development mode where possible.
- Keep Vite and Phaser setup compatible with browser runtime and strict TypeScript.

## Full Guidance

For the complete coding playbook, read `references/agent-guidance.md`. It is copied from the Claude subagent definition but should be applied as a portable skill; ignore Claude-only fields such as `model`, `color`, and `tools`.
