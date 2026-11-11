---
name: atlas-uv-fitting
description: Detect texture-atlas regions and map each source part to its own UV rectangle or projected UV surface. Use when a texture pack must fit a Blender model 1:1, when textures look off/stretched, when alpha decals or lightmaps are provided, or before exporting a textured GLB for a brand mascot/logo.
allowed-tools: Read Bash Glob Grep mcp__blender__execute_blender_code mcp__blender__get_object_info mcp__blender__get_objects_summary mcp__blender__get_object_detail_summary mcp__blender__render_viewport_to_path mcp__blender__search_api_docs mcp__blender_official__execute_blender_code mcp__blender_official__get_objects_summary mcp__blender_official__get_object_detail_summary mcp__blender_official__render_viewport_to_path mcp__blender_official__search_api_docs
---


## MCP backend

Use when: Texture atlas region detection, per-part UV mapping, front-projected UVs, decal/lightmap handling, texture validation against source templates.

Before the first Blender call, read [../text-to-blender/references/mcp-backends.md](../text-to-blender/references/mcp-backends.md). Prefer official MCP for shared capabilities; preserve the selected backend for the whole task. Tool names in recipes are client/legacy examples: map them through that reference and its agent-host guide.
# Atlas UV Fitting

This skill exists because assigning a texture material is not the same as fitting a texture.

## Supplemental map sanity rule

Do not blindly wire emissive/roughness/bump/lightmap images into every atlas-mapped part. First verify the supplemental map has the same UV layout and semantic region as the basecolor. If it contains aura dots, guide marks, lightmap blobs, or decorations outside the part, leave it disconnected for that mesh and use constant roughness/bump plus explicit edge/glow geometry instead.

## Hard rules

- Atlas textures must be mapped by region; never apply the full atlas to every structural mesh.
- Front-facing hero surfaces use front-projected UVs or a source-region rectangle.
- Side/back surfaces use their own UV islands or procedural/baked fills.
- Roughness, bump, normal, AO, and lightmap images are `Non-Color`.
- Alpha decals must use alpha-connected materials and no black backing planes.
- Base GLB should not include reference planes or optional aura unless explicitly requested.

## Workflow

1. Run `scripts/atlas_region_detector.py` on basecolor/decal/aura atlases.
2. Name regions semantically in `atlas_regions.json`.
3. Create/activate UV map per mesh.
4. Remap local 0-1 UVs into the matching atlas rectangle.
5. Audit the GLB/export material node graph: Principled BSDF + Image Texture nodes.
6. Render texture overlay validation before export.

## Sources distilled

- Blender UV/Image Texture node uses UV maps for rendered/exported texture output.
- Blender baking needs UV maps and active image targets.
- Blender glTF exporter is most reliable with Principled BSDF, UVs, textures, normals.
- Khronos glTF PBR: base color, metallic/roughness, normal maps are standard channels.


## Semantic atlas mapping

Region detection is only a candidate list. For source-locked work, create an `atlas_part_map.json` that binds each structural part name to exactly one atlas region or declares `procedural/no_texture`.

Mapping order:

1. Detect candidate regions from basecolor/decal/lightmap.
2. Reject decorative/aura/composite-preview regions unless the target is context/aura.
3. Match structural parts by role, aspect ratio, and relative size.
4. Manually rename ambiguous regions before automated UV assignment.
5. Verify supplemental maps share the same region layout before connecting roughness/bump/emission/lightmap.

Do not map a full rosette/composite atlas region onto individual petals unless the mesh is a single rosette sheet. Individual meshes need individual source regions.

## Additional script

- `scripts/atlas_region_mapper.py` proposes part→atlas-region mappings using aspect/size similarity. Treat output as a draft; semantic names still win.
