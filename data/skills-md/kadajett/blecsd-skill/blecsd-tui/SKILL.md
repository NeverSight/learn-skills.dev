---
name: blecsd-tui
description: Best practices and module map for blECSd, a modern TypeScript terminal UI library built on ECS (bitecs). Use when building, reviewing, or refactoring blECSd apps, widgets, systems, or ECS/game-loop code.
license: MIT
metadata:
  author: blecsd
  version: "2.0.0"
---

# blECSd Core Library Skill

blECSd is a modern, high-performance terminal UI library built on TypeScript and ECS (Entity Component System) architecture using bitecs. It is a ground-up rewrite of the original blessed node library, NOT backwards-compatible. Version: 0.7.0. Node.js >= 22.0.0.

## Hard Rules (Non-Negotiable)

### 1. Purely Functional, No OOP

**BANNED:** `class`, `this`, `new` (except `Map`/`Set`/`Error`), prototype manipulation, inheritance.

```typescript
// WRONG
class MyWidget { private x: number; constructor(x: number) { this.x = x; } }

// CORRECT
interface MyWidget { readonly x: number; }
function createMyWidget(x: number): MyWidget { return { x }; }
```

### 2. No Direct bitecs Imports

Only three files may import from `'bitecs'`: `src/core/ecs.ts`, `src/core/world.ts`, `src/core/types.ts`. Everything else imports from `'blecsd'` (external) or `'../core/ecs'` (internal).

### 3. Library-First Design

Users control their own world and update loop. All functions take `world` as a parameter. Never own a global world.

### 4. Input Priority

INPUT phase is always first in the update loop. Cannot be reordered. All pending input is processed every frame.

### 5. Early Returns and Guard Clauses

Handle errors first, happy path last. Max nesting 2-3 levels.

### 6. File Size Limits

- Component files: max 200 lines
- Widget files: max 300 lines per sub-file
- All other source files: max 500 lines

### 7. Strict TypeScript

- All functions have explicit return types
- No `any` (use `unknown` + type guards)
- Prefer `readonly` arrays and objects
- Branded types for IDs

## Architecture

### Update Loop Phases (in order)

1. **INPUT** (always first, immutable position) — keyboard/mouse
2. **EARLY_UPDATE** — pre-processing, state transitions
3. **UPDATE** — main game/app logic
4. **LATE_UPDATE** — post-processing, cleanup
5. **ANIMATION** — physics, springs, tweens, momentum scrolling
6. **LAYOUT** — positions, sizes, constraints
7. **RENDER** — write to screen buffer
8. **POST_RENDER** — cleanup, telemetry

### Where Does Logic Go?

| Question | Module |
|----------|--------|
| Pure data storage (typed arrays)? | `components/` (200 lines max) |
| Queries entities and transforms state? | `systems/` |
| Combines components into user-facing API? | `widgets/` (300 lines/sub-file) |
| Pure function, no ECS dependency? | `utils/` |
| Validates config or input? | `schemas/` |
| Handles terminal I/O? | `terminal/` |
| ECS primitive (addEntity, etc.)? | `core/` |

**Rule: Components = data only. Systems = logic. Never put business logic in component files.**

## API Surface (Three Tiers)

### Tier 2: Subpath Imports (Recommended)

Full module access — the default for all applications:

```typescript
import { position, content, scroll } from 'blecsd/components';
import { animationSystem, collisionSystem } from 'blecsd/systems';
import { box, tabs, modal, flexbox } from 'blecsd/widgets';
import { createDoubleBuffer, createProgram } from 'blecsd/terminal';
import { BoxConfigSchema } from 'blecsd/schemas';
import { renderText, wrapText } from 'blecsd/utils';
import { enableDebugOverlay } from 'blecsd/debug';
import { queueKeyEvent } from 'blecsd/input';
import { createViState, processViKey } from 'blecsd/input';
```

### Tier 1: Curated Top-Level (`'blecsd'`)

~80 exports for small scripts and quick prototypes. See [API Reference](./ref/api-surface.md).

### Tier 3: Namespace Objects (Preferred for Complex Apps)

Frozen plain objects grouping related functions:

```typescript
import { position, content, dimensions, border } from 'blecsd/components';

position.set(world, eid, 10, 5);
content.set(world, eid, 'Hello');
dimensions.set(world, eid, 40, 10);
border.set(world, eid, { type: 'line' });
```

## Quick Start with createApp()

The **recommended** way to bootstrap a blECSd application (added in v0.7.0):

```typescript
import { createApp } from 'blecsd';
import { createBoxEntity, createTextEntity } from 'blecsd/core';

const app = await createApp({ fullscreen: true, fps: 30 });

// app.world — ECS world
// app.program — terminal input handling
// app.cols, app.rows — terminal dimensions
// app.render() — run one frame
// app.shutdown() — clean exit
// app.start() — start render loop (returns stop fn)

const panel = createBoxEntity(app.world, {
  x: 2, y: 1, width: 40, height: 12,
  border: { type: 1, top: true, bottom: true, left: true, right: true },
});

createTextEntity(app.world, {
  x: 4, y: 2, text: 'My Dashboard', parent: panel,
});

app.program.on('key', (e) => { if (e.name === 'q') app.shutdown(); });
app.start();
```

### createApp Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `cols` | `number` | auto | Terminal columns |
| `rows` | `number` | auto | Terminal rows |
| `fps` | `number` | `0` | Target FPS (0 = manual) |
| `fullscreen` | `boolean` | `true` | Use alternate screen |
| `programOptions` | `ProgramConfig` | — | Additional program config |

### Other DX Helpers

| Function | Purpose |
|----------|---------|
| `createRenderPipeline(stream, opts?)` | Wire output → double-buffer → dirty-tracker pipeline manually |
| `onShutdown(world, opts?)` | Register SIGINT/SIGTERM handlers for clean teardown |
| `renderToString(world, cols, rows)` | Render one frame to a string (testing/snapshots) |

## Reference Documents

Detailed API surfaces are split into reference files to keep this skill focused:

- **[API Surface Reference](./ref/api-surface.md)** — Full Tier 1 exports, component namespaces, widget namespaces, systems list
- **[Terminal & Server Reference](./ref/terminal-server.md)** — Terminal control, server-side (SSH/Telnet/WebSocket), process utils, custom streams, vi mode
- **[Graphics & Media Reference](./ref/graphics-media.md)** — Graphics manager, braille canvas, vector-to-pixel bridge, image widgets

## Common Patterns

### Using the Scheduler

```typescript
import { createWorld, createScheduler, PhaseType } from 'blecsd';

const world = createWorld();
const scheduler = createScheduler();

scheduler.register(inputSystem, PhaseType.INPUT);
scheduler.register(layoutSystem, PhaseType.LAYOUT);
scheduler.register(renderSystem, PhaseType.RENDER);
scheduler.register(outputSystem, PhaseType.POST_RENDER);

function tick() {
  scheduler.run(world);
  requestAnimationFrame(tick);
}
tick();
```

### Custom System

```typescript
import { defineQuery, defineSystem, hasComponent } from 'blecsd';
import { Position, Velocity } from 'blecsd/components';

const movingQuery = defineQuery([Position, Velocity]);

function createMovementSystem() {
  return defineSystem((world) => {
    for (const eid of movingQuery(world)) {
      Position.x[eid] += Velocity.x[eid];
      Position.y[eid] += Velocity.y[eid];
    }
    return world;
  });
}
```

### Widget API Pattern

```typescript
import { createBox, setBoxContent, isBox } from 'blecsd/widgets';

const box = createBox(world, {
  position: { x: 0, y: 0 },
  dimensions: { width: '100%', height: '100%' },
  border: { type: 'line', fg: 0x00ff00 },
  padding: { top: 1, left: 2 },
  content: 'Initial content',
});

setBoxContent(world, box, 'Updated content');
if (isBox(world, box)) { /* ... */ }
```

### Keyboard Shortcuts

Global: Tab (focus next), Shift+Tab (focus prev), Escape (blur).
Lists: Up/k, Down/j, Home/g, End/G, PageUp/Down, Enter (select), / (search).
Text input: Ctrl+A (start), Ctrl+E (end), Ctrl+U (delete to start), Ctrl+K (delete to end), Ctrl+W (delete word).

### Error Handling

```typescript
import { ok, err, isOk, isErr, map } from 'blecsd/errors';

function parseConfig(raw: unknown): Result<Config, ValidationError> {
  const result = ConfigSchema.safeParse(raw);
  if (!result.success) return err(createValidationError(result.error));
  return ok(result.data);
}
```

Error categories: `validation`, `terminal`, `system`, `entity`, `component`, `input`, `render`, `config`, `internal`.

### Testing

```typescript
import { describe, it, expect } from 'vitest';
import { createWorld, addEntity, addComponent, hasComponent } from 'blecsd';

describe('movement system', () => {
  it('updates position from velocity', () => {
    const world = createWorld();
    const eid = addEntity(world);
    addComponent(world, eid, Position);
    addComponent(world, eid, Velocity);
    Position.x[eid] = 0;
    Velocity.x[eid] = 5;

    movementSystem(world);

    expect(Position.x[eid]).toBe(5);
  });
});
```

## ⚠️ Critical: renderSystem Does NOT Render Text Content

The base `renderSystem` only renders **borders and backgrounds**. The `renderContent()` function is a no-op placeholder (see `src/systems/renderSystem.ts:341`). This means:
- `setContent(world, eid, "text")` stores data but nothing appears on screen
- `createTextEntity(world, { text: "Hello" })` creates an invisible text entity

**All official examples use raw ANSI rendering** via `writeRaw()` from `blecsd/systems`. For TUI apps that need visible text, use:
```typescript
import { writeRaw, cursorHome, enterAlternateScreen, hideCursor, setOutputStream } from "blecsd/systems";
import { clearScreen } from "blecsd";

setOutputStream(process.stdout);
enterAlternateScreen();
hideCursor();

// Render with ANSI escape codes
writeRaw(`\x1b[${row};${col}H\x1b[38;2;${r};${g};${b}mHello blECSd!`);
```

## ⚠️ Critical: Dev Server Setup for TUI Apps

**NEVER use `tsx watch` or `nodemon` for interactive TUI apps.** They steal or pipe stdin, breaking `process.stdin.setRawMode(true)`. Symptoms: keypress restarts app, ANSI escape codes echo on screen, arrow keys don't work.

**Use this `dev.mjs` pattern instead:**
```javascript
import { spawn } from "node:child_process";
import { watch } from "node:fs";
let child = null, restarting = false;
function start() {
  child = spawn("npx", ["tsx", "src/index.ts"], {
    stdio: "inherit",  // Child gets actual TTY
    env: { ...process.env },
  });
  child.on("exit", (code) => {
    child = null;
    if (restarting) { restarting = false; start(); }
    else process.exit(code || 0);
  });
}
let debounce = null;
watch("src", { recursive: true }, (_, f) => {
  if (!f?.endsWith(".ts") || debounce) return;
  debounce = setTimeout(() => { debounce = null; }, 500);
  if (child) { restarting = true; child.kill("SIGTERM"); } else start();
});
start();
```

```json
{ "scripts": { "dev": "node dev.mjs" } }
```

## ⚠️ Critical: Use Entity Factories, Not addEntity()

`addEntity(world)` creates a bare entity with **zero components** — no Renderable, no Position, no Dimensions. It will be completely invisible with no error. Always use `createBoxEntity()`, `createTextEntity()`, or other factories from `blecsd/core`.

## Common Anti-Patterns

1. **Using classes** — All code must be functional.
2. **Importing from bitecs directly** — Always import from `blecsd` or `../core/ecs`.
3. **Putting logic in component files** — Components are data only.
4. **Deep nesting** — Use guard clauses and early returns.
5. **Using `any`** — Use `unknown` with type guards.
6. **Missing Zod validation at boundaries** — All config objects need Zod schemas.
7. **Forgetting barrel exports** — Update the module's `index.ts` when adding exports.
8. **Processing input outside INPUT phase** — All input goes through `inputSystem`.
9. **Using addEntity() for UI elements** — Use `createBoxEntity()` etc. Bare entities lack Renderable and are invisible.
10. **Using tsx watch for TUI apps** — Use `dev.mjs` with `stdio: "inherit"` spawn. See warning above.
11. **Expecting renderSystem to show text** — It only renders borders/backgrounds. Use `writeRaw()` for text.

## Module Ownership (Ambiguous Names)

| Function | Canonical Module | Notes |
|----------|-----------------|-------|
| `moveCursor` | `components/textInput/cursor` | 6+ versions exist |
| `fillRect` | `terminal/screen/cell` | 3D package has its own |
| `getText` | `components/content` | Rope utils also have one |

## Development Commands

```bash
pnpm install          # Install dependencies
pnpm dev              # Development mode
pnpm build            # Build (catches issues tests miss)
pnpm test             # Run tests
pnpm test:watch       # Watch mode
pnpm lint             # Biome linter
pnpm lint:fix         # Auto-fix lint
pnpm typecheck        # TypeScript type check
```

## Performance Tips

- Cache queries: `const myQuery = defineQuery([Position, Velocity])` once, reuse everywhere.
- Batch component reads in one pass per entity.
- Use dirty tracking: only re-render changed entities.
- Virtualize large lists with `createVirtualizedList`.
- Use double buffering (`createDoubleBuffer`) for flicker-free rendering.
- Avoid allocations in hot loops.
- Use `frameBudgetSystem` to monitor frame times.

## Add-on Packages

| Package | Import | Purpose |
|---------|--------|---------|
| `@blecsd/3d` | `import { ... } from '@blecsd/3d'` | 3D rendering with software rasterizer |
| `@blecsd/ai` | `import { ... } from '@blecsd/ai'` | AI/LLM interface widgets |
| `@blecsd/game` | `import { ... } from '@blecsd/game'` | High-level game API |
| `@blecsd/audio` | `import { ... } from '@blecsd/audio'` | Audio management |
| `@blecsd/media` | `import { ... } from '@blecsd/media'` | Image/video/GIF rendering |
