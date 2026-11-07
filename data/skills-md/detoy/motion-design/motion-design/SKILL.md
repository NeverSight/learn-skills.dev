---
name: motion-design
description: Turn a product, website, service, app, or brand into a top-tier short motion-design launch video. Use when the user wants a launch video, product reel, motion design, showreel, promo, kinetic type, UI morph, brag video, or /motion-reel. Accepts a URL, project folder, screenshots, logo, copy, reference frame, or brief. Builds a deterministic seek(t) composition, critiques its own frames, and delivers mp4 plus poster and share copy.
license: MIT
metadata:
  type: workflow
  version: "1.0"
  inspired-by: latent-spaces/brag and the Movez 12-step motion studio
---

# Motion Design

You are a motion-design studio, not a slideshow generator. The prompt is 10% of the video. The other 90% is the harness — inspect the source, write a director brief, build a deterministic `seek(t)` renderer, look at your own frames, and only then encode.

Default deliverable is a 15–25s launch film (sweet spot 18–22s) with soundtrack, poster frame, and share copy. Nothing on screen or in the mix that does not earn its place.

## Invocation

Parse natural language or flags.

| Option | Values | Default |
|---|---|---|
| input | URL, project dir, image paths, pasted copy | current project or ask |
| `--tone` | preset or freeform | inferred |
| `--format` | `landscape`, `vertical`, `square` | `landscape` |
| `--duration` | seconds | ~20 |
| `--fps` | 30 or 60 | 30 |
| `--no-music` | flag | music on |
| `--no-sfx` | flag | sfx on |
| `--voice` | flag | off |
| `--reference` | image/video path or URL | none |
| `--loop` | flag | off |

Tone presets: `default`, `polished`, `yc-parody`, `chaotic`, `deadpan`, `cinematic`, `app-store`. Freeform direction ("fake Series A launch from 2016") overrides the preset's voice while keeping its pacing table. Full definitions: [references/tones.md](references/tones.md)

If input is missing and the working directory is not a product, ask what to film.

## Hard bans (the mid look)

Do not ship any of these unless the user explicitly asked for a parody of them:

- Centered sentence on a gradient, fading in
- Generic SaaS copy ("streamline your workflow", "unlock your potential")
- Logo slam as the only ending idea
- Ken Burns pans across a flat landing-page screenshot
- CSS `ease-in-out` on everything, no mass, no overshoot
- A plain crossfade between two busy layouts (muddy double exposure)
- Invented metrics, fake testimonials, or claims not in the source
- Rendering without looking at stills first

Without a reference, models collapse to that default. Name a look or attach a frame.

## Pipeline (do not skip gates)

Work in `motion-output/` or, if that folder already exists, `motion-output-YYYY-MM-DD-HHmmss/`. Keep intermediates in `<output-dir>/work/`.

```
<output-dir>/
  reel.mp4
  reel.jpg
  share-copy.txt
  plan.md
  brief.md
  critique.md
  work/           composition, frames, stems, captures
```

### 1. Inspect the source

Read [references/inspect.md](references/inspect.md).

Gather identity, copy, real UI, and the product-in-use flow (entry → key action → result). Prefer the working product over the marketing page. Download logos, product shots, and fonts into `work/source/`.

If the user attached a reference frame or named a look, write `work/style-notes.md` — what to steal (palette, type, grain, pacing) and what not to steal (subject).

**Gate:** you can answer the inspect rubric in one pass.

### 2. Plan like a director

Read [references/plan.md](references/plan.md).

Write `<output-dir>/plan.md` (story, hook, beat sheet) and `<output-dir>/brief.md` (crew packet — logline, references, constraints, state list, deliverables).

Shape, unless tone says otherwise: Hook 2–3s → Reveal 2–4s → 2–3 highlights → Punchline/outro 2–4s.

**Gate:** scene durations sum to the target. Every readable line has a hold floor. At least one scene shows the real product doing a job.

### 3. Build the engine

Read [references/engine.md](references/engine.md) and [references/motion.md](references/motion.md).

Create `work/composition/index.html` plus `work/composition/motion.js`. The page must expose:

```js
window.seek(t)    // paint the exact frame at t seconds — pure, no timers
window.DURATION   // seconds
window.WIDTH
window.HEIGHT
```

Motion is closed-form springs (see `assets/motion.js`), not CSS transitions. Values that change target more than once use `track()` so frame 812 does not require simulating 0–811.

Reuse real markup, screenshots as textured UI chrome, brand colors, and source copy. Rebuild only what you cannot reuse.

Copy `assets/motion.js` into the composition. Copy `assets/player.html` only if you need the scrubber shell — do not keep its sample scenes.

### 4. Score the picture

Read [references/sound.md](references/sound.md).

If the user supplied a track, probe it and lock 1–3 strong cues. If not, synthesize a bed with `scripts/synth-bed.py` into `work/stems/bed.wav`. Write SFX as part of the same piece (same key, same room), not stickers on top.

Voiceover only when `--voice` is set. Do not narrate on-screen text.

### 5. Critique loop (non-negotiable)

Read [references/critique.md](references/critique.md).

Before the full encode, render stills at every scene midpoint **and** mid-transition with `scripts/render-frames.mjs --stills`. Look at them with the image reader. Score composition, type, contrast, overflow, product-truth, and motion clarity 1–10. Write the three worst problems into `<output-dir>/critique.md`, fix, re-still. Repeat until every category is 8+ or you have done 3 honest passes and logged why a leftover is acceptable.

A still pass that you did not look at does not count.

### 6. Render and deliver

```bash
node <skill-dir>/scripts/render-frames.mjs \
  --html <output-dir>/work/composition/index.html \
  --out <output-dir>/work/frames \
  --fps 30

# stitch + audio (see engine.md for the exact ffmpeg graph)
# then bake poster
bash <skill-dir>/scripts/bake-poster.sh \
  <output-dir>/work/reel-raw.mp4 \
  <output-dir>/reel.mp4 \
  <output-dir>/reel.jpg \
  <settled-timestamp>
```

`<skill-dir>` is the directory that contains this `SKILL.md`.

Poster rules: pick the strongest *settled* frame (type fully in, not mid-transition). Bake it as frame 0 of `reel.mp4` without adding duration.

Write `share-copy.txt` — 1–3 postable sentences, specific to this product, matching the tone. No "excited to share".

If the user asked for more than one aspect ratio, reflow the layout function and render each format. Do not crop a 16:9 master into 9:16.

Tell the user the output paths, the angle in one sentence, and offer a scene re-roll or a different tone.

## Creative laws

- **Short.** 15–25s. Cut before you decorate.
- **Clear to a stranger.** After one viewing they know what it is, who it is for, and how to get it.
- **The hook is everything.** Plan the first 2 seconds first.
- **Show the thing.** Real UI, real copy, real product-in-use. Rebuild only what you cannot reuse.
- **Specific.** Use this product's words. Ban generic SaaS language.
- **Readable.** Pace comes from motion and cuts. Readable type holds ~0.3s per word from the moment the whole line is settled (~0.8s for a 1–3 word label, ~1.2s min for a headline).
- **Alive.** Staggered entrances, simulated clicks, swipes, typing. Not static slides.
- **Every frozen frame postable.**
- **Funny earns its place.** Humor from the product's own absurdity, not from trying.

## Formats

| Format | Size | Use |
|---|---|---|
| landscape | 1920×1080 | default, X/LinkedIn/site |
| vertical | 1080×1920 | Reels, Shorts, TikTok, Stories |
| square | 1080×1080 | feed, avatar-adjacent |

Write scenes against a layout function (`layout.safe`, `layout.gutter`, type scale), not hardcoded pixels, so a second format is a reflow not a crop.

## Quality bar

A finished reel must have all of:

1. A hook that would stop a thumb
2. At least one shot of the real product (UI, mark, or in-use flow)
3. Brand-accurate color and type
4. Motion with mass (springs, not generic fades)
5. Readable type at the hold floor
6. Sound that feels scored, not pasted
7. A critique file proving you watched the frames
8. Poster + share copy that can ship as-is

If a pass fails that bar, do not present it as final.
