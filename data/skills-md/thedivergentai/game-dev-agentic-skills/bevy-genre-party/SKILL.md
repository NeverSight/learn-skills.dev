---
name: bevy-genre-party
description: "Bevy 0.20 party router: local seats, shared scores, and minigame swaps as ECS data. Use when routing a local party game. Keywords: Bevy, Party, minigame, score, ECS, router."
---

# Bevy Party (thin router)

Genre router. Domain work lives in the Bevy skills below.

## When to use

Load this for local minigame swaps and shared scores.

## ECS shape

- **Components** hold the genre's per-entity flags as plain data. This file does not name new engine types.
- **Resources** hold run-wide counters (score, wave index, seed) via bevy-data-resources.
- **Systems** read those components on `Update` or the fixed timestep from bevy-master. Order them with `.chain()` when a later system must see the result.
- **Schedule:** gameplay mode changes go through bevy-state-machines. This file registers only seat scores and the minigame swap.

## Routing

- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Minigame mode.
- [bevy-input-handling](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-input-handling/SKILL.md) - Local devices. Gamepad exists.
- [bevy-game-loop-time-trial](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-game-loop-time-trial/SKILL.md) - When a minigame is timed.

## Scope

Local seats, the shared board, and the current minigame are plain data. Mode machines, devices, and timed rounds stay in the skills linked above.

| Call | Owner here | Leave to the linked skill |
| --- | --- | --- |
| One seat earns the round | `PartyBoard.award_pending`, then clear it | Input devices in bevy-input-handling |
| Hub opens a race | `CurrentMinigame` on a just-pressed key | The state machine in bevy-state-machines |
| Score mode ends | bump `round` and the active seat, then return to hub | The timer in bevy-game-loop-time-trial |

```toml
[dependencies]
bevy = "0.20"
```

```rust
#[derive(Component)]
struct LocalSeat {
    index: u8,
    score: i32,
}

#[derive(Resource)]
struct PartyBoard {
    active: u8,
    round: u32,
    award_pending: bool,
}

fn award(mut board: ResMut<PartyBoard>, mut seats: Query<&mut LocalSeat>) {
    if !board.award_pending {
        return;
    }
    board.award_pending = false;
    for mut seat in &mut seats {
        if seat.index == board.active {
            seat.score += 1;
        }
    }
}

pub struct ScorePlugin;

impl Plugin for ScorePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(PartyBoard {
            active: 0,
            round: 1,
            award_pending: true,
        })
        .add_systems(Update, award);
    }
}
```

```rust
#[derive(Resource)]
struct PartyBoard {
    active: u8,
    round: u32,
    award_pending: bool,
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum Minigame {
    Hub,
    Race,
    Score,
}

#[derive(Resource)]
struct CurrentMinigame(Minigame);

fn open_race(keys: Res<ButtonInput<KeyCode>>, mut current: ResMut<CurrentMinigame>) {
    if keys.just_pressed(KeyCode::Digit1) && current.0 == Minigame::Hub {
        current.0 = Minigame::Race;
    }
}

fn advance_round(
    keys: Res<ButtonInput<KeyCode>>,
    mut current: ResMut<CurrentMinigame>,
    mut board: ResMut<PartyBoard>,
) {
    if keys.just_pressed(KeyCode::Digit2) && current.0 == Minigame::Score {
        board.round += 1;
        board.active = board.active.wrapping_add(1) % 4;
        board.award_pending = true;
        current.0 = Minigame::Hub;
    }
}

pub struct MinigamePlugin;

impl Plugin for MinigamePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(CurrentMinigame(Minigame::Hub))
            .add_systems(Update, (open_race, advance_round).chain());
    }
}
```

```rust
#[derive(Component)]
struct LocalSeat {
    index: u8,
    score: i32,
}

fn join_seat(keys: Res<ButtonInput<KeyCode>>, mut commands: Commands, seats: Query<&LocalSeat>) {
    if keys.just_pressed(KeyCode::KeyJ) {
        let index = seats.iter().count() as u8;
        if index < 4 {
            commands.spawn(LocalSeat { index, score: 0 });
        }
    }
}

pub struct JoinPlugin;

impl Plugin for JoinPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Update, join_seat);
    }
}

fn main() {
    App::new()
        .add_plugins(MinimalPlugins)
        .add_plugins(JoinPlugin)
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

- Do not add to a seat score every frame. WHY: the board flag awards once, then clears, so the active seat does not climb for free.
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
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Minigame mode.
- [bevy-input-handling](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-input-handling/SKILL.md) - Local devices. Gamepad exists.
- [bevy-game-loop-time-trial](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-game-loop-time-trial/SKILL.md) - When a minigame is timed.

#### Downstream / consumers
- None. This router does not own a second implementation.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
