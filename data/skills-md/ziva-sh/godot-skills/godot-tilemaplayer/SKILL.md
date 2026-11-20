---
name: godot-tilemaplayer
description: Correct Godot 4.3+ TileMapLayer code - set_cell(coords, source_id, atlas_coords), reading cells and custom data, erasing, coordinate conversion, terrains, tile collision through TileSet physics layers, finding the tile a body hit, and migrating from the deprecated TileMap node and its layer-index API. Use when placing, reading or erasing tiles from GDScript, building a TileSet in code, generating levels procedurally, handling tile collisions, or porting TileMap code from Godot 3 or Godot 4.0 to 4.2.
license: MIT
compatibility: Godot 4.3 or later (snippets tested on 4.7.2)
---

# TileMapLayer (Godot 4.3+)

Godot 4.3 added the `TileMapLayer` node and deprecated `TileMap`. Each `TileMapLayer` is one layer, so a level with ground, walls and decoration is three sibling `TileMapLayer` nodes sharing one `TileSet`. Do not write new code against `TileMap`, and never use the Godot 3 API (`set_cellv`, `world_to_map`, `set_cell(x, y, tile_id)`).

## The cell API

A cell is identified by integer map coordinates (`Vector2i`). A tile is identified by three values:

- `source_id`: the ID of a source in the `TileSet` (an atlas texture or a scenes collection). The first atlas is usually `0`; check the TileSet editor or the return value of `TileSet.add_source()`.
- `atlas_coords`: the tile's column and row inside that atlas, in tiles, not pixels.
- `alternative_tile`: `0` unless you made flipped or rotated alternatives.

```gdscript
extends TileMapLayer

const SOURCE_ID := 0
const GRASS := Vector2i(0, 0)
const WALL := Vector2i(1, 0)


func _ready() -> void:
	for x in range(10):
		set_cell(Vector2i(x, 5), SOURCE_ID, GRASS)
	set_cell(Vector2i(3, 4), SOURCE_ID, WALL)

	var source_id := get_cell_source_id(Vector2i(3, 4))  # -1 when the cell is empty
	var atlas := get_cell_atlas_coords(Vector2i(3, 4))  # Vector2i(-1, -1) when empty
	print(source_id, atlas)

	erase_cell(Vector2i(3, 4))
	print(get_used_cells().size(), " cells, bounds ", get_used_rect())


func cell_at_global(global_point: Vector2) -> Vector2i:
	return local_to_map(to_local(global_point))


func center_of_cell(coords: Vector2i) -> Vector2:
	# map_to_local returns the cell centre in this layer's local space.
	return to_global(map_to_local(coords))
```

Facts that matter:

- `set_cell(coords)` with the default arguments erases the cell (`source_id` defaults to `-1`). Always pass `source_id` and `atlas_coords` when placing a tile.
- Setting `atlas_coords` that do not exist in the atlas stores the cell without an error (`get_cell_source_id()` returns the source), and `get_cell_tile_data()` later logs `The TileSetAtlasSource atlas has no tile at (x, y).` and returns `null`.
- `local_to_map()` and `map_to_local()` work in the layer's local space. Convert with `to_local()` / `to_global()` when the layer is moved or scaled.
- `get_used_cells_by_id(source_id, atlas_coords)` finds every cell using one tile.
- Changes are batched to the end of the frame. Call `update_internals()` if you need collision or scene tiles updated immediately.

## Custom data per tile

Add a custom data layer in the TileSet (Inspector > TileSet > Custom Data Layers, for example `damage` of type `int`), paint values in the TileSet editor, then read them:

```gdscript
extends TileMapLayer


func damage_at(coords: Vector2i) -> int:
	var data := get_cell_tile_data(coords)
	if data == null:
		return 0
	return data.get_custom_data("damage")
```

`get_cell_tile_data()` returns `null` for empty cells and for scene-collection tiles, so check before calling methods on it.

## Terrains (autotiling)

Godot 3 autotile bitmasks became terrain sets. In the TileSet, add a terrain set and a terrain, then paint each tile's terrain peering bits in the TileSet editor. In code, pass every cell you want filled:

```gdscript
extends TileMapLayer

const TERRAIN_SET := 0
const DIRT := 0


func paint_room(rect: Rect2i) -> void:
	var cells: Array[Vector2i] = []
	for x in range(rect.position.x, rect.end.x):
		for y in range(rect.position.y, rect.end.y):
			cells.append(Vector2i(x, y))
	set_cells_terrain_connect(cells, TERRAIN_SET, DIRT)
```

`set_cells_terrain_connect()` picks tiles so the edges connect; `set_cells_terrain_path()` is for roads and rivers drawn as a path. If the result shows wrong or missing tiles, the peering bits in the TileSet are incomplete; code cannot fix that.

## Collision

Tiles collide only when the TileSet has a physics layer (TileSet inspector > Physics Layers > Add Element) and the tile has a collision polygon on that layer (TileSet editor, select the tile, Physics > Physics Layer 0; press F for a full-tile rectangle). The layer's `collision_enabled` property is on by default. Physics layers also carry `collision_layer` and `collision_mask`, set on the TileSet, not on the node.

To find which tile a `CharacterBody2D` touched, use the collision point. `get_coords_for_body_rid()` returns the coordinates of a physics quadrant, not of a cell, unless `physics_quadrant_size` is `1` (Godot 4.5+ merges up to 16 x 16 cells into one body by default):

```gdscript
extends CharacterBody2D

@export var level: TileMapLayer


func _physics_process(delta: float) -> void:
	velocity += get_gravity() * delta
	move_and_slide()
	for i in get_slide_collision_count():
		var collision := get_slide_collision(i)
		if collision.get_collider() == level:
			# Step slightly into the tile, because the contact point is on its edge.
			var inside := collision.get_position() - collision.get_normal()
			var coords := level.local_to_map(level.to_local(inside))
			print("Touching tile ", coords)
```

## Building a TileSet in code

Useful for procedural levels and for tests that cannot use the TileSet editor. Collision polygon points are relative to the tile centre.

```gdscript
extends Node2D


func _ready() -> void:
	var tile_set := TileSet.new()
	tile_set.tile_size = Vector2i(16, 16)
	tile_set.add_physics_layer()

	var source := TileSetAtlasSource.new()
	source.texture = load("res://tiles.png") as Texture2D
	source.texture_region_size = Vector2i(16, 16)
	source.create_tile(Vector2i(0, 0))
	var source_id := tile_set.add_source(source)

	var data := source.get_tile_data(Vector2i(0, 0), 0)
	data.add_collision_polygon(0)
	data.set_collision_polygon_points(0, 0, PackedVector2Array([
		Vector2(-8, -8), Vector2(8, -8), Vector2(8, 8), Vector2(-8, 8),
	]))

	var layer := TileMapLayer.new()
	layer.tile_set = tile_set
	add_child(layer)
	layer.set_cell(Vector2i(0, 0), source_id, Vector2i(0, 0))
```

## Migrating from TileMap

In the editor: select the `TileMap`, open the TileMap bottom panel, click the toolbox icon and choose "Extract TileMap layers as individual TileMapLayer nodes". Then update scripts: every `TileMap` method that took a `layer` index first becomes a method on that layer's node, without the index.

| Old code | TileMapLayer |
| --- | --- |
| `tile_map.set_cell(0, coords, source_id, atlas_coords)` | `ground.set_cell(coords, source_id, atlas_coords)` |
| `tile_map.get_cell_source_id(1, coords)` | `walls.get_cell_source_id(coords)` |
| `tile_map.get_used_cells(0)` | `ground.get_used_cells()` |
| `tile_map.set_layer_enabled(2, false)` | `decoration.enabled = false` |
| `tile_map.set_layer_z_index(1, 5)` | `walls.z_index = 5` |
| Godot 3 `set_cellv(pos, id)`, `world_to_map(p)`, `map_to_world(c)` | `set_cell(coords, source_id, atlas_coords)`, `local_to_map(p)`, `map_to_local(c)` |

## Common mistakes

- Passing pixel positions to `set_cell()`. Convert with `local_to_map()` first.
- Calling `set_cell(coords, tile_index)` with one number: the second argument is the source ID, and `atlas_coords` defaults to `Vector2i(-1, -1)`, which erases the cell.
- Expecting collisions from a TileSet that has no physics layer, or from tiles with no painted polygon.
- Using `get_coords_for_body_rid()` with the default `physics_quadrant_size` and getting a quadrant coordinate.
- Calling methods on `get_cell_tile_data()` without a `null` check.
- Adding a `TileMap` node for new work because older tutorials do. Use one `TileMapLayer` per layer.
