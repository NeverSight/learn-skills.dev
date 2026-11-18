---
name: blender-animation
description: >-
  Animates 3D objects and characters in Blender with Python (bpy): keyframes, armatures and IK rigs, shape keys, F-Curves, the NLA editor and drivers. Use when the user wants to keyframe properties, create armatures and rigs, set up IK/FK chains, animate shape keys for facial animation, edit F-Curves, blend actions with NLA strips, add drivers, or script any animation workflow in Blender from the terminal.
license: Apache-2.0
compatibility: >-
  Blender 4.4 or newer (verified on 5.2.2 LTS); run scripts with blender --background --python script.py. Blender 5.0 removed the old action.fcurves API used by older tutorials.
metadata:
  author: terminal-skills
  version: "1.1.0"
  category: design
  tags: "blender, animation, rigging, keyframes, armature"
  repository: https://projects.blender.org/blender/blender
---

# Blender Animation

## Overview

Create and control animations in Blender using Python: keyframe object and bone transforms, build armatures with IK rigs, animate shape keys, edit F-Curves, layer actions in the NLA editor and wire up drivers, all from a script.

Since Blender 4.4 an **Action** is layered and has **slots**: a slot says which data-block an Action animates, and the F-Curves live in a *channelbag* on a keyframe strip inside a layer. Blender 5.0 removed the old shortcuts `action.fcurves`, `action.groups` and `action.id_root`, so code from older tutorials raises `AttributeError: 'Action' object has no attribute 'fcurves'`. `obj.keyframe_insert(...)` still works unchanged and creates the action, slot and channelbag for you. Run scripts in the background:

```bash
blender --background --factory-startup --python animate.py
```

A factory-startup scene contains `Cube`, `Camera` and `Light`.

## Instructions

### 1. Keyframe object properties

```python
import bpy
obj = bpy.data.objects["Cube"]
for loc, frame in [((0, 0, 0), 1), ((5, 0, 3), 30), ((5, 4, 0), 60)]:
    obj.location = loc
    obj.keyframe_insert(data_path="location", frame=frame)
obj.rotation_euler = (0, 0, 3.14159)
obj.keyframe_insert(data_path="rotation_euler", frame=60)
obj.scale = (2, 2, 2)
obj.keyframe_insert(data_path="scale", frame=60)
obj["intensity"] = 1.0                                        # custom property
obj.keyframe_insert(data_path='["intensity"]', frame=30)
obj.keyframe_insert(data_path="location", index=2, frame=45)  # one axis only (Z)
bpy.context.scene.frame_start, bpy.context.scene.frame_end = 1, 60
```

The created action is `obj.animation_data.action` and its slot is `obj.animation_data.action_slot`.

### 2. Control F-Curve interpolation and modifiers

F-Curves are reached through the channelbag of the slot:

```python
import bpy
from bpy_extras import anim_utils
obj = bpy.data.objects["Cube"]
anim = obj.animation_data
channelbag = anim_utils.action_get_channelbag_for_slot(anim.action, anim.action_slot)
for fcurve in channelbag.fcurves:
    for kp in fcurve.keyframe_points:
        kp.interpolation = 'BEZIER'   # CONSTANT, LINEAR, BEZIER, SINE, EXPO, BOUNCE, ELASTIC
        kp.easing = 'EASE_IN_OUT'     # AUTO, EASE_IN, EASE_OUT, EASE_IN_OUT
    mod = fcurve.modifiers.new(type='CYCLES')   # loop the animation
    mod.mode_before = mod.mode_after = 'REPEAT'  # NONE, REPEAT, REPEAT_OFFSET, MIRROR
z_curve = channelbag.fcurves.find("location", index=2)
if z_curve:
    noise = z_curve.modifiers.new(type='NOISE')
    noise.strength, noise.scale = 0.3, 5.0
# Get-or-create a curve in a named channel group
fc = channelbag.fcurves.ensure("location", index=0, group_name="Object Transforms")
```

`anim_utils.action_ensure_channelbag_for_slot(action, slot)` creates the layer, strip and channelbag when none exist.

### 3. Create armatures and bones

```python
import bpy
arm_data = bpy.data.armatures.new("Rig")
arm_obj = bpy.data.objects.new("Rig", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='EDIT')
# (name, head, tail, parent_name, connected)
bone_defs = [
    ("Spine",      (0, 0, 1.0),   (0, 0, 1.4),    None,         False),
    ("Chest",      (0, 0, 1.4),   (0, 0, 1.8),    "Spine",      False),
    ("UpperArm.L", (0.2, 0, 1.7), (0.5, 0, 1.4),  "Chest",      False),
    ("Forearm.L",  (0.5, 0, 1.4), (0.8, 0, 1.1),  "UpperArm.L", True),
    ("Thigh.L",    (0.1, 0, 1.0), (0.1, 0, 0.5),  "Spine",      False),
    ("Shin.L",     (0.1, 0, 0.5), (0.1, 0, 0.05), "Thigh.L",    True),
]
for name, head, tail, parent, connected in bone_defs:
    b = arm_data.edit_bones.new(name)
    b.head, b.tail = head, tail
    if parent:
        b.parent = arm_data.edit_bones[parent]
        b.use_connect = connected
bpy.ops.object.mode_set(mode='OBJECT')
```

### 4. Constraints on bones

```python
import bpy
arm_obj = bpy.data.objects["Rig"]
for name, loc in (("IK_Target", (0.8, 0, 1.1)), ("IK_Pole", (0.5, -1, 1.4)), ("ChestCtrl", (0, 0, 2))):
    empty = bpy.data.objects.new(name, None)          # an Empty: object data is None
    empty.location = loc; bpy.context.collection.objects.link(empty)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='POSE')
ik = arm_obj.pose.bones["Forearm.L"].constraints.new('IK')
ik.target = bpy.data.objects["IK_Target"]
ik.pole_target = bpy.data.objects["IK_Pole"]
ik.chain_count = 2                                    # 0 = whole chain up to the root
cr = arm_obj.pose.bones["Chest"].constraints.new('COPY_ROTATION')
cr.target = bpy.data.objects["ChestCtrl"]
```

### 5. Keyframe bone poses

Pose bones default to quaternion rotation, so set `rotation_mode = 'XYZ'` before keying `rotation_euler`. Keying creates the action; rename it afterwards:

```python
import bpy, math
arm_obj = bpy.data.objects["Rig"]
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='POSE')
thigh = arm_obj.pose.bones["Thigh.L"]
thigh.rotation_mode = 'XYZ'
for angle, frame in [(-30, 1), (0, 13), (30, 25), (-30, 37)]:   # back, neutral, forward, back
    thigh.rotation_euler = (math.radians(angle), 0, 0)
    thigh.keyframe_insert(data_path="rotation_euler", frame=frame)
arm_obj.animation_data.action.name = "WalkCycle"
bpy.ops.object.mode_set(mode='OBJECT')
```

### 6. Create and animate shape keys

```python
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0)
head = bpy.context.active_object
head.name = "Head"
if not head.data.shape_keys:
    head.shape_key_add(name="Basis", from_mix=False)      # Basis must exist first
smile = head.shape_key_add(name="Smile", from_mix=False)
for vert in smile.data:
    if vert.co.y < -0.6 and abs(vert.co.z) < 0.3:         # a patch on the front of the sphere
        vert.co.z += 0.1
sk = head.data.shape_keys.key_blocks["Smile"]
for val, frame in [(0.0, 1), (1.0, 15), (0.0, 30)]:
    sk.value = val
    sk.keyframe_insert(data_path="value", frame=frame)
```

### 7. Layer actions with the NLA editor

```python
import bpy, math
arm_obj = bpy.data.objects["Rig"]
anim = arm_obj.animation_data
anim.action = None                       # detach WalkCycle; it stays in bpy.data.actions
upper = arm_obj.pose.bones["UpperArm.L"]
upper.rotation_mode = 'XYZ'
for angle, frame in [(0, 1), (60, 10), (0, 20)]:
    upper.rotation_euler = (0, 0, math.radians(angle))
    upper.keyframe_insert(data_path="rotation_euler", frame=frame)
anim.action.name = "WaveHand"
anim.action = None                       # an active action overrides NLA, so clear it
track1 = anim.nla_tracks.new(); track1.name = "Walk"
strip1 = track1.strips.new("Walk", start=1, action=bpy.data.actions["WalkCycle"])
strip1.repeat = 4
strip1.blend_type = 'REPLACE'            # REPLACE, COMBINE, ADD, SUBTRACT, MULTIPLY
track2 = anim.nla_tracks.new(); track2.name = "Wave"
strip2 = track2.strips.new("Wave", start=25, action=bpy.data.actions["WaveHand"])
strip2.blend_type = 'COMBINE'            # on top of the walk
strip2.influence = 0.8
```

Strips pick a compatible slot automatically (`strip.action_slot`). Assigning `anim.action = some_action` can leave no slot selected; if the object stays static, also set `anim.action_slot = some_action.slots[0]`.

### 8. Drivers

```python
import bpy
cube = bpy.data.objects["Cube"]
driver = cube.driver_add("location", 2).driver      # drive Z location
driver.type = 'SCRIPTED'
var = driver.variables.new()
var.name = "ctrl"
var.type = 'TRANSFORMS'
var.targets[0].id = bpy.data.objects["ChestCtrl"]
var.targets[0].transform_type = 'LOC_X'
var.targets[0].transform_space = 'WORLD_SPACE'
driver.expression = "ctrl * 3 + sin(frame * 0.1)"   # shape keys work too: sk.driver_add("value")
print(driver.is_valid)                               # scripted expressions need auto-run scripts allowed
```


### 9. Bake before export

Other software cannot read constraints, NLA or drivers. Bake to plain keyframes (a new action is written and the constraints are removed):

```python
arm_obj = bpy.data.objects["Rig"]
arm_obj.select_set(True); bpy.context.view_layer.objects.active = arm_obj
bpy.ops.nla.bake(frame_start=1, frame_end=60, only_selected=False,
                 visual_keying=True, clear_constraints=True, bake_types={'POSE'})
```

## Examples

### Example 1: Bouncing ball with squash and stretch

User request: "Animate a ball bouncing with squash and stretch."

```python
import bpy, os
from bpy_extras import anim_utils
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 3))
ball = bpy.context.active_object
ball.name = "BouncingBall"
keyframes = [  # (frame, z_pos, scale_x, scale_y, scale_z)
    (1, 3.0, 1, 1, 1), (12, 0.5, 1, 1, 1),                  # fall
    (15, 0.3, 1.3, 1.3, 0.6), (18, 0.5, 0.85, 0.85, 1.2),   # squash, then stretch
    (30, 2.2, 1, 1, 1), (42, 0.5, 1, 1, 1),                 # apex, second fall
    (45, 0.3, 1.2, 1.2, 0.7), (55, 1.5, 1, 1, 1), (62, 0.5, 1, 1, 1),
]
for frame, z, sx, sy, sz in keyframes:
    ball.location = (0, 0, z)
    ball.keyframe_insert(data_path="location", frame=frame)
    ball.scale = (sx, sy, sz)
    ball.keyframe_insert(data_path="scale", frame=frame)
anim = ball.animation_data
for fc in anim_utils.action_get_channelbag_for_slot(anim.action, anim.action_slot).fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'BEZIER'
bpy.context.scene.frame_end = 62; bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("bouncing_ball.blend"))
```

Result: `bouncing_ball.blend` in the working directory with 6 F-Curves (location and scale, XYZ) over frames 1 to 62; the ball flattens on impact and stretches on the way up.

### Example 2: Arm rig with IK reaching for a cube

User request: "Create a simple arm rig with IK and animate it reaching for a cube."

```python
import bpy, os
from bpy_extras import anim_utils
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
arm_data = bpy.data.armatures.new("ArmRig")
arm_obj = bpy.data.objects.new("ArmRig", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='EDIT')
prev = None
for name, x0, x1 in [("UpperArm", 0, 0.6), ("Forearm", 0.6, 1.2), ("Hand", 1.2, 1.4)]:
    b = arm_data.edit_bones.new(name)
    b.head, b.tail = (x0, 0, 1.5), (x1, 0, 1.5)
    if prev:
        b.parent, b.use_connect = prev, True
    prev = b
bpy.ops.object.mode_set(mode='OBJECT')
ik_target = bpy.data.objects.new("IK_Hand", None)
ik_target.location = (1.4, 0, 1.5); bpy.context.collection.objects.link(ik_target)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='POSE')
ik = arm_obj.pose.bones["Hand"].constraints.new('IK')
ik.target, ik.chain_count = ik_target, 3
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.mesh.primitive_cube_add(size=0.3, location=(1.0, 0.5, 1.0))   # the cube to reach
for loc, frame in [((1.4, 0, 1.5), 1), ((1.0, 0.5, 1.0), 30), ((1.0, 0.5, 1.3), 50)]:
    ik_target.location = loc
    ik_target.keyframe_insert(data_path="location", frame=frame)
anim = ik_target.animation_data
for fc in anim_utils.action_get_channelbag_for_slot(anim.action, anim.action_slot).fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation, kp.easing = 'BEZIER', 'EASE_IN_OUT'
bpy.context.scene.frame_end = 50; bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("arm_grab.blend"))
```

Result: at frame 30 the hand bone's tip sits at the cube (1.0, 0.5, 1.0) in world space, then lifts to z=1.3 by frame 50.

## Guidelines

- `data_path` must match the RNA path exactly: `"location"`, `"rotation_euler"`, `"scale"`, `'["custom_prop"]'`, `'pose.bones["Thigh.L"].rotation_euler'`.
- Shape keys need a "Basis" key first; animate `key_blocks["Name"].value` from 0.0 to 1.0.
- Do not write `action.fcurves`, `action.groups` or `action.id_root`; they are gone in 5.0. Use the channelbag, and `slot.target_id_type` instead of `id_root`.
- An active action overrides NLA: set `animation_data.action = None` so strips drive the object.
- Armature workflow: Edit mode for `edit_bones`, Pose mode for constraints and keyframes (`pose.bones`); return to Object mode before saving.
- Run scripts in a separate `--background` process, never inside a session the user is working in.
- `bpy.ops` calls depend on context (active object, mode): set the active object explicitly and prefer data API calls such as `bpy.data.objects.new`.
