---
name: stelow-product-pricing
description: Pricing strategies and models for product offerings. Covers exchange bases, consumption control, interest alignment, and perception techniques to formalize value exchange agreements.
metadata:
  frequency: rare
  category: product
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
disable-model-invocation: true
---

# Product Pricing

Thinking about pricing is thinking about the nature of the relationship we want to build. Price is not just a number; it's the **formalization of a value exchange** — an agreement on how risk and benefit are shared.

## Models — Theme: Exchange Base

**One-Time Payment for Ownership — "Buy It, It's Yours"**
Definitive transaction. The customer pays once and assumes total ownership and responsibility. Works well for durable goods or digital products where the maintenance cost for the creator is zero after sale.

**Payment for Access (Instead of Ownership)**
The logic is the exchange of permanent ownership for temporary access. Manifests in main forms:

1. **Access by Time Period**:
   - *Recurring subscription*: periodic payment (usually monthly) to maintain continuous access. Standard model for Netflix, Spotify, most SaaS.
   - *Finite term license*: one-time payment for access for a long and predetermined period (one or five years). At the end of the term, access ends without automatic renewal. Offers predictability for both sides.

2. **Access per Unit of Outcome**: payment is tied to a specific and transactional delivery. Example: AI service that transcribes audios — the customer pays R$ 0.10 per minute of transcribed audio. Pays for output, not for time of use.

⚠️ Don't confuse with "value-generated pricing": in access per unit of outcome, the price is fixed per transaction (X per minute, Y per image). In value-generated pricing, it's a variable percentage of a business impact (Z% of revenue increase).

## Models — Theme: Consumption Control

**Pre-Paid Credits Payment**
The customer buys a package of "credits" in advance, consumed as they use the service. Gives clear control over spending and guarantees upfront revenue for the company. Forces awareness about use — each action has a visible cost that deducts the balance, making consumption more intentional.

**Computational Granularity Pricing**
Driven by variable cost technologies like AI. Price is tied directly to the resource consumed: per seconds/minutes of time that an AI model uses a specialized processor (GPU/TPU), per token of text processed, or per image generated. Reflects the real economy behind the service.

## Models — Theme: Interest Alignment

**Performance Payment**
The provider assumes part of the client's risk. Payment is not tied to the product or time of use, but to the concrete result it generates. If the expected result is not achieved, payment is reduced or non-existent. Requires high trust and ability to measure "performance", but creates powerful alignment of interests.

**Value-Generated Pricing**
Evolution of performance payment. Price is tied to a high-level business indicator — percentage of additional revenue or cost savings that the service provided. It's the deepest form of partnership, turning the provider into a partner in the result.

**Payment with Data**
The customer receives a discount or free access in exchange for permission for their data to be used to train and improve the system, especially AI models. Formalizes a value exchange that often happens in a hidden way.

## Models — Theme: Combinations and New Frontiers

**Bundling**
Instead of selling items separately, group them in a "bundle" with a single price. Increases perceived value (the customer feels they get more for less) and simplifies the pain of purchase decision (a single transaction instead of several micro-transactions).

**Hybrid Pricing**
Combines stability with flexibility. Usually: a fixed subscription fee to guarantee access to the platform and basic set of features, plus a variable component for consumption of more expensive resources (AI credits, advanced features). Seeks balance: revenue predictability for the company and feeling of fairness for the customer.

---

## Application Strategies

**Stepped Pricing / Tiered Pricing — Pre-Sale/Launch Strategy**
Turns pricing into a participatory event, directly rewarding the trust and agility of the first adopters. The risk for the buyer is higher at the beginning (little social proof), so the price should be as low as possible at this moment.

*Example*:
- Initial batch: symbolic value (e.g., R$ 10) for the first buyers
- Following batches: with each new group of 50 people, the price increases by fixed amount (e.g., R$ 50) or percentage (e.g., 10%)

Benefits: creates strong sense of urgency; clear incentive not to "leave for later"; generates quick feedback cycle on demand.

⚠️ Requires transparent communication — the increase rules must be clear to everyone from the beginning.

**Subscription Fatigue — Market Response Strategy**
We are in a phase of "subscription fatigue" — the accumulation of small monthly charges generates constant cognitive and financial burden for consumers. Alternatives:

- *Alternative billing cycles*: offer quarterly or annual — longer cycle usually comes with discount
- *One-Time Payment (Lifetime Deal)*: return to one-time payment. "Buy once, use forever" eliminates recurrence anxiety and creates a sense of ownership.
- *Long-Term License*: usage license for a determined time (one, two, or three years) with expressive discount for single upfront payment.

---

## Perception and Trust

The way price is presented has a profound impact on how it is perceived.

**Monetary Abstraction**: when presenting a price as "20" instead of "R$ 20.00", two sources of noise are removed: the dollar sign (explicit reminder of the act of spending) and cents. A clean and direct number tends to be processed more fluently.

**Magnitude Perception (Endings 5, 7, and 9)**: left-digit effect — the brain processes the first digit from the left as an anchor for magnitude perception. That's why 9.99 seems significantly cheaper than 10.00.

**Time (Temporal Reframing)**: fractioning into smaller and more palatable time unit. Software that costs R$ 365 per year can be presented as "just R$ 1 per day". Anchors the cost to a trivial daily expense.

**Decoy (The Decoy Effect)**: introduce a third price option intentionally less attractive, to make one of the others look better in comparison.

**Recontextualization (Value Anchoring)**: instead of anchoring the price on direct competitors, anchor on the **value of the solution you replace**. Example: an AI agent that performs sales should not be compared to other software, but rather to the cost of a salesperson's salary.

---

## The Trust Pact: An Anti-Lock-In Pricing Approach

In a saturated market, where customers feel increasingly trapped in services by contracts, inertia, or difficulty migrating data, **trust can be the biggest competitive differential**.

Building a "trust pact" means designing the commercial relationship in a way that gives power and autonomy to the customer. It rests on three principles:

**1. Contractual Freedom (The Right to Exit)**
The customer can end the relationship whenever they want, without bureaucratic barriers or punitive fines. *The message: the customer stays for the quality of the service, not for a contractual obligation.*

**2. Financial Freedom (Insurance Against Initial Risk)**
Ensures that if a customer changes their mind — especially in the first few months — they don't lose their entire investment. Mechanics: fair refund with the returned value deducting only the usage period calculated based on the standard price, without discount.

**3. Informational Freedom (Data Belongs to the Customer)**
The exit barrier of a service cannot be the difficulty of taking their data away. An explicit commitment to **data portability** — exporting information easily, freely, and in an open format — is the recognition that the company offers a tool, but the work and creation belong to the user.

**Why Adopting These Principles is Also a Business Strategy**: a company that facilitates customer entry and exit is making a bold bet on the quality of its own product, signaling that it intends to retain customers **by merit, and not by lock-in**.

## Completeness contract

The host validates these minima — never submit fewer:

- Metric recommendation with guardrails and perception framing.
- At least 600 words and 3 headings.

## Examples

### Example: price a new analytics add-on

**Input:** "What should we charge for the add-on?"

**Steps:**
1. Pick the exchange base (seats, events, value metric?).
2. Check consumption control (what stops runaway cost?).
3. Align interest (does the price grow when customer value grows?).

**Output:** Metric recommendation + guardrails + perception framing.

## Edge Cases

### Costs scale faster than willingness to pay
- Redesign the metric before discounting; discounts don't fix unit economics.
### Enterprise demands custom pricing
- Contain it: custom quotes, standard metric.
### Price increase on existing customers
- Grandfather explicitly; trust compounds, surprises destroy it.

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

