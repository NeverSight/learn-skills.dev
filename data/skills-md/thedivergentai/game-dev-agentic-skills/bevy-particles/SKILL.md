---
name: bevy-particles
description: "Bevy ECS skill for particle effects. Use when spawning a one-shot burst or a trail of sprite motes with life and velocity. Keywords: Bevy, particles, burst, trail, Sprite, ECS."
---

# Bevy particles

## When to use

Load this before adding a burst, trail, or GPU particle effect. Particle effects are yours to build in ECS. Do not invent a particle plugin.

## ECS shape

- **Components** own each mote (`Particle`) and each emitter (`Emitter`). A `Sprite` is the visible quad.
- **Resources:** none. Burst origin and rate live on the emitter entity.
- **Systems:** one system spawns motes, one integrates them and despawns the dead.
- **Schedule:** both run on `FixedUpdate`, chained so a mote spawned this step is integrated next step.

## Coming from Godot

| Godot idea | Bevy idiom |
| --- | --- |
| CPU particles | Entities with `Particle`, `Sprite`, and `Transform` |
| GPU particles | The same entities, drawn by the sprite pipeline |
| One-shot burst | Spawn a fixed count, then despawn when `life` hits zero |

## Scope

Bevy ships no particle module. A burst is a spawn loop over `Sprite` entities. A trail is an emitter component that spends a rate accumulator.

## Examples

```toml
[package]
name = "particles"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.20"
rand = "0.9"
```

A one-shot burst scatters sprites. Each mote stores velocity and remaining life.

```rust
use rand::Rng;

#[derive(Component)]
struct Particle {
    velocity: Vec2,
    life: f32,
}

fn burst(mut commands: Commands) {
    let mut rng = rand::rng();
    for _ in 0..24 {
        let angle = rng.random_range(0.0..std::f32::consts::TAU);
        let speed = rng.random_range(1.0..4.0);
        commands.spawn((
            Particle {
                velocity: Vec2::new(angle.cos(), angle.sin()) * speed,
                life: rng.random_range(0.3..0.8),
            },
            Sprite {
                color: Color::srgba(1.0, 0.45, 0.1, 1.0),
                custom_size: Some(Vec2::splat(6.0)),
                ..default()
            },
            Transform::from_xyz(0.0, 0.0, 0.0),
        ));
    }
}
```

Integration writes `Transform` and despawns when life expires. Gravity is a constant acceleration on Y.

```rust
#[derive(Component)]
struct Particle {
    velocity: Vec2,
    life: f32,
}

fn simulate(
    time: Res<Time<Fixed>>,
    mut commands: Commands,
    mut motes: Query<(Entity, &mut Transform, &mut Particle, &mut Sprite)>,
) {
    let dt = time.delta_secs();
    for (entity, mut transform, mut particle, mut sprite) in &mut motes {
        particle.life -= dt;
        if particle.life <= 0.0 {
            commands.entity(entity).despawn();
            continue;
        }
        particle.velocity.y -= 6.0 * dt;
        transform.translation.x += particle.velocity.x * dt;
        transform.translation.y += particle.velocity.y * dt;
        sprite.color.set_alpha(particle.life.clamp(0.0, 1.0));
    }
}
```

An emitter on a moving entity spends `accumulator` and spawns motes at its translation. That is a trail.

```rust
use rand::Rng;

#[derive(Component)]
struct Emitter {
    rate: f32,
    accumulator: f32,
}

#[derive(Component)]
struct Particle {
    velocity: Vec2,
    life: f32,
}

fn emit(
    time: Res<Time<Fixed>>,
    mut commands: Commands,
    mut emitters: Query<(&Transform, &mut Emitter)>,
) {
    let dt = time.delta_secs();
    let mut rng = rand::rng();
    for (transform, mut emitter) in &mut emitters {
        emitter.accumulator += emitter.rate * dt;
        while emitter.accumulator >= 1.0 {
            emitter.accumulator -= 1.0;
            commands.spawn((
                Particle {
                    velocity: Vec2::new(rng.random_range(-0.4..0.4), rng.random_range(0.2..1.0)),
                    life: 0.6,
                },
                Sprite {
                    color: Color::srgba(0.7, 0.7, 0.7, 0.8),
                    custom_size: Some(Vec2::splat(4.0)),
                    ..default()
                },
                Transform::from_translation(transform.translation),
            ));
        }
    }
}

fn simulate(
    time: Res<Time<Fixed>>,
    mut commands: Commands,
    mut motes: Query<(Entity, &mut Transform, &mut Particle, &mut Sprite)>,
) {
    let dt = time.delta_secs();
    for (entity, mut transform, mut particle, mut sprite) in &mut motes {
        particle.life -= dt;
        if particle.life <= 0.0 {
            commands.entity(entity).despawn();
            continue;
        }
        particle.velocity.y -= 6.0 * dt;
        transform.translation.x += particle.velocity.x * dt;
        transform.translation.y += particle.velocity.y * dt;
        sprite.color.set_alpha(particle.life.clamp(0.0, 1.0));
    }
}

pub struct ParticlePlugin;

impl Plugin for ParticlePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(FixedUpdate, (emit, simulate).chain());
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

- No Godot particle node types. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No named particle crate as the chosen solution. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

- No Godot types in Bevy code. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference


### Official Documentation
- `bevy crate` - API reference and Cargo feature list.
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.

#### Complements
- [bevy-shaders](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-shaders/SKILL.md) - Materials are not a particle system.
- [godot-particles](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-particles/SKILL.md) - Equivalent Godot skill.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
