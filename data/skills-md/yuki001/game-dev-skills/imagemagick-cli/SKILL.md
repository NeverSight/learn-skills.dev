---
name: imagemagick-cli
description: Comprehensive ImageMagick 7 command-line image processing for inspecting, converting, resizing, cropping, compositing, masking, drawing, annotating, color correction, quantization, filtering, morphology, distortion, animation, montage, comparison, metadata, batch automation, and advanced pixel analysis. Use whenever a task mentions ImageMagick, `magick`, `identify`, `mogrify`, raster image conversion or batch image manipulation, or when a reproducible CLI pipeline is preferable to a GUI or language binding. Also use for debugging ImageMagick commands, porting ImageMagick 6 `convert` syntax to version 7, choosing coder/delegate options, and safely processing untrusted or large images. Do not use merely to edit an existing SVG as vector source or when the user explicitly requests a different image tool.
---

# ImageMagick CLI

Use ImageMagick 7 to build, run, and verify reproducible image-processing commands. Keep the main workflow short; load the bundled reference that matches the requested operation.

## Workflow

1. Resolve `magick` and run `magick -version`. Use `scripts/resolve-imagemagick.ps1` on Windows or `scripts/resolve-imagemagick.sh` on Linux/macOS when discovery is uncertain. If ImageMagick cannot be found, tell the user to download and install it from [https://imagemagick.org/download](https://imagemagick.org/download).
2. Inspect the input with `magick identify -ping` or `magick identify -verbose` when metadata, alpha, profiles, pages, or frames matter.
3. Read the relevant reference below, construct an ImageMagick 7 command for the user’s shell, and preserve originals unless in-place editing is explicit.
4. Run the command when requested, check the exit code, then verify the output with `identify`, `compare`, and visual inspection as appropriate.

## Core rules

- Use ImageMagick 7 syntax: `magick input [operators] output` and subcommands such as `magick identify`, `magick mogrify`, `magick montage`, `magick compare`, and `magick stream`.
- Respect sequential evaluation. Put read settings such as `-density`, raw `-size`, and decoder `-define` values before the input they affect.
- Quote all paths and shell-sensitive geometry. Use parentheses to isolate operations on overlays, masks, clones, or other nested image lists.
- Treat `magick mogrify` as destructive unless `-path` writes to a separate directory.
- Run `-auto-orient` before geometry-sensitive work on camera images.
- Use `+repage` after crop or trim when later operations should ignore the old virtual canvas.
- Manage alpha, colorspace, profiles, animation timing, and multi-page scenes deliberately; do not silently discard them.
- Confirm optional formats, fonts, delegates, policies, compose methods, and kernels with the installed `magick -list ...` commands.
- For untrusted or very large inputs, use format allowlists and limits for area, memory, map, disk, time, and threads.
- Verify outputs instead of relying on file existence alone.

## Shell forms

PowerShell:

```powershell
$magick = (Get-Command magick -ErrorAction Stop).Source
& $magick "input image.png" -auto-orient -resize "1600x1600>" "output image.jpg"
```

Pass parentheses as literal arguments:

```powershell
& $magick "background.png" "(" "overlay.png" -resize "25%" ")" `
  -gravity southeast -geometry "+24+24" -compose over -composite "result.png"
```

Bash/zsh:

```bash
magick "input image.png" -auto-orient -resize '1600x1600>' "output image.jpg"
magick background.png \( overlay.png -resize 25% \) \
  -gravity southeast -geometry +24+24 -compose over -composite result.png
```

Prefer PowerShell over `cmd.exe` for complex Windows commands. In cmd batch files, use `^` for continuation and double `%` characters.

## Command references

- `references/cli-foundations.md` — evaluation order, settings and operators, stacks, geometry grammar, pseudo-images, streams, shell quoting, and IM6-to-IM7 conversion.
- `references/inspect-formats-metadata.md` — `identify`, percent escapes, EXIF/profiles, format prefixes, multi-image I/O, common and specialist coders, delegates, encrypted images, raw data, and large streams.
- `references/geometry-resize-crop.md` — fit/fill/exact resize, thumbnails, resampling filters, density, orientation, crop/page/extent, advanced trim, borders, tiling, and framing.
- `references/color-tone-quantize.md` — colorspaces, ICC, channels, alpha, grayscale, levels, histogram operations, thresholds, palettes, and dithering.
- `references/compose-mask-layers.md` — compose operators, placement, opacity, alpha/read/write masks, background removal, chroma key, hole filling, regions, clones, layers, watermarks, and shadows.
- `references/draw-text-canvas.md` — canvases, gradients, patterns, fonts, label/caption/annotate, Pango, form filling, gravity, symbols, MVG, paths, and text effects.
- `references/filters-effects-morphology.md` — blur, sharpen, denoise, convolution, edge/Hough detection, morphology kernels and pattern matching, deskew, CLAHE, shade, and photographic effects.
- `references/distort-map-fx.md` — affine/SRT, perspective, lens correction, control points, virtual pixels, displacement/absolute/variable-blur maps, `-evaluate`, `-function`, `-fx`, and sparse color.
- `references/animation-montage-compare.md` — frame metadata, coalesce/disposal, animation edits/merging/optimization, video palettes/deinterlacing, contact sheets, metrics, diffs, and subimage search.
- `references/batch-performance-security.md` — safe PowerShell/Bash batching, `mogrify`, naming, resource limits, concurrency, policies, temporary files, and failure logs.
- `references/advanced-analysis.md` — histograms, pixel enumeration, connected components, convex hull, classification heuristics, kernels, FFT/HDRI, raw streaming, and calculated options.
- `references/photo-thumbnail-effects.md` — digital-photo cleanup, selective focus/anonymization, multiple exposures, green screen, sketch/vignette work, thumbnail decoration, reflections, and constructed lighting effects.
- `references/options-index.md` — on-demand alphabetized CLI option signatures. Search for the exact option; do not read the index end to end.
- `references/defines-index.md` — on-demand `-define` keys grouped by coder or operation. Search for the coder/prefix or exact key; do not read the index end to end.

For large indexes, search before reading the entire file:

```text
options-index.md:  ^### -resize\b
defines-index.md:  png:|jpeg:|compare:|connected-components:
```

## Verification patterns

```bash
magick identify -format '%f|%m|%wx%h|%z-bit|%[colorspace]|%[channels]|%n\n' output.png
magick identify -format '%s|%T|%D|%wx%h|%[page]\n' animation.gif
magick compare -metric RMSE expected.png actual.png null:
```

Comparison metrics commonly write to stderr, and a nonzero compare status can mean that images differ. Capture the metric and diagnostic text separately in automation.

## Response style

- State assumptions that affect pixels, cropping, transparency, metadata, colorspace, or animation behavior.
- Give commands for the user’s actual shell.
- Explain only the non-obvious ordering or operators.
- Warn before destructive `mogrify` use.
- Include verification for batch, lossy, animated, color-managed, multi-page, or security-sensitive work.
