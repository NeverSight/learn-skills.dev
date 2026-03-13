---
name: worldlabs
description: Generate photorealistic 3D worlds and environments with the World Labs Marble API — Gaussian Splat scenes from text prompts or reference images. Use when the user says "generate a 3D world", "create an environment", "make a 3D scene", or "use World Labs". Requires WLT_API_KEY environment variable.
argument-hint: "[prompt or 'image path/url']"
license: MIT
compatibility: Requires WLT_API_KEY environment variable and internet access for World Labs API calls.
metadata:
  author: OpusGameLabs
  version: 1.3.0
  tags: [game, 3d, worldlabs, environment, gaussian-splat, generation]
---

# World Labs — 3D World/Environment Generation

Generate photorealistic 3D environments from text prompts or images using the World Labs Marble API. Outputs Gaussian Splat scenes (SPZ) rendered via SparkJS in Three.js, plus collider meshes (GLB) for physics.

## When to Use

- **Environment/level generation** — create entire 3D worlds (rooms, landscapes, buildings) from reference images or text
- **Complementary to Meshy AI** — Meshy generates individual models/characters; World Labs generates the environments they exist in
- **Photorealistic scenes** — Gaussian Splats produce photorealistic quality vs mesh-based environments

## Input Priority

**Image-first** — always prefer image input over text:

1. **Image mode (default)** — if the user has a reference image, concept art, screenshot, or photo, use `--mode image`. This produces the most faithful results because the AI can match the exact visual style, layout, lighting, and mood.
2. **Text mode (fallback)** — only use `--mode text` when no reference image is available. The API auto-expands short prompts into rich scene descriptions, but results are less predictable than image-driven generation.

When the game-creator pipeline runs, **ask the user for a reference image first**:

> I can generate a photorealistic 3D environment for your game using World Labs.
> Do you have a reference image (photo, concept art, screenshot) for the environment?
> - **Yes** → provide the file path or URL
> - **No** → I'll generate from a text description instead

## Tech Stack

| Component | Technology |
|-----------|-----------|
| API | World Labs Marble API (`https://api.worldlabs.ai/marble/v1`) |
| Auth | `WLT-Api-Key` header |
| Output: Visual | Gaussian Splat (`.spz`) — 100k, 500k, full resolution tiers |
| Output: Physics | Collider mesh (`.glb`) — for collision detection |
| Output: Skybox | Panorama image (`.jpg`/`.png`) |
| Browser Renderer | SparkJS (`@worldlabs/spark`) — Three.js compatible |
| CLI Script | `scripts/worldlabs-generate.mjs` (zero dependencies) |

## Environment Variable

Before prompting the user, check if the key already exists:
`test -f .env && grep -q '^WORLDLABS_API_KEY=.' .env && echo "found"`
If found, export it with `set -a; . .env; set +a` and skip the prompt.

If not set, ask the user:

> I'll generate a photorealistic 3D environment with World Labs. You can get a free API key:
> 1. Sign up at https://platform.worldlabs.ai
> 2. Go to API Keys
> 3. Create a new key
>
> Paste your key below like: `WORLDLABS_API_KEY=your-key-here`
> (It will be saved to .env and redacted from this conversation automatically.)
>
> Or type "skip" to use basic geometry instead.

## CLI Script Usage

```bash
# Text to 3D world
WORLDLABS_API_KEY=<key> node scripts/worldlabs-generate.mjs \
  --mode text --prompt "a medieval tavern with wooden beams and a roaring fireplace" \
  --output public/assets/worlds/ --slug tavern

# Image to 3D world (local file or URL)
WORLDLABS_API_KEY=<key> node scripts/worldlabs-generate.mjs \
  --mode image --image ./reference-photo.jpg \
  --output public/assets/worlds/ --slug my-world

# Check generation status
WORLDLABS_API_KEY=<key> node scripts/worldlabs-generate.mjs \
  --mode status --operation-id <op-id>

# Download assets from existing world
WORLDLABS_API_KEY=<key> node scripts/worldlabs-generate.mjs \
  --mode get --world-id <id> --output public/assets/worlds/ --slug my-world

# List your worlds
WORLDLABS_API_KEY=<key> node scripts/worldlabs-generate.mjs --mode list
```

### Output Files

```
public/assets/worlds/
  tavern.spz              # Gaussian Splat (full resolution)
  tavern-500k.spz         # Gaussian Splat (500k, medium quality)
  tavern-100k.spz         # Gaussian Splat (100k, lightweight/mobile)
  tavern-collider.glb     # Collider mesh for physics (GLB)
  tavern-pano.jpg         # Panorama image (skybox)
  tavern.meta.json        # Metadata: world ID, prompt, timestamps, asset URLs
```

## Integration with Three.js Games

**Tested & working** — see `examples/worldlabs-arcade/` for a complete runnable demo.

### Install SparkJS

```bash
npm install @sparkjsdev/spark
```

**Package**: `@sparkjsdev/spark` — high-performance Gaussian Splat renderer for Three.js. Supports SPZ, PLY, SOGS, KSPLAT, SPLAT formats.

### Constants.js — World Configuration

```js
export const WORLD = {
  splatPath: 'assets/worlds/tavern-500k.spz',   // 500k is a good desktop default
  colliderPath: 'assets/worlds/tavern-collider.glb',
  panoPath: 'assets/worlds/tavern-pano.png',
  scale: 1,
  position: { x: 0, y: 0, z: 0 },
};
```

### WorldLoader.js — Load Gaussian Splat + Collider

```js
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { SplatMesh } from '@sparkjsdev/spark';
import { WORLD } from '../core/Constants.js';

let _colliderMesh = null;
let _splatMesh = null;

export async function loadWorld(scene, renderer, camera) {
  const promises = [];

  // 1. Gaussian Splat via SparkJS — SplatMesh works like any Three.js object
  if (WORLD.splatPath) {
    promises.push((async () => {
      const splat = new SplatMesh({ url: WORLD.splatPath });
      splat.scale.setScalar(WORLD.scale);
      splat.position.set(WORLD.position.x, WORLD.position.y, WORLD.position.z);
      scene.add(splat);
      _splatMesh = splat;
    })());
  }

  // 2. Collider mesh (GLB) — invisible, for physics raycasting only
  if (WORLD.colliderPath) {
    promises.push((async () => {
      const loader = new GLTFLoader();
      const gltf = await loader.loadAsync(WORLD.colliderPath);
      _colliderMesh = gltf.scene;
      _colliderMesh.visible = false;
      _colliderMesh.scale.setScalar(WORLD.scale);
      _colliderMesh.position.set(WORLD.position.x, WORLD.position.y, WORLD.position.z);
      _colliderMesh.traverse(c => { if (c.isMesh) c.material.side = THREE.DoubleSide; });
      scene.add(_colliderMesh);
    })());
  }

  // 3. Panorama as equirectangular skybox + environment lighting
  if (WORLD.panoPath) {
    promises.push((async () => {
      const texLoader = new THREE.TextureLoader();
      const panoTex = await texLoader.loadAsync(WORLD.panoPath);
      panoTex.mapping = THREE.EquirectangularReflectionMapping;
      panoTex.colorSpace = THREE.SRGBColorSpace;
      scene.background = panoTex;
      scene.environment = panoTex;
    })());
  }

  await Promise.all(promises);
  return { splat: _splatMesh, collider: _colliderMesh };
}

// Raycast down to find ground height on collider mesh
const _raycaster = new THREE.Raycaster();
const _downDir = new THREE.Vector3(0, -1, 0);
const _rayOrigin = new THREE.Vector3();

export function getGroundHeight(x, z, fallback = 0) {
  if (!_colliderMesh) return fallback;
  _rayOrigin.set(x, 50, z);
  _raycaster.set(_rayOrigin, _downDir);
  const hits = _raycaster.intersectObject(_colliderMesh, true);
  return hits.length > 0 ? hits[0].point.y : fallback;
}

export function getCollider() { return _colliderMesh; }
```

### Game.js — Render Loop Integration

SplatMesh renders as part of the normal Three.js scene — **no separate render pass needed**. Just `scene.add(splat)` and call `renderer.render(scene, camera)` as usual.

```js
import { loadWorld, getGroundHeight } from '../level/WorldLoader.js';

// In init():
await loadWorld(scene, renderer, camera);

// In the render loop — standard Three.js, no extra splat pass:
function animate() {
  requestAnimationFrame(animate);

  player.update(delta, input, azimuth);

  // Snap player Y to collider ground
  const groundY = getGroundHeight(player.mesh.position.x, player.mesh.position.z, 0);
  player.mesh.position.y = groundY;

  // Single render call handles both meshes AND splats
  renderer.render(scene, camera);
}
```

## Resolution Tiers

| Tier | File | Quality | Use Case |
|------|------|---------|----------|
| `100k` | `{slug}-100k.spz` | Low | Mobile, fast loading, previews |
| `500k` | `{slug}-500k.spz` | Medium | Desktop games, good balance |
| `full_res` | `{slug}.spz` | High | High-end, hero environments |

Choose based on target platform. The collider mesh (GLB) is the same regardless of splat resolution.

## Pipeline: World Labs + Meshy AI

For a complete 3D game, combine both:

1. **World Labs** → Generate the environment (room, landscape, arena)
2. **Meshy AI** → Generate characters and props (player, enemies, items)
3. **Integrate** → Characters walk on World Labs collider mesh, rendered inside the Gaussian Splat scene

```
┌─────────────────────────────────────────────────┐
│                Complete 3D Scene                 │
├─────────────────────────────────────────────────┤
│  World Labs (environment)                        │
│    └─ Gaussian Splat (visual)                    │
│    └─ Collider mesh (physics)                    │
│    └─ Panorama (skybox)                          │
│                                                   │
│  Meshy AI (entities)                              │
│    └─ Player character (rigged, animated GLB)     │
│    └─ Enemies (rigged, animated GLB)              │
│    └─ Props/items (static GLB)                    │
│                                                   │
│  Three.js (engine)                                │
│    └─ SparkJS renders splats                      │
│    └─ GLTFLoader renders characters/props         │
│    └─ Raycaster uses collider for ground/walls    │
└─────────────────────────────────────────────────┘
```

## Reference Implementation

See `examples/worldlabs-arcade/` — a complete, tested demo with:
- World Labs Gaussian Splat environment (retro arcade)
- Animated Soldier character (walk/run/idle)
- OrbitControls third-person camera
- Collider-mesh ground raycasting
- Panorama skybox

## Troubleshooting

### Scene appears upside down (Y-flip)
**Cause:** World Labs SPZ files use Y-inverted coordinates compared to Three.js convention.
**Fix:** Apply `rotation.x = Math.PI` to both the splat mesh and collider mesh. Then adjust position.z to compensate: `position.z += (minZ + maxZ)`. Do NOT use `scale.y = -1` on a parent group — SparkJS breaks with negative parent scale.

### Raycast hits ceiling instead of floor
**Cause:** After Y-flip, the coordinate system is inverted. Downward raycasts hit what was originally the floor (now the ceiling in flipped space).
**Fix:** Raycast UPWARD from Y=-50 with direction `(0, 1, 0)` to hit the visual floor first. The floor is the lowest surface after the flip.

### Collider mesh raycasts return no hits
**Cause:** The collider mesh's world matrix hasn't been updated after setting rotation/position, especially before the first render frame.
**Fix:** Call `_colliderMesh.updateMatrixWorld(true)` immediately after setting rotation and position, before any raycast operations.

### Scene appears doubled / world inside a world
**Cause:** Using the World Labs panorama as `scene.background` shows the same environment as a giant sphere surrounding the 3D scene.
**Fix:** Don't use the panorama as scene background. Use a solid color (`scene.background = new THREE.Color(0x87CEEB)`) or a custom skybox instead.

### Generation times out or takes too long
**Cause:** World Labs generation typically takes 3-8 minutes. Complex scenes or high server load can extend this.
**Fix:** Poll the operation status endpoint every 10-15 seconds. Check `progress.status` for `"IN_PROGRESS"` vs `"COMPLETE"`. If stuck beyond 15 minutes, create a new generation request — don't retry the same operation.

### Cannot find SparkJS package
**Cause:** The package name is `@sparkjsdev/spark`, not `@worldlabs/spark` or other variations.
**Fix:** Install with `npm install @sparkjsdev/spark`. Import `SplatMesh` from this package. It integrates directly into the Three.js scene — no separate render pass needed.

### Media upload fails with 404
**Cause:** Using the wrong endpoint for media upload preparation.
**Fix:** Use `POST /media-assets:prepare_upload` (NOT `/media-assets`). This returns a signed URL for PUT upload. The colon syntax is intentional — it's a custom action on the resource.

### API returns 401 Unauthorized
**Cause:** Using the wrong authentication header format.
**Fix:** Use `WLT-Api-Key: <your-key>` header, NOT `Authorization: Bearer <your-key>`. The World Labs API uses a custom header format.

## Checklist

- [ ] `WORLDLABS_API_KEY` environment variable is set
- [ ] Ask user for reference image first (image-to-world is preferred)
- [ ] Run `scripts/worldlabs-generate.mjs` to generate world (~3-8 min)
- [ ] SPZ + collider GLB + panorama downloaded to `public/assets/worlds/`
- [ ] `@sparkjsdev/spark` installed (`npm install @sparkjsdev/spark`)
- [ ] `WorldLoader.js` created in `src/level/` (SplatMesh + GLTFLoader + TextureLoader)
- [ ] `Constants.js` updated with `WORLD` config (splatPath, colliderPath, panoPath)
- [ ] `Game.js` calls `loadWorld()` in init, uses `getGroundHeight()` for player Y
- [ ] Single `renderer.render(scene, camera)` handles both splats and meshes — no extra pass
- [ ] Physics uses invisible collider mesh for ground/wall raycasting
- [ ] Test: character walks on collider surface, splat renders around them
- [ ] Performance: use 500k SPZ for desktop, 100k for mobile
