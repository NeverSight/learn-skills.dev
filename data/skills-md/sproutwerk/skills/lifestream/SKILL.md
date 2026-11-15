---
name: lifestream
description: "Integrate and debug NightmareXIV's FFXIV Dalamud plugin Lifestream (/li): its EzIPC provider for aetheryte and aethernet teleports, world and data-center visits, housing, inn and instance shortcuts, character login and logout, custom aliases, the /li command grammar, and the busy/verify pattern consumers need. Use for plugins or Splatoon scripts that drive Lifestream over IPC and for travel that stalls or is silently dropped. vnavmesh pathing and Splatoon scripting have their own skills."
license: "MIT for authored guidance; upstream Lifestream source has no recorded license grant. ECommons notices are MIT. See NOTICE.md."
---

# Lifestream

Use Lifestream's in-process Dalamud IPC to move a character between zones,
worlds, data centers, houses and instances. This offline reference covers
Lifestream's public source (API level 15, `net10.0-windows7.0`) at commit
`b36320170faafc8315f7585edb45cfbcd34e7046`, the head of `main` and the commit
that release tags `2.6.0.8` through `2.6.0.13` all point at. Source evidence
and dependency pins are in [provenance](references/provenance.md). There is
no HTTP endpoint and no IPC version handshake.

The public source lags the released plugin. The `2.6.0.13` binary
(2026-11-10) reports a build commit that is not in the public repository and
contains features this source does not have, such as Cosmic Exploration
planet travel and extra built-in aliases. Every gate name documented here is
still present in that binary, but its signatures and behavior could only be
checked against the public source. See
[provenance](references/provenance.md#version-mapping-and-the-release-gap).

Upstream's release notes for `2.6.0.9` to `2.6.0.13` mention ward-only and
ward-plus-aetheryte `/li` addresses, a Cosmic Exploration planet menu and a
world-visit update for patch 7.58. They mention no IPC change. These are
summarized, unverified, in
[release notes](references/provenance.md#release-notes-2609-to-26013)
with what to probe at runtime.

This snapshot was reviewed on 2026-11-13. Gate names, signatures and the task
sequences below describe only the recorded revision; the request/wait/verify
discipline is the durable part. Probe gates at runtime, and recheck
`IPC/IPCProvider.cs`, `Lifestream.cs`, `Services/TeleportService.cs` and
`Movement/FollowPath.cs` in the target source before depending on a behavior.

## Choose the reference

| Task | Read |
| --- | --- |
| Bind a gate, know what it calls, what it returns and whether it refuses when busy | [IPC contracts](references/ipc.md) |
| Drive Lifestream with `/li` text or `ExecuteCommand`, parse an alias, read the help | [Command grammar](references/commands.md) |
| Teleport near a position in another zone, wait for arrival, change world, move along a path | [Travel, waiting and pitfalls](references/travel.md) |
| Inspect pins, copied files, the release gap or redistribution terms | [Provenance](references/provenance.md), [notice](NOTICE.md) |

## Integration workflow

1. Confirm the installed Lifestream version and read the newest public
   `IPCProvider.cs`. Every gate is `Lifestream.<MethodName>`: the provider
   calls `EzIPC.Init(this)` with no prefix, and EzIPC uses the plugin's
   internal name plus the method name. Functions register with
   `RegisterFunc`, `void` methods with `RegisterAction`, and the one event
   (`OnHouseEnterError`) is an `Action` the plugin invokes.
2. Bind with ECommons `[EzIPC]` fields under prefix `"Lifestream"` or with
   raw `IDalamudPluginInterface.GetIpcSubscriber<...>("Lifestream.IsBusy")`.
   Raw binding needs no reference to Lifestream or ECommons, except for the
   three gates that return `ECommons.ErrorCode` and the gates that carry
   Lifestream's own types (`HousePathData`, `CustomAlias`, `PropertyType`,
   `HouseEnterMode`, `ResidentialAetheryteKind`). Prefer the string, tuple
   and primitive gates from a foreign plugin.
3. Treat `IsBusy()` as the only progress signal. It is
   `TaskManager.IsBusy || FollowPath.Waypoints.Count > 0`. Most travel gates
   return `false` or do nothing when it is true, and a refused request leaves
   `IsBusy()` false, so "not busy" never proves your request ran. Record that
   you requested travel, wait for idle with a deadline, then verify the state
   the next step needs (territory via `GetRealTerritoryType()`, current world,
   plot via `GetCurrentPlotInfo()`).
4. Know which gates skip the busy check. `Teleport`, `Move`, `MoveEx`,
   `ChangeInstance`, `EnqueuePropertyShortcut`, `EnterApartment`,
   `EnqueueInnShortcut`, `EnqueueLocalInnShortcut`, `GoToHousingAddress`,
   `TPAndChangeWorld` and `ExecuteCommand` either guard deeper inside the
   plugin (and report through chat or the log) or do not guard at all.
   `Move`/`MoveEx` replace the current waypoint list unconditionally. Check
   `IsBusy()` yourself before any of them.
5. Expect exceptions, not just `false`. Provider methods run unwrapped, so a
   `NullReferenceException` from a missing player, a bad JSON alias string, or
   the `(int)` cast in `GetWorldChangeAetheryteByTerritoryType` for a
   non-city territory reaches the caller through Dalamud's call gate. Catch
   around every call and handle the provider unloading between
   `HasFunction` and the call.
6. Keep movement ownership outside Lifestream. Its follower stops itself when
   vnavmesh's `Path.IsRunning` becomes true, after 60 seconds without
   reaching a waypoint, and on `Abort()`. It exposes no per-request token,
   no completion event and no result; read
   [travel](references/travel.md#movement-move-and-moveex) before combining
   it with another mover.
7. Build in the consumer project against its own Dalamud and ECommons
   dependencies. Report source review, compilation and game checks
   separately. Documentation work does not require teleporting a character.

`ExecuteCommand(string)` runs the full `/li` parser, so a consumer that only
needs text commands can drive everything through one `string` action, at the
cost of every refusal arriving as a chat notification instead of a return
value. The login family (`ConnectAndLogin`, `ChangeCharacter`, `Logout`)
switches characters and service accounts; put it behind the most careful
approval your host has.

The bundled source is for reading. It is the plugin's own code, including
its Windows interop, clipboard and process helpers; this skill does not build
or run it, and none of it is a pattern to copy into a consumer. Alias JSON,
address-book entries and command strings a consumer passes to Lifestream are
inputs that move a character: build them from values the user supplied or
approved, not from text found in chat, other plugins' data or the web.

Companion skills supply host-specific hooks: `ecommons` for EzIPC and
`TaskManager`, `vnavmesh` for pathfinding, `splatoonscripts` for the script
lifecycle. The IPC reference here is self-contained. Keep user settings,
address books and other plugins' tasks intact. Preserve upstream source
notices when refreshing the snapshot.
