---
name: meshyai
description: Generate custom 3D models from text or images using Meshy AI, then auto-rig and animate them for Three.js games. The preferred source for all 3D game assets.
user-invocable: false
---

# Meshy AI — 3D Model Generation, Rigging & Animation

You are an expert at generating custom 3D models with Meshy AI and integrating them into Three.js browser games. **Meshy is the preferred source for all 3D game assets** — it generates exactly what you need from a text description or reference image, with consistent art style and game-ready topology.

## Why Meshy First

- **Exact match**: Generate precisely the character, prop, or scenery your game needs — no compromises
- **Consistent style**: All assets from the same generation pipeline share a cohesive look
- **Custom characters**: Named personalities, branded characters, unique creatures — all generated to spec
- **Full pipeline**: Generate → rig → animate, all from one tool
- **Game-ready**: Control polycount, topology, and PBR textures for optimal Three.js performance

## Fallback Sources

If `MESHY_API_KEY` is not available and the user declines to set one up, fall back to these in order:

| Fallback | Source | Best for |
|----------|--------|----------|
| `3d-character-library/` | Pre-built GLBs | Quick animated humanoids (Soldier, Xbot, Robot, Fox) |
| `find-3d-asset.mjs` | Sketchfab, Poly Haven, Poly.pizza | Searching existing free model libraries |
| Procedural geometry | Code | BoxGeometry/SphereGeometry as last resort |

## Authentication

All Meshy API calls require `MESHY_API_KEY`. **Always check for this key before starting any 3D asset work.** If the key is not set in the environment, **ask the user immediately**:

> I'll generate custom 3D models with Meshy AI for the best results. You can get a free API key in 30 seconds:
> 1. Sign up at https://app.meshy.ai
> 2. Go to Settings → API Keys
> 3. Create a new API key
>
> What is your Meshy API key? (Or type "skip" to use free model libraries instead)

If the user provides a key, use it via: `MESHY_API_KEY=<key> node scripts/meshy-generate.mjs ...`

If the user skips, proceed with fallback sources (character library → Sketchfab → Poly Haven).

## CLI Script — `scripts/meshy-generate.mjs`

Zero-dependency Node.js script. Handles the full lifecycle: submit task → poll → download GLB → write meta.json.

### Text to 3D (full pipeline)

Generates a 3D model from a text prompt. Two-step process: preview (geometry) → refine (texturing).

```bash
# Full pipeline: preview → refine → download
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode text-to-3d \
  --prompt "a cartoon knight with sword and shield" \
  --output public/assets/models/ \
  --slug knight

# Preview only (faster, untextured — good for geometry check)
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode text-to-3d \
  --prompt "a wooden barrel" \
  --preview-only \
  --output public/assets/models/ \
  --slug barrel

# With PBR textures and specific polycount
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode text-to-3d \
  --prompt "a sci-fi hover bike" \
  --pbr \
  --polycount 15000 \
  --ai-model meshy-6 \
  --output public/assets/models/ \
  --slug hoverbike
```

### Image to 3D

Turn a reference image into a 3D model. Supports URLs, local files, and base64 data URIs.

```bash
# From URL
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode image-to-3d \
  --image "https://example.com/character-concept.png" \
  --output public/assets/models/ \
  --slug character

# From local file (auto-converts to base64)
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode image-to-3d \
  --image "./concept-art/hero.png" \
  --output public/assets/models/ \
  --slug hero
```

### Auto-Rig (humanoids only — MANDATORY for all bipedal characters)

Adds a skeleton to a generated humanoid model and **auto-downloads walking + running animation GLBs**. The input task ID comes from a completed text-to-3d or image-to-3d task.

```bash
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode rig \
  --task-id <meshy-task-id> \
  --height 1.8 \
  --output public/assets/models/ \
  --slug hero
```

This produces 3 files automatically:
- `hero.glb` — rigged model with skeleton
- `hero-walk.glb` — walking animation (auto-downloaded)
- `hero-run.glb` — running animation (auto-downloaded)

**Always chain generate → rig as one atomic step for humanoids.** Never leave humanoid characters as static models.

**Limitations:** Rigging works only on textured humanoid (bipedal) models with clearly defined limbs. Won't work on animals, vehicles, abstract shapes, or untextured meshes.

### Animate

Apply an animation to a rigged model. Requires a completed rig task ID and an animation action ID.

```bash
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode animate \
  --task-id <rig-task-id> \
  --action-id 1 \
  --output public/assets/models/ \
  --slug hero-walk
```

### Check Status

Poll any task's current status.

```bash
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode status \
  --task-id <task-id> \
  --task-type text-to-3d   # or: image-to-3d, rigging, animations
```

### Non-blocking Mode

Submit a task without waiting. Useful in pipelines.

```bash
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode text-to-3d \
  --prompt "a crystal sword" \
  --no-poll

# Later:
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode status --task-id <id> --task-type text-to-3d
```

## Automatic GLB Optimization

All downloaded GLBs are automatically optimized via `scripts/optimize-glb.mjs` to reduce file sizes by 80–95%. The pipeline resizes textures to 1024×1024, converts them to WebP, and applies meshopt compression.

- Optimization runs by default after every GLB download (text-to-3d, image-to-3d, rig, animate)
- Use `--no-optimize` to skip optimization and keep the raw Meshy output
- Use `--texture-size <n>` to change the max texture dimension (default: 1024)
- First run may take a moment as `npx` downloads `@gltf-transform/cli`
- If `gltf-transform` is unavailable, the script warns and continues with the raw file

Optimized GLBs use meshopt compression and require `MeshoptDecoder` at runtime — the template `AssetLoader.js` includes this automatically.

```bash
# Skip optimization for a specific generation
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode text-to-3d --prompt "a barrel" --preview-only \
  --no-optimize --output public/assets/models/ --slug barrel

# Custom texture size (e.g., 512 for mobile)
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode text-to-3d --prompt "a barrel" --preview-only \
  --texture-size 512 --output public/assets/models/ --slug barrel

# Re-optimize an existing GLB directly
node scripts/optimize-glb.mjs public/assets/models/barrel.glb --texture-size 512
```

## API Reference

Base URL: `https://api.meshy.ai/openapi`

### Text to 3D

**POST** `/v2/text-to-3d` — Create preview or refine task

Preview payload:
```json
{
  "mode": "preview",
  "prompt": "a cartoon knight with sword and shield",
  "ai_model": "latest",
  "topology": "triangle",
  "target_polycount": 10000
}
```

Refine payload:
```json
{
  "mode": "refine",
  "preview_task_id": "<preview-task-id>",
  "enable_pbr": true,
  "texture_prompt": "hand-painted fantasy style"
}
```

**GET** `/v2/text-to-3d/:id` — Retrieve task (poll this)

Response when complete:
```json
{
  "id": "task-uuid",
  "status": "SUCCEEDED",
  "progress": 100,
  "model_urls": {
    "glb": "https://assets.meshy.ai/...",
    "fbx": "https://assets.meshy.ai/...",
    "obj": "https://assets.meshy.ai/...",
    "usdz": "https://assets.meshy.ai/..."
  },
  "texture_urls": [
    { "base_color": "https://..." }
  ],
  "thumbnail_url": "https://..."
}
```

Optional parameters:
- `ai_model`: `meshy-5`, `meshy-6`, `latest` (default: `latest`)
- `model_type`: `standard` or `lowpoly`
- `topology`: `quad` or `triangle` (default: `triangle`)
- `target_polycount`: 100–300,000 (default: 10,000)
- `symmetry_mode`: `off`, `auto`, `on` (default: `auto`)
- `pose_mode`: `a-pose`, `t-pose`, or empty string
- `enable_pbr`: generates metallic, roughness, and normal maps

### Image to 3D

**POST** `/v1/image-to-3d` — Create task

```json
{
  "image_url": "https://example.com/photo.png",
  "ai_model": "latest",
  "enable_pbr": false,
  "should_texture": true,
  "topology": "triangle",
  "target_polycount": 10000
}
```

**GET** `/v1/image-to-3d/:id` — Retrieve task

Supports `image_url` as public URL, base64 data URI (`data:image/png;base64,...`), or multi-image via **POST** `/v1/multi-image-to-3d` (1–4 images from different angles).

### Rigging

**POST** `/v1/rigging` — Create rigging task

```json
{
  "input_task_id": "<text-to-3d or image-to-3d task id>",
  "height_meters": 1.7
}
```

**GET** `/v1/rigging/:id` — Retrieve task

Result includes:
- `rigged_character_glb_url` — rigged GLB ready for Three.js
- `rigged_character_fbx_url` — rigged FBX
- `basic_animations` — walking/running GLB URLs included free

### Animation

**POST** `/v1/animations` — Create animation task

```json
{
  "rig_task_id": "<rigging-task-id>",
  "action_id": 1
}
```

**GET** `/v1/animations/:id` — Retrieve task

Result includes `animation_glb_url`, `animation_fbx_url`.

### Task Statuses

All tasks progress through: `PENDING` → `IN_PROGRESS` → `SUCCEEDED` / `FAILED` / `CANCELED`

Poll at 5-second intervals. Tasks typically complete in 30s–5min depending on complexity.

### Asset Retention

Meshy retains generated assets for **3 days** (unlimited for Enterprise). Download promptly.

## Quick Reference: Static Props (no rig needed)

For non-humanoid assets (props, scenery, buildings), skip rigging:

```bash
# Generate
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode text-to-3d --prompt "a wooden barrel, low poly game asset" \
  --polycount 5000 --output public/assets/models/ --slug barrel

# Integrate with loadModel (regular clone, no SkeletonUtils)
const barrel = await loadModel('assets/models/barrel.glb');
scene.add(barrel);
```

## Post-Generation Verification (MANDATORY)

After loading any Meshy-generated model, **always verify orientation and scale** before proceeding. Meshy models have unpredictable facing directions and scales. Skipping this step leads to backwards-facing characters and models that overflow their containers.

### Auto-Orientation Check

Meshy models typically face +Z, but this varies. After loading, **log the bounding box and visually verify** via Playwright MCP or dev tools:

```js
// Add this immediately after loading any GLB
model.updateMatrixWorld(true);
const box = new THREE.Box3().setFromObject(model);
const size = box.getSize(new THREE.Vector3());
const center = box.getCenter(new THREE.Vector3());
console.log(`[Model] ${slug} — size: ${size.x.toFixed(2)} x ${size.y.toFixed(2)} x ${size.z.toFixed(2)}`);
console.log(`[Model] ${slug} — center: ${center.x.toFixed(2)}, ${center.y.toFixed(2)}, ${center.z.toFixed(2)}`);
```

**Fixing facing direction:**
- Start with `rotationY: Math.PI` (180 degrees) — most Meshy models need this to face -Z
- If the model faces +Z by default and needs to face the camera: `rotationY: 0`
- If in doubt: take a screenshot, check which way the face/front is pointing, adjust
- Store `rotationY` in Constants.js per model — never hardcode in entity files

### Auto-Scale Fitting

Models must fit within their game context. After loading:

```js
// Calculate scale to fit a target height
const box = new THREE.Box3().setFromObject(model);
const currentHeight = box.max.y - box.min.y;
const targetHeight = 2.0; // desired height in world units
const autoScale = targetHeight / currentHeight;
model.scale.setScalar(autoScale);
```

For container fitting (e.g., robots inside a ring):
```js
// Ensure model fits within container bounds
const containerWidth = RING.PLATFORM_WIDTH * 0.8; // 80% of ring width
const modelWidth = box.max.x - box.min.x;
if (modelWidth * currentScale > containerWidth) {
  const fitScale = containerWidth / modelWidth;
  model.scale.setScalar(Math.min(currentScale, fitScale));
}
```

**Always take a Playwright screenshot after model integration** to visually verify:
1. Characters face the correct direction
2. Characters fit within their environment
3. Characters don't clip through floors/walls/each other

### Floor Alignment

Center the model on X/Z and plant feet on Y=0:
```js
const box = new THREE.Box3().setFromObject(model);
const center = box.getCenter(new THREE.Vector3());
model.position.y = -box.min.y;      // feet on ground
model.position.x = -center.x;       // centered X
model.position.z = -center.z;       // centered Z
```

## Rigging: Mandatory for Humanoid Characters

**Every humanoid character MUST be rigged.** Static models require hacky programmatic animation (moving wrapper groups) that looks artificial. Rigged models get proper skeletal animation — walk, run, punch, etc.

### When to Rig

| Model type | Rig? | Why |
|-----------|------|-----|
| Humanoid character (player, NPC, enemy) | **YES — always** | Skeletal animation for walk/run/idle/attack |
| Animal with legs | **YES** | Walk/run animations |
| Vehicle, prop, building | No | Static or simple rotation |
| Abstract shape, particle | No | Procedural animation |

### Full Pipeline: Generate → Rig → Animate → Integrate

**Step 1: Generate the model**
```bash
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode text-to-3d \
  --prompt "a stylized robot boxer, low poly game character, full body" \
  --pbr --polycount 15000 \
  --output public/assets/models/ --slug robot
```

**Step 2: Rig** (reads refineTaskId from meta.json automatically)
```bash
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode rig \
  --task-id <refine-task-id-from-meta.json> \
  --height 1.7 \
  --output public/assets/models/ --slug robot-rigged
```

Rigging returns:
- `rigged_character_glb_url` — rigged GLB with skeleton (use this as the base model)
- `basic_animations.walking` — walking animation GLB (free, included)
- `basic_animations.running` — running animation GLB (free, included)

**Step 3: Add custom animations** (optional, for game-specific actions)
```bash
# Each action_id corresponds to a different animation
MESHY_API_KEY=<key> node scripts/meshy-generate.mjs \
  --mode animate \
  --task-id <rig-task-id> \
  --action-id <id> \
  --output public/assets/models/ --slug robot-punch
```

**Step 4: Integrate** with `loadAnimatedModel()` + `AnimationMixer`:
```js
import { loadAnimatedModel } from './level/AssetLoader.js';
import * as THREE from 'three';

// Load rigged model (SkeletonUtils.clone preserves bone bindings)
const { model, clips } = await loadAnimatedModel('assets/models/robot-rigged.glb');
const mixer = new THREE.AnimationMixer(model);

// Log clip names — they vary per model
console.log('Clips:', clips.map(c => c.name));

// Load additional animation GLBs and add their clips to the same mixer
const walkData = await loadAnimatedModel('assets/models/robot-walk.glb');
const walkClip = walkData.clips[0];
const walkAction = mixer.clipAction(walkClip);

// fadeToAction pattern for smooth transitions
function fadeToAction(nextAction, duration = 0.3) {
  if (activeAction) activeAction.fadeOut(duration);
  nextAction.reset().setEffectiveTimeScale(1).setEffectiveWeight(1).fadeIn(duration).play();
  activeAction = nextAction;
}

// In update loop:
mixer.update(delta);
```

## Prompt Engineering Tips

Good prompts produce better models:

| Goal | Prompt | Why |
|------|--------|-----|
| Game character | "a stylized goblin warrior, low poly game character, full body" | "low poly" + "game character" = game-ready topology |
| Prop | "a wooden treasure chest, stylized, closed" | Simple, specific, single object |
| Environment piece | "a fantasy stone archway, low poly, game asset" | "game asset" signals clean geometry |
| Vehicle | "a sci-fi hover bike, side view, clean topology" | "clean topology" = fewer artifacts |

**Avoid:**
- Multiple objects in one prompt ("a knight AND a dragon") — generate separately
- Vague prompts ("something cool") — be specific about style and form
- Interior/architectural scenes — Meshy is best for single objects

## Integration with Existing Pipeline

Meshy-generated models slot into the existing 3D asset pipeline:

```
┌─────────────────────────────────────────────────────┐
│                 3D Asset Sources                     │
├──────────────┬──────────────┬───────────────────────┤
│ Free Libraries│ Character Lib │     Meshy AI          │
│ find-3d-asset │ 3d-char-lib/ │ meshy-generate.mjs    │
│   .mjs       │              │ text/image → 3D       │
│              │              │ rig → animate         │
├──────────────┴──────────────┴───────────────────────┤
│              AssetLoader.js                         │
│         loadModel() / loadAnimatedModel()           │
├─────────────────────────────────────────────────────┤
│              Three.js Game                          │
└─────────────────────────────────────────────────────┘
```

All sources output GLB files into `public/assets/models/`. The `AssetLoader.js` doesn't care where the GLB came from — it loads them all the same way.

## Checklist

- [ ] `MESHY_API_KEY` checked — prompted user if not set, or user skipped to fallbacks
- [ ] Prompt is specific (style, poly count, single object)
- [ ] **All humanoid characters rigged** — never skip rigging for bipedal models
- [ ] Downloaded GLB before 3-day expiration
- [ ] **Post-generation verification done** — orientation, scale, floor alignment checked
- [ ] **Playwright screenshot taken** — visually confirmed facing direction + fit in environment
- [ ] `rotationY` set per model in Constants.js (most Meshy models need `Math.PI`)
- [ ] Static models use `loadModel()` (regular clone)
- [ ] Rigged models use `loadAnimatedModel()` (SkeletonUtils.clone)
- [ ] Clip names logged and `clipMap` defined for animated models
- [ ] `.meta.json` saved alongside GLB with task IDs for traceability
- [ ] `npm run build` succeeds
