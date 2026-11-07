---
name: bevy-genre-platformer
description: "Route a Bevy 0.20 platformer: coyote time and jump buffer on Mover, gravity on FixedUpdate, one-way ledges, follow camera. Keywords: Bevy, platformer, coyote, Mover, FixedUpdate, Camera2d, ECS."
---

# Bevy Platformer (thin router)

Genre router. Domain work lives in the Bevy skills below.

## When to use

Load this to route a platformer to movement, camera, and tiles.

## ECS shape

- **Components** hold the genre's per-entity flags as plain data. This file does not name new engine types.
- **Resources** hold run-wide counters (score, wave index, seed) via bevy-data-resources.
- **Systems** read those components on `Update` or the fixed timestep from bevy-master. Order them with `.chain()` when a later system must see the result.
- **Schedule:** gameplay mode changes go through bevy-state-machines. Do not invent a genre plugin.

## Routing

- [bevy-character-movement](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-character-movement/SKILL.md) - Locomotion.
- [bevy-camera-systems](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-camera-systems/SKILL.md) - Follow camera.
- [bevy-tilemap](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-tilemap/SKILL.md) - Ground tiles.
- [bevy-2d-animation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-2d-animation/SKILL.md) - Sprite clips.

## Examples

```toml
[dependencies]
bevy = "0.20"
```

Coyote time and the jump buffer live on the mover. Gravity and the jump write `velocity` in one system so they cannot race.

```rust
#[derive(Component)]
struct Mover {
    velocity: Vec2,
    grounded: bool,
    coyote: f32,
    jump_buffer: f32,
}

fn arm_jump(keys: Res<ButtonInput<KeyCode>>, mut movers: Query<&mut Mover>) {
    if !keys.just_pressed(KeyCode::Space) {
        return;
    }
    for mut mover in &mut movers {
        mover.jump_buffer = 0.15;
    }
}

fn feel(mut movers: Query<&mut Mover>, time: Res<Time<Fixed>>) {
    let dt = time.delta_secs();
    for mut mover in &mut movers {
        if mover.grounded {
            mover.coyote = 0.12;
        } else {
            mover.coyote = (mover.coyote - dt).max(0.0);
        }
        mover.jump_buffer = (mover.jump_buffer - dt).max(0.0);
        if mover.jump_buffer > 0.0 && mover.coyote > 0.0 {
            mover.velocity.y = 420.0;
            mover.coyote = 0.0;
            mover.jump_buffer = 0.0;
            mover.grounded = false;
        }
        if !mover.grounded {
            let gravity = if mover.velocity.y < 0.0 { 2200.0 } else { 1400.0 };
            mover.velocity.y -= gravity * dt;
        }
    }
}

fn install_feel(app: &mut App) {
    app.add_systems(Update, arm_jump)
        .add_systems(FixedUpdate, feel);
}
```

`arm_jump` and `feel` both write `Mover`, and they sit on different schedules. If that borrow conflicts, move `arm_jump` onto `FixedUpdate` and `.chain()` it before `feel`.

Integration reads `Mover` and writes `Transform`. Chain it after `feel`.

```rust
#[derive(Component)]
struct Mover {
    velocity: Vec2,
}

fn integrate(mut bodies: Query<(&Mover, &mut Transform)>, time: Res<Time<Fixed>>) {
    let dt = time.delta_secs();
    for (mover, mut tf) in &mut bodies {
        tf.translation.x += mover.velocity.x * dt;
        tf.translation.y += mover.velocity.y * dt;
    }
}
```

A one-way ledge is a component with a top height. The mover only snaps when it is falling.

```rust
#[derive(Component)]
struct OneWay {
    half_width: f32,
    top: f32,
}

#[derive(Component)]
struct Mover {
    velocity: Vec2,
    grounded: bool,
}

fn land(
    mut bodies: Query<(&mut Mover, &Transform)>,
    platforms: Query<(&OneWay, &Transform)>,
) {
    for (mut mover, body_tf) in &mut bodies {
        if mover.velocity.y > 0.0 {
            continue;
        }
        let feet = body_tf.translation.truncate();
        for (plat, plat_tf) in &platforms {
            let top = plat_tf.translation.y + plat.top;
            let dx = (feet.x - plat_tf.translation.x).abs();
            if dx <= plat.half_width && (feet.y - top).abs() < 6.0 {
                mover.grounded = true;
                mover.velocity.y = 0.0;
            }
        }
    }
}
```

The camera copies the player translation and keeps its own z.

```rust
#[derive(Component)]
struct Player;

fn follow(
    player: Query<&Transform, With<Player>>,
    mut cameras: Query<&mut Transform, (With<Camera2d>, Without<Player>)>,
) {
    let Ok(player_tf) = player.single() else {
        return;
    };
    let Ok(mut cam) = cameras.single_mut() else {
        return;
    };
    cam.translation.x = player_tf.translation.x;
    cam.translation.y = player_tf.translation.y;
}
```

## Scope

- Tile collision and sprite clips route to bevy-tilemap and bevy-2d-animation.
- `land` and `feel` both write `Mover`. Chain them on `FixedUpdate` when both are installed.

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
| Per-entity data | `Component` + `Query` | A field stored off the entity |
| App-wide config or clock | `Resource` | Copy the value onto every entity |
| Stable simulation step | `FixedMain` and the `Fixed` clock | Tie simulation to raw frame `Update` |
| Startup spawn | `Commands` in `Startup` | Spawn from a render system |
| Cross-system notice that is not shared state | Message or observer slot in `bevy-events-messaging` | A new event type invented in this file |
| An API outside the documented set | Use the examples in this skill | A made-up crate or API |

Load [references/ecs-ownership.md](references/ecs-ownership.md) for the ownership table.

## NEVER

- Do not pin `/0.20.0/` in docs URLs. WHY: links stay on `latest`; the 0.20 target is stated once in prose.
- Do not mutably query the same component from two unordered systems. WHY: the schedule runs systems in parallel unless `.chain()` orders them.
- Do not invent a physics, navigation, networking, or XR crate here. WHY: this skill only names documented Bevy crates and modules.

- Do not apply gravity on `Update` while coyote and the jump buffer tick on `FixedUpdate`. WHY: frame time then changes jump height.
- Do not write `Mover` from `arm_jump` and `feel` on two schedules. WHY: those systems alias the same component; put both on `FixedUpdate` and `.chain()` `arm_jump` before `feel`.
- No invented genre APIs. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- Do not pick a physics or net crate here. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Official pages stay on the unversioned `latest` branch.

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
- [godot-genre-platformer](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-genre-platformer/SKILL.md) - Platformer on the Godot engine, same depth.
- [bevy-character-movement](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-character-movement/SKILL.md) - Locomotion.
- [bevy-camera-systems](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-camera-systems/SKILL.md) - Follow camera.
- [bevy-tilemap](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-tilemap/SKILL.md) - Ground tiles.
- [bevy-2d-animation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-2d-animation/SKILL.md) - Sprite clips.

#### Downstream / consumers
- None. This router does not own a second implementation.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
