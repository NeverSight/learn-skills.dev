---
name: blender-shader-nodes
description: Blender 5.x shader nodes — PBR materials, procedural textures, Principled BSDF, glass/metal/skin shaders, world/HDRI lighting, raycast shader node, and scripting material node trees via Python (bpy). Includes 5.1 changes (Normal Map OpenGL/DirectX, Raycast, OpenColorIO 2.5).
---

# Blender Shader Nodes Expert

## Overview

This skill provides expert guidance for Blender 5.x shader nodes: designing material setups, writing Python scripts to build shader node trees programmatically, understanding render engine differences (Cycles vs EEVEE), and accessing the complete shader node catalog. Includes 5.0 and 5.1 changes (Raycast node, Normal Map OpenGL/DirectX toggle, OpenColorIO 2.5).

## MCP-First Approach

Prefer the **official Blender MCP Server** (Blender Lab, Blender 5.1+) for creating materials, wiring shader trees, sampling viewport renders directly in a running Blender session. Fall back to emitting Python scripts only when the MCP server is not connected.

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

- **"Create a material for X"** -> Identify the material type, design the node tree, generate Python code (see Material Recipes)
- **"My material looks wrong"** -> Follow the Debugging workflow
- **"What node does X?"** -> Consult `references/node_reference.md`
- **"Set up world lighting / HDRI"** -> See World/Environment pattern in Python API reference
- **"Script a shader node tree"** -> Consult `references/python_api.md` for API patterns
- **"Cycles vs EEVEE?"** -> Check the Render Engine Compatibility section in node_reference.md

## Generating Shader Node Trees

When creating materials via Python:

1. Read `references/python_api.md` for the correct API patterns and node type strings
2. Structure the script following this pattern:
   - Create the material with `use_nodes = True`
   - Clear default nodes
   - Add all nodes with correct type strings
   - Position nodes left-to-right (x spacing ~300, y spacing ~200)
   - Set default values on inputs
   - Create all links between nodes
   - Assign material to the target object
3. Use Frame nodes to organize complex setups into logical sections

### Node Type String Conventions

- Most shader nodes: `ShaderNode<PascalCaseName>` (e.g., `ShaderNodeBsdfPrincipled`, `ShaderNodeTexNoise`)
- Geometry input: `ShaderNodeNewGeometry` (not `ShaderNodeGeometry`)
- Color attribute: `ShaderNodeVertexColor`
- Mix node: `ShaderNodeMix` with `data_type` set to `'RGBA'`, `'FLOAT'`, or `'VECTOR'`
- Color Ramp: `ShaderNodeValToRGB`
- When uncertain about the exact type string, consult `references/python_api.md`

## Material Recipes

### PBR Material (Texture-Based)
1. Texture Coordinate -> Mapping -> Image Texture(s) -> Principled BSDF -> Material Output
2. Connect maps: Base Color (sRGB), Roughness (Non-Color), Metallic (Non-Color), Normal Map (Non-Color) -> Normal Map node -> Normal input
3. Set non-color images to `image_tex.image.colorspace_settings.name = 'Non-Color'`

### Procedural Material
1. Texture Coordinate -> Noise/Voronoi/Wave Texture -> Color Ramp -> Principled BSDF
2. Layer multiple textures using Mix nodes for complexity
3. Use Separate XYZ on Texture Coordinate for axis-dependent patterns

### Glass / Transparent
1. Principled BSDF with Transmission Weight = 1.0, Roughness = 0.0 (clear) or >0 (frosted), IOR = 1.45-1.52
2. Alternative: Glass BSDF node for simpler setup
3. EEVEE: Enable Screen Space Refraction on material and render settings

### Metal
1. Principled BSDF with Metallic = 1.0, Base Color = metal tint (gold: 1.0, 0.766, 0.336), Roughness = 0.1-0.4
2. Alternative (5.0): Metallic BSDF node for physically accurate complex IOR
3. Add fingerprints/scratches: mix Roughness with procedural texture

### Skin / Subsurface
1. Principled BSDF with Subsurface Weight = 0.3-1.0, Subsurface Radius = (1.0, 0.2, 0.1) for RGB scattering
2. Connect skin texture to Base Color, detail normal map to Normal
3. Cycles: Use Random Walk method for best quality

### Emission / Neon
1. Principled BSDF with Emission Color = desired color, Emission Strength = 1-50+
2. Or standalone Emission node -> Material Output (Surface)
3. Enable Bloom in render settings (EEVEE) for glow effect

### Toon / Cel Shading (EEVEE)
1. Principled BSDF (or any BSDF) -> Shader to RGB -> Color Ramp (Constant interpolation) -> Material Output (via Emission or custom output)
2. Color Ramp stops create discrete shading bands
3. Shader to RGB is EEVEE-only

### World / HDRI Environment
1. Environment Texture (load .exr/.hdr) -> Background -> World Output
2. Add Mapping node between Texture Coordinate (Generated) and Environment Texture for rotation
3. Set Background Strength for intensity

### Displacement
1. Texture -> Displacement node -> Material Output (Displacement socket)
2. Set material displacement method: `mat.cycles.displacement_method = 'BOTH'`
96#HB|3. Requires subdivision on the mesh (Subdivision Surface modifier or Adaptive Subdivision in Cycles)

### Raycast Node (Blender 5.1)
1. **ShaderNodeRaycast** casts a ray from the shading point and returns hit information
2. Outputs: **Position**, **Normal**, **Distance**, **Object**, **Is Hit**
3. Useful for material-driven proximity effects, occlusion, and intersection detection
4. Supports specifying ray direction and length limits
5. Works in both Cycles and EEVEE

### Normal Map Improvements (Blender 5.1)
1. New **OpenGL/DirectX** toggle for normal map tangent space convention
2. OpenGL (default) vs DirectX flip — fix inverted normal maps from game engines
3. New option to compute normal maps on the **displaced mesh** (Cycles only)
4. Use `normal_map_node.invert_y` or `normal_map_node.tangent_space_convention` to toggle

### Volume (Fog/Smoke)
1. Principled Volume -> Material Output (Volume socket)
2. Or: Volume Absorption + Volume Scatter -> Add Shader -> Material Output (Volume)
3. Set Density, Color, Anisotropy

## Debugging & Optimization

### Common Visual Issues

- **Material appears black**: Check that Material Output has a valid Surface connection. Verify the object has UV coordinates if textures require them
- **Material appears white/flat**: Missing texture connections or all textures set to wrong color space
- **Glass/transparency not working in EEVEE**: Enable Screen Space Refraction in both render settings and material settings. Set blend mode to Alpha Hashed or Alpha Blend
- **Normal map looks bumpy/wrong**: Ensure normal map image is set to Non-Color color space. Check that Normal Map node is set to correct space (Tangent for most cases)
- **Texture stretching**: Object needs proper UV unwrap. Alternatively, use Object or Generated texture coordinates with Mapping node
- **Fireflies in Cycles render**: Reduce light bounces, use Clamp Direct/Indirect in render settings, or denoise

### Performance Tips

1. **Principled BSDF over separate shaders**: The Principled BSDF is optimized internally; combining Diffuse + Glossy + Glass manually is slower
2. **Minimize texture resolution**: Use 2K textures for most cases, 4K only when close-up detail is needed
3. **Avoid excessive Noise Texture stacking**: Each noise computation is expensive. Bake complex procedural textures for animation
4. **EEVEE screen-space effects**: Screen Space Reflections, Refraction, and SSS add per-material cost. Only enable on materials that need them
5. **Simplify for viewport**: Use lower texture resolution or simpler shaders in viewport preview mode

### EEVEE vs Cycles Quick Guide

| Feature              | Cycles                     | EEVEE                          |
| -------------------- | -------------------------- | ------------------------------ |
| Rendering            | Path tracing (accurate)    | Rasterization (fast, approx.)  |
| SSS                  | Random Walk (accurate)     | Screen-space (approximate)     |
| Reflections          | Ray traced                 | Screen-space + probes          |
| Transparency         | Ray traced                 | Alpha blending / hashing       |
| Volumes              | Full volumetrics           | Limited volumetric support     |
| Displacement         | True + adaptive subdivision| Not supported (use Normal Map) |
| OSL                  | Supported (CPU only)       | Not supported                  |
| Shader to RGB        | Not supported              | Supported (toon shading)       |

## Node Reference

For the complete catalog of all shader nodes organized by category (Input, Output, Shader, Texture, Color, Vector, Converter, Script), consult `references/node_reference.md`.

Key sections to search:
- BSDF/shader types: grep for "BSDF" or "Shader" in node_reference.md
- Texture nodes: grep for "Texture"
- Principled BSDF inputs: grep for "Principled BSDF - Detailed"
- Render engine compatibility: grep for "Cycles Only" or "EEVEE"
- Blender 5.0 changes: grep for "5.0"
- Blender 5.1 changes: grep for "5.1" or "Raycast" or "Normal Map"
- OpenColorIO 2.5: Updated color management with improved display transforms

## Python API Reference

For the complete Python API patterns including node type strings, socket types, linking, material assignment, world setup, and Color Ramp configuration, consult `references/python_api.md`.
