---
name: code-based-films
description: Make a short animated or cinematic film (15–30 s) in which every frame is drawn by our own code — models, rigs, animation and simulations as JS programs, procedural textures in Python/numpy, rendered by the kit's own offline WebGPU path tracer on the local GPU (remote GPUs optional) and encoded with FFmpeg. Use for story-led character films, kids' craft-look films and cinematic shorts built with this kit, from story and beat sheet through assets, animatic, look, final render, sound, QA and delivery. Not for generated-video tools (text- or image-to-video), not for After Effects or Blender projects, and not for real-time or game-engine renders.
---

# Code-based films

A film here is a program. Each frame is a pure function of its frame number: the story timeline gives every
character, prop and light its state at time `t`, a shot file gives the camera, the path tracer renders the frame,
FFmpeg assembles the film. Generated images (styleframes, turnarounds) exist only as a **target** to compare
against. They never appear in the frame and are never used as textures.

## Layout

`$SKILL` is this skill's folder. It ships the engine and the tools; paths like `engine/…`, `tools/…` and
`references/…` in this skill are relative to it.

| Path | What it is |
|---|---|
| `setup.sh` | One-time setup on this machine: checks Node ≥ 22.12 and Chrome, installs the engine's two pinned npm packages into `engine/node_modules`. Run `bash "$SKILL/setup.sh"` before the first render. |
| `engine/` | Our GPU path tracer: WebGPU compute (WGSL) in headless Chrome on the local GPU, driven from Node via `puppeteer-core`. `engine/bin/render.mjs` is the CLI (single frames and `--frames a-b` sequences). `engine/README.md` documents the API: `Scene`, materials, lights, media, camera, `PathTracer.launch/render/renderSequence`. |
| `requirements.txt` | Locked Python packages (with checksums) for all optional tools: numpy, pillow, scipy. Install with `python3 -m pip install --require-hashes -r "$SKILL/requirements.txt"`. |
| `tools/beatmap.py` | Music analysis: BPM, downbeats, bars, sections, drop. Writes the bar map the film is timed to. |
| `tools/encode.sh` | FFmpeg encode of frame sequences plus title overlay plus mixed audio. |
| `tools/rp`, `tools/rp_pool.mjs`, `tools/rp_pod/` | Optional: remote rendering on a Runpod pool of RTX 4090 pods (setup, job runner, chunk pool). Not needed for anything. |

The reference film lives in the repo, not in the skill:
`git clone https://github.com/higgsfield-ai/higgsfield-video-engineer`, then `examples/felt-good-morning/`, a complete
20 s felt-and-paper kids' film. Read it as the reference implementation whenever you need a working pattern.

Inside the example: `BEATS.md` (beat sheet), `assets/lib/geo.mjs` (procedural geometry kit) and `assets/lib/rig.mjs`
(rig and scene helpers), `assets/<hero>/build.mjs` (one module per asset), `shots/film.mjs` (shot list, cameras,
per-frame scene factory), `shots/story.mjs` (timeline as functions of `t`), `render_local.mjs` (resumable local
renderer with `preview`/`final` presets, `--dry-run` and `--encode`), `shots/render_job.mjs` (one render job),
`tools/textures.py`, `tools/sfx.py`, `tools/glow.py`, `tools/title_ofl.py`.

A new film is a new project folder with the same structure. `$PROJECT` below means that folder. Link the engine
into it once, `ln -s "$SKILL/engine" "$PROJECT/engine"`, and import it relatively: `../engine/src/scene.mjs` from
`shots/`, `../../engine/src/geom.mjs` from `assets/<x>/`. Inside the repo, `bin/hve new <name>` copies the example
into `projects/<name>` instead, with working imports.

## Pipeline (in order; each phase has a gate)

1. **Story.** Three loglines, pick one. Hook in the first second; a twist that plays on the material of the world
   (yarn, paper, felt, rain, metal); a final image. Gate: approved by the lead.
2. **Music and bar map.** Generate or commission the music first, run `tools/beatmap.py`, read the bars, the
   drop and the stops. The film is timed to this map.
3. **Beat sheet** (`BEATS.md`): one row per shot with time, frame range, picture, lens, light, sound. Big events
   sit on downbeats; the drop carries the story's peak.
4. **Styleframes and turnarounds** (generated images in `refs/`): one styleframe per shot, a turnaround per hero.
   Gate: approved as the target.
5. **Assets in code**, built side by side with the refs, each with a proof render and an honest `GAPS.md`.
6. **Animatic** under the music: real assets, real cameras, low spp (32–64), small resolution (640×480). Gate: edit lock.
7. **Notes pass** on the animatic: story reads without words, every cut has a cause, timing hits the bars.
8. **Light and look pass**: 2–3 test frames per shot against their styleframes at final resolution.
9. **Final render** on the local GPU, in `--frames` chunks, resumable (remote GPUs optional for speed).
10. **Post and sound**: own glow/grade pass, title with an OFL font, own SFX synthesised on the events, music mix.
11. **QA**: machine pass over every frame, one frame per shot by eye, fresh-eyes reviewer, fixed gates.
12. **IP check and delivery.**

Details of every phase: `references/production-map.md`.

## Hard rules

- **Our code only in the frame.** No third-party renderers or DCC apps, no downloaded models, textures, mocap or
  stock footage. Python/numpy and Node are fine. Install packages only through the team's approved dependency
  channel.
- **Generated images are targets, never content.** Nothing from `refs/` is rendered, projected or sampled.
- **Renders run locally by default.** Proofs, animatic and finals render on the machine's own GPU. On laptops keep
  previews small (640×480, 32–64 spp), cap seconds per frame (`--max-seconds`), run one render process at a time
  and render finals in chunks (`--frames a-b`). Remote GPUs are optional, for speed only; see
  `references/rendering.md`.
- **Determinism.** Every random value comes from a seeded RNG. The same frame number must always produce the same
  scene, so any frame can be re-rendered alone and match its neighbours.
- **One frame = one pure function.** `sceneFor(i)` reads nothing from previous frames. Simulations are pre-baked to
  per-frame caches and read by frame index.
- **Units:** metres, Y up, characters face +Z, feet on y = 0.
- **Light has shape.** Key plus rim on every hero, real shadows and contact, no flat wash. See the light standard.
- **Time is the music.** Cuts, hits and reveals land on the bar map; the drop is the peak.
- **No IP.** Own characters, own designs, own or generated music, OFL fonts with their licence file.
- **Credentials come from environment variables only.** Never write keys, pod ids or host addresses into the
  project, logs that ship, or docs.
- **Cost discipline on rented GPUs (only if you use them).** Create pods only for a render, record them in a
  ledger, delete each pod as soon as its part is done and confirm the deletion.
- **Nothing ships without QA.** A film that has not passed the review in `references/qa.md` is not shown.

## Default format

1440×1080 (4:3) or as briefed, 24 fps, 15–30 s, H.264 `yuv420p` CRF 16–18 plus AAC 48 kHz, loudness about
−14 LUFS integrated, true peak ≤ −1 dBTP. Animatic: 640×480 (or 720×540) at 32–64 spp. Final: 1440×1080 at 192–1024 spp
depending on noise and the denoiser (sequences want enough spp that the denoiser polishes rather than reconstructs).

## Where to read more (load only what the current step needs)

| Read | When |
|---|---|
| `references/production-map.md` | Starting a film, or moving from one phase to the next. |
| `references/light-standard.md` | Lighting any shot, proof or test frame; judging a look pass. |
| `references/asset-contract.md` | Writing or reviewing an asset module, a rig, a material set or a proof render. |
| `references/shots-and-timeline.md` | Writing `film.mjs`, `story.mjs` or shot files; cameras; timing to the bar map; cutting music. |
| `references/rendering.md` | Any render: proofs, animatic, finals, re-renders, laptop settings; optional remote pods. |
| `references/qa.md` | Reviewing an animatic or a final; writing the review and fix list. |
| `references/ip-clean-delivery.md` | Choosing music and fonts, designing characters, and before delivery. |
| `references/briefing-agents.md` | Splitting work across sub-agents. |
| `engine/README.md` | Any engine API question: materials, lights, volumes, camera, render settings, limits. |
| `examples/felt-good-morning/` (repo) | Need a working pattern for an asset, a story function, a shot or a render job. |

## Roles

The lead owns story, look, edit, music timing and acceptance. Sub-agents get narrow, verifiable tasks: one asset,
one simulation, one shot to its styleframe. Nobody but the lead edits `BEATS.md`, `story.mjs` timing or the cut.

## Lessons the example taught

- Stills hide edit problems. Judge the animatic under music, not frames on their own.
- A same-angle cut with a small scale change reads as a mistake. Either change the angle and lens decisively or
  keep it one continuous shot.
- Keep the cause of a gag in a medium shot. If the action that triggers the joke is tiny in frame, the joke is lost.
- Geometry passes through geometry when nobody checks: solve contact points (beak on yarn, feet on ground) from the
  contact, not from the body root.
- Static openers lose the hook. Something must move in the first 0.5 s.
- A fresh reviewer with no context finds what the team no longer sees. Always run one.
