---
name: stelow-product-trust-building
description: Building trust through perception and guarantee mechanisms. Covers ten pillars to materialize trust, guarantee types from unconditional to anti-guarantees, and strategic approaches for different contexts.
metadata:
  frequency: rare
  category: product
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
disable-model-invocation: true
---

# Building Trust: Perception and Guarantee

## Increasing Success Perception

When someone seeks us out, they carry the weight of past experiences, skepticism, and the fear of making the wrong decision once again. The person is not just asking themselves "does this work?", but rather "**will this work for me?**".

### Ten Pillars to Materialize Trust

1. **Your own story**: showing that you've already walked the path the person wants to travel.
2. **Others' stories**: showing that other people succeeded in accomplishing (testimonials and depositions).
3. **Proof volume**: presenting the number of positive reviews or the quantity of people you've already helped.
4. **Formal validation**: displaying certifications and training that legitimize your knowledge on the subject.
5. **Data and research**: using statistics to anchor the promise of results in evidence.
6. **Expert endorsement**: showing that other reference figures in the field attest to your credibility.
7. **Public figure endorsement**: celebrities and influencers that the person trusts and who recommend you.
8. **Contextual empathy**: describing the person's situation or challenge with such a level of detail that they feel deeply understood.
9. **A new mechanism**: presenting a unique approach or feature that the person hasn't tried yet, opening the possibility that "this time, it might work".
10. **Practical demonstration**: showing the result happening, either live or in a recording, to make success tangible.

---

## Guarantee Commitment

Trust manifests here in a deeper way: not in more gain promises, but in the **removal of loss risk**. Subtracting fear becomes more powerful than adding one more benefit.

### Unconditional Guarantee
The most radical form of removing friction. The message: *"I'm not asking you to say yes or no today, but to make an informed decision. Both choices are risk-free, but only one of them can help you reach your purpose."* The responsibility for risk is fully absorbed by whoever offers the help.

### Super Conditional Guarantees
Co-responsibility approach. Must be **"better than money back"** — because the person's time and energy are also valuable. Aligns commitment: *"If you do your part, I guarantee mine."*

Explicitly state the minimum requirements that the person must fulfill to access the guarantee (e.g., having used the product with a minimum of Y people for so long; having participated for at least X days of training; etc.)

**Examples of super guarantee after passing minimum requirements**:
1. Excess refund (e.g., 2–3x the cost of the product/program/service)
2. Service guarantee (e.g., continue working with them for free)
3. Modified service guarantee (e.g., continue working for twice the time, for free)
4. Credit-based guarantee (e.g., give credit for other programs)
5. Personal service guarantee (e.g., you'll help them 1:1 until they achieve the result)
6. Hotel and airfare (e.g., you'll refund the program and the cost of hotel and airfare)
7. Salary payment (e.g., you'll pay their hourly rate for each hour spent with you, plus the program cost)
8. Commitment release (e.g., they don't need to remain in your contract)
9. Second deferred payment (e.g., you won't charge them again until after they make or get their first result)
10. First result guarantee (e.g., you'll continue paying their accessory expenses until they achieve their first result)

### Anti-Guarantees
In contexts of high demand or rare opportunities, the absence of a guarantee can, paradoxically, signal value. The "all sales are final" policy works best for high-value services or explosive situations, where the opportunity itself is the great attraction.

### Implicit Guarantees (Performance / Revenue Sharing)
- *Performance*: "Pay me only $X per sale you make, per kilo lost, per scheduled appointment"
- *Result sharing*: "Pay me only X% of revenue generated with the product, X% profit share, X% revenue growth relative to baseline"

### Guarantee Stacking
- **Option A**: choose one conditional and one unconditional guarantee and combine them.
- **Option B**: choose two conditional guarantees around small and large results with different terms.
- **Option C**: choose two conditional guarantees with the same terms, but short and long deadlines to show what they could achieve.

## Completeness contract

The host validates these minima — never submit fewer:

- Fear → guarantee mapping with placement and wording.
- At least 500 words and 3 headings.

## Examples

### Example: users hesitate at the payment step

**Input:** "Checkout abandonment is 70%. Help."

**Steps:**
1. Diagnose success perception (what looks risky?).
2. Pick the guarantee matching the fear (money-back, trial, social proof).
3. Place it at the decision point, not on the about page.

**Output:** Fear → guarantee mapping + placement + wording.

## Edge Cases

### Guarantee gets abused
- Constrain scope (time window, usage cap), keep the promise.
### Trust problem is the product, not perception
- Say so: no guarantee fixes a broken core.
### B2B committee buying
- One guarantee rarely fits all stakeholders; layer them.

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

