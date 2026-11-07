---
name: bevy-game-loop-waves
description: "Bevy ECS skill for encounter waves. Keywords: Bevy, waves, spawn, encounter, ECS."
---

# Bevy wave loop

## When to use

Load this when enemies arrive in waves and the wave index advances after a clear.

## ECS shape

- **Components:** a wave index and a remaining-count you define.
- **Resources:** run-wide tables live in a resource (bevy-data-resources).
- **Systems:** mutate those components on `Update` or the fixed timestep. Use `.chain()` when damage must land before death.
- **Messages:** one-shot facts (hit, pickup, quest advance) go through bevy-events-messaging. Wave advance below is a resource, not a new message type.

## Examples

```toml
[dependencies]
bevy = "0.20"
```

The wave index and the spawn budget are one resource. Each enemy is an entity. Spawning and clearing share `WaveDirector`, so those systems are chained.

```rust
#[derive(Resource)]
struct WaveDirector {
    index: u32,
    budget: u32,
    intermission: f32,
}

#[derive(Component)]
struct Enemy;

fn boot(mut commands: Commands) {
    commands.insert_resource(WaveDirector {
        index: 1,
        budget: 4,
        intermission: 0.0,
    });
}

fn spawn_budget(mut commands: Commands, mut wave: ResMut<WaveDirector>) {
    if wave.intermission > 0.0 || wave.budget == 0 {
        return;
    }
    for _ in 0..wave.budget {
        commands.spawn(Enemy);
    }
    wave.budget = 0;
}

fn advance_on_clear(
    enemies: Query<(), With<Enemy>>,
    mut wave: ResMut<WaveDirector>,
    time: Res<Time>,
) {
    if !enemies.is_empty() {
        wave.intermission = 0.0;
        return;
    }
    wave.intermission += time.delta_secs();
    if wave.intermission < 2.0 {
        return;
    }
    wave.index += 1;
    wave.budget = 3 + wave.index;
    wave.intermission = 0.0;
}

fn install(app: &mut App) {
    app.add_systems(Startup, boot)
        .add_systems(Update, (spawn_budget, advance_on_clear).chain());
}
```

A fixed step is the right place to tick remaining time on a live enemy. The clear system above stays on `Update` and only reads `Enemy`.

```rust
#[derive(Component)]
struct Lifetime(f32);

fn age_enemies(
    mut commands: Commands,
    mut enemies: Query<(Entity, &mut Lifetime)>,
    time: Res<Time<Fixed>>,
) {
    for (entity, mut life) in &mut enemies {
        life.0 -= time.delta_secs();
        if life.0 <= 0.0 {
            commands.entity(entity).despawn();
        }
    }
}

fn install_lifetime(app: &mut App) {
    app.add_systems(FixedUpdate, age_enemies);
}
```

## Scope

- Wave, spawner, and encounter data are yours to build as components.
- Enemy motion routes to bevy-ai-navigation and bevy-character-movement.

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

- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Official pages stay on the unversioned site.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.
- [bevy-ai-navigation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ai-navigation/SKILL.md) - What spawned actors do.
- [bevy-data-resources](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-data-resources/SKILL.md) - Tables and definitions.
- [bevy-events-messaging](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-events-messaging/SKILL.md) - One-shot facts.

#### Complements
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Mode flags.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
