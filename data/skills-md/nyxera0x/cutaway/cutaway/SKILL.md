---
name: cutaway
description: Build a robotic cutaway of any object or creature from one reference image - a three.js scene written entirely in code that takes itself apart on camera, a page with a button for every part, and a 60 fps film with a synced procedural score. Claude matches the build to the picture, grades it line by line, measures its density and proportions, and films it only after the user approves the still. Use when someone hands over a picture of a robotic animal, machine or device and wants it built in 3D, opened up part by part, or recorded; or asks for a "cutaway", an "exploded view", a "robot animal simulator" or "make this image a 3D model that comes apart".
---

# Cutaway

One picture in, one object out: built from code, opened part by part, filmed. The visitor sees the object move, a cursor presses a button, and that part comes apart under its own camera while live cards around it react. The same code records the film frame by frame, with a score built on the same timeline.

`SKILL_DIR` below is the folder this file lives in. Builds and renders go to `./cutaway-out` of the folder you run from.

## First run

```
cd "$SKILL_DIR" && npm install && npx playwright install chromium
```

The pages need nothing else. The video needs `ffmpeg` on PATH and the score needs Python 3 (standard library only). Set `FFMPEG`, `PYTHON` or `CHROMIUM` to point at other binaries.

## The 3 examples

Build one, open the HTML, watch it take itself apart. Start a new object from the example whose body is closest.

| | The object | Its parts | Worth stealing |
|---|---|---|---|
| `tarantula-*` | A robotic tarantula on 8 bristled legs, a glass abdomen full of lit coils. | Optics, a front leg coming apart on its servos, the abdomen cage opening, the head plates lifting; two jumps. | A walking body: an alternating tetrapod gait integrated from velocity keys, a jump with a crouch and a tuck. |
| `piranha-*` | A deep-bodied robotic piranha with 2 rows of glass fangs and a glass flank over drive gears. | The eye unscrewing in macro, the tail stalk telescoping, the glass flank opening from above, the jaw dropping from below. | One camera per beat aimed at its own part; a mirrored scene; a lunge at the lens. |
| `wasp-*` | A robotic wasp with frosted wings, a telescoping abdomen and a glass stinger. | Optics, a wing pulled out of its hinge and turned over, thorax gears, the abdomen telescoping. | A slow-motion explode as a warp of film time into scene time; a dive in from above and a climb out of the frame. |

Each comes in 3 folders: `<name>-shared/` holds the object, `<name>-film/` the full film (it also opens as a looping page), `<name>-demo/` a 10-second version with its own script.

```
node "$SKILL_DIR/sims/build.mjs" piranha-film      # → cutaway-out/dist/piranha-film.html, offline, ~900 KB
node "$SKILL_DIR/sims/build.mjs"                   # all of them
```

## The method

The 4 files in `docs/` are the method. Read them before the first object, and keep `docs/JOB_DESCRIPTION.md` open the whole time.

| File | What it holds |
|---|---|
| `docs/JOB_DESCRIPTION.md` | The brief: the look, the order of work, the camera, the film, the short version. Every correction the user gives goes into it, one line per mistake. |
| `docs/CHECKLIST.md` | How to write 10 to 12 numbered lines on what one picture stands on, a template and a full example. |
| `docs/PROMPTS.md` | Every prompt, from the reference image to the sound. |
| `docs/LESSONS.md` | Every mistake so far and the line it added to the brief. |

The order, every time:

1. **The reference.** One picture. If the user has none, generate one with the prompt in `docs/PROMPTS.md`. It sets the look and nothing else: never import it, rebuild it.
2. **Measure the picture.** Body height, head length, jaw or limb length as shares of the body length. Dark-pixel share (luma under 80) in its bounding box.
3. **Write the checklist** for this picture before the first line of code.
4. **The still loop.** Build, render a still posed like the reference, stack reference | still | an approved still, plus the stack at 900 px wide, grade every line yes / partial / no against the picture. **Stop after round 2 and show the user.** Nothing gets filmed until they say yes.
5. **The film.** Port the example with the closest body 1:1: its tour, its beat times, its moves, distances scaled. Change the body only. Give every part its own camera.
6. **The short version.** Its own script, never pieces of the long film.
7. **Render and score.**

## How an object is built

One folder per object, split by job. The examples follow this exactly:

| File | Job |
|---|---|
| `spider.js` / `piranha.js` / `bee.js` | The body, built from code: shells, gears, pistons, hoses, lenses, membranes. Every part that comes apart is its own group with a named anchor; `pose(state)` sets the whole object for one moment. |
| `parts.js` | The shop: materials (gloss white shell, accent, graphite, black, steel, lens, glass) and shape helpers. `PAL` holds the colours. |
| `stage.js` | The studio: paper backdrop, lights, soft floor shadow, post. `frame(cam)` draws one frame. |
| `tour.js` / `tour_bee.js` / `tour_v2.js` | The film as functions of time: each act's clock, the flight or walk, the explode, every camera, the telemetry for the page. |
| `sim_green.js` | The wiring: state for t → pose, flight, camera, page. Applies the green look. |
| `../green/` | The page around every object (title, pill buttons the cursor presses, a section list, 4 cards, labels with leaders) and the green look (`look.js`). |
| `score.py` | The sound on the film's timeline. |

For an object outside `SKILL_DIR`, make a folder with a `main.js` and import the kit by name: `import {runSim} from 'cutaway-kit/runtime.js'`. Build it with `node "$SKILL_DIR/sims/build.mjs" ./my-object`.

## Rules that decide whether it works

1. **Start from the picture, never from imagination.** Asked for a robot animal with nothing to match, the model returns a generic toy. With a picture and a checklist it rebuilds what is in front of it.
2. **Port the closest approved film.** A new body on an existing choreography works; a new body on a new choreography is twice the rounds. Flag an object with no close body before starting.
3. **Measure, don't eyeball.** Features pass the checklist while the whole reads as a tidy white diagram. Dark share must reach 0.8 of the reference's; proportions must match within a few hundredths.
4. **One main set of limbs.** Legs, or wings, or tentacles. Two systems fighting for the same half second is noise.
5. **Dense core, plates with gaps.** Break white surfaces into separate curved plates in 3 sizes with gaps over the mechanism. A long smooth shell reads as a toy however many rounds it gets.
6. **Every beat its own camera.** Aim at the part itself, from its own side and height, and push in while it hangs open. Check with `sims/green/cam_track.mjs`: if az, el and distance barely move between beats, the film looks parked.
7. **Review after round 2, 2 objects at a time.** A note after round 2 changes the outcome; after round 6 it only costs tokens.

## The green look

`sims/green/look.js` turns any object green without touching its code: set `PAL.orange` and the paper before the build, then call `retint(root)` after the build and after every pose. It handles material colours, emissive glows, HDR glow colours above 1, colours a pose rewrites every frame, lights and vertex colours. `SHIFT` moves the subject into the page's 3D window. Before a render, run `node sims/green/probe_warm.mjs <entry> <t> <global>`: it lists any warm colour left.

## render(t) contract

```js
import {runSim} from '../kit/runtime.js';

const DEFAULTS = {duration: 20, fps: 60, hud: {enabled: false}, director: {enabled: false}};

runSim(DEFAULTS, async ({cfg, canvas, capture}) => {
  // build the scene, precompute anything stateful
  return {render(t) { /* draw frame t from scratch */ return {}; }, resize() {}};
});
```

- `render(t)` is pure: no `Math.random` (use `rng(seed)` from `kit/util.js` at setup), no `Date`, no state carried between frames. Capture calls it at arbitrary times.
- Anything integrated over time (a gait, the gears' busy clock, a speed ramp) is tabulated at load; `render` only reads the tables.
- Every beat goes into `<name>-film/timeline.json` in seconds. The score reads the same file.
- A short version may run its scene faster than the film: `{"duration": 11.3, "film": 10.0}` plays 11.3 s of scene in 10 s.
- Frame 0 is the thumbnail. It must already show the object big, front 3/4, moving.

## Commands

```
node "$SKILL_DIR/sims/build.mjs" piranha-film
node "$SKILL_DIR/sims/capture.mjs" piranha-film --size 1600x900 --dpr 1.2 --stills beats --cols 4 --out cutaway-out/piranha-beats.png
node "$SKILL_DIR/sims/capture.mjs" piranha-film --size 1600x900 --dpr 1.2 --still 9.4 --out cutaway-out/piranha-9.4.png
node "$SKILL_DIR/sims/capture.mjs" piranha-film --size 1600x900 --dpr 2.4 --out cutaway-out/piranha-4k.mp4
python "$SKILL_DIR/run_sfx.py" "$SKILL_DIR/sims/piranha-shared/score.py"
ffmpeg -y -i cutaway-out/piranha-4k.mp4 -i cutaway-out/piranha-score.wav -map 0:v -map 1:a -vf scale=1920:1080:flags=lanczos -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest -movflags +faststart cutaway-out/piranha.mp4
```

For a demo whose scene runs faster than its film, score the scene and stretch the sound by the same factor:

```
TL="$SKILL_DIR/sims/piranha-demo/timeline.json" OUT=cutaway-out/piranha-demo-scene.wav python "$SKILL_DIR/run_sfx.py" "$SKILL_DIR/sims/piranha-shared/score.py"
ffmpeg -y -i cutaway-out/piranha-demo-scene.wav -af atempo=1.12 cutaway-out/piranha-demo-score.wav
```

`--size` is the CSS layout and `--dpr` multiplies it: 1600 x 900 at 1.2 gives 1920 x 1080, at 2.4 gives 4K to bring down to 1080p (thin veins stay sharp). Capture prints the GPU it got; a software renderer means the GPU flags in `paths.mjs` did not take.

## Review loop

You cannot watch the video; you can look at frames. Never report an object as done without reading sheets of the current render.

1. `--stills beats`: one tile per timeline beat, 0.3 s after it, each labelled `t=`.
2. Read every tile against the checklist below.
3. Zoom in: `--stills every:0.2 --from A --to B` for a transition, `--still T` for one full frame.
4. `node sims/green/cam_track.mjs <entry> <global>` prints the camera every 0.5 s; `node sims/green/anchors_dump.mjs <entry> <global>` prints the parts' rest points to aim cameras at.
5. Fix, rebuild, go back to 1. Stop when a full pass finds nothing.
6. Final: `node "$SKILL_DIR/sheet.mjs" --video <final.mp4> --timeline <timeline.json>` and read that too.

Checklist:

- **The object.** Every part that comes apart goes back where it was; nothing passes through anything; the cards match the motion.
- **Composition.** The opening part fills the frame; the rest may run off. Labels never cover the part they name.
- **The look.** No warm colour left (`probe_warm.mjs`). Green only as lines and glows, never dots.
- **Camera.** A new side, height or distance at every beat. No beat parked.
- **Timing.** A part opens in about 1 s, holds, closes in 0.5 s; a new beat every 2 to 3 s.

## three.js traps the examples already hit

- A glow colour above 1 (an HDR `MeshBasicMaterial`) breaks `getHSL`: read and write it at unit peak.
- A colour the pose rewrites every frame comes back each frame: retint whatever changed since the last write.
- Colours baked into vertex attributes ignore the material: retint the `color` attribute too.
- `smoothstep(a, b, x)` with `a > b` returns 0 on Windows (ANGLE/D3D). Write `1.0 - smoothstep(b, a, x)`.
- One NaN pixel blacks out the whole frame through bloom. Clamp every `pow()` base in a shader.

## Sound

`sfx/` synthesises every sound in pure Python (48 kHz, reproducible) and reads the film's timeline, so sound cannot drift out of sync. `python "$SKILL_DIR/run_sfx.py" --list` shows the generators. `sfx/score_kit.py` has the bed and accents the 3 scores use: a chord bed with soft drums, a pad, airy whooshes, clicks and ticks.

- Every time comes from the timeline, never a typed number.
- Mastering is automatic: −14 LUFS, true peak ≤ −2 dBFS.
- Accent, never narrate: a quiet click per button, a short accent on every part that moves, continuous motion silent.

## Taste, with numbers

- Frame 0: the front 3/4 hero view, the object big and already moving.
- A beat every 2 to 3 s. Visible wing beats 1.5 to 2.5 Hz; faster only as a motion-blurred fan.
- Bristles and spikes 0.15 to 0.25 of the limb's thickness.
- The object fills 60-70% of the 3D window at rest; the opening part fills the frame.
- One accent colour, and it marks what is moving right now.

## Credits

The kit, frame capture, sfx engine and review rules come from [whaleyxbt/claude-motion](https://github.com/whaleyxbt/claude-motion) (MIT). The recorded samples are CC0 from Freesound, trimmed by [Barty-Bart/motion-graphics](https://github.com/Barty-Bart/motion-graphics) (MIT); sources in `sfx/samples/SOURCES.md`.
