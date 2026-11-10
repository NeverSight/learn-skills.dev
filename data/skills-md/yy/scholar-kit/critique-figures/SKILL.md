---
name: critique-figures
user_invocable: true
description: Critique academic figures for print quality, accessibility, legibility, visual encoding, and statistical presentation. Use when reviewing figures or preparing a manuscript for submission.
---

# Critique academic figures

Review the rendered figures. Do not modify figures or source code unless the user asks for changes.

## Find and render the figures

Use paths supplied by the user. Otherwise, resolve figures from the manuscript's TeX tree, including `\includegraphics`, `\includesvg`, `\includestandalone`, and figure-related `\input` commands. Ask only when multiple manuscript entrypoints remain plausible or the resolved set is unexpectedly broad.

Render each figure at its likely final dimensions when possible. Inspect multi-panel figures panel by panel and refer to specific panel labels in the findings.

## Programmatic checks

Inspect file type, pixel dimensions, and intended display size. Judge format by content rather than extension:

- Expect raster output for photographs, microscopy, medical imaging, satellite imagery, screenshots, and other pixel-native data.
- Estimate effective DPI at final size. Treat roughly 300 DPI for photographic content and 600 DPI for rasterized line art as heuristics, not automatic verdicts.

### Raster plots and line art

Treat a raster-only plot, chart, diagram, network visualization, line-art figure, or other text-heavy graphic as a submission blocker, even when it looks acceptable on screen or reports high DPI. Require a native vector export such as PDF, SVG, or EPS regenerated from the figure source. Renaming a bitmap, embedding it in a PDF, or auto-tracing it does not satisfy this requirement.

Allow raster content when the underlying data are pixel-native, including photographs, microscopy, medical imaging, satellite imagery, and screenshots. Mixed figures are acceptable only when text, axes, lines, and other drawn elements remain vector while the intentionally raster panels have adequate effective resolution.

For PDF figures, inspect embedded images with:

```bash
pdfimages -list <figure.pdf>
```

Embedded raster components are not failures by themselves. Distinguish intentional mixed figures from PDFs that merely wrap a rasterized plot. If `pdfimages` is unavailable, note the skipped check and continue.

## Review criteria

Review only the dimensions that apply to each figure:

- Subpanels: flag multi-panel figures without clear panel labels, and identify the affected panel in each finding.
- Legibility: flag text below roughly 8 pt at final size or noticeably smaller than the manuscript's caption text. Also inspect symbols, line weights, legends, and annotation density.
- Color: flag red and green as primary distinguishing colors and any encoding that relies on color alone. Recommend a colorblind-safe palette plus shape, line style, pattern, or direct-label redundancy.
- Categories: flag more than 5–6 categories distinguished by color in one panel. Recommend grouping, faceting, direct labeling, or emphasizing a smaller subset.
- Statistical communication: axes, scales, units, uncertainty, and visual emphasis relative to the claim.
- Overplotting: flag scatterplots when overlap makes structure or density impossible to discern. Recommend transparency, smaller marks, binning, density contours, or faceting.
- Dynamite plots: flag bars with error bars used to summarize continuous data. Recommend point-range, strip, or violin plots, with individual observations when feasible.

## Report

Prioritize material findings instead of emitting a pass/fail table for every possible check. Label raster-only plots, diagrams, and line art as blockers. For each issue, identify the file and panel, describe the visible evidence, explain its effect, and give a concrete recommendation. Separate definite problems from judgments that depend on final size or venue requirements. State plainly when no material problem is visible.
