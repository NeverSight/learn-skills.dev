---
name: dayz-enfusion-script
description: Write, extend, and debug DayZ server/client mods in Enforce Script (the Enfusion engine C-like scripting language).
---

# DayZ Enforce Script Skill

Always consult [community.bistudio.com DayZ Modding](https://community.bistudio.com/wiki/DayZ:Modding) and the [Enforce Script Language Reference](https://community.bistudio.com/wiki/Enforce_Script_Language) for authoritative API docs.

## Overview

Enforce Script is a statically-typed, C-like scripting language embedded in the Bohemia Interactive Enfusion engine. It drives all gameplay logic in DayZ: items, players, AI, missions, GUI, economy, and RPC networking. Mods are distributed as `.pbo` archives compiled from `.c` script files layered on top of vanilla scripts.

## When to Use This Skill

Trigger this skill when the user asks to:

- Create or extend DayZ mod classes (items, players, weapons, missions, GUI menus)
- Implement server-side logic (actions, spawning, persistence, economy)
- Set up RPC communication between server and clients
- Sync variables from server to client via NetSync
- Create `.layout` XML files for in-game GUI panels and HUDs
- Integrate with Community Framework (CF), DABS, or vanilla plugin systems
- Debug Enforce Script compile errors or runtime issues

## Quick Start

Minimal mod structure:

```
MyMod/
  config.cpp          <- PBO manifest + CfgPatches
  Scripts/
    4_World/
      MyMod_Item.c    <- your class
```

**config.cpp**

```cpp
class CfgPatches
{
    class MyMod
    {
        units[]  = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] = { "DZ_Data" };
    };
};
```

**Minimal modded class**

```c
// Scripts/4_World/MyMod_Item.c
modded class Apple
{
    override void OnConsume(PlayerBase player)
    {
        super.OnConsume(player);  // ALWAYS call super
        Print("[MyMod] Apple consumed by: " + player.GetIdentity().GetName());
    }
}
```

## Critical Language Quirks

- **No ternary operator** — use `if/else` instead of `x ? a : b`
- **`auto` != type inference** — `auto` means `autoptr` (reference-counted ownership alias for `ref`)
- **No lambdas** — use `ScriptCaller` for single callbacks, `ScriptInvoker` for multicast events
- **Primitives are never null** — `int`, `float`, `bool`, `string` default to `0 / 0.0 / false / ""`; only class instances can be null
- **`modded class`** — the ONLY extension mechanism; produces one merged class. Always call `super.*` in overrides
- **`super.*` is mandatory** — skipping it silently breaks every other mod in the chain
- **Write/read order in persistence** — `OnStoreSave` and `OnStoreLoad` must write/read fields in identical order; mismatch destroys saves
- **No function overloading** — methods must have unique names; use optional parameters instead
- **String format** — `string.Format("Value: %1", val)` with 1-indexed `%N` placeholders (not `%s`/`%d`)

## Mod Structure and Script Layers

Scripts load in layer order. Classes defined in lower layers are available to higher ones.

| Folder               | Layer | Purpose                                   |
| -------------------- | ----- | ----------------------------------------- |
| `Scripts/1_Core/`    | 1     | Engine primitives, proto definitions      |
| `Scripts/2_GameLib/` | 2     | Base game library, input, menus           |
| `Scripts/3_Game/`    | 3     | Core gameplay (items, players, RPC enums) |
| `Scripts/4_World/`   | 4     | World entities — most mod code lives here |
| `Scripts/5_Mission/` | 5     | Mission logic (server init, spawn tables) |

A `modded class PlayerBase` must live in `Scripts/4_World/`; a `modded class MissionServer` in `Scripts/5_Mission/`.

## Technical Terms

- **NetSync** — engine-managed variable replication from server to all clients via `RegisterNetSyncVariable*` + `SetSynchDirty()`
- **RPC** — Remote Procedure Call; integer-keyed messages sent between server and clients, received in `OnRPC()` overrides
- **CF / Community Framework** — most-used modding library; adds module system, event bus, `ModStorage` persistence, and attribute-based actions
- **DABS** — attribute-based action framework built on CF; declarative action definitions
- **PluginBase** — vanilla service-locator pattern for decoupled gameplay subsystems
- **ScriptInvoker** — multicast delegate (add/remove listeners, fire all)

## Resources

Use the references for API lookups. Check patterns when implementing a common mechanic. Examples show complete working files.

`references/player_api.md` and `references/game_api.md` are the most frequently needed starting points.

### references/

Core API documentation split by topic:

- `types_collections.md` - Primitive types, string methods, array/map/set API, vector math, Math class
- `player_api.md` - PlayerBase stats, vitals, agents, modifiers, inventory, NetSync, RPC helpers
- `item_api.md` - ItemBase quantity/health/flags, action registration, spawning, config.cpp properties
- `game_api.md` - GetGame(), GetWorld(), GetMission(), CreateObject, CallLater, logging
- `erpc_defines.md` - Vanilla eRPCs/eAgents/eModifiers tables, custom ID range convention
- `file_paths.md` - $profile/$saves path tokens, FileExist, MakeDirectory, JsonFileLoader, FileMode
- `gui_layout.md` - Layout file format (WidgetClassNameClass syntax, RGBA colors, coords, all widget types, colums property, ItemPreviewWidget/PlayerPreviewWidget API)

### integrations/

Guides for integrating with external frameworks and vanilla systems:

- `community_framework.md` - CF module system, ModStorage persistence, event bus, inter-mod events
- `dabs_framework.md` - Attribute-based action system, CF_ModAttribute, MVC layout, settings API
- `vanilla_plugins.md` - PluginBase lifecycle, GetPlugin(), service-locator mod isolation pattern
- `central_economy.md` - CE XML format, runtime CE with SpawnObject/DeleteObject, cfgeconomycore.xml
- `input_bindings.md` - inputs.xml, UAInput API, GetUApi(), context guards, client-only input rules

### patterns/ (optional)

Common implementation patterns for recurring mechanics:

- `netsync.md` - RegisterNetSyncVariable\*, SetSynchDirty, OnVariablesSynchronized, bitfield packing
- `persistence.md` - OnStoreSave/OnStoreLoad, version header, write-order rules, CF_ModStorage alternative
- `rpc.md` - ScriptRPC, RPCSingleParam, OnRPC switch template, client-to-server validation rules
- `modded_class.md` - super.\* rules, field injection, mod load order, compatibility patterns
- `singleton.md` - Static s_Instance, lazy init, GetInstance(), JSON config with nested sub-objects
- `language_workarounds.md` - No ternary, no auto type inference, no lambdas, no exceptions, no overloading

### examples/ (optional)

Complete working script files demonstrating full implementations:

- `01_custom_item.c` - Custom item with NetSync bool flag and versioned OnStoreSave/OnStoreLoad
- `02_custom_action_singleuse.c` - Single-use ActionBase with CanPerformAction guard and server execution
- `03_continuous_action.c` - Hold-to-complete action with progress bar, interrupt handling, cooldown
- `04_rpc_patterns.c` - All three RPC APIs: RPCSingleParam, GetGame().RPC, ScriptRPC multi-field
- `05_mission_server.c` - MissionServer overrides: PlayerConnect, PlayerDisconnect, OnUpdate tick
- `06_json_config.c` - JsonFileLoader singleton config with nested sub-config and admin UID list
- `07_agent_modifier.c` - Full SymptomBase + ModifierBase disease stack with agent threshold trigger
- `08_gui_menu.c` - UIScriptedMenu with TextListboxWidget rows, EditBox filter, button handlers
- `09_scheduler_timer.c` - CallLater, Timer, OnScheduledTick patterns with frame-skip guard
- `10_modded_playerbase.c` - Comprehensive PlayerBase mod combining NetSync, RPC, persistence, actions
- `11_hud_plain_text.layout` - HUD overlay with TextWidgets (float RGBA colors, pixel coords); companion modded Hud Update() script
- `12_menu_interactions.layout` - Dialog with EditBoxWidgetClass filter, 2-column TextListboxWidgetClass, ButtonWidgetClass
- `13_item_preview.layout` - Item inspect panel with ItemPreviewWidgetClass for live 3D model; rotate via SetModelOrientation
