---
name: agentic-website-design
description: Design and build websites using AI coding agents with static site generators. Covers Astro-first workflow, iterative visual refinement via browser feedback, skill-enhanced prompting (frontend-design, copywriting), animations, and high-bar polish loops. Use when building a website with an AI agent, designing landing pages, or iterating on web design with LLM assistance.
---

# Agentic Website Design

Build production-quality websites where the AI coding agent has full control over every line of code. Use static site generators (Astro preferred) — never no-code tools like Framer or Webflow that limit LLM control.

## Core Principles

1. **Full code control** — The LLM generates all HTML, CSS, JS, and content. No drag-and-drop, no visual editors, no black boxes.
2. **Browser-in-the-loop** — The agent MUST see what it builds. Use browser tools to screenshot and inspect the live site after every change.
3. **Skill-enhanced prompting** — Delegate specialized work to dedicated skills (frontend-design, copywriting, etc.) instead of doing everything in one prompt.
4. **Relentless iteration** — Never accept the first output. Set a high bar and improve repeatedly until the result is exceptional.

---

## Stack Selection

### Default: Astro

Astro is the preferred static site generator because it ships zero JS by default, supports any UI framework, and gives the LLM full template control.

```bash
npm create astro@latest my-site
cd my-site
npm run dev
```

### Alternatives

| Generator | When to Use |
|-----------|-------------|
| Astro | Default choice — best DX, island architecture |
| Next.js | Need SSR, API routes, or React ecosystem |
| Nuxt | Vue-based projects |
| SvelteKit | Svelte-based projects |
| 11ty | Simplest possible static sites |

Pick one and stick with it. The LLM must have full control over templates, styles, and content.

---

## Browser Feedback Loop

The agent MUST visually verify every change. Without browser access, the agent is coding blind.

### Setup

**Cursor**: Install the Browser plugin (browser-tools MCP) to give the agent access to screenshots, console logs, and network requests.

**Claude Code**: Use the Chrome DevTools integration to capture screenshots and inspect the DOM.

### Workflow

After every meaningful change:

1. **Save files** and wait for hot reload
2. **Screenshot the page** — capture the full viewport
3. **Inspect the result** — check layout, spacing, colors, typography
4. **Identify issues** — misalignment, overflow, broken responsive, missing states
5. **Fix and re-screenshot** — repeat until the section looks correct

```
Loop:
  Make change → Save → Screenshot → Evaluate → Fix → Screenshot
  Exit when: section meets quality bar
```

**Never skip the screenshot step.** The visual feedback loop is what separates good agentic design from broken layouts.

For browser tool setup details, see [references/browser-setup.md](references/browser-setup.md).

---

## Skill-Enhanced Prompting

Delegate specialized tasks to dedicated skills. This produces dramatically better results than generic prompting.

### Pattern

When working on a specific aspect of the site, invoke the relevant skill explicitly:

```
"Use the frontend-design skill to redesign the hero section with modern layout patterns"
"Use the copywriting skill to rewrite the homepage headline and subheading"
"Use the frontend-design skill to add micro-interactions to the CTA buttons"
"Use the copywriting skill to improve the feature descriptions — make them benefit-driven"
```

### Recommended Skills

| Skill | Use For |
|-------|---------|
| frontend-design | Layout, visual hierarchy, component patterns, responsive design |
| copywriting | Headlines, CTAs, feature descriptions, brand voice |
| seo | Meta tags, structured data, performance, Core Web Vitals |
| accessibility | ARIA labels, keyboard navigation, color contrast |

### Composing Skills

Chain skills together for full-section work:

```
1. "Use the copywriting skill to write compelling copy for the pricing section"
2. "Use the frontend-design skill to design the pricing cards layout with the copy above"
3. "Now screenshot and let's iterate on the visual design"
```

---

## Iterative Improvement Workflow

This is the most important section. The difference between mediocre and exceptional output is iteration count.

### The Improvement Loop

```
Task Progress:
- [ ] Step 1: Generate initial version
- [ ] Step 2: Screenshot and evaluate
- [ ] Step 3: Identify the weakest element
- [ ] Step 4: Improve that element specifically
- [ ] Step 5: Screenshot and compare
- [ ] Step 6: Repeat steps 3-5 at least 3 more times
- [ ] Step 7: Final polish pass
```

### Setting a High Bar

After every change, ask:

- "Now improve what you just did"
- "Make the animations smoother and more intentional"
- "This is good, but push it further — what would a top design agency do differently?"
- "Add subtle micro-interactions that make this feel premium"
- "The spacing feels off — tighten it up and make it breathe properly"

**Never settle on the first version.** Always push for at least 3 rounds of improvement on each section.

### Section-by-Section Approach

Work on one section at a time, fully polishing it before moving on:

1. **Hero** — Most important. Spend the most time here. Nail the headline, visual, and CTA.
2. **Social proof** — Logos, testimonials, metrics. Make it feel credible.
3. **Features** — Clear, benefit-driven, with supporting visuals or icons.
4. **Pricing** — Clean comparison, obvious recommended tier.
5. **Footer** — Professional, complete, well-organized.

For each section: generate → screenshot → critique → improve → screenshot → critique → improve → move on.

---

## Animations & Micro-Interactions

Animations are what separate a flat page from a polished product. Always add them.

### Must-Have Animations

| Element | Animation |
|---------|-----------|
| Hero headline | Fade-in + slight upward slide on load |
| CTA buttons | Hover scale + color transition |
| Feature cards | Scroll-triggered fade-in with stagger |
| Navigation | Smooth scroll, sticky header with backdrop blur |
| Page transitions | Subtle fade between routes |
| Images | Lazy load with fade-in |

### Implementation

Use CSS animations and `IntersectionObserver` for scroll-triggered effects. Avoid heavy JS animation libraries unless needed.

```css
/* Scroll-triggered fade-in */
.animate-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.animate-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}
```

For Astro-specific animation patterns, see [references/animations.md](references/animations.md).

### Demanding Quality

After adding animations:

- "The easing feels linear — use a custom cubic-bezier for more natural motion"
- "Stagger the feature cards so they animate in sequence, not all at once"
- "Add a subtle parallax effect to the hero background"
- "The hover states need more personality — try a slight rotation or shadow lift"

---

## Responsive Design

Every page MUST work on mobile, tablet, and desktop. Screenshot at all breakpoints.

### Breakpoint Checklist

```
- [ ] Mobile (375px) — single column, touch-friendly targets
- [ ] Tablet (768px) — adapted grid, readable line lengths
- [ ] Desktop (1280px) — full layout, max-width containers
- [ ] Wide (1536px+) — content doesn't stretch awkwardly
```

After building each section, screenshot at mobile and desktop minimum. Fix layout issues before moving on.

---

## Project Structure (Astro)

```
my-site/
├── src/
│   ├── layouts/
│   │   └── Layout.astro          # Base HTML shell
│   ├── components/
│   │   ├── Hero.astro
│   │   ├── Features.astro
│   │   ├── Pricing.astro
│   │   └── Footer.astro
│   ├── pages/
│   │   └── index.astro
│   └── styles/
│       └── global.css
├── public/
│   └── fonts/
├── astro.config.mjs
└── package.json
```

Use component-per-section architecture. Each section is its own `.astro` file for clean iteration.

---

## Quality Checklist

Before considering a page done:

```
Visual Quality:
- [ ] Every section screenshotted and reviewed at mobile + desktop
- [ ] Typography hierarchy is clear (max 2-3 font sizes per section)
- [ ] Color palette is consistent (3-5 colors max)
- [ ] Whitespace is generous and intentional
- [ ] Images are optimized and properly sized

Animations:
- [ ] Hero has entry animation
- [ ] Scroll-triggered animations on content sections
- [ ] Hover states on all interactive elements
- [ ] No janky or stuttering animations
- [ ] Animations respect prefers-reduced-motion

Content:
- [ ] Headlines are benefit-driven, not feature-driven
- [ ] CTAs are clear and compelling
- [ ] No lorem ipsum or placeholder content
- [ ] Copy reviewed with copywriting skill

Technical:
- [ ] Lighthouse score 90+ on all categories
- [ ] Responsive at all breakpoints
- [ ] Semantic HTML throughout
- [ ] Accessible (keyboard nav, ARIA labels, contrast)
- [ ] Fast load time (minimal JS, optimized assets)
```

---

## Additional Resources

- [Browser Setup](references/browser-setup.md) — Cursor Browser plugin and Claude Code Chrome integration
- [Animations](references/animations.md) — Astro animation patterns, scroll effects, and micro-interactions
- [Prompting Patterns](references/prompting-patterns.md) — Example prompts for each design phase
