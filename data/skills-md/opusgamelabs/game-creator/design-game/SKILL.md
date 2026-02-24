---
name: design-game
description: Audit and improve the visual design, polish, and player experience of an existing game
argument-hint: "[path-to-game]"
disable-model-invocation: true
---

# Design Game

Run a UI/UX design pass on an existing game to improve visuals, atmosphere, and game feel. No design experience needed — this command analyzes your game and applies proven visual patterns.

## Instructions

Analyze the game at `$ARGUMENTS` (or the current directory if no path given).

First, load the game-designer skill to get the full design vocabulary and patterns.

### Step 1: Audit

- Read `package.json` to identify the engine
- Read `src/core/Constants.js` for the current color palette and config
- Read all scene files to understand current visuals
- Read entity files to see how game objects are drawn
- Read `src/core/EventBus.js` for existing events

### Step 2: Design Report

Score each area 1-5 and present as a table:

| Area | Score | Notes |
|------|-------|-------|
| Background & Atmosphere | | |
| Color Palette | | |
| Animations & Tweens | | |
| Particle Effects | | |
| Screen Transitions | | |
| Typography | | |
| Game Feel / Juice | | |
| Game Over | | |

Then list the top improvements ranked by visual impact, with a plain-English description of what each one does (e.g., "Add a sky gradient so the background looks like a real sky instead of a flat color").

### Step 3: Implement

Ask the user which improvements they want, or implement all if they say so. Follow the game-designer skill patterns:

1. All new values in `Constants.js`
2. Use EventBus for triggering effects
3. Don't alter gameplay (physics, scoring, controls, spawn timing)
4. Prefer procedural graphics
5. New files in proper directories

### Step 4: Verify

- Run `npm run build` to confirm no errors
- Summarize all changes made in plain English

## Next Step

Tell the user:

> Your game looks much better now! Next, run `/game-creator:add-audio` to add chiptune background music and retro sound effects — all procedurally generated, no audio files needed.
>
> **Pipeline progress:** ~~/make-game~~ → ~~/design-game~~ → `/add-audio` → `/qa-game` → `/review-game`
