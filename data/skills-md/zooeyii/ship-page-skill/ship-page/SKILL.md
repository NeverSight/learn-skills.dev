---
name: ship-page
description: Create stunning, interactive landing pages for products, startups, and side projects — zero dependencies, single HTML file. Use this skill whenever the user wants to build a landing page, product page, launch page, marketing page, or any promotional web page for their app, tool, SaaS, open-source project, or personal brand. Also triggers when users say "I need a website for my product", "help me launch", "make a page for my app", or want to convert a README into a visual landing page. Works great for Product Hunt launches, GitHub project pages, and indie hacker ship days.
---

# Ship Page

Create interactive, animation-rich landing pages that run entirely in the browser as a single HTML file.

This skill helps non-designers ship professional product pages through visual exploration ("show, don't tell"), then generates production-quality landing pages with real interactivity — not static mockups.

## Core Principles

- **Zero Dependencies** — Single HTML file with inline CSS/JS. No npm, no build tools, no frameworks. A single HTML file will outlive any React project.
- **Show, Don't Tell** — People can't describe what they want, but they know it when they see it. Generate visual previews, let them pick.
- **Anti-AI-Slop** — No purple gradients on white. No generic SaaS templates. Every page should feel custom-crafted for the product.
- **Interactive by Default** — Landing pages aren't slides. They have scroll animations, hover states, data counters, particle effects, and micro-interactions that make visitors stay.
- **Ship-Ready** — Output works immediately. Drop the HTML file anywhere — GitHub Pages, Vercel, Netlify, or just open it in a browser.

## Detect Mode

- **Mode A: New Page** — Create from scratch. Go to Phase 1.
- **Mode B: README Conversion** — Turn a GitHub README or product description into a landing page. Extract content, then go to Phase 1 Step 2 (skip content questions, go straight to style).
- **Mode C: Enhancement** — Improve an existing HTML landing page. Read it, understand the structure, enhance while preserving content. Follow viewport and section density rules.

---

## Phase 1: Discovery

Understand the product and gather content. Ask ALL questions in a single AskUserQuestion call.

**Question 1 — Product Type** (header: "Product"):
What are you building?
Options: SaaS / Developer Tool / Mobile App / Open Source Project / Personal Brand / Other

**Question 2 — Content** (header: "Content"):
What should the page include?
Options: I'll paste my content / Pull from my README / Just describe it for me / I have a document

**Question 3 — Key Sections** (header: "Sections", multiSelect: true):
Which sections do you need?
Options: Hero with CTA / Features Grid / How It Works / Pricing / Testimonials / FAQ / Stats & Metrics / Newsletter Signup / GitHub Stars Badge

**Question 4 — Launch Target** (header: "Launch"):
Where will this page live?
Options: GitHub Pages / Standalone website / Product Hunt launch / Just exploring

If user provides content (README, description, document), proceed to:

### Step 1.1: Content Analysis

Parse the provided content and extract:
- Product name and one-line description
- Key features (aim for 3-6)
- Target audience signals
- Any metrics/numbers mentioned
- Call-to-action (what should visitors do?)

Confirm via AskUserQuestion (header: "Content Check"):
"Here's what I extracted — does this look right?"
Options: Looks good / Let me adjust

---

## Phase 2: Style Discovery

This is the "show, don't tell" phase. Most people can't articulate design preferences in words.

### Step 2.1: Vibe Selection

Ask via AskUserQuestion (header: "Vibe", multiSelect: true, max 2):
What feeling should visitors get?
Options: Futuristic & Tech / Clean & Minimal / Bold & Energetic / Dark & Premium / Playful & Creative / Corporate & Trust

### Step 2.2: Generate Style Previews

Based on vibe selection, generate **3 distinct single-section HTML previews** showing:
- Typography choices (heading + body font pairing)
- Color palette (background, text, accent, CTA)
- Hero section layout with the product name
- One micro-interaction or animation
- Overall atmosphere (background treatment, spacing)

Each preview should be a complete, working HTML file showing just the hero section styled three completely different ways. Save previews to `.ship-page/previews/`.

**Read `references/STYLE_PRESETS.md`** for curated preset definitions. Use presets as a FOUNDATION, then customize for the specific product.

Confirm via AskUserQuestion (header: "Pick Your Style"):
"Which direction resonates?"
Options: Style A / Style B / Style C / Mix elements (describe)

### Step 2.3: Direct Preset Selection (Alternative)

If user already knows what they want or says "just make it dark/minimal/tech":
- Read `references/STYLE_PRESETS.md`
- Match to nearest preset
- Skip preview generation, go to Phase 3

---

## Phase 3: Generate Landing Page

Generate the full landing page using content from Phase 1 and style from Phase 2.

### Structure Rules

Every landing page follows this architecture:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Fonts, CSS variables, all styles inline -->
  <!-- No external dependencies except Google Fonts + Font Awesome CDN -->
</head>
<body>
  <nav><!-- Sticky nav with product name + CTA --></nav>
  
  <section class="hero"><!-- Above the fold: headline, subheadline, CTA --></section>
  <section class="features"><!-- Feature grid or showcase --></section>
  <section class="social-proof"><!-- Stats, testimonials, logos --></section>
  <!-- ... additional sections as needed ... -->
  <section class="cta-final"><!-- Final call to action --></section>
  <footer><!-- Links, copyright --></footer>

  <script>
    // Scroll animations, counters, interactions — all inline
  </script>
</body>
</html>
```

### Mandatory Technical Requirements

1. **Viewport Fitting** — Each section should feel "full" but never overflow. Use `min-height: 100vh` for hero, proportional heights for others.
2. **Responsive** — Must work on mobile. Use `clamp()` for all font sizes, viewport-relative units for spacing.
3. **Scroll Animations** — Use IntersectionObserver for reveal-on-scroll. Elements should animate in as user scrolls.
4. **Performance** — CSS animations preferred over JS. `will-change` on animated elements. Debounce scroll handlers.
5. **Accessible** — Semantic HTML, sufficient contrast, `prefers-reduced-motion` media query for all animations.

### Section Density Limits

Per section (to prevent overcrowding):
- **Hero**: 1 headline (max 8 words), 1 subheadline (max 20 words), 1-2 CTAs, optional background effect
- **Features**: Max 6 cards. Each card: icon + title (3-4 words) + description (max 15 words)
- **Stats/Metrics**: Max 4 counters
- **Testimonials**: Max 3 quotes
- **Pricing**: Max 3 tiers
- **FAQ**: Max 6 items (use accordion/collapse)

Too much content for one section? Split into two sections with a visual break between them.

### CSS Architecture

```css
:root {
  /* Typography — always use clamp() */
  --font-display: 'YOUR_CHOICE', sans-serif;
  --font-body: 'YOUR_CHOICE', sans-serif;
  --heading-size: clamp(2rem, 5vw, 4.5rem);
  --body-size: clamp(0.875rem, 1.5vw, 1.125rem);
  
  /* Colors — define full palette */
  --bg-primary: #...;
  --bg-secondary: #...;
  --text-primary: #...;
  --text-secondary: #...;
  --accent: #...;
  --accent-hover: #...;
  --cta-gradient: linear-gradient(...);
  
  /* Spacing */
  --section-padding: clamp(3rem, 8vw, 8rem);
  --content-width: min(90vw, 1200px);
  
  /* Animation */
  --transition-fast: 0.3s ease;
  --transition-smooth: 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Scroll reveal base class */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity var(--transition-smooth), transform var(--transition-smooth);
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### JavaScript Essentials

Always include these patterns:

```javascript
// Scroll reveal with IntersectionObserver
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// Animated counters (for stats sections)
function animateCounter(el, target, duration = 2000) { ... }

// Smooth scroll for nav links
document.querySelectorAll('a[href^="#"]').forEach(anchor => { ... });
```

**Read `references/SECTION_LIBRARY.md`** for complete section templates with HTML, CSS, and JS patterns for each section type.

### Anti-AI-Slop Checklist

Before generating, verify:
- [ ] Fonts are NOT Inter, Roboto, Arial, or system defaults
- [ ] Color scheme is NOT purple-gradient-on-white
- [ ] Hero doesn't use the word "Revolutionize" or "Supercharge"
- [ ] CTA buttons have hover animations, not just color change
- [ ] Background has texture/depth — NOT flat solid color
- [ ] At least one unexpected design choice (asymmetric layout, bold typography, creative section divider)

### Delivery

1. Save the HTML file with a descriptive name: `{product-name}-landing.html`
2. Open in browser: `open {product-name}-landing.html`
3. Present to user and ask for feedback

---

## Phase 4: Iteration

After initial generation, ask via AskUserQuestion (header: "Feedback"):
"How does it look?"
Options: Ship it! / Adjust colors-fonts / Change layout / Add-remove sections / Start over with new style

For modifications, follow these rules:
- **Adding content**: Check section density limits first. If exceeded, split sections.
- **Changing style**: Update CSS variables, don't rewrite structure.
- **Adding sections**: Read `references/SECTION_LIBRARY.md` for the section template, insert in logical order.
- **Removing sections**: Delete cleanly, check that no JS references break.

---

## References (Progressive Disclosure)

This skill uses progressive disclosure — load reference files only when needed:

| File | When to read | What it contains |
|------|-------------|-----------------|
| `references/STYLE_PRESETS.md` | Phase 2 (style discovery) | 5 curated style presets with full CSS variables, font pairings, and background treatments |
| `references/SECTION_LIBRARY.md` | Phase 3 (generation) | Complete HTML/CSS/JS templates for every section type (hero, features, pricing, etc.) |
