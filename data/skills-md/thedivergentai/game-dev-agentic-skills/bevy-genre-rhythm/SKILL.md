---
name: bevy-genre-rhythm
description: "Bevy 0.20 rhythm router: chart notes, a song clock, and hit windows as ECS data. Use when routing a rhythm game. Keywords: Bevy, Rhythm, chart, hit window, ECS, router."
---

# Bevy Rhythm (thin router)

Genre router. Domain work lives in the Bevy skills below.

## When to use

Load this for chart time and hit windows aligned to audio.

## ECS shape

- **Components** hold the genre's per-entity flags as plain data. This file does not name new engine types.
- **Resources** hold run-wide counters (score, wave index, seed) via bevy-data-resources.
- **Systems** read those components on `Update` or the fixed timestep from bevy-master. Order them with `.chain()` when a later system must see the result.
- **Schedule:** gameplay mode changes go through bevy-state-machines. This file registers only the chart clock and the hit judge.

## Routing

- [bevy-audio-systems](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-audio-systems/SKILL.md) - Music playback.
- [bevy-input-handling](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-input-handling/SKILL.md) - Hits.
- [bevy-game-loop-time-trial](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-game-loop-time-trial/SKILL.md) - Score time.

## Scope

Chart notes, the song clock, and hit windows live here. Playback, input devices, and score presentation stay in the skills linked above.

| Call | Owner here | Leave to the linked skill |
| --- | --- | --- |
| Song time advances | `ChartClock` from `Time::delta_secs` | Playback in bevy-audio-systems |
| Lane press inside the tight window | `ChartNote.grade = 2` | Device mapping in bevy-input-handling |
| Lane press inside only the wide window | `ChartNote.grade = 1` | Score presentation in bevy-game-loop-time-trial |

```toml
[dependencies]
bevy = "0.20"
```

```rust
#[derive(Component)]
struct ChartNote {
    hit_at: f32,
    lane: u8,
    judged: bool,
}

#[derive(Resource)]
struct HitWindow {
    perfect: f32,
    good: f32,
}

#[derive(Resource, Default)]
struct ChartClock(f32);

fn advance_chart(time: Res<Time>, mut clock: ResMut<ChartClock>) {
    clock.0 += time.delta_secs();
}

pub struct ClockPlugin;

impl Plugin for ClockPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<ChartClock>()
            .add_systems(Update, advance_chart);
    }
}
```

```rust
#[derive(Component)]
struct ChartNote {
    hit_at: f32,
    lane: u8,
    judged: bool,
    grade: u8,
}

#[derive(Resource)]
struct HitWindow {
    perfect: f32,
    good: f32,
}

#[derive(Resource, Default)]
struct ChartClock(f32);

fn judge(
    keys: Res<ButtonInput<KeyCode>>,
    clock: Res<ChartClock>,
    window: Res<HitWindow>,
    mut notes: Query<&mut ChartNote>,
) {
    if !keys.just_pressed(KeyCode::KeyF) {
        return;
    }
    for mut note in &mut notes {
        if note.judged || note.lane != 0 {
            continue;
        }
        let delta = (clock.0 - note.hit_at).abs();
        if delta <= window.perfect {
            note.judged = true;
            note.grade = 2;
        } else if delta <= window.good {
            note.judged = true;
            note.grade = 1;
        }
    }
}

pub struct JudgePlugin;

impl Plugin for JudgePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(HitWindow {
            perfect: 0.04,
            good: 0.09,
        })
        .add_systems(Update, judge);
    }
}
```

```rust
#[derive(Component)]
struct ChartNote {
    hit_at: f32,
    lane: u8,
    judged: bool,
    grade: u8,
}

fn spawn_chart(mut commands: Commands) {
    for (index, lane) in [0u8, 1, 0, 2].into_iter().enumerate() {
        commands.spawn(ChartNote {
            hit_at: 1.0 + index as f32 * 0.5,
            lane,
            judged: false,
            grade: 0,
        });
    }
}

pub struct ChartPlugin;

impl Plugin for ChartPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_chart);
    }
}

fn main() {
    App::new()
        .add_plugins(MinimalPlugins)
        .add_plugins(ChartPlugin)
        .run();
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
| Per-entity data | `Component` + `Query` | One mutable blob shared by every entity |
| App-wide config or clock | `Resource` | Copy the value onto every entity |
| Stable simulation step | `FixedMain` and the `Fixed` clock | Tie simulation to raw frame `Update` |
| Startup spawn | `Commands` in `Startup` | Spawn from a render system |
| Cross-system notice that is not shared state | Message or observer slot in `bevy-events-messaging` | A new event type invented in this file |
| Behavior a linked domain skill already owns | Keep this router to components and resources | A second implementation in this file |

Load [references/ecs-ownership.md](references/ecs-ownership.md) for the ownership table.

## NEVER

- Do not pin `/0.20.0/` in docs URLs. WHY: links stay on `latest`; the 0.20 target is stated once in prose.
- Do not mutably query the same component from two unordered systems. WHY: the schedule runs systems in parallel unless `.chain()` orders them.
- Do not invent a physics, navigation, networking, or XR crate here. WHY: this skill only names documented Bevy crates and modules.

- Do not treat every press inside the wide window as perfect. WHY: the tight window writes grade 2 and the wide window writes grade 1.
- No invented genre APIs. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- Do not pick a physics or net crate here. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Official pages stay on the unversioned site.

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
- [bevy-audio-systems](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-audio-systems/SKILL.md) - Music playback.
- [bevy-input-handling](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-input-handling/SKILL.md) - Hits.
- [bevy-game-loop-time-trial](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-game-loop-time-trial/SKILL.md) - Score time.

#### Downstream / consumers
- None. This router does not own a second implementation.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
