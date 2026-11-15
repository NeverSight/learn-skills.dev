---
name: wrathcombo
description: "Integrate and debug the FFXIV Dalamud WrathCombo plugin through WrathCombo.API or its IPC: revocable leases, PvE combo and option overrides, automatic rotation, action requests, and positional hints. Use for consumer plugins or scripts, preset configuration, cancellation handling, and conflicting clients. Other rotation engines have separate APIs."
license: "MIT for authored guidance; bundled BSD, AGPL, and inherited GPL notices are preserved in NOTICE.md."
---

# WrathCombo integration

Use the public Dalamud IPC for consumer plugins and scripts. The bundled
snapshot is WrathCombo `main` at `a457838` (project version `1.0.4.27`, six
commits after that tag, Dalamud API 15) with its WrathCombo.API `0.5.8` gitlink
`b40c88c`. It was reviewed on 2026-11-13.
Full pins, dependencies, and source paths are in
[provenance](references/provenance.md).

Upstream can change multiple times daily, including breaking changes. Pinned
snapshots inevitably lag and cannot promise exact parity with the installed
plugin. This skill shortcuts understanding of the integration architecture and
where to verify contracts; it is not continuously synchronized. Ownership and
cancellation guidance is durable. Recheck endpoints, signatures, enums, and
behavior in the target provider and wrapper before relying on pinned details.

## Choose the reference

| Task | Read |
| --- | --- |
| Connect a consumer, handle errors, own and release a lease | [IPC and lifecycle](references/ipc.md) |
| Configure combos, options, or auto-rotation; debug competing clients | [Configuration and troubleshooting](references/configuration.md) |
| Request an action, apply a temporary blacklist, or display positional hints | [Action requests and hints](references/actions-and-hints.md) |
| Trace a claim, refresh the snapshot, or inspect licenses | [Provenance](references/provenance.md) and [NOTICE.md](NOTICE.md) |

## Workflow

1. Identify the installed WrathCombo version and the consumer's API dependency.
   Match provider and wrapper revisions before changing a signature. There is
   no version-negotiation gate in this snapshot; `IPCReady()` reports cache
   readiness, not compatibility or permission to mutate settings.
2. Initialize `WrathIPCWrapper.Init(pluginInterface)` before its first call.
   Prefer wrapper methods over the obsolete `RawMethod` fields. Keep errors
   visible during integration; suppressed failures can become `false`, `null`,
   or `SetResult.IGNORED`.
3. Inspect the existing job configuration before requesting control. Reads do
   not need a lease. Use discovered internal preset names, not translated UI
   labels or action IDs. The lease API supports PvE; PvP and arbitrary job
   sliders are outside its supported contract.
4. For a requested mutation, create one lease per consumer integration, register
   its cancellation callback first, and check every result. Make only the
   requested overrides. Broad job setup can select Simple mode or enable
   Advanced mode options, so it needs an explicit product choice.
5. Stop dependent work when a lease is revoked, an IPC call fails, or the player
   changes job. Release your lease when finished and during disposal. A release
   exposes remaining leases and saved settings; it does not guarantee rotation
   stops. Do not restore old global settings or clear another client's requests.
6. Build the integration against its target dependencies and report build and
   runtime results separately. Writing or reviewing integration code does not
   require executing combat actions in a live client.

Run game-facing calls on the framework thread. Lease callbacks should invalidate
local work and return; the provider invokes them before removing the lease.
Do not release or re-register recursively from the callback. See the
[consumer example](references/ipc.md#consumer-example) for this lifetime pattern.

The examples are source-derived and have not been compiled or tested in game.
The source mirror is selected evidence, not a buildable plugin distribution.
Missing files here do not establish that a feature is absent upstream.
