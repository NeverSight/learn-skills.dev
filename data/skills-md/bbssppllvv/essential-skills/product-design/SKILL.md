---
name: product-design
description: >
  Product design best practices — typography, color, spacing, motion, icons, accessibility,
  and craft details for professional web/mobile UI. Prevents generic "AI slop" designs through
  intentional, research-grounded decisions. Use when: (1) designing or building UI screens,
  dashboards, landing pages, or components, (2) reviewing UI for quality and polish,
  (3) setting up a design system (tokens, scales, palettes), (4) implementing CSS/frontend
  with professional-grade craft, (5) any task involving visual design quality, typography
  choices, color palettes, animation/motion, icon systems, or accessibility.
  Triggers on: UI design, product design, design system, typography, color palette,
  spacing system, motion/animation, icons, dark mode, accessibility, anti-AI-slop,
  design review, visual polish, CSS tokens, responsive design.
---

# Product Design Best Practices

Professional design methodology. Don't guess — make intentional, justified decisions.

> Always ask: "If I showed this to 10 users tomorrow, what would they remember?"

## Before You Design: Discovery

**Never design blind.** Answer these first:

```
1. WHAT are we building?    → Screen type, platform, scope
2. WHO is this for?         → Audience, technical level
3. WHAT should users do?    → Primary action, success metric
4. WHAT feeling to evoke?   → Tone, energy
5. WHAT JOB does this do?   → "Help me decide" / "Convince me" / "Get me started"
6. WHAT objections exist?   → "Is it worth it?" / "Is it legit?" / "Will it work?"
7. WHAT should they remember? → The hook, the differentiator
8. ANY constraints?         → Brand, tech requirements, inspirations
```

**Design Brief:** "I'm designing a **[WHAT]** for **[WHO]** that helps them **[GOAL]** and should feel **[TONE]**."

---

## Design Workflow

```
0. DISCOVER  → Design Brief
       ↓
1. RESEARCH  → Study real products, competitors, best-in-class examples
       ↓
2. ANALYZE   → Extract patterns, compare approaches, make decisions
       ↓
3. DESIGN    → Apply craft: typography, color, spacing, copy, soul
       ↓
4. IMPLEMENT → Build, validate against quality gates
```

---

## Research & Analysis

### Research ≠ Copying the Average

Research is about understanding WHY choices work, not copying WHAT everyone does.

- Best practices = starting point, not destination
- "Safe" often = "forgettable"
- Document reasoning: "Most use X, but we chose Y because..."

### Three Lenses (Use All)

**Lens A: Structure** — Layout, components, information hierarchy. Common solutions to common problems.

**Lens B: Visual Craft** — For each strong reference, notice:
1. Typography — fonts, sizes, weights, letter-spacing
2. Color — warm or cool? Accent? Hierarchy?
3. Spacing — tight or airy? What's the rhythm?
4. Details — shadows, borders, radii, gradients
5. Icons/illustrations — style? Consistent?
6. Overall vibe — premium? Playful? Technical?

**Lens C: Conversion & Soul** — What makes this one WORK?
1. What's the HOOK in the first 3 seconds?
2. How do they handle OBJECTIONS?
3. Where's the TRUST (social proof, guarantees)?
4. What's UNIQUE?
5. What MICROCOPY has personality?
6. What would a user REMEMBER tomorrow?

### Steal List (Minimum 5 Items)

| Source | What | Why It Works | How I'll Use It |
|--------|------|--------------|-----------------|
| ... | Specific tactic with exact copy/numbers | Psychology behind it | Adaptation plan |

**Be specific, not vague:**
- "Linear — 13px/20px body, -0.01em tracking, 48px section gaps, #5E6AD2 accent at 8% opacity for hover"
- NOT "Linear — clean design"

---

## Typography

**Scale:** Ratio 1.2 (minor third). Max 6–8 sizes: Display (48–64px), H1 (36–48px), H2 (24–32px), Body (16–18px), Small (13–14px), Caption (11–12px).

**Leading:** Large text = tight (1.0–1.2). Body = loose (1.5–1.6).

**Letter-spacing — DO NOT SKIP:**

| Text Type | Letter-spacing |
|-----------|----------------|
| Body (14–18px) | `0` |
| Small text (11–13px) | `0.01–0.02em` — **required** |
| UI labels/buttons | `0.02em` — **required** |
| ALL CAPS | `0.06–0.1em` — **always required** |
| Large headings (32px+) | `-0.01` to `-0.02em` |
| Display (48px+) | `-0.02` to `-0.03em` |

**Line length:** 50–75 chars (`max-width: 65ch`). **Pairing:** Max 2 fonts.

> Full guide: [references/typography.md](references/typography.md)

## Color

**Palette:** 4 layers — Neutrals (70–90%), Primary accent (5–10%), Semantic (success/warning/danger), Effects (rare).

**Primary:** One brand color with scale (50–950). 600 default, 700 hover, 800 active.

**Contrast:** 4.5:1 body text, 3:1 large text.

**Dark theme:** Not inverted. Background `#0f0f0f`, not `#000`. Text `#f0f0f0`, not `#fff`. Separate neutral scale.

**Tokens:** Name by purpose (`--primary`), not color (`--blue`).

> Full guide: [references/color.md](references/color.md)

## Spacing

**Base unit:** 4px or 8px. Everything multiplies from this.

```
4px: 4, 8, 12, 16, 24, 32, 48, 64, 96
8px: 8, 16, 24, 32, 48, 64, 96, 128
```

**Proximity = relationship.** Closer = connected, farther = separate.

**Density:** Match spacing to context — dense for dashboards (8-12px padding), default for product UI (16-24px), spacious for marketing (24-32px).

**Responsive:** Structural spacing (sections, containers) scales down 0.5-0.75x on mobile. Internal component spacing (icon-to-text, button padding) stays fixed.

> Full guide: [references/spacing.md](references/spacing.md)

## Avoiding AI Slop

> **NO INDIGO/VIOLET** — Unless explicitly requested. Every LLM defaults to indigo (#6366f1). It's the biggest tell of AI-generated design. Choose brand-appropriate colors from research.

**Generic (bad):** default fonts, safe blue gradients, perfect symmetry, blob backgrounds, stock illustrations.

**Professional (good):** brand-appropriate color, intentional font pairing, visual tension/asymmetry, purposeful whitespace, custom imagery, social proof present.

**Generic structure trap:** Don't default to Hero → Features → Pricing → FAQ → CTA. Ask: "What can I add, remove, or reorder for THIS product?"

> Full guide: [references/anti-ai-slop.md](references/anti-ai-slop.md)

## Motion

Motion serves: **Feedback** (it worked), **Continuity** (where it went), **Hierarchy** (look here). If it doesn't do one — remove it.

| Category | Duration |
|----------|----------|
| Instant (hover, press, toggle) | 90–150ms |
| State change (accordion, tabs) | 160–240ms |
| Large transition (modal, drawer) | 240–360ms |

**Easing:** Enter = ease-out, Exit = ease-in, Change = ease-in-out.

**Required:** `prefers-reduced-motion` support. No animation > 500ms in product UI. Never `transition: all`.

> Full guide: [references/motion.md](references/motion.md)

## Icons

One style per product (outline OR solid). No mixing libraries.

**Optical corrections:** Geometric center ≠ visual center. Arrows/chevrons need 0.5–1px shift.

**Color:** `currentColor` by default. Semantic colors only for status.

**Accessibility:** Action icons need `aria-label`. Hit area 44×44px minimum.

**Libraries:** Lucide (SaaS default), Heroicons (Tailwind), Material Symbols, SF Symbols (Apple).

> Full guide: [references/icons.md](references/icons.md)

## The Persuasion Layer

**Fill this table before writing code:**

| Element | Your Answer |
|---------|-------------|
| **Hook** (first 3 sec) | Hero headline + visual |
| **Story arc** | Problem → Solution → Proof → Action |
| **Objection killers** | 1. ___ 2. ___ 3. ___ |
| **Trust signals** | Social proof / Guarantee / Security / Specifics (pick 2+) |
| **Urgency/Scarcity** | ___ or "N/A" |
| **The memorable thing** | What will they screenshot? |

**If you can't fill this table, you're designing decoration, not persuasion.**

## The Soul

~80% proven patterns + ~20% unique choices.

- One bold visual choice (color, type treatment, illustration style)
- Voice and personality in copy
- Micro-interactions that surprise
- One detail users will remember

**Test:** "If someone screenshots this, would they know it's from THIS product?"

---

## Implementation Quality Gate

| Category | Check |
|----------|-------|
| **Functional** | Primary action obvious? Error states? Works on mobile? |
| **Visual** | Squint test passes? Spacing rhythm? Typography intentional? |
| **Persuasion** | Hook in 3 sec? 2+ trust signals? Objections addressed? |
| **Polish** | No orphaned words? Icons aligned? Buttons consistent? |

> Implementation details (focus states, forms, images, touch, performance, accessibility): [references/craft-details.md](references/craft-details.md)

---

## Reference Files

| Guide | What's Inside |
|-------|---------------|
| [typography.md](references/typography.md) | Scale, pairing, weight, line-height, letter-spacing, responsive type, tokens |
| [color.md](references/color.md) | Palette structure, neutrals, primary/semantic colors, dark theme, OKLCH, tokens |
| [spacing.md](references/spacing.md) | Spacing scale, component patterns, density, proximity, responsive adjustments |
| [motion.md](references/motion.md) | Micro-interactions, timing, easing, reduced motion, animation tokens |
| [icons.md](references/icons.md) | Grid system, optical corrections, accessibility, icon+text pairing, libraries |
| [craft-details.md](references/craft-details.md) | Focus states, forms, images, touch, performance, accessibility, navigation |
| [anti-ai-slop.md](references/anti-ai-slop.md) | What makes designs look generic and how to avoid it |
