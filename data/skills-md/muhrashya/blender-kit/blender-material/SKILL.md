---
name: blender-material
description: "Use when creating or fixing materials that must export to a game engine - Principled-only PBR, palette materials, emissive or glow, transparency modes, texture slots, color spaces, texture naming. Triggers: material, color, metal, glow, emission, transparent, PBR, palette, shader, texture slots."
---
# Material (exportable PBR only)

## Requires
UVs done (blender-uv-bake). engine.md Materials rows (workflow, channel packing, normal map convention, color spaces, transparency).

## Inputs
Style (palette or PBR) | list of materials from ref-analysis section 6 | glow/transparency needs.

## Steps
1. LIST materials: one per surface type; merge identical ones (fewer materials = fewer draw calls).
2. BUILD with `references/pbr-minimum.md`: Principled BSDF + Image Texture nodes only; no node groups, no procedural nodes in the exported material (bake them first).
3. SLOTS: base color (sRGB), normal (Non-Color + Normal Map node), roughness/metallic/AO (Non-Color); packing only if engine.md lists the channel order.
4. PALETTE styles: single material with the palette texture, nearest filtering note in the report.
5. EMISSIVE: emission color/strength per pbr-minimum; engine support from engine.md.
6. TRANSPARENCY: pick the mode that engine.md lists (opaque / cutout / blend); default opaque.
7. NAMES: `MAT_<Asset>_<Part>`, textures `T_<Asset>_<Slot>`.
8. AUDIT: `audit_naming.py`; list node types per material (pbr-minimum section 4); screenshot with a neutral light.

## Hard rules
| Rule | Detail |
|---|---|
| Principled only | exporters read Principled BSDF + image nodes; anything else is lost |
| Socket names | read them from the node (`[i.name for i in bsdf.inputs]`), they differ between Blender versions |
| Color spaces | base color sRGB; all data maps Non-Color |
| Materials per mesh | as few as possible; engine limit from engine.md (UNVERIFIED if unknown) |
| Alpha | no blending unless the brief needs it |
| Texture size | config.md table |

## Done when
Every material uses only Principled + image nodes; names correct; textures present and sized; screenshot saved; audit_naming pass.

## On fail
| Failure | Action |
|---|---|
| Procedural nodes in the material | bake to image (blender-uv-bake) and rebuild |
| Colors differ in engine | blender-diagnose row B (color space) |
| Missing textures after export | check relative paths; pack or save images |

## Next
blender-rig (deforming) or blender-qa.
