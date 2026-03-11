---
name: pricing-strategy
description: "Design products around price using Madhavan Ramanujam's \"Monetizing Innovation\" methodology—determine willingness to pay before you build, not after. Use when: **Set pricing for a new product** before or during development; **Validate willingness to pay** before investing in features; **Structure pricing tiers** (Good-Better-Best) for different segments; **Choose the right monetization model** (subscription, usage-based, freemium, etc.); **Diagnose why a product isn't monetizing** as expected"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Pricing Strategy

> Design products around price using Madhavan Ramanujam's "Monetizing Innovation" methodology—determine willingness to pay before you build, not after.

## When to Use This Skill

Use this skill when you need to:

- **Set pricing for a new product** before or during development
- **Validate willingness to pay** before investing in features
- **Structure pricing tiers** (Good-Better-Best) for different segments
- **Choose the right monetization model** (subscription, usage-based, freemium, etc.)
- **Diagnose why a product isn't monetizing** as expected
- **Avoid common pricing failures** like leaving money on the table
- **Communicate value** in ways that justify your price
- **Maintain price integrity** after launch

This skill is particularly valuable for:
- Product managers designing new offerings
- Founders pricing SaaS or subscription products
- Teams launching into new markets or segments
- Companies suspecting they're underpricing
- Anyone who built first and is now struggling to monetize

---

## Methodology Foundation

**Source:** Madhavan Ramanujam & Georg Tacke - *Monetizing Innovation: How Smart Companies Design the Product Around the Price* (2016)

**Core Principle:** Price determines product, not the other way around. Companies that design products around willingness to pay—rather than pricing as an afterthought—capture dramatically more value.

> "Price isn't a number. It's the perceived value that your product holds for the customer."

---


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

When invoked, I will guide you through the Monetizing Innovation methodology:

1. **Diagnose monetization risk** by identifying which failure type threatens your product
2. **Conduct willingness-to-pay research** with the right questions
3. **Segment customers** by value perception, not demographics
4. **Configure products** using Leaders/Fillers/Killers and Good-Better-Best
5. **Select the right monetization model** for your business
6. **Apply behavioral pricing tactics** to optimize conversion
7. **Build price integrity** and avoid post-launch erosion

---

## How to Use

Provide information about your pricing situation:

**Example prompts:**

- "Help me set pricing for my new B2B SaaS product"
- "I think we're underpricing our service—how do I validate and fix this?"
- "Design a Good-Better-Best pricing structure for our software"
- "What monetization model should I use for a developer tool?"
- "Our new product launched but sales are disappointing—diagnose the pricing"

**Information that helps:**

- Your product/service description
- Target customer segments
- Current pricing (if any)
- Competitor pricing landscape
- Key features and their perceived value
- Business model and goals
- Any existing willingness-to-pay data

---

## Instructions

### Phase 1: Diagnose Monetization Risk

Before setting prices, identify which failure type threatens your product:

#### The Four Types of Monetization Failure

| Failure Type | Symptoms | Root Cause |
|--------------|----------|------------|
| **Feature Shock** | Too many features, high price, confused value prop | Built everything instead of what customers pay for |
| **Minivation** | Strong adoption, weak revenue | Priced too low, leaving money on table |
| **Hidden Gem** | Great innovation stuck inside company | Dismissed as "not our core business" |
| **Undead** | No willingness to pay at any price | Built on assumptions, not customer evidence |

**Diagnostic Questions:**

1. Have you validated willingness to pay with real customers?
2. Are you including features because customers will pay for them, or because you can build them?
3. Could any feature be a standalone paid product?
4. Is there evidence customers would pay more than your current price?

---

### Phase 2: Conduct Willingness-to-Pay Research

**Critical:** This happens BEFORE product design is finalized, not after.

#### The Four Key Questions

Ask potential customers:

1. **"What would be an acceptable price for [product]?"**
   - Establishes the comfort zone

2. **"What would be an expensive price?"**
   - Identifies the premium threshold

3. **"What would be a prohibitively expensive price?"**
   - Finds the ceiling

4. **"Would you buy this at $X?"**
   - Tests specific price points

**Follow every answer with: "Why?"**

#### Research Methods

| Method | Best For | Sample Size |
|--------|----------|-------------|
| **1:1 Interviews** | Deep understanding, B2B | 10-20 customers |
| **Focus Groups** | Testing reactions, consumer | 3-5 groups of 6-8 |
| **Surveys** | Quantitative validation | 100+ responses |
| **Purchase Simulations** | Realistic behavior data | 50+ scenarios |

#### Pro Tips for WTP Conversations

- Position as a conversation about "value," not "pricing"
- Make 25% of questions "why" questions
- Look at distributions, not just averages (you may have distinct segments)
- Be precise: "Would you buy at $20?" not "Would you buy?"
- Test features individually to understand relative value

---

### Phase 3: Segment by Willingness to Pay

**Critical shift:** Segment by needs and willingness to pay, NOT demographics.

**Wrong segmentation:**
- Small/Medium/Enterprise (by company size)
- Marketing/Sales/Product (by role)
- US/Europe/Asia (by geography)

**Right segmentation:**
- High-value seekers vs. budget-conscious buyers
- Power users vs. occasional users
- Self-service vs. high-touch support needs

#### Segmentation Process

1. **Cluster by WTP data** - Group customers with similar price sensitivity
2. **Validate with behavior** - Do they actually behave differently?
3. **Ensure you can reach them** - Can marketing/sales target this segment?
4. **Keep it simple** - Fewer segments is better (3-4 max)
5. **Describe for action** - Define segments so teams can sell to them

---

### Phase 4: Configure Products with Leaders, Fillers, Killers

#### Identify Feature Types

| Feature Type | Definition | Identification | Action |
|--------------|------------|----------------|--------|
| **Leaders** | Drive purchase decision, high WTP | >50% highly value, willing to pay | Emphasize, charge premium |
| **Fillers** | Nice-to-have, rounds out offering | 30-50% value, moderate WTP | Include in bundles |
| **Killers** | Low value, blocks deals if included | <20% value OR >20% actively dislike | Remove or make optional |

#### Build Good-Better-Best Tiers

```
GOOD (Entry)          BETTER (Standard)       BEST (Premium)
━━━━━━━━━━━━━━        ━━━━━━━━━━━━━━━━        ━━━━━━━━━━━━━━━
Core Leaders only     Leaders + Key Fillers   All Leaders + Fillers
Self-service          Email support           Priority support
Basic limits          Generous limits         Unlimited/Custom
$X/month             $2-3X/month             $5-10X/month
```

**Configuration Principles:**

- Each tier appeals to a specific segment
- Don't give away too much in entry tier
- Clear differentiation between tiers
- Maximum 4 tiers, 9 benefits per tier
- **Requires courage to remove features**

---

### Phase 5: Select the Right Monetization Model

**Key insight:** How you charge is often more important than how much.

#### Five Monetization Models

| Model | Description | Best For | Example |
|-------|-------------|----------|---------|
| **Subscription** | Fixed recurring payment | Predictable value delivery | Netflix, SaaS |
| **Usage-Based** | Pay per unit consumed | Variable consumption | AWS, Twilio |
| **Freemium** | Free tier + paid upgrades | High-volume acquisition | Slack, Dropbox |
| **Dynamic** | Prices vary by demand | Perishable inventory | Airlines, Uber |
| **One-Time** | Single purchase | Finite value delivery | Software licenses |

#### Model Selection Questions

1. **Customer acceptance:** Will customers accept this model?
2. **Future-proofing:** Does it work as the product evolves?
3. **Company stage:** Does it match your growth phase?
4. **Competition:** What are competitors doing?
5. **Implementation:** How hard is it to execute?

#### Hybrid Approaches

Many successful products combine models:
- **Subscription + Usage:** Base fee + overage charges
- **Freemium + Subscription:** Free tier + paid tiers
- **One-Time + Recurring:** License + maintenance fees

---

### Phase 6: Apply Behavioral Pricing Tactics

> "Behavioral pricing is the magic that happens when value pricing meets irrational customer psychology."

#### Six Proven Tactics

**1. Compromise Effect**
When presented with 3 options, people choose the middle.
- **Application:** Design 3 tiers where the middle is most profitable
- **Why it works:** Reduces decision anxiety, feels "safe"

**2. Anchoring**
First price seen influences all subsequent judgments.
- **Application:** Show highest-priced option first
- **Why it works:** Makes other options seem more reasonable

**3. Price = Quality Signal**
Higher prices imply better quality.
- **Application:** Don't underprice premium offerings
- **Why it works:** Customers use price as shortcut for value

**4. Razor/Razor Blades**
Low upfront cost, revenue from consumables/services.
- **Application:** Subsidize hardware, monetize software/services
- **Why it works:** Reduces adoption friction, locks in revenue

**5. Pennies-a-Day**
Break prices into smallest time unit.
- **Application:** "$3/day" instead of "$90/month"
- **Why it works:** Makes large numbers feel manageable

**6. Psychological Thresholds**
Prices just below round numbers convert better.
- **Application:** $99 vs $100, $999 vs $1,000
- **Why it works:** Perception stays in lower digit range

---

### Phase 7: Maintain Price Integrity

> "When your product launches and the market is less than enthusiastic, you'll feel pressure to cut the price. That's almost always a bad idea."

#### Why Price Cuts Hurt

- **Signals diminished value** - "It must not be worth what they said"
- **Erodes profits** - Margin compression, growth impact
- **Reduces lifetime value** - Customers expect future discounts
- **Creates precedent** - Sales team learns discounting works

#### The 3-Before-1 Rule

Before approving ANY price cut, require your team to propose 3 non-pricing solutions:

1. Better value communication
2. Improved targeting
3. Enhanced support/onboarding
4. Feature adjustments
5. Channel optimization

#### Post-Launch Discipline

- **Be patient** - Early results often improve with time
- **Track more than revenue** - Win/loss reasons, deal velocity, customer feedback
- **Deconstruct deals** - Understand why you won/lost
- **War-game competition** - Anticipate reactions before cutting price

---

## Examples

### Example 1: B2B SaaS Analytics Platform

**Situation:** Early-stage analytics tool, competitors range from free to enterprise

**Willingness-to-Pay Research Findings:**
- Segment A (Startups): WTP $29-79/month, need simplicity
- Segment B (Growth Companies): WTP $199-399/month, need integrations
- Segment C (Enterprise): WTP $999+/month, need security & support

**Feature Analysis:**
| Feature | Leaders | Fillers | Killers |
|---------|---------|---------|---------|
| Real-time dashboards | ✓ | | |
| Custom reports | ✓ | | |
| Slack integration | | ✓ | |
| 50+ data connectors | | ✓ | |
| AI predictions | | | ✓ (too early) |
| White-labeling | | | ✓ (only 10% need) |

**Tier Structure:**

```
STARTER ($49/mo)        GROWTH ($199/mo)         SCALE ($499/mo)
━━━━━━━━━━━━━━━━        ━━━━━━━━━━━━━━━━         ━━━━━━━━━━━━━━━
3 dashboards            Unlimited dashboards     Unlimited + custom
5 data sources          20 data sources          Unlimited sources
Email support           Chat support             Dedicated CSM
                        Slack integration        SSO + audit logs
```

**Monetization Model:** Subscription with usage-based overage for data volume

**Behavioral Tactics Applied:**
- Compromise effect: Growth tier is most profitable, positioned as "Most Popular"
- Anchoring: Scale tier shown first on pricing page
- Threshold pricing: $49, $199, $499 (not $50, $200, $500)

---

### Example 2: Professional Services (Consulting)

**Situation:** Strategy consulting firm, hourly billing, price pressure from clients

**Willingness-to-Pay Research Findings:**
- Clients value outcomes, not hours
- High WTP for "guaranteed results" or risk-sharing
- Resistance to open-ended hourly engagements

**Monetization Model Shift:** From hourly to value-based

**New Pricing Structure:**

```
DIAGNOSTIC ($15K)       IMPLEMENTATION ($75K)      PARTNERSHIP ($25K/mo)
━━━━━━━━━━━━━━━━━       ━━━━━━━━━━━━━━━━━━━        ━━━━━━━━━━━━━━━━━━━
2-week assessment       12-week execution          Ongoing advisory
Defined deliverables    Milestone-based            Monthly retainer
Fixed scope             Performance bonus          Unlimited access
No risk to client       Shared upside              Predictable cost
```

**Key Changes:**
- Removed hourly rates entirely
- Introduced performance bonus tied to outcomes
- Created subscription-like retainer option
- Packaged discovery as separate paid product

**Result:** 40% increase in average engagement value, improved client satisfaction

---

## Checklists & Templates

### Willingness-to-Pay Interview Guide

```
INTRODUCTION (2 min)
"We're exploring a new [product/service] and want to understand
what would be valuable to you. This is about understanding value,
not selling you anything."

CURRENT SITUATION (5 min)
- How do you currently solve [problem]?
- What do you spend on this today (time/money)?
- What's frustrating about current solutions?

VALUE EXPLORATION (10 min)
- What would an ideal solution do for you?
- Which of these features [show list] matter most?
- Why is [top feature] important to you?

PRICING QUESTIONS (10 min)
- "What would be an acceptable price for this?"
- "What would be an expensive price?"
- "What would be prohibitively expensive?"
- "At $X, would you definitely buy, probably buy,
   probably not buy, or definitely not buy?"
- "Why did you choose that answer?"

WRAP-UP (3 min)
- What would make this a no-brainer purchase?
- Anything else we should know?
```

### Pricing Tier Design Template

```
TIER NAME: _______________
TARGET SEGMENT: _______________
PRICE POINT: $___/[period]

LEADERS (must-have features):
1. _______________
2. _______________
3. _______________

FILLERS (nice-to-have):
1. _______________
2. _______________

EXCLUDED (saved for higher tiers):
1. _______________
2. _______________

POSITIONING STATEMENT:
"For [segment] who need [primary job], [Tier] provides [key benefit]
at [price], unlike [alternative] which [limitation]."
```

### Monetization Model Decision Matrix

| Factor | Subscription | Usage | Freemium | One-Time |
|--------|-------------|-------|----------|----------|
| Customer prefers predictability | ✓✓✓ | ✓ | ✓✓ | ✓ |
| Value varies by usage | ✓ | ✓✓✓ | ✓✓ | ✓ |
| Need volume for network effects | ✓ | ✓ | ✓✓✓ | ✓ |
| High CAC, need long payback | ✓✓✓ | ✓✓ | ✓ | ✓ |
| Easy to measure usage | ✓ | ✓✓✓ | ✓✓ | ✓ |

(✓✓✓ = strong fit, ✓ = weak fit)

### Price Integrity Checklist

Before approving any price reduction:
- [ ] Have we clearly communicated value?
- [ ] Have we targeted the right segment?
- [ ] Have we addressed specific objections?
- [ ] Have we tried alternative packaging?
- [ ] Have we war-gamed competitive response?
- [ ] Have 3 non-pricing alternatives been proposed?
- [ ] What precedent does this set?

---

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

**Primary Source:**
- Ramanujam, Madhavan & Tacke, Georg. (2016). *Monetizing Innovation: How Smart Companies Design the Product Around the Price*. Wiley.

**Additional Resources:**
- Lenny's Newsletter: "The Art and Science of Pricing" podcast episode
- Simon-Kucher & Partners pricing research
- Strategyzer webinars on pricing

---

## Related Skills

- **value-proposition-canvas** - Understand customer pains/gains that drive WTP
- **grand-slam-offers** - Alex Hormozi's approach to offer construction
- **positioning-dunford** - How positioning affects price perception
- **jobs-to-be-done** - Understanding what job customers hire your product for
- **competitive-analysis** - Mapping competitive pricing landscape
