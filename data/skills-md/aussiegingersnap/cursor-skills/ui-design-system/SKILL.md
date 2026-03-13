---
name: ui-design-system
description: Complete design system with principles + living style guide. Enforces precise, crafted UI inspired by Linear, Notion, and Stripe. Includes boilerplate style-guide page template for Next.js/React projects. Use when building any UI that needs Jony Ive-level precision.
---

# Design System

This skill provides a complete design system: the **philosophy** (how to think about design) and the **documentation** (a living style guide template). Every interface should look designed by a team that obsesses over 1-pixel differences.

## Workflow

1. **Start with Design Direction** — Read Part 1 and commit to a direction before writing code
2. **Apply Craft Principles** — Follow the core rules in Part 2 as you build
3. **Document in Style Guide** — Add every component to the style guide (Part 3)

---

# Part 1: Design Direction

**Before writing any code, commit to a design direction.** Don't default. Think about what this specific product needs to feel like.

## Think About Context

- **What does this product do?** A finance tool needs different energy than a creative tool.
- **Who uses it?** Power users want density. Occasional users want guidance.
- **What's the emotional job?** Trust? Efficiency? Delight? Focus?
- **What would make this memorable?** Every product has a chance to feel distinctive.

## Choose a Personality

Enterprise/SaaS UI has more range than you think. Consider these directions:

**Precision & Density** — Tight spacing, monochrome, information-forward. For power users who live in the tool. Think Linear, Raycast, terminal aesthetics.

**Warmth & Approachability** — Generous spacing, soft shadows, friendly colors. For products that want to feel human. Think Notion, Coda, collaborative tools.

**Sophistication & Trust** — Cool tones, layered depth, financial gravitas. For products handling money or sensitive data. Think Stripe, Mercury, enterprise B2B.

**Boldness & Clarity** — High contrast, dramatic negative space, confident typography. For products that want to feel modern and decisive. Think Vercel, minimal dashboards.

**Utility & Function** — Muted palette, functional density, clear hierarchy. For products where the work matters more than the chrome. Think GitHub, developer tools.

**Data & Analysis** — Chart-optimized, technical but accessible, numbers as first-class citizens. For analytics, metrics, business intelligence.

Pick one. Or blend two. But commit to a direction that fits the product.

## Choose a Color Foundation

**Don't default to warm neutrals.** Consider the product:

- **Warm foundations** (creams, warm grays) — approachable, comfortable, human
- **Cool foundations** (slate, blue-gray) — professional, trustworthy, serious
- **Pure neutrals** (true grays, black/white) — minimal, bold, technical
- **Tinted foundations** (slight color cast) — distinctive, memorable, branded

**Light or dark?** Dark modes aren't just light modes inverted. Dark feels technical, focused, premium. Light feels open, approachable, clean. Choose based on context.

**Accent color** — Pick ONE that means something. Blue for trust. Green for growth. Orange for energy. Violet for creativity. Don't just reach for the same accent every time.

## Choose a Layout Approach

The content should drive the layout:

- **Dense grids** for information-heavy interfaces where users scan and compare
- **Generous spacing** for focused tasks where users need to concentrate
- **Sidebar navigation** for multi-section apps with many destinations
- **Top navigation** for simpler tools with fewer sections
- **Split panels** for list-detail patterns where context matters

## Choose Typography

Typography sets tone. Don't always default:

- **System fonts** — fast, native, invisible (good for utility-focused products)
- **Geometric sans** (Geist, Inter) — modern, clean, technical
- **Humanist sans** (SF Pro, Satoshi) — warmer, more approachable
- **Monospace influence** — technical, developer-focused, data-heavy

---

# Part 2: Craft Principles

These apply regardless of design direction. This is the quality floor.

## The 4px Grid

All spacing uses a 4px base grid:
- `4px` - micro spacing (icon gaps)
- `8px` - tight spacing (within components)
- `12px` - standard spacing (between related elements)
- `16px` - comfortable spacing (section padding)
- `24px` - generous spacing (between sections)
- `32px` - major separation

## Symmetrical Padding

**TLBR must match.** If top padding is 16px, left/bottom/right must also be 16px. Exception: when content naturally creates visual balance.

```css
/* Good */
padding: 16px;
padding: 12px 16px; /* Only when horizontal needs more room */

/* Bad */
padding: 24px 16px 12px 16px;
```

## Border Radius Consistency

Stick to the 4px grid. Sharper corners feel technical, rounder corners feel friendly. Pick a system and commit:

- Sharp: 4px, 6px, 8px
- Soft: 8px, 12px
- Minimal: 2px, 4px, 6px

Don't mix systems. Consistency creates coherence.

## Depth & Elevation Strategy

**Match your depth approach to your design direction.** Depth is a tool, not a requirement:

**Borders-only (flat)** — Clean, technical, dense. Works for utility-focused tools where information density matters more than visual lift. Linear, Raycast, and many developer tools use almost no shadows — just subtle borders to define regions.

**Subtle single shadows** — Soft lift without complexity. A simple `0 1px 3px rgba(0,0,0,0.08)` can be enough.

**Layered shadows** — Rich, premium, dimensional. Multiple shadow layers create realistic depth. Stripe and Mercury use this approach.

**Surface color shifts** — Background tints establish hierarchy without any shadows. A card at `#fff` on a `#f8fafc` background already feels elevated.

Choose ONE approach and commit.

```css
/* Borders-only approach */
--border: rgba(0, 0, 0, 0.08);
border: 0.5px solid var(--border);

/* Single shadow approach */
--shadow: 0 1px 3px rgba(0, 0, 0, 0.08);

/* Layered shadow approach */
--shadow-layered:
  0 0 0 0.5px rgba(0, 0, 0, 0.05),
  0 1px 2px rgba(0, 0, 0, 0.04),
  0 2px 4px rgba(0, 0, 0, 0.03),
  0 4px 8px rgba(0, 0, 0, 0.02);
```

## Card Layouts

Monotonous card layouts are lazy design. Design each card's internal structure for its specific content — but keep the surface treatment consistent: same border weight, shadow depth, corner radius, padding scale, typography.

## Isolated Controls

UI controls deserve container treatment. Date pickers, filters, dropdowns should feel like crafted objects.

**Never use native form elements for styled UI.** Build custom components instead:
- Custom select: trigger button + positioned dropdown menu
- Custom date picker: input + calendar popover
- Custom checkbox/radio: styled div with state management

## Typography Hierarchy

- Headlines: 600 weight, tight letter-spacing (-0.02em)
- Body: 400-500 weight, standard tracking
- Labels: 500 weight, slight positive tracking for uppercase
- Scale: 11px, 12px, 13px, 14px (base), 16px, 18px, 24px, 32px

## Monospace for Data

Numbers, IDs, codes, timestamps belong in monospace. Use `tabular-nums` for columnar alignment.

## Iconography

Use **Phosphor Icons** (`@phosphor-icons/react`) or **Lucide** (`lucide-react`). Icons clarify, not decorate — if removing an icon loses no meaning, remove it.

## Animation

- 150ms for micro-interactions, 200-250ms for larger transitions
- Easing: `cubic-bezier(0.25, 1, 0.5, 1)`
- No spring/bouncy effects in enterprise UI

## Contrast Hierarchy

Build a four-level system: foreground (primary) → secondary → muted → faint. Use all four consistently.

## Color for Meaning Only

Gray builds structure. Color only appears when it communicates: status, action, error, success. Decorative color is noise.

## Navigation Context

Screens need grounding:
- **Navigation** — sidebar or top nav showing where you are
- **Location indicator** — breadcrumbs, page title, or active nav state
- **User context** — who's logged in, what workspace/org

## Dark Mode Considerations

**Borders over shadows** — Shadows are less visible on dark backgrounds. Lean more on borders.

**Adjust semantic colors** — Status colors often need to be slightly desaturated for dark backgrounds.

---

# Part 3: Anti-Patterns

## Never Do This

- Dramatic drop shadows (`box-shadow: 0 25px 50px...`)
- Large border radius (16px+) on small elements
- Asymmetric padding without clear reason
- Pure white cards on colored backgrounds
- Thick borders (2px+) for decoration
- Excessive spacing (margins > 48px between sections)
- Spring/bouncy animations
- Gradients for decoration
- Multiple accent colors in one interface

## Always Question

- "Did I think about what this product needs, or did I default?"
- "Does this direction fit the context and users?"
- "Does this element feel crafted?"
- "Is my depth strategy consistent and intentional?"
- "Are all elements on the grid?"

---

# Part 4: Style Guide Template

**The style guide is living documentation of your design system.** Every component you build should be documented here.

## What the Template Creates

A `/style-guide` page with:
- **Left navigation** — Sticky sidebar with hierarchical section navigation
- **Colors** — Brand palette, category colors, system colors
- **Typography** — Font families, sizes, weights
- **Buttons** — All variants, sizes, states
- **Inputs** — Default, focus, error, disabled states
- **Cards** — Layout variations
- **Avatars** — Sizes and fallback states
- **Dialogs** — Modal patterns
- **Loading/Thinking** — Spinners, indicators, animated states
- **Design Tokens** — Spacing scale, border radius, shadows

## Using the Template

### 1. Copy to Your Project

```bash
cp templates/style-guide-page.tsx your-app/app/style-guide/page.tsx
```

### 2. Customize

1. **Update the header title** — Replace "STYLE GUIDE" with your project name
2. **Add your brand colors** — Update the Colors section with your palette
3. **Add your fonts** — Update the Typography section
4. **Import your components** — Replace placeholder imports with your actual components
5. **Add project-specific sections** — Add sections for custom components

### 3. Maintain

**The style guide is the canonical source for all UI components.**

When building or modifying components:

1. **Check the style guide first** — See if a component exists before creating
2. **Add new components** — Every reusable component gets a section
3. **Show all states** — Normal, hover, focus, disabled, error, loading
4. **Update on changes** — Modify a component? Update its style guide entry

## Template Structure

Navigation items define the sidebar structure:

```typescript
const NAV_ITEMS = [
  { id: 'colors', label: 'Colors', icon: Palette, children: [
    { id: 'brand', label: 'Brand' },
    { id: 'system', label: 'System' },
  ]},
  { id: 'typography', label: 'Typography', icon: Type },
  { id: 'buttons', label: 'Buttons', icon: MousePointer },
  // ... more sections
]
```

Each section follows this pattern:

```tsx
<section id="buttons">
  <SectionHeader title="Buttons" />
  <div>
    <h4 className="text-xs font-medium text-muted-foreground mb-3 uppercase tracking-wide">
      Variants
    </h4>
    <div className="flex flex-wrap gap-3">
      <Button variant="default">Default</Button>
      <Button variant="secondary">Secondary</Button>
    </div>
  </div>
</section>
```

## Adding Custom Sections

1. Add to `NAV_ITEMS`:
```typescript
{ id: 'my-component', label: 'My Component', icon: Box },
```

2. Add the section:
```tsx
<section id="my-component">
  <SectionHeader title="My Component" />
  {/* Component variations */}
</section>
```

## Maintenance Checklist

For every UI change:

- [ ] Component added to style guide (if new)
- [ ] All states shown (normal, hover, disabled, loading, error)
- [ ] Uses design tokens (colors, spacing, radius from theme)
- [ ] Properly exported from component index

## Best Practices

1. **Keep it current** — Outdated style guides are worse than none
2. **Show real data** — Use realistic mock data, not "Lorem ipsum"
3. **Test interactions** — Dialogs should open, buttons should click
4. **Document edge cases** — Long text, empty states, loading
5. **Mobile considerations** — Show responsive variants if applicable

---

# The Standard

Every interface should look designed by a team that obsesses over 1-pixel differences. Not stripped — *crafted*. And designed for its specific context.

The goal: intricate minimalism with appropriate personality. Same quality bar, context-driven execution.
