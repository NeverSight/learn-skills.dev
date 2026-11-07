---
name: bevy-rpg-stats
description: "Bevy ECS skill for character stats. Keywords: Bevy, stats, attributes, modifiers, ECS."
---

# Bevy RPG stats

## When to use

Load this when attributes, modifiers, or derived numbers live on an actor. Combat applies them via bevy-combat-system.

## ECS shape

- **Components:** base attributes, a modifier list, and current health on the actor.
- **Resources:** the level curve is one resource for the whole run (bevy-data-resources).
- **Systems:** recompute max health when `Attributes` change. An `IncomingHit` or `XpGain` is a component removed after it is applied. `.chain()` so a vitality gain runs before the health sync.
- **Messages:** one-shot facts (hit, pickup, quest advance) go through bevy-events-messaging.

```toml
[dependencies]
bevy = "0.20"
serde = { version = "1", features = ["derive"] }
ron = "0.10"
```

Attributes and modifiers live on the actor. Derived attack is a function, not a second source of truth.

```rust
#[derive(Component, Clone, Copy)]
struct Attributes {
    strength: i32,
    vitality: i32,
}

enum ModKind {
    Add,
    Mul,
}

struct Modifier {
    kind: ModKind,
    amount: f32,
}

#[derive(Component)]
struct ModifierList(Vec<Modifier>);

fn derived_attack(attrs: &Attributes, mods: &ModifierList) -> f32 {
    let mut value = attrs.strength as f32;
    let mut scale = 1.0;
    for modifier in &mods.0 {
        match modifier.kind {
            ModKind::Add => value += modifier.amount,
            ModKind::Mul => scale *= modifier.amount,
        }
    }
    (value * scale).max(0.0)
}
```

Health max follows vitality. The system runs only when `Attributes` changed, so idle frames do not recompute.

```rust
#[derive(Component, Clone, Copy)]
struct Attributes {
    strength: i32,
    vitality: i32,
}

#[derive(Component)]
struct Health {
    current: i32,
    max: i32,
}

fn sync_health(mut actors: Query<(&Attributes, &mut Health), Changed<Attributes>>) {
    for (attrs, mut health) in &mut actors {
        health.max = (20 + attrs.vitality * 5).max(1);
        health.current = health.current.min(health.max);
    }
}

#[derive(Component, Clone, Copy)]
struct IncomingHit(i32);

fn apply_hits(mut commands: Commands, mut actors: Query<(Entity, &mut Health, &IncomingHit)>) {
    for (entity, mut health, hit) in &mut actors {
        health.current = (health.current - hit.0).max(0);
        commands.entity(entity).remove::<IncomingHit>();
    }
}
```

The curve is data. Load it once into a resource. Awarding experience mutates the actor component and reads that table.

```rust
use serde::Deserialize;

#[derive(Deserialize, Resource, Clone, Copy)]
struct LevelCurve {
    base_xp: u32,
    growth: f32,
}

#[derive(Component)]
struct Progression {
    level: u32,
    xp: u32,
}

fn load_curve() -> LevelCurve {
    let text = "(base_xp: 100, growth: 1.15)";
    ron::from_str(text).expect("level curve")
}

fn xp_to_advance(curve: &LevelCurve, level: u32) -> u32 {
    let scaled = curve.base_xp as f32 * curve.growth.powi(level as i32);
    scaled.clamp(1.0, 1_000_000.0) as u32
}

#[derive(Component, Clone, Copy)]
struct Attributes {
    strength: i32,
    vitality: i32,
}

#[derive(Component)]
struct Health {
    current: i32,
    max: i32,
}

fn sync_health(mut actors: Query<(&Attributes, &mut Health), Changed<Attributes>>) {
    for (attrs, mut health) in &mut actors {
        health.max = (20 + attrs.vitality * 5).max(1);
        health.current = health.current.min(health.max);
    }
}

#[derive(Component, Clone, Copy)]
struct XpGain(u32);

fn grant_xp(
    mut commands: Commands,
    curve: Res<LevelCurve>,
    mut actors: Query<(Entity, &mut Progression, &mut Attributes, &XpGain)>,
) {
    for (entity, mut progress, mut attrs, gain) in &mut actors {
        progress.xp += gain.0;
        let need = xp_to_advance(&curve, progress.level);
        if progress.xp >= need {
            progress.xp -= need;
            progress.level += 1;
            attrs.vitality += 1;
        }
        commands.entity(entity).remove::<XpGain>();
    }
}

pub struct StatsPlugin;

impl Plugin for StatsPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(load_curve())
            .add_systems(Update, (grant_xp, sync_health).chain());
    }
}
```

## Choose the owner

| Need | Owner |
| --- | --- |
| Attributes | `Attributes` on the actor. |
| Modifier | `ModifierList` of additive and multiplicative rows. |
| Level | `Progression` plus a `LevelCurve` resource loaded from RON. |

## Scope

- Attribute, modifier, and level data are components and one curve resource, as in the systems above.
- Combat resolution that spends the derived attack value belongs on bevy-combat-system.

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

- No Godot node, resource, or signal types for this mechanic. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

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
- [bevy-combat-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-combat-system/SKILL.md) - Consumes derived attack and health.
- [bevy-data-resources](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-data-resources/SKILL.md) - Tables and definitions.
- [bevy-events-messaging](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-events-messaging/SKILL.md) - One-shot facts.

#### Complements
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Mode flags.
- [godot-rpg-stats](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-rpg-stats/SKILL.md) - Equivalent Godot skill.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
