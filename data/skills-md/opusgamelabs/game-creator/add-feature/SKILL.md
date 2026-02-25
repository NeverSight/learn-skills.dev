---
name: add-feature
description: Add a new gameplay feature to your game — just describe what you want
argument-hint: "[feature-description]"
disable-model-invocation: true
---

# Add Feature

Add a new feature to your game. Just describe what you want in plain English — for example, "add a double-jump power-up" or "add a high score leaderboard" — and the feature will be built following your game's existing patterns.

## Instructions

The user wants to add: $ARGUMENTS

### Step 1: Understand the codebase

- Read `package.json` to identify the engine (Three.js or Phaser)
- Read `src/core/Constants.js` for existing configuration
- Read `src/core/EventBus.js` for existing events
- Read `src/core/GameState.js` for existing state
- Read `src/core/Game.js` (or GameConfig.js) for existing system wiring
- Read existing scene and gameplay files to understand what's already built

### Step 2: Plan the feature

Before writing code, explain the plan in plain English:

1. **What it does**: Describe the feature from the player's perspective
2. **How it works**: List the new files, events, and settings that will be created
3. **What it touches**: List existing files that need small changes to wire in the feature

Then determine what's needed technically:
- New module file(s) and where they go in the directory structure
- New events to add to the Events enum
- New constants to add to Constants.js
- New state to add to GameState.js
- How to wire it into the Game orchestrator

### Step 3: Implement

Follow these rules strictly:
1. Create the new module in the correct `src/` subdirectory
2. Add ALL new events to `EventBus.js` Events enum
3. Add ALL configuration values to `Constants.js` (zero hardcoded values)
4. Add any new state domains to `GameState.js`
5. Wire the new system into `Game.js` (import, instantiate, update in loop)
6. Use EventBus for ALL communication with other systems
7. Follow the existing code style and patterns in the project

### Step 4: Verify

- Run `npm run build` to confirm no errors
- Confirm the feature integrates without breaking existing systems
- Check that no circular dependencies were introduced
- Ensure event listeners are properly cleaned up if applicable
- Summarize what was added in plain English

## Output

Tell the user:
1. What the feature does (from the player's perspective)
2. What files were created or changed
3. How to test it — "Run `npm run dev` and try [specific action]"

## Tips

> You can run this command as many times as you want to keep adding features. Each one builds on the last.
>
> When you're happy with the gameplay, run `/game-creator:design-game` to polish the visuals, `/game-creator:add-audio` for music and sound effects, or `/game-creator:review-game` for a full quality check.
