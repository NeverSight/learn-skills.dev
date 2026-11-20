---
name: brand-identity
description: Builds brand foundations for a product, company, or personal brand, including a positioning statement, audience, personality traits with this-not-that pairs, voice, color and type direction, a logo brief with required versions, imagery style, and usage rules, delivered as a one-page Markdown brand guide. Use when asked to define a brand, create a brand guide, write a logo brief, or plan a rebrand. Not for UI color scales, which is color-system.
---

# Brand Identity

Produces a one-page brand guide that gives designers, writers, and developers the same answers about who the brand serves, how it sounds, and how it looks.

## When to use
- "Help me define the brand for my startup / app / portfolio."
- Writing a brief for a logo designer or for logo exploration.
- A product looks and sounds different on its website, app, and social channels.
- Personal branding for a freelancer, creator, or job seeker.
- A rebrand or refresh that must decide what to keep and what to change.

## Workflow
1. Gather inputs: what it is, who it is for, the problem it solves, 2–3 alternatives people use today, and existing assets (name, logo, colors) that must stay. Ask at most two questions if the audience or offer is unclear; otherwise state assumptions.
2. Write the positioning statement: "For [audience] who [need], [brand] is the [category] that [key benefit]. Unlike [alternative], it [differentiator]." Keep the differentiator provable.
3. Define the audience: primary and secondary segments, their context, what they value, and what would put them off.
4. Choose 3–5 personality traits, each with a this-not-that pair ("Confident, not arrogant"; "Playful, not childish") and one concrete example of it in practice.
5. Derive the voice: words to use and avoid, sentence length, humor level, and how tone shifts between errors and celebrations. Hand detailed microcopy rules to ux-writing.
6. Set visual direction: the role and mood of primary, accent, and neutral colors, and the character of display and text typefaces. Hand exact scales to color-system and typography-system.
7. Write the logo brief, the imagery and illustration style, and the usage rules.
8. Assemble the one-page guide and list decisions that still need validation with real users.

## Rules
**Strategy**
- Traits must separate the brand from alternatives; "modern, clean, simple" alone says nothing, so every trait gets a "not" side.
- Every visual decision traces back to a trait or an audience need; write the link.
- Never copy or closely imitate another company's name, logo, mascot, trademarked characters, or signature visual style. Recommend a trademark and domain check before committing to a name or mark, and note that this is not legal advice.

**Logo brief**
- Specify 2–3 concept directions with rationale and the constraints: works in one color, at small sizes, and on light and dark backgrounds.
- Required versions: horizontal lockup, stacked lockup, symbol or mark only, monochrome (black and white), and reversed.
- Define a minimum size (the width below which the full lockup switches to the mark) and clear space as a multiple of a logo element, such as the height of the mark, not a fixed pixel value.
- Deliverables: SVG for digital, PDF or EPS for print vendors, transparent PNG at several sizes, and favicon and app icon versions.

**Color and type direction**
- A primary color used behind text must reach 4.5:1 with its text color; otherwise reserve it for large elements and accents that need 3:1 (WCAG 2.2 AA).
- At most 2 typefaces (display and text), licensed for every planned use: web, app, print.

**Imagery**
- Describe style with concrete attributes: photography or illustration, lighting, color treatment, subjects, composition, and what to avoid. Include alt text guidance.

## Output
A single Markdown brand guide of about one page:
```
# [Brand] brand guide
## Positioning        statement + one-line pitch
## Audience           primary, secondary, what they value
## Personality        table: Trait | This | Not that | Example
## Voice              words to use and avoid, sample lines for 3 situations
## Color direction    ## Type direction
## Logo               brief, versions, minimum size, clear space, misuse
## Imagery and illustration
## Usage rules        do / don't
## Open decisions
```
- Next steps pointing to color-system, typography-system, design-tokens, and social-graphics where relevant.

## Avoid
- Trait lists without this-not-that pairs or examples.
- Choosing colors and fonts before positioning and personality exist.
- Logos that need gradients, fine detail, or color to be recognizable.
- Abstract mood words ("bold", "innovative") with no concrete example.
- Rules that cover only ideal use and not misuse (stretching, recoloring, busy backgrounds).
- Invented market data, statistics, or competitor claims.

## Final check
- [ ] The positioning statement names audience, need, category, benefit, and differentiator.
- [ ] 3–5 traits, each with a this-not-that pair and an example.
- [ ] Voice includes words to use and avoid plus sample lines.
- [ ] The logo brief lists all required versions, the minimum size rule, and the clear space rule.
- [ ] Color and type direction respect WCAG 2.2 AA contrast and font licensing.
- [ ] Nothing imitates another brand's protected assets.
- [ ] Open decisions are listed.
