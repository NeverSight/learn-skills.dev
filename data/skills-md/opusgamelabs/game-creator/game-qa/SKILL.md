---
name: game-qa
description: Game QA testing with Playwright — visual regression, gameplay verification, performance, and accessibility for browser games
user-invocable: false
---

# Game QA with Playwright

You are an expert QA engineer for browser games. You use Playwright to write automated tests that verify visual correctness, gameplay behavior, performance, and accessibility.

## Reference Files

For detailed reference, see companion files in this directory:
- `visual-regression.md` — Screenshot comparison tests, masking dynamic elements, performance/FPS tests, accessibility tests, deterministic testing patterns
- `clock-control.md` — Playwright Clock API patterns for frame-precise testing
- `playwright-mcp.md` — MCP server setup, when to use MCP vs scripted tests, inspection flow
- `iterate-client.md` — Standalone iterate client usage, action JSON format, output interpretation
- `mobile-tests.md` — Mobile input simulation and responsive layout test patterns

## Tech Stack

- **Test Runner**: Playwright Test (`@playwright/test`)
- **Visual Regression**: Playwright built-in `toHaveScreenshot()`
- **Accessibility**: `@axe-core/playwright`
- **Build Tool Integration**: Vite dev server via `webServer` config
- **Language**: JavaScript ES modules

## Project Setup

When adding Playwright to a game project:

```bash
npm install -D @playwright/test @axe-core/playwright
npx playwright install chromium
```

Add to `package.json` scripts:

```json
{
  "scripts": {
    "test": "npx playwright test",
    "test:ui": "npx playwright test --ui",
    "test:headed": "npx playwright test --headed",
    "test:update-snapshots": "npx playwright test --update-snapshots"
  }
}
```

## Required Directory Structure

```
tests/
├── e2e/
│   ├── game.spec.js       # Core game tests (boot, scenes, input, score)
│   ├── visual.spec.js     # Visual regression screenshots
│   └── perf.spec.js       # Performance and FPS tests
├── fixtures/
│   ├── game-test.js       # Custom test fixture with game helpers
│   └── screenshot.css     # CSS to mask dynamic elements for visual tests
├── helpers/
│   └── seed-random.js     # Seeded PRNG for deterministic game behavior
playwright.config.js
```

## Playwright Config

```js
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html', { open: 'never' }], ['list']],

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 200,
      threshold: 0.3,
    },
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },
});
```

Key points:
- `webServer` auto-starts Vite before tests
- `reuseExistingServer` reuses a running dev server locally
- `baseURL` matches the Vite port configured in `vite.config.js`
- Screenshot tolerance is generous (games have minor render variance)

## Testability Requirements

For Playwright to inspect game state, the game MUST expose these globals on `window` in `main.js`:

### 1. Core globals (required)

```js
// Expose for Playwright QA
window.__GAME__ = game;
window.__GAME_STATE__ = gameState;
window.__EVENT_BUS__ = eventBus;
window.__EVENTS__ = Events;
```

### 2. `render_game_to_text()` (required)

Returns a concise JSON string of the current game state for AI agents to reason about the game without interpreting pixels. Must include coordinate system, game mode, score, and player state.

```js
window.render_game_to_text = () => {
  if (!game || !gameState) return JSON.stringify({ error: 'not_ready' });

  const activeScenes = game.scene.getScenes(true).map(s => s.scene.key);
  const payload = {
    coords: 'origin:top-left x:right y:down',          // coordinate system
    mode: gameState.gameOver ? 'game_over' : 'playing',
    scene: activeScenes[0] || null,
    score: gameState.score,
    bestScore: gameState.bestScore,
  };

  // Add player info when in gameplay
  const gameScene = game.scene.getScene('GameScene');
  if (gameState.started && gameScene?.player?.sprite) {
    const s = gameScene.player.sprite;
    const body = s.body;
    payload.player = {
      x: Math.round(s.x), y: Math.round(s.y),
      vx: Math.round(body.velocity.x), vy: Math.round(body.velocity.y),
      onGround: body.blocked.down,
    };
  }

  // Extend with visible entities as you add them:
  // payload.entities = obstacles.map(o => ({ x: o.x, y: o.y, type: o.type }));

  return JSON.stringify(payload);
};
```

Guidelines for `render_game_to_text()`:
- Keep the payload **succinct** — only current, visible, interactive elements
- Include **coordinate system note** (origin and axis directions)
- Include **player position/velocity**, active obstacles/enemies, collectibles, timers, score, and mode flags
- Avoid large histories; only include what's currently relevant
- The iterate client and AI agents use this to verify game behavior without screenshots

### 3. `advanceTime(ms)` (required)

Lets test scripts advance the game by a precise duration. The game loop runs normally via RAF; this waits for real time to elapse.

```js
window.advanceTime = (ms) => {
  return new Promise((resolve) => {
    const start = performance.now();
    function step() {
      if (performance.now() - start >= ms) return resolve();
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  });
};
```

For frame-precise control in `@playwright/test`, prefer `page.clock.install()` + `page.clock.runFor()`. The `advanceTime` hook is primarily used by the standalone iterate client (`scripts/iterate-client.js`).

For Three.js games, expose the `Game` orchestrator instance similarly.

## Custom Test Fixture

Create a reusable fixture with game-specific helpers:

```js
import { test as base, expect } from '@playwright/test';

export const test = base.extend({
  gamePage: async ({ page }, use) => {
    await page.goto('/');
    // Wait for Phaser to boot and canvas to render
    await page.waitForFunction(() => {
      const g = window.__GAME__;
      return g && g.isBooted && g.canvas;
    }, null, { timeout: 10000 });
    await use(page);
  },
});

export { expect };
```

## Core Testing Patterns

### 1. Game Boot & Scene Flow

Test that the game initializes and scenes transition correctly.

```js
import { test, expect } from '../fixtures/game-test.js';

test('game boots directly to gameplay', async ({ gamePage }) => {
  const sceneKey = await gamePage.evaluate(() => {
    return window.__GAME__.scene.getScenes(true)[0]?.scene?.key;
  });
  expect(sceneKey).toBe('GameScene');
});
```

### 2. Gameplay Verification

Test that game mechanics work — input affects state, scoring works, game over triggers.

```js
test('bird flaps on space press', async ({ gamePage }) => {
  // Start game
  await gamePage.keyboard.press('Space');
  await gamePage.waitForFunction(() => window.__GAME_STATE__.started);

  // Record position before flap
  const yBefore = await gamePage.evaluate(() => {
    const scene = window.__GAME__.scene.getScene('GameScene');
    return scene.bird.y;
  });

  // Flap
  await gamePage.keyboard.press('Space');
  await gamePage.waitForTimeout(100);

  // Bird should have moved up (lower y)
  const yAfter = await gamePage.evaluate(() => {
    const scene = window.__GAME__.scene.getScene('GameScene');
    return scene.bird.y;
  });
  expect(yAfter).toBeLessThan(yBefore);
});

test('game over triggers on collision', async ({ gamePage }) => {
  await gamePage.keyboard.press('Space');
  await gamePage.waitForFunction(() => window.__GAME_STATE__.started);

  // Don't flap — let bird fall to ground
  await gamePage.waitForFunction(
    () => window.__GAME_STATE__.gameOver,
    null,
    { timeout: 10000 }
  );

  expect(await gamePage.evaluate(() => window.__GAME_STATE__.gameOver)).toBe(true);
});
```

### 3. Scoring

```js
test('score increments when passing pipes', async ({ gamePage }) => {
  await gamePage.keyboard.press('Space');
  await gamePage.waitForFunction(() => window.__GAME_STATE__.started);

  // Keep flapping to survive
  const flapInterval = setInterval(async () => {
    await gamePage.keyboard.press('Space').catch(() => {});
  }, 300);

  // Wait for at least 1 score
  await gamePage.waitForFunction(
    () => window.__GAME_STATE__.score > 0,
    null,
    { timeout: 15000 }
  );

  clearInterval(flapInterval);

  const score = await gamePage.evaluate(() => window.__GAME_STATE__.score);
  expect(score).toBeGreaterThan(0);
});
```

## Core Gameplay Invariants

Every game built through the pipeline **must** pass these minimum gameplay checks. These verify the game is actually playable, not just renders without errors.

### 1. Scoring works

The player must be able to earn at least 1 point through normal gameplay actions:

```js
test('player can score at least 1 point', async ({ gamePage }) => {
  // Start the game (space/tap)
  await gamePage.keyboard.press('Space');
  await gamePage.waitForFunction(() => window.__GAME_STATE__.started, null, { timeout: 5000 });

  // Perform gameplay actions — keep the player alive
  const actionInterval = setInterval(async () => {
    await gamePage.keyboard.press('Space').catch(() => {});
  }, 400);

  // Wait for score > 0
  await gamePage.waitForFunction(
    () => window.__GAME_STATE__.score > 0,
    null,
    { timeout: 20000 }
  );
  clearInterval(actionInterval);

  const score = await gamePage.evaluate(() => window.__GAME_STATE__.score);
  expect(score).toBeGreaterThan(0);
});
```

### 2. Death/fail condition triggers

The player must be able to die or lose through inaction or collision:

```js
test('game over triggers through normal gameplay', async ({ gamePage }) => {
  // Start the game
  await gamePage.keyboard.press('Space');
  await gamePage.waitForFunction(() => window.__GAME_STATE__.started, null, { timeout: 5000 });

  // Do nothing — let the fail condition trigger naturally (fall, timer, collision)
  await gamePage.waitForFunction(
    () => window.__GAME_STATE__.gameOver === true,
    null,
    { timeout: 15000 }
  );

  const isOver = await gamePage.evaluate(() => window.__GAME_STATE__.gameOver);
  expect(isOver).toBe(true);
});
```

### 3. Game-over buttons have visible text

After game over, restart/play-again buttons must show their text labels:

```js
test('game over buttons display text labels', async ({ gamePage }) => {
  // Trigger game over
  await gamePage.keyboard.press('Space');
  await gamePage.waitForFunction(() => window.__GAME_STATE__.started, null, { timeout: 5000 });
  await gamePage.waitForFunction(() => window.__GAME_STATE__.gameOver, null, { timeout: 15000 });

  // Wait for GameOverScene to render
  await gamePage.waitForFunction(() => {
    const scenes = window.__GAME__.scene.getScenes(true);
    return scenes.some(s => s.scene.key === 'GameOverScene');
  }, null, { timeout: 5000 });
  await gamePage.waitForTimeout(500);

  // Check that text objects exist and are visible in the scene
  const hasVisibleText = await gamePage.evaluate(() => {
    const scene = window.__GAME__.scene.getScene('GameOverScene');
    if (!scene) return false;
    const textObjects = scene.children.list.filter(
      child => child.type === 'Text' && child.visible && child.alpha > 0
    );
    // Should have at least: title ("GAME OVER"), score, and button label ("PLAY AGAIN")
    return textObjects.length >= 3;
  });
  expect(hasVisibleText).toBe(true);
});
```

### 4. `render_game_to_text()` returns valid state

The AI-readable state function must return parseable JSON with required fields:

```js
test('render_game_to_text returns valid game state', async ({ gamePage }) => {
  const stateStr = await gamePage.evaluate(() => window.render_game_to_text());
  const state = JSON.parse(stateStr);

  expect(state).toHaveProperty('mode');
  expect(state).toHaveProperty('score');
  expect(['playing', 'game_over']).toContain(state.mode);
  expect(typeof state.score).toBe('number');
});
```

## When Adding QA to a Game

1. Install Playwright: `npm install -D @playwright/test @axe-core/playwright && npx playwright install chromium`
2. Create `playwright.config.js` with the game's dev server port
3. Expose `window.__GAME__`, `window.__GAME_STATE__`, `window.__EVENT_BUS__` in `main.js`
4. Create `tests/fixtures/game-test.js` with the `gamePage` fixture
5. Create `tests/helpers/seed-random.js` for deterministic behavior
6. Write tests in `tests/e2e/`:
   - `game.spec.js` — boot, scene flow, input, scoring, game over
   - `visual.spec.js` — screenshot regression for each scene
   - `perf.spec.js` — load time, FPS budget
7. Add npm scripts: `test`, `test:ui`, `test:headed`, `test:update-snapshots`
8. Generate initial baselines: `npm run test:update-snapshots`

## What NOT to Test (Automated)

- **Exact pixel positions** of animated objects (non-deterministic without clock control)
- **Active gameplay screenshots** — moving objects make stable screenshots impossible; use MCP instead
- **Audio playback** (Playwright has no audio inspection; test that audio objects exist via evaluate)
- **External API calls** unless mocked (e.g., Play.fun SDK — mock with `page.route()`)
- **Subjective visual quality** — use MCP for "does this look good?" evaluations
