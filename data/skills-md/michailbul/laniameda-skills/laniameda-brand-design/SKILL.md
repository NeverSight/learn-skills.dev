---
name: Laniameda Brand Design
description: >-
  This skill should be used when the user asks to "design a landing page",
  "create a website design", "build a page in Pencil", "follow the laniameda design system",
  "use our brand colors", "design for developers", or mentions laniameda brand guidelines,
  warm editorial style, brutalist-editorial hybrid, or code-savvy developer marketing pages.
  Provides the complete laniameda design system (colors, typography, shadows, components)
  and a proven Pencil MCP workflow for building high-quality landing pages.
version: 0.1.0
---

# Laniameda Brand Design System & Landing Page Workflow

Build marketing pages and product websites that follow the laniameda design system — a warm editorial + brutalist hybrid aesthetic designed for technical/developer audiences.

## Brand Identity

**Mood**: Warm editorial, studio console, paper & ink, artisan digital
**Tone**: Quiet confidence — authoritative but never loud. Sharp, technical, no fluff.
**Audience**: AI engineers, vibe coders, developers who live in the terminal
**Test**: "These people get it" — if a developer reads the hero at 11pm and thinks that, it works.

### What It Is NOT

- SaaS corporate, playful/whimsical, enterprise formal
- No Lorem Ipsum. No "game-changing". No "unlock potential".
- No pure white (`#ffffff`) backgrounds. No pure black (`#000000`) text.
- No cold/gray shadows. No neon accents.

---

## Quick Color Reference

| Token | Hex | Role |
|-------|-----|------|
| Paper | `#fffaf5` | Page background |
| Surface-1 | `#fff4ea` | Secondary areas |
| Surface-2 | `#f7ede2` | Card backgrounds |
| Surface-3 | `#efe2d4` | Deeper fills |
| Ink | `#201710` | Darkest text, brand mark |
| Text Secondary | `#4c3a2d` | Descriptions, metadata |
| Text Tertiary | `#7d6755` | Section labels |
| Text Ghost | `#ab9381` | Placeholders, hints |
| Coral | `#ff7a64` | Primary accent (sparingly) |
| Coral Hover | `#ff917d` | Hover state |
| Inverse BG | `#18181b` | Dark panels, terminals |
| Inverse Text | `#fafafa` | Text on dark |

For the full token set including amber ramp, borders, and semantic mappings, consult `references/design-tokens.md`.

## Quick Typography Reference

| Family | Mapping in Pencil | Role |
|--------|-------------------|------|
| Instrument Serif (italic) | Playfair Display italic | Display headlines, hero text, serif moments |
| Geist Sans | Inter | Body text, UI text, descriptions |
| Geist Mono | JetBrains Mono | Labels, badges, code, terminal, nav items |

**Key rules:**
- Monospace labels are ALWAYS uppercase with 0.08-0.22em letter-spacing
- Display text is ALWAYS italic serif
- Headlines: Inter 800/900, -0.04em letter-spacing
- Terminal bg: `#0f0f0f`, coral/green/white syntax coloring

## Quick Shadow Reference

| Type | Value | Use |
|------|-------|-----|
| Soft SM | `0 1px 3px rgba(32,23,16,0.06)` | Cards at rest |
| Soft MD | `0 4px 12px rgba(32,23,16,0.08)` | Hover, dropdowns |
| Soft LG | `0 12px 40px rgba(32,23,16,0.12)` | Modals, panels |
| Brutalist | `4px 4px 0 #201710` | Brutalist cards, CTAs |
| Brutalist SM | `2px 2px 0 #201710` | Smaller elements |
| Brutalist Hover | `6px 6px 0` + translate(-2px,-2px) | Lift effect |

---

## Design Workflow in Pencil

### Phase 1: Setup

1. Get editor state with `get_editor_state(include_schema: true)` to understand the active document
2. Open or create a `.pen` file with `open_document`
3. Set design variables using `set_variables` — register the color palette
4. Get guidelines with `get_guidelines(topic: "landing-page")` for layout rules
5. Get style guide tags with `get_style_guide_tags`, then `get_style_guide` with relevant tags

### Phase 2: Build Reusable Components

Before building any screens, create reusable components (`reusable: true`). Standard component library for laniameda landing pages is documented in `references/component-library.md`.

Core components to build:
- **macOS Window Chrome** — titlebar with traffic light dots + body placeholder
- **CTA Pill** — coral bg, monospace prompt + command text
- **Ghost Button** — ink outline, monospace label
- **Section Label** — monospace coral eyebrow with `//` prefix
- **Brutalist Card** — zero-radius, ink offset shadow, icon + title + desc
- **Soft Card** — 20px radius, editorial shadow
- **Badges** — ink variant + coral variant, pill-shaped

### Phase 3: Build Screen Sections

Standard landing page section order:
1. **Hero** — eyebrow + massive headline + sub + CTA pill + terminal/product preview
2. **Problems** — 3 pain points in brutalist or soft cards
3. **Features** — 8-item grid (2x4 or numbered list)
4. **Setup** — tabbed terminal blocks (Install / Configure / Docker)
5. **Compatibility** — agent + platform badges
6. **FAQ** — accordion-style Q&A with coral borders
7. **Footer** — links + copyright

### Phase 4: Verify

After each major section, take a screenshot with `get_screenshot` to verify visual quality. Check for:
- Color consistency (no stray whites/blacks)
- Typography hierarchy (serif display, sans body, mono labels)
- Spacing rhythm (generous whitespace)
- Shadow consistency

### Bulk Color Operations

To retheme an entire direction, use `search_all_unique_properties` to audit colors, then `replace_all_matching_properties` for bulk changes. IMPORTANT: Always manually fix terminal windows, traffic light dots, and syntax-colored text afterward — these should stay dark even in light themes.

---

## Design Directions Pattern

When building multiple directions, differentiate through:

| Lever | Options |
|-------|---------|
| Card style | Brutalist (0 radius) vs Soft (20px) |
| Hero approach | Terminal output vs Editorial serif vs Product mockup |
| Section rhythm | Dense/continuous vs Dramatic chapter breaks |
| Feature layout | 2x4 grid vs Numbered editorial list vs Annotated mockup |
| Dark sections | None vs Full-bleed ink breaks vs Terminal-only dark |

Example proven directions:
- **"Workbench"** — light paper bg, dark terminals as focal points, brutalist 0-radius cards, monospace-heavy
- **"Paper Press"** — massive italic serif headlines, full-bleed ink chapter breaks, numbered features, editorial rhythm
- **"Window Stack"** — macOS app mockup in hero, soft cards, multiple floating terminals, Spotlight-style CTA

---

## Pencil Operation Patterns

Refer to `references/pencil-workflow.md` for detailed batch_design operation syntax, including:
- Insert/Update patterns for component instances
- Copy with descendant overrides
- Layout configuration (vertical/horizontal/gap/padding)
- Text styling with fill, fontSize, fontFamily, fontWeight

## Landing Page Section Examples

Refer to `examples/landing-page-sections.md` for concrete batch_design operations showing how to build each section type.

---

## Critical Rules

1. **All copy from `lib/content.ts`** — never hardcode strings in designs
2. **Coral used sparingly** — key CTAs, accent moments only
3. **Brutalist shadows: `4px 4px 0 #201710`** — never add blur
4. **Hover lift: translate(-2px, -2px)** + shadow grows to `6px 6px 0`
5. **JetBrains Mono for**: labels, eyebrows, badges, nav, terminal, code
6. **Inter 800/900 for**: ALL display headings
7. **No pure white/black** — warm paper stack and ink scale only
8. **Traffic light dots**: `#ff5f56` (red), `#ffbd2e` (yellow), `#27c93f` (green)
9. **Terminal interiors stay dark** even in light themes — `#0f0f0f` or `#1a1a1a`
10. **Verify with screenshots** after each section

## Additional Resources

### Reference Files
- **`references/design-tokens.md`** — Complete CSS custom properties, color palette, typography scale, shadows, spacing, timing
- **`references/pencil-workflow.md`** — Pencil MCP tool patterns, batch_design syntax, component architecture
- **`references/component-library.md`** — Full specs for all reusable components (macOS chrome, cards, buttons, badges)

### Examples
- **`examples/landing-page-sections.md`** — Concrete batch_design operations for hero, problems, features, setup, FAQ, footer sections
