---
name: setup-augmentations
description: Create augmentations.json with leaderboard configuration using deeds
---

# Setup Augmentations

Create an `augmentations.json` file that configures leaderboards and other meta-game features using the deeds defined in the previous step.

## Steps

1. Create `augmentations.json` in the project root:
   ```json
   {
     "_v": 1,
     "augmentations": {
       "leaderboards": [
         {
           "displayName": "Fastest Time",
           "stableID": "game-GAMESLUG:time",
           "order": "Lower=better",
           "deedID": "time",
           "formatString": "[time]"
         },
         {
           "displayName": "High Score",
           "stableID": "game-GAMESLUG:points",
           "order": "Higher=better",
           "deedID": "points",
           "formatString": "%@"
         }
       ]
     }
   }
   ```

2. Replace `GAMESLUG` with the actual game slug (the directory name, lowercased).

3. Add leaderboards for each meaningful deed. The `stableID` format MUST be `game-[gameslug]:[deed-id]`.

4. Choose appropriate `formatString` values:
   - `"[time]"` - Converts seconds to `MM:SS` format
   - `"%@"` - Shows the number with locale formatting
   - `"%@ moves"` - Appends a unit
   - `"%@%"` - Shows as percentage

5. Set `order` appropriately:
   - `"Lower=better"` for time, moves, errors
   - `"Higher=better"` for score, accuracy, streaks

## Success Criteria

- `augmentations.json` exists and is valid JSON
- At least 2 leaderboards are configured
- All `stableID` values follow the `game-slug:deed-id` format
- `formatString` values are appropriate for each metric
