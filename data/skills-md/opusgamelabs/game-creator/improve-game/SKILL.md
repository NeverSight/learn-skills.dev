---
name: improve-game
description: Analyze a game, find what needs work, and implement the highest-impact improvements
argument-hint: "[area-to-focus]"
disable-model-invocation: true
---

# Improve Game

Make your game better. This command deep-audits gameplay, visuals, code quality, performance, and player experience, then implements the highest-impact improvements. Run it as many times as you want — each pass finds the next most impactful thing to fix.

## Instructions

Improve the game in the current directory. If `$ARGUMENTS` specifies a focus area (e.g., "gameplay", "visuals", "performance", "polish", "game-over"), weight that area higher but still audit everything.

### Step 1: Deep audit

Read the entire game codebase to build a complete picture:

- `package.json` — engine, dependencies, scripts
- `src/core/Constants.js` — all configuration values
- `src/core/EventBus.js` — all events and their usage
- `src/core/GameState.js` — state shape and reset logic
- `src/core/Game.js` (or `GameConfig.js`) — orchestrator and game loop
- Every file in `src/scenes/` or `src/systems/` — gameplay logic
- Every file in `src/entities/` — game objects
- Every file in `src/ui/` — game over, overlays
- Every file in `src/audio/` — music and sound effects
- `index.html` — markup, overlays, styles, viewport meta
- `src/systems/InputSystem.js` — input handling, mobile support (gyro, joystick, touch)
- `tests/` — test coverage and quality

Don't skim. Read every file completely so you understand the full picture before making recommendations.

### Step 2: Score and diagnose

Rate each area on a 1–5 scale (1 = broken/missing, 3 = functional but basic, 5 = polished and complete). Present a diagnostic table:

| Area | Score | Diagnosis |
|------|-------|-----------|
| **Gameplay feel** | | Is the core loop fun? Are controls responsive? Does difficulty ramp? |
| **Visual polish** | | Backgrounds, colors, particles, animations, screen effects |
| **Game Over & UI** | | Game over screen, transitions, restart flow, buttons |
| **Audio** | | BGM for each state, SFX for each action, volume balance, mute toggle |
| **Code architecture** | | EventBus, GameState, Constants, no circular deps |
| **Restart safety** | | Does GameState.reset() fully clean up? 3 restarts identical? No stale listeners/timers? |
| **Performance** | | Delta capping, object pooling, disposal, no leaks |
| **Player experience** | | Onboarding, feedback, difficulty curve, replayability |
| **Mobile support** | | Touch input, responsive layout, gyro/joystick, 44px touch targets |
| **Play.fun safe zone** | | All UI elements below `SAFE_ZONE.TOP` (~8% / 75px)? Nothing hidden behind Play.fun widget? |
| **Gameplay invariants** | | Can the player score? Can the player die? Do game-over buttons show text? Does `render_game_to_text()` return valid JSON? |
| **Entity sizing** | | Are characters large enough to read? Character-driven games need 12–15% of GAME.WIDTH. Proportional sizing (`GAME.WIDTH * ratio`), not fixed pixels? |
| **Test coverage** | | Boot, gameplay, scoring, restart, visual, perf tests |

**Overall score: X / 65**

### Step 3: Improvement plan

From the audit, identify the **top 5–8 improvements** ranked by player impact. For each one:

1. **Title** — short name (e.g., "Add difficulty progression")
2. **Area** — which category it improves
3. **Impact** — why this matters to the player
4. **What to do** — plain-English description of the change
5. **Files touched** — which files will be created or modified

Format as a numbered list. Put the highest-impact items first.

Present the plan to the user and ask which improvements to implement. Options:
- "All" — implement everything
- Specific numbers — implement selected items
- "Top 3" — just the most impactful

**Wait for the user to choose before implementing.**

### Step 4: Implement

For each selected improvement, follow these rules:

1. **Constants first** — add all new config values to `Constants.js`. Zero hardcoded values.
2. **Events next** — add any new events to `EventBus.js` using `domain:action` naming.
3. **State if needed** — add new state fields to `GameState.js` with proper reset.
4. **New files in proper directories** — entities in `entities/`, systems in `systems/`, UI in `ui/`.
5. **Wire through orchestrator** — register new systems in `Game.js` with proper lifecycle.
6. **EventBus for communication** — modules never import each other directly.
7. **Match existing code style** — same patterns, naming, formatting as the rest of the project.
8. **Don't break what works** — existing gameplay, controls, and scoring must still function identically unless the improvement specifically targets them.

After implementing each improvement, run `npm run build` to catch errors immediately. Fix any build errors before moving to the next improvement.

### Step 5: Verify

After all improvements are implemented:

1. Run `npm run build` — confirm clean build with no errors
2. Run `npm test` if tests exist — confirm all tests still pass
3. If tests fail because of intentional changes (new scenes, changed elements), fix the tests to match the new behavior
4. If the game has visual regression tests, update snapshots: `npm run test:update-snapshots`

### Step 6: Report

Tell the user what changed:

> **Improvement report**
>
> **Score: X/65 → Y/65** (+Z points)
>
> **Implemented:**
> 1. [Title] — [one-sentence summary of what changed]
> 2. [Title] — [one-sentence summary of what changed]
> ...
>
> **Files created:** [list new files]
> **Files modified:** [list changed files]
>
> **How to test:** Run `npm run dev` and try:
> - [specific thing to look for]
> - [specific thing to look for]
>
> **Next improvements:** Run `/game-creator:improve-game` again to find the next batch.

## Focus areas

When `$ARGUMENTS` includes a focus area keyword, weight these specific checks:

**"gameplay"** — core loop, controls, difficulty progression, enemy variety, power-ups, risk/reward, pacing, level design

**"visuals"** — load the game-designer skill and apply its full design audit (backgrounds, palette, animations, particles, transitions, typography, juice)

**"performance"** — delta capping, object pooling, geometry/material disposal, event listener cleanup, requestAnimationFrame usage, draw call count, texture atlas usage

**"polish"** — screen shake, hit pause, squash/stretch, easing curves, sound timing, button feedback, score popups, death animations, transition smoothness

**"game-over"** — game over screen appeal, restart flow, button styling, score display, best score display, animations. **Button text must be visible** — verify the `createButton()` pattern uses Container + Graphics + Text (Graphics first, Text second, Container interactive). If button labels are invisible, the pattern is broken. Note: games do not have title/menu screens by default (Play.fun handles the chrome). Only add a title screen if the user explicitly requests one. Score HUD is handled by the Play.fun widget — do not add a separate in-game score display. All game-over UI must be below `SAFE_ZONE.TOP`.

**"audio"** — load the game-audio skill. Check BGM coverage (every game state should have music), SFX coverage (every player action should have feedback), volume mixing, transition smoothness between tracks

**"mobile"** — touch input implemented (tap zones, virtual joystick, or gyroscope), responsive canvas (`Phaser.Scale.FIT` or CSS `width:100%`), 44px minimum touch targets, virtual joystick or tap zones for movement, gyroscope support for tilt games, no hover-only interactions, tested on mobile viewport (Pixel 5 emulation). Read `InputSystem.js`, all scene/system `update()` methods, `index.html` viewport meta, and `Constants.js` for touch target sizes.

**"ux"** — onboarding (does the player know what to do?), feedback (does every action have a response?), difficulty curve (is it too hard/easy?), replayability (is there a reason to play again?)

## Tips

> This command is designed for iterative improvement. Run it multiple times:
> - First pass: fix the biggest gaps (missing features, broken UX)
> - Second pass: add polish (particles, transitions, juice)
> - Third pass: fine-tune (difficulty curve, timing, balance)
>
> Each run picks up where the last left off — previously fixed areas will score higher, surfacing new priorities.
>
> For targeted work, use the focus area: `/game-creator:improve-game gameplay` or `/game-creator:improve-game visuals`
