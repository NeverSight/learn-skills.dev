---
name: presentation-builder
description: Build professional PPTX presentations with brand-aligned layouts using structured deck briefs and validation steps for pitch, roadmap, and product decks.
metadata:
  tags: presentation, pptx, slides, storytelling, branding, pitch-deck
  platforms: Claude, ChatGPT, Gemini, Codex
---


# PPTX Presentation Builder

A professional PPTX presentation builder skill aligned with brand guidelines. Generates various presentations including pitch decks, roadmaps, and product introductions using structured briefs and validation steps.

## When to use this skill

- **Professional Slide Deck Needed**: Generate presentations from prompts
- **Brand Consistency Required**: Consistent slides aligned with guidelines
- **Reusable Templates**: Templatize product, pitch, roadmap decks

---

## Instructions

### Step 1: Gather Brand Constraints

```yaml
brand_kit:
  colors:
    primary: "#2563EB"
    secondary: "#6366F1"
    accent: "#F59E0B"
    background: "#FFFFFF"
    text: "#1F2937"
  fonts:
    heading: "Inter"
    body: "Inter"
    mono: "JetBrains Mono"
  logo:
    placement: "top-left" | "bottom-right"
    size: "small" | "medium"
  style:
    tone: "minimal" | "bold" | "executive"
    corners: "sharp" | "rounded"
    shadows: true | false
```

### Step 2: Define Deck Structure

```markdown
## Deck Brief

### Meta
- **Title**: [deck title]
- **Audience**: [audience]
- **Goal**: [goal - fundraising, product intro, reporting]
- **Duration**: [presentation time]

### Slides
| # | Type | Title | Key Message |
|---|------|-------|-------------|
| 1 | Title | Company Name | Tagline |
| 2 | Agenda | Today's Agenda | 3-5 bullet points |
| 3 | Problem | The Challenge | Pain point statement |
| 4 | Solution | Our Approach | Value proposition |
| 5 | Features | Key Capabilities | 3 features with icons |
| 6 | Demo | Product in Action | Screenshot/video |
| 7 | Traction | Growth Numbers | Key metrics |
| 8 | Team | Who We Are | Team photos + roles |
| 9 | Ask | The Opportunity | Investment/partnership ask |
| 10 | Contact | Get in Touch | Contact info + CTA |
```

### Step 3: Generate Slides

Generate content per slide:

```markdown
## Slide 1: Title Slide

### Layout: Centered

### Content
- **Title**: [Company Name]
- **Subtitle**: [Tagline - 10 words max]
- **Visual**: Logo centered
- **Background**: Gradient (#2563EB → #6366F1)

### Speaker Notes
Welcome the audience. Introduce yourself and the company.
Set the context for why you're presenting today.
```

**Templates by Slide Type**:

| Type | Layout | Elements |
|------|--------|----------|
| Title | Centered | Logo, Title, Subtitle |
| Agenda | Left-aligned | Numbered list (3-5 items) |
| Problem | Split | Text left, Visual right |
| Solution | Split | Visual left, Text right |
| Features | 3-column | Icon + Title + Description |
| Stats | Data cards | 3-4 key metrics |
| Quote | Centered | Quote text + attribution |
| Team | Grid | Photos + Names + Roles |
| CTA | Centered | Headline + Button |

### Step 4: Review and Refine

```markdown
## Review Checklist

### Layout Balance
- [ ] Check visual balance
- [ ] Ensure sufficient whitespace
- [ ] Alignment consistency

### Typography
- [ ] Font size hierarchy (H1 > H2 > Body)
- [ ] Ensure readability (minimum 18pt body)
- [ ] Consistent font usage

### Content
- [ ] One idea per slide
- [ ] Avoid text density
- [ ] Cite sources for data/claims

### Accessibility
- [ ] Sufficient color contrast
- [ ] Alt text for images
- [ ] Logical reading order
```

### Step 5: Export and Handoff

```markdown
## Handoff Package

### Files
- presentation.pptx
- presentation.pdf (backup)
- assets/ (images, logos)

### Summary
- **Total Slides**: [count]
- **Estimated Duration**: [minutes]
- **Key Narrative Arc**: [brief description]

### Editing Notes
- Slide 5: [specific edit note]
- Slide 8: [specific edit note]

### Post-Export Checklist
- [ ] Font embedding verified
- [ ] Images high resolution
- [ ] Animations functional
- [ ] Links active
```

---

## Examples

### Example 1: 5-Slide Roadmap

**Prompt**:
```
Create a 5-slide roadmap deck for Q2–Q4
with modern design and speaker notes.
Target: Engineering leadership.
```

**Expected output**:
```markdown
## Roadmap Deck

### Slide 1: Title
- Q2-Q4 Product Roadmap
- Engineering Review | [Date]

### Slide 2: Executive Summary
- 3 key themes for the period
- Success metrics overview

### Slide 3: Timeline
- Gantt-style view
- Q2: Foundation | Q3: Scale | Q4: Optimize
- Key milestones marked

### Slide 4: Dependencies & Risks
- Cross-team dependencies
- Risk matrix (Impact vs Likelihood)
- Mitigation strategies

### Slide 5: Next Steps
- Immediate action items
- Review cadence
- Feedback channels
```

### Example 2: Investor Pitch Deck

**Prompt**:
```
Build a 10-slide investor pitch deck for an AI SaaS.
Include: problem, solution, market, traction, team, ask.
Series A context, $5M target.
```

**Expected output**:
- Slide-by-slide content with speaker notes
- Consistent brand styling
- Data visualization for traction
- Clear ask slide with use of funds

### Example 3: Product Demo Deck

**Prompt**:
```
Create an 8-slide product demo deck.
Audience: Potential enterprise customers.
Focus: Features, integrations, security.
```

**Expected output**:
- Feature showcase slides
- Integration diagram
- Security compliance overview
- Customer success stories
- Next steps / trial CTA

---

## Best practices

1. **One idea per slide**: Avoid overcrowding
2. **Visual hierarchy**: Titles > Headings > Body
3. **Use speaker notes**: Minimize text on slides
4. **Data clarity**: Charts > text paragraphs
5. **Consistent theming**: Unify colors, fonts, spacing

---

## Common pitfalls

- **Mixed Themes**: Multiple styles in one deck
- **Inconsistent Spacing/Typography**: Different across slides
- **No Narrative Flow**: Lack of logical connection

---

## Troubleshooting

### Issue: Slides feel inconsistent
**Cause**: Missing brand tokens
**Solution**: Provide template, enforce theme

### Issue: Slides are too dense
**Cause**: Too much text per slide
**Solution**: Split content, use visuals

### Issue: Narrative unclear
**Cause**: Slide order issue
**Solution**: Restructure story arc

---

## Output format

```markdown
## Presentation Report

### Overview
- **Title**: [deck title]
- **Slides**: [count]
- **Duration**: [minutes]
- **Audience**: [target]

### Slide-by-Slide

#### Slide 1: [Title]
**Type**: [slide type]
**Layout**: [layout description]
**Content**:
- [content items]

**Speaker Notes**:
[notes]

---
#### Slide 2: [Title]
...

### Brand Tokens Applied
- Primary: [color]
- Font: [font family]
- Style: [tone]

### Files Delivered
- [ ] presentation.pptx
- [ ] assets.zip
```

---

## Multi-Agent Workflow

### Validation & Retrospectives

- **Round 1 (Orchestrator)**: Narrative arc, slide count alignment
- **Round 2 (Analyst)**: Layout consistency, brand compliance
- **Round 3 (Executor)**: Export readiness check

### Agent Roles

| Agent | Role |
|-------|------|
| Claude | Narrative composition, content generation |
| Gemini | Data visualization suggestions, reference research |
| Codex | Template code generation, automation |

---

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2026-01-21
- **Compatible Platforms**: Claude, ChatGPT, Gemini, Codex

### Related Skills
- [technical-writing](../technical-writing/SKILL.md)
- [image-generation](../../creative-media/image-generation/SKILL.md)
- [marketing-automation](../../marketing/marketing-automation/SKILL.md)

### Tags
`#presentation` `#pptx` `#slides` `#storytelling` `#branding` `#pitch-deck`
