---
name: bevy-physics-3d
description: "Bevy ECS skill for 3D physics. Keywords: Bevy, physics, ECS, 3D."
---

# Bevy 3D physics

## When to use

Load this when a Bevy app needs simulated 3D bodies (props, impulses, constraints) before choosing a solver. Pair with bevy-character-movement for player motion that should not be a rigid body.

## ECS shape

- **Components** own velocity, mass, and a sphere radius for props you simulate yourself.
- **Resources** own gravity.
- **Systems** integrate on `FixedUpdate`, then separate overlapping spheres. `.chain()` runs separation after the step.
- **Schedule:** the fixed step is the clock. A separate solver plugin can replace the integrator when you need joints and a broadphase. This file does not name that plugin's types. Player locomotion stays on bevy-character-movement.

## Ownership

| Need | Bevy shape |
| --- | --- |
| Simulated prop | `Body` plus `Transform`, integrated on `FixedUpdate` |
| Player locomotion | bevy-character-movement, not this integrator |
| Joints and ragdolls | A separate solver plugin once those features are required. This file does not name that plugin's types |
| Layers and masks | A `Layer` component you define, filtered in the overlap system |

## Scope

- Gravity, velocity, and sphere overlap are ordinary components stepped on `FixedUpdate`.
- Joints, ragdolls, and continuous collision belong to a physics solver you add as a plugin. This skill does not call that plugin's types.

## Examples

```toml
[package]
name = "physics3d"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.20"
```

Integrate velocity under gravity, then push overlapping spheres apart. Both systems write `Body` and `Transform`, so they run as one chain.

```rust
#[derive(Component)]
struct Body {
    velocity: Vec3,
    mass: f32,
    radius: f32,
}

#[derive(Component)]
struct Layer(u32);

#[derive(Resource)]
struct Gravity(Vec3);

fn integrate(
    time: Res<Time<Fixed>>,
    gravity: Res<Gravity>,
    mut bodies: Query<(&mut Transform, &mut Body)>,
) {
    let dt = time.delta_secs();
    for (mut tf, mut body) in &mut bodies {
        body.velocity += gravity.0 * dt;
        tf.translation += body.velocity * dt;
        if tf.translation.y < body.radius {
            tf.translation.y = body.radius;
            body.velocity.y = body.velocity.y.max(0.0);
        }
    }
}

fn separate(mut bodies: Query<(Entity, &mut Transform, &mut Body, &Layer)>) {
    let mut pairs: Vec<(Entity, Entity)> = Vec::new();
    for (a, tf_a, body_a, layer_a) in &bodies {
        for (b, tf_b, body_b, layer_b) in &bodies {
            if a.index() >= b.index() || layer_a.0 != layer_b.0 {
                continue;
            }
            let min = body_a.radius + body_b.radius;
            if tf_a.translation.distance(tf_b.translation) < min {
                pairs.push((a, b));
            }
        }
    }
    for (a, b) in pairs {
        let Ok([(_, mut tf_a, mut body_a, _), (_, mut tf_b, mut body_b, _)]) =
            bodies.get_many_mut([a, b])
        else {
            continue;
        };
        let delta = tf_b.translation - tf_a.translation;
        let dist = delta.length();
        let min = body_a.radius + body_b.radius;
        if dist >= min || dist == 0.0 {
            continue;
        }
        let normal = delta / dist;
        let push = (min - dist) * 0.5;
        tf_a.translation -= normal * push;
        tf_b.translation += normal * push;
        let rel = (body_b.velocity - body_a.velocity).dot(normal);
        if rel < 0.0 {
            let inv_a = 1.0 / body_a.mass.max(0.001);
            let inv_b = 1.0 / body_b.mass.max(0.001);
            let impulse = -rel / (inv_a + inv_b);
            body_a.velocity -= normal * impulse * inv_a;
            body_b.velocity += normal * impulse * inv_b;
        }
    }
}

pub struct PhysicsPlugin;

impl Plugin for PhysicsPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(Gravity(Vec3::new(0.0, -9.8, 0.0)))
            .add_systems(FixedUpdate, (integrate, separate).chain());
    }
}
```

An impulse adds velocity. Spawn places a crate above the ground plane so the next fixed step can fall.

```rust
#[derive(Component)]
struct Body {
    velocity: Vec3,
    mass: f32,
    radius: f32,
}

fn kick(mut bodies: Query<&mut Body>) {
    for mut body in &mut bodies {
        body.velocity += Vec3::new(0.0, 6.0, 2.0);
    }
}

fn spawn_crate(mut commands: Commands) {
    commands.spawn((
        Transform::from_xyz(0.0, 2.0, 0.0),
        Body {
            velocity: Vec3::ZERO,
            mass: 2.0,
            radius: 0.5,
        },
    ));
}
```

A ray against the ground plane reports the hit point without a physics crate.

```rust
fn ray_ground(origin: Vec3, dir: Vec3) -> Option<Vec3> {
    if dir.y >= 0.0 {
        return None;
    }
    let t = -origin.y / dir.y;
    if t < 0.0 {
        return None;
    }
    Some(origin + dir * t)
}

fn aim_at_ground(aimers: Query<&Transform>, mut gizmos: Gizmos) {
    for tf in &aimers {
        let dir = tf.forward().as_vec3();
        if let Some(hit) = ray_ground(tf.translation, dir) {
            gizmos.sphere(hit, 0.1, Color::srgb(1.0, 0.2, 0.2));
        }
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
| Per-entity data | `Component` + `Query` | A field stored outside a component |
| App-wide config or clock | `Resource` | Copy the value onto every entity |
| Stable simulation step | `FixedMain` and the `Fixed` clock | Tie simulation to raw frame `Update` |
| Startup spawn | `Commands` in `Startup` | Spawn from a render system |
| Cross-system notice that is not shared state | Message or observer slot in `bevy-events-messaging` | A new event type invented in this file |
| Props under gravity | `Body` on `FixedUpdate` | Treating `FixedUpdate` itself as a solver |

Load [references/ecs-ownership.md](references/ecs-ownership.md) for the ownership table.

## NEVER

- Do not pin `/0.20.0/` in docs URLs. WHY: links stay on `latest`; the 0.20 target is stated once in prose.
- Do not name a third-party solver's types as Bevy APIs. WHY: the `bevy` feature list has no physics-engine feature.
- Do not pin a solver crate in this skill. Check that crate's own docs before naming its plugin path.
- Do not treat `Fixed` / `FixedMain` as a physics engine. WHY: `bevy::time` documents a clock, not a solver.
- Do not mutably query the same body component from two unordered systems. WHY: systems run in parallel unless `.chain()` orders them.

## Reference

Official links stay on bevy.org. The library pin on bevy-master stays **0.20**. The 0.20 feature list has no physics-engine feature.

### Official Documentation
- [Assets](https://bevy.org/assets/)  -  Official asset catalog. No physics plugin is named from it here.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples)  -  Example tree on the `latest` branch.
- [Quick Start: plugins](https://bevy.org/learn/quick-start/getting-started/plugins/)  -  `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and third-party `add_plugins`.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/)  -  `Component`, `Query`, and `.chain()`. `Fixed` / `FixedMain` are a clock, not a solver.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  ECS ownership and the fixed-timestep schedule names.

#### Complements
- [bevy-character-movement](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-character-movement/SKILL.md)  -  Player locomotion that should not be a rigid body.

#### Downstream / consumers
- Combat, racing, and shooter skills cover hits, vehicles, and shots.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Bevy router.
