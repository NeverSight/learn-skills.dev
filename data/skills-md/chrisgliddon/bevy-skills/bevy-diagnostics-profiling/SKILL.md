---
name: bevy-diagnostics-profiling
description: "Use when profiling Bevy 0.20 with `DiagnosticPath`, `DiagnosticsStore`, `info_span!`, `RenderDiagnosticsPlugin`, or the `RenderDebugOverlay`: custom metrics, CPU/GPU pass timings, queue/task/upload telemetry, stale-result counts, and native, Steam Deck, or WebGPU budgets."
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "2"
  area: diagnostics
  bevy_version: "0.20"
---

# Bevy 0.20 — diagnostics and profiling

## When to use this skill

- A frame, render pass, worker pipeline, or upload path needs causal evidence.
- A queue/task system needs stable gauges, counters, latency, and high-water marks.
- Performance claims must pass native, Steam Deck, or browser acceptance budgets.
- Render GPU diagnostics are absent or disagree with CPU traces.

Diagnostics answer “what is happening over time?” Tracing answers “where did this
execution spend time?” Render diagnostics expose pass-level renderer measurements.
Use all three, but do not treat any one of them as proof of a bottleneck.

## Canonical pattern

```rust
use bevy::{
    diagnostic::{
        Diagnostic, DiagnosticPath, Diagnostics, RegisterDiagnostic,
    },
    prelude::*,
};

const REMESH_QUEUE_DEPTH: DiagnosticPath =
    DiagnosticPath::const_new("voxel/remesh_queue_depth");

#[derive(Resource, Default)]
struct RemeshQueue {
    valid_jobs: usize,
}

struct VoxelDiagnosticsPlugin;

impl Plugin for VoxelDiagnosticsPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<RemeshQueue>()
            .register_diagnostic(
                Diagnostic::new(REMESH_QUEUE_DEPTH).with_suffix(" sections"),
            )
            .add_systems(Update, record_voxel_diagnostics);
    }
}

fn record_voxel_diagnostics(
    queue: Res<RemeshQueue>,
    mut diagnostics: Diagnostics,
) {
    diagnostics.add_measurement(&REMESH_QUEUE_DEPTH, || queue.valid_jobs as f64);
}
```

Paths are an API: use namespaced, stable names with explicit units in suffixes or
documentation. Register before recording. `DiagnosticsStore` provides latest and
historical/smoothed values for displays and exporters. Measurements are deferred
telemetry, not a same-system synchronisation mechanism.

## Built-in plugins

- `FrameTimeDiagnosticsPlugin`: FPS, frame time, and frame count.
- `EntityCountDiagnosticsPlugin`: live entity count.
- `SystemInformationDiagnosticsPlugin`: process/system CPU and memory on supported
  native targets. It is unavailable/no-op for WASM, iOS, and dynamic-link builds.
- `LogDiagnosticsPlugin`: development output; filter paths and cadence to avoid noise.
- `RenderDiagnosticsPlugin`: CPU/GPU time per recorded render span and pipeline
  statistics where the backend supports them.
- `RenderDebugOverlayPlugin` (0.20): on-screen render debug overlay, in
  `DefaultPlugins` under the `dev` feature (`bevy_dev_tools` + `render_dev_tools`).
  Off until `RenderDebugOverlayKeybindings { enable_keybindings: true, .. }`
  is inserted; F1 cycles mode, F2 cycles opacity.

Add `RenderDiagnosticsPlugin` from `bevy::render::diagnostic`. It creates dynamic
paths shaped like `render/<span>/elapsed_cpu` and, when supported,
`render/<span>/elapsed_gpu` plus invocation/primitive statistics.

## Tracing for causality

Enable a backend in an optimised build:

```text
cargo run --release --features bevy/trace_tracy
cargo run --release --features bevy/trace_chrome
```

`trace_tracy_memory` adds allocation tracking with extra overhead. Add coarse spans
around work whose cause matters:

```rust
use bevy::prelude::*;

fn rebuild_visible_sections() {
    let _span = info_span!("rebuild_visible_sections").entered();
    // measured work
}
```

Avoid high-cardinality span names and per-element spans. Record section/entity IDs as
fields only during targeted captures. Keep a low-overhead diagnostic gauge/counter
for continuous observability and switch on detailed traces for investigation.

## Gotchas and platform truth

- 0.19→0.20: `Render`, `RenderGraph`, and `Core3d` sets order with `chain_weak`.
  A diagnostic-recording render system that relied on an earlier set finishing via
  a channel or atomic needs an explicit `.after(system)`.
- `tracing` is not a direct dependency: write `bevy::log::tracing::field::Empty`.
- Stale output imports `RenderDebugOverlayPlugin` without the `dev` feature; the
  `bevy::dev_tools` module does not exist without `bevy_dev_tools`.

Bevy 0.20 render timestamp queries and pipeline statistics are supported on Vulkan
and DX12. Metal, WebGPU, and WebGL2 expose CPU render timings only through
`RenderDiagnosticsPlugin`. Missing `elapsed_gpu` is an unsupported measurement, not
zero GPU cost. Use vendor/platform GPU profilers where available; RenderDoc is a
graphics debugger, not a performance profiler.

Profile the shipping renderer, resolution, power mode, content, and build profile.
Desktop results do not establish Steam Deck or browser budgets.

## Choose the relevant deep dive

| Problem | Read |
|---|---|
| Metric types, stable paths, diagnostics store, tracing spans | [Diagnostics and tracing](references/diagnostics-and-tracing.md) |
| Render diagnostics, backend limitations, CPU/GPU tool choice | [Render and platform profiling](references/render-and-platform-profiling.md) |
| Acceptance thresholds, replay design, queue/task/upload telemetry | [Budgets and telemetry](references/budgets-and-telemetry.md) |

## Review checklist

- Every number has a type (gauge/counter/histogram), unit, scope, and sampling rule.
- Queue depth excludes obsolete heap entries; latency timestamps use one clock.
- Spans cover queue wait, worker compute, main-thread apply, and render/upload costs.
- Captures are release-like, repeatable, warm, and made on each claimed target.
- Reports include percentiles and worst sustained intervals, not averages alone.
- Unsupported GPU values remain absent and are never converted to zero.
- Instrumentation overhead is measured and disabled/reduced in normal shipping runs.

## See also

- [`bevy-voxel-runtime`](../bevy-voxel-runtime/SKILL.md) — concrete queue, stale-result, and upload metrics.
- [`bevy-rendering`](../bevy-rendering/SKILL.md) — renderer architecture and custom render systems.
- [`bevy-testing`](../bevy-testing/SKILL.md) — deterministic benchmark replays and visual captures.
- [`bevy-migration-0-19-to-0-20`](../bevy-migration-0-19-to-0-20/SKILL.md) — weak ordering and render-world renames.
- [Bevy diagnostics](https://docs.rs/bevy/0.20.1/bevy/diagnostic/index.html)
- [Bevy render diagnostics](https://docs.rs/bevy/0.20.1/bevy/render/diagnostic/index.html)
- [Bevy 0.20 profiling guide](https://github.com/bevyengine/bevy/blob/v0.20.1/docs/profiling.md)
