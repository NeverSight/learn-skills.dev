---
name: product-color-match
description: Match the color of a product photo to a user-approved reference, preview localized corrections, and process a confirmed group of product images while protecting product details and backgrounds. Use for 商品颜色对齐、商品图色差统一、商品参考图校色 and e-commerce product color consistency, including camera RAW files; not for inventing new product colorways.
---

# 商品色准

Use an approved reference photo or explicitly selected color sample to bring the corresponding area of a product image closer to that reference. Work for any product category, but do not assume all photos, finishes, colors or lighting conditions are interchangeable.

## Workflow

1. Inspect the complete group and identify the reference, each target, product/color grouping, lighting and material. Preserve the originals. Generate previews with longest edge at most 1200 pixels for visual inspection. If the reference or matching product/color is ambiguous, ask; never infer that a reference photo is physically color-accurate.
2. For RAW inputs, run `scripts/raw_preview.py` first to produce a preview no larger than 1200 pixels and determine the developed dimensions. RAW files are developed with camera white balance, no automatic brightening and sRGB output; assess exposure and white balance before color alignment. Coordinates and masks must match the fully developed, orientation-corrected image, not the downsized preview. Do not overwrite the RAW. Camera/format support depends on LibRaw.
3. Select a representative target and a normally lit, uniform reference patch away from shadows, glare, text and other colors. Record pixel coordinates at the original reference resolution; explain the selected area and let the user correct it. If the user has not supplied a selection, propose a reasonable one and show it in the sample preview.
4. Establish a target mask: white means adjust, black means protect, grey means partial effect. Use a supplied mask or a suitable available local selection/segmentation tool, then visually inspect its alignment. Explicitly protect labels, text, hardware, background and other colors. Do not pretend that a generic image editing model preserves the product exactly. If a trustworthy mask cannot be created, request one or a clear way to select the target; do not silently apply a global transform.
5. Create a single sample with `scripts/match_product_color.py`. Start conservatively, preserving brightness and texture. Show a small before/after preview and the selected region; ask for the user's judgment before batch processing. Adjust intensity or the selected reference patch based on feedback. Preserve each iteration.
6. After sample approval, process the same confirmed product/color group. Use and verify an appropriate mask for each target; do not reuse a mask across different framing. Inspect each result for spill, edges, label changes, texture and clipping. Mark difficult images for individual review. Deliver completed files without waiting for optional refinements.
7. Report output file links, pixel dimensions, format, quantity and check outcome. Preserve source files, metadata/color assumptions and reference/target selections in a brief report. State clearly this is visual alignment to the chosen photo, not certified real-world color accuracy.

## Local helper

The scripts require Python 3, Pillow, NumPy, rawpy and tifffile (`requirements.txt`). Install these requirements in a suitable Python environment before use; local `.venv` files are not included in the repository. Use an existing environment; if unavailable, use the configured workspace dependency runtime or explain the missing dependencies. Never automatically install network packages without need.

```
python scripts/match_product_color.py --reference reference.jpg --reference-box 100,150,220,260 --target target.jpg --mask target-mask.png --output output.tiff --strength 0.65
```

The box is `left,top,right,bottom` in original reference pixels, right/bottom exclusive. Mask dimensions must match target; alpha, if present, is used as the mask, otherwise luminance. The helper accepts common RAW extensions when supported by LibRaw, JPEG, PNG, and 16-bit RGB TIFF. RAW and 16-bit TIFF targets must be saved as 16-bit TIFF; 8-bit sources may use PNG or TIFF. RAW develops directly to 16-bit display-referred sRGB using camera white balance and no automatic brightening; this is a rendered image, not a RAW/DNG or scene-linear output. For 16-bit TIFF input, orientation must be normalized and the profile must be sRGB or absent; untagged input is assumed sRGB. Tagged 8-bit input is converted to sRGB. The helper applies an approximate RGB chroma adjustment under the mask, preserves source luminance approximately, and does not reconstruct clipped color or perform device calibration. Output includes an sRGB profile. Convert preview coordinates to full developed-image coordinates and use a full-size aligned mask. Output must be a new file. Inspect clipping, boundaries and labels visually; numerical consistency is not proof of visual fidelity.

Do not promise a single LUT can selectively distinguish product, label, skin and background. Transparent, metallic, fluorescent, patterned or highly reflective surfaces and mixed light require extra review; severe clipping cannot be reliably recovered. Do not invent masks, reference regions or claim real-camera/colorimetric validation.
