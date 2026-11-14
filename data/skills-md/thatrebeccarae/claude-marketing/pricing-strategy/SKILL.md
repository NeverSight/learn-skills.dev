---
name: pricing-strategy
description: Pricing model design, competitive positioning, value metric selection, price testing, and pricing page optimization. Use when the user asks about pricing strategy, pricing models, price testing, value-based pricing, or competitive pricing analysis.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: strategy
  domain: pricing
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# Pricing Strategy

Pricing model design, competitive analysis, and pricing page optimization.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/pricing-strategy ~/.claude/skills/
```

## Pricing Models

| Model | How It Works | Best For | Risk |
|-------|-------------|----------|------|
| **Per-seat** | Price per user/month | Collaboration tools | Discourages adoption |
| **Usage-based** | Pay for what you use | APIs, infrastructure | Revenue unpredictability |
| **Tiered** | Feature-gated plans | SaaS with clear feature tiers | Complexity, feature gating frustration |
| **Freemium** | Free tier + paid upgrades | PLG, network effects | Low conversion (2-5% typical) |
| **Flat-rate** | One price for everything | Simple products | Leaves money on table |
| **Hybrid** | Base + usage or seat + usage | Complex products | Pricing complexity |
| **Per-unit** | Price per resource (project, site) | Agencies, multi-property | Usage ceiling anxiety |

## Value Metric Selection

The value metric is what you charge for (seats, API calls, revenue managed, etc.).

**Good value metric criteria:**
1. **Scales with customer value** — as they get more value, they naturally pay more
2. **Easy to understand** — customer can predict their bill
3. **Measurable** — you can track and bill accurately
4. **Controllable** — customer can influence their usage

| Product Type | Common Value Metrics |
|-------------|---------------------|
| Email marketing | Contacts, emails sent |
| Analytics | Events tracked, monthly users |
| CRM | Seats, contacts |
| Infrastructure | Compute hours, storage, requests |
| E-commerce platform | GMV, orders, SKUs |
| Design tools | Seats, projects, exports |

## Competitive Pricing Analysis

### Analysis Framework

1. **Inventory competitors** — list all direct and indirect alternatives
2. **Map pricing models** — how does each charge?
3. **Normalize to common unit** — price per seat/month at comparable usage
4. **Position on value map** — plot price vs. feature completeness
5. **Identify gaps** — underserved price points or segments

### Positioning Strategies

| Strategy | Description | When to Use |
|----------|-----------|-------------|
| **Premium** | Price above market, justify with value | Strong brand, unique features |
| **Competitive** | Match market prices | Commoditized market, feature parity |
| **Penetration** | Price below market to gain share | New entrant, land-and-expand model |
| **Value** | Price based on ROI delivered | Measurable customer outcomes |

## Good/Better/Best Tier Design

### Tier Structure

```
FREE (or Starter): Entry point — enough to get hooked, not enough for serious use
PRO (or Growth):   Primary revenue tier — designed for most customers
ENTERPRISE:        High-touch — custom pricing, premium support, compliance features
```

### Tier Design Rules

1. **Most Popular = middle tier** — anchor it visually and with a badge
2. **Free tier** limits should push to paid naturally (not by being crippled)
3. **Feature fences** should align with customer maturity (not arbitrary gates)
4. **Price anchoring** — show enterprise price to make pro feel reasonable
5. **Annual discount** — 15-20% for annual commitment (show monthly equivalent)

## Pricing Page Optimization

### Best Practices

- Default to annual billing toggle (pre-selected) with monthly option
- Show savings for annual ("Save 20%")
- Highlight recommended plan (visual emphasis + "Most Popular" badge)
- Feature comparison table with max 8-10 rows (not 40)
- CTA per plan with specific text ("Start Free Trial" vs "Contact Sales")
- Social proof per tier ("Used by 500+ teams")
- FAQ section addressing pricing objections
- Money-back guarantee or free trial prominently displayed

## Price Testing Methods

| Method | Sample | What It Tests |
|--------|--------|--------------|
| **Van Westendorp** | Survey 200+ | Price sensitivity (too cheap, too expensive, bargain, deal-breaker thresholds) |
| **Gabor-Granger** | Survey 300+ | Demand curve at specific price points |
| **A/B test** | Website traffic | Actual conversion at different prices |
| **Cohort pricing** | New signups | Different prices for different cohorts over time |

## Integration with Other Skills

- **cro-auditor** — Pricing page conversion optimization
- **ab-testing-framework** — Design price tests with statistical rigor
- **landing-page-optimizer** — Optimize the pricing page layout
- **icp-research** — Willingness to pay by segment
