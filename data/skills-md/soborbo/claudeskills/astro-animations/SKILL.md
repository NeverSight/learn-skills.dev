---
name: astro-animations
description: Animation patterns for Astro sites. Scroll animations, micro-interactions, transitions, loading states. Performance-focused, accessibility-aware.
---

# Astro Animations Skill

## Purpose

Provides animation patterns that enhance UX without harming performance or accessibility. All animations must serve a functional purpose and respect user motion preferences.

## Core Rules

1. **Purpose over polish** — Every animation should serve UX
2. **Performance first** — Use CSS, avoid JS where possible
3. **Respect preferences** — Honor `prefers-reduced-motion`
4. **Subtle over flashy** — Enhance, don't distract
5. **Fast** — Animations under 300ms for interactions
6. **No layout shift** — Animations must not cause cumulative layout shift
7. **Progressive enhancement** — UI must work without animations
8. **Intersection Observer** — Use for scroll-based reveals
9. **View Transitions API** — Leverage for page transitions in Astro
10. **Loading feedback** — Always show loading states with skeletons or spinners

## Animation Timing

| Type | Duration | Easing |
|------|----------|--------|
| Micro-interaction | 100-200ms | ease-out |
| Reveal/Fade | 200-400ms | ease-out |
| Slide | 300-500ms | ease-in-out |
| Page transition | 200-300ms | ease-out |

## References

- [CSS Utilities](references/css-utilities.md) — Base animation classes and keyframes
- [Scroll Animations](references/scroll-animations.md) — Intersection Observer-based reveals
- [Micro-Interactions](references/micro-interactions.md) — Button hovers, form focus, success/error animations
- [Loading States](references/loading-states.md) — Skeleton loaders and shimmer effects
- [Page Transitions](references/page-transitions.md) — View Transitions API implementation
- [Stagger Animations](references/stagger-animations.md) — Sequential reveal patterns
- [Reduced Motion](references/reduced-motion.md) — Accessibility best practices

## Forbidden

- ❌ Animations without `prefers-reduced-motion` handling
- ❌ Animations over 500ms for UI feedback
- ❌ Animations that block interaction
- ❌ Gratuitous/decorative-only animations
- ❌ JS animations when CSS works
- ❌ Animations that cause layout shift
- ❌ Auto-playing animations without user control
- ❌ Animations that flash more than 3 times per second

## Definition of Done

- [ ] All animations respect reduced motion
- [ ] Interaction animations under 300ms
- [ ] Reveal animations under 500ms
- [ ] No layout shift from animations
- [ ] Loading states have skeleton/spinner
- [ ] Page transitions smooth
- [ ] Focus states animated
- [ ] All animations tested with `prefers-reduced-motion: reduce`
- [ ] Scroll animations use Intersection Observer
- [ ] No animation blocks user interaction
