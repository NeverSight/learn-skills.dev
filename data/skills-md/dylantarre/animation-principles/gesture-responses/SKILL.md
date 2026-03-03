---
name: gesture-responses
description: Use when responding to touch or click interactions - button presses, drag feedback, swipe responses, tap ripples, or any direct manipulation animation.
---

# Gesture Response Animations

Apply Disney's 12 principles to direct user interactions.

## Principle Application

**Squash & Stretch**: Elements compress on press (scale 0.95-0.97), spring back on release.

**Anticipation**: The press IS the anticipation. Response should be immediate - no delay.

**Staging**: Response originates from interaction point. Ripples expand from tap location.

**Straight Ahead vs Pose-to-Pose**: Define rest, pressed, and released poses. Transitions flow between them.

**Follow Through & Overlapping**: Release animation overshoots rest position. Scale to 1.02, settle to 1.0.

**Slow In/Slow Out**: Press: instant. Release: ease-out with overshoot `cubic-bezier(0.34, 1.56, 0.64, 1)`.

**Arcs**: Drag elements follow finger with slight lag on curves. Snapping follows arc to destination.

**Secondary Action**: Press triggers ripple + scale + shadow change simultaneously.

**Timing**:
- Press response: 0-50ms (must feel instant)
- Release recovery: 150-300ms (can be playful)
- Ripple expansion: 400-600ms (decorative, can be slower)

**Exaggeration**: Subtle for press (0.97), playful for release (overshoot 1.03).

**Solid Drawing**: Pressed state should feel "pushed in" - smaller scale, reduced shadow, shifted color.

**Appeal**: Gestures should feel physically satisfying. Like pressing a real button.

## Timing Recommendations

| Gesture | Press Duration | Release Duration | Easing |
|---------|---------------|------------------|--------|
| Tap/Click | 50ms | 200ms | ease-out + overshoot |
| Long Press | 50ms | 300ms | ease-out |
| Drag Start | 100ms | - | ease-out |
| Drag Release | - | 300ms | spring |
| Swipe | - | 200-400ms | ease-out |
| Pinch | real-time | 300ms | spring |

## Implementation Patterns

```css
/* Button press */
.button {
  transition: transform 50ms ease-out;
}

.button:active {
  transform: scale(0.97);
}

/* Release with overshoot */
.button:not(:active) {
  transition: transform 250ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Material ripple */
.ripple {
  animation: ripple 600ms ease-out forwards;
}

@keyframes ripple {
  from {
    transform: scale(0);
    opacity: 0.5;
  }
  to {
    transform: scale(4);
    opacity: 0;
  }
}
```

## Drag Feedback Pattern

```javascript
// Smooth drag with slight lag
element.style.transform = `translate(${x}px, ${y}px)`;
element.style.transition = 'transform 50ms ease-out';

// Snap back with spring
element.style.transition = 'transform 300ms cubic-bezier(0.34, 1.56, 0.64, 1)';
element.style.transform = 'translate(0, 0)';
```

## Critical Rule

Gesture responses must be under 100ms to feel connected to the action. Anything slower breaks the direct manipulation illusion. Test on actual touch devices.
