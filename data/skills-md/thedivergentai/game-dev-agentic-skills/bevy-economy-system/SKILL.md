---
name: bevy-economy-system
description: "Bevy ECS economy: Wallet components, a PriceTable resource, Purchase and Transfer messages, vendor stock. Use when a debit must see the price row and two wallets must not be written by unordered systems. Keywords: Bevy, economy, wallet, price, Purchase, get_many_mut."
---

# Bevy economy system

## When to use

Load this when wallets, prices, or vendors change numbers. Item identity stays on bevy-inventory-system.

## ECS shape

- **Components:** wallet amounts you define.
- **Resources:** price rows live in one resource (bevy-data-resources).
- **Systems:** mutate wallets on `Update`. Use `.chain()` when stock must drop before the wallet debit.
- **Messages:** a purchase or transfer is a message. This file names `Purchase` and `Transfer`.

## Idioms

| Need | Bevy shape |
| --- | --- |
| Wallet | A component of currency amounts you define. |
| Price row | A resource table. |
| Transaction | A message. One system writes both wallets with `get_many_mut`. |

## Scope

- Coins live on a wallet component. Prices live in one resource. A purchase message is the only writer of the buyer wallet.
- Persistence of the wallet belongs on bevy-save-load.

## Examples

```toml
[package]
name = "economy"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.20"
```

Price lookup and the wallet write share one chain so the debit sees the row that was chosen.

```rust
#[derive(Component)]
struct Wallet {
    coins: u32,
}

#[derive(Clone, Copy)]
struct PriceRow {
    item: u32,
    cost: u32,
}

#[derive(Resource)]
struct PriceTable {
    rows: Vec<PriceRow>,
}

#[derive(Message)]
struct Purchase {
    buyer: Entity,
    item: u32,
}

fn buy(
    mut purchases: MessageReader<Purchase>,
    table: Res<PriceTable>,
    mut wallets: Query<&mut Wallet>,
) {
    for purchase in purchases.read() {
        let Some(row) = table.rows.iter().find(|row| row.item == purchase.item) else {
            continue;
        };
        let Ok(mut wallet) = wallets.get_mut(purchase.buyer) else {
            continue;
        };
        if wallet.coins < row.cost {
            continue;
        }
        wallet.coins -= row.cost;
    }
}

pub struct EconomyPlugin;

impl Plugin for EconomyPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(PriceTable {
            rows: vec![
                PriceRow { item: 1, cost: 12 },
                PriceRow { item: 2, cost: 40 },
            ],
        })
        .add_message::<Purchase>()
        .add_systems(Update, buy);
    }
}
```

Moving coins between two wallets uses one mutable query so the two writes cannot race.

```rust
#[derive(Component)]
struct Wallet {
    coins: u32,
}

#[derive(Message)]
struct Transfer {
    from: Entity,
    to: Entity,
    amount: u32,
}

fn transfer(mut moves: MessageReader<Transfer>, mut wallets: Query<&mut Wallet>) {
    for mv in moves.read() {
        if mv.amount == 0 || mv.from == mv.to {
            continue;
        }
        let Ok([mut from, mut to]) = wallets.get_many_mut([mv.from, mv.to]) else {
            continue;
        };
        if from.coins < mv.amount {
            continue;
        }
        from.coins -= mv.amount;
        to.coins += mv.amount;
    }
}
```

A vendor lists stock. The purchase message names the item id; this system only refuses an empty shelf.

```rust
#[derive(Component)]
struct Vendor {
    item: u32,
    stock: u32,
}

#[derive(Message)]
struct Purchase {
    buyer: Entity,
    item: u32,
}

fn take_stock(mut purchases: MessageReader<Purchase>, mut vendors: Query<&mut Vendor>) {
    for purchase in purchases.read() {
        for mut vendor in &mut vendors {
            if vendor.item != purchase.item || vendor.stock == 0 {
                continue;
            }
            vendor.stock -= 1;
            break;
        }
    }
}
```

Chain `take_stock` before `buy` when a sale must decrement the shelf and the wallet together.

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
| Per-entity data | `Component` + `Query` | A scene-tree script on the actor |
| App-wide config or clock | `Resource` | Copy the value onto every entity |
| Stable simulation step | `FixedMain` and the `Fixed` clock | Tie simulation to raw frame `Update` |
| Startup spawn | `Commands` in `Startup` | Spawn from a render system |
| Cross-system notice that is not shared state | Message or observer slot in `bevy-events-messaging` | A new event type invented in this file |
| An API outside the documented set | Read the official manual linked below | A made-up crate or API |

Load [references/ecs-ownership.md](references/ecs-ownership.md) for the ownership table.

## NEVER

- Do not pin `/0.20.0/` in docs URLs. WHY: links stay on `latest`; the 0.20 target is stated once in prose.
- Do not mutably query the same component from two unordered systems. WHY: the schedule runs systems in parallel unless `.chain()` orders them.
- Do not invent a physics, navigation, networking, or XR crate here. WHY: this skill only names documented Bevy crates and modules.

- No scene-tree node or signal bus for this mechanic. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20**.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.
- [bevy-inventory-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-inventory-system/SKILL.md) - Item stacks.
- [bevy-save-load](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-save-load/SKILL.md) - Persist the wallet.
- [bevy-data-resources](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-data-resources/SKILL.md) - Tables and definitions.
- [bevy-events-messaging](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-events-messaging/SKILL.md) - One-shot facts.

#### Complements
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Mode flags.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
