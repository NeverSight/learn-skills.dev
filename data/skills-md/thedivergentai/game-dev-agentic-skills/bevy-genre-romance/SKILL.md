---
name: bevy-genre-romance
description: "Bevy genre router for Romance. Keywords: Bevy, Romance, genre, ECS, router."
---

# Bevy Romance

Genre router. Domain work lives in the Bevy skills below.

## When to use

Load this for relationship values and scene routes on top of dialogue.

## ECS shape

- **Components** hold the genre's per-entity flags as plain data. This file does not name new engine types.
- **Resources** hold run-wide counters (score, wave index, seed) via bevy-data-resources.
- **Systems** read those components on `Update` or the fixed timestep from bevy-master. Order them with `.chain()` when a later system must see the result.
- **Schedule:** gameplay mode changes go through bevy-state-machines. Affection and route flags below are a component plus one resource.

## Examples

```toml
[dependencies]
bevy = "0.20"
```

Each character stores affection and the last choice. Route flags are a resource. Apply the choice, then pick the next scene id. Those systems share `Bond`, so they chain.

```rust
#[derive(Clone, Copy, PartialEq, Eq)]
enum Choice {
    Warm,
    Cool,
}

#[derive(Component)]
struct Bond {
    affection: i32,
    last: Choice,
}

#[derive(Resource)]
struct RouteFlags {
    confession_open: bool,
    scene: u32,
}

fn boot(mut commands: Commands) {
    commands.insert_resource(RouteFlags {
        confession_open: false,
        scene: 0,
    });
    commands.spawn(Bond {
        affection: 0,
        last: Choice::Cool,
    });
}

fn apply_choice(keys: Res<ButtonInput<KeyCode>>, mut bonds: Query<&mut Bond>) {
    let choice = if keys.just_pressed(KeyCode::Digit1) {
        Some(Choice::Warm)
    } else if keys.just_pressed(KeyCode::Digit2) {
        Some(Choice::Cool)
    } else {
        None
    };
    let Some(choice) = choice else {
        return;
    };
    for mut bond in &mut bonds {
        bond.last = choice;
        bond.affection += if choice == Choice::Warm { 10 } else { -5 };
    }
}

fn advance_route(bonds: Query<&Bond>, mut route: ResMut<RouteFlags>) {
    let Some(bond) = bonds.iter().next() else {
        return;
    };
    route.confession_open = bond.affection >= 30;
    if route.confession_open {
        route.scene = 4;
    } else if bond.last == Choice::Warm {
        route.scene = 2;
    } else {
        route.scene = 1;
    }
}

fn install(app: &mut App) {
    app.add_systems(Startup, boot)
        .add_systems(Update, (apply_choice, advance_route).chain());
}
```

A scene is available when affection is at least the threshold stored on that scene.

```rust
#[derive(Component)]
struct SceneGate {
    id: u32,
    min_affection: i32,
}

#[derive(Component)]
struct Bond {
    affection: i32,
}

fn gate_open(bonds: Query<&Bond>, gates: Query<&SceneGate>, scene_id: u32) -> bool {
    let Some(bond) = bonds.iter().next() else {
        return false;
    };
    gates
        .iter()
        .any(|gate| gate.id == scene_id && bond.affection >= gate.min_affection)
}
```

## Scene shape

| Piece | Bevy idiom |
| --- | --- |
| Genre content | Entities plus the domain skills linked below |
| Run-wide director | A `Resource` |
| Loop notices | bevy-events-messaging |

## Routing

- [bevy-dialogue-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-dialogue-system/SKILL.md) - Scenes.
- [bevy-rpg-stats](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-rpg-stats/SKILL.md) - Affection as a stat you name.
- [bevy-save-load](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-save-load/SKILL.md) - Route flags.

## Scope

- Affection lives on `Bond`. `RouteFlags` stores the open scene. Bevy has no relationship type; the example above is the data.

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
| Per-entity data | `Component` + `Query` | One script that owns the whole tree |
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

- No foreign-engine types in Bevy code. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented genre APIs. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- Do not pick a physics or net crate here. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

Official pages stay on unversioned permalinks. The library pin on bevy-master stays **0.20**.

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
- [godot-genre-romance](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-genre-romance/SKILL.md) - Peer skill for the same genre.
- [bevy-dialogue-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-dialogue-system/SKILL.md) - Scenes.
- [bevy-rpg-stats](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-rpg-stats/SKILL.md) - Affection as a stat you name.
- [bevy-save-load](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-save-load/SKILL.md) - Route flags.

#### Downstream / consumers
- None. This router does not own a second implementation.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
