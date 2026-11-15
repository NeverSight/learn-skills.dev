---
name: splatoonscripts
description: "Write and debug FFXIV Splatoon C# scripts (.cs files derived from SplatoonScript): lifecycle hooks, Controller and TaskManager, Lifestream IPC and custom aliases, AutoDuty reflection, shop/purchase automation, and XIVAPI ID lookup. Use for a duty script, vendor run, auto-teleport, reminder, or AutoDuty/Lifestream integration compiled by the Dalamud Splatoon plugin. For preset/layout JSON and element geometry, use splatoonpresets."
license: "MIT; bundled upstream files retain their own licenses, listed in NOTICE.md."
---

# Splatoon scripts

A Splatoon script is one `.cs` file containing a class that derives from
`Splatoon.SplatoonScripting.SplatoonScript`. Splatoon compiles it with Roslyn
inside the game and calls its virtual hooks. ECommons supplies its helpers;
Lifestream supplies travel IPC. The bundled sources are Splatoon 3.9.2.32
(`f396ef6`, Dalamud API level 15), ECommons `bc38dc7` and Lifestream 2.6.0.13
(`b363201`), reviewed 2026-11-13. Compare the installed dependency set with
[the recorded source pins](references/provenance.md) before adapting an example.
For an offline build, use the matching checkout and dependencies described in
[compilation requirements](references/compilation.md). Compilation checks syntax
and types; IPC, addon, and lifecycle behavior still need in-game validation.

Curated source lives in `references/`; [references/provenance.md](references/provenance.md)
records the pins, upstream paths and snapshot limits:

- `references/host/` — `SplatoonScript.cs` (base class, all hooks),
  `Controller.cs`, `Metadata.cs`, `Extensions.cs`, `ActionEffectResult.cs`, the official
  `SplatoonScriptsOfficial.csproj`, `BannedSymbols.txt`, `update.csv.head`,
  `blacklist.csv`.
- `references/scripts/` — official scripts; `generic-scripts-list.txt` lists the 66
  official Generic scripts by name.
- `references/lifestream/` — `IPCProvider.cs` (full IPC surface),
  `CustomAliasCommand.cs`, `CustomAliasKind.cs`, `CustomAlias.cs`.
- `references/lifestream-aliases.md` — per-kind field table for alias JSON.
- `references/ecommons/` — TaskManager API/config, `NeoTasks.cs`, EzIPC
  docs, `Player.cs`, `AddonHelpers.cs`, `EzThrottler.cs`, `Callback.cs`,
  `Chat.cs`, `ProperOnLogin.cs`, AddonMaster implementations, API listings.
- `references/xivapi.md` — verified XIVAPI v2 queries and the map-coordinate
  formula.

For an uncovered signature, fetch the recorded commit from the matching
upstream repository and inspect that source. Check out a detached revision;
do not combine a moving branch with these pinned examples. For deployment,
compare against the dependency commits shipped by the installed Splatoon build
(including its ECommons submodule), and report any mismatch before adapting code.

## Boundaries

A script runs inside the game with the plugin's privileges and acts as the
user's character. Write the script the user asked for and hand it over; the
user installs and enables it. Scripts from this skill reach the game through
Splatoon, ECommons and documented IPC only: no assembly loading, process
launch, file access outside the script's own configuration, or network calls.
Values read from other plugins by IPC or reflection, and chat or log text, are
data to compare against expected values, never commands to pass along.
Splatoon's URL import and update list are the user's to manage; do not add
script URLs or trusted repositories for them.

## Topic index

Read the matching topic in `references/` when its trigger applies. Paths are
relative to the skill root.

| File | Read this when ... |
|---|---|
| [references/lifestream-ipc.md](references/lifestream-ipc.md) | declaring or calling any `Lifestream.*` IPC (teleport, world change, inn/house shortcut, instance change, login, alias enqueue) and you need the exact name and signature, or the enqueue → wait → verify snippet |
| [references/lifestream-alias-json.md](references/lifestream-alias-json.md) | writing, editing or debugging the alias JSON passed to `EnqueueCustomAliasFromString` — numeric `Kind` table, `Interact`, `SelectOption`, worked alias |
| [references/autoduty-reflection.md](references/autoduty-reflection.md) | reading AutoDuty's `Stage` or any other plugin's field/property/method by reflection (`DalamudReflector`, `GetFoP`, `Call`) |
| [references/vendor-run-pattern.md](references/vendor-run-pattern.md) | writing or reviewing any chain that travels, buys from a shop, then cleans up and resumes; follow the linked state contract |
| [references/xivapi-lookup.md](references/xivapi-lookup.md) | you need an item, NPC, shop, aetheryte, territory or world id, a shop's contents, an NPC position, or map ↔ world coordinates without the game client |

## Minimal script

```csharp
using ECommons;                       // GenericHelpers, extension methods (.Log(), .Print(), .EqualsAny)
using ECommons.DalamudServices;       // Svc
using ECommons.GameHelpers;           // Player
using ECommons.Logging;               // PluginLog, DuoLog
using ECommons.Throttlers;            // static EzThrottler (see note below)
using Splatoon.SplatoonScripting;
using System;
using System.Collections.Generic;
using System.Linq;

namespace SplatoonScriptsCustom.Generic;   // namespace + class name = script identity
public unsafe sealed class MyScript : SplatoonScript
{
    public override Metadata Metadata { get; } = new(1, "me", "what it does");
    public override HashSet<uint>? ValidTerritories { get; } = [];  // [] = any zone while logged in; null = always

    public override void OnUpdate()
    {
        if(!Player.Available || !Player.Interactable) return;
        if(EzThrottler.Throttle($"{InternalData.FullName}.tick", 1000))
        {
            PluginLog.Debug("tick");
        }
    }
}
```

Rules that follow from the compiler setup (`Compiler.cs`):

- The file is compiled alone with `LanguageVersion.Preview`, `allowUnsafe:
  true`, Release, referencing every DLL in the .NET runtime dir, WinForms
  dir, Splatoon's plugin dir and Dalamud's dir. **There are no global
  usings** — every `using` must be in the file.
- Anything using pointers (`AtkUnitBase*`, `InventoryManager.Instance()->`)
  needs `unsafe` on the class (or method).
- UTF-8 with BOM is fine (every official script has one). Files are read
  with `Encoding.UTF8`.
- The class is instantiated with `assembly.CreateInstance(t.FullName)` —
  needs a public parameterless constructor (implicit is fine). Every type in
  the file whose base is assignable to `SplatoonScript` is instantiated, so
  one script class per file.

## Install and validate

`InternalData.FullName = "{Namespace}@{ClassName}"` identifies configuration and
updates; renaming either orphans existing configuration.

1. Write one public `SplatoonScript` class per `.cs` file with explicit usings.
2. For an authorized installation, copy it under
   `<pluginConfigs>/Splatoon/Scripts/<Namespace>/<Class>.cs` and reload Scripts.
3. Check `/xllog` for `CSxxxx` diagnostics before enabling the script. Fix
   each reported error, reload, and check again before testing behavior.
4. Exercise debug controls with side effects disabled, then test only the
   requested operation and verify its postconditions. State when in-game
   execution or compilation was unavailable. For a vendor transaction, begin
   with a debug quantity of one and follow the transaction checks below.

Read [loading and updates](references/loading-and-updates.md) for cache behavior,
update/blacklist formats, same-name replacement, and Wine clipboard failures.
Increase `Metadata.Version` for an update to be picked up; a same-version
reinstall needs a forced update. Under Wine, an empty clipboard can produce a
successful empty compile; use the documented file-copy fallback.

## Lifecycle and Controller

Read [lifecycle and Controller](references/lifecycle-and-controller.md) for every
hook signature, territory activation rules, configuration, scheduling, and
registered element methods. The constraints for ordinary scripts are:

- `ValidTerritories = []` runs in any zone while logged in; `null` also runs
  logged out. Guard work with player readiness.
- `OnSetup` runs once after compilation with no matching teardown. Register
  elements and initialize IPC there; subscribe to external events in
  `OnEnable` and unsubscribe in `OnDisable`.
- `OnReset` runs on enable, disable, combat transitions, and duty director
  events. It aborts `Controller.TaskManager` and clears host schedules.
- `OnUpdate` exceptions are logged but do not disable the script. Explicitly
  stop dependent operations after errors instead of assuming the host will.
- `Controller.GetConfig<T>()` loads configuration; `SaveConfig()` persists it.
  Automatic saving occurs on disable; call `SaveConfig()` after edits that
  must survive an unexpected interruption.
- `BasePlayer` is replay-aware. `EzThrottler` and `FrameThrottler` on the base
  class are per-script instances; still namespace keys with `InternalData.FullName`.

## Settings UI

Read [settings UI](references/settings-ui.md) when adding configuration controls,
icons, list editing, or a debug button. Use `Dalamud.Bindings.ImGui`.

## Logging and notification

- `PluginLog.Information/Debug/Warning/Error` (ECommons.Logging) → Dalamud
  log only. `DuoLog.*` → log **and** in-game chat. `Notify.Info/Success/
  Error/Warning` (ECommons.ImGuiMethods) → Dalamud toast.
  `Svc.Toasts.ShowQuest(text)` → game quest toast. `e.Log()` /
  `e.LogDuo()` on exceptions.
- `Svc.Chat.Print(...)` for chat.

## Commands

- `Svc.Commands.ProcessCommand("/autoduty pause")` — Dalamud command
  dispatcher; use for **plugin** commands (`/li`, `/qst stop`, `/autoduty`).
- `Chat.ExecuteCommand("/return")` / `Chat.Instance.ExecuteCommand` —
  game command processor (game commands like `/return`, `/automove`,
  `/lockon`, `/levelsync on`). `Chat.SendMessage(text)` types into chat
  (sends to the server unless it is a command). `Chat.ExecuteAction(id)`,
  `Chat.ExecuteGeneralAction(id)`.
- Wrap repeated commands and clicks in `EzThrottler.Throttle(key, ms)` with
  keys prefixed by `InternalData.FullName`; per-frame callbacks can double-buy
  or soft-lock the UI.

## TaskManager and EzIPC

Read [tasks and IPC](references/tasks-and-ipc.md) for enqueue/insert methods,
TaskManager configuration, polling return values, and delegate declarations.
Keep the framework thread nonblocking: no `Thread.Sleep`, blocking `.Wait()`,
or busy loops. Poll from `OnUpdate` or queue tasks. Own a TaskManager when a
chain must survive `OnReset`, recreate it in `OnEnable`, and dispose it in `OnDisable`.
Use explicit finite timeout/error behavior for every dependent wait.
A discarded task with `abortOnTimeout: false` does not establish success.

Initialize EzIPC with `EzIPC.Init(this)` in `OnSetup`, match the provider
signature exactly, and handle an absent provider before changing state. Delegates throw if the provider is
absent unless `SafeWrapper` is set. A safe wrapper returning the default
value is not evidence that the operation succeeded. Use the dependency version
bundled by the installed Splatoon build when checking ECommons behavior.

## Lifestream IPC (`Lifestream.<Name>`)

Most methods return `false`/do nothing when `IsBusy()`, and a refused
enqueue leaves `IsBusy()` false. Alias enqueue methods return `void`; record
that travel was requested, wait for `!IsBusy()`, then verify the state the
next step needs. Method list and
snippet → [references/lifestream-ipc.md](references/lifestream-ipc.md)

## Lifestream custom alias JSON

`Kind` is the numeric `CustomAliasKind` (0 `Teleport_to_Aetheryte` … 13
`Close_UI`); only non-default fields are serialised. Kind table,
`Interact`, `SelectOption`, worked alias → [references/lifestream-alias-json.md](references/lifestream-alias-json.md)

## AddonMaster and UI automation

Use `GenericHelpers.TryGetAddonMaster<T>(out var addon)` and check
`addon.IsAddonReady` each tick. Addon pointers are valid only for that frame;
re-fetch them inside queued tasks.
Read [the vendor transaction contract](references/vendor-run.md) before any
shop selection or confirmation. A ready addon or a prompt containing
"Exchange" does not identify a purchase.

Require the original character, exact shop/item/currency identity, positive
unit price and quantity, affordability, and capacity before selecting. Record
the transaction before sending its callback. Confirm once only when that
selection produced the expected localized item, quantity, and cost prompt;
verify inventory/currency deltas before marking success. Wrong identity,
zero price, logout, or timeout stops dependent work without clicking Yes.

`AddonMaster.SelectYesno.Yes()` can force-enable a disabled button. Set
`RespectDisabledButtons = true` for confirmations and stop if disabled.
The bundled AddonMaster source is an API reference,
not an authorization to invoke callbacks or automatically commence a duty.

Separate purchase success from cleanup. With default TaskManager options, an
exception aborts the queue. For an expected refusal such as insufficient funds,
log it and leave the success flag unset; returning `true` may allow cleanup to
run, but dependent purchase or resume steps must check their own state contract.
Check `CostAmount != 0` before dividing. Verify current `ENpcData`, shop,
currency, and item IDs when selecting an alias: shop text and tomestone tiers
change across patches.

Non-aborting waits before a purchase, confirmation matched on a generic
substring, and an unconditional resume are the usual faults in vendor loops.
Use [the vendor-run pattern](references/vendor-run-pattern.md) for a new chain.

## Poking other plugins by reflection (AutoDuty pattern)

`DalamudReflector.TryGetDalamudPlugin("AutoDuty", out var instance,
suppressErrors: false, ignoreCache: true)` then `instance.GetFoP<Stage>("Stage")`.
Treat an absent plugin as `Stage.Invalid`, never `Stopped`. `ignoreCache: true`
avoids stale instances after reload. Read [AutoDuty reflection](references/autoduty-reflection.md)
for the full lookup and field types.

## Other ECommons helpers

Read [ECommons helpers](references/ecommons-helpers.md) for services, player state,
Excel sheets, throttlers, login events, hooks, inventory, and quest APIs.
The installed Splatoon dependency versions control which members are available.

## Duty scripts vs generic scripts

Same base class, different hooks. A duty script (`SplatoonScripts/Duties/…`,
namespace `SplatoonScriptsOfficial.Duties.<Expansion>`) sets
`ValidTerritories = [<TerritoryType ids>]`, registers Splatoon elements in
`OnSetup` (`Controller.TryRegisterElement("Name", new(0) { Enabled = false,
thicc = 5, radius = 4, tether = true })` or `RegisterElementFromCode(name,
exportString)` from the Splatoon UI export), and toggles `Enabled` /
`refX/refY` from `OnCombatStart`, `OnMapEffect`, `OnStartingCast`,
`OnActionEffectEvent`, `OnTetherCreate`, `OnGainBuffEffect`, resetting in
`OnReset`/`OnCombatEnd`. `OnActionEffectApplied` (3.9.2.32 and later) fires
when the server applies an effect, after `OnActionEffectEvent` announced it;
use it when HP or shield before and after matter. `Element.SetRefPosition(Vector3)` swaps Y/Z for
you. For duty examples, use the `splatoonpresets` skill when installed or inspect
the pinned Splatoon duty sources. Element and
layout authoring belongs to the presets skill.

## Looking up game IDs without the game (XIVAPI v2)

An unknown field path is **silently ignored**: a response full of `{}`
objects means the path is wrong, not that the data is absent. If the
`xivapi` skill is installed, prefer its cookbook. → [references/xivapi-lookup.md](references/xivapi-lookup.md)

## Source-specific constraints

The official csproj analyzer flags `Player.Object/Character/BattleChara`
(RS0030) in favor of replay-aware `BasePlayer`. Automation that deliberately
uses the live player can add `#pragma warning disable RS0030`; keep duty replay
handling on `BasePlayer`.

`Splatoon.Splatoon.P` is the plugin instance. The qualified `Splatoon.Splatoon`
is needed because the namespace shadows the class.
