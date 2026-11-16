---
name: animation-reverse-engineering
description: Reverse-engineer any motion reference (a video from X/Twitter, Dribbble, a screen recording, a GIF) into production animation code through frame-level dissection. Use when the user shares a video/URL and says "implement this animation", "recreate this motion", "port this interaction", "how does this animate", "clone this effect", or wants to study how a reference moves before building it. Covers both timeline choreography (entrances, text sweeps, staggers) and interaction-driven motion (scrubbers, sliders, drag-driven scenes). Also fires when the user asks where to find good animation references or inspiration — it suggests curated sites and X accounts to hunt, then reverse-engineers whatever they bring back.
---

# Animation Reverse-Engineering → Production Port

Turn a motion reference into faithful production code via a measured, frame-level
pipeline instead of eyeballing. **Eyeballing a video at 1× lies about easing,
stagger order, overlap, and timing** — always dissect first.

```
acquire → overview → dissect → analyse → (prototype) → port → verify → document
```

## Phase 0 — Classify the animation

Before anything, decide which species you're studying. It changes the analysis
checklist and the port architecture:

| Species | Driven by | Examples | Port shape |
| --- | --- | --- | --- |
| **Timeline choreography** | Time (mount, trigger) | Page entrances, text sweeps, staggered lists, modals | Keyframes, springs, delays, `AnimatePresence` |
| **Interaction-driven** | User input (drag, scroll, hover) | Scrubbers, sliders, pull-to-refresh, scroll scenes | One progress value → property mappings + derived discrete state |

Hybrids exist (an interaction that *triggers* timelines — e.g. release-to-reset
rewinds). Classify each layer separately.

## Phase 0.5 — No reference yet? Help the user discover one

If the user wants a great animation but has no reference link, don't invent
motion from scratch — send them hunting and offer this shortlist (full list,
search phrases, and capture tips in `references/discovery.md`):

- **[60fps.design](https://60fps.design)** + **[@60fpsdesign](https://x.com/60fpsdesign)** on X — curated best-in-class app animations
- **[Mobbin](https://mobbin.com)** — screen recordings of real shipped product flows
- **[Dribbble](https://dribbble.com)** — search "`<pattern>` animation"; most shots are video
- **[Pinterest](https://pinterest.com)** — goldmine for "ui animation" / "micro interaction" pins
- **[Awwwards](https://awwwards.com)** / **[Godly](https://godly.website)** — motion-heavy websites (screen-record)
- X craft accounts: **@emilkowalski_**, **@raunofreiberg**, **@jh3yy**, **@jsngr**

Ask them to bring back a link or screen recording, then continue at Phase 1.

## Phase 1 — Acquire

- Download the reference (`yt-dlp` handles X/Twitter, YouTube, most hosts; plain
  `curl` for direct mp4/GIF; ask the user for a screen recording if undownloadable).
- **Check tooling first**: `command -v yt-dlp ffmpeg ffprobe` — install what's
  missing (`brew install yt-dlp ffmpeg`) before starting.
- Probe before dissecting — fps, resolution, duration set every later command:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,duration,nb_frames \
  -of default=nw=1 ref.mp4
```

See `references/acquisition.md` for edge cases.

## Phase 2 — Overview contact sheet

One tiled grid at ~2fps to map the whole video and find the transition windows:

```bash
ffmpeg -i ref.mp4 -vf "fps=2,scale=270:270,tile=7x5" overview.png
```

Read it and note: distinct states, when each transition starts/ends, what the
interactions are (finger/cursor visible?), and which screen regions matter.

## Phase 3 — Crop-band frame stacks

Extract dense vertical stacks of just the region that moves, at (or near) native
fps. **Derive crop coordinates mathematically from the overview sheet's scale
factor — do not eyeball.** Keep stacks to 14–17 rows for readability; use
`not(mod(n,k))` sampling to fit; always pair `select=` with `-vsync 0`.

```bash
# every 2nd frame of frames 96–126, one region, 16 rows
ffmpeg -i ref.mp4 -vf "crop=W:H:X:Y,select='between(n,96,126)*not(mod(n,2))',tile=1x16" \
  -frames:v 1 -vsync 0 stack.png
```

Start stacks ~0.3s before visible motion so you capture the exit phase, not just
the entrance. Full recipes in `references/dissection.md`.

## Phase 4 — Analysis checklist

Work through the checklist for your species (both, for hybrids). Write the
findings down as a doc — this becomes the implementation spec *and* the
verification baseline.

**Timeline choreography** (full list in `references/analysis.md`):
1. Which properties change (translate, opacity, scale, blur, letter-spacing…)
2. Direction grammar (conveyor vs mirror)
3. Stagger order (forward, reverse-index, center-out)
4. Feather — how many units are mid-transition simultaneously
5. Easing measured from frame-by-frame deltas — never guessed
6. Asymmetric timing (fast exit + long settle is the norm)
7. Handoff overlap between elements
8. Intermediate/transient values
9. What explicitly does NOT move

**Interaction-driven** (full list in `references/porting-interactions.md`):
1. The progress domain — what does 0→1 span? Is it clamped, rubber-banded, wrapped?
2. Continuous mappings — which properties interpolate smoothly with progress
   (gradients, positions, magnification fields)
3. Discrete derivations — which values step at thresholds, and how each step
   transitions (crossfade? roll? hard cut?) — check for ghost frames at 60fps
4. Interaction grammar — every gesture and button: does reset *jump* or *rewind*?
   does release snap, settle, or stay? is there an autoplay?
5. State-dependent chrome — does the scene's palette/theme flip at some progress
   value (e.g. day→night)? Does the flip lead or lag the continuous background?
6. Smoothing — does the driven value track input 1:1 or through a spring?

## Phase 5 — HTML motion lab (optional, decide deliberately)

A single self-contained HTML file (no deps) with toggles + speed slider, to lock
timing before touching production. **Build it when** the animation is
timeline-choreographed and timing/easing is the hard part. **Skip it when** the
animation is interaction-driven — easing comes from the user's finger, so go
straight to the production port and move the iteration loop into Phase 7
verification instead.

## Phase 6 — Production port

Default target is framer-motion (`references/porting-framer-motion.md` for the
pitfall table — filter containing-block trap, per-property transition delays,
double-animation nesting, rAF progress bars). For interaction-driven animations
use the one-MotionValue architecture in `references/porting-interactions.md`.
Phases 0–5 are framework-agnostic: the same analysis doc ports to CSS/WAAPI,
React Native Reanimated, or SwiftUI.

## Phase 7 — Verify against the reference

Don't stop at "it runs". Drive your implementation to the same states you
dissected (Playwright/browser automation), screenshot them, and compare against
the frame stacks from Phase 3. This is where mismatches surface — a theme flip
threshold that lags the sky, a crossfade that's too slow, a stagger running the
wrong direction. Loop: compare → adjust constant → re-screenshot. Method in
`references/verification.md`.

## Phase 8 — Document

Record: source link, probe output, the analysis doc, tuning constants (with
comments explaining which measurement each encodes), deliberate deviations from
the reference (and why), and the exact ffmpeg commands so the dissection is
reproducible.

## Worked examples

- `references/examples/text-sweep.md` — timeline species: the X Money
  reverse-index text sweep (stagger math, blur feather, spring settle)
- `references/examples/timelapse-slider.md` — interaction species: a weather
  timelapse scrubber (continuous sky interpolation, discrete hourly crossfades,
  rewind-not-jump reset, scene theme flip)

## Ethics

This skill is for studying motion *technique* — timing, easing, structure — to
build your own work. Don't use it to ship 1:1 clones of a branded product's
identity.
