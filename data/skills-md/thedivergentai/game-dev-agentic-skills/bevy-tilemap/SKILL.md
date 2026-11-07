---
name: bevy-tilemap
description: "Bevy ECS skill for tile maps. Keywords: Bevy, tilemap, tiles, ECS, Sprite."
---

# Bevy tilemap

## When to use

Load this before storing a grid of tiles. Bevy draws cells with `Sprite` and a `TextureAtlas`. The grid itself is a resource and a set of entities you own.

## ECS shape

- **Resource:** `TileGrid` owns width, height, and one cell id per slot.
- **Component:** `TileCell` stores the grid coordinate on the sprite entity.
- **Draw:** `TextureAtlasLayout::from_grid` slices a sheet. `Sprite::from_atlas_image` picks a cell index.
- **Schedule:** spawn the grid in `Startup`. Autotile rules are a plain function over neighbor ids.

## Examples

```toml
[dependencies]
bevy = "0.20"
```

The grid is the source of truth. Sprites are a view of it.

```rust
#[derive(Resource)]
struct TileGrid {
    width: i32,
    height: i32,
    cells: Vec<u16>,
}

impl TileGrid {
    fn index(&self, x: i32, y: i32) -> Option<usize> {
        if x < 0 || y < 0 || x >= self.width || y >= self.height {
            return None;
        }
        Some((y * self.width + x) as usize)
    }

    fn get(&self, x: i32, y: i32) -> u16 {
        self.index(x, y).map(|i| self.cells[i]).unwrap_or(0)
    }
}

#[derive(Component)]
struct TileCell {
    x: i32,
    y: i32,
}
```

A 4 by 4 sheet of 16-pixel tiles becomes one layout asset. Each solid cell spawns a sprite.

```rust
#[derive(Resource)]
struct TileGrid {
    width: i32,
    height: i32,
    cells: Vec<u16>,
}

impl TileGrid {
    fn get(&self, x: i32, y: i32) -> u16 {
        if x < 0 || y < 0 || x >= self.width || y >= self.height {
            return 0;
        }
        self.cells[(y * self.width + x) as usize]
    }
}

#[derive(Component)]
struct TileCell {
    x: i32,
    y: i32,
}

fn spawn_tiles(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut layouts: ResMut<Assets<TextureAtlasLayout>>,
    grid: Res<TileGrid>,
) {
    let layout = layouts.add(TextureAtlasLayout::from_grid(
        UVec2::splat(16),
        4,
        4,
        None,
        None,
    ));
    let image = asset_server.load("tiles.png");
    let tile = 16.0;
    for y in 0..grid.height {
        for x in 0..grid.width {
            let id = grid.get(x, y);
            if id == 0 {
                continue;
            }
            commands.spawn((
                Sprite::from_atlas_image(
                    image.clone(),
                    TextureAtlas {
                        layout: layout.clone(),
                        index: id as usize,
                    },
                ),
                Transform::from_xyz(x as f32 * tile, y as f32 * tile, 0.0),
                TileCell { x, y },
            ));
        }
    }
    commands.spawn(Camera2d);
}
```

Four-neighbor bits pick an atlas index. Empty neighbors stay zero.

```rust
#[derive(Resource)]
struct TileGrid {
    width: i32,
    height: i32,
    cells: Vec<u16>,
}

impl TileGrid {
    fn get(&self, x: i32, y: i32) -> u16 {
        if x < 0 || y < 0 || x >= self.width || y >= self.height {
            return 0;
        }
        self.cells[(y * self.width + x) as usize]
    }
}

#[derive(Component)]
struct TileCell {
    x: i32,
    y: i32,
}

fn autotile_index(grid: &TileGrid, x: i32, y: i32) -> usize {
    let solid = |nx: i32, ny: i32| u16::from(grid.get(nx, ny) != 0);
    let mask = solid(x, y + 1)
        | (solid(x + 1, y) << 1)
        | (solid(x, y - 1) << 2)
        | (solid(x - 1, y) << 3);
    mask as usize
}

fn repaint(grid: Res<TileGrid>, mut tiles: Query<(&TileCell, &mut Sprite)>) {
    for (cell, mut sprite) in &mut tiles {
        if let Some(atlas) = sprite.texture_atlas.as_mut() {
            atlas.index = autotile_index(&grid, cell.x, cell.y);
        }
    }
}
```

## Same job, Bevy types

| Design | Bevy idiom |
| --- | --- |
| TileSet atlas | `TextureAtlasLayout::from_grid` plus `Sprite::from_atlas_image` |
| TileMap layer | `TileGrid` resource and one entity per visible cell |
| Autotile | A function from neighbor ids to an atlas index |

## Scope

There is no engine tilemap type. Collision from the grid is a physics concern on bevy-physics-2d. Streaming a larger world means spawning and despawning `TileCell` entities from the same resource.

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
| Per-entity data | `Component` + `Query` | A scene-tree script hung on the entity |
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

- No Godot TileMap or TileSet types. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No named tilemap crate as the chosen solution. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

- No Godot types in Bevy code. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.
- No invented APIs or unnamed third-party crates as the chosen solver. WHY: Bevy code stays idiomatic ECS and uses only documented Bevy APIs.

## Reference

Official pages stay on unversioned bevy.org URLs. The library pin on bevy-master stays **0.20.0**. Cells draw with `Sprite` and `TextureAtlas`. There is no engine tile-map type.

### Official Documentation
- [Assets](https://bevy.org/assets/) - Official asset catalog. No third-party crate was selected.
- [Examples](https://github.com/bevyengine/bevy/tree/latest/examples#examples) - Example tree on the `latest` branch.
- [ECS](https://bevy.org/learn/quick-start/getting-started/ecs/) - `Component`, systems, `Query`, `Startup`, `Update`, and `.chain()`.
- [Plugins](https://bevy.org/learn/quick-start/getting-started/plugins/) - `Plugin`, `DefaultPlugins`, `MinimalPlugins`, and `add_plugins`.

### Related Skills

#### Prerequisites
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Hub and schedules.
- [bevy-ecs-composition](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-ecs-composition/SKILL.md) - Components and systems.
- [bevy-procedural-generation](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-procedural-generation/SKILL.md) - Seeded layouts.
- [bevy-data-resources](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-data-resources/SKILL.md) - Map resource.

#### Complements
- [godot-tilemap-mastery](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/godot-tilemap-mastery/SKILL.md) - Equivalent Godot skill.

#### Downstream / consumers
- None yet.

#### Master
- [bevy-master](https://github.com/thedivergentai/Game-Dev-Agentic-Skills/blob/main/skills/bevy-master/SKILL.md) - Bevy router.
