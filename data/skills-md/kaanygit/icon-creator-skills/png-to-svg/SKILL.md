---
name: png-to-svg
description: Convert PNG/JPG icons and logo marks into SVG with suitability analysis, algorithm selection, comparison PNG, and stats.
---

# png-to-svg

Use this skill when the user asks to vectorize a PNG/JPG, create an SVG from an icon, or compare vectorization algorithms.

## How to invoke

```bash
python skills/png-to-svg/scripts/vectorize.py --input output/example/master.png
```

Optional arguments:

- `--output-dir <path>`: output root, default `output`
- `--output-path <path>`: explicit SVG destination
- `--algorithm <auto|vtracer|potrace|imagetracer>`: default `auto`
- `--color-count <n>`: quantized color count
- `--simplify <0-100>`: higher means fewer cells/paths, default `50`
- `--force`: proceed even when suitability is poor
- `--no-optimize`: skip SVG optimization
- `--no-comparison`: skip comparison PNG

The script prints the generated SVG path on the last stdout line.

## Current implementation

External tracers are optional. If `vtracer`, `potrace`, or `imagetracerpy` are missing, the skill uses a deterministic Pillow-based fallback tracer that emits rect-based SVGs. It is best for flat icons and honest about similarity in `stats.json`.
