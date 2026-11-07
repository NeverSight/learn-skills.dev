---
name: godot-brainstorming
description: "Architecture decision patterns for Godot game development across genres (RPG, platformer, RTS, puzzle). Covers scene organization, state machines, network architecture, and component composition. Use when designing a Godot game's architecture or making Godot-specific technical decisions."
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
    - architecture
    - state-machines
    - multiplayer
  created: 2026-06-20
---

# Godot Brainstorming & Architecture

Help design game architecture using Godot's node-based composition model.

## Scene Organization Strategies

### Composition Over Inheritance

Godot's strength is scene composition. Prefer composing small, focused scenes over deep inheritance hierarchies.

```gdscript
# Instead of: PlayerCharacter extends CharacterBody2D with all abilities
# Use: Compose a player from reusable components
# - BaseCharacter (CharacterBody2D) — movement, health
# - InventoryComponent (Node) — inventory logic
# - AbilitySystem (Node) — ability management
```

### Scene Hierarchy Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Single root scene | Entire game/level | Main.tscn, Level1.tscn |
| Component scenes | Reusable behaviors | HealthBar.tscn, ProgressBar.tscn |
| Entity templates | Instantiable objects | Enemy.tscn, Collectible.tscn |
| UI compositions | Complex screens | MainMenu.tscn, SettingsPanel.tscn |

## State Machine Patterns

### AnimationTree State Machine

```gdscript
@export var animation_tree: AnimationTree
@onready var state_machine: AnimationNodeStateMachinePlayback = \
    animation_tree.get("parameters/playback")

func change_state(new_state: String):
    state_machine.travel(new_state)
```

### Custom State Machine

For complex AI or game logic:

```gdscript
class_name GameState extends RefCounted

var current_state: String = "menu"

func transition_to(new_state: String):
    var prev = current_state
    current_state = new_state
    on_transition(prev, new_state)

func on_transition(from: String, to: String):
    match to:
        "playing": handle_playing()
        "paused": handle_paused()
```

## Network Architecture Decisions

### Authoritative Server Model
- Best for competitive multiplayer
- Server validates all actions
- Client sends inputs, server simulates

### Peer-to-Peer Model
- Best for casual/co-op games
- Lower latency for local interactions
- Higher cheating risk

### Godot 4.7: Steam Frame Integration
For multiplayer with Steam, use the new Steam Frame configuration for lobby management and overlay features.

## Genre-Specific Patterns

### RPG Architecture
- Entity-component system for character stats
- Dialogue tree system (use `RichTextLabel` + custom parser)
- Save/load system using `JSON` or `Resource` serialization

### Platformer Architecture
- Level streaming for large worlds
- Input buffering for responsive controls
- TileMapLayer for layered level design

### RTS Architecture
- Pathfinding with A* on NavigationMesh
- Unit grouping and selection system
- Command queue pattern for input handling

## Godot 4.7 Brainstorming Considerations

- **tween_await()** — Use for sequential animation chains instead of nested callbacks
- **VirtualJoystick** — Built-in mobile controls simplify mobile game development
- **Control offset transforms** — New UI animation system enables complex transitions without custom shaders

## MCP Bridge Tools (Optional — Live Editor Integration)

When the MCP bridge is running (Phase 2), these tools can inspect your live project:

- **`scene_tree`** — Inspect current scene hierarchy for architecture decisions
- **`class_db_info`** — Query class capabilities to choose the right node type
- **`map_project`** — Generate a project graph to visualize architecture
- **`project_settings_read`** — Check current project configuration during brainstorming

> **Note:** MCP tools require the Godot editor to be running with the MCP plugin enabled. Skills work independently without the bridge.

## References

- [Scene Composition Patterns](references/scene-composition.md)
- [State Machine Implementations](references/state-machines.md)
- [Network Architecture Guide](references/network-architecture.md)
