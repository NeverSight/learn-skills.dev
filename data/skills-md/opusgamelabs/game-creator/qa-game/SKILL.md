---
name: qa-game
description: Add Playwright QA tests to a game — visual regression, gameplay verification, performance, and accessibility
argument-hint: "[path-to-game]"
disable-model-invocation: true
---

# QA Game

Add automated QA testing with Playwright to an existing game project. Tests verify your game boots, scenes work, scoring functions, and visuals haven't broken — like a safety net for your game.

## Instructions

Analyze the game at `$ARGUMENTS` (or the current directory if no path given).

First, load the game-qa skill to get the full testing patterns and fixtures.

### Step 1: Audit testability

- Read `package.json` to identify the engine and dev server port
- Read `vite.config.js` for the server port
- Read `src/main.js` to check if `window.__GAME__`, `window.__GAME_STATE__`, `window.__EVENT_BUS__` are exposed
- Read `src/core/GameState.js` to understand what state is available
- Read `src/core/EventBus.js` to understand what events exist
- Read all scene files to understand the game flow

### Step 2: Setup Playwright

1. Install dependencies: `npm install -D @playwright/test @axe-core/playwright && npx playwright install chromium`
2. Create `playwright.config.js` with the correct dev server port and webServer config
3. Expose `window.__GAME__`, `window.__GAME_STATE__`, `window.__EVENT_BUS__`, `window.__EVENTS__` in `src/main.js` if not already present
4. Create the test directory structure:
   ```
   tests/
   ├── e2e/
   │   ├── game.spec.js
   │   ├── visual.spec.js
   │   └── perf.spec.js
   ├── fixtures/
   │   └── game-test.js
   └── helpers/
       └── seed-random.js
   ```
5. Add npm scripts: `test`, `test:ui`, `test:headed`, `test:update-snapshots`

### Step 3: Generate tests

Write tests based on what the game actually does:

- **game.spec.js**: Boot test, scene transitions, input handling, scoring, game over, restart
- **visual.spec.js**: Screenshot regression for stable scenes (gameplay initial state, game over). Skip active gameplay screenshots — moving objects make them unstable.
- **perf.spec.js**: Load time budget, FPS during gameplay, canvas dimensions

Follow the game-qa skill patterns. Use `gamePage` fixture. Use `page.evaluate()` to read game state. Use `page.keyboard.press()` for input.

### Step 4: Run and verify

1. Run `npx playwright test` to execute all tests
2. If visual tests fail on first run, that's expected — generate baselines with `npx playwright test --update-snapshots`
3. Run again to verify all tests pass
4. Summarize results

### Step 5: Report

Tell the user in plain English:

- How many tests were created and what they check
- How to run them: `npm test` (headless), `npm run test:headed` (see the browser), `npm run test:ui` (interactive dashboard)
- "These tests are your safety net. Run them after making changes to make sure nothing broke."

## Next Step

Tell the user:

> Your game now has automated tests! Finally, run `/game-creator:review-game` for a full architecture review — it checks your code structure, performance patterns, and gives you a score with specific improvement suggestions.
>
> **Pipeline progress:** ~~/make-game~~ → ~~/design-game~~ → ~~/add-audio~~ → ~~/qa-game~~ → `/review-game`
