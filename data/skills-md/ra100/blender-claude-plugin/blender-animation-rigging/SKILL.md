---
name: blender-animation-rigging
description: Blender 5.x animation and rigging — keyframes, FCurves, layered actions, drivers, constraints, armatures, IK/FK, shape keys, NLA editor, and bone collections via Python (bpy). Includes 5.1 changes (Smooth Gaussian FCurve modifier, Apply to Basis, layered action performance).
---

# Blender Animation & Rigging Expert

## Overview

This skill provides expert guidance for Blender 5.x animation and rigging: keyframing, FCurve editing, drivers, bone constraints, armature creation, IK/FK chains, shape keys, NLA strips, and Python automation of animation workflows. Includes 5.1 changes (Smooth Gaussian FCurve modifier, Apply to Basis, layered action performance). The reference files contain the complete constraint catalog and Python API patterns.

## MCP-First Approach

Prefer the **official Blender MCP Server** (Blender Lab, Blender 5.1+) for inserting keyframes, creating armatures, wiring constraints, baking actions directly in a running Blender session. Fall back to emitting Python scripts only when the MCP server is not connected.

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

- **"Animate object X"** -> Use keyframe insertion patterns (see Keyframe Patterns)
- **"Create a rig / armature"** -> See Armature Creation section and `references/python_api.md`
- **"Set up IK"** -> See IK Chain Setup
- **"Create a driver"** -> See Driver Recipes
- **"Add a constraint"** -> Consult `references/constraint_reference.md` for the correct type and properties
- **"Work with shape keys"** -> See Shape Key Patterns
- **"Use the NLA editor"** -> See NLA Management
- **"Edit FCurves"** -> See FCurve Manipulation in `references/python_api.md`
- **"Bone rolls/orientations are wrong"** -> See Mode Switching Gotchas

## Blender 5.1 Changes

### Smooth (Gaussian) FCurve Modifier (New in 5.1)
1. New FCurve modifier type: `'SMOOTH'` with blend mode `'GAUSSIAN'`
2. Provides smoother interpolation than the legacy Smooth modifier
3. Apply via Python: `fcurve.modifiers.new('Smooth', 'SMOOTH')` then set blend type
4. Useful for reducing jitter in motion capture data

### Apply to Basis (New in 5.1)
1. Operator to apply the current pose as the new rest pose (bake pose to rest)
2. Python: `bpy.ops.pose.apply_to_basis()`
3. Useful for fixing bone orientations after rigging

### Layered Actions Performance (5.1)
1. Significant performance improvements for layered (non-destructive) animation
2. Reduced evaluation overhead for complex NLA/layer setups
3. Better viewport playback with layered animation active

### ANIM_OT_convert_legacy_action Removed (5.1)
1. The `bpy.ops.anim.convert_legacy_action` operator has been removed
2. Legacy single-strip NLA actions are now automatically handled by the layered action system
3. Update any scripts that referenced this operator
## Keyframe Patterns

### Basic Keyframing

```python
import bpy

obj = bpy.context.active_object

# Set value and insert keyframe
obj.location = (0, 0, 0)
obj.keyframe_insert(data_path="location", frame=1)

obj.location = (5, 0, 0)
obj.keyframe_insert(data_path="location", frame=60)

# Keyframe specific channel (e.g., X location only)
obj.keyframe_insert(data_path="location", index=0, frame=1)

# Keyframe rotation
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="rotation_euler", frame=1)

# Keyframe scale
obj.keyframe_insert(data_path="scale", frame=1)
```

### Keyframeable Properties

| Property | data_path | Components |
| --- | --- | --- |
| Location | `"location"` | 0=X, 1=Y, 2=Z |
| Rotation (Euler) | `"rotation_euler"` | 0=X, 1=Y, 2=Z |
| Rotation (Quaternion) | `"rotation_quaternion"` | 0=W, 1=X, 2=Y, 3=Z |
| Scale | `"scale"` | 0=X, 1=Y, 2=Z |
| Custom Property | `'["prop_name"]'` | — |
| Material Value | Via material node inputs | — |
| Shape Key Value | `"value"` (on key block) | — |
| Modifier Property | `'modifiers["name"].property'` | — |

## Armature Creation

```python
import bpy
from mathutils import Vector

# Create armature data and object
armature = bpy.data.armatures.new("MyArmature")
arm_obj = bpy.data.objects.new("MyArmature", armature)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj

# Enter edit mode to create bones
bpy.ops.object.mode_set(mode='EDIT')
edit_bones = armature.edit_bones

# Root bone
root = edit_bones.new("Root")
root.head = (0, 0, 0)
root.tail = (0, 0, 0.5)

# Spine chain
spine = edit_bones.new("Spine")
spine.head = root.tail
spine.tail = (0, 0, 1.0)
spine.parent = root
spine.use_connect = True

chest = edit_bones.new("Chest")
chest.head = spine.tail
chest.tail = (0, 0, 1.5)
chest.parent = spine
chest.use_connect = True

# Arm bones (left)
upper_arm_l = edit_bones.new("UpperArm.L")
upper_arm_l.head = (0.2, 0, 1.4)
upper_arm_l.tail = (0.7, 0, 1.4)
upper_arm_l.parent = chest

lower_arm_l = edit_bones.new("LowerArm.L")
lower_arm_l.head = upper_arm_l.tail
lower_arm_l.tail = (1.2, 0, 1.4)
lower_arm_l.parent = upper_arm_l
lower_arm_l.use_connect = True

# Return to object mode
bpy.ops.object.mode_set(mode='OBJECT')
```

## IK Chain Setup

```python
import bpy

arm_obj = bpy.data.objects["MyArmature"]
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.mode_set(mode='POSE')

# Add IK constraint to the last bone in the chain
pose_bone = arm_obj.pose.bones["LowerArm.L"]
ik = pose_bone.constraints.new('INVERSE_KINEMATICS')
ik.target = bpy.data.objects["IK_Target"]  # Empty or other object
ik.chain_count = 2  # Number of bones in chain (0 = to root)
ik.use_rotation = False  # Optional: also match target rotation
ik.influence = 1.0

# IK with pole target (for knee/elbow direction)
ik.pole_target = bpy.data.objects["Pole_Target"]
ik.pole_angle = 0.0  # Adjust if elbow/knee points wrong direction

bpy.ops.object.mode_set(mode='OBJECT')
```

## Driver Recipes

### Simple Expression Driver

```python
import bpy

obj = bpy.context.active_object

# Add driver to Z location
fcurve = obj.driver_add("location", 2)  # index 2 = Z
driver = fcurve.driver
driver.type = 'SCRIPTED'
driver.expression = "frame / 24"  # Z = current second
```

### Driver with Variable

```python
# Drive Y scale from another object's X location
fcurve = obj.driver_add("scale", 1)  # Y scale
driver = fcurve.driver
driver.type = 'SCRIPTED'

var = driver.variables.new()
var.name = "ctrl_x"
var.type = 'TRANSFORMS'
var.targets[0].id = bpy.data.objects["Controller"]
var.targets[0].transform_type = 'LOC_X'
var.targets[0].transform_space = 'WORLD_SPACE'

driver.expression = "ctrl_x * 2"
```

### Driver from Custom Property

```python
fcurve = obj.driver_add("location", 0)  # X location
driver = fcurve.driver
driver.type = 'SCRIPTED'

var = driver.variables.new()
var.name = "my_val"
var.type = 'SINGLE_PROP'
var.targets[0].id = bpy.data.objects["Controller"]
var.targets[0].data_path = '["my_custom_property"]'

driver.expression = "my_val"
```

### Driver Variable Types

| Type | Description |
| --- | --- |
| `'SINGLE_PROP'` | Value of an RNA property |
| `'TRANSFORMS'` | Transform channel of an object/bone |
| `'ROTATION_DIFF'` | Rotation difference between two bones |
| `'LOC_DIFF'` | Distance between two objects/bones |
| `'CONTEXT_PROP'` | Active scene/view layer property |

### Transform Types for TRANSFORMS Variables

`LOC_X`, `LOC_Y`, `LOC_Z`, `ROT_X`, `ROT_Y`, `ROT_Z`, `ROT_W`, `SCALE_X`, `SCALE_Y`, `SCALE_Z`, `SCALE_AVG`

## Shape Key Patterns

### Create Shape Keys

```python
import bpy

obj = bpy.context.active_object
mesh = obj.data

# Create basis (reference shape)
if mesh.shape_keys is None:
    obj.shape_key_add(name="Basis", from_mix=False)

# Add shape keys
key_smile = obj.shape_key_add(name="Smile", from_mix=False)
# Modify vertices for the smile shape
for i, v in enumerate(key_smile.data):
    if mesh.vertices[i].co.z > 0.5:  # Upper face
        v.co.y += 0.1

key_frown = obj.shape_key_add(name="Frown", from_mix=False)
for i, v in enumerate(key_frown.data):
    if mesh.vertices[i].co.z > 0.5:
        v.co.y -= 0.1
```

### Animate Shape Keys

```python
# Access shape keys
shape_keys = obj.data.shape_keys
key_blocks = shape_keys.key_blocks

# Set value and keyframe
key_blocks["Smile"].value = 0.0
key_blocks["Smile"].keyframe_insert(data_path="value", frame=1)

key_blocks["Smile"].value = 1.0
key_blocks["Smile"].keyframe_insert(data_path="value", frame=30)
```

### Shape Key Properties

```python
key = key_blocks["Smile"]
key.value = 0.5           # Current blend value (0-1)
key.slider_min = 0.0      # Minimum slider value
key.slider_max = 1.0      # Maximum slider value
key.mute = False           # Mute this shape key
key.relative_key = key_blocks["Basis"]  # Reference shape
key.vertex_group = ""      # Limit influence to vertex group
```

## NLA Management

### Create and Manage NLA Strips

```python
import bpy

obj = bpy.context.active_object

# Ensure animation data exists
if obj.animation_data is None:
    obj.animation_data_create()

# Push current action to NLA track
action = obj.animation_data.action
if action:
    track = obj.animation_data.nla_tracks.new()
    track.name = "Walk Cycle"
    strip = track.strips.new(name="Walk", start=1, action=action)
    obj.animation_data.action = None  # Clear active action
```

### NLA Strip Properties

```python
strip.frame_start = 1
strip.frame_end = 60
strip.repeat = 3.0              # Loop count
strip.scale = 1.0               # Time scale (0.5 = half speed)
strip.blend_type = 'REPLACE'    # REPLACE, COMBINE, ADD, SUBTRACT, MULTIPLY
strip.influence = 1.0           # Blend influence (0-1)
strip.mute = False
strip.use_auto_blend = True     # Auto-blend between adjacent strips
strip.blend_in = 5.0            # Blend-in frames
strip.blend_out = 5.0           # Blend-out frames
strip.use_reverse = False       # Play in reverse
strip.extrapolation = 'HOLD'    # NOTHING, HOLD, HOLD_FORWARD
```

## Mode Switching Gotchas

1. **Edit bones vs Pose bones**: `armature.edit_bones` only accessible in EDIT mode. `object.pose.bones` accessible in POSE and OBJECT mode.
2. **Bone data loss**: Switching modes updates bone data. Don't cache edit bone references across mode switches.
3. **Constraint targets**: Must be set in POSE mode. Constraint properties can be read in OBJECT mode.
4. **Shape keys in edit mode**: Modifying mesh in EDIT mode modifies the active shape key, not the basis (unless basis is active).
5. **Keyframe insertion context**: `keyframe_insert()` works in any mode, but `bpy.ops.anim.keyframe_insert()` requires correct context.
6. **Bone roll**: Set `edit_bone.roll` in EDIT mode. Incorrect roll causes IK plane flipping.
7. **Rest pose vs Pose**: `armature.bones[].head_local` is rest pose. `pose.bones[].head` is posed position (read-only, computed from matrix).

## Debugging Animation Issues

- **Animation not playing**: Check frame range (start/end), check if action is assigned, check NLA strips aren't muting
- **Keyframes on wrong channels**: Check `data_path` and `array_index` on FCurves
- **IK flipping**: Adjust pole target position or bone roll in edit mode
- **Driver not updating**: Check for circular dependencies, ensure expression syntax is valid, check variable targets
- **Shape key not blending**: Check that Basis shape exists and `relative_key` is set correctly
- **Constraint not working**: Check influence (0 = disabled), check target object exists, check bone name spelling

## Constraint Reference

For the complete catalog of all ~45 constraints with type strings, properties, and use cases, consult `references/constraint_reference.md`.

Key categories:
- Motion tracking: grep for "Track" or "Motion"
- Transform control: grep for "Copy" or "Limit" or "Transform"
- IK/Rigging: grep for "Inverse" or "Spline" or "Stretch"
- Relationship: grep for "Child Of" or "Pivot" or "Follow"

## Python API Reference

For complete Python API patterns including keyframe insertion, FCurve manipulation, driver creation, armature/bone setup, NLA strips, and shape key management, consult `references/python_api.md`.
