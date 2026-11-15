---
name: ecommons
description: "Write and debug FFXIV Dalamud plugins that use ECommons. Use when working with ECommonsMain.Init/Dispose, Svc, ImGuiEx, TaskManager, AddonMaster, Callback.Fire, EzIPC, EzHook, EzThrottler, EzConfig, EzConfigGui config windows, commands, logging, game helpers, Excel sheet access, Splatoon drawing from a regular plugin, or ECommons/Dalamud version mismatches. Covers pinned member signatures and automation lifetimes; use stock Dalamud guidance for its own services."
license: "MIT; bundled upstream files retain their own licenses, listed in references/NOTICE.md."
---

# ECommons

The bundled ECommons snapshot is `master` at `bc38dc7` (2026-11-08), version `3.2.1.26`, checked against Dalamud API 15. Match the user's package or submodule pin before copying a signature. The API/version mapping in the guide is inferred from packages and target frameworks, not an upstream compatibility guarantee.

The NuGet package `3.2.1.26` was built from the earlier commit `26d30b9` and lacks a few members the mirror has; [setup](references/topic-setup.md#package-and-master-differences) lists them. For a plugin on `3.2.1.22` or older, read the [changes since 3.2.1.21](references/guide.md#changes-since-32121) before using TaskManager stacks, UI click helpers, or `EnumCombo`. Resolve members missing from the mirror against the project's exact ECommons commit.

## Workflow

1. Read the plugin project to determine whether it builds ECommons from NuGet or a submodule. A `.gitmodules` entry alone does not establish which copy is used; avoid shipping both.
2. Read [setup](references/topic-setup.md) for dependency and initialization work, then the task-specific topic below.
3. Find uncertain members in `references/all-public-members.txt` or `references/all-public-types.txt` and inspect the corresponding file under `references/ecommons/`. An index hit is a lookup aid; inspect accessibility and surrounding code.
4. Initialize ECommons before using `Svc`, configuration, task queues, hooks, or IPC helpers. Select only the modules the plugin needs. Dispose the plugin's own consumers before `ECommonsMain.Dispose()`.
5. Build against the user's SDK and dependency pin. On version errors, verify package/project selection, target framework, and member spelling before changing a call.
6. Reload in an available development client and exercise the changed behavior. Check `/xllog`, teardown, task cancellation, and repeated load/unload. For automation, validate the target addon and readiness before callbacks. If the client is unavailable, report source review and build results without claiming runtime verification.

## Initialization

```csharp
using ECommons;

// Inside the plugin constructor, before ECommons consumers:
ECommonsMain.Init(pluginInterface, this);
// In plugin disposal, after disposing those consumers:
ECommonsMain.Dispose();
```

TaskManager uses retry and timeout semantics that depend on its API generation. Read [TaskManager](references/topic-taskmanager.md) before adding queued automation; provide a bounded completion condition and an abort path. Check game/addon state on each step instead of retaining a pointer across frames.

## Task routing

| Task | Read |
|---|---|
| Dependency setup or complete plugin example | [Setup](references/topic-setup.md), [examples](references/topic-examples.md) |
| ImGuiEx text/layout, widgets, textures | [Core helpers](references/topic-imguiex-core.md), [widgets](references/topic-imguiex-widgets.md), [other ImGui helpers](references/topic-imgui-helpers.md) |
| Config windows, save/load, migration | [Simple GUI](references/topic-simplegui.md), [configuration](references/topic-configuration.md) |
| Queues, addon callbacks, native windows | [TaskManager](references/topic-taskmanager.md), [automation](references/topic-automation.md), [AddonMaster](references/topic-addonmaster.md) |
| IPC and hooks | [EzIPC](references/topic-ezipc.md), [EzHook](references/topic-ezhook.md), [game hooks](references/topic-game-hooks.md) |
| Throttlers, scheduling, player state, sheets | [Events](references/topic-events-throttlers-schedulers.md), [game helpers](references/topic-game.md), [Excel](references/topic-excel.md) |
| Extension methods, commands, reflection | [Generic helpers](references/topic-generic-helpers.md), [logging and commands](references/topic-logging-commands.md), [reflection](references/topic-reflection-interop.md) |
| Splatoon drawing from a regular plugin | [SplatoonAPI](references/topic-splatoonapi.md) |

[The technical guide](references/guide.md) retains module flags, the namespace catalog, examples, and pitfalls. See [NOTICE.md](references/NOTICE.md) for file-specific licenses and provenance gaps; the upstream tree includes terms beyond ECommons' top-level MIT license.
