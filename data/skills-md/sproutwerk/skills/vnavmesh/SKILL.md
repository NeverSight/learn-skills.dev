---
name: vnavmesh
description: "Integrate and debug awgil's FFXIV Dalamud vnavmesh (ffxiv_navmesh, vnav, sometimes called vnavmash): navigation IPC, mesh readiness, asynchronous path queries, path following, flying, cancellation, and arrival checks in consumer plugins or Splatoon scripts. Use for vnavmesh development and stuck navigation. BossMod combat AI and unrelated navmesh libraries have different contracts."
license: "MIT for authored guidance; upstream vnavmesh source has no recorded license grant. DotRecast notices are separate. See NOTICE.md."
---

# vnavmesh

Use vnavmesh's in-process Dalamud IPC for navigation. This offline reference
covers vnavmesh `1.2.3.15`, using `Dalamud.NET.Sdk/15.0.0`. The pinned provider is
`38d2a24c3306f24640e64efe13915a78d301e878`; dependencies and source evidence are
in [provenance](references/provenance.md). Match the installed version before
using a channel. There is no HTTP endpoint or IPC version handshake in this
provider.

Upstream can change several times a day, including breaking changes. This
snapshot was reviewed on 2026-11-13 and will lag; it is not continuously synced
and cannot promise exact parity with an installed build. Use the skill to
understand the integration architecture and find the contracts to verify.
Lifetime ownership, bounded waits and independent arrival checks are durable
design guidance. Channel names, signatures, defaults and implementation behavior
below describe only the recorded revision. Recheck `IPCProvider.cs`,
`NavmeshManager.cs`, `AsyncMoveRequest.cs` and `Movement/FollowPath.cs` in the
target source before relying on them.

## Choose the reference

| Task | Read |
| --- | --- |
| Bind IPC, query a route, distinguish state and return types | [IPC contracts](references/ipc.md) |
| Start/stop movement, cancel work, observe arrival, integrate a script | [Consumer lifecycle and bounded example](references/consumers.md) |
| Diagnose loading, bad coordinates, flight, empty paths or retries | [Navigation and troubleshooting](references/navigation.md) |
| Inspect source, dependencies, actual callers or redistribution terms | [Provenance](references/provenance.md), [notice](NOTICE.md) |

## Integration workflow

1. Inspect the consumer's Dalamud SDK and installed vnavmesh version. Read the
   matching provider and implementation, not just a wrapper's method names.
   Raw IPC needs no reference to the vnavmesh assembly or ECommons.
   Prefer these exported channels over reflection into manager fields, native
   hooks or copying the provider's startup/resolver code into a consumer.
2. Choose who owns movement. `Nav.Pathfind*` returns a task containing positions
   and does not move. `Path.MoveTo` follows supplied positions without finding
   a route. `SimpleMove.*` queries internally, then follows its typed waypoints.
   Raw position lists lose special waypoint metadata.
3. Check provider availability, player/territory state, and mesh readiness on
   the framework thread. Bound readiness waits. `Nav.IsReady` is only a non-null
   mesh check; it does not establish flight capability or a usable route.
4. Give each operation a lifetime token, deadline, and local generation number.
   Cancel on reset, zoning, disable or disposal. Recheck context before consuming
   an asynchronous result. Do not block the framework thread on a task.
5. For movement, coordinate exclusive use outside vnavmesh. Its IPC has no owner
   token, lock, per-client stop or arrival event. An accepted request, completed
   query, or empty waypoint queue does not prove arrival. Compare the current
   player position with the requested destination in the intended territory.
6. Build in the consumer project against its target dependencies. Report source
   review, compilation and game checks separately. Documentation work does not
   require running navigation against a character.

`Path.Stop` clears the current path but leaves pending SimpleMove work alive.
`Nav.PathfindCancelAll` reloads the shared mesh and affects other clients.
Read [cancellation](references/consumers.md#cancellation-and-ownership) before
implementing a stop button or timeout recovery.

Use the consumer's existing framework/Splatoon lifecycle. Companion Dalamud or
Splatoon skills can supply host-specific hooks when installed; the IPC reference
here is self-contained. Keep user settings and other plugins' operations intact.
Preserve upstream source notices when refreshing the snapshot.
