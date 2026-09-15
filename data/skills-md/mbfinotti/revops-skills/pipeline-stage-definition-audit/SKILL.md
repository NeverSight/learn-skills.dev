---
name: pipeline-stage-definition-audit
description: Audit existing sales pipeline stage definitions against buyer-verifiable milestones and flag the ones built on rep activity instead. Core test - does each stage exit criterion name something the buyer did, said, or agreed to, checkable by two managers independently? Adds stage aging, conversion decay, stage-skip rate, and close-date push diagnostics. Use whenever the user mentions stage definitions, stage exit criteria, stage inflation, stages named after rep activity ("demo scheduled", "proposal sent"), "our stages don't mean anything", or "why is everything stuck in one stage" - even if they never say "audit". Covers enterprise and high-velocity pipelines, B2B and B2C. Do NOT use for designing a funnel stage set from scratch - use mbfinotti/revops-skills@revenue-funnel instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.10"
---

# Stage Definition Audit

Evaluate whether an existing pipeline's stage definitions reflect buyer-verifiable milestones - things the buyer did, said, or agreed to - rather than internal rep activity, and deliver a severity-ranked findings report with rewritten exit criteria and a safe migration plan.

Reference frameworks:

- **Gartner's six B2B buying jobs** (buyer-side reference structure): Problem Identification, Solution Exploration, Requirements Building, Supplier Selection, Validation, Consensus Creation.
- **GitLab's public commercial sales handbook** (real-world exemplar of a published stage-definition document): definition, who's involved, activities, system enforcement, exit criteria, cross-links.
- **MEDDPICC-style gating**: each exit-criterion element scored red/yellow/green, all-green to advance.
- **Winning by Design's SPICED** (buyer-side diagnostic lens): its elements are confirmed with the buyer, not assumed by the rep.

## Ground Rules

- Audit, never redesign. The existing stage set is the input. If the funnel model itself is the defect, say so and route to the funnel-design see-also (Reference) instead of rebuilding it here.
- Label every threshold with its provenance: published company practice, practitioner consensus, or derived from the user's own data. Never present a vendor heuristic as an industry constant.
- Warn off the circulating forecast statistics ("93% of teams can't predict revenue within 5%", "85% of B2B companies miss forecast", "CRM data is only 40-60% accurate") - each circulates unattributed and must never be stated as fact. Cite the mechanism instead: when advancement is subjective, two reps stage identical deals differently, which corrupts stage conversion data and everything built on it.
- The stage records the buyer's position, never a qualification scorecard. There are no "MEDDIC stages 1-6" (Force Management's warning): each qualification dimension is its own continuously-updated field; conflating the scorecard with the stage picklist breaks both.
- Classify the pipeline type (below) before judging any stage. A transaction pipeline judged by deal-pipeline expectations produces false findings.
- Never rename or delete an existing stage value. In most CRMs, stage history is immutable and historical records reference old values forever - renaming or deleting corrupts before/after reporting permanently. Deactivate the old value and add a new one. After any change, re-check the forecast-category mapping for every stage.
- 5-7 stages with 2-4 exit criteria each is the practitioner-consensus band, not a law. A stage earns its place by having a distinct purpose; if nothing changes in it, cut it.

## Pipeline Types

Establish the pipeline's type before judging a single stage - the three types come from The RevOps Show (Doug Davidoff and Jess Cardenas):

- **Development pipeline** - moves an account from no intent to intent. Stages track buyer interest signals, not deal mechanics.
- **Deal pipeline** - intent to decision. The classic enterprise B2B model this audit's examples assume by default.
- **Transaction pipeline** - high-velocity, lower-value, friction-reduction focus. Fewer stages, lighter criteria, often automated progression signals.

High-velocity, self-serve, PLG, and B2C teams frequently run no rep-owned pipeline at all: they run buyer-facing lifecycle/funnel stages owned by marketing or growth. A true pipeline construct reappears only when the motion goes sales-assisted or upmarket, and then funnel and pipeline must coexist as distinct reporting constructs, never merged into one stage list.

- **Identical across B2B and B2C:** the verifiability test itself, the stage-aging and conversion diagnostics, and the deactivate-don't-rename migration rule.
- **Divergent across B2B and B2C:** stage count, evidence type (product events and payment signals versus signed documents and security reviews), and ownership.

Named-practitioner literature on B2C stage definition is thin, so the three-pipeline-type framing is the best available anchor; derive the rest from the user's own data and say so.

## Interview

Ask before judging anything. One question per message; multiple-choice where possible; skip anything already answered.

- Paste the current stage list with each stage's written definition, exactly as documented. If definitions live only in people's heads, say so - that is itself a finding.
- Which motion feeds this pipeline: enterprise sales-led, mid-market, high-velocity inside sales, PLG sales-assisted? One pipeline or several, and do multiple motions share one?
- ACV band and typical cycle length?
- What symptoms triggered this audit: deals stuck in one stage, forecast misses, managers disagreeing on staging, stage skipping, silent close-date pushes?
- What is the forecast-category mapping per stage?
- Which required fields, validation rules, and automations are keyed to stage values?
- What data can be exported or queried: stage-change history, closed-won/lost records, close-date change history, per-rep breakdowns?
- Who owns stage definitions and who approves changes (RevOps, sales leadership, finance)?
- Are two people available to score the same deals independently - two managers, or any two reviewers who can judge a deal record without conferring? The Pass Threshold's inter-rater check needs them. If only one reviewer exists, say so now: the check becomes an automated-event spot audit against machine-recorded criteria, and the deliverable must state that substitution rather than claim an agreement rate it never measured.
- When were stages last changed, and how did that rollout go?
- Can you provide samples: 20-30 recent closed deals and the open deals currently sitting in each stage?
- By what date must the result land, and does that date fall inside a live quarter? A stage change corrupts the quarter it lands in, so a mid-quarter deadline strikes every migration rung in Remediation Order and leaves criterion rewrites only.
- Do you want a one-off correction before a specific forecast, or a definition set that holds every quarter? One-off promotes the criterion rewrite alone; a compounding mandate promotes the evidence plumbing and makes the standing inspection non-optional.
- What is the effort ceiling: is a CRM admin available, how many reps must be retrained, and can the pipeline's trend series afford to restart at a cutover date? No admin strikes the evidence-plumbing rung; no tolerance for a trend break strikes the stage cut and the stage add.

## Workflow

1. Run the Interview; classify the pipeline type and confirm the scope boundary (audit, not redesign).
2. Gather artifacts and run stakeholder interviews per [references/audit-intake.md](references/audit-intake.md). Look at the data before talking to anyone.
3. Apply the verifiability test from [references/verifiability-test.md](references/verifiability-test.md) to every stage: the exit criterion must name something the buyer did, said, or agreed to; be observable independently of the rep's opinion; and be recorded somewhere checkable. Operational form: could two managers, looking at the same deal record, independently reach the same verdict on whether the criterion is met?
4. Map each stage to a Gartner buying job (table in the same reference). Flag stages that map to no job (rep activity in disguise) and multiple stages crowding one job (redundant stages).
5. Compute the diagnostics in [references/diagnostic-metrics.md](references/diagnostic-metrics.md) where the pipeline's data can be queried directly; otherwise derive what the deal samples and interviews support, and mark each unmeasured diagnostic as such.
6. Record every defect as a finding with this schema: **Stage | Current exit criterion | Verdict + why | Severity | Fix rung + effort | Evidence | Buying job mapped | Proposed criterion | Migration note**. Severity scale:
   - **Critical** - exit criterion is pure rep activity or undocumented; advancement is opinion.
   - **High** - criterion references the buyer but is unverifiable or recorded nowhere checkable.
   - **Medium** - verifiable but ambiguous; two managers could plausibly disagree.
   - **Low** - criterion sound; defect is naming, ordering, or redundancy.

   Severity is the value axis of a finding, never its queue position. A Critical defect fixed by one wording change ships before a Medium one that needs a picklist migration. Tag each finding with the rung it lands on and that rung's effort order of magnitude, then order the list by Remediation Order below.

7. Draft rewritten exit criteria for every failing stage (wording guidance in the verifiability reference), then build the remediation and rollout plan from [references/remediation-rollout.md](references/remediation-rollout.md) - fixes sequenced by Remediation Order, deactivate-and-add migration, forecast-category re-mapping, automation audit, training and rollout shape.
8. Emit the report (Output Shape below) one section at a time for user validation; ground it in the matching worked example from [references/worked-examples.md](references/worked-examples.md).
9. Check the Pass Threshold; iterate the criteria and plan until it holds or the remaining gaps are explicitly scheduled (e.g. metrics that need a full sales cycle of new data).
10. If your harness has persistent memory, store the stage inventory, per-stage verdicts, and agreed thresholds so the post-rollout re-check starts from them instead of re-interviewing.

## Remediation Order

Six fix types, ordered by forecast accuracy recovered per unit of effort - never by severity, and never cheapest-first. Effort here is admin configuration, retraining every rep who works the stage, historical data migration, and reversibility. Reversibility dominates this list: a stage definition changed twice in a quarter destroys the trend data the definitions exist to produce, so any fix that touches a stage value is close to one-way.

- value (accuracy recovered, most first): `full redefinition > criterion rewrite > evidence plumbing > stage add == stage cut > standing inspection`
- effort (most first): `full redefinition > stage add > stage cut > evidence plumbing > standing inspection > criterion rewrite`
- efficiency (best first): `criterion rewrite > standing inspection > evidence plumbing > stage cut > stage add > full redefinition`

`stage add == stage cut` on value: pipeline type decides which one wins, and nothing else does.

- **Deal pipeline:** recovers more from the add, since enterprise deals die in Validation and Consensus Creation, the jobs most often left uncovered.
- **Transaction pipeline:** recovers more from the cut, since friction removal is that motion's design goal, and a stage deals skip is a stage that converts better skipped.

They do not tie on effort: the migration is identical, and only the add asks reps for evidence they have never been asked to produce.

1. **Criterion rewrite** - restate a failing exit criterion as a buyer act pointing at a field or artifact the system already holds. No picklist change, no migration, no forecast re-map. Near-zero to an hour per stage, plus one walkthrough in the review meeting that already happens; the old wording is a document edit away. Retires most Critical and High findings on its own.
2. **Standing inspection** - exit criteria on the recurring pipeline-review agenda, plus a quarterly inter-rater re-sample. An hour a quarter, forever. Recovers no accuracy by itself, and earns its rank by being the only rung that stops every rung above it drifting back to opinion within two quarters.
3. **Evidence plumbing** - create the required field, validation rule, or evidence link a rewritten criterion names but the system does not capture. A week of admin configuration plus retraining every rep who touches that stage. Reversible in configuration, never in retraining. This is what turns a criterion that passes review into one that holds in production.
4. **Stage cut or merge** - deactivate-and-add a stage that maps to no buying job or duplicates its neighbor. A week to a quarter: open-deal moves, forecast-category re-map, and the stage-keyed automation inventory. Breaks the trend series at cutover, and reversing it breaks it a second time.
5. **Stage add** - a new stage for a buying job nothing covers. The same migration as the cut, plus a behavior reps have never been asked for and managers have never inspected. A quarter.
6. **Full redefinition** - the stage set rebuilt as a coherent series rather than patched cell by cell. Out of scope here by Ground Rules; route it rather than attempting it.

Default rung: run every criterion rewrite in one pass, then schedule the standing inspection. Take on the next rung down only when a rewritten criterion names evidence the system does not capture - there the plumbing is not a later phase, it is what makes the rewrite true.

What this order starves is the full redefinition. It ranks first on value: the only fix that treats the stage set as a series instead of a list of separately worded cells. It ranks last on the ratio in every engagement, so a severity-and-effort ranking defers it indefinitely, and the pipeline accumulates well-written criteria on a stage model that cannot carry them.

Promote it, and route out of this skill to `mbfinotti/revops-skills@revenue-funnel`, when:

- Fewer than two stages survive the audit as usable anchors.
- Multiple motions share one stage list.
- The pipeline type itself is misclassified.

Delete a ruled-out rung rather than demoting it: a rung parked at the bottom of the plan returns later as scope nobody budgeted.

- **No approver for a stage-definition change** (per the Interview): strike the cut and the add from the plan, and say they are struck. A migration with no approver ships never.
- **No CRM admin available:** strike the evidence plumbing the same way.

The order is a default, not a law: it shifts with context and with who executes it. Re-rank it against the Interview's answers.

- **CRM admin on hand:** collapses the plumbing rung from a week to an hour and moves it above the standing inspection.
- **Sales team mid-quarter:** strikes every migration rung until the quarter closes, because a stage change corrupts the quarter it lands in.
- **Pipeline small enough to re-stage by hand:** drops the cut and add rungs by an order of magnitude and promotes both above the plumbing.

## Output Shape

Every threshold line carries a provenance tag.

```
STAGE DEFINITION AUDIT - <pipeline>, <date>
Pipeline type    : development / deal / transaction + motion, ACV band, cycle length
Stage inventory  : count vs 5-7 consensus band; definitions documented or tribal;
                   forecast-category map present/absent
Per-stage verdict: stage -> exit criterion -> pass/fail verifiability -> severity
Buying-job map   : which Gartner job each stage covers; jobs with no stage; jobs
                   with several stages
Diagnostics      : conversion decay shape, aging outliers, skip/backward rate,
                   close-date push counts, per-rep variance (provenance-tagged)
Findings         : records ordered by Remediation Order, severity carried per
                   record as its value axis (schema in Workflow step 6)
Remediation      : rewritten exit criteria, rungs chosen and rungs struck with the
                   constraint that struck them, deactivate-and-add migration plan,
                   forecast-category re-map, automation/dashboard checklist,
                   training + rollout shape
Measurement      : baseline values captured, post-change KPIs, re-check date
                   (>= one full sales cycle out)
```

## Pass Threshold

- Every stage has at least one exit criterion that names a buyer action and is attached to a checkable field or artifact in the system of record.
- Inter-rater check: two managers (or two independent reviewers) score a sample of 10-20 open deals against the rewritten criteria without conferring. Verdicts must agree on at least 90% of deals - a working bar to derive tighter from the user's own data, not a published standard. Disagreements point at the ambiguous criterion; rewrite it and re-sample.
- Stage-to-stage conversion decays monotonically across the funnel, or every exception is explained by deliberate design (e.g. a verification stage meant to disqualify).
- No open-pipeline stage holds a share of deals wildly out of line with its expected dwell time - derive the expected distribution from the pipeline's own history rather than an industry constant.

Iterate until all four hold. Conversion and distribution checks need a full sales cycle of deals under the new definitions before they are trustworthy - if that data does not exist yet, say so in the deliverable and schedule the re-check as the first post-rollout gate.

## Common Failure Modes

Deliberately unranked: each row is one diagnosis with one fix, not a menu of competing fixes for one problem, so an efficiency order over them would rank the reader's symptoms rather than their options. Apply every row that matches.

| Defect                                             | Consequence                                                            | Fix                                                                        |
| -------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Renaming or deleting stage values in place         | Historical reporting corrupted permanently; automations silently break | Deactivate old values, add new ones; bridge with a mapping field           |
| Skipping the forecast-category re-map              | Forecast rollups silently skew while stage names look right            | Re-check the mapping for every stage after any change                      |
| Qualification scorecard baked into the picklist    | Stage stops tracking buyer position; both constructs degrade           | Separate continuously-updated qualification fields; stage = buyer position |
| Criteria written as rep activities                 | Stage inflation; advancement on optimism                               | Rewrite every criterion to start with a buyer action                       |
| Criterion verifiable on paper, recorded nowhere    | Passes the audit, unenforceable in practice                            | Attach each criterion to a required field or evidence link                 |
| Transaction pipeline judged by deal-pipeline rules | False findings; friction added to a motion built on removing it        | Classify pipeline type first; weight criteria to the motion                |
| More than ~7 stages or look-alike stages           | Adjacent stages indistinguishable; criteria diluted                    | Merge; every stage needs a distinct purpose (practitioner consensus)       |
| Success measured by logging/compliance rate        | Reps log more, faster, worse; data no better                           | Measure conversion stability and inter-rater agreement instead             |
| Judging the fix in week two                        | Conversion metrics meaningless without a full cycle of new deals       | Wait at least one sales cycle; use 30/60/90-day adoption checkpoints       |
| Rolling out criteria reps first see live           | Ignored criteria; stage data quality unchanged                         | Train first; build exit criteria into the recurring pipeline review        |

## KPIs

- Track: stage-to-stage conversion stability and monotonic decay, per-rep conversion variance (the sharpest single indicator of subjective definitions), median time-in-stage and outlier count, stage-skip and backward-move rate, close-date push count per deal, inter-rater agreement on periodic deal samples, and forecast accuracy measured as the absolute % difference between the day-one forecast and the period's final result, at least quarterly.
- Never report adoption or logging-compliance rates as success - they measure pressure, not accuracy.
- Re-run the inter-rater sample each quarter; a decaying agreement rate means criteria are drifting back to opinion.

## Invocation Examples

- "Our stages are 'Demo Scheduled', 'Proposal Sent', 'Verbal Commit', and every deal sits in Proposal Sent for months. Audit our stage definitions."
- "Two of my managers can't agree on whether the same deal belongs in stage 3. Review our exit criteria and tell me which stages are rep activity in disguise."
- "We're PLG going upmarket and sales-assisted deals now share a pipeline with self-serve signups. Audit whether our stages mean anything before we forecast off them."

## Reference

- [references/verifiability-test.md](references/verifiability-test.md) - the test, passing and failing wording, the Gartner buying-job mapping table, and a negative example.
- [references/diagnostic-metrics.md](references/diagnostic-metrics.md) - how to compute each metric, its red-flag pattern, and its provenance.
- [references/audit-intake.md](references/audit-intake.md) - the artifact checklist, interview guides, and ownership map.
- [references/remediation-rollout.md](references/remediation-rollout.md) - migration mechanics, cutover and comparability, training, and the optional vendor-specific integration note.
- [references/worked-examples.md](references/worked-examples.md) - one enterprise audit, one high-velocity audit, and one audit done wrong.
- `mbfinotti/revops-skills@sales-forecast-diagnostic` - overall forecast reliability
- `mbfinotti/revops-skills@sales-pipeline-hygiene` - recurring stale-deal sweep and hygiene cadence
- `mbfinotti/revops-skills@crm-data-governance` - field dictionary and picklist governance
- `mbfinotti/revops-skills@revenue-leakage` - tracing revenue lost between stages
