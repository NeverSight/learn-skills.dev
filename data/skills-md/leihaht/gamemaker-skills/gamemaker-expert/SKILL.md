---
name: gamemaker-expert
description: Comprehensive GameMaker Studio 2 and GML expertise covering beginner to advanced topics. Provides guidance on object creation, GML syntax, event systems, data structures, file I/O, shaders, networking, platform-specific features, performance optimization, and debugging. Automatically invoked when working with .gml files, .yy files, .yyp projects, or GameMaker-related tasks. References official manual (manual.gamemaker.io) for authoritative documentation.
---

# GameMaker Expert

## Overview

This skill provides comprehensive GameMaker Studio 2 and GML (GameMaker Language) expertise for all GameMaker projects. It covers everything from basic object creation to advanced topics like shader programming, networking, and platform-specific development.

**When to use this skill:**
- Working with `.gml` files (GML scripts and events)
- Creating or modifying `.yy` files (object definitions, sprite definitions, etc.)
- Editing `.yyp` project files
- Creating GameMaker objects, scripts, or assets
- Debugging GameMaker compile errors or runtime issues
- Implementing GameMaker features (drawing, collision, networking, etc.)
- Optimizing GameMaker performance
- Any GameMaker Studio 2 development task

## Official GameMaker Manual

**PRIMARY REFERENCE**: Always consult the official GameMaker Manual for comprehensive, up-to-date documentation:
https://manual.gamemaker.io/monthly/en/

### Key Manual Sections

- **GML Overview**: https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Overview.htm
  - Variables, data types, operators, keywords, control flow
- **GML Reference**: https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference.htm
  - All built-in functions organized by category (drawing, math, strings, instances, etc.)
- **Objects & Events**: https://manual.gamemaker.io/monthly/en/The_Asset_Editors/Objects.htm
  - Object properties, event system, parent-child relationships
- **Sprites**: https://manual.gamemaker.io/monthly/en/The_Asset_Editors/Sprites.htm
  - Sprite editor, collision masks, animations
- **Data Structures**: https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference/Data_Structures.htm
  - ds_list, ds_map, ds_grid, ds_priority, ds_queue, ds_stack
- **File Handling**: https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference/File_Handling.htm
  - File I/O, JSON, buffers, directories

**When to use the official manual:**
- Looking up function signatures and parameters
- Understanding platform-specific behavior
- Checking latest syntax changes for your IDE version
- Detailed explanations of GameMaker features

### Additional References

**For advanced architectural guidance:**

- **Architecture Patterns**: [references/ARCHITECTURE_PATTERNS.md](references/ARCHITECTURE_PATTERNS.md)
  - GameMaker-specific patterns (Service Locator, Command Pattern, Event-Driven Flow)
  - SOLID principles adapted for GML
  - Encapsulation patterns with manager constructors
  - Performance patterns and anti-patterns
- **Manager Constructor Guide**: [references/MANAGER_CONSTRUCTOR_GUIDE.md](references/MANAGER_CONSTRUCTOR_GUIDE.md)
  - Step-by-step guide for creating manager constructors
  - Public API design patterns
  - Reference exposure pattern for backwards compatibility
  - Cleanup responsibilities and testing strategies
- **Built-in Variables**: [references/BUILT_IN_VARIABLES.md](references/BUILT_IN_VARIABLES.md)
  - Complete list of GameMaker reserved variables
  - Position, sprites, physics, paths, timelines categories
  - Deprecated globals (`health`, `score`, `lives`)
  - Safe alternatives and validation checklist
- **GML Reference**: [references/GML_REFERENCE.md](references/GML_REFERENCE.md)
  - Language syntax, operators, data types
- **Common Pitfalls**: [references/COMMON_PITFALLS.md](references/COMMON_PITFALLS.md)
  - Frequent mistakes and solutions
- **Quick Reference**: [references/QUICK_REFERENCE.md](references/QUICK_REFERENCE.md)
  - Cheat sheet for common patterns

**When to use these references:**
- Designing manager constructors for game-wide state
- Avoiding conflicts with GameMaker built-in variables
- Implementing encapsulation patterns in GML
- Understanding `__` prefix convention for pseudo-private members
- Learning SOLID principles in GameMaker context
- Finding architectural patterns for maintainable code

## Core GameMaker Workflows

### Object Creation Workflow (CRITICAL)

Creating GameMaker objects requires completing ALL four steps. Missing any step will cause the object to not appear in the IDE or fail to compile.

#### Step 1: Create Object Directory

```bash
objects/objYourObjectName/
```

**Naming Convention:**
- Start with `obj` prefix
- Use PascalCase (e.g., `objPlayer`, `objEnemyMelee`, `objInventoryUI`)
- Descriptive name indicating purpose

#### Step 2: Create Event Files

Create `.gml` files for each event your object needs:

**Common Events:**

| Event File | Event Type | When to Use |
|------------|------------|-------------|
| `Create_0.gml` | Create Event | Initialize variables (ALWAYS include) |
| `Step_0.gml` | Step Event | Update logic every frame |
| `Draw_0.gml` | Draw Event | Render in-world graphics |
| `Draw_64.gml` | Draw GUI Event | Render UI overlays |
| `Destroy_0.gml` | Destroy Event | Cleanup when destroyed |
| `Collision_objX.gml` | Collision Event | Handle collisions |

**Event Naming Rules:**
- Create: `Create_0.gml`
- Step: `Step_0.gml`
- Draw: `Draw_0.gml`
- Draw GUI: `Draw_64.gml` (NOT `Draw_GUI_0.gml`!)
- Collision: `Collision_objTargetName.gml`

**Example Create_0.gml:**
```gml
/// objPlayer Create Event
// Initialize player variables

// Movement
move_speed = 4;
direction = 0;

// Stats
health = 100;
max_health = 100;

// State
is_moving = false;

show_debug_message("objPlayer created");
```

#### Step 3: Create .yy File (REQUIRED)

**File**: `objects/objYourObjectName/objYourObjectName.yy`

**Template:**
```json
{
  "$GMObject":"",
  "%Name":"objYourObjectName",
  "eventList":[
    {"$GMEvent":"v1","%Name":"","collisionObjectId":null,"eventNum":0,"eventType":0,"isDnD":false,"name":"","resourceType":"GMEvent","resourceVersion":"2.0",},
    {"$GMEvent":"v1","%Name":"","collisionObjectId":null,"eventNum":64,"eventType":8,"isDnD":false,"name":"","resourceType":"GMEvent","resourceVersion":"2.0",},
    {"$GMEvent":"v1","%Name":"","collisionObjectId":null,"eventNum":0,"eventType":3,"isDnD":false,"name":"","resourceType":"GMEvent","resourceVersion":"2.0",},
  ],
  "managed":true,
  "name":"objYourObjectName",
  "overriddenProperties":[],
  "parent":{
    "name":"Objects",
    "path":"folders/Objects.yy",
  },
  "parentObjectId":null,
  "persistent":false,
  "physicsAngularDamping":0.1,
  "physicsDensity":0.5,
  "physicsFriction":0.2,
  "physicsGroup":1,
  "physicsKinematic":false,
  "physicsLinearDamping":0.1,
  "physicsObject":false,
  "physicsRestitution":0.1,
  "physicsSensor":false,
  "physicsShape":1,
  "physicsShapePoints":[],
  "physicsStartAwake":true,
  "properties":[],
  "resourceType":"GMObject",
  "resourceVersion":"2.0",
  "solid":false,
  "spriteId":null,
  "spriteMaskId":null,
  "visible":true,
}
```

**Event Type Numbers:**

| Event | eventType | eventNum |
|-------|-----------|----------|
| Create | 0 | 0 |
| Step | 3 | 0 |
| Draw | 8 | 0 |
| Draw GUI | 8 | 64 |
| Destroy | 1 | 0 |

**Important Fields:**
- `%Name` and `name`: Must match object name exactly
- `eventList`: Include entry for each .gml file created
- `parentObjectId`: Set to parent object resource path if using inheritance (e.g., `{"name":"objCreature","path":"objects/objCreature/objCreature.yy"}`)
- `persistent`: Set to `true` if object should persist across rooms
- `visible`: Set to `false` for controller objects with no sprite

#### Step 4: Register in Project File (REQUIRED)

**File**: `YourProject.yyp`

**Location**: Find the `"resources":[` array

**Add Entry (alphabetically sorted):**
```json
{"id":{"name":"objYourObjectName","path":"objects/objYourObjectName/objYourObjectName.yy",},},
```

**Example:**
```json
"resources":[
  {"id":{"name":"objInventoryUI","path":"objects/objInventoryUI/objInventoryUI.yy",},},
  {"id":{"name":"objPlayer","path":"objects/objPlayer/objPlayer.yy",},},
  {"id":{"name":"objYourObjectName","path":"objects/objYourObjectName/objYourObjectName.yy",},},
]
```

**CRITICAL**: Missing this step will cause compile errors like "object not found".

### GML Language Essentials

#### Variable Scope

```gml
// Local variable (function/script scope only)
var _local_var = 100;

// Instance variable (attached to object instance)
instance_var = 50;

// Global variable (accessible everywhere)
global.game_state = "playing";
```

**Best Practice**: Start local variable names with underscore `_` for clarity.

#### Data Types

- **Real**: Numbers `var _x = 100;` `var _pi = 3.14159;`
- **String**: Text `var _name = "Player";`
- **Boolean**: True/False `var _is_alive = true;`
- **Array**: `var _items = [1, 2, 3];` `var _nested = [[1,2], [3,4]];`
- **Struct**: `var _player = { x: 0, y: 0, health: 100 };`
- **Undefined**: `undefined` (check with `is_undefined()`)
- **Pointer/ID**: References to instances, data structures, assets

#### Operators

**Arithmetic**: `+ - * / div mod`
**Comparison**: `== != > < >= <=`
**Logical**: `&& || ! ^^ (and, or, not, xor)`
**Bitwise**: `& | ^ << >> ~`
**Ternary**: `condition ? true_value : false_value`

**CRITICAL - Ternary Operator Chaining:**

Chained ternary operators MUST wrap nested conditions in double parentheses:

```gml
// ✅ CORRECT
var _result = condition_a ? "foo" : ((condition_b ? "bar" : "baz"));

// ❌ WRONG (will cause compile error in some versions)
var _result = condition_a ? "foo" : condition_b ? "bar" : "baz";
```

**Reference**: https://manual.gamemaker.io/beta/en/GameMaker_Language/GML_Overview/Expressions_And_Operators.htm

#### Control Flow

```gml
// If statement
if (condition) {
    // code
} else if (other_condition) {
    // code
} else {
    // code
}

// Switch statement
switch (value) {
    case 1:
        // code
        break;
    case 2:
    case 3:
        // code for 2 or 3
        break;
    default:
        // code
        break;
}

// For loop
for (var _i = 0; _i < 10; _i++) {
    show_debug_message(_i);
}

// While loop
while (condition) {
    // code
}

// Repeat loop
repeat (10) {
    // code
}

// With loop (iterate instances)
with (objEnemy) {
    health -= 10;
}
```

### Data Structures & Memory Management

#### Structs (Lightweight - Recommended)

```gml
// Create struct (no manual cleanup needed!)
var _player = {
    name: "Hero",
    health: 100,
    max_health: 100,
    level: 1
};

// Access properties
show_debug_message(_player.name); // "Hero"
_player.health -= 10;

// Check if property exists
if (variable_struct_exists(_player, "mana")) {
    // property exists
}

// Dynamic property access
var _prop_name = "health";
var _value = _player[$ _prop_name]; // Same as _player.health
```

**When to use**: Lightweight data containers, configuration data, simple key-value pairs.
**Benefits**: No manual cleanup required, garbage collected automatically.

#### ds_list (Dynamic Array)

```gml
// Create
var _list = ds_list_create();

// Add items
ds_list_add(_list, "apple", "banana", "cherry");
ds_list_insert(_list, 1, "orange"); // Insert at index

// Access
var _item = _list[| 0]; // "apple"
var _size = ds_list_size(_list);

// Iterate
for (var _i = 0; _i < ds_list_size(_list); _i++) {
    show_debug_message(_list[| _i]);
}

// CRITICAL: Always destroy when done!
ds_list_destroy(_list);
```

**When to use**: Large collections, need specific list operations, performance-critical code.
**CRITICAL**: Must manually destroy with `ds_list_destroy()` or memory leak will occur!

#### ds_map (Key-Value Pairs)

```gml
// Create
var _map = ds_map_create();

// Add items
_map[? "name"] = "Player";
_map[? "health"] = 100;

// Access
var _hp = _map[? "health"]; // 100

// Check if key exists
if (ds_map_exists(_map, "mana")) {
    // key exists
}

// Iterate
var _key = ds_map_find_first(_map);
while (!is_undefined(_key)) {
    show_debug_message(_key + ": " + string(_map[? _key]));
    _key = ds_map_find_next(_map, _key);
}

// CRITICAL: Always destroy when done!
ds_map_destroy(_map);
```

**When to use**: Legacy code, need specific map operations, integration with existing ds_map code.
**CRITICAL**: Must manually destroy with `ds_map_destroy()` or memory leak will occur!

**Recommendation**: Use structs instead of ds_map when possible - they're simpler and don't require manual cleanup.

#### Memory Leak Prevention

**Data structures that MUST be destroyed:**
- `ds_list_destroy(_list)`
- `ds_map_destroy(_map)`
- `ds_grid_destroy(_grid)`
- `ds_priority_destroy(_priority)`
- `ds_queue_destroy(_queue)`
- `ds_stack_destroy(_stack)`
- `surface_free(_surface)`
- `buffer_delete(_buffer)`

**Pattern for cleanup in Destroy event:**
```gml
/// objPlayer Destroy Event
// Clean up data structures

if (ds_exists(inventory_list, ds_type_list)) {
    ds_list_destroy(inventory_list);
}

if (surface_exists(shadow_surface)) {
    surface_free(shadow_surface);
}
```

### File System & Persistence

#### datafiles/ Folder (Included Files)

**CRITICAL LIMITATION**: Some GameMaker versions only support root-level files in `datafiles/` - NO subdirectories!

```
✅ CORRECT:
datafiles/config.json
datafiles/items.json
datafiles/level_data.json

❌ WRONG (may not work in all versions):
datafiles/configs/game_config.json
datafiles/data/items/weapons.json
```

**Registration Required**: Every file in `datafiles/` must be registered in the `.yyp` project file:

```json
{"$GMIncludedFile":"","%Name":"config.json","CopyToMask":-1,"filePath":"datafiles","name":"config.json","resourceType":"GMIncludedFile","resourceVersion":"2.0",},
```

#### JSON Files

```gml
// Load JSON from datafiles/
function load_json_file(_filename) {
    if (!file_exists(_filename)) {
        show_debug_message("ERROR: File not found: " + _filename);
        return noone;
    }

    var _file = file_text_open_read(_filename);
    var _json_string = "";
    while (!file_text_eof(_file)) {
        _json_string += file_text_read_string(_file);
        file_text_readln(_file);
    }
    file_text_close(_file);

    return json_parse(_json_string);
}

// Save JSON to working directory
function save_json_file(_filename, _data) {
    var _json_string = json_stringify(_data);
    var _file = file_text_open_write(_filename);
    file_text_write_string(_file, _json_string);
    file_text_close(_file);
}
```

#### Save File Locations

```gml
// Working directory (platform-dependent save location)
var _save_path = working_directory + "savegame.json";

// Game save ID (unique folder for your game)
// On Windows: %LOCALAPPDATA%/[game_save_id]/
var _save_id = game_save_id;
```

### Event System & Execution Order

#### Event Execution Order (Per Frame)

1. **Begin Step** - Before main logic
2. **Alarm Events** - Countdown timers
3. **Keyboard/Mouse Events** - Input detection
4. **Step** - Main update logic
5. **Collision Events** - After movement
6. **End Step** - After all logic
7. **Draw** - Render in-world graphics
8. **Draw GUI** - Render UI overlays
9. **Draw End** - Post-processing

#### Persistent Objects

Set `persistent: true` in `.yy` file to survive room transitions.

**CRITICAL**: When using persistent objects with event handlers, clear handlers when re-entering rooms to avoid duplicate registrations!

```gml
// rmGameplay Room Creation Code
// Clear handlers to prevent duplicates
global.input_controller.clear_all_handlers();

// Register handlers fresh
global.input_controller.register_handler("ACTION", function(_cmd) {
    // handle action
});
```

### Drawing & Graphics

#### Basic Drawing

```gml
// Draw sprite
draw_sprite(spr_player, image_index, x, y);
draw_sprite_ext(spr_player, image_index, x, y, scale_x, scale_y, rotation, color, alpha);

// Draw text
draw_text(x, y, "Hello World");
draw_set_font(fnt_arial);
draw_set_color(c_white);
draw_set_halign(fa_center);
draw_set_valign(fa_middle);

// Draw shapes
draw_rectangle(x1, y1, x2, y2, outline);
draw_circle(x, y, radius, outline);
draw_line(x1, y1, x2, y2);
```

#### Surfaces (Render Targets)

```gml
// Create surface
if (!surface_exists(shadow_surface)) {
    shadow_surface = surface_create(room_width, room_height);
}

// Draw to surface
surface_set_target(shadow_surface);
draw_clear_alpha(c_black, 0);
// ... draw operations ...
surface_reset_target();

// Draw surface to screen
draw_surface(shadow_surface, 0, 0);

// CRITICAL: Free surface when done
if (surface_exists(shadow_surface)) {
    surface_free(shadow_surface);
}
```

### Performance Optimization

#### Draw Call Optimization
- Minimize draw calls by batching sprites onto texture pages
- Use layers for static content (backgrounds, tiles)
- Cache expensive calculations (don't recalculate in Draw event)
- Avoid creating/destroying instances in Draw events

#### Collision Optimization
- Use broad-phase distance checks before precise collision
- Set appropriate collision masks (precise vs bounding box)
- Use collision layers and groups
- Consider using `instance_position()` instead of `place_meeting()` when you need the instance

#### Memory Management
- Always destroy data structures when done
- Free surfaces when no longer needed
- Delete buffers after use
- Clean up in Destroy events

## Common Pitfalls & Solutions

**See [COMMON_PITFALLS.md](references/COMMON_PITFALLS.md) for comprehensive troubleshooting guide.**

### Quick Reference

**Object Creation Issues:**
- **Missing .yy file** → Object doesn't appear in IDE → Create .yy file using template above
- **Missing .yyp registration** → Compile error "object not found" → Add entry to .yyp resources array
- **Wrong event name** → Event doesn't trigger → Use exact names (Draw_64.gml, NOT Draw_GUI_0.gml)

**Memory Issues:**
- **Data structure leaks** → Memory usage grows → Always call ds_destroy functions
- **Surface leaks** → Memory usage grows → Always call surface_free()
- **Forgotten Destroy event** → Resources not cleaned up → Add Destroy event with cleanup code

**File System Issues:**
- **datafiles/ subdirectory** → File not found error → Move files to datafiles/ root level
- **Missing .yyp registration** → Included file not found → Register file in .yyp

**GML Syntax Issues:**
- **Ternary chaining** → Compile error → Wrap nested conditions in double parentheses
- **Variable scope** → Undefined variable → Check local vs instance vs global scope
- **Array bounds** → Index out of range → Check array size before accessing

## Advanced Topics

For in-depth coverage of advanced features, see:

- **[GML_REFERENCE.md](references/GML_REFERENCE.md)** - Complete GML function reference organized by category
- **[QUICK_REFERENCE.md](references/QUICK_REFERENCE.md)** - Tables, constants, and quick lookups
- **[ADVANCED_TOPICS.md](references/ADVANCED_TOPICS.md)** - Shaders, networking, platform-specific development

### Shader Programming (GLSL ES)

**When to use shaders:**
- Advanced visual effects (lighting, blur, outline, color grading)
- Per-pixel operations (custom rendering effects)
- Performance optimization (GPU-based calculations)

**Basic shader workflow:**
1. Create shader asset in IDE
2. Write vertex shader (.vsh) and fragment shader (.fsh)
3. Set shader: `shader_set(shd_outline);`
4. Pass uniforms: `shader_set_uniform_f(u_time, current_time);`
5. Draw sprites/surfaces
6. Reset shader: `shader_reset();`

**See ADVANCED_TOPICS.md for GLSL ES syntax, examples, and common shader patterns.**

### Networking & Multiplayer

**When to use networking:**
- Multiplayer games (client-server, peer-to-peer)
- Online leaderboards
- HTTP API integration
- Cloud save systems

**Async HTTP example:**
```gml
// Send GET request
var _request_id = http_get("https://api.example.com/data");

// In Async HTTP event
var _id = async_load[? "id"];
if (_id == _request_id) {
    var _status = async_load[? "status"];
    if (_status == 0) {
        var _result = async_load[? "result"];
        var _data = json_parse(_result);
        // Process data
    }
}
```

**See ADVANCED_TOPICS.md for network sockets, buffers, multiplayer architecture, and synchronization patterns.**

### Platform-Specific Development

**Mobile (iOS/Android):**
- Touch input: `device_mouse_x_to_gui()`, `device_mouse_y_to_gui()`
- Virtual buttons: `virtual_key_add()`
- Sensors: `device_get_tilt_x()`, `device_get_tilt_y()`

**Console (PlayStation, Xbox, Nintendo Switch):**
- Gamepad support: `gamepad_button_check()`, `gamepad_axis_value()`
- Platform detection: `os_type`, `os_get_config()`

**HTML5:**
- Browser integration: `clickable_add()`, `clickable_set_style()`
- JavaScript execution: `js_runner_eval()`

**Desktop (Windows, macOS, Linux):**
- File dialogs: `get_open_filename()`, `get_save_filename()`
- Window control: `window_set_fullscreen()`, `window_set_size()`

**See ADVANCED_TOPICS.md for detailed platform-specific development guides.**

## Resources

This skill includes comprehensive reference documentation:

### references/

**[GML_REFERENCE.md](references/GML_REFERENCE.md)** (~1500 lines)
- Complete GML function reference organized by category
- Drawing, math, strings, instances, rooms, data structures, files, networking, shaders, surfaces, particles, audio
- Code patterns for common tasks (inventory, state machines, dialogue, save/load, camera systems)
- Struct vs Object decision guidance
- Constructor patterns and method variables

**[ARCHITECTURE_PATTERNS.md](references/ARCHITECTURE_PATTERNS.md)** (~500 lines)
- GameMaker-specific architectural patterns (Service Locator, Command Pattern, Event-Driven Flow, Procedural Logic, Data-Driven Design)
- Why NOT MVC/MVP for game engines (event-driven vs request/response architecture)
- SOLID principles in GML context (SRP, OCP, LSP, ISP, DIP with code examples)
- Design principles (DRY, KISS, YAGNI)
- Performance patterns (hot path optimization, struct vs ds_map, lookup maps)
- Anti-patterns to avoid (global abuse, deep hierarchies, function redefinition)

**[COMMON_PITFALLS.md](references/COMMON_PITFALLS.md)** (~800 lines)
- Object creation issues (missing .yy, missing .yyp registration, wrong event names)
- File system issues (datafiles/ subdirectories, .yyp registration, paths)
- GML syntax traps (ternary operators, variable scope, array bounds, undefined access)
- Memory management (ds_* leaks, surface leaks, buffer leaks, cleanup patterns)
- Performance issues (draw optimization, collision optimization, instance management)
- Networking issues (async events, buffer types, timeouts, platform differences)
- Shader issues (GLSL ES compatibility, uniform naming, texture sampling)

**[QUICK_REFERENCE.md](references/QUICK_REFERENCE.md)** (~600 lines)
- Event type/number complete table with execution order
- Keyboard constants (vk_* constants, ord() usage, key press vs check)
- Mouse constants (mb_* constants, mouse event types, device_mouse_* functions)
- Common GML patterns (distance checks, direction calculation, collision checks, random ranges)
- Color functions (constants, make_color_*, color_get_*, merge_color)
- IDE version reference (common versions, features, compatibility notes)

**[ADVANCED_TOPICS.md](references/ADVANCED_TOPICS.md)** (~1000 lines)
- Shader Programming (GLSL ES syntax, vertex/fragment shader examples, uniforms, multi-pass techniques, debugging)
- Networking Patterns (client-server architecture, lobby systems, packet structure, latency compensation, buffers)
- Platform-Specific Development (mobile touch/sensors, console gamepad/achievements, HTML5 browser API, desktop OS interactions)
- Advanced Graphics (surfaces, lighting systems, normal maps, particles, tilemaps, cameras)
- Performance Profiling (debug overlay, bottleneck identification, memory profiling, draw call reduction, code profiling)

---

**Remember**: This skill provides guidance and reference. Always consult the official GameMaker Manual for the most up-to-date and comprehensive documentation!
