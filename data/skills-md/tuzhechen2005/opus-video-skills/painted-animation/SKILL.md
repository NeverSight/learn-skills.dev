---
name: painted-animation
description: Make hand-painted watercolour-and-ink cartoon videos (MP4) with code — p5.js + p5.brush rendered frame by frame in headless Chrome, encoded with ffmpeg — starring Clawd or any character. Use when the user asks to make an animation, animated short, cartoon, music video, lyric video, animated GIF/loop or "a video of Clawd…", or mentions the PDoomVideo / ClaudeAnimationBase approach. Covers storyboarding, the engine API, the render-and-look review loop, music/lyric sync and splitting long videos across subagents.
---

# Painted animation

A method for making short cartoons entirely in code, distilled from [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) (a 156 s music video painted by Claude Opus) and its generalised kit [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) (MIT), which is bundled here as `template/`.

**How it works:** every frame is a pure function of time `t`. `studio.html` loads p5.js + p5.brush and your scene files; each shot paints the whole 1920×1080 frame with watercolour fills and boiling ink lines. `render.mjs` drives headless Chrome to render contact sheets for review, or every frame in parallel, and ffmpeg encodes the MP4 (with audio if given).

## Workflow

### 0. Scaffold

```bash
bash ~/.claude/skills/painted-animation/scripts/new_project.sh <project-dir>        # add --keep-demo to keep the example scene hooked up
```

This copies the template, unhooks the demo scene, runs `npm install` and checks node / ffmpeg / Chrome. Then **read `<project-dir>/ANIMATION_GUIDE.md` in full** before designing anything: it holds the rules, the animation principles and the complete engine / Clawd API. Look at `docs/emotions.jpg` and `docs/views.jpg` (the model sheets) with the Read tool.

For a music video or anything longer than ~20 s, also read [references/music-video.md](references/music-video.md). For a lyric video, ask for the song file and an LRC first, and measure the tempo with `scripts/beat_grid.py`: lines are usually faster than you'd guess.

### 1. Storyboard before code

Write `STORYBOARD.md` in the project (format in the guide: logline, world + palette arc, motif, the character's emotion arc, then shots with **reads** — the timed list of what the viewer must understand). Worked example: [examples/xiaozhen/](examples/xiaozhen/) (a 31 s lyric video: storyboard and full scene code).

Show the storyboard to the user and let them react before building, unless they said to just go ahead.

### 2. Build shot by shot

- Set `duration`, `bpm`, `offset` (and `audio`) in `src/config.js`.
- One IIFE-wrapped file per scene/chapter in `src/scenes/`, ending with `shots([[t0, fn], ...])`; add its `<script>` to `studio.html`.
- Block key poses first, check them as stills, then add the motion between them.

### 3. Render and look — every shot, several times

You can't see motion by reading code. From the project dir:

```bash
node render.mjs --sheet=0.1,0.8,1.6,2.4 --cols=4 --w=480 --out=out/check/a.jpg        # key frames
node render.mjs --strip=2.1:2.6 --out=out/check/strip.jpg                             # every frame of a moment
node render.mjs --sheet=2.3 --crop=760,420,500,400 --w=500 --out=out/check/face.jpg   # full-res detail
```

Open each image with Read and actually check it against the guide's review list: event clear? character big enough? reads timed so a first-time viewer gets them? anticipation / follow-through, no snaps? feet and held props touching? transitions at every seam? no text, no 3D, no pure black/white, no muddy glows? Fix and look again. Budget: ≥ 1 sheet per shot, a strip per key motion and transition, a crop per story-carrying face.

### 4. Render the video

```bash
node render.mjs --clip --out=out/video.mp4                                   # short videos, one worker
node render.mjs --frames --workers=4 && node render.mjs --encode --out=out/video.mp4 [--audio=assets/song.mp3]   # long ones, parallel + resumable
```

Report the output path, length and ms/frame. Offer `open out/video.mp4`.

## The rules that matter most

These are the guide's rules condensed; the guide is authoritative.

1. **Handmade medium.** Only `paint()` / `inkLine()` (p5.brush) — never plain p5 `rect`/`ellipse`/`fill`. Flat 2D only: turns go through drawn key views (`turn()`, `spinView()`), never 3D projection. Light via `glow()` (additive), because pigment-mixing makes yellow-over-blue go green.
2. **No text.** No captions, labels, signs or word bubbles; show it instead. Reactions are painted emotes (`!`, sweat, hearts…). The one exception is karaoke in a lyric video, and at most a few big SFX.
3. **Something happens in every shot** — an event, cause → reaction, set-ups that pay off.
4. **Time for the viewer.** List each shot's reads; one read at a time; fast actions, held meanings; lead the eye; the reads set the shot length. This is where generated animation fails most.
5. **Alive.** Nothing is still (idles from `feel()`, drifting cameras, boil); faces change through `emotions()` never by swapping; the character is big (medium shot u≈20–28, close-up 40–70); everything rides the beat.
6. **Transitions at every seam**, chosen to fit the story (brush wipe, iris / shaped iris, whip pan, match cut, cut on action, camera carry-through).
7. **One piece.** One world, a colour arc, an emotional thread, linked scenes, an ending that rhymes with the opening.

## Engine gotchas

- **Pure functions of `t`.** Frames render in parallel and out of order: no state across frames, no `Math.random()`, no frame-by-frame physics. `hash(i)` for stable randomness, `jit()` for boil.
- **`boilSeed(key)`** before each separate background element/prop, or a moving thing makes everything drawn after it re-boil every frame (jitter).
- **Don't name globals after p5's.** p5 defines `line`, `OVERLAY`, `text`, `color`, `scale`, … as globals; a top-level `function line()` fails with `Cannot redefine property` and the page never becomes ready (the renderer times out). Keep helpers inside the scene IIFE or give them distinct names.
- **Layering in doorways, windows and screens:** draw what's inside, then paint the surrounding wall/frame back over it, so nothing wider than the opening shows outside it (the train's `inDoor` + door jambs, the TV bezel pieces).
- A `NaN` in a point list throws `Failed to construct 'OffscreenCanvas'` — guard degenerate geometry.
- Under camera zoom ≳ 2, huge shapes lose outlines; outline weight scales with zoom, so scale `sw` down in close-ups.
- Cost = number of fills and strokes. Aim for ≤ ~1.5–2.5 s/frame (the log prints ms/frame). Prefer fewer, bigger shapes. On machines without a real GPU, watercolour fills are slow — consider fewer `fill` shapes, or `--soft-gl` as a last resort.
- macOS: the renderer uses `--use-angle=metal` and finds `/Applications/Google Chrome.app` automatically; otherwise pass `--chrome=<path>`.

## Adapting

- Clawd is the default star, not a requirement. New characters, props and emotions are drawn with the same tools (`paint`, `ribbon`, `through`, `glow`) and kept on-model across shots; new emotions go in `EMO` in `src/clawd.js`.
- `src/karaoke.js` (template) adds word-by-word karaoke for lyric videos via the `window.overlayHook` hook in `core.js`.
- `LOOPS.name = t => {...}; LOOPS.name.len = 4;` + `node render.mjs --loop=name --png` makes a seamless loop for GIFs (`ffmpeg -i out/loop_name/f%04d.png …`).
- Higher reasoning effort tends to give more extravagant, detailed scenes.
