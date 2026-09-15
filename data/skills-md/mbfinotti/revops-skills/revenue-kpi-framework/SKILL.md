---
name: revenue-kpi-framework
description: Design the org-wide revenue KPI framework at the macro level - which metrics matter at each org level from board to IC, how they roll up through a reconciling metric tree with explicit math, who owns each branch, which guardrail counter-metrics ride alongside each owned number, and how the set is gated by company stage and business model. Use whenever the user mentions a revenue KPI framework, a metric hierarchy, a KPI tree, a North Star metric, driver metrics, guardrail counter-metrics, NRR, or which revenue metrics each org level should track - even if they never say "framework". Covers B2B and B2C. Do NOT use for writing the board report itself - use mbfinotti/revops-skills@revenue-reporting instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.1"
---

# Revenue KPI Framework

You are the strategic partner to revenue leadership designing the company's KPI framework: which metrics matter at which org level, and how they roll up. The deliverable is a reconciling metric tree with named owners, paired guardrails, and an altitude/cadence map - a causal model of how this business makes money, not a longer list of numbers.

## Ground Rules

- Macro only. Decide which metrics exist, how they decompose, who owns each branch, and at what altitude and cadence each is reviewed. Never build dashboards, write SQL, or draft the board narrative - route those to the sibling skills in Reference.
- The tree is the artifact, not the single number. Two independent practitioner critiques converge here, and the convergence is the central design caution, never a footnote:
  - John Cutler, co-author of Amplitude's own North Star Playbook: the durable artifact is the causal/driver diagram, not the discipline of forcing alignment on one metric.
  - Christina Wodtke and Felipe Castro: reject strict multi-level OKR cascading ("doesn't scale at all").
- Decompose metrics causally, align goals through negotiation:
  - a KPI tree is metric structure with reconciling math
  - an OKR cascade is goal-setting
  - never present the tree as an OKR cascade repeated at every level, and never claim goal alignment falls out of metric decomposition
  - OKRs, KPIs, and a North Star interconnect rather than compete, a Key Result can target a KPI or one of its inputs; never compare them as three alternatives to pick from
- A tree only earns the name if every parent equals the sum, product, or ratio of its children and every number reconciles up. A bullet list of metrics that merely sound related is not a tree. The operator is dictated by the business arithmetic, not chosen for taste.
- Every branch has exactly one owner. Shared ownership is no ownership: when a jointly-owned number misses, each owner points at the other. When a metric genuinely spans two teams, re-cut it at the handoff boundary (marketing owns lead-to-MQL and MQL quality; sales owns SQL-to-opportunity and close) instead of sharing it.
- Every owned metric gets exactly one paired counter-metric measuring the quality dimension its quantity dimension can't see (Andy Grove's paired indicators, 1983 - the only durable defense against Goodhart's Law). A guardrail is not "a second metric to also watch"; it is the specific quality-side pair.
- Classify leading vs. lagging relative to the metric being predicted, never as a fixed label on the metric itself. Pipeline leads revenue but lags the outbound that built it. Test per the 4DX standard: a good lead measure is predictive AND influenceable by the team inside the current cycle.
- Cap any single level or view at 5-7 metrics. Beyond that the reader stops orienting; 5-7 tracked intensely beats 50 tracked loosely.
- Cite every benchmark with its survey, sample size, and year; never blend figures across surveys or vintages - published sources differ by definition and segmentation, so a blended number is wrong by construction.
- This skill decides WHICH metrics and how they cascade. Where definitions live, who signs them, and how they change is governance - specify what each definition stub must disclose, then hand the stubs to the data-governance skill (see Reference).
- Every ranked menu below states a default order, not a law - it shifts with context and with who executes it. Re-rank against the Interview answers and what this company already has: a warehouse team that can encode definitions, an exec sponsor already convinced, a metric dictionary half-built. Name which answer moved which option.

## Interview

Ask before designing anything. One question per message; multiple-choice where possible; skip anything already answered.

- What triggered this: no framework exists, teams hit their numbers while revenue stays flat, every dashboard shows a different figure, a new leader wants one scoreboard, or a planning cycle demands it?
- B2B, B2C, or both? If B2C: subscription, transactional/e-commerce, or marketplace?
- Revenue model: seat subscription, usage/consumption, hybrid (committed base + overage), PLG/self-serve, sales-led, marketplace/take-rate? This decides whether ARR/NRR conventions even apply.
- Company stage: pre-seed/seed, Series A, Series B, Series C+/growth, late/pre-IPO?
- Which org levels actually exist and review numbers today: board, exec team, function heads, team leads, ICs? A 20-person company doesn't need six altitudes.
- Roughly what share of revenue comes from existing customers (retention + expansion) vs. new logos? This weights the tree's branches.
- What already circulates: a North Star, OKRs, a metric dictionary, named owners? Design around what has traction rather than demolishing it.
- How many quarters of history exist per candidate metric, and do finance and the CRM agree on the headline number today?
- By what date must the framework land - is a board meeting or annual planning cycle waiting on it? A hard deadline promotes the shallower build rungs.
- Is this a one-off scoreboard for a specific decision, or a compounding operating asset? A compounding mandate promotes the deeper rungs and makes cadence design non-optional.
- What is the effort ceiling: workshop hours from function heads, analyst time, political capital to name single owners for contested numbers? No sponsor for ownership fights caps the build at the driver-tree rung, and the deliverable says so.

## Workflow

1. Run the Interview. Confirm the scope boundary: framework design, not report writing, not dashboard building, not definition governance.
2. Pick the build depth from Depth of Build below, re-ranked against the Interview answers. Get the user's explicit agreement on the rung before designing.
3. Settle the top of the tree per Top of the Tree below. Do not decompose until the user validates the top-level outcome.
4. Enter explicit brainstorming: present 2-3 candidate tree designs per Candidate Designs below, with trade-offs and one recommendation. Let the user pick or blend; validate before building on it.
5. Decompose the chosen design per Tree Design below, using the matching worked tree in [references/worked-metric-trees.md](references/worked-metric-trees.md) as the model.
6. Assign one owner per branch and one guardrail pair per owned metric per Ownership and Guardrails below, mechanics in [references/guardrail-pairs.md](references/guardrail-pairs.md).
7. Map each metric to an altitude and review cadence per Altitude and Cadence below.
8. Run the stage and business-model gate per [references/stage-and-model-gating.md](references/stage-and-model-gating.md): strike metrics that don't matter yet, add the ones the stage now demands.
9. Emit the deliverable (Output Shape below) one artifact at a time for user validation. Never present the whole framework as a fait accompli.
10. Check the Pass Threshold; iterate until it holds or every remaining gap is explicitly scheduled.
11. If your harness has persistent memory, store the settled top metric, tree, owners, and guardrail pairs so later reporting and planning runs start from the decided framework instead of re-interviewing.

## Depth of Build

The four rungs below are listed by increasing depth; the efficiency line is what picks between them, not the row order. Deeper is not automatically better - each rung down adds standing maintenance cost.

- value: `encoded framework > full tree > driver tree > metric shortlist`
- effort: `encoded framework > full tree > driver tree > metric shortlist`
- efficiency: `driver tree > metric shortlist > full tree > encoded framework`

1. **Metric shortlist** - the 5-7 board/exec metrics picked by stage and business model, no decomposition. An afternoon. Enough for a one-off board ask; gives teams nothing to pull.
2. **Driver tree** - top outcome plus 3-5 driver metrics with reconciling math, one owner and one guardrail each. Days, including the ownership negotiations.
3. **Full tree** - drivers decomposed to team-owned and activity-level leaves, altitude and cadence map attached. Weeks of cross-functional workshops.
4. **Encoded framework** - the full tree's definitions written into a metric dictionary or semantic layer, reviews wired into standing WBR/MBR/QBR cadences. A quarter to establish, then a standing job.

- Default rung: the driver tree.
- Move up to the full tree when:
  - two teams dispute an owned number
  - planning needs activity-level decomposition to size headcount and budget
- The efficiency order starves the encoded framework: highest value, highest effort, loses every round. Its promotion condition:
  - recurring dashboard disagreements on the same metric
  - more than one BI tool serving the same numbers
- Below that threshold, encoding is premature centralization.

## Top of the Tree

- Revenue itself is usually a poor North Star: it lags, reporting that growth happened without showing where to intervene. A well-chosen top metric leads revenue. Sean Ellis's definition: the single metric that best captures the core value the product delivers to customers.
- The top metric should sit one level out of reach - moved only through its inputs, never directly (Cutler: "If you can move your North Star directly, it's probably not a good North Star"). A North Star alone is not operable; it needs its 3-5 input metrics to mean anything.
- Common defensible tops:
  - NRR or the ARR waterfall for B2B subscription
  - a usage/consumption outcome plus RPO for usage-based
  - repeat-purchase or cohort-retention outcomes for B2C
- Published company examples in [references/stage-and-model-gating.md](references/stage-and-model-gating.md) - treat them as illustrations, not benchmarks.
- Growth-framework vocabulary, if the user brings it:
  - AARRR (McClure, 2007): tags effort to funnel stages, useful as a coverage check, not a tree.
  - RARRA reordering: encodes the same retention-before-acquisition priority the stage gate applies.
  - Reforge growth loops: model compounding growth mechanics as their own spreadsheet metric tree, a sibling artifact for the growth team, not a replacement for the revenue tree.
  - David Skok's "A High Growth SaaS Playbook - 12 Metrics to Drive Success" (SaaStock NYC, 2018): a sequential layer stack from bookings through funnel metrics, salesforce metrics, sales/marketing alignment, and churn - use as a coverage check for which metric categories a SaaS business needs, not as this skill's decomposition structure.
- If the user insists on a single composite number with no decomposition, state the Cutler caution once, then build the shortlist rung well rather than a tree badly.

## Candidate Designs

Brainstorm before recommending. Present 2-3 candidate trees, each specified as:

- top metric
- the 3-5 drivers with their decomposition operator
- where ownership would sit
- what the design optimizes for
- its standing maintenance cost

Follow with a trade-off comparison and one recommendation with reasoning. Candidates should genuinely differ, e.g.:

- NRR-topped, retention-weighted
- ARR-waterfall-topped, acquisition-weighted
- North-Star-usage-topped, PLG

Not three paint jobs on one design.

This menu is generated per engagement, so it carries no fixed efficiency ranking: rank the candidates for this user by fit to their Interview answers (revenue mix, stage, model), and say which answer drove the recommendation.

## Tree Design

- Four decomposition operators cover practically every case. Pick per node from the arithmetic, not from taste:
  - **multiplicative**: Revenue = Traffic × Conversion × AOV
  - **additive**: Net New ARR = New Logo + Expansion − Churn − Contraction
  - **funnel/ratio**: stage-to-stage conversion, coverage = qualified pipeline / target
  - **input/output**: controllable inputs feeding an outcome
- Branching factor: one top metric, 3-5 drivers, 2-3 team-owned metrics per driver. Stop decomposing once a leaf is a metric one team can move within a week.
- Cycle-time chain test, applied per node:
  - activity-level leaf: should move same-day
  - team metric: within the natural business cycle
  - driver: within the reporting period
- If the chain doesn't hold, the tree is decorative rather than causal.
- Composites must decompose. NRR is itself gross retention + expansion − contraction; a tree that stops at NRR gives teams nothing to pull. Same for Rule of 40, magic number, and any ratio: expose the numerator and denominator as their own nodes.
- Worked trees - a full B2B SaaS ARR tree with owners and guardrails, a B2C subscription/repeat-purchase tree, a usage-based variant, and a negative example that fails reconciliation - are in [references/worked-metric-trees.md](references/worked-metric-trees.md).

## Ownership and Guardrails

- Name a single directly-responsible owner per branch - the accountable decision-maker for the number, not necessarily the person doing the work. A company-level metric should also exist at the functional level with a functional owner; a metric nobody below the exec team owns is a scoreboard, not a lever.
- Split owner from steward where the org can:
  - **Owner**: answers for the number's performance.
  - **Steward**: answers for its definition and data quality.
- The steward can differ from the owner without violating single ownership - they own different things.
- Attach 2-3 guardrails at the level of the input metrics, riding alongside them - not bolted onto the top metric as an afterthought. Standard GTM pairs, Grove's method, and the named laws are in [references/guardrail-pairs.md](references/guardrail-pairs.md).
- Write the gaming decision rule into the framework itself: an owned metric rising while its paired counter-metric falls for two consecutive review cycles is treated as gaming, not improvement - escalate, never reward it.

## Altitude and Cadence

Map every metric in the tree to the level that reviews it and how often. The scaffold (adapt the metric-to-altitude mapping per business; the mapping below is a starting point, the cadence structure is Amazon's documented practice):

| Altitude      | Typical metrics                            | Cadence                   |
| ------------- | ------------------------------------------ | ------------------------- |
| IC / team     | Activity leaves, one owned driver input    | Daily / weekly (WBR)      |
| Function head | Driver metrics, efficiency ratios          | Weekly / monthly (MBR)    |
| Executive     | Top metric, NRR, Rule of 40, burn multiple | Monthly / quarterly (QBR) |
| Board         | ARR growth, net ARR, cash, Rule of 40      | Quarterly                 |

- Enforce the 5-7 cap per altitude. The same tree serves every level; each level sees its own slice, not the whole tree.
- A metric owner presents insight at the review, not the number - reading the figure aloud is the failure mode the cadence exists to prevent.
- Cadence tiers check different things, monthly vs. quarterly:
  - **Monthly**: checks execution, changes behavior.
  - **Quarterly**: checks strategy, changes the plan.
- A monthly meeting that quietly acquires quarterly authority (changing quotas, territories) destroys the plan the quarterly tier is supposed to test - state each tier's decision rights in the framework.
- A metric can be green at one altitude while hiding a real problem one level down - which is exactly why every altitude's slice must connect to the slice below through the tree's math, not through summary judgment.

## Stage and Business-Model Gate

Run every candidate metric through two gates before it enters the framework; full tables in [references/stage-and-model-gating.md](references/stage-and-model-gating.md).

- **Stage gate.** Which metrics matter shifts by funding stage:
  - pre-seed: activation and retention lead
  - Series B: NRR and fully-loaded LTV:CAC arrive
  - growth stage: Rule of 40 and burn multiple

  The governing rule:
  - early-stage: a pass on efficiency metrics, never on retention
  - late-stage: a pass on growth rate, never on efficiency

  Enforcing a metric too early (unit economics pre-PMF) is as much a design error as adopting one too late.

- **Model gate.** ARR/NRR conventions were built for committed monthly subscriptions and degrade as commitment weakens:
  - usage-based: RPO and committed-vs-consumed tracking, alongside or instead of NRR
  - marketplaces: GMV with take rate (GMV alone is vanity)
  - B2C transactional: cohort curves and the contribution-margin stack

  The tree's math, ownership discipline, guardrail pairing, and altitude capping transfer unchanged across models - only the atoms change.

- Every definition stub the framework hands to governance must disclose its method choices where methods genuinely diverge: which NRR method (cohort vs. formula), how overage revenue is treated, what ARR excludes. A metric without these disclosures is not comparable across periods, let alone companies.

## B2B and B2C

- **B2B subscription:** the tree is retention-weighted - NRR/GRR and the ARR waterfall on top, pipeline drivers (coverage, win rate, deal size) under the new-logo branch, and expansion and churn drivers under the retention branch. Logo retention and dollar retention are separate nodes; netting them hides opposite dynamics.
- **B2C subscription/transactional:** the tree is repeat-purchase-weighted - cohort retention curves (they must flatten; great ones smile), repeat purchase rate, DAU/MAU where frequency genuinely matters, and the CM1/CM2/CM3 contribution stack as the efficiency spine. Prefer contribution-margin LTV and cohort curves over point-estimate LTV formulas, whose inputs are interdependent rather than independent.
- What is identical in both, and worth saying so:
  - reconciling decomposition
  - single-owner branches
  - Grove guardrail pairs
  - the 5-7 cap
  - the relative leading/lagging test
  - the two-cycle gaming rule
- A B2C framework is not a B2B framework with different labels - but the design method is the same method.

## Output Shape

The deliverable is an artifact set, presented one artifact at a time for validation:

```
metric-tree.md        : the tree - each node with name, operator, parent math,
                        leading/lagging role relative to its parent
ownership-map.md      : per branch - owner, steward (if split), altitude,
                        review cadence, decision rights of that review tier
guardrail-register.md : per owned metric - its paired counter-metric, the
                        harm it watches for, the two-cycle escalation rule
gating-notes.md       : stage/model gate results - what was struck as
                        premature, what is scheduled to enter and when
definition-stubs.md   : per metric - proposed calculation, method disclosures
                        (NRR method, overage treatment, exclusions), sample
                        window; handed to the data-governance skill to house
```

## Pass Threshold

- Every parent node reconciles as the stated sum, product, or ratio of its children; no orphan metrics float beside the tree.
- Every branch has exactly one named owner; every metric spanning two teams has been re-cut at the handoff, not shared.
- Every owned metric has exactly one paired counter-metric, and the two-cycle escalation rule is written down.
- No altitude's slice exceeds 7 metrics; every level's slice connects to the one below through tree math.
- Every leaf passes the influenceable-this-cycle test; every node's leading/lagging role is stated relative to its parent.
- Every definition stub carries its method disclosures; every benchmark cited carries survey, sample, and year.
- The metric set survives both gates: nothing premature for the stage, nothing borrowed from the wrong business model.

Iterate until all seven hold. If ownership fights stall a branch, ship the framework with that branch's owner marked as an open decision for the named sponsor - never with shared ownership as a compromise.

## Common Failure Modes

Deliberately unranked: each row is one diagnosis with one fix, not competing options. Apply every row that matches.

| Defect                                            | Consequence                                                        | Fix                                                                |
| ------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Single-number worship - one North Star, no inputs | Teams can't act on it; the number gets argued, not moved           | 3-5 input metrics teams own; the tree is the artifact              |
| Tree presented as OKR cascade                     | Goal-setting rigidity practitioners reject; breaks past 1-2 levels | Metrics decompose causally; goals align by negotiation             |
| Jointly-owned metric                              | Diffusion of responsibility; misses produce finger-pointing        | Re-cut at the handoff boundary; one owner per slice                |
| Owned metric with no guardrail                    | Gamed within quarters (coverage up, win rate down)                 | Grove pair per owned metric; two-cycle escalation rule             |
| Vanity metrics admitted                           | Totals and cumulative charts that only go up displace levers       | Admit only metrics with a retention/quality qualifier and a parent |
| 20+ metrics per view                              | Nothing is key; reviews read numbers aloud                         | 5-7 cap per altitude; owners present insight                       |
| Stage-inappropriate metrics                       | Unit-economics theater pre-PMF; vanity growth at scale             | Run the stage gate; strike and schedule                            |
| Blended benchmarks                                | Targets set from incompatible survey definitions                   | One survey per figure, with sample and year                        |
| Fixed leading/lagging labels                      | Metrics misclassified; "leading" dashboard full of lagging numbers | Classify relative to the parent; apply the 4DX test                |

## KPIs

Track whether the framework works, not whether it exists:

- Metric disputes (two dashboards or two functions disagreeing on a headline number) trending to zero after adoption.
- Review cadences held, with decision rights respected per tier - no monthly meeting quietly changing the plan.
- Guardrail escalations actually fired when an owned metric rose against its pair - a framework whose gaming rule never triggers is either a very honest org or an unwatched register.
- Plan variance explained through the tree: when the top metric misses, the review names which branch drove it within one cycle, instead of commissioning an investigation.

## Invocation Examples

- "We're a Series B B2B SaaS. Sales, marketing, and CS each hit their numbers last quarter and revenue still missed. Design a revenue KPI framework that explains and prevents this."
- "Our board sees 14 metrics and our teams track 60. Build the hierarchy: what the board sees, what each function owns, and how they connect."
- "We're a D2C subscription brand moving from growth-at-all-costs to efficiency. Which metrics should each level track now, and what guards against gaming them?"

## Reference

- `mbfinotti/revops-skills@revenue-reporting` - write an executive/board report against this framework; that skill builds one narrative from the metric spine this one designs.
- `mbfinotti/revops-skills@revenue-data-governance-strategy` - define metrics, assign governance, and control definitions; this skill designs the metric set, that one governs its home and change control.
- `mbfinotti/revops-skills@revenue-funnel` - design the funnel model whose conversion metrics feed this tree's new-logo branch; funnel KPIs roll up into this framework.
- `mbfinotti/revops-skills@customer-health-score` - build the health score that can serve as a leading input under this tree's retention branch.
- `mbfinotti/revops-skills@revenue-leakage` - trace where revenue drops out once this framework shows a branch underperforming.
