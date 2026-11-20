---
name: reference-analysis
description: Analyze reference sites and extract brand elements (colors, typography, layout, animation style). Combines site reference analysis and brand extraction into one workflow. Use when a client provides reference sites or when analyzing an existing site for redesign.
allowed-tools: Read, Write, WebFetch, WebSearch, Bash
---

# Reference Analysis

## TL;DR (5 rules)
1. **Analyze dimensions, not pixels** — borrow layout philosophy, color mood, animation timing. Never copy exact code/assets.
2. **Extract to a structured brief** — colors (hex), fonts (family + weights), spacing, animation style, standout element
3. **Always add ONE unique element** — what makes THIS project memorable vs the reference?
4. **Check Atelier catalogs first** — SITE-TEARDOWNS, HERO-CATALOG, COMPONENT-CATALOG may already have the pattern documented
5. **Cross-reference fonts** against typography skill banned list — don't inherit a reference's Inter/Roboto habit

## When To Use
- Client provides a reference URL ("make it look like this")
- Redesigning an existing site (need to extract current brand first)
- Searching for design inspiration in a specific industry

## Checklist
- [ ] Fetched reference via WebFetch (homepage + 1-2 key pages)
- [ ] Documented: colors, typography, spacing, animation, standout element
- [ ] Extracted brand guidelines to markdown (if redesign)
- [ ] Identified ONE unique element for differentiation
- [ ] Cross-referenced fonts against typography skill
- [ ] Checked Atelier catalogs for existing patterns

---

## Phase 1: Find References

### Sources (by quality)
- **Awwwards** (awwwards.com) — Site of the Day winners
- **Godly** (godly.website) — Modern web design gallery
- **SiteInspire** (siteinspire.com) — Curated gallery
- **Land-book** (land-book.com) — Landing pages
- **Dribbble** (dribbble.com) — UI concepts
- **SaaSUI** (saasui.design) — SaaS dashboard patterns specifically

Use `WebSearch` for niche: "best [industry] website design 2026"

## Phase 2: Analyze the Reference

```
WebFetch URL: https://example.com
Prompt: Describe the layout structure, color palette (hex codes), font families, 
animation style, whitespace usage, and what makes this site distinctive.
```

Document as a structured brief:
```markdown
## Reference Brief: [site name]
**Vibe:** [e.g., Clean, confident, lots of whitespace]
**Layout:** [e.g., Asymmetric, full-bleed sections, split hero]
**Colors:** Primary #___ · Secondary #___ · Accent #___ · Background #___
**Typography:** Headlines: [font, weight] · Body: [font, weight]
**Animation:** [e.g., Subtle scroll reveals, spring tab indicators]
**Spacing:** [e.g., Generous — 48px section padding, 8px component scale]
**Standout Element:** [The ONE thing that makes it memorable]
```

## Phase 3: Extract Brand (for Redesigns)

When redesigning a client's existing site, extract their current brand identity:

1. **Fetch the site**: WebFetch homepage + about + services pages
2. **Document colors**: Primary, secondary, accent, background, text (with hex codes and where used)
3. **Document typography**: Heading font, body font, accent font (with weights)
4. **Document voice**: Tagline, value props, CTA patterns, tone (professional/casual/etc.)
5. **Note inconsistencies**: These are opportunities to improve

Output as `brand-guidelines.md` in the project folder.

## Phase 4: Adapt + Differentiate

Apply the CLIENT's identity on top of the reference vibe:
1. Swap in client's brand colors
2. Choose fonts from typography skill (not the reference's fonts)
3. Add ONE unique element: unusual interaction, distinctive color treatment, memorable entrance

### Ethical Boundaries
| Borrow | Don't Copy |
|--------|-----------|
| Layout patterns | Exact source code |
| Color philosophy | Their images/assets |
| Animation timing | Their written content |
| Typography approach | Their brand identity |
