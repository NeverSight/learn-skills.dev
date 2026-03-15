---
name: game-completion
description: Wire up game completion signaling to the Puzzmo host
---

# Game Completion

Add proper game completion signaling so Puzzmo knows when the player has finished.

## Steps

1. Find the game's win condition / completion check.

2. When the game is won, call `sdk.gameCompleted()` with gameplay metrics:
   ```ts
   sdk.gameCompleted({
     pointsAwarded: calculateScore(),
     elapsedTimeSecs: sdk.timer.timeSecs(),
     additionalTimeAddedSecs: sdk.timer.addedTimeSecs(),
     hintsUsed: hintsUsed,
     resetsUsed: 0,
     metric1: 0,
     metric2: 0,
     metric3: 0,
     metric4: 0,
     metricStrings: [],
     cheatsUsed: 0,
   })
   ```

3. After any victory animation completes, call `sdk.showCompletionScreen()`:
   ```ts
   sdk.showCompletionScreen(
     [
       { type: "md", text: "**Congratulations!** You solved the puzzle!" },
     ],
     gameplayData,
     true // showRetry
   )
   ```

4. Make sure `gameCompleted` is called BEFORE `showCompletionScreen`. The host processes the completion data first, then displays the completion UI.

5. The timer automatically stops when `gameCompleted` is called - you don't need to stop it manually.

## Success Criteria

- `npm run build` completes without errors
- When the game is won, `gameCompleted` fires with score data
- After victory animation, `showCompletionScreen` fires
- The completion flow works: play -> win -> gameCompleted -> animation -> showCompletionScreen
