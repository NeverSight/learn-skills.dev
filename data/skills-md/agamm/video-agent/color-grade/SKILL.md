---
name: color-grade
description: Color-grade a video — apply a cinematic look / LUT, or generate and compare candidate looks for the user to pick. Use whenever footage looks flat/muted/cold and needs grading, you want a named reusable look (warm, teal-orange, punchy, neutral), or you have a .cube LUT to apply. Covers applying .cube/HALD LUTs via ffmpeg, baking a look from a color-filter chain, and the "render a few looks, let me choose" workflow.
---

# Color grade (LUTs via ffmpeg)

Grade through **LUT files** rather than re-deriving filter params each time. Two LUT formats,
both native to ffmpeg, no extra deps:
- **`.cube`** — a 3D LUT (what colorists ship). Applied with `lut3d`.
- **`.png` HALD-CLUT** — a look baked from a filter chain (below). Applied with `haldclut`.

The `grade` command auto-detects by extension.

```bash
# Apply a look
uv run video-agent grade apply in.mp4 --lut luts/teal_orange.cube -o out.mp4
uv run video-agent grade apply in.mp4 --lut luts/warm.png        -o out.mp4   # HALD
```

## "Make a few looks and let me choose"

The best grading UX: render the SAME frame through several candidate looks into one labelled
contact sheet, show it, let the user pick — then apply the winner to the whole video.

```bash
uv run video-agent grade preview in.mp4 --at 45.0 \
    --lut none --lut luts/warm.png --lut luts/teal_orange.cube --lut luts/punchy.png \
    -o looks.png
# read looks.png → user picks → grade apply with that one
```
`none` = the ungraded original (always include it for reference). Pick a frame (`--at`) with
skin tones + a bright and a dark area so the grade's effect is visible.

## Bake a look into a reusable LUT

Author a look as a **color-filter chain**, then bake it into a HALD LUT once so it's reusable
and fast to apply:

```bash
uv run video-agent grade gen-lut \
    --eq "curves=r='0/0 .5/.55 1/1':b='0/.03 1/.97',colorbalance=rs=.05:bs=-.05" \
    -o luts/warm.png
```
This runs an identity HALD-CLUT through the chain → a `.png` LUT. **Use available filters
only** — this ffmpeg is LGPL, so **no `eq`** (and no `drawtext`). Grade with: `curves` (the
workhorse — per-channel tone curves), `colorbalance` (shadows/mids/highlights RGB),
`colorchannelmixer` (channel mixing / saturation), `lut1d`. Quick starting points:
- **warm**: `colorbalance=rs=.04:rm=.03:bs=-.04:bm=-.03`
- **teal-orange**: `colorbalance=rh=.06:bs=.08` + lift shadows blue, push highlights warm
- **punchy**: `curves=all='0/0 .25/.18 .75/.82 1/1'` (S-curve contrast) + light saturation via `colorchannelmixer`
- **desaturate/filmic**: `colorchannelmixer` toward grey, or `curves` to lift blacks

## Where grading sits in a pipeline

- Grade **at the final encode**, after cuts/reframe, before captions/overlays (so burned text
  keeps its intended color). In an `edl-edit` job, set `"grade": "luts/x.png"` in the EDL and
  it's applied to the whole cut in the same pass.
- Grading helps most on **flat/log/prosumer footage**; typical Rec.709 screen-recordings and
  webcams need only a gentle lift. Don't over-grade — a subtle look beats a heavy filter.

## Gotchas

- **`.cube` vs HALD**: external colorist LUTs are usually `.cube` (→`lut3d`); looks you bake
  here are `.png` HALD (→`haldclut`). The command handles both; just keep the extension honest.
- **HALD level**: `gen-lut` defaults to level 8 (a 64³ grid) — plenty for smooth grades;
  raising it makes a bigger file, rarely needed.
- **Grade once, reuse**: commit your `luts/*.png` (or `.cube`) so the look is plain-text/
  data and re-applies identically across clips and re-renders.
