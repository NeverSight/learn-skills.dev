---
name: cad-bim-automation
description: Safely automate repetitive architecture CAD/BIM/model/document workflows using available tools. Use for Revit, IFC, DWG, DXF, SVG, Blender, FreeCAD, batch edits, exports, naming, or model-data extraction.
---

# CAD/BIM Automation

Inspect formats/versions, available tools/APIs, source-vs-issued status, units, coordinates/origin, levels/grids, layers/categories, naming, and revisions.

Choose the least destructive method: read/report → export to new file → supported API/script → original edit only with explicit permission. For proprietary formats, produce an application-native workflow rather than pretending an unsupported direct edit occurred.

Batch protocol: inventory → dry run → sample → validate → full run → post-change audit.

Verify counts, units, geometry bounds, naming, missing objects/categories, export integrity, and deltas. Never alter surveyed coordinates, structural geometry, life-safety elements, or issued information outside explicit scope and review.

**Opt-in local Blender prototype (separately installed skill):** if a trusted Blender executable is available and the user requests a NEW conceptual 3D scene, discover the installed `architectural-drawing-generation` skill first. Its **own** `scripts/blender_native.py` (worker and validator included) is the portable entry point; run `doctor`, then `build SPEC.json NEW_OUT` from that skill directory. Do not assume the standalone `cad-bim-automation` skill contains Blender code or repo docs. In a Gridline checkout, `scripts/blender_native.py` is merely a convenience launcher; `docs/BLENDER_NATIVE_BRIDGE.md` documents its limits. If the drawing skill is absent, report a missing dependency rather than inventing a path. This bridge creates editable conceptual mesh geometry and .glb with native readback; it cannot edit live models, install MCPs, reconstruct images, establish IFC/AutoCAD compliance or approve drawings. Ask for missing reference measurements and report unsupported details.


**Optional signed source workflow:** the drawing skill also supplies
`component_state.py` for typed component/level/wall/opening/room proposals, exact
Ed25519 owner approvals, immutable revisions, indexed impacts, stale conflicts,
revalidated disjoint merges and approved restore. Keep owner keys outside the
agent and never self-sign as a real owner. `archimesh_components.py build --state-db
DB --owner-key-sha256 PIN` requires the signed current source and new output only;
`component_ifc.py` additionally requires the state database, requirements and
trusted source/owner pins. These source/file operations do not authorize live
Revit/AutoCAD writes, replace native transactions/rollback, establish a complete
external drawing dependency graph or close the general #15 gate. Read the drawing
skill's actual commands/limits; do not assume this standalone automation skill
contains its scripts.
