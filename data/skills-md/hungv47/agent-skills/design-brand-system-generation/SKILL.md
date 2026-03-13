---
name: design-brand-system-generation
description: This skill should be used when the user asks to "create a design system", "build brand identity", "create brand guidelines", "define brand voice", "define design tokens", "create typography system", "define color palette", "create component patterns", "design UI system", "generate style guide", "brand strategy", "brand personality", "brand archetype", or mentions design system, brand identity, brand guidelines, brand voice, brand personality, design tokens, typography, color palette, component specifications, or visual design standards. Transforms product documentation into comprehensive brand identity and design systems — from strategy and personality to visual identity, design tokens, and component specifications.
license: MIT
metadata:
  author: hungv47
  version: "3.0.0"
---

# Brand Identity & Design System Generator

Transform product artifacts into a complete brand identity and design system — from strategy and personality to visual identity, design tokens, and component patterns — that feels so inevitable users think "of course, how else would it be?"

## Philosophy

A brand is not a logo. A brand is not a color palette. A brand is the gut feeling people have about your product, company, or service. A design system is the precise implementation of that feeling in code. This skill produces both.

Work from the inside out:

1. **Strategy first** — Who are you, why do you exist, who do you serve, and what makes you different?
2. **Personality second** — If your brand were a person, what kind of person? What archetype?
3. **Voice third** — How does that person speak? What do they say and how?
4. **Visual identity fourth** — What does that person look like? Logo, color, type, imagery.
5. **Design tokens fifth** — The precise, implementable specifications for digital products.
6. **Component patterns last** — How tokens compose into reusable UI components.

Every visual, verbal, and technical decision must trace back to strategy. If you can't explain *why* a color, font, token, or word was chosen, it's decoration, not identity.

## Input Requirements

Gather from the user:

**Required:**
- Product description or PRD (what the product does, who it serves)
- Target audience profile (demographics, psychographics, context of use)
- Competitive context (who else serves this audience, how they're positioned)

**Strongly Recommended:**
- Existing brand assets if any (logos, colors, fonts, past guidelines)
- Founder/team values and origin story
- Key differentiators (what makes this genuinely different)
- User flow or key screens/wireframes

**Helpful:**
- Admired brands (who they want to feel like, and who they DON'T)
- Market positioning intent (premium, accessible, disruptive, trusted, etc.)

If missing critical inputs, ask. Don't hallucinate audience or product details.

---

# Part I: Brand Identity

---

## 1. Brand Strategy Foundation

The bedrock everything else is built on.

### Purpose, Mission, Vision

```
BRAND PURPOSE (Why we exist — beyond making money)
---------------------------------------------------
[One sentence. The fundamental reason this brand exists.]

MISSION (What we do, for whom, and how)
----------------------------------------
[One to two sentences. Present-tense, action-oriented.]

VISION (Where we're headed — the future state we're building toward)
--------------------------------------------------------------------
[One sentence. Aspirational but believable.]
```

**Example:**
```
PURPOSE: To make personal finance feel empowering, not shameful.
MISSION: We help young professionals build financial confidence through honest tools and zero-judgment education.
VISION: A world where everyone feels in control of their money by 30.
```

### Core Values

Define 3-5 values. Each must be specific enough to guide real decisions (not generic like "innovation" or "excellence").

```
VALUES
------
1. [Value]: [What it means in practice — a specific behavioral standard]
2. [Value]: [What it means in practice]
3. [Value]: [What it means in practice]
```

**Test**: If the opposite of a value is obviously stupid ("we value quality" — who values bad quality?), it's too generic. Good values have a real tradeoff ("we value transparency over comfort" — some companies genuinely choose comfort over transparency).

### Brand Positioning

```
POSITIONING STATEMENT
---------------------
For [target audience],
[brand name] is the only [category/competitive frame]
that [primary point of difference]
because [reasons to believe / proof points].

BRAND PROMISE
-------------
[One sentence. The single most important commitment to customers.]

VALUE PROPOSITION
-----------------
We help [who] do [what] by [how], so they can [outcome/benefit].
```

### Competitive Landscape

```
PERCEPTUAL MAP
--------------
Axis 1: [dimension, e.g., Affordable ←→ Premium]
Axis 2: [dimension, e.g., Traditional ←→ Innovative]

Our position: [where on the map and why]
White space: [what opportunity this position exploits]

KEY COMPETITORS:
- [Competitor A]: positioned as [description]. Their weakness: [gap we exploit].
- [Competitor B]: positioned as [description]. Their weakness: [gap we exploit].
```

---

## 2. Brand Personality & Archetype

A brand's personality determines everything downstream — visual choices, voice, tone, imagery, and token decisions. Define it precisely.

### Brand Archetype

Select one primary and one secondary archetype from the 12 Jungian archetypes. Use a 70/30 blend — primary archetype dominates, secondary adds nuance and differentiation.

Reference `references/brand-archetypes.md` for the complete archetype guide with visual and verbal mappings.

```
BRAND ARCHETYPE
---------------
Primary (70%): [Archetype] — [why this fits the brand's core desire and strategy]
Secondary (30%): [Archetype] — [what nuance this adds]

Archetype in action:
- How we inspire: [behavior]
- How we communicate: [style]
- How we make people feel: [emotion]
- What we'd never do: [anti-behavior]
```

### Brand Personality Traits

Define 3-5 personality traits using the "trait, but not" format to prevent misinterpretation.

```
PERSONALITY TRAITS
------------------
1. [Trait] — but not [opposite extreme to avoid]
   In practice: [specific example of how this shows up]

2. [Trait] — but not [opposite extreme]
   In practice: [specific example]

3. [Trait] — but not [opposite extreme]
   In practice: [specific example]
```

### Emotional Journey Map

```
AUDIENCE EMOTIONAL MAPPING
--------------------------
Before product: [emotional state — frustration, confusion, desire, shame, etc.]
During product: [transformation happening — clarity, relief, excitement, etc.]
After product: [desired emotional outcome — empowerment, confidence, pride, etc.]

CORE TENSION: [what problem/desire the product resolves]
DESIGN PROMISE: [one sentence — what the entire brand experience must communicate]
```

---

## 3. Brand Voice & Tone

Voice is constant — the brand's personality expressed through words. Tone is variable — it shifts based on context, audience, and situation.

Reference `references/brand-voice.md` for complete frameworks.

### Voice Attributes

Define 3-5 voice attributes using the voice chart format:

```
VOICE CHART
-----------
| Attribute    | Description                              | Do                                  | Don't                              |
|-------------|------------------------------------------|-------------------------------------|-------------------------------------|
| [Attribute] | [What this means for our brand]          | [Specific example of doing it right]| [Specific example of doing it wrong]|
| [Attribute] | [What this means]                        | [Do example]                        | [Don't example]                     |
| [Attribute] | [What this means]                        | [Do example]                        | [Don't example]                     |
```

### Tone Spectrum

Map how tone shifts across the four NN/g dimensions depending on context:

```
TONE DIMENSIONS
---------------
                    ← Our range →
Formal     [---|===|------] Casual
Serious    [-----|==|------] Funny
Respectful [---|====|-----] Irreverent
Enthusiastic [----|===|---] Matter-of-fact

TONE BY CONTEXT:
- Marketing / landing pages: [position on each spectrum]
- Product UI / in-app: [position]
- Help docs / support: [position]
- Error messages: [position]
- Social media: [position]
```

### Writing Guidelines

```
ON-BRAND vs. OFF-BRAND:
| Context         | On-brand ✓                                    | Off-brand ✗                              |
|----------------|-----------------------------------------------|------------------------------------------|
| Welcome email  | "[on-brand example]"                          | "[off-brand example]"                    |
| Error message  | "[on-brand example]"                          | "[off-brand example]"                    |
| CTA button     | "[on-brand example]"                          | "[off-brand example]"                    |
```

---

## 4. Messaging Architecture

The hierarchy of what the brand says, from most compressed to most expanded.

```
MESSAGING HIERARCHY
===================

TAGLINE (2-7 words):
[The big idea, compressed. Memorable, ownable, evocative.]

ELEVATOR PITCH (25 words / 20 seconds spoken):
[What you do, for whom, and why it matters — one breath.]

VALUE PROPOSITION (1-2 sentences):
[Functional and emotional benefits articulated clearly.]

MESSAGING PILLARS (3-5 pillars):

Pillar 1: [Headline]
  Narrative: [2-3 sentences expanding the idea]
  Proof points:
  - [Evidence, stat, or feature that proves it]
  - [Evidence]

Pillar 2: [Headline]
  Narrative: [2-3 sentences]
  Proof points:
  - [Evidence]
  - [Evidence]

Pillar 3: [Headline]
  Narrative: [2-3 sentences]
  Proof points:
  - [Evidence]
  - [Evidence]

BOILERPLATE DESCRIPTIONS:
- One-liner (10 words): [description]
- Short (50 words): [description]
- Standard (100 words): [description]
- Full (200 words): [description]
```

---

## 5. Visual Identity System

Every visual decision traces back to archetype, personality, and positioning. This is where strategy becomes visible.

Reference `references/visual-identity.md` for detailed rules on logo systems, imagery, and iconography.

### Logo System

```
LOGO SYSTEM
-----------
Primary logo: [Full lockup — wordmark + symbol]
Secondary logo: [Alternate layout — stacked or horizontal variant]
Logomark: [Symbol/icon standalone — for small spaces, favicons, app icons]
Wordmark: [Text-only version]

CLEAR SPACE: Defined by [relative unit]. Minimum [1.5x] on all sides.
MINIMUM SIZE: Print [width]. Digital [height px].

COLOR VARIATIONS:
- Full color on light, full color on dark, single-color black, single-color white

DO NOT: Stretch, recolor, add effects, rotate, crop, place on busy backgrounds.
```

### Color System

Colors must serve the emotional journey and archetype. Reference `references/color-emotion.md` for color psychology and `references/brand-archetypes.md` for archetype-to-color mapping.

```
COLOR SYSTEM
============
PRIMARY (1-2 colors — 60% usage):
  [Name]: [hex] / [oklch] / [Pantone] / [CMYK] / [RGB]
  Emotional purpose: [why — traced to archetype and positioning]

SECONDARY (1-3 colors — 30% usage):
  [Name]: [values]
  Role: [supporting purpose]

ACCENT (1-2 colors — 10% usage):
  [Name]: [values]
  Role: [CTAs, highlights, celebration moments]

SEMANTIC:
  Success: [hex] — completion, positive feedback
  Warning: [hex] — caution, attention needed
  Error:   [hex] — problems, blockers
  Info:    [hex] — neutral information

NEUTRALS:
  [Full scale from near-white to near-black]
  See references/token-architecture.md for neutral base presets
```

Provide color values in all formats: Hex, OKLCH, Pantone, CMYK, RGB.

### Typography System

Select fonts that embody the archetype and personality. Reference `references/typography-psychology.md`.

```
TYPOGRAPHY SYSTEM
=================
DISPLAY / HEADING: [Font] — [why it fits archetype/personality]
  Weights: [specific weights]

BODY / TEXT: [Font] — [why it fits]
  Weights: [specific weights]

MONO (if needed): [Font]

TYPE HIERARCHY:
  H1: [size/weight/line-height/letter-spacing]
  H2-H3: [specs]
  Body: [specs]
  Small/Caption: [specs]
  Label/Overline: [specs]

RULES:
- Maximum 2 font families (3 if mono needed)
- Maximum line width: 65-75 characters
- Never use display fonts for body text
```

### Imagery & Photography Direction

```
PHOTOGRAPHY STYLE
=================
Mood: [3-5 keywords — traced to archetype]
Lighting: [natural/studio, soft/hard, warm/cool]
Color treatment: [saturated, muted, brand-tinted, B&W policy]
Subjects: [types of people, environments, contexts]
Composition: [framing, depth of field, point of view]
```

### Iconography & Graphic Elements

```
ICON STYLE: [line/filled/duotone] | Stroke: [weight] | Grid: [size] | Color: [rule]

BRAND DEVICES: Patterns, shapes, textures, gradients — with usage rules.
```

---

# Part II: Design System

---

## 6. Token Architecture

Translate the visual identity from Part I into precise, implementable tokens using a **three-layer system** inspired by shadcn/ui and the W3C Design Tokens specification.

```
PRIMITIVE (what exists)     →  color.blue.500, spacing.4, font.size.md
     ↓
SEMANTIC (what it means)    →  --primary, --muted-foreground, --border
     ↓
COMPONENT (where it goes)   →  button.primary.background, input.border.default
```

**The background/foreground convention**: Every semantic role comes as a pair. The base name (e.g., `--primary`) is the background/fill. The `-foreground` suffix (e.g., `--primary-foreground`) is the text/icon color on that surface. Always pair them: `bg-primary text-primary-foreground`.

**Color format**: Use OKLCH as the primary color space. Provide hex fallbacks for readability.

See `references/token-architecture.md` for the complete specification, neutral base presets, and OKLCH reference.

---

## 7. Primitive Tokens

The raw palette — all available values before semantic meaning. Derived directly from the visual identity in Part I.

### Neutral Base

Select from the presets. Each creates a distinct feel connected to archetype:

| Base | Undertone | Feels Like | Archetype Fit |
|------|-----------|------------|---------------|
| Neutral | Pure gray | Clean, stark, digital-native | Creator, Sage |
| Stone | Warm gray | Grounded, earthy, natural | Explorer, Caregiver, Everyman |
| Zinc | Cool gray | Industrial, precise, technical | Ruler, Hero |
| Gray | Blue-gray | Corporate, reliable, familiar | Everyman, Sage |
| Slate | Blue-tinted | Professional, established, calm | Ruler, Sage, Caregiver |

```
NEUTRAL BASE: [selected base]

Light mode scale:
  50:  [oklch] / [hex]    -- Backgrounds, subtle fills
  100: [oklch] / [hex]    -- Alternate backgrounds
  200: [oklch] / [hex]    -- Borders, dividers
  300: [oklch] / [hex]    -- Disabled text, placeholders
  400: [oklch] / [hex]    -- Muted text
  500: [oklch] / [hex]    -- Secondary text
  600: [oklch] / [hex]    -- Body text (light bg)
  700: [oklch] / [hex]    -- Headings
  800: [oklch] / [hex]    -- High emphasis
  900: [oklch] / [hex]    -- Maximum emphasis
  950: [oklch] / [hex]    -- Near-black

Dark mode scale: [reversed with adjusted lightness/chroma]
```

### Brand Color Primitives

```
Primary scale (50-950): [oklch + hex, derived from brand color system]
Secondary scale (50-950): [if brand demands a second hue]
Accent scale (50-950): [for delight, celebration, highlights]
Destructive scale (50-950): [reds for error/danger states]
```

### Typography Primitives

```
FONT FAMILIES: Display: [Font] | Body: [Font] | Mono: [Font]

SIZE SCALE (base 16px):
  xs: 12px/0.75rem  sm: 14px/0.875rem  base: 16px/1rem  lg: 18px/1.125rem
  xl: 20px/1.25rem  2xl: 24px/1.5rem   3xl: 30px/1.875rem  4xl: 36px/2.25rem  5xl: 48px/3rem

WEIGHT: regular(400) medium(500) semibold(600) bold(700)
LINE HEIGHT: tight(1.25) normal(1.5) relaxed(1.75)
LETTER SPACING: tight(-0.025em) normal(0) wide(0.025em)
```

### Spacing & Radius Primitives

```
SPACING (base 4px):
  0:0  1:4px  2:8px  3:12px  4:16px  5:20px  6:24px  8:32px  10:40px  12:48px  16:64px  20:80px  24:96px

RADIUS: none(0) sm(4px) md(6px) lg(8px) xl(12px) 2xl(16px) full(9999px)
```

---

## 8. Semantic Tokens

Map primitives to UI roles. This is the design system's API — the contract between brand decisions and implementation.

### The Complete Semantic Token Map

```
SEMANTIC TOKENS (light / dark)
==============================

--- Core Surfaces ---
--background:            [page background]
--foreground:            [default text on page background]

--card:                  [card/elevated surface]
--card-foreground:       [text on card]

--popover:               [dropdown/tooltip/overlay surface]
--popover-foreground:    [text on popover]

--- Interactive ---
--primary:               [main brand action — buttons, links]
--primary-foreground:    [text/icon on primary]

--secondary:             [secondary actions, subtle buttons]
--secondary-foreground:  [text on secondary]

--accent:                [hover highlights, subtle emphasis]
--accent-foreground:     [text on accent]

--destructive:           [danger/error actions]
--destructive-foreground:[text on destructive]

--muted:                 [disabled backgrounds, subtle fills]
--muted-foreground:      [placeholder text, disabled text, captions]

--- Structural ---
--border:                [default border color]
--input:                 [input field border color]
--ring:                  [focus ring color]

--- Global Shape ---
--radius:                [global border radius — brand personality]

--- Data Visualization ---
--chart-1 through --chart-5

--- Sidebar (complex apps) ---
--sidebar / --sidebar-foreground
--sidebar-primary / --sidebar-primary-foreground
--sidebar-accent / --sidebar-accent-foreground
--sidebar-border / --sidebar-ring
```

**Radius as brand personality** (connected to archetype):

| Radius | Personality | Archetype Fit |
|--------|------------|---------------|
| 0 | Sharp, serious, enterprise | Ruler, Outlaw |
| 0.25rem | Professional, restrained | Sage, Hero |
| 0.375rem | Balanced, modern default | Creator, Explorer |
| 0.5rem | Friendly, approachable | Everyman, Caregiver |
| 0.75rem | Soft, consumer-friendly | Innocent, Lover |
| 1rem+ | Playful, app-like | Jester, Magician |

### Mapping Example

Show explicitly how brand identity decisions become implementable tokens:

```
MAPPING: Brand Identity → Primitives → Semantic Tokens
========================================================
Given: Hero archetype, primary = blue, neutral base = slate

Light Mode:
  --background:           slate.50     oklch(0.984 0.003 247)  / #f8fafc
  --foreground:           slate.950    oklch(0.129 0.042 264)  / #020617
  --primary:              blue.600     oklch(0.546 0.245 262)  / #2563eb
  --primary-foreground:   white        oklch(1 0 0)            / #ffffff
  --secondary:            slate.100    oklch(0.968 0.007 247)  / #f1f5f9
  --secondary-foreground: slate.900    oklch(0.208 0.042 265)  / #0f172a
  --accent:               slate.100    oklch(0.968 0.007 247)  / #f1f5f9
  --accent-foreground:    slate.900    oklch(0.208 0.042 265)  / #0f172a
  --destructive:          red.600      oklch(0.577 0.245 27)   / #dc2626
  --destructive-foreground: white      oklch(1 0 0)            / #ffffff
  --muted:                slate.100    oklch(0.968 0.007 247)  / #f1f5f9
  --muted-foreground:     slate.500    oklch(0.554 0.046 257)  / #64748b
  --border:               slate.200    oklch(0.929 0.013 255)  / #e2e8f0
  --input:                slate.200    oklch(0.929 0.013 255)  / #e2e8f0
  --ring:                 blue.600     oklch(0.546 0.245 262)  / #2563eb
  --radius:               0.25rem      (sharp — Hero archetype)

Dark Mode:
  --background:           slate.950    oklch(0.129 0.042 264)  / #020617
  --foreground:           slate.50     oklch(0.984 0.003 247)  / #f8fafc
  --primary:              blue.500     oklch(0.623 0.214 259)  / #3b82f6
  --primary-foreground:   slate.950    oklch(0.129 0.042 264)  / #020617
  --muted:                slate.800    oklch(0.279 0.041 260)  / #1e293b
  --muted-foreground:     slate.400    oklch(0.704 0.04 256)   / #94a3b8
  --border:               slate.800    oklch(0.279 0.041 260)  / #1e293b
  --input:                slate.800    oklch(0.279 0.041 260)  / #1e293b
  --ring:                 blue.500     oklch(0.623 0.214 259)  / #3b82f6
  --radius:               0.25rem
```

---

## 9. Component Tokens & Patterns

Map semantic tokens to specific components. Reference `references/component-patterns.md` for full patterns with token consumption maps.

### Component Token Map

```
COMPONENT TOKENS
================
button.primary.background:     var(--primary)
button.primary.foreground:     var(--primary-foreground)
button.primary.hover:          [primary with adjusted lightness]
button.secondary.background:   var(--secondary)
button.secondary.foreground:   var(--secondary-foreground)
button.destructive.background: var(--destructive)
button.destructive.foreground: var(--destructive-foreground)
button.ghost.background:       transparent
button.ghost.foreground:       var(--foreground)
button.ghost.hover:            var(--accent)

input.background:              var(--background)
input.border:                  var(--input)
input.border.focus:            var(--ring)
input.placeholder:             var(--muted-foreground)

card.background:               var(--card)
card.foreground:               var(--card-foreground)
card.border:                   var(--border)

badge.default.background:      var(--primary)
badge.default.foreground:      var(--primary-foreground)
badge.secondary.background:    var(--secondary)
badge.secondary.foreground:    var(--secondary-foreground)
badge.destructive.background:  var(--destructive)
badge.destructive.foreground:  var(--destructive-foreground)
badge.outline.background:      transparent
badge.outline.border:          var(--border)
```

### Buttons

```
BUTTON HIERARCHY
----------------
1. PRIMARY (one per view max)
   Tokens: bg-primary text-primary-foreground
   Hover: primary with +5% lightness
   Use: The ONE action you want users to take

2. SECONDARY
   Tokens: bg-secondary text-secondary-foreground
   Hover: secondary with +5% lightness
   Use: Alternative valid paths

3. DESTRUCTIVE
   Tokens: bg-destructive text-destructive-foreground
   Use: Delete, remove, cancel subscription

4. OUTLINE
   Tokens: border-input bg-background text-foreground
   Hover: bg-accent text-accent-foreground
   Use: Lower-priority actions

5. GHOST
   Tokens: bg-transparent text-foreground
   Hover: bg-accent text-accent-foreground
   Use: Toolbar actions, inline actions

6. LINK
   Tokens: text-primary underline
   Use: Inline text actions

BUTTON SIZES:
  sm:   h-8 px-3 text-xs     rounded-[calc(var(--radius)-2px)]
  md:   h-9 px-4 text-sm     rounded-[var(--radius)]
  lg:   h-10 px-6 text-sm    rounded-[var(--radius)]
  xl:   h-11 px-8 text-base  rounded-[var(--radius)]
  icon: h-9 w-9              rounded-[var(--radius)]
```

### Form Elements

```
INPUT FIELDS
------------
Height: h-9 (36px) to h-10 (40px)
Padding: px-3 py-1
Border: 1px solid var(--input)
Focus: ring-2 ring-[var(--ring)] ring-offset-2
Radius: rounded-[var(--radius)]
Background: var(--background)
Text: var(--foreground)
Placeholder: var(--muted-foreground)

Label: text-sm font-medium text-foreground
Helper: text-xs text-muted-foreground
Error: text-xs text-destructive

VALIDATION:
- Inline on blur, not keystroke
- Error: border-destructive + error message below
- Success: subtle checkmark (optional)
```

### Cards

```
CARD SPECIFICATION
------------------
Background: var(--card)
Border: 1px solid var(--border)
Radius: rounded-[var(--radius)]
Shadow: sm (light mode), none (dark mode)
Padding: p-6

Card Header: pb-2
Card Title: text-lg font-semibold text-card-foreground
Card Description: text-sm text-muted-foreground
Card Content: pt-0
Card Footer: pt-4 flex items-center
```

---

## 10. Motion & Interaction

```
MOTION PRINCIPLES
-----------------
Purpose: Guide attention, provide feedback, create delight
Never: Delay users, distract from content, add without purpose

TIMING TOKENS:
  instant: 0ms       -- State changes, toggles
  fast:    100-150ms  -- Micro-interactions, hovers, focus rings
  normal:  200-300ms  -- Transitions, reveals, collapses
  slow:    400-500ms  -- Page transitions, celebrations

EASING:
  ease-out:    entering elements (decelerate in)
  ease-in:     exiting elements (accelerate out)
  ease-in-out: moving elements, layout shifts
  spring:      playful interactions (if archetype supports it — Jester, Magician)

INTERACTION FEEDBACK:
  Button press:  scale(0.98) + slight darken, fast timing
  Hover:         background token shift (e.g., accent), fast timing
  Focus:         ring-2 ring-[var(--ring)] ring-offset-2, instant
  Success:       brief pulse or checkmark, normal timing
  Error:         subtle shake (2px, 3 cycles), fast timing
  Loading:       skeleton shimmer or spinner, never frozen UI
  Accordion:     height transition, normal timing, ease-out
```

---

## 11. Accessibility Baseline

```
CONTRAST REQUIREMENTS (WCAG 2.1 AA):
  Normal text (<18px):     4.5:1 minimum
  Large text (18px+ bold): 3:1 minimum
  UI components:           3:1 minimum
  Focus indicators:        3:1 against adjacent colors

INTERACTIVE TARGETS:
  Minimum: 44x44px touch targets (WCAG 2.5.8)
  Spacing: 8px minimum between targets

FOCUS STATES:
  Visible focus ring on ALL interactive elements
  Style: ring-2 ring-[var(--ring)] ring-offset-2 ring-offset-[var(--background)]
  Never remove focus outline without replacement

COLOR INDEPENDENCE:
  Never use color alone to convey meaning
  Pair color with: icons, text labels, patterns, or position

MOTION SAFETY:
  Respect prefers-reduced-motion
  Provide reduced/no-animation fallbacks for all transitions
```

---

## 12. Dark Mode Rules

Dark mode is not an afterthought — it's a parallel track built into the token system from step 1.

- Every semantic token MUST have both light and dark values
- Dark mode reduces saturation and shifts lightness, never inverts
- Surface hierarchy uses multiple levels (background → card → popover), not just "black"
- Primary colors shift lighter in dark mode for visibility
- Foreground colors flip (dark text → light text) maintaining contrast ratios
- Semantic colors (success, error, warning) preserve hue but adjust lightness
- Borders become more subtle (lower contrast against dark surfaces)
- Shadows are usually removed or replaced with subtle border differentiation

---

# Part III: Applications

---

## 13. Brand Applications

Show the brand identity and design system applied across key touchpoints.

```
APPLICATIONS
============

DIGITAL:
- Website: [key pages — homepage, product, about. Which tokens, which type hierarchy.]
- App: [icon, splash, key screens. How tokens map to native UI.]
- Social media: [profile images, cover images, post templates. Brand color + type usage.]
- Email: [signatures, newsletter templates.]
- Presentations: [slide templates. Logo placement, color usage, type.]

PRINT (if applicable):
- Business cards, stationery, marketing materials

ENVIRONMENTAL (if applicable):
- Signage, packaging, merchandise
```

---

## Process

1. **Gather** inputs — product docs, audience profile, competitive context, existing assets
2. **Define** strategy — purpose, mission, vision, values, positioning
3. **Select** archetype — primary + secondary, with rationale traced to strategy
4. **Establish** personality — 3-5 traits in "trait, but not" format
5. **Build** voice — voice chart, tone spectrum, writing guidelines
6. **Create** messaging — tagline through boilerplate, pillars with proof points
7. **Design** visual identity — logo, colors, type, imagery, icons, graphic elements
8. **Select** neutral base and define primitive token scales (colors in OKLCH, type, spacing, radius)
9. **Map** primitives to semantic tokens using background/foreground pairs
10. **Specify** component tokens and patterns referencing semantic layer
11. **Add** motion that matches brand personality
12. **Verify** every token pair meets WCAG AA; every decision traces back to strategy
13. **Document** dark mode values for every semantic token
14. **Show** applications — brand applied across touchpoints

## References

- `references/brand-archetypes.md` — 12 Jungian archetypes with visual and verbal mappings
- `references/brand-voice.md` — Voice frameworks, tone dimensions, messaging architecture
- `references/visual-identity.md` — Logo systems, imagery direction, iconography, graphic elements
- `references/token-architecture.md` — Three-layer token system, semantic token map, neutral presets
- `references/typography-psychology.md` — Font personality mappings and pairing rules
- `references/color-emotion.md` — Color psychology, OKLCH values, audience palettes
- `references/component-patterns.md` — UI component patterns with token consumption maps

## Anti-Patterns

### Brand Anti-Patterns
- **Visual-first thinking**: Choosing colors and fonts before defining strategy, personality, and voice. The brand will feel hollow.
- **Generic values**: "Innovation, quality, integrity" — every company claims these. Good values have real tradeoffs.
- **Archetype confusion**: Trying to be everything. Commit to one primary archetype. The secondary adds nuance, not contradiction.
- **Voice without examples**: Saying "we're friendly" means nothing without showing what friendly looks like in an error message, a CTA, a support reply.
- **The logo IS the brand**: A logo is one asset in a system. If you can only recognize a brand by its logo, the identity system has failed.

### Design System Anti-Patterns
- **Token soup**: ~20 semantic tokens cover an entire component library. More creates decision paralysis.
- **Skipping the semantic layer**: Never reference primitives directly in components. Always go through semantic tokens.
- **Mismatched pairs**: Using `bg-primary text-primary` instead of `bg-primary text-primary-foreground`.
- **Hex-only thinking**: Use OKLCH for perceptually uniform color manipulation. Hex is for readability.
- **Dark mode as inversion**: Flipping black/white is not dark mode. It requires deliberate surface hierarchy.
- **Radius inconsistency**: Use one global `--radius` value. All components derive from it.

### Shared Anti-Patterns
- **Color without purpose**: Every color must trace to archetype, positioning, or emotional journey.
- **Ignoring context**: A fitness app and a banking app need different energy even with similar demographics.
- **Trend-chasing**: Glassmorphism and purple gradients aren't personality. What's the actual brand intent?
- **Aesthetic without strategy**: Every decision — from tagline to token — should trace back to purpose, positioning, and archetype.
