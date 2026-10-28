---
name: bevy-genre-stealth
description: "Thin Bevy genre router for Stealth. Keywords: Bevy, Stealth, genre, ECS, router."
---

# Bevy Stealth (thin router)

Genre router. Domain work lives in the Bevy skills below.

## When to use

Load this for vision cones you author and alert states.

## ECS shape

- **Components** hold the genre's per-entity flags as plain data. This file does not name new engine types.
- **Resources** hold run-wide counters (score, wave index, seed) via bevy-data-resources.
- **Systems** read those components on `Update` or the fixed timestep from bevy-master. Order them with `.chain()` when a later system must see the result.
- **Schedule:** gameplay mode changes go through bevy-state-machines. Do not invent a genre plugin.

## Coming from Godot

| Godot idea | Bevy idiom |
| --- | --- |
| Genre scene tree | Entities plus the domain skills linked below |
| Autoload director | A resource, not a singleton node |
| Signal bus for the loop | bevy-events-messaging |

## Routing

- [bevy-ai-navigation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ai-navigation/SKILL.md) - Patrol.
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Alert enum on the agent.
- [bevy-3d-lighting](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-3d-lighting/SKILL.md) - Readability of darkness.
- [bevy-spatial-queries](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-spatial-queries/SKILL.md) - Line of sight.

## Scope

Vision cones, exposure, and alert meters are components you own. A ray that must stop on solid geometry belongs on bevy-spatial-queries. Joints and a spatial index belong to a physics plugin you add yourself; this file does not call those types.

## Examples

```toml
[dependencies]
bevy = "0.20"
```

A guard samples the player's head, torso, and feet. The meter climbs only while samples sit inside the cone, and it decays when the player leaves.

```rust
#[derive(Component)]
struct Player;

#[derive(Component)]
struct Vision {
    range: f32,
    half_angle_cos: f32,
    eye_offset: Vec3,
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum AlertState {
    Idle,
    Suspicious,
    Alerted,
}

#[derive(Component)]
struct Alert {
    meter: f32,
    state: AlertState,
}

fn in_cone(eye: Vec3, forward: Vec3, target: Vec3, vision: &Vision) -> bool {
    let to = target - eye;
    let dist = to.length();
    if dist > vision.range || dist < 0.001 {
        return false;
    }
    (to / dist).dot(forward) >= vision.half_angle_cos
}

fn raise_alert(
    time: Res<Time>,
    players: Query<&Transform, With<Player>>,
    mut guards: Query<(&Transform, &Vision, &mut Alert)>,
) {
    let Some(player_tf) = players.iter().next() else {
        return;
    };
    let dt = time.delta_secs();
    let samples = [
        player_tf.translation + Vec3::Y * 1.6,
        player_tf.translation + Vec3::Y * 0.9,
        player_tf.translation + Vec3::Y * 0.2,
    ];
    for (tf, vision, mut alert) in &mut guards {
        let eye = tf.translation + vision.eye_offset;
        let forward = tf.forward().as_vec3();
        let hits = samples
            .iter()
            .filter(|point| in_cone(eye, forward, **point, vision))
            .count();
        let rate = hits as f32 / samples.len() as f32;
        if rate > 0.0 {
            alert.meter = (alert.meter + rate * 40.0 * dt).min(100.0);
        } else {
            alert.meter = (alert.meter - 15.0 * dt).max(0.0);
        }
        alert.state = if alert.meter >= 100.0 {
            AlertState::Alerted
        } else if alert.meter >= 25.0 {
            AlertState::Suspicious
        } else {
            AlertState::Idle
        };
    }
}
```

Hearing uses travel distance, not a raw radius. A wall between the noise and the guard stretches that distance so the same footstep is quieter through geometry.

```rust
#[derive(Component)]
struct Hearing {
    range: f32,
}

#[derive(Component)]
struct Noise {
    loudness: f32,
}

#[derive(Component)]
struct Alert {
    meter: f32,
}

fn hear(
    time: Res<Time>,
    noises: Query<(&Transform, &Noise)>,
    mut guards: Query<(&Transform, &Hearing, &mut Alert)>,
) {
    let dt = time.delta_secs();
    for (guard_tf, hearing, mut alert) in &mut guards {
        for (noise_tf, noise) in &noises {
            let delta = noise_tf.translation - guard_tf.translation;
            let straight = delta.length();
            let blocked = delta.x.abs() > 2.0 && delta.z.abs() > 2.0;
            let travel = if blocked { straight * 2.5 } else { straight };
            if travel < hearing.range {
                let gain = noise.loudness * (1.0 - travel / hearing.range);
                alert.meter = (alert.meter + gain * dt).min(100.0);
            }
        }
    }
}

pub struct HearingPlugin;

impl Plugin for HearingPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Update, hear);
    }
}
```

Light scales how fast the meter fills. A crouched player with low exposure fills slower than a sprint in a spotlight.

```rust
#[derive(Component)]
struct Exposure {
    light: f32,
    speed: f32,
}

fn exposure_rate(exposure: &Exposure) -> f32 {
    let light = exposure.light.clamp(0.0, 1.0);
    let speed = (exposure.speed / 6.0).clamp(0.0, 1.5);
    0.15 + light * 0.7 + speed * 0.15
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum AlertState {
    Idle,
    Suspicious,
    Alerted,
}

#[derive(Component)]
struct Vision {
    range: f32,
    half_angle_cos: f32,
    eye_offset: Vec3,
}

#[derive(Component)]
struct Alert {
    meter: f32,
    state: AlertState,
}

#[derive(Component)]
struct Hearing {
    range: f32,
}

fn spawn_guard(mut commands: Commands) {
    commands.spawn((
        Transform::from_xyz(4.0, 0.0, 0.0),
        Vision {
            range: 12.0,
            half_angle_cos: 0.5,
            eye_offset: Vec3::Y * 1.6,
        },
        Alert {
            meter: 0.0,
            state: AlertState::Idle,
        },
        Hearing { range: 8.0 },
    ));
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

- No Godot types in Bevy code. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented genre APIs. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- Do not pick a physics or net crate here. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**.

### Official Documentation
- `bevy crate` - API reference and Cargo feature list.
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - ECS ownership and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Spawn and query shape.

#### Complements
- [godot-genre-stealth](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-genre-stealth/SKILL.md) - Equivalent Godot skill.
- [bevy-ai-navigation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ai-navigation/SKILL.md) - Patrol.
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Alert enum on the agent.
- [bevy-3d-lighting](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-3d-lighting/SKILL.md) - Readability of darkness.
- [bevy-spatial-queries](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-spatial-queries/SKILL.md) - Line of sight.

#### Downstream / consumers
- None. This router does not own a second implementation.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
