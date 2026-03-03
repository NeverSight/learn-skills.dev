---
name: attention-grabbers
description: Use when drawing user focus - notification badges, new feature highlights, error callouts, promotional banners, or any animation meant to attract attention.
---

# Attention-Grabbing Animations

Apply Disney's 12 principles to focus-drawing motion.

## Principle Application

**Squash & Stretch**: Pulsing scale draws attention. 1.0 → 1.1 → 1.0 cycle catches peripheral vision.

**Anticipation**: Brief pause before attention animation. Let it build then release.

**Staging**: Position attention elements where users will see them. Corner badges, inline highlights.

**Straight Ahead vs Pose-to-Pose**: Design attention states: rest, active/pulsing, acknowledged.

**Follow Through & Overlapping**: Badge pulses, then count updates. Stagger the attention signals.

**Slow In/Slow Out**: Ease in/out on pulses. Smooth oscillation is less jarring than sharp bounces.

**Arcs**: Shake animations follow arc patterns. Left-right with slight vertical oscillation.

**Secondary Action**: Pulse + glow + color shift for maximum attention (use sparingly).

**Timing**:
- Single attention grab: 300-500ms
- Repeating pulse: 2000-3000ms cycle
- Urgent pulse: 1000-1500ms cycle
- Decay: Stop after 3-5 cycles or 10 seconds

**Exaggeration**: This is where exaggeration shines. Scale to 1.2, bright colors, bold motion.

**Solid Drawing**: Attention elements must still feel part of the UI, not floating or detached.

**Appeal**: Attention should feel like helpful notification, not aggressive demand.

## Timing Recommendations

| Attention Type | Duration | Cycles | Decay |
|---------------|----------|--------|-------|
| Badge Pulse | 300ms | 2-3 | Stop after animation |
| Notification Dot | 2000ms | 3 | 6 seconds total |
| New Feature | 500ms | 2 | Stay subtle |
| Error Shake | 400ms | 1 | None |
| Urgent Alert | 1000ms | infinite | Until dismissed |
| Promotional | 3000ms | 2 | 6 seconds |

## Implementation Patterns

```css
/* Pulse attention */
.badge-pulse {
  animation: pulse 2000ms ease-in-out 3;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.15); }
}

/* Subtle glow */
.glow-attention {
  animation: glow 2000ms ease-in-out 3;
}

@keyframes glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
  50% { box-shadow: 0 0 0 8px rgba(59, 130, 246, 0.3); }
}

/* Error shake */
.shake {
  animation: shake 400ms ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-8px); }
  40%, 80% { transform: translateX(8px); }
}

/* Ring animation (notification) */
.ring {
  animation: ring 2500ms ease-in-out 2;
}

@keyframes ring {
  0%, 100% { transform: rotate(0); }
  10%, 30% { transform: rotate(10deg); }
  20%, 40% { transform: rotate(-10deg); }
  50%, 100% { transform: rotate(0); }
}
```

## Attention Budget

```javascript
// Auto-stop attention after timeout
const attention = element.animate([
  { transform: 'scale(1)' },
  { transform: 'scale(1.15)' },
  { transform: 'scale(1)' }
], {
  duration: 2000,
  iterations: 3
});

// Or with CSS
setTimeout(() => {
  element.classList.remove('attention');
}, 6000);
```

## Key Rules

1. Maximum 1 attention animation visible at a time
2. Auto-stop after 3-5 cycles (10 seconds max)
3. Provide way to permanently dismiss
4. Never use for non-essential content
5. `prefers-reduced-motion`: static indicator only, no animation
6. Urgent animations must have audio/haptic alternative for accessibility
