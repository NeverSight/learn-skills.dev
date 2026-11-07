---
name: blender-hands
description: "Use when building, fixing or retopologizing hands, fingers, thumbs, gloves, paws or claws for a character or creature - clean ring continuity from forearm to fingertip, joint loops, low triangle counts and an easy-to-weight rig. Triggers: hand, finger, thumb, glove, paw, claw, tangan, jari."
---
# Hands (rig-ready, low triangles)

## Requires
brief.md (style, role, budget for the whole character), character base mesh or forearm ring. `docs/blender/reference/deformation-zones.md`.

## Inputs
Variant (human 5-finger / cartoon 4-finger / blocky / claw-paw) | tier (Ultra, Low, Mid, Hero) | forearm ring vertex count | reference image of the hand (optional).

## Steps
1. TIER: take the tier from the style (voxel = blocky; lowpoly = Low; stylized = Mid or Low; realistic = Hero) and the hand budget (character budget x 10-15 percent, config.md; or the user's number [USER]).
2. PARAMETERS: see `docs/blender/reference/figures/finger-tiers.png` and `hand-layout.png`; read `docs/blender/reference/hand-topology.md` section 1; copy the row for the tier; compute tris with the formulas in section 2 and compare with the hand budget BEFORE modeling. Too high: lower the tier or sides, not the joint loops.
3. VARIANT: read ONE file from `variants/` and apply its overrides.
4. WRIST RING: ring vertex count = forearm ring count at the wrist (read it from the mesh, do not assume).
5. PALM: build the palm block with one opening per finger (each opening has `sides` vertices) following hand-topology.md section 3.
6. FINGERS: tubes with constant `sides`, joint loops per tier (hand-topology.md section 4), tips per section 5.
7. THUMB: extra base loops (section 6), angled away from the index in the rest pose.
8. REST POSE: relaxed, fingers slightly curled and spread with gaps (section 7).
9. AUDIT: `audit_mesh.py` (BUDGET = hand budget), `audit_topology.py` (ARMATURE if it exists): ngons 0, thin quads 0, poles outside joint zones, symmetry between left and right hands if mirrored.
10. WEIGHT PLAN: write the bone plan and weight ramps (hand-topology.md section 8) into state.md Decisions for blender-rig.
11. SCREENS: wireframe back of hand, palm side, side view, 90-degree finger curl test (pose the bones if an armature exists).

## Hard rules
| Rule | Detail |
|---|---|
| Quads only | in every joint zone; no triangles, no poles within 1 ring of a finger joint |
| Constant sides | each finger keeps the same vertex count per ring from base to tip |
| Ring continuity | forearm ring = wrist ring = palm opening counts; mismatches use a transition pattern mid-segment |
| Joint loops | count per tier; they straddle the joint center |
| Finger gaps | adjacent fingers never touch in the rest pose |
| Budget first | compute tris before building |
| Left hand | mirror the right hand; never rebuild |
| Static hands | if the hand never deforms (blocky variant), no joint loops |

## Done when
audit_mesh pass for the hand budget; audit_topology joint counts all 0; ring continuity verified (counts quoted from the mesh); 90-degree curl screenshot shows no collapse; weight plan written.

## On fail
| Failure | Action |
|---|---|
| Fingers collapse when curled | add joint loops (blender-topology-fix recipe) or raise the tier |
| Over budget | lower sides first (8 -> 6), then rows between joints; keep joint loops |
| Wrist seam shading | match ring vertex count and normals; weld |
| Hand mesh is a scan/sculpt | blender-retopo with hands guide loops |
| Fingers weights bleed | blender-rig hands weights plan |

## Next
blender-topology (full audit) -> blender-uv-bake -> blender-rig.
