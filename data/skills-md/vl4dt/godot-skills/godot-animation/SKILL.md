---
name: godot-animation
description: "Animation systems for Godot 4.x: AnimationPlayer vs AnimationTree, state machines, blend spaces (1D/2D/directional), animation libraries, root motion, collapsible tracks, and tween_await(). Use when building character animations, cutscenes, or visual effects in Godot."
license: MIT
compatibility:
  - godot-4.0
  - godot-4.1
  - godot-4.2
  - godot-4.3
  - godot-4.4
  - godot-4.5
  - godot-4.6
  - godot-4.7
metadata:
  author: vl4dt
  version: 0.1.0
  tags:
    - godot
    - animation
    - animationplayer
    - animationtree
    - blend-space
    - root-motion
  created: 2026-06-20
---

# Animation Systems for Godot 4.x

Comprehensive patterns for character animation, state machines, and visual effects in Godot 4.x.

## AnimationPlayer vs AnimationTree

### AnimationPlayer — Simple Animations

Use AnimationPlayer for linear sequences, cutscenes, and simple property animations.

```gdscript
@onready var anim_player = $AnimationPlayer

func play_attack():
    anim_player.play("attack")

func play_transition(target: String, fade_time: float = 0.2):
    anim_player.play(target, fade_time)

# Signal-based animation completion
func _ready():
    anim_player.animation_finished.connect(_on_animation_finished)

func _on_animation_finished(anim_name: String):
    if anim_name == "attack":
        print("Attack animation complete")
```

### AnimationTree — State Machine Animations

Use AnimationTree for complex character animations with branching states (idle, walk, run, jump).

```gdscript
@onready var anim_tree = $AnimationTree
@onready var anim_state = anim_tree.get("state_machine")

func _ready():
    anim_state.travel("Idle")  # Start at Idle state

func set_animation(state_name: String):
    if anim_state.has_state(state_name):
        anim_state.travel(state_name)

func _physics_process(delta: float):
    var speed = velocity.length()
    anim_tree.set("parameters/Move/speed", speed)
    anim_tree.process(delta)
```

### When to Use Which

| Use Case | Tool |
|----------|------|
| Cutscenes, UI animations | AnimationPlayer |
| Character movement states | AnimationTree + StateMachine |
| Simple one-shot effects | AnimationPlayer |
| Blending between movements | AnimationTree + BlendSpace2D |
| Complex combat combos | AnimationTree + AnimationNodeBlendTree |

## State Machines in AnimationTree

### Building a Character State Machine

```gdscript
# In the AnimationTree, create an AnimationNodeStateMachine:
# States: Idle, Walk, Run, Jump, Fall, Attack
# Transitions: Idle <-> Walk, Idle <-> Run, Walk -> Run, etc.

@onready var anim_tree = $AnimationTree
@onready var state_machine = anim_tree.get("state_machine")

func _physics_process(delta: float):
    var speed = velocity.length()
    var new_state = "Idle"
    
    if not is_on_floor():
        new_state = "Fall" if velocity.y < 0 else "Jump"
    elif speed > 0.1:
        new_state = "Run" if speed > run_threshold else "Walk"
    
    # Only transition if the target state exists
    if state_machine.has_state(new_state):
        state_machine.travel(new_state)
    
    anim_tree.set("parameters/Move/speed", speed)
    anim_tree.process(delta)
```

### Transition Conditions

Set transition conditions in the AnimationTree editor:
- **Blend**: Use blend amounts based on parameters (e.g., speed)
- **One Shot**: Play once then return (for attacks, interactions)
- **Transition Rules**: Define when transitions are allowed

## Blend Spaces

### 1D Blend Space

Use for animations ordered along a single axis (e.g., walk speed).

```gdscript
# AnimationTree setup:
# BlendSpace1D: Walk -> Run -> Sprint
# Parameter: "speed" (float)

anim_tree.set("parameters/BlendSpace1D/speed", current_speed)
```

### 2D Blend Space

Use for directional movement blending.

```gdscript
# AnimationTree setup:
# BlendSpace2D: X = speed, Y = direction blend
# Parameters: "speed" and "direction"

anim_tree.set("parameters/BlendSpace2D/speed", velocity.length())
anim_tree.set("parameters/BlendSpace2D/direction", velocity.angle())
```

### Directional Blend Space (Godot 4.x)

Use a directional blend for 8-directional character animations.

```gdscript
# Set up AnimationNodeBlendDBone2D for directional blending
@onready var anim_tree = $AnimationTree

func _physics_process(delta: float):
    var dir = velocity.normalized()
    anim_tree.set("parameters/Directional/speed", velocity.length())
    anim_tree.set("parameters/Directional/direction", dir)
    anim_tree.process(delta)
```
## Animation Libraries and Blending Tracks

### Animation Libraries

Group related animations into libraries for organization.

```gdscript
# Access library animations by name
@onready var anim_player = $AnimationPlayer

func play_animation(anim_name: String):
    # Animations are organized by library in the editor
    anim_player.play(anim_name)

# List available animations
func get_available_animations() -> Array:
    return anim_player.get_animation_list()
```

### Blending Tracks

Blend between multiple animation tracks for smooth transitions.

```gdscript
# Set blend amount in AnimationTree
anim_tree.set("parameters/Idle/blend_amount", 1.0)

# Blend between two animations
anim_player.play("idle", -1.0, 1.0)  # loop, 1s fade-in
anim_player.play("walk", -1.0, 0.5)  # loop, 0.5s fade-in

# Crossfade by playing both simultaneously
# The AnimationTree blend space handles the mixing
```
## Root Motion for Character Movement

### Using Root Motion in AnimationTree

Root motion applies bone animation directly to the character transform.

```gdscript
class_name RootMotionCharacter extends CharacterBody3D

@onready var anim_tree = $AnimationTree
@onready var anim_state = anim_tree.get("state_machine")

@export var root_motion_enabled: bool = true

func _physics_process(delta: float):
    # Calculate root motion displacement
    var prev_transform = global_transform
    
    # Process animation tree (applies root motion)
    anim_tree.process(delta)
    
    if root_motion_enabled:
        var root_delta = global_transform.xform_inv(prev_transform)
        velocity = Vector3(root_delta.origin.x / delta, 0, root_delta.origin.z / delta)
    else:
        # Use scripted movement instead
        velocity = transform.basis.z * speed
    
    move_and_slide()
```

### When to Use Root Motion
- Platformer jump arcs (precise landing positions)
- Attack animations with fixed reach distances
- Cutscene character movements

### When to Avoid Root Motion
- Multiplayer games (server authority conflicts)
- Characters that need precise position control
- Games with custom physics responses
## Godot 4.7 Animation Features

### Collapsible Animation Tracks

Godot 4.7 introduces collapsible animation tracks for better organization in the AnimationPlayer editor.

```gdscript
# No code change needed — this is an editor feature
# In the AnimationPlayer inspector, click track headers to collapse/expand
# Group related properties under collapsible sections
```

### tween_await() for Sequential Animations

Use await with tweens for clean sequential animation chains.

```gdscript
func play_combo_animation():
    # Chain animations without nested callbacks
    await create_tween().tween_property($Sprite, "offset:x", 10.0, 0.1).finished
    await create_tween().tween_property($Sprite, "offset:x", 0.0, 0.1).finished
    print("Combo animation complete")

# Or with AnimationPlayer
func play_with_wait():
    var tween = create_tween()
    anim_player.play("attack")
    await tween.tween_interval(0.5)
    anim_player.play("recovery")
```
## Animation Performance Tips

- Use **AnimationTree** with state machines instead of multiple AnimationPlayers
- Keep animation libraries small and focused
- Use **AnimationNodeSync** to synchronize multiple character animations
- Preload animation resources with preload() for always-needed scenes
- Avoid animating properties that can be set directly (e.g., position vs tween)
- Use `animation_finished` signal instead of polling for completion

## Quick Reference: Animation Methods

| Method | Use Case |
|--------|----------|
| `anim_player.play(name)` | Start an animation |
| `anim_player.play(name, fade_time)` | Crossfade to animation |
| `anim_tree.process(delta)` | Update state machine |
| `anim_tree.set("params/...", value)` | Set blend parameters |
| `state_machine.travel(name)` | Switch to a state |
| `create_tween()` | Create animation tweens |
| `await tween.finished` | Wait for tween completion |

## MCP Bridge Tools (Optional — Live Editor Integration)

When the MCP bridge is running (Phase 2), these tools enhance animation debugging:

- **`animation_play`** — Play any animation from the project without opening the editor
- **`animation_list`** — List all available animations and their libraries
- **`animation_state_get`** — Query current AnimationTree state machine status
- **`animation_preview_frame`** — Preview a specific frame of any animation

> **Note:** MCP tools require the Godot editor to be running with the MCP plugin enabled. Skills work independently without the bridge.

## References

- [AnimationPlayer Documentation](references/animationplayer-guide.md)
- [AnimationTree State Machine Patterns](references/animationtree-states.md)
- [Blend Space Design Guide](references/blend-spaces.md)