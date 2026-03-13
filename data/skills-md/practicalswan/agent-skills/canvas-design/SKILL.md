---
name: canvas-design
description: Design philosophy docs and canvas-based visual creation. Use when articulating design principles, crafting multi-page design documents, or exploring aesthetic philosophy with intentional design thinking.
license: Complete terms in LICENSE.txt
---



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`


A two-step design workflow: first articulate a design philosophy, then create visual designs on canvas. Based on the [anthropics/skills canvas-design](https://github.com/anthropics/skills) approach.

## When to Use This Skill

- Creating design philosophy documents (.md)
- Generating visual canvas designs (.png/.pdf)
- Articulating design principles and aesthetic rationale
- Crafting multi-page design documents
- Exploring design thinking and intentional visual communication


---

## Step 1: Design Philosophy Document

Create a markdown document that articulates the design philosophy before any visual creation.

### Philosophy Document Structure
```markdown


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`


## Core Intent
What is this design trying to communicate? What feeling should it evoke?

## Guiding Principles
1. **[Principle Name]** — Explanation of how this shapes decisions
2. **[Principle Name]** — Explanation
3. **[Principle Name]** — Explanation

## Aesthetic Direction
- **Color Philosophy**: Why these colors, what they represent
- **Typography Philosophy**: What the type choices communicate
- **Spatial Philosophy**: How whitespace and layout serve the intent
- **Material/Texture**: Physical or digital texture decisions

## Inspirations & References
- [Reference 1]: What specifically resonates and why
- [Reference 2]: The element to borrow vs. what to avoid

## Anti-Patterns
- What this design explicitly avoids and why
```

### Philosophy Examples

**Minimalist App Design**:
> "Every element must earn its place. If removing something doesn't hurt the experience, it shouldn't exist. Whitespace is not empty — it's breathing room for the content that matters."

**Warm Community Platform**:
> "Design should feel like a well-lit kitchen — inviting, warm, organized but not sterile. Rounded corners, warm neutrals, and generous spacing signal 'you belong here.'"

**Technical Documentation**:
> "Clarity is kindness. Dense information needs generous hierarchy, consistent patterns, and visual anchors. The reader should never wonder where they are."

---

## Step 2: Canvas Creation

After establishing the philosophy, create visual designs that embody those principles.

### Canvas Workflow
1. **Review philosophy** — Reread the design philosophy document
2. **Define canvas** — Set dimensions, background, grid system
3. **Establish hierarchy** — Place primary elements first
4. **Apply philosophy** — Every decision references a stated principle
5. **Refine** — Remove anything that doesn't serve the core intent

### Essential Design Principles

| Principle | Description |
|-----------|-------------|
| **Intentionality** | Every element exists for a reason |
| **Hierarchy** | Guide the eye through deliberate contrast and spacing |
| **Consistency** | Repeated patterns build trust and comprehension |
| **Restraint** | Fewer elements, each carrying more weight |
| **Craftsmanship** | Pixel-perfect alignment, harmonious proportions |

### Multi-Page Documents
For multi-page designs:
- Maintain consistent margins and grid across pages
- Use a master color palette derived from the philosophy
- Create a visual rhythm — varying density to prevent monotony
- Include breathing pages (minimal content) between dense sections

### Quality Checklist
- [ ] Every element traces back to a stated principle
- [ ] Color choices align with the documented philosophy
- [ ] Typography serves the content hierarchy
- [ ] Whitespace is intentional, not leftover
- [ ] The design could be explained purely through its philosophy doc
- [ ] Nothing decorative exists without purpose

---

## Craftsmanship Emphasis

Design is a craft. The difference between good and great design:

- **Alignment**: Not "close enough" but mathematically precise
- **Spacing**: Consistent rhythm using a base unit (4px, 8px)
- **Color**: Not just "looks nice" but optically balanced, accessible (WCAG AA+)
- **Typography**: Line height, letter spacing, and measure all tuned for readability
- **Details**: Transitions, hover states, focus indicators — the invisible work

> "The details are not the details. They make the design." — Charles Eames
```
---

## References & Resources

### Documentation
- [Design Principles](./references/design-principles.md) — Gestalt principles, visual hierarchy, typography pairing, golden ratio, and grid systems
- [Color Psychology](./references/color-psychology.md) — Color emotional associations, harmony types, industry palettes, and accessibility

### Scripts
- [Palette Generator](./scripts/generate-palette.py) — Python script to generate color palettes with WCAG contrast ratio checking

### Examples
- [Kitchen Odyssey Design Philosophy](./examples/design-philosophy-example.md) — Complete design philosophy document example for a recipe sharing platform


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [frontend-design](../frontend-design/SKILL.md) | Color theory and layout principles for visual designs |
| [excalidraw-diagram-generator](../excalidraw-diagram-generator/SKILL.md) | Diagram generation for architecture and process visuals |

---
