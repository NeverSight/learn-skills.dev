---
name: motion-animation
description: Motion design principles, when to animate, transitions, and accessibility. Use when adding animations, micro-interactions, or ensuring accessibility for motion.
version: 1.0.0
---

# Motion & Animation

This skill covers motion design for user interfaces — when and why to animate, transitions, micro-interactions, and respecting user preferences for reduced motion.

## Use-When

This skill activates when:
- Agent adds animations or transitions to components
- Agent designs micro-interactions (button hover, loading states)
- Agent builds interactive elements with state changes
- Agent needs to respect prefers-reduced-motion
- Agent creates page transitions

## Core Rules

- ALWAYS use motion to communicate state changes, not for decoration
- ALWAYS respect prefers-reduced-motion for accessibility
- ALWAYS keep animations short (150-300ms for UI, 300-500ms for page)
- NEVER animate properties that cause layout shifts (width, height)
- PREFER CSS transitions over JavaScript animations when possible

## Common Agent Mistakes

- Animating everything (causes distraction and performance issues)
- Not respecting prefers-reduced-motion
- Animating layout-triggering properties (width, height, top, left)
- Using JavaScript animations where CSS would suffice
- Animations that are too slow or too fast

## Examples

### ✅ Correct

```tsx
// Short, purposeful transitions
<button className="transition-colors duration-200 hover:bg-primary/90">
  Submit
</button>

// Respect reduced motion
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}

// Smooth opacity/transform animations
<div className="transition-opacity duration-300 opacity-0 data-[show]:opacity-100" />
```

### ❌ Wrong

```tsx
// Animating layout properties
<div className="transition-all" style={{ width: expanded ? '100%' : '50%' }} />

// No reduced motion support
<button className="animate-pulse">Loading</button>

// Too slow
<button className="transition-all duration-1000">Submit</button>
```

## References

- [MDN - CSS Transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Transitions/Using_CSS_transitions)
- [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [Material Design Motion](https://m3.material.io/styles/motion)
