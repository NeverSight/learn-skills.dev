---
name: modern-frontend-design
description: >
  How to design and build modern, premium-quality frontend interfaces that look like high-end SaaS
  products, modern AI tools, and award-winning design websites — not generic templates or outdated
  layouts. Use this skill whenever the user asks you to build a frontend, create a landing page,
  design a dashboard, scaffold a web app UI, build a SaaS interface, create a portfolio site, or
  produce any kind of user-facing web interface. Also use it when the user says things like "make
  it look modern", "build me a beautiful UI", "create a homepage for my app", "design a pricing
  page", or mentions anything related to frontend design, UI/UX, component architecture, or
  responsive web layouts — even if they don't explicitly say "frontend" or "design".
version: "1.0.0"
author: deveshpunjabi
tags:
  - frontend
  - design
  - ui-ux
  - landing-page
  - dashboard
  - web-design
  - tailwind
  - nextjs
  - react
  - saas
---

# Modern Frontend Design

You are not just writing code. You are a senior frontend developer, a UI/UX designer, a product designer, and a visual design strategist — all at once. Your mission is to transform any user prompt, idea, or product concept into a visually stunning, modern, premium-quality website or web application.

Why this matters: most AI-generated frontends look generic, use dated patterns, and ignore the product context entirely. The result should resemble high-end SaaS products, modern AI tools, and award-winning design websites. A fintech dashboard should feel different from a creator platform. A cybersecurity tool should feel different from a social app. The design must serve the product.

## Design Philosophy — The Premium Standard

The difference between a forgettable UI and a premium one is taste, restraint, and invisible details:

- **Restraint over excess.** Fewer colors, fewer fonts, fewer gimmicks. Every element earns its place. If a gradient doesn't serve the brand, remove it. If a shadow doesn't create hierarchy, it's noise.
- **Rhythm and proportion.** Professional interfaces feel musical — consistent spacing intervals, proportional font sizes, balanced whitespace. The eye flows smoothly without jarring jumps or cramped sections.
- **Contextual authenticity.** A fintech dashboard should feel like Bloomberg meets Linear. A creative portfolio should feel like a gallery opening. The design must inhabit its category so completely that users immediately sense "this is a serious product."
- **Emotional first impression.** Users form opinions within 50 milliseconds. Hero section, color palette, typography weight — all contribute to an instant reaction: "This is trustworthy. This is modern. This is worth my time."
- **The startup test.** Before delivering, ask: "Would a well-funded startup with a full design team ship this?" If no — iterate.

Follow this 10-step **Atom of Thought Design Process** before and during code generation. Each step builds on the last — skipping steps is how generic UIs happen.

---

## Step 1 — Understand the Product

Before writing a single line of code, deeply understand what you're building and for whom.

Analyze the user's prompt and extract:

- **Product type**: SaaS tool, landing page, dashboard, marketplace, portfolio, AI product, mobile-first web app, admin panel
- **Target audience**: developers, enterprise teams, consumers, creators, students, executives
- **Core value proposition**: what is the single most important thing this product communicates?
- **Main conversion goal**: sign up, book a demo, start free trial, explore features, purchase

Ask internally: *What is the website trying to communicate? What is the user's main action?*

### Niche-Aware Design Adaptation

Each niche has conventions that users expect. Violating them feels jarring; following them builds instant trust.

| Niche | Design Direction |
|-------|-----------------|
| AI / ML tools | Dark themes, glowing accents, futuristic gradients, clean data viz |
| Developer tools | Monospace accents, high-contrast, code-block styling, minimal chrome |
| Fintech | Trust-heavy, clean whites/blues, data-dense but organized, professional typography |
| Social platforms | Vibrant colors, rounded shapes, avatar-centric, card-based feeds |
| Cybersecurity | Dark UI, terminal aesthetics, status indicators, alert-driven layouts |
| Creative agencies | Bold typography, warm tones, media-rich, gallery layouts, personality-forward |
| SaaS dashboards | Sidebar navigation, metric cards, tables, clean neutral palettes |
| E-commerce | Product grid focus, prominent CTAs, trust badges, review integration |
| Health / Wellness | Soft colors, generous whitespace, calming gradients, accessible fonts |
| Education | Structured layouts, progress indicators, readable typography, friendly colors |
| Startups / Landing pages | Hero-driven, social proof, feature grids, pricing, strong CTAs |
| Consulting / B2B | Authority-driven, dark premium backgrounds, numbered value props, client logos |

Blend conventions when the product crosses niches.

---

## Step 2 — Visual Inspiration Research

Before designing, study modern web design patterns mentally. Reference inspiration from:

- Awwwards, Dribbble, Behance, Pinterest (for layout and visual patterns)
- Best-in-class products: Vercel, Linear, Raycast, Stripe, Notion, Arc Browser
- Modern AI product pages: dark gradients, planet/globe visuals, glowing highlights

Analyze these key elements from premium reference designs:

- **Hero layouts**: large bold typography with gradient or italic accent words, floating badges/labels, prominent CTA buttons with glow effects
- **Typography hierarchy**: display-size headlines that demand attention, smaller muted subheadlines, mixed font weights (regular + italic, light + bold)
- **Color palettes**: deep dark backgrounds (navy #0a0a1a, near-black #050510), blue/purple accent systems, warm copper/gold alternatives for agencies
- **Gradient and glow effects**: subtle radial glows behind heroes, gradient text, soft light bleeds on background
- **Card design**: glassmorphism (backdrop-blur + translucent borders), dark cards with subtle 1px borders, numbered feature cards
- **Spacing**: generous padding between sections (96–128px), intentional breathing room between elements
- **Social proof**: logo bars with grayscale client logos, avatar stacks, "Trusted by X+ teams" badges
- **Section flow**: hero → why/about → features/services → how it works → pricing → CTA → footer

### Premium Design Qualities to Emulate

These qualities appear consistently across high-end modern interfaces:

1. **Dark futuristic gradient backgrounds** — deep navy to near-black with subtle radial color bleeds
2. **Glowing highlight effects** — soft, refined accent glows on key elements (not garish neon)
3. **Minimal premium layouts** — fewer elements, more impact, strong visual focus
4. **Bold hero typography** — 48–72px display text with mixed weights and italic accents
5. **Glassmorphism cards** — `backdrop-filter: blur(12px)`, rgba backgrounds, subtle light borders
6. **Smooth visual flow** — clear reading path from top to bottom through every section
7. **Floating UI elements** — decorative badges, labels, dots, subtle grid patterns for depth
8. **Earth/globe/planet visuals** — popular in AI/SaaS heroes for a sense of scale and innovation

Use these only as inspiration — adapt them to the product's personality, never copy templates directly.

### 2025–2026 Design Trends to Incorporate

- **Bento grid layouts** — asymmetric grids where cards have different sizes and visual weights, creating editorial-feeling compositions (see: Apple, Linear, Vercel)
- **Animated gradient meshes** — smooth organic color transitions as backgrounds, replacing flat solid colors
- **Scroll-driven storytelling** — sections that transform, parallax, or reveal content based on scroll position rather than static page loads
- **Mono-accent palettes** — one strong accent color used surgically, everything else in neutrals — produces a striking, confident look
- **Oversized typography heroes** — headline text at 80–120px with tight line-height and negative letter-spacing, creating immediate visual authority
- **Subtle grain/noise textures** — slight grain overlay on backgrounds adds warmth and tactile quality to flat digital surfaces
- **Interactive cursor effects** — custom cursors, hover spotlights, magnetic buttons that add a layer of delight
- **Dark mode by default** — most premium SaaS/AI products now default to dark themes with carefully managed contrast

---

## Step 3 — Visual System Planning

Define the complete visual identity before building. This is what separates a UI that feels "designed" from one that feels "coded."

### Typography

Pick 2 fonts maximum (1 for headings, 1 for body). Define sizes for display, h1–h4, body, small, caption. Use `clamp()` for fluid sizing.

Strong modern pairings:
- **Inter + Inter** — clean, neutral, Swiss-style (most versatile)
- **Cal Sans + Inter** — modern SaaS product feel
- **Space Grotesk + DM Sans** — tech / developer tools
- **Playfair Display + Source Sans 3** — editorial, luxury, agencies
- **Clash Display + Satoshi** — bold, creative, startup energy

### Color Palette

Construct a complete palette — not random colors:

- **Primary**: main brand color (used sparingly for CTAs and accents only)
- **Primary gradient**: pair of colors for gradient effects (e.g., blue-500 → purple-500)
- **Neutral scale**: 50 through 950 for backgrounds, borders, and text
- **Semantic colors**: success (green), warning (amber), error (red), info (blue)

Dark theme rules (for AI, SaaS, cybersecurity niches):
- Use gray-900/950 for backgrounds, never pure black (#000)
- Elevate surfaces with slightly lighter backgrounds, not stronger shadows
- Reduce primary saturation by 10-20% to avoid eye strain
- Ensure 4.5:1 contrast for body text, 3:1 for large text

### Spacing, Radius, and Shadows

- **Spacing scale** (4px base): 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128
- **Border radius**: sharp (2–4px) for fintech/enterprise, soft (8–12px) for SaaS, rounded (16–24px) for consumer — stay consistent throughout
- **Shadows**: 3 levels (cards, dropdowns, modals), tinted toward primary hue for a premium feel

For complete reference tables, font scales, CSS recipes, and detailed examples, see `references/design-systems.md`.

---

## Step 4 — Layout Architecture

Design the page structure before coding. Every section should guide the user toward the conversion goal.

### Landing Page Architecture

```
Navigation (logo + links + primary CTA button)
↓
Hero (display headline + subheadline + CTA buttons + visual/demo/globe)
↓
Social Proof (logo bar, stats, or "Trusted by X+ teams")
↓
Why / About (value proposition statement — 2-3 crisp sentences)
↓
Features or Services (grid of cards, alternating sections, or numbered cards)
↓
How It Works (numbered steps with icons or visuals)
↓
Product Demo / Screenshots / Interactive Preview
↓
Testimonials or Case Studies
↓
Pricing (2-3 tier glassmorphism cards with highlighted recommended plan)
↓
Final CTA (strong headline + prominent button)
↓
Footer (links, social icons, copyright)
```

### Dashboard Architecture

```
Top Nav (search bar, notifications bell, user avatar dropdown)
├── Sidebar (icon + label navigation, section grouping, collapsible)
└── Main Content Area
    ├── Summary Cards (key metrics with sparklines or trend arrows)
    ├── Primary Data View (charts, tables, or data feeds)
    └── Secondary Panels (filters, activity logs, detail views)
```

Adapt the structure to the product — never force every project into the same layout.

---

## Step 5 — UI Component System

Build modular, reusable components. Each component should do one thing well, accept props for content/variants (not hard-coded text), handle its own responsive behavior, and use semantic HTML with ARIA attributes.

### Component Organization

```
components/
├── layout/       → Navbar, Footer, Sidebar, Container
├── ui/           → Button, Card, GlassCard, Badge, Input, Modal, Toggle
├── sections/     → Hero, Features, Pricing, Testimonials, CTA, HowItWorks
└── data/         → DataTable, MetricCard, Chart, StatCard
```

### Component Quality Standards

- Consistent spacing, typography, color usage, and alignment across every component
- Variant-driven props: `<Button variant="primary" size="lg">` — not separate component files per variant
- Glassmorphism card recipe: `backdrop-filter: blur(12px)`, `background: rgba(255,255,255,0.05)`, `border: 1px solid rgba(255,255,255,0.1)`
- Interactive elements: visible hover/focus states, smooth 200ms transitions, proper cursor styles

---

## Step 6 — Modern Interaction Design

Add subtle motion and interaction. Animations make the UI feel alive and premium — they must be smooth and purposeful, never excessive.

### Essential Interactions

- **Hover effects**: scale transforms (1.02–1.05), color shifts, glow intensification on cards and buttons
- **Smooth transitions**: 150–300ms ease-out on all state changes (color, shadow, transform)
- **Micro-animations**: button press feedback, icon rotations, progress indicators, toggle switches
- **Scroll reveals**: elements fading/sliding in as they enter the viewport (translate 20–30px + opacity 0→1, 400–600ms)
- **Staggered reveals**: children in grids/lists animate with 50–100ms stagger delay

### Animation Libraries

| Library | Best For |
|---------|---------|
| Framer Motion | React projects — declarative, performant, page transitions |
| GSAP | Complex timelines, scroll-triggered sequences, SVG animation |
| CSS transitions | Simple hovers and state changes (no library needed) |
| Intersection Observer | Scroll-triggered class toggling with vanilla JS |

### Animation Rules

- Use `transform` and `opacity` for GPU-accelerated performance
- Respect `prefers-reduced-motion` — accessibility is non-negotiable
- Entrance animations should feel natural: slight upward slide + fade, not dramatic fly-ins
- Interactive feedback should be instant (< 100ms) — delays feel broken

---

## Step 7 — Technology Stack

Prefer modern technologies that enable rapid, high-quality development:

| Layer | Recommended | Why |
|-------|------------|-----|
| Framework | React / Next.js | Component model, ecosystem, SSR/RSC support |
| Styling | Tailwind CSS | Rapid iteration, design-system-friendly, responsive utilities |
| Components | shadcn/ui + Radix UI | Accessible, unstyled primitives you can theme to any design |
| Animation | Framer Motion | Declarative, performant, micro-interactions and page transitions |
| Language | TypeScript | Type safety, better DX, self-documenting interfaces |
| Icons | Lucide React | Clean, consistent, extensive icon set that matches modern UIs |

If the user specifies a different stack (Vue, Svelte, plain HTML/CSS/JS), respect that choice — the design principles are tool-agnostic. For simpler projects (single page, portfolio), plain HTML + CSS + vanilla JS is valid. Don't over-engineer.

### Project Structure

```
/app or /pages   → routes and page components
/components      → reusable UI components (layout/, ui/, sections/, data/)
/styles          → global styles, theme configuration, CSS variables
/utils           → helpers, constants, type definitions
/public          → static assets (images, fonts, icons)
```

---

## Step 8 — Backend Awareness

Design the frontend with real data integration in mind — not static mock layouts that break when connected to APIs.

- **Loading states**: skeleton loaders (pulsing placeholder shapes), never bare spinners
- **Error states**: meaningful error messages with retry actions — never blank screens
- **Empty states**: friendly messages with CTAs ("No projects yet — create your first one")
- **Form validation**: inline error messages on blur/submit with clear visual indicators
- **Authentication**: login/signup flows, user menus, protected route handling
- **Dynamic content**: every component accepts data via props/API — no hard-coded strings
- **Optimistic UI**: update the interface immediately on action, roll back gracefully on failure

Use realistic placeholder data during development — real-sounding names, plausible numbers, proper-length text. "Lorem ipsum" and "Test 123" make it impossible to judge the real design quality.

---

## Step 9 — Responsive System

Every interface must work perfectly on desktop, tablet, and mobile. This is a core requirement, never an afterthought.

### Breakpoints (Tailwind defaults)

| Token | Width | Target |
|-------|-------|--------|
| `sm` | 640px | Large phones (landscape) |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large displays |

### Responsive Patterns

- Grid columns: 4 → 2 → 1 as viewport shrinks
- Navigation: full menu → hamburger/drawer below 768px
- Typography: display text scales from 72px → 48px → 32px using `clamp()`
- Side-by-side layouts: stack vertically on mobile
- Touch targets: minimum 44×44px on mobile devices
- Section padding: 128px → 80px → 48px (desktop → tablet → mobile)
- Card layouts: horizontal cards → vertical stacked cards
- Max content width: 1200–1440px with 16px (mobile) → 32px (desktop) side padding

Design mobile-first when sensible. Test the mental model at 375px, 768px, and 1440px.

---

## Step 10 — Visual Quality Validation

Before finalizing, run this checklist. If any answer is "no" — go back and fix it.

**Typography**
- [ ] Type hierarchy is strong (display > h1 > h2 > body are clearly distinct)
- [ ] Headings use negative letter-spacing (-0.02em to -0.04em)
- [ ] Body text is 16–18px with 1.5–1.7 line height
- [ ] Lines capped at 65–75 characters maximum width

**Spacing**
- [ ] Every spacing value comes from the defined scale (no arbitrary numbers)
- [ ] Sections have generous vertical padding (80–128px on desktop)
- [ ] Layout feels spacious and intentional, nothing cramped

**Color and Polish**
- [ ] Primary color used sparingly — CTAs and key accents only
- [ ] All text meets contrast ratios (4.5:1 body, 3:1 large)
- [ ] Gradients are subtle and purposeful (not garish or overwhelming)
- [ ] Interactive elements have hover/focus states with smooth transitions
- [ ] Shadows are colored/tinted, never pure black rgba(0,0,0,x)

**Overall Impression**
- [ ] The UI looks premium and modern — not like a generic template
- [ ] It resembles high-end SaaS products (Linear, Vercel, Stripe quality)
- [ ] The design serves this specific product's niche and audience
- [ ] A user would trust and respect this product based on UI alone

If the UI looks generic or outdated — redesign. The standard is award-winning quality.

---

## Step 11 — Final Automated Testing & Error Resolution (MANDATORY)

**This step is non-negotiable.** After the build is complete, the agent MUST run these automated checks and fix every issue found before declaring the task done. Do NOT skip this step. Do NOT hand back to the user with unresolved errors.

### 11.1 — Build Verification

Run the production build and capture all errors:

```bash
# Install dependencies (catch missing packages)
npm install

# Run TypeScript compiler — catch ALL type errors
npx tsc --noEmit

# Run the production build — catch build-time errors
npm run build
```

**If any command fails:**
1. Read the full error output
2. Fix every error in the source code
3. Re-run the failing command
4. Repeat until zero errors

### 11.2 — Lint & Code Quality

```bash
# Run ESLint — catch code quality issues
npx next lint

# Check for unused imports and variables
npx tsc --noEmit --noUnusedLocals --noUnusedParameters 2>&1 || true
```

Fix all lint errors. Warnings should be reviewed — fix if they indicate real problems.

### 11.3 — Runtime Smoke Test

```bash
# Start the dev server and verify it boots without crashing
npm run dev &
sleep 5

# Check if the server is responding
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
# Must return 200

# Kill the dev server
kill %1 2>/dev/null || true
```

If the server crashes on boot, read the terminal output, fix the error, and retry.

### 11.4 — Component-Level Error Scan

Check every component file for common issues:

| Check | What to Look For | Fix |
|-------|-----------------|-----|
| **Import errors** | Importing from non-existent files or packages | Add missing dependencies or fix import paths |
| **Type mismatches** | Props passed incorrectly between components | Align prop types with usage |
| **Missing keys** | `.map()` without `key` prop | Add unique `key` to mapped elements |
| **Hydration mismatches** | `window`/`document` used at top level in SSR | Wrap in `useEffect` or dynamic import with `ssr: false` |
| **Event handler types** | `onClick` handlers with wrong TypeScript types | Use `React.MouseEvent<HTMLElement>` |
| **Image optimization** | `<img>` tags instead of `next/image` | Replace with `<Image>` component |
| **Missing alt text** | Images without `alt` attributes | Add descriptive alt text |
| **Broken links** | Anchor tags pointing to non-existent routes | Fix `href` values or create missing pages |

### 11.5 — Cross-Page Navigation Test

If the site has multiple pages/routes:

```bash
# Check all routes return 200
for route in "/" "/about" "/pricing" "/contact"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000$route")
  echo "$route -> $status"
done
```

### 11.6 — Responsive & Accessibility Quick Check

| Check | Method | Fix |
|-------|--------|-----|
| **Mobile layout** | Verify no horizontal scrollbar at 375px | Fix overflow, use `overflow-x-hidden` on wrapper |
| **Touch targets** | All buttons/links ≥ 44×44px on mobile | Increase padding or min-height/width |
| **Focus states** | Tab through all interactive elements | Add `focus:ring` or `focus-visible` styles |
| **Color contrast** | Run `npx axe` or Lighthouse accessibility audit | Adjust text/background color pairs |
| **Heading order** | h1 → h2 → h3, no skipped levels | Fix heading hierarchy |

### 11.7 — Final Error Resolution Loop

```
WHILE errors exist:
  1. Run: npm run build
  2. IF build fails → read error → fix → GOTO 1
  3. Run: npx next lint
  4. IF lint fails → read error → fix → GOTO 1
  5. Run: npm run dev (verify server boots)
  6. IF server crashes → read error → fix → GOTO 1
  7. All clear → EXIT loop
```

**The agent MUST NOT declare the task complete until:**
- [ ] `npm run build` exits with code 0
- [ ] `npx next lint` passes (no errors)
- [ ] `npm run dev` boots without crashing
- [ ] No TypeScript errors (`npx tsc --noEmit` passes)
- [ ] All pages render without console errors
- [ ] No hydration mismatch warnings
- [ ] Mobile layout has no overflow issues

> **Rule: If you generated the code, you own the errors. Fix them before finishing.**

---

## Final Output Requirements

Deliver:

- **Modern premium UI** with visual polish and attention to detail — the kind of site that makes people say "this looks expensive"
- **Modular component architecture** — reusable, prop-driven, well-typed
- **Clean project structure** — /components, /sections, /styles, /utils
- **Fully responsive design** — beautiful on mobile, tablet, and desktop
- **Production-ready code** — TypeScript, proper types, clean patterns
- **Visually impressive layout** that clearly communicates the product's value
- **Realistic content** — believable copy, realistic data, proper-length text (never lorem ipsum)
- **Smooth interactions** — hover effects, scroll reveals, micro-animations that feel alive

Include a brief summary of design decisions: color palette rationale, typography choices, layout strategy, and where to customize.

### Cross-Agent Compatibility

This skill works with any AI coding agent that supports Markdown-based skill files:

| Agent | Installation |
|-------|-------------|
| Claude Code | `npx skills add deveshpunjabi/modern-frontend-skill` |
| Cursor | Copy to `.cursor/skills/` |
| Windsurf | Copy to `.windsurf/skills/` |
| Cline | Copy to `.cline/skills/` |
| Codex | Copy to `.codex/skills/` |
| Aider | Reference in `.aider.conf` |
| Any agent | Copy SKILL.md to the agent's skill/instruction directory |

The skill is a standalone Markdown file with optional reference documents — no runtime dependencies, no API keys, no build steps.

---

## Anti-Patterns — What to Avoid

These are the hallmarks of AI-generated UIs that look "off." Understanding why they fail helps you avoid them:

| Anti-Pattern | What Goes Wrong | Fix |
|-------------|----------------|-----|
| **Rainbow soup** | Too many unrelated colors | Stick to your palette — primary, neutral, 1-2 accents max |
| **Wall of cards** | Identical cards in grid, no visual hierarchy | Vary sizes, highlight featured items, use visual weight |
| **Giant hero, empty page** | Massive hero, thin underwhelming content below | Maintain proportional section weight throughout the page |
| **Button overload** | Multiple CTAs competing for attention | One primary + one secondary CTA per section maximum |
| **Fake depth** | Shadows and gradients on everything | Use depth purposefully to create clear visual hierarchy |
| **Stock photo blanket** | Generic photos unrelated to the product | Use illustrations, product screenshots, or abstract visuals |
| **Inconsistent radius** | Mixing sharp + fully rounded randomly | Pick one radius language and commit to it throughout |
| **Bootstrap syndrome** | Default template look with swapped colors | Design from scratch using the visual system you defined |
| **Typography neglect** | Same size/weight for all text elements | Build clear hierarchy: display, heading, subhead, body, caption |
| **Spacing chaos** | Random margins and padding, no system | Every value from the spacing scale — no arbitrary numbers |
| **The gray wasteland** | Everything is gray text on gray background | Use contrast deliberately — important content gets high contrast |
| **Lorem ipsum laziness** | Placeholder text that makes design unjudgeable | Write realistic copy that matches the product's voice and length |
| **Navbar graveyard** | Navigation with 8+ links crammed in one row | Group into sections, add dropdowns, max 5-6 primary nav items |
| **The flat page** | No visual rhythm — sections blend into each other | Alternate backgrounds, use dividers, vary section layouts |

### The "Premium or Redo" Test

After building, view the full page and honestly evaluate:

1. **Screenshot test** — Take a screenshot and put it next to Linear.app, Vercel.com, or Stripe.com. Does yours look like it belongs in the same category?
2. **Squint test** — Squint at the page. Can you see clear visual hierarchy? Are the important elements dominant?
3. **3-second test** — Show it to someone for 3 seconds. Can they tell what the product does and where to click?

If the answer to any of these is "no" — the design needs work before delivery.
