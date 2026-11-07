---
name: blender-animate
description: "Use when creating game animation clips in Blender - idle, walk, run, attack, interactions, prop animations; loops, root motion, frame ranges, clip naming, NLA, export-ready actions. Triggers: animate, animation, walk, run, idle, attack, loop, clip, keyframe, NLA."
---
# Animate (game clips)

## Requires
Rigged asset with state.md rig = PASS. engine.md Animation rows (fps, clip source, loop flag, root motion, clip naming). Clip list from the brief.

## Inputs
Clips: name, type (loop / one-shot), duration or frame count, root motion yes/no.

## Steps
1. FPS: set scene fps from engine.md (UNVERIFIED -> ask once; label [USER]). Never key at one fps and export at another.
2. CLIP LIST: write the table into state.md Decisions (name, frames, loop, root motion).
3. TIMING: starting values from `references/cycles.md` (locomotion), `references/combat.md` (attacks), `references/props.md` (props). Label [START].
4. POSE-TO-POSE: key poses first (contact, passing, etc.), then breakdowns, then inbetweens. Key only deform bones that move.
5. LOOPS: first and last pose identical (copy the first key to the last frame); loop clip names end with `_loop` (config.md); do not duplicate the last frame in the export range if the engine loops by time (engine.md; UNVERIFIED -> note it).
6. ROOT MOTION: per the clip table; in-place clips keep the root fixed.
7. NAME: `AN_<Asset>_<Clip>` (+ `_loop`); engine suffix hints from engine.md only.
8. ACTIONS: one action per clip; fake user on; NLA tracks only if engine.md says clips come from NLA.
9. AUDIT: `audit_anim.py` (ROOT_BONE set when root motion matters); screenshots of key poses.

## Hard rules
| Rule | Detail |
|---|---|
| Fps | from engine.md before keying |
| Loops | closed channels (audit loop_closed true) |
| Root | single root; drift only when the clip says root motion |
| Keys | no keys on non-deform helper bones unless baked for export |
| Naming | config.md + engine.md; never invent engine hints |
| Evidence | durations in seconds are computed from frames and fps in the audit |

## Done when
audit_anim pass; every loop clip closed; clip table matches the actions; key pose screenshots saved.

## On fail
| Failure | Action |
|---|---|
| Loop pops | copy first key to last frame for the open channels listed |
| Foot sliding | match root speed to stride; or use engine root motion (engine.md) |
| Mesh breaks in pose | blender-rig test poses / blender-diagnose |
| Clip not exported | blender-export animation option introspection |

## Next
blender-qa -> blender-export.
