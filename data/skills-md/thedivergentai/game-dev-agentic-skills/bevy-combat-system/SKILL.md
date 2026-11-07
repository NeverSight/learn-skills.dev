---
name: bevy-combat-system
description: "Bevy ECS combat: Health, Team, and Invuln on actors, Hit messages, melee reach, despawn on FixedUpdate after damage. Use when a hit must change health before death. Keywords: Bevy, combat, health, Hit, Invuln, chain, FixedUpdate."
---

# Bevy combat system

## When to use

Load this when hits change health. Overlap tests wait on bevy-spatial-queries and the unpicked physics solver.

## ECS shape

- **Components:** health and team id that you define. No engine combat component was opened.
- **Resources:** run-wide tables live in a resource (bevy-data-resources).
- **Systems:** mutate those components on `Update` or the fixed timestep. Use `.chain()` when damage must land before death.
- **Messages:** one-shot facts (hit, pickup, quest advance) go through bevy-events-messaging. This file does not add a new event type name.

## Idioms

| Need | Bevy shape |
| --- | --- |
| Health | A component with current and max. Fields are yours. |
| Confirmed hit | A message the health system consumes. |
| Hurt volume | A reach check on `Transform` until a solver owns shapes. |

## Scope

- Health, damage, invulnerability, and team id are components. A hit is a message the health system consumes.
- Volume overlap stays with bevy-physics-2d and bevy-physics-3d. A reach check on `Transform` is enough when you have no solver yet.

## Examples

```toml
[package]
name = "combat"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.20"
```

Health and team live on the actor. Apply hits, then despawn the dead, on one chain so death sees the new health.

```rust
#[derive(Component)]
struct Health {
    current: i32,
    max: i32,
}

#[derive(Component)]
struct Team(u32);

#[derive(Component)]
struct Invuln {
    remaining: f32,
}

#[derive(Message)]
struct Hit {
    target: Entity,
    amount: i32,
    source_team: u32,
}

fn apply_hits(
    mut hits: MessageReader<Hit>,
    mut actors: Query<(&Team, &mut Health, &mut Invuln)>,
) {
    for hit in hits.read() {
        let Ok((team, mut health, mut invuln)) = actors.get_mut(hit.target) else {
            continue;
        };
        if team.0 == hit.source_team || invuln.remaining > 0.0 || hit.amount <= 0 {
            continue;
        }
        health.current = (health.current - hit.amount).max(0);
        invuln.remaining = 0.25;
    }
}

fn tick_invuln(time: Res<Time<Fixed>>, mut actors: Query<&mut Invuln>) {
    let dt = time.delta_secs();
    for mut invuln in &mut actors {
        invuln.remaining = (invuln.remaining - dt).max(0.0);
    }
}

fn despawn_dead(mut commands: Commands, actors: Query<(Entity, &Health)>) {
    for (entity, health) in &actors {
        if health.current <= 0 {
            commands.entity(entity).despawn();
        }
    }
}

pub struct CombatPlugin;

impl Plugin for CombatPlugin {
    fn build(&self, app: &mut App) {
        app.add_message::<Hit>().add_systems(
            FixedUpdate,
            (tick_invuln, apply_hits, despawn_dead).chain(),
        );
    }
}
```

A swing writes hits from translation distance. Physics volumes replace this query when a solver owns the shapes.

```rust
#[derive(Component)]
struct Melee {
    reach: f32,
    damage: i32,
    active: bool,
}

#[derive(Component)]
struct Team(u32);

#[derive(Message)]
struct Hit {
    target: Entity,
    amount: i32,
    source_team: u32,
}

fn melee_hits(
    attackers: Query<(&Transform, &Team, &Melee)>,
    targets: Query<(Entity, &Transform, &Team)>,
    mut hits: MessageWriter<Hit>,
) {
    for (atk_tf, atk_team, melee) in &attackers {
        if !melee.active {
            continue;
        }
        for (entity, tgt_tf, tgt_team) in &targets {
            if atk_team.0 == tgt_team.0 {
                continue;
            }
            if atk_tf.translation.distance(tgt_tf.translation) <= melee.reach {
                hits.write(Hit {
                    target: entity,
                    amount: melee.damage,
                    source_team: atk_team.0,
                });
            }
        }
    }
}
```

Spawn a fighter with full health and a clear invulnerability window.

```rust
#[derive(Component)]
struct Health {
    current: i32,
    max: i32,
}

#[derive(Component)]
struct Team(u32);

#[derive(Component)]
struct Invuln {
    remaining: f32,
}

fn spawn_fighter(mut commands: Commands) {
    commands.spawn((
        Health { current: 40, max: 40 },
        Team(1),
        Invuln { remaining: 0.0 },
        Transform::from_xyz(0.0, 0.0, 0.0),
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
| Per-entity data | `Component` + `Query` | A scene-tree script on the actor |
| App-wide config or clock | `Resource` | Copy the value onto every entity |
| Stable simulation step | `FixedMain` and the `Fixed` clock | Tie simulation to raw frame `Update` |
| Startup spawn | `Commands` in `Startup` | Spawn from a render system |
| Cross-system notice that is not shared state | Message or observer slot in `bevy-events-messaging` | A new event type invented in this file |
| An API outside the documented set | Read the official manual linked below | A made-up crate or API |

Load [references/ecs-ownership.md](references/ecs-ownership.md) for the ownership table.

## NEVER

- Do not pin `/0.20.0/` in docs URLs. WHY: links stay on `latest`; the 0.20 target is stated once in prose.
- Do not mutably query the same component from two unordered systems. WHY: the schedule runs systems in parallel unless `.chain()` orders them.
- Do not invent a physics, navigation, networking, or XR crate here. WHY: this skill only names documented Bevy crates and modules.

- No scene-tree node or signal bus for this mechanic. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20**.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.
- [bevy-spatial-queries](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-spatial-queries/SKILL.md) - Casts. Solver still unpicked.
- [bevy-rpg-stats](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-rpg-stats/SKILL.md) - Attack numbers.
- [bevy-data-resources](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-data-resources/SKILL.md) - Tables and definitions.
- [bevy-events-messaging](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-events-messaging/SKILL.md) - One-shot facts.

#### Complements
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Mode flags.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
