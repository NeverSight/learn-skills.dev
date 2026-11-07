---
name: bevy-performance
description: "Bevy ECS skill for runtime cost. Keywords: Bevy, parallel systems, chain, FrameTimeDiagnosticsPlugin, Handles."
---

# Bevy performance

## When to use

Load this when a system is slow or assets stay in memory. Pair it with `bevy-debugging-profiling` for the counters.

## ECS shape

- **Systems:** the ECS page says systems run in parallel when they can. `.chain()` forces order and removes that parallelism for the chained set. Put `.chain()` only on the systems that must see each other's writes.
- **Fixed step:** movement and other gameplay that should not follow the render frame belong on `Fixed` / `FixedMain` (`bevy::time`), not on every `Update`.
- **Measures:** `FrameTimeDiagnosticsPlugin` records frame time, fps, and frame count. `EntityCountDiagnosticsPlugin` records entity count. `SystemInformationDiagnosticsPlugin` records process `cpu_usage` and `mem_usage`. `LogDiagnosticsPlugin` prints them. No target milliseconds are stated on those pages.
- **Memory:** `Handle` is reference counted. A strong handle kept in a long-lived `Resource` keeps the asset. The last strong drop removes it from `Assets<T>`. `Assets::add` does not deduplicate procedural assets. `AssetServer::load` reuses a handle while one remains.
- **Schedule:** diagnostics plugins are added on the `App` after `DefaultPlugins`. Do not invent a budget resource.

## Scope

Chain only the systems that share a mutable query. Read frame diagnostics from `DiagnosticsStore`. Keep a strong `Handle` in a resource only while the asset must stay loaded. `Changed<T>` skips entities whose component did not change this tick.

## Examples

```toml
[package]
name = "performance"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.20"
```

Damage writes health. The death system is chained after it so it observes the same tick. Movement does not share that query, so it stays outside the chain.

```rust
#[derive(Component)]
struct Health(f32);

#[derive(Component)]
struct Velocity(Vec3);

fn apply_damage(mut query: Query<&mut Health>) {
    for mut health in &mut query {
        health.0 = (health.0 - 1.0).max(0.0);
    }
}

fn reap(mut commands: Commands, query: Query<(Entity, &Health)>) {
    for (entity, health) in &query {
        if health.0 <= 0.0 {
            commands.entity(entity).despawn();
        }
    }
}

fn integrate(time: Res<Time<Fixed>>, mut query: Query<(&Velocity, &mut Transform)>) {
    let dt = time.delta_secs();
    for (velocity, mut transform) in &mut query {
        transform.translation += velocity.0 * dt;
    }
}

pub struct SimPlugin;

impl Plugin for SimPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(FixedUpdate, (apply_damage, reap).chain())
            .add_systems(FixedUpdate, integrate);
    }
}
```

Frame diagnostics record fps. A strong mesh handle in a resource keeps that mesh loaded until the resource is dropped.

```rust
use bevy::diagnostic::{DiagnosticsStore, FrameTimeDiagnosticsPlugin, LogDiagnosticsPlugin};

#[derive(Resource)]
struct KeptMesh(Handle<Mesh>);

fn spawn_kept_mesh(mut commands: Commands, mut meshes: ResMut<Assets<Mesh>>) {
    let handle = meshes.add(Mesh::from(Cuboid::new(1.0, 1.0, 1.0)));
    commands.insert_resource(KeptMesh(handle));
}

fn read_fps(diagnostics: Res<DiagnosticsStore>) {
    let Some(fps) = diagnostics.get(&FrameTimeDiagnosticsPlugin::FPS) else {
        return;
    };
    let _value = fps.smoothed();
}

pub struct MeasurePlugin;

impl Plugin for MeasurePlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins((
            FrameTimeDiagnosticsPlugin::default(),
            LogDiagnosticsPlugin::default(),
        ))
        .add_systems(Startup, spawn_kept_mesh)
        .add_systems(Update, read_fps);
    }
}
```

Anchors that moved this tick are the only transforms the follower reads. `Changed<Transform>` leaves the rest of the query idle.

```rust
#[derive(Component)]
struct Marker;

#[derive(Component)]
struct Anchor;

fn follow_changed(
    movers: Query<&Transform, (With<Anchor>, Changed<Transform>)>,
    mut markers: Query<&mut Transform, (With<Marker>, Without<Anchor>)>,
) {
    let Some(source) = movers.iter().next() else {
        return;
    };
    let translation = source.translation;
    for mut marker in &mut markers {
        marker.translation = translation;
    }
}
```

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
| Per-entity data | `Component` + `Query` | A Godot node script |
| App-wide config or clock | `Resource` | Copy the value onto every entity |
| Stable simulation step | `FixedMain` and the `Fixed` clock | Tie simulation to raw frame `Update` |
| Startup spawn | `Commands` in `Startup` | Spawn from a render system |
| Cross-system notice that is not shared state | Message or observer slot in `bevy-events-messaging` | A new event type invented in this file |
| An API outside the documented set | Check the official docs first | A made-up crate or API |

Load [references/ecs-ownership.md](references/ecs-ownership.md) for the ownership table.

## NEVER

- Do not pin `/0.20.0/` in docs URLs. WHY: links stay on `latest`; the 0.20 target is stated once in prose.
- Do not mutably query the same component from two unordered systems. WHY: the schedule runs systems in parallel unless `.chain()` orders them.
- Do not invent a physics, navigation, networking, or XR crate here. WHY: this skill only names documented Bevy crates and modules.

- No Godot servers, visibility notifiers, or profiler monitors. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No culling or batching API this file did not open. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No third-party profiler crates. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Official pages stay on the unversioned `latest` branch.

### Official Documentation
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/)  -  Parallel systems and `.chain()`.
- [Time examples](https://github.com/bevyengine/bevy/tree/latest/examples/time)  -  `Fixed` and `FixedMain`.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples)  -  Example tree on the `latest` branch.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Who owns which piece of state.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md)  -  Systems and `.chain()`.
- [bevy-debugging-profiling](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-debugging-profiling/SKILL.md)  -  How those diagnostics are plugged in.

#### Complements
- [bevy-asset-scenes](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-asset-scenes/SKILL.md)  -  When handles are loaded and dropped.
- [bevy-character-movement](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-character-movement/SKILL.md)  -  Work that belongs on the fixed timestep.
- [godot-performance-optimization](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-performance-optimization/SKILL.md)  -  Performance on the Godot engine, same depth.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Bevy router.
