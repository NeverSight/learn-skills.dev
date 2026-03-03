---
name: transition-sequences
description: Use when orchestrating multi-step animations - page transitions, onboarding flows, wizard steps, complex reveals, or any choreographed animation sequence.
---

# Transition Sequence Animations

Apply Disney's 12 principles to choreographed multi-step motion.

## Principle Application

**Squash & Stretch**: Each element in sequence can compress/expand independently for organic feel.

**Anticipation**: Sequence starts with a setup phase. Brief pause or gather before motion begins.

**Staging**: Direct attention through the sequence. Most important element animates first or last.

**Straight Ahead vs Pose-to-Pose**: Plan keyframes for each step. Map the entire sequence before implementing.

**Follow Through & Overlapping**: Elements don't move in unison. Stagger starts by 50-100ms. Let motion cascade.

**Slow In/Slow Out**: Each step eases. The sequence overall should ease too - faster middle, slower ends.

**Arcs**: Transitions across space follow arcs. Page sliding left curves slightly, not linear slide.

**Secondary Action**: Primary transition + secondary details. Page slides while elements within fade/scale.

**Timing**:
- Step overlap: 30-50% of previous step's duration
- Total sequence: 300-800ms for UI, up to 1500ms for dramatic
- Gap between steps: 0-100ms (overlap preferred)

**Exaggeration**: Sequence itself is exaggeration. Individual steps stay subtle.

**Solid Drawing**: Maintain spatial consistency. If A goes left, B should come from left.

**Appeal**: Sequences tell a story. Beginning, middle, end - satisfying resolution.

## Timing Recommendations

| Sequence Type | Total Duration | Step Count | Step Overlap |
|--------------|----------------|------------|--------------|
| Tab Change | 300ms | 2 | 50% |
| Page Transition | 500-600ms | 2-3 | 30% |
| Modal Open | 400ms | 3 | 40% |
| Wizard Step | 400ms | 2 | 50% |
| Onboarding | 800-1200ms | 4-6 | 30% |
| Dramatic Reveal | 1000-1500ms | 5-8 | 40% |

## Implementation Patterns

```css
/* Staggered sequence */
.sequence-item {
  opacity: 0;
  transform: translateY(20px);
  animation: reveal 400ms ease-out forwards;
}

.sequence-item:nth-child(1) { animation-delay: 0ms; }
.sequence-item:nth-child(2) { animation-delay: 80ms; }
.sequence-item:nth-child(3) { animation-delay: 160ms; }
.sequence-item:nth-child(4) { animation-delay: 240ms; }

@keyframes reveal {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Page transition choreography */
.page-exit {
  animation: page-out 250ms ease-in forwards;
}

.page-enter {
  animation: page-in 300ms ease-out 200ms forwards;
}

@keyframes page-out {
  to { opacity: 0; transform: translateX(-30px); }
}

@keyframes page-in {
  from { opacity: 0; transform: translateX(30px); }
  to { opacity: 1; transform: translateX(0); }
}
```

## Sequence Orchestration Formula

```javascript
// Calculate stagger delays
const items = document.querySelectorAll('.sequence-item');
const totalDuration = 600; // ms
const overlap = 0.4; // 40% overlap

items.forEach((item, index) => {
  const stepDuration = totalDuration / items.length;
  const delay = index * stepDuration * (1 - overlap);
  item.style.animationDelay = `${delay}ms`;
});
```

## Key Rules

1. Overlap steps 30-50% - no gaps, no simultaneous starts
2. Total sequence under 800ms for functional UI
3. Test at 0.5x speed to verify choreography
4. Provide skip option for sequences over 500ms
5. `prefers-reduced-motion`: instant state change, no sequence
