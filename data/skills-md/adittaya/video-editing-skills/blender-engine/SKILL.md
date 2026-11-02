---
name: blender-engine
description: "The pack's primary 3D / graphics engine. Drives Blender HEADLESS via Python (bpy) - no GUI, no desktop, no account - for 3D modelling, motion graphics, materials, cameras and animation, camera tracking / matchmoving, VFX / particles / simulations, rigging, Geometry Nodes, compositing, rendering and video encoding. Environment-adaptive: it detects the machine, researches the latest Blender and the best engine/packages for the job, and uses the full power available. Use for any build that needs real 3D, motion graphics, 3D text, camera tracking or procedural geometry."
---

# Blender Engine — the primary 3D / graphics engine

**Scope.** The pack's **primary engine** for 3D and motion graphics. It runs
**headless** and is driven **entirely by Python** through `bpy`. Nothing needs a
desktop, a GUI, or a login.

**When to use.** Whenever the build needs real 3D — 3D text/objects, motion
graphics, camera tracking / matchmoving, geometry nodes, simulations, particles,
rigging, compositing, or a 3D render. Also when a web code-kit is not enough and
the element is genuinely volumetric.

> **THE PROGRAM-IT LAW (mandatory).** Your AI does not need to *see* Blender.
> Your AI **programs** Blender. Never describe UI clicks — write `bpy` code and
> execute it headless. If you can do it in Blender's UI, you can do it in Python.

---

## STEP 0 — THE ENGINE GATE (detect, research, choose — before you script)

Do **not** assume a limit. Detect the machine, research the latest, then choose:

1. **DETECT the environment** — CPU cores, RAM, GPU and its kind (CUDA / OptiX /
   HIP / Metal / none), OS, and the Python version.
   ```python
   import bpy
   p = bpy.context.preferences.addons['cycles'].preferences
   p.get_devices()
   for d in p.devices: print(d.type, d.name, "usable:", d.use)
   ```
2. **RESEARCH the latest** — the current stable **Blender**, the best **render
   engine** for this hardware, and the best **supporting package** per job
   (`TOOLCHAIN.md`). Prefer the latest stable unless the environment requires otherwise.
3. **CHOOSE** version + engine + packages that fit **this** machine, then use its
   **full power**. GPU box → Cycles GPU / EEVEE; CPU box → Cycles CPU. Same
   Blender, different settings.

**Install** (pick the route that fits): portable build (bundles Python — most
robust), the `bpy` module (Python-pinned: 4.x → 3.11, 5.1+ → 3.13), a distro /
container package, or archived wheels. See `BLENDER-ENGINE.md`.
**Verify** before the real job: `blender -b --python-expr "import bpy; print(bpy.app.version_string)"`.

## STEP 0.5 — A-ROLL PREP (if a person speaks)

If a person speaks to camera, prep the A-roll first (see `a-roll-matting`).
Blender's motion tracker can then **matchmove** the shot (STEP 3.4).

---

## 1 · Run it headless

```bash
blender --background --python script.py          # run a script
blender -b scene.blend --python script.py        # open a .blend, then run
blender -b --render-frame 1                      # render a frame
```

## 2 · Pick the engine for the box (adapt, don't assume)

- **GPU present** → **Cycles GPU** (OptiX / CUDA / HIP / Metal), or **EEVEE Next** for speed.
- **No GPU / headless server** → **Cycles CPU** (EEVEE needs a GPU/GL context).
- **Tune to the hardware**: samples, tiles, resolution, and denoising to fit RAM/VRAM.
  On a modest box the denoiser may OOM — lower samples or disable it, and re-enable
  it on a bigger machine.

```python
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'GPU'          # or 'CPU' — chosen from STEP 0
sc.cycles.samples = 128           # raise on a strong box
sc.render.filepath = "/out/frame.png"
bpy.ops.render.render(write_still=True)
```

## 3 · What to script (the pipeline)

1. **Model / edit** — meshes, booleans, modifiers (`bpy.ops.mesh.*`, `bpy.data.meshes`).
2. **Materials, textures, lighting** — Principled BSDF, procedural + image textures, HDRI, sun/area lights.
3. **Cameras & animation** — camera rigs, keyframes, f-curves, motion blur, easing.
4. **Camera tracking / matchmoving** — track footage, solve the camera, reconstruct motion (`bpy.ops.clip.*`); place 3D on the moving shot.
5. **VFX, particles, simulations** — fluids, smoke, cloth, rigid body, particles.
6. **Rigging & character animation** — armatures, weights, constraints.
7. **Geometry Nodes / procedural generation** — node graphs for procedural geometry.
8. **Compositing** — compositor node tree, render passes.
9. **Render** — stills and animation; choose engine, samples, resolution, passes.
10. **Encode video** — Blender bundles **FFmpeg**; encode image sequences to MP4/WebM (or hand frames to the workspace's FFmpeg).

## 4 · Quality checks (before you trust a render)

- **Look at the frame.** Render one frame and *view* it before rendering the
  sequence — never render 120 frames blind.
- **Check the camera** — framing, lens, the move; is the subject in frame the whole time?
- **Check the matte/track** — no drift, no sliding, no holes.
- **Check the render settings** — engine, samples, resolution, colour management.
- **Check the encode** — codec, fps, colour range, audio.

## 5 · Where it sits

- **Remote workspace** (`REMOTE-WORKSPACE.md`) — the execution environment (GPU).
- **`bpy`** — how the AI commands Blender.
- **`TOOLCHAIN.md`** — the packages to pair with it, by use case.
- **FFmpeg** — the encoder (bundled, or the workspace's).
- **`a-roll-matting`** — the prep step when a person speaks.
- **`ADVANCED-FEATURE-USE-CASES.md`** — 3D camera tracking, motion graphics, compositing.

---

## QA GATE
Run `skills/edit-qa-validator` and `tools/qa_check.py` before delivery — audit the
render (framing, matte/track, colour, encode), AI-re-think anything weak,
revalidate, and write `EDIT-QA.md`.

## HARD LIMITS
- **Program it, never click it.** Headless, scripted, no GUI.
- **Detect, research, choose** — never assume the environment's limits.
- **Use the power you have** — GPU when present, CPU when not.
- **Never invent** geometry, brands, faces or claims; label every reconstruction.
- **Route heavy jobs to the workspace**; run one job at a time, release the GPU.
- No account or login is ever required for the core software.
