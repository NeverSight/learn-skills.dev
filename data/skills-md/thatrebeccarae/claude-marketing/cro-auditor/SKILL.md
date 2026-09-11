---
name: cro-auditor
description: Conversion Rate Optimization auditing for landing pages, signup flows, checkout funnels, forms, and CTAs. Identifies friction points, runs heuristic evaluations, produces prioritized recommendations using ICE/PIE frameworks. Use when the user asks about conversion optimization, funnel analysis, landing page audits, form optimization, CTA testing, or checkout improvement.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: growth
  domain: conversion-optimization
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# CRO Auditor

Conversion Rate Optimization — audit landing pages, funnels, forms, and CTAs for friction and opportunities.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/cro-auditor ~/.claude/skills/
```

## Audit Framework

### Heuristic Evaluation (LIFT Model)

Score each page element on 6 dimensions:

| Factor | Question | Increases/Decreases Conversion |
|--------|----------|-------------------------------|
| **Value Proposition** | Is the benefit clear and compelling? | Increases |
| **Relevance** | Does this match what brought the user here? | Increases |
| **Clarity** | Is the message and action obvious? | Increases |
| **Urgency** | Is there a reason to act now? | Increases |
| **Anxiety** | Are there concerns about taking action? | Decreases |
| **Distraction** | Are there elements competing for attention? | Decreases |

### Page-Level Audit Checklist

#### Above the Fold
- [ ] Value proposition visible without scrolling
- [ ] Primary CTA visible and prominent
- [ ] Hero image/visual supports the message (not stock photo)
- [ ] Navigation does not distract from primary conversion goal
- [ ] Page loads in under 2.5 seconds (LCP)

#### Value Proposition
- [ ] Headline communicates specific benefit (not feature)
- [ ] Subheadline provides supporting detail
- [ ] Unique differentiator is clear (why you vs alternatives)
- [ ] Social proof near the value proposition (logos, count, rating)

#### Call to Action
- [ ] CTA text is action-oriented and specific ("Start Free Trial" not "Submit")
- [ ] CTA button contrasts with page design (stands out visually)
- [ ] Single primary CTA per page section (no competing actions)
- [ ] CTA appears multiple times on long pages (top, middle, bottom)
- [ ] Microcopy near CTA reduces anxiety ("No credit card required")

#### Social Proof
- [ ] Customer logos (if B2B)
- [ ] Testimonials with real names, photos, and specific results
- [ ] Case studies or metrics ("Helped 5,000+ companies increase revenue by 34%")
- [ ] Trust badges (security, certifications, awards)
- [ ] User count or activity ("Join 50,000+ marketers")

#### Forms
- [ ] Minimum fields necessary (every field reduces conversion 5-10%)
- [ ] Labels above fields (not placeholder-only)
- [ ] Inline validation with helpful error messages
- [ ] Progress indicator for multi-step forms
- [ ] Autofill enabled (autocomplete attributes)
- [ ] Mobile-friendly input types (tel, email, number)

#### Friction & Anxiety
- [ ] No unexpected costs or requirements revealed late
- [ ] Privacy policy and terms linked (not gating)
- [ ] Money-back guarantee or free trial clearly stated
- [ ] Contact information visible (phone, chat, email)
- [ ] FAQ section addressing common objections

### Funnel Analysis

#### Funnel Mapping

```
Awareness → Interest → Desire → Action → Retention
   ↓          ↓          ↓        ↓          ↓
 Ad/SEO → Landing → Pricing → Signup → Onboarding
            Page      Page      Form      Flow
```

For each stage:
1. **Traffic volume**: How many users enter this stage?
2. **Drop-off rate**: What percentage leave without advancing?
3. **Top exit pages**: Where exactly do users abandon?
4. **Friction indicators**: Time on page, scroll depth, rage clicks

#### Conversion Benchmarks

| Page Type | Good | Average | Poor |
|-----------|------|---------|------|
| Landing page (paid traffic) | >5% | 2-5% | <2% |
| Landing page (organic) | >3% | 1-3% | <1% |
| Signup form | >25% | 10-25% | <10% |
| Checkout (e-commerce) | >3% | 1.5-3% | <1.5% |
| Free trial → paid | >25% | 10-25% | <10% |
| Email opt-in | >5% | 2-5% | <2% |
| Pricing page → signup | >10% | 5-10% | <5% |

### Prioritization Frameworks

#### ICE Score

| Dimension | Definition | Scale |
|-----------|-----------|-------|
| **Impact** | How much will this change improve conversion? | 1-10 |
| **Confidence** | How sure are we this will work? | 1-10 |
| **Ease** | How easy is it to implement? | 1-10 |

**ICE Score** = (Impact + Confidence + Ease) / 3

#### PIE Score

| Dimension | Definition | Scale |
|-----------|-----------|-------|
| **Potential** | How much room for improvement? | 1-10 |
| **Importance** | How valuable is the traffic to this page? | 1-10 |
| **Ease** | How easy is it to run a test? | 1-10 |

**PIE Score** = (Potential + Importance + Ease) / 3

## Audit Output Format

### Executive Summary
- Current conversion rate vs benchmark
- Top 3 conversion killers identified
- Estimated revenue impact of fixes
- Quick wins (implementable in <1 day)

### Issue Format

```
**Issue:** [What is wrong]
**Location:** [Page/element affected]
**Impact:** [HIGH/MEDIUM/LOW] — [Estimated conversion impact]
**Evidence:** [Data, heuristic principle, or benchmark comparison]
**Fix:** [Specific recommendation]
**Test:** [A/B test hypothesis: "Changing X will increase Y by Z%"]
**ICE Score:** [X/10]
```

### A/B Test Recommendations

For each recommendation, provide:
- **Hypothesis**: If we [change], then [metric] will [improve/increase] because [reason]
- **Primary metric**: The conversion metric to measure
- **Minimum sample size**: Based on current traffic and expected effect size
- **Test duration**: Minimum days to reach significance (usually 2-4 weeks)

## Common Conversion Killers

1. **Slow page load** — Every 100ms delay reduces conversion by 1%
2. **Unclear value proposition** — Visitor cannot answer "What is this and why should I care?" in 5 seconds
3. **Too many form fields** — Each additional field reduces completion by 5-10%
4. **Weak CTA** — Generic text ("Submit", "Click Here") vs specific ("Start Free Trial")
5. **No social proof** — 92% of consumers read reviews before purchasing
6. **Hidden costs** — Unexpected shipping/fees are the #1 reason for cart abandonment
7. **Competing CTAs** — Multiple equal-weight actions create decision paralysis
8. **Mobile friction** — Tiny buttons, horizontal scroll, slow load on mobile
9. **Trust deficit** — No security badges, reviews, or contact info
10. **Exit without capture** — No email capture, exit intent, or remarketing pixel

## Integration with Other Skills

- **google-analytics** — Pull conversion data to ground CRO recommendations in real metrics
- **landing-page-optimizer** — Deep-dive on specific landing pages (when built)
- **a-b-testing-framework** — Design and analyze tests for CRO recommendations (when built)
- **pro-report-builder** — Generate professional CRO audit deliverable
