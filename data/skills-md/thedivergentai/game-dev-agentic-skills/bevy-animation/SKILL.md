---
name: bevy-animation
description: "Bevy ECS skill for animation playback. Keywords: Bevy, AnimationPlayer, AnimationClip, AnimationPlugin, animate_targets."
---

# Bevy animation playback

## When to use

Load this when an entity should play an AnimationClip. Blend graphs belong on bevy-animation-graph. 2D sprite specifics belong on bevy-2d-animation.

## ECS shape

- **Components:** `AnimationPlayer` controls playback. `AnimatedBy` links a target entity to the player entity. `AnimationTargetId` selects which curves apply.
- **Assets:** `AnimationClip` holds `VariableCurve` entries.
- **Systems:** `advance_animations` advances time. `animate_targets` writes the curves. `AnimationPlugin` adds animation support.
- **Events:** `AnimationEvent` can be triggered from a clip. Check the animation docs for observer wiring beyond the trait name.

## Playback pieces

| Need | Bevy idiom |
| --- | --- |
| Who advances time | `AnimationPlayer` on an entity |
| Clip asset | `AnimationClip` inside an `AnimationGraph` node |
| Which bone or field | `AnimationTargetId` plus `AnimatedBy` |
| Repeat | `ActiveAnimation::repeat`, which sets `RepeatAnimation::Forever` |

## Examples

```toml
[dependencies]
bevy = "0.20"
```

`AnimationPlayer::play` takes an `AnimationNodeIndex` from an `AnimationGraph`, not a clip handle. `AnimationGraph::from_clip` builds that one-node graph. `AnimatedBy` points the target at the player entity. `AnimationTargetId::from_name` selects the curves for that name.

```rust
use bevy::animation::{AnimatedBy, AnimationTargetId};

#[derive(Resource)]
struct WalkNode(AnimationNodeIndex);

fn setup_walk(
    mut commands: Commands,
    mut clips: ResMut<Assets<AnimationClip>>,
    mut graphs: ResMut<Assets<AnimationGraph>>,
) {
    let clip = clips.add(AnimationClip::default());
    let (graph, index) = AnimationGraph::from_clip(clip);
    let player = commands
        .spawn((
            AnimationPlayer::default(),
            AnimationGraphHandle(graphs.add(graph)),
        ))
        .id();
    commands.spawn((
        AnimatedBy(player),
        AnimationTargetId::from_name(&Name::new("Hips")),
        Transform::default(),
    ));
    commands.insert_resource(WalkNode(index));
}

fn play_loop(mut players: Query<&mut AnimationPlayer>, walk: Res<WalkNode>) {
    for mut player in &mut players {
        player.play(walk.0).repeat();
    }
}
```

Pause, resume, and seek act on every active clip on that player.

```rust
fn pause_players(mut players: Query<&mut AnimationPlayer>) {
    for mut player in &mut players {
        player.pause_all();
    }
}

fn resume_and_seek(mut players: Query<&mut AnimationPlayer>) {
    for mut player in &mut players {
        player.resume_all().seek_all_by(0.25);
    }
}
```

Stop one node, or ask whether it is still active, without touching the other clips on the same player.

```rust
fn stop_walk(mut players: Query<&mut AnimationPlayer>, walk: Res<WalkNode>) {
    for mut player in &mut players {
        if player.is_playing_animation(walk.0) {
            player.stop(walk.0);
        }
    }
}

#[derive(Resource)]
struct WalkNode(AnimationNodeIndex);
```

Scale every active clip on the player. glTF files load as `AnimationClip` assets; this player plays the graph node that holds that clip.

```rust
fn slow_motion(mut players: Query<&mut AnimationPlayer>) {
    for mut player in &mut players {
        player.adjust_speeds(0.5);
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

- Do not pass an `AnimationClip` handle to `AnimationPlayer::play`. WHY: `play` takes an `AnimationNodeIndex` from the graph built with `AnimationGraph::from_clip`.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Permalinks stay unversioned.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [Animation examples](https://github.com/bevyengine/bevy/tree/latest/examples/animation) - Player, graph, and glTF clip samples.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.

#### Complements
- [bevy-animation-graph](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-animation-graph/SKILL.md) - Blend instead of a single clip.
- [bevy-2d-animation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-2d-animation/SKILL.md) - Sprite targets.
- [bevy-asset-scenes](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-asset-scenes/SKILL.md) - Load clip assets.

#### Downstream / consumers
- [bevy-animation-graph](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-animation-graph/SKILL.md) - Consumes clips.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
