---
name: monogame-ui-dropdown
description: MonoGame UI Dropdown / ComboBox control — collapsed header showing the selected item plus an arrow, expandable overlay list of options, keyboard/gamepad navigation, and automatic positioning to stay within screen bounds. Use this skill whenever the user asks about a dropdown, combo box, select list, option picker, "how do I let the user choose from a list of options" in a UI, or any collapsed-expand selection control in MonoGame UI.
---

# MonoGame UI Dropdown

A dropdown (combo box) shows a single selected item in a collapsed header. On click or Enter, it expands an overlay list below (or above if near the bottom of the screen). Selecting an item collapses the list and fires `SelectionChanged`. For complete code, read `references/ui-dropdown.md`.

## Assumed Contract

Extends `UIElement` from `monogame-ui-core`. Receives pointer events from `monogame-ui-interaction`. Participates in focus via `monogame-ui-focus`. The expanded list is drawn as an **overlay at the end of the UI Draw pass**, always on top of other elements.

## Two-State Architecture

```
Collapsed state:
  [Selected Item Text ▼]     ← draws as a single button-like element

Expanded state:
  [Selected Item Text ▲]     ← header still visible
  ┌────────────────────┐
  │ Option A           │     ← overlay list; drawn last (above everything)
  │ Option B  ←selected│
  │ Option C           │
  └────────────────────┘
```

The overlay list is not part of the normal layout tree. It is drawn by `UIOverlayManager` after the entire UI tree is drawn — this ensures it appears above sibling panels.

## Overlay Management

Never place the expanded list as a child of the dropdown itself — it would be clipped by any parent scissor rectangle and drawn at the wrong Z-order.

Inject `UIOverlayManager` into the constructor — do not use it as a static. The dropdown holds a reference to an overlay `UIPanel` and calls `Show`/`Hide` on the manager:

```csharp
// Constructor — UIOverlayManager is injected (usually via Core.UIOverlay):
var dropdown = new Dropdown(Core.UIOverlay);

// When dropdown opens:
_overlayManager.Show(_listPanel);   // panel draws on top of everything

// When dropdown closes:
_overlayManager.Hide(_listPanel);
```

The root `Game.Draw()` calls `UIOverlayManager.Draw(spriteBatch)` after `_uiRoot.Draw(spriteBatch)`.

## Screen-Boundary Flip

Before opening the list, check if the list would overflow the screen bottom:

```csharp
int listHeight = _items.Count * ItemHeight;
bool flipUp    = (Bounds.Bottom + listHeight) > screenHeight;
_listBounds    = flipUp
    ? new Rectangle(Bounds.X, Bounds.Y - listHeight, Bounds.Width, listHeight)
    : new Rectangle(Bounds.X, Bounds.Bottom,          Bounds.Width, listHeight);
```

## Keyboard Navigation

When expanded and focused:
- **Up / Down** — move highlighted index within the list (does NOT immediately select)
- **Enter / A** — confirm selection, collapse
- **Escape / B** — cancel, collapse without changing selection

When collapsed and focused:
- **Enter / A / Space** — expand
- **Up / Down** — navigate directly (selects immediately, no expand needed for simple cases)

## Click Outside to Close

Track "expanded" state. In `UIInteractionManager.Update()`, if any click occurs and the hit target is not the dropdown or its overlay, call `dropdown.Close()`. The simplest implementation: the overlay registers itself as a full-screen transparent hit area behind the list content.

## Items

Add string items via `AddItem(string text)`. For rich items (icon + label), pass a `UIElement` as the item template — the dropdown measures it for `ItemHeight`.

## Anti-Patterns

- Never draw the expanded list as a child of the dropdown element — it will be clipped and Z-ordered incorrectly.
- Never keep the list open across scene/screen transitions — always call `Close()` on screen exit.
- Never allocate new `Rectangle` objects for `_listBounds` every frame — compute once on open, cache.

## Reference

Complete `Dropdown`, `UIOverlayManager`, and overlay draw pattern: `references/ui-dropdown.md`.
