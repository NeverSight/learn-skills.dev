---
name: bevy-ui-layout
description: "Lays out Bevy HUD and menu nodes with Flexbox, CSS Grid, Button, and ImageNode. Use when spawning Node trees; text and theming stay on their own skills. Keywords: Bevy, UI, Node, Flexbox, GridTrack, Button, Pressed, ImageNode."
---

# Bevy UI layout

## When to use

Load this when laying out HUD or menu nodes. Text content stays on bevy-ui-text. Colors and widget styling stay on bevy-ui-theming.

## ECS shape

- **Nodes:** spawn `Node` entities. Children are child entities. Flexbox and CSS Grid are fields on `Node`.
- **Widgets:** `ui_widgets::Button` plus the `Pressed` marker for the held state. `ImageNode` for a texture. Text content stays on `bevy-ui-text`.
- **Systems:** layout is engine-owned. Game systems read `Pressed` and `ComputedNode`. They do not run a second layout pass.

A column fills the window. The button is a child with a fixed size. `BackgroundColor` is the fill. `BorderRadius` rounds the control.

```rust
use bevy::ui_widgets::Button;

fn spawn_menu(mut commands: Commands) {
    let root = commands
        .spawn(Node {
            width: Val::Percent(100.0),
            height: Val::Percent(100.0),
            flex_direction: FlexDirection::Column,
            justify_content: JustifyContent::Center,
            align_items: AlignItems::Center,
            row_gap: Val::Px(12.0),
            ..default()
        })
        .id();
    commands.spawn((
        Button,
        Node {
            width: Val::Px(180.0),
            height: Val::Px(48.0),
            justify_content: JustifyContent::Center,
            align_items: AlignItems::Center,
            border_radius: BorderRadius::all(CornerRadius::circular(Val::Px(6.0))),
            ..default()
        },
        BackgroundColor(Color::srgb(0.15, 0.15, 0.15)),
        ChildOf(root),
    ));
}

pub struct MenuPlugin;

impl Plugin for MenuPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_menu);
    }
}
```

One system writes `BackgroundColor` from the `Pressed` marker. That marker is the only signal this system reads, so it is the only writer of the button fill.

```rust
use bevy::ui::Pressed;
use bevy::ui_widgets::Button;

fn paint_buttons(mut buttons: Query<(&mut BackgroundColor, Has<Pressed>), With<Button>>) {
    for (mut color, pressed) in &mut buttons {
        *color = if pressed {
            BackgroundColor(Color::srgb(0.35, 0.75, 0.35))
        } else {
            BackgroundColor(Color::srgb(0.15, 0.15, 0.15))
        };
    }
}
```

A grid names its tracks on the parent. Each child sets `grid_row` and `grid_column`.

```rust
fn spawn_grid(mut commands: Commands) {
    let root = commands
        .spawn(Node {
            display: Display::Grid,
            width: Val::Percent(100.0),
            height: Val::Px(200.0),
            grid_template_columns: vec![GridTrack::flex(1.0), GridTrack::px(120.0)],
            grid_template_rows: vec![GridTrack::auto()],
            column_gap: Val::Px(8.0),
            ..default()
        })
        .id();
    commands.spawn((
        Node {
            grid_column: GridPlacement::start(1),
            grid_row: GridPlacement::start(1),
            ..default()
        },
        BackgroundColor(Color::srgb(0.2, 0.2, 0.4)),
        ChildOf(root),
    ));
}
```

An image is `ImageNode` plus a sized `Node`. The handle comes from `AssetServer`.

```rust
fn spawn_icon(mut commands: Commands, assets: Res<AssetServer>) {
    let image = assets.load("icons/sword.png");
    commands.spawn((
        ImageNode::new(image),
        Node {
            width: Val::Px(64.0),
            height: Val::Px(64.0),
            ..default()
        },
    ));
}
```

## Widget map

| Need | Bevy idiom |
| --- | --- |
| Column or row | A `Node` entity. Children are child entities via `ChildOf` |
| Button | `ui_widgets::Button` plus the `Pressed` marker |
| Image | `ImageNode` sized by `Node` |
| Grid | `Display::Grid`, `GridTrack`, `GridPlacement` |

## Scope

- Flex fields used above: `flex_direction`, `justify_content`, `align_items`, `row_gap`. Grid fields: `display`, `grid_template_columns`, `grid_template_rows`, `grid_column`, `grid_row`.
- `bevy_feathers` is a styled widget collection for editors. Game HUDs use `Node`, `Button`, and `ImageNode`.

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

- No control-tree anchors or container nodes. WHY: layout is `Node` fields, `ChildOf`, and `ComputedNode`.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20**.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.
- [UI examples](https://github.com/bevyengine/bevy/tree/latest/examples/ui) - `Node`, Flexbox, grid, buttons, and images.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.

#### Complements
- [bevy-ui-text](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ui-text/SKILL.md) - Text on a node.
- [bevy-ui-theming](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ui-theming/SKILL.md) - Colors and backgrounds.

#### Downstream / consumers
- [bevy-ui-text](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ui-text/SKILL.md) - Consumes layout nodes.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
