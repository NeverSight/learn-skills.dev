---
name: bevy-adapt-3d-to-2d
description: "Bevy ECS skill for moving a Bevy game from 3D to 2D. Keywords: Bevy, 3D, 2D, adapt, sprite, camera."
---

# Bevy adapt 3D to 2D

## When to use

Load this when a 3D design should render as sprites or billboards. Gameplay components stay. Render components change.

## ECS shape

- **Draw:** replace mesh and PBR material entities' render parts with `Sprite` where a billboard is enough.
- **Camera:** use `Camera2d` from bevy-camera-systems.
- **Lights:** 3D light entities are not required for an unlit sprite. Do not leave clustered-light assumptions in gameplay code.

## What stays and what changes

| Piece | Bevy idiom |
| --- | --- |
| Gameplay on the actor | Keep the same components. Swap render components for `Sprite`. |
| View | `Camera2d`. |
| Draw order | A `DrawOrder` component you store, then write into `Transform`. |

## Examples

```toml
[dependencies]
bevy = "0.20"
```

Gameplay components stay on the entity. The 3D render components come off, and a `Sprite` goes on. `Camera2d` is the view.

```rust
#[derive(Component)]
struct Actor;

#[derive(Component)]
struct DrawOrder(f32);

fn spawn_flat_view(mut commands: Commands) {
    commands.spawn(Camera2d);
}

fn present_as_sprites(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    actors: Query<(Entity, &DrawOrder), With<Actor>>,
) {
    let image = asset_server.load("actors/hero.png");
    for (entity, order) in &actors {
        commands
            .entity(entity)
            .remove::<Mesh3d>()
            .remove::<MeshMaterial3d<StandardMaterial>>()
            .insert((
                Sprite {
                    image: image.clone(),
                    custom_size: Some(Vec2::new(64.0, 64.0)),
                    ..default()
                },
                Transform::from_xyz(0.0, order.0, 0.0),
            ));
    }
}
```

A new actor can spawn already flat. The same `Actor` component is what gameplay systems query.

```rust
#[derive(Component)]
struct Actor;

fn spawn_sprite_actor(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        Actor,
        Sprite {
            image: asset_server.load("actors/hero.png"),
            color: Color::WHITE,
            ..default()
        },
        Transform::from_xyz(0.0, 0.0, 0.0),
    ));
}

fn face_motion(mut actors: Query<(&Transform, &mut Sprite), With<Actor>>) {
    for (transform, mut sprite) in &mut actors {
        sprite.flip_x = transform.translation.x < 0.0;
    }
}
```

Sort sprites from the stored order without a 3D camera. Higher `DrawOrder` maps to a higher Y so the 2D camera draws it later in a top-down layout.

```rust
#[derive(Component)]
struct DrawOrder(f32);

fn apply_draw_order(mut sprites: Query<(&DrawOrder, &mut Transform), With<Sprite>>) {
    for (order, mut transform) in &mut sprites {
        transform.translation.y = order.0;
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
| Per-entity data | `Component` + `Query` | A plain struct stored outside the world |
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

- No leftover `Mesh3d` or `MeshMaterial3d` on an entity that is now a sprite. WHY: both render paths on one entity fight over the same transform.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Permalinks stay unversioned.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [2D examples](https://github.com/bevyengine/bevy/tree/latest/examples/2d) - Sprite and camera samples.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.
- [bevy-camera-systems](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-camera-systems/SKILL.md) - Camera2d.
- [bevy-2d-animation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-2d-animation/SKILL.md) - Sprite clips.

#### Complements
- [bevy-adapt-2d-to-3d](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-adapt-2d-to-3d/SKILL.md) - The reverse adapt.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
