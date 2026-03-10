---
name: review-web-design
description: >
  Review web design for layout quality, typography, colour usage, spacing,
  responsive behaviour, brand consistency, and visual hierarchy. Covers
  design principles evaluation and improvement recommendations. Use when
  reviewing a design mockup before development, assessing an implemented
  site for design quality, providing feedback during a design review session,
  evaluating brand consistency, or checking responsive behaviour across breakpoints.
license: MIT
allowed-tools: Read Grep Glob WebFetch
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: review
  complexity: intermediate
  language: multi
  tags: web-design, layout, typography, colour, responsive, visual-hierarchy, branding
---

# Review Web Design

Evaluate a web design for visual quality, consistency, and effectiveness across devices.

## When to Use

- Reviewing a design mockup or prototype before development
- Assessing an implemented website or web application for design quality
- Providing feedback on visual design during a design review session
- Evaluating brand consistency across multiple pages or sections
- Checking responsive design behaviour across breakpoints

## Inputs

- **Required**: Design to review (URL, mockup files, screenshots, or source code)
- **Optional**: Brand guidelines or design system documentation
- **Optional**: Target audience description
- **Optional**: Reference designs or competitor examples
- **Optional**: Specific areas of concern

## Procedure

### Step 1: Assess Visual Hierarchy

Visual hierarchy guides the user's eye through content in order of importance.

- [ ] **Clear focal point**: Is there an obvious entry point on each page/screen?
- [ ] **Heading hierarchy**: Do headings descend logically (H1 → H2 → H3)?
- [ ] **Size contrast**: Are important elements larger than supporting elements?
- [ ] **Colour contrast**: Are CTAs and key actions visually prominent?
- [ ] **Whitespace**: Does spacing separate logical groups effectively?
- [ ] **Reading flow**: Does the layout follow a natural reading pattern (F-pattern, Z-pattern)?

```markdown
## Visual Hierarchy Assessment
| Page/Section | Focal Point | Hierarchy Clear? | Issues |
|-------------|-------------|-----------------|--------|
| Homepage | Hero section CTA | Yes | Secondary CTA competes with primary |
| Product page | Product image | Mostly | Price not prominent enough |
| Contact form | Submit button | No | Form title same size as body text |
```

**Expected:** Each major page/section assessed for clear visual hierarchy.
**On failure:** If mockups are unavailable, assess from live code using browser dev tools.

### Step 2: Evaluate Typography

- [ ] **Font selection**: Are fonts appropriate for the brand and content type?
- [ ] **Font pairing**: Do heading and body fonts complement each other (max 2-3 families)?
- [ ] **Type scale**: Is there a consistent scale (e.g., 1.25 major second, 1.333 perfect fourth)?
- [ ] **Line height**: Body text has 1.4-1.6 line height; headings have 1.1-1.3
- [ ] **Line length**: Body text line length is 45-75 characters (optimal ~66)
- [ ] **Font weight**: Weight variations used consistently to indicate hierarchy
- [ ] **Font size**: Base font size is at least 16px for body text

```css
/* Example well-structured type scale (1.25 ratio) */
:root {
  --text-xs: 0.64rem;    /* 10.24px */
  --text-sm: 0.8rem;     /* 12.8px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.25rem;    /* 20px */
  --text-xl: 1.563rem;   /* 25px */
  --text-2xl: 1.953rem;  /* 31.25px */
  --text-3xl: 2.441rem;  /* 39.06px */
}
```

**Expected:** Typography assessed for consistency, readability, and hierarchy.
**On failure:** If the design uses more than 3 font families, recommend consolidation.

### Step 3: Review Colour Usage

- [ ] **Palette coherence**: Is the colour palette intentional and limited (typically 3-5 colours + neutrals)?
- [ ] **Brand alignment**: Do colours match brand guidelines?
- [ ] **Contrast ratios**: Text meets WCAG AA (4.5:1 for normal text, 3:1 for large text)
- [ ] **Semantic colour**: Are colours used consistently for meaning (red=error, green=success)?
- [ ] **Colour blindness**: Is information conveyed by more than colour alone?
- [ ] **Dark/light mode**: If supported, both modes maintain readability and brand consistency

```markdown
## Colour Assessment
| Usage | Colour | Contrast Ratio | WCAG AA | Notes |
|-------|--------|----------------|---------|-------|
| Body text on white | #333333 | 12.6:1 | Pass | Good |
| Link text on white | #2563eb | 5.2:1 | Pass | Good |
| Muted text on light gray | #9ca3af on #f3f4f6 | 2.1:1 | FAIL | Increase contrast |
| CTA button text | #ffffff on #22c55e | 3.1:1 | FAIL for small text | Use darker green or larger text |
```

**Expected:** Colour palette reviewed for coherence, accessibility, and semantic consistency.
**On failure:** Use a contrast checker tool (WebAIM) to verify exact ratios.

### Step 4: Assess Layout and Spacing

- [ ] **Grid system**: Is a consistent grid used (12-column, auto-layout, or custom)?
- [ ] **Spacing scale**: Is spacing systematic (4px/8px base, or Tailwind-like scale)?
- [ ] **Alignment**: Are elements aligned to the grid (no "almost aligned" items)?
- [ ] **Density**: Is information density appropriate for the content type (data-heavy vs. marketing)?
- [ ] **Whitespace**: Is whitespace used intentionally to group and separate?
- [ ] **Consistency**: Are similar sections spaced identically?

Spacing audit:

```markdown
## Spacing Consistency Check
| Element Pair | Expected Gap | Actual Gap | Consistent? |
|-------------|-------------|------------|-------------|
| Section title to content | 24px | 24px | Yes |
| Card to card | 16px | 16px/24px | No — inconsistent |
| Form label to input | 8px | 4px/8px/12px | No — varies |
```

**Expected:** Layout uses a systematic grid and spacing scale consistently.
**On failure:** If spacing is inconsistent, recommend adopting a spacing scale (e.g., Tailwind's `space-*`).

### Step 5: Evaluate Responsive Design

Test across key breakpoints:

| Breakpoint | Width | Represents |
|-----------|-------|-----------|
| Mobile | 375px | iPhone SE / small phones |
| Mobile L | 428px | iPhone 14 / large phones |
| Tablet | 768px | iPad portrait |
| Desktop | 1280px | Standard laptop |
| Wide | 1536px+ | Desktop monitor |

Check at each breakpoint:
- [ ] **Layout adaptation**: Does the layout reflow appropriately (stack on mobile, side-by-side on desktop)?
- [ ] **Touch targets**: Are interactive elements at least 44x44px on mobile?
- [ ] **Text readability**: Is font size appropriate for the viewport?
- [ ] **Image scaling**: Do images resize without distortion or overflow?
- [ ] **Navigation**: Is mobile navigation accessible (hamburger, bottom nav, etc.)?
- [ ] **No horizontal scroll**: Content doesn't overflow the viewport horizontally

```markdown
## Responsive Review
| Breakpoint | Layout | Touch Targets | Text | Images | Navigation | Issues |
|-----------|--------|---------------|------|--------|------------|--------|
| 375px | OK | OK | OK | Overflow on hero | Hamburger | Hero image clips |
| 768px | OK | OK | OK | OK | Hamburger | None |
| 1280px | OK | N/A | OK | OK | Full nav | None |
| 1536px | OK | N/A | Line length too long | OK | Full nav | Add max-width to content |
```

**Expected:** Design tested at all key breakpoints with issues documented.
**On failure:** If responsive testing tools are unavailable, review CSS media queries for coverage.

### Step 6: Check Brand Consistency

- [ ] **Logo usage**: Logo rendered correctly (size, spacing, clear zone)
- [ ] **Colour accuracy**: Brand colours match spec (hex values, not "close enough")
- [ ] **Typography match**: Fonts match brand guidelines
- [ ] **Tone/voice**: UI copy matches brand personality
- [ ] **Iconography**: Icons are from a consistent set (style, weight, grid)
- [ ] **Photography style**: Images match brand guidelines (if applicable)

**Expected:** Brand elements verified against guidelines with specific deviations noted.
**On failure:** If brand guidelines don't exist, note this as a recommendation and assess internal consistency instead.

### Step 7: Write the Design Review

```markdown
## Web Design Review

### Overall Impression
[2-3 sentences: overall quality, strongest and weakest aspects]

### Visual Hierarchy: [Score/5]
[Key findings with specific references]

### Typography: [Score/5]
[Key findings with specific references]

### Colour: [Score/5]
[Key findings with specific references]

### Layout & Spacing: [Score/5]
[Key findings with specific references]

### Responsive Design: [Score/5]
[Key findings with specific references]

### Brand Consistency: [Score/5]
[Key findings with specific references]

### Priority Improvements
1. [Most impactful change — specific and actionable]
2. [Second priority]
3. [Third priority]

### Positive Notes
1. [What works well and should be preserved]
```

**Expected:** Review provides specific, visual-reference feedback with prioritized improvements.
**On failure:** If scoring feels arbitrary, use a simpler pass/concern/fail system instead.

## Validation

- [ ] Visual hierarchy assessed for all major pages/sections
- [ ] Typography evaluated for readability, consistency, and scale
- [ ] Colour contrast verified against WCAG AA minimums
- [ ] Layout and spacing checked for grid consistency
- [ ] Responsive design tested at 3+ breakpoints
- [ ] Brand consistency verified against guidelines (or internal consistency assessed)
- [ ] Feedback is specific with visual references (page, section, element)

## Common Pitfalls

- **Subjective without reasoning**: "I don't like the colour" is not actionable. Explain why (contrast, brand mismatch, accessibility).
- **Ignoring accessibility**: Visual design review must include WCAG contrast checks. Beautiful designs that exclude users are not good designs.
- **Reviewing mockups only**: Test responsive behaviour, hover states, and transitions — not just static layouts.
- **Prescribing solutions**: Describe the problem ("text is hard to read on this background") rather than dictating a specific fix ("use #333").
- **Forgetting context**: A banking app and a gaming site have different design standards. Review against the appropriate context.

## Related Skills

- `review-ux-ui` — usability, interaction patterns, and accessibility (complementary to visual design)
- `setup-tailwind-typescript` — Tailwind CSS implementation for design systems
- `scaffold-nextjs-app` — Next.js application scaffolding
