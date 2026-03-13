---
name: framer-animations
description: Add Framer Motion micro-animations to page sections. Includes section reveals, staggered lists, hover effects, and performance optimization. Use after section-backgrounds for each page.
---

# Section Animations

Add subtle micro-animations to finalize the look and feel of each page.

## Prerequisites

- Framer Motion already installed (v12.23.25)
- MotionSection component exists at `components/ui/motion-section.tsx`

## Workflow

1. **Wrap Page Sections** - Add MotionSection to each section
2. **Add Staggered Lists** - Animate feature grids, pricing cards, process steps
3. **Add Hover Effects** - Cards, buttons, interactive elements
4. **Verify Performance** - Ensure smooth 60fps animations

## Animation Types

### 1. Section Reveals

Wrap each section with MotionSection for scroll-triggered fade-in:

```jsx
import { MotionSection } from "@/components/ui/motion-section";

// In page.tsx
<MotionSection delay={0}>
  <Hero />
</MotionSection>
<MotionSection delay={0.1}>
  <Logos />
</MotionSection>
<MotionSection delay={0.1}>
  <Features />
</MotionSection>
```

**Delay Pattern:** 0, 0.1, 0.1, 0.1... (first section immediate, rest staggered)

### 2. Staggered Lists

For grids and lists (features, pricing cards, process steps):

```jsx
import { motion } from "framer-motion";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.div
  variants={container}
  initial="hidden"
  whileInView="show"
  viewport={{ once: true }}
  className="grid grid-cols-3 gap-6"
>
  {features.map((feature) => (
    <motion.div key={feature.id} variants={item}>
      <FeatureCard {...feature} />
    </motion.div>
  ))}
</motion.div>
```

### 3. Hover Effects

For cards and interactive elements:

```jsx
// Card hover - lift and scale
<motion.div
  whileHover={{ scale: 1.02, y: -4 }}
  transition={{ type: "spring", stiffness: 300 }}
  className="p-6 rounded-lg border"
>
  {/* Card content */}
</motion.div>

// Button press feedback
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  className="btn"
>
  Click me
</motion.button>
```

### 4. Image Reveals

For hero images or featured media:

```jsx
// Clip-path wipe effect
<motion.div
  initial={{ clipPath: "inset(100% 100% 0% 0%)" }}
  whileInView={{ clipPath: "inset(0% 0% 0% 0%)" }}
  viewport={{ once: true }}
  transition={{ type: "spring", stiffness: 150, damping: 20 }}
>
  <img src={image} alt="" />
</motion.div>

// Zoom-in on scroll
<motion.div
  initial={{ scale: 1.1, opacity: 0 }}
  whileInView={{ scale: 1, opacity: 1 }}
  viewport={{ once: true }}
  transition={{ duration: 0.6 }}
>
  <img src={image} alt="" />
</motion.div>
```

## Performance Rules

See references/performance-tips.md for details.

1. **Animate only once:** `viewport={{ once: true }}`
2. **GPU-accelerated properties only:** `opacity`, `transform` (scale, translate, rotate)
3. **Avoid:** `width`, `height`, `top`, `left`, `margin`, `padding`
4. **Duration:** 0.3-0.6s (subtle, not distracting)
5. **Easing:** `easeOut` for entries, `spring` for interactions

## Where to Apply

| Section Type | Animation |
|--------------|-----------|
| Hero | MotionSection (immediate) |
| Logos | MotionSection + stagger |
| Features | MotionSection + stagger grid |
| Process | MotionSection + stagger steps |
| Pricing | MotionSection + stagger cards + hover |
| Testimonials | MotionSection + stagger |
| FAQ | MotionSection |
| CTA | MotionSection |

## Output

- All sections wrapped with MotionSection
- Grids and lists with stagger animations
- Cards with hover lift effect
- Buttons with tap feedback
- Smooth 60fps performance
