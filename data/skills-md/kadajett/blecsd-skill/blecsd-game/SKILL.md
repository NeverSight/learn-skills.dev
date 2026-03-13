---
name: blecsd-game
description: Build terminal games with @blecsd/game. Covers the high-level game API, input actions, fixed timestep physics, game loop lifecycle, and widget creation for game development.
license: MIT
metadata:
  author: blecsd
  version: "2.0.0"
---

# @blecsd/game Package Skill

The `@blecsd/game` package provides a high-level API for building terminal games with blECSd. It wraps the core ECS world, input system, and game loop into a simple `createGame()` factory. All blECSd functional programming rules apply.

**Install:** `pnpm add @blecsd/game`
**Peer dependency:** `blecsd >= 0.7.0`
**Import:** `import { createGame } from '@blecsd/game'`

## Quick Start

```typescript
import { createGame } from '@blecsd/game';

const game = createGame({
  title: 'My Game',
  width: 80,
  height: 24,
  targetFPS: 30,
  mouse: true,
  alternateScreen: true,
  hideCursor: true,
});

// Create UI
const player = game.createBox({
  position: { x: 10, y: 10 },
  dimensions: { width: 3, height: 1 },
  content: '@',
});

// Input
game.onKey('q', () => game.quit());

// Update loop
game.onUpdate((dt) => {
  if (game.isKeyDown('up')) moveUp(dt);
  if (game.isKeyDown('down')) moveDown(dt);
});

// Start
game.start();
```

## API Reference

### createGame(config?)

Factory function that returns a `Game` interface. Config is optional:

```typescript
interface GameConfig {
  title?: string;                // Window title
  width?: number;                // Terminal width
  height?: number;               // Terminal height
  targetFPS?: number;            // Target frame rate (default: 60)
  mouse?: boolean;               // Enable mouse input
  alternateScreen?: boolean;     // Use alternate screen buffer
  hideCursor?: boolean;          // Hide terminal cursor
  fixedTimestep?: {
    tickRate: number;            // Physics tick rate (e.g., 60)
    maxUpdatesPerFrame: number;  // Prevent spiral of death
    interpolate: boolean;        // Interpolate between ticks
  };
}
```

### Widget Creation

All widget factories take a config object and return an entity ID:

```typescript
const box = game.createBox(config);
const text = game.createText(config);
const button = game.createButton(config);
const input = game.createInput(config);
const textarea = game.createTextarea(config);
const textbox = game.createTextbox(config);
const checkbox = game.createCheckbox(config);
const radio = game.createRadioButton(config);
const radioSet = game.createRadioSet(config);
const select = game.createSelect(config);
const slider = game.createSlider(config);
const progress = game.createProgressBar(config);
const list = game.createList(config);
const form = game.createForm(config);
```

### Input System

#### Key Handlers

```typescript
// Single key handler
game.onKey('space', () => shoot());
game.onKey('escape', () => pause());

// Any key handler
game.onAnyKey((keyName) => {
  console.log(`Key pressed: ${keyName}`);
});

// Check if key is currently held
if (game.isKeyDown('left')) moveLeft();
if (game.isKeyDown('right')) moveRight();
```

#### Mouse Handler

```typescript
game.onMouse((event) => {
  // event: { x, y, button, action }
  if (event.action === 'click') {
    handleClick(event.x, event.y);
  }
});
```

#### Action System

Map multiple keys/buttons to named actions:

```typescript
game.defineActions([
  { action: 'move_up', keys: ['up', 'w', 'k'] },
  { action: 'move_down', keys: ['down', 's', 'j'] },
  { action: 'move_left', keys: ['left', 'a', 'h'] },
  { action: 'move_right', keys: ['right', 'd', 'l'] },
  { action: 'shoot', keys: ['space'], mouseButtons: [0] },
  { action: 'interact', keys: ['e', 'enter'] },
]);

// Check action state
game.onUpdate((dt) => {
  if (game.isActionActive('move_up')) player.y -= speed * dt;
  if (game.isActionActive('move_down')) player.y += speed * dt;
  if (game.isActionActive('shoot')) fireBullet();
});
```

### Game Loop

#### Variable Timestep (UI, movement)

```typescript
game.onUpdate((deltaTime) => {
  // deltaTime is seconds since last frame
  playerX += velocityX * deltaTime;
  playerY += velocityY * deltaTime;
  updateAnimations(deltaTime);
});
```

#### Fixed Timestep (Physics, deterministic logic)

```typescript
const game = createGame({
  fixedTimestep: {
    tickRate: 60,             // 60 physics ticks per second
    maxUpdatesPerFrame: 5,    // Prevent spiral of death
    interpolate: true,        // Smooth between ticks
  },
});

game.onFixedUpdate((fixedDt, tick) => {
  // fixedDt is always 1/60 (or 1/tickRate)
  // tick is the current tick number
  applyPhysics(fixedDt);
  checkCollisions();
});
```

#### Render Callback

```typescript
game.onRender((alpha) => {
  // alpha is interpolation factor (0-1) between physics ticks
  // Use for smooth rendering when using fixed timestep
  const renderX = prevX + (currX - prevX) * alpha;
  const renderY = prevY + (currY - prevY) * alpha;
  drawPlayer(renderX, renderY);
});
```

### Lifecycle

```typescript
game.start();              // Start the game loop
game.stop();               // Stop the game loop
game.pause();              // Pause (loop still runs, logic skipped)
game.resume();             // Resume from pause
game.quit();               // Full cleanup and exit

// State queries
game.isRunning();          // Is the loop active?
game.isPaused();           // Is the game paused?

// Performance stats
const stats = game.getStats();
// { fps, frameTime, updateTime, renderTime, entityCount }
```

### ECS World Access

For advanced use, access the underlying blECSd world:

```typescript
import { addEntity, addComponent, hasComponent } from 'blecsd';
import { Position, Velocity } from 'blecsd/components';

// Access world directly
const eid = addEntity(game.world);
addComponent(game.world, eid, Position);
addComponent(game.world, eid, Velocity);
Position.x[eid] = 40;
Velocity.x[eid] = 2;
```

## Common Game Patterns

### Roguelike Movement

```typescript
const game = createGame({ title: 'Roguelike', alternateScreen: true });

let playerX = 40, playerY = 12;

game.defineActions([
  { action: 'up', keys: ['up', 'k'] },
  { action: 'down', keys: ['down', 'j'] },
  { action: 'left', keys: ['left', 'h'] },
  { action: 'right', keys: ['right', 'l'] },
]);

game.onUpdate(() => {
  if (game.isActionActive('up')) playerY--;
  if (game.isActionActive('down')) playerY++;
  if (game.isActionActive('left')) playerX--;
  if (game.isActionActive('right')) playerX++;
});

game.onKey('q', () => game.quit());
game.start();
```

### Simple Physics Game

```typescript
const game = createGame({
  targetFPS: 60,
  fixedTimestep: { tickRate: 60, maxUpdatesPerFrame: 3, interpolate: true },
});

let ballX = 40, ballY = 12, velX = 10, velY = 5;

game.onFixedUpdate((dt) => {
  ballX += velX * dt;
  ballY += velY * dt;

  // Bounce off walls
  if (ballX <= 0 || ballX >= 79) velX *= -1;
  if (ballY <= 0 || ballY >= 23) velY *= -1;
});

game.start();
```

### Dashboard with Stats

```typescript
const game = createGame({ title: 'Dashboard' });

const fpsText = game.createText({
  position: { x: 0, y: 0 },
  dimensions: { width: 20, height: 1 },
});

game.onUpdate(() => {
  const stats = game.getStats();
  setText(game.world, fpsText, `FPS: ${stats.fps.toFixed(1)}`);
});

game.start();
```

## Best Practices

1. **Use `defineActions` for game input.** Map multiple keys to actions instead of checking individual keys everywhere.
2. **Use fixed timestep for physics.** Variable timestep causes non-deterministic physics. Use `fixedTimestep` config and `onFixedUpdate`.
3. **Access `game.world` for advanced ECS.** The game API is a convenience wrapper. For full power, use the blECSd core APIs on `game.world`.
4. **Set `maxUpdatesPerFrame`** to prevent spiral of death when the game can't keep up.
5. **Use `interpolate: true`** with fixed timestep for smooth rendering between physics ticks.
6. **Clean up with `game.quit()`.** This restores the terminal state (cursor, alternate screen, mouse).
7. **All blECSd rules apply.** No classes, no `this`, pure functions, early returns, Zod validation at boundaries.
