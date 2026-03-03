---
name: hover-interactions
description: Use when creating mouse hover effects - button highlights, card lifts, link underlines, image zooms, or any pointer-triggered animation.
---

# Hover Interaction Animations

Apply Disney's 12 principles to mouse hover states.

## Principle Application

**Squash & Stretch**: Cards can subtly scale (1.02-1.05) on hover, creating "lift" effect.

**Anticipation**: Hover IS anticipation for click. The hover state previews the interaction.

**Staging**: Hover effects should highlight the interactive element, not distract from it.

**Straight Ahead vs Pose-to-Pose**: Define rest and hover poses precisely. Transition smoothly between them.

**Follow Through & Overlapping**: Child elements animate after parent. Card lifts, then shadow expands.

**Slow In/Slow Out**: Hover-in: ease-out (fast response). Hover-out: ease-in-out (graceful return).

**Arcs**: Underlines can draw from center outward. Highlights sweep in curved paths.

**Secondary Action**: Combine multiple subtle effects. Scale + shadow + color shift together.

**Timing**:
- Hover response: 150-200ms (must feel responsive)
- Hover exit: 200-300ms (can be slightly slower)
- Never exceed 300ms for hover-in

**Exaggeration**: Subtle - hover is preview, not performance. Scale max 1.05, shadow max +8px.

**Solid Drawing**: Hover states must feel like the same element elevated, not a replacement.

**Appeal**: Hover should invite clicking. Create anticipation without demanding action.

## Timing Recommendations

| Hover Effect | Hover-In | Hover-Out | Easing |
|-------------|----------|-----------|--------|
| Color Change | 150ms | 200ms | ease-out / ease-in-out |
| Scale/Lift | 200ms | 250ms | ease-out / ease-in-out |
| Shadow | 200ms | 250ms | ease-out / ease-in-out |
| Underline Draw | 200ms | 200ms | ease-out |
| Image Zoom | 300ms | 400ms | ease-out |
| Icon Shift | 150ms | 200ms | ease-out |

## Implementation Patterns

```css
/* Card lift with shadow */
.card {
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
}

.card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

/* Slower return */
.card:not(:hover) {
  transition: transform 250ms ease-in-out, box-shadow 250ms ease-in-out;
}

/* Underline draw from center */
.link {
  position: relative;
}

.link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: currentColor;
  transition: width 200ms ease-out, left 200ms ease-out;
}

.link:hover::after {
  width: 100%;
  left: 0;
}
```

## Icon Animation Pattern

```css
.button-icon {
  transition: transform 150ms ease-out;
}

.button:hover .button-icon {
  transform: translateX(4px);
}

/* Arrow grows */
.arrow-icon {
  transition: transform 150ms ease-out;
}

.link:hover .arrow-icon {
  transform: translateX(4px) scale(1.1);
}
```

## Key Rules

1. Touch devices don't have hover - ensure functionality without it
2. Hover-in must be under 200ms to feel responsive
3. Don't move elements enough to cause mis-clicks
4. Test with `@media (hover: hover)` to scope to pointer devices
5. Combine max 3 properties to avoid overwhelming

```css
@media (hover: hover) {
  .card:hover { /* hover effects */ }
}
```
