---
name: godot
description: "MANDATORY for ALL GDScript/.gd files and Godot resources (.tscn, .tres). Invoke this skill FIRST before writing ANY Godot code—never write GDScript directly without this skill. Provides documentation lookup, syntax checking, and testing instructions."
---

# Godot development

Requirements:
- Godot 4+
- `godot-docs` MCP server (npm package `@fernforestgames/mcp-server-godot-docs`)
- `godot-editor` MCP server (GitHub project `fernforestgames/mcp-server-godot-editor` installed into `addons/`)

## GDScript workflow

When writing or modifying GDScript, copy this checklist and track your progress:

```
- [ ] Step 1: Read source files
- [ ] Step 2: Look up relevant Godot documentation
- [ ] Step 3: Write or modify GDScript code
- [ ] Step 4: Import new files with Godot CLI
- [ ] Step 5: Typecheck and validate syntax
- [ ] Step 6: Test the changes
```

### Step 1: Read source files

Read any relevant GDScript source files in the current project.

### Step 2: Look up relevant Godot documentation

Use the `godot-docs:get_godot_class` tool to look up everything about a specific Godot class.
Use the `godot-docs:search_godot_docs` tool to find a string in the Godot documentation.

### Step 3: Write or modify GDScript code

Adhere to the following rules while writing GDScript:
- Use the latest Godot 4.5 syntax and features, including typed arrays and dictionaries: `Array[int]`, `Dictionary[String, float]`, etc.
- Always use static typing
- Don't use `:=` type inference declarations for AI-generated code (prefer explicit annotations)
- Prefix private variables/methods with `_`
- Indent with tabs
- Use `@export` or dependency injection instead of hardcoded node paths
- Prefer methods with static typing over equivalent `StringName` variants

### Step 4: Import new files with Godot CLI

Run the Godot CLI with `--import` after adding new files, to make sure they get picked up by the editor:

```sh
godot --headless --import
```

This should be run in the project root directory (where `project.godot` is located). Remember that any folder containing `.gdignore` will be skipped during import.

### Step 5: Typecheck and validate syntax

Directly invoke the provided `check_syntax.sh` script to check the syntax of all GDScript files in the project.

For example:

```sh
./.claude/skills/godot/scripts/check_syntax.sh
```

### Step 6: Test the changes

Use the testing workflow described below to test your changes.

## Testing workflow

### Automated tests

Unit tests can be written with the GUT (Godot Unit Test) framework:
https://github.com/bitwes/Gut
https://gut.readthedocs.io

If not already present in the current project in the `addons/` directory, do NOT attempt to install it. Ask the user to install it from the Godot Asset Library instead.

**Important:** use a sub-agent to write and run GUT tests, as this consumes a lot of tokens.

#### Writing tests

Test cases should be scripts that extend `GutTest`:

```gdscript
extends GutTest

# GUT assertions are untyped, so disable this warning
@warning_ignore_start("unsafe_call_argument")

func before_all():
	pass

func before_each():
	pass

func test_passes():
	assert_eq(1, 1)

func test_fails():
	assert_eq("hello", "goodbye")

func after_each():
	pass

func after_all():
	pass
```

Run the Godot CLI with `--import` after adding new files, to make sure they get picked up by the editor:

```sh
godot --headless --import
```

This should be run in the project root directory (where `project.godot` is located).

**Assertions**

```gdscript
assert_true(got)
assert_false(got)
assert_null(got)
assert_not_null(got)

assert_eq(got, expected)
assert_eq_deep(got, expected)  # Like assert_eq but more detailed failure messages for nested collections
assert_almost_eq(got, expected, error_interval)
assert_ne(got, not_expected)
assert_ne_deep(got, not_expected)
assert_almost_ne(got, not_expected, error_interval)
assert_gt(got, expected)
assert_gte(got, expected)
assert_lt(got, expected)
assert_lte(got, expected)

assert_same(got, expected)  # Checks that reference types (Object, Dictionary, Array) are exactly the same reference
assert_not_same(got, expected)

assert_has(obj, element)
assert_does_not_have(obj, element)

assert_is(obj, class_or_script_obj)
assert_typeof(obj, type_constant)  # TYPE_INT, TYPE_STRING, etc.
assert_not_typeof(obj, type_constant)

assert_engine_error(matching_text)
assert_engine_error_count(count)
assert_push_error(matching_text)
assert_push_error_count(count)
assert_push_warning(matching_text)
assert_push_warning_count(count)

assert_freed(obj)
assert_not_freed(obj)
```

**Helpers**

```gdscript
await wait_seconds(10)
await wait_idle_frames(5)  # 5 _process frames
await wait_physics_frames(2)
await wait_for_signal(scene_tree.node_removed, 3)  # time out after 3 seconds
await wait_until(callable, 3)  # time out after 3 seconds
```

#### Running tests

Once tests have been written and imported, run them using the GUT command line script:

```sh
godot --headless --script addons/gut/gut_cmdln.gd

# Run a specific test file
godot --headless --script addons/gut/gut_cmdln.gd -gtest=res://tests/sample_tests.gd
```

GUT is configured with an optional `res://.gutconfig.json` file. A sample can be generated with:

```sh
godot --headless --script addons/gut/gut_cmdln.gd -gprint_gutconfig_sample
```

### Interactive testing with the Godot Editor MCP server

The `godot-editor` MCP server allows you to control running games from the editor, enabling automated UI testing and visual verification.

#### Starting and stopping scenes

```
godot-editor:play_main_scene      # Start the project's main scene
godot-editor:play_scene           # Start a specific scene by path (e.g., "res://levels/test.tscn")
godot-editor:stop_playing_scene   # Stop the currently running scene
```

**Important:** Always follow up `play_main_scene` or `play_scene` with another action (screenshot, input, etc.) or `stop_playing_scene`. Never leave a scene running indefinitely.

#### Taking screenshots

Use `godot-editor:take_screenshot` to capture the current game viewport. The screenshot is returned as an image that you can view directly.

#### Node interaction

Use `godot-editor:click_node` and `godot-editor:hover_node` to interact with controls and nodes (2D or 3D). Use `godot-editor:get_node_tree` to inspect the current scene tree and determine node paths.

```
godot-editor:click_node
  node_path: "/root/Main/UI/StartButton"
  button_index: 1  # Optional, defaults to left click
  offset: {x: 0, y: 0}  # Optional offset from center

godot-editor:hover_node
  unique_name: "InventorySlot"

godot-editor:click_node
  accessibility_name: "SubmitButton"
```

#### Input synthesis

Use `godot-editor:synthesize_input` to simulate user input events (only if you cannot use `click_node` or `hover_node`).

For example:
- `type: "key", keycode: "Space", pressed: true` (uses Key enum names)
- `type: "mouse_button", button_index: 1, position: {x, y}, pressed: true`
- `type: "mouse_motion", position: {x, y}`
- `type: "action", action: "ui_accept", pressed: true`

#### Example workflow for UI testing

1. `godot-editor:play_main_scene`
2. `godot-editor:take_screenshot`, verify initial state
3. `godot-editor:get_node_tree`, check node paths
4. `godot-editor:hover_node` with unique_name "PlayButton"
5. `godot-editor:take_screenshot`, verify hover visual feedback
6. `godot-editor:click_node` with unique_name "PlayButton"
7. `godot-editor:take_screenshot`, verify button was clicked (new screen, animation, etc.)
8. `godot-editor:stop_playing_scene`

## Godot resource files (.tres, .tscn)

- NEVER manually assign or generate `uid://` fields—Godot fills these in automatically

### Connecting @exports in scene files

When a script uses `@export var some_node: SomeNodeType`, you can assign it via a `.tscn` file:
```
[node name="MyNode" type="Node3D" parent="." node_paths=PackedStringArray("player", "camera")]
script = ExtResource("1_abc123")
player = NodePath("../Player")
camera = NodePath("CameraPivot/Camera3D")
```
