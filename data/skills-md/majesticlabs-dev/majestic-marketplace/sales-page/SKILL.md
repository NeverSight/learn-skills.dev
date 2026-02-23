---
name: sales-page
description: Create high-converting sales pages by orchestrating competitive research, positioning, copywriting, and offer skills. Assembles components into a complete sales page blueprint.
allowed-tools: Read Write Edit Grep Glob WebSearch WebFetch AskUserQuestion
disable-model-invocation: true
---

# Sales Page Blueprint

Orchestrate the creation of high-converting sales pages by combining specialized skills.

**Audience:** Founders and marketers creating sales pages for products at any price point.

**Goal:** Research competitors, find positioning angles, write conversion copy, and build irresistible offers.

## Conversation Starter

Use `AskUserQuestion` to gather initial context:

"I'll help you create a sales page that converts cold traffic into customers.

**Please provide:**
1. **Product/Service**: What are you selling?
2. **Price Point**: What does it cost?
3. **Target Customer**: Who is this for?
4. **Traffic Source**: Where will visitors come from?
5. **Competitors**: Who else sells something similar?

I'll research winning pages in your niche and build a conversion-optimized blueprint."

## Orchestration Workflow

### Phase 1: Research & Analysis

**Use `competitive-positioning` skill:**
- Analyze competitor sales pages
- Identify positioning weaknesses
- Find differentiation opportunities
- Craft unique positioning statement

### Phase 2: Find the Angle

**Use `positioning-angles` skill:**
- Select from 24 positioning frameworks
- Match angle to awareness stage
- Generate headline options for each angle
- Choose primary and secondary angles

### Phase 3: Build the Offer

**Use `irresistible-offer` skill:**
- Create 7-part offer framework
- Build value stack (10-20x perceived value)
- Design risk reversal/guarantee
- Add authentic scarcity elements
- Map objection destroyers

### Phase 4: Write the Copy

**Use `direct-response-copy` skill:**
- Write headlines using proven formulas
- Craft opening hooks
- Apply pain quantification
- Structure founder story
- Format testimonials as mini case studies
- Write benefit-oriented CTAs

### Phase 5: Assemble & Optimize

**Reference local resources:**
- [references/bullet-frameworks.md](references/bullet-frameworks.md) - Bullet point patterns
- [references/ab-test-insights.md](references/ab-test-insights.md) - Data-backed optimization

## Sales Page Structure

```
1. Above the Fold
   - Headline (from positioning-angles)
   - Subheadline with specific promise
   - Primary CTA
   - Trust signals

2. Problem Section
   - Quantified pain (direct-response-copy)
   - Agitation with vivid scenario

3. Solution Introduction
   - Transformation promise
   - Founder story (if applicable)

4. Features/Benefits
   - Bullets using frameworks (references/bullet-frameworks.md)
   - Feature → Benefit → Emotion chain

5. Social Proof
   - Testimonials as mini case studies
   - Logos, numbers, specifics

6. Offer Stack
   - Value stack from irresistible-offer
   - Price presentation with anchoring

7. Risk Reversal
   - Guarantee (from irresistible-offer)
   - Objection handlers

8. Final CTA
   - Urgency (if authentic)
   - Friction reducers
```

## Output Format

```markdown
# SALES PAGE BLUEPRINT: [Product/Service]

## Research Summary
[Key findings from competitive-positioning]

## Positioning Strategy
**Primary Angle:** [From positioning-angles]
**Tagline:** [From competitive-positioning]

## The Offer
[7-part framework from irresistible-offer]

## Copy Sections

### Above the Fold
[Headline, subheadline, CTA]

### Problem Section
[Quantified pain, agitation]

### Solution Section
[Transformation, story]

### Features/Benefits
[Bullets using frameworks]

### Social Proof
[Formatted testimonials]

### Offer Stack
[Value presentation]

### Guarantee
[Risk reversal copy]

### Final CTA
[Closing copy with urgency]

## A/B Test Recommendations
[From references/ab-test-insights.md]

## Implementation Checklist
[ ] Headline tested with 3 variations
[ ] Above-fold CTA present
[ ] Problem agitation complete
[ ] Minimum 10 benefit bullets
[ ] 3+ trust elements placed
[ ] Price properly anchored
[ ] Guarantee clearly stated
[ ] Mobile optimized
```

## Quality Standards

- **Research actual pages**: Use competitive-positioning skill for real examples
- **Data-backed decisions**: Reference ab-test-insights for optimization
- **Specific, not generic**: Every template should be customized
- **Orchestrate, don't duplicate**: Let specialized skills do the heavy lifting

## Related Skills

| Phase | Skill | Purpose |
|-------|-------|---------|
| Research | `competitive-positioning` | Competitor analysis |
| Strategy | `positioning-angles` | Find the angle |
| Offer | `irresistible-offer` | Build compelling offer |
| Copy | `direct-response-copy` | Write conversion copy |
| Hooks | `hook-writer` | Generate headline variations |
| Landing | `landing-page-builder` | Full page structure |
