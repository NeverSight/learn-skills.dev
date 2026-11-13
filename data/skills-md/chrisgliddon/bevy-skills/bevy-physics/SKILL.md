---
name: bevy-physics
description: Use when adding `RapierPhysicsPlugin`, spawning `RigidBody`/`Collider`, reading `CollisionEvent` or `PhysicsQuarantineEvent`, querying with `ReadRapierContext`, configuring `KinematicCharacterController`, or ordering gameplay around `PhysicsSet` in Bevy 0.20.
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "2"
  area: physics
  bevy_version: "0.20"
---

# Bevy 0.20 — physics with Rapier

## When to use this skill

- Add 2D/3D rigid bodies, colliders, sensors, joints, or character movement.
- Decide between `bevy_rapier` and an alternative such as Avian.
- Place input/gameplay systems around a physics step without transform jitter.
- Read collision messages or perform ray, shape, point, and overlap queries.
- Configure headless physics, interpolation, CCD, collision groups, or tests.

Bevy core does not include a physics engine. For Bevy 0.20, use
`bevy_rapier2d`/`bevy_rapier3d 0.37` for the mature Rapier integration. Consider
`avian2d`/`avian3d 0.8` when its ECS-native architecture or modular solver is the
specific reason to choose it. Do not install both engines on the same simulated
entities.

## Canonical fixed-step Rapier 3D pattern

```toml
[dependencies]
bevy = "0.20"
bevy_rapier3d = "0.37"
```

```rust
use bevy::prelude::*;
use bevy_rapier3d::prelude::*;

const PHYSICS_HZ: f64 = 60.0;
const PHYSICS_DT: f32 = 1.0 / PHYSICS_HZ as f32;

#[derive(Component)]
struct Player;

#[derive(SystemSet, Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum GamePhysics {
    Drive,
    React,
}

fn main() {
    let mut app = App::new();
    app.add_plugins(DefaultPlugins)
        .insert_resource(Time::<Fixed>::from_hz(PHYSICS_HZ))
        .insert_resource(TimestepMode::Fixed {
            dt: PHYSICS_DT,
            substeps: 1,
        })
        .add_plugins((
            RapierPhysicsPlugin::<NoUserData>::default().in_fixed_schedule(),
            RapierDebugRenderPlugin::default(),
        ))
        .configure_sets(
            FixedUpdate,
            (
                GamePhysics::Drive.before(PhysicsSet::SyncBackend),
                GamePhysics::React.after(PhysicsSet::Writeback),
            ),
        )
        .add_systems(Startup, setup)
        .add_systems(FixedUpdate, drive_player.in_set(GamePhysics::Drive))
        .add_systems(FixedUpdate, react_to_collisions.in_set(GamePhysics::React));
    app.run();
}

fn setup(mut commands: Commands) {
    commands.spawn((
        Camera3d::default(),
        Transform::from_xyz(8.0, 6.0, 12.0).looking_at(Vec3::ZERO, Vec3::Y),
    ));

    // A collider without RigidBody is fixed. Cuboid arguments are half-extents.
    commands.spawn((
        Name::new("Ground"),
        Collider::cuboid(8.0, 0.25, 8.0),
        Transform::from_xyz(0.0, -0.25, 0.0),
    ));

    commands.spawn((
        Name::new("Player"),
        Player,
        RigidBody::Dynamic,
        Collider::ball(0.5),
        Velocity::linear(Vec3::new(1.5, 0.0, 0.0)),
        ActiveEvents::COLLISION_EVENTS,
        Transform::from_xyz(0.0, 4.0, 0.0),
    ));
}

fn drive_player(mut bodies: Query<&mut Velocity, With<Player>>) {
    for mut velocity in &mut bodies {
        velocity.linear.x = 1.5;
    }
}

fn react_to_collisions(mut events: MessageReader<CollisionEvent>) {
    for event in events.read() {
        if let CollisionEvent::Started(a, b, _) = event {
            let _pair = (*a, *b);
        }
    }
}
```

The plugin normally runs in `PostUpdate` with `TimestepMode::Variable`. This example
deliberately moves it to `FixedUpdate`, makes Rapier's `dt` match Bevy's fixed clock,
drives bodies before `PhysicsSet::SyncBackend`, and reacts after
`PhysicsSet::Writeback`. Keep the default schedule if frame-coupled simulation is the
intent; order systems in that same schedule.

## Choose the relevant deep dive

| Problem | Read |
|---|---|
| Cargo profiles, default vs fixed/interpolated stepping, multiple worlds | [Setup and scheduling](references/setup-and-scheduling.md) |
| Body types, collider shapes, mass, units, CCD, transform authority | [Bodies and colliders](references/bodies-and-colliders.md) |
| Collision messages, sensors, groups, ray/shape queries, hooks | [Events, queries, and filtering](references/events-queries-and-filtering.md) |
| Kinematic character motion, controller output, joints | [Controllers and joints](references/controllers-and-joints.md) |
| Rollback, determinism limits, headless tests, performance evidence | [Determinism and testing](references/determinism-and-testing.md) |

## Bevy 0.20 / Rapier 0.37 gotchas

- `bevy_rapier 0.36` targets Bevy 0.19; `0.37` is the Bevy 0.20 line. `avian 0.7`
  targets 0.19; `0.8` targets 0.20. Stale output pairs `bevy = "0.20"` with `0.36`.
- The `headless` Cargo feature is gone in 0.37. `default-features = false` plus
  `dim3`/`dim2` is the headless profile; `features = ["headless"]` fails to resolve.
- `Velocity` fields are `linear` and `angular`, not `linvel` and `angvel`.
- `CollisionEvent` and `ContactForceEvent` are messages (`MessageReader`, not
  `EventReader`). At least one collider must enable the matching `ActiveEvents` flag.
- New in 0.37: `PhysicsQuarantineEvent`. Rapier disables bodies/colliders whose state
  became NaN/inf and inserts `RigidBodyDisabled`/`ColliderDisabled`. Fix the state,
  then remove that component; do not assume a silently exploded body.
- `ReadRapierContext` is a `SystemParam`; call `.single()` and handle its `Result`.
  `RapierContext` is not a resource and Rapier supports multiple worlds. Batch several
  queries under one filter with `context.with_query_pipeline(filter, |pipeline| ..)`.
- Dynamic bodies own their simulated pose. Repeatedly writing their `Transform` is a
  teleport and commonly causes jitter; write forces, impulses, or velocity instead.
- Kinematic bodies follow the trajectory you prescribe and do not avoid obstacles by
  themselves. Use scene queries or `KinematicCharacterController`.
- Rapier's default Cargo features pull Bevy asset/render crates. Disable defaults for
  headless or external-renderer builds and enable the correct `dim2`/`dim3` feature.
- Bevy 0.20 orders built-in render/UI sets with `chain_weak`; `PhysicsSet` is Rapier's
  own chained set and is unaffected. Order your systems with `.before`/`.after` on
  `PhysicsSet` as shown, never by schedule position.
- `RapierDebugRenderPlugin` is diagnostic visualization, not a renderer or a shipping
  requirement.

## See also

- [`bevy-migration-0-19-to-0-20`](../bevy-migration-0-19-to-0-20/SKILL.md) — engine-side 0.20 breakage.
- [`bevy-core-concepts`](../bevy-core-concepts/SKILL.md) — fixed schedules and ordering.
- [`bevy-rendering`](../bevy-rendering/SKILL.md) — rendering and physics ownership boundary.
- [`bevy-cameras`](../bevy-cameras/SKILL.md) — camera rays for picking and aiming.
- [Third-person orbit camera](../bevy-cameras/references/third-person-orbit.md) —
  Rapier sphere-cast obstruction and recovery hysteresis.
- [`bevy-input-actions`](../bevy-input-actions/SKILL.md) — fixed-tick movement/aim commands.
- [`bevy-testing`](../bevy-testing/SKILL.md) — deterministic app stepping and headless worlds.
- [`bevy-a11y`](../bevy-a11y/SKILL.md) — accessible movement, timing, and aim alternatives.
- [`bevy-voxel-pipeline`](../bevy-voxel-pipeline/SKILL.md) — collider proxies for voxel worlds.
