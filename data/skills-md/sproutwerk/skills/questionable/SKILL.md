---
name: questionable
description: "Integrate and debug Puni.sh Questionable for FFXIV: Dalamud IPC, quest selection and priority queues, completion checks, quest-path JSON, sequence and step conditions, and path-data loading. Use for Questionable consumer plugins, Splatoon integrations, or quest-path development. General navigation and combat rotation APIs have separate contracts."
license: "MIT for authored guidance; bundled Questionable source is AGPL-3.0. See NOTICE.md."
---

# Questionable

This skill covers Puni.sh Questionable `15.756.3.60` at
`0a1510bd7be42f3e5063a8bccf398312d2d2f7e9`, reviewed on 2026-11-13.
The plugin uses Dalamud SDK `15.0.0`. Check the target fork and revision before
using these contracts; an installed version number alone does not identify
its exact source or downloaded quest-path bundle.

## Choose the reference

| Task | Read |
| --- | --- |
| Bind IPC, interpret IDs and return values, change priorities | [IPC contracts](references/ipc.md) |
| Drive a quest from a consumer, handle cancellation and completion | [Consumer lifecycle](references/consumers.md) |
| Author quest JSON, fix sequences, diagnose unloaded or stuck paths | [Quest paths and diagnostics](references/quest-paths.md) |
| Find provider implementations, refresh the snapshot, check attribution | [Provenance](references/provenance.md), [notice](NOTICE.md) |

## Working rules

Use the exported `Questionable.*` Dalamud IPC channels for consumer plugins.
The provider does not expose an HTTP API, version handshake, ownership token,
or per-consumer queue. A caller does not need to reference Questionable's
assembly to use primitive IPC contracts.

Run game-state queries and mutations on the host's framework thread. Handle
provider unload separately from an idle result. Bind against the provider's
types, then inspect the controller to understand the side effects: a `true`
start result means the quest was found and start was invoked, while some
priority mutations return `true` even when nothing changes.

For one quest, prefer `StartSingleQuest`. `StartQuest` enables automatic
questing, which can continue beyond the requested quest. Check completion for
the requested ID, keep waits bounded, and coordinate with other automation
before calling the global `Stop`. Read the lifecycle reference before adding
timeout recovery or editing the user's priority list.

For quest-path work, match the pinned schema, model converters, and task
implementation. Preserve authors and existing `LastChecked` evidence; an
offline edit does not establish that a path works in game. The bundled source
is a lookup snapshot, not a complete build tree. Report source review,
compilation, schema checks, and runtime checks separately. Do not operate a
live character merely to validate documentation.
