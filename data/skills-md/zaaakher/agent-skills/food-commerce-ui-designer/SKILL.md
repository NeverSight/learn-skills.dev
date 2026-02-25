---
name: food-commerce-ui-designer
description: >-
  Create distinctive, production-grade frontend interfaces with high design
  quality for an ecommerce brand selling sauces and bone broth. Use this skill
  when building any web components, pages, product listings, landing sections,
  or UI elements for the store. Generates warm, inviting, food-forward designs
  with smooth Motion-powered animations and colorful, friendly aesthetics.
  Always use this skill for any UI, page, component, or layout work — even if
  the user just says "make a card" or "build a section" or "add animations".
license: Complete terms in LICENSE.txt
metadata:
  tags:
    - ecommerce
    - food
    - animated
    - ui
    - frontend
  category: general
  version: 2.0.0
  public: false
  created: '2026-02-24'
  updated: '2026-02-24'
---
This skill guides creation of warm, inviting, production-grade frontend interfaces for a sauce and bone broth ecommerce brand. Every design should feel like it came from a beloved artisan food brand — not a generic SaaS tool. Implement real working React code with rich Motion animations, food-forward color palettes, and friendly, approachable aesthetics.

The user provides frontend requirements: a component, page, product card, hero section, checkout flow, or any other UI element. They may include context about specific products, promotions, or page purpose.

## Brand Aesthetic Direction

This is a **warm artisan food brand** selling sauces and bone broth. The aesthetic lives at the intersection of:
- **Farmers market warmth** — earthy, handcrafted, honest
- **Modern food editorial** — clean, appetite-forward, beautiful food photography framing
- **Friendly & approachable** — inviting copy-forward layouts, never cold or clinical

### Color Language
Always work within this warm, food-forward palette (use CSS variables):

```css
--cream: #FBF5E6;         /* warm off-white base */
--amber: #D4843A;         /* rich sauce amber — primary accent */
--burnt-sienna: #C0522A;  /* deep hot sauce red */
--golden: #F2B84B;        /* golden broth warmth */
--forest: #3D5A3E;        /* herb green — secondary accent */
--chocolate: #3B1F0E;     /* deep rich brown — text/dark bg */
--blush: #F5D5B8;         /* soft peach — light accents */
--bone: #EDE0C8;          /* bone broth neutral */
```

Combine these with purpose: cream backgrounds, amber CTAs, forest for fresh/herb notes, chocolate for richness and depth. Avoid cold blues, grays, or anything that reads as tech/SaaS.

### Typography
Always use Google Fonts. Pair a warm display font with a readable body:
- **Display**: Playfair Display, Cormorant Garamond, Lora, or Fraunces — serif warmth for headlines
- **Body**: DM Sans, Nunito, or Instrument Sans — friendly, rounded, readable
- **Accent**: A handwritten font (Caveat, Pacifico, Dancing Script) for taglines, labels, badge text

Never use Inter, Roboto, Arial, or geometric sans-serifs as the primary font. They read as cold and tech-forward.

### Spatial Composition
- Generous padding — food brands breathe
- Warm card designs with subtle rounded corners (12–20px)
- Layered depth: subtle drop shadows, cream cards on warm backgrounds
- Organic shapes: blob SVGs, wavy section dividers, slightly uneven grids
- Product-forward: images large, prominent, appetite-inducing

## Motion & Animation (React/Motion)

**Always use the Motion library** (`motion/react`) for React components. Animations should feel warm, smooth, and appetite-whetting — never jarring or mechanical.

### Import Pattern
```jsx
import { motion, AnimatePresence, useInView, useScroll, useTransform } from "motion/react"
```

### Core Animation Patterns

**Page / Section Entry** — staggered reveals as content scrolls into view:
```jsx
const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } }
}
const itemVariants = {
  hidden: { opacity: 0, y: 28 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] } }
}
// Use with useInView for scroll-triggered reveals
const ref = useRef(null)
const isInView = useInView(ref, { once: true, margin: "-80px" })
```

**Product Cards** — lift and warm glow on hover:
```jsx
<motion.div
  whileHover={{ y: -6, boxShadow: "0 20px 40px rgba(212,132,58,0.2)" }}
  transition={{ duration: 0.3, ease: "easeOut" }}
/>
```

**CTA Buttons** — satisfying press + warmth:
```jsx
<motion.button
  whileHover={{ scale: 1.04, backgroundColor: "#C0522A" }}
  whileTap={{ scale: 0.97 }}
  transition={{ duration: 0.18 }}
/>
```

**Hero parallax** — subtle depth scroll:
```jsx
const { scrollY } = useScroll()
const y = useTransform(scrollY, [0, 500], [0, -80])
// Apply to background image layer
```

**Add-to-cart success** — celebratory micro-animation:
```jsx
<AnimatePresence>
  {added && (
    <motion.span
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0, opacity: 0 }}
      transition={{ type: "spring", stiffness: 400, damping: 20 }}
    >
      ✓ Added!
    </motion.span>
  )}
</AnimatePresence>
```

**Number counters / stats** — animate values up on entry.

**Image zoom** — subtle scale on product image hover:
```jsx
<motion.img whileHover={{ scale: 1.06 }} transition={{ duration: 0.5 }} />
```

### Animation Principles
- Ease curves: prefer `[0.22, 1, 0.36, 1]` (ease-out-expo) for entries, `easeOut` for hovers
- Duration sweet spot: 0.3–0.7s for most interactions, 0.8–1.2s for page-level reveals
- Spring physics for delightful moments (add to cart, quantity selectors, toggles)
- Never animate more than 3 things simultaneously — sequence and stagger instead
- Scroll-triggered reveals for all below-fold content sections

## Component Patterns

### Product Card
- Large product image (aspect-ratio: 4/5 portrait, object-fit: cover)
- Subtle image zoom on hover (Motion)
- Product name in display serif, short tagline in body
- Price in amber, prominent
- Add-to-cart button with press animation + success state
- Optional badge (e.g., "Best Seller", "New", "Spicy 🌶️") in handwritten accent font

### Hero Section
- Full-width with warm gradient overlay on lifestyle/product image
- Large serif headline (3–5rem), short subheadline
- Primary CTA button (amber) + secondary (ghost/outline)
- Scroll indicator (animated chevron)
- Parallax depth on background

### Flavor / Heat Scale
- Visual indicator with warm gradient bar (cream → golden → amber → burnt-sienna)
- Animated fill on mount (Motion width transition)
- Pepper emoji or custom icon indicators

### Testimonial / Review Block
- Warm card style, handwritten quote marks
- Star ratings in golden
- Staggered card entrance on scroll

### Navigation
- Sticky, cream/transparent background with blur
- Logo centered or left
- Amber cart icon with item count badge
- Smooth underline hover on nav links

## Implementation Requirements

1. **Always React + Motion** — no plain HTML/CSS for animated components
2. **Google Fonts** — import via `@import url(...)` in the style block or `<link>` tag
3. **CSS custom properties** — define the full color palette as variables on `:root`
4. **Responsive** — mobile-first, food brands have high mobile traffic
5. **Accessible** — sufficient color contrast, focus states, aria labels on icon buttons
6. **No placeholder grays** — use brand colors even for skeleton/empty states
7. **Appetite-forward copy** — if writing placeholder text, make it sound delicious

## What Makes This Unforgettable

Every component should evoke one of these feelings:
- **"I want to taste that"** — visuals and copy work together to create craving
- **"This feels handmade with love"** — warmth, texture, organic imperfection
- **"This brand gets me"** — friendly, unpretentious, real

Avoid: clinical white space, cold grays, generic card layouts, boring CTA buttons, anything that could be mistaken for a SaaS dashboard.

Commit fully. A well-executed warm serif headline on a cream background with a perfectly timed scroll reveal is worth more than ten mediocre animations.
