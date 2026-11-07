---
name: bevy-debugging-profiling
description: "Bevy ECS skill for logs and diagnostics. Keywords: Bevy, LogPlugin, DiagnosticsPlugin, FrameTimeDiagnosticsPlugin."
---

# Bevy debugging and profiling

## When to use

Load this when a running app should print logs or record frame time, entity count, or process CPU and memory.

## ECS shape

- **Logs:** `LogPlugin` is part of `DefaultPlugins`. Override it with `DefaultPlugins.set(LogPlugin { level, filter, .. })`. The page's example uses `Level::DEBUG` and a filter string such as `wgpu=error,bevy_render=info,bevy_ecs=trace`. The same filter works as `RUST_LOG`. To bring your own collector, disable this plugin on `DefaultPlugins`.
- **Diagnostics core:** `DiagnosticsPlugin` adds the core resources. `DiagnosticsStore` holds the collection. `Diagnostic` is a timeline of `DiagnosticMeasurement` values addressed by `DiagnosticPath`. `RegisterDiagnostic` adds `register_diagnostic` on `App`.
- **Built-in plugins:** `FrameTimeDiagnosticsPlugin` adds frame time, fps, and frame count. `EntityCountDiagnosticsPlugin` adds an entity count. `SystemInformationDiagnosticsPlugin` adds `cpu_usage` and `mem_usage` percent. `LogDiagnosticsPlugin` prints diagnostics to the console. `FrameCount` / `FrameCountPlugin` count frames since start.
- **Order:** the log-diagnostics example adds these plugins after `DefaultPlugins` because they use the time plugin for timestamps.
- **Schedule:** built-in plugins measure on their own. Read `DiagnosticsStore` when a HUD needs the latest sample. Register a `Diagnostic` only for a value you measure yourself.

## Examples

```toml
[dependencies]
bevy = "0.20"
```

`LogPlugin` ships inside `DefaultPlugins`. Replace its level and filter when the default `info` stream is too quiet or too loud.

```rust
use bevy::log::{Level, LogPlugin};

fn main() {
    App::new()
        .add_plugins(DefaultPlugins.set(LogPlugin {
            filter: "wgpu=error,bevy_render=info,bevy_ecs=trace".into(),
            level: Level::DEBUG,
            ..default()
        }))
        .run();
}
```

Frame time, entity count, process CPU and memory, and a console dump are four plugins. Add them after `DefaultPlugins` so timestamps exist.

```rust
use bevy::diagnostic::{
    EntityCountDiagnosticsPlugin, FrameTimeDiagnosticsPlugin, LogDiagnosticsPlugin,
    SystemInformationDiagnosticsPlugin,
};

fn main() {
    App::new()
        .add_plugins((
            DefaultPlugins,
            FrameTimeDiagnosticsPlugin::default(),
            EntityCountDiagnosticsPlugin {
                max_history_length: 60,
            },
            SystemInformationDiagnosticsPlugin,
            LogDiagnosticsPlugin::default(),
        ))
        .run();
}
```

A HUD reads the smoothed frame-time sample from the store. The path constants live on the plugin that recorded them.

```rust
use bevy::diagnostic::{DiagnosticsStore, FrameTimeDiagnosticsPlugin};

fn read_frame_time(store: Res<DiagnosticsStore>) {
    let Some(frame) = store.get(&FrameTimeDiagnosticsPlugin::FRAME_TIME) else {
        return;
    };
    let Some(ms) = frame.smoothed() else {
        return;
    };
    info!("frame {ms:.2} ms");
}
```

A custom counter is a `DiagnosticPath` plus `register_diagnostic`. One system writes the measurement; nothing else mutates that path.

```rust
use bevy::diagnostic::{Diagnostic, DiagnosticPath, Diagnostics, RegisterDiagnostic};

const LIVE_ENEMIES: DiagnosticPath = DiagnosticPath::const_new("game/live_enemies");

#[derive(Component)]
struct Enemy;

fn install(app: &mut App) {
    app.register_diagnostic(Diagnostic::new(LIVE_ENEMIES).with_max_history_length(60));
}

fn measure_enemies(mut diagnostics: Diagnostics, enemies: Query<(), With<Enemy>>) {
    let count = enemies.iter().count() as f64;
    diagnostics.add_measurement(&LIVE_ENEMIES, || count);
}
```

## Scope

- Per-system flame graphs and Tracy stay outside this skill. `LogPlugin` covers level and filter.
- Custom measurements use `Diagnostic`, `DiagnosticPath`, and `register_diagnostic` as in the example above.
- This skill does not forward diagnostics into the render app.

## Expert Knowledge Delta

Target: **Bevy 0.20+**.

Core ECS types: `Component`, `Resource`, `Query`, `Commands`, `Startup`, `Update`, `Fixed` / `FixedMain` (`bevy::time`), `.chain()`, `Plugin`, `DefaultPlugins`, `MinimalPlugins`. Messages and observers are an ownership slot. See `bevy-events-messaging` for their APIs. Systems run in parallel unless `.chain()` orders the ones that conflict.

### Who owns state

| Piece | Owner | Who may mutate | Schedule |
| --- | --- | --- | --- |
| Data on one entity | `Component` | One system via `Query` | `Update` or `FixedMain` |
| One value for the whole app | `Resource` | One system | `Startup` to insert, then the schedule that reads it |
| Spawn | `Commands` | The spawning system | `Startup` for the initial world; later schedules for runtime spawn |
| Order that must not race | `.chain()` | The chained systems only | Same schedule |
| Plugin boundary | `Plugin` | `build` registers systems and resources | Before the app runs |

Borrow rule: two systems that both mutably query the same component must be ordered (`.chain()`) or split so only one writes. Unrelated systems stay parallel. That is the ECS page rule, not a guess at a system-set API.

### Decision

| If you need | Do this | Do not |
| --- | --- | --- |
| Per-entity data | `Component` + `Query` | One mutable blob shared by every entity |
| App-wide config or clock | `Resource` | Copy the value onto every entity |
| Stable simulation step | `FixedMain` and the `Fixed` clock | Tie simulation to raw frame `Update` |
| Startup spawn | `Commands` in `Startup` | Spawn from a render system |
| Cross-system notice that is not shared state | Message or observer slot in `bevy-events-messaging` | A new event type invented in this file |
| An API outside the documented set | Read the official Bevy pages | A made-up crate or API |

Load [references/ecs-ownership.md](references/ecs-ownership.md) for the ownership table.

## NEVER

- Do not pin `/0.20.0/` in docs URLs. WHY: links stay on `latest`; the 0.20 target is stated once in prose.
- Do not mutably query the same component from two unordered systems. WHY: the schedule runs systems in parallel unless `.chain()` orders them.
- Do not invent a physics, navigation, networking, or XR crate here. WHY: this skill only names documented Bevy crates and modules.

- No Tracy or external profiler setup this file did not open. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No third-party profiling crates. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Official pages stay on the unversioned site.

### Official Documentation
- [Log diagnostics example](https://github.com/bevyengine/bevy/blob/latest/examples/diagnostics/log_diagnostics.rs)  -  `LogPlugin`, frame time, entity count, system info, and the log dump.
- [Custom diagnostic example](https://github.com/bevyengine/bevy/blob/latest/examples/diagnostics/custom_diagnostic.rs)  -  `DiagnosticPath`, `register_diagnostic`, and `Diagnostics`.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples)  -  Example tree on the `latest` branch.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Who owns which piece of state.
- [bevy-project-foundations](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-project-foundations/SKILL.md)  -  `DefaultPlugins` and `App`.

#### Complements
- [bevy-performance](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-performance/SKILL.md)  -  What the frame-time numbers are for.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Bevy router.
