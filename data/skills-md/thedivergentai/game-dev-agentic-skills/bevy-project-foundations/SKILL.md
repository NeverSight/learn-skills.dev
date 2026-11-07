---
name: bevy-project-foundations
description: "Pins a Bevy 0.20 crate, dev-profile opt-level, and plugin boundaries before gameplay systems exist. Use when starting a windowed or headless Bevy app. Keywords: Bevy, Cargo.toml, DefaultPlugins, MinimalPlugins, opt-level."
---

# Bevy project foundations

## When to use

Load this when a new Bevy app needs a crate, a pin, and a place for feature code before gameplay systems exist. Folder names below are layout habits. They are not engine types.

## ECS shape

- **Crate:** `cargo new` plus a `bevy` dependency pinned at **0.20**.
- **Features:** `default` pulls windowing, input, and rendering. Turn `default-features` off only when the binary should stay headless.
- **App shell:** `App::new()`, plugins, then systems and resources on that `App`.
- **Code layout:** Split by feature in ordinary Rust modules. The engine does not require a directory tree.

Pin the crate and keep dev builds usable. Bevy's default debug profile compiles dependencies unoptimized, so the dev profile lifts dependency `opt-level` while the game crate stays easy to step through.

```toml
[package]
name = "game"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.20"

[profile.dev]
opt-level = 1

[profile.dev.package."*"]
opt-level = 3
```

A headless tool crate drops the default feature set and adds only what that binary calls.

```toml
[dependencies]
bevy = { version = "0.20", default-features = false }
```

The windowed game plugs `DefaultPlugins` and a feature plugin. `GameConfig` is app-wide state inserted before the first schedule runs.

```rust
#[derive(Resource)]
struct GameConfig {
    title: String,
}

fn boot(config: Res<GameConfig>) {
    let _title = config.title.as_str();
}

pub struct GamePlugin;

impl Plugin for GamePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(GameConfig {
            title: "Game".to_string(),
        })
        .add_systems(Startup, boot);
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(GamePlugin)
        .run();
}
```

A second module owns one feature. The plugin is the boundary. Systems stay in the module that declares their components.

```rust
#[derive(Component)]
struct Player;

fn spawn_player(mut commands: Commands) {
    commands.spawn(Player);
}

pub struct PlayerPlugin;

impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_player);
    }
}
```

## Layout choices

| Need | Bevy idiom |
| --- | --- |
| New crate | `cargo new` plus the `bevy` dependency |
| Window, input, rendering | Cargo features and profiles on the `bevy` crate |
| Feature split | Rust modules you choose |
| Project file | `Cargo.toml` plus Rust modules |

## Scope

- Pin `bevy = "0.20"` in `Cargo.toml`. `DefaultPlugins` brings the window, input, and audio backends that crate feature enables.
- Workspace members and naming linters are ordinary Cargo. This skill does not invent a folder enforcer.

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
| Per-entity data | `Component` + `Query` | A free-floating struct outside the `World` |
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

- No scene-tree project types or autoload singletons in this crate. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented Cargo features beyond the profiles this skill names. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No third-party crates. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20**.

### Official Documentation
- [Getting started](https://bevy.org/learn/quick-start/getting-started/)  -  `cargo new` / `cargo add bevy`.
- [Apps](https://bevy.org/learn/quick-start/getting-started/apps/)  -  `App::new()`, `World`, and `Schedule`.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples)  -  Example tree on the `latest` branch.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Library pin and which Bevy skill to load next.

#### Complements
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md)  -  Entities, components, and systems after the crate exists.

#### Downstream / consumers
- [bevy-app-resources](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-app-resources/SKILL.md)  -  App-wide resources once the `App` exists.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Bevy router.
