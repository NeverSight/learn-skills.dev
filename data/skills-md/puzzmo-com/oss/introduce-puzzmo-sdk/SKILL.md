---
name: introduce-puzzmo-sdk
description: Integrate the Puzzmo SDK into a Vite game project for host communication
---

# Introduce Puzzmo SDK

Add the `@puzzmo/sdk` package and wire up the game lifecycle.

## Steps

1. Install `@puzzmo/sdk`:
   ```
   npm install @puzzmo/sdk
   ```

2. In the main game entry file, import and initialize the SDK:
   ```ts
   import { createPuzzmoSDK } from "@puzzmo/sdk"

   const sdk = createPuzzmoSDK()
   ```

3. Replace the game's initialization flow with the SDK lifecycle:
   ```ts
   // Wait for puzzle data from the host
   const { puzzleString, boardState, theme, completed } = await sdk.gameReady()

   // Parse puzzle data and set up the game
   const puzzle = JSON.parse(puzzleString)
   initializeGame(puzzle)

   // If there's saved state, restore it
   if (boardState) restoreState(boardState)

   // Apply the Puzzmo theme colors
   if (theme) applyTheme(theme)

   // Signal that the game is ready to start
   sdk.gameLoaded()
   ```

4. Wire up lifecycle events:
   ```ts
   sdk.on("start", () => { /* start game logic, timer auto-starts */ })
   sdk.on("pause", () => { /* pause game, timer auto-pauses */ })
   sdk.on("resume", () => { /* resume game, timer auto-resumes */ })
   sdk.on("retry", () => { /* reset game state, timer auto-resets */ })
   ```

5. Wire up state saving - call `sdk.updateGameState(stateString)` whenever the game state changes so the host can save progress.

6. Create a `sample-puzzle.json` file with test puzzle data that matches what the game expects.

7. Set up the dev simulator for local testing. Add the Vite plugin to `vite.config.ts`:
   ```ts
   import { defineConfig } from "vite"
   import { puzzmoSimulator } from "@puzzmo/sdk/vite"

   export default defineConfig({
     plugins: [
       puzzmoSimulator({
         slug: "my-game",
         puzzlePath: "./sample-puzzle.json",
       }),
     ],
   })
   ```

   The plugin automatically:
   - Injects the simulator UI in dev mode only (tree-shaken from production builds)
   - Handles OAuth callback routing for authenticated API features

   For non-Vite setups, use the standalone script tag instead:
   ```html
   <script>
     window.SIMULATOR_CONFIG = { puzzlePath: "./sample-puzzle.json", slug: "my-game" }
   </script>
   <script type="module" src="@puzzmo/sdk/simulator/standalone"></script>
   ```

## Key SDK APIs

- `sdk.gameReady()` - Async. Sends READY, waits for puzzle data. Returns `{ puzzleString, boardState, theme, completed }`.
- `sdk.gameLoaded()` - Signals game is ready. Host will send START_GAME.
- `sdk.on(event, handler)` - Listen for lifecycle events: `start`, `pause`, `resume`, `retry`, `settingsUpdate`.
- `sdk.updateGameState(stateString)` - Save current game state.
- `sdk.timer` - Auto-managed timer with `.timeMs()`, `.timeSecs()`, `.display()`, `.addPenalty(ms)`.

## Success Criteria

- `npm run build` completes without errors
- Game initializes through SDK lifecycle (gameReady -> gameLoaded -> on start)
- Game state is saved via `updateGameState` on each user action
- Pause/resume/retry events are handled
- A sample-puzzle.json exists for local testing
- Simulator appears in dev mode but is not included in production builds
