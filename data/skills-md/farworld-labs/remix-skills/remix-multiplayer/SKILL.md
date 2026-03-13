---
name: remix-multiplayer
description: Enable multiplayer support for a Remix game
---

# Implement Multiplayer Workflow

## Overview

This skill guides you through enabling and integrating multiplayer functionality
for games on the Remix platform.

## Prerequisites

- A game must be created on the Remix platform (you need a game ID).
- The `REMIX_API_KEY` environment variable must be set.
- The game must include the RemixSDK script tag:
  ```html
  <script src="https://cdn.jsdelivr.net/npm/@remix-gg/sdk@latest/dist/index.min.js"></script>
  ```

## Steps

### 1. Check for Existing Game ID

Read `.remix-settings.json` in the current directory. If it exists and contains
a `gameId`, use that value.

Only if `.remix-settings.json` does not exist or has no `gameId` should you
follow the **upload-game** workflow to create one.

### 2. Enable Multiplayer

Enable multiplayer for the game via REST:

```
POST https://api.remix.gg/v1/games/{gameId}
Authorization: Bearer $REMIX_API_KEY
Content-Type: application/json

{ "isMultiplayer": true }
```

### 3. Integrate Multiplayer in Game Code

```js
const sdk = window.RemixSDK
await sdk.ready()

// Access all players in the session
const players = sdk.players // Array of player objects

// Listen for game state updates from other players
sdk.onGameStateUpdated((state) => {
  // Sync game state from other players
})

// Send game state to other players
sdk.multiplayer.actions.gameOver({ scores: playerScores })
```

### Important: Use Multiplayer gameOver

For multiplayer games, use `multiplayer.actions.gameOver` -- NOT
`singlePlayer.actions.gameOver`. Pass a scores object keyed by player ID:

```js
sdk.multiplayer.actions.gameOver({
  scores: { [playerId]: score }
})
```

### Keep Standard Hooks

Multiplayer games still need these callbacks:

```js
sdk.onPlayAgain(() => {
  // Reset game state and restart
})

sdk.onToggleMute(({ isMuted }) => {
  // Mute or unmute all audio
})
```

## Tips

- Use `sdk.players` to get the list of players and their IDs.
- `onGameStateUpdated` fires whenever another player sends state -- use it to
  keep all clients in sync.
- Do NOT mix `singlePlayer.actions.gameOver` and `multiplayer.actions.gameOver`
  in the same game. Use one or the other.
