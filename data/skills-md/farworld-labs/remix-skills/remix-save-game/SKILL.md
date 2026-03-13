---
name: remix-save-game
description: Add save and load game state functionality via RemixSDK
---

# Integrate Save Game State Workflow

## Overview

This skill guides you through integrating save game state into an HTML game on
the Remix platform. Save game state lets players persist progress across
sessions -- scores, unlocked levels, inventory, and more -- using the RemixSDK.

## Prerequisites

- The game must include the RemixSDK script tag:
  ```html
  <script src="https://cdn.jsdelivr.net/npm/@remix-gg/sdk@latest/dist/index.min.js"></script>
  ```
- The game must already be playable (follow the **game-creation** workflow first
  if starting from scratch).

## Steps

### 1. Initialize the SDK

Call `await window.RemixSDK.ready()` **before** the game loop starts. This
ensures the SDK is loaded and any existing saved state is available.

```js
await window.RemixSDK.ready();
```

### 2. Load Existing State

Read `window.RemixSDK.gameState` to get previously saved data. It returns
`Record<string, unknown> | null | undefined` -- always check for null before
using it.

```js
const savedState = window.RemixSDK.gameState;
```

Use the saved state to restore game progress, or fall back to defaults if the
player is starting fresh:

```js
const state = savedState ?? { score: 0, level: 1 };
```

### 3. Save State During Gameplay

Call `saveGameState` whenever the player reaches a meaningful checkpoint. The
`gameState` value must be a JSON-serializable object.

```js
window.RemixSDK.singlePlayer.actions.saveGameState({
  gameState: { score: player.score, level: player.level },
});
```

## Examples

### Simple Clicker Game

```html
<script>
  let clicks = 0;

  async function init() {
    await window.RemixSDK.ready();

    // Load
    const gameState = window.RemixSDK.gameState;
    if (gameState && typeof gameState.clicks === "number") {
      clicks = gameState.clicks;
    }

    document.getElementById("count").textContent = clicks;
    document.getElementById("btn").addEventListener("click", () => {
      clicks++;
      document.getElementById("count").textContent = clicks;

      // Save after every click
      window.RemixSDK.singlePlayer.actions.saveGameState({
        gameState: { clicks },
      });
    });
  }

  init();
</script>
```

### Platformer with Level Progression

```html
<script>
  let level = 1;
  let coins = 0;

  async function init() {
    await window.RemixSDK.ready();

    // Load
    const saved = window.RemixSDK.gameState;
    if (saved) {
      level = saved.level ?? 1;
      coins = saved.coins ?? 0;
    }

    startLevel(level);
  }

  function onLevelComplete() {
    level++;
    coins += 10;

    // Save at level transitions
    window.RemixSDK.singlePlayer.actions.saveGameState({
      gameState: { level, coins },
    });

    startLevel(level);
  }

  init();
</script>
```

## Tips

- **Keep state small.** Only save what's needed to restore the session -- avoid
  storing large arrays or transient UI state.
- **Save at meaningful moments** -- level completion, checkpoints, purchases --
  not every frame.
- **State must be JSON-serializable.** No functions, class instances, or
  circular references.
- **Always guard against null.** The first time a player loads the game there is
  no saved state.
