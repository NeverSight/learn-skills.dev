---
name: design-advisor
description: Pre-build design consultation protocol that produces a DESIGN-BRIEF.md for all builders to reference.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Design Advisor

The mandatory pre-build consultation that runs BEFORE any new website, landing page, dashboard, or major redesign. Produces a DESIGN-BRIEF.md that all downstream skills and builders reference.

---

## When to Invoke

Invoke this skill at the start of any:
- New website or landing page build
- Major redesign of an existing site
- New dashboard or web application
- Client project kickoff that involves frontend work

Do NOT skip this step. Building without a design brief leads to generic AI-slop output, rework, and misaligned expectations.

---

## The Design Interview

These questions are MANDATORY. Ask them before writing a single line of CSS.

### Question 1: Tone
> "What's the tone for this project?"

Offer these options (allow combinations):
| Tone | Characteristics |
|------|----------------|
| **Luxury** | Dark backgrounds, gold/cream accents, serif headings, lots of whitespace |
| **Minimalist** | Max 2 colors, extreme whitespace, small text, no decoration |
| **Bold** | Large type, bright colors, strong contrast, confident copywriting |
| **Playful** | Rounded shapes, bright palette, casual language, subtle motion |
| **Editorial** | Magazine-style layout, serif headings, long-form content focus |
| **Corporate** | Professional, structured grid, blue/navy palette, trust-focused |
| **Organic** | Earth tones, natural textures, soft edges, warm photography |

### Question 2: Mode
> "Dark mode, light mode, or both?"

Notes:
- Dark mode is more dramatic, feels premium, common for tech/creative
- Light mode is cleaner, better for readability-heavy sites, common for healthcare/professional
- Both requires a token swap system (see color-system skill)

### Question 3: References
> "Any reference sites you love? Drop URLs or screenshots."

If the user provides references:
- Screenshot each reference at 1440px desktop width
- Identify what they like about each: layout, color, typography, animation, vibe
- Note specific patterns to replicate or avoid

If the user has no references:
- Suggest 2-3 sites from the SITE-TEARDOWNS catalog that match their tone
- Ask "Does this direction feel right?"

### Question 4: Animation Level
> "How much animation? Minimal, Moderate, or Rich?"

| Level | What It Means |
|-------|---------------|
| **Minimal** | Fade-in on scroll, hover states only. Clean and fast. |
| **Moderate** | Entrance animations, parallax sections, animated counters. The sweet spot. |
| **Rich** | Page transitions, scroll-linked animations, interactive elements, 3D. Requires careful performance tuning. |

### Question 5: Brand Assets
> "Do you have brand assets? Logo, colors, fonts, brand guidelines?"

Check the project for a `brand-assets/` folder. If it exists, read its contents. If not:
- Ask if they have a logo (SVG preferred)
- Ask if they have established brand colors
- Ask if they have font preferences
- If nothing exists, note this — the advisor will recommend everything

### Question 6: Primary CTA
> "What's the ONE thing visitors should do on this site?"

Examples:
- "Book a free consultation"
- "Sign up for the waitlist"
- "Call this phone number"
- "Download the guide"

This becomes the primary CTA across the entire site. Every section should ultimately drive toward this action.

---

## After the Interview: Advisor Actions

Once the interview is complete, the advisor performs these 7 actions in sequence.

### Action 1: RECOMMEND Font Pairings

Consult `Atelier/catalogs/TYPOGRAPHY-CATALOG.md` and recommend 2-3 pairings that match the tone.

**Format:**
```
FONT RECOMMENDATIONS:

Option A: Clash Display (headings) + General Sans (body)
  → Bold, modern, high contrast. Good for tech/creative.

Option B: Playfair Display (headings) + Source Sans 3 (body)
  → Editorial, sophisticated. Good for luxury/content-heavy.

Option C: Cabinet Grotesk (headings) + Inter (body)
  → Clean, versatile, professional. Good for SaaS/corporate.

Recommendation: Option A — matches the "Bold" tone you described.
```

### Action 2: RECOMMEND Hero Archetype

Consult `Atelier/catalogs/HERO-CATALOG.md` and recommend a hero layout.

**Hero archetypes:**
| Archetype | Description | Best For |
|-----------|-------------|----------|
| Manifesto Hero | Big bold text, minimal imagery, statement-driven | Bold, editorial, manifesto brands |
| Split Hero | Text left, image/visual right (or vice versa) | Product showcases, SaaS, healthcare |
| Full-Bleed Hero | Full-screen background image/video with text overlay | Visual brands, real estate, restaurants |
| Minimal Hero | Small centered text, lots of whitespace, subtle | Luxury, minimalist, agencies |
| Interactive Hero | 3D element, canvas animation, or interactive component | Tech, creative, portfolios |

### Action 3: RECOMMEND Color System

Consult `Atelier/catalogs/COLOR-CATALOG.md` and recommend a palette strategy.

If the client has brand colors, build the system around them. If not, propose a palette based on tone and industry.

### Action 4: SUGGEST Component Patterns

Consult `Atelier/catalogs/COMPONENT-CATALOG.md` and suggest patterns for:
- Navigation style (sticky, transparent, minimal)
- Feature/benefit sections
- Social proof / testimonials
- Pricing (if applicable)
- Footer style

### Action 5: FLAG Anti-Slop Risks

Actively scan the design direction for AI-slop patterns and flag them:

```
ANTI-SLOP FLAGS:

⚠ Dark mode + purple gradient — AI slop signature.
  → Recommendation: Use teal (#14B8A6) or amber (#F59E0B) as accent instead.

⚠ Inter for display headings — generic default.
  → Recommendation: Swap to Satoshi or Cabinet Grotesk.

⚠ Centered text + 3-column card grid — the most common AI layout.
  → Recommendation: Use asymmetric layout. Text left-aligned, cards in 2-column offset.

✓ Self-hosted fonts — good.
✓ Specific CTA text — good.
✓ Reference sites provided — good.
```

### Action 6: CHECK Brand Assets

Look for a `brand-assets/` folder in the project root.

**If it exists:** Read and inventory the contents. Note what's present and what's missing.

**If it doesn't exist:** Create one from template:

```
brand-assets/
  README.md          # Brand overview
  colors.json        # Color definitions
  logo.svg           # Primary logo (placeholder note if missing)
  typography.md      # Font selections and usage
```

`colors.json` template:
```json
{
  "primary": "",
  "secondary": "",
  "accent": "",
  "background": "",
  "surface": "",
  "text-primary": "",
  "text-secondary": "",
  "border": ""
}
```

### Action 7: CHECK Expertise

Read `Atelier/EXPERTISE.md` (if it exists) for learnings from similar past projects. Apply any relevant patterns or avoid past mistakes.

---

## Output: DESIGN-BRIEF.md

After completing all 7 actions, generate a `DESIGN-BRIEF.md` in the project root. This is the single source of truth for all builders.

**Template** (use `Atelier/templates/design-brief-template.md` if available, otherwise use this):

```markdown
# Design Brief: [Project Name]

## Overview
- **Client**: [Name]
- **Project type**: [Website / Landing page / Dashboard / App]
- **Primary CTA**: [The one thing visitors should do]
- **Target audience**: [Who visits this site]

## Tone & Style
- **Tone**: [From interview]
- **Mode**: [Dark / Light / Both]
- **Animation level**: [Minimal / Moderate / Rich]
- **Reference sites**: [URLs or "none provided"]

## Typography
- **Headings**: [Font name] ([weight])
- **Body**: [Font name] ([weight range])
- **Monospace** (if needed): [Font name]

## Color System
- **Background primary**: [hex]
- **Background secondary**: [hex]
- **Text primary**: [hex]
- **Text secondary**: [hex]
- **Accent**: [hex]
- **Accent hover**: [hex]
- **Border**: [rgba or hex]

## Layout
- **Hero archetype**: [Name from catalog]
- **Navigation**: [Style]
- **Section patterns**: [List key sections and their layout pattern]
- **Footer**: [Style]

## Components
- [List specific component patterns selected from catalogs]

## Anti-Slop Notes
- [List any flags and their resolutions]

## Brand Assets
- Logo: [Available / Missing — describe if available]
- Brand guidelines: [Available / Missing]
- Photography: [AI-generated / Stock / Client-provided / None yet]

## Pages
- [List all pages to build with brief description of each]
```

---

## Catalog Paths

The design advisor references these catalogs. All paths are relative to the Atelier root:

| Catalog | Path |
|---------|------|
| Hero layouts | `Atelier/catalogs/HERO-CATALOG.md` |
| Animation patterns | `Atelier/catalogs/ANIMATION-CATALOG.md` |
| Typography pairings | `Atelier/catalogs/TYPOGRAPHY-CATALOG.md` |
| Color palettes | `Atelier/catalogs/COLOR-CATALOG.md` |
| Component patterns | `Atelier/catalogs/COMPONENT-CATALOG.md` |
| Site teardowns | `Atelier/catalogs/SITE-TEARDOWNS.md` |
| Design brief template | `Atelier/templates/design-brief-template.md` |
| Brand assets template | `Atelier/templates/brand-assets/` |
| Past learnings | `Atelier/EXPERTISE.md` |

---

## What Happens After the Brief

Once DESIGN-BRIEF.md is generated, reference `Atelier/ROUTER.md` to determine which skills to load next. Typical flow:

1. **design-advisor** (this skill) → produces DESIGN-BRIEF.md
2. **color-system** → implements the CSS variable system from the brief
3. **typography** → sets up font loading and type scale from the brief
4. **vibe-design** → generates brand-matched images if needed
5. **frontend-master** or **stitch-loop** → builds the actual pages
6. **screenshot-loop** → validates the build against the brief
7. **optimization** → prepares for production deployment

---

## Edge Cases

### Client says "I don't know" to tone/style questions
Recommend based on their industry:
- Healthcare → Organic or Corporate
- Tech/SaaS → Bold or Minimalist
- Real Estate → Luxury
- Content/Media → Editorial
- Agency/Creative → Bold or Playful

### Client provides a Figma mockup
Skip the recommendation steps. Extract the design decisions directly from the mockup:
- Screenshot the mockup at each breakpoint
- Extract colors, fonts, spacing from the Figma file
- Document everything in DESIGN-BRIEF.md
- Still run the anti-slop check on the mockup design

### Client wants to match an existing brand exactly
Read their brand guidelines. Populate DESIGN-BRIEF.md directly from the guidelines. Only recommend where the guidelines have gaps (e.g., no web-specific typography defined, no dark mode specified).

### Redesign of an existing site
Screenshot the current site first. Ask: "What do you want to KEEP from the current design? What do you want to CHANGE?" This prevents accidentally losing elements the client values.

---

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `color-system` | Receives the color palette from this brief and implements CSS variables. |
| `typography` | Receives font selections from this brief and implements loading/scale. |
| `vibe-design` | Receives brand context from this brief for AI image generation prompts. |
| `screenshot-loop` | Compares builds against the brief produced here. |
| `frontend-master` | Uses this brief as the primary reference during the build. |
| `optimization` | References the brief for final production checklist validation. |
