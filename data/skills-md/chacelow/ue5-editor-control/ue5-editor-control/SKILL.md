---
name: ue5-editor-control
description: Control Unreal Engine 5 editor via HTTP commands. Spawn/delete/transform actors, manage blueprints, materials, animation blueprints, and any UObject property via reflection. Use when the user asks to create, modify, or query anything in UE5 editor, or mentions UE5, Unreal, actors, blueprints, levels, materials, animation, input, or characters.
license: MIT
compatibility: Requires UE5 (5.4+) editor running with UE5AIAssistant plugin enabled. macOS/Windows/Linux. Needs curl.
metadata:
  author: caishilong
  version: "1.0.0"
  ue5-version: "5.4+"
  commands: "65"
---

# UE5 Editor Control

HTTP API for the UE5 editor. Plugin `UE5AIAssistant` runs on `localhost:58080`.

## Auto-Setup Flow (MUST follow on first use)

Every time you need to use this skill, **start here**:

### Step 1: Check if plugin is already running

```bash
curl -s --max-time 3 http://localhost:58080/api/ping
```

- If response contains `"success": true` → **Skip to Quick Start** below
- If connection refused / timeout → Plugin not running, continue to Step 2

### Step 2: Find user's UE5 project

Ask the user: **"你的 UE5 项目路径是什么？"**

Or auto-detect (look for `.uproject` files):

```bash
# macOS common locations
find ~/Documents ~/Desktop ~/Projects ~/codeprojects -maxdepth 3 -name "*.uproject" 2>/dev/null
```

Save the project path for later use.

### Step 3: Check if plugin is installed in the project

```bash
# Check if plugin exists in the UE5 project
test -f "<UE5_PROJECT_PATH>/Plugins/UE5AIAssistant/UE5AIAssistant.uplugin" && echo "INSTALLED" || echo "NOT INSTALLED"
```

- If `INSTALLED` → Tell user: **"插件已安装，请打开 UE5 编辑器然后告诉我"**
- If `NOT INSTALLED` → Continue to Step 4

### Step 4: Install the plugin

**Option A — Download prebuilt binary (recommended, no C++ required):**

```bash
bash scripts/install.sh "<UE5_PROJECT_PATH>"
```

If this fails (no releases published yet), fall back to Option B.

**Option B — Copy source code (requires UE5 C++ compilation):**

The skill's GitHub repo contains the C++ source. Clone and copy:

```bash
# Clone the repo (if not already available)
git clone https://github.com/1103837067/ue5-editor-control.git /tmp/ue5-editor-control

# Copy plugin source to UE5 project
mkdir -p "<UE5_PROJECT_PATH>/Plugins/UE5AIAssistant"
cp -r /tmp/ue5-editor-control/Source "<UE5_PROJECT_PATH>/Plugins/UE5AIAssistant/"
cp /tmp/ue5-editor-control/UE5AIAssistant.uplugin "<UE5_PROJECT_PATH>/Plugins/UE5AIAssistant/"
```

Then tell user: **"插件已复制到项目中。请打开 UE5 编辑器，它会自动编译插件。打开后告诉我。"**

### Step 5: Verify connection

```bash
curl -s --max-time 3 http://localhost:58080/api/ping
```

If still failing, tell user to check:
- UE5 editor is open with the correct project
- Check Output Log for "UE5AIAssistant: HTTP server started on port 58080"
- Plugin is enabled: Edit → Plugins → search "UE5AIAssistant"

## Prerequisites Summary

| Requirement | Detail |
|-------------|--------|
| UE5 | 5.4+ installed and project created |
| OS | macOS / Windows / Linux |
| curl | Pre-installed on macOS/Linux; Git Bash on Windows |
| UE5 Editor | Must be running with plugin enabled |
| C++ (Option B only) | Only if no prebuilt binary available for your platform |

## Quick Start

```bash
# Execute command (preferred for complex JSON)
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"command":"get_actors_in_level","args":{}}' \
  http://localhost:58080/api/execute

# Simple commands via helper
bash scripts/ue5cmd.sh exec get_actors_in_level '{}'
```

Response: `{ "success": true|false, "data": {...}|null, "error": "..."|null }`

## Common Mistakes — Do NOT

- Do NOT add nodes one-by-one — **always use `batch_execute`**
- Do NOT guess C++ function names — use `list_functions` first
- Do NOT hardcode pin names — read them from response `pins` array
- Do NOT skip `compile_blueprint` after editing
- Do NOT use `ue5cmd.sh` for complex JSON — use `curl` directly

## Task Router — Read the Right Module

Based on the user's task, read **only** the relevant module file for detailed commands, parameters, and workflows:

| User wants to... | Read this file |
|---|---|
| Work with **actors** (spawn, delete, transform, properties) | [references/actor.md](references/actor.md) |
| Build **blueprint** structure & logic (create BP, variables, functions, nodes, batch_execute) | [references/blueprint.md](references/blueprint.md) |
| Create **materials** (expressions, connections, apply) | [references/material.md](references/material.md) |
| Build **animation blueprints** (state machines, states, transitions) | [references/animation.md](references/animation.md) |
| Access **any property** via reflection, manage assets (create/read/write) | [references/property.md](references/property.md) |
| Set up **Enhanced Input**, configure character movement, build end-to-end characters | [references/input-character.md](references/input-character.md) |

**Rules:**
1. Read only the module(s) needed for the current task — do NOT read all files
2. If unsure which module, check the table above or read the user's intent
3. Multiple tasks may require multiple modules (e.g., character = blueprint + input-character)

## 65 Commands Overview (for quick orientation only)

| Category | Commands | Count |
|---|---|---|
| Actor | `get_actors_in_level`, `find_actors_by_name`, `get_selected_actors`, `spawn_actor`, `delete_actor`, `set_actor_transform`, `get_actor_properties`, `set_actor_property`, `attach_actor`, `detach_actor` | 10 |
| Blueprint Structure | `create_blueprint`, `compile_blueprint`, `read_blueprint_content`, `create_variable`, `add_component_to_blueprint`, `create_function`, `add_function_parameter`, `create_event_dispatcher`, `create_blueprint_interface`, `implement_interface`, `add_widget_child` | 11 |
| Blueprint Discovery | `list_node_types`, `list_blueprint_classes`, `list_functions` | 3 |
| Blueprint Nodes | `add_node`, `connect_nodes`, `remove_node`, `get_node_pins`, `set_pin_default`, `batch_execute`, `add_pin`, `auto_layout_graph` | 8 |
| Material | `create_material`, `add_material_expression`, `connect_material_expressions`, `apply_material_to_actor`, `get_available_materials` | 5 |
| Asset | `search_assets`, `get_assets_by_class`, `get_asset_details` | 3 |
| Editor | `focus_viewport`, `get_current_level_info`, `save_all`, `get_project_settings`, `set_project_setting`, `get_world_settings`, `set_world_setting` | 7 |
| Animation | `create_anim_blueprint`, `get_anim_blueprint_info`, `add_anim_state_machine`, `add_anim_state`, `add_anim_transition`, `set_anim_state_animation`, `compile_anim_blueprint` | 7 |
| **Generic Reflection** | `list_components`, `list_properties`, `get_component_property`, `set_component_property`, `create_asset`, `get_asset_property`, `set_asset_property`, **`call_function`**, **`get_object`**, **`modify_array_property`**, **`execute_python`** | **11** |

## Error Quick Reference

| Error pattern | Fix |
|---|---|
| `"not found"` | Use discovery commands (`find_actors_by_name`, `search_assets`, `list_functions`, `list_node_types`, `list_properties`) |
| `"Pin 'xxx' not found"` | Error response lists all available pins — use the correct name |
| `compile_blueprint` diagnostics | Read [references/blueprint.md](references/blueprint.md) error handling section |
