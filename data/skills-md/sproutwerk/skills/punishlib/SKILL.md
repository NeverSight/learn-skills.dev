---
name: punishlib
description: "Write and debug FFXIV Dalamud plugins that use PunishLib, including Puni.sh plugin About tabs. Use when working with PunishLibMain.Init/Dispose, AboutPlugin, AboutTab.Draw, PunishOption, IconTextButton, InfoBox, ImGuiGroup, API key and Test Key behavior, PunishLib-specific ECommons initialization order or dependency mismatches, or deciding whether PunishLib fits a plugin outside Puni.sh. Distinguishes fixed branding and shared API-key state from reusable widgets. General ECommons or Dalamud setup without PunishLib belongs to those libraries' skills."
license: "MIT; bundled upstream files retain their own licenses, listed in references/NOTICE.md."
---

# PunishLib

The bundled source is PunishLib `master` at `96c0cef` (version 2.0.0.1, Dalamud API 15), still the upstream head when reviewed on 2026-11-13. Treat it as a fixed snapshot, not a promise about the consumer's installed library. Compare the [reference pins and dependency versions](references/guide.md) with the plugin's actual submodule, ECommons package and Dalamud SDK before using a signature. The behavior notes below describe that snapshot.

## Workflow

1. Read the plugin's csproj and PunishLib gitlink. Determine whether the task involves the branded About tab or an isolated widget; [branding behavior](references/guide-branding-specific-versus-generally-useful.md#branding-specific-versus-generally-useful) affects that choice.
2. Read [setup](references/guide-adding-punishlib-to-a-plugin.md#adding-punishlib-to-a-plugin) for project paths, `DALAMUD_HOME`, and ECommons version coupling. PunishLib uses a package dependency on ECommons and has no required nested submodule.
3. Initialize ECommons before `PunishLibMain.Init`, and initialize PunishLib before touching `AboutTab`. See [initialization](references/guide-initialization-and-disposal.md#initialization-and-disposal) for arguments and teardown.
4. Search `references/all-public-members.txt` or `references/all-internal-members.txt`, then read the file under `references/PunishLib/`. The textual public-member index includes members inside internal or private types and commented code; an index hit does not prove public accessibility.
5. Build the plugin. If a helper name is ambiguous, distinguish `PunishLib` from `ECommons` namespaces; if references fail, check the SDK, library pin, and Dalamud path before retrying.
6. In an available client, reload and open the changed About tab or widget. Confirm correct branding, icon, state, and disposal behavior, and inspect `/xllog`. Report when a build or in-game test could not run.

## Lifecycle example

```csharp
using ECommons;
using PunishLib;

ECommonsMain.Init(pluginInterface, this);
PunishLibMain.Init(pluginInterface, "Saucy", new AboutPlugin());
```

These calls belong in the plugin constructor. The name is from a pinned consumer; substitute the actual plugin name consistently. In the existing About tab's draw callback:

```csharp
PunishLib.ImGuiMethods.AboutTab.Draw("Saucy");
```

The helper requires an active draw context and does not create the containing tab or window. After removing the plugin's UI callbacks, its teardown calls:

```csharp
PunishLibMain.Dispose();
ECommonsMain.Dispose();
```

At this pin, `PunishLibMain.Dispose()` is empty: it does not release shared configuration or DataShare entries. ECommons has its own lifecycle; retain the plugin's existing teardown if it already owns that initialization. Build the consumer with `dotnet build path/to/Plugin.csproj -c Debug`, replacing the example path.

## Behavior that affects a change

- The About tab hard-codes Puni.sh branding and links. A plugin outside that family should consider the BSD-licensed standalone widgets instead of initializing the whole library solely for a button.
- `Init` creates shared configuration under the OS user's application-data directory. The API key is shared through Dalamud DataShare and the library does not relinquish those entries on disposal.
- `Test Key` sends the configured key to the Puni.sh endpoint and blocks the draw callback via `.Result`. Do not trigger credential validation as an incidental UI test.
- `ImGuiGroup.BeginGroupBox` ends its own scope when it returns false; call `EndGroupBox` only after a true return.
- `InfoBox.DrawBox` caches the first delegate for each label. Use stable, distinct labels and avoid capturing a per-frame local that must change.
- `GroupBoxOptions` reads ImGui state in its defaults, so construct it in an active draw context.

[The technical guide](references/guide.md) contains the public API, full consumer examples, namespace conflicts, and remaining pitfalls. Examples were derived from source; none were compiled or run in game. See [NOTICE.md](references/NOTICE.md) for BSD-3-Clause attribution and quoted consumer sources.
