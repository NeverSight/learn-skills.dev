---
name: bevy-tweening
description: "Bevy ECS skill for tween and juice. Keywords: Bevy, tween, juice, curve, ECS."
---

# Bevy tweening

## When to use

Load this when a value should ease over time. A tween player is yours to build in ECS from elapsed time.

## ECS shape

- **Feature:** `EasingCurve` samples an ease between two values. It is not a player that stores entity state.
- **Components:** a tween you own: start, end, elapsed, and duration.
- **Systems:** step elapsed time on `Update` with `Time::delta_secs`, then write `Transform`.
- **Animation:** property animation over a clip is `AnimationClip` on bevy-animation. That is a clip, not a one-shot UI tween.

```toml
[dependencies]
bevy = "0.20"
```

One system advances elapsed time. The eased `t` is `EasingCurve::sample_clamped`. Finished tweens are despawned by the marker, not by a callback type.

```rust
use bevy::curve::Curve;
use bevy::curve::easing::{EaseFunction, EasingCurve};

#[derive(Component)]
struct Slide {
    start: Vec3,
    end: Vec3,
    elapsed: f32,
    duration: f32,
}

fn spawn_slide(mut commands: Commands) {
    commands.spawn((
        Transform::from_translation(Vec3::ZERO),
        Slide {
            start: Vec3::ZERO,
            end: Vec3::new(2.0, 1.0, 0.0),
            elapsed: 0.0,
            duration: 0.6,
        },
    ));
}

fn step_slides(
    time: Res<Time>,
    mut slides: Query<(Entity, &mut Slide, &mut Transform)>,
    mut commands: Commands,
) {
    let curve = EasingCurve::new(0.0, 1.0, EaseFunction::QuadraticOut);
    for (entity, mut slide, mut transform) in &mut slides {
        slide.elapsed = (slide.elapsed + time.delta_secs()).min(slide.duration);
        let t = if slide.duration <= 0.0 {
            1.0
        } else {
            slide.elapsed / slide.duration
        };
        let eased = curve.sample_clamped(t);
        transform.translation = slide.start.lerp(slide.end, eased);
        if slide.elapsed >= slide.duration {
            commands.entity(entity).remove::<Slide>();
        }
    }
}

pub struct JuicePlugin;

impl Plugin for JuicePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_slide)
            .add_systems(Update, step_slides);
    }
}
```

A punch scale uses the same clock and a different ease. When elapsed reaches duration, the marker comes off so later systems stop writing that transform.

```rust
use bevy::curve::Curve;
use bevy::curve::easing::{EaseFunction, EasingCurve};

#[derive(Component)]
struct Punch {
    elapsed: f32,
    duration: f32,
    amount: f32,
}

fn step_punch(time: Res<Time>, mut punches: Query<(Entity, &mut Punch, &mut Transform)>, mut commands: Commands) {
    let curve = EasingCurve::new(0.0, 1.0, EaseFunction::CubicOut);
    for (entity, mut punch, mut transform) in &mut punches {
        punch.elapsed = (punch.elapsed + time.delta_secs()).min(punch.duration);
        let t = punch.elapsed / punch.duration.max(0.0001);
        let eased = curve.sample_clamped(t);
        let scale = 1.0 + punch.amount * (1.0 - eased);
        transform.scale = Vec3::splat(scale);
        if punch.elapsed >= punch.duration {
            commands.entity(entity).remove::<Punch>();
        }
    }
}
```

Delay then move is two components. The delay system inserts `Slide` only after its timer ends, so the order is data, not a sequence asset.

```rust
#[derive(Component)]
struct Slide {
    start: Vec3,
    end: Vec3,
    elapsed: f32,
    duration: f32,
}

#[derive(Component)]
struct Wait {
    remaining: f32,
    end: Vec3,
}

fn release_waits(time: Res<Time>, mut waits: Query<(Entity, &mut Wait)>, mut commands: Commands) {
    for (entity, mut wait) in &mut waits {
        wait.remaining -= time.delta_secs();
        if wait.remaining <= 0.0 {
            commands.entity(entity).insert(Slide {
                start: Vec3::ZERO,
                end: wait.end,
                elapsed: 0.0,
                duration: 0.4,
            });
            commands.entity(entity).remove::<Wait>();
        }
    }
}
```

## Choose the owner

| Need | Owner |
| --- | --- |
| Property tween | `Slide` plus `EasingCurve` writing `Transform`. |
| Sequence | A `Wait` component that inserts `Slide` when it elapses. |
| Finish | Remove the marker when `elapsed` reaches `duration`. Clip events stay on bevy-animation. |

## Scope

- `EasingCurve::sample_clamped` is the ease used above. `EaseFunction::QuadraticOut` and `EaseFunction::CubicOut` are two of the built-in curves.
- The player is the `Slide` / `Punch` / `Wait` components. A third-party tween crate is optional and is not required for this pattern.

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
| Per-entity data | `Component` + `Query` | A value that is not a component |
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

- No Godot Tween node. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No named tween crate as the chosen solution. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

- No Godot types in Bevy code. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.
- [bevy-animation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-animation/SKILL.md) - Clip-based property animation.
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Fixed clock name.

#### Complements
- [godot-tweening](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-tweening/SKILL.md) - Equivalent Godot skill.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
