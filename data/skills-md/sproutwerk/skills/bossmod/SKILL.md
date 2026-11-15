---
name: bossmod
description: "Integrate and develop awgil's FFXIV BossMod (Boss Mod, VBM): Dalamud IPC, encounter modules and components, state machines, world-state hints, rotation presets, AI controls, and replay debugging. Use for VBM consumer plugins or module packs. Identify the repository and build before porting code; forks can expose different endpoints and types."
license: "MIT for authored guidance; bundled BossMod source is BSD-3-Clause. See NOTICE.md."
metadata:
  aliases: "BossMod, Boss Mod, VBM"
  reviewed-at: "2026-11-13"
  compatibility: "Offline reference for awgil/ffxiv_bossmod c50e67f3, version 7.5.8.2, Dalamud.NET.Sdk 15.0.0. Examples are source-derived and uncompiled."
---

# BossMod / VBM

Use this skill for awgil's BossMod, also called VBM. The full source pin is
`c50e67f37aa22f86d064489913ec9887f116accf`. Confirm the target repository and
version before reusing an IPC signature or module constructor. The `BossMod`
namespace and `BossMod.*` IPC prefix alone do not identify the provider.

Upstream can change multiple times daily, including breaking changes. Pinned
snapshots inevitably lag and cannot promise exact parity. Use this skill to
understand the integration architecture and find the contracts to recheck
against the target plugin; it is not continuously synchronized. The durable
workflow below is separate from the revision-specific APIs in the references.

## Choose the reference

| Task | Read |
| --- | --- |
| Call IPC, inspect availability, manage presets or transient strategies | [IPC contracts](references/ipc.md) |
| Write an encounter component, state machine, or module pack | [Module authoring](references/modules.md) |
| Interpret world state, AI hints, rotation selection, or stop controls | [World state and automation](references/world-and-rotation.md) |
| Reproduce a mechanic, debug loading, or plan a build | [Replay and development](references/development.md) |
| Identify the provider or port an integration | [Fork boundary](references/fork-boundary.md) |
| Locate source, dependency pins, and verification limits | [Provenance](references/provenance.md) |

## Workflow

1. Establish whether the task changes a consumer plugin, an encounter module,
   or a rotation module. Prefer registered IPC for external consumers. Public
   C# classes inside BossMod are version-specific implementation APIs, not a
   shared cross-fork ABI.
2. Read the matching provider and its called implementation. The bundled
   snapshot is selective; a missing file does not prove a feature is absent.
   For another revision, retrieve that revision before choosing types or names.
3. Keep calls that read or change plugin/game state on the framework thread.
   Treat provider absence, an exception, and a normal false/null result as
   different outcomes. Stop dependent work on an uncertain mutation; reread
   state before deciding whether to retry.
4. Use the module's `WorldState` and clock for mechanics. Its events and replay
   operations drive the same logic offline. Avoid game singleton reads in
   encounter components and do not retain actors across world resets.
5. Build code changes against the target project. For mechanics, inspect a
   replay around activation, resolution, phase changes, and reset. Report
   source review, compilation, and runtime checks separately.

## Read-only IPC example

For an existing Dalamud plugin with `IDalamudPluginInterface pi`, this reports
whether a module is registered for a BNpcBase/DataId. It does not report whether
that module is loaded, enabled, or active:

```csharp
static bool TryHasVbmModule(Dalamud.Plugin.IDalamudPluginInterface pi,
    uint dataId, out bool hasModule, out string? error)
{
    hasModule = false;
    error = null;
    try
    {
        hasModule = pi.GetIpcSubscriber<uint, bool>(
            "BossMod.HasModuleByDataId").InvokeFunc(dataId);
        return true;
    }
    catch (System.Exception ex)
    {
        error = ex.Message;
        return false;
    }
}
```

A false return from this helper means the read failed; its `hasModule` value
is then unknown. The example is source-derived, uncompiled, and untested in
game. It assumes the caller has already identified VBM.

Documentation and offline development do not require live game actions.
Execute movement, targeting, combat, configuration writes, or preset changes
only within the user's requested scope. Do not enable automation to probe
availability. Preserve user presets and stop flags; the IPC has no ownership
lease that arbitrates competing consumers.

Keep private replays and character data out of reusable examples. Preserve
upstream notices when copying or refreshing source; see [NOTICE.md](NOTICE.md).
