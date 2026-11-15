---
name: bevy-3d-world-building
description: "Bevy ECS skill for 3D level assembly. Keywords: Bevy, level, scene, mesh, world, ECS."
---

# Bevy 3D world building

## When to use

Load this when placing meshes, lights, and colliders into a level. Scene spawn mechanics stay on bevy-asset-scenes. Physics bodies stay on bevy-physics-3d.

## ECS shape

- **Spawn:** entities with transforms and render components. Primitives (`Cuboid`, `Sphere`, `Cylinder`) convert into `Mesh` and ride on `Mesh3d` plus `MeshMaterial3d`.
- **Scenes:** `bevy_scene` and `bevy_gltf` are features. Spawn details are on bevy-asset-scenes (`AssetServer`, scene spawn).
- **Lights:** a `DirectionalLight` is an entity with a `Transform`. Fog is `DistanceFog` on the camera entity. Full lighting setups stay on bevy-3d-lighting.
- **Systems:** which cells are present is a `Resource`. Spawning a cell is `Commands` in `Update`.

```rust
fn spawn_level(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
) {
    let stone = materials.add(StandardMaterial {
        base_color: Color::srgb(0.45, 0.42, 0.38),
        ..default()
    });
    let floor = materials.add(StandardMaterial {
        base_color: Color::srgb(0.28, 0.30, 0.26),
        ..default()
    });
    commands.spawn((
        Mesh3d(meshes.add(Cuboid::new(24.0, 0.2, 24.0))),
        MeshMaterial3d(floor),
        Transform::from_xyz(0.0, -0.1, 0.0),
    ));
    commands.spawn((
        Mesh3d(meshes.add(Cylinder::new(0.4, 3.0))),
        MeshMaterial3d(stone.clone()),
        Transform::from_xyz(-4.0, 1.5, -2.0),
    ));
    commands.spawn((
        Mesh3d(meshes.add(Sphere::new(0.6))),
        MeshMaterial3d(stone),
        Transform::from_xyz(2.0, 0.6, 1.0),
    ));
    commands.spawn((
        DirectionalLight {
            illuminance: 12_000.0,
            shadow_maps_enabled: true,
            ..default()
        },
        Transform::from_xyz(6.0, 10.0, 4.0).looking_at(Vec3::ZERO, Vec3::Y),
    ));
    commands.spawn((
        Camera3d::default(),
        DistanceFog {
            color: Color::srgb(0.55, 0.62, 0.70),
            falloff: FogFalloff::Linear {
                start: 12.0,
                end: 40.0,
            },
            ..default()
        },
        Transform::from_xyz(0.0, 8.0, 14.0).looking_at(Vec3::ZERO, Vec3::Y),
    ));
}
```

Kitbash props are ordinary entities. A helper returns the entity id so later systems can parent markers to it.

```rust
fn spawn_prop(
    commands: &mut Commands,
    meshes: &mut Assets<Mesh>,
    materials: &mut Assets<StandardMaterial>,
    at: Vec3,
    size: Vec3,
    color: Color,
) -> Entity {
    commands
        .spawn((
            Mesh3d(meshes.add(Cuboid::from_size(size))),
            MeshMaterial3d(materials.add(StandardMaterial {
                base_color: color,
                ..default()
            })),
            Transform::from_translation(at),
        ))
        .id()
}
```

Cells already in the world live on one resource. The streamer inserts a marker component and a mesh only for cells that are not recorded yet.

```rust
#[derive(Resource, Default)]
struct LoadedCells {
    coords: Vec<(i32, i32)>,
}

#[derive(Component)]
struct CellMarker {
    x: i32,
    z: i32,
}

fn stream_cells(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    mut loaded: ResMut<LoadedCells>,
    focus: Query<&Transform, With<Camera3d>>,
) {
    let Ok(focus) = focus.single() else {
        return;
    };
    let cx = (focus.translation.x / 8.0).floor() as i32;
    let cz = (focus.translation.z / 8.0).floor() as i32;
    for dz in -1..=1 {
        for dx in -1..=1 {
            let coord = (cx + dx, cz + dz);
            if loaded.coords.contains(&coord) {
                continue;
            }
            loaded.coords.push(coord);
            commands.spawn((
                CellMarker {
                    x: coord.0,
                    z: coord.1,
                },
                Mesh3d(meshes.add(Cuboid::new(8.0, 0.1, 8.0))),
                MeshMaterial3d(materials.add(StandardMaterial {
                    base_color: Color::srgb(0.3, 0.34, 0.28),
                    ..default()
                })),
                Transform::from_xyz(coord.0 as f32 * 8.0, 0.0, coord.1 as f32 * 8.0),
            ));
        }
    }
}
```

```toml
[dependencies]
bevy = "0.20"
```

## Level choices

| Need | Bevy approach |
| --- | --- |
| Packed level | A scene asset spawned through bevy-asset-scenes |
| Kitbash props | Entities with `Mesh3d` and `MeshMaterial3d` |
| Atmosphere | `DirectionalLight`, `DistanceFog`, and the camera entity |

## Scope

- Primitives above cover greybox blocks, columns, and spheres. Heightmaps are a `Mesh` you fill yourself, then the same `Mesh3d` spawn.
- Collider authoring belongs with bevy-physics-3d once you choose a physics solver.

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

- No CSG, grid-map, or world-environment node types in Bevy code. WHY: greybox meshes, lights, and `DistanceFog` are the documented Bevy pieces.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

Official links stay on bevy.org. The library pin on bevy-master stays **0.20.0**.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.
- [bevy-asset-scenes](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-asset-scenes/SKILL.md) - Scene spawn.
- [bevy-3d-lighting](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-3d-lighting/SKILL.md) - Lights.
- [bevy-3d-materials](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-3d-materials/SKILL.md) - Surfaces.
- [bevy-camera-systems](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-camera-systems/SKILL.md) - View.

#### Complements
- [bevy-procedural-generation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-procedural-generation/SKILL.md) - Generated layouts.
- [bevy-physics-3d](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-physics-3d/SKILL.md) - Simulated props. Solver still unpicked.
- [godot-3d-world-building](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-3d-world-building/SKILL.md) - Same topic on the Godot track.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
