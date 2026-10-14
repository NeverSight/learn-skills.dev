---
name: avatar-animations
description: Author custom avatar animations (scene emotes) for the player in Blender on the official Decentraland avatar rig, export them as `_emote.glb`, verify them, and hand them to a scene — including upper-body-only (masked) clips. Use when the user wants a custom emote, a new avatar animation, to animate the player/avatar, to make the avatar do something specific (sit, hold cards, carry a crate, throw, cheer), to work with the Blender avatar rig, to produce a scene emote .glb, or an upper-body / sitting / holding animation for the player. Do NOT use for playing animations baked into a model (see animations-tweens), for merely triggering emotes that already exist (see player-avatar), or for NPC animation (see npcs).
---

# Authoring Avatar Animations (Scene Emotes)

This skill covers **making the animation file**: posing the official Decentraland avatar rig in Blender, exporting a clip as a `*_emote.glb`, verifying it, and handing it to the scene. The scene-side API that plays it — `triggerSceneEmote`, `stopEmote`, `AvatarEmoteCommand`, the `AvatarMask` enum, the permission — lives in **player-avatar**; this skill links there rather than repeating it.

**Check the embedded emotes before authoring anything.** The Explorer ships 21 emotes playable by name from a scene (`triggerEmote`) or on an `AvatarShape` — including looping sitting poses. Full list with loop flags (single source of truth): `{baseDir}/references/embedded-emotes.md`.

**Scope check before you start:**

| The user wants | Skill |
| --- | --- |
| A new animation *of the player's avatar* that doesn't exist yet | **this skill** |
| To play a built-in emote, or a `_emote.glb` that already exists | **player-avatar** |
| To play an animation clip baked into a `.glb` model/prop | **animations-tweens** |
| To animate an NPC | **npcs** |
| To move/rotate an entity procedurally | **animations-tweens** (`Tween`) |

## Workflow

1. **Get the rig** — `Avatar_File.blend`, never a hand-built armature. Download + bone/control/property reference: `{baseDir}/references/avatar-rig.md`.
2. **Set up** — set the scene to **30 fps** (the shipped file is 24), capture the `Starting_Pose` values, create one new action per clip.
3. **Author** — pose `CTRL_` bones only, in Pose mode, keyframing every bone you touch at every keyframe.
4. **Verify while authoring** — print world positions (clipping, floor, animation area) *and* render four angles per keyframe into a contact sheet.
5. **Export** — one clip per file, armature only, `export_def_bones=True`, `ACTIVE_ACTIONS`.
6. **Verify the GLB** — parse the JSON chunk: 1 animation, 0 meshes, 63 nodes, 62 channels per path, duration = `(frames − 1) / 30`.
7. **Hand off** — rename to `*_emote.glb`, drop under `assets/animations/`, add the permission, play it (see **player-avatar**).

Ready-made `bpy` helpers for every step — the helper module, sign detection, render/contact-sheet setup, the export call, and the GLB verifier — are in `{baseDir}/references/blender-emote-patterns.md`.

**How to drive Blender** (headless CLI vs Blender MCP, binary paths, and the rule that you must never fall back from the MCP to headless silently) is already covered in `{baseDir}/../add-3d-models/references/blender-authoring.md`. Emote authoring uses exactly those two paths; do not re-derive them.

## RULE: One new action per clip — and reset to the idle pose, not identity

Create a fresh action for every clip. In Blender 4.4+/5 actions are **slotted**, and `Action.fcurves` no longer exists (curves live under `act.layers[0].strips[0].channelbags`):

```python
act  = bpy.data.actions.new(name)
slot = act.slots.new('OBJECT', 'Avatar_Animation')
arm.animation_data.action = act
arm.animation_data.action_slot = slot
```

Before authoring anything, `scene.frame_set(0)` to evaluate `Starting_Pose` and **capture every pose bone's transform**. That snapshot — not the identity transform — is the baseline you reset to between keyframes. The rest pose of the armature is an A/T-pose; the idle the runtime blends from is `Starting_Pose`. Resetting to identity gives you a clip that snaps to a T-pose on the first frame.

## RULE: Key everything you pose, at every keyframe

`scene.frame_set()` **re-evaluates the active action and overwrites any un-keyed pose** (`view_layer.update()` does not). A render taken after `frame_set` of a pose you forgot to key silently shows the idle instead — you will debug the wrong thing. So insert keys on location, rotation and scale for every control bone you touched, plus any custom property you changed:

```python
pb.keyframe_insert('["FK > IK Leg L"]', frame=f)
```

On the **first and last frame**, also key location/rotation/scale on **every deform bone**. Channels left without boundary keys stay "open" and keep whatever a previously playing emote left there — the official docs call these *emote overrides*, and they show up as an avatar whose legs are still doing the last emote.

## RULE: Upper arms — world axes for direction, local Y for twist

The upper-arm bone's local X is tilted. Rotating about it sweeps the arm across the chest, and a pose that should have both arms forward ends up with the arms **crossed** — this happens in practice and is not obvious in a front render. So set the arm's *direction* with world axes, converting the world axis into the bone's current frame first:

```python
M = (arm.matrix_world @ pb.matrix).to_3x3().normalized()
local_axis = M.inverted() @ Vector(world_axis)
pb.rotation_quaternion @= Quaternion(local_axis, math.radians(deg))
```

- Pure forward raise → world **X**.
- Moving a raised arm in/out → yaw about world **Z**.

World axes alone do not give a perfect arm pose, though. Arms move in many directions, and the rig's animator works with world **and** local rotations together. Two things need the bone's **local** axes:

- **Twist** — palm up/down, elbow pointing out or in, a wrist that has to face a prop — can only be done by rotating the bone about its own length, which is **local Y** on this rig (verified: local Y of `CTRL_FK_Avatar_Arm.*` is the bone axis; rotating it leaves the elbow where it is and only rolls the forearm and hand). `rl('CTRL_FK_Avatar_Arm.L', 'Y', deg)`.
- **Fine-tuning** once the gross direction is right — a small local correction is often more precise than another world-axis rotation.

Elbows, knees, wrists and fingers hinge on their **local X** (Y/Z are locked on those controls) — `rl()` is correct there.

## RULE: Legs mirror, the upper body does not — fix the pasted upper body by flipping X and Z

Blender's **Pose ▸ Copy Pose / Paste X-Flipped** only works on half of this rig (verified on `Avatar_File.blend`; numbers in `{baseDir}/references/avatar-rig.md`):

- **Legs and feet mirror normally**, FK or IK — Paste X-Flipped is exact for IK legs and within ~3 cm for FK legs.
- **Shoulders, upper arms, forearms, hands and fingers do not** — Paste X-Flipped lands the other hand 40–70 cm away. The rig animator's fix: on every pasted upper-body control, **negate the X and Z values and keep Y**. Example: a pasted arm reading X −0.5, Z 0.1 becomes X 0.5, Z −0.1. Apply it to the rotation (quaternion or Euler) and, on the IK hand and elbow controls, to the location too. Verified exact (0.000 m) for the whole arm chain, FK and IK, all 30 finger controls included.
- `mirror_side('L')` in `{baseDir}/references/blender-emote-patterns.md` does both steps for every control at once.
- When you pose a **single** joint rather than mirroring, still detect its sign programmatically — rotate +15°, measure which way the downstream bone moved, cache (`auto_sign`). The same angle on `.L` and `.R` does not produce a symmetric pose.

## RULE: FK or IK — lose contact → FK, keep contact → IK

Legs default to **IK**, arms to **FK** (`FK > IK *` properties on `CTRL_Avatar_UpperBody`). Switch only when the pose needs it, using one rule: **if a hand or foot has to keep contact** with the floor, a seat, a wall or a prop, it should be **IK**; **if it loses contact**, it should be **FK**.

- FK legs: jumps, rolls, flying, handstands, swimming, legs dangling off a ledge or a theatre seat.
- IK hands: push-ups, climbing, leaning on a table, both hands fixed on one prop.
- Do **not** flip modes during walk cycles, dances or anywhere contact is lost only briefly — the defaults handle those, and every switch pops unless the two chains match exactly at that frame.
- Key the `FK > IK` property itself when you change it, not just the bones.

**Seated poses.** Lower the body with `CTRL_Avatar_UpperBody` — it is the centre of gravity and moves the **whole** body. `CTRL_Avatar_Hips` moves only pelvis + legs and stretches the torso — wrong tool for sitting. Then decide per leg:

| Feet | Legs |
| --- | --- |
| Both feet on the ground (chair, bench) | Stay **IK**: move `CTRL_IK_Foot.*` to where the feet will rest, then drop the COG — the knees bend on their own, feet stay planted (verified: toes stay at Z = 0 through a 0.4 m drop). Aim the knees with `CTRL_Avatar_Knee.*`. |
| One leg crossed over the other | Only the lifted leg to **FK**; the grounded one stays IK. |
| Feet off the ground (pond edge, theatre seat, high stool) | Both legs **FK**. |

```python
setprop('CTRL_Avatar_UpperBody', 'FK > IK Leg L', 0.0)   # only for a leg that leaves the ground
setprop('CTRL_Avatar_UpperBody', 'FK > IK Leg R', 0.0)
# ...then pose CTRL_FK_Avatar_UpLeg / _Leg / _Foot / _ToeBase on that side
```

Whatever the mode, check the feet: world Z of `Avatar_LeftToeBase` / `Avatar_RightToeBase` must stay **≥ 0** or the avatar sinks through the floor.

## RULE: Verify with numbers as well as renders

Renders catch composition; numbers catch clipping. Print world positions of hands, head, feet and any prop reference at **every** keyframe:

- Keep hands **≥ ~0.3 m** from the head centre when a limb passes the head. A throw over the shoulder clipped straight through the skull until the arm was routed outward first.
- Keep hands **≥ ~0.10 m** apart rather than overlapping at the centre line.
- Keep the **face visible** in any default/holding pose — hold objects at upper-chest height with the head tilted down, not in front of the face.

Render four angles per keyframe (front three-quarter, straight front, side, top) with Workbench and tile them into one contact sheet. Iterate in a cheap **pose-only stage** first (seconds per run), and only then do the full build with exports.

## RULE: Stay inside the animation area

Measured on the reference objects in `Avatar_File.blend` (world metres, Blender Z-up):

| Reference object | Extent | Meaning |
| --- | --- | --- |
| `Animation_Area_Reference` | 4 × 4 × 4 m box — X, Y ∈ [−2, 2], Z ∈ [0, 4] | **Everything** stays inside for the whole clip: every body part, prop and particle. Nothing moves more than 4 m in any direction. |
| `Root_Animation_Area` | 2 m diameter cylinder on the origin | The avatar **root / centre of gravity** (`CTRL_Avatar_UpperBody`, i.e. `Avatar_Hips`) travels at most **1 m** forward, back, left or right — 2 m across. Vertically it may rise as far as the box allows (the docs say 4 m; the cylinder mesh in the file is 3 m tall). |
| `Ground_Reference` | plane at Z = 0 | Nothing below it. |

Within that budget a clip **may carry root translation** — the whole body walking forward, slumping sideways or sinking through the floor — and the Explorer plays that translation back on an `AvatarShape` NPC as well as on the player (in-world observation, Unity Explorer v0.186.0-alpha, SDK 7.30.1, 2026-10-10). It is the only way to move an NPC while a full-body emote plays, since a `Transform`/`Tween` move cancels the emote (**npcs**).

Legs, arms, head and props may leave the root cylinder — a kick or a cartwheel does — as long as they stay inside the box. Add the checks to the per-keyframe report: `|hips.x| ≤ 1`, `|hips.y| ≤ 1`, every deform bone head and tail inside the box, every toe Z ≥ 0 (`in_area()` in `{baseDir}/references/blender-emote-patterns.md`). The Decentraland Tools add-on's **Validate Emote** only *warns* when `CTRL_Avatar_UpperBody` moves more than 1 m horizontally or vertically from its first frame; it does not check the box, so the `in_area()` check is yours to run.

## RULE: Loops must close; one-shots must land where the scene resumes

- **Looping** clip: make the first and last keyframes **identical** (e.g. frame 1 and frame 121 for a 4 s loop) or the loop pops.
- **One-shot** clip: start *and* end in the resting pose the scene returns to — for a seated game, the seated holding pose; otherwise `Starting_Pose`.

## RULE: Export one clip per file, armature only

Delete every other object first — meshes, `WGT_*` widgets, reference planes, `Armature_Prop`, cameras, lights — and remove the `Starting_Pose` action, or the exporter emits two clips. `export_animation_mode='ACTIVE_ACTIONS'` is what guarantees exactly one animation per file. Full export call in `{baseDir}/references/blender-emote-patterns.md`.

Save an editable `.blend` (meshes included) **before** stripping, so the user can tweak the actions by hand afterwards.

## RULE: Verify the exported GLB before handing it over

Parse the GLB's JSON chunk and assert: **1 animation, 0 meshes, 63 nodes** (`Armature` + 62 deform bones), **1 skin**, **62 channels each** for translation/rotation/scale, and `duration == (last_frame − first_frame) / 30`. Verifier script in `{baseDir}/references/blender-emote-patterns.md`. A duration mismatch means the scene FPS wasn't 30.

Typical size for a 1–4 s clip at `export_frame_step=1` is **70–110 KB** — far under the 3 MB cap, so there is normally no reason to raise the sampling step.

## Upper-body (masked) animations

A masked emote is not a different file format — the **same** `.glb` is played with `mask: AvatarMask.AM_UPPER_BODY` at trigger time (API and enum details: **player-avatar** → "Emote masks"). What changes is what you should *author*.

**Which bones the mask keeps** — verified against the Explorer's `UpperBodyAvatarMask.mask` asset:

- **Animated:** `Avatar_Spine`, `_Spine1`, `_Spine2`, both shoulders/arms/forearms/hands, **all 40 finger bones**, `Avatar_Neck`, `Avatar_Head`.
- **Ignored:** `Avatar_Hips` and both legs (`UpLeg`/`Leg`/`Foot`/`ToeBase`) — these keep whatever the locomotion state or another emote is doing that frame.

Mechanically the renderer samples your clip each `LateUpdate`, then **restores the non-masked bones' local position and rotation** from the pose the Animator had already produced (`MaskedLegacyEmoteBlender`). So:

- **Hip/root motion in a masked clip has no effect.** `Avatar_Hips` is outside the mask, so the drop you authored with `CTRL_Avatar_UpperBody` to sit the avatar down is discarded; the legs show the locomotion state (idle, walk, run).
- **A masked clip does NOT layer over another emote.** Verified in the Explorer's `SceneMaskedEmoteSystem`: starting a masked emote on the local player stops any full-body emote that is playing, and starting a full-body emote cancels the masked one. So a masked clip cannot run on top of a chair's sitting emote — the avatar stands up. It layers only over locomotion, which is what the mask is for: carrying, holding or cheering while the player walks, runs or idles.
- **For a seated player, check `sittingChair1`/`sittingGround1` first** — they loop and hold the pose for free (see the embedded-emote note at the top of this skill). If you do author one, **have the owner look at the arms and hands before it ships**: observed 2026-10-12, the IK-feet + lowered-`UpperBody` recipe below produced a correct seat with awkward arms, which only a human eye caught.
- **For a seated player, play the clip full body.** Author a seated lower body into every clip (hips lowered, FK legs bent), trigger it unmasked, and have the scene replay the sitting emote (`triggerEmote({ predefinedEmote: 'sittingChair1' })` or the chair's own) when the clip ends and no looping seated clip takes over. A one-shot that returns to the same seated pose as your looping idle clip chains into it without a pop; the only visible pop is the height difference against the built-in sitting emote, which you tune with the hip drop.
- **Author the full body anyway, even for masked use.** A plausible lower body makes the same file usable unmasked. The mask is a trigger-time decision, not a property of the file.
- **Masked emotes on the local player emit no `AvatarEmoteCommand` lifecycle events** (documented in **player-avatar**). The scene must therefore time them itself — store each clip's duration alongside its path in scene config, since you know it exactly from the frame count.

Design notes for a seated holding pose that reads well: hips ≈ 0.6 m, hands at chest height, head tilted toward the hands.

> The bone list and blending mechanism above were read from the Explorer source (`MaskedLegacyEmoteBlender`, `SceneMaskedEmoteSystem`, `CharacterEmoteSystem` on `main`, 2026-09); the "masked stops full-body" rule was confirmed in-world on a seated player. For the **enum values and call signatures**, trust **player-avatar**, which is verified against the shipped protocol.

## File requirements

| Requirement | Value | Source |
| --- | --- | --- |
| Frame rate | **30 fps** (Blender defaults to 24) | docs |
| Max length | **10 s / 300 frames** | docs |
| Format | `.glb` | docs |
| Max file size | **3 MB** | docs |
| Sampling rate | `1` by default; `2` or `3` to shrink | docs |
| Animation clips per file | **exactly 1** (Emotes 2.0 may add 1 prop clip; sequences unsupported) | docs |
| File contents | deforming skeleton + animation **only** — no mesh, no control bones, no cameras/lights | docs |
| Start / end pose | both from the idle (`Starting_Pose`) | docs |
| Deform-bone keys | location + rotation + scale on the **first and last** frame, every bone | docs |
| Animation area | root ≤ **1 m** in each horizontal direction (2 m across); **every mesh part and prop** inside the **4 × 4 × 4 m** `Animation_Area_Reference` box (see RULE above) | docs + measured |
| **Filename** | must end **`_emote.glb`** (case-insensitive) | **player-avatar** |
| Scene permission | `ALLOW_TO_TRIGGER_AVATAR_EMOTE` in `scene.json` `requiredPermissions` | **player-avatar** |

Conventional location in the scene: `assets/animations/`. The glTF animation's *name* is irrelevant to the runtime — the file path is the identifier.

Blender's glTF exporter UI equivalents, if the user is exporting by hand: **Include > Limit to > Visible Objects**, **Data > Armature > Export Deformation Bones Only**, **Animation > Sampling Animations**.

The Decentraland Tools add-on's **Validate Emote** operator checks most of this (30 fps, ≤ 300 frames, exactly one armature action, first/last-frame keys on deform channels) before it will export, and warns — without blocking — when the COG moves more than 1 m horizontally or vertically. It does not check the 4 m bounding box.

## Testing in the scene

The fastest harness is a row of clickable primitive cubes — `MeshRenderer` + `MeshCollider` + `pointerEventsSystem.onPointerDown` with a generous `maxDistance` so they stay clickable from a chair — one per clip, plus a **Stop** cube and a **mask toggle** cube:

```typescript
pointerEventsSystem.onPointerDown(
	{ entity: cube, opts: { button: InputAction.IA_POINTER, hoverText: label, maxDistance } },
	() => void triggerSceneEmote({ src, loop: false, mask: upperBody ? AvatarMask.AM_UPPER_BODY : undefined })
)
```

Gate the whole harness behind a config flag and remove it before publishing.

**The Explorer MCP's `trigger_emote` only plays URN/base emotes, not scene files** — it cannot test a `_emote.glb`. Use in-scene triggers (see **unity-explorer-mcp** for driving the client around them).

## Cross-references

- **player-avatar** — `triggerSceneEmote` / `stopEmote` / `AvatarEmoteCommand` / `AvatarMask`, the `_emote.glb` rule, the permission, and freezing the player with `InputModifier` during a full-body emote.
- **add-3d-models** → `references/blender-authoring.md` — how to drive Blender at all (headless CLI vs MCP), plus general model export rules.
- **animations-tweens** — animations baked into props and models, and procedural `Tween` motion.
- **npcs** — animating `AvatarShape` NPCs and GLB NPCs.
- Official docs: [creating emotes](https://docs.decentraland.org/creator/wearables-and-emotes/emotes/creating-emotes/) · [rig features](https://docs.decentraland.org/creator/wearables-and-emotes/emotes/rig-features/) · [avatar rig](https://docs.decentraland.org/creator/wearables-and-emotes/emotes/avatar-rig/)
