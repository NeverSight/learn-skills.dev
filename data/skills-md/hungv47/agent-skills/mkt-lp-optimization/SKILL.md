---
name: mkt-lp-optimization
description: This skill should be used when the user asks to "optimize a landing page", "improve conversion rates", "review my landing page", "create a high-converting landing page", "audit my LP", "reduce bounce rate", or mentions landing page design, conversion optimization, A/B testing strategy, or CTA optimization.
license: MIT
metadata:
  author: hungv47
  version: "2.1.0"
  sources:
    - https://copyhackers.com
    - https://cxl.com
    - https://unbounce.com/landing-page-articles/
---

# Landing Page Conversion Optimization

*Horizontal skill — optimizes the conversion layer where communication meets action.*

## Inputs Required
- Landing page URL or description of the page
- ICP research from `.agents/mkt/icp-research.md` (recommended — VoC language strengthens copy)
- Traffic source context (where visitors come from)

## Output
- Optimization recommendations with specific copy/structure changes
- For new pages: complete page structure with copy

## Quality Gate
Before delivering, verify:
- [ ] Headline scores ≥3 out of 4 on the U's (Useful, Unique, Urgent, Ultra-specific)
- [ ] Message matches the traffic source (headline echoes the ad/link that brought them)
- [ ] One primary CTA per page (secondary CTAs don't compete)
- [ ] Trust signals appear within scroll-distance of every CTA
- [ ] Form has ≤5 fields (or justified why more are needed)

## Chain Position
Horizontal — works with `mkt-icp-research` (audience data), `mkt-copywriting` (copy principles), `mkt-experiment` (test design)

---

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If available, read for product details and accuracy.

### Required Artifacts
None — can audit any page standalone.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `icp-research.md` | mkt-icp-research | VoC data for persuasion |
| `product-context.md` | mkt-copywriting | Product details for accuracy |
| `experiment-*.md` | mkt-experiment | Test design context |

---

## Core Frameworks

### 4-U Headline Formula

| U | Question | Scoring |
|---|---------|---------|
| **Useful** | Does it communicate clear value? | Y/N |
| **Unique** | Could a competitor use this headline? | Y/N (N = good) |
| **Urgent** | Is there a reason to act now? | Y/N |
| **Ultra-specific** | Does it include a number or concrete outcome? | Y/N |

80% of visitors won't read past the headline. Generate 10+ variations, score each.

### PAS Copy Framework

1. **Problem**: Lead with pain in the audience's own language. If `.agents/mkt/icp-research.md` exists, use VoC quotes directly.
2. **Agitate**: What happens if they don't solve this? Make consequences vivid.
3. **Solve**: Your product as the relief. Benefits, not features.

### Message Match

Check: does the landing page headline echo the exact promise from the ad/email/link? Broken promise = instant bounce.

**WebSearch directive:** If auditing a live page, search `site:[domain] "[headline text]"` to find the ads/links driving traffic. Verify message match.

### First-Person CTA

"Get MY guide" > "Get YOUR guide" (90% more clicks). Formula: `[Action Verb] + [What They Get]`

---

## Quick Reference

### Social Proof Hierarchy (most → least powerful)
1. Testimonials with specific results ("Increased revenue 40% in 3 months")
2. Case studies with before/after numbers
3. Customer count ("Join 10,000+ teams")
4. Media mentions / press logos
5. Expert endorsements
6. Customer logos

### Cognitive Bias Stack

| Bias | How to Apply |
|------|-------------|
| Loss aversion | "Don't miss..." / limited genuine availability |
| Social proof | Testimonials near CTAs, user counts |
| Anchoring | Show higher price first, then actual price |
| Reciprocity | Give free value before asking (lead magnet, calculator) |
| Authority | Expert quotes, certification badges, press logos |

### Form Rules
- ≤5 fields. Every additional field costs ~10% conversions
- Start with just email. Use progressive profiling for the rest
- Each field must justify its existence — if you can ask later, do

### Trust Signals
Cluster near CTAs and forms: security badges, money-back guarantee, privacy link, contact info.

---

## Testing Priority

Test in this order (highest impact first):
1. Headlines (biggest swing)
2. Offers (what you're promising)
3. CTAs (text, color, placement)
4. Page layout
5. Form fields

Use `mkt-experiment` for proper test design with success/kill thresholds and sample size validation.

---

## Workflows

### New Landing Page
1. Read ICP research (if available) for VoC language and pain points
2. Define primary conversion goal (one per page)
3. Generate 10+ headline variations using 4-U formula
4. Structure body with PAS framework
5. Add social proof (strongest above fold)
6. Design form (minimal fields)
7. Place trust signals near every CTA
8. Verify message match with traffic source
9. Run through quality gate checklist

### Optimization Audit
1. Check message match between traffic sources and headline
2. Score headline against 4-U formula
3. Audit social proof: placement, specificity, relevance
4. Count form fields — can any be removed?
5. Check mobile experience (thumb zone CTAs, load time)
6. Identify highest-impact fix
7. Design A/B test via `mkt-experiment`

---

## Artifact Frontmatter

When saving optimization artifacts, use this frontmatter:

```yaml
---
skill: mkt-lp-optimization
version: 1
date: [today's date]
status: draft
---
```

> On re-run: rename existing artifact to `[name].v[N].md` and create new with incremented version.

---

## References

| Reference | Use For |
|-----------|---------|
| [core-principles.md](references/core-principles.md) | Headlines, value props, CTAs, forms, message match, PAS |
| [social-proof-trust.md](references/social-proof-trust.md) | Social proof hierarchy, biases, trust signals |
| [ux-design.md](references/ux-design.md) | Visual hierarchy, mobile optimization |
| [advanced-psychology.md](references/advanced-psychology.md) | Headline formulas, close sequences, pricing, urgency |
| [testing-optimization.md](references/testing-optimization.md) | A/B testing, tracking |
| [implementation-checklist.md](references/implementation-checklist.md) | Pre-launch checklists |
