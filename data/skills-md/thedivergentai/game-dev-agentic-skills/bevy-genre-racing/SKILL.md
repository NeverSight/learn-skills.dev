---
name: bevy-genre-racing
description: "Route a Bevy 0.20 race. Use when lap and gate index live on the racer, the race clock is one resource, and gate checks run after the clock step in one chain. Keywords: Bevy, Racing, Racer, RaceClock, FixedUpdate, chain, genre."
---

# Bevy Racing (thin router)

Genre router. Domain work lives in the Bevy skills below.

## When to use

Load this for laps, splits, and vehicle motion you own.

## ECS shape

- **Components** hold the genre's per-entity flags as plain data. This file does not name new engine types.
- **Resources** hold run-wide counters (score, wave index, seed) via bevy-data-resources.
- **Systems** read those components on `Update` or the fixed timestep from bevy-master. Order them with `.chain()` when a later system must see the result.
- **Schedule:** gameplay mode changes go through bevy-state-machines. Do not invent a genre plugin.

## Routing

- [bevy-game-loop-time-trial](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-game-loop-time-trial/SKILL.md) - Splits.
- [bevy-character-movement](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-character-movement/SKILL.md) - Stand-in motion until a vehicle solver exists.
- [bevy-3d-world-building](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-3d-world-building/SKILL.md) - Track.

## Scope

Lap index, gate order, and a kinematic vehicle are components. A rigid-body vehicle solver stays on the physics skill once one is chosen.

## Examples

```toml
[package]
name = "racing"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.20"
```

Gates are entities. The racer stores the next gate index and the lap count. Crossing the last gate increments the lap and records the clock.

```rust
#[derive(Component)]
struct Racer {
    lap: u32,
    next_gate: u32,
    gate_count: u32,
}

#[derive(Component)]
struct Gate {
    index: u32,
}

#[derive(Resource)]
struct RaceClock {
    elapsed: f32,
    best_lap: f32,
    lap_start: f32,
}

fn tick_clock(time: Res<Time<Fixed>>, mut clock: ResMut<RaceClock>) {
    clock.elapsed += time.delta_secs();
}

fn cross_gates(
    mut racers: Query<(&Transform, &mut Racer)>,
    gates: Query<(&Transform, &Gate)>,
    mut clock: ResMut<RaceClock>,
) {
    for (transform, mut racer) in &mut racers {
        for (gate_tf, gate) in &gates {
            if gate.index != racer.next_gate {
                continue;
            }
            if transform.translation.distance(gate_tf.translation) > 6.0 {
                continue;
            }
            let last = racer.gate_count.saturating_sub(1);
            if gate.index == last {
                let lap_time = clock.elapsed - clock.lap_start;
                if racer.lap == 0 || lap_time < clock.best_lap {
                    clock.best_lap = lap_time;
                }
                clock.lap_start = clock.elapsed;
                racer.lap += 1;
                racer.next_gate = 0;
            } else {
                racer.next_gate += 1;
            }
        }
    }
}

pub struct RacePlugin;

impl Plugin for RacePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(RaceClock {
            elapsed: 0.0,
            best_lap: f32::MAX,
            lap_start: 0.0,
        })
        .add_systems(FixedUpdate, (tick_clock, cross_gates).chain());
    }
}
```

Heading and speed live on the vehicle. Input changes them; one system writes `Transform`.

```rust
#[derive(Component)]
struct Vehicle {
    speed: f32,
    heading: f32,
}

fn drive(
    time: Res<Time<Fixed>>,
    keys: Res<ButtonInput<KeyCode>>,
    mut vehicles: Query<(&mut Transform, &mut Vehicle)>,
) {
    let dt = time.delta_secs();
    for (mut transform, mut vehicle) in &mut vehicles {
        if keys.pressed(KeyCode::KeyA) {
            vehicle.heading += dt * 1.5;
        }
        if keys.pressed(KeyCode::KeyD) {
            vehicle.heading -= dt * 1.5;
        }
        if keys.pressed(KeyCode::KeyW) {
            vehicle.speed = (vehicle.speed + dt * 12.0).min(40.0);
        } else {
            vehicle.speed = (vehicle.speed - dt * 8.0).max(0.0);
        }
        let forward = Vec3::new(vehicle.heading.sin(), 0.0, vehicle.heading.cos());
        transform.translation += forward * vehicle.speed * dt;
    }
}
```

Startup places the car and three gates along Z.

```rust
#[derive(Component)]
struct Racer {
    lap: u32,
    next_gate: u32,
    gate_count: u32,
}

#[derive(Component)]
struct Gate {
    index: u32,
}

#[derive(Component)]
struct Vehicle {
    speed: f32,
    heading: f32,
}

fn spawn_track(mut commands: Commands) {
    commands.spawn((
        Racer {
            lap: 0,
            next_gate: 0,
            gate_count: 3,
        },
        Vehicle {
            speed: 0.0,
            heading: 0.0,
        },
        Transform::from_xyz(0.0, 0.0, 0.0),
    ));
    for index in 0..3 {
        commands.spawn((
            Gate { index },
            Transform::from_xyz(0.0, 0.0, 20.0 + index as f32 * 30.0),
        ));
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
| Per-entity data | `Component` + `Query` | A scene-tree script |
| App-wide config or clock | `Resource` | Copy the value onto every entity |
| Stable simulation step | `FixedMain` and the `Fixed` clock | Tie simulation to raw frame `Update` |
| Startup spawn | `Commands` in `Startup` | Spawn from a render system |
| Cross-system notice that is not shared state | Message or observer slot in `bevy-events-messaging` | A new event type invented in this file |
| Lap and split timing | `Racer` plus a `RaceClock` resource stepped on `FixedUpdate` | A lap type invented as an engine singleton |

Load [references/ecs-ownership.md](references/ecs-ownership.md) for the ownership table.

## NEVER

- Do not pin `/0.20.0/` in docs URLs. WHY: links stay on `latest`; the 0.20 target is stated once in prose.
- Do not mutably query the same component from two unordered systems. WHY: the schedule runs systems in parallel unless `.chain()` orders them.
- Do not invent a physics, navigation, networking, or XR crate here. WHY: this skill only names documented Bevy crates and modules.

- No scene-tree types in Bevy code. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented genre APIs. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- Do not pick a physics or net crate here. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Official links stay on the unversioned learn pages.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - ECS ownership and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Spawn and query shape.

#### Complements
- [bevy-game-loop-time-trial](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-game-loop-time-trial/SKILL.md) - Splits.
- [bevy-character-movement](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-character-movement/SKILL.md) - Stand-in motion until a vehicle solver exists.
- [bevy-3d-world-building](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-3d-world-building/SKILL.md) - Track.

#### Downstream / consumers
- None. This router does not own a second implementation.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
