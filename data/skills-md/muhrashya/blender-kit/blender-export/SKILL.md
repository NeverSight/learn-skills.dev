---
name: blender-export
description: "Use when exporting a finished Blender asset to a game engine or web - FBX or GLB/glTF, axis and scale, apply modifiers, deform-only skeleton, animation clips, textures, naming, import test. Triggers: export, FBX, GLB, glTF, import into Roblox/Unity/Unreal/Godot, scale wrong, rotated 90."
---
# Export (engine profile driven)

## Requires
state.md qa = PASS for the CURRENT asset version (no STALE stages). `docs/blender/engine.md` filled: Import, Coordinates, Mesh rules, Rig, Animation, Materials, Export call. Checkpoint.

## Inputs
Objects to export (names) | formats (from engine.md preferred) | clips (animated assets) | destination folder (`blender-out/<asset>/export/`).

## Steps
1. GATE: read state.md; any STALE or FAIL stage -> stop, route to it.
2. PROFILE: read engine.md. List every UNVERIFIED or [RECALLED] row that this export depends on; show it to the user in the report.
3. CHECKPOINT (`checkpoint.py`, STAGE = "pre-export").
4. PREPARE a clean selection per `references/exporters.md` section 1 (deliverables only; no references, cameras, lights, simulation objects, helper bones).
5. TRIANGULATE only if engine.md says so (export copy or exporter option; never the working mesh).
6. OPTIONS: read the engine.md Export call; introspect the exporter properties for THIS Blender version (exporters.md section 2); `export_asset.py` drops unsupported keys and reports them.
7. RUN `docs/blender/scripts/export_asset.py` (FORMAT, OBJECTS, OUT_PATH, OPTIONS). Require `EXPORT_OK=True` and a non-empty file.
8. VERIFY in Blender: re-import into a temporary scene or inspect the file size and object list (exporters.md section 3).
9. REPORT: file paths, bytes, options used, options dropped, engine.md rows relied on that are UNVERIFIED/[RECALLED], and the engine import test steps from engine.md.
10. LOG: assets.md row (Status SHIP, date), state.md.

## Hard rules
| Rule | Detail |
|---|---|
| No SHIP, no export | qa verdict required for this version |
| Introspect options | never pass an exporter argument that the introspection list does not contain |
| Engine facts | only from engine.md with their labels; UNVERIFIED rows are disclosed, never filled |
| Clean selection | `use_selection` true; deliverables only |
| Scale and axis | from engine.md; unknown -> export a 1 m cube first and ask the user to measure it in the engine |
| Textures | relative paths or packed; report where they are |
| File check | exists and non-empty, or the export did not happen |

## Done when
`EXPORT_OK=True`, file(s) verified, report delivered with the import test steps, assets.md updated.

## On fail
| Failure | Action |
|---|---|
| Option not supported | script reports dropped keys; use the version's equivalent from the introspection list |
| Empty or tiny file | wrong selection; modifiers hiding geometry; re-check selection and visibility |
| Wrong scale/rotation in engine | blender-diagnose row C; adjust options per engine.md; re-export |
| Animations missing | animation option (name differs per version) from introspection |
| STALE stages | run blender-qa again |

## Next
User runs the engine import test; then blender-qa logs the result, or blender-diagnose if the engine shows a problem.
