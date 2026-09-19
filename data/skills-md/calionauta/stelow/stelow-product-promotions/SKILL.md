---
name: stelow-product-promotions
description: Launch promotion strategies using the MAGIC framework. Covers Loss Leader, Gift Card Sale, Limited High-Value Package, and Irresistible Freebie strategies with tactical examples.
metadata:
  frequency: rare
  category: product
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
disable-model-invocation: true
---

# Promotions for Launch

A simple offer, but communicated unequivocally, tends to work better than a brilliant offer that nobody understands.

## MAGIC Structure

**M (Magnet → Reason)**: what is the magnetic reason for this offer to exist now? (discount, special launch condition, seasonal offer) Creates the context.

**A (Avatar → Avatar)**: who is this offer for? Naming the audience helps the person immediately identify. (small business owners? writers? those seeking a healthy lifestyle?)

**G (Goal → Purpose)**: what is the desired outcome the person can achieve? It's not a guarantee, but the direction, the purpose. (clarity in business? launching a product?)

**I (Interval → Timeframe)**: in how much time or for how long? Defines a temporal horizon that makes the promise more concrete. (30 days? 6 weeks? a single meeting?)

**C (Container → Packaging)**: what is the "packaging" of the offer? A word that gives shape to the experience and helps make it tangible. (a program, a blueprint, a workshop, a mentoring, a consulting)

---

## 4 Promotion Strategies for Launch

### Strategy 1: The Loss Leader
Drastically reduce the entry barrier so a new customer can experience your work. You offer an initial product or service with a calculated loss, knowing that a portion of these customers will purchase higher-value solutions in the future.

- **Reason (M)**: give an accessible first step to experience a high-impact solution
- **Avatar (A)**: small business owners who need an initial boost and have a limited budget
- **Purpose (G)**: unlock a specific area of the business and know the potential of deeper work
- **Interval (I)**: visible results in the first session or within a few days
- **Container (C)**: initial consulting with 80% discount to unlock the business

*Tactical Examples*:
- **Unbundle**: offer a part of your main service (a diagnostic session) with a real and significant discount.
- **Next step (upsell)**: at the end of the session, present a clear path to continue the work (full package), perhaps with a small discount for those who decide on the spot.

---

### Strategy 2: Gift Card Sale
Allows generating upfront revenue and turning current customers into an acquisition channel. The person buys a service (for themselves or to gift) with perceived value much higher than the amount paid.

- **Reason (M)**: advance purchase of a future service with a big discount
- **Avatar (A)**: current customers, their friends and family
- **Purpose (G)**: gift someone (or themselves) with a transformation experience
- **Interval (I)**: the service can be redeemed within a defined period (e.g., 6 months)
- **Container (C)**: R$ 200 gift card for only R$ 50 — a gift worth four times

*Tactical Examples*:
- **Card value**: define a credit value (e.g., R$ 200) and a much lower selling price (e.g., R$ 50)
- **Limit**: to avoid cannibalizing future sales, limit the quantity per person (e.g., 3 cards per CPF)
- **Validity**: establish a deadline for redemption (e.g., 6 months) — creates slight urgency

---

### Strategy 3: The Limited High-Value Package
Instead of offering a discount to everyone, create an exclusive and premium offer for the most engaged audience. Scarcity is not in the price, but in **access**.

- **Reason (M)**: access to a unique and exclusive opportunity
- **Avatar (A)**: customers who already trust your work and are ready for a larger investment in exchange for accelerated results
- **Purpose (G)**: achieve a level of result that wouldn't be possible with standard solutions
- **Interval (I)**: limited to the first 10% of the base who respond, or a fixed number of slots
- **Container (C)**: VIP gold package — a 6-month immersion for maximum results

*Tactical Examples*:
- **Premium product**: offer something you don't normally sell (individual mentoring program, close accompaniment for 6 months)
- **Proposed value**: the price must reflect the high value and exclusivity (e.g., R$ 10,000)
- **Scarcity and urgency**: limit the offer to a small number of slots (e.g., 5 people) or short time period (e.g., 48 hours)

---

### Strategy 4: The Irresistible Freebie
Instead of giving a price discount, you **add more value to the original offer**. The perception of getting something valuable for free can be psychologically more attractive than a simple discount.

- **Reason (M)**: a "buy 1, get 2" offer for a limited time
- **Avatar (A)**: customers seeking to maximize the value of their investment and appreciate a good deal
- **Purpose (G)**: get more results for the same price, accelerating the process
- **Interval (I)**: the freebie is enjoyed together with the main purchase
- **Container (C)**: buy 1 consulting package and get 2 extra sessions as a gift

*Tactical Examples*:
- **Valuable freebie**: the freebie must have real perceived value. If you sell a package of 4 consultations, offer 2 extra sessions.
- **Differential in the freebie**: the extra sessions can include a premium service that's not in the normal package
- **Limit**: to create urgency, the offer can be limited to the first 5 customers

## Completeness contract

The host validates these minima — never submit fewer:

- Dated promotion calendar; every offer carries its cap and rollback price.
- At least 600 words and 3 headings.

## Examples

### Example: launch week for a course

**Input:** "Course launches in 3 weeks. Promotion plan?"

**Steps:**
1. Pick the MAGIC strategy fitting the goal (e.g. limited high-value package for revenue + testimonials).
2. Set scarcity honestly (real caps, real dates).
3. Define the post-launch price ladder before discounting anything.

**Output:** Dated promotion calendar with offer, cap, and rollback price.

## Edge Cases

### Audience is cold (no list)
- Borrowed audiences first (partners, affiliates); paid cold traffic last.
### Discount trains bargain hunters
- Bundle value instead of cutting price; protect the anchor.
### Launch flops
- Debrief in public if the brand allows; silent flops teach nothing.

## Entry (mode detection)

When this skill loads, check for the stelow workflow marker:

```bash
if [ -n "$STELOW_WORKFLOW" ] && [ -n "$STELOW_STATE" ]; then
  echo "stelow: workflow mode (state=$STELOW_STATE)"
else
  echo "stelow: standalone mode (no STELOW_WORKFLOW marker)"
fi
```

In **standalone mode** (no marker), run the existing skill body unchanged.
In **workflow mode**, skip to `### Workflow slice` and emit a complete
`## Hand-off (workflow mode)` block at the end. See
`../stelow-workflow-entry/SKILL.md` for the full marker protocol.

## Hand-off (workflow mode)

```
stage          : shape
description    : Shape stage. Define appetite, hill chart, rabbit holes.
status         : <done|partial|blocked>
artifacts      : <paths created or modified>
next-candidate : critique
gate           : none
rework-on      : shape
```

Workflow mode: emit the above Hand-off block verbatim, then stop. The
router skill consumes the next-candidate field and calls
`scripts/stelow advance <next-candidate>` to move state forward.

### Workflow slice

Workflow mode for the **shape** stage. Standalone behavior lives in
the rest of this file (unchanged). Summary:

> Shape stage. Define appetite, hill chart, rabbit holes.

Primary actions (per stages.yaml): `read, write`. Run only the actions that
produce the artifacts promised in `## Hand-off`; skip anything that does
not advance the workflow.

