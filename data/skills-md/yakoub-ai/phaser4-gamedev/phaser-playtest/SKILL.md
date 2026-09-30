---
name: phaser-playtest
description: This skill should be used when the user asks to "playtest my game", "test my Phaser game", "does my game actually run", "check the game in a browser", "verify the game works", "smoke test the game", "automate game testing", "catch black screens", "check for asset 404s", "measure FPS", "screenshot the game", "write a playtest scenario", or whenever Phaser 4 code has been written or changed and needs runtime verification before being handed back to the user.
version: 0.7.0
---

# Phaser 4 Playtesting (Runtime Verification)

`npx tsc --noEmit` proves the code *compiles*. It says nothing about whether the game
**runs**. Every failure below type-checks perfectly and still ships a broken game:

| Failure | What the player sees | What TypeScript says |
|---|---|---|
| Asset path typo | Invisible sprites | Nothing — it's a string |
| Scene missing from `scene: []` | Black screen | Nothing |
| `create()` throws after first line | Half-built scene | Nothing |
| Depth/alpha/camera-scroll mistake | Blank canvas | Nothing |
| Physics body never added | Player falls through floor | Nothing |
| Uncapped emitter | 12 fps | Nothing |

**Runtime verification is not optional.** Run the harness after any change that touches
scene lifecycle, asset loading, physics, or rendering — before telling the user it works.

## Run It

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/phaser-playtest/scripts/playtest.mjs" --project .
```

The harness starts the dev server itself, drives headless Chromium, and shuts the
server down again. No config, no test files required.

Requires Playwright in the project (once):

```bash
npm install -D playwright && npx playwright install chromium
```

### What it checks

1. **Page loads** — HTTP status of the document
2. **Canvas created** — a sized `<canvas>` exists (fails ⇒ Phaser never booted)
3. **Phaser instance reachable** — finds the `Phaser.Game` on `window`
4. **Game booted** — `isBooted === true`
5. **Active scenes** — which scenes run, and how many display objects each holds
6. **Scenes render content** — warns on a scene with an empty display list
7. **Frame rate** — median and 5th-percentile FPS sampled over real frames
8. **Canvas renders content** — pixel analysis; catches the black screen
9. **No uncaught exceptions** — `pageerror` with stack
10. **No console errors**
11. **All assets load** — including files the dev server masks as `200 text/html`

Exit code `0` = pass, `1` = check failures, `2` = harness error. Writes
`.playtest/report.json` plus PNG screenshots.

### Options

| Flag | Purpose |
|---|---|
| `--project DIR` | Project root (default: cwd) |
| `--url URL` | Test an already-running server instead of starting one |
| `--mode dev\|build` | `build` runs `npm run build` + `preview` — catches base-path and bundling bugs |
| `--scenario FILE` | Drive a scripted play session (see below) |
| `--device iphone\|android` | Mobile viewport, DPR, touch, and UA |
| `--settle MS` | Wait before probing (default 3000; raise for slow preloads) |
| `--fail-on-warn` | Treat console warnings as failures (CI) |
| `--json` | Emit only JSON — use when parsing results |
| `--headed` | Show the browser |

## Make the Game Testable (one line)

The deep checks need the game instance. Bundled games keep it in module scope, so
expose it in dev builds only:

```typescript
const game = new Phaser.Game(config);
if (import.meta.env.DEV) (window as any).__PHASER_GAME__ = game;
export default game;
```

Without it the harness still catches black screens, exceptions, and 404s, but skips
scene, FPS, and state assertions — and says so. Add the line; it costs nothing in
production. See `references/instrumenting-games.md` for deterministic-testing hooks
(seeded RNG, time control, state injection).

## Scenario Scripts

A scenario drives input and asserts on live game state. `game` is bound to the
running instance inside every `expression`.

```javascript
// playtest/combat.mjs
export default [
  { name: 'reaches gameplay', action: 'expect',
    expect: { expression: `game.scene.isActive('GameScene')`, equals: true } },

  { name: 'walk right', action: 'key', key: 'ArrowRight', duration: 600 },

  { name: 'player advanced', action: 'expect',
    expect: { expression: `game.scene.getScene('GameScene').player.x > 400`, equals: true } },

  { name: 'attack lands', action: 'press', key: 'Space',
    expect: { expression: `game.registry.get('enemyHp')`, atMost: 90 } },

  { name: 'after-combat', action: 'screenshot' },

  { name: 'holds frame rate', action: 'expect',
    expect: { expression: `game.loop.actualFps`, atLeast: 55 } },
];
```

Actions: `wait` (`ms`), `key` (`key`, `duration`), `press` (`key`), `click` (`x`, `y`
canvas-relative), `screenshot` (`name`), `expect`.
Assertions: `equals` (deep), `atLeast`, `atMost`, or bare `expression` for truthy.

Full reference: `references/playtest-harness.md`.
Worked example: `examples/scenario.example.mjs`.

## Turning a Plan into Tests

Acceptance criteria from `/phaser-gdd` or the phaser-architect agent translate
directly into scenario steps. Write the scenario **when the feature is specified**,
not after it breaks:

| Acceptance criterion | Scenario assertion |
|---|---|
| "Player jumps 3 tiles high" | `game.scene.getScene('GameScene').player.y`, `atMost: spawnY - 96` |
| "Enemy dies in 3 hits" | press attack ×3, then `enemy.active`, `equals: false` |
| "Score persists across scenes" | start GameOver, then `game.registry.get('score')`, `atLeast: 10` |
| "Runs at 60fps with 50 enemies" | spawn via `eval`, then `game.loop.actualFps`, `atLeast: 55` |

## Reading a Failure

| Harness output | Root cause to check first |
|---|---|
| `canvas created` fails | Scene threw in `constructor`/`init`, or the bundle 500s. Read console errors. |
| `active scenes: no scene is running` | Scene missing from `scene: []`, or `create()` threw before completing |
| `canvas renders content` blank, scenes active | Objects off-camera, `alpha: 0`, wrong depth, or camera not following |
| `scenes render content` warns empty | `create()` returned early — usually an exception swallowed by a `try` |
| `all assets load` fails with `text/html` | Path typo, or the asset is in `src/` instead of `public/` |
| `frame rate` low | Uncapped particles, no object pooling, per-frame allocation. Use `/phaser-analyze`. |
| `Phaser game instance found` warns | Add the `__PHASER_GAME__` line above |

## CI

```yaml
- run: npm ci
- run: npx playwright install --with-deps chromium
- run: npx tsc --noEmit
- run: node scripts/playtest.mjs --project . --mode build --fail-on-warn
```

Copy `playtest.mjs` into the project's own `scripts/` so CI does not depend on the
plugin being installed.

## Discipline

- Run the harness **before** reporting a feature complete — not after the user reports a bug.
- A passing `tsc` plus a failing playtest means the work is **not** done.
- When it fails, read `.playtest/report.json` and the screenshots before editing code.
  Investigation-first applies here exactly as in `phaser-debugger`.
- Keep a scenario per major feature under `playtest/`; they are regression tests.

---

## When the failure came from a player

If you are here because someone reported a bug rather than because you just changed code,
use `skills/phaser-feedback/` instead of writing a scenario straight away. It covers
triaging the report first (a "too hard" complaint is not a defect and has no repro), and
maps each claim shape to the right construct — `--repeat` for "sometimes", `sample` for
"gets stuck", `waitFor` for "takes too long", `--heap` for "slows down over time".
