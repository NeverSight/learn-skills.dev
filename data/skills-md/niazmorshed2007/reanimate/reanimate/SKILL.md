---
name: reanimate
description: Clone a section, widget, page or animation from any reference (a live website URL, a screen recording, an mp4/mov/webm, a gif, a Lottie file, a prototype export) frame by frame into the user's own codebase, then record the clone and verify it against the reference frame by frame, iterating until timing, easing, sequence and layout match. Use whenever the user wants to clone, copy, replicate, recreate, reverse-engineer, port or "steal" a hero, section, widget, marquee, carousel, hover effect, page transition, loader, scroll animation or interaction from a site or video, says "make it look/feel/move like this", "same animation as", "match this exactly", or hands over a gif/video and asks to build it, including when they also want to add their own content, colours or extra features on top, or only want part of the reference (one section, one widget, a few seconds). Covers canvas, WebGL, WebGPU and three.js / 3D scenes (shaders, particles, globes, glTF models) as well as CSS and JS motion. Pixel-level matching of fonts, colours and spacing is done only when they ask for it.
---

# reanimate

Rebuild what the user points at so that it moves the way the reference moves, prove it with a frame-by-frame comparison, and keep going until the comparison passes. The deliverable is code in the user's project plus evidence (numbers and side-by-side sheets), never "it looks about right".

## What "done" means

Pick the fidelity level from the user's words and state it in the first message; it decides what you verify.

| Level | When | Must match | May differ |
|---|---|---|---|
| **motion-faithful** (default) | "clone this animation", "make ours feel like theirs", "same hero as X but our copy" | trigger, sequence and order, stagger, timing of every step (±80 ms), easing family, direction and distance of movement relative to the element size, layout proportions | copy, colours, fonts, images, brand details |
| **pixel-faithful** | "match it exactly", "pixel-perfect", "details should match", "1:1" | everything above plus fonts, sizes, colours, spacing, radii, shadows, assets; mean frame mismatch ≤ 2 % | nothing the user did not ask to change |
| **mixed** | "clone X and add Y", "like theirs but with our pricing tiers" | the cloned parts at one of the levels above | the additions, which you describe and show but verify only for not breaking the cloned motion |

The user can narrow the target to one section, one widget, one page, or a time range of a video ("the first 3 seconds", "0:12 to 0:15"). Clone exactly that; do not pull in the rest of the page.

## Workflow

Everything below lives in `.reanimate/<name>/` inside the user's project (add it to `.gitignore` unless they want the evidence committed). Keep each round's artefacts; they are the proof.

### 0. Scope

Write three lines at the top of `.reanimate/<name>/spec.md` before any capture:

- **Target**: what to clone, as precisely as the user said it (URL + selector / time range / "the toggle in the gif").
- **Destination**: where the code goes and in what stack (read `package.json`, existing components and the animation library already in use; match it rather than introducing a new one).
- **Fidelity**: motion-faithful, pixel-faithful or mixed, plus the list of additions for mixed.

Infer what you can from the request and the repo. Ask only when two readings lead to different work (for instance "the hero" on a page with two candidate sections). When a reference is a login-walled page or a YouTube/Loom link you cannot download here, ask the user for a screen recording and continue with everything else meanwhile.

### 1. Setup

`<skill>` below is the directory this SKILL.md lives in. Scripts need [Bun](https://bun.sh); the first run downloads Playwright's Chromium and a static ffmpeg (about 250 MB).

```bash
bash <skill>/scripts/setup.sh      # installs playwright, ffmpeg, pixelmatch once; prints "ready"
```

All scripts are run with `bun <skill>/scripts/<name>.ts --help`. They are deterministic and share one rule: capture the reference and the clone with the **same** viewport, selector crop, trigger, duration and fps, otherwise the comparison measures your setup instead of your work.

### 2. Capture the reference

Read `references/capture.md` for the recipe for your source type. In short:

- **Website**: `capture.ts --url … --out ref --selector <section> --trigger load|scroll|hover|click|none --duration … --track "<moving elements>"`. You get `video.webm`, `frames/`, `inspect.json` (declared animations, keyframes, computed styles, fonts, detected libraries) and `track.json` (per animation frame position, size, opacity, transform of each tracked element). For CSS/WAAPI motion `inspect.json` often contains the exact durations, delays and easings: use them, it beats estimating.
- **Video or gif**: `frames.ts --in file --out ref/frames --fps 10..30 --start … --end … --crop …`. Probe first with `--probe`, then view a few frames to find the crop of the widget you are cloning.
- **Canvas, WebGL, WebGPU, 3D** (`inspect.json › canvases` shows one, or the page uses three.js, Pixi, Babylon, Spline…): add `--clock virtual --gl --assets` to the capture and read `gl/summary.md` (`gl.ts summary <out>`). You get the shader sources, every constant uniform, the scene graph, the render passes, the textures and models, and each animated uniform or object property as a channel in `gl-track.json`. The virtual clock makes every frame exact and every capture identical, random particles included. Read `references/webgl.md`.
- **Lottie / Rive / prototype export**: the file is the spec; read it, do not re-derive it from pixels.

Then build labelled sheets and look at them: `sheet.ts filmstrip --frames ref/frames --out ref/sheets`. Read every sheet with the image viewer. This is the frame-by-frame inspection the user asked for; do not skip it or sample only the first sheet.

### 3. Write the motion spec

Fill `spec.md` using the template in `references/analysis.md`. One row per element per property: trigger, start time, duration, delay or stagger, from → to, easing, notes. Get the numbers from, in order of preference: `inspect.json` animations and keyframes → `easing.ts` on `track.json`, or on `gl-track.json --channel` for canvas → reading frames (first frame where it changes, last frame where it changes, overshoot or not). Also note the static facts the motion depends on: element sizes and positions, z-order, overflow clipping, transform origins, and for pixel-faithful work fonts, colours, spacing and assets.

The spec is the contract between the reference and the clone. Every row becomes a check in step 5. If a row has a "?" you have not finished reading the frames.

### 4. Build

Implement in the user's stack following `references/implementation.md` (easing tables, stagger math, scroll and hover triggers, reduced motion). Keep the DOM structure close to the reference's role structure so the tracked selectors have equivalents. For mixed work, put additions in clearly separate components or blocks and mention them in `spec.md` under "Additions".

Give the clone a way to be captured the same way as the reference: a route or a static page that renders the component at the reference viewport with the same trigger. A dev server is fine (`capture.ts --url http://localhost:5173/…`); a standalone HTML file also works.

### 5. Verify, fix, repeat

Capture the clone with the exact command used for the reference, changing only `--url` and `--out clone-N`, then:

```bash
bun <skill>/scripts/compare.ts --ref ref/frames --clone clone-N/frames --out compare-N
bun <skill>/scripts/sheet.ts compare --ref ref/frames --clone clone-N/frames --diff compare-N/diff --out compare-N/sheets --every 2
bun <skill>/scripts/easing.ts --track clone-N/track.json --selector "<el>" --prop <translateY|opacity|…> --compare-track ref/track.json
```

For canvas work, also run `gl.ts compare --ref ref --clone clone-N`, which checks canvas settings, draw structure and every animated channel.

Read `references/verify.md` for how to read the report, the pass criteria for each fidelity level and the fixes that each kind of failure usually needs. Look at the compare sheets yourself, every round; the numbers tell you that something is off, the sheets tell you what.

Loop until every spec row passes. Each round: change the smallest thing the evidence points at, re-capture, re-compare. Expect 2 to 5 rounds. If after 5 rounds a row still fails, stop and report it with its numbers and the reason (missing font, a shader or model the user may not copy, a physics spring you approximated), do not quietly lower the threshold or drop the row.

### 6. Report

The final message must stand alone:

- Fidelity level and what was cloned, what was added.
- Where the code is (files) and how to trigger the motion.
- A short table of the last compare round: timing error, mean mismatch, easing match per key element, pass/fail.
- Paths to the final compare sheets, embedded as images when the environment shows them.
- Residual deviations, each with a number and a reason.

## Pitfalls that waste rounds

- Different viewport or crop between reference and clone: fix the capture before touching code.
- Judging from the first frame and the last frame only: the easing lives in the middle frames; read the sheets.
- Fonts: a different fallback font changes every frame's pixels. For pixel-faithful work load the same font (from `inspect.json` fonts) before judging mismatch; for motion-faithful work ignore text pixels and read the timing columns.
- Reference recorded on a loaded page vs clone captured cold: use `--wait-before`, or `--trigger none` with a `--pre-js` that restarts the animation, so both start from rest.
- Scroll-driven motion: it is a function of scroll position, not time. Capture both with the same `--scroll-steps` and `--scroll-ms`, and compare per scroll position (the track's `scrollY`), not per second.
- JS libraries (GSAP, Framer Motion springs): `--playback-rate` does not slow them. Use `track.json` and `easing.ts` (it reports overshoot and "spring-like") and tune spring parameters by the overshoot and settle time.
- Videos of someone else's screen have a cursor, a browser chrome and compression noise: crop them out and raise `--pixel-threshold` a little (0.15) rather than chasing noise.
- Canvas and WebGL captured on the real clock: frames drop in software GL and random content differs on every load, so the comparison measures the machine. Capture both sides with `--clock virtual` and the same `--seed`.
- Rebuilding a shader from screenshots: the trace already has its source and every constant. Read `gl/shaders/` and the fixed uniforms before writing GLSL.
