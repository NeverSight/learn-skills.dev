---
name: validation-experiments
description: Designs smoke tests, fake doors, concierge and Wizard of Oz MVPs, pre-sales, and design-partner experiments with ILI metrics, success and fail thresholds. Use when the user asks to test demand, run a smoke test, pretotype, validate an idea, or design an experiment.
disable-model-invocation: true
---

# Validation Experiments

Link each experiment to one row in the `assumption-map` ledger. Map results to evidence levels in `idea-scorecard` (Intent = 3; payment = 5).

## Loop

1. **Assume** — state the riskiest assumption
2. **Design** — choose the smallest test that can falsify it
3. **Test** — run the experiment
4. **Measure** — collect quantitative data (ILI, CTR, conversion, payment)
5. **Learn** — extract insights
6. **Decide** — proceed, pivot, or kill

## Technique picker

| Technique                     | Best for                                                    | Not for                            |
| ----------------------------- | ----------------------------------------------------------- | ---------------------------------- |
| **Fake door**                 | Demand for a specific offer/feature; priced CTA             | Proving retention or full workflow |
| **Smoke test / landing**      | Message–market fit, segment + offer at scale                | Deep workflow discovery            |
| **Concierge MVP**             | Learning what to build; pains and language (5–10 customers) | Scalable unit economics            |
| **Wizard of Oz**              | Testing UX and workflow without backend                     | First read on abstract demand      |
| **Pre-sale / design partner** | Willingness to pay and delivery commitment                  | Anonymous traffic only             |

**Recommended sequence:** fake door (priced) → concierge (5–10) → Wizard of Oz at small scale → build only if assumptions falsify the kill path.

## ILI (Initial Level of Interest)

From pretotyping: **ILI = actions_taken / opportunities_offered**

- *Opportunities:* visitors who saw the offer (or segment reached)
- *Actions:* paid pre-orders, deposits, qualified signups with stated intent, or explicit purchase clicks per your threshold

Record ILI with segment, offer, and date. Label as proxy — not audited revenue.

## Experiment plan template

| Field                   | Value                                                                             |
| ----------------------- | --------------------------------------------------------------------------------- |
| Riskiest assumption     |                                                                                   |
| Linked assumption ID    | (from assumption-map)                                                             |
| Method                  | fake door / smoke test / concierge MVP / Wizard of Oz / pre-sale / design partner |
| Audience                |                                                                                   |
| Duration                |                                                                                   |
| Price shown?            | yes / no — **must be yes** for WTP tests                                          |
| Success threshold       |                                                                                   |
| Fail threshold          |                                                                                   |
| Evidence quality target | (scorecard level 3–5)                                                             |
| ILI target              | optional numeric                                                                  |

## Ethical fake door

After the CTA, be honest: the product is not built yet. Offer waitlist, founder call, or refund policy — do not imply shipping software that does not exist.

## Benchmarks (calibrate per segment)

- Landing visitor → signup: **5–15%** can be healthy for warm/niche traffic; **&lt;1%** on cold paid traffic is often a kill signal for that offer.
- Pre-sales and design-partner **time commitments** beat email-only signups.
- Do not count views, likes, or unqualified clicks as validation.

## Output

Save plans and results to `discovery/<topic-slug>/experiments/YYYY-MM-DD-<topic-slug>-experiment.md`.

Default sections: Facts, Assumptions, Evidence, Analysis, Decision, Next experiment.
