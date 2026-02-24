---
name: game-architecture
description: Game architecture patterns and best practices for browser games. Use when designing game systems, planning architecture, structuring a game project, or making architectural decisions about game code.
user-invocable: false
---

# Game Architecture Patterns

Reference knowledge for building well-structured browser games. These patterns apply to both Three.js (3D) and Phaser (2D) games.

## Reference Files

For detailed reference, see companion files in this directory:
- `system-patterns.md` — Object pooling, delta-time normalization, resource disposal, wave/spawn systems, buff/powerup system, haptic feedback, asset management

## Core Principles

1. **Core Loop First**: Implement the minimum gameplay loop before any polish. The order is: input -> movement -> fail condition -> scoring -> restart. Only after the core loop works should you add visuals, audio, or juice. Keep initial scope small: 1 scene/level, 1 mechanic, 1 fail condition.

2. **Event-Driven Communication**: Modules never import each other for communication. All cross-module messaging goes through a singleton EventBus with predefined event constants.

3. **Centralized State**: A single GameState singleton holds all game state. Systems read state directly and modify it through events. No scattered state across modules.

4. **Configuration Centralization**: Every magic number, balance value, asset path, spawn point, and timing value goes in `Constants.js`. Game logic files contain zero hardcoded values.

5. **Orchestrator Pattern**: One `Game.js` class initializes all systems, manages game flow (boot -> gameplay -> death/win -> restart), and runs the main loop. Systems don't self-initialize. **No title screen by default** — boot directly into gameplay. Only add a title/menu scene if the user explicitly asks for one.

6. **Restart-Safe and Deterministic**: Gameplay must survive full restart cycles cleanly. `GameState.reset()` restores a complete clean slate. All event listeners are removed in cleanup/shutdown. No stale references, lingering timers, leaked tweens, or orphaned physics bodies survive across restarts. Test by restarting 3x in a row — the third run must behave identically to the first.

7. **Clear Separation of Concerns**: Code is organized into functional layers:
   - `core/` - Foundation (Game, EventBus, GameState, Constants)
   - `systems/` - Engine-level systems (input, physics, audio, particles)
   - `gameplay/` - Game mechanics (player, enemies, weapons, scoring)
   - `level/` - World building (level construction, asset loading)
   - `ui/` - Interface (menus, HUD, overlays)

## Event System Design

### Event Naming Convention

Use `domain:action` format grouped by feature area:

```js
export const Events = {
  // Player
  PLAYER_DAMAGED: 'player:damaged',
  PLAYER_HEALED: 'player:healed',
  PLAYER_DIED: 'player:died',

  // Enemy
  ENEMY_SPAWNED: 'enemy:spawned',
  ENEMY_KILLED: 'enemy:killed',

  // Game flow
  GAME_STARTED: 'game:started',
  GAME_PAUSED: 'game:paused',
  GAME_OVER: 'game:over',

  // System
  ASSETS_LOADED: 'assets:loaded',
  LOADING_PROGRESS: 'loading:progress'
};
```

### Event Data Contracts

Always pass structured data objects, never primitives:

```js
// Good
eventBus.emit(Events.PLAYER_DAMAGED, { amount: 10, source: 'enemy', damageType: 'melee' });

// Bad
eventBus.emit(Events.PLAYER_DAMAGED, 10);
```

## State Management

### GameState Structure

Organize state into clear domains:

```js
class GameState {
  constructor() {
    this.player = { health, maxHealth, speed, inventory, buffs };
    this.combat = { killCount, waveNumber, score };
    this.game = { started, paused, isPlaying };
  }
}
```

## Game Flow

Standard flow for both 2D and 3D games:

```
Boot/Load -> Gameplay <-> Pause Menu (if requested)
                      -> Game Over -> Gameplay (restart)
```

**No title screen by default.** Games boot directly into gameplay. The Play.fun widget handles score display, leaderboards, and wallet connect in a deadzone at the top of the game, so no in-game score HUD is needed. Only add a title/menu scene if the user explicitly requests one.

## Mute State Management

Games with audio MUST have a global mute toggle. Store `isMuted` in GameState and wire it to both BGM and SFX:

```js
// In GameState
game: {
  isMuted: false,
  // ...
}

// AudioManager checks before playing
playMusic(patternFn) {
  if (gameState.game.isMuted || !this.initialized) return;
  // ...
}

// SFX checks before playing
export function scoreSfx() {
  if (gameState.game.isMuted) return;
  playNotes([659.25, 987.77], 'square', 0.12, 0.07, 0.3, 5000);
}

// Toggle via EventBus
eventBus.on(Events.AUDIO_TOGGLE_MUTE, () => {
  gameState.game.isMuted = !gameState.game.isMuted;
  if (gameState.game.isMuted) audioManager.stopMusic();
  else audioManager.playMusic(currentTheme);
});
```

Wire mute to a UI button (speaker icon) and keyboard shortcut (M key). Persist preference in `localStorage` if available.

## Common Architecture Pitfalls

- **Unwired physics bodies** — Creating a static physics body (e.g., ground, wall) without wiring it to other bodies via `physics.add.collider()` or `physics.add.overlap()` has no gameplay effect. Every boundary or obstacle needs explicit collision wiring to the entities it should interact with. After creating any static body, immediately add the collider call.
- **Interactive elements blocked by overlapping display objects** — When building UI (buttons, menus), the topmost display object in the scene list receives pointer events. Never hide the interactive element behind a decorative layer. Either make the visual element itself interactive, or ensure nothing is rendered on top of the hit area.
- **Polish before gameplay** — Adding particles, screen shake, and transitions before the core loop works is a common time sink. Get input -> action -> fail condition -> scoring -> restart working first. Everything else is polish.
- **No cleanup on restart** — Forgetting to remove event listeners, destroy timers, and dispose resources in `shutdown()` causes ghost behavior, double-firing events, and memory leaks after restart.

## Pre-Ship Validation Checklist

Before considering a game complete, verify all items:

- [ ] **Core loop** — Player can start, play, lose/win, and see the result
- [ ] **Restart** — Works cleanly 3x in a row with identical behavior
- [ ] **Mobile input** — Touch/tap/swipe/gyro works; 44px minimum tap targets
- [ ] **Desktop input** — Keyboard + mouse works
- [ ] **Responsive** — Canvas resizes correctly on window resize
- [ ] **Constants** — Zero hardcoded magic numbers in game logic
- [ ] **EventBus** — No direct cross-module imports for communication
- [ ] **Cleanup** — All listeners removed in shutdown, resources disposed
- [ ] **Mute toggle** — Audio can be muted/unmuted via UI and keyboard (M)
- [ ] **Delta-based** — All movement uses delta time, not frame count
- [ ] **Build** — `npm run build` succeeds with no errors
- [ ] **No errors** — No uncaught exceptions or console errors at runtime
