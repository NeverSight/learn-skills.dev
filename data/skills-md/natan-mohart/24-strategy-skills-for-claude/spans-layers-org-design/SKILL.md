---
name: spans-layers-org-design
description: Measures average span of control by management layer against benchmark via a bundled calculator, prices the annual cost of carrying more management layers than the organization needs, and flags narrow spans without assuming they're automatically wrong. Use whenever the user wants to review org structure for efficiency, is deciding whether to flatten layers or consolidate management roles, needs to size the cost of an over-layered organization, or has a headcount plan built without checking actual spans of control.
---

# Spans & Layers Org Design

## When to use
Use whenever an organization's cost structure needs review and management headcount hasn't been checked against actual span of control, or when deciding whether to flatten a structure. This is a well-established organization-design technique: narrow spans of control (too few direct reports per manager) usually mean more total layers than necessary, which adds cost, slows decisions, and dilutes accountability without adding real supervisory value.

## What it does
Computes actual average span of control at every management layer, compares it to a benchmark span by layer type (executive, middle management, frontline management typically warrant different benchmark spans), and via a bundled calculator prices the annual cost of the excess management positions implied by spans narrower than benchmark — turning "our org feels top-heavy" into a specific, defensible dollar figure.

## Method
1. **Map every management layer** from the top of the organization down to individual contributors, with the manager count and total direct reports at each layer.
2. **Set benchmark spans by layer type**, not one blanket number — executive layers typically warrant a narrower span (5-7) than frontline management (8-12), since the nature of the work differs; use company-specific or industry benchmark data where available rather than a generic rule of thumb.
3. **Run the bundled calculator** (`scripts/spans_layers.py`) to compute actual average span per layer, flag layers narrower than benchmark, and estimate the annual cost of excess management positions implied by those narrow spans.
4. **Do not treat every narrow span as automatically wrong.** A narrow span sometimes reflects genuine complexity (highly technical work needing closer supervision, a newly formed team still stabilizing) — investigate each flagged layer before recommending consolidation, rather than mechanically applying the benchmark.
5. **Distinguish structural narrowness from a point-in-time artifact**: a layer that's narrow because of a recent reorg or a temporary vacancy reads differently than one that's been narrow for years, which usually signals accumulated organizational layering (title inflation, legacy structure, avoiding a hard consolidation conversation).
6. **Size the total opportunity** as the calculator's estimated cost of excess positions, but present it as an upper bound to investigate, not a mandate to cut — the number's job is to justify spending time on the org-design question, not to prescribe headcount reductions before the qualitative check in step 4 happens.
7. **Where consolidation is genuinely warranted, sequence it deliberately**: which layers, in what order, with what transition plan for affected managers — this feeds directly into a 100-day-plan or transformation execution sequence rather than being announced all at once.
8. **Recheck periodically**, since spans drift naturally as an organization grows through hiring that doesn't keep pace with headcount added below a given layer.

## Inputs
- Organization chart data: manager count and direct reports at every layer
- Benchmark span of control by layer type (company history, industry benchmark, or a defensible default)
- Average fully loaded manager cost
- Config saved as JSON matching the format documented at the top of `scripts/spans_layers.py`

## Output format
Layer-by-layer table of actual span vs. benchmark with a narrow/OK flag; total management headcount and layer count; estimated excess management positions and their annual cost; explicit caveat distinguishing genuine complexity from accumulated layering; sequencing guidance for any warranted consolidation.

## Example
A mid-market company's org chart shows four management layers with spans consistently in the 3-4 range against a 5-8 benchmark by layer type, implying roughly 93 more management positions than a benchmark structure would need, priced at $13.5M annually. Rather than announcing an immediate cut, the qualitative check finds two of the four layers were recently reorganized and are still stabilizing (narrow for a legitimate reason), while the other two have been structurally narrow for over three years — the consolidation recommendation focuses only on those two, sequenced over two quarters with a clear transition plan for affected managers.

## Common pitfalls
- Treating every narrow span as a cost-cutting mandate without checking whether it reflects genuine, current complexity.
- Using one blanket benchmark span across every layer type instead of differentiating executive, middle management, and frontline benchmarks.
- Announcing a full reorganization immediately instead of sequencing consolidation deliberately, which damages trust and execution quality.
