---
name: revenue-reporting
description: Define the metric set and narrative structure for an executive or board revenue report so it tells one coherent story - a small stable metric spine, locked definitions, an answer-first narrative around plan vs actual vs forecast, presenting a miss without surprising the board, the reconciliation and sign-off chain, and weekly vs monthly vs quarterly cadences. Use whenever the user mentions a board revenue report, exec deck metrics, the QBR revenue section, a monthly revenue review, an investor update, or a board deck that reads as a data dump - even if they never say "reporting". Covers B2B subscription, B2C, transactional, usage-based, and PLG. Do NOT use for designing the org-level KPI hierarchy - use mbfinotti/revops-skills@revenue-kpi-framework instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.1"
---

# Revenue Reporting

Build the executive or board revenue report as one coherent story: a small, stable metric spine wrapped in an answer-first narrative organized around plan vs. actual vs. forecast. The hard part is rarely the arithmetic - it is agreeing on definitions, reconciling the CRM record against the finance record, and making sure the board never learns bad news live.

Scope boundary, stated up front:

**In scope:**

- What goes in the report and how it reads.
- The number and its confidence.

**Out of scope:**

- Building a dashboard in any specific BI tool.
- Designing the org-level KPI framework (which metrics matter at which org level and how they roll up) - a separate strategy exercise outside this repository.
- Investigating why a forecast was wrong - hand that to `mbfinotti/revops-skills@sales-forecast-diagnostic`, then use this skill to turn the finished diagnosis into the board narrative.

## Interview

Ask before proposing anything. One question per message; offer multiple-choice options when possible. Skip anything already answered.

- What is the business model - B2B contract subscription, usage/consumption-based, PLG/self-serve, B2C/transactional/marketplace, or mixed?
- Which artifact is being built - quarterly board deck, monthly executive review, weekly revenue review, an investor update, or the whole cadence stack?
- What stage is the company - pre-institutional, early venture, growth, or late? (The spine tightens and shifts with stage.)
- What exists today - nothing, an ad-hoc deck rebuilt each period, or a recurring report people have stopped trusting?
- Do written metric definitions exist anywhere, and do any two dashboards currently disagree on a spine metric (recurring revenue, retention, coverage)?
- Who produces the numbers today - RevOps/ops, finance, a founder - and does finance certify them before they ship?
- What is this period's story - on plan, a miss, a beat, or unknown until reconciliation?
- Which data is reachable - CRM/pipeline record, billing system, general ledger, product usage events?
- By when must this land - the next board meeting, this month's close, or no fixed date?
- One-off artifact, or a recurring asset rebuilt every period from here on?
- What is the effort ceiling - analyst hours per period, whether finance will reconcile on request, and whether a warehouse or semantic layer already models revenue?

The last three questions set the spine ranking before any metric is chosen:

- **Deadline inside the finance close**: drops every metric needing certification (payback, growth-plus-margin, the three-basis lines) out of this cycle.
- **Compounding mandate**: builds the recurring-revenue waterfall and the dictionary first despite their cost, since every later period reuses them.
- **One-off artifact**: skips both and reports the bridge from a billing export.
- **Low effort ceiling**: caps the spine at five single-system metrics.
- **Existing revenue model in the warehouse**: promotes every cohort metric to the top of the order.

## Workflow

1. Run the Interview; fix the artifact, audience, model, and cadence before touching metrics.
2. Choose the metric spine: five to six core metrics, eight at the absolute cap. Rank candidates by decisions changed per unit of production cost - analyst hours, data the systems already emit, reconciliation burden against finance, how often it must be rebuilt - never by how standard the metric looks. Default B2B order, highest ratio first: pipeline coverage > win rate > recurring-revenue waterfall > retention pair > attainment distribution > growth-plus-margin > acquisition payback > bookings/billings/recognized lines. It is a default, not a law: re-rank it against the Interview answers and against everything else already known about the user, and delete a metric their data rules out rather than ranking it last. Full axes, justified ties, per-model orders, stage deletions and the durability metrics this order starves are in [references/metric-spine.md](references/metric-spine.md). The same spine repeats every period so trends stay visible; a metric enters only by replacing one, with the swap footnoted.
3. Lock definitions: write a dictionary entry for every spine metric - formula, inclusions/exclusions, source of truth, owner, window, and every contested rule resolved in writing (entry shape and worked example in [references/metric-dictionary-entry.md](references/metric-dictionary-entry.md)). Field ownership and source-of-truth rules come from `mbfinotti/revops-skills@crm-data-governance` - reference them, do not redefine them here. Freeze the dictionary before drafting; definition changes mid-cycle are what make numbers move between meetings.
4. Reconcile before narrating: the CRM read (bookings, pipeline) and the finance read (billed, recognized) diverge by design and only tie at the contract level over the full term - the check is that billings minus recognized revenue equals the change in deferred revenue, and that the headline number matches what finance will certify. When the harness can execute code, script the bridge and the reconciliation from a two-file export (billing/GL revenue by account, CRM bookings by deal); otherwise request the finance-certified totals and reconcile by hand. Never ship a number finance has not seen.
5. Build the plan-vs-actual-vs-forecast table for every spine metric - the three columns every discussion hangs from. Show movement bridges (beginning, additions, losses, ending) rather than netted deltas, and distributions rather than averages wherever a distribution exists (attainment, deal size, cohort curves).
6. Write the narrative answer-first: verdict, cause, response, ask - on the first page. Structure per the Narrative section below; worked report, and a good-vs-bad opening, in [references/worked-report-example.md](references/worked-report-example.md).
7. If the period is a miss, follow the Presenting-a-miss section: quantify it, state the cause at the confidence actually held, name the fix and its proof metric. Root-cause depth belongs to `mbfinotti/revops-skills@sales-forecast-diagnostic`, not to this report.
8. Assemble to cadence (see Cadence): short main body, everything backward-looking and detailed in the appendix, deck shipped as a pre-read days before the meeting. Optionally pass the narrative prose through a humanizer skill before sign-off.
9. Run the sign-off chain:
   - RevOps publishes to a deadline.
   - Finance certifies against the ledger.
   - Each functional leader validates their section.
   - CEO/CFO approve.
   - The pre-read ships three to four days ahead.
   - Short pre-wire calls surface reactions before the room does.
10. Check the Measurement thresholds below; fix and re-check until every one holds.
11. When the harness has persistent memory, store the locked dictionary, the spine, and a restatement log - the next period starts from them instead of re-deciding. Otherwise keep the dictionary as a versioned document wherever the team already keeps documents.

## Narrative structure

- Answer first, evidence beneath (Pyramid Principle / BLUF): the first page states the period verdict, the single biggest driver, the response underway, and the decision being asked of the audience. A reader who stops there has the whole story.
- Plan vs. actual vs. forecast is the organizing spine; every section is "what happened, why, what we are doing about it" - never a tour of charts.
- The deck is a pre-read; the meeting is for decisions. Aim the live agenda at forward decisions - practitioners converge on roughly two-thirds of board time forward, one-third backward - and let the backward detail live in the pre-read and appendix. The silent-read narrative memo practice pushes the same direction: prose forces complete arguments where bullets hide gaps.
- Keep the main body short. A main body that has grown past roughly twenty to thirty slides has become the pre-read; split it and rebuild the summary.
- Track the same metrics every meeting, in the same order, so trend is readable across periods without re-orientation.

## Presenting a miss

- No surprises, ever: every material negative appears in the pre-read and in pre-wire calls before the meeting. Bad news learned live costs more trust than the miss itself.
- Hit the bad news early in the document and end on the strongest true note - never sandwich the miss into an appendix.
- Never smooth: report the raw series and let the volatility show; smoothing defers the uncomfortable conversation and destroys the variance a reader needs. Offsetting movements are reported separately, not netted into a quiet-looking total.
- Anatomy of a reported miss:
  - The gap quantified against plan.
  - The driver named with the confidence actually held ("root cause confirmed" vs. "under investigation, findings next period").
  - The fix with an owner and the single metric that will prove it worked.
  - The forecast restated with the miss's cause reflected.

  If the cause is not yet confirmed, say so - a premature cause presented as fact is the next restatement.

- "Macro environment" is not a cause unless data separates market movement from execution.

## Reconciliation, restatement, and sign-off

- Ownership split:
  - RevOps publishes the numbers.
  - Finance certifies them.
  - Leadership decides.

  RevOps holds a publishing deadline, not a presenting role; a report finance cannot reconcile to the ledger does not ship.

- One definition beats one system: CRM and ledger will always disagree in-period - the fix is a written definition of what "right" means at each stage (sourced, contracted, billed, recognized), not a debate about which system wins.
- Restatement etiquette: when a shipped number was materially wrong, restate it visibly.
  - Label the column "as restated".
  - Footnote the cause and per-line effect.
  - Log it.

  Silent corrections are how trust dies. Repeated restatements are a controls problem to fix at the source, not a formatting problem.

- Numbers freeze when the pre-read ships. A correction after that point is a restatement, communicated as one - never a quietly different number in the room.

## Cadence

Three artifacts, not one report at three speeds - each has its own audience, depth, and forward commitment:

| Dimension        | Weekly revenue review                       | Monthly executive review                     | Quarterly board meeting                                       |
| ---------------- | ------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------- |
| Audience         | Revenue team + ops                          | Functional heads + CFO                       | Executive team + board                                        |
| Focus            | Current-period execution, deal/account risk | Plan-vs-actual trends, funnel, efficiency    | Full spine + narrative + decisions                            |
| Artifact         | Live view, no narrative                     | Scorecard + one-page narrative               | Pre-read deck + appendix + pre-wire                           |
| Forward edge     | This period's commit                        | Next month's priorities                      | Reset targets, capital, hiring                                |
| Preparation cost | Near-zero per run once the live view exists | An hour to a day, gated on the finance close | A week or more: pre-read, appendix, pre-wires, sign-off chain |

These are layers, not competing options, so no efficiency ranking applies between them - each answers a different audience's question, and weekly execution signals feed the monthly trend read, which feeds the quarterly reset. Ranking three artifacts that do not substitute for each other would be false precision.

What does need an order is what gets dropped when the effort ceiling binds:

- **First**: the monthly narrative (the weekly view plus a short written trend note covers it).
- **Second**: the weekly commentary.
- **Never**: the quarterly board artifact - it carries an external obligation the other two do not.

An analyst team of one should plan for that collapse in week 1, not discover it in week 12.

Escalate a topic one layer up only when it needs that layer's audience to decide.

## B2B and B2C / transactional / usage-based / PLG

- **Structurally identical across all models, state this in the deliverable.** These all carry over unchanged:
  - The movement-bridge shape (beginning, additions, losses, ending).
  - The plan-vs-actual-vs-forecast spine.
  - Cohort logic.
  - The answer-first narrative.
  - The reconciliation and sign-off chain.
  - The no-surprises discipline.
  - The cadence stack.
- **What changes is the atoms.** A contractual recurring base does not exist in consumption, transactional, and consumer models - the "recurring" number is a behavioral output. Swap spine atoms accordingly (per-model spines in [references/metric-spine.md](references/metric-spine.md)):
  - Gross transaction volume vs. net revenue vs. take rate.
  - Cohort retention curve shape.
  - Repeat purchase rate.
  - Contribution-margin layers.
  - Engagement ratios.
  - Consumption-based retention.
- Never annualize a month that contains one-time or seasonal revenue into a run-rate without saying so; consumption businesses in particular must separate seasonality from health degradation before either is reported.
- Benchmark against the matching model and the team's own history - seat-based subscription benchmarks flatter or slander every other model.

## Failure modes

| Trap                                      | Why it fails                                                                        | Fix                                                                                              |
| ----------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Data-dump deck                            | Audience reconciles charts instead of deciding                                      | Answer-first page one; detail to appendix; spine capped                                          |
| Definitions drift between meetings        | Same words, different numbers - the meeting becomes a definitions debate            | Frozen versioned dictionary; changes only as footnoted restatements                              |
| Two dashboards disagree on a spine metric | Credibility of every number collapses with the first contradiction                  | Reconcile to one written definition before the deck ships, never in the room                     |
| Smoothed or netted series                 | Hides the movement that was the signal; irreversible once raw variance is discarded | Raw series, bridges over nets, offsets reported separately                                       |
| Vanity metric creep                       | Cumulative charts and flattering cuts always go up; they carry no decision          | Cohort and distribution views; every metric must answer a question                               |
| Averages hiding distributions             | Two teams share a mean and nothing else                                             | Report attainment and deal-size as distribution bands                                            |
| Stage-mismatched spine                    | Late-stage efficiency metrics on an early company (or the reverse) mislead          | Stage tiering in the spine reference; resist audience pressure to report a stage not yet reached |
| Benchmarks asserted as fact               | Circulating numbers are dated and segment-specific                                  | Derive thresholds from own history; date and attribute any external figure                       |
| Surprise in the room                      | Trust erodes immediately and permanently                                            | Pre-read plus pre-wire calls; misses early in the document                                       |

## Measurement and pass thresholds

The report must pass every check below before it ships; iterate until it does:

- **Spine discipline**: at most 8 spine metrics in the main body (target 5-6); 100% of the prior period's spine metrics reappear with identical definitions, or the change is footnoted as a restatement.
- **Durability check**: the spine carries at least one durability metric (retention pair, cohort retention curve, consumption net retention, or margin-adjusted payback), or the report states which data gap deleted it. A spine ranked purely on production cost drifts to all velocity metrics and reads healthy until the base stops holding.
- **Definition coverage**: every spine metric has a dictionary entry with formula, source of truth, owner, and window; zero metrics in the deck without one.
- **Reconciliation**: the headline revenue number matches the finance-certified figure exactly, or the reconciling item is named in the deck; the billings/recognized/deferred identity checks out on the numbers shown.
- **Answer-first test**: hand page one alone to a reader with no context; they must be able to state the period verdict, the biggest driver or risk, and the ask. Any of the three missing fails the report.
- **Miss handling**: every material gap to plan appears in the first third of the document with a cause-confidence label, an owner, and a proof metric; nothing material appears for the first time after the appendix boundary.
- **Meeting design** (board cadence only): the live agenda allocates the majority of time - target two-thirds - to forward decisions, and every decision item names the decision, the context, and a recommendation.

After shipping, track these ongoing signals:

- **Restatement count per year**: rising means a controls problem upstream.
- **Whether meetings end with recorded decisions**: a recurring meeting that stops producing decisions means the artifact has drifted back into a data dump.

## Optional integration note

Skip this section unless the user names one of these platforms.

- **Semantic layers** (dbt MetricFlow, Cube, Looker/LookML): implement the versioned metric-dictionary discipline in code, define each spine metric once there and let every dashboard read the same definition.
- **Salesforce**: forecast-category fields are editable independently of stage, and report-time roll-ups can differ from dashboard snapshots - certify against an export, not a live view.
- **HubSpot**: default deal-stage probabilities are editable placeholders, not measured conversion - never let a weighted-pipeline figure built on them reach the deck unadjusted.

## Reference

- See [references/metric-spine.md](references/metric-spine.md) for the spine per business model, stage tiering, and the contested definitions to lock before first ship.
- See [references/metric-dictionary-entry.md](references/metric-dictionary-entry.md) for the dictionary entry shape and a worked example.
- See [references/worked-report-example.md](references/worked-report-example.md) for the report shape, a worked quarterly example with a miss, and a good-vs-bad narrative opening.
- `mbfinotti/revops-skills@revenue-kpi-framework` for designing the org-wide metric tree this report selects from - that skill decides which metrics exist and how they reconcile up, and this one turns the resulting spine into one narrative for one audience.
- `mbfinotti/revops-skills@revenue-data-governance-strategy` when the definitions themselves are contested across systems or functions - it settles whose ARR wins and who may change it, which this report's dictionary then cites rather than re-litigates.
- `mbfinotti/revops-skills@sales-forecast-diagnostic` to investigate why a forecast missed.
- `mbfinotti/revops-skills@crm-data-governance` for the field-ownership and source-of-truth rules the metric dictionary depends on.
- `mbfinotti/revops-skills@sales-pipeline-hygiene` for the recurring audit that keeps pipeline-derived spine metrics (coverage, win rate) trustworthy.
- `mbfinotti/revops-skills@pipeline-stage-definition-audit` when weighted pipeline is distrusted because stages are not buyer-verifiable.
