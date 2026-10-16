---
name: monogame-ui-controls
description: MonoGame UI component library — Label, Button (with hover animation), ProgressBar/health bar, ScrollView with scissor clipping, Panel, Sprite (texture display), and Checkbox. Use this skill whenever the user asks about specific UI components - buttons, labels, text display, health bars, progress bars, scroll views, inventory slots, dialog boxes, tooltips, panels, image/sprite in UI, checkbox, toggle, or "how do I build a specific component" in MonoGame — even if they just say "I need a button", "how do I make a health bar", or "how do I show an image in my UI".
---

# MonoGame UI Controls — Component Library

Ready-to-use UI components built on `UIElement` from `monogame-ui-core`. For layout positioning, see `monogame-ui-layout`. For click/hover events, see `monogame-ui-interaction`. For complete code templates, read `references/ui-controls.md`.

## Assumed Contract

> Controls in this skill extend `UIElement` (partial class from `monogame-ui-core`). They implement `Measure`/`Arrange` from `monogame-ui-layout` and receive pointer events via the hit test/bubbling system from `monogame-ui-interaction`. If you need gamepad navigation, assign neighbor IDs and register with `UIFocusManager` from `monogame-ui-focus`.
>
> `RasterizerState` for scissor clipping is created **once** (in the constructor or `LoadContent`) — never inside `Draw()`.

## Label

Wraps `SpriteFont.MeasureString` to auto-size and supports horizontal/vertical alignment.

**Measure:** Call `font.MeasureString(text)`, store as `DesiredSize`. Respect `FixedSize` if set.  
**Draw:** Call `spriteBatch.DrawString` — position computed from `Bounds` + alignment offset.

**Rules:**
- Store the measured `Vector2` size as a field; only re-measure when `Text` changes (set the dirty flag in the setter).
- Apply `EffectiveOpacity` as the alpha channel of the draw color.
- For word wrap, split text manually into lines at spaces — do not use LINQ or `string.Split` inside `Draw()`.

## Button

Button extends `Label` (or has a `Label` child) and adds three states: Normal, Hovered, Pressed. Each state can have a different texture region or color tint.

**Hover animation:** Scale pulse — `_currentScale` (float field) lerps toward `_targetScale`:
```
Normal  → _targetScale = 1.0f
Hovered → _targetScale = 1.05f
Pressed → _targetScale = 0.97f
```

In `Update()`:
```csharp
_currentScale += (_targetScale - _currentScale) * 12f * deltaTime;
```

In `Draw()`, apply scale from the center of `Bounds`:
```csharp
Vector2 origin = new Vector2(_texture.Width / 2f, _texture.Height / 2f);
Vector2 center = Bounds.Center.ToVector2();
// Draw background texture scaled from center
spriteBatch.Draw(_texture, center, sourceRect, tintColor * EffectiveOpacity,
    0f, origin, _currentScale, SpriteEffects.None, 0f);
```

**No `new Vector2()`** inside `Draw()` — cache `origin` as a field (computed once in constructor or when `FixedSize` changes).

## ProgressBar / Health Bar

Renders two rectangles: a background and a fill bar whose width is `fillFraction * Bounds.Width`.

```csharp
int fillWidth = (int)(FillFraction * Bounds.Width);
var fillRect  = new Rectangle(Bounds.X, Bounds.Y, fillWidth, Bounds.Height);
```

`fillRect` is recomputed each Draw call — it's cheap (integer math) and avoids a stale cached value when `FillFraction` changes mid-frame.

**Color interpolation** (green → yellow → red):
```csharp
Color barColor = FillFraction > 0.5f
    ? Color.Lerp(Color.Yellow, Color.Green, (FillFraction - 0.5f) * 2f)
    : Color.Lerp(Color.Red,    Color.Yellow, FillFraction * 2f);
```

No allocations. `Color.Lerp` returns a struct.

## ScrollView

`ScrollView` clips its children to its visible area using a `ScissorRectangle`. Content taller/wider than the view is scrolled via an offset.

**Scissor setup (once in constructor):**
```csharp
_scissorState = new RasterizerState { ScissorTestEnable = true };
```

**Draw:**
```csharp
// End the current SpriteBatch, restart with scissor state.
spriteBatch.End();

Rectangle savedScissor = graphicsDevice.ScissorRectangle;

// Always intersect with the parent scissor to handle nested scroll views.
Rectangle clip = Rectangle.Intersect(Bounds, savedScissor);
graphicsDevice.ScissorRectangle = clip;

spriteBatch.Begin(SpriteSortMode.Deferred, BlendState.AlphaBlend,
    SamplerState.LinearClamp, null, _scissorState);

// Draw children with scroll offset applied
for (int i = 0; i < Children.Count; i++)
{
    // Temporarily shift child Bounds by -_scrollOffset before drawing.
    // Restore after. OR: pass offset into a virtual DrawWithOffset method.
    Children[i].Draw(spriteBatch);
}

spriteBatch.End();

// Restore previous scissor and restart the parent batch.
graphicsDevice.ScissorRectangle = savedScissor;
spriteBatch.Begin(SpriteSortMode.Deferred, BlendState.AlphaBlend,
    SamplerState.LinearClamp, null, null);
```

**Nested scissor rule:** Always call `Rectangle.Intersect(myBounds, parentScissor)` — never assign `myBounds` directly. A child `ScrollView` inside a `Panel` must not draw outside the `Panel`'s clip region.

**Scroll offset:** Update via mouse wheel delta or drag. Clamp `_scrollOffset.Y` to `[0, contentHeight - Bounds.Height]`.

## Panel

A container with a background drawn before its children. Background can be:
- A solid color (draw a 1×1 white pixel texture scaled to `Bounds`)
- A 9-slice (nine-patch) texture for scalable borders

**9-slice draw pattern:** Split the texture into a 3×3 grid of corner/edge/center regions; draw each piece into the corresponding sub-rectangle of `Bounds`. Store the `Rectangle` slice definitions as static fields — they never change.

## Tooltip

Attach to any element via `element.Tooltip = new Tooltip(font, "description")`. Draw at the end of the UI pass, above all other elements:

```csharp
// In Draw, after _uiRoot.Draw:
if (_hoveredElement?.Tooltip != null)
    _hoveredElement.Tooltip.Draw(spriteBatch, mousePos, screenBounds);
```

Clamp tooltip `Bounds` to screen edges before drawing so it never overflows off-screen.

## Scissor Nesting Rule (Summary)

Every container that applies `ScissorRectangle` must:
1. Read the current `GraphicsDevice.ScissorRectangle` before changing it.
2. Apply `Rectangle.Intersect(myClip, currentScissor)` as the new scissor.
3. Restore the saved scissor after drawing children.

Failure to intersect causes child containers to "escape" their parent's clip area.

## Anti-Patterns

- Never create `RasterizerState` inside `Draw()` — it allocates GPU state and triggers GC.
- Never cache `Bounds.Center.ToVector2()` as a `Vector2` field and forget to update it when layout runs — recalculate from `Bounds` in `Draw` if needed (it's cheap) or invalidate the cache in `Arrange()`.
- Never use `string.Split` or LINQ for word wrap inside `Draw()`.
- Never apply a camera transform matrix to the scissor-clipped SpriteBatch batch.

## Sprite (UISprite)

Displays a `Texture2D` inside its `Bounds`. The primary use case is decorative images, icons, backgrounds inside panels, and avatar portraits in dialogue boxes.

**Measure:** Returns the texture's natural size unless `FixedSize` is set. Use `FixedSize` to stretch/fit the image to a specific area.

**Draw modes:**

| Mode | Behavior |
|------|---------|
| `Stretch` | Draws texture scaled to fill `Bounds` exactly |
| `Fit` | Scales uniformly to fit within `Bounds`, preserving aspect ratio |
| `Crop` | Draws at natural size; content outside `Bounds` is clipped (requires scissor) |
| `Tile` | Uses `SamplerState.LinearWrap` to tile the texture (see `monogame-2d`) |

Source rectangle (`SourceRect`) allows using a texture atlas — set it to the sprite's region within the atlas.

```csharp
var icon = new UISprite(texture) { DrawMode = SpriteDrawMode.Fit };
panel.Add(icon);
```

## Checkbox

A toggle control with a checked/unchecked visual state. Fires `CheckedChanged` when toggled.

**Anatomy:** Background box (drawn from texture or solid rectangle) + optional checkmark sprite drawn on top when checked.

**Update:** On `OnClick`, flip `IsChecked` and fire `CheckedChanged`. No `Update()` logic needed beyond what `UIElement` inherits.

**Keyboard:** When focused (from `monogame-ui-focus`), Space bar toggles the checked state via `HandleKeyboardInput`.

```csharp
var chk = new UICheckbox(font, "Enable music");
chk.CheckedChanged += (sender, isChecked) => AudioManager.MusicEnabled = isChecked;
```

For mutually exclusive options (only one can be selected), use `monogame-ui-radiobutton` instead.

## Anti-Patterns

- Never create `RasterizerState` inside `Draw()` — it allocates GPU state and triggers GC.
- Never cache `Bounds.Center.ToVector2()` as a `Vector2` field and forget to update it when layout runs — recalculate from `Bounds` in `Draw` if needed (it's cheap) or invalidate the cache in `Arrange()`.
- Never use `string.Split` or LINQ for word wrap inside `Draw()`.
- Never apply a camera transform matrix to the scissor-clipped SpriteBatch batch.

## Reference

Complete Label, Button, ProgressBar, ScrollView, Panel, Tooltip, UISprite, and Checkbox templates: `references/ui-controls.md`.
