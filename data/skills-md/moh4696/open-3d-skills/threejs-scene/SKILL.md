---
name: threejs-scene
description: Builds real-time 3D websites in three.js from code alone, with no model files. Covers buildings and landmarks, vehicles, machines, landscapes and product studies made of procedural geometry (profile sweeps, lathes, instancing), canvas textures, shader patches, a physically based sky and sun, soft shadows, ambient occlusion and bloom, light presets, camera vantages and flights, quality tiers, and a starter that runs at 60 fps. Use when someone asks for a 3D website, a three.js scene, a WebGL hero, an interactive 3D model of a real place or object, a "3D version" of something, or when an existing three.js page looks flat, plasticky, aliased, washed out or slow.
---

# three.js scene

A convincing 3D page is mostly light and proportion, not polygon count. The White House reads as the White House because its storeys, column spacing and cornice depth are right, and because a low sun throws long shadows across it, not because every window has a frame. This skill builds scenes the way an architect's model is made: from real dimensions, in code, with lighting done properly.

## Start from the starter

`assets/starter/` is a complete, working scene (a round pavilion on a lawn) with everything below already wired. Copy it, keep `env.js`, `kit.js` and `main.js`, and replace `scene.js` with your subject.

```bash
cp -r assets/starter my-scene && cd my-scene
python3 -m http.server 8000      # any static server; ES modules need http://, not file://
```

| File | Holds |
| --- | --- |
| `index.html` | Import map pinned to three r169 (`three@0.169.0`), canvas, title, light buttons, loader |
| `main.js` | Renderer, camera, post stack, quality tiers, vantages and flights, recording hooks, frame loop |
| `env.js` | Sky, sun, image-based light, fog, clouds, night sky; three presets that blend; shadow fitting |
| `kit.js` | Seeded RNG, canvas textures, instancing kit, lathe, arc, profile sweep with mitred corners |
| `scene.js` | The example subject and every pattern worth copying |

URL parameters work out of the box: `?view=front|corner|low|aerial`, `?light=morning|golden|night`, `?quality=high|balanced|fast`, and `?record=1` for a frame-exact recording with `frame-capture`.

## Workflow

1. **Collect references and dimensions before writing geometry.** Plans, elevations, a photo from each side, the real measurements (storey heights, bay spacing, column diameter, wheelbase). Write them as constants at the top of the scene file in metres. A building built from guessed proportions looks like a toy however detailed it is.
2. **Block it out in boxes** at the right size and check from the vantages a visitor will see. Fix proportions now; detail hides nothing.
3. **Detail by kind, not by instance.** Write one column, one window, one baluster as a function, then place hundreds through the `Kit` (one draw call per part). Mouldings, kerbs, steps and rails are profiles swept along paths (`sweep`); round things are lathes.
4. **Light it** with a preset from `env.js`, then tune exposure, sun elevation and fog for the mood. Most of the realism arrives in this step.
5. **Add life:** wind in trees, water, flags, people or traffic as instanced sprites, lamps that come on at night. Drive all of it from the shared uniforms (`U.uTime`, `U.uWind`, `U.uNight`) so recording and light changes stay in sync.
6. **Measure and check** with `site-check`: frame time, draw calls, every vantage at every light, a phone. Then record with `frame-capture`.

## Rendering setup that matters

These are set in `main.js`; keep them unless you know why not.

- **Tone mapping** `ACESFilmicToneMapping` with exposure per preset (0.6 to 1.0). Without tone mapping, bright skies clip and everything looks like a game from 2009.
- **Antialiasing in the composer, not the canvas:** `antialias: false` on the renderer, and a `HalfFloatType` render target with `samples: 4` for the effect composer. Canvas MSAA does nothing once post-processing is on.
- **Post stack:** `RenderPass` → `GTAOPass` (ambient occlusion: contact shadows under cornices, between columns, where walls meet ground) → `UnrealBloomPass` (strength about 0.12 by day, 0.5 at night) → `OutputPass` (tone mapping and sRGB last). The GTAO pass is subclassed to hide anything with `userData.noAO` (sky layers, particles, glass) because AO darkens whatever it sees.
- **Image-based light from the sky itself:** `env.js` renders a private copy of the sky into a PMREM environment map, so reflections and ambient light match the sky's colour at every preset. Regenerate it while presets blend (every sixth frame is enough: PMREM is expensive).
- **One shadow-casting sun** with a 4096 map, its frustum sized to the view and centred on the camera target, snapped to whole texels so shadows do not shimmer as the camera moves. `normalBias` scaled to the scene removes acne without peter-panning.
- **Long lens:** field of view 38. On tall screens the starter widens the vertical FOV so the horizontal view matches a 16:9 screen; a phone sees the whole subject instead of a crop.
- **Pixel ratio capped at 2.** A 3x phone renders 2.25 times the pixels of 2x for no visible gain.

## Light

Each preset in `env.js` moves the sky, sun, hemisphere light, fog, exposure and clouds together. Read `references/lighting.md` before tuning. The short version:

- Low sun (5 to 10 degrees) is where scenes look expensive: long shadows, warm faces, a gradient sky. Set the light a few degrees above the painted sun so faces still read.
- Night is mostly the absence of light. Keep sun intensity near 0.15, let windows and lamps carry the scene with emissive materials plus bloom, and add very few real lights. Point and spot lights use physical units (candela) with `decay: 2`. With decay 1.4 and a guessed intensity, a single fountain light blew out half a scene.
- Every dark light still costs a shadow pass. Hide lights (`visible = false`) when their intensity is zero.

## Geometry patterns

See `references/geometry.md` for details and code. The ones used most:

- `sweep(profile, path, { closed, y })`: a 2D profile of `[outward offset, height]` pairs swept along a path in the XZ plane with mitred corners. Cornices, entablatures, kerbs, road edges, steps, skirting, picture rails. Closed paths detect their winding, so "outward" is always outward.
- `lathe([[r, y], ...])`: columns with entasis, balusters, urns, domes, lamp posts, wheels, bottles.
- `Kit`: define a part once, `add` matrices, `build` one `InstancedMesh` per part. Per-instance colour gives variety (leaf greens, brick tones) at no cost.
- `canvasTex(w, h, draw)`: textures drawn in code with a seeded RNG. Stone speckle, grass, gravel, signage, window grids. No downloads, no licensing, identical on every load.
- Merge static geometry that shares a material (`BufferGeometryUtils.mergeGeometries`) when it is not repeated enough to instance.

## Shader patches

Extend built-in materials with `onBeforeCompile` instead of writing shaders from scratch; you keep lighting, shadows and fog for free. `references/shaders.md` has tested patches for: wind sway, snow on upward faces, seasonal foliage tint, windows that light up at night, water ripple.

The rule that is easy to miss: **a patch that moves vertices must also patch the shadow pass.** Give the mesh a `customDepthMaterial` (a `MeshDepthMaterial` with `RGBADepthPacking`) carrying the same `onBeforeCompile`, as `scene.js` does for the trees. Otherwise leaves sway while their shadows stand still.

## Performance

Budget for a laptop GPU at 1440x900: under 10 ms a frame, under 300 draw calls, under 2 million triangles. `references/performance.md` covers measuring and fixing. In order of payoff:

1. Instance repeated parts (the `Kit`). Draw calls, not triangles, are usually the limit.
2. Quality tiers: `high` (DPR up to 2, GTAO, 4096 shadows), `balanced` (DPR 1.5), `fast` (DPR 1, no GTAO, 2048 shadows). The starter drops a tier by itself after three seconds of slow frames, and never while recording.
3. Do not render what is not moving: if nothing animates and the camera is still, skip `composer.render()`.
4. Keep `castShadow` off for small, distant and flat things.

## Camera

- Define named **vantages** (position plus look-at target) for every view worth seeing. Buttons, deep links, stills and recordings all use them.
- **Flights** between vantages rise over the midpoint and ease in and out (`flyTo` in `main.js`). A straight lerp clips through buildings and feels robotic.
- Limit `OrbitControls`: `maxPolarAngle` just under horizontal, sensible min and max distance, damping on.
- With `prefers-reduced-motion`, flights jump instead of fly, and nothing moves by itself.

## Recording

`?record=1` hides the UI and runs a scripted tour from `window.__recordFrame(t)`, timed on the page clock. Anything delayed must use `later(secs, fn)` from `main.js`, not `setTimeout`. Record with the `frame-capture` skill (`<frame-capture>` is where that skill is installed):

```bash
python3 <frame-capture>/scripts/record.py "http://127.0.0.1:8000/?record=1" tour.mp4 --seconds 20 --ready "window.__ready === true"
```

## Before calling it done

- Every vantage at every light preset, on a laptop size and a phone (`site-check`).
- No shadow acne, no shimmering shadow edges while orbiting, no z-fighting where surfaces meet (offset coplanar decals by 1 to 2 cm).
- Nothing floats or sinks: check where every object meets the ground from a low vantage.
- Frame time and draw calls inside budget.
- If the subject is a real place, object or brand, label the page as an unofficial study and do not use logos.
