---
name: entrance-animations
description: Use when elements need to appear on screen - page loads, modals opening, items being added, content reveals, or any "coming into view" animation.
---

# Entrance Animations

Apply Disney's 12 principles when bringing elements into view.

## Principle Application

**Squash & Stretch**: Scale from 95% to 100% on entry. Elements feel elastic, not rigid.

**Anticipation**: Start slightly below/smaller than final position. A -10px offset before sliding up creates expectation.

**Staging**: Enter from the direction of user attention. New list items from the top, modals from center, sidebars from their edge.

**Straight Ahead vs Pose-to-Pose**: Use pose-to-pose. Define clear start state (invisible, offset) and end state (visible, positioned).

**Follow Through & Overlapping**: Child elements should lag slightly. Container enters first, content 50-100ms after.

**Slow In/Slow Out**: Use ease-out for entrances. Fast start, gentle landing: `cubic-bezier(0, 0, 0.2, 1)`.

**Arcs**: Combine Y and X movement. Don't just fade - slide in on a subtle curve.

**Secondary Action**: Pair fade with scale. Opacity 0→1 while scaling 0.95→1 adds depth.

**Timing**:
- Quick entrances: 150-200ms (toasts, tooltips)
- Standard entrances: 200-300ms (modals, cards)
- Dramatic reveals: 300-500ms (hero sections, page transitions)

**Exaggeration**: Scale can start at 0.8 for dramatic effect, 0.95 for subtle polish.

**Solid Drawing**: Maintain consistent 3D space. Elements entering from "behind" should scale up; from sides should slide.

**Appeal**: Entrances should feel welcoming. Avoid jarring pops - everything deserves an introduction.

## Timing Recommendations

| Element Type | Duration | Easing | Delay Pattern |
|-------------|----------|--------|---------------|
| Toast/Alert | 150ms | ease-out | None |
| Modal | 250ms | ease-out | Content +50ms |
| Card/Item | 200ms | ease-out | None |
| List Items | 200ms | ease-out | Stagger 50ms |
| Page Section | 300ms | ease-out | Stagger 100ms |
| Hero Content | 400ms | ease-out | Stagger 150ms |

## Implementation Pattern

```css
.entering {
  animation: entrance 250ms cubic-bezier(0, 0, 0.2, 1) forwards;
}

@keyframes entrance {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
```

## Stagger Formula

For multiple items: `delay = index * 50ms`, cap at 500ms total sequence time.

Never exceed 5 items in a stagger sequence without user-initiated action.
