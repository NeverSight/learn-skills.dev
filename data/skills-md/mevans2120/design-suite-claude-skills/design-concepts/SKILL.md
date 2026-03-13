---
name: design-concepts
description: Creates conceptual designs that illustrate design strategy and approach. Use when user says "mockup", "wireframe", "concept", "mood board", "visual direction", "design options", "explore designs", "UI design", "prototype", "design this", "show me designs", "create a design", "look and feel", or "design variations". Leverages research insights and design briefs to develop UI concepts, mood boards, and interactive prototypes. Do NOT use when user needs to understand users first (use design-research), is reviewing an implemented product (use design-qa), or is writing code.
---

# Design - Concepts

This skill guides Claude through creating conceptual designs that bridge research insights and production-ready code. Concepts communicate design direction, explore visual possibilities, and validate approaches before implementation.

## Core Methodology

### Purpose of Concept Design
Concept design is NOT final design - it's exploration and communication:
- **Explore possibilities**: Test multiple visual directions quickly
- **Communicate intent**: Show stakeholders what "good" could look like
- **Validate approach**: Get feedback before investing in implementation
- **Build alignment**: Create shared understanding of design direction

### Concept Design Process
1. **Brief Review**: Understand goals, constraints, research insights
2. **Design Intent Interview**: Uncover emotional and experiential goals
3. **Inspiration & Research**: Gather visual references from diverse sources
4. **Lens Selection**: Choose conceptual lenses that fit the project context
5. **Initial Concepts**: Develop 3 distinct concepts through chosen lenses (unless told otherwise)
6. **Presentation**: Create artifacts that tell the story and invite feedback
7. **Refinement** (if needed): Iterate on the chosen direction

### Why Multiple Concepts?
Creating 3 concept variations is standard design practice **when initially exploring**:
- **Divergent exploration**: Shows different strategic approaches, not just visual variations
- **Better decisions**: Stakeholders choose between meaningful alternatives
- **Reduced bias**: Multiple options prevent "approve this" vs. "which solves the problem best?"

**When to create 3 concepts vs. 1:**
- 3 concepts: First time designing a product/feature, exploring strategic direction, major redesigns
- 1 concept: Refining a chosen direction, iterating based on feedback, minor updates

**What makes concepts "different"?**
- Different information architecture
- Different interaction models
- Different navigation patterns
- Different content priorities
- Different emotional registers / aesthetic languages

## Step 1: Brief Review & Context Gathering

**Gather Context:**
```
Questions to ask user:
1. What research/insights should inform this concept?
2. What's the design challenge or goal?
3. Who's the audience for these concepts?
4. Any brand guidelines or design constraints?
5. What fidelity level? (wireframes/mockups/high-fi)
6. Is this initial exploration or refining an existing concept?
```

Use `view` to read:
- Research artifacts (personas, design principles)
- Existing brand guidelines
- Competitive analysis
- Design briefs or requirements

## Step 2: Design Intent Interview

**CRITICAL: Do this before any visual work.** These questions give Claude strong creative constraints that produce varied, contextually appropriate concepts.

Ask the user:

1. **Emotional target**: "What 3 adjectives describe how a user should *feel* when they use this?" (e.g., calm + confident + curious)
2. **Non-digital reference**: "Name a physical space, product, or experience (not a website) that captures the vibe you're going for." (e.g., "an Aesop store", "a Muji notebook", "a busy Tokyo train station")
3. **Anti-reference**: "What should this absolutely NOT feel like?" (e.g., "not clinical", "not playful/childish", "not enterprise-y")
4. **Design hero**: "Is there a specific brand, publication, or product whose aesthetic you admire *for this project*?" (doesn't need to be in the same industry)

These four inputs dramatically shape the design direction. If the user gives even partial answers, use them as strong constraints. If they can't answer, propose options based on the brief and research.

## Step 3: Inspiration & Research

Use web tools to gather current design patterns:
```
web_search: "best [industry] app ui design 2025"
web_search: "[design pattern] examples mobile"
web_fetch: Dribbble, Behance, Awwwards for visual inspiration
```

### Diverse Inspiration Sources

**CRITICAL: Go beyond the usual Dribbble/Behance cycle.** These sources produce sameness. Deliberately seek inspiration from:

- **Architecture & interiors**: Spatial relationships, material palettes, lighting moods
- **Print & editorial design**: Magazine layouts, book covers, poster typography
- **Physical product design**: Packaging, industrial design, material textures
- **Film & cinematography**: Color grading, framing, mood, title sequences
- **Fashion**: Color stories, seasonal palettes, texture combinations
- **Data visualization**: Information density approaches, chart aesthetics
- **Vintage graphic design**: Mid-century modern, art nouveau, constructivism
- **Cultural & regional design**: Japanese minimalism, Scandinavian functional, Latin American vibrancy
- **Nature & science**: Organic forms, crystalline structures, topographic patterns

**Design Provocation Step:** Before creating concepts, find 2-3 unexpected visual references from *outside digital design* that connect to the project's emotional goals from the Design Intent Interview. Document why each reference connects to the user's stated feelings.

### Mood Board Creation

**IMPORTANT: Mood boards MUST be visual HTML files, NOT markdown.**

Mood boards should include:
1. **Color Palette**: Actual color swatches with hex values and usage descriptions
2. **Typography Samples**: Real text at different sizes showing the font in use
3. **Imagery & Illustration Direction**: Per-concept photo treatment and illustration style (see below)
4. **Spacing Scale**: Visual representation of spacing units
5. **Component Examples**: Interactive examples showing hover states, transitions
6. **Non-Digital References**: Screenshots/descriptions of the inspiration sources from outside digital design
7. **Design Rationale**: Why these choices support user jobs and the emotional targets from the Design Intent Interview

**Imagery & Illustration Direction** — Each concept should define its own visual treatment for photos and illustrations, just like each uses a different font and color palette. Include in the mood board:
- **Photo treatment**: How photos are styled — warm overlays, desaturation, high-contrast B&W, duotone, color tinting, grain/noise, etc.
- **Illustration style**: What decorative elements accompany the concept — hand-drawn, geometric, botanical, art deco, minimal line art, halftone, etc.
- **Example pairings**: Show 1-2 sample photos with the treatment applied, alongside the illustration style, so the difference between concepts is visible in the mood board itself.

**Format**: Static HTML file (save as `.html`, NOT `.md`)

**DO NOT hardcode a specific theme into the template.** Let the project context, emotional targets, and references determine whether it's dark, light, warm, cool, etc.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mood Board - [Project Name]</title>
  <!-- Choose fonts based on project context, NOT defaults -->
  <style>
    /* Let the mood board's own aesthetic reflect the design direction */
    /* The mood board itself should FEEL like the concept */
  </style>
</head>
<body>
  <h1>Mood Board - [Project Name]</h1>

  <section>
    <h2>Emotional Targets</h2>
    <!-- The 3 adjectives from Design Intent Interview -->
    <!-- Non-digital reference and why it connects -->
  </section>

  <section>
    <h2>Color Palette</h2>
    <!-- Actual rendered swatches, not just hex codes -->
  </section>

  <section>
    <h2>Typography</h2>
    <!-- Real text rendered at size, not described -->
  </section>

  <section>
    <h2>Imagery & Illustration Direction</h2>
    <!-- Per-concept: photo treatment (overlays, filters, grain) -->
    <!-- Per-concept: illustration style (geometric, botanical, line art) -->
    <!-- Show example photos WITH the treatment applied -->
  </section>

  <section>
    <h2>Visual References</h2>
    <!-- Mix of digital and non-digital inspiration -->
    <!-- Explain WHY each reference connects to the emotional targets -->
  </section>

  <section>
    <h2>Component Examples</h2>
    <!-- Interactive examples with hover states -->
  </section>
</body>
</html>
```

## Step 4: Lens Selection

### The Design Lens System

Instead of always producing "Safe / Bold / Experimental" archetypes, select conceptual lenses that are appropriate to the project. Each lens produces a fundamentally different design approach.

**Select 3 lenses from the categories below** based on the project context, emotional targets, and user inputs. Mix across categories for maximum variety.

#### Aesthetic Lenses
| Lens | Character | Good For |
|------|-----------|----------|
| **Swiss/International** | Grid-precise, rational, typographic hierarchy | Data-heavy tools, dashboards, professional SaaS |
| **Editorial** | Magazine-like, asymmetric, bold typography, white space | Content platforms, portfolios, storytelling |
| **Brutalist** | Raw, honest, unconventional layouts, monospace | Developer tools, creative agencies, statements |
| **Japanese Minimal** | Generous white space, restraint, subtle detail | Wellness, luxury, meditation, premium products |
| **Retro-Futurism** | Vintage-meets-modern, neon, CRT aesthetics | Gaming, creative tools, entertainment |
| **Organic/Natural** | Soft shapes, earth tones, flowing layouts | Health, sustainability, community platforms |
| **Neo-Deco** | Geometric patterns, gold accents, dramatic contrast | Finance, luxury, high-end e-commerce |
| **Glassmorphism** | Frosted glass, depth, layered translucency | Modern dashboards, music apps, creative tools |
| **Scandinavian Functional** | Warm neutrals, clean lines, accessible, cozy | E-commerce, home, lifestyle, productivity |

#### Interaction Model Lenses
| Lens | Character | Good For |
|------|-----------|----------|
| **Single-Page Flow** | Everything on one scroll, progressive reveal | Landing pages, onboarding, simple tools |
| **Card-Based** | Modular, scannable, rearrangeable | Dashboards, content feeds, project management |
| **Sidebar Navigation** | Persistent nav, workspace feel, power-user | Complex apps, admin panels, dev tools |
| **Bottom Sheet Mobile** | Thumb-friendly, layered sheets, gesture-driven | Mobile-first, consumer apps |
| **Command Palette** | Keyboard-driven, search-first, minimal chrome | Developer tools, power-user apps |
| **Conversational** | Chat-like, step-by-step, guided | Onboarding, support, AI interfaces |

#### Content Strategy Lenses
| Lens | Character | Good For |
|------|-----------|----------|
| **Data-Dense** | High information density, compact, scannable | Analytics, trading, monitoring |
| **Story-Driven** | Narrative scroll, chapters, visual storytelling | Marketing, case studies, annual reports |
| **Tool/Utility** | Minimal chrome, content is the interface | Editors, calculators, code tools |
| **Discovery** | Browse-first, visual grid, serendipity | Marketplaces, media, social platforms |

### How to Select Lenses

1. Review the Design Intent Interview answers
2. Consider the product type and user context
3. Pick 3 lenses that are **meaningfully different from each other**
4. At least one should feel like a stretch — unexpected but defensible
5. Announce your lens selections to the user before building concepts

**Example:**
> For a healthcare appointment booking app where the user said "calm, trustworthy, effortless" and referenced "a well-organized pharmacy":
> - **Lens 1: Scandinavian Functional** — warm, accessible, clean
> - **Lens 2: Japanese Minimal** — serene, spacious, premium
> - **Lens 3: Conversational** — guided, step-by-step, approachable

Each lens produces a concept that feels like it was designed by a different designer with a different philosophy.

## Step 5: Creating Concepts

### Frontend Aesthetics — Avoiding "AI Slop"

**CRITICAL:** You tend to converge toward generic outputs. Make creative, distinctive frontends that surprise and delight.

**Typography** — Research fonts for each project. Do NOT fall back on the same familiar set every time.

**Before choosing fonts, you MUST:**
1. Run a web search for fonts that match the project's emotional targets and industry (e.g., `"best Google Fonts for [warm/bold/elegant] [restaurant/SaaS/editorial] design 2025"`)
2. Search for fonts used by the design heroes or non-digital references from the Design Intent Interview (e.g., `"fonts similar to [brand] typography"`)
3. Browse Google Fonts filtered by the aesthetic you need — look beyond page 1 results
4. Pick fonts you have NOT used in recent concepts for this user — track what you've already chosen and avoid repeating

**Selection criteria:**
- Does it match the emotional targets from the Design Intent Interview?
- Is it distinctive enough to give this project its own identity?
- Does it have the weights and styles needed (italic, bold, etc.)?
- Is it available on Google Fonts (or another free CDN) for easy embedding?
- Have you already used this font in another concept in this session? If yes, pick something else.

**Avoid these overused fonts:** Inter, Roboto, Arial, system fonts (unless contextually appropriate), Space Grotesk, Fraunces, Lora, Crimson Pro, Syne — and any font you find yourself reaching for by default

**Color & Theme** — Commit to a cohesive aesthetic:
- **Dominant + Accent**: 80% one color family, 20% sharp contrast
- **Monochrome + single hue**: Grayscale with one bold color for CTAs
- **Cultural aesthetics**: Draw from Brutalism, Memphis, Bauhaus, Vaporwave, etc.

**Avoid:** Purple gradients on white, generic blue + gray, pastel everything, rainbow palettes with equal distribution

**Motion** — Focus on high-impact moments:
- Page load orchestration with staggered reveals
- Transition between major states
- Hover effects on key interactive elements

**Backgrounds** — Create atmosphere:
- Gradient meshes, noise textures, geometric patterns
- Radial gradients, layered gradients, backdrop filters

**Photography & Illustration** — Each concept MUST have a distinct imagery approach, just like each has distinct typography and color. Do NOT reuse the same photo treatment or illustration style across concepts.

1. **Different photo treatment per concept** — Each lens implies a different way to handle photos. Examples: warm amber overlays for organic, high-contrast B&W or desaturated for editorial, duotone/color-tinted for themed, soft grain for vintage. Define the treatment in the mood board and apply it consistently in the concept.
2. **Different illustration style per concept** — Each concept should use a different decorative language. Examples: botanical SVGs for organic, bold geometric shapes for editorial, art deco line work for neo-deco, hand-drawn sketches for playful. Inline SVGs work well for HTML concepts.
3. **Use free, embeddable photo sources** — Unsplash (`images.unsplash.com` URLs) is preferred for hotlinking in HTML concepts. Pexels also works. Pixabay does NOT allow hotlinking.
4. **Always provide CSS gradient fallbacks** — Layer photos behind semi-transparent gradients so concepts still look complete if images fail to load.
5. **Note what you couldn't source** — If a concept needs imagery you can't find freely (venue-specific, custom illustration), use the best available alternative and note it for the client.

### Concept Format

**For Wireframes/Low-Fi:**
```html
<!-- Focus on layout, hierarchy, content structure -->
<!-- Use grayscale, simple shapes, annotate key decisions -->
```

**For Visual Mockups/Mid-Hi Fi:**
```jsx
// Use Tailwind for rapid styling
// Focus on key screens, not complete flows
// Include annotations explaining design decisions
```

**For Interactive Prototypes:**
```jsx
// Use React hooks for state management
// Create realistic interactions for key flows
// Add transition/animation for important interactions
```

### Per-Concept Requirements

Each concept MUST:
- Name its design lens explicitly
- Explain the strategic rationale (not just aesthetic choices)
- Connect back to the emotional targets from the Design Intent Interview
- Use a different font family from the other concepts
- Use a different color approach from the other concepts
- Annotate key decisions with WHY, tied to research insights

## Step 6: Presentation

### File Organization

**Organize all deliverables by feature/assignment in dated folders:**

```
docs/design/{feature-name}-concepts-{MMDDYY}/
├── {feature-name}-mood-board.html
├── {feature-name}-concept-1-{lens-name}.html or .jsx
├── {feature-name}-concept-2-{lens-name}.html or .jsx
├── {feature-name}-concept-3-{lens-name}.html or .jsx
└── {feature-name}-overview.md
```

**Feature Name Guidelines:**
- Use kebab-case (lowercase with hyphens)
- Ask the user for the feature name if not provided

### Design Concept Document

**File**: `{feature-name}-overview.md`

```markdown
# [Project Name] Design Concepts

## Design Challenge
[What problem are we solving? Who for? Why now?]

## Design Intent
- **Emotional targets**: [3 adjectives]
- **Non-digital reference**: [What they said and why it matters]
- **Anti-reference**: [What to avoid]
- **Design hero**: [Aesthetic inspiration]

## Key Research Insights
1. [Insight that informs these concepts]
2. [Another key insight]

## Concept 1: [Name] — [Lens Name]
**Lens**: [Which design lens and why it fits]
**Approach**: [High-level strategy]
**Strengths**: [What this does well]
**Tradeoffs**: [What this sacrifices]
[Link to prototype/mockup]

## Concept 2: [Name] — [Lens Name]
...

## Concept 3: [Name] — [Lens Name]
...

## Recommendation
[If asked: Which concept to pursue and why]

## Next Steps
- [ ] Gather feedback from [stakeholders]
- [ ] Test [specific assumption] with users
- [ ] Refine chosen direction into implementation
```

## Quality Criteria

### Excellent Concepts:
- **Three distinct directions** using different design lenses (for initial exploration)
- **Tied to research**: Design decisions directly address user jobs/pain points
- **Connected to emotional targets**: Each concept clearly maps to the Design Intent Interview
- **Strategically different**: Each explores a meaningfully different approach
- **Appropriate fidelity**: Level of detail matches the questions being answered
- **Annotated**: Key decisions are explained with WHY, not just shown
- **Realistic**: Use real or realistic content, not Lorem Ipsum
- **Accessible baseline**: Even concepts consider color contrast, text size
- **Responsive-aware**: Show how designs adapt to different screens (if relevant)

### Excellent Mood Boards:
- **Cohesive**: Each direction feels unified and intentional
- **Distinctive**: Different directions are clearly different
- **Cross-disciplinary**: Include non-digital inspiration sources
- **Emotionally grounded**: Tied to the Design Intent Interview adjectives
- **Annotated**: Explain WHY these visuals, not just WHAT they are

## Common Pitfalls to Avoid

### Designing in a Vacuum
**Problem**: Creating concepts without reviewing research or existing materials
**Instead**: Start every concept by reviewing personas, design principles, and competitive analysis

### Concepts That Look Identical
**Problem**: Three concepts that only differ in color or button shape
**Instead**: Use different design lenses — different information architecture, navigation models, interaction patterns, content priorities

### The Same 3 Archetypes Every Time
**Problem**: Always producing "Safe/Polished, Bold/Dark, Experimental/Brutalist"
**Instead**: Use the lens system. A healthcare app and a gaming platform should NOT get the same three archetypes. Let the project context drive lens selection.

### Mood Board Echo Chamber
**Problem**: Only pulling from Dribbble/Behance, which produces sameness
**Instead**: Include references from architecture, print, film, fashion, nature. The non-digital reference from the Design Intent Interview should appear in the mood board.

### Premature Pixel-Perfect Polish
**Problem**: Spending hours on shadows/gradients before validating the approach
**Instead**: Match fidelity to the question - use low-fi until direction is validated

### Lorem Ipsum Syndrome
**Problem**: Using placeholder text that hides content design problems
**Instead**: Use realistic content that exposes real layout and hierarchy challenges

### Missing the "Why"
**Problem**: Beautiful designs with no explanation of decisions
**Instead**: Annotate key decisions with rationale tied to research insights and emotional targets

### Ignoring Technical Feasibility
**Problem**: Concepts requiring tech that doesn't exist or can't be built in timeline
**Instead**: Check technical constraints early, design within feasible boundaries

## Design Patterns Library

**Navigation Patterns**: Tab bars, hamburger menu, bottom sheets, breadcrumbs, command palette, sidebar
**Form Patterns**: Inline validation, progressive disclosure, smart defaults, multi-step wizards
**Content Patterns**: Cards, lists, grids, feeds, masonry, editorial columns
**Feedback Patterns**: Toast notifications, modal dialogs, skeleton screens, empty states

## Integration Points

### Inputs
- **Design Research**: Personas, design principles, user insights, competitive analysis
- **Product/PM**: Feature requirements, business goals, timeline constraints
- **Engineering**: Technical constraints, API capabilities, performance requirements
- **Brand/Marketing**: Brand guidelines, messaging, visual identity

### Outputs
- **Engineering**: Validated direction to implement directly
- **Product/PM**: Visual artifacts to communicate product vision
- **Marketing**: Visual concepts for early marketing/PR materials

### Related Skills
- Use **design-research** artifacts (personas, principles) to inform concepts
- Use **design-qa** to review implemented designs against concepts

## Validation Checklist

Before delivering concept artifacts, verify:
- [ ] Conducted Design Intent Interview (or used brief as proxy)
- [ ] Gathered inspiration from diverse sources (not just Dribbble)
- [ ] Selected 3 design lenses appropriate to the project context
- [ ] **For initial exploration**: Created 3 meaningfully different concepts using different lenses
- [ ] **For refinement**: Focused on iterating 1 chosen concept based on feedback
- [ ] Each concept uses a different font family and color approach
- [ ] Each concept is annotated with rationale tied to research and emotional targets
- [ ] Used realistic content, not Lorem Ipsum
- [ ] Checked responsive behavior for mobile/tablet
- [ ] Verified color contrast meets minimum standards (4.5:1 for text)
- [ ] Created overview document comparing concepts
- [ ] Clearly communicated next steps and decisions needed
