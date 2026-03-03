---
name: loading-states
description: Use when indicating progress or waiting - spinners, progress bars, skeleton screens, shimmer effects, or any animation showing the system is working.
---

# Loading State Animations

Apply Disney's 12 principles to communicate system activity.

## Principle Application

**Squash & Stretch**: Progress indicators can pulse/breathe to show life. Slight scale oscillation (0.98-1.02).

**Anticipation**: Show loading state immediately on action. Don't wait for slow response to show spinner.

**Staging**: Loading indicators appear where content will be. Skeleton screens match final layout.

**Straight Ahead vs Pose-to-Pose**: Design loading as a sequence: instant indicator → progress → completion → content.

**Follow Through & Overlapping**: Loading fades as content enters. Overlap the transition by 100ms.

**Slow In/Slow Out**: Progress bars ease-in-out between known percentages. Indeterminate uses smooth oscillation.

**Arcs**: Circular spinners follow true circular paths. Avoid jerky rotation.

**Secondary Action**: Skeleton shimmer + subtle pulse. Multiple signals reinforce "loading."

**Timing**:
- Show spinner after 200ms delay (avoid flash for fast loads)
- Minimum display: 500ms (prevent jarring flash)
- Skeleton shimmer cycle: 1500-2000ms

**Exaggeration**: Keep minimal - loading shouldn't distract, just reassure.

**Solid Drawing**: Skeletons should match content proportions. Wrong shapes break the illusion.

**Appeal**: Loading should feel optimistic, not tedious. Smooth motion suggests progress.

## Timing Recommendations

| Loading Type | Appear Delay | Min Display | Animation Cycle |
|-------------|--------------|-------------|-----------------|
| Spinner | 200ms | 500ms | 700-800ms |
| Progress Bar | 0ms | - | smooth fill |
| Skeleton | 0ms | 500ms | 1500ms shimmer |
| Button Spinner | 0ms | 400ms | 600ms |
| Full Page | 100ms | 800ms | 1000ms |

## Implementation Patterns

```css
/* Skeleton shimmer */
.skeleton {
  background: linear-gradient(
    90deg,
    #e0e0e0 0%,
    #f0f0f0 50%,
    #e0e0e0 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1500ms ease-in-out infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Spinner with smooth rotation */
.spinner {
  animation: spin 700ms linear infinite;
  opacity: 0;
  animation: fade-in 200ms 200ms ease-out forwards, spin 700ms linear infinite;
}

/* Progress bar with easing */
.progress-fill {
  transition: width 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

## Loading-to-Content Transition

```css
.content-enter {
  animation: content-reveal 300ms ease-out forwards;
}

@keyframes content-reveal {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

## Key Rules

1. Delay spinner appearance by 200ms to avoid flash
2. Keep loading visible minimum 500ms once shown
3. Skeleton shapes must match real content dimensions
4. Transition smoothly from loading to content - never pop
5. Respect `prefers-reduced-motion` - show static indicator instead
