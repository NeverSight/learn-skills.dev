---
name: godot-scene-organization
description: Structures Godot 4 projects so scenes stay reusable and references do not break - when to make a scene, a script or a Resource, instancing with @export PackedScene, preload and load, @onready and %UniqueName node access, _ready order, groups, autoloads, class_name, and resource UIDs with the .uid files added in Godot 4.4, including how to move or rename files safely. Use when creating new scenes or scripts, deciding how nodes find each other, adding global state or an event bus, moving or renaming files, editing .tscn files by hand, or fixing "Node not found", null @onready variables or broken references after a move.
license: MIT
compatibility: Godot 4.3 or later (snippets tested on 4.7.2)
---

# Scene organization in Godot 4

## Scene, script or Resource

- **Scene (`.tscn`)**: a reusable tree of nodes with its own resources: a player, an enemy, a pickup, a UI panel, a level. Anything you place more than once or want to run alone (F6) is a scene.
- **Script (`.gd`)**: behaviour attached to one node. Attach it to the root of the scene it controls, not to a parent that reaches into it.
- **Resource script (`extends Resource` with `class_name`)**: data without a node, such as item stats, wave definitions or save data, edited in the Inspector and saved as `.tres`.

A scene should work when run on its own. If it needs something from outside (a target, a spawn parent), expose it with `@export` or a signal instead of `get_parent()` chains.

## Instancing scenes

```gdscript
extends Node2D

@export var enemy_scene: PackedScene
@export var spawn_parent: Node2D


func spawn_enemy(at: Vector2) -> void:
	var enemy := enemy_scene.instantiate() as Node2D
	enemy.position = at
	spawn_parent.add_child(enemy)


func load_level(path: String) -> void:
	var packed := load(path) as PackedScene
	if packed == null:
		push_error("Level not found: " + path)
		return
	get_tree().change_scene_to_packed(packed)
```

- `@export var x: PackedScene` is set in the Inspector and survives file moves, because the scene stores the reference.
- `const BULLET := preload("res://bullet.tscn")` resolves at parse time: a missing file is a parse error (`Preload file "res://bullet.tscn" does not exist.`). Good for fixed assets.
- `load()` resolves at runtime and returns `null` with an error if the path is wrong. Use it for paths built at runtime.
- `instantiate()` (not Godot 3's `instance()`) returns a `Node`; cast it to the type you need. Free instances with `queue_free()`.

## Finding nodes

```gdscript
extends Control

@onready var title: Label = %Title
@onready var start_button: Button = %StartButton
@onready var music: AudioStreamPlayer = $Music
@onready var optional_hint: Label = get_node_or_null("Hint")


func _ready() -> void:
	title.text = "Main menu"
	start_button.grab_focus()
	if optional_hint:
		optional_hint.visible = false
	music.play()
```

- `$Path` is `get_node("Path")`, relative to this node. It errors if the node is missing; use `get_node_or_null()` for optional nodes.
- `%Name` reaches a node marked "Access as Unique Name" (right-click in the Scene dock) anywhere in the same scene, so it survives reparenting inside the scene. It does not reach into instanced child scenes: use `$Child/%Name`, or `%Child/%Name` when the instance is itself unique.
- `@onready` variables are assigned just before `_ready()`. They are `null` in `_init()` and `_enter_tree()`.
- `_ready()` runs on children before their parent, so a parent's `_ready()` can use its children, but a child's `_ready()` must not rely on the parent being ready.
- Type `@onready` variables (`: Label`) so the parser checks member names; `$Label.txt` on an untyped path is only caught at runtime.

## Groups

Groups tag nodes across scenes. Add them in the Node dock (Groups tab) or in code, then query the tree:

```gdscript
extends Node


func _ready() -> void:
	add_to_group("enemies")


func alert_all_enemies() -> void:
	get_tree().call_group("enemies", "set_alerted", true)
	for enemy in get_tree().get_nodes_in_group("enemies"):
		print(enemy.name)
	var player := get_tree().get_first_node_in_group("player") as Node2D
	if player:
		print("Player at ", player.global_position)
```

`call_group()` calls immediately in Godot 4. Use `get_tree().call_group_flags(SceneTree.GROUP_CALL_DEFERRED, ...)` to defer.

## Autoloads

An autoload is a node created before the main scene and kept across scene changes. Use it for state that outlives one scene (settings, save data, a scene switcher) and for a signal-only event bus. Register it in Project Settings > Globals > Autoload; `project.godot` then contains:

```ini
[autoload]

Events="*res://autoload/events.gd"
```

The `*` means "Enable" is checked, so scripts can use the name directly (`Events.player_died.emit()`). Do not `free()` or `queue_free()` an autoload. Keep autoloads few: anything that belongs to one level should live in that level's scene.

Note for tools: `godot --check-only --script` does not load autoloads, so a script that uses an autoload name reports `Identifier not found: Events` there even though it runs fine. Verify such scripts by running the scene (see the godot-verify skill).

## class_name

`class_name Player` registers a global type, so other scripts can write `var player: Player` and get member checking. The editor keeps a global class cache in `.godot/`; after adding a `class_name` outside the editor, open the editor or run `godot --headless --path . --import` before checking scripts that use it.

## UIDs, .uid files and moving files

Godot 4 references resources by UID as well as path. Scenes and resources store their own UID in the file header, imported assets in their `.import` file, and since Godot 4.4 scripts and shaders get a companion file (`player.gd.uid`, `water.gdshader.uid`). An editor-saved reference looks like:

```text
[ext_resource type="Script" uid="uid://dxxoiuob4eoum" path="res://game_manager.gd" id="1_feb5d"]
```

Rules:

- Commit `*.uid` files to version control. Do not add them to `.gitignore`.
- Move and rename files in the Godot FileSystem dock when you can; it updates references.
- When moving a script or shader outside Godot (shell, IDE, agent), move its `.uid` file with it, then open the editor or run `godot --headless --path . --import` so the UID cache learns the new path. Until that scan, the old path is still used and loading fails.
- If the `.uid` file is left behind, Godot generates a new UID for the moved script and scenes that referenced the old one fall back to their stale path: `WARNING: ... invalid UID: uid://... - using text path instead: res://old/path.gd`, then `ERROR: ... referenced non-existent resource`.
- When writing a `.tscn` by hand, do not invent `uid=` values. Omit the attribute and use a correct `path`; the editor adds UIDs when it next saves the scene.
- A hand-written Godot 4 scene starts with `[gd_scene format=3]` and references resources by string id: `[ext_resource type="Script" path="res://main.gd" id="1_main"]`, then `script = ExtResource("1_main")` on the node. Child nodes need `parent="."` or a path from the root. Godot 4.7 also writes `unique_id=` on nodes; omit it by hand.
- `load("uid://...")` and `preload("uid://...")` accept UID strings. Copy a UID from the FileSystem dock context menu; `ResourceUID.id_to_text(ResourceLoader.get_resource_uid(path))` returns it from code.

## Common mistakes

- Reaching up with `get_parent().get_parent()` or absolute paths like `/root/Main/Player`. Export a reference, use a group, or emit a signal.
- Using a node in `_init()` or before it entered the tree.
- Hard-coding `res://` paths to scenes in many scripts instead of exporting a `PackedScene`.
- Moving `.gd` files without their `.uid` files, or ignoring `*.uid` in git.
- Making everything an autoload because it is convenient.
