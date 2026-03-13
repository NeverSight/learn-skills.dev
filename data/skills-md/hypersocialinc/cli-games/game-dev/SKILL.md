---
name: game-dev
description: Create terminal games for cli-games. Use when asked to "create a game", "make a terminal game", "add a game", "vibe code a game", build arcade/puzzle/action games for the terminal, or contribute a new game.
---

# Game Dev Skill

This skill enables rapid creation of terminal-based games for `@hypersocial/cli-games`.

## Quick Start

1. Get game concept and name from user
2. Create game file at `src/games/{name}/index.ts`
3. Register in `src/games/index.ts`
4. Follow patterns below for consistent look and feel

## Architecture Overview

All games share these characteristics:
- **GameController interface**: `stop()` method and `isRunning` getter
- **State machine**: `gameStarted`, `gameOver`, `paused`, `won` flags
- **Shared pause menu**: Import from `../shared/menu`
- **Shared effects**: Import from `../shared/effects`
- **Theme awareness**: Use `getCurrentThemeColor()` from `../utils`
- **Terminal rendering**: ANSI escape codes, alternate buffer mode

## File Structure

```
src/games/
├── {gamename}/
│   ├── index.ts          # Main game file (required)
│   └── effects.ts        # Complex games: separate effects
├── shared/
│   ├── menu.ts           # Shared pause menu system
│   ├── effects.ts        # Shared particle, popup, shake, flash utilities
│   └── index.ts          # Re-exports
├── gameTransitions.ts    # Quit/switch game helpers
├── utils.ts              # Theme colors, utilities
└── index.ts              # Game registry
```

## Required Imports

```typescript
import type { Terminal } from '@xterm/xterm';
import { getCurrentThemeColor } from '../utils';
import { dispatchGameQuit, dispatchGameSwitch, dispatchGamesMenu } from '../gameTransitions';
import { PAUSE_MENU_ITEMS, renderSimpleMenu, navigateMenu } from '../shared/menu';
```

For effects, import from the shared module:

```typescript
import {
  type Particle,
  type ScorePopup,
  spawnParticles,
  updateParticles,
  addScorePopup,
  updatePopups,
  triggerShake,
  applyShake,
  createShakeState,
  MAX_PARTICLES,
  PARTICLE_CHARS,
} from '../shared/effects';
```

## GameController Interface

Every game exports a controller with this shape:

```typescript
export interface {Name}Controller {
  stop: () => void;
  isRunning: boolean;
}
```

## State Machine Pattern

```typescript
let running = true;
let gameStarted = false;
let gameOver = false;
let paused = false;
let pauseMenuSelection = 0;
let won = false;
```

**State transitions:**
- Start: `!gameStarted && !paused` -> any key -> `gameStarted = true`
- Pause: ESC toggles `paused`, reset `pauseMenuSelection = 0`
- Game Over: collision/loss -> `gameOver = true`, optionally `won = true`
- Quit: Q key or menu selection -> `controller.stop()` + `dispatchGameQuit()`

## Pause Menu Integration

**CRITICAL**: Always use the shared menu system:

```typescript
import { PAUSE_MENU_ITEMS, renderSimpleMenu, navigateMenu } from '../shared/menu';

// In render():
if (paused) {
  output += renderSimpleMenu(PAUSE_MENU_ITEMS, pauseMenuSelection, {
    centerX: Math.floor(cols / 2),
    startY: pauseY + 2,
    showShortcuts: false,
  });
}

// In key handler:
if (paused) {
  const { newSelection, confirmed } = navigateMenu(
    pauseMenuSelection,
    PAUSE_MENU_ITEMS.length,
    key,
    domEvent
  );

  if (newSelection !== pauseMenuSelection) {
    pauseMenuSelection = newSelection;
    return;
  }

  if (confirmed) {
    switch (pauseMenuSelection) {
      case 0: paused = false; break;  // Resume
      case 1: initGame(); gameStarted = true; paused = false; break;  // Restart
      case 2: controller.stop(); dispatchGameQuit(terminal); break;  // Quit
      case 3: dispatchGamesMenu(terminal); break;  // List Games
      case 4: dispatchGameSwitch(terminal); break;  // Next Game
    }
  }
}
```

## Terminal Size Handling

Always check minimum size and show helpful resize message:

```typescript
const MIN_COLS = 40;
const MIN_ROWS = 20;

// In render():
if (cols < MIN_COLS || rows < MIN_ROWS) {
  const msg1 = 'Terminal too small!';
  const needWidth = cols < MIN_COLS;
  const needHeight = rows < MIN_ROWS;
  let hint = needWidth && needHeight ? 'Make pane larger'
    : needWidth ? 'Make pane wider ->' : 'Make pane taller';
  const msg2 = `Need: ${MIN_COLS}x${MIN_ROWS}  Have: ${cols}x${rows}`;
  // Center and render messages...
  return;
}
```

## Glitch Title Effect

Every game has a glitchy ASCII title:

```typescript
const title = [
  '{TITLE_LINE_1}',
  '{TITLE_LINE_2}',
];

let glitchFrame = 0;

// In render():
glitchFrame = (glitchFrame + 1) % 60;
const glitchOffset = glitchFrame >= 55 ? Math.floor(Math.random() * 3) - 1 : 0;
const titleX = Math.floor((cols - title[0].length) / 2) + glitchOffset;

if (glitchFrame >= 55 && glitchFrame < 58) {
  output += `\x1b[1;${titleX}H\x1b[91m${title[0]}\x1b[0m`;
  output += `\x1b[2;${titleX + 1}H\x1b[96m${title[1]}\x1b[0m`;
} else {
  output += `\x1b[1;${titleX}H${themeColor}\x1b[1m${title[0]}\x1b[0m`;
  output += `\x1b[2;${titleX}H${themeColor}\x1b[1m${title[1]}\x1b[0m`;
}
```

## Game Loop Setup

```typescript
setTimeout(() => {
  if (!running) return;

  // Enter alternate buffer, hide cursor
  terminal.write('\x1b[?1049h');
  terminal.write('\x1b[?25l');

  initGame();
  gameStarted = false;

  const renderInterval = setInterval(() => {
    if (!running) { clearInterval(renderInterval); return; }
    render();
  }, 50);  // 20 FPS

  const gameInterval = setInterval(() => {
    if (!running) { clearInterval(gameInterval); return; }
    update();
  }, 50);

  const keyListener = terminal.onKey(({ domEvent }) => {
    if (!running) { keyListener.dispose(); return; }
    domEvent.preventDefault();
    domEvent.stopPropagation();
    // Handle input...
  });

  // Override stop to clean up
  const originalStop = controller.stop;
  controller.stop = () => {
    clearInterval(renderInterval);
    clearInterval(gameInterval);
    keyListener.dispose();
    originalStop();
  };
}, 50);
```

## Registering a Game

In `src/games/index.ts`, add a direct import and entry:

```typescript
// 1. Add the import at the top with existing imports:
import { run{Name}Game } from './{name}';

// 2. Add to the games array:
export const games: GameInfo[] = [
  // ... existing games
  { id: '{name}', name: '{Name}', description: 'Game description', run: run{Name}Game },
];

// 3. Add to the individual game runner exports:
export {
  // ... existing exports
  run{Name}Game,
};
```

## Effect Patterns

See `patterns/effects.md` for:
- Particle systems (burst, trail, firework)
- Screen shake
- Score popups
- Flash effects
- Kill streaks and combos

Use the shared effects module at `src/games/shared/effects.ts` for common effect logic.

## Input Patterns

See `patterns/input-handling.md` for:
- Arrow key navigation
- Action keys (space, etc.)
- ESC/Q handling
- Start screen any-key

## Rendering Patterns

See `patterns/rendering.md` for:
- ANSI escape codes reference
- Border drawing
- Centering content
- Color cycling
- Perspective effects

## Game Complexity Guide

**Simple (~300-500 lines):** Snake, Hangman
- Single file
- Basic collision
- Minimal physics

**Medium (~500-800 lines):** Tetris, Pong
- Single file with more systems
- AI or grid mechanics
- More effect polish

**Complex (~1000+ lines):** Chopper
- Multiple files (index.ts, effects.ts)
- Physics, particles, popups
- Level progression

## Contributing a Game

1. Create your game in `src/games/{name}/index.ts`
2. Register it in `src/games/index.ts`
3. Use shared effects from `../shared/effects` instead of inlining particle/popup code
4. Use the shared menu from `../shared/menu` for pause/game-over menus
5. Run `npm run build` and `npm run typecheck` to verify
6. Submit a PR

## Template

Use the scaffold template at `templates/game-scaffold.ts` as a starting point.
