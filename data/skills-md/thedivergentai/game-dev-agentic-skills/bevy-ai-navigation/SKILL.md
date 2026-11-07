---
name: bevy-ai-navigation
description: "Bevy 0.20 chase, patrol, and wait policy: an enum brain, a goal, a desired velocity, and a retarget timer on FixedUpdate. Use when an actor must choose a goal before movement. Paths stay on bevy-navigation. Keywords: Brain, Goal, DesiredVelocity, PatrolRoute, FixedUpdate, chase, patrol."
---

# Bevy AI navigation

## When to use

Load this when an actor must chase, patrol, or wait. This skill owns the intent and the desired velocity. Paths stay on bevy-navigation. Transform integration stays on bevy-character-movement. Line-of-sight sensors stay on bevy-spatial-queries.

## ECS shape

- **Components:** a mode flag can be an enum `Component` (see bevy-state-machines for the pattern). Goal position can be your own component. No agent, radius, or layer type was opened.
- **Resources:** a shared patrol table can be a `Resource` you define. No navigation resource was opened.
- **Systems:** read the mode and write a desired velocity or waypoint on `Update` or `Fixed`. Use `.chain()` so policy runs before movement. Do not call an agent callback that writes `Transform`.
- **Schedule:** `Fixed` / `FixedMain` when the result feeds the movement step.

## Policy map

| Need | Owner |
| --- | --- |
| Chase vs patrol vs wait | Enum `Component` plus a system that writes `Goal` |
| Retarget throttle | `Timer` resource ticked on `FixedUpdate` |
| Crowd and avoidance | bevy-navigation |
| Bake and obstacles | bevy-navigation |
| Line of sight | bevy-spatial-queries |

Policy writes `DesiredVelocity`. It does not move `Transform` and it does not query a navmesh.

```toml
[dependencies]
bevy = "0.20"
```

```rust
#[derive(Clone, Copy, PartialEq, Eq, Component)]
enum Brain {
    Wait,
    Patrol,
    Chase,
}

#[derive(Component)]
struct WaypointIndex(usize);

#[derive(Component)]
struct Goal(Vec3);

#[derive(Component)]
struct DesiredVelocity(Vec3);

#[derive(Component)]
struct Player;

#[derive(Resource)]
struct PatrolRoute {
    points: Vec<Vec3>,
}

#[derive(Resource)]
struct RetargetClock(Timer);

fn tick_policy(
    time: Res<Time>,
    mut clock: ResMut<RetargetClock>,
    route: Res<PatrolRoute>,
    players: Query<&Transform, With<Player>>,
    mut actors: Query<(&Brain, &Transform, &mut WaypointIndex, &mut Goal)>,
) {
    clock.0.tick(time.delta());
    if !clock.0.just_finished() {
        return;
    }
    let player_pos = players.iter().next().map(|transform| transform.translation);
    for (brain, transform, mut cursor, mut goal) in &mut actors {
        match *brain {
            Brain::Wait => goal.0 = transform.translation,
            Brain::Patrol => {
                if route.points.is_empty() {
                    continue;
                }
                cursor.0 = (cursor.0 + 1) % route.points.len();
                goal.0 = route.points[cursor.0];
            }
            Brain::Chase => {
                if let Some(pos) = player_pos {
                    goal.0 = pos;
                }
            }
        }
    }
}

fn steer(mut actors: Query<(&Transform, &Goal, &mut DesiredVelocity), With<Brain>>) {
    for (transform, goal, mut velocity) in &mut actors {
        let offset = goal.0 - transform.translation;
        let flat = Vec3::new(offset.x, 0.0, offset.z);
        velocity.0 = if flat.length_squared() < 0.05 {
            Vec3::ZERO
        } else {
            flat.normalize() * 3.0
        };
    }
}

pub struct NavPolicyPlugin;

impl Plugin for NavPolicyPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(PatrolRoute {
            points: vec![Vec3::new(-6.0, 0.0, 0.0), Vec3::new(6.0, 0.0, 4.0)],
        })
        .insert_resource(RetargetClock(Timer::from_seconds(
            0.4,
            TimerMode::Repeating,
        )))
        .add_systems(FixedUpdate, (tick_policy, steer).chain());
    }
}
```

```rust
#[derive(Component)]
struct PatrolAgent;

fn spawn_patrol(mut commands: Commands) {
    commands.spawn((
        PatrolAgent,
        Transform::from_xyz(0.0, 0.0, 0.0),
        DesiredDir(Vec3::X),
    ));
}

#[derive(Component)]
struct DesiredDir(Vec3);

fn hold_when_close(mut agents: Query<(&Transform, &mut DesiredDir), With<PatrolAgent>>) {
    for (transform, mut desired) in &mut agents {
        if transform.translation.distance(Vec3::ZERO) < 0.5 {
            desired.0 = Vec3::ZERO;
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
| Per-entity data | `Component` + `Query` | One script that owns the whole actor |
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

- No navigation-agent or nav-server types from another engine. WHY: this skill writes `Goal` and `DesiredVelocity`; a foreign agent type would move `Transform` and skip the chain into movement.
- No named third-party navigation or physics crate. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented path, bake, or avoidance APIs. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. No AI navigation module was opened. Load [references/ecs-ownership.md](references/ecs-ownership.md) when splitting goal writes from velocity writes. Do not load it to bake a mesh.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog. No AI plugin was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, `Resource` pairing via bevy-data-resources, systems, and `.chain()`.
- App states are not per-entity patrol modes. Per-entity flags stay components (bevy-state-machines).

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - ECS ownership.
- [bevy-navigation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-navigation/SKILL.md) - Paths and navigation meshes.
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Enum components for a mode flag.

#### Complements
- [bevy-character-movement](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-character-movement/SKILL.md) - Integrates a waypoint or velocity.
- [bevy-spatial-queries](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-spatial-queries/SKILL.md) - Sensors and spatial queries.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
