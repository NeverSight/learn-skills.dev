---
name: programming-monogame
description: Use when working with MonoGame.Extended library classes, features, or APIs - provides quick reference to local markdown documentation files
module: monogame
---

# MonoGame.Extended Documentation Reference

## Overview

Quick reference index for MonoGame.Extended documentation. Local markdown files are stored in the `references/` subdirectory.

**This skill contains ONLY file paths, not documentation.** You MUST use Read to retrieve the actual docs.

## Workflow (REQUIRED)

**CRITICAL:** This skill is a file path index ONLY. You MUST use Read to get actual documentation.

1. Find relevant file path(s) in Quick Reference table below
2. **Call Read tool** with the file path from the table
3. Extract information from Read results
4. Answer using the documentation content

**Example:**
```
User asks: "How do I use Texture2DAtlas?"
Step 1: Find file path in table → references/texture-handling/texture2datlas/texture2datlas.md
Step 2: Read("/home/.../programming-monogame/references/texture-handling/texture2datlas/texture2datlas.md")
Step 3: Use Read results to answer
```

**DO NOT:**
- Answer questions without calling Read first
- Make up API details not in the documentation files
- Use prior knowledge instead of current docs

## Quick Reference

All paths are relative to `.pi/skills/programming-monogame/`

| Feature | File Path | Description |
|---------|-----------|-------------|
| **2D Animations** | | |
| AnimatedSprite | references/2d-animations/animatedsprite/animatedsprite.md | Frame-based sprite animation playback |
| SpriteSheet | references/2d-animations/spritesheet/spritesheet.md | Define animations from texture atlas |
| **Camera** | | |
| Camera Overview | references/camera/camera.md | Camera concepts and transformation matrices |
| OrthographicCamera | references/camera/orthographic-camera/orthographic-camera.md | 2D camera with zoom, rotation, position |
| **Collections** | references/collections/collections.md | Custom collection types |
| **Collision** | | |
| Collision Overview | references/collision/collision.md | Actor/world collision management and 2D collision queries |
| Collision Quick Start | references/collision/quick-start.md | 6.0 workflow with ICollisionActor, CollisionShape2D, Layer, CollisionWorld2D |
| Collision 2D Geometry | references/collision/2d-geometry.md | Bounding volumes, primitives, and geometric collision queries |
| Collision Technical Reference | references/collision/technical-reference.md | Collision architecture, query flow, layers, and performance |
| Collision Migration | references/collision/migration.md | Migrate from legacy IShapeF-based collision APIs to 6.0 |
| **Content Extensions** | | |
| ContentManager | references/content-extensions/contentManager.md | Extended content loading |
| ContentReader | references/content-extensions/contentReader.md | Custom content readers |
| **Entities** | references/entities/entities.md | Entity Component System (ECS) |
| **Fonts** | | |
| BitmapFont | references/fonts/bitmapfont/bitmapfont.md | Bitmap font rendering |
| **Input** | | |
| InputListener | references/input/inputlistener/inputlistener.md | Event-based input handling |
| KeyboardExtended | references/input/keyboardextended/keyboardextended.md | Enhanced keyboard state |
| MouseExtended | references/input/mouseextended/mouseextended.md | Enhanced mouse state |
| **Object Pooling** | references/object-pooling/object-pooling.md | Object pool pattern |
| **Particles** | | |
| Quick Start | references/particles/quick_start_guide.md | Particle system basics |
| Emission Profiles | references/particles/emission_profiles.md | Spray, Circle, Point profiles |
| Modifiers | references/particles/modifiers.md | Gravity, Drag, Age, Rotation, etc. |
| Interpolators | references/particles/interpolators.md | Opacity, Scale, Color, Hue, etc. |
| Loading Ember Files | references/particles/loading_ember_files.md | Load particle effects from files |
| **Scene Graphs** | references/scene-graphs/scene-graphs.md | Hierarchical scene organization |
| **Screen Management** | references/screen-management/screen-management.md | Game screen/state management |
| **Serialization** | references/serialization/serialization.md | JSON serialization utilities |
| **Texture Handling** | | |
| Sprite | references/texture-handling/sprite/sprite.md | Basic sprite with position, rotation, scale |
| Texture2DAtlas | references/texture-handling/texture2datlas/texture2datlas.md | Sprite sheet atlas with regions |
| Texture2DRegion | references/texture-handling/texture2dregion/texture2dregion.md | Single region from texture |
| **Tilemaps** | | |
| Tilemaps Overview | references/tilemaps/tilemaps.md | 6.0 unified tilemap API for Tiled, LDtk, and Ogmo Editor |
| Tilemaps Quick Start | references/tilemaps/quick-start.md | Load and render a tilemap in minutes |
| Tilemaps Technical Reference | references/tilemaps/technical-reference.md | Tilemap architecture, rendering, coordinate systems, and class hierarchy |
| Tilemaps Migration | references/tilemaps/migration.md | Migrate from legacy MonoGame.Extended.Tiled to the unified tilemap system |
| Legacy Tiled | references/tiled/tiled.md | Removed in 6.0; use Tilemaps instead |
| **Tweening** | references/tweening/tweening.md | Property animation/interpolation |
| **UI** | | |
| Gum Forms | references/ui/gum/gum-forms/gum-forms.md | Gum UI integration |

## Using Read

For each relevant file path, construct the absolute path and read it:

```
Read(
  file_path: "/home/.../programming-monogame/references/[feature]/[feature].md"
)
```

**Note:** You'll need to construct the absolute path based on the current working directory. The skill files are located at `.pi/skills/programming-monogame/` relative to the repository root.

## Common Patterns

**Multiple Related Features:**
Read all related files in parallel. Example for textures:
1. Texture2DAtlas (atlas creation)
2. Texture2DRegion (single region)
3. Sprite (rendering)

**Hierarchical Features:**
Start with overview or quick-start, then read sub-pages. Examples:
- Particles: quick_start_guide → emission_profiles/modifiers/interpolators as needed
- Collision: quick-start → 2d-geometry/technical-reference as needed
- Tilemaps: quick-start → tilemaps/technical-reference/migration as needed

## When NOT to Use

- MonoGame core classes (GraphicsDevice, SpriteBatch, etc.) - use MonoGame docs
- Third-party libraries (TexturePacker, Tiled editor) - use their docs
- General C# questions - standard resources apply
