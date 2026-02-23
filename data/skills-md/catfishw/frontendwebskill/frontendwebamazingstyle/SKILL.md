---
name: FrontendWebAmazingStyle
description: World-class cinematic landing page architect. Creates high-fidelity, pixel-perfect landing pages with "High-End Organic Tech" aesthetic. Use for premium brand landing pages requiring sophisticated animations, micro-interactions, and production-quality frontend craftsmanship.
---

# Cinematic Landing Page Architect

Role: Act as a World-Class Senior Creative Technologist and Lead Frontend Engineer.

Objective: Architect a high-fidelity, cinematic "1:1 Pixel Perfect" landing page for [BRAND_NAME], a premium [PRODUCT_CATEGORY e.g. health optimization / longevity / personalized medicine] brand.

Aesthetic Identity: "High-End Organic Tech" / "Clinical Boutique." The site should feel like a bridge between a biological research lab and an avant-garde luxury magazine.

---

## 1. CORE DESIGN SYSTEM (STRICT)

### Palette

| Name | Hex | Usage |
|------|-----|-------|
| Moss (Primary) | `#2E4036` | Primary brand color |
| Clay (Accent) | `#CC5833` | Accent, CTAs, highlights |
| Cream (Background) | `#F2F0E9` | Background, light sections |
| Charcoal (Dark) | `#1A1A1A` | Text, dark sections |

### Typography

- **Headings**: "Plus Jakarta Sans" & "Outfit" (Tracking tight)
- **Drama/Emphasis**: "Cormorant Garamond" (Must use Italic for biological/organic concepts)
- **Data**: Clean Monospace font for clinical telemetry

### Visual Texture

- Global CSS Noise overlay (SVG turbulence at 0.05 opacity) to eliminate flat digital gradients
- Border radius system: `rounded-[2rem]` to `rounded-[3rem]` for all containers

---

## 2. COMPONENT ARCHITECTURE & BEHAVIOR

### A. NAVBAR (The Floating Island)

- Fixed, pill-shaped container
- **Morphing Logic**: 
  - Transparent with white text at hero top
  - Transitions to white/60 glassmorphic blur with moss text and subtle border on scroll

```tsx
// Tailwind reference
className="fixed top-4 left-1/2 -translate-x-1/2 px-8 py-3 rounded-full z-50 transition-all duration-500"
// Scroll state: bg-white/60 backdrop-blur-md border border-[#2E4036]/10
```

### B. HERO SECTION

- **Height**: `100dvh`
- **Background**: Moody, cinematic misty forest image (generate via T2I-Studio-Premium) with heavy Moss-to-Black gradient overlay
- **Layout**: Content pushed to bottom-left third
- **Typography**: Large scale contrast
  - "[Brand Nature Statement]" (Bold Sans)
  - "[Powerful Concept.]" (Massive Serif Italic)
- **Animation**: GSAP staggered fade-up for all text parts

```tsx
// Gradient overlay
className="absolute inset-0 bg-gradient-to-b from-[#2E4036]/80 via-[#2E4036]/60 to-[#1A1A1A]"
```

### C. FEATURES (The Precision Micro-UI Dashboard)

Replace standard cards with Interactive Functional Artifacts:

#### Card 1 (Intelligence Layer): "Diagnostic Shuffler"
- 3 overlapping white cards that cycle vertically
- Labels adapted to brand context
- Use GSAP for cycling animation

#### Card 2 (Live Intelligence): "Telemetry Typewriter"
- Live optimizing messages with blinking clay cursor
- Pulsing "Live Feed" dot
- Typewriter effect with GSAP

#### Card 3 (Protocol Engine): "Mock Cursor Protocol Scheduler"
- Weekly grid with animated SVG cursor
- Subtle motion indicating active scheduling

### D. PHILOSOPHY (The Manifesto)

- High-contrast Charcoal section
- Parallaxing organic texture background (generate via T2I-Studio-Premium)
- **Text Layout**: Huge typography comparison
  - "Modern medicine asks: What is wrong?" vs. "We ask: What is optimal?"
- **Animation**: Split-text GSAP reveals

```tsx
className="bg-[#1A1A1A] min-h-screen relative overflow-hidden"
// Parallax background with organic texture
```

### E. PROTOCOL (Sticky Stacking Archive)

- Vertical stack of 3 full-screen cards
- **Stacking Interaction**: Using GSAP ScrollTrigger
  - As new card scrolls into view:
    - Card underneath scales to 0.9
    - Blur filter increases to 20px
    - Opacity fades to 0.5

```tsx
// GSAP ScrollTrigger pattern
gsap.to(card, {
  scale: 0.9,
  filter: "blur(20px)",
  opacity: 0.5,
  scrollTrigger: {
    trigger: nextCard,
    start: "top bottom",
    end: "top top",
    scrub: true
  }
});
```

**Artifacts** (adapt to brand):
- Rotating double-helix gear
- Scanning laser-grid
- Pulsing EKG waveform

### F. MEMBERSHIP & FOOTER

- Three-tier pricing grid
- Middle card ("Signature / Performance") "pops" with:
  - Moss background
  - Clay button
  - Subtle scale-up

- **Footer**: 
  - Deep Charcoal
  - `rounded-t-[4rem]`
  - High-end utility links
  - "System Operational" status indicator with pulsing green dot

---

## 3. TECHNICAL REQUIREMENTS

### Tech Stack

- React 19
- Tailwind CSS
- GSAP 3 (with ScrollTrigger)
- Lucide React

### Animation Lifecycle

```tsx
// Use gsap.context() within useEffect for clean mounting/unmounting
useEffect(() => {
  const ctx = gsap.context(() => {
    // All GSAP animations here
    gsap.from(".hero-text", {
      y: 100,
      opacity: 0,
      duration: 1,
      stagger: 0.2
    });
  }, componentRef);
  
  return () => ctx.revert(); // Cleanup
}, []);
```

### Micro-Interactions

- **Buttons**: "Magnetic" feel (subtle scale-up on hover)
- **Color transitions**: Use `overflow-hidden` with sliding background layer

```tsx
// Button pattern
className="relative overflow-hidden group"
// Background slides in on hover
className="absolute inset-0 bg-[#CC5833] translate-y-full group-hover:translate-y-0 transition-transform duration-300"
```

### Code Quality

- No placeholders
- Use real Unsplash image URLs or generated images via T2I-Studio-Premium
- Dashboard elements must feel like functional software, not static layouts

---

## 4. EXECUTION DIRECTIVE

> "Do not build a website; build a digital instrument. Every scroll should feel intentional, every animation should feel weighted and professional. Eradicate all generic AI patterns."

### Quality Checklist

- [ ] Noise overlay implemented globally
- [ ] Navbar morphs on scroll
- [ ] Hero has cinematic depth with gradient overlay
- [ ] Feature cards are interactive artifacts, not static boxes
- [ ] Philosophy section uses split-text reveals
- [ ] Protocol cards stack with proper ScrollTrigger effects
- [ ] Pricing middle tier pops appropriately
- [ ] Footer has operational status indicator
- [ ] All animations use gsap.context() for cleanup
- [ ] Buttons have magnetic hover states
- [ ] Typography hierarchy creates drama
- [ ] No flat gradients—texture throughout

---

## 5. IMAGE GENERATION PROMPTS

When using T2I-Studio-Premium skill, use these prompt templates:

### Hero Background
```
Cinematic misty forest, moody atmosphere, dark green moss tones, fog rolling through ancient trees, ethereal morning light, high contrast shadows, 8k quality, editorial photography style
```

### Philosophy Background
```
Organic texture, microscopic cellular structure, abstract biological patterns, dark charcoal tones, subtle depth, scientific editorial aesthetic, high detail
```

### Protocol Backgrounds
```
Abstract geometric patterns, DNA helix visualization, medical technology aesthetic, dark sophisticated background with subtle glow, premium healthcare branding
```

---

## Usage

When user requests a cinematic/premium landing page:

1. Ask for BRAND_NAME and PRODUCT_CATEGORY if not provided
2. Generate required images using T2I-Studio-Premium skill
3. Implement full component architecture
4. Ensure all GSAP animations use proper cleanup
5. Verify micro-interactions feel premium
6. Check against quality checklist before completion
