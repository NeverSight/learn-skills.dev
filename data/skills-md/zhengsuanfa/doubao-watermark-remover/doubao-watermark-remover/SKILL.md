---
name: doubao-watermark-remover
description: Remove the visible Doubao (豆包) AI watermark from images. Use when asked to remove Doubao watermarks, clean Doubao-generated images, or process images with the "豆包AI生成" watermark.
---

# Doubao Watermark Remover

## Dependencies

- Python 3.9+
- Pillow (install with `pip install -r requirements.txt`)

## Quick start

1) Install dependencies in the scripts folder:
   - `cd doubao-watermark-remover/scripts && pip install -r requirements.txt`

2) Run the CLI:
   - `python remove_watermark.py <input-image> <output-image>`

## CLI usage

- Parameters:
  - `input-image`: path to the Doubao watermarked image
  - `output-image`: path for the cleaned image (format inferred from extension)

Example:

```
python remove_watermark.py ./in.png ./out.png
```

## What this skill provides

- `scripts/remove_watermark.py`: CLI entry point and core algorithm.
- `scripts/capture_alpha_map.py`: Tool to capture Doubao watermark alpha map.
- `references/algorithm.md`: Math, detection rules, and usage guide.

## Workflow

1) First time: Generate alpha map using `capture_alpha_map.py`
2) Use `remove_watermark.py` for batch processing.

## Capturing Alpha Map (First Time Required)

Since Doubao watermark pattern may vary, you need to capture the alpha map first:

1. Generate a pure black image (0,0,0) and have Doubao add watermark to it
2. Run the capture tool:
   ```
   python capture_alpha_map.py <black-with-watermark.png> <width> <height>
   ```
   Size options: 140x35 (small images) or 180x40 (large images)

3. The tool will save the alpha map to `assets/` folder

## Notes

- Doubao watermark "豆包AI生成" appears in the **bottom-right** corner
- Script uses Pillow for image IO and per-pixel edits
- Output format is inferred from the output file extension
