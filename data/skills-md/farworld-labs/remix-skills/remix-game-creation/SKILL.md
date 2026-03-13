---
name: remix-game-creation
description: Create a new game draft via the Remix API
---

# Game Creation Workflow

## Overview

This skill guides you through creating a new HTML game on the Remix platform.

## Prerequisites

- The `REMIX_API_KEY` environment variable must be set.

## Constraints

- The game must target a **2:3 aspect ratio** (e.g. 720x1080).
- It must fill the entire viewport at that ratio -- use `width: 100vw; height: 100vh`
  on the game container. No scrollbars, no overflow.
- The game **must support touch controls** as the primary input method (the Remix
  platform is primarily mobile/touch-based). Keyboard and mouse controls are
  welcome but optional.

## Steps

### 1. Plan the Game

Decide on the game concept, mechanics, and visual style. Keep scope small --
a single-file HTML game should be playable in under 30 seconds.

### 2. Write the HTML

Create a single HTML file with inline `<style>` and `<script>` tags. Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Game Title</title>
  <script src="https://cdn.jsdelivr.net/npm/@remix-gg/sdk@latest/dist/index.min.js"></script>
  <style>
    /* Game styles can go here */
  </style>
</head>
<body>
  <!-- Game markup can go here -->
  <script>
    // Game logic here
  </script>
</body>
</html>
```

### Required RemixSDK Functions

1. **`window.RemixSDK.singlePlayer.actions.gameOver({ score })`** -- Call when the game
   ends, passing the player's final score as `{ score: number }`. This reports
   the score to the platform.

2. **`window.RemixSDK.onPlayAgain(callback)`** -- Register a callback (no arguments)
   that fires when the player requests to play again. The callback should reset
   game state and restart the game.

3. **`window.RemixSDK.onToggleMute(callback)`** -- Register a callback that receives
   `{ isMuted: boolean }`. The game must mute or unmute all audio based on the
   `isMuted` value.

### 3. Validate

Before uploading, read the HTML file and verify:

1. Has `<!DOCTYPE html>` declaration
2. Has `<meta name="viewport" ...>` tag
3. Has RemixSDK script tag: `<script src="https://cdn.jsdelivr.net/npm/@remix-gg/sdk@latest/dist/index.min.js"></script>`
4. No legacy `@farcade/game-sdk` script tag
5. Calls `singlePlayer.actions.gameOver(` OR `multiplayer.actions.gameOver(` (not both)
6. Registers `.onPlayAgain(` callback
7. Registers `.onToggleMute(` callback
8. No `localStorage` or `sessionStorage` usage
9. No inline event handlers (`onclick=`, `onload=`, etc.)

Fix any issues before proceeding.

### 4. Upload the Game

Follow the **upload-game** workflow to create the game on the Remix platform and
deploy your HTML code.

## Tips

- Use `requestAnimationFrame` for game loops, not `setInterval`.
- Touch controls are required (primary input); keyboard/mouse are optional extras.
- Keep the total HTML under 100KB for fast loading.
