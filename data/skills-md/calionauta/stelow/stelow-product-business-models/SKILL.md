---
name: stelow-product-business-models
description: Business model creativity triggers for reducing costs and generating revenue. Based on Jobs to Be Done frameworks from Strategyn to adapt and experiment with new models.
metadata:
  frequency: rare
  category: product
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
disable-model-invocation: true
---

# Business Models

Creativity triggers from Strategyn (Outcome-Driven Innovation / Jobs to Be Done) to adapt and experiment with new business models.

## To Reduce Variable Costs

1. Pass a cost entirely to the customer (self-serve, assemble, install, maintain the product, etc.)
2. Pass an expense to suppliers (inventory tracking sensors, customization of supplies/packaging, etc.)
3. Pass an expense to distributors (acquire and install optional features, maintain the product, store inventory, etc.)
4. Turn a cost into revenue (charge for a sales call, etc.)
5. Turn waste into revenue (sell as byproduct, repurpose, reuse, etc.)
6. Get free supplies and materials (use someone else's waste as raw material, etc.)
7. Use free labor (volunteers, interns, non-profit organizations, academics, etc.)
8. Eliminate an essential business activity or process and reinvest the savings to gain competitive advantage.
9. Incorporate costs when they are at their lowest level (specific period of the year, surplus or liquidation sale, etc.)
10. Decrease a variable cost that forces a reduction in other variable costs.
11. Make costs more variable (hiring methods to suit costs to market conditions, etc.)
12. Reduce costs using existing infrastructure for multiple purposes.
13. Outsource non-essential activities performed inefficiently.
14. Acquire essential activities performed efficiently.
15. Own the infrastructure, not the content.
16. Incorporate more expenses in one area to cut even more expenses in another (bundles instead of tracking multiple packages, etc.)
17. Eliminate a cost through barter.
18. Make a charity contribution in exchange for necessary services.
19. Make a variable cost fixed.

## To Reduce Fixed Costs

1. Use existing resources wisely to eliminate capital investments (facilities, equipment, tools, etc.)
2. Reduce fixed costs by incurring them when they are lowest (when subsidized, when financial incentives are in place, etc.)
3. Use other people's money to pay for capital investments.
4. Own the content, not the infrastructure.
5. Leverage a capital investment made by someone else (intermediary, third party, etc.)
6. Pass a fixed cost to the community (regulatory fees, taxes, etc.)
7. Make a fixed cost variable.

## For Revenue Generation

1. Divert a revenue source from someone elsewhere in the value chain (supplier, distributor, installer, maintainer, etc.)
2. Identify resources inherent to the value delivery platform and sell/use them (information, energy, etc.)
3. Collect revenue that will coerce future revenue generation.
4. Accept a non-cash form of payment (credit card, subscription, royalties, etc.)
5. Accept a non-traditional form of ownership (share, earn, repeat, etc.)
6. Add a revenue source related to the product (optional features, different product line, replacement parts, etc.)
7. Add a revenue source related to the time of purchase (help the customer make the purchase, finance the product, etc.)
8. Add a revenue source related to support (maintenance, installation, training, storage, after-sales service, disposal, etc.)
9. Collect revenue from a different payer (insurer, distributor, advertiser, government, etc.)
10. Generate revenue from operational operations (charge admission for facilities/tours, sell training content to third parties, etc.)
11. Sell a consumable to collect revenue.
12. Increase revenue from charity sources (fundraising organization, non-profit organization.)
13. Collect revenue at a different point in time or at a different frequency.
14. Collect revenue during downtime.
15. Own the content and the infrastructure.

## Completeness contract

The host validates these minima — never submit fewer:

- 2–3 model tweaks (not a pricing change), each with cost math.
- Cost and revenue implications plus the experiment that tests each tweak.
- At least 600 words and 3 headings.

## Examples

### Example: SaaS with crushing onboarding costs

**Input:** "Each new customer costs us 4 hours of onboarding. Ideas?"

**Steps:**
1. Map cost type (variable, human-driven).
2. Pull variable-cost reducers (self-serve onboarding, productized setup, community support).
3. Pair with a revenue-side move (setup fee or onboarding tier).

**Output:** 2-3 model tweaks with cost math, not a pricing change.

## Edge Cases

### Costs are fixed, not variable
- Use the fixed-cost section instead; don't force variable-cost plays.
### Regulated pricing constraints
- Note what the model cannot change before proposing.
### Model change needs sales buy-in
- Flag the stakeholder; models die without the team that sells them.

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

