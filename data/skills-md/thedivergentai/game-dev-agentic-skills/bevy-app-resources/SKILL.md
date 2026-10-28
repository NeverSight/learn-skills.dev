---
name: bevy-app-resources
description: "Bevy ECS skill for app-wide resources and schedules. Keywords: Bevy, Resource, App, Schedule, Plugin."
---

# Bevy app resources

## When to use

Load this when data or logic must exist for the whole app: one clock, one ruleset, startup spawn, or an ordered pair of systems. Pair with bevy-data-resources for the component-versus-resource split.

## ECS shape

- **App.** The Apps page: an `App` contains a `World` and the outer loop. It initializes resources (one copy), adds systems to a `Schedule`, and imports other `App` changes through plugins.
- **Resources.** `Resource`, `Res`, `ResMut`, and `insert_resource` (Resources page). `Time` arrives from `add_plugins(DefaultPlugins)`.
- **Plugins.** The Resources page implements `Plugin` and inserts the resource inside `build`. `DefaultPlugins` is the plugin set that adds `Time`. Name only the plugins this page documents.
- **Schedules.** `add_systems(Startup, ...)` runs once before other systems. `add_systems(Update, ...)` is the repeating schedule in the ECS page. `.chain()` orders systems that must see each other's writes. `bevy::ecs::message` names `FixedUpdate` only as the schedule after which `signal_message_update_system` runs. Fixed-timestep clock types stay in bevy-character-movement.
- **States.** App-wide modes are `bevy::state`, not a global node. See bevy-state-machines.

## App choices

| Need | Bevy idiom |
| --- | --- |
| One copy for the whole app | A `Resource` inserted on the `App` |
| Logic that ticks every frame | A system on `Update` (or a chained pair) |
| Boot setup | A `Startup` system or `insert_resource` in a `Plugin` |
| One-shot notice | A message or event. See bevy-events-messaging. |

## Scope

- Insert app-wide data with `insert_resource` inside `Plugin::build`, or from a `Startup` system.
- Order two systems that both mutably use the same resource with `.chain()`.
- Save files are a `Resource` you serialize yourself. The running copy stays in the `World`.

## Examples

```toml
[package]
name = "app_resources"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.20"
```

One rules resource, one startup spawn, and a pair of systems that must not race on `Score`.

```rust
#[derive(Resource)]
struct Ruleset {
    gravity: f32,
}

#[derive(Resource, Default)]
struct Score(u32);

#[derive(Component)]
struct Falling;

fn spawn_session(mut commands: Commands) {
    commands.spawn((Name::new("session"), Transform::default(), Falling));
}

fn apply_gravity(
    rules: Res<Ruleset>,
    time: Res<Time>,
    mut bodies: Query<&mut Transform, With<Falling>>,
) {
    let step = rules.gravity * time.delta_secs();
    for mut transform in &mut bodies {
        transform.translation.y += step;
    }
}

fn award(mut score: ResMut<Score>) {
    score.0 = score.0.saturating_add(1);
}

fn publish(score: Res<Score>, mut bodies: Query<&mut Transform, With<Falling>>) {
    let lift = score.0 as f32;
    for mut transform in &mut bodies {
        transform.translation.x = lift;
    }
}

pub struct RulesPlugin;

impl Plugin for RulesPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(Ruleset { gravity: -9.8 })
            .init_resource::<Score>()
            .add_systems(Startup, spawn_session)
            .add_systems(Update, (apply_gravity, award, publish).chain());
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(RulesPlugin)
        .run();
}
```

`award` and `publish` both touch `Score` or `Transform`. `apply_gravity` also writes `Transform`, so the three systems stay in one chain.

A second plugin only reads the rules resource.

```rust
#[derive(Resource)]
struct Ruleset {
    gravity: f32,
}

fn log_rules(rules: Res<Ruleset>) {
    let _gravity = rules.gravity;
}

pub struct HudPlugin;

impl Plugin for HudPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Update, log_rules);
    }
}
```

Fixed-step simulation reads `Time<Fixed>` and stays on `FixedUpdate`.

```rust
#[derive(Component)]
struct Falling;

fn fixed_step(time: Res<Time<Fixed>>, mut bodies: Query<&mut Transform, With<Falling>>) {
    let step = time.delta_secs();
    for mut transform in &mut bodies {
        transform.translation.z += step;
    }
}

pub struct FixedRulesPlugin;

impl Plugin for FixedRulesPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(FixedUpdate, fixed_step);
    }
}
```

`fixed_step` owns `Falling` in this module. The startup example uses its own `Falling` marker.

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

- No process-global static for app data. WHY: a `Resource` on the `App` is the single owner, and systems borrow it through `Res` or `ResMut`.
- No invented plugin lists beyond `DefaultPlugins` and the `Plugin` trait the Resources page uses. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No third-party crates. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Permalinks stay unversioned.

### Official Documentation
- [Apps](https://bevy.org/learn/quick-start/getting-started/apps/)  -  `App`, `World`, resources, `Schedule`, plugins.
- [Resources](https://bevy.org/learn/quick-start/getting-started/resources/)  -  `Resource`, `insert_resource`, `Plugin::build`, `DefaultPlugins`, `Time`.
- [Quick Start: ECS](https://bevy.org/learn/quick-start/getting-started/ecs/)  -  `Startup`, `Update`, `add_systems`, `.chain()`.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples)  -  Example tree on the `latest` branch.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Hub and schedules.
- [bevy-project-foundations](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-project-foundations/SKILL.md)  -  Crate and `App::new()`.

#### Complements
- [bevy-data-resources](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-data-resources/SKILL.md)  -  When data is a component instead of a resource.
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md)  -  App-wide `States` for mode changes.

#### Downstream / consumers
- Save, audio, and scene skills cover persistence, playback, and scene spawn.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md)  -  Bevy router.
