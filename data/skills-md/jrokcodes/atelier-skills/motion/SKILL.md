---
name: motion
description: Add professional animations and motion effects using Framer Motion and GSAP. Use when building hero sections, scroll animations, hover effects, page transitions, or any interactive motion in React projects.
allowed-tools: Read, Write, Bash
---

# Motion Effects

Add purposeful, professional animations that enhance UX without being distracting. Default to Framer Motion for React component animations; use GSAP for complex timelines and text splitting.

For extended code snippets and ready-to-paste recipes, see:
- `Atelier/snippets/framer-motion-recipes.md`
- `Atelier/snippets/gsap-recipes.md`

## Installation

```bash
# Framer Motion (default for React projects)
npm install framer-motion

# GSAP (for complex timelines, text splitting, SVG morphing)
npm install gsap
```

## Framer Motion Quick Start

### Basic Fade-In
```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: "easeOut" }}
>
  Content
</motion.div>
```

### Scroll-Triggered
```jsx
<motion.div
  initial={{ opacity: 0 }}
  whileInView={{ opacity: 1 }}
  viewport={{ once: true, amount: 0.3 }}
>
  Appears on scroll
</motion.div>
```

### Hover Effects
```jsx
<motion.button
  whileHover={{ scale: 1.02, boxShadow: "0 10px 30px rgba(0,0,0,0.1)" }}
  whileTap={{ scale: 0.98 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
>
  Button
</motion.button>
```

## Animation Patterns

### Hero Section
- Staggered text reveal (parent + children with `staggerChildren`)
- Parallax background (`useScroll` + `useTransform`)
- Gradient blob animations (CSS `@keyframes` or Framer `animate`)

### Navigation
- Smooth underline on hover (`layoutId` for shared layout)
- Mobile menu slide (`AnimatePresence` + slide variant)

### Cards
- Hover lift with shadow (`whileHover` scale + boxShadow)
- 3D tilt effect (`useMotionValue` + `useTransform` on mouse position)
- Image zoom on hover (overflow hidden + scale)

### Page Transitions
- Fade between pages (`AnimatePresence` wrapping router outlet)
- Slide transitions (x-axis variants)
- Shared element animations (`layoutId`)

## When to Use GSAP vs Framer Motion

| Use Framer Motion | Use GSAP |
|-------------------|----------|
| React component animations | Complex multi-step timelines |
| Gestures (drag, hover, tap) | Text splitting effects (SplitText) |
| Layout animations | Scroll-triggered sequences (ScrollTrigger) |
| Simple transitions | SVG morphing |
| AnimatePresence (mount/unmount) | Pin sections during scroll |

## Best Practices

1. **Performance** -- Only animate `transform` and `opacity` (GPU-accelerated properties)
2. **Timing** -- 0.2-0.5s for micro-interactions, 0.5-1s for larger animations
3. **Easing** -- Use custom cubic-bezier or spring physics, never linear
4. **Purpose** -- Every animation must serve a purpose: guide attention, confirm action, or delight
5. **Reduced motion** -- Respect `prefers-reduced-motion` media query
