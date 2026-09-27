---
name: godot
description: Godot 4 craft — the node, resource and pattern a Godot developer reaches for in each job. Use when designing or ticketing Godot work, implementing scenes, UI or GDScript, or reviewing Godot code.
---

# Godot craft

Build the way a Godot developer working in the editor builds: **scene-first**. Every visible thing is a node in a scene, every reusable thing is its own scene, events travel on signals, and motion is owned by the node that moves. Reach for the **native** primitive — the one the engine ships for the job — and code only what no primitive covers.

Check the version before trusting any advice: most Godot material online is Godot 3. The reference is the [Godot 4 best practices](https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html); read the project's pinned version from `project.godot` and use that version's docs.

## Steps

1. **Sketch the scene tree.** Before writing code for anything visible, write its node tree: which nodes, which are their own `.tscn`, which script owns which job, which signals go up and which calls go down, which `Resource`s hold data. Done when every element of the spec or mock maps to a node in the sketch. At design time, the sketch is the ticket's **Godot structure** section — template in [references/ticket-section.md](references/ticket-section.md).
2. **Pick each primitive** from the table below. Where a row points at a reference, read it before building that part.
3. **Build in scenes.** Author node trees in `.tscn` files; scripts instance scenes and set state on them. Styles, fonts and colours live in the project `Theme`.
4. **Verify by looking.** Run `scripts/smell_check.py` over the game code (it reads `.gd` and `.tscn`) and clear every finding, either by switching to the native primitive or by tagging a deliberate exception `# godot-ok: <reason>` (`; godot-ok: <reason>` in a `.tscn`) on or above the line. Wire it into validation so a non-zero exit fails the build. Then capture frames of every state and a motion clip of every transition (`--write-movie out.png --fixed-fps 30 --quit-after N`), open the frames, and compare each against the spec or mock. Attach them wherever the work is reported. Done when the check fails the build on a finding and is green, and you have looked at a frame of every state and transition and each one matches. A report that the game "boots" or "runs" is not verification; a frame you have looked at is.

## Primitives

| Job | Native primitive | Red flag |
|---|---|---|
| A game object (field, unit, pickup, card) | Its own scene, instanced; state set through a typed method | One `_draw()` painting every object |
| Clicking or hovering a world object | `Area2D` + `CollisionShape2D`, `input_pickable`, `mouse_entered` / `input_event` | `Rect2(...).has_point(mouse)` with literal sizes |
| Text | `Label` / `RichTextLabel`, styled by the theme | `draw_string`, `ThemeDB.fallback_font` |
| Panels, badges, button looks | `StyleBox` in the `Theme`, or a theme type variation | `StyleBoxFlat.new()` in script |
| Static UI layout | Containers and anchors in a `.tscn` | `Label.new()` / `add_child` building UI in `_ready` |
| Overlays on a container (badge, border, pip) | A plain `Control` root holding the container and the overlays as siblings | Children placed by offsets inside a container, which stretches them to fill it |
| Art on a card or panel | `StyleBoxTexture` in the theme, `NinePatchRect` for frames, `TextureRect` for pictures — [references/art.md](references/art.md) | `Sprite2D` inside the UI tree |
| Art in the world | `Sprite2D`, `AnimatedSprite2D`, `TileMapLayer` — [references/art.md](references/art.md) | `Polygon2D` placeholders standing in for finished art |
| A layout whose children animate (card hand, radial menu) | A custom `Control` computing target transforms; children ease toward them — [references/motion.md](references/motion.md) | Animated children inside a `BoxContainer` |
| Reacting to game events | Signals from the model, connected by the view | Polling every frame and diffing arrays to guess what changed |
| A list that changes (hand, inventory) | One persistent view per item, keyed by the item; add and remove singly | Freeing every child and re-instancing on each change |
| One-shot motion (pop, shake, fly-to) | `Tween` from `create_tween()` on the moving node | Countdown floats passed down through refresh calls |
| Authored, multi-track motion | `AnimationPlayer` | Hand-sequenced timers |
| World objects that move | Move in `_physics_process` with physics interpolation on | Transforms set in `_process` on interpolated nodes |
| UI easing and view refresh | `_process` | Visual work in `_physics_process` |
| Framing the world | `Camera2D` | World laid out against literal viewport sizes |
| Tooltips | `_make_custom_tooltip()` returning a scene | Default `tooltip_text` for game content |
| Tunable data, card and item definitions | `Resource` subclasses saved as `.tres` | Dictionaries of constants in scripts |
| Per-object state | Typed `var`s | `set_meta` / `get_meta` |
| Node references | `@onready var x: Type = %Name`; `class_name` on scripts others reference | Untyped `@onready var x = $Path` |

Custom `_draw()` is the native primitive for three jobs only: many simple repeated shapes (a grid, a board), shapes no node provides (trails, arcs, procedural polygons), and the non-text face of a custom control. Everything else is a node.

## Communication

Call down, signal up. A parent calls methods on its children; a child emits signals and never reaches for its parent. A scene receives what it needs through a setter or `bind()` from the scene that owns it, and runs on its own when opened alone.

## References

- [references/ticket-section.md](references/ticket-section.md) — the Godot structure section every Godot ticket carries.
- [references/motion.md](references/motion.md) — target-easing layouts, tweens, drag and snap-back.
- [references/ui.md](references/ui.md) — themes, containers, input routing between UI and world.
- [references/art.md](references/art.md) — where art goes in UI versus world, and pixel-art settings.
