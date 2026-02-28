---
name: image-processing
description: "Process images for web development — resize, crop, trim whitespace, convert formats (PNG/WebP/JPG), optimise file size, generate thumbnails, create OG card images. Uses Pillow (Python) — no ImageMagick needed. Trigger with 'resize image', 'convert to webp', 'trim logo', 'optimise images', 'make thumbnail', 'create OG image', 'crop whitespace', 'process image', or 'image too large'."
compatibility: claude-code-only
---

# Image Processing

Process images for web development using Pillow (Python). Resize, convert, trim, optimise, and composite — no ImageMagick or native dependencies required.

## Prerequisites

Pillow is usually pre-installed. If not:

```bash
pip install Pillow
```

## Commands

All commands use `scripts/process-image.py`. Each takes `--output` (`-o`) and optional `--quality` (`-q`).

### Resize

Scale an image to specific dimensions or by width/height (maintains aspect ratio if only one given).

```bash
python3 plugins/design-assets/skills/image-processing/scripts/process-image.py \
  resize input.png -o resized.png --width 1920 --height 1080

# Width only — height calculated from aspect ratio
python3 .../process-image.py resize input.png -o resized.png -w 800
```

### Convert Format

Convert between PNG, JPG, WebP. RGBA→JPG automatically composites onto white background.

```bash
python3 .../process-image.py convert logo.png -o logo.webp
python3 .../process-image.py convert photo.webp -o photo.jpg -q 90
```

### Trim Whitespace

Auto-crop surrounding whitespace from logos and icons.

```bash
python3 .../process-image.py trim logo-with-padding.png -o logo-trimmed.png
```

### Thumbnail

Create a thumbnail fitting within a max dimension (maintains aspect ratio).

```bash
python3 .../process-image.py thumbnail product.jpg -o thumb.jpg --size 300
```

### Optimise for Web

Resize + compress in one step. Ideal for preparing uploaded images for production.

```bash
python3 .../process-image.py optimise hero.jpg -o hero.webp -w 1920 -q 85
```

### OG Card

Generate a 1200x630 Open Graph card image with title and subtitle overlay.

```bash
# With background image
python3 .../process-image.py og-card \
  --background hero.jpg \
  --title "My Page Title" \
  --subtitle "A brief description" \
  -o og-image.png

# Solid colour background
python3 .../process-image.py og-card \
  --bg-color "#1a1a2e" \
  --title "My Page Title" \
  -o og-image.png
```

## Common Workflows

### Logo Cleanup (client-supplied JPG with white background)

```bash
# 1. Trim whitespace
python3 .../process-image.py trim client-logo.jpg -o logo-trimmed.png

# 2. Convert to PNG (for transparency on non-white backgrounds)
python3 .../process-image.py convert logo-trimmed.png -o logo.png

# 3. Create favicon-sized version
python3 .../process-image.py thumbnail logo.png -o favicon-source.png --size 512
```

### Prepare Hero Image for Production

```bash
# Resize to max width, convert to WebP, compress
python3 .../process-image.py optimise uploaded-hero.jpg -o public/images/hero.webp -w 1920 -q 85
```

### Batch Process (Multiple Images)

For batch operations, write a quick script rather than running commands one by one:

```python
import subprocess, glob
for img in glob.glob("uploads/*.jpg"):
    name = img.rsplit("/", 1)[-1].replace(".jpg", ".webp")
    subprocess.run(["python3", ".../process-image.py", "optimise", img, "-o", f"public/images/{name}", "-w", "1200", "-q", "85"])
```

## Pipeline with Gemini Image Gen

Generate → Process → Deploy:

```bash
# 1. Generate with Gemini
python3 plugins/design-assets/skills/gemini-image-gen/scripts/generate-image.py \
  --prompt "..." --output raw-hero.png --count 3

# 2. User picks favourite (e.g. raw-hero-2.png)

# 3. Optimise for web
python3 plugins/design-assets/skills/image-processing/scripts/process-image.py \
  optimise raw-hero-2.png -o public/images/hero.webp -w 1920 -q 85
```

## Output Format Guide

| Use case | Format | Why |
|----------|--------|-----|
| Photos, hero images | WebP | Best compression, wide browser support |
| Logos, icons (need transparency) | PNG | Lossless, supports alpha |
| Fallback for older browsers | JPG | Universal support |
| Thumbnails | WebP or JPG | Small file size priority |
| OG cards | PNG | Social platforms handle PNG best |
