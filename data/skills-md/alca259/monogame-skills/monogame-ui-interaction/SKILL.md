---
name: monogame-ui-interaction
description: MonoGame UI hit testing and event bubbling — DFS reverse traversal to find the topmost element under the cursor, UIEventArgs with Handled flag, pointer event propagation up the visual tree, and hover state management. Use this skill whenever the user asks about detecting clicks on UI elements, mouse-over effects, OnClick handlers, event bubbling, hit testing, containsPoint, "why does my button not respond to clicks", or any pointer interaction with MonoGame UI.
---

# MonoGame UI Interaction — Hit Testing & Event Bubbling

This skill covers how pointer input (mouse, touch) connects to UI elements. For input polling fundamentals (prev/curr state), see `monogame-input`. For keyboard/gamepad focus, see `monogame-ui-focus`. For complete code templates, read `references/ui-interaction.md`.

## Assumed Contract

> **UIElement.Bounds must be an up-to-date absolute screen Rectangle before hit testing runs.** If Bounds is empty (`Rectangle.Empty` or default), no element will be hit. Always run the layout Arrange pass (from `monogame-ui-layout`) before processing pointer input.
>
> Hit testing reads `MouseState` from `monogame-input`'s prev/curr state pattern — do not poll `Mouse.GetState()` a second time inside UI update code.

## Hit Testing: DFS Reverse Traversal

The visual tree is painted parent → children (painter's algorithm). The child drawn last appears on top. Therefore, hit testing must check children in **reverse order** (last drawn = first tested):

```
Tree:                   Draw order:   Hit test order:
Root                    1. Root       5. Root
 ├─ PanelA              2. PanelA     4. PanelA
 │   ├─ ButtonX         3. ButtonX    3. ButtonX  ← check first
 │   └─ ButtonY         4. ButtonY    2. ButtonY
 └─ PanelB              5. PanelB     1. PanelB   ← check last (drawn on top!)
```

The DFS walks children from `Count-1` down to `0`, recursing depth-first. The first element whose `Bounds.Contains(point)` returns true and has no visible child also containing the point is the **hit target**.

Only test elements where `IsVisible == true` and `IsEnabled == true`.

## UIEventArgs and the Handled Flag

```csharp
public class UIPointerEventArgs
{
    public Point Position;    // screen coordinates
    public bool Handled;      // set to true to stop bubbling
}
```

`Handled = true` means "I consumed this event — stop propagating." This prevents a button click from also triggering the panel behind it.

## Event Bubbling

After finding the deepest hit target, fire the event on it. If `Handled` remains false, the event propagates up through `Parent` until it reaches the root or a handler sets `Handled = true`:

```
Click at ButtonX
  → ButtonX.OnPointerDown(args)   args.Handled = true  → stop
  (PanelA.OnPointerDown never fires)

Click at empty area of PanelA
  → (no child consumed it)
  → PanelA.OnPointerDown(args)
```

## Hover State

Track `IsHovered` as a boolean field on `UIElement`. Each frame:
1. Run the DFS hit test to find the element under the cursor.
2. If it differs from last frame's hovered element, fire `OnPointerLeave` on the old one and `OnPointerEnter` on the new one.
3. `IsHovered` changes only at `OnPointerEnter` / `OnPointerLeave` — never computed on-the-fly in `Draw`.

This avoids per-frame allocations and keeps rendering code free of input logic.

## Where to Run Hit Testing

Run the full hit test in `UIContainer.Update()`, after children's own `Update()` calls. This ordering ensures children see input before parents (deepest = highest priority):

```csharp
// In your root UIContainer.Update():
// 1. Run layout if dirty
// 2. Poll input (prev/curr mouse state)
// 3. Run hit test DFS
// 4. Fire hover enter/leave
// 5. On click: bubble event up
```

## Click vs. Press vs. Release

Use the prev/curr state pattern from `monogame-input`:

| Event | Condition |
|-------|-----------|
| `OnPointerDown` | left button `Pressed` this frame, `Released` last frame |
| `OnPointerUp` | left button `Released` this frame, `Pressed` last frame |
| `OnClick` | `OnPointerUp` fired on the same element that received `OnPointerDown` (click = press + release on same target) |

Track `_pressedElement` to implement the click contract:

```csharp
if (justPressed)
    _pressedElement = hitTarget;

if (justReleased && _pressedElement == hitTarget)
    BubbleEvent(hitTarget, OnClickArgs);

if (justReleased)
    _pressedElement = null;
```

## Stardew Approach: containsPoint Chains

For simple static menus where the full bubbling system is overkill:

```csharp
public void ReceiveLeftClick(int x, int y)
{
    if (_okButton.ContainsPoint(x, y))
    {
        // handle OK
        return;  // explicit "stop" — no bubbling needed
    }
    if (_cancelButton.ContainsPoint(x, y))
    {
        // handle Cancel
        return;
    }
}
```

Add `return` after each handler — this is the manual equivalent of `Handled = true`.

## Anti-Patterns

- Do not call `Mouse.GetState()` inside individual element `Update()` methods — poll once at the root and pass the result down.
- Do not allocate `new UIPointerEventArgs()` every frame — pool or reuse a single instance per frame.
- Do not test hidden elements (`IsVisible == false`) — skip them in the DFS loop.
- Do not put layout calculations inside hit test code — Bounds must already be set.

## Reference

Complete DFS hit test, BubbleEvent, UIPointerEventArgs, and hover management: `references/ui-interaction.md`.
