---
name: image-to-vector
description: Raster→SVG via VTracer; icons/logos/line art; optional ImageMagick/SVGO.
---

# Image To Vector

## Overview

Use `<skill-path>/scripts/vectorize-image.py` to convert raster images into SVGs. The wrapper uses VTracer for tracing, can optionally preprocess noisy images with ImageMagick, can render PNG previews, and can optimize SVGs with SVGO when `svgo` or `npx` is available.

The CLI is intentionally generic: start with a built-in profile, then override tracing or optimization settings when the input needs a different tradeoff.

## Requirements

- `vtracer` is required.
- `magick` from ImageMagick is optional, but needed for `--preprocess quantize` and PNG previews.
- `svgo` or `npx` is optional, but recommended for smaller SVG output.

Install VTracer with:

```bash
cargo install vtracer
```

## Quick Start

Convert one image with the default balanced profile:

```bash
<skill-path>/scripts/vectorize-image.py input.png --output output.svg
```

Create a smaller web-oriented SVG:

```bash
<skill-path>/scripts/vectorize-image.py input.png --profile web --output output.svg
```

Create a compact SVG when slight simplification is acceptable:

```bash
<skill-path>/scripts/vectorize-image.py input.png --profile compact --output output.svg
```

Create the smallest smooth SVG when more visible simplification is acceptable:

```bash
<skill-path>/scripts/vectorize-image.py input.png --profile ultra --output output.svg
```

Compare direct tracing with ImageMagick-preprocessed tracing:

```bash
<skill-path>/scripts/vectorize-image.py input.png --compare --out-dir ./vectorized
```

Disable SVG optimization when comparing raw VTracer output:

```bash
<skill-path>/scripts/vectorize-image.py input.png --optimize-svg none --output raw.svg
```

Override tracing and optimization settings directly:

```bash
<skill-path>/scripts/vectorize-image.py input.png \
  --profile compact \
  --color-precision 5 \
  --filter-speckle 16 \
  --segment-length 10 \
  --path-precision 0 \
  --svgo-precision 0 \
  --output output.svg
```

## Workflow

1. Inspect the input image before vectorizing. Decide whether it is flat-color artwork, line art, a logo, a diagram, or photo-like content.
2. Start with `balanced` for general flat-color artwork.
3. Use `web` when file size matters but visual fidelity should remain close.
4. Use `compact` when byte size matters more than exact shape fidelity.
5. Use `ultra` only when the smallest smooth output matters more than detail.
6. Use `bw` for pure black-and-white artwork.
7. Prefer direct tracing for clean generated images, icons, and logos.
8. Use `--preprocess quantize` only when the source has JPEG artifacts, speckles, excessive near-duplicate colors, or a very large palette.
9. Render previews and inspect the SVG before choosing a final profile.

## Profiles

- `balanced`: Default profile for general flat-color artwork, generated images, icons, and cartoons.
- `web`: Similar to `balanced`, but uses integer path coordinates and SVGO precision `0` for smaller website SVGs.
- `compact`: More aggressive simplification for smaller smooth SVGs.
- `ultra`: Most aggressive smooth profile; details flatten sooner.
- `cartoon`: Simplified profile for illustrations with thick outlines and broad fills.
- `poster`: General VTracer poster mode for flat-color images.
- `photo`: Softer approximation for photo-like or gradient-heavy images.
- `bw`: Binary tracing mode for pure black-and-white artwork.

## Guidance

Use SVG when the asset needs infinite scaling, editability, CSS styling, crisp vector semantics, or small file size for simple shapes. Use AVIF/WebP/PNG when the source is photo-like or when a raster version is visibly better at lower byte size.

For detailed tuning notes, read `references/vtracer-profiles.md`.
