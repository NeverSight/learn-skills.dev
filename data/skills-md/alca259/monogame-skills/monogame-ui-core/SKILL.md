---
name: monogame-ui-core
description: MonoGame UI system architecture guide — visual tree, UIElement base class, UIContainer, painter's algorithm rendering, and the foundational rule that UI lives in its own SpriteBatch separate from the game world. Use this skill whenever the user asks about building a UI system, HUD, menus, overlays, or any on-screen interface in MonoGame — even if they just say "how do I draw UI over my game", "how do I make a menu", "what is a visual tree", or "should I use game entities for UI". Also covers the pragmatic Stardew Valley–style approach (IClickableMenu / ClickableComponent) as an alternative.
---

# MonoGame UI Core — Architecture Guide

This skill establishes the foundational architecture for a MonoGame UI system. For layout engines, see `monogame-ui-layout`. For click/hover handling, see `monogame-ui-interaction`. For gamepad/keyboard focus, see `monogame-ui-focus`. For ready-made components, see `monogame-ui-controls`.

For complete code templates, read `references/ui-core.md`.

## The Golden Rule

**UI is not a game entity.** Never mix UI elements into your ECS, physics system, or world-space scene graph. The two systems have fundamentally different coordinate spaces and lifecycles:

| Concern | Game World | UI Layer |
|---------|-----------|----------|
| Coordinates | World space (camera-transformed) | Absolute screen pixels |
| Physics | Yes | No |
| SpriteBatch transform | Camera matrix | Identity (no matrix) |
| Draw order | Per frame, sorted by depth/layer | Painter's algorithm, tree order |
| Lifetime | Managed by scene | Managed by UI tree root |

Always render UI in its own `SpriteBatch.Begin()` call **after** the world batch, with no `transformMatrix`:

```csharp
// In Draw():
// 1. World batch (with camera matrix)
_worldBatch.Begin(transformMatrix: _cameraMatrix);
DrawWorld();
_worldBatch.End();

// 2. UI batch (no matrix — absolute screen coords)
_uiBatch.Begin();
_uiRoot.Draw(_uiBatch);
_uiBatch.End();
```

## The Visual Tree

A UI system is a tree (directed acyclic graph), not a flat list. Every element knows its parent and its children. This unlocks:

- **Relative positioning** — children positions are relative to the parent; the layout pass converts them to absolute screen coords (see `monogame-ui-layout`).
- **State inheritance** — hiding or disabling a parent automatically hides/disables all descendants.
- **Batch operations** — a single `Update()` / `Draw()` call on the root propagates to the entire tree.

`UIElement` is a **`partial class`** deliberately split across files:
- `UIElement.Core.cs` — structure (this skill)
- `UIElement.Layout.cs` — Measure/Arrange fields (`monogame-ui-layout`)
- `UIElement.Focus.cs` — gamepad neighbor IDs (`monogame-ui-focus`)

This keeps each skill's code self-contained while producing one coherent class when all files are compiled together.

## UIElement Base Class

Key fields in `UIElement.Core.cs` (see `references/ui-core.md` for full code):

| Field | Type | Description |
|-------|------|-------------|
| `Parent` | `UIElement` | Null for the root node |
| `Children` | `List<UIElement>` | Direct children only |
| `Bounds` | `Rectangle` | Absolute screen rectangle; set by the layout Arrange pass |
| `IsVisible` | `bool` | False = skip Draw and hit testing |
| `IsEnabled` | `bool` | False = skip Update and input |
| `Opacity` | `float` | 0–1, multiplied with children's opacity |

Methods to override:
- `virtual void Update(GameTime gameTime)` — input and animation logic
- `virtual void Draw(SpriteBatch spriteBatch)` — self rendering only (children handled by UIContainer)
- `virtual void OnChildAdded(UIElement child)` / `OnChildRemoved` — hook for layout invalidation

**Allocation rule:** Never allocate `new Rectangle(...)`, `new Vector2(...)`, or `new Color(...)` inside `Update()` or `Draw()`. Pre-compute and store as fields.

## UIContainer

`UIContainer` extends `UIElement` and owns the recursive traversal. Its `Update` and `Draw` iterate `Children` with an indexed `for` loop — never `foreach`, never LINQ:

```csharp
// Correct — no allocations
for (int i = 0; i < Children.Count; i++)
{
    if (Children[i].IsVisible)
        Children[i].Draw(spriteBatch);
}
```

`Add(child)` / `Remove(child)` set `child.Parent` and raise `_layoutDirty` on the nearest container ancestor.

## Painter's Algorithm

Draw parent before children. The deepest (most nested) child is drawn last = appears on top. Do not use depth sorting for UI — tree order is the draw order:

```
Root (panel background)
 └─ Header (label text)
 └─ Body (list background)
     └─ Item 0 (row background → row text)
     └─ Item 1 (row background → row text)
     └─ Scrollbar
```

Each node calls `Draw(spriteBatch)` for itself, then `UIContainer` calls `Draw` on each child in order.

## The Pragmatic Alternative: Stardew Valley Style

For jam games, prototypes, or when extending Stardew Valley–compatible codebases, the full tree architecture may be overkill. The Stardew pattern uses:

- **`IClickableMenu`** — abstract base for a full "screen" of UI (inventory, shop, dialog). Each menu is a self-contained unit.
- **`ClickableTextureComponent`** — stores a `Rectangle bounds` and a `string name`. No `Update`/`Draw` of its own.
- **Constructor math** — layout calculated once from `Game1.viewport` size. On window resize, the menu is destroyed and re-created.
- **`receiveLeftClick(int x, int y)`** — the game calls this; the menu does `if (btn.containsPoint(x,y))` chains.

When to use it:
- Building a single, static menu (settings screen, pause menu)
- Extending or modding an existing Stardew-style codebase
- Jam / rapid prototype with a known, fixed resolution

When NOT to use it:
- Dynamic layouts (content that changes size at runtime)
- Reusable component libraries
- Resolution-independent UIs

## Frame Rendering Order (Complete)

```
Update():
  1. World entities update (physics, AI, animation)
  2. _uiRoot.Update(gameTime)  ← hit testing happens here

Draw():
  1. SetRenderTarget(null)
  2. _worldBatch.Begin(transformMatrix: cameraMatrix)
     DrawWorld()
     _worldBatch.End()
  3. _uiBatch.Begin()           ← NO transformMatrix
     _uiRoot.Draw(_uiBatch)
     _uiBatch.End()
```

## Anti-Patterns

- Do not pass a camera `transformMatrix` to the UI `SpriteBatch.Begin()`.
- Do not put game-world queries (physics raycasts, ECS lookups) inside `UIElement.Draw()`.
- Do not use `foreach` or LINQ to iterate `Children` — allocates enumerators on the heap.
- Do not share a `SpriteBatch` instance between world and UI — different states, different Begin/End pairs.

## Reference

For the full `UIElement.Core.cs` and `UIContainer` templates, read `references/ui-core.md`.
