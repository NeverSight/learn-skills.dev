---
name: promo-video
description: >
  Record a high-FPS autonomous promo video of a Phaser game using Playwright.
  Triggers on: promo video, gameplay recording, marketing video, game capture.
---

# Promo Video Recording

Record smooth, autonomous promo footage of a Phaser game for marketing / social media. The output is a 50 FPS MP4 in mobile portrait (9:16) — ready for TikTok, Reels, Moltbook, or X.

## Technique

Playwright's `recordVideo` caps at 25 FPS with no config option. We work around it:

1. **Slow the game to 0.5×** by patching all 5 Phaser time subsystems
2. **Record for 2× the desired duration** at Playwright's native 25 FPS
3. **FFmpeg speed-up 2×** → effective 50 FPS output

| Parameter | Default | Effect |
|-----------|---------|--------|
| `SLOW_MO_FACTOR` | `0.5` | Game runs at half speed → 50 FPS output |
| `WALL_CLOCK_DURATION` | `DESIRED_GAME_DURATION / SLOW_MO_FACTOR` | Record for 2× to get correct game-time |
| `VIEWPORT` | `{ width: 1080, height: 1920 }` | 9:16 mobile portrait (always default unless user specifies otherwise) |
| `DESIRED_GAME_DURATION` | `13000` (ms) | ~13s of game-time → ~6.5s promo clip |

## Prerequisites

- **Playwright** — must be installed (`npm install -D @playwright/test && npx playwright install chromium`)
- **FFmpeg** — must be available on PATH (`brew install ffmpeg` on macOS)
- **Dev server running** — game must be served on localhost

Check both before starting:
```bash
npx playwright --version
ffmpeg -version | head -1
```

If FFmpeg is not found, warn the user and skip the promo video step (it's non-blocking — the game still works without it).

## Capture Script — Game-Specific Adaptation

Every game gets a custom `scripts/capture-promo.mjs`. The subagent **must read the game's source files** to determine:

### 1. Death/Failure Patching (CRITICAL)

The video must show continuous gameplay — never game over. Read `GameScene.js` (or equivalent) to find the death/failure method and monkey-patch it out.

**How to find it**: Search for the method called on collision/death. Common patterns:
- `this.triggerGameOver()` — dodge games
- `this.takeDamage()` → `this.lives <= 0` — multi-life games
- `this.gameOver()` — direct call
- `eventBus.emit(Events.PLAYER_HIT)` / `eventBus.emit(Events.GAME_OVER)` — event-driven

**Patch template** (adapt per game):
```js
await page.evaluate(() => {
  const scene = window.__GAME__.scene.getScene('GameScene');
  if (scene) {
    // Patch ALL paths to game over
    scene.triggerGameOver = () => {};
    scene.onPlayerHit = () => {};
    // For multi-life games, also prevent damage:
    // scene.takeDamage = () => {};
    // scene.playerDied = () => {};
  }
});
```

### 2. Input Sequence Generation

The video must show dynamic, natural-looking gameplay. Read the game's input handling to determine:

- **Which keys** — ArrowLeft/ArrowRight? Space? WASD? Mouse clicks?
- **Input style** — continuous hold (movement), tap (jump/shoot), or both?
- **Movement pattern** — should the player sweep across the screen, dodge reactively, jump rhythmically?

**Input patterns by game type:**

| Game Type | Input Keys | Pattern |
|-----------|-----------|---------|
| Side dodger | ArrowLeft, ArrowRight | Alternating holds (150-600ms) with variable pauses, occasional double-taps |
| Platformer / Flappy | Space | Rhythmic taps (80-150ms hold) with variable gaps (200-800ms) |
| Top-down | WASD / Arrows | Mixed directional holds, figure-eight patterns |
| Shooter | ArrowLeft/Right + Space | Movement interleaved with rapid fire |
| Clicker/Tapper | Mouse click / Space | Rapid bursts separated by brief pauses |

**Randomize timing** to avoid robotic-looking movement:
```js
const holdMs = 150 + Math.floor(Math.random() * 450);
const pauseMs = 50 + Math.floor(Math.random() * 250);
```

**Add a pause at the start** (1-2s) to let the entrance animation play — this is the hook.

### 3. Game Boot Detection

All games built with the make-game pipeline expose these globals:
- `window.__GAME__` — Phaser.Game instance
- `window.__GAME_STATE__` — GameState singleton
- `window.__EVENT_BUS__` — EventBus singleton

Wait for both boot and active gameplay:
```js
await page.waitForFunction(() => window.__GAME__?.isBooted, { timeout: 15000 });
await page.waitForFunction(() => window.__GAME_STATE__?.started, { timeout: 10000 });
```

### 4. Time Scaling Injection

Slow all 5 Phaser time subsystems for the recording:

```js
await page.evaluate(({ factor }) => {
  const game = window.__GAME__;
  const scene = game.scene.getScene('GameScene');

  // 1. Update delta — slows frame-delta-dependent logic
  const originalUpdate = scene.update.bind(scene);
  scene.update = function(time, delta) {
    originalUpdate(time, delta * factor);
  };

  // 2. Tweens — slows all tween animations
  scene.tweens.timeScale = factor;

  // 3. Scene timers — slows scene.time.addEvent() timers
  scene.time.timeScale = factor;

  // 4. Physics — slows Arcade/Matter physics
  // NOTE: Arcade physics timeScale is INVERSE (higher = slower)
  if (scene.physics?.world) {
    scene.physics.world.timeScale = 1 / factor;
  }

  // 5. Animations — slows sprite animation playback
  if (scene.anims) {
    scene.anims.globalTimeScale = factor;
  }
}, { factor: SLOW_MO_FACTOR });
```

**The 5 subsystems:**
1. **Update delta** — `scene.update(time, delta * factor)` slows frame-delta-dependent logic
2. **Tweens** — `scene.tweens.timeScale` slows all tween animations
3. **Scene timers** — `scene.time.timeScale` slows `scene.time.addEvent()` timers
4. **Physics** — `scene.physics.world.timeScale` slows Arcade/Matter physics (uses inverse: `1/factor`)
5. **Animations** — `scene.anims.globalTimeScale` slows sprite animation playback

### 5. Video Finalization

```js
const video = page.video();
await context.close();  // MUST close context to finalize the video file
const videoPath = await video.path();
```

## Full Capture Script Template

```js
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_DIR = path.resolve(__dirname, '..');

// --- Config ---
const args = process.argv.slice(2);
function getArg(name, fallback) {
  const i = args.indexOf(`--${name}`);
  return i !== -1 && args[i + 1] ? args[i + 1] : fallback;
}

const PORT = getArg('port', '3000');
const GAME_URL = `http://localhost:${PORT}/`;
const VIEWPORT = { width: 1080, height: 1920 }; // 9:16 mobile portrait
const SLOW_MO_FACTOR = 0.5;
const DESIRED_GAME_DURATION = parseInt(getArg('duration', '13000'), 10);
const WALL_CLOCK_DURATION = DESIRED_GAME_DURATION / SLOW_MO_FACTOR;
const OUTPUT_DIR = path.resolve(PROJECT_DIR, getArg('output-dir', 'output'));
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'promo-raw.webm');

// <ADAPT: Generate game-specific input sequence>
function generateInputSequence(totalMs) {
  const sequence = [];
  let elapsed = 0;

  // Pause for entrance animation
  sequence.push({ key: null, holdMs: 0, pauseMs: 1500 });
  elapsed += 1500;

  // <ADAPT: Replace with game-specific keys and timing>
  const keys = ['ArrowLeft', 'ArrowRight'];
  let keyIdx = 0;

  while (elapsed < totalMs) {
    const holdMs = 150 + Math.floor(Math.random() * 450);
    const pauseMs = 50 + Math.floor(Math.random() * 250);

    // Occasional double-tap for variety
    if (Math.random() < 0.15) {
      sequence.push({ key: keys[keyIdx], holdMs: 100, pauseMs: 60 });
      elapsed += 160;
    }

    sequence.push({ key: keys[keyIdx], holdMs, pauseMs });
    elapsed += holdMs + pauseMs;

    // Alternate direction (with occasional same-direction repeats)
    if (Math.random() < 0.75) keyIdx = 1 - keyIdx;
  }

  return sequence;
}

async function captureGameplay() {
  console.log('Capturing promo video...');
  console.log(`  URL: ${GAME_URL} | Viewport: ${VIEWPORT.width}x${VIEWPORT.height}`);
  console.log(`  Game duration: ${DESIRED_GAME_DURATION}ms | Wall clock: ${WALL_CLOCK_DURATION}ms`);

  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: VIEWPORT,
    recordVideo: { dir: OUTPUT_DIR, size: VIEWPORT },
  });

  const page = await context.newPage();
  await page.goto(GAME_URL, { waitUntil: 'networkidle' });

  // Wait for game boot + gameplay active
  await page.waitForFunction(() => window.__GAME__?.isBooted, { timeout: 15000 });
  await page.waitForFunction(() => window.__GAME_STATE__?.started, { timeout: 10000 });
  await page.waitForTimeout(300);
  console.log('  Game active.');

  // <ADAPT: Patch out death — find the actual methods from GameScene.js>
  await page.evaluate(() => {
    const scene = window.__GAME__.scene.getScene('GameScene');
    if (scene) {
      scene.triggerGameOver = () => {};
      scene.onPlayerHit = () => {};
    }
  });
  console.log('  Death patched.');

  // Slow all 5 Phaser time subsystems
  await page.evaluate(({ factor }) => {
    const game = window.__GAME__;
    const scene = game.scene.getScene('GameScene');
    const originalUpdate = scene.update.bind(scene);
    scene.update = function(time, delta) { originalUpdate(time, delta * factor); };
    scene.tweens.timeScale = factor;
    scene.time.timeScale = factor;
    if (scene.physics?.world) scene.physics.world.timeScale = 1 / factor;
    if (scene.anims) scene.anims.globalTimeScale = factor;
  }, { factor: SLOW_MO_FACTOR });
  console.log(`  Slowed to ${SLOW_MO_FACTOR}x.`);

  // Execute input sequence
  const sequence = generateInputSequence(WALL_CLOCK_DURATION);
  console.log(`  Playing ${sequence.length} inputs over ${WALL_CLOCK_DURATION}ms...`);

  for (const seg of sequence) {
    if (!seg.key) { await page.waitForTimeout(seg.pauseMs); continue; }
    await page.keyboard.down(seg.key);
    await page.waitForTimeout(seg.holdMs);
    await page.keyboard.up(seg.key);
    if (seg.pauseMs > 0) await page.waitForTimeout(seg.pauseMs);
  }

  console.log('  Input complete.');

  // Finalize video
  const video = page.video();
  await context.close();
  const videoPath = await video.path();

  if (videoPath !== OUTPUT_FILE) {
    fs.renameSync(videoPath, OUTPUT_FILE);
  }

  await browser.close();
  console.log(`  Raw recording: ${OUTPUT_FILE}`);
  console.log('Done.');
}

captureGameplay().catch(err => { console.error('Capture failed:', err); process.exit(1); });
```

## FFmpeg Conversion

After recording, convert the raw slow-mo WebM to a high-FPS MP4. The `convert-highfps.sh` script is bundled with this skill at `skills/promo-video/scripts/convert-highfps.sh`.

```bash
# Copy to project (orchestrator does this)
cp <plugin-root>/skills/promo-video/scripts/convert-highfps.sh <project-dir>/scripts/

# Run conversion
bash scripts/convert-highfps.sh output/promo-raw.webm output/promo.mp4 0.5
```

The script:
- Applies `setpts` to speed up the video by `1/factor`
- Sets output framerate to `25 / factor` (= 50 FPS for 0.5× slow-mo)
- Encodes H.264 with `crf 23`, `yuv420p`, `faststart`
- Verifies output duration, frame rate, and file size

## Viewport Defaults

**Always record in mobile portrait (9:16)** unless the user explicitly requests otherwise. Rationale:
- Games are played on phones — promo footage should show the real mobile experience
- 9:16 is native for TikTok, Instagram Reels, YouTube Shorts
- 1080×1920 is the standard resolution

| Aspect Ratio | Viewport | Use Case |
|---|---|---|
| **9:16 (default)** | `1080 × 1920` | Mobile portrait — TikTok, Reels, Shorts, Moltbook |
| 1:1 | `1080 × 1080` | Square — Instagram feed, X posts |
| 16:9 | `1920 × 1080` | Landscape — YouTube, trailers, desktop games |

## Duration Guidelines

| Game Type | Recommended Duration | Why |
|-----------|---------------------|-----|
| Arcade / dodger | 10-15s | Fast action, multiple dodge cycles |
| Platformer | 15-20s | Show jump timing, level progression |
| Shooter | 12-18s | Show targeting, enemy waves |
| Puzzle | 8-12s | Show one solve sequence |

## Checklist

Before running the capture:
- [ ] Dev server is running and responding
- [ ] FFmpeg is installed on the system
- [ ] Playwright is installed with Chromium
- [ ] Game boots directly into gameplay (no menu blocking)
- [ ] Death/failure method identified and patched
- [ ] Input keys match the game's actual controls
- [ ] Entrance animation pause is included (1-2s)
- [ ] Output directory exists

After capture:
- [ ] Raw WebM exists in output/
- [ ] FFmpeg conversion produces valid MP4
- [ ] Duration is ~half the raw recording (speed-up worked)
- [ ] Frame rate is 50 FPS
- [ ] Video shows gameplay (not a black screen)
