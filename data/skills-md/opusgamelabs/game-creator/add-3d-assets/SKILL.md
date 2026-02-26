---
name: add-3d-assets
description: Replace primitive 3D shapes with real GLB models — animated characters, world props, buildings, and scenery for Three.js games
argument-hint: "[path-to-game]"
disable-model-invocation: true
---

# Add 3D Assets

Replace basic geometric shapes (BoxGeometry, SphereGeometry) with real 3D models. The player gets an animated character with idle/walk/run animations. World objects get GLB models from free libraries.

## Instructions

Analyze the game at `$ARGUMENTS` (or the current directory if no path given).

First, load the game-3d-assets skill for the full model pipeline, AssetLoader pattern, and integration patterns.

### Step 1: Audit

- Read `package.json` to confirm this is a Three.js game (not Phaser — use `/add-assets` for 2D games)
- Read `src/core/Constants.js` for entity types, sizes, colors
- Read entity files (`src/gameplay/*.js`, `src/entities/*.js`) — find `BoxGeometry`, `SphereGeometry`, etc.
- Read `src/level/LevelBuilder.js` for environment primitives
- List every entity using geometric shapes
- Identify which entity is the **player character** (needs animated model)

### Step 2: Plan

Split entities into two categories:

**Animated characters** (player, enemies with AI) — use pre-built GLBs from `3d-character-library/`:

| Entity | Character | Reason |
|--------|-----------|--------|
| Player | Soldier | Military/action theme |
| Enemy | RobotExpressive | Sci-fi theme, 13 animations |

Available characters in `3d-character-library/manifest.json`:
- **Soldier** — realistic military (Idle, Walk, Run) — best default
- **Xbot** — stylized mannequin (idle, walk, run + additive poses)
- **RobotExpressive** — cartoon robot (Idle, Walking, Running, Dance, Jump + 8 more)
- **Fox** — low-poly animal (Survey, Walk, Run) — scale 0.02

**World objects** (buildings, props, scenery, collectibles) — search free libraries:

| Entity | Search Query | Source | Notes |
|--------|-------------|--------|-------|
| Tree | "low poly tree" | Sketchfab | Environment |
| House | "medieval house" | Poly Haven | Background |
| Barrel | "barrel" | Poly Haven | Obstacle |
| Coin | "gold coin" | Sketchfab | Collectible |

### Step 3: Download

**Characters** — copy from library (no auth, instant):
```bash
# Find the plugin root (where 3d-character-library/ lives)
cp <plugin-root>/3d-character-library/models/Soldier.glb public/assets/models/
```

**World objects** — search and download:
```bash
# Use --list-only first to review results
node <plugin-root>/scripts/find-3d-asset.mjs --query "barrel" --source polyhaven --list-only

# Download the best match
node <plugin-root>/scripts/find-3d-asset.mjs --query "barrel" --source polyhaven \
  --output public/assets/models/ --slug barrel

# Poly Haven = no auth, CC0 (best for props)
# Sketchfab = search free, download needs SKETCHFAB_TOKEN
```

### Step 4: Integrate

1. Create `src/level/AssetLoader.js` — **use `SkeletonUtils.clone()` for animated models** (import from `three/addons/utils/SkeletonUtils.js`). Regular `.clone()` breaks skeleton → T-pose.
2. Add `CHARACTER` to Constants.js with `path`, `scale`, `facingOffset`, `clipMap`
3. Add `ASSET_PATHS` and `MODEL_CONFIG` for static models
4. Update `Player.js`:
   - `THREE.Group` as position anchor
   - `loadAnimatedModel()` + `AnimationMixer`
   - `fadeToAction()` for idle/walk/run crossfade
   - Camera-relative WASD via `applyAxisAngle(_up, cameraAzimuth)`
   - Model facing: `atan2(v.x, v.z) + CHARACTER.facingOffset`
   - `model.quaternion.rotateTowards(targetQuat, turnSpeed * delta)`
5. Update `Game.js`:
   - Add `OrbitControls` — third-person camera orbiting player
   - Camera follows: move `orbitControls.target` + `camera.position` by player delta
   - Pass `orbitControls.getAzimuthalAngle()` to Player for camera-relative movement
6. Replace environment primitives with `loadModel()` calls + `.catch()` fallback
7. Add `THREE.GridHelper` for visible movement reference
8. Preload all models on startup with `preloadAll()` for instant loading

### Step 5: Tune & Verify

- Run `npm run dev` — walk around with WASD, orbit camera with mouse
- Confirm character animates (Idle when stopped, Walk when moving, Run with Shift)
- Adjust `MODEL_CONFIG` values (scale, rotationY, offsetY) per model
- Run `npm run build` to confirm no errors
- Generate `ATTRIBUTION.md` from `.meta.json` files

## Next Step

Tell the user:

> Your 3D game now has animated characters and real models! The player walks, runs, and idles with smooth animation crossfading. World objects are loaded from GLB files.
>
> **Files created:**
> - `src/level/AssetLoader.js` — model loader with SkeletonUtils
> - `public/assets/models/` — character and world GLB models
> - OrbitControls third-person camera
>
> **Controls:** WASD to move, Shift to run, mouse drag to orbit camera, scroll to zoom.
> Run the game to see everything in action. Adjust `MODEL_CONFIG` in Constants.js to fine-tune scale and orientation.
