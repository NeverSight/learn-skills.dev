---
name: godot-verify
description: Verifies GDScript and scenes with the Godot 4 command line instead of trusting that code looks right - parse-checking scripts with --check-only, running a scene headless with --quit-after, writing a SceneTree test script with an exit code, and reading the output, because Godot exits with code 0 even when scripts fail at runtime. Use after writing or editing any GDScript, .tscn or project.godot, before telling the user a change works, and when a fix needs evidence from the engine rather than from reading code.
license: MIT
compatibility: Godot 4.3 or later (snippets tested on 4.7.2)
---

# Verifying Godot 4 changes from the command line

Reading code is not verification. Run the engine and read what it prints. Use the Godot 4 editor binary the project targets (often `godot` on PATH); the commands below use `godot` and run from the project root (the folder with `project.godot`). `--headless` needs no display or GPU.

## 1. Parse-check each changed script

```bash
godot --headless --path . --check-only --script res://player/player.gd
```

Parse errors print as `SCRIPT ERROR: Parse Error: <message>` followed by `at: GDScript::reload (res://player/player.gd:<line>)`, and the exit code is 1. A clean script prints only the version banner.

Check every new or modified script in a git checkout, staged or not, in one go (from the project root; paths with spaces need a different loop):

```bash
for f in $( { git diff --name-only --relative --diff-filter=d HEAD -- '*.gd'; git ls-files --others --exclude-standard -- '*.gd'; } | sort -u); do
  out=$(godot --headless --path . --check-only --script "res://$f" 2>&1)
  if echo "$out" | grep -q 'ERROR'; then echo "== $f"; echo "$out" | grep -A1 'ERROR'; fi
done
```

Known limits of `--check-only`:

- **`class_name` types from other files** are unknown until the editor has scanned the project. In a fresh clone or after adding a `class_name` outside the editor, run `godot --headless --path . --import` once (it also writes `.uid` files and imports assets), or every use reports `Could not find type "MyClass" in the current scope.` (in a type annotation) or `Identifier "MyClass" not declared in the current scope.` (in an expression).
- **Autoload names** are never resolved. A script that uses an autoload such as `Events` reports `Compile Error: Identifier not found: Events` even though the game runs. Verify those scripts by running a scene (step 2).
- **Members missing on other objects' classes** (for example Godot 3's `scene.instance()` on a `PackedScene`, or `$Panel.rect_size`) pass with default settings. To make them fail, set `debug/gdscript/warnings/unsafe_method_access` and `unsafe_property_access` to Error (`2`) in a temporary `override.cfg` in the project root and delete it afterwards. Do not leave them in `project.godot`: they turn every untyped call into a parse error. See the godot-4-api-pitfalls skill.

## 2. Run the scene and read the output

```bash
timeout 60 godot --headless --path . --quit-after 300 res://levels/level_1.tscn 2>&1 | tee run.log
grep -nE 'SCRIPT ERROR|ERROR:|WARNING:' run.log
```

`--quit-after N` stops after N frames; `timeout` guards against a scene that blocks. Omit the scene path to run the project's main scene.

**The exit code is 0 even when scripts fail.** A null access (`SCRIPT ERROR: Cannot call method 'queue_free' on a null value.`) and even a parse error in an attached script (`Failed to load script ... with error "Parse error"`) both end with exit code 0. Always grep the output. A runtime error aborts the rest of that function, so missing `print()` output after an error is expected, not a second bug.

## 3. Test behaviour with a script that sets the exit code

For logic you can check without rendering, write a throwaway test that extends `SceneTree` and calls `quit(1)` on failure:

```gdscript
extends SceneTree


func _init() -> void:
	# Autoloads are added after _init(), so do the work on the first frame.
	_run.call_deferred()


func _run() -> void:
	var failures := 0
	var scene := load("res://player/player.tscn") as PackedScene
	if scene == null:
		printerr("FAIL: player scene did not load")
		failures += 1
	else:
		var player := scene.instantiate()
		root.add_child(player)
		await process_frame
		if not player.has_method("take_damage"):
			printerr("FAIL: player has no take_damage()")
			failures += 1
		player.queue_free()
	print("failures: ", failures)
	quit(1 if failures else 0)
```

```bash
godot --headless --path . --script res://tests/test_player.gd; echo "exit=$?"
```

Here the exit code is meaningful because the script sets it, but still read the output for `SCRIPT ERROR` lines from the code under test.

## What headless runs cannot show

Headless runs check logic, signals, physics and errors. They do not show what the screen looks like: UI that is cut off, wrong colours or a camera in the wrong place need a real window or a screenshot from a non-headless run. Say so when reporting, instead of claiming a visual change works.

## Report honestly

When you report back, include the commands you ran and the relevant output lines. "No `ERROR` lines in a 300-frame run of level_1.tscn" is evidence; "the code looks correct" is not.
