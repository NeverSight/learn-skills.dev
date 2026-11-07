---
name: painted-animation
description: Make hand-painted watercolour-and-ink cartoon videos (MP4) with code — p5.js + p5.brush rendered frame by frame in headless Chrome, encoded with ffmpeg — starring Clawd or any character. Use when the user asks to make an animation, animated short, cartoon, music video, lyric video, animated GIF/loop or "a video of Clawd…", or mentions the PDoomVideo / ClaudeAnimationBase approach. Covers storyboarding, the engine API, music and LRC lyric sync, cloud-friendly preview review, and choosing local or cloud rendering for the final video.
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

For a music video or anything longer than ~20 s, also read [references/music-video.md](references/music-video.md).

For every music video, complete this intake before storyboarding or scene implementation:

1. Ask the user to provide both the song audio file and its `.lrc` lyric file. Do not invent, transcribe or approximate missing lyrics when an LRC is expected.
2. Always ask for the creative direction, even if the user has already mentioned part of it. Ask it as **one natural-language question in one message**, covering the desired story and overall feeling plus any recurring visual idea or content to avoid. Do not split it into separate questions, fields, a checklist or a five-part form. Tell the user they may answer in one sentence or leave it blank. Example: "What kind of story and overall feeling should this MV have, and is there any recurring image you want included or anything you want avoided? You can leave this blank if you have no preference."
3. Confirm the received files and summarize the creative direction inferred from the single answer. Internally extract story, emotion, atmosphere / imagery, visual motif and content to avoid; do not ask the user to answer those five categories separately. Treat a blank answer as "no preference", not as missing input, and propose an appropriate interpretation during storyboarding. If the audio or LRC file is missing, pause the music-video workflow and request it.
4. Measure the tempo with `scripts/beat_grid.py`; lyric lines are usually faster than you'd guess. Treat the provided audio and LRC as the timing source of truth.

### 1. Storyboard before code

Write `STORYBOARD.md` in the project (format in the guide: logline, world + palette arc, motif, the character's emotion arc, then shots with **reads** — the timed list of what the viewer must understand). Worked example: [examples/xiaozhen/](examples/xiaozhen/) (a 31 s lyric video: storyboard and full scene code).

For a music video, turn the user's story and mood into a coherent visual narrative and emotional arc rather than illustrating each lyric literally. Show the storyboard to the user and let them react before building, unless they said to just go ahead.

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

Contact sheets, stills, short strips and other few-frame previews may be rendered and reviewed in the current cloud environment. Keep these preview renders deliberately small and targeted; they are for visual validation, not a substitute for rendering the whole video.

### 4. Render the video

Never start a complete render directly. After preview review is finished, tell the user that complete cloud rendering can be very slow and ask explicitly whether they want the final video rendered locally or in the cloud. Wait for their answer; storyboard approval, preview approval, or a previous general instruction to proceed is not render authorization.

- If the user chooses local rendering, cloud full rendering is prohibited. Do not start the full sequence in the cloud unless the user later explicitly changes their choice. Finish the validated project files, ask for the local operating system if unknown, and provide the exact prerequisite, `npm install`, frame-render and encode commands for that platform. Keep preview images available so the user knows what was approved.
- If the user chooses cloud rendering, confirm the expected duration, frame count and likely cost/time, then proceed with the resumable multi-worker render.
- If the user does not answer or gives an ambiguous answer, do not run a complete render. Ask again for an explicit local-or-cloud choice.

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
