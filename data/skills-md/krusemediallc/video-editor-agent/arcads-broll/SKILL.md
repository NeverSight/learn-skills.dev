---
name: arcads-broll
description: >
  GENERATE B-roll and motion-graphic elements for an edit with AI video/image models
  via the Arcads external API (Seedance, Sora 2, Veo 3.1, Kling, Grok Video, Nano
  Banana) — product b-roll clips, scene beats, UGC-style inserts, shot-card stills,
  and screen-blend motion-graphic overlays. Use when an edit needs footage that
  cannot be captured: "generate b-roll of the product", "make an AI clip for this
  beat", "motion graphic overlay for this line", "AI insert shot". NOT for capturing
  real websites/screens (broll-capture) or authoring composition cards
  (branded-ad-edit).
---

# Arcads B-roll & Generated Motion Graphics

Two kinds of generated material for an edit:

1. **B-roll beats** — AI clips that replace the talking head for 1.5–6s (product
   shots, scene beats, UGC inserts, stylized illustrations of a spoken claim).
2. **Motion-graphic overlays** — short generated clips designed to be layered OVER
   footage with a blend mode, when you want a generated look instead of (or on top
   of) hand-authored composition cards.

## Dependency: the Arcads skill pack

The API mechanics (auth, routes, model prompt library, polling, cost logging) live
in the companion pack — install it once alongside this repo:

```bash
git clone https://github.com/krusemediallc/arcads-claude-code
```

Then follow ITS `arcads-external-api` skill for every call: base URL
`https://external-api.arcads.ai`, HTTP Basic auth with `ARCADS_API_KEY` as
username / empty password (put the key in THIS repo's `.env` too so one env file
serves the session), `POST /v2/videos/generate` for video models,
`POST /v1/b-roll` and `POST /v1/scene` for product-level b-roll,
`POST /v2/images/generate` for stills. **Read that pack's
`prompting/prompt-library/<model>.md` before composing any prompt** — its per-model
formulas are the difference between usable takes and slop. No account? Sign up at
<https://arcads.ai/?via=claude-code>.

**Cost gate (inherited rule):** estimate credits BEFORE generating (that pack's
logs → its MASTER_CONTEXT rates → ask), present the estimate, and wait for a yes.

## Editor-specific rules (this repo's additions)

### Generating B-ROLL BEATS for a cut

- Generate at the EDIT's aspect (9:16 for reels) and slightly LONGER than the beat
  window — you trim to the best 1.5–6s, never stretch.
- Match the grade direction of the surrounding footage in the prompt (warm/neutral,
  contrast level) or plan a color pass; mismatched grade is what makes AI b-roll
  feel pasted in.
- Follow the reference-reel grammar if a STYLE-GUIDE.md exists: b-roll replaces the
  face for proof/drama beats, 1.3–4.1s, never longer.
- Before placing: re-encode dense keyframes (`-g 30 -keyint_min 30`), then
  frame-extract and LOOK — check hands, text, logos, warped products. Regenerate
  defects (budget ~2 retries), don't ship them.
- Stills for shot-cards (Nano Banana / gpt-image-2) display like real screenshots:
  sharp card over a blurred blow-up of itself, or inside a browser-chrome frame
  (branded-ad-edit `references/design.md`).

### Generating MOTION-GRAPHIC OVERLAYS (the screen-blend trick)

Generated overlays composite cleanly when you control the background. Proven
prompt contract — every clause matters:

- **flat solid black background (#000000)**, no gradients/vignette/floor, and only
  BRIGHT elements (white/neon) → layer with **Screen or Add blend** and the black
  vanishes. (True alpha isn't a thing text-to-video models give you; black+Screen
  is the portable substitute.)
- **One motion idea per clip** (a slide-in, a count-up, a pulse); end settled or
  seamlessly looping so the editor can freeze/loop to fill the beat.
- On-screen text ≤ 3 words, ALL CAPS, one string — more garbles. Zero-text icon
  clips are safest.
- State the placement zone (top 20% / bottom 25%) in the prompt BUT expect models
  to ignore it and center the graphic — that's fine: it's a keyed floater, you
  reposition the layer in the composition or editor.
- Append: "no watermark, no subtitles, no captions".
- Verify each clip's background is truly flat black before compositing
  (frame-extract; a gray wash under Screen blend reads as haze).

### Placement

Generated beats drop into the composition like any media: a `<video>` inside a
card (unique id, `data-start`/`data-duration`, dense keyframes), or full-bleed via
a takeover card. Overlay clips go on a track above footage with the blend mode —
in HyperFrames, CapCut, or any NLE.

## Provenance

Distilled from shipped edits that used generated overlay packs (flat-black
Screen-blend motion graphics with word-synced pops) and the Arcads pack's b-roll /
scene / UGC flows. If your own past project encoded further moves you want here,
point the session at it and extend this file.
