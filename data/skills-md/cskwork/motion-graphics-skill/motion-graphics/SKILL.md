---
name: motion-graphics
description: Make code-driven motion-graphics videos rendered from HTML, frame-accurate and reproducible. Formats - product launch or feature-announcement video built from real captures of the user's running app (Apple/Google keynote style, SaaS launches on X), and vertical shorts for YouTube Shorts, Reels, or TikTok (hook-first, loopable). Use when asked for a launch video, promo, app trailer, Shorts, or any motion-graphics video.
---

# motion-graphics

A video is one HTML page whose every pixel is a pure function of time `t`, rendered frame by frame in headless Chromium and encoded with ffmpeg. The bar is a senior motion designer's showreel, never a slideshow.

## 1. Pick the format

| Request | Read |
| --- | --- |
| Launch, promo, commercial, feature reel, app trailer for a real product | [formats/launch-video.md](formats/launch-video.md) |
| Shorts, Reels, TikTok, vertical explainer or story | [formats/shorts.md](formats/shorts.md) |

Follow the format file for the brief, the content steps, and the beat structure. It hands back here for the build. Also read [references/pitfalls.md](references/pitfalls.md) before writing the composition.

**Fresh concept every run.** Each video gets its own idea, script, and look. When the user says not to look at past work, leave earlier videos and compositions in the workspace unopened.

## 2. Work folder

Make `<slug>-<YYYYMMDD>/` where the user wants it (default: the current directory):

```
brief.md          parameters from the format's brief table
beats.md          the beat sheet (time, copy, asset, move, transition, accent hit)
assets/           captures, images, fonts, audio
assets/manifest.md  one line per asset file: source, license or "captured from <surface>", what it shows
motion.html       the composition
motion.json       {"size": [W, H], "fps": 60, "duration": 30, "stills": [beat times], "captions": []}
engine/           copied from this skill's engine/
out/              stills, renders, contact sheet
```

Set up the engine once per folder:

```bash
cp -R <this-skill>/engine engine && (cd engine && npm install && npx playwright install chromium)
```

## 3. Compose

`motion.html` loads `engine/runtime.css` and `engine/runtime.js`, builds its DOM, registers scenes, then calls `MG.ready()`.

| Helper | Use |
| --- | --- |
| `MG.scene(start, end, fn, el)` | `fn(local, t, dur)` runs while `start <= t < end`; `el` is hidden outside. Set every animated property on every call. |
| `MG.always(fn)` | Runs every frame: backgrounds, grain, progress bars. |
| `MG.prog(t, a, b, ease)` | Eased 0..1 progress. Eases: `MG.ease.*` (linear, in/out/inOut Quad, Cubic, Quart, Expo, inBack, outBack, outElastic, outBounce) or any function. |
| `MG.tween(t, [[t0, v0], [t1, v1, ease], …])` | Keyframes; values may be arrays. |
| `MG.spring(t, {stiffness, damping})` | Physical 0 → 1 with overshoot. |
| `MG.split(el, "grapheme" \| "word")` | Per-letter or per-word spans (Korean-safe). |
| `MG.set(el, {x, y, s, sx, sy, r, o, blur, ...css})` | One call per element per frame. |
| `MG.clip(videoEl, start, rate)` | Plays a screen recording frame-accurately from `start`. |
| `MG.rng(seed)`, `MG.noise(x, seed)` | Deterministic randomness and wobble. |
| `MG.fmt(n, {decimals})` | Locale number formatting for counters. |
| `MG.captions()` | Draws `motion.json` captions above the bottom UI block. |

Determinism: no `Date`, `performance.now()`, `requestAnimationFrame`, or `Math.random` in render logic. CSS `@keyframes` are allowed; the runtime pauses them at `t`, so time them with `animation-delay`. Use only fonts and images listed in the manifest.

Preview a frame: `open "motion.html?w=1920&h=1080&t=3.2&guides=1"` (guides show safe zones). Real-time: `?play=1`. Captions show only in renders.

## 4. Craft bar

- **Frame 0 is already moving.** No fade from black, no logo intro.
- Something meaningful changes every 0.8–2 s: layout, scale, colour, number, or camera.
- Entrances use springs or ease-out-expo with slight overshoot; 30–60 ms staggers; linear only for tickers.
- Motion blur only during fast moves; a slow push (scale 1 → 1.04) on held shots; parallax across 2–3 depth layers.
- One background family, one text colour, one accent. Add grain or gradient noise so flat fills do not band after upload.
- Copy stays on screen long enough to read twice; key text stays inside the safe zones.
- Beats land on sound: a whoosh, hit, or music beat at each change.

## 5. Render

```bash
node engine/render.mjs --html motion.html --config motion.json --stills <t1,t2,...> --stills-dir out/stills
node engine/render.mjs --html motion.html --config motion.json --out out/video.mp4 --workers 4
```

Settle the layout on stills first: one per beat, one inside every tween, one at every spring's overshoot peak. Run one full render at a time (about 10 minutes for 25 s at 1080p60 with 4 workers).

## 6. Audio

Use only music and SFX listed in the manifest with a license that allows the use, or files the user supplies. Without them, deliver silent and say so. Mix cues, then mux:

```bash
ffmpeg -i music.wav -i whoosh.wav -filter_complex \
  "[0]volume=-16dB[m];[1]adelay=1200|1200,volume=-8dB[a];[m][a]amix=inputs=2:normalize=0[out]" -map "[out]" out/mix.wav
ffmpeg -i out/video.mp4 -i out/mix.wav -map 0:v -map 1:a -c:v copy \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 256k -shortest -movflags +faststart out/final.mp4
ffmpeg -i out/final.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^ +(I|Peak):"
```

Target about −14 LUFS integrated and true peak at or below −1 dBFS. SFX sit about −6 to −14 dB, music −14 to −18 dB. Music under on-screen text is instrumental.

## 7. QA

1. `ffprobe` duration, size, and fps match the brief.
2. Contact sheet: `ffmpeg -i out/final.mp4 -vf "fps=2,scale=360:-1,tile=10x6" -frames:v 1 out/contact.png`. View it and a full-size frame at every beat change (`ffmpeg -ss <t> -i out/final.mp4 -frames:v 1 out/check-<t>.png`).
3. Every frame: nothing clipped at the edges, no blank or half-faded frames, no leftover guides, no typos or placeholder text, nothing static longer than 2 s.
4. The format file's own checks.

Fix and re-render until every check passes. Add any new lesson to `references/pitfalls.md` in the skill as `date · video · lesson`.

## Deliver

Report the final MP4 path, length, size and fps, what it shows, audio status with credits needed, and the re-render commands. Keep the work folder. Upload or post only when the user asks.
