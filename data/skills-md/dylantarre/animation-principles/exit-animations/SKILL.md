---
name: exit-animations
description: Use when elements need to leave the screen - closing modals, dismissing notifications, removing items, page transitions out, or any "leaving view" animation.
---

# Exit Animations

Apply Disney's 12 principles when removing elements from view.

## Principle Application

**Squash & Stretch**: Scale down to 95-98% on exit. Element compresses slightly as it departs.

**Anticipation**: Brief pause or micro-movement before departure. A 50ms hesitation acknowledges the exit.

**Staging**: Exit toward logical destinations. Deleted items fall down, dismissed modals shrink to origin, sidebars return to their edge.

**Straight Ahead vs Pose-to-Pose**: Pose-to-pose with clear visible→invisible states. Plan the exit trajectory.

**Follow Through & Overlapping**: Content exits before container. Text fades 50ms before the card collapses.

**Slow In/Slow Out**: Use ease-in for exits. Gentle start, accelerating departure: `cubic-bezier(0.4, 0, 1, 1)`.

**Arcs**: Exit on curves, not straight lines. Dismissed notifications arc upward-and-out.

**Secondary Action**: Combine opacity fade with directional movement. Pure fades feel like errors.

**Timing**:
- Exits should be 20-30% faster than entrances
- Quick exits: 100-150ms (tooltips, dropdowns)
- Standard exits: 150-200ms (modals, toasts)
- Graceful exits: 200-300ms (page transitions)

**Exaggeration**: Scale to 0.9 for dramatic departure, 0.97 for subtle dismissal.

**Solid Drawing**: Maintain spatial logic. Elements should exit the way they came or toward where they "belong."

**Appeal**: Exits confirm user intent. Make dismissals feel decisive, not abrupt.

## Timing Recommendations

| Element Type | Duration | Easing | Notes |
|-------------|----------|--------|-------|
| Tooltip | 100ms | ease-in | Faster than entrance |
| Dropdown | 150ms | ease-in | Collapse upward |
| Toast | 150ms | ease-in | Slide to origin |
| Modal | 200ms | ease-in | Content first, overlay last |
| Deleted Item | 200ms | ease-in | Collapse height after fade |
| Page | 250ms | ease-in | Current page exits, then new enters |

## Implementation Pattern

```css
.exiting {
  animation: exit 200ms cubic-bezier(0.4, 0, 1, 1) forwards;
}

@keyframes exit {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(-10px) scale(0.98);
  }
}
```

## Collapse Pattern

For removed list items:
1. Fade out content (150ms)
2. Collapse height (150ms, starts at 100ms)
3. Remove from DOM after animation completes

Total perceived time: 250ms. Always use `will-change: opacity, transform` for smooth exits.
