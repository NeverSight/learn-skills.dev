---
name: landing-page-builder
description: Generate structured landing page copy OR audit existing pages for conversion optimization. Framework-agnostic - adapts approach based on awareness level and offer type.
triggers:
  - landing page
  - landing page copy
  - sales page copy
  - conversion page
  - lead page
  - audit landing page
  - optimize landing page
  - review my landing page
  - improve conversion
  - cro audit
allowed-tools: Read Write Edit AskUserQuestion WebFetch
disable-model-invocation: true
---

# Landing Page Builder

Two modes:
1. **Build Mode** (default): Generate structured landing page copy that converts
2. **Audit Mode**: Analyze existing pages and recommend conversion improvements

Detect mode from user intent. If they share a URL or existing copy, switch to Audit Mode.

## Required Inputs

Use `AskUserQuestion` to gather these inputs from the user:

| Input | Description |
|-------|-------------|
| **Product/Offer** | What's being offered (name, price, bonuses, guarantee) |
| **Target Audience** | Who this is for (demographics, psychographics) |
| **Pain Points** | 2-3 specific problems the audience faces |
| **Key Benefits** | 2-3 outcome-focused benefits |
| **Proof** | Testimonials, case studies, or statistics |
| **Page Goal** | Single conversion goal (lead, sale, demo, signup) |
| **Awareness Level** | Problem-aware, solution-aware, or product-aware |
| **Traffic Source** | Where visitors come from (ad copy, email, organic) |

If the user doesn't provide all inputs, ask for the missing ones before proceeding.

## Conversation Starter

If the user hasn't provided context, begin with:

---

I'll help you create landing page copy. Please share:

**The Basics:**
1. What product/service are you promoting? (name, price, offer details)
2. What's the conversion goal? (lead, sale, demo, signup)
3. Where is traffic coming from? (ads, email, organic - share the source copy if available)

**Your Audience:**
4. Who is this for? (role, situation, sophistication level)
5. What's their current painful situation vs. dream outcome?
6. What keeps them from taking action? (fears, objections, skepticism)

**Your Proof:**
7. Best testimonials or case studies? (specific results preferred)
8. Any trust indicators? (logos, credentials, media mentions)

I'll use this to create copy that matches your audience's awareness level.

---

## Output Structure

Produce copy in this order (a complete landing page):

### 1. Hero Section
- **Headline**: 8-12 words, matches traffic source messaging
- **Subheadline**: 15-20 words, expands on promise
- **Hero CTA**: Primary button text

### 2. Problem Section
- Acknowledge the pain (2-3 sentences)
- Show you understand their situation
- Create resonance before presenting solution

### 3. Solution Section
- Introduce the product/offer
- Explain the mechanism (how it works)
- Keep it simple - avoid jargon

### 4. Benefits Section
- 3-5 benefit blocks
- Each: bold outcome + supporting detail
- Focus on transformation, not features

### 5. Proof Section
- Testimonials with specific results
- Case study snippets
- Trust indicators (logos, numbers, credentials)

### 6. Objection Handling
- Address 2-3 common objections
- Use FAQ format or inline handling
- Turn skepticism into confidence

### 7. Offer Stack
- Clear breakdown of what's included
- Price presentation (anchor if appropriate)
- Bonuses listed with values
- Guarantee prominently displayed

### 8. Final CTA
- Urgency element if genuine
- Risk reversal reminder
- Clear button text

## Approach Guidelines

**For Problem-Aware audiences:**
- Lead with pain acknowledgment
- Spend more time on problem/agitate
- Educate on solution category before introducing product

**For Solution-Aware audiences:**
- Lead with differentiation
- Focus on why THIS solution
- Compare to alternatives (tactfully)

**For Product-Aware audiences:**
- Lead with offer/deal
- Focus on proof and objection handling
- Shorter copy, faster to CTA

## Audience Psychology Checklist

When gathering inputs, ensure you understand:

| Factor | Questions to Answer |
|--------|---------------------|
| **Current State** | What frustrations do they face daily? |
| **Desired State** | What does success look like to them? |
| **Hidden Fears** | What are they secretly afraid of? |
| **Trust Barriers** | Why might they not believe you? |
| **Decision Triggers** | What would make them act now? |

Use these insights to:
- Write problem sections that resonate emotionally
- Choose headlines that match their awareness
- Address objections before they arise
- Create urgency that feels authentic

## Quality Standards

1. **Message Match**: Headline must echo traffic source copy
2. **One Goal**: All copy drives toward single conversion
3. **Specific Proof**: No vague claims - numbers, names, results
4. **Clear CTA**: Obvious next step, no confusion
5. **Mobile-First**: Short paragraphs, scannable structure
6. **No Fluff**: Cut "very", "really", "just", "amazing"

## Output Format

```
## [PAGE TITLE]

### Hero
**Headline:** [8-12 words]
**Subheadline:** [15-20 words]
**CTA Button:** [Button text]

---

### Problem
[2-3 sentences acknowledging pain]

---

### Solution
[Product introduction + mechanism]

---

### Benefits
**[Benefit 1]**: [Supporting detail]
**[Benefit 2]**: [Supporting detail]
**[Benefit 3]**: [Supporting detail]

---

### Proof
[Testimonials/case studies/trust indicators]

---

### Objections
**[Objection 1]?** [Response]
**[Objection 2]?** [Response]

---

### Offer
**What You Get:**
- [Item 1] (Value: $X)
- [Item 2] (Value: $X)
- [Bonus] (Value: $X)

**Total Value:** $XXX
**Your Investment:** $XX

**Guarantee:** [Guarantee details]

---

### Final CTA
[Urgency + risk reversal + button text]
```

## What This Skill Does NOT Do

- Prescribe specific frameworks (AIDA, PAS, etc.) - you choose
- Generate multiple variations - one focused version
- Include design/visual direction - copy only
- Promise specific conversion rates

---

## CRO Audit Mode

When user provides existing page URL or copy, switch to audit mode.

### Detection

Audit mode triggers when user:
- Shares a URL to analyze
- Pastes existing landing page copy
- Asks to "review", "audit", "optimize", or "improve" a page

### CRO Analysis Hierarchy

Analyze in order of conversion impact (highest first):

| Priority | Element | What to Check |
|----------|---------|---------------|
| 1 | **Value Proposition** | Can visitor understand what this is and why they should care within 5 seconds? |
| 2 | **Headline** | Does it match traffic source? Specific outcome? Customer language? |
| 3 | **CTA Placement & Copy** | Above fold? Benefit-oriented? Repeated after proof? |
| 4 | **Visual Hierarchy** | Clear reading path? Key info scannable? |
| 5 | **Trust Signals** | Near CTAs? After benefit claims? Specific not generic? |
| 6 | **Objection Handling** | Top 3 objections addressed? Before final CTA? |
| 7 | **Friction Points** | Form length? Required fields? Unclear next steps? |

### Page-Type Experiment Libraries

Provide 3-5 prioritized experiments based on page type:

**Homepage Experiments:**
- Hero headline A/B (outcome vs. category statement)
- Social proof placement (above fold vs. below hero)
- CTA copy (action-focused vs. benefit-focused)
- Navigation visibility (full vs. minimal)

**Landing Page Experiments:**
- Long-form vs. short-form copy
- Video vs. text hero
- Single CTA vs. multiple CTAs
- Testimonial format (text vs. video vs. case study)
- Price anchoring presence

**Pricing Page Experiments:**
- Number of tiers (2 vs. 3 vs. 4)
- Feature comparison table presence
- Annual vs. monthly default
- "Most popular" badge placement
- FAQ section inclusion

**Signup Flow Experiments:**
- Single-page vs. multi-step form
- Social login prominence
- Field reduction (email-only vs. full form)
- Progress indicator presence
- Benefit reminders during form

### Audit Output Format

```markdown
## CRO AUDIT: [Page Name/URL]

### 5-Second Test Result
[What a visitor understands in 5 seconds - pass/fail]

### Priority Issues (Fix First)
1. **[Element]**: [Problem] → [Specific fix]
2. **[Element]**: [Problem] → [Specific fix]
3. **[Element]**: [Problem] → [Specific fix]

### Quick Wins (Easy improvements)
- [Change 1]
- [Change 2]
- [Change 3]

### Recommended Experiments
| Test | Hypothesis | Expected Impact |
|------|------------|-----------------|
| [Test 1] | [Why it might work] | High/Medium/Low |
| [Test 2] | [Why it might work] | High/Medium/Low |

### Rewritten Elements
**Current Headline:** "[Original]"
**Suggested Headline:** "[Improved version]"

**Current CTA:** "[Original]"
**Suggested CTA:** "[Improved version]"

### Before/After Score
| Element | Before | After (if implemented) |
|---------|--------|------------------------|
| Clarity | X/10 | X/10 |
| Trust | X/10 | X/10 |
| Urgency | X/10 | X/10 |
| Overall | X/10 | X/10 |
```

---

## When to Use This vs. `sales-page`

| Use `landing-page-builder` when... | Use `sales-page` when... |
|------------------------------------|--------------------------|
| You know your messaging already | Starting from scratch |
| Need quick copy execution | Want competitive research |
| Already have positioning | Need formula libraries |
| Time is limited | Want blueprint + templates |
| Auditing an existing page | Building from scratch with templates |
