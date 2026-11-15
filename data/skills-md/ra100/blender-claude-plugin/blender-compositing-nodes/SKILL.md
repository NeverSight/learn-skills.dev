---
name: blender-compositing-nodes
description: Blender 5.x compositor nodes — post-processing, color grading, denoising, keying, glare, depth of field, render pass separation, multi-layer EXR output, and scripting compositing pipelines via Python (bpy). Includes 5.1 changes (Sequencer Strip Info, Mask to SDF, Mix node alpha improvements).
---

# Blender Compositing Nodes Expert

## Overview

This skill provides expert guidance for Blender 5.x compositor nodes: designing compositing pipelines, writing Python scripts to build compositor node trees, combining and processing render passes, color grading, keying, and configuring multi-layer output. The reference files contain the full node listing and Python API patterns.

## MCP-First Approach

Prefer the **official Blender MCP Server** (Blender Lab, Blender 5.1+) for building compositor trees, adjusting passes, previewing renders directly in a running Blender session. Fall back to emitting Python scripts only when the MCP server is not connected.

**Detection:** at session start, look for tools whose names match `execute_blender_code`, `get_objects_summary`, or `search_api_docs` — these belong to the official `blender-mcp` server. If any are present, MCP is available.

**Tools used by this skill:**

- `execute_blender_code` — run `bpy` Python in the live session (primary action)
- `get_objects_summary`, `get_object_detail_summary` — inspect scene state before mutating
- `get_blendfile_summary_datablocks` / `_missing_files` / `_of_linked_libraries` / `_path_info` / `_usage_guess` — inventory the file
- `search_api_docs`, `get_python_api_docs`, `search_manual_docs` — confirm correct API/operator names before calling them
- `get_screenshot_of_window_as_image` / `_as_json`, `get_screenshot_of_area_as_image` — verify visual results
- `jump_to_tab_by_name`, `jump_to_tab_by_space_type`, `jump_to_view3d_object_by_name`, `jump_to_view3d_object_data_by_name` — drive the UI to make changes visible
- `render_thumbnail_to_path`, `render_viewport_to_path` — capture quick visual feedback

**Workflow:** inspect with a `get_*` / `search_*` tool → mutate via `execute_blender_code` → verify with a screenshot or summary tool. Keep code blocks small and idempotent so failures are easy to localize.

Setup: see [docs/blender-mcp-setup.md](../../docs/blender-mcp-setup.md).

## Task Decision Tree

- **"Set up compositing for X"** -> Design the node tree, then generate Python code (see Compositing Recipes)
- **"Denoise my render"** -> See Denoise recipe
- **"Color grade my render"** -> See Color Grading recipe
- **"Key out green screen"** -> See Keying recipe
- **"Add glare/bloom"** -> See Glare recipe
- **"Separate render passes"** -> See Render Pass Separation recipe
- **"Save to multi-layer EXR"** -> See File Output recipe
- **"What compositor node does X?"** -> Consult `references/node_reference.md`
- **"Script a compositor tree"** -> Consult `references/python_api.md` for API patterns

## Generating Compositor Trees

When creating compositor setups via Python:

1. Read `references/python_api.md` for the correct API patterns and node type names
2. Structure the script following this pattern:
   - Enable compositor use on the scene: `scene.use_nodes = True`
   - Access the compositor node tree: `tree = scene.node_tree`
   - Clear default nodes
   - Add all nodes with correct type strings
   - Position nodes left-to-right (x spacing ~300, y spacing ~200)
   - Set default values on node inputs
   - Create all links between nodes
   - Enable required render passes on the view layer
3. Use Frame nodes to organize complex setups into logical sections

### Node Type String Conventions

- Most compositor nodes: `CompositorNode<PascalCaseName>` (e.g., `CompositorNodeRLayers`, `CompositorNodeComposite`)
- When uncertain about the exact type string, consult `references/python_api.md`

## Compositing Recipes

### Denoise

1. Render Layers → Denoise node → Composite
2. Connect: Image → Image, Denoising Normal → Normal, Denoising Albedo → Albedo
3. Enable denoising data passes: `view_layer.use_pass_denoising_normal = True`, `view_layer.use_pass_denoising_albedo = True`
4. Use the built-in Denoise node (OpenImageDenoise) for best quality
5. For Cycles, prefer the built-in render denoiser (`scene.cycles.use_denoising = True`) for simpler setups

### Color Grading

1. Render Layers → Color Balance (Lift/Gamma/Gain or Offset/Power/Slope) → Composite
2. Add Hue/Saturation/Value for saturation adjustments
3. Add Color Curves (RGB Curves) for fine control over tone curves
4. Chain: Render Layers → Bright/Contrast → Color Balance → Hue Sat → Curves → Composite
5. Use Split Viewer to compare before/after

### Keying (Green/Blue Screen)

1. Image/Movie Clip → Keying node → Composite
2. Set Key Color to the screen color (use eyedropper)
3. Adjust: Pre Blur, Screen Balance, Clip Black/White, Despill Factor/Balance
4. For challenging keys: Image → Keying Screen → Keying node
5. Add Dilate/Erode to clean matte edges
6. Add Blur (Gaussian) on the matte for soft edges
7. Combine: Set Alpha → Alpha Over (foreground over background plate)

### Glare (Bloom/Streaks/Fog Glow)

1. Render Layers → Glare → Composite
2. Glare types: `'BLOOM'`, `'STREAKS'`, `'FOG_GLOW'`, `'GHOSTS'`
3. Key settings: Threshold (lower = more glow), Quality (High for final), Mix (blend amount)
4. For selective bloom: Separate highlights first with Color Ramp or Math (> threshold)

### Depth of Field (Post-Process)

1. Render Layers → Defocus node → Composite
2. Connect Z pass to Z input (enable Z pass: `view_layer.use_pass_z = True`)
3. Set f-Stop, Max Blur, Threshold
4. Prefer camera DOF over post-process Defocus for Cycles (better quality)
5. For EEVEE, camera DOF is recommended over compositor DOF

### Lens Distortion

1. Render Layers → Lens Distortion → Composite
2. Distortion: barrel (-1 to 0) or pincushion (0 to 1)
3. Enable "Fit" to avoid black borders
4. Dispersion: chromatic aberration (subtle values like 0.01-0.05)

### Vignette

1. Ellipse Mask → Blur (Gaussian) → Mix (Multiply) → Composite
2. Or: Lens Distortion with just Dispersion for subtle vignette
3. Adjust mask size/position to control vignette shape

### Film Grain

1. Render Layers → Mix → Composite
2. Generate noise: value node + Noise Texture (or use image-based grain)
3. Mix mode: Overlay or Add at low factor (0.05-0.15)

### Render Pass Separation

1. Render Layers node exposes all enabled passes
2. Enable passes: Diffuse Color/Direct/Indirect, Glossy Color/Direct/Indirect, Transmission, Emission, Environment, AO, Shadow, Mist, Normal, Z
3. Process each pass independently (e.g., boost Glossy, desaturate Diffuse)
4. Recombine: Add Shader passes, then Multiply with Color passes

### Multi-Layer EXR Output

1. Render Layers → File Output node (set to OpenEXR Multilayer)
2. Add input sockets for each pass to save
3. Set base path and file name
4. Each input becomes a layer in the EXR
5. For separate files: use File Output with per-socket file paths

### Sequencer Strip Info (Blender 5.1)
1. **CompositorNodeStripInfo** outputs timing metadata from VSE strips (new in 5.1)
2. Outputs: **Frame**, **Strip Start**, **Strip End**, **Strip Duration**, **Speed Factor**
3. Useful for driving compositor effects based on clip timing
4. Requires an active sequencer strip in the scene

### Mask to SDF (Blender 5.1)
1. **CompositorNodeMaskToSDF** converts a binary mask to a signed distance field (new in 5.1)
2. Outputs: **SDF** (signed distance values, negative inside, positive outside)
3. Useful for creating smooth edges on masks, variable-width outlines, and glow effects
4. Combine with Math nodes to threshold or adjust the SDF width
### Fog/Mist

1. Enable Mist pass: `view_layer.use_pass_mist = True`
2. Configure mist in Scene Properties → World → Mist Pass (Start, Depth, Falloff)
3. Render Layers (Mist) → Color Ramp → Mix (with fog color) → Composite

### Cryptomatte

1. Enable Cryptomatte passes in view layer
2. Add Cryptomatte node in compositor
3. Pick objects/materials in the Viewer
4. Outputs: Image (extracted), Matte (mask), Pick (ID visualization)
5. Use the matte for selective post-processing

## Debugging & Optimization

### Common Issues

- **Compositor not running**: Ensure Use Nodes is checked in compositor header and Compositing is enabled in Post Processing (Render Properties)
- **Black output**: Check that Render Layers node is connected to Composite node. Ensure scene has been rendered (compositor works on render result)
- **Wrong pass data**: Verify the pass is enabled in View Layer Properties. Re-render after enabling passes
- **Backdrop not showing**: Enable Backdrop in compositor header. Connect a Viewer node
- **Slow compositing**: Reduce preview resolution. Use "Fast Gaussian" blur type. Disable unused nodes

### Performance Tips

1. Use Viewer node to preview intermediate results without full recomposite
2. Mute unused branches (Ctrl+M)
3. Use lower quality settings during iteration, switch to High for final render
4. For animation, prefer render-level denoising over compositor denoising (faster)
5. File Output node adds minimal overhead — use it freely for pass debugging
6. Mix node: up to 2x faster in 5.1 for alpha-aware blending operations

## Node Reference

For the complete catalog of all compositor nodes organized by category (Input, Output, Color, Filter, Converter, Matte, Vector, Distort), consult `references/node_reference.md`.

Key categories to search:
- Color adjustments: grep for "Color" or "Balance" or "Curves"
- Blur/filter effects: grep for "Blur" or "Filter"
- Keying/matte: grep for "Key" or "Matte"
- Render passes: grep for "Render Layers" or "pass"
- Output: grep for "File Output" or "Composite"
- Blender 5.1 changes: grep for "5.1" or "Strip Info" or "SDF"

## Python API Reference

For the complete Python API patterns including compositor node type strings, tree setup, render pass enabling, and File Output configuration, consult `references/python_api.md`.
