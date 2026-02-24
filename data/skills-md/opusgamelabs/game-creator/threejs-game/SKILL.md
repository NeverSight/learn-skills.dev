---
name: threejs-game
description: Build 3D browser games with Three.js using event-driven modular architecture. Use when creating a new 3D game, adding 3D game features, setting up Three.js scenes, or working on any Three.js game project.
---

# Three.js Game Development

You are an expert Three.js game developer. Follow these opinionated patterns when building 3D browser games.

> **Reference**: See `reference/llms.txt` (quick guide) and `reference/llms-full.txt` (full API + TSL) for official Three.js LLM documentation. Prefer patterns from those files when they conflict with this skill.

## Reference Files

For detailed reference, see companion files in this directory:
- `tsl-guide.md` — Three.js Shading Language reference (NodeMaterial classes, when to use TSL)
- `input-patterns.md` — Gyroscope input, virtual joystick implementation, input priority system

## Tech Stack

- **Renderer**: Three.js (`three@0.183.0+`, ESM imports)
- **Build Tool**: Vite
- **Language**: JavaScript (not TypeScript) for game templates — TypeScript optional
- **Package Manager**: npm

## Project Setup

When scaffolding a new Three.js game:

```bash
mkdir <game-name> && cd <game-name>
npm init -y
npm install three@^0.183.0
npm install -D vite
```

Create `vite.config.js`:

```js
import { defineConfig } from 'vite';

export default defineConfig({
  root: '.',
  publicDir: 'public',
  server: { port: 3000, open: true },
  build: { outDir: 'dist' },
});
```

Add to `package.json` scripts:

```json
{
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

## Modern Import Patterns

### Vite / npm (default — used in our templates)

```js
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
```

### Import Maps / CDN (standalone HTML games, no build step)

```html
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.183.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.183.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
</script>
```

Use import maps when shipping a single HTML file with no build tooling. Pin the version in the import map URL.

## Required Architecture

Every Three.js game MUST use this directory structure:

```
src/
├── core/
│   ├── Game.js          # Main orchestrator - init systems, render loop
│   ├── EventBus.js      # Singleton pub/sub for all module communication
│   ├── GameState.js     # Centralized state singleton
│   └── Constants.js     # ALL config values, balance numbers, asset paths
├── systems/             # Low-level engine systems
│   ├── InputSystem.js   # Keyboard/mouse/gamepad input
│   ├── PhysicsSystem.js # Collision detection
│   └── ...              # Audio, particles, etc.
├── gameplay/            # Game mechanics
│   └── ...              # Player, enemies, weapons, etc.
├── level/               # Level/world building
│   ├── LevelBuilder.js  # Constructs the game world
│   └── AssetLoader.js   # Loads models, textures, audio
├── ui/                  # User interface
│   └── ...              # Game over, overlays
└── main.js              # Entry point - creates Game instance
```

## Core Principles

1. **Core loop first** — Implement one camera, one scene, one gameplay loop. Add player input and a terminal condition (win/lose) **before** adding visual polish. Keep initial scope small: 1 mechanic, 1 fail condition, 1 scoring system.
2. **Gameplay clarity > visual complexity** — Treat 3D as a style choice, not a complexity mandate. A readable game with simple materials beats a visually complex but confusing one.
3. **Restart-safe** — Gameplay must be fully restart-safe. `GameState.reset()` must restore a clean slate. Dispose geometries/materials/textures on cleanup. No stale references or leaked listeners across restarts.

## Core Patterns (Non-Negotiable)

### 1. EventBus Singleton

ALL inter-module communication goes through an EventBus. Modules never import each other directly for communication.

```js
class EventBus {
  constructor() {
    this.listeners = new Map();
  }

  on(event, callback) {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event).add(callback);
    return () => this.off(event, callback);
  }

  once(event, callback) {
    const wrapper = (...args) => {
      this.off(event, wrapper);
      callback(...args);
    };
    this.on(event, wrapper);
  }

  off(event, callback) {
    const cbs = this.listeners.get(event);
    if (cbs) {
      cbs.delete(callback);
      if (cbs.size === 0) this.listeners.delete(event);
    }
  }

  emit(event, data) {
    const cbs = this.listeners.get(event);
    if (cbs) cbs.forEach(cb => {
      try { cb(data); } catch (e) { console.error(`EventBus error [${event}]:`, e); }
    });
  }

  clear(event) {
    event ? this.listeners.delete(event) : this.listeners.clear();
  }
}

export const eventBus = new EventBus();

// Define ALL events as constants — use domain:action naming
export const Events = {
  // Group by domain: player:*, enemy:*, game:*, ui:*, etc.
};
```

### 2. Centralized GameState

One singleton holds ALL game state. Systems read from it, events update it.

```js
import { PLAYER_CONFIG } from './Constants.js';

class GameState {
  constructor() {
    this.player = {
      health: PLAYER_CONFIG.HEALTH,
      score: 0,
    };
    this.game = {
      started: false,
      paused: false,
      isPlaying: false,
    };
  }

  reset() {
    this.player.health = PLAYER_CONFIG.HEALTH;
    this.player.score = 0;
    this.game.started = false;
    this.game.paused = false;
    this.game.isPlaying = false;
  }
}

export const gameState = new GameState();
```

### 3. Constants File

Every magic number, balance value, asset path, and configuration goes in `Constants.js`. Never hardcode values in game logic.

```js
export const PLAYER_CONFIG = {
  HEALTH: 100,
  SPEED: 5,
  JUMP_FORCE: 8,
};

export const ENEMY_CONFIG = {
  SPEED: 3,
  HEALTH: 50,
  SPAWN_RATE: 2000,
};

export const WORLD = {
  WIDTH: 100,
  HEIGHT: 50,
  GRAVITY: 9.8,
  FOG_DENSITY: 0.04,
};

export const CAMERA = {
  FOV: 75,
  NEAR: 0.01,
  FAR: 100,
};

export const COLORS = {
  AMBIENT: 0x404040,
  DIRECTIONAL: 0xffffff,
  FOG: 0x000000,
};

export const ASSET_PATHS = {
  // model paths, texture paths, etc.
};
```

### 4. Game.js Orchestrator

The Game class initializes everything and runs the render loop. Uses `renderer.setAnimationLoop()` — the official Three.js pattern (handles WebGPU async correctly and pauses when the tab is hidden):

```js
import * as THREE from 'three';
import { CAMERA, COLORS, WORLD } from './Constants.js';

class Game {
  constructor() {
    this.clock = new THREE.Clock();
    this.init();
  }

  init() {
    this.setupRenderer();
    this.setupScene();
    this.setupCamera();
    this.setupSystems();
    this.setupUI();
    this.setupEventListeners();
    this.renderer.setAnimationLoop(() => this.animate());
  }

  setupRenderer() {
    this.renderer = new THREE.WebGLRenderer({
      antialias: false,
      powerPreference: 'high-performance',
    });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('game-container').appendChild(this.renderer.domElement);
    window.addEventListener('resize', () => this.onWindowResize());
  }

  setupScene() {
    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(COLORS.FOG, WORLD.FOG_DENSITY);

    this.scene.add(new THREE.AmbientLight(COLORS.AMBIENT, 0.5));
    const dirLight = new THREE.DirectionalLight(COLORS.DIRECTIONAL, 1);
    dirLight.position.set(5, 10, 5);
    this.scene.add(dirLight);
  }

  setupCamera() {
    this.camera = new THREE.PerspectiveCamera(
      CAMERA.FOV,
      window.innerWidth / window.innerHeight,
      CAMERA.NEAR,
      CAMERA.FAR,
    );
  }

  setupSystems() {
    // Initialize game systems
  }

  setupUI() {
    // Initialize UI overlays
  }

  setupEventListeners() {
    // Subscribe to EventBus events
  }

  onWindowResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  animate() {
    const delta = Math.min(this.clock.getDelta(), 0.1); // Cap delta to prevent spiral
    // Update all systems with delta
    this.renderer.render(this.scene, this.camera);
  }
}

export default Game;
```

## Renderer Selection

### WebGLRenderer (default — use for all game templates)

Maximum browser compatibility. Well-established, most examples and tutorials use this. Our templates default to WebGLRenderer.

```js
import * as THREE from 'three';
const renderer = new THREE.WebGLRenderer({ antialias: true });
```

### WebGPURenderer (when you need TSL or compute shaders)

Required for custom node-based materials (TSL), compute shaders, and advanced rendering. Note: import path changes to `'three/webgpu'` and init is async.

```js
import * as THREE from 'three/webgpu';
const renderer = new THREE.WebGPURenderer({ antialias: true });
await renderer.init();
```

**When to pick WebGPU**: You need TSL custom shaders, compute shaders, or node-based materials. Otherwise, stick with WebGL. See `tsl-guide.md` for TSL details.

## Play.fun Safe Zone

The Play.fun SDK renders a **75px fixed iframe** at `top: 0; z-index: 9999`. All HTML overlay UI (game-over screens, menus, buttons, text) must account for this.

### Constants

```js
// In Constants.js
export const SAFE_ZONE = {
  TOP_PX: 75,          // pixels — use for CSS/HTML overlays
  TOP_PERCENT: 8,      // percent of viewport height
};
```

### CSS Rule

All `.overlay` elements (game-over, pause, menus) must include padding to avoid the widget:

```css
.overlay {
  padding-top: max(20px, 8vh); /* Safe zone for Play.fun widget bar */
}
```

### What to Check

- No text, buttons, or interactive elements in the top ~75px of the viewport
- Game-over overlays center content in the **usable area** (below the widget), not the full viewport
- Score displays, titles, and restart buttons are all visible and not hidden behind the widget

**Note**: The 3D canvas itself renders behind the widget, which is fine — only HTML overlay UI needs the safe zone offset. In-world 3D elements (HUD textures, floating text) should avoid the top 8% of screen space.

## Performance Rules

- **Use `renderer.setAnimationLoop()`** instead of manual `requestAnimationFrame`. It pauses when the tab is hidden and handles WebGPU async correctly.
- **Cap delta time**: `Math.min(clock.getDelta(), 0.1)` to prevent death spirals
- **Cap pixel ratio**: `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` — avoids GPU overload on high-DPI screens
- **Object pooling**: Reuse `Vector3`, `Box3`, temp objects in hot loops to minimize GC. Avoid per-frame allocations — preallocate and reuse.
- **Disable shadows on first pass** — Only enable shadow maps when specifically needed and tested on mobile. Dynamic shadows are the single most expensive rendering feature.
- **Keep draw calls low** — Fewer unique materials and geometries = fewer draw calls. Merge static geometry where possible. Use instanced meshes for repeated objects.
- **Prefer simple materials** — Use `MeshBasicMaterial` or `MeshStandardMaterial`. Avoid `MeshPhysicalMaterial`, custom shaders, or complex material setups unless specifically needed.
- **No postprocessing by default** — Skip bloom, SSAO, motion blur, and other postprocessing passes on first implementation. These tank mobile performance. Add only after gameplay is solid and perf budget allows.
- **Keep geometry/material count small** — A game with 10 unique materials renders faster than one with 100. Reuse materials across objects with the same appearance.
- **Use `powerPreference: 'high-performance'`** on the renderer
- **Dispose properly**: Call `.dispose()` on geometries, materials, textures when removing objects
- **Frustum culling**: Let Three.js handle it (enabled by default) but set bounding spheres on custom geometry

## Asset Loading

- Place static assets in `/public/` for Vite
- Use GLB format for 3D models (smaller, single file)
- Use `THREE.TextureLoader`, `GLTFLoader` from `three/addons`
- Show loading progress via callbacks to UI

```js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();

function loadModel(path) {
  return new Promise((resolve, reject) => {
    loader.load(
      path,
      (gltf) => resolve(gltf.scene),
      undefined,
      (error) => reject(error),
    );
  });
}
```

## Input Handling (Mobile-First)

All games MUST work on desktop AND mobile unless explicitly specified otherwise. Allocate 60% effort to mobile / 40% desktop when making tradeoffs. Choose the best mobile input for each game concept:

| Game Type | Primary Mobile Input | Fallback |
|-----------|---------------------|----------|
| Marble/tilt/balance | Gyroscope (DeviceOrientation) | Virtual joystick |
| Runner/endless | Tap zones (left/right half) | Swipe gestures |
| Puzzle/turn-based | Tap targets (44px min) | Drag & drop |
| Shooter/aim | Virtual joystick + tap-to-fire | Dual joysticks |
| Platformer | Virtual D-pad + jump button | Tilt for movement |

### Unified Analog InputSystem

Use a dedicated InputSystem that merges keyboard, gyroscope, and touch into a single analog interface. Game logic reads `moveX`/`moveZ` (-1..1) and never knows the source:

```js
class InputSystem {
  constructor() {
    this.keys = {};
    this.moveX = 0;  // -1..1
    this.moveZ = 0;  // -1..1
    this.isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ||
      (navigator.maxTouchPoints > 1);
    document.addEventListener('keydown', (e) => { this.keys[e.code] = true; });
    document.addEventListener('keyup', (e) => { this.keys[e.code] = false; });
  }

  /** Call from a user gesture (e.g. PLAY button) to init gyro/joystick. */
  async initMobile() {
    // Request gyroscope permission (required on iOS 13+)
    // If denied/unavailable, show virtual joystick fallback
  }

  /** Call once per frame. Merges all sources into moveX/moveZ. */
  update() {
    let mx = 0, mz = 0;
    // Keyboard (always active, acts as override)
    if (this.keys['ArrowLeft'] || this.keys['KeyA']) mx -= 1;
    if (this.keys['ArrowRight'] || this.keys['KeyD']) mx += 1;
    if (this.keys['ArrowUp'] || this.keys['KeyW']) mz -= 1;
    if (this.keys['ArrowDown'] || this.keys['KeyS']) mz += 1;
    const kbActive = mx !== 0 || mz !== 0;
    if (!kbActive) {
      // Read from gyro or joystick (whichever is active)
    }
    this.moveX = Math.max(-1, Math.min(1, mx));
    this.moveZ = Math.max(-1, Math.min(1, mz));
  }
}
```

For detailed gyroscope input, virtual joystick implementation, and input priority patterns, see `input-patterns.md`.

## When Adding Features

1. Create a new module in the appropriate `src/` subdirectory
2. Define new events in `EventBus.js` Events object using `domain:action` naming
3. Add configuration to `Constants.js`
4. Add state to `GameState.js` if needed
5. Wire it up in `Game.js` orchestrator
6. Communicate with other systems ONLY through EventBus

## Pre-Ship Validation Checklist

Before considering a game complete, verify:

- [ ] **Core loop works** — Player can start, play, lose/win, and see the result
- [ ] **Restart works cleanly** — `GameState.reset()` restores a clean slate, all Three.js resources disposed
- [ ] **Touch + keyboard input** — Game works on mobile (gyro/joystick/tap) and desktop (keyboard/mouse)
- [ ] **Responsive canvas** — Renderer resizes on window resize, camera aspect updated
- [ ] **All values in Constants** — Zero hardcoded magic numbers in game logic
- [ ] **EventBus only** — No direct cross-module imports for communication
- [ ] **Resource cleanup** — Geometries, materials, textures disposed when removed from scene
- [ ] **No postprocessing** — Unless explicitly needed and tested on mobile
- [ ] **Shadows disabled** — Unless explicitly needed and budget allows
- [ ] **Delta-capped movement** — `Math.min(clock.getDelta(), 0.1)` on every frame
- [ ] **Mute toggle** — Audio can be muted/unmuted; `isMuted` state is respected
- [ ] **Safe zone respected** — All HTML overlay UI has `padding-top: max(20px, 8vh)` for Play.fun widget (75px at top)
- [ ] **Build passes** — `npm run build` succeeds with no errors
- [ ] **No console errors** — Game runs without uncaught exceptions or WebGL failures
