---
name: add-deeds
description: Generate interesting gameplay statistics (deeds) sent on game completion
---

# Add Deeds

Deeds are interesting statistics about a gameplay session. They're sent on completion and used for leaderboards, achievements, and social sharing.

## Steps

1. Identify 3-6 interesting metrics from the game. Good deeds are things like:
   - Number of moves made
   - Words found / items collected
   - Accuracy percentage
   - Streak length (consecutive correct answers)
   - Unique items discovered
   - Time per move/action

2. Track these metrics during gameplay. Add counters/trackers to the game state.

3. On completion, include deeds in the `gameCompleted` call via the config parameter:
   ```ts
   sdk.gameCompleted(gameplayMetrics, {
     deeds: [
       { id: "moves", value: totalMoves },
       { id: "accuracy", value: Math.round(correctMoves / totalMoves * 100) },
       { id: "streak", value: longestStreak },
       { id: "items-found", value: itemsFound },
     ],
   })
   ```

4. Deed IDs should be:
   - Lowercase kebab-case
   - Short and descriptive
   - Stable (don't change between versions)

5. The SDK automatically adds `points` and `time` deeds - you don't need to add those.

6. Also send deeds during checkpoints if the game has intermediate milestones:
   ```ts
   sdk.hitCheckpoint("level-complete", {
     interruptible: true,
     complete: false,
     process: [],
   }, {
     deeds: [{ id: "items-found", value: itemsFound }],
   })
   ```

## Success Criteria

- `npm run build` completes without errors
- At least 3 meaningful deeds are tracked during gameplay
- Deeds are sent with `gameCompleted`
- Deed IDs are kebab-case and descriptive
