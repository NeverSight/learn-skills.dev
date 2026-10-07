---
name: roblox-performance
description: Performance diagnosis and optimization - MicroProfiler, Script Profiler, Developer Console, Scene Analysis, Luau heap and memory categories, memory leaks, network/replication cost, rendering and physics cost, streaming, native codegen, Parallel Luau with Actors. Use when a game lags, stutters, drops FPS, crashes on mobile, has high ping, or before optimizing hot code.
---

# Roblox performance

**Measure before optimizing.** Identify whether the bottleneck is server compute, client compute
(CPU/GPU), memory, network, or load time, then use the matching tool.

## Tools

| Tool | Open | Use for |
| --- | --- | --- |
| Developer Console | F9 (in game) | Errors, server/client memory by category, network, script activity. Works in live servers. |
| MicroProfiler | Ctrl+Alt+F6 (⌘⌥F6); Dev Console for server | Per-frame timing; spikes; dump a frame for detail. |
| Script Profiler | Studio / Dev Console | Which functions consume Luau time (sampling). |
| Luau heap snapshots | Dev Console → Memory → Luau Heap | What tables/closures/instances are held and by what (leaks). |
| Scene Analysis | Studio | Script memory, unparented instances (leaks), instance composition, audio/animation memory, triangles. Also `SceneAnalysisService` via Studio MCP. |
| Performance Stats / Debug Stats | Ctrl+Alt+F7 / Shift+Ctrl+F1–F5 | Live CPU/GPU/memory/network overlays. |
| Network Simulation | Studio (Alt+S) | Test with latency, jitter, packet loss. |
| Performance dashboard | Creator Hub | Live aggregate FPS, server heartbeat, memory, crash rates by device. |

Label your own code in the MicroProfiler and memory views:

```luau
--!strict
local RunService = game:GetService("RunService")

debug.setmemorycategory("EnemyAI") -- memory allocated by this thread is attributed to "EnemyAI"

RunService.Heartbeat:Connect(function(_deltaTime)
	debug.profilebegin("EnemyAI.think") -- shows as a labeled bar in the MicroProfiler
	-- ... work ...
	debug.profileend()
end)
```

## Targets

- Client: 60 FPS on mid-range phones (≈16.6 ms/frame); many players are on low-end Android.
- Server: heartbeat near 60 Hz; `Stats` (`workspace:GetRealPhysicsFPS()`, Dev Console Server Stats).
- Memory: mobile clients crash from OOM first. Keep client memory well under ~1–1.5 GB on low-end
  devices; watch `PlaceMemory`, `LuaHeap`, `GraphicsTexture`, `Sounds`, `Animation` categories.

## Most common problems → fixes

| Symptom | Usual cause | Fix |
| --- | --- | --- |
| Memory grows over time | Leaked connections, tables keyed by players/instances, destroyed-but-referenced instances, unparented instances | Disconnect/clean up per player & per character; clear tables on `PlayerRemoving`; use Scene Analysis "unparented instances" and heap snapshots. |
| Server lag with many players | Per-player loops each frame, `while true do task.wait() end` loops, heavy remote handlers, physics of many unanchored parts | Event-driven code, one scheduler loop, throttled think rates, anchor static parts, server-own fewer assemblies. |
| Client FPS drops | Too many parts/draw calls, shadows from many lights, transparency/particles overdraw, per-frame UI updates | Merge/instance meshes, `CastShadow = false` on small parts, fewer shadowed lights, limit particles, update UI on change only. |
| Spikes every N seconds | Autosave/GC bursts, synchronized loops across players, big `Clone()`s | Stagger with random offsets; pool objects; spread work across frames. |
| High ping / rubber banding | Remote spam, large payloads, replicating many property changes | Batch, delta-compress, throttle; tween on clients; see `roblox-networking`. |
| Long join times | Huge place, many unique assets, no streaming | Streaming, SLIM LOD, fewer unique meshes/textures, `ContentProvider:PreloadAsync` only for critical assets. |

## Luau hot paths

- Cache services, instances, and `RaycastParams` outside loops; avoid `FindFirstChild`/`GetDescendants`
  per frame. Replace `GetDescendants` scans with tags (`CollectionService`) or maintained sets.
- Use `deltaTime` from `Heartbeat`/`PreSimulation` rather than `task.wait()` loops for per-frame work.
- Avoid creating closures/tables per frame in hot loops; reuse buffers with `table.clear`.
- `--!native` (whole script) or `@native` (per function) for math-heavy code; typed parameters help
  the native compiler. Don't blanket-enable: compile time and a global native-code memory limit.
- `--!optimize 2` is how Roblox compiles live games already; don't rely on Studio timings for micro-benchmarks.

## Rendering and assets

- Parts: fewer, larger parts; `MeshPart`s with shared `MeshId` are instanced (cheap); unions (`PartOperation`)
  can be expensive — check triangle counts in Scene Analysis.
- `RenderFidelity = Automatic`/`Performance` for detailed meshes; `CollisionFidelity = Box`/`Hull` for
  decorative meshes; `CanCollide/CanQuery/CanTouch = false` for pure decoration.
- Lights: limit shadow-casting `PointLight`/`SpotLight`/`SurfaceLight`; limit `ParticleEmitter.Rate`
  and particle size (overdraw); `Beam`/`Trail` counts.
- Textures/images: reuse, keep resolutions reasonable (1024² max for most); `SurfaceAppearance` sparingly.
- Enable streaming (`roblox-architecture`), `Model.LevelOfDetail = SLIM` for static models, and let
  `StreamOutBehavior = Opportunistic` free memory.

## Physics

- Anchor everything that doesn't need to move. Welded decorative parts on moving assemblies add cost.
- Fewer, simpler collisions (`CollisionFidelity`, collision groups to skip pairs); `CanTouch = false`
  where `Touched` isn't needed.
- Avoid setting `CFrame` of unanchored parts every frame; use constraints or anchor + CFrame.
- `workspace:BulkMoveTo(parts, cframes, Enum.BulkMoveMode.FireCFrameChanged)` to move many anchored parts.
- Adaptive timestepping (`PhysicsSteppingMethod = Adaptive`) reduces physics CPU.

## Parallel Luau

Scripts under different `Actor` instances can run in parallel:

```luau
--!strict
-- Script parented under an Actor (one Actor per logical unit, e.g. per NPC group or chunk).
local RunService = game:GetService("RunService")

local results: { number } = {}

RunService.Heartbeat:ConnectParallel(function(_deltaTime)
	-- Parallel phase: read-only access to most instances, pure computation, thread-safe APIs (raycasts).
	for i = 1, 100 do
		results[i] = math.noise(i / 10, os.clock())
	end
	task.synchronize()
	-- Serial phase: write to instances, fire events, call thread-unsafe APIs.
end)
```

- `task.desynchronize()` / `task.synchronize()` switch phases; `ConnectParallel` starts in parallel.
- Scripts in the **same** Actor run serially relative to each other: split work across many Actors.
- Can't `require` or modify most instances while desynchronized. Communicate with `Actor:SendMessage` /
  `BindToMessageParallel` or `SharedTable` (`SharedTableRegistry`).
- Good fits: raycast validation, procedural generation, pathfinding-adjacent math, large simulations.
  Bad fits: tiny tasks (sync overhead), instance-heavy work.

Profiling walkthrough and memory-leak hunting: [references/profiling.md](references/profiling.md).

## Related skills

`roblox-architecture` (streaming), `roblox-networking` (bandwidth), `roblox-physics`, `roblox-npc-ai`,
`roblox-studio-mcp` (Roblox's `rbx-perf-profiling`/scene analysis via MCP).
