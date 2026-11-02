---
name: a-roll-matting
description: "A-roll prep: get a talking character OFF their background (matte) or onto green BEFORE any editing. Covers chroma key, temporal AI video matting (RVM/MODNet/backgroundremover), per-frame AI matting (rembg), and roto - with verified local recipes, quality checks, and output formats. Use as the FIRST job on any voiceover / talking-head / avatar / podcast video."
---

# A-Roll Matting — the first job

**Scope.** The prep step for any piece with a **person speaking to camera** — a
talking-head, a voiceover presenter, an avatar, a podcast. Before you cut, plan
or animate anything else, decide the **background strategy**, and by default get
the character **off their background** (matte) or **onto green**.

**When to use.** At **STEP 0.5**, right after the source arrives and before the
build skill's concept — on every A-roll piece.

> **THE A-ROLL PREP LAW (mandatory).** When the edit has a person speaking —
> talking-head, voiceover, avatar, podcast — the **first job is the background**,
> not the cut. Decide: keep it, matte it, or key it. Matte/keey FIRST unlocks
> everything downstream (text-behind-subject, screen replacement, graphic
> backgrounds, floating UI, lower-thirds, compositing). Do it before the concept.

---

## 1 · Decide the path (in order of quality)

1. **Shoot on green** — best. If you can still shoot, key the character on a flat,
   evenly-lit green (`#00B140`) or blue screen. A real key beats AI matting on
   edges and hair every time. This is why "add green screen first" is right.
2. **Editable-asset extraction via the MANDATORY generative environment** —
   **SAM 2.1 Large** for segmentation + **BiRefNet** for refinement. The strongest
   path for **existing** footage and for **maximally editable transparent
   assets** (cut-outs, subject layers, alpha). Load
   [`local-generative-colab-skill`](https://github.com/adittaya/local-generative-colab-skill)
   and run it on the remote GPU. Prefer this over the local `rembg` fallback
   whenever the environment is available.
3. **Temporal AI video matting** — best for **existing** footage when the
   environment is not available. Models that see
   time (RVM / Robust Video Matting, MODNet, `backgroundremover`) are far more
   stable than per-frame matting: no flicker, better hair, fewer holes.
4. **Per-frame AI matting** — `rembg` (u2net / u2netp / isnet). Fast and local;
   good for quick work and stills, but **soft/jagged edges, holes on low-contrast
   shots, and it treats baked-in captions/graphics as subject.**
5. **Roto** — mask the hard frames by hand. Always the fallback for the shots the
   model fails.

**When NOT to matte:** if the **background is the message** (a real room, an
office, a house tour, a location) — keep it. Matte only when the background will
be replaced or the subject must float.

## 2 · The verified local recipe (rembg + ffmpeg)

Tested in-sandbox: `rembg 2.0.85` + `onnxruntime 1.30.0` + `ffmpeg` (via
`imageio-ffmpeg`). On a 720x1280 talking-head frame, **u2netp matted in ~3.9 s,
u2net in ~4.3 s** at 55-60% scale.

```bash
pip install rembg onnxruntime opencv-python-headless imageio-ffmpeg
# 1) frames out of the video
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FF" -i aroll.mp4 -vf fps=25 frames/f%05d.png
# 2) matte each frame (see tools/matte.py for the batched runner)
# 3) rebuild: alpha clip + a green-screen version + a matte (alpha) pass
"$FF" -framerate 25 -i matte/f%05d.png -c:v libvpx-vp9 -pix_fmt yuva420p alpha.webm
"$FF" -framerate 25 -i green/f%05d.png -c:v libx264 -crf 16 green.mp4
```

**Sandbox / low-memory rules (learned the hard way):**
- **Downscale the matte input** to ~55-60% (or max side ~640). u2net OOMs at full
  720x1280 in a small container; the alpha is upscaled back with Lanczos.
- **Cap threads** — `OMP_NUM_THREADS=1` (onnxruntime spawns many; a constrained
  box throws `Resource temporarily unavailable`). Run **one model at a time** in
  its own process so memory is freed.
- **Model choice:** `u2netp` (4.6 MB, fastest, softest), `u2net` (176 MB, better),
  `isnet-general-use` (179 MB, best on people, heaviest — may OOM; downscale more).
- Models download on first use to `~/.local/share/rembg/models/` (~176 MB for
  u2net) — cache them once.

## 3 · Quality checks (before you trust a matte)

- **No holes** — the subject is solid; no background showing through the torso.
- **No baked-caption artifacts** — if captions/graphics are burned into the
  frame, the model keeps them as "subject". **Matte BEFORE you add captions, or
  remove the burned ones first.**
- **Edges** — hair is not smudged; no hard/blocky stair-steps; no colour halo.
- **Contrast** — a white shirt on a white wall is a hard case; if the matte fails,
  the answer is **roto**, or re-shoot on green.
- **Temporal stability** — scrub the alpha; it should not flicker or breathe.

**Honest verdict from testing:** per-frame `rembg` on low-contrast talking-head
frames was **usable-with-cleanup at best, unusable at worst** (white-on-white,
baked captions). It is a fast first pass, not a finished key. For production,
shoot on green or use a **temporal video matting** model.

## 4 · Outputs (pick per need)

- **Alpha clip** — WebM VP9 `yuva420p` or ProRes 4444 (best quality) for comp.
- **Green-screen version** — composite on `#00B140` so it drops into any
  chroma-key pipeline.
- **Matte pass** — the grayscale alpha as a PNG sequence (for manual cleanup).
- **Cut-out stills** — transparent PNGs for the ASSETS-PROMPT / graphics kit.

## 5 · Then use it (why matting first unlocks everything)

Once the character is matted, the rest of the pack gets easier:
- **Text-behind-subject** — type passes behind them (Caption system).
- **Screen / set replacement** — put them in any scene (VFX).
- **Graphic background** — put them on a branded plate.
- **Floating UI / lower-thirds** — composites around a clean subject.
- **Chroma key** — if keyed to green, any downstream keyer works.

## 6 · The connection to the rest of the pack

This is **STEP 0.5** in the pipeline: SOURCE -> **A-ROLL PREP (matting)** ->
CONCEPT -> ASSETS-PROMPT -> BUILD -> RENDER GATE -> QA GATE. The matte is an
**asset**, so it is requested/recorded in the asset manifest and checked at the
QA gate (no holes, no baked-caption artifacts, stable alpha).

## Hard limits
Never fabricate a matte that does not hold up — if it fails, roto it or re-shoot
on green. Label any AI matte in the edit notes. Do not matte a background that is
the message.
