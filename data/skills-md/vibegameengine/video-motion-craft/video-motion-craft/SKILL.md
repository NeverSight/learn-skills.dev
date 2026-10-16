---
name: video-motion-craft
description: Create and edit video with cinematic motion — Remotion (React video) for motion graphics, reels, intros, promos, titles and game trailers, plus FFmpeg/Whisper for editing real footage (trim, jump-cut, captions, overlays, speed). Load ALWAYS before the first line of video code. Triggers — "make a video", "edit this video", "reel", "Shorts/TikTok", "intro", "logo animation", "titles", "captions", "promo video", "cinematic", "sync to music", "hit the beat", "the video looks cheap/generic/AI-made", "game trailer", "store/showcase video", "gameplay capture", Remotion, ffmpeg, motion graphics, video render.
---

# video-motion-craft

One skill for two jobs that always travel together in real work:

- **Build** a video from code — motion graphics, reels, intros, promos, titles (Remotion).
- **Edit** real footage — trimming, silence removal, captions, overlays, speed (FFmpeg + Whisper).

The bottleneck is **not the code, it is motion design craft**. An uncalibrated model
produces linear easing, opacity-only fades, simultaneous entrances, flat fills and
silence. That is the "cheap AI video" look. The whole point of this skill is to stop
that from happening.

## Picking the route

| What is asked | Route |
|---|---|
| Video from scratch: intro, reel, promo, titles, logo animation | **Remotion** → `references/remotion-patterns.md` |
| Existing video: trim, cut silence, burn captions/text, change speed | **FFmpeg** → `references/ffmpeg-editing.md` |
| Footage that needs packaging: intro + grade + grain + captions on top | **Hybrid** — footage as an `<OffthreadVideo>` layer inside Remotion |
| Game trailer, store showcase, app screen recording | **`references/game-capture.md` first** — how to get the material, then Remotion |
| A video cut to a specific track | **`references/beat-sync.md` first**, everything else after |

Mixed case ("edit this screencast and give it an intro") — an FFmpeg pass over the
footage first, then Remotion on top of the finished clip.

## Non-negotiable rules

They apply to **every** composition. Break one deliberately if you must, but every
break gets written into the project README: which rule, and why.

1. **Linear easing does not exist.** Every `interpolate()` gets a curve, every
   entrance prefers `spring()`. Always `extrapolateLeft/Right: "clamp"` — both.
2. **An entrance animates 2–3 properties at once** (opacity + translateY + scale).
   A lone fade is forbidden.
3. **Stagger everything.** Lists, words, cards, rays: 3–6 frames. Nothing enters at
   the same time as anything else.
4. **Exits exist and are faster than entrances** (~10 frames against ~20).
5. **Five layers in every scene**, bottom to top: background mesh → assets →
   graphics/type → colour grade → grain + vignette. A flat fill is not a background.
6. **Every still gets Ken Burns** (scale 1→1.08 + pan). Video is `<OffthreadVideo>`,
   never `<Video>`.
7. **Idle things breathe**: anything on screen longer than 2s gets sine-wave
   micro-motion.
8. **Timing derives from `fps`** through `useVideoConfig()`. No bare frame numbers.
9. **One `theme.ts` per project** (colours, easings, spring presets, fonts). A hex
   code or an easing curve inside a component is a mistake.
10. **Render → extract frames → LOOK at them → fix → re-render.** An unverified
    render is not delivered. This is a pipeline step, not a suggestion.
11. **Deterministic render**: `Date.now()` and `Math.random()` are banned; any
    pseudo-randomness uses a fixed seed (mulberry32, seed derived from the index).
    Otherwise frames are not reproducible and checking them proves nothing.
12. **Material from a game or app is captured clean** — without its interface — and
    the interface and text go on as separate layers in the edit. A HUD baked into
    the recording means re-shooting for every language and every timing change.
    Details and exceptions in `references/game-capture.md`.

## Workflow

### 0. Frame the job
Decide: duration, fps (30 by default; 60 only for heavy fast motion), dimensions
(1080×1920 reels/Shorts, 1920×1080 landscape), which assets already exist (images,
footage, audio, logo), whether this is a new project or an edit to an existing one,
**and how many languages the video is needed in**.

Languages are settled here, not at the end: they decide whether to capture a clean
plate (rule 12) and whether to parameterise the composition by locale. Finding out
about a second language after the edit means rebuilding the material.

Editing an existing project: read `src/` in full first, find the theme (or create
one), **fix the violations of the rules above** — and only then add anything new.

**If music is already chosen — stop, read `references/beat-sync.md` first.** The beat
grid has to pass acceptance before the storyboard exists. Boarding first and
stretching it onto the track afterwards is a guaranteed redo.

### 1. Setup
```bash
npm install remotion @remotion/cli react react-dom
# as needed: @remotion/transitions @remotion/motion-blur @remotion/google-fonts @remotion/captions
```
Copy `assets/theme.ts` into `src/theme.ts` and adjust the palette to the brand.
Structure: `src/index.ts` (registerRoot) → `src/Root.tsx` (Composition) →
`src/scenes/*.tsx` → `src/components/*.tsx`. User assets go in `public/`, loaded
through `staticFile()`.

No audio? That is **not** a reason to ship silence: `node scripts/gen-sfx.mjs <dir>`
synthesises a minimal WAV kit (whoosh, pop, tick, bass, pad) with zero downloads.
Without an argument it writes to `<cwd>/public/sfx`.

### 2. Storyboard
Write the shot list BEFORE the code: order, duration, what is in frame, which
technique, which caption, which transition, which SFX. One technique (fly-in /
stacking / page turn) is **the hero of exactly one shot in the whole video**. A
repeated shot or a repeated tagline gets cut.

The vocabulary to choose from: `references/shot-vocabulary.md`.
Rhythm and the energy curve: `references/motion-laws.md`.

### 3. Build
Copy components from `references/remotion-patterns.md` (BgMesh, Grade, Grain,
Vignette, KenBurns, WordReveal, Stagger, Counter, Spark, transitions, parallax,
captions). Colour, typography and composition rules: `references/motion-laws.md`.

Scene rhythm: **HIT → hold (15–20 still frames) → build → HIT.** Something must move
in the first 15 frames. Never more than 90 frames without a new visual element.

### 4. Sound
`references/sound-design.md`. In short: sound is done **after** the picture is
locked; any change to a shot's duration means rebuilding the whole SFX table. Cues
are pinned relative to the shot start (`SHOTS.x.from + offset`), never as bare numbers.

### 5. Render
```bash
npx remotion render src/index.ts <CompId> out/video.mp4 --codec h264 --crf 16 --overwrite
```
Forgetting `--overwrite` and then inspecting the stale file is a classic hour lost.

### 6. Acceptance (never skipped)
Extract frames and **look at every one**:
```bash
for f in 15 45 90 150; do
  npx remotion still src/index.ts <CompId> out/check_$f.png --frame $f --overwrite
done
```
If a system ffmpeg is available, extracting from the finished mp4 additionally
verifies the encode: `ffmpeg -v error -ss 1.5 -i out/video.mp4 -frames:v 1 check.png`.

Then walk `references/review-checklist.md` item by item, with frame numbers as
evidence. **The first review is never handed to the user** — the author's eye is
tired, and "looks fine overall" without frame numbers is not a review.

## What to read when

| Moment | File |
|---|---|
| Before the storyboard and on every rhythm change | `references/motion-laws.md` |
| Before the first line of a component | `references/remotion-patterns.md` |
| Music chosen up front / cutting to the beat | `references/beat-sync.md` |
| Placing SFX, mixing, riser→impact | `references/sound-design.md` |
| Editing real footage | `references/ffmpeg-editing.md` |
| Capturing material from a game or app | `references/game-capture.md` |
| Choosing the technique for a shot | `references/shot-vocabulary.md` |
| Before delivery | `references/review-checklist.md` |

## Failure modes to actively avoid

- **Emoji as icons.** They render as full-colour platform glyphs, ignore the palette,
  silently break the one-hero-colour rule and sink into the background (an orange
  mascot on an orange tile is invisible). Draw glyphs in CSS/SVG in theme colours,
  or verify every emoji against the extracted frames.
- **`gap`/`margin` in `em` next to large type.** `em` resolves against the PARENT
  font-size (usually 16px), not the text size — next to a 150px face the gap comes
  out near zero. In flex containers around big type, px only.
- **One giant component** instead of reusable pieces sharing a theme.
- **Composition `durationInFrames` not matching the scene content** → dead air.
- **A system font in a headline.** Always load a display face through
  `@remotion/google-fonts` or `@font-face` + `staticFile`.
- **Describing the result in words** instead of rendering it and looking.

## Sources

Assembled from four open skills, keeping their case-law intact:
[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) (aesthetic rules,
beat sync, sound), [claude-remotion-skill](https://github.com/haidrrrry/claude-remotion-skill)
(patterns, theme, checklist), [video-editing-skill](https://github.com/6missedcalls/video-editing-skill)
(ffmpeg scripts), [claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit)
(pipeline structure). Per-file attribution in `THIRD-PARTY-NOTICES.md`.
