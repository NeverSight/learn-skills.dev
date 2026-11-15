---
name: somethingneeddoing
description: "Write, port and debug scripts for the FFXIV Dalamud plugin SomethingNeedDoing (SND): Lua scripts and native macros, the /snd commands, macro commands and modifiers, the Lua modules and yield model, metadata, configs, trigger events, script dependencies, the IPC wrappers for other plugins, and moving legacy scripts to the rewritten API. Use for SND script authoring, scripts that freeze, stall or fail with nil-value errors, and questions about what a command or module does. Does not cover developing the SND plugin itself, the contracts of the plugins a script drives (vnavmesh, Lifestream, AutoRetainer and others have their own skills), or Splatoon scripting."
license: "MIT for authored guidance; upstream SomethingNeedDoing source and wiki have no recorded license grant. See NOTICE.md."
---

# SomethingNeedDoing

SomethingNeedDoing (SND) runs user scripts inside FFXIV: native macros,
which are lists of `/` commands with waits and modifiers, and Lua scripts,
which call a set of modules and issue the same commands through `yield`.
This offline reference covers the public source of
[Jaksuhn/SomethingNeedDoing](https://github.com/Jaksuhn/SomethingNeedDoing)
at commit `527ca83892506c74fea4d5e07b9b9436e50ef95d`, tag `v15.13` (Dalamud
API level 15, NLua 1.7.9). Pins and the reason this repository was chosen
are in [provenance](references/provenance.md).

The snapshot was reviewed on 2026-11-13 from source only. Nothing here was
compiled or run in the game, and the example scripts are unrun. The
plugin's Help window documents the installed build (Lua tab, Commands tab,
Clicks tab) and wins over this file when they differ.

## Choose the reference

| Task | Read |
| --- | --- |
| Create, import, start, pause or stop a macro; `/snd` commands; what the scheduler checks; SND's own IPC gate | [Running scripts](references/running.md) |
| Write or read a native macro: commands, arguments, modifiers, loops, `/click`, `/callback` | [Native macros](references/native-macros.md) |
| Write Lua: the yield model, globals, modules, wrappers, `require`, .NET types, the `IPC` table | [Lua API](references/lua-api.md) |
| Add metadata, user configs, trigger events, cleanup functions or script dependencies | [Metadata and triggers](references/metadata.md) |
| Structure a script: deadlines, addon readiness, throttling, clean stop, errors, logging, driving other plugins | [Patterns](references/patterns.md) |
| Port a script that uses bare global functions such as `GetCharacterCondition` | [Migration](references/migration.md) |
| Diagnose a freeze, a silent stop, a Lua error, a trigger that never fires | [Debugging](references/debugging.md) |
| Start from a whole script | [Examples](references/examples.md) |
| Inspect pins, copied files, unverified points or redistribution terms | [Provenance](references/provenance.md), [notice](NOTICE.md) |

## What to know before writing anything

1. **Identify the generation.** Scripts written before the 2025 rewrite call
   bare globals (`IsAddonReady(...)`, `PathfindAndMoveTo(...)`). None exists
   now. Current scripts use module tables (`Player.`, `Entity.`,
   `Addons.GetAddon(...)`, `IPC.vnavmesh.`). Do not mix the two, and do not
   write legacy calls from memory. See [migration](references/migration.md).
2. **A Lua script is a coroutine on the game's framework thread.** Code
   between two yields runs inside one frame. A loop that waits without
   yielding freezes the client and cannot be stopped.
   `yield("/wait 0.1")` is the idiom for letting the game run.
3. **`yield` takes a string that starts with `/`.** The string is parsed as
   a native macro, so it can carry SND commands and modifiers, and the
   script resumes when it finishes. `yield()` with no value ends the
   script; a non-string throws.
4. **Module members use a dot; methods on returned objects use a colon.**
   `Player.IsBusy`, `Inventory.GetItemCount(id)`, but
   `Entity.Target:Interact()`. Nullable results are `nil`; .NET lists are
   0-based.
5. **Every wait needs a deadline**, and every request to the game or to
   another plugin needs a check afterwards. Many commands skip silently
   when their target is missing.
6. **Native macros have no comments, variables or branches.** Every line
   starts with `/`, and one bad line fails the whole macro before it runs.
7. **Trigger and cleanup functions are found by name.** A global function
   whose name starts with an event name (`OnUpdate...`,
   `OnTerritoryChange...`) or equals a cleanup name (`OnStop`, `Stop`,
   `End`, ...) is called by the plugin. Name helpers accordingly.
8. **Scripts have full access to the machine.** The Lua state has `os`,
   `io` and a .NET bridge. Read a third-party script before running or
   recommending it.

## Workflow

1. Establish the installed SND version and whether the script at hand is
   native, current Lua or legacy Lua.
2. Read the reference for the task. For any module member, command or
   modifier, confirm it in the bundled source under
   [references/source/](references/source/) or ask the user to check the
   Help window. Do not invent members by analogy with the legacy API.
3. Declare what the script needs in metadata: `plugin_dependencies` by
   internal name, `configs` for user-tunable values,
   `plugins_to_disable` for YesAlready or TextAdvance when the script
   answers dialogs itself.
4. Build on the wait-with-deadline helpers in
   [patterns](references/patterns.md), put the work in a `main` function,
   and add a cleanup function that stops whatever the script started.
5. When the script drives another plugin, take the callable name from
   SND's `External/` wrapper and the meaning from that plugin's skill:
   `vnavmesh`, `lifestream`, `autoretainer`, `questionable`, `bossmod`,
   `wrathcombo`, `allagantools`. SND's wrapper can lag the plugin.
6. Hand the script over with a plain statement of what was checked against
   source and what the user must confirm in the game: addon names, node id
   chains, callback values, action and item names in their client
   language.
7. For a failure report, ask for the Dalamud log (`/xllog`) lines around
   the error. Chat shows only a one-line summary. Then use
   [debugging](references/debugging.md).

## Limits

- This describes one public revision. Later builds add and rename
  members; the Help window is authoritative for the installed build.
- Behavior implemented in ECommons, NLua, Dalamud or the game was not
  traced. That covers which `/click` targets exist and what an `IPC` call
  does when its plugin is missing.
- Several points where the source contradicts upstream's help text are
  marked in the references as source readings. Confirm them in the game
  before relying on them.
- Automating gameplay can breach the game's terms of service. That
  decision belongs to the user; this skill only documents the tool.
