---
name: web-design-skills
description: >
  Comprehensive web design skill pack for building professional, accessible, well-designed
  websites. Framework-agnostic — works with Tailwind, vanilla CSS, CSS-in-JS, or any stack.
  Use this skill whenever building any web interface — landing pages, web apps, dashboards,
  portfolios, e-commerce sites, or any frontend project. Trigger whenever the agent is making
  design decisions about layout, typography, color, spacing, components, responsive behavior,
  accessibility, interaction patterns, content structure, or frontend implementation. This
  skill pack should be consulted at the START of any web project, not as an afterthought.
---

# Web Design Skill Pack

A modular library of 14 interconnected skills that help an AI agent build better websites
consistently. Each skill focuses on design principles, values, and outcomes — not on any
particular CSS framework or toolchain. The guidance works equally well with Tailwind, vanilla
CSS, CSS modules, Styled Components, or any other approach.

## How to Use This Skill Pack

This is an orchestrator skill. Read the relevant sub-skills based on what you're building:

### For any new web project, always start with:
1. **`content-structure`** — Plan the page sections and information flow
2. **`layout-and-spacing`** — Set up the grid, spacing system, and spatial relationships
3. **`typography`** — Choose fonts, define the type scale, set line heights
4. **`color-systems`** — Build the color palette, define tokens for theming
5. **`frontend-implementation`** — Set up design tokens, resets, and base patterns

### Then consult based on what you're building:

**For marketing sites / landing pages:**
6. **`content-structure`** already covers site-specific page anatomy (hero, social proof, pricing, etc.)
7. **`seo`** — Set up metadata, Open Graph, structured data, sitemaps, and search discoverability

**For web apps / dashboards:**
6. **`app-patterns`** — App shell layouts, sidebar nav, tabs, command palettes, data-heavy components

**Always consult as needed:**
7. **`visual-hierarchy`** — Ensure the right things get attention in the right order
8. **`responsive-design`** — Make layouts work across all screen sizes
9. **`ui-components`** — Build buttons, cards, navigation, forms, and other shared UI elements
10. **`interaction-patterns`** — Design hover states, animations, loading states, and user flows
11. **`ux-flows`** — Plan user journeys, conversion paths, onboarding, and trust placement
12. **`internationalization`** — Design for multiple languages, RTL scripts, text expansion, and cultural differences
13. **`accessibility`** — Ensure WCAG 2.2 AA compliance across the entire interface

## Skill Directory

Read each skill's SKILL.md when working on its domain:

| Skill | Path | Use When |
|-------|------|----------|
| Layout & Spacing | `skills/layout-and-spacing/SKILL.md` | Building page structure, grids, setting margins/padding/gaps |
| Typography | `skills/typography/SKILL.md` | Choosing fonts, sizing text, setting line heights and letter spacing |
| Color Systems | `skills/color-systems/SKILL.md` | Picking colors, building palettes, implementing dark/light mode |
| Responsive Design | `skills/responsive-design/SKILL.md` | Making layouts work on mobile, tablet, and desktop |
| UI Components | `skills/ui-components/SKILL.md` | Building buttons, cards, nav, forms, modals, hero sections |
| Accessibility | `skills/accessibility/SKILL.md` | Ensuring keyboard nav, contrast, ARIA, screen reader support |
| Visual Hierarchy | `skills/visual-hierarchy/SKILL.md` | Deciding what to emphasize, scanning patterns, focal points |
| Interaction Patterns | `skills/interaction-patterns/SKILL.md` | Designing animations, hover states, loading, error handling |
| Content Structure | `skills/content-structure/SKILL.md` | Planning page sections, information architecture, copy |
| UX Flows | `skills/ux-flows/SKILL.md` | User journeys, conversion, onboarding, checkout, trust signals |
| SEO & Discoverability | `skills/seo/SKILL.md` | Meta tags, Open Graph, structured data, sitemaps, crawling |
| App Patterns | `skills/app-patterns/SKILL.md` | App shells, sidebar nav, tabs, command palettes, app-specific components |
| Internationalization | `skills/internationalization/SKILL.md` | Multi-language design, RTL, text expansion, cultural considerations |
| Frontend Implementation | `skills/frontend-implementation/SKILL.md` | Design tokens, resets, performance, production readiness |

## Universal Principles

These principles run through every skill in this pack. Keep them in mind at all times:

### 1. Don't Make Users Think
Every click, scroll, and field should feel effortless. If users pause to figure out your
interface, you've already lost them. Simplicity is a skill — it's harder to make something
simple than to make something complex.

### 2. Consistency Beats Perfection
A consistent spacing system with "wrong" values still looks better than random "correct"
values. Apply the same tokens, the same patterns, the same conventions everywhere.
Consistency builds trust and reduces cognitive load.

### 3. Hierarchy Is Everything
If everything is emphasized, nothing is. Use size, weight, color, and spacing to create
three clear levels of importance: primary (what users see first), secondary (what supports
the primary), and tertiary (details for those who want them).

### 4. Start with More Space, Then Reduce
Generous whitespace is almost always the right move. Cramped designs feel cheap;
spacious designs feel premium. Start with too much padding and reduce only if you run
out of room.

### 5. Design is for the User, Not the Designer
Every decision — from font choice to section order — should serve the person using the
website. Design for their goals, not for visual novelty or portfolio impressiveness.

### 6. Accessibility Is Not Optional
Build accessible from the start. Semantic HTML, proper contrast, keyboard navigation,
screen reader support. It's easier (and cheaper) to build it right than to retrofit it later.

### 7. Design for Emotion, Not Just Aesthetics
Before starting any project, write down one core emotion the viewer should feel: calm,
urgency, trust, joy, excitement. Then audit every design decision against that emotion.
Does the color support it? Does the font reinforce it? Does the animation match? If
anything feels neutral or contradictory, rethink it. A beginner says "this looks good" —
a pro says "this feels right."

### 8. Pre-Mortem Before Shipping
Before delivering, ask: "Where could this go wrong?" Will the logo be misread at small
sizes? Does the palette work on different backgrounds? Does the type still function on
tiny mobile screens? Professionals don't wait for failure — they test for it before launch.

### 9. Test on Real Devices
What looks great in a browser preview may break on an actual phone. Test at real
breakpoints (320px, 768px, 1024px, 1920px), test with a keyboard, test with zoom at 200%.

## Quick-Start Design Token Checklist

Before writing any component code, define tokens for these categories (how you store
them — CSS custom properties, Tailwind config, theme object — depends on your stack):

1. **Fonts**: Display font + body font (2 families max)
2. **Type scale**: 5-7 sizes from 0.75rem to 2.5rem
3. **Spacing scale**: Base-4 increments from 0.25rem to 6rem
4. **Colors**: Background, text (3 levels), accent, border, shadow, semantic (success/error/warning)
5. **Radii**: 3-4 sizes from subtle (4px) to pill (9999px)
6. **Transitions**: Fast (150ms), base (200ms), slow (300ms)

See `skills/frontend-implementation/SKILL.md` for the complete token reference tables.

## Sources and Influences

This skill pack synthesizes principles from:
- Professional web design video courses on typography, layout, spacing, color, and responsive design
- Anthropic's official frontend-design skill for Claude
- Vercel Labs' web-interface-guidelines
- WCAG 2.2 Level AA accessibility standards
- Baymard Institute UX research
- Gestalt principles of visual perception
- Industry patterns from top-tier websites (Figma, Webflow, Stripe, Apple)
