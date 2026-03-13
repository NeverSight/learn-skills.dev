---
name: remix-game-best-practices
description: Mobile-first game creation best practices for Remix
---

# Game Creation Best Practices

## Mobile-First Requirements

- Build for portrait orientation only.
- Canvas must be `720x1080` (2:3 aspect ratio).
- Do not use landscape layouts or controls.
- Design for thumb-friendly interactions and readable UI.

## Mandatory Remix SDK Usage

Include the SDK script in HTML `<head>`:

- `<script src="https://cdn.jsdelivr.net/npm/@remix-gg/sdk@latest/dist/index.min.js"></script>`

Use only the supported SDK APIs:

- `window.RemixSDK.singlePlayer.actions.saveGameState({ gameState: {...} })`
- `window.RemixSDK.singlePlayer.actions.gameOver({ score: number })`
- `window.RemixSDK.onPlayAgain(() => { ... })`
- `window.RemixSDK.onToggleMute((data) => { ... })`
- `window.RemixSDK.ready()`
- `window.RemixSDK.gameState`
- `window.RemixSDK.hapticFeedback()`

## Forbidden APIs and Patterns

- Do not use `localStorage`.
- Do not use `sessionStorage`.
- Do not use `navigator.vibrate(...)`.
- Do not use `window.RemixSDK.vibrate(...)`.
- Do not use non-existent SDK methods (`save`, `checkpoint`, etc.).

## Game Over and Restart Flow

- End runs only with:

```javascript
window.RemixSDK.singlePlayer.actions.gameOver({ score: finalScore })
```

- Do not implement a custom game-over screen.
- Handle replay via `window.RemixSDK.onPlayAgain(...)`.

## State Persistence

- Persist progress only with `saveGameState`.
- Read persisted values from `window.RemixSDK.gameState` after `await window.RemixSDK.ready()`.
- Keep saved state compact and serializable.

## Haptics and Audio

- Use `window.RemixSDK.hapticFeedback()` for collisions, scoring, UI interactions, and game over.
- Respect `onToggleMute` state for all game audio.
- Use lightweight Web Audio API SFX for better mobile performance.

## Framework Rules

### Phaser (2D)

- Use global `Phaser` (no imports).
- Use scene lifecycle (`preload`, `create`, `update`).
- Use Arcade physics for collisions.
- Do not set `parent` in `Phaser.Game` config.

### Three.js + Cannon-ES (3D)

- Use globals `THREE` and `CANNON` (no imports).
- Use `requestAnimationFrame` loop.
- Include ambient + directional lighting.
- Sync mesh transforms from physics bodies every frame.

## Code and Runtime Constraints

- Write ES6 JavaScript only (no TypeScript).
- Do not use `import` statements.
- Assume browser-only runtime (no Node.js APIs).
- Define `initGame()` and call it at the end of the file.

## Validation Checklist

Before finalizing a game, verify:

- Portrait 2:3 canvas (`720x1080`).
- SDK hooks present (`gameOver`, `onPlayAgain`, `onToggleMute`).
- No forbidden storage or vibration APIs.
- Haptics integrated for meaningful gameplay events.
- Restart flow works cleanly from `onPlayAgain`.
