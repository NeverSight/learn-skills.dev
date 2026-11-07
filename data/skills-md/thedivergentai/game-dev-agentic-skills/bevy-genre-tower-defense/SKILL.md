---
name: bevy-genre-tower-defense
description: "Bevy genre router for tower defense. Use when placing towers, marching creeps along waypoints, and spending gold on a fixed timestep. Keywords: Bevy, tower defense, creep, waypoint, gold, ECS."
---

# Bevy Tower defense (thin router)

Genre router. Domain work lives in the Bevy skills below.

## When to use

Load this for towers, creeps, and waves on a path.

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

- [bevy-game-loop-waves](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-game-loop-waves/SKILL.md) - Creep waves.
- [bevy-navigation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-navigation/SKILL.md) - Paths and navigation meshes.
- [bevy-combat-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-combat-system/SKILL.md) - Tower shots.
- [bevy-economy-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-economy-system/SKILL.md) - Build costs.

## Scope

Towers, creeps, waypoints, and gold are plain components and one resource. A navigation mesh belongs on bevy-navigation.

## Examples

```toml
[package]
name = "tower-defense"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.20"
```

Creeps walk a waypoint list. Towers that are off cooldown and in range spend a shot and damage the nearest creep. Gold is one resource.

```rust
#[derive(Component)]
struct Tower {
    range: f32,
    cooldown: f32,
    damage: i32,
}

#[derive(Component)]
struct Creep {
    hp: i32,
    waypoint: usize,
    speed: f32,
}

#[derive(Resource)]
struct Path {
    points: Vec<Vec3>,
}

#[derive(Resource)]
struct Gold(i32);

fn march_creeps(
    time: Res<Time<Fixed>>,
    path: Res<Path>,
    mut creeps: Query<(Entity, &mut Transform, &mut Creep)>,
    mut commands: Commands,
) {
    let dt = time.delta_secs();
    for (entity, mut transform, mut creep) in &mut creeps {
        let Some(goal) = path.points.get(creep.waypoint) else {
            commands.entity(entity).despawn();
            continue;
        };
        let delta = *goal - transform.translation;
        let step = creep.speed * dt;
        if delta.length() <= step {
            transform.translation = *goal;
            creep.waypoint += 1;
        } else {
            transform.translation += delta.normalize() * step;
        }
    }
}

fn towers_fire(
    time: Res<Time<Fixed>>,
    mut towers: Query<(&Transform, &mut Tower)>,
    mut creeps: Query<(&Transform, &mut Creep)>,
) {
    let dt = time.delta_secs();
    for (tower_tf, mut tower) in &mut towers {
        tower.cooldown = (tower.cooldown - dt).max(0.0);
        if tower.cooldown > 0.0 {
            continue;
        }
        let mut best: Option<(f32, Mut<Creep>)> = None;
        for (creep_tf, creep) in &mut creeps {
            let dist = tower_tf.translation.distance(creep_tf.translation);
            if dist > tower.range {
                continue;
            }
            let closer = match &best {
                Some((best_dist, _)) => dist < *best_dist,
                None => true,
            };
            if closer {
                best = Some((dist, creep));
            }
        }
        if let Some((_, mut creep)) = best {
            creep.hp -= tower.damage;
            tower.cooldown = 0.6;
        }
    }
}
```

Startup inserts the path and gold, then spawns one tower and one creep. The two systems share `Creep`, so they run in one chain.

```rust
#[derive(Component)]
struct Tower {
    range: f32,
    cooldown: f32,
    damage: i32,
}

#[derive(Component)]
struct Creep {
    hp: i32,
    waypoint: usize,
    speed: f32,
}

#[derive(Resource)]
struct Path {
    points: Vec<Vec3>,
}

#[derive(Resource)]
struct Gold(i32);

fn setup(mut commands: Commands) {
    commands.insert_resource(Path {
        points: vec![
            Vec3::new(0.0, 0.0, 0.0),
            Vec3::new(8.0, 0.0, 0.0),
            Vec3::new(8.0, 0.0, 8.0),
        ],
    });
    commands.insert_resource(Gold(100));
    commands.spawn((
        Tower {
            range: 5.0,
            cooldown: 0.0,
            damage: 10,
        },
        Transform::from_xyz(4.0, 0.0, 2.0),
    ));
    commands.spawn((
        Creep {
            hp: 30,
            waypoint: 0,
            speed: 2.5,
        },
        Transform::from_xyz(0.0, 0.0, 0.0),
    ));
}

fn march_creeps(
    time: Res<Time<Fixed>>,
    path: Res<Path>,
    mut creeps: Query<(Entity, &mut Transform, &mut Creep)>,
    mut commands: Commands,
) {
    let dt = time.delta_secs();
    for (entity, mut transform, mut creep) in &mut creeps {
        let Some(goal) = path.points.get(creep.waypoint) else {
            commands.entity(entity).despawn();
            continue;
        };
        let delta = *goal - transform.translation;
        let step = creep.speed * dt;
        if delta.length() <= step {
            transform.translation = *goal;
            creep.waypoint += 1;
        } else {
            transform.translation += delta.normalize() * step;
        }
    }
}

fn towers_fire(
    time: Res<Time<Fixed>>,
    mut towers: Query<(&Transform, &mut Tower)>,
    mut creeps: Query<(Entity, &Transform, &mut Creep)>,
) {
    let dt = time.delta_secs();
    for (tower_tf, mut tower) in &mut towers {
        tower.cooldown = (tower.cooldown - dt).max(0.0);
        if tower.cooldown > 0.0 {
            continue;
        }
        let mut best_dist = f32::MAX;
        let mut best_entity = None;
        for (entity, creep_tf, _) in creeps.iter() {
            let dist = tower_tf.translation.distance(creep_tf.translation);
            if dist <= tower.range && dist < best_dist {
                best_dist = dist;
                best_entity = Some(entity);
            }
        }
        let Some(entity) = best_entity else {
            continue;
        };
        let Ok((_, _, mut creep)) = creeps.get_mut(entity) else {
            continue;
        };
        creep.hp -= tower.damage;
        tower.cooldown = 0.6;
    }
}

pub struct TowerDefensePlugin;

impl Plugin for TowerDefensePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup)
            .add_systems(FixedUpdate, (march_creeps, towers_fire).chain());
    }
}
```

Selling a tower pays gold and despawns it. One system owns both writes.

```rust
#[derive(Component)]
struct Tower {
    range: f32,
    cooldown: f32,
    damage: i32,
}

#[derive(Resource)]
struct Gold(i32);

fn sell(
    keys: Res<ButtonInput<KeyCode>>,
    mut gold: ResMut<Gold>,
    towers: Query<Entity, With<Tower>>,
    mut commands: Commands,
) {
    if !keys.just_pressed(KeyCode::KeyX) {
        return;
    }
    let Some(entity) = towers.iter().next() else {
        return;
    };
    gold.0 += 40;
    commands.entity(entity).despawn();
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
- [godot-genre-tower-defense](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-genre-tower-defense/SKILL.md) - Equivalent Godot skill.
- [bevy-game-loop-waves](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-game-loop-waves/SKILL.md) - Creep waves.
- [bevy-navigation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-navigation/SKILL.md) - Paths and navigation meshes.
- [bevy-combat-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-combat-system/SKILL.md) - Tower shots.
- [bevy-economy-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-economy-system/SKILL.md) - Build costs.

#### Downstream / consumers
- None. This router does not own a second implementation.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
