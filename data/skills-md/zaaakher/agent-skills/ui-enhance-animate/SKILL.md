---
name: ui-enhance-animate
description: >-
  Comprehensively upgrades and polishes an existing website's UI design —
  improving layout, typography, spacing, depth, visual hierarchy, and component
  refinement — while preserving the site's existing color palette. Also adds
  smooth, staggered blur+slide-up reveal animations using Framer Motion (or CSS
  if plain HTML) triggered when elements enter the viewport. Use this skill
  whenever the user wants to improve, modernize, polish, or animate an existing
  website or React/HTML page. Trigger even when the user only mentions "make it
  look better", "animate it", "improve the design", "upgrade the UI", "make it
  more modern", or "add scroll animations" — this skill handles all of those,
  not just animation.
metadata:
  tags: []
  category: general
  version: 1.0.0
  public: false
  created: '2026-02-24'
  updated: '2026-02-24'
---
# UI Enhancement + Staggered Animation Skill

This skill performs a **full design upgrade** of an existing website or component. It is NOT just about adding animations — it is a holistic visual refinement pass that touches typography, spacing, layout, depth, micro-interactions, and motion. The existing **color palette is preserved**; everything else can and should be improved.

---

## Phase 1 — Audit & Understand Before Touching Anything

Before writing a single line of code, do a thorough read of the existing code. Extract and note:

1. **Color palette** — all hex/hsl/rgb values, CSS variables, Tailwind color classes. These are **sacred and must be preserved exactly**.
2. **Font stack** — what fonts are currently in use.
3. **Layout structure** — is it CSS Grid, Flexbox, plain blocks? What's the overall page structure?
4. **Component inventory** — list every distinct section/component: hero, navbar, cards, features, testimonials, CTA, footer, etc.
5. **Current weaknesses** — visually identify what looks amateur or generic: flat cards, no spacing rhythm, weak typography hierarchy, no depth/shadow, boring hover states, no visual flow, walls of text, etc.
6. **Tech stack** — React (use Framer Motion), plain HTML/CSS (use CSS animations + IntersectionObserver), Vue, etc.

Only after this audit should you begin making changes.

---

## Phase 2 — Full Design Upgrade (Non-Animation)

Apply ALL of the following improvements that are relevant to the site. Be thorough — don't skip sections because they "look okay". Every part of the site should be elevated.

### Typography
- Introduce a **clear typographic hierarchy**: display sizes (clamp-based fluid sizing), section headings, subheadings, body, caption — each with distinct weight and size.
- Replace generic system fonts (Arial, Helvetica, system-ui) with a **distinctive pairing** from Google Fonts or similar. A strong display/heading font paired with a clean readable body font.
- Use `letter-spacing` for uppercase labels and overlines.
- Add `line-height` rhythm: ~1.2 for headings, ~1.6–1.7 for body text.
- Tighten long text blocks with `max-width: 65ch` for readability.

### Spacing & Rhythm
- Introduce a consistent spacing scale (e.g., 4/8/16/24/32/48/64/96px).
- Increase section padding — most amateur sites are too cramped.
- Add generous whitespace between section components.
- Ensure consistent internal card/component padding.

### Depth & Surfaces
- Add layered `box-shadow` to cards, modals, and elevated surfaces. Use multi-layer soft shadows, not harsh single-layer ones.
- Use subtle `border` with low-opacity color instead of hard outlines.
- Apply `backdrop-filter: blur()` to glass-morphism elements like navbars or overlapping cards where appropriate.
- Use subtle `background` differentiation between sections (slightly lighter/darker tint of existing colors).

### Layout & Composition
- Break out of purely uniform grid layouts. Use asymmetric or offset compositions where they add interest.
- Add visual **anchors**: decorative elements, large background text/numbers, gradient blobs, or geometric shapes using the existing color palette (low opacity).
- Ensure the hero is impactful with generous sizing and a strong focal point.
- Use CSS Grid for complex layouts; avoid excessive nested divs.

### Cards & Components
- Round all corners consistently (usually 8–16px for cards, 6–8px for buttons/inputs).
- Add hover states to all interactive elements: cards should lift (translateY + shadow), buttons should shift or glow.
- Ensure buttons have visible padding, strong contrast, and consider adding a subtle icon or arrow.
- Add `transition: all 0.2s ease` baseline to interactive elements.

### Visual Polish Details
- Add subtle gradient overlays to hero images or dark sections.
- Use `overflow: hidden` on cards to clip child images and effects cleanly.
- Ensure images use `object-fit: cover` and have defined aspect ratios.
- Add divider treatments between sections (subtle border, gradient fade, or decorative wave/angle).
- If there are icons, ensure they are consistently sized and optically aligned with text.

---

## Phase 3 — Staggered Blur + Slide-Up Reveal Animations

### Animation Philosophy
- Animations should feel **natural and elegant** — not flashy or distracting.
- **Every major content section** should animate in when it enters the viewport.
- Use a **staggered pattern**: child elements within a section animate in one by one with a delay offset (e.g., 0.1s apart).
- The animation: elements start `opacity: 0`, `filter: blur(8px)`, `translateY(24px)` and transition to `opacity: 1`, `filter: blur(0px)`, `translateY(0)`.
- Duration: **0.6s** for most elements. Easing: `ease-out` or a custom cubic-bezier like `cubic-bezier(0.16, 1, 0.3, 1)` (snappy spring).
- Respect `prefers-reduced-motion` — disable animations for users who opt out.

---

### React — Framer Motion Implementation

Install if not present:
```bash
npm install framer-motion
```

#### Core Animation Variants

```tsx
// lib/animations.ts
import { Variants } from "framer-motion";

export const fadeUpBlur: Variants = {
  hidden: {
    opacity: 0,
    y: 24,
    filter: "blur(8px)",
  },
  visible: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: {
      duration: 0.6,
      ease: [0.16, 1, 0.3, 1],
    },
  },
};

export const staggerContainer: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.05,
    },
  },
};

// For heavier stagger (e.g., feature grids)
export const staggerContainerSlow: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.15,
      delayChildren: 0.1,
    },
  },
};
```

#### Reusable AnimateInView Wrapper

```tsx
// components/AnimateInView.tsx
import { motion, useInView } from "framer-motion";
import { useRef } from "react";
import { staggerContainer, fadeUpBlur } from "@/lib/animations";

interface AnimateInViewProps {
  children: React.ReactNode;
  className?: string;
  delay?: number;
  stagger?: boolean;
}

export function AnimateInView({
  children,
  className,
  delay = 0,
  stagger = false,
}: AnimateInViewProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });

  if (stagger) {
    return (
      <motion.div
        ref={ref}
        className={className}
        variants={staggerContainer}
        initial="hidden"
        animate={isInView ? "visible" : "hidden"}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <motion.div
      ref={ref}
      className={className}
      variants={fadeUpBlur}
      initial="hidden"
      animate={isInView ? "visible" : "hidden"}
      transition={{ delay }}
    >
      {children}
    </motion.div>
  );
}

// Individual animated child (use inside AnimateInView with stagger=true)
export function AnimatedItem({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <motion.div className={className} variants={fadeUpBlur}>
      {children}
    </motion.div>
  );
}
```

#### Usage Pattern

```tsx
// Hero section — single block fade
<AnimateInView>
  <h1>Your Headline</h1>
  <p>Subheadline text here</p>
  <Button>CTA</Button>
</AnimateInView>

// Feature grid — staggered children
<AnimateInView stagger className="grid grid-cols-3 gap-6">
  {features.map((f) => (
    <AnimatedItem key={f.id}>
      <FeatureCard {...f} />
    </AnimatedItem>
  ))}
</AnimateInView>

// Section heading + body — slight delays
<div>
  <AnimateInView delay={0}>
    <h2>Section Title</h2>
  </AnimateInView>
  <AnimateInView delay={0.1}>
    <p>Section description</p>
  </AnimateInView>
</div>
```

#### Reduced Motion

```tsx
// Wrap your app or layout:
import { LazyMotion, domAnimation, MotionConfig } from "framer-motion";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <MotionConfig reducedMotion="user">
      <LazyMotion features={domAnimation}>
        {children}
      </LazyMotion>
    </MotionConfig>
  );
}
```

---

### Plain HTML/CSS/JS — CSS + IntersectionObserver Implementation

#### CSS Animation Classes

```css
/* Add to your global stylesheet */

@media (prefers-reduced-motion: no-preference) {
  .reveal {
    opacity: 0;
    transform: translateY(24px);
    filter: blur(8px);
    transition:
      opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
      transform 0.6s cubic-bezier(0.16, 1, 0.3, 1),
      filter 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .reveal.in-view {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0px);
  }

  /* Stagger delays for children */
  .stagger-children .reveal:nth-child(1) { transition-delay: 0.0s; }
  .stagger-children .reveal:nth-child(2) { transition-delay: 0.1s; }
  .stagger-children .reveal:nth-child(3) { transition-delay: 0.2s; }
  .stagger-children .reveal:nth-child(4) { transition-delay: 0.3s; }
  .stagger-children .reveal:nth-child(5) { transition-delay: 0.4s; }
  .stagger-children .reveal:nth-child(6) { transition-delay: 0.5s; }
  /* Add more as needed */
}
```

#### IntersectionObserver Script

```js
// Add before closing </body>
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in-view");
        observer.unobserve(entry.target); // animate once
      }
    });
  },
  { rootMargin: "-80px 0px", threshold: 0.1 }
);

document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));
```

#### Usage Pattern

```html
<!-- Single block -->
<section>
  <div class="reveal">
    <h2>Section Title</h2>
    <p>Description text</p>
  </div>
</section>

<!-- Staggered grid -->
<div class="stagger-children grid">
  <div class="reveal card">Feature 1</div>
  <div class="reveal card">Feature 2</div>
  <div class="reveal card">Feature 3</div>
</div>
```

---

## Phase 4 — Section-by-Section Application Guide

Apply improvements and animations to each section type as follows:

| Section | Design Upgrades | Animation Pattern |
|---|---|---|
| **Navbar** | Glassmorphism `backdrop-blur`, subtle border-bottom, refined logo spacing | Fade in on load (no scroll trigger) |
| **Hero** | Large fluid type, strong hierarchy, gradient or decorative blob, CTA button polish | Single block stagger: headline → subtext → CTA button (0.1s each) |
| **Features/Grid** | Card depth (shadow + hover lift), icon refinement, consistent spacing | Stagger grid items with 0.1–0.15s offset |
| **Testimonials** | Quote styling, avatar polish, card surface differentiation | Stagger cards left-to-right |
| **Stats/Numbers** | Oversized numbers with accent color, label typography, divider lines | Each stat fades in with offset |
| **CTA Section** | Strong background treatment, button refinement, generous padding | Single block reveal |
| **Footer** | Column spacing, link hover states, subtle dividers | Single reveal |

---

## Phase 5 — Quality Checklist

Before delivering the result, verify:

- [ ] All original colors are preserved (no new palette colors introduced)
- [ ] Every section has at least one `.reveal` / `AnimateInView` wrapper
- [ ] Stagger is applied to all grid/list/card groups of 2+ items
- [ ] `prefers-reduced-motion` is respected
- [ ] Hover states exist on all interactive elements
- [ ] Typography has clear hierarchy (not all same size/weight)
- [ ] Cards/surfaces have depth (shadow, border, or background distinction)
- [ ] Spacing feels generous and rhythmic — not cramped
- [ ] No generic placeholder improvements — every change is intentional and visible
- [ ] The site feels noticeably more polished than before

---

## Notes & Edge Cases

- **If the site uses Tailwind**: Use `motion.div` from Framer Motion with Tailwind classes. Add arbitrary values for blur: `[filter:blur(8px)]` or inline styles for the animation initial state.
- **If colors are defined as Tailwind config values**: Reference them in the animation components but don't change them.
- **If there are images**: Ensure they have defined height/aspect-ratio + `object-fit: cover`. Consider adding subtle scale-on-hover.
- **For dark sites**: Glassmorphism works especially well. Use `bg-white/5` or similar low-opacity whites for card surfaces.
- **For light sites**: Use soft, layered shadows (`shadow-sm` + `shadow-md` combo). Use slight background tints to distinguish sections.
- **Performance**: `blur()` filter animations can be GPU-intensive on low-end devices. If performance is a concern, drop the blur and use only `opacity` + `translateY`.
