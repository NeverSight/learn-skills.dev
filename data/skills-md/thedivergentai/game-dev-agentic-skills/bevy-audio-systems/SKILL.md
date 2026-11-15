---
name: bevy-audio-systems
description: "Bevy ECS skill for audio playback. Keywords: Bevy, AudioPlayer, AudioSink, PlaybackSettings, AssetServer."
---

# Bevy audio systems

## When to use

Load this when a clip should start, loop, pause, or change volume. `bevy::audio` in Bevy 0.20 and the `audio_control` example are the sources.

## ECS shape

- **Play:** spawn `AudioPlayer::new(asset_server.load(...))`. `AudioPlayer<Source>` holds `Handle<Source>` where `Source: Asset + Decodable`. If the asset is not ready, playback starts when it is. `AudioPlayer` requires `PlaybackSettings`.
- **Settings:** `PlaybackSettings` configures the start. `PlaybackSettings::LOOP` and `.with_spatial(true)` appear in the spatial examples. Changes to `PlaybackSettings` do not affect audio that is already playing. `PlaybackMode` is `Once`, `Loop`, `Despawn`, or `Remove`.
- **Control:** when playback begins, Bevy inserts `AudioSink`. The control example queries `AudioSink` and calls `pause`, `toggle_mute`, `set_volume`, `set_speed`, and `position`. `SpatialAudioSink` is the spatial counterpart named on the playback page.
- **Replay:** after a non-looping sound finishes and the sink is drained, that `AudioPlayer` cannot be reused. Remove the audio components and add them again.
- **Schedule:** spawn on `Startup` or from a system that has `Res<AssetServer>` and `Commands`. Control systems in the example run where they read `ButtonInput<KeyCode>` and `Res<Time>`.

## Playback pieces

| Need | Bevy idiom |
| --- | --- |
| Start a file | `AudioPlayer::new` plus `AssetServer::load` |
| Loop | `PlaybackSettings::LOOP` |
| Pause, mute, or volume while playing | `AudioSink` methods on the same entity |
| One-shot that should leave the world | `PlaybackMode::Despawn` or `Remove` |
| Positional emitter | `PlaybackSettings` with `with_spatial(true)` and `SpatialAudioSink` |

## Examples

```toml
[dependencies]
bevy = "0.20"
```

`AudioPlayer` starts when the handle is ready. `PlaybackSettings` applies only at that start. `AudioSink` is inserted once playback begins and is the live control.

```rust
use bevy::audio::{AudioSinkPlayback, Volume};

fn spawn_music(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        AudioPlayer::new(asset_server.load("audio/music.ogg")),
        PlaybackSettings::LOOP.with_volume(Volume::Linear(0.6)),
    ));
}

fn spawn_oneshot(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        AudioPlayer::new(asset_server.load("audio/ui.ogg")),
        PlaybackSettings::DESPAWN,
    ));
}

fn duck_music(mut sinks: Query<&mut AudioSink>) {
    for mut sink in &mut sinks {
        sink.set_volume(Volume::Linear(0.25));
        sink.pause();
    }
}
```

A positional emitter sets `with_spatial(true)` and a `Transform`. Live control of that emitter uses `SpatialAudioSink`.

```rust
use bevy::audio::{AudioSinkPlayback, Volume};

fn spawn_footstep(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        AudioPlayer::new(asset_server.load("audio/step.ogg")),
        PlaybackSettings::ONCE.with_spatial(true),
        Transform::from_xyz(3.0, 0.0, 1.0),
    ));
}

fn quiet_nearby(mut sinks: Query<&mut SpatialAudioSink>) {
    for mut sink in &mut sinks {
        sink.set_volume(Volume::Linear(0.5));
    }
}
```

A finished non-looping player cannot be reused. Drop the player and the sink, then insert them again with the same handle.

```rust
use bevy::audio::AudioSinkPlayback;

fn replay_when_empty(mut commands: Commands, playing: Query<(Entity, &AudioPlayer, &AudioSink)>) {
    for (entity, player, sink) in &playing {
        if !sink.empty() {
            continue;
        }
        let handle = player.0.clone();
        commands.entity(entity).remove::<AudioPlayer>().remove::<AudioSink>();
        commands.entity(entity).insert((
            AudioPlayer::new(handle),
            PlaybackSettings::ONCE,
        ));
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

- Do not change `PlaybackSettings` to retune audio that is already playing. WHY: those settings apply only when playback starts; live control is `AudioSink`.
- No volume curves or mixer nodes this file did not open. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No third-party audio crates. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Permalinks stay unversioned.

### Official Documentation
- [Assets](https://bevy.org/assets/)  -  Official asset catalog.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples)  -  Example tree on the `latest` branch.
- [Audio examples](https://github.com/bevyengine/bevy/tree/latest/examples/audio)  -  Playback, spatial, and control samples.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/)  -  `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Who owns which piece of state.
- [bevy-asset-scenes](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-asset-scenes/SKILL.md)  -  `AssetServer` and `Handle`.

#### Complements
- [bevy-input-handling](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-input-handling/SKILL.md)  -  Keys the control example uses.

#### Downstream / consumers
- None yet. Genre skills that play stingers should route here when they exist.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Bevy router.
