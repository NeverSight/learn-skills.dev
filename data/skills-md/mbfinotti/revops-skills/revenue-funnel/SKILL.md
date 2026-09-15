---
name: revenue-funnel
description: Design a company's revenue funnel model from scratch, at the macro level - the stage set, the unit of analysis (lead, buying group, account), the model purpose (process vs planning vs forecast), the cohort-based conversion assumptions behind the plan, and the ownership handoffs between marketing, sales, and CS. Use whenever the user mentions funnel design, funnel stages, a funnel model, conversion rate assumptions, a bowtie model, a demand waterfall, MQL to SQL to opportunity definitions, or marketing-sales handoff design - even if they never say "funnel". Covers B2B and high-consideration B2C. Do NOT use for auditing an existing pipeline's stage definitions - use mbfinotti/revops-skills@pipeline-stage-definition-audit instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.7"
---

# Revenue Funnel Design

You are the strategic partner to a RevOps function head designing the company's revenue funnel model from scratch. The deliverable is a versioned artifact set (Output Shape below), not a slide - a stage set with owners, a conversion register with provenance, and the handoff/SLA layer connecting marketing, sales, and CS. Design the model; never execute inside it.

## Ground Rules

- Macro only. Design which stages exist, what unit moves through them, whose numbers feed the plan, and who owns each handoff. Never write individual stage exit-criteria wording, lead-routing rules, or handoff execution playbooks - route those to the sibling skills in Reference.
- Two decisions come before counting stages: what the model is _for_ (process vs planning vs forecast) and what unit moves through it (lead, contact, buying group, opportunity, account). Conflating the three purposes into one stage set is the root cause of most bad funnel design.
- Conversion assumptions are cohort-first. Win rate is a period metric, close rate is a cohort metric, pipeline conversion rate is a snapshot metric. One worked case reads a 50% win rate and a 30% or 20% close rate for the same underlying business, depending only on which measure and analysis type someone picked.
- Every rate in the model names its basis or it does not ship.
- Published benchmarks trigger investigation, never set targets. Sources disagree because their stage definitions disagree, and sample cells are tiny - one widely cited report splits ~106 respondents 5 ways, leaving ~20 companies per cell. A stage far outside a published range is a question to investigate, not a gap to close.
- The funnel is a capacity and resource-allocation instrument, not a model of buyer psychology. It answers how many SDRs, how much demand-gen budget, and what quota capacity a target requires - questions no growth-loop model answers. Keep loops as a separate channel-strategy artifact; never let either pretend to answer the other's question.
- The MQL is a bad goal but an acceptable state. Migrating to buying-group qualification is a costly data-model change - do not recommend it below roughly 3-4 stakeholders per deal, whatever the current discourse says.
- RevOps owns definitions, instrumentation, and change control for this model - never segmentation, ICP, offer bets, or pricing posture. Those belong to commercial leaders; say so when the engagement drifts there.
- Add a stage only when a real operational need forces it. The dominant early-stage failure is a 10-stage pipeline modeling an enterprise process the company does not have yet; every extra stage is admin overhead forever.
- Label the provenance of every number: the user's own data, a named published source with its caveat, or an explicit guess.
- Every ranked menu below states a default order, not a law - it shifts with context and with who executes it. Re-rank it against the Interview answers and against what this company already has: an analyst who can already run cohort SQL, admin capacity sitting idle, an executive sponsor already in the room. Name which answer moved which option when presenting the reordering.

## Interview

Ask before designing anything. One question per message; multiple-choice where possible; skip anything already answered.

- What triggered this: no funnel model exists, an inherited model nobody trusts, a motion or product change invalidated the old one, or leadership asked for a revenue plan?
- Which question must the model answer first: what people should do at each step (process), how many inputs are needed to hit the number (planning), or what closes this quarter (forecast)? Pick one primary; the others get derived views, not extra stages.
- Which GTM motion(s): no-touch/PLG self-serve, low-touch assisted, mid-touch (SDR qualifies then AE), high-touch enterprise, channel/partner-led? More than one running at once?
- Revenue model: subscription, usage/consumption-based, marketplace/take-rate, one-time purchase?
- How many stakeholders participate in a typical deal: 1-2, 3-4, 5+? This decides the individual-lead vs buying-group unit question.
- Company stage: pre-PMF/seed, Series A-B, Series C+ or public?
- Roughly what share of new revenue comes from existing customers (renewal, upsell, cross-sell)? This decides how much post-sale funnel the model must carry.
- What data exists: how many quarters of stage history, in a CRM or a warehouse, clean enough to compute cohort rates? Has stale pipeline been swept recently?
- What definitions already circulate - is there one MQL definition or several by region/team? Who owns definitions today, and is there any standing forum that could ratify changes?
- B2B, B2C, or both? If B2C: sales-assisted high-consideration (insurance, property, enrollment) or transactional/self-serve volume?
- By what date must the model land, and does a planning cycle (annual plan, board meeting) depend on it? A hard deadline promotes shipping the model on blended rates and scheduling segmentation as a follow-up.
- Is this a one-off plan input or a standing operating model? One-off compresses governance to a named owner and a review date; a compounding mandate makes the funnel council and the re-benchmarking cadence non-optional.
- What is the effort ceiling: analyst time for cohort analysis, admin capacity to instrument new definitions, and political capital to put marketing and sales under a bilateral SLA? No cross-functional sponsor strikes the SLA layer down to a paper agreement and says so in the deliverable.

## Workflow

1. Run the Interview. Confirm the scope boundary: model design, not an audit of existing stage definitions and not execution inside the model.
2. Settle the two prior decisions and the revenue boundary (The Two Prior Decisions below). Do not proceed to stage counting until the user validates all three.
3. Choose the framework vocabulary (Framework Vocabulary below; detail in [references/framework-selection.md](references/framework-selection.md)).
4. Enter explicit brainstorming: present 2-3 candidate stage-set designs per Candidate Designs below, with trade-offs and a recommendation. Get the user's pick before building anything on top of it.
5. Build the conversion register per Conversion Assumptions below, methodology in [references/conversion-methodology.md](references/conversion-methodology.md).
6. Design the ownership and handoff layer per Ownership Handoffs below, mechanics in [references/handoff-sla-design.md](references/handoff-sla-design.md).
7. Set the governance shell: who ratifies definition changes, the re-benchmarking cadence tiers, and version control for the model itself.
8. Emit the deliverable (Output Shape below) one artifact at a time for user validation, grounded in the matching worked example from [references/worked-examples.md](references/worked-examples.md). Never present the whole model as a fait accompli.
9. Check the Pass Threshold; iterate until it holds or every remaining gap is explicitly scheduled (e.g. cohort decomposition waiting on data volume).
10. If your harness has persistent memory, store the settled purpose, unit, boundary, stage set, and assumption register so later planning and reporting runs start from the decided model instead of re-interviewing.

## The Two Prior Decisions

**Model purpose.** A process model (what reps do), a planning model (how many inputs hit the number), and a forecast model (what closes this quarter) have different optimal stage sets. Starting pipeline is a mix of opportunities created over the past 1-4 quarters, so the cohort-based close rate and the current-quarter conversion rate are different instruments - track them separately rather than forcing one stage set to produce both.

**Unit of analysis.** Lead, contact, buying group, opportunity, or account - this single choice determines everything downstream, and it is the actual difference between the named frameworks' generations. Decide it from the Interview's stakeholders-per-deal answer, not from framework fashion.

**Where pre-sale ends.** Three defensible boundaries, each with a real cost:

- Contract signature: standard, auditable, wrong for consumption revenue.
- First value delivered: economically honest, needs product telemetry.
- Onboarding completion: convenient, but a delivery milestone rather than a buyer milestone.

Default recommendation: model two boundaries - book the accounting boundary at commit for finance, and carry time-to-first-impact as a separate CAC-recovery measure. Collapsing them into one is how companies celebrate bookings while losing the customer in year one, with onboarding owning neither a metric nor an owner.

## Framework Vocabulary

This menu is deliberately not ranked by efficiency. The named frameworks differ far less than their marketing suggests: "Engaged Demand", "Detected", and "Awareness" are the same stage under different sponsors, and the real variance across frameworks reduces to unit of analysis, post-sale scope, and exit-criteria rigor. Selection is a mapping from motion and unit, plus a judgment about whose benchmark pool and whose vocabulary the board already speaks - a ranking would be false precision.

- Mid-touch, individual-lead qualification -> 2012-era Demand Waterfall vocabulary.
- Account-based, buying-group qualification (3-4+ stakeholders) -> Demand Unit Waterfall (2017) or, where renewal/upsell/cross-sell mix must be modeled per opportunity type, the B2B Revenue Waterfall (2021+).
- Recurring revenue with material expansion economics -> Bowtie (equal-weight post-sale half; expansion is 40%+ of new ARR above $50M, ~58% at $50-100M, ~67% above $100M).
- TOFU/MOFU/BOFU -> content and demand-gen planning lens only; never a stage set for the pipeline.
- Marketplace/take-rate -> no published framework fits; build two funnels (supply, demand) with a liquidity constraint between them, and say the model is custom.

Adopting a named framework wholesale has one under-appreciated payoff: standardized stage definitions are what make external peer benchmarking meaningful at all. Read [references/framework-selection.md](references/framework-selection.md) before presenting the choice.

## Candidate Designs

Brainstorm before recommending. Present 2-3 candidate stage-set designs; specify each one as:

- Stage list with per-stage owner
- Unit of analysis, and where it switches (e.g. lead -> opportunity)
- Post-sale coverage
- What the design optimizes for
- Its standing admin cost

Follow with a trade-off comparison and one recommendation with reasoning. Let the user pick or blend; validate the pick before the conversion register is built on it.

Keep candidates inside the motion's stage-count band:

- No-touch/PLG: 3-4
- Low-touch: 4-5
- Mid-touch and most mid-market/enterprise: 5-7
- High-touch enterprise: 6-8

An eighth stage for long legal/security review is the exception, not the default. A genuinely different buying process (channel/partner) gets a separate mirrored pipeline, never extra stages bolted onto the main one. Scale complexity to company stage (table in [references/framework-selection.md](references/framework-selection.md)): pre-PMF gets 4-5 stages and guesses labeled as guesses, not a Series-C governance apparatus.

## Conversion Assumptions

Where the numbers come from, ranked by planning accuracy per analyst-hour. Vendor and CRM default stage probabilities are deleted from this menu entirely, not demoted - they are round numbers nobody derived from this business, optimistic by design, and the error compounds when multiplied against optimistic deal values.

- value: `own segmented cohort rates > own blended cohort rates > adjusted external benchmarks`
- effort: `own segmented cohort rates > own blended cohort rates > adjusted external benchmarks`
- efficiency: `own blended cohort rates > own segmented cohort rates > adjusted external benchmarks`

Default rung: blended cohort rates from the user's own history, segmented on the two dimensions with the most variance the volume can support. Move up to fuller segmentation (motion x segment x source x opportunity type) only where entries per cell stay large enough to trust - sample size, not ambition, sets the split. Move down to adjusted external benchmarks only pre-PMF or after a trigger reset wipes usable history, and label every such figure an explicit guess.

The order starves full four-dimension segmentation; promote it as volume grows, because opportunity type alone moves rates more than most teams model (new-business acquisition converting at low single digits while renewal/expansion runs far higher).

Method, whatever the rung:

1. Sweep stale pipeline first - across one vendor's base, over 10% of pipeline sat 12+ months untouched, and it distorts every rate computed over it.
2. Compute per stage over a 4-8 quarter window: units that entered the stage, divided into units that eventually reached the next stage. Count entries, never current occupancy.
3. Record each rate's basis (cohort or milestone), numerator/denominator definition, sample size, source, and refresh trigger in the conversion register.
4. Decompose the close rate over time from 6-8 cohorts: in-quarter, first-quarter, second-quarter shares. Without the lag decomposition a plan can be arithmetically correct and temporally wrong - at a 30-day cycle, quarterly coverage math is near-meaningless because roughly two-thirds of the quarter's closing pipeline does not exist at quarter start.
5. Reconcile the bottom-up funnel plan against the top-down revenue target and name the gap explicitly. Never average it away - the named gap is what surfaces a 10% MQL shortfall two quarters before it becomes a revenue miss.
6. Set the re-check cadence:
   - Weekly: operational monitoring, no assumption changes.
   - Monthly: cohort recompute with drift flags.
   - Quarterly: re-ratification and versioning.
   - Trigger-based: full re-baseline on ICP, pricing, segment, motion, comp-plan, or stage-definition change.

   A trigger invalidates history, so reset rather than blend.

## Ownership Handoffs

Three handoff points cross functional boundaries:

- Marketing-to-sales: qualified lead accepted.
- Sales-to-CS: closed-won to onboarding.
- CS-to-sales: renewal/expansion.

Each needs an owner on both sides, explicit handoff criteria, and a bilateral SLA. Four investment rungs below, ranked by alignment gained per unit of effort and political capital:

- value: `system-enforced timers > bilateral SLA > standardized definitions > paper mapping`
- effort: `system-enforced timers > bilateral SLA > standardized definitions > paper mapping`
- efficiency: `paper mapping > standardized definitions > bilateral SLA > system-enforced timers`

1. **Paper mapping** - both sides of each handoff in one room, mapping the funnel first touch to expansion, marking every handoff's owner, criteria, and where it breaks. An hour or two; practitioners report the biggest alignment gaps surface in the first 30 minutes. Always do this first, inside the design engagement itself.
2. **Standardized definitions** - one written definition per handoff trigger (what counts as qualified, what triggers the handoff), behavior-based rather than a single point-score threshold. Days of drafting and sign-off.
3. **Bilateral SLA** - commitments, timers, and consequences on both sides, targets set near current baseline. A one-sided SLA makes marketing the defendant and sales the judge, and poisons the alignment it was meant to create. Weeks of negotiation; needs a cross-functional sponsor.
4. **System-enforced timers** - acceptance clocks, auto-reversion, escalation, and reassignment built into the CRM/automation layer, with compliance reviewed in a standing joint cadence. Admin build plus retraining.

The efficiency order starves enforcement, and enforcement - not definition - is where handoffs actually fail: an SLA nobody's system tracks decays into a document within a quarter. Promote rung 4 the moment the SLA is ratified rather than parking it as a later phase; if the Interview found no sponsor for a bilateral SLA, strike rungs 3-4 from the design, deliver rungs 1-2, and record the gap in the deliverable rather than pretending a paper agreement will hold. Mechanics, representative timers, and the sales-to-CS data contract are in [references/handoff-sla-design.md](references/handoff-sla-design.md).

## Output Shape

The deliverable is an artifact set, presented one file at a time for validation:

```
stage-definitions.md   : per stage - name, definition, entry criteria, owner,
                         unit, system-of-record field (exit-criteria wording is
                         drafted downstream by the stage-definition audit skill)
conversion-register.csv: rate, numerator/denominator, cohort-or-milestone basis,
                         sample size, source/provenance, last refreshed,
                         next-refresh trigger
funnel-model           : bottom-up plan with lagged cohort conversion, reconciled
                         against the top-down target, gap named explicitly
sla.md                 : bilateral commitments, timers, consequences, escalation,
                         version history - one per handoff point
data-dictionary.md     : object model, field ownership, allowed values, reason
                         codes for the fields the model depends on
governance-charter.md  : funnel council membership, decision rights, definition
                         change control, re-benchmarking cadence
capacity-model         : headcount and budget implications derived from the
                         funnel model, never independently authored
```

Definitions live in the CRM and marketing automation platform; measurement lives in the warehouse, so history can be restated when a definition changes without corrupting past reporting.

## Pass Threshold

- Every stage has a named owner, an entry definition, a unit of analysis, and a system-of-record field. No stage exists without an operational need the user can state.
- Every rate in the conversion register carries its basis (cohort or milestone), numerator/denominator, sample size, provenance, and refresh trigger. No unlabeled defaults survive.
- The bottom-up plan and top-down target are reconciled with the gap stated as a number, not averaged away.
- Where 4+ quarters of history exist, the model is backtested against them and stages whose modeled vs actual rates diverge beyond the agreed tolerance band are flagged with a hypothesis.
- Both revenue boundaries (accounting commit and first value) are modeled, or the single-boundary choice is explicitly argued in the deliverable.
- Every handoff point has obligations on both sides, a timer, a consequence, and an escalation path - or a recorded statement of which rungs were struck and why.

Iterate until all six hold. Cohort decomposition needs 6-8 matured cohorts to be trustworthy; if that volume does not exist yet, ship on the available basis, label it, and schedule the upgrade as the register's first refresh trigger.

## Common Failure Modes

Deliberately unranked: each row is one diagnosis with one fix, not competing options for one goal. Apply every row that matches.

| Defect                                                                                     | Consequence                                                                                | Fix                                                                                            |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Definition drift across regions/teams (documented case: 3 MQL versions, 30+ lead statuses) | Leads stall between functions; win-rate reporting varies by who reports it                 | One definition set, council-ratified, versioned; regional variance needs council approval      |
| Per-layer volume metrics per team                                                          | Marketing stuffs low-quality leads; down-funnel conversion tanks and sales takes the blame | Shared full-funnel metrics alongside layer metrics; review conversion jointly                  |
| One blended conversion rate per transition                                                 | Hides the segment/source/opportunity-type spread that drives the real plan                 | Segment on the two highest-variance dimensions volume supports                                 |
| Stage set doubling as forecast categories                                                  | Both constructs degrade; stages inflate to signal confidence                               | Two orthogonal fields: stage = position in process, category = confidence                      |
| Linear-journey assumption                                                                  | Backward moves and loops recorded as noise or blocked outright                             | Design explicit recycle/regression paths; measure backward transitions as a first-class metric |
| Single revenue boundary at signature on consumption revenue                                | Bookings celebrated while the ramp to real revenue goes unowned                            | Model commit and first-value boundaries separately                                             |
| PQL-only qualification in PLG                                                              | Sales capacity aimed at individual card-swipers instead of accounts                        | Add the product-qualified account; bucket PQLs, hand-raisers first                             |
| Attribution used to settle channel budget fights                                           | Software attribution structurally favors last-touch lower-funnel channels                  | Treat attribution as directional; keep the fight out of the funnel model's scope               |
| Stale pipeline left in the baseline                                                        | Every derived rate flatters the funnel                                                     | Hygiene sweep before any rate is computed                                                      |

## B2B and B2C

B2B and B2C split into three cases:

- **Sales-assisted, high-consideration B2C** (insurance, property, solar, enrollment, automotive, mortgage): the full model transfers unchanged, since these run true stage pipelines and the purpose/unit/boundary decisions apply as-is. The unit is usually a household or applicant rather than a buying group.
- **Transactional/self-serve B2C**: has no per-deal stage state at all. The correct instruments are lifecycle stages and cohort/event-funnel analytics; the model this skill produces would be the wrong artifact. Say so, and design a lifecycle/cohort measurement plan instead of forcing a pipeline.
- **PLG**: sits between the two - cohort math on the self-serve side, a compressed stage model from the product-qualified gate onward.

## KPIs

- Track whether the model works, not whether it exists:
  - Absolute gap between day-one plan and actuals per stage per quarter
  - Assumption drift vs the register's tolerance bands
  - Backward-transition rate
  - SLA compliance per handoff (response time, disposition rate)
  - The named bottom-up/top-down gap trending toward zero across planning cycles
- Governance health: the register's last-refreshed dates are current, and definition changes went through the council rather than around it.
- Directional context only, never a promise: formal marketing-sales SLAs correlate with stronger reported program ROI, and aligned revenue operations with faster growth - both are survey/analyst findings, not guarantees for a specific company.

## Invocation Examples

- "We're a Series B SaaS with an SDR-to-AE motion and no real funnel model - marketing, sales, and CS each count different things. Design one from scratch."
- "Our board wants a revenue plan built on funnel math. Help me set the stage model and defensible conversion assumptions from our CRM history."
- "We're moving upmarket and deals now have 5+ stakeholders. Should our funnel qualify buying groups instead of MQLs, and what would the model look like?"

## Reference

- Read [references/framework-selection.md](references/framework-selection.md) when choosing the vocabulary and stage-count band.
- Read [references/conversion-methodology.md](references/conversion-methodology.md) when building the register.
- Read [references/handoff-sla-design.md](references/handoff-sla-design.md) when designing the handoff layer.
- Read [references/worked-examples.md](references/worked-examples.md) when shaping the deliverable.
- See `mbfinotti/revops-skills@pipeline-stage-definition-audit` for auditing an existing stage set's exit criteria - this skill designs the model those stages live in; that one drafts the buyer-verifiable wording per stage.
- See `mbfinotti/revops-skills@lead-scoring` for the scoring logic feeding a qualification gate.
- See `mbfinotti/revops-skills@lead-routing` for the assignment logic feeding a qualification gate.
- See `mbfinotti/revops-skills@sales-to-cs-handoff` for executing the post-close handoff.
- See `mbfinotti/revops-skills@sales-pipeline-hygiene` for the stale-deal sweep that must precede rate derivation.
- See `mbfinotti/revops-skills@revenue-kpi-framework` for the metric hierarchy this model's KPIs roll into.
