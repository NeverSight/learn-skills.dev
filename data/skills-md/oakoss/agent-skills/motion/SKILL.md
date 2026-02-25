---
name: motion
description: |
  Web animations with Motion (formerly Framer Motion) for React -- gestures, scroll effects, spring physics, layout animations, SVG, micro-interactions, loading states.

  Use when: drag-and-drop, scroll animations, modals, carousels, parallax, page transitions, hover effects, staggered lists, loading spinners, number counters.
  Troubleshoot: AnimatePresence exit, list performance, Tailwind conflicts, Next.js "use client", layout in scaled containers.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://motion.dev/docs'
user-invocable: false
---

# Motion

## Overview

Motion (package: `motion`, formerly `framer-motion`) is the standard React animation library. Import from `motion/react`. Provides declarative props for gestures, scroll-linked animations, layout transitions, SVG path drawing, and spring physics. Uses a hybrid animation engine (WAAPI for transforms/opacity, ScrollTimeline for scroll-linked effects). Bundle ranges from 2.3 KB (useAnimate mini) to 34 KB (full), optimizable to 4.6 KB with LazyMotion. Compatible with React 18.2+, React 19, Next.js App Router, and Vite.

Do NOT use Motion for simple list add/remove animations (use AutoAnimate instead at 3.28 KB). Do NOT use for 3D (use Three.js / React Three Fiber).

## Quick Reference

| Pattern                | API / Props                                             |
| ---------------------- | ------------------------------------------------------- |
| Fade in on mount       | `initial`, `animate`, `transition`                      |
| Exit animations        | `AnimatePresence` + `exit` prop (unique `key` required) |
| Staggered list         | `variants` with `staggerChildren`                       |
| Hover / tap / focus    | `whileHover`, `whileTap`, `whileFocus`                  |
| Drag                   | `drag`, `dragConstraints`, `dragElastic`                |
| Scroll-triggered       | `whileInView`, `viewport={{ once: true }}`              |
| Scroll-linked/parallax | `useScroll` + `useTransform`                            |
| Progress indicator     | `scrollYProgress` + `scaleX`                            |
| Layout animation       | `layout` prop (FLIP technique)                          |
| Shared element         | `layoutId` (same ID across views)                       |
| Layout group           | `LayoutGroup` wrapping sibling lists                    |
| Page transition        | `AnimatePresence` + `key={pathname}`                    |
| SVG path drawing       | `pathLength` on `motion.path`                           |
| Animated counter       | `useSpring` + `useTransform`                            |
| Imperative control     | `useAnimate` hook returns `[scope, animate]`            |
| Custom components      | `motion.create(Component)` wraps any component          |
| Bundle optimization    | `LazyMotion` + `domAnimation` + `m` component (4.6 KB)  |
| Reduced motion         | `MotionConfig reducedMotion="user"`                     |

## Common Mistakes

| Mistake                                                   | Correct Pattern                                                   |
| --------------------------------------------------------- | ----------------------------------------------------------------- |
| AnimatePresence inside a conditional                      | Keep AnimatePresence mounted; place conditional content inside it |
| Missing unique `key` on AnimatePresence children          | Add unique `key` to each direct child for exit animations         |
| Tailwind `transition-*` classes with Motion animate props | Remove Tailwind transition classes to avoid stuttering            |
| Importing from `framer-motion`                            | Use `import { motion } from "motion/react"` (renamed late 2024)   |
| Animating 50+ items without virtualization                | Use react-window or @tanstack/react-virtual for large lists       |
| Full 34 KB bundle for simple animations                   | Use LazyMotion + domAnimation (4.6 KB) or useAnimate (2.3 KB)     |
| Missing `"use client"` in Next.js App Router              | Add directive or use `motion/react-client` import                 |
| Animating `width`/`height` directly                       | Use `layout` prop or `transform: scale` for GPU acceleration      |
| No `prefers-reduced-motion` handling                      | Wrap app in `MotionConfig reducedMotion="user"`                   |

## Delegation

- **Audit animation performance and bundle size**: Use `Explore` agent to find heavy imports, missing LazyMotion, and reflow-triggering properties
- **Build complex multi-step animations**: Use `Task` agent for scroll-linked parallax, shared layout transitions, and staggered sequences
- **Plan animation architecture for a new project**: Use `Plan` agent to evaluate Motion vs AutoAnimate vs CSS-only based on requirements

> If the `design-system` skill is available, delegate animation token definitions and motion design guidelines to it.

## References

- [Core Patterns](references/core-patterns.md) -- Animation patterns: fade, exit, stagger, gestures, modal, accordion, tabs, scroll, layout, drag, SVG, loading
- [Scroll Animations](references/scroll-animations.md) -- useScroll, useTransform, scroll-triggered, parallax, progress indicators, offset configuration
- [Performance](references/performance.md) -- LazyMotion, useAnimate, hardware acceleration, virtualization, production checklist
- [Next.js Integration](references/nextjs-integration.md) -- App Router patterns, motion/react-client, Pages Router, known issues
- [Accessibility & CSS](references/accessibility-css.md) -- prefers-reduced-motion, MotionConfig, useReducedMotion, CSS keyframes, Tailwind animations
- [Library Selection Guide](references/library-selection.md) -- Motion vs AutoAnimate decision guide with feature comparison and use-case recommendations
- [Troubleshooting](references/troubleshooting.md) -- AnimatePresence bugs, Tailwind conflicts, layout glitches, React 19 issues, naming migration
