---
name: phaser-2d-arcade
description: Build mobile-first 2D browser games with Phaser 3 Arcade Physics
metadata:
  tags: phaser, game-dev, html5, arcade-physics, remix
---

# Phaser 2D Arcade

Use this skill when a user asks for a Phaser browser game, especially for fast single-file 2D gameplay loops.

## Workflow

1. Start from `assets/starter-single-file.html`.
2. Implement core loop first: `boot -> preload -> create -> update`.
3. Add win/lose condition and scoring before polish.
4. Add touch controls and responsive layout early (mobile-first).
5. If targeting Remix, apply SDK hooks from `references/sdk-integration.md`.
6. Validate required hooks (`gameOver`, `onPlayAgain`, `onToggleMute`) before handoff.

## Guardrails

- Prefer Phaser Arcade Physics for simplicity/performance.
- Keep initial scope small: 1 scene, 1 mechanic, 1 fail condition.
- Avoid expensive per-frame allocations and unnecessary visual effects.
- Keep gameplay restart-safe and deterministic.
- For Remix uploads, produce single-file HTML with inline JS/CSS unless user asks otherwise.
- For Remix uploads, include `<script src="https://cdn.jsdelivr.net/npm/@remix-gg/sdk@latest/dist/index.min.js"></script>` in HTML `<head>`.

## References

- `references/phaser-arcade-patterns.md` for scene architecture, controls, and perf defaults.
- `references/sdk-integration.md` for Remix SDK hooks and integration shape.
