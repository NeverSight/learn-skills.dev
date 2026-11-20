---
name: frontend-master
description: >
  Master frontend design skill. Produces distinctive, production-grade
  websites that avoid AI slop. Combines design thinking, typography, motion,
  component patterns, and research catalogs. Invoke before ANY website or landing
  page build.
---

# Frontend Master Skill

## Design Consultation Protocol (MANDATORY — Do This First)

Before writing ANY frontend code, act as a design advisor:

1. **ASK** the user: What tone/aesthetic? Dark or light? Any reference sites? Animation level (minimal / moderate / rich)?
2. **RECOMMEND** patterns from the Atelier catalogs at `catalogs/` — suggest hero archetypes, component patterns, color palettes that match the brief
3. **SUGGEST** 2-3 font pairings from the Proven Pairings below based on project tone
4. **FLAG** any anti-slop violations during build ("Inter for display text detected — swapping to Satoshi")
5. **OFFER** component upgrades from catalogs when relevant ("Glass morphism card from COMPONENT-CATALOG fits here — want it?")
6. **CHECK** for a `brand-assets/` folder in the project — ask about missing items (no logo? no guidelines?)
7. **PRESENT** hero archetype options with visual descriptions

---

## Pre-Build Checklist

| Step | Action | Result |
|------|--------|--------|
| 1 | Choose ONE tone from archetypes table | Bold aesthetic direction |
| 2 | Pick display + body font pairing | Distinctive typography |
| 3 | Define color system (3-5 colors with CSS variables) | Cohesive palette |
| 4 | Identify ONE unforgettable element | Memorable differentiator |
| 5 | Check Atelier catalogs for latest patterns | Fresh, non-generic design |

---

## Design Thinking Framework

Choose an EXTREME aesthetic direction. Pick ONE and commit fully:

| Tone | Characteristics | Reference |
|------|-----------------|-----------|
| **Brutalist** | Raw, honest, bold typography, minimal decoration | — |
| **Maximalist** | Rich, layered, ornate, high visual density | — |
| **Retro-Futuristic** | Vintage meets sci-fi, neon, chrome | — |
| **Organic** | Natural shapes, earth tones, flowing curves | calm.com |
| **Luxury** | Refined, elegant, high contrast, premium feel | — |
| **Playful** | Bright colors, rounded shapes, animations | — |
| **Editorial** | Magazine-like, strong typography hierarchy | Bloomberg |
| **Minimalist** | Essential only, generous whitespace, precise | Linear.app, Stripe |

Ask: **"What single element will make this UNFORGETTABLE?"** — a unique interaction, a distinctive color, an unusual layout, a memorable animation.

---

## Typography Rules

### BANNED Fonts (Scream "AI Generated")
Inter, Roboto, Arial, Open Sans, system fonts — NEVER use these for display/headlines.

### Proven Pairings

| Display | Body | Vibe | Best For |
|---------|------|------|----------|
| **Clash Display** | DM Sans | Bold modern | Tech, SaaS, agencies |
| **Fraunces** | Source Sans 3 | Elegant editorial | Luxury, healthcare, editorial |
| **Cabinet Grotesk** | Plus Jakarta Sans | Clean editorial | Professional services |
| **Space Grotesk** | JetBrains Mono | Developer/tech | Dev tools, AI products |
| **Satoshi** | Outfit | Geometric clean | Startups, modern B2B |
| **Syne** | DM Sans | Unique tech | Creative agencies, AI |
| **Playfair Display** | DM Sans | Luxury serif | Real estate, high-end |

### Hierarchy Scale
```
Hero:     48-72px, weight 700
Section:  32-48px, weight 600
Subtitle: 24-32px, weight 500
Body:     16-18px, weight 400
Caption:  12-14px, weight 400
```

### Text Effects
```css
/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Animated underline on hover */
.animated-underline {
  background-image: linear-gradient(currentColor, currentColor);
  background-position: 0% 100%;
  background-repeat: no-repeat;
  background-size: 0% 2px;
  transition: background-size 0.3s;
}
.animated-underline:hover { background-size: 100% 2px; }
```

---

## Color Strategy

### Always Use CSS Variables
```css
:root {
  --color-primary: #hex;
  --color-secondary: #hex;
  --color-accent: #hex;
  --color-bg: #hex;
  --color-text: #hex;
}
```

### Palette Patterns
- **Dominant + Sharp Accent**: One strong color (60%) + one contrasting accent (10%) + neutrals (30%)
- **Unexpected Combinations**: Avoid safe corporate blues. Try terracotta + sage, deep navy + warm gold, near-black + white accent
- **Gradients**: Use on CTA buttons, screenshot overlays, accent borders on hover — NOT on backgrounds

### Dark Mode Structure
```css
.dark {
  --bg-primary: #0F172A;
  --bg-secondary: #1E293B;
  --bg-elevated: #334155;
  --text-primary: #F8FAFC;
  --text-secondary: #94A3B8;
  --border: #334155;
}
```

### Healthcare Palettes (Common Client Type)
- **Warm Trust**: Terracotta #E07A5F, Charcoal #3D405B, Sage #81B29A, Cream #F4F1DE
- **Ocean Professional**: Teal #2A9D8F, Navy #264653, Gold #E9C46A, Cool White #FAFBFC

---

## Motion Library (Framer Motion)

### Fade-In on Mount
```jsx
<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: "easeOut" }}>
```

### Scroll-Triggered Reveal
```jsx
<motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }}
  viewport={{ once: true, amount: 0.3 }}>
```

### Hover Lift
```jsx
<motion.div whileHover={{ y: -4, boxShadow: "0 10px 30px rgba(0,0,0,0.1)" }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}>
```

### Staggered Children
```jsx
const container = { hidden: {}, show: { transition: { staggerChildren: 0.1 } } };
const item = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } };
<motion.div variants={container} initial="hidden" whileInView="show">
  {items.map(i => <motion.div key={i} variants={item} />)}
</motion.div>
```

### Best Practices
- Use `transform` and `opacity` only (GPU accelerated)
- Timing: 0.2-0.5s micro-interactions, 0.5-1s larger animations
- Easing: custom cubic-bezier or spring, NEVER linear
- Respect `prefers-reduced-motion`
- Use GSAP for complex timelines, text splitting, SVG morphing

---

## Hero Archetypes

### 1. Split Hero (Text Left + Visual Right)
Best for SaaS, healthcare, B2B. Text + CTA on left, dashboard/image on right, social proof strip below.

### 2. Centered Hero
Best for product launches, landing pages. Large centered headline, subheadline, dual CTAs, visual below.

### 3. Full-Bleed Media Hero
Best for luxury, real estate, portfolios. Background video/image fills viewport, overlay text + CTA.

### 4. Manifesto Hero
Best for AI/consulting, bold brands. Two-line bold statement (second line muted). Words ARE the hero — no product image.

### 5. Asymmetric Overlap Hero
Best for creative, editorial, agencies. Large headline breaking grid, image overlapping text area, offset CTA.

### Background Treatments
```tsx
/* Gradient Mesh */
<div className="absolute -top-40 -right-40 h-80 w-80 rounded-full bg-emerald-500/20 blur-3xl" />

/* Dot Grid */
<div className="bg-[radial-gradient(circle,_rgba(0,0,0,0.1)_1px,_transparent_1px)] bg-[size:20px_20px]" />

/* Noise Texture */
<div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'url(/noise.svg)' }} />
```

---

## Component Patterns

### Glass Morphism Card
```tsx
<div className="rounded-2xl border border-white/20 bg-white/10 p-6 backdrop-blur-xl shadow-xl">
```

### Hover Reveal Card
```tsx
<motion.div className="group relative overflow-hidden rounded-2xl bg-slate-900 p-8" whileHover={{ y: -4 }}>
  <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/10 to-cyan-500/10 opacity-0 group-hover:opacity-100 transition-opacity" />
  <div className="relative z-10">{/* Content */}</div>
</motion.div>
```

### Sticky Blur Nav
```tsx
<nav className="sticky top-0 z-50 border-b border-white/10 bg-white/80 backdrop-blur-lg dark:bg-slate-900/80">
```

### Trust Badge Row
```tsx
<div className="flex flex-wrap items-center justify-center gap-3">
  <Badge variant="outline"><ShieldCheck className="w-3 h-3 mr-1" /> HIPAA Compliant</Badge>
  ...
</div>
```

### Logo Bar (Social Proof)
Grayscale logos, hover to color. "Trusted by X+ companies" label above.

### Numbered Section System
```tsx
<span className="text-sm font-mono tracking-widest text-muted-foreground">01 - CODE</span>
<h2 className="text-3xl font-medium mb-4">Section Title</h2>
```

---

## Anti-AI-Slop Checklist

Before shipping, verify ALL pass:

- [ ] **No banned fonts** — display text uses distinctive fonts, NOT Inter/Roboto/Arial
- [ ] **No purple gradients** — colors are brand-specific with hex codes, not generic
- [ ] **No symmetrical layouts** — vary sizes, create hierarchy, embrace asymmetry
- [ ] **No predictable cards** — mix card styles, use accents, vary heights
- [ ] **No bouncy animations** — use ease-out, subtle transforms, spring physics
- [ ] **Real content** — names, numbers, dates — never "Lorem ipsum"
- [ ] **Distinctive font pairing** — heading font differs from body font
- [ ] **Intentional whitespace** — 32-48px section padding, generous gaps
- [ ] **Specific borders** — exact rgba values, not vague outlines
- [ ] **Named aesthetic** — design matches ONE committed tone, not generic "modern"

---

## Tech Stack Defaults

| Tool | Version | Purpose |
|------|---------|---------|
| React | 19+ | UI framework (TypeScript) |
| Vite | 7+ | Build tool |
| Tailwind CSS | v4 | Styling |
| Framer Motion | 12+ | Animations |
| React Router | 7+ | Routing (multi-page) |
| GSAP | 3+ | Complex timelines (when needed) |
| Spline | — | 3D elements (when needed) |

---

## Optimization Checklist (Pre-Deploy)

- [ ] Convert PNG → WebP via `sharp` (typical: 40MB → 1.1MB)
- [ ] Add `<link rel="preload">` for hero images
- [ ] Add `<link rel="prefetch">` for below-fold images
- [ ] Create `vercel.json` with SPA rewrites + immutable cache headers
- [ ] Semantic HTML5 with alt text on all images
- [ ] Mobile-first responsive (sm:640, md:768, lg:1024, xl:1280)
- [ ] Test with Lighthouse (target: 90+ all categories)

---

## Reference Catalogs

Before any build, check the latest patterns at:
`catalogs/`

| Catalog | What It Contains |
|---------|-----------------|
| HERO-CATALOG.md | Hero layouts, CTA patterns, background treatments |
| ANIMATION-CATALOG.md | Framer Motion, GSAP, CSS animation recipes |
| TYPOGRAPHY-CATALOG.md | Font pairings, type scale, text effects |
| COLOR-CATALOG.md | Palettes, dark mode systems, gradient strategies |
| COMPONENT-CATALOG.md | Cards, nav, stats, trust badges, testimonials |
| SITE-TEARDOWNS.md | Full breakdowns of award-winning sites |

---

## Screenshot Loop

Take screenshots and compare to reference designs:
```bash
node "tools/screenshot/screenshot.js" <url> <output.png> [--full-page] [--width=1440] [--delay=2000]
```
- Read the output image (multimodal) to compare against reference
- Do NOT screenshot animated elements (freeze mid-frame)
- Use `--delay=2000` for pages with entrance animations

## Component Sources

When looking for specific components:
- **21st.dev** — AI-optimized React + Tailwind components (copy-paste ready)
- **shadcn/ui** — Base components (`npx shadcn@latest add [component]`)
- **Aceternity UI** — Animated backgrounds, cards, effects
- **Magic UI** — Animated text, borders, effects
- Always adapt to project's design system — NEVER use as-is
