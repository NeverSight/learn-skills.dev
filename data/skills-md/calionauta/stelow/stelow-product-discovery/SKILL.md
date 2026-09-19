---
name: stelow-product-discovery
description: >
  [stelow] Complete expert in the short-cycle product learning method,
  based on the e-book "Guide to Creating Products with Short Learning Cycles" by calionauta.
  Use this skill whenever the user asks about: idea validation, customer discovery,
  product experimentation, jobs to be done, pricing strategies, business models, marketing channels,
  early adopters, MVP, product-market fit, pre-sales, launch strategies, product innovation,
  product lifecycle, building customer trust, marketplace, open source as strategy,
  or any concept related to creating and validating digital products with low risk and fast learning.
  This skill contains ALL the method details — do not skip any detail.
metadata:
  frequency: monthly
  category: product
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
---

# Product with Short Learning Cycles

This guide is a method to replace speculation with evidence, step by step.
**Core principle**: experiment before building. Reduce uncertainty with small, fast, and cheap experiments.

> "Life is too short to build something that nobody wants." — Ash Maurya

## Method Structure

The process has **8 stages** (not necessarily linear):
1. Find and understand the audience
2. Define the market
3. Define and prioritize solutions
4. Develop and evaluate the offer
5. Assess commitment
6. Discover the process
7. Evolve to a viable business
8. The pulse of the system: signals in tension

**→ Read reference files as needed:**
- `references/01-experimentation-principles.md` — criteria for reliable data + 6 principles
- `references/02-stages-1-to-3.md` — audience, market, solutions
- `references/03-stages-4-to-6.md` — offer, commitment, manual process
- `references/04-stage-7.md` — viable business, product-market fit, channels
- `references/05-stage-8-signals.md` — pulse of the system, signals in tension
- `references/06-appendix-business-models.md` — business models, open source, pricing
- `references/07-appendix-strategies.md` — marketplace, solutions, trust, bonuses, promotions, ads, lifecycle

## When to Read Each Reference

| User asks about... | Read... |
|---|---|
| How to validate an idea / experiment | 01, 02 |
| Target audience, market, jobs to be done | 02 |
| Solution, product, features | 02, 03 |
| Offer, advertisement, early adopters | 03 |
| Pre-sale, commitment, waitlist | 03 |
| MVP, manual process, concierge, wizard of oz | 03 |
| Product-market fit, channels, viable business | 04 |
| Metrics, retention, growth | 04, 05 |
| Pricing, pricing models | 06 |
| Business models, revenue, costs | 06 |
| Open source as strategy | 06 |
| Marketplace, supply and demand | 07 |
| Trust, guarantees, social proof | 07 |
| Bonuses, launch promotions | 07 |
| Online ads, stages of awareness | 07 |
| Product lifecycle, innovation | 07 |

## Interaction Tool Guidelines

**IMPORTANT**: When the user needs to choose between predefined options, ALWAYS use the `question` tool (if available) with enumerated format:
- Options with short `label` and `description`
- Examples: topic selection, next steps, etc.

When `question` tool is not available, use enumerated text in chat (A/B/C/D or 1/2/3).

**Note for this skill**: This is primarily a reference/exploratory skill. If the user wants to explore a specific concept, you may ask clarifying questions to understand context before recommending which references to read or which stage to focus on.

---

## Rules for Using This Skill

1. **Never omit details** — the e-book is already concise; every detail matters.
2. **Use concrete examples** from the method when explaining concepts.
3. **Reference specific tools and tactics** mentioned in the method.
4. **Preserve the order and logic** of stages when guiding the user.
5. **Combine stages** when context demands (e.g., stages 4 and 5 often go together).

---

## Attribution

This skill is based on the e-book **"Guia para criar produtos com aprendizado em ciclos curtos"** (Guide to Creating Products with Short Learning Cycles) by **calionauta**.

**Author**: calionauta  
**Substack**: [Practical Guide to Validate Ideas](https://calionauta.substack.com/p/roteiro-pratico-para-validar-ideias)  
**GitHub**: [@calionauta](https://github.com/calionauta)

This skill was translated and adapted by permission and attribution to the original author.

---

**Original Repository**: [github.com/calionauta/my-opencode-config](https://github.com/calionauta/my-opencode-config)

---

## Extended Deep-Dives (Optional)

For specialized analysis, these standalone skills are vendored in this repo
under `skills/` (historically published at
[github.com/calionauta/agent-sync-public](https://github.com/calionauta/agent-sync-public/tree/main/skills)):

| Skill | Description | Lines |
|-------|-----------|--------|
| `stelow-product-health` | Product health monitoring via signals in tension | ~100 |
| `stelow-product-pricing` | Pricing strategy: Exchange Base, Consumption Control, Interest Alignment, Trust Pact | ~100 |
| `stelow-product-open-source` | OSS as business strategy: Proprietary Problem, Org Structures, Competition Protection | ~60 |
| `stelow-product-trust-building` | 10 pillars of trust, guarantees, perception, commitment | ~60 |
| `stelow-product-promotions` | MAGIC framework, 4 launch strategies, bonuses | ~60 |
| `stelow-product-business-models` | Cost reduction & revenue generation models | ~80 |
| `stelow-product-ads` | 5 awareness stages, ad categories | ~50 |
| `stelow-product-paywall` | Paywall & onboarding monetization funnel (paywall-first build order, 3 funnel benchmarks, trial policy, web2app) | ~310 |

**Install:** already vendored in this repo — no separate install needed.
**Note:** These are optional enhancements. The core method works without them — the references/ contain all the necessary content.

## Completeness contract

The host validates these minima — never submit fewer:

- Experiment plan with success/abort thresholds and the next step either way.
- At least 600 words and 3 headings.

## Examples

### Example: validate a meal-planning app idea in two weeks

**Input:** "I have an idea for an app. What do I do first?"

**Steps:**
1. Frame the riskiest assumption (will busy parents pay for planning?).
2. Pick the shortest-cycle experiment (concierge week, not a build).
3. Define abort criteria before running.

**Output:** Experiment plan with success/abort thresholds and next step either way.

## Edge Cases

### User wants to build immediately
- Slow down explicitly: name the unvalidated assumption building would bet on.
### No access to users
- Proxy with adjacent audiences; mark evidence weaker.
### Experiment succeeds ambiguously
- Treat as not-validated; tighten the threshold and re-run once.

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
stage          : context
description    : Strategic context. Market analysis, JTBD, domain detection. Gated by `context:5` (appetite/review mode): Product Spec Ga
status         : <done|partial|blocked>
artifacts      : <paths created or modified>
next-candidate : shape
gate           : none
rework-on      : setup
```

Workflow mode: emit the above Hand-off block verbatim, then stop. The
router skill consumes the next-candidate field and calls
`scripts/stelow advance <next-candidate>` to move state forward.

### Workflow slice

Workflow mode for the **context** stage. Standalone behavior lives in
the rest of this file (unchanged). Summary:

> Strategic context. Market analysis, JTBD, domain detection. Gated by `context:5` (appetite/review mode): Product Spec Gate+Auto skips; others use reduced ask. S

Primary actions (per stages.yaml): `read, write`. Run only the actions that
produce the artifacts promised in `## Hand-off`; skip anything that does
not advance the workflow.

