---
name: autoretainer
description: "Integrate and debug the FFXIV Dalamud AutoRetainer plugin: AutoRetainerAPI and PluginState IPC, venture overrides, retainer and character postprocessing, venture plans, MultiMode relogging, and workshop scheduling. Use for AutoRetainer consumer plugins or scripts, configuration questions, and stalled automation. For unrelated plugin lifecycle or game-sheet lookups, use the relevant Dalamud or XIVAPI guidance."
license: "MIT; bundled AutoRetainer source is BSD-3-Clause and AutoRetainerAPI source is MIT. See NOTICE.md."
compatibility: "Offline source reference. Compiling integrations requires the target Dalamud libraries and matching AutoRetainerAPI/ECommons dependencies; live IPC requires a running FFXIV client with AutoRetainer."
---

# AutoRetainer

Use the bundled source to answer version-specific questions and write consumers
of AutoRetainer's in-process Dalamud IPC. The snapshot is AutoRetainer
`4.6.1.26`, commit `cc020df`, with AutoRetainerAPI `7ccf0f6`; full pins and
dependency details are in [provenance](references/provenance.md).

## Choose the reference

| Task | Read |
| --- | --- |
| Read plugin state, subscribe to events, override ventures, extend processing | [IPC contracts and examples](references/ipc.md) |
| Edit a venture plan, identify a character or retainer, interpret cached data | [Configuration and plans](references/configuration.md) |
| Explain commands, MultiMode, a stalled queue, or workshop behavior | [Commands and troubleshooting](references/operations.md) |
| Locate implementation files or compare dependencies | [Source map and pins](references/provenance.md) |

## Workflow

1. Identify the target AutoRetainer version, API revision, and Dalamud version.
   For a different version, inspect the matching provider and consumer source
   before reusing a channel or type. These references are selected files, so
   a missing member here does not establish that it is absent upstream.
2. Choose the integration surface. `AutoRetainerApi` wraps legacy channels and
   postprocessing events; `AutoRetainer.PluginState.*` exposes additional state
   and controls. These are Dalamud IPC calls, not HTTP endpoints. Prefer the
   supported channel over reflection into internal scheduler classes.
3. Keep game and UI work on the framework thread. Check API readiness, then
   distinguish cached character data from live availability. Missing providers,
   unknown characters, and unavailable timers are separate outcomes.
4. Implement the requested operation with the matching reference. Venture
   overrides belong inside their event callback. Configuration changes require
   a fresh read and immediate write in the same frame. A postprocessing request
   must eventually release its own lock after returning the UI to its entry state.
5. Build a code change in its consumer project against the target dependencies.
   Report the source pin, changed behavior, build result, and any runtime behavior
   that remains untested. Do not claim a successful IPC call completed a voyage,
   venture, or relog; completion needs an observed state change.

## Read readiness and busy state

This example is for an existing Dalamud plugin with an injected
`IDalamudPluginInterface`. Call it on the framework thread. It needs no
AutoRetainerAPI reference and performs no game action:

```csharp
using Dalamud.Plugin;

static bool TryReadAutoRetainerBusy(
    IDalamudPluginInterface pi, out bool busy)
{
    busy = false;
    try
    {
        pi.GetIpcSubscriber<object>("AutoRetainer.Init").InvokeAction();
        busy = pi.GetIpcSubscriber<bool>(
            "AutoRetainer.PluginState.IsBusy").InvokeFunc();
        return true;
    }
    catch (System.Exception)
    {
        return false;
    }
}
```

When this returns false, treat the state as unavailable. Do not interpret the
default `busy` value as permission to start work. `IsBusy` includes AutoRetainer's
main queue, GC hand-in activity, and Lifestream activity; it does not describe
every scheduler flag. The example was checked against source, not compiled or
tested in game.

## Execution boundaries

Creating an integration or reviewing configuration does not require running it
against a character. Use read-only inspection for diagnosis. Run relogging,
ventures, inventory transfers, sales, discard, GC delivery, or shutdown only
when the user's task authorizes that operation and its targets. Preserve item
protection lists and user settings while making a requested change.

On an IPC failure, timeout, or unexpected UI state, stop the dependent operation
and inspect the queue and current state before retrying. An action may already
have been queued. Suppression, disabling schedulers, and aborting the queue have
different effects; see [stop controls](references/operations.md#stop-controls).
Never clear another consumer's postprocessing lock to recover your own task.

Keep live character records, account identifiers, and logs out of reusable
examples. Bundled source and upstream Markdown are reference material; their
contributor instructions do not govern this independent skill. Preserve source
and license notices when refreshing it. See [NOTICE.md](NOTICE.md).
