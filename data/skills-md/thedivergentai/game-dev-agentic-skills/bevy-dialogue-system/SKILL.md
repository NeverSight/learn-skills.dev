---
name: bevy-dialogue-system
description: "Bevy 0.20 dialogue data: line tables in a resource, the current line index on a component, and choice flags filtered before the write. Use when lines or choices advance. Keywords: Bevy, dialogue, line index, choices, ECS."
---

# Bevy dialogue system

## When to use

Load this when lines, choices, or speaker ids advance. Rendering the line is bevy-ui-text.

## ECS shape

- **Components:** a line id and a speaker id that you define.
- **Resources:** run-wide tables live in a resource (bevy-data-resources), not an autoload.
- **Systems:** mutate those components on `Update` or the fixed timestep. Use `.chain()` when damage must land before death.
- **Messages:** one-shot facts (hit, pickup, quest advance) go through bevy-events-messaging. This file does not add a new event type name.

## Engine counterparts

| Godot idea | Bevy idiom |
| --- | --- |
| Line table | A resource of ids and strings. |
| Current line | A component that stores the line index. |
| Portrait | An image handle via bevy-asset-scenes. Layout is bevy-ui-layout. |

## Scope

Dialogue data is a resource of lines plus a component that stores the current line index. Rich text rendering belongs on bevy-ui-text.

```toml
[dependencies]
bevy = "0.20"
```

```rust
#[derive(Clone)]
struct LineDef {
    speaker: &'static str,
    text: &'static str,
    next: Option<usize>,
}

#[derive(Resource)]
struct DialogueTable {
    lines: Vec<LineDef>,
}

#[derive(Component)]
struct LineMark {
    index: usize,
    open: bool,
}

fn advance_line(
    keys: Res<ButtonInput<KeyCode>>,
    table: Res<DialogueTable>,
    mut marks: Query<&mut LineMark>,
) {
    if !keys.just_pressed(KeyCode::Space) {
        return;
    }
    for mut mark in &mut marks {
        if !mark.open {
            continue;
        }
        let Some(line) = table.lines.get(mark.index) else {
            mark.open = false;
            continue;
        };
        match line.next {
            Some(next) => mark.index = next,
            None => mark.open = false,
        }
    }
}

fn spawn_conversation(mut commands: Commands) {
    commands.insert_resource(DialogueTable {
        lines: vec![
            LineDef {
                speaker: "guide",
                text: "The gate opens at dusk.",
                next: Some(1),
            },
            LineDef {
                speaker: "guide",
                text: "Bring the key.",
                next: None,
            },
        ],
    });
    commands.spawn(LineMark {
        index: 0,
        open: true,
    });
}

pub struct DialoguePlugin;

impl Plugin for DialoguePlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, spawn_conversation)
            .add_systems(Update, advance_line);
    }
}
```

Choices are data on the line. Hide a choice when its required flag is absent.

```rust
#[derive(Clone)]
struct ChoiceDef {
    label: &'static str,
    next: usize,
    requires_flag: Option<&'static str>,
}

#[derive(Resource)]
struct ChoiceList {
    choices: Vec<ChoiceDef>,
}

#[derive(Resource, Default)]
struct StoryFlags {
    names: Vec<&'static str>,
}

#[derive(Component)]
struct LineMark {
    index: usize,
}

fn shown_choices(flags: &StoryFlags, list: &ChoiceList) -> Vec<usize> {
    list.choices
        .iter()
        .enumerate()
        .filter_map(|(index, choice)| match choice.requires_flag {
            Some(flag) if !flags.names.iter().any(|name| *name == flag) => None,
            _ => Some(index),
        })
        .collect()
}

fn choose_first(
    keys: Res<ButtonInput<KeyCode>>,
    flags: Res<StoryFlags>,
    list: Res<ChoiceList>,
    mut marks: Query<&mut LineMark>,
) {
    if !keys.just_pressed(KeyCode::Digit1) {
        return;
    }
    let Some(choice_index) = shown_choices(&flags, &list).first().copied() else {
        return;
    };
    let next = list.choices[choice_index].next;
    for mut mark in &mut marks {
        mark.index = next;
    }
}

fn open_choice(mut commands: Commands) {
    commands.spawn(LineMark { index: 0 });
}

pub struct ChoicePlugin;

impl Plugin for ChoicePlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(StoryFlags {
            names: vec!["has_key"],
        })
        .insert_resource(ChoiceList {
            choices: vec![
                ChoiceDef {
                    label: "Open the gate",
                    next: 2,
                    requires_flag: Some("has_key"),
                },
                ChoiceDef {
                    label: "Leave",
                    next: 3,
                    requires_flag: None,
                },
            ],
        })
        .add_systems(Startup, open_choice)
        .add_systems(Update, choose_first);
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
| Per-entity data | `Component` + `Query` | A Godot node script |
| App-wide config or clock | `Resource` | Copy the value onto every entity |
| Stable simulation step | `FixedMain` and the `Fixed` clock | Tie simulation to raw frame `Update` |
| Startup spawn | `Commands` in `Startup` | Spawn from a render system |
| Cross-system notice that is not shared state | Message or observer slot in `bevy-events-messaging` | A new event type invented in this file |
| An API outside this skill | Load the skill that owns it | A made-up crate or API |

Load [references/ecs-ownership.md](references/ecs-ownership.md) for the ownership table.

## NEVER

- Do not pin `/0.20.0/` in docs URLs. WHY: links stay on `latest`; the 0.20 target is stated once in prose.
- Do not mutably query the same component from two unordered systems. WHY: the schedule runs systems in parallel unless `.chain()` orders them.
- Do not copy the line table onto every speaker. WHY: the table is one resource; the line index is the per-conversation component.
- Do not invent a physics, navigation, networking, or XR crate here. WHY: this skill only names documented Bevy crates and modules.

- No Godot node, resource, or signal types for this mechanic. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

- No Godot types in Bevy code. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

The library pin on bevy-master stays **0.20.0**. Official pages stay on the unversioned site.

### Official Documentation
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.
- [bevy-ui-text](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ui-text/SKILL.md) - Draw the line.
- [bevy-quest-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-quest-system/SKILL.md) - Quest gates.
- [bevy-data-resources](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-data-resources/SKILL.md) - Tables and definitions.
- [bevy-events-messaging](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-events-messaging/SKILL.md) - One-shot facts.

#### Complements
- [bevy-state-machines](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-state-machines/SKILL.md) - Mode flags.
- [godot-dialogue-system](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-dialogue-system/SKILL.md) - Equivalent Godot skill.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
