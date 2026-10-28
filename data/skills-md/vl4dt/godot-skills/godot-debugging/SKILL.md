---
name: godot-debugging
description: "Debugging workflow for Godot 4.x: print vs push_error, editor output window, debugger panel, profiling with built-in profiler, network debugging, export/build troubleshooting. Use when debugging Godot games or resolving Godot-specific errors."
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
    - debugging
    - profiling
    - error-handling
  created: 2026-06-20
---

# Godot Debugging Guide

Comprehensive debugging workflow and common issue resolution for Godot 4.x.

## Output Methods

### print() vs push_error() vs push_warning()

```gdscript
# print() — General output, filtered in editor output
print("Debug: position = ", position)
print("Debug: player health = ", player_health)

# printf-style formatting
printf("Player %s has %d health", player_name, health)

# push_error() — Shows in red, includes file and line number
push_error("Failed to load resource: ", resource_path)

# push_warning() — Shows in yellow, non-fatal issues
push_warning("Missing animation for state: ", state)

# load() returns null on failure — check before use
var data = load(risky_path)
if data == null:
    push_error("Could not load resource at: %s" % risky_path)

# Or with ResourceLoader for error codes
var err, data = ResourceLoader.load_interactive(risky_path)
if err != OK:
    push_error("Failed to load: %s (error code %d)" % [risky_path, err])
```

### Editor Output Window

Access via **Window > Debugger** or **Debug > Start Debugging**. The output panel shows:
- Standard print output (gray)
- Warnings (yellow)
- Errors (red) with file/line info
- Custom logger messages

## Debugger Panel

### Built-in Debugger Features

1. **Scene Tree** — Visual tree of current scene with property inspection
2. **Resources** — List of loaded resources, check for leaks
3. **Profiler** — CPU and GPU usage breakdown
4. **Remote Transform** — Edit node properties in running scenes
5. **Network Profiler** — Monitor multiplayer traffic

### Remote Debugging

```gdscript
# Connect to remote scene tree from editor
# When running in debug mode (F6), the editor connects automatically

# Access remote nodes
func get_remote_node(path: String):
    var node = get_node(path)  # Works on local and remote
    return node
```

## Profiling Workflow

### CPU Profiler

```
Profile > Start Profiling in the editor
Then view: Profile > CPU Usage or Profile > Frame Time Graph
```

Key metrics:
- **Frame time** — Should be under 16.67ms for 60fps
- **Physics FPS** — Should match target (usually 60)
- **Script time** — Time spent in GDScript/C# code
- **Draw calls** — Number of GPU draw calls per frame

### Memory Profiler

```
Profile > Memory Usage
Check for:
- Growing resource count over time
- Unfreed scene instances
- Large textures not being unloaded
```

### GPU Profiler

```
Project Settings > Rendering > Debug > GPU Profiling = On
Then: Profile > GPU Usage
```

## Common Error Patterns & Fixes

### "Script class 'XXX' does not exist in current project"
- **Cause:** Autoload script reference broken after rename/move
- **Fix:** Re-add the autoload in Project Settings > Autoload

### "Cannot instantiate non-imported scene: res://..."
- **Cause:** Scene file not saved or path is incorrect
- **Fix:** Open the scene in editor and save it, verify path

### "Invalid get index 'XXX' (on base: 'Node2D')"
- **Cause:** Accessing a property that doesn't exist on the node
- **Fix:** Check node type and available properties, use `has_method()` or `is()` checks

### "Failed to connect signal"
- **Cause:** Method name mismatch or signal doesn't exist
- **Fix:** Verify signal exists on source node, check method signature matches

### Export/Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Export failed with code -1" | Missing export preset config | Re-create export preset |
| "Android build failed" | SDK/NDK path wrong | Check Project Settings > Android |
| "HTML5 export failed" | Emscripten not installed | Install Godot HTML5 export template |
| "Windows export failed" | MSVC not installed | Install Visual Studio Build Tools |

## Network Debugging

### Multiplayer API Inspection

```gdscript
# Check connection status
print("Connected: ", Network.multiplayer.is_connected_to_server())
print("Peer count: ", Network.multiplayer.get_peers().size())

# Log RPC calls for debugging
func _rpc_debug_message(msg):
    print("[RPC] ", msg)

# Monitor network traffic
# Use Profile > Network Profiler in the editor
```

### Lag Compensation Debugging

```gdscript
# Log timing information
print("Server time: ", get_tree().get_network_unique_id())
print("Local latency: ", Network.multiplayer.get_connection_status())
```

## Godot 4.7 Debugging Notes

- **Perfetto tracing** — New built-in Android profiler for detailed performance analysis
- **New editor log improvements** — Better error messages with more context
- **tween_await() debugging** — Use `await` breakpoints in C# debugger for animation sequences

## Debug Utility Functions

```gdscript
class_name DebugUtils extends Node

static func draw_rect_debug(rect: Rect2, color: Color, lifetime: float = 0.0):
    # Draw debug rectangle (use with CanvasItem.draw_rect)
    pass

static func log_tree(node: Node, indent: int = 0):
    # Print scene tree for debugging
    var prefix = "  ".repeat(indent)
    print(prefix + node.name, " (", node.get_class(), ")")
    for child in node.get_children():
        log_tree(child, indent + 1)

static func check_node_ready(node: Node):
    # Verify node is ready before accessing children
    if not node.is_inside_tree():
        push_error("Node not in tree: ", node.name)
    return node.is_inside_tree()
```

## MCP Bridge Tools (Optional — Live Editor Integration)

When the MCP bridge is running (Phase 2), these tools provide live debugging capabilities:

- **`debugger_output`** — Read real-time debugger output from the running scene
- **`output_log`** — Read Godot's output log with level filtering (error/warning/info)
- **`scene_run` / `scene_stop`** — Start and stop scenes for testing fixes
- **`pause_resume`** — Pause execution to inspect state at breakpoints
- **`script_validate`** — Validate scripts without leaving the agent workflow
- **`scene_tree`** — Inspect runtime scene hierarchy for missing nodes

> **Note:** MCP tools require the Godot editor to be running with the MCP plugin enabled. Skills work independently without the bridge.

## References

- [Debugging Guide](references/debugging-workflow.md)
- [Profiler Deep Dive](references/profiler-guide.md)
- [Network Debugging](references/network-debug.md)
