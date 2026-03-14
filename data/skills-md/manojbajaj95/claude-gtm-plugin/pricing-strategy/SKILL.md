---
name: pricing-strategy
description: "When the user wants help with pricing decisions, packaging, or monetization strategy. Use when the user mentions 'pricing,' 'pricing model,' 'pricing tiers,' 'freemium,' 'free trial,' 'packaging,' 'price increase,' 'value metric,' 'Van Westendorp,' 'willingness to pay,' 'monetization,' 'pricing strategy,' 'pricing experiments,' 'price anchoring,' 'enterprise pricing,' 'GTM pricing,' 'price setting,' 'value-based pricing,' 'revenue optimization,' or 'pricing psychology.' This skill covers pricing research, tier structure, packaging strategy, discount frameworks, upsell mechanics, and pricing experiments."
---

# Pricing Strategy

Expert guidance on SaaS pricing, value metrics, tier structure, pricing research, and monetization.

## Before Starting

Gather: product type, target market (SMB/mid-market/enterprise), GTM motion (self-serve/sales-led/hybrid), primary value delivered, competitive pricing, current conversion rate and ARPU, pricing goals (growth vs. revenue vs. profitability).

---

## Pricing Fundamentals

**Three axes**: Packaging (what's in each tier) + Value metric (what you charge for) + Price point (the amount).

**Core principle**: 1% improvement in pricing = 11% improvement in profit (McKinsey). Price to value, not cost.

**Value-based pricing**: Price between the next best alternative and perceived value. Cost is a floor, not a basis.

```
Perceived value of your solution: $1,000
Your price:                        $500  ← capture value here
Next best alternative:             $300  ← your floor
Your cost to serve:                 $50
```

**Value calculation template**:
```
Time savings: [hours/week × hourly rate × 52]
Revenue impact: [additional deals × deal value × 12]
Cost avoidance: [errors prevented × cost per error × 12]
Total annual value: $____

Suggested price: $[10% of value] – $[20% of value] / year
```

---

## Pricing Models

| Model | Pros | Cons |
|-------|------|------|
| **Flat Rate** ($99/mo, unlimited) | Simple to sell | Leaves money on table |
| **Tiered** (Starter/Pro/Business) | Captures segments, clear upsell | Anchor pricing matters |
| **Usage-Based** ($0.01/call) | Perfect value alignment, low barrier | Unpredictable revenue |
| **Hybrid** ($49/mo + $0.50/extra user) | Predictable base + scales | More complex to explain |

---

## Value Metrics

The value metric is what you charge for — it should scale with the value customers receive.

| Metric | Best For | Examples |
|--------|----------|---------|
| Per user/seat | Collaboration tools | Slack, Notion |
| Per usage/consumption | Variable workloads | AWS, Twilio |
| Per contact/record | CRM, email tools | Mailchimp, HubSpot |
| Per transaction | Payments, marketplaces | Stripe, Shopify |
| Flat fee | Simple, bounded products | Basecamp |
| Revenue share | High-value outcome tools | Affiliate platforms |

**Choosing your metric**: Analyze which usage patterns predict retention and expansion in your highest-LTV customers. If "more of X = more value," X is your metric.

---

## Pricing Research Methods

### Van Westendorp Price Sensitivity Meter

Ask 100–300 respondents four questions:
1. Too expensive — would not buy
2. Too cheap — would question quality
3. Expensive but would consider
4. Bargain / great value

**Key intersections**:
- PMC (Point of Marginal Cheapness): "Too cheap" × "Expensive" → lower bound
- PME (Point of Marginal Expensiveness): "Too expensive" × "Cheap" → upper bound
- OPP (Optimal Price Point): "Too cheap" × "Too expensive" → best price
- IDP (Indifference Price Point): "Expensive" × "Cheap" → acceptable midpoint

**Acceptable range**: PMC → PME. **Optimal zone**: OPP → IDP.

### MaxDiff / Feature Importance

Show sets of 4–5 features; ask "most important" and "least important." Results rank features by utility score:

| Utility | Packaging Decision |
|---------|-------------------|
| Top 20% | Include in all tiers (table stakes) |
| 20–50% | Use to differentiate tiers |
| 50–80% | Higher tiers only |
| Bottom 20% | Cut or premium add-on |

### Willingness to Pay

- **Gabor-Granger**: Show price → "Would you buy at $X?" (Yes/No). Vary price across respondents to build demand curve.
- **Conjoint analysis**: Show bundles at different prices; respondents choose preferred option.

---

## Tier Structure

**The Rule of 3**: Starter (50–60% of customers) → Pro/sweet spot (30–40%) → Business/Enterprise (5–10%).

**Anchor pricing**: Middle tier 3–4× starter price; top tier 2–3× middle. This makes the middle tier the obvious choice.

```
Starter:  $29/mo  — core features, 5 users, email support
Pro:      $99/mo  — everything + integrations, 20 users, priority support  ← Most Popular
Business: $299/mo — everything + SSO, unlimited users, dedicated support
```

### Good-Better-Best Framework

| Tier | Purpose | Price | Target |
|------|---------|-------|--------|
| **Good** (Starter) | Remove barriers to entry | Low, accessible | Small teams, trial converts |
| **Better** (Pro) | Where most customers land | Anchor price | Growing teams |
| **Best** (Business) | Capture high-value customers | 2–3× Better | Larger teams, power users |

### Feature Gating

**What to gate:**
- Scale limits: users, projects, API calls, storage
- Sophistication: advanced analytics, automations, integrations
- Control: SSO/SAML, admin roles, audit logs, custom branding

**Never gate**: core functionality, security features, data export.

---

## Freemium vs. Free Trial

| | Freemium | Free Trial |
|-|----------|-----------|
| **Best for** | PLG, wide top of funnel | Sales-led, high-ACV |
| **Conversion** | 2–5% free → paid | 15–25% trial → paid |
| **Risk** | Free riders, support cost | Shorter window to prove value |
| **Use when** | Network effects, viral growth | Complex product needing onboarding |

---

## Pricing Psychology

- **Anchor effect**: Show highest tier first to anchor perception
- **Charm pricing**: $49 vs. $50 (perceived as significantly cheaper)
- **Decoy pricing**: Add a "bad" middle option to push customers to "best"
- **Annual vs. monthly**: Offer 15–20% discount for annual (improves LTV and reduces churn). Offer at signup, after 2–3 months, and during renewal
- **Per user transparency**: Show total cost at common team sizes (e.g., "5 users = $X/mo")

---

## Pricing Experiments

**What to A/B test**: Price points, tier packaging, billing frequency, free trial length, anchor tier.

**Sample sizes**: ~1,000 visitors/variant to detect 10% change; ~5,000 for 5% change.

**Metrics to track**: Conversion (trial → paid), ARPU, CAC, LTV, payback period.

**Price increases**: Raise every 12–18 months as you add value. Communicate 30+ days in advance. Grandfather existing customers for 12 months or offer annual lock-in at current price.

---

## Revenue Expansion

**Upsell triggers**:
- User hits usage limit → show upgrade prompt immediately
- User clicks locked feature → show upgrade at moment of value
- User active 30+ days on starter → "power user" upgrade nudge

**Add-ons** (use when a feature has standalone value not everyone needs):
```
Base plan: $99/mo
+ Extra users: $10/user/mo
+ Advanced analytics: $49/mo
+ White label: $99/mo
+ Priority support: $199/mo
```

---

## Pricing by Segment

| Segment | Price Point | Sales Motion | Decision Maker | Sales Cycle |
|---------|-------------|--------------|----------------|-------------|
| SMB | $29–99/mo | Self-serve | End user/team lead | Minutes–days |
| Mid-Market | $99–999/mo | Self-serve + light touch | Dept head | Days–weeks |
| Enterprise | $1,000+/mo | High-touch sales | VP/C-level | Weeks–months |

---

## Key Metrics

| Metric | Healthy Benchmark |
|--------|------------------|
| Trial → Paid conversion | >15% |
| MRR Growth (early stage) | >10%/month |
| Churn Rate | <5%/mo (SMB), <1%/mo (enterprise) |
| LTV:CAC | >3:1 |
| Payback Period | <12 months |
| Net Revenue Retention | >100% |

---

## Discount Framework

| Type | Trigger | Range |
|------|---------|-------|
| Volume | Commitment to scale | 10–30% |
| Term | Annual commitment | 15–25% (2 months free) |
| Competitive | Switching from competitor | 20–40% |
| Strategic | Reference customer / logo value | Up to 50% |

**Never discount when**: customer hasn't articulated value, no competitive pressure, early in negotiation, or deal doesn't meet minimum size.

**Alternatives to discounting**: extended payment terms, additional services/training, extended trial, success milestone unlocks, multi-year lock-in.

---

## Common Pricing Mistakes

- Pricing on cost, not value
- Too many tiers (analysis paralysis — stick to 3)
- Feature gates customers don't care about
- Gating core functionality (lock what makes your product worth using)
- Complex value metric (users shouldn't need a calculator for their bill)
- Ignoring price sensitivity by segment
- Never testing or iterating on pricing
- Burying the price page (hiding = distrust)

---

## Price Increase Playbook

1. **Quantify value** delivered since last price (new features, outcomes, benchmarks)
2. **Grandfather existing customers** for 3–6 months (or 12 months for best customers)
3. **Communicate early** (60-day notice minimum)
4. **Frame as investment** not cost increase — tie to ROI
5. **Offer annual lock-in** before increase date to capture cash
6. **Monitor churn** closely for 90 days post-increase

---

## Checklists

**Launching pricing**:
- [ ] Pick value metric; design 3 tiers with anchor prices (3–4× between tiers)
- [ ] Package features (60% / 85% / 100%); offer 14-day trial; set up billing

**Optimizing pricing**:
- [ ] Track conversion rates by tier; survey customers on pricing perception
- [ ] A/B test price points; add annual billing option; create in-app upgrade prompts
- [ ] Monitor NRR; review pricing every 6–12 months

---

*Deep-dive on pricing models, discount structures, and services pricing: see `references/pricing.md`*
