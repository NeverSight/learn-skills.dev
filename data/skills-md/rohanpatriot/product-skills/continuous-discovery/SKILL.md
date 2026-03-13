---
name: continuous-discovery
description: Applies Teresa Torres's continuous discovery habits to help product teams discover products that create customer and business value. Use when setting product outcomes, interviewing customers, mapping opportunities, generating solutions, testing assumptions, or when user mentions Opportunity Solution Trees, product trios, assumption testing, or continuous interviewing.
---

# Continuous Discovery

I help product teams build the habits needed to continuously discover products that create customer value and business value. Discovery is not a phase — it is a sustained practice of weekly touchpoints with customers, conducted by the product trio, using small research activities, in pursuit of a desired outcome.

## Essential Principles

### Discovery Is Continuous, Not a Phase

Discovery doesn't happen before delivery — it happens alongside it, every week. Teams that treat discovery as a phase front-load research and then stop learning. Continuous teams sustain weekly customer contact throughout the life of the product.

### Outcomes Over Outputs

Shipping features is not the goal. Creating value is. Start with the business outcome, map it to a product outcome you can influence, and let the outcome drive what you build. If you can't connect a feature to an outcome, you shouldn't build it.

### The Product Trio Decides Together

Product managers, designers, and software engineers make discovery decisions as a trio — not sequentially, not in silos. The trio brings complementary perspectives: business viability, usability, and feasibility. If one voice is missing, you're making incomplete decisions.

### Opportunities, Not Solutions

Don't start with solutions. Start with customer needs, pain points, and desires — opportunities. Map the opportunity space before generating solutions. The best solutions come from deeply understanding the problem.

### Compare, Don't Choose

Never fall in love with one idea. Generate at least three solutions for every target opportunity. Compare them against each other. Compare-and-contrast decisions are more rigorous than evaluate-one-at-a-time decisions.

### Test Assumptions, Not Ideas

Ideas are bundles of assumptions. Don't test the whole idea — break it into assumptions, identify the riskiest ones, and test those first. Small, fast assumption tests reduce risk before you commit to building.

## Intake

Use the `AskUserQuestion` tool to determine what the user needs:

**Question:** "Where are you in your discovery process?"

**Options:**
1. **Set or negotiate a product outcome** — Define what success looks like and align with leadership
2. **Discover and map opportunities** — Interview customers and build an Opportunity Solution Tree
3. **Generate and compare solutions** — Ideate, compare, and select solutions for a target opportunity
4. **Test assumptions** — Identify, prioritize, and run assumption tests

## Routing

| Response | Workflow |
|----------|----------|
| 1, "outcome", "goal", "metric", "OKR", "negotiate" | [workflows/set-outcomes.md](workflows/set-outcomes.md) |
| 2, "opportunity", "interview", "customer", "OST", "tree", "map" | [workflows/map-opportunities.md](workflows/map-opportunities.md) |
| 3, "solution", "ideate", "idea", "compare", "story map" | [workflows/ideate-solutions.md](workflows/ideate-solutions.md) |
| 4, "assumption", "test", "experiment", "validate", "risk" | [workflows/test-assumptions.md](workflows/test-assumptions.md) |
| other | Clarify intent, then route appropriately |

**After identifying intent, read the matching workflow and follow it exactly.**

> **Note:** If the user's discovery task involves code changes — instrumenting metrics, building prototypes, setting up recruiting tools — recommend `EnterPlanMode` before proceeding with the workflow.

## Framework Selection

Different frameworks apply to different discovery activities:

| Discovery Activity | Primary Reference | Key Frameworks |
|--------------------|-------------------|----------------|
| Setting outcomes, aligning with leadership | [core-thesis.md](references/core-thesis.md), [frameworks.md](references/frameworks.md) | Outcome Types Hierarchy |
| Customer interviewing, opportunity mapping | [frameworks.md](references/frameworks.md), [techniques.md](references/techniques.md) | Experience Map, Interview Snapshot, Opportunity Solution Tree |
| Solution generation and selection | [frameworks.md](references/frameworks.md), [techniques.md](references/techniques.md) | Story Mapping, Compare-and-Contrast Decision Making |
| Assumption testing | [frameworks.md](references/frameworks.md), [techniques.md](references/techniques.md) | Assumption Mapping |

For any discovery activity, read the relevant reference files before proceeding.

## References

**Core Knowledge:**
- [core-thesis.md](references/core-thesis.md) — Central argument and prerequisite mindsets
- [frameworks.md](references/frameworks.md) — All 8 discovery frameworks with application guidance
- [principles.md](references/principles.md) — 12 guiding principles for effective discovery
- [techniques.md](references/techniques.md) — 11 step-by-step methods for discovery activities

**Quality and Voice:**
- [anti-patterns.md](references/anti-patterns.md) — 28 anti-patterns organized by discovery phase
- [voice.md](references/voice.md) — Terminology precision guide

## Workflows

| Workflow | Purpose |
|----------|---------|
| [set-outcomes.md](workflows/set-outcomes.md) | Negotiate and set product outcomes with leadership |
| [map-opportunities.md](workflows/map-opportunities.md) | Interview customers, create snapshots, and build an Opportunity Solution Tree |
| [ideate-solutions.md](workflows/ideate-solutions.md) | Generate, compare, and select solutions for a target opportunity |
| [test-assumptions.md](workflows/test-assumptions.md) | Identify, prioritize, and test riskiest assumptions |
