---
name: scroll-animations
description: Use when triggering animations on scroll - reveal effects, parallax, sticky headers, progress indicators, or any scroll-linked motion.
---

# Scroll Animations

Apply Disney's 12 principles to scroll-triggered motion.

## Principle Application

**Squash & Stretch**: Elements can compress slightly while scrolling fast, settle when stopped.

**Anticipation**: Content should be slightly visible before full reveal. Start animations at 10-20% visibility.

**Staging**: Reveal content in reading order. Top-to-bottom, left-to-right progression.

**Straight Ahead vs Pose-to-Pose**: Define clear "hidden" and "revealed" poses. Scroll position interpolates between them.

**Follow Through & Overlapping**: Stagger reveals. First element triggers at 20% viewport, next at 25%, etc.

**Slow In/Slow Out**: Use ease-out for reveals triggered by scroll. Content settles into place.

**Arcs**: Parallax elements move on curves relative to scroll. Slight horizontal offset as vertical scroll occurs.

**Secondary Action**: Fade + slide + scale can combine for richer reveals.

**Timing**:
- Reveal animation: 400-600ms (allows scroll to continue)
- Parallax: real-time, 1:1 or fractional ratios
- Sticky transitions: 200-300ms

**Exaggeration**: Subtle for scroll - users control the pace. Let scroll speed be the exaggeration.

**Solid Drawing**: Elements should never jump or teleport. Smooth interpolation at all scroll positions.

**Appeal**: Scroll animations should reward exploration, not obstruct it.

## Timing Recommendations

| Scroll Animation | Duration | Trigger Point | Easing |
|-----------------|----------|---------------|--------|
| Fade In | 500ms | 20% visible | ease-out |
| Slide Up | 600ms | 15% visible | ease-out |
| Parallax | real-time | continuous | linear |
| Sticky Header | 200ms | threshold | ease-out |
| Progress Bar | real-time | continuous | linear |
| Section Reveal | 600ms | 25% visible | ease-out |

## Implementation Patterns

```css
/* Scroll-triggered reveal */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 500ms ease-out, transform 600ms ease-out;
}

.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* CSS-only parallax */
.parallax-container {
  perspective: 1px;
  overflow-y: auto;
}

.parallax-slow {
  transform: translateZ(-1px) scale(2);
}
```

## Intersection Observer Pattern

```javascript
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  },
  { threshold: 0.2, rootMargin: '0px 0px -10% 0px' }
);

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

## Scroll-Linked Animation (CSS)

```css
@keyframes reveal {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.scroll-reveal {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 50%;
}
```

## Key Rules

1. Never block scroll or hijack scroll behavior
2. Animations should complete within viewport, not require precise scroll position
3. Trigger early (10-20% visible) so animation completes before full view
4. Provide `prefers-reduced-motion` alternative - instant reveals, no parallax
5. Test on mobile - scroll animations must be smooth at 60fps
