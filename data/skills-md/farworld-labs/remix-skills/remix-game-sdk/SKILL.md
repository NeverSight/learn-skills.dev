---
name: remix-game-sdk
description: Reference for the @remix-gg/sdk game integration hooks and APIs
---

# Remix Game SDK Reference (`@remix-gg/sdk`)

Use this file when generating or repairing game code for Remix.

## Runtime model

- In Remix-hosted uploads, the SDK is available as `window.RemixSDK`.
- Include SDK script in the HTML `<head>`:
  - `<script src="https://cdn.jsdelivr.net/npm/@remix-gg/sdk@latest/dist/index.min.js"></script>`
- Do not rely on package imports in uploaded single-file game code.
- Always call `await window.RemixSDK.ready()` before reading player/game data.

## Required hooks for v1 agent validation

These checks are required by `GET /v1/games/{gameId}/versions/{versionId}/validate`:

- `window.RemixSDK.singlePlayer.actions.gameOver({ score })`
- `window.RemixSDK.onPlayAgain(() => { ... })`
- `window.RemixSDK.onToggleMute(({ isMuted }) => { ... })`

## Commonly used SDK surface

Properties/getters:

- `window.RemixSDK.player`
- `window.RemixSDK.players`
- `window.RemixSDK.gameState`
- `window.RemixSDK.gameInfo`
- `window.RemixSDK.purchasedItems`
- `window.RemixSDK.isReady`
- `window.RemixSDK.hasItem(itemId)`
- `window.RemixSDK.getItemPurchaseCount(itemId)`

Single-player actions:

- `window.RemixSDK.singlePlayer.actions.gameOver({ score })`
- `window.RemixSDK.singlePlayer.actions.saveGameState({ gameState })`
- `window.RemixSDK.singlePlayer.actions.purchase({ item })`
- `window.RemixSDK.singlePlayer.actions.reportError({ message, ... })`
- `window.RemixSDK.hapticFeedback()`

Multiplayer actions:

- `window.RemixSDK.multiplayer.actions.gameOver({ scores })`
- `window.RemixSDK.onGameStateUpdated(callback)`

Multiplayer actions/events are optional for basic single-player games.

## Minimal integration template

```javascript
async function initGame() {
  const sdk = window.RemixSDK
  await sdk.ready()

  let muted = true
  sdk.onToggleMute(({ isMuted }) => {
    muted = isMuted
  })

  sdk.onPlayAgain(() => {
    restart()
  })

  function finish(score) {
    sdk.singlePlayer.actions.gameOver({ score })
  }

  function save(state) {
    sdk.singlePlayer.actions.saveGameState({ gameState: state })
  }

  function restart() {
    // reset local game state and render
  }

  // start gameplay loop...
}

initGame()
```

## Mistakes to avoid

- Calling SDK getters before `ready()` resolves.
- Omitting one of the required validation hooks (`gameOver`, `onPlayAgain`, `onToggleMute`).
- Using non-existent SDK methods such as `vibrate`, `checkpoint`, or `save`.
- Using `localStorage`/`sessionStorage` as primary persistence instead of `saveGameState`.
