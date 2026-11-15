---
name: bevy-2d-animation
description: "Bevy ECS skill for 2D sprite animation. Keywords: Bevy, sprite, animation, AnimationPlayer, AnimationClip, 2D."
---

# Bevy 2D animation

## When to use

Load this when a 2D actor needs clip playback on a sprite entity. Pair with bevy-animation for the player and clip types. Pair with bevy-animation-graph when clips must blend.

## ECS shape

- **Components:** `Sprite` (bevy::sprite) on the visible entity. `AnimationPlayer` and `AnimationTargetId` / `AnimatedBy` (bevy::animation) link a clip to that entity.
- **Resources:** clip assets are `AnimationClip` handles, not a global player.
- **Systems:** `advance_animations` and `animate_targets` are the engine systems named on the animation page. Gameplay code should not reimplement them.
- **Schedule:** those systems are engine-owned. Gameplay that reacts to a finished clip chains after them.

## Playback choices

| Need | Bevy idiom |
| --- | --- |
| Frame cells | `Sprite` with `texture_atlas: Some(TextureAtlas { .. })`, or an `AnimationClip` curve. |
| Named cutout limb | `AnimationTargetId::from_name` / `from_names` selects which entity a curve writes. |
| Loop | `ActiveAnimation::repeat` sets `RepeatAnimation::Forever`. |

## Scope

- Frame sheets use `Sprite::from_atlas_image` and `TextureAtlas`. Clip curves use `animated_field!` plus `AnimatableCurve`.
- A cutout limb is an entity with `AnimationTargetId` and `AnimatedBy` pointing at the entity that owns `AnimationPlayer`.

## Examples

Atlas frame on a sprite. `TextureAtlas.index` is the cell.

```rust
fn spawn_sheet(
    mut commands: Commands,
    assets: Res<AssetServer>,
    mut layouts: ResMut<Assets<TextureAtlasLayout>>,
) {
    let layout = TextureAtlasLayout::from_grid(UVec2::splat(32), 4, 1, None, None);
    let layout = layouts.add(layout);
    let image = assets.load("actor.png");
    commands.spawn((
        Sprite::from_atlas_image(image, TextureAtlas { layout, index: 0 }),
        FrameClock {
            timer: Timer::from_seconds(0.12, TimerMode::Repeating),
            frames: 4,
        },
    ));
}

#[derive(Component)]
struct FrameClock {
    timer: Timer,
    frames: usize,
}

fn tick_frames(time: Res<Time>, mut sprites: Query<(&mut Sprite, &mut FrameClock)>) {
    for (mut sprite, mut clock) in &mut sprites {
        clock.timer.tick(time.delta());
        if clock.timer.just_finished() {
            if let Some(atlas) = sprite.texture_atlas.as_mut() {
                atlas.index = (atlas.index + 1) % clock.frames;
            }
        }
    }
}
```

Clip playback. The player stores an `AnimationNodeIndex` from the graph, not a raw clip handle.

```rust
use bevy::animation::animated_field;
use bevy::animation::{AnimatedBy, AnimationTargetId};

#[derive(Component)]
struct IdleNode(AnimationNodeIndex);

fn spawn_clip(
    mut commands: Commands,
    mut clips: ResMut<Assets<AnimationClip>>,
    mut graphs: ResMut<Assets<AnimationGraph>>,
) {
    let name = Name::new("actor");
    let target = AnimationTargetId::from_name(&name);
    let samples = UnevenSampleAutoCurve::new([
        (0.0, Vec3::ZERO),
        (0.4, Vec3::new(8.0, 0.0, 0.0)),
    ])
    .expect("two samples");
    let mut clip = AnimationClip::default();
    clip.add_curve_to_target(
        target,
        AnimatableCurve::new(animated_field!(Transform::translation), samples),
    );
    let clip_handle = clips.add(clip);
    let (graph, indices) = AnimationGraph::from_clips([clip_handle]);
    let idle = indices[0];
    let graph_handle = graphs.add(graph);
    let player = commands
        .spawn((
            name,
            Sprite::from_color(Color::WHITE, Vec2::splat(32.0)),
            AnimationPlayer::default(),
            AnimationGraphHandle(graph_handle),
            target,
            IdleNode(idle),
        ))
        .id();
    commands.entity(player).insert(AnimatedBy(player));
}

fn play_idle(mut actors: Query<(&mut AnimationPlayer, &IdleNode)>) {
    for (mut player, idle) in &mut actors {
        player.play(idle.0).repeat();
    }
}

fn cutout_id(root: &Name, limb: &Name) -> AnimationTargetId {
    AnimationTargetId::from_names([root, limb].into_iter())
}
```

Facing and frame ticks both write `Sprite`, so they share one chain.

```rust
fn face_keys(keys: Res<ButtonInput<KeyCode>>, mut sprites: Query<&mut Sprite>) {
    let left = keys.pressed(KeyCode::KeyA);
    let right = keys.pressed(KeyCode::KeyD);
    if !left && !right {
        return;
    }
    for mut sprite in &mut sprites {
        sprite.flip_x = left;
    }
}

#[derive(Component)]
struct SheetClock {
    timer: Timer,
    frames: usize,
}

fn advance_sheet(time: Res<Time>, mut sprites: Query<(&mut Sprite, &mut SheetClock)>) {
    for (mut sprite, mut clock) in &mut sprites {
        clock.timer.tick(time.delta());
        if clock.timer.just_finished() {
            if let Some(atlas) = sprite.texture_atlas.as_mut() {
                atlas.index = (atlas.index + 1) % clock.frames;
            }
        }
    }
}

pub struct SpriteAnimPlugin;

impl Plugin for SpriteAnimPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Update, (face_keys, advance_sheet).chain());
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
| Per-entity data | `Component` + `Query` | A value stored off the entity |
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

- No sprite-frame type outside `Sprite`, `TextureAtlas`, and `AnimationClip`. WHY: those are the documented owners of a 2D frame and a sampled curve.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Permalinks stay unversioned.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [2D examples](https://github.com/bevyengine/bevy/tree/latest/examples/2d) - Sprite and atlas samples.
- [Animation examples](https://github.com/bevyengine/bevy/tree/latest/examples/animation) - `AnimationPlayer`, clips, and graphs.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.
- [bevy-animation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-animation/SKILL.md) - AnimationPlayer and AnimationClip.

#### Complements
- [bevy-animation-graph](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-animation-graph/SKILL.md) - Blend clips.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
