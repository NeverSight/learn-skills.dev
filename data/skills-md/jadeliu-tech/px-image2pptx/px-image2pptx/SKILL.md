---
name: px-image2pptx
description: >
  Convert static images (slides, posters, infographics) to editable PowerPoint files.
  Pipeline: OCR detects text → classical CV textmask detects ink pixels → mask-clip
  ANDs with OCR bboxes (preserves illustrations) → LAMA inpaints clean background →
  python-pptx assembles editable text boxes with auto-scaled fonts and detected colors.
  Trigger on 'convert image to pptx', 'make slide editable', 'image to powerpoint',
  'extract text from slide as editable', 'reconstruct slide', or when the user has
  a slide/poster image and wants an editable .pptx file.
metadata:
  author: Jade Liu
  source: https://github.com/JadeLiu-tech/px-image2pptx
risk: low
---

# px-image2pptx: Image to Editable PowerPoint

## What It Does

Converts a static image into an editable .pptx file where every text element is
a selectable, editable text box over a clean inpainted background. The full pipeline
runs in 8-16 seconds:

1. **OCR** (PaddleOCR) — detects text regions with bounding boxes and content
2. **Textmask** (classical CV) — finds text ink pixels via adaptive thresholding
3. **Mask-clip** — ANDs textmask with OCR bboxes to preserve non-text elements
4. **Inpaint** (LAMA) — reconstructs masked regions with neural inpainting
5. **Assemble** — places editable text boxes with auto-scaled fonts and detected colors

## When to Use This

| Scenario | Use px-image2pptx? |
|----------|-------------------|
| Slide with text on solid/flat background | Yes — best results |
| Slide with photo background | Yes — uses inpainting (warn about overlap areas) |
| Slide with solid background | Yes — use `--skip-inpaint` for speed |
| Chinese/multilingual slide | Yes — `ch` OCR handles both Chinese and English |
| Poster or infographic with text | Yes — works well if text is separate from graphics |
| Dense chart with axis labels on bars | Caution — removing text damages chart structure |
| Text directly overlapping a photo | Caution — inpainting artifacts likely on complex areas |
| Extract individual assets as PNGs | No — use px-asset-extract |
| Read text from image without PPTX | No — use OCR directly |
| Edit an existing .pptx file | No — use the pptx skill |

## Installation

```bash
git clone https://github.com/JadeLiu-tech/px-image2pptx.git
cd px-image2pptx
pip install -e ".[all]"
```

## Usage

### CLI

```bash
# Full pipeline
px-image2pptx <image> -o <output.pptx>

# Chinese text
px-image2pptx <image> -o <output.pptx> --lang ch

# Skip inpainting (solid-bg slides)
px-image2pptx <image> -o <output.pptx> --skip-inpaint

# Pre-computed OCR (skips PaddleOCR dependency)
px-image2pptx <image> -o <output.pptx> --ocr-json text_regions.json

# Keep intermediate files
px-image2pptx <image> -o <output.pptx> --work-dir ./debug/
```

### Python API

```python
# One-line conversion
from px_image2pptx import image_to_pptx
report = image_to_pptx("slide.png", "output.pptx")

# With options
report = image_to_pptx(
    "slide.png", "output.pptx",
    lang="ch",            # Chinese OCR
    sensitivity=16,       # textmask sensitivity
    dilation=12,          # textmask dilation
    skip_inpaint=False,   # True for solid-bg slides
    work_dir="./debug/",  # save intermediates
)

# Step-by-step
from px_image2pptx.ocr import run_ocr
from px_image2pptx.textmask import compute_masks
from px_image2pptx.inpaint import inpaint
from px_image2pptx.assemble import assemble_pptx

regions = run_ocr("slide.png", lang="ch")
tight, clipped, dilated = compute_masks(cv2.imread("slide.png"), regions)
background = inpaint(cv2.cvtColor(cv2.imread("slide.png"), cv2.COLOR_BGR2RGB), dilated)
report = assemble_pptx("slide.png", regions, "output.pptx", "background.png", tight)
```

## CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `-o`, `--output` | `output.pptx` | Output PPTX path |
| `--ocr-json` | | Pre-computed OCR JSON (skips OCR) |
| `--lang` | `auto` | OCR language: `auto`, `en`, `ch` |
| `--sensitivity` | `16` | Textmask sensitivity (lower = more) |
| `--dilation` | `12` | Textmask dilation pixels |
| `--min-font` | `8` | Min font size in points |
| `--max-font` | `72` | Max font size in points |
| `--skip-inpaint` | | Skip LAMA inpainting |
| `--work-dir` | | Save intermediate files |

## OCR JSON Format

```json
{
  "text_regions": [
    {
      "id": 0,
      "text": "Hello World",
      "confidence": 0.95,
      "bbox": {"x1": 100, "y1": 50, "x2": 400, "y2": 90}
    }
  ]
}
```

## Key Design Decisions

### Font auto-scaling (90-94% of bbox width)
Uses PIL ImageFont for accurate Latin text measurement, 1.0x em for CJK.
Bidirectional: shrinks if text overflows, grows if text is too small.

### Text color from tight mask
Samples ink pixel colors from the pre-dilation mask (actual ink, no background bleed).
Falls back to contrast-based sampling for light-on-dark text where textmask misses.

### Column-aware line grouping
Two-pass: vertical proximity, then horizontal gap split (3x median height).
Prevents merging left/right column text into one wide text box.

### OCR-guided masking
Raw textmask detects ANY dark pixels (including illustration outlines, borders).
Mask-clip ANDs with OCR bboxes so only confirmed text gets inpainted.
Removes 30-90% of false positive mask pixels depending on image content.

## Dependencies

| Package | Extra | Purpose |
|---------|-------|---------|
| Pillow, numpy, opencv-python, python-pptx | core | Always needed |
| paddleocr, paddlepaddle | `[ocr]` | Text detection |
| torch, simple-lama-inpainting | `[inpaint]` | Background reconstruction |

## Models

Models are downloaded automatically on first use (~370 MB total).

| Model | Size | License |
|-------|------|---------|
| PP-OCRv5_server_det (text detection) | 84 MB | Apache 2.0 |
| PP-OCRv5_server_rec (text recognition) | 81 MB | Apache 2.0 |
| big-lama (inpainting) | 196 MB | Apache 2.0 |

## Performance

| Step | Time | Model |
|------|------|-------|
| OCR (PaddleOCR PP-OCRv5) | 2-5s | 165 MB |
| Textmask + clip | 1-3s | None |
| Inpaint (LAMA) | 4-8s | 196 MB |
| Assembly | <0.2s | None |
| **Total** | **8-16s** | **~370 MB** |

## Limitations — When to Warn the User

Before running the pipeline, assess the input image and set expectations:

| Input characteristic | Impact | What to tell the user |
|---------------------|--------|----------------------|
| Text on solid/flat background | Best results | No caveats needed |
| Text on textured background (paper, fabric) | Good results | LAMA handles repeating textures well |
| Text overlapping photos or illustrations | Inpainting artifacts likely | Warn: "areas where text covers photos may show blurring or hallucinated details" |
| Chart/diagram with axis labels or legends | Removing text damages the chart | Warn: "text tightly coupled with the chart cannot be cleanly separated — consider `--skip-inpaint`" |
| Light text on dark background | Blockier inpainting | Warn: "white-on-dark text uses box masks instead of tight ink masks, which may leave rectangular artifacts" |
| WebP image | OCR will fail silently (0 regions) | Convert to PNG before processing: `Image.open("input.webp").save("input.png")` |
| Very large image (>4000px long side) | Inpainting may take minutes | Suggest `--skip-inpaint` or downscaling first |
| Decorative/handwritten fonts | Text content is correct, but typeface won't match | Warn: "fonts are reconstructed as Arial/Helvetica — decorative fonts are not preserved" |
| Centered or justified text | Layout will be left-aligned | Warn: "text alignment and paragraph formatting are not preserved" |

### When NOT to use this skill

- The user wants to **extract individual assets** (icons, logos, illustrations) → use `px-asset-extract`
- The user wants to **read text** from an image without creating a PPTX → use OCR directly
- The input is **already a .pptx file** → use the `pptx` skill to edit it directly
- The image has **no text** (pure photo, illustration) → there's nothing for this pipeline to do
