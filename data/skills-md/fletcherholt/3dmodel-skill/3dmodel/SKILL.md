---
name: 3dmodel
description: Create 3D models and interactive 3D viewers from a coding agent. Use when asked to model/generate an object/product/part/character in 3D, recreate something in 3D, design a precise/manufacturable/parametric part (CAD), build a web 3D viewer or product display, make an exploded or x-ray/cutaway view, export a GLB/STEP/STL, or improve how a real-time 3D scene looks. Covers the fast AI-generation lane (text/image-to-3D with Tripo/Meshy/Rodin/TRELLIS/Hunyuan3D, then refine), the closed-loop method (generate, render, look, critique, iterate), Blender headless mesh modelling, Autodesk Fusion (formerly Fusion 360) parametric CAD and its Python API (driven via an MCP bridge), Three.js web delivery, realism + delivery optimisation, sourcing real existing CAD models, photogrammetry/Gaussian-splat capture, and interactive-viewer UI patterns.
---

# 3D modelling and interactive 3D viewers

You cannot "see" a 3D scene by intuition. The only way to model well is a **closed feedback loop**: generate geometry, render it to a PNG (or screenshot the live viewer), **Read the image**, critique it like a picky art director, fix the worst defect, repeat. Never ship 3D you have not looked at. One defect per pass; re-render after each. This loop is the edge — it beats one-shotting blind regardless of how strong the underlying model is.

**Default to generating, not hand-modelling, for anything organic or one-off.** The fastest, highest-quality path for props, characters, creatures and "a model of X" is to generate a base mesh in seconds with a text/image-to-3D model, then refine it. Hand-modelling is for surgical edits and for precise CAD. See `references/ai-generation.md` and the section below.

## Decide the delivery target first

- **Blender headless GLB** when the user wants an asset (a `.glb`/`.gltf` to reuse, hand off, or drop into a game/AR/another app), or photoreal stills. See `references/blender-pipeline.md`.
- **Procedural Three.js** when the user wants an interactive web viewer (orbit, animate, click, exploded/x-ray, configurator). You build geometry in JS, so you control everything and avoid export limits. See `references/realtime-3d-web.md`.
- **Fusion 360 (parametric CAD)** when the thing must be precise, dimensioned, manufacturable or engineered — a real product part, an enclosure with exact tolerances, anything heading to CNC/3D-print/sheet-metal, or assemblies with moving joints. Fusion is history-based parametric; Blender is mesh. See `references/fusion360.md`. Export STEP/IGES for engineering, STL/OBJ to bridge into Blender for render.
- **Hybrid**: model detailed parts in Blender, export GLB, load it in a Three.js viewer for interaction. Or: engineer the part in Fusion (STEP) → import to Blender for look-dev/render → glTF to the web.

**Blender vs Fusion 360, the clean split** (verified against Autodesk + Blender docs): Fusion for precise parametric/manufacturable engineering (sketches→constraints→features→assemblies, CAD/CAM, sheet metal, generative design, simulation); Blender for organic/mesh modelling, sculpting, look-dev, animation and rendering. The interop bridge is STEP/IGES (CAD) and STL/OBJ/FBX/glTF (mesh). A common pro pipeline: design in Fusion, render in Blender.

If the user wants a model on a website that is coloured, animated and user-movable, the simplest path is Google `<model-viewer>` (one HTML tag: `camera-controls`, `autoplay`, `ar`); the powerful path is Three.js / React-Three-Fiber. model-viewer plays only ONE animation clip at a time and is awkward to script, so for multi-part animation or click-to-reveal use Three.js directly.

## Generate the base, then refine (the fast lane)

This is what powerful 3D systems actually do, and it is both faster and better than hand-modelling organic shapes. Full detail in `references/ai-generation.md`.

1. **Generate** a base mesh from a text prompt or reference image (these output GLB in seconds via REST APIs you can call end to end):
   - **Tripo** — fastest (~20-30s) and cheapest; default for speed and best-of-N exploration.
   - **Meshy** — strong print-readiness, separate texture-refine step.
   - **Rodin / Hyper3D** — highest fidelity, slower/premium; for a hero asset.
   - **Self-host, free, offline:** TRELLIS-2 (Microsoft, runs ~6GB VRAM) or Hunyuan3D-2.1 (Tencent, production PBR). Best when there is no per-asset budget.
   - Image-to-3D beats text when you have a reference image; fire one prompt at several engines and **pick best-of-N**.
2. **Close the loop on the generation itself:** render/Read the result; if it's wrong, re-prompt or feed a cleaner reference image, don't accept the first output.
3. **Refine** in Blender: import GLB, fix scale, retopologise if it must deform (or just decimate for a static prop), UV unwrap, **bake** the generated detail (normal/AO/colour) onto clean topology, re-shade, then optimise + export through the normal pipeline.
4. **Real-world objects:** photogrammetry (COLMAP/RealityCapture → editable mesh) or Gaussian splatting (photoreal capture; convert to mesh if you need geometry).

Do NOT generate for precise/manufacturable parts — those go to Fusion 360 (parametric CAD). And always check whether a real model already exists to download first.

## The loop, concretely

1. Set up a reusable render harness once (camera framing, 3-point or studio lights, neutral environment, sensible tone mapping). Reuse it for every iteration.
2. Build the model. Start simple, add detail in passes.
3. Render at low samples (fast). For Blender use EEVEE for drafts and Cycles only for hero shots. For web, screenshot the running page.
4. **Read the PNG.** Name the single worst problem (framing, proportion, material, lighting, a missing feature) and fix only that.
5. Repeat until it matches the reference. Then do a final high-quality render/export.

Always work to a reference. If recreating a real object, get reference images (or ask the user for them) and match proportion, colour, layout and the small identifying details. Looking "like a mockup" almost always means: flat untextured surfaces, no bevels, no shadows between parts, and wrong proportions.

## Making real-time 3D look real (not a mockup)

Biggest wins, roughly in order:
- **Soft shadow maps** (`renderer.shadowMap.enabled=true; type=PCFSoftShadowMap`, a key `DirectionalLight` with `castShadow`, large `shadow.mapSize`, `shadow.radius`/`blurSamples` for softness). Component-to-component shadows give crevice depth; a `ShadowMaterial` ground plane gives a soft contact shadow that grounds the object.
- **Bevelled edges** on everything (`RoundedBoxGeometry`, small radius). Sharp 90 degree edges read as fake because real edges catch a highlight.
- **Environment lighting** (`RoomEnvironment` + `PMREMGenerator`, or an HDRI) so metals and glossy plastics reflect something. Bump `envMapIntensity`.
- **Tone mapping** `ACESFilmicToneMapping` with tuned `toneMappingExposure`; modern Three.js lights need higher intensity than you expect.
- **PBR done right**: metalness is effectively binary (0 dielectric, 1 metal); never 0.2-0.8. Combine roughness + metalness + normal maps. For PCBs/painted plastic, a `MeshPhysicalMaterial` with a little `clearcoat` gives the lacquer/solder-mask sheen.
- **Texture detail beats geometry detail** at distance: bake silkscreen/labels/trace patterns into a canvas texture rather than modelling every part. Procedural shader nodes do NOT survive glTF export, so bake to image textures if exporting.
- Optional postprocessing (`EffectComposer`): subtle bloom on emissive parts, SSAO/N8AO for contact occlusion. Add only if needed; it adds dependencies and breakage risk.

## Premium / keynote-grade presentation

To make a viewer feel like a company presenting to Apple, the jump is post-processing plus a real studio stage plus restrained motion. Concretely:

- **Post-processing pipeline** (`EffectComposer`, all from `three/addons/postprocessing/`): `RenderPass` then `GTAOPass` (ground-truth ambient occlusion, built in, no extra dependency, gives grounded contact darkening in crevices) then a SUBTLE `UnrealBloomPass` (strength ~0.4, radius ~0.5, threshold ~0.85 so only bright emissive/speculars bloom) then `OutputPass` (tone mapping + colour space at the end) then `SMAAPass` (MSAA does not work with AO, so anti-alias here). Swap `renderer.render()` for `composer.render()` and call `composer.setSize()` on resize.
- **Studio stage**: a deep, subtle vertical-gradient background (not flat white/paper); a dark low-roughness floor that receives real shadows and softly reflects the environment, which reads as the product floating on glass; and **RectAreaLight softboxes** (`RectAreaLightUniformsLib.init()` first) for the crisp, expensive-looking speculars on plastic and glass. Keep one shadow-casting directional light.
- **A CSS radial vignette** over the canvas (cheap, no shader) frames the shot cinematically.
- **Considered motion** (Apple's rule: every motion has a job): a very slow idle auto-rotate that only runs in the resting hero state and pauses the moment the user touches it (track last input time, not camera movement, or auto-rotate fights itself); a one-second intro that fades the UI chrome up after load; smooth eased state transitions. Nothing moves just to move.
- **Restrained UI**: dark theme, generous whitespace, a small uppercase kicker over a larger sans-serif title, monospace for technical labels, frosted-glass callout cards. Let the product hold the frame.
- Emissive materials with `toneMapped:false` get tonemapped anyway once `OutputPass` runs, but stay bright enough to bloom; tune bloom threshold rather than fighting it.

**Premium has a cost ceiling, respect it.** Post-processing (especially GTAO/SSAO, and to a lesser extent bloom + SMAA) is the most likely thing to make a scene "run like shit" on a normal laptop. Add effects one at a time, watch the frame rate, and be ready to cut them. A clean dark stage with soft shadow maps, environment reflections, an emissive additive-glow for any LEDs, and restrained motion already reads premium with near-zero overhead, no composer required. RectAreaLights are gorgeous for speculars but blow out a glossy floor into a white blob at some angles, use a matte floor (high roughness) or keep area-light intensity low. When in doubt, premium-but-fast beats fancy-but-janky.

**Verify the canvas fills the real window**, not just your test viewport. A WebGL canvas sized to `innerWidth/innerHeight` is correct, but a headless/automation viewport pinned smaller than the actual browser window shows dark margins on the right and bottom that look like a layout bug and are not. Confirm `renderer.setSize` runs on load and on `resize`, then check at the true window size.

## Ship it light (optimise for delivery)

Premium is worthless if it stutters; budget every asset and frame (detail in `references/realtime-3d-web.md`):
- **Compress geometry:** Draco for static, **Meshopt for animated/morph** (Draco drops those). Bake at Blender export or post-process with the `gltf-transform` CLI; wire the matching decoders on the web loader or the GLB won't load.
- **Compress textures:** KTX2/Basis (GPU-native), resize to what's actually visible.
- **LOD:** export decimated variants and swap by distance, or stream progressively.
- **Draw calls:** `InstancedMesh` for repeats, merge static meshes sharing a material, reuse geometry/materials.
- **Lazy + progress:** load big assets on intent, show a `LoadingManager` progress bar, reveal when ready; dispose removed resources.
- **Frame loop:** cap pixel ratio at 2, pause rendering off-screen, cut post-processing first when the rate drops.
Aim for a smooth 60fps on a normal laptop before adding polish.

## Scroll-driven and multi-library scenes (narrative pages)

For Apple-style story pages, separate concerns into layers: a 3D layer (Three.js scene + render loop), an animation layer (scroll/timeline driving 3D properties), and a UI layer (HTML/React overlays). Link camera position, model rotation, or a baked clip's `currentTime` to scroll progress (a plain scroll handler, or GSAP ScrollTrigger / Theatre.js for orchestration). Every motion has a job (reveal, direct, reinforce); ease everything; pin sections during a beat; keep heavy graphical motion sparing and lazy-loaded. When a full WebGL scene is overkill, lightweight depth (CSS 3D transforms, tilt, `<model-viewer>`) is enough.

## Interactive viewer UI patterns

- **Orbit + zoom**: `OrbitControls` with damping. Constrain min/max distance and polar angle so users cannot lose the object.
- **Frame to fit**: pick camera distance from the object's size and the viewport aspect so it never clips off-screen; re-check on resize. Reserve screen margins if you draw side labels.
- **Camera moves**: interpolate camera position in SPHERICAL coordinates around the target (not linear) so it arcs around the object instead of flying through it. Disable `OrbitControls` while a scripted camera move is running, re-enable after, or it fights you.
- **Reveal internals two ways**: (a) **exploded view** parts translate apart along an axis; (b) **x-ray** the outer shell fades out (keep a faint `EdgesGeometry` wireframe so the silhouette stays) and the internals show. If the real product does not open, prefer x-ray and do not imply a hinge/removable cover.
- **Labels / callouts**: do NOT pin labels to the live projected 3D point of each part; they overlap and jitter. Put labels in **fixed screen lanes** (e.g. three down each side) and draw a thin **leader line + dot** from each label to its part's projected point. Stable, no overlap. Write what the part DOES, not just its name.
- **Flow / relationship lines**: draw colour-coded lines between parts to show what connects to what and what it carries (e.g. power vs data vs signal), with a small mid-line label and a legend. Makes an assembly understandable to a non-expert.
- **Hide the overlay while moving**: lines anchored to 3D points swing and look glitchy during a drag. Track whether the camera moved this frame; if it did (or inertia is still settling), fade the whole label/line overlay out, and fade it back in only once the view is still for ~200ms. Also hide any label/line whose part is behind the camera (projected z >= 1).
- **Click vs drag**: a tap (pointer moved < ~6px and < ~320ms) is a click action (e.g. toggle x-ray); anything longer is a drag/rotate. Distinguish on `pointerup`.
- **Match the user's design language** for the surrounding UI; keep chrome minimal and let the object lead.

## Parametric CAD with Autodesk Fusion (formerly Fusion 360)

Autodesk renamed "Fusion 360" to just "Autodesk Fusion" — same application, same `adsk.core`/`adsk.fusion` Python API, same workflow; only the brand name changed (community/tooling, including the MCP bridges, still say "fusion360"). When the job is a precise/manufacturable part, work parametrically, not as a mesh. Full detail + code in `references/fusion360.md`; the essentials:

- **Workflow:** 2D **sketch** → **constrain it fully** (geometric constraints + dimensions; under-constrained geometry is blue, fully-constrained is black) → **features** (extrude/revolve/loft/sweep/fillet/shell/pattern) that record in the **timeline** and auto-update on change → organise as **components** (not bodies — joints need components) → **joints** for motion, **user parameters** for every key dimension so one number drives the model.
- **Design for change:** minimise dependencies, name parameters meaningfully (`wall`, not `D1`), drive shared dims from one parameter, debug via the timeline's error markers.
- **Python API** (`adsk.core`/`adsk.fusion`): `app=Application.get()`, `design=adsk.fusion.Design.cast(app.activeProduct)`, `root=design.rootComponent`. **Units gotcha: internal units are centimetres and radians** — `ValueInput.createByReal(5)` is 5 cm; use `createByString("5 mm")` for real units. Feature pattern: `inp=extrudes.createInput(profile, op); inp.setDistanceExtent(False, dist); extrudes.add(inp)`. Export via `design.exportManager` (STEP/STL/IGES/F3D). **No true headless mode** — scripts run inside the running GUI.
- **Drive Fusion like Blender-MCP:** community MCP servers bridge Claude to a running Fusion via an add-in. The best for a coding agent is **`ndoo/fusion360-mcp-bridge`** (`fusion_execute` to run any Fusion API Python + `fusion_screenshot` for the viewport) — that gives the same generate→run→screenshot→critique loop as Blender. Requires Fusion installed + open. Wire it up like blender-mcp: install the add-in, `claude mcp add`, restart.
- Pro breadth to know exists: CAM/manufacturing (Manufacture workspace, toolpaths, `adsk.cam.generateAllToolpaths` async), sheet metal (flanges → flat patterns for laser/waterjet), generative design (goal-driven, ranked, manufacturing-method-aware), simulation, and Configurations for variants.

## Use a real existing model when it must match reality

Before modelling a real-world part from scratch, **look for the actual CAD/3D model first** (this is what makes "looks like real life" achievable, and what the LED-panel and component searches proved). Sources:
- **Fusion built-in:** Insert → Insert McMaster-Carr Component (real STEP by part number) and Insert Manufacturer Part; the **SnapEDA** Fusion app for PCB parts.
- **Libraries:** McMaster-Carr (free STEP for most parts), GrabCAD (millions of files), 3D ContentCentral, TraceParts, Digi-Key/SnapEDA for electronics, manufacturer STEP downloads.
- **For the web:** Sketchfab/poly.pizza for GLBs (mostly auth-gated or low-poly). If no usable download exists, recreate from reference images with textured PBR — never flat boxes.
Always verify a candidate link is live (they rot fast); prefer a search-results page over a specific listing URL when handing links to a user.

## Pitfalls that waste time (check these first when something looks wrong)

- **Transparent material clipping**: a semi-transparent solid still writes depth and visibly cuts whatever is behind it. Set `depthWrite=false` while transparent; keep materials fully opaque when not fading, or sorting artifacts appear on other objects (e.g. glowing text).
- **Z-fighting**: never leave two faces coplanar. Offset by a hair, or show only one at a time.
- **Frame-swap "animation"** (e.g. a dot-matrix showing different frames): glTF cannot animate textures/materials; either bake separate emissive textures and toggle mesh visibility in JS, or stack frames and step their scale. Do this in the web layer, not the GLB.
- **Procedural shaders do not export** to glTF. Only Principled-BSDF channels + image textures survive. Bake first.
- **Exporter quirks** (Blender): apply object scale to 1,1,1 before export; `export_apply=True` can bake a node's translation into the mesh so `getWorldPosition` returns the origin (anchor labels to known coords instead); auto/`smart_project` UV on a single quad mangles a texture, so set UVs explicitly; the Action API changed in Blender 4.x/5.x (use the keyframe-interpolation preference instead of poking `action.fcurves`).
- **Finding real part models**: Sketchfab/GrabCAD models are mostly login-gated; STLs (Printables/Thingiverse/MakerWorld) have no materials; poly.pizza is free but low-poly. Often the most reliable route is to recreate the part from reference images with textured PCBs/bodies rather than chase a download.

## Verify before claiming done

Render or screenshot the FINAL state and Read it. For interactive viewers, drive the live page (a headless browser via Playwright works well), exercise each state (closed, opening, open, while-dragging) and screenshot each, because bugs hide in transitions.

## Keep this skill growing

After any 3D task, fold genuinely new techniques or pitfalls back into this skill and its reference files (see the linked memory). Prefer durable, reusable knowledge over project specifics; never put a specific client's or project's details here.
