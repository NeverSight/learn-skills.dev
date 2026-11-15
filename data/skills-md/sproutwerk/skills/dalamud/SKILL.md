---
name: dalamud
description: "Create, port, debug, or review C# FFXIV Dalamud plugins. Use when working with Dalamud.NET.Sdk setup, IDalamudPlugin and IAsyncDalamudPlugin lifecycle, service injection, framework threading, hooks and signatures, IPC, SeString, Lumina sheets, addon events, dev-plugin loading, publishing requirements, or an API-level migration. For ImGui drawing APIs use the Dalamud ImGui skill."
license: "MIT; bundled upstream files retain their own licenses, listed in references/NOTICE.md."
compatibility: "Pinned reference: Dalamud 43b3411 (15.0.3.9, API 15; reviewed 2026-11-13), with API 9–16 migration notes. Match the target SDK, manifest API level, and runtime before using snapshot-specific APIs."
---

# Dalamud plugin development

## Compatibility

Inspect the user's SDK, manifest API level, and runtime version before applying a snapshot-specific API. Compare them with the [bundled revision record](references/guide.md) and consult [migration notes](references/topic-migration.md) and [changes within API 15](references/guide.md#changes-within-api-15-since-the-previous-pin) when they differ.

## Workflow

1. Inspect the project, manifest, and failure: setup, loading, compile error, hook, service, or game-thread behavior. Read the matching topic below before changing code.
2. Resolve service names and signatures from the source at the target runtime's commit. Use the bundled `references/dalamud/` sources and indexes when their pin matches; an absent index entry does not rule out a newer API.
3. Make the change within the plugin's existing lifecycle. Constructor injection and `[PluginService]` both work; unsubscribe events, dispose hooks, and remove commands during disposal.
4. Build the plugin using its target SDK. If compilation fails after an API bump, check SDK, target framework, manifest, package/submodule pins, and renamed service members together.
5. In an available development client, reload through `/xlplugins`, exercise the changed path, and inspect `/xllog`. Verify the plugin appears with the expected manifest and that unload/reload does not leave duplicate callbacks. If loading fails, follow [dev-workflow diagnostics](references/topic-dev-workflow.md), correct the cause, rebuild, and retry.
6. Report build and runtime checks separately. When no game client is available, state that runtime behavior remains untested.

## Framework event lifecycle

Constructor-injected services can be retained for teardown. Subscribe once and remove the same delegate on disposal:

```csharp
using Dalamud.Plugin;
using Dalamud.Plugin.Services;

public sealed class Plugin : IDalamudPlugin
{
    private readonly IFramework framework;

    public Plugin(IFramework framework)
    {
        this.framework = framework;
        framework.Update += OnUpdate;
    }

    public void Dispose() => framework.Update -= OnUpdate;

    private void OnUpdate(IFramework framework)
    {
        // Perform the plugin's per-tick game-state work here.
    }
}
```

Use this as the entry class only when creating a plugin; merge the subscription and teardown into an existing entry class when editing one. Build with `dotnet build` from the plugin project directory, then follow the reload check above.

## Runtime constraints

Use injected public service interfaces. Access game state on the framework thread; choose `IFramework.Run`, `RunOnFrameworkThread`, or `RunOnTick` according to the scheduling semantics in [threading](references/guide-threading.md#threading). Avoid blocking the draw callback or framework thread on network or long-running work.

Create hooks through `IGameInteropProvider`; keep the delegate and hook alive and dispose them on unload. Prefer `IAddonLifecycle`, `IAddonEventManager`, or `IAgentLifecycle` for events those services already expose. Dalamud initializes its bundled FFXIVClientStructs resolver; a normal plugin must not repeat that initialization.

## Task routing

| Task | Read |
|---|---|
| SDK, manifest, build, references | [Project setup](references/topic-project-setup.md) |
| Plugin interface, configuration, UI events | [Plugin interface](references/topic-plugin-interface.md) |
| Service members and lifetimes | [Services](references/topic-services.md) |
| Hooks, signatures, native interop | [Hooking](references/topic-hooking.md) |
| IPC call gates and DataShare | [IPC](references/topic-ipc.md) |
| SeString, chat, payloads | [Text and chat](references/topic-sestring-chat.md) |
| Addon and agent events | [Addons](references/topic-addons.md) |
| Plugin discovery, reload, debugging | [Development workflow](references/topic-dev-workflow.md) |
| API migration or broken post-update build | [Migration](references/topic-migration.md) |
| Submission to an official plugin repository | [Publishing](references/topic-publishing.md); this documents requirements and does not authorize submission |

[The technical guide](references/guide.md) contains lifecycle examples, service summaries, threading rules, commands, configuration, and pitfalls. For stock drawing APIs use `dalamudimgui`; for native memory layouts use `clientstructs`. These companion skills are optional; the bundled sources remain available independently.

Source material has separate licenses in [NOTICE.md](references/NOTICE.md). When a file is not bundled, read it from `https://github.com/goatcorp/Dalamud` at the commit the target runtime reports. Upstream contribution policies remain relevant to an actual submission.
