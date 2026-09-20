---
name: hand-drawn-canvas-animation
description: >-
  Create hand-drawn short films with whole-pose drawings, expressive strokes and intentional exposure in JavaScript and Canvas 2D: ink, pencil, risograph, screen print, or brush-pen doodles on photos. Includes performance animation, real-motion tracing, sand animation and pop-up paper. Use for hand-drawn cartoons, animated explainers, procedural films, rotoscope, sand stories or drawings interacting with objects. Not for UI animation or slide decks.
---

# Hand-drawn canvas animation

Produce a film that feels drawn by hand in both its marks and its movement.
For character animation, default to whole-pose drawings, expressive strokes and
intentional exposure. Design the keys and breakdowns before any rig or texture.
A rig may guide construction and contacts; the final drawing must carry the pose.
Canvas 2D is the renderer; SVG path data may be used for authored shapes. No
Blender or video model is needed. WebGL is not a dependency. Deliver an HTML
film with its local modules and an offline MP4. Length and format follow the
brief; a short, finished action is the starting point for a longer film.

## Choose the right references

- Read [style.md](references/style.md) for the five looks and their quality gates.
- For a film combining looks or techniques, read
  [mixed-media.md](references/mixed-media.md). Plan why the material changes and
  what carries through the transition before drawing separate style samples.
- Read [redrawn-animation.md](references/redrawn-animation.md) for the default
  stroke-led character workflow, whole cels, assisted inbetweens and exposure sheets.
- Read [motion.md](references/motion.md) before animating characters or a camera.
- Read [studio.md](references/studio.md) for exposure tracks, stable strokes,
  contact IK and materials for optional deformation and construction helpers.
- Read [architecture.md](references/architecture.md) for core APIs and export.
- Read [doodle.md](references/doodle.md) for photo sourcing, anchors and masking;
  [found-motion.md](references/found-motion.md) for traced movement;
  [sand.md](references/sand.md) or [paper3d.md](references/paper3d.md) for those media.
- [palettes.md](references/palettes.md), [scenes.md](references/scenes.md) and
  [reference-films.md](references/reference-films.md) contain optional palettes,
  scene devices and historical references. They are not mandatory film structures.

## Workflow

1. Fill [brief-template.md](references/brief-template.md). Infer routine choices;
   ask only for missing decisions that materially affect the result. Specify the
   intended material and acting reference separately. Pick a primary aspect ratio;
   alternate formats need composition review, not just a different canvas size.
2. Create one project folder. Copy `assets/core.js`, `assets/studio.js`,
   `assets/cels.js`, optional `assets/materials.js`, `scripts/render.mjs` and
   `scripts/package.json` into it. For characters, study
   `examples/sketchbook-bird.html` and build an original cast with whole drawings.
   Its example imports use `../assets/`; change these to local module paths in a
   standalone project. `assets/film-template.html` is a legacy rig demonstration,
   useful for runtime wiring, not the default visual model. Install the local
   renderer dependencies with `npm i --no-audit --no-fund`; system Chrome and ffmpeg
   are required. Keep reusable engine edits in the skill, not in film copies.
3. Establish the drawing: silhouette, proportions, expressions, necessary views,
   line hierarchy, recognizable stroke gestures and a few material samples. Render at delivery size and at
   240 px. A material cannot rescue an unclear pose. Use designed curves and
   replacement drawings where simple primitives fail.
4. Plan the keys and breakdowns of the hardest action. Mark contacts, gaze,
   anticipation, weight transfer and reaction. Use enough controls to express it;
   there is no fixed part count or parameter limit. Build a finite exposure sheet
   of whole drawings. Use geometric inbetweens only for corresponding forms;
   redraw changed overlaps, head angles, compressed silhouettes and expressions.
   Establish timing without decorative textures first. Do not add springs to rigid or motor-driven motion.
5. Finish one representative production shot before building the whole film.
   Evaluate normal-speed playback, consecutive-frame strips and stills. Correct
   anatomy, spacing, contacts and line stability before adding more scenes.
6. Build the remaining shots using a beat sheet: start, duration, what the viewer
   notices, main action, camera and sound cue. Cuts, transitions, blueprint views,
   montages, anchors and sign-offs are artistic choices. Give each action time to
   read. When mixing materials, carry the character's action, position or a
   physical object across the change. A palette swap alone does not establish
   a new style; several impressive but disconnected shots do not establish a story.
7. Render and inspect. Start with `--grid 24`, then use `--strip 48,12` around
   a fast action or contact, and `--only 48` for full-size detail. Run the full
   renderer for the MP4 and generated score. A contact sheet alone cannot pass
   motion QA. If playback is unavailable, explicitly report that limitation.
8. Deliver the source, dependencies/assets, MP4, contact sheet and the remaining
   known limitations. Verify duration, dimensions, frame count and successful
   decode. Never call a film studio-quality solely because its code or checklist
   passed; assess the actual result against the chosen visual reference.

## Production invariants

- `defineFilm` defaults to **24 fps**. A scene receives continuous `tau`; `i`
  remains the legacy 12 Hz index for `pulse`, `boil` and older clips. Use exposure
  tracks per action. Ones, twos, threes and held drawings are all valid.
- Separate camera timing, drawing exposure and root motion. Check their combined
  screen-space motion, especially in a tracking shot. Avoid quantizing twice.
- Randomness is seeded. Make strokes once per drawing, with stable semantic ids.
  A held drawing holds its marks too. Seed changes belong to a new drawing, not
  every output frame. In a deformation workflow, use stable rest-space marks. Specify
  whether a texture belongs to the paper, an object or the screen. A fixed seed
  does not prevent swimming if sampling positions or topology change.
- Each frame must reproduce after seeking in the same pinned runtime. Sand uses
  fixed-step simulation and bounded checkpoints. Font and browser differences
  can change pixels between machines; provide fonts or use path lettering when
  reproducibility matters. Allow fonts and photos to load before export.
- Preserve physical contacts until their planned release. IK clamps unreachable
  targets; check the returned error and fix the pose rather than stretching bones.
- Record sources/licences for external media. Use only assets permitted for the
  intended delivery. Optional SVG is path geometry, not automatic rigging.

## Quality gates

**Drawing:** clear silhouette; consistent proportions across views; controlled
outer/inner line weights; purposeful pressure, taper and gaps; no accidental
tangencies or broken joints. Avoid assembled oval limbs with a texture laid over
them. Clean curves and aligned fills remain valid for the selected medium, but
the default sketch should retain visible drawing gestures. Wobble,
misregistration and boil require a purpose.

**Motion:** whole poses that feel redrawn, meaningful keys, readable breakdowns, deliberate spacing, convincing
weight and planted contacts. Inspect overshoot, camera tracking, topology changes
and fast movement at normal speed and frame by frame. Use a designed smear when
needed; legacy `smear()` makes a ghost trail, not a new drawing.

**Material:** ink hatching follows form; graphite respects pressure and tone;
riso plates register coherently; screen ink may be solid; doodles interact with
the photo. Avoid excessive grain, changing raster phase and unintended shimmer.
For mixed-media work, inspect the transitions as actions, not only a style board.
If weather drives the scene, its force should affect both setting and character.
If paper unfolds, show a compact starting state, the hinges and an attached base.

**Delivery:** no page errors, accidental blank frames, clipped action, stale
frames or unfinished final lettering. If a closing card is requested, let it
finish and hold long enough to read. Check the encoded video, not only PNGs.

## Working examples and commands

[`examples/becoming-phoenix/phoenix.html`](examples/becoming-phoenix/phoenix.html)
is a complete 60-second film with original music. It combines all five looks,
sand and paper projection through one story. Study `inkScene` for a moving
storm, `ensurePrintedPage` for an actual print becoming a page, and
`unfoldPhoenix` for staggered wing and tail opening. Its branding is specific
to the example. Use the techniques that serve the new brief, not its shot list.

`examples/sketchbook-bird.html` is the primary pencil/ink drawing study: nine
whole-body keys, assisted inbetweens, a replacement blink and an exposure sheet.
`examples/weight-study.html` is a secondary seven-second contact/weight study rendered in
five looks with `--look ink|pencil|riso|screen|doodle`. It demonstrates mechanisms,
not the aesthetic target for redrawn characters or proof of feature-film quality. `examples/material-studies.html` adds sand-displacement and page-curl close-ups. Earlier
examples remain useful for particular scene devices; see their references above.

```bash
node scripts/render.mjs examples/sketchbook-bird.html --look pencil --grid 18 --out /tmp/pencil-preview
node scripts/render.mjs examples/sketchbook-bird.html --strip 58,24 --out /tmp/motion-preview
node scripts/render.mjs examples/sketchbook-bird.html --width 1920 --out /tmp/drawn-film
node scripts/verify.mjs
```

The renderer honours the film's aspect ratio unless `--ar` is supplied. Each full
render stages its own frames, then replaces that film's outputs after successful
encoding. Old PNGs cannot extend a shorter revision. `--grid`, `--strip` and
`--only` are preview modes and do not replace the full MP4.

For Remotion integration use timebase conversion:
`drawFrame(Math.min(__NDRAW - 1, Math.floor(frame * __fps / compositionFps)))`.
With film and composition both at 24 fps this is simply `drawFrame(frame)`.
