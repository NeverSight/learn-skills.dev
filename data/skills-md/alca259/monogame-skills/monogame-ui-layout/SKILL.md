---
name: monogame-ui-layout
description: MonoGame UI layout engine — Measure & Arrange two-pass system, StackPanel, Canvas, FlowLayoutPanel, anchoring, dirty-flag invalidation, and resolution-independent UI scaling. Use this skill whenever the user asks about positioning UI elements, centering a button, building a StackPanel, FlowLayout, or grid layout, anchoring elements to screen edges, scaling UI for different resolutions, or any question about "how do I arrange/layout UI" in MonoGame — even if they just say "how do I center my health bar", "how do I flow items like CSS flexbox", or "my UI breaks on different resolutions". For XAML-style Grid with rows and columns, see monogame-ui-grid.
---

# MonoGame UI Layout Engine

This skill covers the Measure & Arrange layout system that sits on top of `UIElement` from `monogame-ui-core`. For click/hover handling, see `monogame-ui-interaction`. For complete code templates, read `references/ui-layout.md`.

## Assumed Contract

This skill extends `UIElement` defined in `monogame-ui-core`:
- `UIElement.Bounds` (Rectangle) is the **absolute screen rectangle** set by the Arrange pass. Hit testing and rendering depend on it being up to date.
- `UIContainer.LayoutDirty` flag triggers re-layout. It is set automatically on `Add()` / `Remove()`.

The layout partial class lives in `UIElement.Layout.cs` and adds `DesiredSize`, `Measure`, and `Arrange` to the existing partial class.

## The Two-Pass Model

Layout runs only when `LayoutDirty == true` — never unconditionally every frame.

```
Invalidation  →  Measure (bottom-up)  →  Arrange (top-down)
```

### Pass 1: Measure (bottom-up)

Each node asks its children how much space they need. Leaf nodes calculate their own natural size (text size, sprite size). Parent nodes sum or wrap children sizes.

- Input: `available` (Vector2) — the space the parent is offering
- Output: sets `DesiredSize` (Vector2) — how much space this node wants
- Must call `Measure(available)` on all children before computing own `DesiredSize`

### Pass 2: Arrange (top-down)

The root calls `Arrange` with the full screen rectangle. Each parent assigns `Bounds` (the final absolute Rectangle) to each child.

- Input: `finalRect` (Rectangle) — the absolute area the parent is giving this node
- Output: sets `this.Bounds = finalRect`, then calls `Arrange` on children with their sub-rectangles

**Critical:** Never read `Bounds` during `Measure`. `Bounds` is only valid after `Arrange` completes.

## Triggering Layout

```csharp
// In your root container's Update, before processing input:
if (LayoutDirty)
{
    Measure(new Vector2(screenWidth, screenHeight));
    Arrange(new Rectangle(0, 0, screenWidth, screenHeight));
    LayoutDirty = false;
}
```

Invalidate manually when content changes (text changed, texture swapped, child added):
```csharp
public string Text
{
    get => _text;
    set { _text = value; InvalidateLayout(); }
}

private void InvalidateLayout()
{
    UIContainer ancestor = Parent as UIContainer;
    while (ancestor != null) { ancestor.LayoutDirty = true; ancestor = ancestor.Parent as UIContainer; }
}
```

Also call `InvalidateLayout()` when the window is resized (`Window.ClientSizeChanged` event).

## No LINQ — Ever

LINQ allocates intermediate collections on the heap. In MonoGame, repeated GC pressure causes frame-rate stuttering. This rule is absolute:

> **NEVER use `.Select()`, `.Where()`, `.Sum()`, `.ToList()`, `.OrderBy()`, or any LINQ method inside `Measure()` or `Arrange()`.**

Use indexed `for` loops:

```csharp
// Correct
int total = 0;
for (int i = 0; i < Children.Count; i++)
    total += (int)Children[i].DesiredSize.X;

// WRONG — allocates IEnumerable + enumerator
int total = Children.Sum(c => c.DesiredSize.X);
```

The same rule applies to `foreach` on `Children` — use indexed `for`.

## StackPanel

`StackPanel` arranges children in a line with optional spacing. Orientation is Horizontal or Vertical.

**Measure:** Sum children sizes along the axis + spacing gaps; max size on the cross-axis.  
**Arrange:** Walk children in order, assigning each a Rectangle offset from the previous.

See `references/ui-layout.md` for the complete implementation.

## Canvas

`Canvas` positions children at explicit offsets relative to the Canvas's top-left corner.

**Measure:** Returns max of all children's desired sizes (or a fixed size if set).  
**Arrange:** Each child's `Bounds` = `Canvas.Bounds.Location + child.Offset`.

Children on a Canvas must set their own `DesiredSize` in `Measure()`.

## Anchoring

Anchors define which corner/edge of the parent a child is positioned relative to. Compute the child's position in `Arrange()` based on `Anchor`:

| Anchor | Formula |
|--------|---------|
| `TopLeft` | `(parent.X + offsetX, parent.Y + offsetY)` |
| `TopRight` | `(parent.Right - childW - offsetX, parent.Y + offsetY)` |
| `BottomLeft` | `(parent.X + offsetX, parent.Bottom - childH - offsetY)` |
| `BottomRight` | `(parent.Right - childW - offsetX, parent.Bottom - childH - offsetY)` |
| `Center` | `(parent.Center.X - childW/2, parent.Center.Y - childH/2)` |
| `TopCenter` | `(parent.Center.X - childW/2, parent.Y + offsetY)` |
| `BottomCenter` | `(parent.Center.X - childW/2, parent.Bottom - childH - offsetY)` |

Store `Anchor` and `Offset` (Vector2) as fields on the element; apply in Arrange.

## Resolution-Independent UI

Design at a fixed virtual resolution and apply a scale matrix to the UI `SpriteBatch.Begin()` call. This is the same technique used in `monogame-2d` for the game world, but **without a camera — the UI root is always at (0,0) of the virtual canvas**:

```csharp
// Compute once per frame (or on window resize):
float scaleX = GraphicsDevice.Viewport.Width  / (float)VirtualWidth;
float scaleY = GraphicsDevice.Viewport.Height / (float)VirtualHeight;
Matrix uiScale = Matrix.CreateScale(scaleX, scaleY, 1f);

// Apply to the UI batch only:
_uiBatch.Begin(transformMatrix: uiScale);
_uiRoot.Draw(_uiBatch);
_uiBatch.End();
```

All layout math (Measure/Arrange) uses virtual resolution coordinates. The matrix stretches them to the real screen.

**On window resize:** Rebuild `uiScale` and call `InvalidateLayout()` on the root so all Bounds are recalculated in virtual space.

## The Stardew Alternative: Constructor Math

When the full Measure/Arrange engine is overkill, calculate positions once in the constructor:

```csharp
public MyMenu(int screenW, int screenH)
{
    int x = screenW / 2 - Width / 2;
    int y = screenH / 2 - Height / 2;
    Bounds = new Rectangle(x, y, Width, Height);
    _okButton.Bounds = new Rectangle(x + Width - 120, y + Height - 50, 100, 36);
}
```

On resize, destroy and re-create the menu. Acceptable for static, single-screen menus; not suitable for dynamic or reusable layouts.

## Anti-Patterns

- Never call `Measure` or `Arrange` every frame without a dirty check — expensive even if nothing changed.
- Never read `Bounds` during `Measure` — it's stale or zero until `Arrange` completes.
- Never use LINQ or `foreach` on `Children` inside layout methods.
- Never allocate new structs (`new Vector2(...)`, `new Rectangle(...)`) inside tight layout loops — pre-compute or mutate fields.

## FlowLayoutPanel

`FlowLayoutPanel` arranges children in a line (horizontal by default) and **wraps to the next line** when they would exceed the container's width — equivalent to CSS `flex-wrap: wrap`.

**Measure:** Simulate the wrap to compute total height needed (or width for vertical flow).  
**Arrange:** Walk children, advancing the cursor; when `cursor + childW > containerW`, start a new row.

Line height = the tallest child on that row. Use `ItemSpacing` (horizontal gap) and `LineSpacing` (vertical gap between rows).

No LINQ — use indexed `for` with local tracking variables for `rowStart`, `rowMaxHeight`, `cursorX`.

```csharp
var flow = new FlowLayoutPanel { ItemSpacing = 8, LineSpacing = 4 };
flow.Add(new UIButton(...));
flow.Add(new UIButton(...));
// Buttons wrap automatically when the panel is too narrow.
```

## Anti-Patterns

- Never call `Measure` or `Arrange` every frame without a dirty check — expensive even if nothing changed.
- Never read `Bounds` during `Measure` — it's stale or zero until `Arrange` completes.
- Never use LINQ or `foreach` on `Children` inside layout methods.
- Never allocate new structs (`new Vector2(...)`, `new Rectangle(...)`) inside tight layout loops — pre-compute or mutate fields.

## Reference

Complete `UIElement.Layout.cs`, `StackPanel`, `Canvas`, `FlowLayoutPanel`, and anchor code: `references/ui-layout.md`.
