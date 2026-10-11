---
name: spritecook-polish-sprites
description: "Inspect and polish SpriteCook sprites after generation or background removal. Use for broken or faint outlines, missing edge pixels, halos, and background debris, and before slicing or animating assets that need edge cleanup. Compare preserved alpha locally and save the selected threshold through MCP."
---

# SpriteCook Polish Sprites

Use with `spritecook-workflow-essentials`. Inspect completed sprites at their intended size and at a nearest-neighbor zoom before delivery, slicing, or animation. If the outline and transparency already look good, keep them. Use this workflow when edge cleanup could improve the result.

## Why Outlines Can Look Broken

Background removal estimates how much each pixel belongs to the subject. Thin outlines, low-contrast edges, hair, handles, and other fine details can receive partial transparency even when they belong to the sprite. Turning that soft alpha into opaque or transparent pixels with a cutoff can discard those edges. Later cleanup such as erosion can also remove pixels.

SpriteCook preserves a pre-alpha-cleanup image for supported assets. A lower cutoff can recover faint outline pixels still present in that source; a higher cutoff can remove halos and background debris. Both Basic and Pro results can benefit from inspection. Pro does not guarantee that every edge survives.

Thresholding cannot reconstruct pixels absent from the preserved source or repair a shape that was generated incorrectly. A processed PNG with only alpha 0 and 255 usually has no recoverable intermediate alpha. Always work from the preserved source, not repeatedly from an already-thresholded preview. Keep intentionally translucent effects translucent unless the user wants hard pixel edges.

If the preserved source itself has only alpha 0 and 255, all positive cutoffs produce the same transparency. That result may still differ from the saved output if later erosion removed pixels, so compare it with the saved image before deciding.

## Inspect Once, Compare Locally, Save Once

1. Call `get_asset_metadata(asset_id)` and inspect `alpha_editing`. It reports `available`, `current_cutoff`, `provider`, `processing`, `source_url`, its expiry, and preview/animation layout. If this field or `set_asset_alpha_cutoff` is missing, the connected server has not exposed this workflow yet. Do not invent a tool or silently run paid background removal instead.
2. If `available=false`, explain that the preserved source is unavailable for this asset. A fresh removal pass or a targeted image edit may be needed; follow the user's scope and credit budget. Stop this threshold workflow.
3. For `processing="binary_alpha_v1"`, download `source_url` once using the shared safe-download workflow. Also download the current `sprite_url` for stills or `spritesheet_url` for animations so the actual saved result can be compared. The URL expires; refresh metadata if necessary. Keep signed URLs out of manifests and committed files.
4. Save the metadata JSON locally and run the bundled helper with Python and Pillow available:

   ```text
   python scripts/compare_alpha.py --metadata asset.json --source preserved.png --current current.png --output-dir alpha-comparison
   ```

   Resolve the script relative to this skill's directory. Use the project's Python environment where available. Install Pillow into that environment if needed. The helper makes no network calls, spends no credits, and does not modify SpriteCook assets. It outputs `comparison.png`, full-size candidate PNGs, and `comparison.json`. It starts near the saved cutoff; use `--cutoffs 48 72 96 120 144` to choose other candidates. Use a fresh output directory for each comparison.
5. Inspect the comparison on both light and dark backgrounds, then inspect promising full-size candidates at native size. Look for continuous outlines, preserved fine parts, unwanted bridges between objects, halos, isolated debris, and lost intentional transparency. For animations, inspect every frame for flickering edges. Choose the candidate with the best balance; pixel counts alone cannot judge quality. Compare with the actual saved output, since the original cleanup may also have applied erosion or other processing.
6. If needed, make one more local comparison around the best candidate. Stop when there is a clear improvement or no useful recovery. Do not cycle through paid generation or removal jobs to tune this number.
7. When a candidate improves the result, call `set_asset_alpha_cutoff(asset_id, cutoff)` once. It updates the existing asset, saves the cutoff, retains the preserved source, and costs zero credits. Download the returned output and verify it matches the selected candidate. Record the asset ID and selected cutoff in the local asset manifest. If no candidate improves the result, keep the saved asset.

## Targeted Outline Repairs

For maximum visual fidelity, make targeted manual or scripted pixel repairs after generation when background removal has left gaps that cutoff tuning cannot fix. Compare with the original image before background removal when available: restore missing outline pixels from it, or reconstruct small, unambiguous gaps using neighboring outline colors and the existing contour. A local image editor or a small script with an explicit repair mask can help. Preserve the sprite's silhouette, outline thickness, palette, and intentional openings; avoid thickening the entire outline or filling every transparent hole automatically.

Inspect the repaired result at native size and nearest-neighbor zoom on light and dark backgrounds. For animations, check that repairs remain consistent across frames without edge flicker. Keep the original and save a separate repaired PNG. `set_asset_alpha_cutoff` saves only threshold changes, not custom pixel edits; use `spritecook-upload-assets` to upload the repaired image when it needs to be reused in SpriteCook, then animate or reference that new asset ID. Record its relationship to the original in the local manifest.

## Processing Details and Limits

- `binary_alpha_v1` preserves RGB and sets alpha to 255 when source alpha is greater than or equal to the cutoff, otherwise 0. Cutoffs range from 0 to 255. Avoid 0 for ordinary cleanup: it makes even fully transparent pixels opaque.
- The helper preserves source dimensions and does not resize or crop candidate PNGs. `preview_crop` only affects the comparison view. Saving uses the full preserved source, just like the app; check output dimensions before integrating it into a game.
- Animation sources use a horizontal PNG spritesheet with the advertised `frame_count`, `frame_width`, and `frame_height`. Use the same cutoff across frames. The helper rejects mismatched layouts and animated preview files.
- `tileset_color_tolerance_v1` uses background-color tolerance rather than alpha thresholding. The helper intentionally rejects it; use the dedicated tileset edge-cleanup editor instead of treating its cutoff as binary alpha.
- Polish a multi-object sheet before slicing when possible. Uploaded or sliced derivatives may lack the original soft-alpha source. Once the sheet looks good, slice it and animate each extracted asset separately using the existing upload and animation skills.
- Local candidates remain local until the save tool is called. Upload a candidate separately only when the user wants an independent copy. A separate upload does not inherit the original asset's editable source.
