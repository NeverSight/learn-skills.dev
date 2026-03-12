---
name: scroll-reveal-animation
description: Add smooth scroll-triggered fade-in and stagger animations using Framer Motion in React/Next.js. Use when the user wants scroll animations, fade-in effects, whileInView animations, staggered reveals, or entrance animations on sections, cards, or text. Triggers on "animate on scroll", "fade in on scroll", "smooth animations", "stagger children", or "scroll reveal".
---

# Smooth Scroll Animations

Reusable Framer Motion animation components for smooth scroll-triggered reveals in React/Next.js.

## Requirements

- `framer-motion` must be installed. React 18+, designed for Next.js App Router and React projects using TypeScript.

## Workflow

1. **Add the animations file** — Copy `assets/animations.tsx` into the project at `components/animations.tsx` (or `lib/animations.tsx`). Add `"use client"` to any file importing these components in Next.js App Router.
2. **Import and use** — Import `AnimatedSection`, `AnimatedChildren`, `AnimatedItem`, and/or `AnimatedText` and wrap UI elements following the patterns below.

## Usage Patterns

**Staggered card grid** — `AnimatedChildren` + `AnimatedItem` for cascading reveals:

```tsx
<AnimatedSection>
  <AnimatedChildren className="grid grid-cols-3 gap-6">
    {items.map((item) => (
      <AnimatedItem key={item.id}><Card {...item} /></AnimatedItem>
    ))}
  </AnimatedChildren>
</AnimatedSection>
```

**Section with heading + content** — heading reveals, then content staggers in:

```tsx
<AnimatedSection>
  <AnimatedChildren className="mb-12 text-center">
    <AnimatedText as="h2" className="text-4xl">Section Title</AnimatedText>
    <AnimatedText as="p" className="text-lg text-muted-foreground">
      Subtitle text here.
    </AnimatedText>
  </AnimatedChildren>
  <AnimatedChildren className="grid grid-cols-2 gap-8">
    <AnimatedItem>Content 1</AnimatedItem>
    <AnimatedItem>Content 2</AnimatedItem>
  </AnimatedChildren>
</AnimatedSection>
```

**List with staggered items** — use `as="ul"` on container and `as="li"` on items:

```tsx
<AnimatedChildren as="ul" className="space-y-4">
  <AnimatedItem as="li">First item</AnimatedItem>
  <AnimatedItem as="li">Second item</AnimatedItem>
</AnimatedChildren>
```

## Notes

- All animations trigger once and start slightly before the element enters the viewport.
- For detailed animation values, props, and customization options, see `references/REFERENCE.md`.
