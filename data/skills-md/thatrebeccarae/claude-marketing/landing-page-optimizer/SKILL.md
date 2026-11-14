---
name: landing-page-optimizer
description: Landing page audit and optimization for conversion. Covers above-the-fold design, value propositions, CTAs, social proof placement, form design, page speed, and mobile optimization. Use when the user asks about landing page optimization, conversion rate improvement, page audits, or CTA optimization.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: growth
  domain: landing-pages
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# Landing Page Optimizer

Audit and optimize landing pages for maximum conversion.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/landing-page-optimizer ~/.claude/skills/
```

## Audit Framework

### Above the Fold (First 5 Seconds)

The visitor must answer 3 questions instantly:
1. **What is this?** (Clear headline)
2. **Why should I care?** (Benefit-focused subheadline)
3. **What do I do next?** (Visible CTA)

### Hero Layout Patterns

| Pattern | Best For | Structure |
|---------|----------|-----------|
| **Left copy / right visual** | SaaS, B2B | Headline + CTA left, product screenshot right |
| **Centered hero** | Simple offers | Centered headline, subheadline, CTA |
| **Video hero** | Complex products | Autoplay background or embedded explainer |
| **Social proof hero** | High-trust needed | Headline with customer logos or metrics |
| **Split test** | Dual audiences | Two distinct paths with separate CTAs |

### Value Proposition Hierarchy

```
H1: Primary benefit (what outcome they get)
Subheadline: How you deliver it (mechanism or differentiator)
Supporting points: 3 proof points or features (bullets)
CTA: Specific action + anxiety reducer
```

### CTA Optimization

**Text:** Action verb + specific outcome ("Start Free Trial" not "Submit")
**Design:** High contrast to background, generous padding, whitespace around it
**Placement:** Above fold, after each content section, sticky on scroll
**Microcopy:** Reduce anxiety below CTA ("No credit card required", "Cancel anytime")

### Social Proof Patterns

| Type | Placement | Impact |
|------|-----------|--------|
| Customer logos | Below hero | Trust (B2B) |
| Metric ("50,000+ users") | Near headline | Scale proof |
| Star rating | Near CTA | Purchase confidence |
| Testimonial quote | Mid-page | Emotional proof |
| Case study result | Deep in page | Detailed proof |
| Trust badges | Near form/checkout | Security |

### Form Optimization

- Every field removed increases completion 5-10%
- Labels above fields (never placeholder-only)
- Inline validation (real-time, not on submit)
- Smart defaults and autofill (autocomplete attributes)
- Multi-step forms outperform single long forms
- Progress indicator for multi-step

### Mobile Optimization

- Touch targets minimum 48x48px
- Single column layout
- Thumb-friendly CTA placement (bottom half of screen)
- No horizontal scrolling
- Simplified navigation (hamburger or none)
- Fast load (LCP <2.5s on 4G)

## Conversion Benchmarks

| Page Type | Good | Average | Poor |
|-----------|------|---------|------|
| SaaS trial signup | >5% | 2-5% | <2% |
| E-commerce product | >3% | 1.5-3% | <1.5% |
| Lead gen (B2B) | >10% | 5-10% | <5% |
| Newsletter signup | >5% | 2-5% | <2% |
| Webinar registration | >30% | 15-30% | <15% |

## Anti-Patterns

1. **Multiple competing CTAs** — one primary action per page
2. **Feature-focused headline** — lead with benefit, not feature
3. **Stock photos** — real product screenshots or real people
4. **Navigation on landing pages** — remove nav for paid traffic pages
5. **Below-fold CTA only** — always have CTA above the fold
6. **No social proof** — every landing page needs trust signals
7. **Slow load time** — every 100ms delay costs 1% conversion
8. **Desktop-only design** — 60%+ traffic is mobile

## Integration with Other Skills

- **cro-auditor** — Broader CRO audit framework; this skill deep-dives on individual pages
- **ab-testing-framework** — Test the changes this skill recommends
- **copywriting-frameworks** — Apply PAS/AIDA to landing page copy
- **frontend-design** — Implement the optimized page design
- **technical-seo-audit** — Page speed and technical optimization
