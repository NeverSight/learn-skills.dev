---
name: mascot-processor
description: Convert mascot or character MP4 animations into transparent-background GIFs, APNGs, and WebMs. Auto-detects the background type (green screen or white/off-white) and removes it. Green screen mode kills every green pixel aggressively; white background mode uses color isolation with a per-frame audit. Outputs at 160px and at original resolution. Use when the user asks to remove a background from an animated MP4, make a transparent GIF or APNG, build a mascot or sticker asset pack, or key out a green screen from pixel-art animation.
---

# Mascot Processor

Convert animated character MP4s into transparent-background assets (GIF, APNG, WebM) for use in infographics, videos, and overlays.

## When to Use

- The user provides mascot or character MP4 files to convert
- The user asks to remove a background from pixel-art or 2D animation
- The user wants a transparent sticker or mascot asset pack

## Output Location

Write into an output directory the user names. If they do not name one, default to `./mascot-pack/` in the current working directory and say so before writing.

```
mascot-pack/
  source/     # Original MP4s preserved
  gif/        # 160px wide, 24fps (lightweight overlays)
  apng/       # 160px wide, 24fps, full 8-bit alpha
  webm/       # Original resolution, 24fps, VP9 alpha (video compositing)
  gif-hd/     # Original resolution, 24fps (high-fidelity)
  apng-hd/    # Original resolution, 24fps, full 8-bit alpha (high-fidelity)
```

## Naming

Name files by the action being performed, one word: `walking.gif`, `loading.gif`, `waving.gif`.

## Dependencies

```bash
pip install numpy scipy pillow
# ffmpeg must be on PATH: brew install ffmpeg (macOS) or apt install ffmpeg (Debian/Ubuntu)
```

```python
import numpy as np
from scipy import ndimage
from PIL import Image
```

## The Process

### Step 0: Auto-Detect Background Type

Sample the corner pixels of frame 0. If the green channel dominates (G > R + 0.15 AND G > B + 0.15 AND G > 0.4), use **Green Screen Mode**. Otherwise use **White Background Mode**.

Green screen preserves every non-green character color (blue, yellow, brown, and so on). White background requires color isolation, which has edge cases with multi-colored characters. Avoid green props in green screen scenes, since they will be removed along with the backdrop.

---

## GREEN SCREEN MODE (Default Method)

Kill ALL green pixels everywhere. No flood-fill, no exceptions. 2px dilation to eat fringe.

```python
def remove_green(frame_path):
    """Kill all green pixels aggressively. 2px dilation for fringe."""
    img = Image.open(frame_path).convert("RGBA")
    a = np.array(img).astype(float)
    r, g, b = a[:,:,0]/255, a[:,:,1]/255, a[:,:,2]/255
    maxc = np.maximum(r, np.maximum(g, b))
    minc = np.minimum(r, np.minimum(g, b))
    diff = maxc - minc
    sat = np.where(maxc == 0, 0, diff / maxc)
    hue = np.zeros_like(r)
    mask = diff > 0
    idx = mask & (maxc == g)
    hue[idx] = 60 * ((b[idx] - r[idx]) / diff[idx]) + 120
    idx = mask & (maxc == r)
    hue[idx] = (60 * ((g[idx] - b[idx]) / diff[idx]) + 360) % 360
    idx = mask & (maxc == b)
    hue[idx] = 60 * ((r[idx] - g[idx]) / diff[idx]) + 240

    # Broad green detection: catch everything
    green_dominant = (g > r + 0.10) & (g > b + 0.10) & (g > 0.35)
    green_hue = (hue > 60) & (hue < 180) & (sat > 0.15)
    is_green = green_dominant | green_hue

    # Dilate 2px to eat all green fringe
    is_green = ndimage.binary_dilation(is_green, iterations=2)

    result = np.array(img)
    result[is_green, 3] = 0
    return Image.fromarray(result)
```

---

## WHITE BACKGROUND MODE

### Single-Hue Isolation (default for white bg)

For characters built from one saturated hue plus black outlines and details, on a white or off-white background.

```python
def remove_bg_single_hue(frame_path):
    """Color isolation: keep saturated color and black, kill everything else."""
    img = Image.open(frame_path).convert("RGBA")
    a = np.array(img).astype(float)
    r, g, b = a[:,:,0]/255, a[:,:,1]/255, a[:,:,2]/255
    maxc = np.maximum(r, np.maximum(g, b))
    minc = np.minimum(r, np.minimum(g, b))
    diff = maxc - minc
    sat = np.where(maxc == 0, 0, diff / maxc)
    val = maxc

    # Keep only saturated (the character's color) or dark (black outlines, eyes)
    keep = (sat > 0.25) | (val < 0.35)

    # Erode 2px to eat compression fringe
    keep = ndimage.binary_erosion(keep, iterations=2)

    # Kill any surviving grayish pixels
    grayish = (sat < 0.25) & (val > 0.30)
    keep = keep & ~grayish

    result = np.array(img)
    result[~keep, 3] = 0
    return Image.fromarray(result)
```

### Multicolor (for characters with yellow/gold effects on white bg)

Auto-detect: sample frame 30. If hue range 20 to 70 holds a significant number of saturated pixels, use this mode.

```python
def remove_bg_multicolor(frame_path):
    """Color isolation with hue awareness for characters mixing cool and warm tones."""
    img = Image.open(frame_path).convert("RGBA")
    a = np.array(img).astype(float)
    r, g, b = a[:,:,0]/255, a[:,:,1]/255, a[:,:,2]/255
    maxc = np.maximum(r, np.maximum(g, b))
    minc = np.minimum(r, np.minimum(g, b))
    diff = maxc - minc
    sat = np.where(maxc == 0, 0, diff / maxc)
    val = maxc
    hue = np.zeros_like(r)
    mask = diff > 0
    idx = mask & (maxc == r)
    hue[idx] = (60 * ((g[idx] - b[idx]) / diff[idx]) + 360) % 360
    idx = mask & (maxc == g)
    hue[idx] = 60 * ((b[idx] - r[idx]) / diff[idx]) + 120
    idx = mask & (maxc == b)
    hue[idx] = 60 * ((r[idx] - g[idx]) / diff[idx]) + 240

    # Keep saturated (any color) OR dark
    keep = (sat > 0.25) | (val < 0.35)

    # Also keep yellow/gold
    yellow_range = (hue > 20) & (hue < 70) & (sat > 0.15)
    keep = keep | yellow_range

    keep = ndimage.binary_erosion(keep, iterations=2)
    grayish = (sat < 0.20) & (val > 0.35)
    keep = keep & ~grayish

    result = np.array(img)
    result[~keep, 3] = 0
    return Image.fromarray(result)
```

---

## Frame-by-Frame Audit (mandatory for white bg mode)

After processing, audit EVERY frame:

```python
opaque = result[:,:,3] > 0
suspect = opaque & (sat < 0.25) & (val >= 0.35)
# suspect.sum() MUST be 0 for every frame
```

If ANY frame fails, tighten thresholds and reprocess. Do NOT output until all frames pass.

For multicolor mode with glow effects, some fringe is inherent, so visual inspection is sufficient.

---

## Output Generation

1. **Extract frames**: `ffmpeg -i input.mp4 {tmpdir}/frame_%04d.png`
2. **Auto-detect background** by sampling the corners for green
3. **Process each frame** through the appropriate function
4. **Audit** (white bg mode)
5. **Generate all 5 outputs**:

```bash
# GIF 160px
ffmpeg -framerate 24 -i clean_%04d.png \
  -vf "scale=160:-1:flags=lanczos,split[s0][s1];[s0]palettegen=reserve_transparent=on:transparency_color=000000:stats_mode=diff[p];[s1][p]paletteuse=alpha_threshold=128:dither=none" \
  -loop 0 output.gif

# GIF HD (original resolution)
ffmpeg -framerate 24 -i clean_%04d.png \
  -vf "split[s0][s1];[s0]palettegen=reserve_transparent=on:transparency_color=000000:stats_mode=diff[p];[s1][p]paletteuse=alpha_threshold=128:dither=none" \
  -loop 0 output.gif

# WebM (original resolution, VP9 alpha)
ffmpeg -framerate 24 -i clean_%04d.png \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 2M -auto-alt-ref 0 -an output.webm
```

```python
# APNG (via Pillow), both 160px and HD
imgs = [Image.open(p) for p in clean_frames]
imgs[0].save("output.apng", save_all=True, append_images=imgs[1:],
             duration=42, loop=0, disposal=2)  # 42ms = 24fps
```

---

## Alternative Methods (backup if defaults aren't working)

These were tested and work for specific situations. Switch to them if the default isn't producing clean results.

### Alt 1: Green Screen, Flood-Fill from Edges

Only removes green connected to the image borders. **Use when**: the character has intentional green elements (plant stems, green accessories) that need to be preserved. **Tradeoff**: green between body parts (gaps in arms and legs) may survive.

```python
# Same green detection as default, but add flood-fill:
labeled, _ = ndimage.label(is_green)
border_mask = np.zeros_like(is_green)
border_mask[0,:] = True; border_mask[-1,:] = True
border_mask[:,0] = True; border_mask[:,-1] = True
seed = border_mask & is_green
border_labels = set(labeled[seed].flatten()) - {0}
bg_green = np.isin(labeled, list(border_labels))
bg_green = ndimage.binary_dilation(bg_green, iterations=1)
```

### Alt 2: Green Screen, Exact Hex Match

Targets only the specific green screen color with euclidean color distance. **Use when**: the character has green elements AND flood-fill leaves too much bleed. **Tradeoff**: may leave green fringe from MP4 compression blending.

```python
def remove_exact_green(fpath, tolerance=60):
    img = Image.open(fpath).convert("RGBA")
    arr = np.array(img).astype(int)
    # Target: R=4, G=250, B=3 (sample the corners to confirm your own value)
    dr = arr[:,:,0] - 4
    dg = arr[:,:,1] - 250
    db = arr[:,:,2] - 3
    dist = np.sqrt(dr*dr + dg*dg + db*db)
    is_bg = dist < tolerance
    result = np.array(img)
    result[is_bg, 3] = 0
    return Image.fromarray(result)
```

### Alt 3: White Background, Flood-Fill from Edges

Removes only white pixels connected to the borders. **Use when**: the character has intentional white elements inside (white accessories, highlights). **Tradeoff**: white between body gaps may survive, and compression fringe at the edges remains.

```python
bg_color = np.mean([arr[0,0,:3], arr[0,-1,:3], arr[-1,0,:3], arr[-1,-1,:3]], axis=0).astype(int)
diff = np.abs(arr[:,:,:3].astype(int) - bg_color)
color_match = np.all(diff <= 30, axis=2)
labeled, _ = ndimage.label(color_match)
# ... flood-fill from borders, same pattern as green
```

### Alt 4: Anti-Aliasing, Gaussian Blur Alpha

Softens jagged edges after removal. **Use when**: edges look too harsh or pixelated at larger sizes. Apply AFTER any removal method. **Note**: only effective in APNG and WebM, since GIF has 1-bit alpha. All 4 AA methods (hard, alpha blur, gradient, smooth) produced identical results at 160px, so this only matters for HD output.

```python
from PIL import ImageFilter
alpha_img = Image.fromarray((keep * 255).astype(np.uint8))
alpha_smooth = alpha_img.filter(ImageFilter.GaussianBlur(radius=1.5))
result[:,:,3] = np.array(alpha_smooth)
# Then kill white pixels that got alpha from blur bleeding
result[white_mask, 3] = 0
```

---

## What NOT to Use

| Method | Why It Fails |
|--------|-------------|
| FFmpeg colorkey | Misses blended edge pixels from MP4 compression |
| rembg (AI) | Designed for photos, creates shading and halos on pixel art |
