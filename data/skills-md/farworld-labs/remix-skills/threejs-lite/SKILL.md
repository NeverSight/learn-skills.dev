---
name: threejs-lite
description: Build lightweight mobile-friendly 3D browser games with Three.js
metadata:
  tags: threejs, webgl, game-dev, 3d, remix
---

# Three.js Lite

Use this skill when a user wants a 3D browser game with minimal rendering complexity and stable mobile performance.

## Workflow

1. Start from `assets/starter-single-file.html`.
2. Implement one camera, one scene, one gameplay loop.
3. Add player input and terminal condition before adding visual polish.
4. Keep geometry/material count small and predictable.
5. If targeting Remix, apply hooks in `references/sdk-integration.md`.
6. Validate required hooks (`gameOver`, `onPlayAgain`, `onToggleMute`) before handoff.

## Guardrails

- Keep draw calls low and avoid postprocessing by default.
- Prefer simple `MeshBasicMaterial`/`MeshStandardMaterial` setups.
- Avoid dynamic shadows on first pass.
- For Remix uploads, output single-file HTML with inline JS/CSS unless user asks otherwise.
- For Remix uploads, include `<script src="https://cdn.jsdelivr.net/npm/@remix-gg/sdk@latest/dist/index.min.js"></script>` in HTML `<head>`.
- Treat 3D as optional style; gameplay clarity is higher priority than visual complexity.

## References

- `references/threejs-mobile-patterns.md` for scene setup, controls, and perf budgets.
- `references/sdk-integration.md` for SDK hooks required by Remix validation.
