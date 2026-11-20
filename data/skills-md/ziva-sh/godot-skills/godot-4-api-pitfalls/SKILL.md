---
name: godot-4-api-pitfalls
description: Fixes Godot 3 APIs and GDScript syntax that AI assistants write into Godot 4 projects, such as KinematicBody2D, move_and_slide(velocity), export, onready, setget, yield, string connect(), instance(), rand_range, the Tween node, File, change_scene, Spatial, rect_* properties, Pool*Array, OS time functions and the old TileMap API. Use when writing, reviewing or porting GDScript for Godot 4.x, when a script fails with "not declared", "not found in base", "was removed in Godot 4" or "is not present on the inferred type", or when adapting a Godot 3 tutorial, forum answer or asset.
license: MIT
compatibility: Godot 4.3 or later (snippets tested on 4.7.2)
---

# Godot 4 API pitfalls

Most GDScript in tutorials, forum answers and model training data is Godot 3. Godot 4 renamed classes, methods and properties and changed the GDScript syntax. Some Godot 3 code fails to parse, and some parses but breaks only at runtime. Before writing code, confirm the version: `project.godot` has a line like `config/features=PackedStringArray("4.7", ...)`.

## Rewrite table

| Godot 3 (wrong in Godot 4) | Godot 4 |
| --- | --- |
| `KinematicBody2D`, `KinematicBody` | `CharacterBody2D`, `CharacterBody3D` |
| `velocity = move_and_slide(velocity, Vector2.UP)` | Set the `velocity` property, then call `move_and_slide()` with no arguments. `up_direction` and `floor_snap_length` are properties |
| `export var x = 1`, `export(int, 0, 10) var x` | `@export var x := 1`, `@export_range(0, 10) var x: int` |
| `export(String, FILE, "*.json") var path` | `@export_file("*.json") var path: String` |
| `export(Array, int) var a` | `@export var a: Array[int]` |
| `onready var`, `tool` | `@onready var`, `@tool` |
| `var hp setget set_hp, get_hp` | `var hp: int: set = set_hp, get = get_hp`, or an inline `set(value):` block |
| `yield(obj, "signal_name")` | `await obj.signal_name` |
| `yield(get_tree().create_timer(1.0), "timeout")` | `await get_tree().create_timer(1.0).timeout` |
| `yield(get_tree(), "idle_frame")` | `await get_tree().process_frame` |
| `connect("pressed", self, "_on_pressed", [arg])` | `pressed.connect(_on_pressed.bind(arg))` |
| `emit_signal("died")` | `died.emit()` (the string form still works but typos are only found at runtime) |
| `scene.instance()` | `scene.instantiate()` |
| `get_tree().change_scene(path)`, `change_scene_to(packed)` | `change_scene_to_file(path)`, `change_scene_to_packed(packed)` |
| `rand_range(a, b)` | `randf_range(a, b)` or `randi_range(a, b)` |
| `stepify`, `deg2rad`, `rad2deg`, `range_lerp`, `str2var` | `snapped`, `deg_to_rad`, `rad_to_deg`, `remap`, `str_to_var` |
| `Tween` node: `$Tween.interpolate_property(...)`, `start()` | `var tween := create_tween()`, then `tween.tween_property(node, "property", final_value, duration)` |
| `File.new()`, `file.open(path, File.READ)` | `FileAccess.open(path, FileAccess.READ)` (returns `null` on failure, see `FileAccess.get_open_error()`) |
| `Directory.new()` | `DirAccess.open(path)` |
| `to_json(v)`, `parse_json(s)` | `JSON.stringify(v)`, `JSON.parse_string(s)` |
| `OS.get_ticks_msec()`, `OS.get_unix_time()`, `OS.get_datetime()` | `Time.get_ticks_msec()`, `Time.get_unix_time_from_system()`, `Time.get_datetime_dict_from_system()` |
| `OS.window_fullscreen = true`, `OS.get_screen_size()` | `DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)`, `DisplayServer.screen_get_size()` |
| `OS.set_window_title("Game")` | `get_window().title = "Game"` |
| `Spatial`, `translation` | `Node3D`, `position` |
| `extends Reference`, `Transform`, `Quat` | `extends RefCounted`, `Transform3D`, `Quaternion` |
| `pause_mode = PAUSE_MODE_PROCESS` | `process_mode = PROCESS_MODE_ALWAYS` |
| `Sprite`, `AnimatedSprite`, `Position2D`, `Particles2D`, `TextureProgress` | `Sprite2D`, `AnimatedSprite2D`, `Marker2D`, `GPUParticles2D`, `TextureProgressBar` |
| `rect_position`, `rect_size`, `rect_min_size` | `position`, `size`, `custom_minimum_size` |
| `margin_left` (Control) | `offset_left` |
| `Label.align = Label.ALIGN_CENTER` | `horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER` |
| `add_color_override`, `add_font_override`, `add_stylebox_override`, `add_constant_override` | `add_theme_color_override`, `add_theme_font_override`, `add_theme_stylebox_override`, `add_theme_constant_override` |
| `Color.red`, `Color.white` | `Color.RED`, `Color.WHITE` |
| `PoolStringArray`, `PoolVector2Array`, `PoolIntArray`, `PoolRealArray` | `PackedStringArray`, `PackedVector2Array`, `PackedInt32Array`, `PackedFloat32Array` |
| `update()` (redraw a CanvasItem) | `queue_redraw()` |
| `TileMap.set_cellv(pos, id)`, `world_to_map` | `TileMapLayer.set_cell(coords, source_id, atlas_coords)`, `local_to_map` (see the godot-tilemaplayer skill) |
| `BUTTON_LEFT`, `BUTTON_WHEEL_UP` | `MOUSE_BUTTON_LEFT`, `MOUSE_BUTTON_WHEEL_UP` |
| `event.scancode`, `event.control` | `event.keycode` (or `physical_keycode`), `event.ctrl_pressed` |
| `array.empty()`, `array.remove(i)`, `array.invert()` | `is_empty()`, `remove_at(i)`, `reverse()` |
| `set_collision_layer_bit(0, true)` (0-based bit) | `set_collision_layer_value(1, true)` (1-based layer number) |
| `space_state.intersect_ray(from, to)` | `space_state.intersect_ray(PhysicsRayQueryParameters2D.create(from, to))` |
| `RayCast2D.cast_to` | `target_position` |
| `get_tree().set_input_as_handled()` | `get_viewport().set_input_as_handled()` |
| `remote func`, `remotesync func`, `puppet func`, `is_network_master()` | `@rpc("any_peer") func`, `@rpc("any_peer", "call_local") func`, `@rpc func` (only the authority may call it), `is_multiplayer_authority()`. `master func` has no direct equivalent: use `@rpc("any_peer")` and check `multiplayer.get_remote_sender_id()` |
| `Engine.editor_hint`, `filename` | `Engine.is_editor_hint()`, `scene_file_path` |
| `RectangleShape2D.extents` (half size) | `size` (full size, so double the old value) |
| `ResourceSaver.save(path, resource)` | `ResourceSaver.save(resource, path)` |

Less common renames (3D, XR, navigation, shaders, threads) are in [references/renames.md](references/renames.md).

## Before and after

Character controller:

```gdscript-godot3
extends KinematicBody2D

export var speed = 200
var velocity = Vector2()

func _physics_process(delta):
	velocity.x = Input.get_axis("ui_left", "ui_right") * speed
	velocity = move_and_slide(velocity, Vector2.UP)
```

```gdscript
extends CharacterBody2D

@export var speed := 200.0
@export var jump_velocity := -400.0


func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity += get_gravity() * delta
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = jump_velocity
	velocity.x = Input.get_axis("ui_left", "ui_right") * speed
	move_and_slide()
```

Properties, signals, timers and tweens:

```gdscript-godot3
tool
extends Node2D

export(int, 0, 100) var health = 100 setget set_health
onready var button = $Button

func _ready():
	button.connect("pressed", self, "_on_button_pressed")

func set_health(value):
	health = clamp(value, 0, 100)
	update()

func _on_button_pressed():
	$Tween.interpolate_property(self, "modulate:a", 1.0, 0.0, 0.5)
	$Tween.start()
	yield($Tween, "tween_all_completed")
	queue_free()
```

```gdscript
@tool
extends Node2D

@export_range(0, 100) var health: int = 100:
	set(value):
		health = clampi(value, 0, 100)
		queue_redraw()

@onready var button: Button = $Button


func _ready() -> void:
	button.pressed.connect(_on_button_pressed)


func _on_button_pressed() -> void:
	var tween := create_tween()
	tween.tween_property(self, "modulate:a", 0.0, 0.5)
	await tween.finished
	queue_free()
```

Files, time, randomness and scenes:

```gdscript-godot3
extends Node

func save_score(score):
	var file = File.new()
	file.open("user://save.json", File.WRITE)
	file.store_string(to_json({"score": score, "time": OS.get_unix_time()}))
	file.close()

func spawn(scene):
	var enemy = scene.instance()
	enemy.position = Vector2(rand_range(0, 100), 0)
	add_child(enemy)
```

```gdscript
extends Node

@export var enemy_scene: PackedScene


func save_score(score: int) -> void:
	var file := FileAccess.open("user://save.json", FileAccess.WRITE)
	if file == null:
		push_error("Cannot open save file: %s" % error_string(FileAccess.get_open_error()))
		return
	file.store_string(JSON.stringify({"score": score, "time": Time.get_unix_time_from_system()}))


func spawn() -> void:
	var enemy := enemy_scene.instantiate() as Node2D
	enemy.position = Vector2(randf_range(0.0, 100.0), 0.0)
	add_child(enemy)


func go_to_menu() -> void:
	get_tree().change_scene_to_file("res://menu.tscn")
```

## What the parser does not catch

`godot --check-only` reports an unknown member as an error only when the receiver is `self`, a built-in type (`Array`, `Vector2`, `Color`) or a class name called statically (`OS.get_unix_time()`); wrong argument counts and types are errors too. A member that is missing on an object, even a typed one such as `var shape := RectangleShape2D.new()`, is treated as "may exist on a subtype" and parses with default settings. These Godot 3 lines all pass `--check-only` on Godot 4.7.2 and fail only when they run:

- `scene.instance()` on a `PackedScene`, `get_tree().change_scene(path)`, `get_tree().set_input_as_handled()`
- `shape.extents` on a `RectangleShape2D`, `$Panel.rect_size`
- `event.scancode` or `event.control` on an `InputEvent`

To make the parser reject them during a check, put these lines in a temporary `override.cfg` next to `project.godot` (Godot reads it on top of `project.godot`, `--check-only` included) and delete it afterwards; if the project already has an `override.cfg`, append and restore it instead. `2` means Error:

```ini
[debug]
gdscript/warnings/unsafe_method_access=2
gdscript/warnings/unsafe_property_access=2
```

Do not leave these in the user's `project.godot` unless asked: at Error every untyped call such as `body.take_damage(1)` or `$Sprite.play()` is a parse error, and the game still starts with exit code 0, printing only `Failed to load script`. Typed code passes, so prefer typed references: `@onready var panel: Panel = $Panel`, and `var key := event as InputEventKey` before reading `key.keycode`.

Behaviour changes that no parser catches:

- Lifecycle methods such as `_ready()` no longer call the parent class implementation implicitly. Call `super()` when an inherited script needs it.
- `Array.slice(begin, end)` excludes `end`.
- `Camera2D.zoom` is inverted: larger values zoom in.
- `String.right(n)` returns the last `n` characters.
- `randomize()` runs automatically at startup. Set `seed()` for reproducible randomness.
- `call_group()` is immediate. Use `call_group_flags(SceneTree.GROUP_CALL_DEFERRED, ...)` for the old deferred behaviour.
- `AnimatedSprite2D.playing` was removed. Call `play()`.
- `TileMap` still exists but is deprecated. New code uses one `TileMapLayer` node per layer.

## Self-check

1. Search the scripts you wrote or changed for Godot 3 names (GNU grep; add `-P` or adapt for other greps):

   ```bash
   grep -rnE --include='*.gd' \
     -e '\b(KinematicBody2D|KinematicBody|Spatial|Position2D|Particles2D|TextureProgress)\b' \
     -e '\b(yield|setget|rand_range|stepify|deg2rad|rad2deg|range_lerp|to_json|parse_json|funcref)\b' \
     -e '\b(idle_frame|pause_mode|Reference|Quat)\b|\bPAUSE_MODE_' \
     -e '^(export|onready|tool)\b|^(remote|master|puppet)(sync)? func' \
     -e '\.instance\(|change_scene(_to)?\(|\b(File|Directory)\.new\(|OS\.(get_ticks|get_unix_time|get_datetime|window_)' \
     -e '\brect_[a-z_]+\b|(^|[^"])\bmargin_(left|right|top|bottom)\b|add_(color|font|stylebox|constant|icon)_override' \
     -e '\bPool[A-Za-z0-9]+Array\b|\bBUTTON_(LEFT|RIGHT|MIDDLE|WHEEL)|\.scancode\b|set_cellv|world_to_map|map_to_world' \
     -e 'connect\("[^"]+", *self|interpolate_property|\bextends +Sprite *$' .
   ```

   Rewrite each match with the table above. The quoted `"margin_left"` theme constants of `MarginContainer` are Godot 4 names and are not matched. No match does not prove the code is Godot 4: the list is the common subset.
2. Parse each changed script from the project root: `godot --headless --path . --check-only --script res://path/to/script.gd`. Read the output, not only the exit code. With the temporary `override.cfg` above, renamed members on typed objects fail here too.
3. Run the scene that uses the script and read its output, because runtime errors do not change the exit code. The godot-verify skill has the commands.
