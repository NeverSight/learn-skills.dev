---
name: monogame-extended-tiled
description: >
  MonoGame.Extended Tilemaps guide — loading, rendering, and querying tile maps created
  with Tiled (.tmx), LDtk (.ldtk), or Ogmo Editor through the unified v6 API.
  Use this skill whenever the user mentions tiled map, tmx file, tilemap, tileset,
  tile-based level, TiledMapRenderer, orthogonal map render, map pipeline, object layer
  spawn, or wants to load a level made in Tiled — even if they just say "I have a .tmx
  file" or "how do I render a tile map".
---

# MonoGame.Extended Tilemaps Implementation Guide

This skill covers the **v6 unified tilemap API** (`MonoGame.Extended.Tilemaps`).
The legacy `MonoGame.Extended.Tiled` namespace and `TiledMap`/`TiledMapRenderer` classes
were removed in v6 — do not use them. For API signatures and complete code read
`references/extended-tiled.md`.

## Supported Formats

| Format | File extension | Notes |
|--------|---------------|-------|
| Tiled Map Editor | `.tmx` | Orthogonal, Isometric, Staggered, Hexagonal |
| LDtk | `.ldtk` | Orthogonal |
| Ogmo Editor | `.ogmo` / `.json` | Orthogonal |

All three share the same runtime API — switching editors requires no game code changes.

## Content Pipeline Setup (Recommended)

1. **MGCB Editor** → References → add `MonoGame.Extended.Content.Pipeline.dll`
2. Add your map file (`.tmx`, `.ldtk`, or `.ogmo`) — the importer is auto-selected
   by file extension
3. For Tiled maps: also add any referenced `.tsx` tileset files
4. Tileset image files (`.png`) go in the content directory but **are not added as
   content items** — the importer discovers them automatically

Load at runtime:
```csharp
Tilemap tilemap = Content.Load<Tilemap>("maps/level1");
```

## Namespaces

```csharp
using MonoGame.Extended.Tilemaps;            // Tilemap, TilemapTileLayer, TilemapObjectLayer…
using MonoGame.Extended.Tilemaps.Rendering;  // TilemapSpriteBatchRenderer, TilemapRenderer
using MonoGame.Extended;                     // OrthographicCamera
using MonoGame.Extended.ViewportAdapters;    // BoxingViewportAdapter
```

## Camera

`TilemapSpriteBatchRenderer.Draw(_spriteBatch, _camera)` requires **`OrthographicCamera`
from MonoGame.Extended** — it does not accept a raw `Matrix`. This is the 2D camera
provided by Extended; it is unrelated to `monogame-camera-modes` which covers 3D cameras.

Set up `OrthographicCamera` once in `Initialize`:

```csharp
protected override void Initialize()
{
    base.Initialize();
    var viewport = new BoxingViewportAdapter(Window, GraphicsDevice, 320, 180);
    _camera = new OrthographicCamera(viewport);
}
```

Move the camera to scroll the map:
```csharp
_camera.LookAt(_player.Position);     // center on player
_camera.Position += velocity * elapsed; // or move manually
```

For entity rendering interleaved with tile layers, get the view matrix:
```csharp
_spriteBatch.Begin(transformMatrix: _camera.GetViewMatrix());
```

## Choosing a Renderer

| | `TilemapSpriteBatchRenderer` | `TilemapRenderer` |
|-|------------------------------|-------------------|
| Backend | `SpriteBatch` | `GraphicsDevice` direct |
| Culling | Frustum culling — only visible tiles | All tiles pre-baked in GPU buffers |
| Setup | Simple, no dispose | Requires `Dispose()` |
| Dynamic tile changes | Instant | Requires `MarkGroupDirty` |
| Best for | Scrolling maps, large worlds | Static maps, minimal draw calls |

**Use `TilemapSpriteBatchRenderer` by default** unless profiling shows draw call count
is a bottleneck on a mostly-static map.

### BlendState

| Loading method | BlendState to use |
|----------------|------------------|
| Content Pipeline | `BlendState.AlphaBlend` (alpha premultiplied) |
| Runtime parser | `BlendState.NonPremultiplied` (default) |

Set it after creating the renderer:
```csharp
_renderer = new TilemapSpriteBatchRenderer();
_renderer.BlendState = BlendState.AlphaBlend;  // for content pipeline
_renderer.LoadTilemap(_tilemap);
```

## Rendering: Full Frame Loop

```csharp
protected override void Update(GameTime gameTime)
{
    _renderer.Update(gameTime);  // advances tile animations
    base.Update(gameTime);
}

protected override void Draw(GameTime gameTime)
{
    GraphicsDevice.Clear(_tilemap.BackgroundColor ?? Color.Black);
    _renderer.Draw(_spriteBatch, _camera);
    base.Draw(gameTime);
}
```

## Interleaving Entities Between Layers

Draw background layers → entities → foreground layers:

```csharp
protected override void Draw(GameTime gameTime)
{
    GraphicsDevice.Clear(Color.Black);

    _renderer.DrawLayers(_spriteBatch, _camera, "Background", "Ground");

    // Draw game entities in world space
    _spriteBatch.Begin(transformMatrix: _camera.GetViewMatrix());
    foreach (var entity in _world.Entities)
        entity.Draw(_spriteBatch);
    _spriteBatch.End();

    _renderer.DrawLayer(_spriteBatch, _camera, "Foreground");
}
```

`TilemapSpriteBatchRenderer` manages its own `Begin`/`End` calls per layer, so there
is no conflict as long as you do not have a `SpriteBatch.Begin` open when calling
`DrawLayers` or `DrawLayer`.

## Reading Object Layers (Spawn Points, Collision, Triggers)

Object layers defined in the map editor map to `TilemapObjectLayer`. Iterate them to
drive game logic — for example, spawning `GameEntity` instances in your `GameWorld`:

```csharp
var objectLayer = _tilemap.Layers["Entities"] as TilemapObjectLayer;

foreach (TilemapObject obj in objectLayer.Objects)
{
    if (!obj.IsVisible) continue;

    string type = obj.Properties.GetString("type", "");

    switch (obj)
    {
        case TilemapPointObject point:
            // Spawn point — use Position directly
            _world.Spawn(type, point.Position);
            break;

        case TilemapRectangleObject rect:
            // Trigger zone or collision area
            _collisionZones.Add(new RectangleF(
                rect.Position.X, rect.Position.Y, rect.Width, rect.Height));
            break;
    }
}
```

To iterate only one type:
```csharp
foreach (TilemapRectangleObject rect in objectLayer.GetObjects<TilemapRectangleObject>())
{
    // collision rect setup
}
```

## Custom Properties

Available on maps, layers, tilesets, tiles, and objects:

```csharp
string zone    = tilemap.Properties.GetString("zone", "default");
int maxEnemies = tilemap.Properties.GetInt("maxEnemies", 10);
float gravity  = tilemap.Properties.GetFloat("gravity", 9.8f);
bool  isBoss   = obj.Properties.GetBool("isBossRoom", false);
```

## Working with Tile Layers at Runtime

```csharp
TilemapTileLayer tileLayer = _tilemap.Layers["Ground"] as TilemapTileLayer;

// Read a tile
TilemapTile? tile = tileLayer.GetTile(col, row);   // tile coords, not pixel coords

// Modify at runtime (then MarkGroupDirty if using TilemapRenderer)
tileLayer.SetTile(col, row, new TilemapTile(newGlobalId));
tileLayer.SetTile(col, row, null);  // clear
```

## Anti-Patterns

- **Never** import from `MonoGame.Extended.Tiled` — that namespace is removed in v6.
  The Extended classes `TiledMap` and `TiledMapRenderer` do not exist in v6.
  Note: the project provides its own `Alca.MonoGame.Kernel.Graphics.Tiled.TiledMapRenderer`
  wrapper (different class, different namespace) — that one is correct and wraps `TilemapSpriteBatchRenderer`.
- **Never** pass a raw `Matrix` to `TilemapSpriteBatchRenderer.Draw` — it requires
  `OrthographicCamera`.
- **Never** call `_renderer.Draw` while a `SpriteBatch` is still open (`Begin` without
  matching `End`) — it will open its own Begin internally and may throw.
- **Dispose** `TilemapRenderer` (not `TilemapSpriteBatchRenderer`) when unloading
  a scene — it holds GPU vertex/index buffers.

## Reference

For complete field declarations, full `Initialize`/`LoadContent`/`Update`/`Draw` code,
and object layer spawn examples, read `references/extended-tiled.md`.
