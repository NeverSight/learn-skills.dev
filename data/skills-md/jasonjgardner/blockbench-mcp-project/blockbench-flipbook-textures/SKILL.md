---
name: blockbench-flipbook-textures
description: Create animated flipbook textures for Blockbench and Minecraft using blockbench-gpt-image-textures and GPT Image 2.5. Plan frame dimensions and motion, generate a sprite sheet, repack grids or horizontal sheets into a vertical PNG, and configure animation playback and target metadata. Use for animated block textures, looping texture effects, or sprite-sheet-to-flipbook conversion.
---

# Blockbench Flipbook Textures

Deliver a vertical PNG containing equal-sized animation frames, with verified timing and the metadata needed by the requested target. For `N` frames of `W × H` pixels, the final bitmap is **`W × (H * N)`**, frame 0 at the top, with no gutters between frames. Each frame is a complete tile or complete UV atlas.

## Required Skills and Tools

- Load [blockbench-use](../blockbench-use/SKILL.md) before Blockbench content changes and [blockbench-texturing](../blockbench-texturing/SKILL.md) for UV inspection and assignment.
- **Use [blockbench-gpt-image-textures](../blockbench-gpt-image-textures/SKILL.md) whenever generating or repainting the artwork.** Use its GPT Image 2.5 Flare/Sunburst workflow and scripts, including its `FAL_KEY` handling. Do not silently substitute a different image model. If the dependency or model is unavailable, explain the missing capability and continue layout/conversion work that does not depend on generation. Converting an existing supplied sheet does not require another generation call.
- Use Python 3.10+ and Pillow for the bundled converter (`python -m pip install Pillow` in the chosen environment). ImageMagick is also suitable for measured crops and vertical assembly; preserve full frame bounds, explicit numeric order, and alpha.

Resolve script paths relative to the installed skills, not the working directory. Commands below assume the current directory is this skill's folder; keep outputs in the user's asset workspace.

## 1. Establish the Animation Contract

Reuse requirements already given. Clarify missing choices that change the result before generating: subject/effect, pixel-art or painted style, **per-frame** pixel size, frame count, duration/FPS or ticks per frame, loop versus one-shot, transparency, spatial tiling, and destination (Blockbench preview, Java resource pack, Bedrock block, or entity). Do not infer that a supplied sheet size is a frame size. If only the timing is unspecified, propose 2 ticks/frame (10 FPS) and state that assumption.

Keep these quantities separate:

| Quantity | Meaning |
|---|---|
| `W, H` | Final pixels in one frame; use square frames for ordinary Minecraft block tiles |
| `N` | Number of physical frames in the exported strip |
| `U, V` | Logical UV dimensions for one complete frame; may differ from `W, H` |
| `C, R` | Columns and rows of the generated source sheet, with `C * R >= N` |
| `S` | Integer generation upscale; source cells are `W*S × H*S` |
| `T` | Positive integer ticks per frame for Minecraft metadata; FPS = `20/T` |

For a simple sequential cycle, duration is `N*T/20` seconds. A custom playback schedule changes that duration. Explain tick rounding when requested FPS cannot be represented exactly; retain the chosen value in preview and export. Standard Minecraft texture metadata loops; one-shot playback requires target-specific control rather than a made-up loop flag.

For an existing model, inspect `get_capabilities`, `list_textures`, and relevant `get_cube_uv` / `get_mesh_info` results. Preserve the one-frame UV layout and proportions in every frame. A standalone tiling texture needs an explicit full-cell layout, not invented geometry or a throwaway model. Bone/keyframe animation is a separate workflow.

## 2. Generate the Sheet with GPT Image 2.5

Load the required GPT image texture skill and its [API constraints](../blockbench-gpt-image-textures/references/fal-api.md). Apply its layout-aware prompting **inside each frame**, then repeat that layout at each source-cell offset. For standalone tiles, the whole cell is the layout. Keep the existing model's UVs unchanged when describing the temporary sheet grid.

Prefer a vertical source sheet only when the generator can represent its aspect ratio and resolution. Otherwise choose a compact grid. The verified fal custom-size limits are multiples of 16, at least 655,360 and at most 8,294,400 pixels, longest edge 3840, and aspect ratio at most 3:1; recheck the dependency's current API reference when needed. An upscale cannot fix an excessive aspect ratio. Choose a different grid, measured outer padding, or explicitly planned batches without changing the requested final dimensions. See the [fal schema](https://fal.ai/models/openai/gpt-image-2.5/flare/text-to-image/api).

Read [sheet prompting](references/sheet-prompting.md) for the prompt structure, coordinate math, and a 16-frame example. Explicitly specify:

- Exact canvas and cell rectangles; row-major chronological order (left to right, then top to bottom), used cells, and unused trailing cells.
- Fixed camera, framing, object anchor, scale, palette, lighting, and shared UV island positions. Describe each frame's motion phase, not independent variations of the subject.
- A seamless last-to-first transition for loops; sample phases `i/N` rather than including both 0 and 1 unless an intentional hold calls for a duplicate. Request spatially seamless edges separately when the texture must tile.
- Full-cell coverage for opaque tiles, or real alpha for transparent sprites. No labels, dividers, captions, decorative borders, or baked checkerboard.

Generate using the dependency's script, for example:

```bash
bun ../blockbench-gpt-image-textures/scripts/fal_gpt_image.mjs --prompt-file /path/to/prompt.json --model flare --width 1024 --height 1024 --background transparent --quality medium --num 1 --format png --out /path/to/output --label portal_sheet
```

Use an opaque background for an opaque tile. Save the prompt and downloaded original. Inspect the **actual** returned dimensions, layout, frame content, and alpha before conversion. An exact API canvas size does not enforce accurate cell boundaries. If substantial content is missing, overlapping, or inconsistent, correct the prompt or edit the relevant artwork with the required generation skill; slicing cannot repair motion. Do not repeatedly regenerate without diagnosing the mismatch.

## 3. Normalize to a Vertical Flipbook

For a verified 1024×1024 source with a 4×4 grid of 256×256 cells, targeting sixteen 32×32 frames:

```bash
python scripts/sheet_to_flipbook.py /path/to/source.png /path/to/portal.png --grid 4 4 --count 16 --frame-width 32 --frame-height 32 --ticks-per-frame 2 --preview /path/to/portal-preview.apng
```

This produces a **static 32×512 RGBA PNG**, an optional looping APNG for inspection, and a JSON report on stdout. The APNG is a preview, not the texture imported into Blockbench or Minecraft. Capture stdout to a report file when handing off assets. The converter does not write game metadata.

- Already vertical: use `--grid 1 N`; horizontal: `--grid N 1`. If the vertical source already has the exact dimensions, order, and alpha, use it directly after validation.
- Unused trailing cells: use `--count N`. Nonsequential or repeated physical frames: use `--indices 0,1,2,1` instead of `--count`. These indices select **source cells**; game metadata indices address the **resulting strip**. Do not apply the same reordering twice.
- Outer padding or consistent gutters: measure `--crop X Y W H` for the grid bounds and `--gap X Y` between cells. All units are source-image pixels.
- Irregular placement: pass `--rects /path/to/rectangles.json`, a JSON array such as `[[8,8,256,256],[280,8,256,256]]`, ordered chronologically. Rectangles must have equal dimensions and remain within the source. Measure complete cells with consistent anchors; independently trimming each sprite's opaque bounds introduces jitter.
- Pixel art: the default nearest-neighbor sampling preserves hard edges. Painted art: use `--resample lanczos`. Each frame is cropped **before** resizing. Never resize the entire grid into a narrow strip.
- Preserve alpha by default. Use `--alpha-threshold 128` only when binary cutout alpha is intended. Do not threshold smoke or soft glows. Alpha snapping cannot remove an opaque generated background.

The helper rejects fractional cells, aspect-ratio changes, invalid indices, and source overwrites. Existing outputs need `--overwrite`. For a measurement error, fix the layout inputs; do not bypass validation by guessing crops or stretching cells.

## 4. Import, Configure, and Verify

Read [Blockbench and Minecraft delivery](references/blockbench-and-minecraft.md) when importing or producing runtime metadata. Discover the active format's `animated_textures`, `per_texture_uv_size`, and `texture_mcmeta` capabilities. Preserve the intended project and use available MCP tools/native dialogs.

Import the static strip with `create_texture` and assign it only to the intended elements. In formats supporting per-texture UV sizes, supply the established one-frame `uv_width=U`, `uv_height=V`; **never use the strip height as the one-frame UV height**. Other formats use project UV dimensions, so check their effect on existing textures before changing them. Configure timing through supported texture properties/animation UI; do not assume a nonexistent `set_flipbook` tool or pass undocumented parameters to `create_texture`.

Verify the following before delivery:

- PNG dimensions are exactly `W × H*N`; each full frame is correctly oriented and ordered, with stable anchors and appropriate alpha.
- `list_textures` reports `bitmap_size=[W,H*N]`, `frame_size=[W,H]`, and the intended `uv_size=[U,V]`. Verify the frame count using bitmap height / frame height.
- Inspect the APNG and several actual Blockbench frames, including last-to-first. Check clipping, temporal flicker, unwanted duplicates, shifting UV islands, spatial seams, and filtering at the intended viewing size. A static screenshot alone does not prove playback.
- Match the target metadata to the exported PNG and verify in the target runtime when available. Java uses `.png.mcmeta`; Bedrock **blocks** use `textures/flipbook_textures.json` plus the texture atlas binding. Bedrock entities require their own UV animation/material setup.

Deliver the strip, requested metadata, source prompt/sheet, conversion report, and optional preview with concise dimensions/count/timing. State which previews and runtime checks actually ran. For PBR animations, all channels need the same frame geometry/order/timing; process frames separately to avoid filters mixing adjacent frames.
