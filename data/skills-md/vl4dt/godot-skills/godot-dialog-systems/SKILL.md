---
name: godot-dialog-systems
description: "Dialogue system patterns for Godot 4.x: resource-based dialogue trees, branching narratives, typewriter text effects, voice sync, and portrait management. Use when building NPC conversations, quest dialogue, or narrative systems in Godot."
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
    - dialogue
    - narrative
    - branching
    - typewriter
  created: 2026-06-21
---

# Dialogue Systems in Godot

Patterns for building conversation and narrative systems.

## Resource-Based Dialogue Data

Store dialogue as `Resource` files for easy editing and versioning:

```gdscript
class_name DialogueLine extends Resource

@export var speaker: String = ""
@export var text: String = ""
@export var voice_file: String = ""  # Optional audio cue
@export var portrait_index: int = -1
@export var next_line_id: String = ""  # Branch target
@export var choices: Array[DialogueChoice] = []

class_name DialogueChoice extends Resource

@export var choice_text: String = ""
@export var target_line_id: String = ""
@export var requires_flag: String = ""  # Optional quest flag check
```

### Dialogue Script Resource

```gdscript
class_name DialogueScript extends Resource

@export var script_name: String = ""
@export var start_line_id: String = ""
@export var lines: Dictionary = {}  # id -> DialogueLine
```

## Dialogue Manager

Central system for playing dialogue sequences:

```gdscript
class_name DialogueManager extends Node

signal dialogue_started(speaker: String, text: String)
signal dialogue_ended()
signal choice_presented(choices: Array[DialogueChoice])
signal typewriter_progress(chars_shown: int, total_chars: int)

var current_script: DialogueScript = null
var current_line: DialogueLine = null
var is_playing: bool = false
var flags: Dictionary = {}  # Quest/state flags

func play(script: DialogueScript) -> void:
    current_script = script
    is_playing = true
    _show_line(script.start_line_id)

func _show_line(line_id: String) -> void:
    if not current_script.lines.has(line_id):
        push_error("DialogueManager: Line '%s' not found" % line_id)
        end_dialogue()
        return

    current_line = current_script.lines[line_id] as DialogueLine
    dialogue_started.emit(current_line.speaker, current_line.text)

    if current_line.choices.size() > 0:
        choice_presented.emit(current_line.choices)
    else:
        # Auto-advance after typewriter
        _auto_advance()

func advance() -> void:
    if not current_line:
        return
    if current_line.next_line_id.is_empty():
        end_dialogue()
    else:
        _show_line(current_line.next_line_id)

func select_choice(choice_index: int) -> void:
    if not current_line or choice_index >= current_line.choices.size():
        return
    var choice = current_line.choices[choice_index]

    # Check flag requirement
    if not choice.requires_flag.is_empty():
        if not flags.get(choice.requires_flag, false):
            return  # Player hasn't met requirement

    _show_line(choice.target_line_id)

func end_dialogue() -> void:
    is_playing = false
    current_script = null
    current_line = null
    dialogue_ended.emit()

func set_flag(flag: String, value: bool = true) -> void:
    flags[flag] = value
```

## Typewriter Text Effect

Animate text appearing character-by-character:

```gdscript
class_name DialogueText extends RichTextLabel

signal typing_complete()

@export var type_speed: float = 0.03  # Seconds per character
var _type_timer: float = 0.0
var _full_text: String = ""
var _char_index: int = 0
var _is_typing: bool = false
var _waiting_for_input: bool = false

func start_typing(text: String) -> void:
    _full_text = text
    _char_index = 0
    _is_typing = true
    _waiting_for_input = false
    text = ""

func _process(delta: float) -> void:
    if not _is_typing:
        return

    if _waiting_for_input:
        return  # Wait for player to click to advance

    _type_timer += delta
    if _type_timer >= type_speed and _char_index < _full_text.length():
        _type_timer = 0.0
        _char_index += 1
        text = _full_text.substr(0, _char_index)
        DialogueManager.typewriter_progress.emit(_char_index, _full_text.length())

        if _char_index >= _full_text.length():
            _is_typing = false
            typing_complete.emit()

# Skip to end on input
func _gui_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        if _is_typing:
            # Show remaining text instantly
            text = _full_text
            _char_index = _full_text.length()
            _is_typing = false
            typing_complete.emit()
```

## Branching Dialogue Pattern

Handle conditional branches based on game state:

```gdscript
# In dialogue script editor or code:
# Line "greeting":
#   text: "Hello there, {0}!"
#   choices:
#     - text: "Hi!" → target: "friendly_chat"
#     - text: "Who are you?" → target: "hostile_chat"
#     - text: "I need help." → target: "quest_offer" (requires: met_quest_giver)

func _resolve_branch(line_id: String) -> String:
    var line = current_script.lines[line_id] as DialogueLine
    if line.choices.size() == 0:
        return line.next_line_id

    # Filter choices by flags
    var valid_choices: Array[DialogueChoice] = []
    for choice in line.choices:
        if choice.requires_flag.is_empty():
            valid_choices.append(choice)
        elif flags.get(choice.requires_flag, false):
            valid_choices.append(choice)

    # If no valid choices, use default next_line_id
    if valid_choices.size() == 0:
        return line.next_line_id

    return ""  # Wait for player choice
```

## Portrait Management

Display character portraits during dialogue:

```gdscript
class_name DialoguePortrait extends Container

@export var portrait_frames: Array[Texture2D] = []

func show_portrait(index: int) -> void:
    if index < 0 or index >= portrait_frames.size():
        return
    # Update portrait sprite with frame[index]
    pass

# Animate portrait reactions (idle, talking, surprised)
enum PortraitState { IDLE, TALKING, SURPRISED }
var current_state: PortraitState = PortraitState.IDLE
```

## Godot 4.7 Dialogue Notes

- **tween_await()** — Animate dialogue panel entrance/exit smoothly: `await get_tree().create_tween().tween_property(panel, "modulate:a", 1.0).finished`
- **RichTextLabel** — Improved bbcode for dialogue formatting (`[wave]`, `[shake]`, `[carousel]`)

## MCP Bridge Tools (Optional — Live Editor Integration)

When the MCP bridge is running (Phase 2), these tools can inspect and modify your project live:

- **`script_read`** / **`script_edit`** — Read and modify dialogue scripts
- **`scene_tree`** — Inspect dialogue UI node hierarchy

> **Note:** MCP tools require the Godot editor to be running with the MCP plugin enabled. Skills work independently without the bridge.

## References

- [Dialogue Resource Design](references/dialogue-resources.md)
- [Branching Narrative Patterns](references/branching-narrative.md)
- [Typewriter Effect Variants](references/typewriter-effects.md)
