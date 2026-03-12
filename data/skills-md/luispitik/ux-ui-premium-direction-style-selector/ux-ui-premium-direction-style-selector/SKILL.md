---
name: ux-ui-premium-direction-style-selector
description: >
  Deploy 8 radically different visual direction demos for a website or webapp project.
  Creates self-contained Next.js pages under /demo/ with distinct identities (typography,
  color palette, layout, animation, accessibility) so the user can compare and choose.
  After selection, generates production-ready theme tokens, Tailwind config, CSS variables,
  and base components matching the chosen direction.
  Use when: starting a new web project, redesigning a site, choosing visual direction,
  the user says "style selector", "choose styles", "visual alternatives", "pick a design
  direction", or wants to compare different aesthetic approaches before committing to one.
  Works with Next.js + Tailwind CSS projects (landing pages, web apps, SaaS, dashboards).
---

# Style Selector

Generate 8 self-contained visual direction demo pages for comparison, then apply the chosen direction to the project.

## Workflow

### 1. Gather project context

Before generating demos, collect:
- **Project type** (landing page, web app, SaaS, dashboard, e-commerce, portfolio)
- **Business type** (consulting, SaaS, agency, e-commerce, portfolio, etc.)
- **Business name and tagline**
- **Key stats** (numbers to display -- users, clients, years, etc.)
- **Services/products** (3-4 items with short descriptions)
- **CTA** (primary call to action -- book a call, sign up, buy, etc.)
- **Language** (Spanish, English, etc.)
- **Tone** (corporate, friendly, luxury, technical, rebellious, playful, etc.)

If the project already has content (existing pages, spec docs, CLAUDE.md), extract this context automatically without asking.

### 2. Verify project setup

Confirm the project uses Next.js App Router + Tailwind CSS. Check:
- `src/app/` or `app/` directory exists
- `tailwind.config.ts` or `tailwind.config.js` exists
- `globals.css` has `@tailwind base/components/utilities` or `@import "tailwindcss"` directives

**Critical**: Ensure globals.css custom styles are wrapped in `@layer base { }`. Unlayered CSS overrides Tailwind utility classes due to CSS cascade layers. If `* { margin: 0; padding: 0; }` or `body { ... }` exist outside a `@layer`, wrap them in `@layer base { }`.

### 3. Create demo infrastructure

Create these files:

**Demo layout** (`src/app/demo/layout.tsx`):
```tsx
'use client'
export default function DemoLayout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 99999, overflow: 'auto', background: '#ffffff', fontFamily: 'system-ui, sans-serif', color: '#000' }}>
      <style>{\`body { overflow: hidden !important; }\`}</style>
      {children}
    </div>
  )
}
```

**Demo index page** (`src/app/demo/page.tsx`): A 'use client' page listing all 8 directions as clickable cards. Each card shows: direction name, subtitle/reference, description, and 4 color swatches. Dark background (#0a0a0a) for the index page.

### 4. Select directions based on project type

Not all 8 directions suit every project type. Pre-select 5 that best match:

| Project Type | Recommended 5 | Skip |
|-------------|---------------|------|
| Landing page (general) | Editorial, Minimal, Luxury, Corporate, Kinfolk | — |
| SaaS / Web app | Minimal, Corporate, Playful, Brutalist, Retro | Luxury, Kinfolk, Editorial |
| E-commerce | Minimal, Luxury, Corporate, Playful, Kinfolk | Brutalist, Retro, Editorial |
| Dashboard | Minimal, Corporate, Playful, Retro, Brutalist | Luxury, Kinfolk, Editorial |
| Portfolio / Creative | Editorial, Luxury, Kinfolk, Brutalist, Playful | Minimal, Corporate, Retro |
| Developer tools | Minimal, Brutalist, Retro, Playful, Corporate | Luxury, Kinfolk, Editorial |

If the user says "show all 8", generate all 8 regardless. Otherwise use the recommended 5 for their project type. Always ask if they want to see all 8 after showing the 5.

### 5. Generate demo pages

See `references/directions.md` for the complete spec of each visual direction, including palette, typography, layout, animation, accessibility, and mobile specs.

Each demo page must be:
- **Self-contained** (no shared component imports -- only `next/link` and `next/font/google`)
- **Mobile-first responsive** (design for 375px first, enhance with Tailwind breakpoints)
- **Complete** (skip-link + nav + hero + storytelling + stats + services + CTA + footer)
- **Unique fonts** via `next/font/google` with CSS variables
- **Custom colors** via inline `style` attributes (not relying on project's Tailwind theme)
- **Animated** per direction specs (scroll reveal, hover effects, micro-interactions)
- **Accessible** (WCAG AA contrast, focus-visible outlines, 44px+ touch targets, skip link)
- **Motion-safe** (respect `prefers-reduced-motion` -- disable all animations/transitions)
- **Back link** to `/demo` in the footer

Pages that use event handlers (onMouseEnter, useState, useEffect) MUST have `'use client'` at the top. Pages with `'use client'` MUST NOT export `metadata`.

Generate all pages in parallel using Agent tool for speed.

### 6. Adapt copy to project

For each direction, rewrite copy to match the project's context:
- Headline adapted to the business and tone direction
- Storytelling adapted to the founder/company narrative
- Stats using real project numbers
- Services listing real offerings
- CTA pointing to real contact mechanism

**Copy quality rules** (avoid AI-sounding text):
- Use imperfect, conversational sentences
- Include specific details, not generic buzzwords
- Short paragraphs, varied rhythm
- Opinions and personality over corporate speak
- Questions to the reader
- First person where appropriate

**Copy tone per direction** (see `references/directions.md` for full table):
- Editorial: authoritative, measured
- Minimal: direct, stripped
- Luxury: intimate, refined
- Corporate: confident, structured
- Kinfolk: thoughtful, quiet
- Brutalist: blunt, irreverent
- Playful: energetic, modern
- Retro: dry, technical, developer humor

### 7. Build and verify

Run `npx next build` to confirm all demo routes compile. Fix any errors:
- Missing `'use client'` for pages with event handlers
- `metadata` export in client components (remove it)
- Unused variables (remove them)

Start dev server and verify:
1. Take screenshots of each demo at **desktop** (1280px)
2. Take screenshots at **mobile** (375px) — resize viewport
3. Check that:
   - No horizontal overflow on mobile
   - All text readable (16px+ body on mobile)
   - All buttons tappable (44px+ height)
   - Nav is functional on both sizes
   - Animations play (and stop with reduced-motion)
   - Focus outlines visible when tabbing
   - Skip link works

### 8. Present to user

Show the user the demo index URL (`/demo`) and a summary table of all directions with their visual identity. Include:

| Direction | Mood | Key Feature | Best For |
|-----------|------|-------------|----------|
| Editorial | Intellectual authority | Serif typography, gold accents | Consulting, media, thought leadership |
| Minimal | Functional clarity | Maximum restraint, red CTAs only | SaaS, tools, developer products |
| Luxury | Warm intimacy | Dark bg, copper accents, slow motion | Premium services, hospitality, beauty |
| Corporate | Confident authority | Navy/white rhythm, purple accents | Enterprise, B2B, consulting |
| Kinfolk | Quiet sophistication | Narrow columns, olive accents, stillness | Creative, wellness, editorial |
| Brutalist | Raw irreverence | Hard shadows, mono uppercase, thick borders | Startups, developer tools, creative agencies |
| Playful | Modern energy | Gradient text, glass cards, living gradients | SaaS, modern startups, tech |
| Retro | Hacker credibility | Terminal aesthetic, typewriter, green-on-black | Developer tools, CLI products, tech |

Ask which direction they prefer or if they want to mix elements from multiple directions.

### 9. Apply direction (post-selection)

Once the user chooses a direction, apply it to the project:

#### 9a. Generate Tailwind theme tokens

Create/update `tailwind.config.ts` with the chosen direction's design tokens:

```typescript
// Example for "Luxury Dark Warm" direction
const config = {
  theme: {
    extend: {
      colors: {
        background: '#171614',
        foreground: '#F0EBE1',
        accent: '#C4956A',
        muted: '#8A8174',
        card: '#1E1D1A',
        border: 'rgba(196,149,106,0.3)',
      },
      fontFamily: {
        display: ['var(--font-cormorant)', 'serif'],
        body: ['var(--font-outfit)', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 800ms ease-out',
        'slide-up': 'slideUp 800ms ease-out',
      },
      keyframes: {
        fadeIn: { '0%': { opacity: '0' }, '100%': { opacity: '1' } },
        slideUp: { '0%': { transform: 'translateY(20px)', opacity: '0' }, '100%': { transform: 'translateY(0)', opacity: '1' } },
      },
    },
  },
}
```

#### 9b. Generate CSS variables

Add to `globals.css`:

```css
@layer base {
  :root {
    --background: <bg-color>;
    --foreground: <text-color>;
    --accent: <accent-color>;
    --muted: <secondary-color>;
    --card: <card-bg>;
    --border: <border-color>;
    --focus-ring: <focus-color>;

    /* Animation tokens */
    --reveal-y: <direction-value>;
    --reveal-duration: <direction-value>;
    --reveal-stagger: <direction-value>;
    --reveal-easing: <direction-value>;
  }

  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
}
```

#### 9c. Generate base components

Create reusable components that encode the chosen direction's patterns:

**`src/components/ui/Button.tsx`** — Primary and secondary variants matching direction style:
- Editorial: gold-bordered, serif text
- Minimal: red bg (primary), text link with arrow (secondary)
- Luxury: copper bg, light weight text
- Corporate: purple filled + outline variants
- Kinfolk: olive outline, minimal
- Brutalist: black border + hard shadow, uppercase mono
- Playful: gradient border, glass effect
- Retro: terminal command style, mono text

**`src/components/ui/Card.tsx`** — Card component matching direction:
- Editorial: no card, just gold left border
- Minimal: border-b divider, no card bg
- Luxury: dark raised bg, copper top border
- Corporate: light gray bg, slate border
- Kinfolk: no card, just text
- Brutalist: 3px black border, hard shadow
- Playful: glass morphism (white 5%, backdrop-blur)
- Retro: green/30% border, terminal bg

**`src/components/ui/Section.tsx`** — Section wrapper with direction-appropriate spacing, dividers, and scroll-reveal animation.

**`src/components/ui/Container.tsx`** — Max-width container matching direction's content width.

**`src/components/ui/Nav.tsx`** — Navigation with direction-appropriate mobile pattern.

**`src/components/ScrollReveal.tsx`** — Reusable scroll reveal hook/component using IntersectionObserver.

#### 9d. Generate font setup

Add to root layout (`src/app/layout.tsx` or `src/app/demo/layout.tsx`):

```tsx
import { FontDisplay, FontBody } from 'next/font/google'

const fontDisplay = FontDisplay({
  subsets: ['latin'],
  variable: '--font-display',
  display: 'swap',
})

const fontBody = FontBody({
  subsets: ['latin'],
  variable: '--font-body',
  display: 'swap',
})

// Add to <html> or <body> className:
// `${fontDisplay.variable} ${fontBody.variable}`
```

#### 9e. Clean up

- Remove `/demo/` directory and all demo pages
- Remove demo layout
- Confirm `npx next build` passes after applying theme

### 10. Verify applied direction

After applying the chosen direction:
1. Start dev server
2. Navigate to the main page
3. Take screenshot at desktop and mobile
4. Verify:
   - Colors match chosen direction
   - Fonts load correctly
   - Animations work (and respect reduced-motion)
   - Mobile layout is correct
   - All components render properly
5. Share screenshots with user for final approval

## The 8 Directions

| ID | Name | Reference | Bg | Accent | Fonts |
|----|------|-----------|-----|--------|-------|
| editorial | Editorial Serif | The Economist | Cream #FAFAF5 | Gold #B8860B | Playfair Display + Source Serif 4 |
| minimal | Swiss Minimal | Dieter Rams | White #FFFFFF | Red #D42B2B | Space Grotesk + Inter |
| luxury | Luxury Dark Warm | Aesop | Charcoal #171614 | Copper #C4956A | Cormorant Garamond + Outfit |
| corporate | Corporate Bold | Accenture | White/Navy #0F1923 | Purple #5B21B6 | Plus Jakarta Sans |
| kinfolk | Understated Elegance | Kinfolk | Bone #F5F2ED | Olive #6B705C | Libre Baskerville + Karla |
| brutalist | Neo-Brutalist | Gumroad | Off-white #FFFDF7 | Yellow #FFE600 + Pink #FF3366 | Space Mono + DM Sans |
| playful | Playful Gradient | Linear/Stripe | Near-black #0C0C0C | Blue→Violet→Pink gradient | Satoshi/Inter |
| retro | Retro Terminal | Stripe CLI | Terminal black #0D1117 | Green #00FF41 + Amber #FFB000 | JetBrains Mono |

For detailed specs (full palette, layout, animation, accessibility, mobile), read `references/directions.md`.

## Direction Selection Guide

| If the user wants... | Recommend |
|---------------------|-----------|
| "Professional but not boring" | Editorial or Corporate |
| "Clean and modern" | Minimal or Playful |
| "Premium / high-end" | Luxury or Kinfolk |
| "Fun / startup vibe" | Brutalist or Playful |
| "Developer audience" | Retro or Minimal |
| "Something different / bold" | Brutalist or Retro |
| "Warm and personal" | Luxury or Kinfolk |
| "Data-driven / enterprise" | Corporate or Minimal |
| "Creative / artistic" | Kinfolk or Brutalist |
| "Tech / SaaS" | Playful or Retro |

## Project Type Adaptations

The common section structure (nav, hero, storytelling, stats, services, CTA, footer) works for landing pages. For other project types, adapt the demo structure:

### Web App / SaaS
Replace storytelling + stats with:
- **Feature showcase** — 3 key features with mock UI screenshots or illustrations
- **How it works** — 3-step flow (Sign up → Configure → Launch)
- **Pricing** — 3 tiers (Free, Pro, Enterprise) or simple pricing card
Keep: Nav, Hero, Services/Features, CTA, Footer

### Dashboard
Replace hero + storytelling with:
- **Dashboard preview** — Mock data visualization (charts placeholder, KPI cards)
- **Sidebar** — Navigation pattern preview
- **Data table** — Sample table with direction's styling
Keep: Nav (sidebar variant), Feature cards, CTA, Footer

### E-commerce
Replace storytelling with:
- **Product grid** — 4-6 product cards with image placeholders, price, CTA
- **Categories** — Category navigation
- **Trust signals** — Reviews, shipping info, guarantees
Keep: Nav (with cart icon), Hero (product-focused), CTA, Footer

### Portfolio
Replace services with:
- **Project grid** — 4-6 project cards with image, title, category
- **About section** — Bio with photo placeholder
- **Testimonials** — 2-3 client quotes
Keep: Nav, Hero (name-focused), Storytelling, CTA (hire me), Footer
