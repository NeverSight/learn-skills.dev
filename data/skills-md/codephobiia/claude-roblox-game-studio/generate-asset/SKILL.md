---
name: generate-asset
description: Generate a 3D asset for Roblox using Blender MCP. Creates models from text descriptions via AI (Hyper3D/Hunyuan3D) or downloads from PolyHaven/Sketchfab, optimizes for Roblox constraints, and exports FBX.
---

# /generate-asset — 3D Asset Generation

## Delegate to: blender-mcp-operator

## Steps

### 1. Gather Requirements
Ask:
- "What asset do you need?" (weapon, prop, character, environment piece, vehicle)
- "What style?" (low-poly, stylized, realistic, cartoon, sci-fi, fantasy)
- "Triangle budget?" (default: <5000 for props, <10000 for hero assets)
- "Any reference?" (image, description, similar game)

### 2. Choose Source
- **AI generation** (no reference exists): `mcp__blender-mcp__generate_hyper3d_model_via_text`
- **From reference image**: use `/asset-from-image` instead
- **From library** (generic asset): `mcp__blender-mcp__search_polyhaven_assets` or `search_sketchfab_models`

### 3. Generate / Download
- For AI: submit prompt, poll `get_hyper3d_status` until complete, `import_generated_asset`
- For library: download and import into Blender scene

### 4. Inspect
- `mcp__blender-mcp__get_viewport_screenshot` — visual review
- `mcp__blender-mcp__get_object_info` — check triangle count, dimensions, materials

### 5. Optimize for Roblox
Via `mcp__blender-mcp__execute_blender_code`:
- Decimate to target triangle budget
- Scale to Roblox units
- Set origin to base center
- UV unwrap if needed
- Apply clean topology (remove doubles, fix normals)

### 6. Export
- Export as FBX to `assets/models/<asset-name>.fbx`
- Verify file size

### 7. Preview and Approve
- `mcp__blender-mcp__get_viewport_screenshot` — final screenshot
- Present to user with: poly count, texture resolution, dimensions, screenshot
- Wait for approval before finalizing
