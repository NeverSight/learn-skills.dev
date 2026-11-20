---
name: conversion-audit
description: Comprehensive CRO audit protocol for landing pages and websites. Runs before any redesign to identify conversion blockers, copy issues, visual problems, and missing trust elements. Produces a CRO-AUDIT-REPORT.md.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# Conversion Audit

A structured conversion rate optimization (CRO) audit for any existing landing page or website. Runs BEFORE design-advisor on any redesign or enhancement project. Produces a `CRO-AUDIT-REPORT.md` that feeds directly into the creative director's `DESIGN-BRIEF.md`.

---

## When to Invoke

Load this skill when:
- Auditing a client's existing website before a redesign
- Conversion rates are below expectations and the cause is unknown
- Planning a landing page refresh or premium visual enhancement pass
- A client asks "why isn't my site converting?"
- Running pre-launch validation on a completed build

Do NOT skip this step before a redesign. Building without an audit means guessing at the problem. The audit makes every recommendation evidence-based.

---

## Pre-Audit Setup

Before running the audit, gather:

1. **URL** of the page or site to audit
2. **Traffic type** — warm (referral, social, existing audience) or cold (paid ads, SEO)
3. **Primary CTA** — what should visitors do? (book a call, fill a form, call a number)
4. **Current conversion rate** — if the client knows it
5. **Brand guide** — if one exists, check the project for `brand-assets/` folder
6. **Analytics data** — drop-off points, heatmap findings, if available

If you have access to the live URL, screenshot it using the Atelier screenshot tool:
```bash
node "tools/screenshot/screenshot.js" <url> audit-screenshot.png --full-page --width=1440 --delay=2000
```

---

## Audit Protocol (5 Phases)

Work through all five phases in sequence. Document findings as you go. Every issue found is a line item in the final report.

---

### Phase 1: Layout Audit

Assess the overall structure and scroll flow of the page.

**Section Order Analysis**

Map out every section on the page top to bottom. Then compare to the optimal order for the traffic type:

| Traffic Type | Optimal Section Order |
|-------------|----------------------|
| Warm (referral, social) | Hero → Trust → Process → Demo → About → CTA |
| Cold (ads, SEO) | Hero → Social Proof → Benefits → Process → Testimonials → FAQ → CTA |
| Enterprise | Hero → Trust → Case Studies → Process → About → Contact Form |

Flag any section that is out of sequence. Note what the current order is vs. what it should be.

**StoryBrand Framework Check**

The page's narrative should follow: Problem → Outcome → Proof → How

Ask:
- Does the hero immediately name the visitor's pain or promise a clear outcome?
- Is there proof (numbers, testimonials, logos) before the "how it works" section?
- Does the page resolve with a clear, singular call to action?

**Dark/Light Balance**

Scan for visual fatigue. Flag if more than 3 consecutive sections share the same tone (all dark or all light). The eye needs alternation for breathing room.

**Above-the-Fold Assessment (5-Second Test)**

Imagine a cold visitor lands on this page. Within 5 seconds, can they answer:
- Who is this for?
- What does it do?
- Why should I care?
- What should I do next?

If any answer is unclear, flag it as a critical above-the-fold failure.

**Visual Breathing Room**

Check section padding. Sections that feel cramped (less than 80px vertical padding on desktop) create cognitive overload. Flag any section that looks compressed.

**Content Density**

Flag sections with too much text. A visitor scans before they read. If any section has more than 4 lines of body text without a visual break (icon, image, divider), flag it.

---

### Phase 2: Copy Audit

Assess the quality and effectiveness of every text element.

**Headline Specificity Test**

The hero headline should do one of two things:
1. Name a specific pain the visitor recognizes in themselves
2. Promise a specific, measurable outcome

Vague headlines like "Your Partner in Growth" or "We Help Businesses Scale" fail this test. Flag any headline that could belong to a competitor without changing a word.

**AI Slop Detection**

Scan all copy for the following patterns. Every match is a flag:

| Word/Phrase | Replace With |
|-------------|-------------|
| "leverage" | "use" |
| "cutting-edge" | describe what it actually does |
| "seamless" | "smooth" or remove |
| "streamline" | "simplify" or "speed up" |
| "holistic" | "complete" or "full" |
| "robust" | "reliable" or "strong" |
| "innovative" | describe what is actually new |
| "Experience the efficiency of" | describe what happens |
| "Elevate your" | describe the actual outcome |
| "Empower your team" | "Free up your team" or "Give your team" |
| "Transform your" | describe the specific change |
| "Next-level" | describe what is different |

**Vocabulary Check: Consultant vs. Vendor Language**

Vendor language (bad): "Our AI platform integrates with existing workflows to optimize operational throughput."
Consultant language (good): "We handle the calls your front desk doesn't have time for — so patients get answers and your staff gets their day back."

Flag any copy that sounds like a product description rather than a conversation with the client's customer.

**CTA Hierarchy Check**

- Is there ONE unmistakable primary CTA? (one button style, one destination, consistent throughout)
- Is there a secondary CTA? (lower-commitment alternative, e.g., "See how it works" vs. "Book a call")
- Does every section path lead toward the primary CTA?
- Does the CTA button text complete the phrase: "I want to ___"?

Flag if: multiple primary CTAs compete with each other, CTA text is vague ("Submit", "Learn More", "Click Here"), or the primary CTA is absent from any major section.

**StoryBrand Message Order**

Map the copy narrative:
1. Does section 1 (hero) state the **Problem** or desired **Outcome**?
2. Does the next block introduce **Proof** (social proof, numbers, logos)?
3. Does the process/features section explain **How**?

Flag if proof comes after the how, or if the problem is never named.

---

### Phase 3: Visual Audit

Assess the premium feel, depth, and visual hierarchy of the design.

**Color Monotony Check**

A one-accent-color design reads as basic. Flag if:
- Only one accent color is in use (minimum 2 for depth)
- The accent color is pure blue, pure green, or a generic brand default with no tonal variation
- No secondary accent for highlights, hover states, or dividers

**Background Treatment Check**

Flat backgrounds signal low effort. Check for depth signals:
- Noise/grain texture (even at 0.02 opacity makes a difference)
- Dot grid patterns
- Gradient meshes or animated gradients
- Gradient orbs or glows
- Section dividers that are more than a flat color change

Flag if all backgrounds are flat solid colors with no texture or depth treatment.

**Animation Quality Check**

Basic animations = fade-up on scroll. Premium animations include:
- Text reveals (word-by-word or character stagger)
- Parallax scroll-linked movement
- 3D card tilt on hover
- Footer reveal (Ciridae underlay pattern)
- Section numbering letter-spacing animation

Flag if the only animation present is a generic fade-up applied to every element.

**Typography Hierarchy Check**

There should be a clear visual scale: hero headline → section heading → subheading → body. The hierarchy should be immediately readable without having to measure anything.

Flag if:
- Hero headline and section headings are the same size
- Body text is larger than 18px (too heavy for scanning)
- Only one font weight is in use (no contrast)
- System fonts (Arial, Helvetica, Times) are used without intentionality

**Mobile Responsiveness**

If screenshots are available at multiple widths, check:
- 375px: Does the hero stack cleanly? Is the CTA above the fold?
- 768px: Does the two-column layout collapse gracefully?
- 1440px: Does the layout breathe (not stretched to full width without a max-width container)?

Flag any layout that breaks, overlaps, or loses readability at a standard breakpoint.

**Anti-AI-Slop Visual Check**

Flag any of these common AI-generated design signatures:
- Purple gradient + dark background (most common AI default)
- Three-column card grid with centered text and identical icon sizes
- Hero with a stock photo of a person smiling at a laptop
- Rounded pill buttons with no hover state
- All sections identically structured (headline + paragraph + button, repeated)

---

### Phase 4: Conversion Audit

Assess the specific mechanics that turn visitors into leads or customers.

**Form Friction Analysis**

Count the fields in every form on the page.

| Field Count | Avg Conversion Rate |
|-------------|-------------------|
| 1-3 fields | ~25% |
| 4-5 fields | ~20% |
| 6+ fields | ~15% |

Reducing from 6 to 3 fields produces approximately a 120% lift in conversions (Leadfeeder 2026). Flag any form with more than 4 fields. Identify which fields are optional vs. required, and which could be asked post-conversion instead.

**CTA Clarity**

- Is there one unmistakable primary action on the page?
- Is the CTA button visible without scrolling on desktop?
- Is the CTA button visible without scrolling on mobile?
- Does the CTA appear in the nav, hero, mid-page, and footer?

Flag if the CTA is only in one location or if the button does not stand out visually from the surrounding content.

**Social Proof Placement**

Trust signals should appear as early as possible — ideally within the first scroll. Check:
- Is there a logo bar or trust bar visible above or just below the fold?
- Are testimonials or case study numbers visible before the features section?
- Is there a stat block (e.g., "500+ practices served," "98% satisfaction") in the hero or immediately below it?

Flag if the first trust signal appears below the 3rd section.

**Trust Signal Inventory**

Document every trust signal present:
- [ ] Client logos
- [ ] Testimonials (with name, title, photo)
- [ ] Case study numbers (specific metrics, not "we helped them grow")
- [ ] Awards or certifications
- [ ] Media mentions
- [ ] Star ratings or review counts
- [ ] Guarantee or refund policy
- [ ] Partnership badges

Flag any category that is absent.

**Phone/Contact Accessibility**

For service businesses, a visible phone number in the header converts significantly better than a form-only approach. Check:
- Is a phone number visible in the nav?
- Is the phone number clickable (tel: link) on mobile?
- Is there a "call us" option in addition to a form?

---

### Phase 5: Missing Elements Check

A final inventory of commonly absent elements that improve conversion and trust.

For each item, mark: Present, Missing, or Not Applicable.

| Element | Status | Notes |
|---------|--------|-------|
| Trust bar / logo bar | | First section below hero |
| OG image (social sharing preview) | | Check `<meta property="og:image">` |
| Favicon | | 32x32 + 180x180 apple-touch-icon |
| Analytics tracking | | GA4, Plausible, or equivalent |
| Scroll progress indicator | | Shows reading position |
| Client/partner logos | | Above fold ideally |
| Video content (VSL or testimonials) | | Highest-converting trust format |
| Section numbering | | Helps visitors orient in long pages |
| FAQ section | | Handles objections passively |
| Privacy policy link | | Required for forms |
| Mobile tap-to-call | | tel: link in header |
| Live chat or chatbot | | Captures visitors not ready to form-fill |
| Exit intent popup | | Last chance to capture leaving visitors |

---

## Enhancement Recommendations Framework

After completing all 5 phases, generate prescriptive recommendations sorted by priority.

### 1. Section Reorder

Based on traffic type and StoryBrand framework findings, provide the exact new section order. Be specific — list every section by name and its new position.

Example output:
```
CURRENT ORDER: Hero → Features → About → Process → Testimonials → CTA
RECOMMENDED ORDER: Hero → Trust Bar → Testimonials → Process → Features → About → CTA
REASON: Cold traffic (paid ads) needs social proof before features. Moving trust bar to position 2 and testimonials to position 3 follows the proven cold-traffic conversion sequence.
```

### 2. Premium Component Suggestions

From these sources (in priority order for Tailwind v4 compatibility):

**Magic UI** (safest — shadcn CLI compatible):
- ShimmerButton — animated shimmer effect on CTA buttons
- NumberTicker — animated counting numbers for stats
- BlurFade — smooth blur-in entrance for sections
- DotPattern — subtle dot grid backgrounds
- Particles — ambient particle backgrounds
- AnimatedShinyText — shiny text effect for badges/labels
- MorphingText — text that morphs between words

Install: `npx shadcn@latest add "https://magicui.design/r/[component-name]"`

**Aceternity UI** (copy/paste, test each for Tailwind v4 compatibility):
- Spotlight — radial spotlight effect on hero sections
- Card Hover Effect — 3D tilt card on hover
- Moving Border — animated border on CTA buttons
- Background Beams — animated beam effect on dark backgrounds
- Aurora Background — northern lights gradient animation

Source: `aceternity.com/components` — copy JSX/CSS directly

**21st.dev** (shadcn registry):
- Browse `21st.dev/s/hero` for production hero components
- Browse `21st.dev/s/cta` for CTA section components
- Browse `21st.dev/s/testimonial` for testimonial components

Install: `npx shadcn@latest add "https://21st.dev/r/[component-slug]"`

For each recommendation, include:
- Component name and source
- Specific use case on this page
- Install command
- Any Tailwind v4 compatibility notes

### 3. Background Treatments

Recommend specific treatments for flat sections:

**Noise/grain texture** (immediate depth, zero performance cost):
```css
background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.02'/%3E%3C/svg%3E");
```

**Dot grid pattern** (subtle structure):
```css
background-image: radial-gradient(circle, #e5e7eb 1px, transparent 1px);
background-size: 24px 24px;
```

**Animated gradient mesh** (premium, modern):
```css
@property --gradient-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}
animation: gradient-rotate 20s linear infinite;
@keyframes gradient-rotate { to { --gradient-angle: 360deg; } }
```

**Gradient orbs with parallax** (see motion skill for scroll-linking):
- 400-600px blurred circle elements
- Use `filter: blur(80px)` and `opacity: 0.15`
- Link to scroll position using Framer Motion `useScroll` + `useTransform`

### 4. Animation Upgrades

Recommend specific upgrades from basic to premium:

**Lenis smooth scroll** (baseline for any premium site):
```bash
npm install lenis
```
Wrap the app root with Lenis for buttery scroll physics.

**Text reveals** (word-by-word stagger):
Split headline text into words. Apply stagger of 0.08s per word. Use `overflow: hidden` on each word container to prevent layout shift.

**Parallax** (Framer Motion):
```tsx
const { scrollYProgress } = useScroll();
const y = useTransform(scrollYProgress, [0, 1], ['0%', '-20%']);
```

**Footer CSS reveal** (Ciridae underlay pattern):
The footer appears to be revealed as the content above scrolls up. Achieved with `position: sticky` on the main content and `position: fixed` on the footer.

**3D card tilt on hover**:
Use `react-tilt` or implement with Framer Motion `useMotionValue` tracking mouse position.

**Section numbering reveal**:
Large section numbers (01, 02, 03) with letter-spacing animating from `0.5em` to `0.1em` on scroll-into-view.

For each animation upgrade, reference the `Atelier/skills/motion/SKILL.md` for implementation details.

### 5. Copy Rewrites

For each flagged copy issue, provide the rewrite in this format:

```
ORIGINAL: "Leverage our cutting-edge AI platform to streamline your operations."
REWRITE: "Your front desk answers every call. Patients get scheduled. Staff stops doing data entry."
REASON: Specific outcomes, no jargon, written from the visitor's perspective.
```

Apply the brand guide vocabulary where available. If no brand guide exists, default to:
- Short sentences (under 15 words each)
- Active voice
- Second person ("you" / "your") not third person
- Specific numbers where possible ("200+ patients served" not "many clients")

---

## Asset Requirements Documentation

For every recommendation made, document the implementation requirements:

| Asset | Source | Install Command | Compatibility | Bundle Impact |
|-------|--------|----------------|---------------|--------------|
| MagicUI ShimmerButton | shadcn CLI | `npx shadcn@latest add "https://magicui.design/r/shimmer-button"` | Tailwind v4 compatible | ~3kb |
| Lenis smooth scroll | npm | `npm install lenis` | Any | ~15kb |
| Aceternity Spotlight | Copy/paste | aceternity.com/components/spotlight | Test Tailwind v4 | ~2kb |
| [component] | [source] | [command] | [notes] | [estimate] |

---

## Output Format

Generate a `CRO-AUDIT-REPORT.md` in the project root structured as follows:

```markdown
# CRO Audit Report: [Site Name]
**Date**: [date]
**URL**: [url]
**Traffic Type**: [warm / cold / enterprise]
**Primary CTA**: [what the page wants visitors to do]

---

## Executive Summary

[3-5 bullet points of the most critical issues found. These are the things that MUST be addressed before launch or before any other work.]

---

## Phase 1: Layout Audit
### Current Section Order
[list sections top to bottom]

### Recommended Section Order
[list the new order with rationale]

### Findings
[bulleted list of layout issues found]

---

## Phase 2: Copy Audit
### AI Slop Flags
[specific quotes from the page with suggested rewrites]

### Headline Assessment
[current headline + assessment + rewrite if needed]

### CTA Hierarchy
[current state + gaps + recommendation]

### Vocabulary Issues
[vendor language found + consultant language rewrites]

---

## Phase 3: Visual Audit
### Color Assessment
[findings]

### Background Treatments
[what's present, what's missing, what to add]

### Animation Assessment
[current animation level + recommendations]

### Typography Hierarchy
[findings]

### Mobile Assessment
[findings at each breakpoint if available]

---

## Phase 4: Conversion Audit
### Form Analysis
[field count, current estimated conversion rate, recommendation]

### CTA Placement
[where it appears, where it's missing]

### Social Proof Placement
[first trust signal location, recommendation]

### Trust Signal Inventory
[complete checklist with present/missing status]

---

## Phase 5: Missing Elements
[full checklist with status for each element]

---

## Recommendations (Prioritized)

### Priority 1: Critical (address before launch)
[items that are actively hurting conversion — fix these first]

### Priority 2: High Impact (first iteration)
[items with significant estimated lift — implement in first design pass]

### Priority 3: Premium Enhancements (polish phase)
[items that elevate the design — implement after core is solid]

---

## Asset Requirements
[full table of every asset needed to implement recommendations]

---

## Estimated Impact
[qualitative assessment: which recommendations will have the highest lift and why]
```

---

## Integration with Atelier Workflow

The conversion audit sits at the beginning of any redesign or enhancement project. It informs every downstream step.

**Standard workflow for a redesign:**
1. **conversion-audit** (this skill) — identify all problems, produce CRO-AUDIT-REPORT.md
2. **brand-extractor** — if the client has an existing site worth extracting brand from
3. **design-advisor** — use audit findings to inform the design brief (CRO-AUDIT-REPORT.md feeds into DESIGN-BRIEF.md)
4. **creative-director** — references both the audit report and design brief when assigning work
5. **page-builder / frontend-builder** — builds with audit issues as explicit acceptance criteria
6. **ui-reviewer** — validates that every Priority 1 and Priority 2 audit issue was resolved
7. Update `Atelier/EXPERTISE.md` with what was found and what worked

**When auditing a client's site (not a redesign):**
1. Run conversion-audit
2. CRO-AUDIT-REPORT.md becomes the deliverable (consulting output)
3. Use it to scope the redesign engagement and justify pricing

---

## CRO Research Reference

### Section Order by Traffic Type

| Traffic | Position 1 | Position 2 | Position 3 | Position 4 | Position 5 | Position 6 | Final |
|---------|-----------|-----------|-----------|-----------|-----------|-----------|-------|
| Warm | Hero | Trust | Process | Demo | About | — | CTA |
| Cold | Hero | Social Proof | Benefits | Process | Testimonials | FAQ | CTA |
| Enterprise | Hero | Trust | Case Studies | Process | About | — | Contact Form |

### Form Field Benchmarks

| Fields | Avg Conversion Rate |
|--------|-------------------|
| 1-3 | ~25% |
| 4-5 | ~20% |
| 6+ | ~15% |

Reducing from 6 to 3 fields = ~120% lift (Leadfeeder 2026)

### CTA Hierarchy Rules

- One primary CTA per page (form submission or phone call — pick one)
- One secondary CTA (the lower-commitment alternative)
- Every section should have a path to the primary CTA
- CTA button text should complete the sentence: "I want to ___"
- Primary and secondary CTA buttons must be visually distinct (color, weight, or style difference)

### Anti-AI-Slop Copy Reference

**Words and phrases to flag and replace:**

| Flag | Replace With |
|------|-------------|
| "leverage" | "use" |
| "cutting-edge" | describe what it actually does |
| "seamless" | "smooth" or remove entirely |
| "streamline" | "simplify" or "speed up" |
| "holistic" | "complete" or "full" |
| "robust" | "reliable" or "strong" |
| "innovative" | describe what is actually new |
| "Experience the efficiency of" | describe what happens |
| "Elevate your" | describe the outcome |
| "Empower your team" | "Free up your team" or "Give your team" |
| "Transform your" | describe the specific change |
| "Next-level" | describe what is different |
| "Game-changing" | describe what changed |
| "Best-in-class" | describe what makes it better |
| "End-to-end" | describe the actual scope |

### Headline Formula Reference

**Pain-based (cold traffic):**
`[Specific Problem] is [costing/causing] [Specific Cost]. [Solution] [Specific Outcome].`

**Outcome-based (warm traffic):**
`[Specific Outcome] for [Specific Audience] — [How/What Makes It Different].`

**Social proof lead:**
`[Credible Number] [Audience] already [Result]. Here's how.`

---

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `design-advisor` | Receives findings from this audit. CRO-AUDIT-REPORT.md should be referenced when generating DESIGN-BRIEF.md. |
| `brand-extractor` | Run alongside or after this audit when extracting design patterns from an existing site. |
| `component-sniping` | Use after this audit to source specific components recommended in Phase 3. |
| `motion` | Handles implementation of animation upgrades recommended in Phase 4. |
| `frontend-master` | Uses CRO-AUDIT-REPORT.md as a second reference doc alongside DESIGN-BRIEF.md during the build. |
| `screenshot-loop` | After build, compare screenshots against audit findings to verify issues were resolved. |
| `optimization` | Cross-check audit's "missing elements" list against the pre-deploy checklist. |
