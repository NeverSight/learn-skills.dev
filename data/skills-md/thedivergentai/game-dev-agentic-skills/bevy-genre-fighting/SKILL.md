---
name: bevy-genre-fighting
description: "Bevy genre router for fighting. Keywords: Bevy, Fighting, genre, ECS, router."
---

# Bevy fighting

Genre router. Domain work lives in the Bevy skills below.

## When to use

Load this for local fighting: frame flags, hitboxes as your data, and a round state. Rollback netcode is out of scope.

## ECS shape

- **Components** hold the genre's per-entity flags as plain data. This file does not name new engine types.
- **Resources** hold run-wide counters (score, wave index, seed) via bevy-data-resources.
- **Systems** read those components on `Update` or the fixed timestep from bevy-master. Order them with `.chain()` when a later system must see the result.
- **Schedule:** gameplay mode changes go through bevy-state-machines. Frame data below is components and one round resource.

## Examples

```toml
[dependencies]
bevy = "0.20"
```

Each fighter stores the frame index, advantage, and health. The round clock is a resource. Input, frame advance, and hit resolution share `Fighter`, so they chain on the fixed step.

```rust
#[derive(Component)]
struct Fighter {
    frame: u16,
    advantage: i16,
    health: i32,
}

#[derive(Component)]
struct Hitbox {
    active: bool,
    damage: i32,
    startup: u16,
    active_until: u16,
}

#[derive(Resource)]
struct RoundClock {
    frames_left: u32,
}

fn boot(mut commands: Commands) {
    commands.insert_resource(RoundClock { frames_left: 60 * 99 });
    commands.spawn((
        Fighter {
            frame: 0,
            advantage: 0,
            health: 10000,
        },
        Hitbox {
            active: false,
            damage: 400,
            startup: 4,
            active_until: 8,
        },
    ));
}

fn open_hitbox(mut fighters: Query<(&Fighter, &mut Hitbox)>) {
    for (fighter, mut hitbox) in &mut fighters {
        hitbox.active = fighter.frame >= hitbox.startup && fighter.frame < hitbox.active_until;
    }
}

fn advance_frames(mut fighters: Query<&mut Fighter>, mut round: ResMut<RoundClock>) {
    for mut fighter in &mut fighters {
        fighter.frame = fighter.frame.saturating_add(1);
    }
    round.frames_left = round.frames_left.saturating_sub(1);
}

fn apply_hits(hitboxes: Query<(Entity, &Hitbox)>, mut fighters: Query<(Entity, &mut Fighter)>) {
    let damage: i32 = hitboxes
        .iter()
        .filter(|(_, box_)| box_.active)
        .map(|(_, box_)| box_.damage)
        .sum();
    if damage == 0 {
        return;
    }
    for (entity, mut fighter) in &mut fighters {
        if hitboxes.iter().any(|(src, box_)| box_.active && src == entity) {
            continue;
        }
        fighter.health -= damage;
        fighter.advantage = -12;
    }
}

fn install(app: &mut App) {
    app.add_systems(Startup, boot).add_systems(
        FixedUpdate,
        (open_hitbox, advance_frames, apply_hits).chain(),
    );
}
```

A round ends when the clock or a health bar hits zero. That system only reads `Fighter` and `RoundClock`.

```rust
#[derive(Component)]
struct Fighter {
    frame: u16,
    advantage: i16,
    health: i32,
}

#[derive(Resource)]
struct RoundClock {
    frames_left: u32,
}

fn round_over(round: Res<RoundClock>, fighters: Query<&Fighter>) -> bool {
    round.frames_left == 0 || fighters.iter().any(|fighter| fighter.health <= 0)
}
```

## Routing

- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Round and character mode.
- [bevy-combat-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-combat-system/SKILL.md) - Strike resolution.
- [bevy-animation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-animation/SKILL.md) - Move clips.
- [bevy-input-handling](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-input-handling/SKILL.md) - Per-frame input.

## Scope

- Local frame data is a `Fighter` component (frame index, advantage, health) plus a `RoundClock` resource. Bevy has no fighting-game type; the example above is the data.

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

- No rollback or netcode crate. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented genre APIs. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- Do not pick a physics or net crate here. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Official pages stay on the unversioned site.

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
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Round and character mode.
- [bevy-combat-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-combat-system/SKILL.md) - Strike resolution.
- [bevy-animation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-animation/SKILL.md) - Move clips.
- [bevy-input-handling](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-input-handling/SKILL.md) - Per-frame input.

#### Downstream / consumers
- None. This router does not own a second implementation.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
