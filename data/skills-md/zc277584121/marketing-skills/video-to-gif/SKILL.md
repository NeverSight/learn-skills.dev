---
name: video-to-gif
description: Convert a video to multiple GIF variants with different quality/size tradeoffs. Generates a comparison set so the user can visually pick the best result.
---

# Skill: Video to GIF

Convert a video file into multiple GIF variants with different parameters, so the user can visually compare and pick the best one.

> **Prerequisite**: FFmpeg must be installed. gifsicle is optional (enables lossy compression variants).

---

## When to Use

The user wants to create a GIF from a video clip but isn't sure about the right parameters. GIF quality involves tradeoffs between:
- **File size** — smaller is better for sharing/embedding
- **Color accuracy** — fewer colors = smaller but may cause banding
- **Smoothness** — higher FPS = smoother but larger
- **Resolution** — wider = sharper detail but larger

Rather than guessing, this skill generates multiple variants and lets the user decide.

---

## Default Workflow

When the user provides a video file:

```bash
python /path/to/skills/video-to-gif/scripts/video_to_gif.py <input.mp4>
```

This generates GIFs in `<input>_gifs/` directory with the **full** preset (18 variants):
- 3 FPS options: 10, 15, 20
- 3 widths: 480px, 640px, 800px
- 2 color counts: 128, 256

Output includes a sorted comparison table showing file size, FPS, width, and colors for each variant.

---

## Presets

| Preset | Variants | Best For |
|--------|----------|----------|
| `full` | ~18 | General use — broad exploration of the parameter space |
| `minimal` | ~4 | Quick comparison — just a few key tradeoff points |
| `lossy` | ~12 | Smallest files — includes gifsicle lossy compression levels |
| `quality` | ~12 | Best visuals — higher res, includes bayer dithering |

```bash
# Quick comparison with fewer variants
python .../video_to_gif.py input.mp4 --presets minimal

# Include lossy compression (requires gifsicle)
python .../video_to_gif.py input.mp4 --presets lossy

# Higher quality focus
python .../video_to_gif.py input.mp4 --presets quality
```

---

## Common Options

| Flag | Default | Description |
|------|---------|-------------|
| `-o`, `--output-dir` | `<input>_gifs/` | Output directory for all GIF variants |
| `--start` | none | Start time in seconds (trim source) |
| `--end` | none | End time in seconds (trim source) |
| `--presets` | `full` | Preset config: full, minimal, lossy, quality |
| `--fps` | preset | Override FPS values (e.g., `--fps 10 15 20`) |
| `--width` | preset | Override width values (e.g., `--width 480 640`) |
| `--colors` | preset | Override color counts (e.g., `--colors 128 256`) |
| `--lossy` | preset | Gifsicle lossy levels (e.g., `--lossy 0 30 80`) |

---

## Examples

```bash
# Convert first 10 seconds of a video
python .../video_to_gif.py demo.mp4 --end 10

# Extract a specific segment
python .../video_to_gif.py demo.mp4 --start 5 --end 15

# Custom parameter sweep
python .../video_to_gif.py demo.mp4 --fps 12 15 --width 480 800 --colors 256

# Lossy compression comparison (needs gifsicle)
python .../video_to_gif.py demo.mp4 --lossy 0 30 60 100
```

---

## How to Choose

After running, open the output directory and compare:

1. **Start with the smallest files** — check if quality is acceptable
2. **Look for color banding** — if visible, try 256 colors or bayer dithering (quality preset)
3. **Check smoothness** — if too choppy, go up to 15 or 20 FPS
4. **Check clarity** — if text is unreadable, go up to 640 or 800px width

The sweet spot for most screen recordings is usually around **640px, 15fps, 256 colors**.

---

## Important Notes

- Widths larger than the source video resolution are automatically skipped.
- The script uses FFmpeg's two-pass palette generation for optimal GIF quality (much better than single-pass).
- Lossy compression via gifsicle can reduce file size by 30-70% with minimal visual impact at level 30-60.
- For very long clips, consider trimming with `--start`/`--end` first — GIFs over 10 seconds can get very large.
