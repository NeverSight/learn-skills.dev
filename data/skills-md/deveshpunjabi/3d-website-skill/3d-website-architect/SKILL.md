---
name: 3d-website-architect
description: >
  Expert skill for designing, building, and deploying modern premium websites with advanced animations
  and 3D interactive experiences using Three.js, React Three Fiber, GSAP, and Framer Motion. Use this
  skill whenever the user wants to build a website with 3D elements, create an immersive web experience,
  add interactive 3D graphics to a page, build a premium landing page with cinematic visuals, design a
  modern startup website with animations, create WebGL or Three.js scenes, build a product showcase with
  3D models, or produce any kind of visually impressive, award-winning web interface. Also trigger when
  the user says things like "make it look like Awwwards", "add 3D to my site", "build an interactive
  landing page", "create an immersive experience", "premium website with animations", "modern startup
  page", "hero with particles or globe", "floating 3D elements", or mentions anything related to
  Three.js, React Three Fiber, WebGL, GSAP timelines, scroll-driven animations, particle systems,
  3D product visualization, or cinematic web design — even if they don't explicitly say "3D" or
  "animation".
version: "1.0.0"
author: deveshpunjabi
tags:
  - 3d
  - threejs
  - react-three-fiber
  - webgl
  - animation
  - gsap
  - framer-motion
  - frontend
  - immersive
  - interactive
---

# 3D Website Architect

You are not just writing code. You are simultaneously a senior frontend engineer, a UI/UX designer, a creative developer, a 3D web developer, and a product designer. Your mission is to transform any user idea into a **high-quality modern website** with premium UI and immersive interactions.

Why this matters: most AI-generated websites look generic — flat layouts, dated patterns, no sense of depth or motion. The result you produce must resemble websites created by top startups or award-winning designs found on Awwwards. A cybersecurity platform should feel dramatically different from a creative portfolio. An AI SaaS should feel different from an e-commerce store. The design, animation, and 3D integration must all serve the product.

## Design Philosophy — The Immersive Premium Standard

What separates a forgettable website from an award-winning one:

- **3D with purpose.** Every 3D element must reinforce the product story. An AI platform gets a neural sphere. A cybersecurity tool gets a threat-detection globe. A creative agency gets morphing organic shapes. Decorative 3D with no connection to the product is worse than no 3D at all.
- **Cinematic restraint.** One breathtaking hero scene with subtle ambient elements beats five competing 3D widgets. Reserve visual energy for moments of maximum impact.
- **Performance is a feature.** A beautiful site that loads in 8 seconds is a failed site. Lazy-load 3D, compress assets, provide instant CSS fallbacks on mobile. Users should see content within 1.5 seconds, with 3D loading gracefully behind it.
- **Sensory hierarchy.** Motion should guide attention, not scatter it. The hero animates boldly, scroll reveals are subtle, and ambient elements drift gently. Each level of motion has a distinct purpose.
- **The Awwwards test.** Before delivering, compare your output to sites on Awwwards.com. If yours doesn't belong in the same conversation — iterate.

The goal is NOT to generate basic templates. The goal is to produce **production-ready premium web experiences**.

Follow this **13-Step Immersive Design Process** before and during code generation. Each step builds on the last — skipping steps produces generic output.

---

## Step 1 — Product Understanding

Before writing any code, deeply understand what you're building and who it serves.

Analyze the user's prompt and extract:

- **Product type**: AI platform, developer tool, cybersecurity product, creative agency, SaaS startup, portfolio, e-commerce, fintech, gaming
- **Target audience**: developers, enterprise teams, consumers, creators, executives, gamers
- **Core value proposition**: the single most important thing this product communicates
- **Primary call-to-action**: sign up, book a demo, start free trial, explore features, purchase

Ask internally: *What feeling should the website evoke? What is the user's journey from landing to conversion?*

### Niche-Aware Design Direction

Each niche carries conventions that users expect. Following them builds instant trust; the 3D and animation layer elevates beyond the expected.

| Niche | Design Direction | 3D Opportunity |
|-------|-----------------|----------------|
| AI / ML platforms | Dark themes, glowing accents, futuristic gradients | Neural network visualizations, AI spheres, particle brains |
| Developer tools | Monospace accents, high-contrast, minimal chrome | Rotating code blocks, 3D terminal, floating geometry |
| Cybersecurity | Dark UI, terminal aesthetics, alert-driven | Shield models, data flow particles, globe with attack vectors |
| Creative agencies | Bold typography, warm tones, personality-forward | Interactive art installations, morphing shapes, 3D portfolios |
| SaaS startups | Hero-driven, social proof, feature grids, strong CTAs | Floating product mockups, isometric scenes, abstract shapes |
| E-commerce / Product | Product-focused grids, prominent CTAs, trust badges | 3D product viewers, 360° rotation, AR-ready models |
| Fintech | Trust-heavy, clean, data-dense but organized | Globe with transaction paths, 3D charts, currency flows |
| Gaming / Entertainment | Vibrant, immersive, full-bleed visuals | Character models, environment previews, particle explosions |
| Portfolio | Project showcases, personal brand, scroll-driven narratives | 3D scene transitions, interactive galleries, camera fly-throughs |
| Web3 / Blockchain | Futuristic, neon accents, decentralized aesthetics | Token visualizations, blockchain node networks, holographic UI |

---

## Step 2 — Visual Inspiration Research

Before designing, study modern web design patterns from the best. Reference inspiration from:

- **Awwwards** — award-winning interaction design and visual storytelling
- **Dribbble / Behance** — layout patterns, color palettes, typography hierarchies
- **Pinterest** — mood boards, visual direction, creative references
- Best-in-class products: Vercel, Linear, Raycast, Stripe, Notion, Arc Browser
- 3D-forward sites: Apple product pages, GitHub Universe, Stripe Globe, Linear releases

Analyze these key elements from premium reference designs:

- **Hero layouts**: large bold typography with gradient/italic accent words, floating 3D elements, prominent CTA buttons with glow effects
- **Typography hierarchy**: display-size headlines (48–96px) that demand attention, smaller muted subheadlines, mixed font weights
- **Color palettes**: deep dark backgrounds (navy #0a0a1a, near-black #050510), blue/purple accent systems, warm alternatives for agencies
- **Gradient and glow effects**: subtle radial glows behind heroes, gradient text, soft light bleeds on 3D elements
- **Card design**: glassmorphism (backdrop-blur + translucent borders), dark cards with subtle 1px borders, numbered feature cards
- **Spacing**: generous padding between sections (96–128px), intentional breathing room
- **3D integration patterns**: hero backgrounds with floating geometry, product model showcases, interactive data visualizations, particle systems as ambient decoration
- **Motion design**: scroll-triggered reveals, parallax depth layers, smooth page transitions, hover-driven 3D transforms

### Premium Design Qualities to Emulate

1. **Dark futuristic gradient backgrounds** — deep navy to near-black with subtle radial color bleeds
2. **Cinematic 3D hero sections** — floating geometry, globe visualizations, particle fields that respond to cursor
3. **Glowing highlight effects** — soft accent glows on key elements and 3D objects
4. **Minimal premium layouts** — fewer elements, more impact, strong visual focus
5. **Bold hero typography** — 48–96px display text with mixed weights and italic accents
6. **Glassmorphism cards** — `backdrop-filter: blur(12px)`, rgba backgrounds, subtle light borders
7. **Depth through 3D** — real parallax via Three.js camera, not CSS hacks
8. **Smooth visual flow** — clear reading path guided by animation timing and scroll choreography

Use these only as inspiration — adapt to the product's personality.

---

## Step 3 — Design System Creation

Define the complete visual identity before building. This is what separates a designed experience from a coded template.

### Typography

Pick 2 fonts maximum (1 for headings, 1 for body). Define sizes for display, h1–h4, body, small, caption. Use `clamp()` for fluid responsive sizing.

Strong modern pairings:

| Heading | Body | Vibe | Best For |
|---------|------|------|----------|
| Inter | Inter | Clean, neutral, Swiss-style | Most versatile |
| Space Grotesk | DM Sans | Tech, developer tools | Dev tools, API products |
| Clash Display | Satoshi | Bold, creative, startup energy | Creative agencies, bold startups |
| Manrope | Inter | Geometric, modern | AI products, modern SaaS |
| Sora | Nunito Sans | Friendly, approachable | Consumer apps, education |
| JetBrains Mono | Inter | Developer, terminal | CLI tools, code-heavy products |

### Color Palette

Construct a complete palette — not random colors:

- **Primary**: main brand color (sparingly: CTAs and accents only)
- **Primary gradient**: pair of colors for gradient effects (e.g., blue-500 → purple-500)
- **Neutral scale**: 50 through 950 for backgrounds, borders, and text
- **Semantic colors**: success (green), warning (amber), error (red), info (blue)
- **Glow color**: primary at 10–20% opacity for 3D element emanation
- **3D material colors**: variations of primary/accent for Three.js materials

Dark theme rules (default for 3D-heavy sites — dark backgrounds make 3D glow effects pop):

- Use gray-900/950 for backgrounds, never pure black (#000)
- Elevate surfaces with slightly lighter backgrounds, not stronger shadows
- Reduce primary saturation by 10–20% to avoid eye strain
- Ensure 4.5:1 contrast for body text, 3:1 for large text
- 3D elements should use emissive materials that complement the accent palette

### Spacing, Radius, and Shadows

- **Spacing scale** (4px base): 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128
- **Border radius**: stay consistent — sharp (2–4px) for enterprise, soft (8–12px) for SaaS, rounded (16–24px) for consumer
- **Shadows**: 3 levels (cards, dropdowns, modals), tinted toward primary hue for premium feel

For complete reference tables, font scales, CSS recipes, glassmorphism patterns, gradient recipes, and detailed palette examples, see `references/design-systems.md`.

---

## Step 4 — Website Structure

Design the page architecture before coding. Every section guides the user toward the conversion goal.

### Modern Landing Page Architecture

```
Navigation (logo + links + primary CTA button — sticky, with backdrop-blur)
↓
Hero Section (display headline + subheadline + CTA buttons + 3D visual/scene)
↓
Social Proof (logo bar, stats, or "Trusted by X+ teams")
↓
Product Introduction (value proposition — 2–3 sentences + visual)
↓
Feature Breakdown (grid of cards, 3D interactive previews, or alternating sections)
↓
Interactive Demo (3D product viewer, live preview, or animated walkthrough)
↓
Benefits Section (why choose us — numbered cards or comparison)
↓
How It Works (numbered steps with icons or 3D visuals)
↓
Pricing (2–3 tier glassmorphism cards with highlighted recommended plan)
↓
Testimonials (avatar + quote + company, or case study cards)
↓
Final CTA (strong headline + prominent button + ambient 3D background)
↓
Footer (links, social icons, copyright)
```

Adapt the structure to the product — never force every project into the same layout.

---

## Step 5 — Component Architecture

Build modular, reusable components. Each component should do one thing well, accept props for content/variants, handle its own responsive behavior, and use semantic HTML with ARIA attributes.

### Component Organization

```
components/
├── layout/       → Navbar, Footer, Container, Section
├── ui/           → Button, Card, GlassCard, Badge, Input, Modal, Toggle
├── sections/     → Hero, Features, Pricing, Testimonials, CTA, HowItWorks
├── three/        → Scene, Canvas, Lights, Camera, custom 3D components
└── animations/   → ScrollReveal, ParallaxWrapper, StaggerContainer
```

### Component Quality Standards

- Consistent spacing, typography, color usage across every component
- Variant-driven props: `<Button variant="primary" size="lg" glow>` — not separate component files per variant
- Glassmorphism card recipe: `backdrop-filter: blur(12px)`, `background: rgba(255,255,255,0.05)`, `border: 1px solid rgba(255,255,255,0.1)`
- Interactive elements: visible hover/focus states, smooth 200ms transitions, proper cursor styles
- 3D components: wrapped in `Suspense` with loading fallbacks, error boundaries for WebGL failures

---

## Step 6 — Advanced Animation System

Animations make the interface feel alive and premium. They must be smooth and purposeful — never excessive or distracting.

### Animation Hierarchy

| Priority | Type | Purpose |
|----------|------|---------|
| 1 | Scroll reveals | Guide attention as user scrolls through content |
| 2 | Hover effects | Provide interactive feedback on actionable elements |
| 3 | Micro-interactions | Polish details: button press, toggle, icon rotation |
| 4 | Page transitions | Smooth navigation between sections or pages |
| 5 | Ambient motion | Background particles, floating shapes, subtle 3D rotation |

### Scroll-Driven Animations

Use Framer Motion's `useInView` or GSAP's ScrollTrigger:

- Elements fade + slide in as they enter viewport (translate 20–30px + opacity 0→1, 400–600ms)
- Stagger children in grids/lists with 50–100ms delay between each
- Pin sections for parallax storytelling sequences
- Progress-based animations: elements transform as scroll progresses through a section

### Hover Effects

- Cards: scale(1.02–1.05), glow intensification, border color shift
- Buttons: background shift, shadow expansion, subtle translate Y (-2px)
- 3D elements: increased rotation speed, color emission change, scale pulse

### Animation Libraries

| Library | Role |
|---------|------|
| Framer Motion | Declarative React animations — scroll reveals, layout transitions, gesture-driven |
| GSAP + ScrollTrigger | Complex timelines, scroll-pinning, SVG morphing, high-performance sequences |
| CSS transitions | Simple hovers and state changes (no library needed for basic interactions) |

### Animation Rules

- Use `transform` and `opacity` for GPU-accelerated performance — never animate `width`, `height`, `top`, `left`
- Respect `prefers-reduced-motion` — provide static fallbacks
- Entrance animations: slight upward slide + fade, not dramatic fly-ins
- Interactive feedback: < 100ms response time — delays feel broken
- 3D animations should run at 60fps — monitor with `Stats.js` or Chrome DevTools performance panel

For detailed GSAP timeline recipes, Framer Motion patterns, and scroll choreography examples, see `references/animation-patterns.md`.

---

## Step 7 — 3D Interactive Experience

This is what elevates a premium website into an immersive experience. 3D should enhance the narrative, not distract from it.

### When to Use 3D

3D elements add value when they:

- **Communicate product identity** — an AI brain, a security shield, a data globe
- **Create visual hierarchy** — drawing attention to the hero or key sections
- **Enable interaction** — product viewers, explorable environments, data visualizations
- **Establish mood** — ambient particles, floating geometry, depth through parallax

3D does NOT add value when it's purely decorative with no connection to the product or when it significantly degrades performance.

### Technology Stack for 3D

| Technology | Role |
|-----------|------|
| Three.js | Core 3D rendering engine — geometry, materials, lights, cameras |
| React Three Fiber | React renderer for Three.js — declarative 3D in JSX components |
| @react-three/drei | Pre-built helpers: OrbitControls, Environment, Float, Text3D, Sparkles |
| @react-three/postprocessing | Post-processing effects: bloom, chromatic aberration, depth of field |
| WebGL | Browser GPU API (underlying Three.js — rarely used directly) |

### Common 3D Elements

**Hero Backgrounds**
- Floating geometric shapes (icosahedrons, torus knots, custom geometry)
- Particle fields that respond to mouse movement
- Gradient sphere/globe with animated shader materials
- Wireframe landscapes or terrain meshes

**Product Showcases**
- 3D product model viewers with orbit controls
- Animated device mockups (floating laptop, phone)
- Exploded-view product breakdowns
- Interactive feature highlights on 3D models

**Data Visualizations**
- 3D globe with connection arcs (network/coverage maps)
- Particle systems representing data flow
- 3D bar/surface charts for complex datasets
- Node networks for architecture/relationship diagrams

**Ambient Elements**
- Floating particles with subtle drift
- Morphing blob shapes (shader-based)
- Light ray effects and volumetric fog
- Stars / space backgrounds

### 3D Scene Architecture

```tsx
<Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
  <Suspense fallback={null}>
    {/* Lighting */}
    <ambientLight intensity={0.5} />
    <pointLight position={[10, 10, 10]} intensity={1} />

    {/* 3D Content */}
    <HeroScene />

    {/* Environment & Effects */}
    <Environment preset="night" />
    <EffectComposer>
      <Bloom luminanceThreshold={0.8} intensity={0.5} />
    </EffectComposer>
  </Suspense>
</Canvas>
```

### 3D Quality Standards

- Always wrap `<Canvas>` content in `<Suspense>` with a loading indicator
- Use low-poly geometry (< 10k triangles per mesh) for web performance
- Apply emissive materials matching the accent color palette
- Add camera movement: subtle float, mouse-follow parallax, or orbit
- Light scenes with 2–3 lights: ambient (base), directional (key), point (accent)
- Use post-processing sparingly: bloom for glow, not stacked heavy effects
- Provide error boundaries for WebGL context loss
- Enable `frameloop="demand"` on Canvas when 3D is not always visible to save GPU

For complete Three.js recipes, material systems, shader examples, and performance patterns, see `references/3d-integration.md`.

---

## Step 8 — Frontend Technology Stack

Use modern production-grade technologies:

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Framework | Next.js (App Router) | SSR/SSG, routing, optimized builds |
| Language | TypeScript | Type safety, self-documenting code |
| Styling | Tailwind CSS | Rapid iteration, design-system utilities |
| UI Primitives | shadcn/ui + Radix UI | Accessible, unstyled components to theme |
| Animation | Framer Motion + GSAP | Declarative + timeline-based animation |
| 3D | Three.js + React Three Fiber | WebGL rendering in React |
| 3D Helpers | @react-three/drei | Pre-built 3D utilities and components |
| Post-processing | @react-three/postprocessing | Bloom, DOF, chromatic aberration |
| Icons | Lucide React | Clean, consistent icon system |

If the user specifies a different stack (Vue, Svelte, plain HTML/CSS/JS), respect that choice — the design and 3D principles are tool-agnostic.

---

## Step 9 — Project Structure

Organize the codebase clearly so the project is maintainable and scalable:

```
app/
├── layout.tsx          → Root layout with fonts, metadata
├── page.tsx            → Main page composing sections
├── globals.css         → Global styles, CSS variables, Tailwind layers
components/
├── layout/             → Navbar, Footer, Container
├── ui/                 → Button, Card, GlassCard, Badge, Input
├── sections/           → Hero, Features, Pricing, Testimonials, CTA
├── three/              → 3D scenes, custom geometries, shaders
│   ├── HeroScene.tsx   → Main hero 3D scene
│   ├── Particles.tsx   → Particle system component
│   └── Globe.tsx       → Globe/sphere visualization
├── animations/         → ScrollReveal, ParallaxWrapper, StaggerContainer
lib/
├── utils.ts            → Helper functions, cn() class merger
├── constants.ts        → Site content, configuration
styles/
├── fonts.ts            → Font configuration (next/font)
public/
├── models/             → .glb/.gltf 3D model files
├── textures/           → HDR environments, texture maps
├── images/             → Optimized static images
```

---

## Step 10 — Performance Optimization

A beautiful website that loads slowly is a failed website. Performance is a core design requirement — especially with 3D.

### Critical Optimizations

| Area | Technique |
|------|-----------|
| 3D Models | Use glTF/GLB format, keep under 2MB, draco compression |
| Textures | Compress to WebP/AVIF, use power-of-2 dimensions, max 2048px |
| Code Splitting | Dynamic import for 3D components — `next/dynamic` with `{ ssr: false }` |
| Canvas Loading | `<Suspense>` with skeleton/placeholder while 3D initializes |
| Frame Rate | Target 60fps — use `Stats.js` in dev, `frameloop="demand"` when idle |
| Shaders | Use simple fragment shaders, avoid complex ray-marching on mobile |
| Images | `next/image` with proper `width`/`height`, lazy loading below fold |
| Fonts | `next/font` for zero layout shift, subset to used characters |
| Bundle | Tree-shake Three.js imports — import specific modules, not the full library |
| GPU | GPU-accelerated CSS: `transform`, `opacity`, `will-change` on animated elements |

### Performance Budgets

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.5s |
| Largest Contentful Paint | < 2.5s |
| Total Bundle (gzipped) | < 300KB (JS), 3D assets separately lazy-loaded |
| 3D Scene Init | < 3s to interactive |
| Frame Rate | Consistent 60fps (30fps acceptable on low-end mobile) |

---

## Step 11 — Responsive Design

Every interface must work perfectly across devices. 3D experiences require special attention on mobile.

### Breakpoints (Tailwind Defaults)

| Token | Width | Target |
|-------|-------|--------|
| `sm` | 640px | Large phones |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large displays |

### Responsive Patterns

- Grid columns: 4 → 2 → 1 as viewport shrinks
- Navigation: full menu → hamburger/drawer below 768px
- Typography: display text scales from 96px → 48px → 32px using `clamp()`
- Section padding: 128px → 80px → 48px (desktop → tablet → mobile)
- Touch targets: minimum 44×44px on mobile

### 3D Responsive Strategy

This is critical — heavy 3D can destroy mobile experience:

- **Desktop**: full 3D scene with post-processing, high particle counts, detailed geometry
- **Tablet**: reduced particle counts, simplified geometry, no post-processing
- **Mobile**: fallback to CSS animations, static images, or minimal 3D (simple rotating shape)
- Detect device capability with `navigator.hardwareConcurrency` and `renderer.capabilities`
- Use `useMediaQuery` or `window.matchMedia` to conditionally render 3D vs. fallback
- Set `pixelRatio` to `Math.min(window.devicePixelRatio, 2)` — no need for 3x on mobile

```tsx
// Example: responsive 3D fallback
const isMobile = useMediaQuery('(max-width: 768px)');

return isMobile ? (
  <AnimatedGradientBackground /> // lightweight CSS fallback
) : (
  <Canvas>
    <HeroScene />
  </Canvas>
);
```

---

## Step 12 — Testing & Quality Assurance

Run production-level validation before declaring the build complete.

### Testing Checklist

**Performance**
- [ ] Lighthouse score > 90 on Performance
- [ ] No layout shift (CLS < 0.1)
- [ ] 3D scene loads within 3 seconds
- [ ] Consistent 60fps during scroll and interaction

**Responsiveness**
- [ ] Test at 375px, 768px, 1024px, 1440px
- [ ] Navigation collapses properly on mobile
- [ ] 3D fallback activates on mobile/low-end devices
- [ ] Touch interactions work (no hover-only states blocking mobile)

**Animation**
- [ ] All scroll reveals trigger correctly
- [ ] Hover states respond within 100ms
- [ ] `prefers-reduced-motion` respected
- [ ] No janky or stuttering animations

**Browser Compatibility**
- [ ] Chrome, Firefox, Safari, Edge — latest two versions
- [ ] WebGL support detection with graceful fallback
- [ ] CSS backdrop-filter fallback for older browsers

**Accessibility**
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Alt text on images, aria-labels on interactive 3D
- [ ] Keyboard navigation works
- [ ] Color contrast meets WCAG 2.1 AA

### Testing Tools

| Tool | Purpose |
|------|---------|
| Lighthouse | Performance, accessibility, SEO audit |
| Chrome DevTools Performance | Frame rate, rendering bottlenecks |
| React Profiler | Component render performance |
| Stats.js | Real-time FPS monitoring for 3D scenes |
| axe DevTools | Accessibility audit |

---

## Step 13 — Production Build, Deployment & Error Resolution (MANDATORY)

**This step is non-negotiable.** After the build is complete, the agent MUST run these checks and fix every issue before declaring the task done.

### 13.1 — Build & Deploy Preparation

1. Optimize bundle: tree-shake unused imports, analyze with `next build --analyze`
2. Compress 3D assets: draco-compress glTF models, optimize textures to WebP/AVIF
3. Configure `next.config.js` for optimal output
4. Run `next build` and verify zero errors
5. Test production build locally with `next start`

### Deployment Targets

| Platform | Command | Notes |
|---------|---------|-------|
| Vercel | `vercel --prod` | Best for Next.js, automatic optimization |
| Netlify | `netlify deploy --prod` | Good for static exports |
| Cloudflare Pages | `wrangler pages deploy` | Edge-first, global CDN |

### 13.2 — Automated Error Resolution

```bash
npm install          # Catch missing packages
npx tsc --noEmit     # Catch ALL type errors
npm run build        # Catch build-time errors
npx next lint        # Catch code quality issues
```

**If any command fails:** read the error, fix it, re-run, repeat until zero errors.

### 13.3 — 3D-Specific Error Checks

| Check | What to Look For | Fix |
|-------|-----------------|-----|
| **WebGL context** | `<Canvas>` renders without console errors | Add error boundary, check WebGL support |
| **Shader compilation** | GLSL errors in custom shaders | Fix shader syntax, test uniforms |
| **Model loading** | `.glb/.gltf` files 404 | Check paths, ensure files in `public/` |
| **Memory leaks** | `useEffect` cleanup disposes geometries/materials | Add `geometry.dispose()`, `material.dispose()` |
| **SSR crashes** | R3F components in server components | Use `'use client'` directive, `next/dynamic` with `ssr: false` |
| **Missing Suspense** | `<Canvas>` without `<Suspense>` boundary | Wrap 3D scenes in `<Suspense fallback={...}>` |

### 13.4 — Final Resolution Loop

```
WHILE errors exist:
  1. Run: npm run build → IF fail → fix → GOTO 1
  2. Run: npx next lint → IF fail → fix → GOTO 1
  3. Run: npm run dev → IF crash → fix → GOTO 1
  4. All clear → EXIT
```

**The agent MUST NOT declare the task complete until:**
- [ ] `npm run build` exits with code 0
- [ ] `npx next lint` passes (no errors)
- [ ] `npm run dev` boots without crashing
- [ ] No TypeScript errors (`npx tsc --noEmit` passes)
- [ ] 3D scenes load with proper Suspense boundaries
- [ ] No hydration mismatch warnings

> **Rule: If you generated the code, you own the errors. Fix them before finishing.**

---

## Visual Quality Validation

Before finalizing, validate against these standards. If any answer is "no" — go back and fix it.

**Typography**
- [ ] Type hierarchy is strong (display > h1 > h2 > body are clearly distinct)
- [ ] Headings use negative letter-spacing (-0.02em to -0.04em)
- [ ] Body text is 16–18px with 1.5–1.7 line height
- [ ] Lines capped at 65–75 characters maximum width

**Spacing & Layout**
- [ ] Every spacing value comes from the defined scale
- [ ] Sections have generous vertical padding (80–128px on desktop)
- [ ] Layout feels spacious and intentional, nothing cramped

**Color & Polish**
- [ ] Primary color used sparingly — CTAs and key accents only
- [ ] Gradients are subtle and purposeful
- [ ] Interactive elements have hover/focus states with smooth transitions
- [ ] Shadows are colored/tinted, never pure black rgba(0,0,0,x)

**3D & Animation**
- [ ] 3D elements serve the product narrative, not just decoration
- [ ] Animations are smooth at 60fps
- [ ] Loading states exist for 3D content
- [ ] Mobile has appropriate fallbacks

**Overall Impression**
- [ ] The UI looks premium and modern — not like a generic template
- [ ] It resembles award-winning websites (Awwwards quality)
- [ ] The design serves this specific product's niche and audience
- [ ] A user would trust and respect this product based on visual quality alone
- [ ] The 3D integration feels natural and purposeful, not gimmicky

---

## Anti-Patterns — What to Avoid

Understanding what fails helps you avoid it:

| Anti-Pattern | What Goes Wrong | Fix |
|-------------|----------------|-----|
| **3D carnival** | Too many 3D elements competing for attention | One hero 3D scene + subtle ambient elements |
| **Performance blindness** | Beautiful but loads in 8 seconds | Performance budgets, lazy load, compress assets |
| **Mobile neglect** | 3D crashes on phones | Device detection, progressive enhancement, CSS fallbacks |
| **Rainbow soup** | Too many unrelated colors | Stick to your palette — primary, neutral, 1–2 accents |
| **Wall of identical cards** | No visual hierarchy | Vary sizes, highlight featured items, use visual weight |
| **Bootstrap syndrome** | Default template look with swapped colors | Design from scratch using the visual system you defined |
| **Shader overkill** | Complex shaders tank frame rate | Simple materials, emissive glow, use post-processing sparingly |
| **Animation overload** | Everything moves, nothing rests | Strategic motion — animate to guide attention, not to decorate |
| **Hover-only 3D** | Touch devices can't interact | Support both pointer and touch, provide passive animation |
| **Decorative 3D** | 3D elements with no connection to product | Every 3D element should reinforce the product story |
| **The gray wasteland** | Everything is gray with no visual interest | Use contrast deliberately and accent colors surgically |
| **Lorem ipsum laziness** | Placeholder text makes design unjudgeable | Write realistic copy that matches the product's voice |
| **Typography neglect** | All text looks the same size/weight | Build clear hierarchy: display, heading, subhead, body |

### The "Awwwards or Redo" Test

After building, honestly evaluate:

1. **Screenshot test** — Put your screenshot next to Linear.app, Stripe.com, or an Awwwards winner. Does it belong?
2. **Squint test** — Squint at the page. Clear visual hierarchy? Important elements dominant?
3. **3-second test** — Show it for 3 seconds. Can someone tell what the product does?
4. **Motion test** — Scroll through once. Does the animation feel choreographed or chaotic?

If any answer is "no" — iterate before delivery.

---

## Final Output

The AI must generate:

- **Complete frontend code** — full Next.js project with TypeScript
- **Modular component system** — reusable, typed, well-organized
- **Modern responsive layout** — beautiful on every screen size
- **Smooth animation system** — scroll reveals, hovers, micro-interactions at 60fps
- **3D interactive experience** — Three.js/R3F scene integrated purposefully into the design
- **Performance-optimized build** — lazy-loaded 3D, compressed assets, efficient rendering
- **Realistic content** — believable copy, real-sounding data, proper text lengths
- **Design system documentation** — brief summary of palette, typography, and design rationale

The final result must feel like an **award-winning modern product website** — the kind featured on Awwwards, not the kind generated by a template builder.

### Cross-Agent Compatibility

This skill works with any AI coding agent that supports Markdown-based skill files:

| Agent | Installation |
|-------|-------------|
| Claude Code | `npx skills add deveshpunjabi/3d-website-skill` |
| Cursor | Copy to `.cursor/skills/` |
| Windsurf | Copy to `.windsurf/skills/` |
| Cline | Copy to `.cline/skills/` |
| Codex | Copy to `.codex/skills/` |
| Aider | Reference in `.aider.conf` |
| Any agent | Copy skill directory to the agent's skill/instruction folder |

The skill is Markdown-based with optional reference documents — no runtime dependencies, no API keys, no build steps.
