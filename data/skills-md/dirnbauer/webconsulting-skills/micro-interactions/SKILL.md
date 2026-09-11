---
name: "micro-interactions"
description: "Use when designing small UI feedback moments like button states, toggles, form validation, loading indicators, or notification badges."
---

# Micro-interaction Animation

Apply Disney's 12 animation principles to small UI feedback moments and interface details.

## Quick Reference

| Principle | Micro-interaction Implementation |
|-----------|--------------------------------|
| Squash & Stretch | Button press compression, toggle bounce |
| Anticipation | Hover state hints, pre-click feedback |
| Staging | Focus attention on active element |
| Straight Ahead / Pose to Pose | Progress vs state changes |
| Follow Through / Overlapping | Ripple effects, settling motion |
| Slow In / Slow Out | Snappy but smooth transitions |
| Arc | Toggle switches, circular menus |
| Secondary Action | Icons respond to parent state |
| Timing | 100-300ms for most interactions |
| Exaggeration | Clear but not distracting |
| Solid Drawing | Consistent transform behavior |
| Appeal | Delightful, purposeful feedback |

## Principle Applications

**Squash & Stretch**: Buttons compress slightly on press (scaleY: 0.95). Toggle thumbs squash when hitting bounds. Notification badges bounce on update. Keep subtle—this is UI, not cartoon.

**Anticipation**: Hover states prepare for click. Buttons lift/grow slightly before press animation. Draggable items elevate on grab start. Loading spinners wind up before spinning.

**Staging**: Active form field clearly distinguished. Error states demand attention. Success confirmations are unmistakable. One interaction feedback at a time.

**Straight Ahead vs Pose to Pose**: Progress indicators animate continuously (straight ahead). Checkboxes snap between states (pose to pose). Combine: loading indicator ends with state-change snap.

**Follow Through & Overlapping**: Ripple effects expand past tap point. Toggle switches overshoot then settle. Checkmarks draw with slight delay after box fills. Menu items stagger in.

**Slow In / Slow Out**: Quick ease-out for responsive feel. 100ms with ease-out feels instant. Avoid linear—looks broken. Snappy entrance, gentle settling.

**Arc**: Toggle switches travel in slight arc. Circular action buttons expand radially. Dropdown carets rotate smoothly. Menu items can follow curved path.

**Secondary Action**: Icon changes color as button state changes. Badge count updates with parent notification. Helper text appears as input focuses. Shadow responds to elevation.

**Timing**: Immediate feedback: 50-100ms. Standard transitions: 100-200ms. Complex micro-interactions: 200-300ms. Anything longer feels sluggish for small UI.

**Exaggeration**: Enough to notice, not enough to distract. Error shakes: 3-5px, not 20px. Success scales: 1.05-1.1, not 1.5. Subtle but unmistakable.

**Solid Drawing**: Transform origin matters—buttons scale from center, tooltips from pointer. Consistent behavior across similar elements. Maintain visual integrity during animation.

**Appeal**: Micro-interactions add personality without overwhelming. Users should feel the interface is responsive and alive. Small delights build into overall experience quality.

## Component Patterns

### Button States
```css
.button {
    transition: transform 100ms ease-out,
                box-shadow 100ms ease-out;
}
.button:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.button:active {
    transform: translateY(0) scale(0.98);
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
```

### Toggle Switch
```css
.toggle-thumb {
    transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toggle-thumb.active {
    transform: translateX(20px);
}
```

### Checkbox
```css
.checkmark {
    stroke-dasharray: 20;
    stroke-dashoffset: 20;
    transition: stroke-dashoffset 200ms ease-out 50ms;
}
.checkbox:checked + .checkmark {
    stroke-dashoffset: 0;
}
```

## Timing Reference

| Interaction | Duration | Easing |
|-------------|----------|--------|
| Hover | 100ms | ease-out |
| Click/tap | 100ms | ease-out |
| Toggle | 150-200ms | spring/elastic |
| Checkbox | 150ms | ease-out |
| Focus ring | 100ms | ease-out |
| Tooltip show | 150ms | ease-out |
| Tooltip hide | 100ms | ease-in |
| Badge update | 200ms | elastic |
| Form error | 200ms | ease-out |

## Best Practices

1. Every interactive element needs feedback
2. Disabled states: no animation, reduced opacity
3. Group related feedback together
4. Don't animate on every change—filter unnecessary updates
5. Test without animation—functionality shouldn't depend on it
6. Respect `prefers-reduced-motion`

---

## Credits & Attribution

This skill is based on the excellent work by
**[Dylan Tarre](https://github.com/dylantarre)**.

Original repository: https://github.com/dylantarre/animation-principles

**Copyright (c) 2024 Dylan Tarre** - Disney's 12 Animation Principles applied to UI micro-interactions (MIT License)

Special thanks to [Dylan Tarre](https://github.com/dylantarre) for their generous open-source contributions, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
