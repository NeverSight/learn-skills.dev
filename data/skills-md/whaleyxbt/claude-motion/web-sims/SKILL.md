---
name: web-sims
description: Build a simulation-style video (agents, particles, 3D machines, fly-throughs) as one HTML page whose render(t) is a pure function of time, then capture it frame by frame to a 60 fps mp4 with sims/capture.mjs. Use when the idea is a simulation or a 3D object rather than motion graphics with text and UI.
---

# Web sims

Read `sims/README.md` first; it has the contract and every command.

## When to use this instead of Remotion

- Hundreds of moving things with their own rules (agents, particles, crawlers).
- A 3D object or machine the camera moves around or flies through.
- Anything that is easier to write as a three.js or canvas page than as React.

Motion graphics with type, UI and timed reveals stay in Remotion (`src/`).

## Workflow

1. Agree on the idea, the hero moment and the length with the user. Default
   format: 1080×1350 layout (4:5), 60 fps, 20–24 s.
2. Put every beat in a `timeline.json` next to the sim (chapters, the hero
   moment, camera keys). Sound scripts read the same file.
3. Start from the closest example: `crawlers` (agents on DOM text),
   `dossier` (the same plus screen-space overlays), `engine` (three.js object
   with cutaway, chapters, fly-through, exploded view, generated sound).
4. Simulate anything stateful once at load; `render(t)` only reads it.
5. Build: `node sims/build.mjs <name>`.
6. Review with stills at every beat:
   `node sims/capture.mjs <name> --stills 0,2,5,8,12,16,20 --cols 4 --out out/sims/<name>-review.png`.
   Open the sheet and check it like the review loop says: frame 0 strong,
   one focal point per frame, nothing blown out by bloom, text readable on a
   phone, labels never cover the subject. Fix and repeat.
7. Sound: a music track (`--music`, the sim gets `cfg.beats` and should hit
   the drop), a generated bed (`python3 sims/<name>/sound.py` like
   `sims/engine/sound.py`), or both mixed with ffmpeg first.
8. Capture: `node sims/capture.mjs <name> --size 1080x1350 --out out/sims/<name>.mp4`
   and look at a sheet of the final file before calling it done.

## Lessons from the examples

- Bloom eats detail: keep emissive and additive layers under ~1.0 and raise
  them only for the one hero moment.
- Glossy metal plus a low sun gives white streaks. Use roughness ≥ 0.45 and
  envMapIntensity ≈ 0.5 on big surfaces.
- One hero object beats a crowd. If parts hide the subject, move them out of
  the way or fade them.
- Chapters + a one-line caption per step + labels with real numbers make a
  simulation read as an explanation, not just eye candy.
- A camera that flies *through* the object is worth more than ten orbits.
