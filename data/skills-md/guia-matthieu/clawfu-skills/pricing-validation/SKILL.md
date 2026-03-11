---
name: pricing-validation
description: "Test willingness to pay before launching with proven pricing research methodologies. Combine Van Westendorp, Gabor-Granger, and behavioral techniques to find your optimal price point. Use when: **After solution validation** to test willingness to pay; **Before launch** to set initial pricing; **Pricing changes** to test new price points; **New segments** to understand price sensitivity by segment; **Competitive positioning** to price against alternatives"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Pricing Validation

> Test willingness to pay before launching with proven pricing research methodologies. Combine Van Westendorp, Gabor-Granger, and behavioral techniques to find your optimal price point.

## When to Use This Skill

- **After solution validation** to test willingness to pay
- **Before launch** to set initial pricing
- **Pricing changes** to test new price points
- **New segments** to understand price sensitivity by segment
- **Competitive positioning** to price against alternatives
- **Feature pricing** to understand value of add-ons

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | Van Westendorp PSM (1976), Gabor-Granger method, behavioral economics |
| **Core Principle** | "People can't accurately predict what they'd pay. Use structured methods to triangulate, and verify with real purchasing behavior." |
| **Why This Matters** | Pricing wrong costs you customers (too high) or money (too low). Every 1% improvement in price has 11% profit impact on average. |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Strategic priorities |
| Synthesizes market data | Competitive positioning |
| Identifies opportunities | Resource allocation |
| Creates strategic options | Final strategy selection |
| Suggests implementation approaches | Execution decisions |

## What This Skill Does

1. **Finds price range** - Identifies acceptable pricing boundaries
2. **Tests price points** - Measures demand at specific prices
3. **Identifies optimal price** - Balances revenue and conversion
4. **Segments by willingness** - Who will pay more vs. less
5. **Validates pricing model** - Subscription vs. one-time vs. usage
6. **Reveals value perceptions** - What drives pricing acceptance

## How to Use

### Run Van Westendorp Analysis
```
I want to find the optimal price range for [product].
Run me through Van Westendorp Price Sensitivity Meter.
Provide the questions and analysis framework.
```

### Test Specific Price Points
```
I'm considering pricing at [$X, $Y, $Z].
Help me design a Gabor-Granger test to measure demand at each price.
```

### Validate Pricing Without Asking Directly
```
I want to validate my $99/month pricing without asking "would you pay?"
What behavioral and indirect methods can I use?
```

## Instructions

### Step 1: Choose Your Pricing Research Method

```
## Pricing Research Methods

### Method Selection Guide

| Method | Best For | Sample Size | Complexity |
|--------|----------|-------------|------------|
| Van Westendorp PSM | Finding price range | 100-200+ | Medium |
| Gabor-Granger | Testing specific prices | 50-100 | Low |
| Conjoint Analysis | Feature/price trade-offs | 200+ | High |
| A/B Testing | Final validation | 500+ visitors | Medium |
| Behavioral Signals | Qualitative insights | 10-30 | Low |

### When to Use Each

**Van Westendorp (Price Sensitivity Meter):**
- You don't know where to start
- Want to find acceptable price range
- Have access to survey respondents

**Gabor-Granger:**
- You have candidate price points
- Want to test specific prices
- Need demand curve

**Conjoint Analysis:**
- Multiple features and price levels
- Need to understand trade-offs
- Have resources for complex analysis

**A/B Testing:**
- Already have traffic/users
- Testing final price decisions
- Want real conversion data

**Behavioral Signals:**
- Early stage, small sample
- Qualitative validation
- Can't run formal surveys
```

---

### Step 2: Van Westendorp Price Sensitivity Meter

```
## Van Westendorp PSM

### The Four Questions

Ask respondents all four questions about the product:

1. **TOO EXPENSIVE:**
   "At what price would you consider this product to be so expensive
   that you would not consider buying it?"

2. **TOO CHEAP:**
   "At what price would you consider this product to be priced so low
   that you would question its quality?"

3. **EXPENSIVE BUT WORTH IT:**
   "At what price would you consider this product starting to get expensive—
   it's not out of the question, but you'd have to think about buying it?"

4. **GOOD VALUE:**
   "At what price would you consider this product to be a bargain—
   a great buy for the money?"

### Analysis

Plot cumulative distribution curves for each response:
- "Too Expensive" (cumulative from low to high)
- "Too Cheap" (cumulative from high to low)
- "Expensive" (cumulative from low to high)
- "Good Value" (cumulative from high to low)

### Key Price Points

| Point | Definition | Meaning |
|-------|------------|---------|
| **PMC** (Point of Marginal Cheapness) | Where "Too Cheap" intersects "Expensive" | Below this, quality concerns emerge |
| **PME** (Point of Marginal Expensiveness) | Where "Too Expensive" intersects "Good Value" | Above this, significant resistance |
| **OPP** (Optimal Price Point) | Where "Too Expensive" intersects "Too Cheap" | Best price for adoption |
| **IDP** (Indifference Price Point) | Where "Expensive" intersects "Good Value" | What people expect to pay |

### Acceptable Price Range
PMC to PME = your acceptable pricing range

### Interpretation Guide

**Narrow range (PMC close to PME):**
- Price sensitive market
- Commodity perceptions
- Strong competitor reference prices

**Wide range (PMC far from PME):**
- Price flexibility
- Differentiated product
- Segmentation opportunity
```

---

### Step 3: Gabor-Granger Method

```
## Gabor-Granger Price Testing

### How It Works

Show product, then ask purchase intent at specific price points.
Start high or low, adjust based on response.

### Question Format

**Monadic (one price per person):**
Show each respondent only ONE price:
"Would you buy this product at $X?"
- Definitely would buy
- Probably would buy
- Might or might not buy
- Probably would not buy
- Definitely would not buy

**Sequential (multiple prices per person):**
If "Yes" → show higher price
If "No" → show lower price
Continue until you find their threshold

### Analysis

**Purchase Intent Translation:**
| Response | Probability |
|----------|-------------|
| Definitely | 90% |
| Probably | 70% |
| Might | 30% |
| Probably not | 10% |
| Definitely not | 0% |

**Demand Curve:**
| Price | Purchase Intent | Weighted % | Expected Revenue |
|-------|-----------------|------------|------------------|
| $49 | 80% | 68% | $49 × 68% = $33.32 |
| $79 | 60% | 48% | $79 × 48% = $37.92 |
| $99 | 40% | 32% | $99 × 32% = $31.68 |
| $149 | 20% | 14% | $149 × 14% = $20.86 |

**Optimal Price:** $79 (highest expected revenue)

### Sample Size Requirements

- 30-50 per price point (monadic)
- 50-100 total (sequential)
- Segment analysis requires more
```

---

### Step 4: Behavioral/Indirect Methods

```
## Pricing Validation Without Asking About Price

### Why Indirect Methods Matter
- People overestimate willingness to pay when hypothetical
- Real behavior differs from stated intent
- Indirect signals often more reliable

### Method 1: Reference Price Anchoring

**Questions to ask:**
- "What are you currently spending on [similar product/solution]?"
- "What's the most you've ever paid for [category]?"
- "What would you expect this to cost based on similar products?"

**Analysis:**
If they're spending $100/month on alternatives, $150 might be possible.
If they've never paid >$50 for similar, $200 is risky.

### Method 2: Value Quantification

**Questions to ask:**
- "How much time does this problem cost you per week?"
- "What's the cost of this problem not being solved?"
- "If this saved you X hours/week, what's that worth?"

**Analysis:**
If problem costs them $500/month in time, $100/month solution seems cheap.
Price relative to quantified value, not arbitrary numbers.

### Method 3: Trade-off Questions

**Instead of:** "Would you pay $X?"
**Ask:** "Which would you choose?"
- Option A: $79/month with features X, Y, Z
- Option B: $49/month with features X, Y only
- Option C: Free with feature X only

**Analysis:**
Distribution reveals price sensitivity and feature value.

### Method 4: Commitment Testing

**Real commitment signals:**
- "Would you put $50 down as a deposit for early access?"
- "Would you sign a letter of intent at $X?"
- "Would you pay for a paid pilot at $X/month?"

**Analysis:**
Real money > stated intent.
Even small commitment = strong signal.

### Method 5: Negotiation Simulation

**Questions to ask:**
- "If this was $X, would you push back? At what price would you push back?"
- "What price would make this an easy decision?"
- "What price would require significant justification internally?"

**Analysis:**
- "Easy decision" price = conservative but low-friction
- "Push back" price = ceiling
```

---

### Step 5: Analyze and Decide

```
## Pricing Analysis Framework

### Data Synthesis

| Method | Finding | Confidence |
|--------|---------|------------|
| Van Westendorp | Range: $X - $Y, OPP: $Z | High/Med/Low |
| Gabor-Granger | Optimal: $X | High/Med/Low |
| Reference prices | Currently paying $X | High/Med/Low |
| Value quantification | Problem worth $X/month | High/Med/Low |
| Commitments | X people committed at $Y | High/Med/Low |

### Triangulation

**Look for convergence:**
- If Van Westendorp OPP = $89
- And Gabor-Granger optimal = $79
- And reference prices = $50-100
→ Price in $79-99 range is validated

**Red flags:**
- Wide divergence between methods
- Reference prices far below target
- No commitments at target price

### Price Setting Decision

| Factor | Weight | Your Finding | Score |
|--------|--------|--------------|-------|
| Research-based optimal | 30% | | |
| Competitive positioning | 25% | | |
| Value quantification | 25% | | |
| Commitment signals | 20% | | |

### Pricing Model Validation

Also validate the MODEL, not just the price:
- Subscription vs. one-time
- Per user vs. flat rate
- Monthly vs. annual
- Usage-based vs. fixed

**Questions to test model:**
- "How do you typically pay for software like this?"
- "Would you prefer monthly or annual billing?"
- "Does per-user pricing make sense for your team?"

### Risk Assessment

| Price Point | Upside | Downside | Risk Level |
|-------------|--------|----------|------------|
| $79 (low) | Faster adoption | Leave money on table | Low |
| $99 (mid) | Balanced | May need to discount | Medium |
| $129 (high) | Max revenue | Slower adoption | High |

**Recommendation format:**
"Launch at $[X] based on [evidence]. Plan to test $[Y] with segment [Z] within 90 days."
```

---

## Examples

### Example 1: SaaS Pricing Validation

**Input:**
> "I'm launching a project management tool for marketing teams. I'm thinking $49/user/month. How do I validate this?"

**Output:**

## Pricing Validation Plan: Marketing PM Tool

### Multi-Method Approach

**Step 1: Reference Price Research**

In customer interviews, ask:
- "What are you paying for project management today?"
- "What's your total spend on marketing tools?"
- "What's the most expensive per-seat tool you use?"

**Common findings in this space:**
- Asana: $10-30/user
- Monday: $8-24/user
- Notion: $10-15/user

**Initial insight:** $49/user is 2-3x competitors. Need strong differentiation story.

**Step 2: Van Westendorp Survey**

Survey 100+ target customers:

"Imagine a project management tool designed specifically for marketing teams with campaign calendars, creative workflows, and ROI tracking."

1. At what price per user/month would you consider this too expensive?
2. At what price per user/month would you question the quality?
3. At what price per user/month does this become expensive but still worth considering?
4. At what price per user/month would this be a great value?

**Step 3: Value Quantification**

In interviews, calculate value:
- "How much time does your team spend on PM overhead?" → 5 hrs/week
- Team of 5 × 5 hrs × $50/hr × 4 weeks = $5,000/month
- If you save 50% = $2,500/month value
- $49 × 5 users = $245/month = 10% of value saved

**Value ratio:** 10:1 → Price has room to increase

**Step 4: Commitment Test**

"We're launching soon. For $199 annual prepay (40% off), you'd get lifetime early-adopter pricing and input on the roadmap. Would you be interested?"

Track:
- How many say yes?
- What objections come up?

### Hypothetical Results

| Method | Finding |
|--------|---------|
| Reference prices | Competitors: $10-30/user. Yours needs differentiation story. |
| Van Westendorp | Range: $29-79. OPP: $49. IDP: $39. |
| Value quantification | 10:1 value ratio at $49. Room for higher. |
| Commitment test | 4 of 10 prepaid at $199 ($50/user equiv) |

### Recommendation

**Launch at $39/user/month** (annual: $29/user)

**Rationale:**
- At competitive upper range ($30 most expensive competitor)
- Inside Van Westendorp comfortable range
- Can test $49 with marketing-specific segments later
- Early customers locked in while you build brand

**Pricing tiers:**
- Starter: $39/user/month (1-10 users)
- Team: $29/user/month (11-50 users)
- Enterprise: Custom

**Test plan:**
- Launch at $39
- A/B test $49 with "marketing agency" segment in Month 2
- Grandfather early customers at launch price

---

### Example 2: Consumer Product Pricing

**Input:**
> "I'm launching a $150/week meal prep delivery service. Is this validated? My interviews showed people spend $100/week on groceries."

**Output:**

## Pricing Analysis: Meal Prep Service at $150/week

### Reference Price Problem

**Current spending:** $100/week on groceries
**Your price:** $150/week

**Gap:** 50% increase from their reference price

**This is a significant psychological hurdle.** You're not competing with meal prep—you're competing with groceries.

### Value Reframe Required

**Wrong frame:** "$150/week for food"
**Right frame:** "$150/week for healthy eating + 5 hours of your time back"

**Value calculation:**
- Time saved: 5 hours/week × $30/hour = $150/week value
- Healthier eating: Lower healthcare costs, energy, etc.
- Total value: >$200/week

**Price vs. Value:** $150 for $200+ value = fair

### Validation Approach

**Question 1: Reference pricing**
"How much do you spend on food per week, including groceries and takeout?"
→ Most spend $150-250 when you include dining out

**Question 2: Time value**
"How much is an hour of your time worth?"
"Would you pay $30 to get an hour back?"
→ If yes, you have room at $150

**Question 3: Commitment test**
"We're doing a 2-week trial at $125/week (no commitment after). Would you try it?"
→ Conversion rate = validation signal

### Gabor-Granger Test Design

Test three prices:
- $99/week (loss leader to test demand curve)
- $125/week (compromise)
- $150/week (target)

Survey 30+ in each condition.

**Expected finding hypothesis:**
| Price | Intent | Weighted Demand |
|-------|--------|-----------------|
| $99 | 60% | 48% |
| $125 | 45% | 34% |
| $150 | 30% | 22% |

**Revenue optimization:**
- $99 × 48% = $47.52/person expected
- $125 × 34% = $42.50/person expected
- $150 × 22% = $33.00/person expected

If this pattern holds → **Price at $99-125**, not $150.

### Alternative Validation Signals

**Strong validation for $150:**
- They're already spending $150+ on food + takeout combined
- They've paid for similar services (HelloFresh, etc.) at $100+
- They'd prepay for a trial
- High earners with time scarcity

**Weak validation:**
- Most spend <$100 on groceries
- Never paid for meal services
- "Seems expensive"
- No urgency around time savings

### Recommendation

**Start at $125/week with trial offer**

- Lower barrier to entry
- Build habit and reviews
- Raise to $150 after establishing value
- Premium tier at $175 for dietary customization

---

### Example 3: B2B Pricing with Decision Maker Validation

**Input:**
> "I'm selling to enterprises at $50K/year. How do I validate pricing when the buyer isn't the user?"

**Output:**

## Enterprise Pricing Validation

### The Challenge
- Users see value but don't control budget
- Buyers control budget but don't use the product
- $50K requires procurement/approval

### Multi-Stakeholder Validation

**Step 1: User Value Validation**
With end users, validate:
- Problem severity (8+/10)
- Solution fit (would use it)
- Value articulation (can describe ROI)

They become internal champions who sell to buyers.

**Step 2: Buyer Price Validation**

With budget holders, ask:
- "What's your budget for tools like this?"
- "What's the most you've spent on similar software?"
- "How does $50K compare to what you expected?"
- "What would it take to justify $50K internally?"

**Step 3: Procurement Reality Check**

- "At $50K, who needs to approve?"
- "What's the procurement process?"
- "What contract terms are standard?"
- "What would make this easier to approve?"

### Price Anchoring for Enterprise

**Anchor to cost, not features:**

"Your team spends 20 hours/week on this process. At $100/hour loaded cost, that's $100K/year. This tool cuts that by 50%, saving $50K and freeing your team for higher-value work. The investment is $50K/year."

**ROI story:** 100% ROI in year 1.

### Commitment Ladder

| Commitment Level | What You Ask | Validation Strength |
|------------------|--------------|---------------------|
| Interest | "Can we demo to your team?" | Weak |
| Champion | "Would you advocate internally?" | Medium |
| Pilot | "Would you run a paid pilot?" | Strong |
| LOI | "Would you sign letter of intent?" | Strong |
| Prepay | "Would you prepay Q1?" | Very Strong |

### Validation Signals for $50K

**Validated if:**
- 3+ LOIs or paid pilots at $50K
- Buyers say it's "within budget" or "expected"
- Clear ROI story they can articulate internally
- Procurement timeline is reasonable (not "next fiscal year")

**Not validated if:**
- "That's much more than we expected"
- "That would need board approval"
- "We've never spent that on a tool like this"
- No one will sign LOI

### Price Testing Approach

**Don't ask:** "Would you pay $50K?"
**Instead:** "Based on the value we discussed, we're thinking $50K/year. What's your reaction?"

**Listen for:**
- "That seems reasonable" → validated
- "Hmm, that's more than I expected" → probe what they expected
- "We'd need to see strong ROI" → they need the business case
- "That's out of our budget" → test lower or different segment

---

## Checklists & Templates

### Pricing Validation Plan Template

```
## Pricing Validation Plan

**Product:** _______________
**Target price:** _______________
**Launch date:** _______________

### Methods to Use
- [ ] Van Westendorp PSM (n=100+)
- [ ] Gabor-Granger (n=50+)
- [ ] Reference price research
- [ ] Value quantification
- [ ] Commitment testing
- [ ] A/B testing (if traffic available)

### Timeline
- Week 1-2: Customer interviews (reference prices, value)
- Week 3-4: Survey (Van Westendorp/Gabor-Granger)
- Week 5: Analysis and decision
- Week 6: Commitment testing

### Decision Criteria
Price validated if:
- Within Van Westendorp acceptable range
- Gabor-Granger shows >30% intent
- Reference prices support
- 3+ commitments obtained
```

---

### Van Westendorp Survey Template

```
## Van Westendorp Price Sensitivity Survey

**Product Description:**
[Clear description of product and value proposition]

**Screening:**
1. Are you a [target customer]? Y/N
2. Do you currently experience [problem]? Y/N

**Price Questions:**

Q1: At what price would you consider [product] to be so expensive
that you would NOT consider buying it?
$_______________

Q2: At what price would you consider [product] to be priced so low
that you would question its quality?
$_______________

Q3: At what price would you consider [product] starting to get expensive—
it's not out of the question, but you'd have to think about buying it?
$_______________

Q4: At what price would you consider [product] to be a bargain—
a great buy for the money?
$_______________

**Additional Context:**
Q5: What do you currently pay for [similar/alternative]?
$_______________

Q6: What would you expect a product like this to cost?
$_______________
```

---

## Skill Boundaries

### What This Skill Does Well
- Structuring strategic analysis
- Identifying market opportunities
- Creating strategic frameworks
- Synthesizing competitive data

### What This Skill Cannot Do
- Replace market research
- Guarantee strategic success
- Know proprietary competitor info
- Make executive decisions

## References

- Van Westendorp, P. "NSS Price Sensitivity Meter" (1976)
- Gabor, A. & Granger, C. "Price as an Indicator of Quality" (1966)
- Simon, H. & Fassnacht, M. "Price Management" (2019)
- Ramanujam, M. & Tacke, G. "Monetizing Innovation" (2016)
- Poundstone, W. "Priceless: The Myth of Fair Value" (2010)

## Related Skills

- [solution-interview](../solution-interview/) - Validate solution before pricing
- [customer-discovery](../customer-discovery/) - Overall validation framework
- [pricing-strategy](../../strategy/pricing-strategy/) - Strategic pricing decisions
- [grand-slam-offers](../../strategy/grand-slam-offers/) - Offer structure beyond price
- [objection-mapping](../objection-mapping/) - Handle price objections

---

## Skill Metadata


- **Mode**: centaur
```yaml
name: pricing-validation
category: validation
subcategory: pricing-research
version: 1.0
author: MKTG Skills
source_expert: Van Westendorp, Gabor-Granger
source_work: Price Sensitivity Meter, Price Management
difficulty: intermediate
estimated_value: $5,000 pricing research project
tags: [pricing, validation, research, Van-Westendorp, willingness-to-pay, YC]
created: 2026-01-25
updated: 2026-01-25
```
