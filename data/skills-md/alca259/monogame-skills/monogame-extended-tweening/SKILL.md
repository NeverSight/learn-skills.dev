---
name: monogame-extended-tweening
description: >
  MonoGame.Extended Tweening guide — animating properties over time with zero allocation using
  the Tweener class and EasingFunctions. Use this skill whenever the user mentions tween,
  tweening, easing, lerp over time, animate a UI property, elastic or bounce animation,
  fade transition in code, smooth property change, or Tweener — even if they just say
  "make this button bounce when clicked" or "fade out the panel smoothly".
---

# MonoGame.Extended Tweening Implementation Guide

This skill covers property animation via the `Tweener` class from MonoGame.Extended.
Apply the rules below when writing tween code. For API signatures and ready-to-paste
examples read `references/extended-tweening.md`.

## Core Concept

A `Tweener` interpolates any property of any object between two values over time.
It holds no per-tween allocations during the update loop — all state lives in structs
pre-allocated when the tween is created.

```csharp
using MonoGame.Extended.Tweening;
```

## Lifecycle: Where Each Call Lives

| Step | Location | What to do |
|------|----------|------------|
| Create tweener | Field initializer or `LoadContent` | `new Tweener()` — one instance shared by all tweens |
| Start a tween | Input handler, event callback, or `Initialize` | `_tweener.TweenTo(...)` |
| Advance tweens | `Update(GameTime)` | `_tweener.Update(gameTime.GetElapsedSeconds())` |
| Read property | `Draw(GameTime)` | Access the target object's property directly |

Never call `TweenTo` from `Draw`. Never create a new `Tweener` per frame.

## TweenTo API

```csharp
_tweener.TweenTo(
    target:     _myObject,              // the object that owns the property
    expression: obj => obj.Position,    // lambda pointing to the property
    toValue:    new Vector2(400, 300),  // destination value
    duration:   0.5f,                   // seconds
    delay:      0f                      // seconds before starting (optional)
)
.Easing(EasingFunctions.ElasticOut)    // optional — defaults to Linear
.RepeatForever(repeatDelay: 0.2f)      // optional — loops forever with a gap
.AutoReverse();                         // optional — ping-pongs back to start
```

The property **must be a settable C# property** (not a field). For structs stored as
fields (e.g., `Vector2 _pos`), wrap them in a class or expose them via a property.

## Easing Functions Reference

All functions live in `EasingFunctions`. Each comes in three variants:
`In` (slow start), `Out` (slow end), `InOut` (slow start and end).

| Family | In | Out | InOut | Best for |
|--------|----|-----|-------|----------|
| Linear | `Linear` | — | — | Progress bars, constant motion |
| Quadratic | `QuadraticIn` | `QuadraticOut` | `QuadraticInOut` | General UI, subtle feel |
| Cubic | `CubicIn` | `CubicOut` | `CubicInOut` | Smooth UI transitions |
| Elastic | `ElasticIn` | `ElasticOut` | `ElasticInOut` | Bouncy button press, spring |
| Bounce | `BounceIn` | `BounceOut` | `BounceInOut` | Dropped object, impact feel |
| Back | `BackIn` | `BackOut` | `BackInOut` | Slight overshoot, playful UI |

Note: Quartic, Quintic, Sine, Exponential, and Circular families are listed in Extended's source but
**not available in v6's `EasingFunctions`** — do not use them. The families above are confirmed working.

**Golden rule**: for UI hover/press animations prefer `ElasticOut` or `BackOut` — they
overshoot slightly and snap back, giving the illusion of physical weight. For panel
slides prefer `CubicOut` (fast start, gentle landing).

## Animation Sequences (Chaining)

`TweenTo` returns an `ITween`. Chain modifiers immediately after the call:

```csharp
// Sequence: move → wait → return
_tweener.TweenTo(_panel, p => p.Position, openPos, duration: 0.3f)
        .Easing(EasingFunctions.CubicOut)
        .AutoReverse()
        .RepeatForever(repeatDelay: 2.0f);
```

For a true ordered sequence (move THEN rotate THEN fade), use `delay` on each tween:

```csharp
float t0 = 0f, d = 0.25f;
_tweener.TweenTo(_obj, o => o.Position, newPos,  duration: d, delay: t0);
_tweener.TweenTo(_obj, o => o.Rotation, MathF.PI, duration: d, delay: t0 + d);
_tweener.TweenTo(_obj, o => o.Alpha,    0f,       duration: d, delay: t0 + d * 2);
```

## Integration with monogame-ui-core

When a UI component owns a visual property (scale, position, alpha), expose it as a
C# property so the tweener can drive it:

```csharp
// In your button component
public float Scale { get; set; } = 1f;
public Vector2 Position { get; set; }
```

Then tween on hover/press events:

```csharp
// Hover enter — scale up with elastic overshoot
_tweener.TweenTo(_button, b => b.Scale, 1.1f, 0.15f)
        .Easing(EasingFunctions.ElasticOut);

// Hover leave — return to normal
_tweener.TweenTo(_button, b => b.Scale, 1.0f, 0.1f)
        .Easing(EasingFunctions.CubicOut);
```

For inventory panels or dialogs, tween `Position` to slide in from off-screen:

```csharp
// Slide-in: panel starts off the bottom edge, moves to its target Y
_tweener.TweenTo(_inventoryPanel, p => p.Position,
    targetPosition, duration: 0.35f)
    .Easing(EasingFunctions.CubicOut);

// Simultaneous fade-in
_tweener.TweenTo(_inventoryPanel, p => p.Alpha,
    1.0f, duration: 0.35f)
    .Easing(EasingFunctions.Linear);
```

## Anti-Patterns to Avoid

- **Never** call `TweenTo` on every `Update` frame — each call starts a new tween.
  Gate it behind a state flag or event.
- **Never** tween a field directly — the lambda `o => o._field` will not compile.
  Always use a property.
- **Never** create `new Tweener()` per Update/Draw call — one shared instance is correct.
- **Avoid** tweening `struct` properties that are returned by value from a parent struct
  (e.g., `transform.Position.X`). Tween the owning object's full property instead.

## Reference

For complete code examples and setup snippets, read `references/extended-tweening.md`.
