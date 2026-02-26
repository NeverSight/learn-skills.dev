---
name: indie-dev-skill
description: Design onboarding and subscription paywalls for mobile apps with pricing, trial, and copy guidance for conversion-focused growth decisions.
---

# Indie Dev Skills

## Quick Start
When invoked, return output in this exact section order:
1. Assumptions
2. Recommended Onboarding Flow
3. Paywall Structure
4. Pricing And Trial Setup
5. Copy Variants
6. Risks And Tradeoffs
7. Next 7 Days Plan

Example output skeleton:
```markdown
## Assumptions
- Region: US
- Category: Mobile app

## Recommended Onboarding Flow
- Screen 1: Problem framing
- Screen 2: Personalization
- Screen 3: Value reveal

## Paywall Structure
- Value -> proof -> trial -> pricing

## Pricing And Trial Setup
- Default: annual plan with trial
- Second option: weekly plan
- Optional third option: monthly plan

## Copy Variants
- Headline A, Headline B

## Risks And Tradeoffs
- Potential annual friction in price-sensitive users

## Next 7 Days Plan
- Day 1-2: Ship onboarding + paywall
- Day 3-4: Refine copy and visuals
- Day 5-7: Iterate based on qualitative feedback
```

## Overview
Use this skill to build onboarding and paywall flows that improve conversion rate for indie apps with limited historical data. It combines onboarding guidance with paywall and pricing strategy, with the paywall shown at the end of onboarding after meaningful user interaction.

## Scope And Assumptions
- Primary scope: mobile apps with subscription-led growth
- Primary user: solo developers and small indie teams with limited time and analytics depth
- If region is missing, assume US and label that assumption explicitly
- If platform is missing, provide platform-agnostic guidance
- Treat all numeric benchmarks as optional context; avoid numeric targets when no prior data exists
- Utility-app benchmark references are directional; adapt recommendations by category

## Indie Execution Mode
When the user has limited data or engineering bandwidth:
- Prioritize the smallest shippable onboarding + paywall flow over complex optimization plans
- Focus on a single primary conversion rate (paywall view -> trial or purchase)
- Include a 1-week shipping plan with concrete steps

## Onboarding Placement Rule
- Require at least one meaningful user interaction before the paywall (input, selection, quiz, scan, or setup step)
- Show the paywall at the end of onboarding, not before the user interacts
- Ensure onboarding demonstrates user-specific value before pricing exposure

## Onboarding UX Rules
- Prefer no dedicated onboarding when the core flow is already obvious
- Use dedicated onboarding only when user data, personalization, or novel workflow explanation is required
- Keep onboarding short (typically 3-5 screens) with one concept per step
- Keep onboarding skippable with visible `Skip` and a clear progress indicator
- Avoid feature-promo carousels at first launch unless the feature is truly unfamiliar
- Prefer contextual help and in-flow guidance over long tutorial slides
- Defer visual theme customization until after users understand core app value
## Paywall Interaction Rules
- Use a close button only in the top-left corner

## Input Checklist
Capture these inputs before recommendations:
- Region and currency
- App category and target user
- Current plans and price points
- Trial setup (length, plan attachment, timing)
- Funnel metrics only if available (use them to pick a single primary conversion rate)
- Constraints (brand, legal copy requirements, launch timing)

If inputs are missing, default to:
- Region: US
- Currency: USD
- Category: Mobile app
- Trial: 7-14 days attached to annual
- Team context: indie/solo, low analytics maturity

## Disallowed Outputs
Never include:
- Legal, tax, or compliance advice
- Backend billing architecture or server implementation plans
- SDK-specific setup instructions or tool walkthroughs
- App architecture mandates (MVVM/MVC or project-structure prescriptions)
- Guaranteed outcome claims from benchmark data

## Workflow Decision Tree

### 1) Clarify context
- App category, user problem, target regions
- Current pricing, trial setup, and metrics (if available)
- If data is missing, state assumptions before making recommendations

### 2) Build onboarding flow
- Identify user problem
- Personalize quickly (scan, quiz, or setup)
- Demonstrate value before pricing
- Include at least one interaction step before presenting the paywall
- Keep each step focused on one job and ensure skip/progress affordances are visible

### 3) Design paywall
- Multi-screen value -> proof -> trial -> pricing
- Annual plan highlighted and preselected
- Equivalent monthly cost shown for annual

### 4) Validate against defaults
- Trial attached to annual plan, 7–14 days
- “Cancel anytime” visible
- Paywall appears at the end of onboarding after interaction

### 5) Plan a simple iteration loop
- Ship, observe qualitative feedback, and iterate on copy and layout

## Decision Policy (Conflict Arbitration)
- Start with Annual Default when:
- No strong evidence of high price sensitivity
- Category supports longer commitment (productivity, health, education, pro utility)
- Use Weekly Entry then Upsell when:
- Early data shows annual trial-start friction
- Audience is high-churn, low-commitment, or highly price-sensitive
- Resolution rule:
- If guidance conflicts, prioritize current product metrics over static defaults
- If metrics are unavailable, provide both variants and mark one as primary with rationale

## Starter Defaults (US Mobile Apps, unless user overrides)
- Currency scope: USD only; localize prices before applying outside US
- Primary default: Annual $29.99 with 7-14 day trial ("Best Value", default selected, "Cancel anytime" visible)
- Second option: Weekly $4.99
- Do not include a monthly plan as the default or primary option
- Recommended first test variant: weekly-first entry with annual upsell

## Conflict Matrix
- `Annual + trial default`: best for conversion when users value longer commitment and trust the product
- `Weekly second option`: best for conversion when price sensitivity or commitment friction is high
- `Tie-breaker`: pick the option most likely to improve paywall conversion rate based on user context

## Deliverables
Provide all or subset as requested:
- Onboarding screen sequence with goals
- Interaction checkpoint before paywall
- Paywall flow outline (screen-by-screen)
- UI design tips for onboarding and paywall layout
- Pricing table and selection hierarchy
- Copy blocks (headline, subhead, benefits, CTA, disclaimers)
- Loss-aversion messaging variants
- Lightweight implementation plan (what to ship this week)

## Minimum Event List (Optional)
If the user asks for instrumentation, keep it minimal:
- `onboarding_started`
- `onboarding_completed`
- `paywall_viewed`
- `trial_started`
- `subscription_purchased`
- `trial_canceled`

## Required Response Template
Return outputs using these sections in order:
1. Assumptions
2. Recommended Onboarding Flow
3. Paywall Structure
4. Pricing And Trial Setup
5. Copy Variants
6. Risks And Tradeoffs
7. Next 7 Days Plan

## References
- `references/onboarding-playbook.md` - Onboarding rules, benchmarks, and tests
- `references/paywall-playbook.md` - Pricing rules, trial strategy, benchmarks, and tests
- `references/subscription-apps-highlights.md` - Report highlights on trial timing, conversion, and paywall placement
- `references/mobile-onboarding-usability-guidance.md` - Usability-first guidance on when onboarding is justified and how to keep it minimal
- `references/mobile-onboarding-paywall-design-tips.md` - Practical mobile UI design tips for onboarding and paywall presentation
- `references/in-app-subscriptions-highlights.md` - Pricing mix, regional trends, and paywall tactics
- `references/metric-definitions.md` - Funnel metric definitions and calculation boundaries

## Philosophy
- The decision to subscribe happens before the paywall
- Optimize for Day-0 trial starts and annual adoption
- Prefer clarity and value-first messaging over gimmicks
