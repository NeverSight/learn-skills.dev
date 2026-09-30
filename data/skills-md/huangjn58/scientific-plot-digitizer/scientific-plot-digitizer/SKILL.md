---
name: scientific-plot-digitizer
description: Extract numeric data from scientific plot images and paper figures. Use when the user asks to digitize, reverse-engineer, or recover data from plotted curves, scatter plots, spectra, stress-strain charts, dose-response curves, bar charts, PDF figures, screenshots, or WebPlotDigitizer-style scientific graph images and wants CSV/Excel/data points. Do not use for ordinary OCR, table screenshots, image editing, or plotting when the original raw data file is already available.
---

# Scientific Plot Digitizer

## Overview

Recover approximate numeric data from scientific figure images by calibrating axes, extracting visible marks or curves, converting pixels to data coordinates, and exporting auditable CSV/Excel outputs with a QA overlay.

Treat digitized values as estimates. Prefer the original source data when available.

## Workflow

1. **Confirm the extraction target**
   - Identify the panel, series, graph type, axis labels, units, and whether axes are linear or logarithmic.
   - If the image contains multiple panels or overlapping series, crop the exact target panel first.
   - If the original spreadsheet/CSV/SVG source is available, use that instead of digitizing the raster image.

2. **Set calibration**
   - Use two known points on the x-axis and two known points on the y-axis. Tick marks are best.
   - Store calibration in JSON using this shape:

```json
{
  "x_scale": "linear",
  "y_scale": "linear",
  "x1": {"pixel": [120, 540], "value": 0},
  "x2": {"pixel": [820, 540], "value": 100},
  "y1": {"pixel": [120, 540], "value": 0},
  "y2": {"pixel": [120, 110], "value": 1.0},
  "roi": [120, 110, 820, 540]
}
```

   - Use `log10` for logarithmic axes. Values used for log calibration must be positive.
   - If calibration points are not obvious from the image, ask the user for the tick values and approximate pixel locations or run a visual inspection step before extraction.

3. **Extract with the bundled script for clean XY plots**
   - Use `scripts/digitize_plot.py` for clean line, scatter, and simple bar-like marks where the target pixels can be isolated by color or darkness.
   - Prefer color mode for colored series and dark mode for black curves on a white background.

```bash
python scripts/digitize_plot.py figure.png --calibration calibration.json --mode color --target "#d62728" --trace line --output extracted.csv --overlay overlay.png --excel extracted.xlsx
```

```bash
python scripts/digitize_plot.py figure.png --calibration calibration.json --mode dark --threshold 90 --trace scatter --output points.csv --overlay overlay.png
```

4. **Use interactive digitizers for difficult figures**
   - Use WebPlotDigitizer or StarryDigitizer when curves overlap, markers are hidden by error bars, gridlines share the same color as the curve, axes are rotated, or automatic extraction fails.
   - Use the same calibration and QA principles even when data is digitized interactively.

5. **QA before delivery**
   - Inspect the overlay to confirm extracted pixels match only the intended series.
   - Verify min/max values against visible tick marks.
   - Check monotonicity or expected ordering for line curves.
   - For curves, sample density should match the scientific purpose: use fewer points for trend recreation and more points for numerical integration or model fitting.
   - Report any uncertainty sources: low resolution, anti-aliased lines, hidden points, log axes, cropped ticks, or overlapping labels.

6. **Deliver outputs**
   - Provide CSV/Excel paths, calibration JSON, QA overlay, and a short note that values are digitized estimates.
   - Never present extracted values as exact original raw data unless the source data file was recovered.

## Script Reference

`scripts/digitize_plot.py` supports:

- `--trace line`: group masked pixels by x-position and output one y-value per x column.
- `--trace scatter`: connected-component extraction for markers or symbols.
- `--trace bars`: connected-component extraction with x-center, y-top, and y-bottom estimates.
- `--mode color`: isolate pixels near `--target "#RRGGBB"` with `--tolerance`.
- `--mode dark`: isolate dark pixels with `--threshold`.
- `--mode non-white`: isolate non-background colored pixels with `--threshold`.
- `--overlay`: write a QA image showing the mask and extracted points.
- `--metadata`: write extraction parameters and calibration details as JSON.

Read `references/extraction-guide.md` for figure-type decisions, calibration pitfalls, and QA rules.
