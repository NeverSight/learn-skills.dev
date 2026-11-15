---
name: bevy-camera-systems
description: "Bevy ECS skill for cameras. Keywords: Bevy, Camera, Camera2d, Camera3d, Transform."
---

# Bevy camera systems

## When to use

Load this when a view must render 2D or 3D. `Camera`, `Camera2d`, `Camera3d`, and the `two_passes` example are the sources for the names below. The library pin is 0.20.

## ECS shape

- **Components:** `Camera` is the viewpoint (projection and render target). A `Camera` with no render graph errors at runtime. `Camera2d` enables the 2D graph and requires `Camera`, `Projection`, and `Frustum`. `Camera3d` enables the main 3D graph and requires `Camera` and `Projection`. 3D space is right-handed: X right, Y up, Z back, so forward is -Z.
- **Spawn:** the example uses `commands.spawn((Camera3d::default(), Transform::from_xyz(...).looking_at(Vec3::ZERO, Vec3::Y)))`. A second camera sets `Camera { order: 1, clear_color: ClearColorConfig::None, ..default() }` so it draws on top without clearing.
- **Query:** systems may take `(&Camera, &GlobalTransform)` with `With<Camera2d>`. `Camera::viewport_to_world_2d` maps a viewport position to a 2D world position for an orthographic camera along Z.
- **Schedule:** spawn on `Startup`. Follow, split viewports, and trauma offset are your components on `Update`.

```rust
fn spawn_cameras(mut commands: Commands) {
    commands.spawn((
        Camera3d::default(),
        Transform::from_xyz(0.0, 6.0, 10.0).looking_at(Vec3::ZERO, Vec3::Y),
    ));
    commands.spawn((
        Camera2d,
        Camera {
            order: 1,
            clear_color: ClearColorConfig::None,
            ..default()
        },
    ));
}
```

```rust
#[derive(Component)]
struct FollowTarget;

#[derive(Component)]
struct FollowCam {
    offset: Vec3,
    stiffness: f32,
}

fn follow_target(
    time: Res<Time>,
    targets: Query<&Transform, (With<FollowTarget>, Without<FollowCam>)>,
    mut cameras: Query<(&FollowCam, &mut Transform)>,
) {
    let Ok(target) = targets.single() else {
        return;
    };
    let dt = time.delta_secs();
    for (follow, mut transform) in &mut cameras {
        let desired = target.translation + follow.offset;
        let t = 1.0 - (-follow.stiffness * dt).exp();
        transform.translation = transform.translation.lerp(desired, t);
        transform.look_at(target.translation, Vec3::Y);
    }
}
```

```rust
use bevy::camera::Viewport;

fn split_view(mut cameras: Query<&mut Camera, With<Camera3d>>) {
    let mut iter = cameras.iter_mut();
    if let Some(mut left) = iter.next() {
        left.viewport = Some(Viewport {
            physical_position: UVec2::new(0, 0),
            physical_size: UVec2::new(640, 720),
            depth: 0.0..1.0,
        });
    }
    if let Some(mut right) = iter.next() {
        right.order = 0;
        right.viewport = Some(Viewport {
            physical_position: UVec2::new(640, 0),
            physical_size: UVec2::new(640, 720),
            depth: 0.0..1.0,
        });
    }
}
```

```rust
fn cursor_to_world(
    windows: Query<&Window>,
    cameras: Query<(&Camera, &GlobalTransform), With<Camera2d>>,
) {
    let Ok(window) = windows.single() else {
        return;
    };
    let Ok((camera, transform)) = cameras.single() else {
        return;
    };
    let Some(cursor) = window.cursor_position() else {
        return;
    };
    let _world = camera.viewport_to_world_2d(transform, cursor);
}

#[derive(Component)]
struct Trauma(f32);

fn apply_trauma(time: Res<Time>, mut cameras: Query<(&mut Trauma, &mut Transform), With<Camera3d>>) {
    for (mut trauma, mut transform) in &mut cameras {
        trauma.0 = (trauma.0 - time.delta_secs()).max(0.0);
        let shake = trauma.0 * trauma.0;
        transform.translation.x += (time.elapsed_secs() * 31.0).sin() * 0.15 * shake;
        transform.translation.y += (time.elapsed_secs() * 27.0).cos() * 0.1 * shake;
    }
}
```

```toml
[dependencies]
bevy = "0.20"
```

## View choices

| Need | Bevy approach |
| --- | --- |
| Active view | An entity with `Camera2d` or `Camera3d` |
| Camera pose | `Transform` on that entity |
| Draw order / overlay | `Camera.order` and `ClearColorConfig::None` |
| Screen point to 2D world | `viewport_to_world_2d` with `GlobalTransform` |

## Scope

- Follow, look-at, trauma offset, and split `Viewport`s are the systems above. A `Camera` still needs its render graph: spawn `Camera2d` or `Camera3d` so Bevy inserts `CameraRenderGraph`.
- A texture target is a `RenderTarget::Image` component on the camera entity. The split example keeps the window target and sets `Camera::viewport`.

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
| Per-entity data | `Component` + `Query` | A script field copied onto the entity |
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

- No scene-tree camera node types in Bevy code. WHY: `Camera2d` and `Camera3d` are the documented Bevy pieces.
- No claim that Bevy ships a follow, spring-arm, or shake component. WHY: those rigs are the `FollowCam` and `Trauma` components in this skill, written as ordinary ECS.
- No third-party camera crates. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

Official links stay on bevy.org. The library pin on bevy-master stays **0.20.0**.

### Official Documentation
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples)  -  Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/)  -  `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Who owns which piece of state.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md)  -  Spawn tuples and systems.

#### Complements
- [bevy-input-handling](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-input-handling/SKILL.md)  -  Mouse motion a camera system may read.
- [bevy-character-movement](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-character-movement/SKILL.md)  -  Actor the view may track.
- [godot-camera-systems](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-camera-systems/SKILL.md)  -  Same topic on the Godot track.

#### Downstream / consumers
- [bevy-asset-scenes](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-asset-scenes/SKILL.md)  -  Scenes that include a camera entity.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Bevy router.
