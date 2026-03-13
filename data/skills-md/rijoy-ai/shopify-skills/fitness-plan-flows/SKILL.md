---
name: fitness-plan-flows
description: Design "training plan"-centric marketing flows for stores selling fitness accessories (resistance bands, elastic bands, yoga rings, foam rollers, massage balls, etc.)—post-purchase plan delivery, advancement plans for repurchase, challenges/plans for acquisition, and member-exclusive content. Trigger when users mention fitness accessories, resistance bands, elastic bands, training-plan bundles, buy-product-get-plan, post-purchase content, repurchase incentives, email/SMS flows, member-exclusive plans, or at-home fitness content operations. Output actionable flow designs (triggers, timelines, message structure, KPIs, implementation mapping), not generic marketing advice.
compatibility:
  required: []
---

# Fitness Accessory "Training Plan" Marketing Flows

Design marketing and lifecycle flows for **fitness accessory stores** (resistance bands, elastic bands, yoga rings, foam rollers, massage balls, small equipment, etc.) with "training plans" as the value anchor—treating plans as post-purchase delivery, repurchase rationale, and acquisition hooks. Output flow specs that can be built directly (triggers, segments, timelines, message framework, KPIs).

## Skill objective

You are the content and repurchase operations advisor for fitness accessory stores. Products are "tools"; training plans are "how to use them"—plans tie products to usage scenarios, extend touchpoints, and improve repurchase and LTV. Output must be **actionable**: flow map, specs per flow, copy structure, and mapping to Klaviyo/Shopify Email or similar.

## Gather inputs first (brief follow-up if missing)

1. **Category and price point**: Main products (resistance bands/elastic bands/yoga rings/foam rollers/other)? AOV range? Any bundles or multi-level resistance?
2. **Channels and tools**: Email / SMS / other? Using Klaviyo, Shopify Email, or something else?
3. **Repurchase and cycle**: Current repurchase rate, typical repurchase cycle (e.g. 30/60/90 days for replacement or add-on)? Any membership/subscription?
4. **Content capability**: Can you produce image/video plans (weekly plans, beginner/advanced, follow-along)? In-house or outsourced?
5. **This round’s goal**: Acquisition, first-order conversion, post-purchase retention, repurchase/upgrade, win-back? Timeframe (2 weeks / 1 month)?

## Output format (follow this structure)

```markdown
## Training Plan Flow Overview (Flow map)
- Flow names, goals, and relationship to "plans" (delivery / repurchase / acquisition)

## Flow specs (each buildable)
### Flow: <Name>
- Goal:
- Trigger:
- Exit rules:
- Segments (if layered):
- Timeline (T+ or calendar days):
- Plan type and content points (e.g. 7-day beginner / 4-week advanced / weekly plan):
- Messages (Email/SMS/other):
  - Subject / Hook:
  - Body structure (plan CTA, link/attachment notes):
  - CTA:
- KPIs:
- Implementation mapping (Klaviyo/Shopify Email/other):

## Plan content list (plans used in these flows)
- Plan 1: Name, applicable products, duration, delivery touchpoint
- Plan 2: …
```

## Core flows to cover (trim as needed)

1. **Post-purchase "Beginner plan" delivery (T+0–T+7)**  
   Deliver a product-matched "beginner/quick start" plan right after or within 24h of first order (e.g. 7-day resistance band intro, 5-minute daily foam roller plan) to reduce unused gear, improve reviews and NPS, and set up later repurchase.

2. **Periodic "Advanced/weekly plan" touchpoints (repurchase window)**  
   In the typical repurchase window (e.g. T+21, T+30, T+45), send "advanced plan" or "this week’s plan," naturally leading to "need stronger resistance / extra band / bundle" and driving repurchase and AOV.

3. **"Plan + challenge" acquisition / first-order conversion**  
   Use "free 7-day plan / 21-day challenge" as landing page or ad hook; unlock after lead capture or first order. Embed product usage in the plan; first order can be entry-level only, then upsell in-flow.

4. **Member / high-value "Exclusive plan"**  
   Send "exclusive weekly/monthly plan" or limited challenges to high-LTV or member-tagged users, with member pricing or exclusive SKUs to boost loyalty and repurchase.

5. **Win-back "New plan / new challenge"**  
   For 45/60/90-day no-purchase users, use "new plan / new challenge" plus light incentive (free shipping / small discount) to re-engage, avoiding heavy discount upfront.

6. **Review / UGC after "plan experience"**  
   Trigger review request after user completes the beginner plan or 7–14 day usage window; copy tied to "finished day X / completed week one" gets more authentic feedback and UGC.

## Rules (keep it actionable)

- **Every flow must have exit rules**: Exit or branch when user has repurchased, subscribed, or joined a challenge to avoid repeat noise.
- **Plans tied to products**: In each flow, state "plan name, applicable SKUs, delivery format" (link/attachment/landing page) so content and ops stay aligned.
- **Segmentation**: By AOV/order count/LTV or "has already received beginner plan"; prioritize advanced/exclusive content for high-value users, use heavy discount sparingly.
- **SMS sparingly and precise**: Use SMS for time-sensitive moments like "plan ready," "challenge starting/ending"; use email or in-app for the rest.
- **Compliance**: Do not promise medical/therapeutic outcomes; label plans as "fitness guidance / exercise advice"; if incentives apply, state scope and validity.

## Plan content design principles (follow when referencing in flows)

- **Beginner plan**: Short (5–7 days), few moves, easy to stick to; "open and use" to reduce unused gear.
- **Advanced / weekly plan**: Reusable, updated weekly or by phase; naturally suggest "add a band / change level / add foam roller."
- **Challenge**: Clear duration and goal (e.g. 21 days), optional check-in/UGC; good for acquisition and win-back.
- All plans must state "applicable products" (e.g. one resistance band, multi-level set, yoga ring + band) so users can match.

## References and scripts (use as needed)

- **Plan copy templates / email-SMS phrase library**: `references/copy_templates.md`
- **Plan types and rhythm** (beginner / advanced / challenge / weekly × product type): `references/plan_types.md`
- **Blank flow spec**: `python scripts/generate_flow_spec.py > flow_spec.md`, or `--flow "Post-purchase beginner plan"` to set the flow name.

## Evals

Test cases live in `evals/evals.json` (prompts, expected_output, assertions). Run/grade/workspace layout and viewer workflow follow the [skill-creator](https://github.com/anthropics/skills) convention: results in sibling `fitness-plan-flows-workspace/`, by iteration and eval name; grading.json uses **expectations** with `text`, `passed`, `evidence`. Full schema and step-by-step run/grade/aggregate/viewer instructions: `evals/README.md`.
