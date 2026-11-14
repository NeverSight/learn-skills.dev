---
name: pricing-plan
description: When the user wants to design, evaluate, or optimize their pricing strategy. Also use when the user mentions "pricing", "pricing page", "pricing tiers", "monetization", "how to price", "pricing model", "freemium vs paid", or "price increase."
version: 1.0.0
---

# Pricing Strategy Planner

Design or optimize a pricing strategy across the three core axes: packaging, pricing metric, and price point.

## Before You Start

**Check for product marketing context first:**
If `.claude/product-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered.

## Phase 1: Information Gathering

Collect pricing context by asking the user focused questions in batches of 2-3.

### Required Context

1. **What are you pricing?** Ask: "What product or service are you pricing? Describe it briefly — what does it do and who is it for?"

2. **Pricing maturity** — Use `AskUserQuestion` with options:
   - Haven't set pricing yet (new product)
   - Have pricing but it's not working
   - Want to add tiers or change packaging
   - Considering a price increase
   - Exploring a new pricing model entirely

3. **Business model** — Use `AskUserQuestion` with options:
   - SaaS subscription (monthly/annual)
   - Usage-based / pay-as-you-go
   - One-time purchase
   - Freemium with paid upgrade
   - Marketplace / transaction fee
   - Service / consulting

4. **Target customer** — Ask: "Who is your primary buyer? (e.g., individual consumer, small business owner, enterprise team lead, developer) What's their budget sensitivity?"

5. **Current pricing** — Ask: "What do you currently charge (if anything)? What tiers exist? What's included in each?"

6. **Competitive landscape** — Ask: "Who are your top 2-3 competitors and roughly what do they charge? How are you positioned against them — cheaper, similar, premium?"

7. **Key metrics** — Ask: "What's your current conversion rate from free/trial to paid? Monthly churn rate? Average revenue per user? (Share what you know, skip what you don't)"

8. **Value metric** — Use `AskUserQuestion` with options:
   - Per user / per seat
   - Per usage (API calls, storage, sends, etc.)
   - Per feature tier
   - Flat fee
   - Not sure — need help figuring this out

9. **Pricing goals** — Use `AskUserQuestion` with multiSelect:
   - Increase revenue per customer
   - Improve free-to-paid conversion
   - Reduce churn
   - Move upmarket (sell to bigger customers)
   - Simplify confusing pricing
   - Launch new pricing from scratch

## Phase 2: Strategy Design

Based on gathered context, design the pricing strategy across three axes:

### Axis 1: Packaging (What's in each tier)
- **Good-Better-Best** model with clear differentiation
- Each tier should have a clear "who it's for"
- Feature gating should follow natural usage patterns
- The upgrade trigger should be organic, not punitive

### Axis 2: Pricing Metric (What you charge for)
- Must align with how customers perceive value
- Common metrics: per seat, per usage unit, per feature tier, flat fee
- The best metric scales with the value customers receive

### Axis 3: Price Point (How much)
- Floor = next best alternative (what they'd pay otherwise)
- Ceiling = perceived value of your solution
- Use Van Westendorp or competitive benchmarking to find the sweet spot

### Pricing Psychology Tactics
- **Anchoring** — show higher-priced plan first
- **Decoy effect** — make the target plan the obvious best value
- **Charm pricing** — $99 vs $100 for value positioning
- **Round pricing** — $100 for premium positioning
- **Rule of 100** — under $100 use %, over $100 use $ for discounts

### Signals You Should Raise Prices
- Conversion rate above 40%
- Monthly churn below 3%
- No price resistance from prospects
- Significant product improvements since last pricing change

## Phase 3: Deliverables

Generate and save:

1. **`pricing-strategy.md`** — Complete pricing strategy with tier breakdown, recommended price points, packaging logic, and migration plan if changing existing pricing

Present a summary and suggest next steps (e.g., "Use /split-test to A/B test pricing changes" or "Use /conversion-audit to optimize your pricing page").

## Guidelines

- Pricing is never "done" — recommend a review cadence (quarterly or after major product changes)
- Always consider the migration path for existing customers when suggesting changes
- Be specific with recommendations, not vague — suggest actual dollar amounts and tier names
- If data is limited, recommend lightweight research methods (customer interviews, Van Westendorp survey)

## User Request

$ARGUMENTS
