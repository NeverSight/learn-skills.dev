---
name: fivem-redm-performance-network
description: >
  Analyze and optimize FiveM and RedM resources for client/server resmon,
  Lua/native CPU, Wait(0) loops, hitch warnings, TriggerServerEvent /
  TriggerClientEvent / TriggerLatent* spam, payload size, broadcasts (-1),
  state bags, first-GET cache, MySQL load-at-start, neteventlog, profiler,
  and bandwidth. Use when reviewing,
  refactoring, debugging, or optimizing FiveM/RedM Lua performance or
  network traffic. Use when the user runs /fivem-redm-performance-network
  or $fivem-redm-performance-network.
license: MIT
metadata:
  author: PHUMWIWAT
  version: "1.0.0"
  short-description: FiveM/RedM resmon and network event optimization
---

# FiveM / RedM performance and network optimization

Specialist skill for **resmon CPU** and **network bytes**. Not a general implementation or natives encyclopedia.

Load references only when the task needs them. Do not preload all three.

| File | Open when |
|---|---|
| [references/profiling.md](references/profiling.md) | Measuring, hitch type, resmon, profiler, `neteventlog`, verification |
| [references/fivem-networking.md](references/fivem-networking.md) | Events, latent, first-GET cache, msgpack/JSON, routing/`-1`, state bags, callbacks, bandwidth math |
| [references/lua-hotpaths.md](references/lua-hotpaths.md) | Threads, `Wait`, natives, pools, alloc, NUI, `GetPlayers`, SQL load-at-start cache |

Unknown native signature → look it up in a natives reference; do not guess. Validate net IDs and never trust the client. This skill does not cover general scaffolding or OneSync exploit encyclopedias.

---

## Goal

Lower CPU **and** network traffic **and** event spam **and** payload size, with correct sync and unchanged gameplay.

A resource at `0.00ms` that still floods events is not optimized. A quiet net log with a `Wait(0)` pool scan is not optimized.

Do not optimize blindly. Do not invent measurements. Do not weaken server validation to save bytes.

---

## Workflow

1. Identify game (FiveM / RedM / shared) and side (client / server / NUI).
2. Measure, or mark estimates. Open `references/profiling.md`.
3. Grep the checklist below. Classify each hit: CPU, network, or both; Critical / High / Medium / Low.
4. Open the matching reference **before** proposing a fix.
5. Preserve gameplay, sync, routing buckets, permissions, exports, NUI, framework state.
6. Report before/after with **measured** vs **estimated** labeled.

---

## Defaults (always on)

- Longest safe sleep. `Wait(0)` only for true per-frame work.
- Event-driven over polling when the state is observable.
- Smallest valid audience. `-1` only when every client must receive it.
- Send a full payload **once** (join / first GET / resource start), then cache it on the client or server. Later traffic is deltas only.
- Load DB rows at resource start or player join into a server memory cache. Query or write the database only when data actually changed.
- Send deltas, not whole player/inventory blobs, after that first snapshot.
- Net events are msgpack. Extra `json.encode` is CPU (and a fat string if you send it).
- Latent events only for large, non-latency-critical payloads.
- Cache natives for this tick; do not cache values that must stay live.
- After any perf change, server still validates `source`, permissions, amounts, ownership, distance, bucket, cooldowns.
- Capture `local src = source` before yields.

---

## Grep checklist

Search the whole resource, both sides:

- `CreateThread` / `Citizen.CreateThread` / `while true`
- `Wait(0)` / `Wait(1)` / `Wait(5)` / `Wait(10)`
- `TriggerServerEvent` / `TriggerClientEvent` / `TriggerLatent`
- `TriggerClientEvent` with `-1`
- `RegisterNetEvent` / `AddEventHandler` / `TriggerEvent`
- `GetGamePool` / `GetActivePlayers` / `GetPlayers`
- `json.encode` / `json.decode`
- `SendNUIMessage`
- `MySQL` / `oxmysql` / `.query` / `.query.await`
- `GlobalState` / `.state` / `AddStateBagChangeHandler`
- `lib.callback` / `emitNet`

For each event: local vs C→S vs S→C; frequency; payload shape; recipient set; inside a loop or not.

---

## Priority

**Critical** — frame-level `Trigger*Event`, `GetGamePool` every frame, large JSON every tick, `-1` broadcast of fat data.

**High** — frequent loops, unnecessary broadcasts, large payloads, expensive natives, sync SQL in loops.

**Medium** — repeated allocs, redundant math, inefficient table scans.

**Low** — micro-opts resmon will not show.

Do not grind Low while Critical remains.

---

## Before editing

1. Understand architecture, event consumers, client/server boundary.
2. Search the **entire** resource (and dependents) before deleting an event. It may be used from another file or resource.
3. Check exports, callbacks, NUI, framework integrations, state bags.
4. Do not change behavior of inventory, money, permissions, entity ownership, or routing buckets unless the user asked.

If an optimization must change behavior, say so explicitly.

---

## Report format

### Summary

Main bottlenecks in one short paragraph.

### Performance

```text
Before:   (measured | estimate)
After:    (measured | estimate)
Expected: ...
```

### Network

```text
Event:
Frequency:
Payload:
Recipients:
Estimated bandwidth:
```

### Changes

Each important change and why.

### Risks

Sync, gameplay, or validation risks.

### Remaining bottlenecks

What to measure next.

### Verification

How to confirm with resmon / profiler / `neteventlog` (`references/profiling.md`).
