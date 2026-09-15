---
name: sales-pipeline-hygiene
description: Run a periodic, checklist-based hygiene audit over an active pipeline snapshot - stale deals (no stage, close date, or amount change, not logged touches) flagged against segment-specific stage medians, close-date push-count anomalies, and missing forecast-critical fields - producing an exception list with a disposition per flagged deal, a remediation plan, and a pass threshold. Use whenever the user mentions pipeline hygiene, a stale deal audit, pipeline cleanup before a QBR, deals that keep pushing, a close date that keeps slipping, missing fields on deals, or "our pipeline is full of junk" - even if they never say "hygiene". Covers B2B and B2C/high-velocity/PLG. Do NOT use for rewriting stage definitions - use mbfinotti/revops-skills@pipeline-stage-definition-audit instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.4"
---

# Pipeline Hygiene

Audit the deals sitting in the active pipeline right now - stale deals, close-date push anomalies, missing forecast-critical fields - and turn the findings into an exception list with one disposition decision per flagged deal, a remediation and communication plan, and a measurable pass threshold. Ownership is split three ways, not shared (ORM):

- RevOps owns the definitions, the snapshot, the automation, and the pre-published data package.
- The front-line manager owns the per-deal disposition and the coaching conversation.
- The rep owns the update and the evidence.

The split is what removes the argument - the manager arrives holding specific records that failed specific rules, not a general complaint. Splitting it the other way produces meetings that run on time and change nothing.

The audit's load-bearing definitional choice comes first: **meaningful activity means a change to Stage, Close Date, or Amount - not logged calls or emails** (ORM). Logged touches are activity in the CRM sense, but they do not indicate the deal moved, so a rule built on them can be satisfied without any progression - which is exactly how stale pipeline survives review after review. This is a live practitioner disagreement (many tools key on last-activity date); default to the field-change definition and use last-activity as a second, independent trigger - together, never interchangeably.

## Scope Boundaries

State these in the deliverable so the audit does not drift:

- This is a periodic audit of the deals in the pipeline today. Designing the standing automated reminder/nudge system that prevents staleness is a different job: the audit may recommend automating a recurring check and describe what it hands off to, but must not design alert timing, channels, or notification-fatigue policy.
- It does not audit or rewrite stage definitions or exit criteria - that is `mbfinotti/revops-skills@pipeline-stage-definition-audit`. Hygiene takes the existing stage set as given and inspects the deals inside it.
- It does not diagnose overall forecast reliability - that is `mbfinotti/revops-skills@sales-forecast-diagnostic`. Hygiene feeds it clean data; it does not fix the forecast method.
- It does not set org-wide field ownership or source-of-truth policy - that is `mbfinotti/revops-skills@crm-data-governance`. Hygiene checks completeness of the fields that already exist.
- It does not trace funnel revenue leakage - that is `mbfinotti/revops-skills@revenue-leakage`.

## Interview

Ask before auditing. One question per message; multiple-choice where possible; skip anything already answered.

- What can you export or query from the system of record: open deals with stage, amount, close date, owner, last activity date, created date, next step? Stage-change history? Close-date change history? As-of snapshots?
- Which motion and segments feed this pipeline: SMB/high-velocity, mid-market, enterprise, B2C/transactional, PLG sales-assisted, mixed? Typical cycle length and deal size per segment?
- Which recurring rituals already exist - weekly forecast call, pipeline review, QBR, deal desk? The audit rides on these; it must not add a meeting.
- Which fields do forecasting and pipeline decisions actually read? (These, not all fields, are what completeness is checked against.)
- Does a written definition of "stale" or any hygiene rule already exist? Is it enforced, and by whom?
- By what date must the result land - a QBR, a forecast call, a board number? A date inside the week promotes the remediations that ship the same day (validation rules, nudges) and demotes anything needing an integration.
- Is this a one-off cleanup (pre-QBR, pre-forecast, new leader) or the start of a recurring cadence? A recurring mandate is what makes auto-capture worth its cost; a one-off run leaves it unbuilt and re-runs the same manual pass next quarter.
- What is the effort ceiling: how much added friction per deal reps will absorb, how much admin configuration time exists, and how much manager review time exists per week? A team already at its friction limit rules nudges out whatever the completeness gap says, and a thin review budget pushes the bulk/conversation split (see [references/disposition-and-communication.md](references/disposition-and-communication.md)) toward bulk.
- Who is the manager who will work the exception list with reps, and who owns closing out dispositions?
- Any history of mass cleanups, and how did reps react? Are there known claim-only "dibs" deals - early-stage records opened just to hold an account?
- Is any compensation currently tied to CRM hygiene, field completion, or forecast accuracy?

## Workflow

1. Run the Interview. Fix the audit scope: all open deals as of a stated as-of date. Freeze that snapshot - dispositions are decided against it, not a moving book.
2. Extract the data. If you can query the pipeline data directly, pull open deals plus stage-change history, close-date change history, and activity records; otherwise request an export with those named columns. Then clean and standardize before measuring anything (Umbrex's audit order):
   - Map custom stages to canonical order.
   - Remove test records.
   - Backfill missing stage-entry dates.
   - Normalize currency and timezone.
3. Size the stale layer first, using the four staleness buckets - under 90 / 90-180 / 180-365 / over 365 days since last meaningful change (ORM). Recompute coverage excluding the over-365 bucket: the gap between that and headline coverage is the honest measure of how much reporting has been overstating the quarter. If more than 20-30% of pipeline value is stale, schedule a pipeline amnesty before any enforcement (see [references/disposition-and-communication.md](references/disposition-and-communication.md)).
4. Derive per-segment baselines from 12-18 months of closed-won history **with the stale layer excluded** - clean before measuring: a deal group carrying a large dead tail produces a longer, flatter close curve than its live deals actually have (ORM), corrupting the very medians the audit runs on. Compute median days-in-stage per stage per segment (median, not mean).
5. Set thresholds per segment - roughly 1.5x median for SMB/high-velocity up to 2.0x for enterprise - plus freshness windows and push triggers (Detection Rules below; derivations and fallbacks in [references/detection-rules.md](references/detection-rules.md)).
6. Run the three rule families over the snapshot. Output one row per deal per tripped rule, with the evidence that tripped it.
7. Merge flags into a per-deal exception list with pipeline value attached; second-push deals and multi-flag deals go to the top.
8. Propose a disposition per flagged deal from the taxonomy below. RevOps proposes; the manager and rep decide - flagging must never be auto-deletion, and the rep never grades their own homework. Every decided disposition gets a named owner and a recorded reason.
9. Draft the communication plan before anything is enforced or automated, and publish the exception list at least 12 hours before the meeting that works it - any meeting that starts by pulling a report has already failed (ORM). Detail in [references/disposition-and-communication.md](references/disposition-and-communication.md).
10. Emit the audit report (Output Shape below), section by section, for user validation.
11. Compute the KPIs and check the Pass Threshold; iterate dispositions and remediation until it holds, or schedule the gap into the next audit.
12. Wire the recurring audit into the rituals that already exist (Cadence below) and recommend automating the recurring check. The prevention layer the audit hands off to is a nudge-escalation system - Jeff Ignacio's (RevOps Impact) mechanic is the reference shape:
    - Message the owner on a past-due close date.
    - Increment a reminder counter.
    - Add the manager at the third reminder.

    Describing that handoff is in scope; designing the system is not (Scope Boundaries).

13. If your harness has persistent memory, store the baselines, thresholds, bucket sizes, and exception counts so the next audit starts from a trend line instead of a re-interview.

## Cadence - Ride Existing Rituals, Never Add a Meeting

- **Weekly forecast call**: RevOps brings committed deals with no meaningful activity in the last 14 days; the rep produces buyer-engagement evidence or the deal drops out of commit (ORM).
- **Biweekly pipeline review** per rep - weekly in the final month of the quarter - working aging, early-stage, and stalled deals off the pre-published exception list.
- **Quarterly territory scrub**, about two weeks before period end, so the cleanup lands before next quarter's coverage is measured.
- **Deal desk** for late-stage, non-standard, or flagged deals (re-stages, deal splits) - not routine hygiene.
- Keep executives out of rep-level pipeline reviews: their presence makes reps defend pipeline instead of exposing risk in it (ORM). Reps attend their manager's session; leadership gets the roll-up.

## Detection Rules

Three families, all reading "meaningful activity" as defined above. Label every threshold with its provenance; numbers are practitioner starting points to calibrate on the user's own data.

- **Stale deals** - two independent triggers, used together:
  - Stage age: flag past 1.5x-2.0x that segment's median days-in-stage. The multiplier is segment-dependent, not a matter of taste: ~1.5x for SMB/high-velocity, 1.5-2.0x mid-market, 2.0x enterprise (convergent: Umbrex, Outreach, DealHub).
  - Last-activity age: no activity in 14 days for mid/late stages (Umbrex, Outreach). As an inactivity rule of thumb, SMB flags at 14-21 days, mid-market 30-45, enterprise 60-90, with legal and procurement reviews explicitly exempt (DealHub).
  - A next step dated in the past, or no scheduled future meeting, also flags.

  Classify every stale deal into the four buckets. ORM's 12-month rule marks the truly dead layer - close curves rarely carry meaningful expectation past 52 weeks.

- **Push-count anomalies** - track pushes as a field, not a memory: count close-date changes per deal from field history.
  - The second push is the escalation trigger (ORM: the best single predictor of slippage is a rep changing the close date, and the second push is the one to act on). It moves the deal to manager inspection.
  - A push crossing a quarter boundary is worse than an in-quarter nudge: require a stated reason on any close-date change that crosses a period boundary.
  - Three or more slips is disqualification-warranting (SalesOpsClub).

  Separate slipping from dead with evidence tests, not the close-date field. Ask "what has to happen before this date becomes realistic?", then stack the signals:
  - Mutual-action-plan progress with dated owners.
  - Multi-threading depth.
  - Economic-buyer engagement.
  - Entry into procurement/legal.
  - Champion responsiveness.

  A delayed next step alone may be harmless; combined with a pushed date, single-threading, and budget hesitation it becomes an explainable case for intervention. Once a slip is confirmed, update the close date immediately with a note on the evidence - the worst outcome is intervening on the deal but leaving the forecast untouched.

- **Field completeness** - check forecast-critical fields only, not the whole schema:
  - Next step and its date, close date, amount, stage, forecast category, loss reason on closed-lost, plus whatever qualification fields the forecast actually reads.
  - Amount, stage, and close date are the highest-value targets - they are the meaningful-activity fields themselves.

  Target 90-95% completeness on forecast-critical fields, 80% as the minimum floor. Remediate in efficiency order - **stage-gated validation rule > owner nudge > auto-capture** - with the three axes behind that order, and the magnitudes, in [references/detection-rules.md](references/detection-rules.md).
  - The validation rule leads: it costs about an hour of admin, fires only on advancement to a late stage so it costs the rep seconds, protects exactly the fields the forecast reads, and switches off again if it misfires. A required field checks that something was entered; a validation rule checks that what was entered makes sense.
  - More required fields is not on that list: it is ruled out rather than ranked last, because heavy requirement produces fabricated placeholders ("n/a n/a n/a" at scale), worse than an honest blank because it looks like signal. Hold the cap at 5-7 required fields per object.
  - Auto-capture is what the order starves: it removes the friction permanently but costs an integration project plus a consent review, so a ratio picks a nudge over it every round. Promote it when a capture tool is already deployed, or when reps are at their friction limit and there is no nudge left to spend.

  The order is a default, not a law; re-rank it against the Interview answers and against who will execute it.

## Dispositions

Every flagged deal exits the review with exactly one disposition, an owner, and a recorded reason. For the stale working list, only two answers are acceptable: revive it with a real next step and a validated close date, or close it out (ORM).

| Disposition                           | When                                                                                           |
| ------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Close lost, with a real reason code   | No buyer-side evidence of an active buying process; the honest state is "not happening"        |
| Move to nurture                       | Genuine future interest, but no active buying process now                                      |
| Re-stage backwards                    | Deal is real, but the stage overstates the buyer's actual position                             |
| Re-date with evidence                 | Date is wrong but the deal is moving; the new date is the answer to "what has to happen first" |
| Keep, with a named next step and date | The flag was a data gap, not a dead deal; fix the record                                       |

This table is deliberately unranked: each row is a different deal state, selected by what the buyer-side evidence supports, not a competing route to the same outcome - ordering them by efficiency would be false precision.

Route non-standard re-stages and deal splits through the deal desk. Never delete - classify instead: deleting removes the record the next audit would learn from, corrupts history and conversion baselines, and recycle-bin retention in typical CRMs is short. Default a returning buyer to a _new_ record linked back to the closed-lost one; reopening the original buys the same recovery at a higher and irreversible cost, and only two named conditions flip that - see [references/disposition-and-communication.md](references/disposition-and-communication.md).

## B2B vs B2C / High-Velocity / PLG

The real divergence is not the thresholds - it is the unit of analysis, the acceptable degree of automation, and whether qualification lives in the CRM at all:

- **B2B (long cycle, high ACV, buying committee)**: deal-by-deal inspection in the pipeline review; 2.0x multipliers, enterprise silence tolerated to 60-90 days; qualification depth in CRM fields (champion, economic buyer, paper process); push-count and quarter-boundary crossings are the slippage focus.
- **High-velocity / B2C**: aggregate rules and exception-based automation replace deal-by-deal review; ~1.5x multipliers, 14-21 day flags; 3-5 stages; scheduled auto-close is acceptable for pre-qualified early stages only, referencing last-activity date to avoid false positives, and only with sales-leadership buy-in. Velocity and conversion-rate thresholds matter more than push counts.
- **Pure PLG**: prospects qualify themselves through usage and self-serve deals convert in-product - a traditional deals pipeline, and therefore a rep-facing hygiene audit, may not be warranted at all. Say so rather than forcing the audit; hygiene shifts to product-signal and PQL routing.

Identical across all motions:

- The meaningful-activity definition (field change, not logged touch).
- Classify-don't-delete.
- Validation-rules-over-required-fields.
- The coaching-not-policing posture.

Shared SLA mechanic: set a maximum allowable age per stage proportional to baseline cycle length, and on SLA breach auto-tag for manager review - never auto-close, which breeds distrust.

## Output Shape

Compact skeleton - full worked examples, including one audit done wrong, in [references/audit-report-examples.md](references/audit-report-examples.md):

```
PIPELINE HYGIENE AUDIT - <pipeline>, as-of <date>
Definitions   : meaningful activity = stage/close date/amount change;
                per-segment thresholds with provenance
Stale layer   : value by bucket (<90 / 90-180 / 180-365 / >365d);
                headline coverage vs coverage excluding >365 bucket;
                amnesty recommended yes/no
Summary       : deals audited, flagged, % of pipeline value flagged
Exception list: deal | owner | flags | evidence | proposed disposition |
                decided disposition | disposition owner | reason
Field gaps    : field | % complete vs 90-95% target | decision it feeds |
                fix (validation rule / nudge - not new required fields)
Push report   : push-count distribution; second-push deals at top with
                stacked-signal evidence and "what has to happen" answers;
                quarter-boundary pushes with stated reasons
Remediation   : actions, owners, due dates
Communication : rituals the audit rides on; exception list published >=12h
                ahead; who is told what before enforcement
KPIs          : baseline vs target per KPI, pass/fail, next audit date
```

## Common Failure Modes

| Failure                                          | Consequence                                                                             | Fix                                                                                                                                  |
| ------------------------------------------------ | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Staleness keyed on logged calls/emails           | Rules satisfied without progression; stale pipeline survives every review               | Key on stage/close date/amount change; last-activity as second trigger                                                               |
| One flat threshold across segments               | Over-flags enterprise, under-flags SMB                                                  | Segment-specific medians and multipliers                                                                                             |
| Measuring before cleaning                        | Dead tail flattens close curves; baselines corrupted                                    | Exclude the stale layer, then compute medians and coverage                                                                           |
| RevOps as "CRM police" / auto-close, auto-delete | Distrust; real activity moves off-CRM; honesty punished                                 | Auto-tag for manager review; amnesty before enforcement; coaching posture                                                            |
| Deleting flagged deals                           | The record the next audit would learn from is gone; baselines and rep metrics corrupted | Classify, never delete                                                                                                               |
| Enforcing rules nobody was told about            | Reps discover rules by being flagged; gaming begins                                     | Publish rules and thresholds first; exception list 12h ahead                                                                         |
| More required fields as the completeness fix     | "TBD" / "." / "123" junk at scale                                                       | Cap at 5-7 required; stage-gated validation rule first, nudge second                                                                 |
| Comp tied to field completion                    | Fast, complete, low-quality data                                                        | If comp touches hygiene at all, tie it to forecast accuracy (outcome), never completion (input)                                      |
| Close-date stuffing at quarter end               | Mass date edits to pass the audit; forecast fiction                                     | Require a stated reason on any push crossing a period boundary; fix the incentive                                                    |
| Sandbagging                                      | Deals held or timed for comp/quota reasons                                              | EOQ close concentration 20-25% is healthy; sustained >35% for one rep opens a comp-design conversation, not a compliance one (Avoma) |
| Happy ears                                       | Commit deals slip or no-decision out at 40-60% too late to react                        | Evidence-based forecast categories; stacked-signal tests                                                                             |
| Treating every push as a dead deal               | Genuinely slipping deals killed; legal/procurement stalls mislabeled                    | Evidence test; exempt legal/procurement review periods                                                                               |
| "Dibs" deals left untouched                      | Claim-only records rot, block marketing and territory moves                             | Explicit disposition rule for claim-only deals                                                                                       |
| Hygiene score as vanity KPI / audit theatre      | Score improves, forecast doesn't; same problems persist yearly                          | Grade on forecast-linked KPIs; recurring exceptions past 30 days become system rules, not more meetings                              |

## KPIs and Pass Threshold

Track per audit and as a trend across audits, each labelled with provenance:

- Stale value as % of open pipeline: healthy is below 20-30%, late-stage stale below 15% (Umbrex); bucket distribution across the four staleness buckets.
- Honest coverage: headline coverage vs coverage excluding the over-365-day bucket - track the gap shrinking.
- Slipped-deal rate (forecasted deals that push out of period): target below 20%; consistently above 30% signals systemic qualification or discipline problems (Revenue.io).
- Push-count distribution: share of deals at 0 / 1 / 2+ pushes; quarter-boundary pushes with vs without stated reasons.
- Field completeness on forecast-critical fields: 90-95% target, 80% floor (Saber; Komo/DAMA).
- % of open deals with a future-dated next step: core metric; set the target from the user's own baseline, never a published number.
- Close-date accuracy: % of closed deals whose CRM close date matched actual within a tolerance (14 days is ORM's version; tighten from own data).
- EOQ close concentration per rep, as the sandbagging watch metric.

Pass threshold - the first audit sets the baseline; targets come from that baseline, not published numbers. The audit passes when:

- Every flagged deal has a decided disposition with an owner and reason - zero unresolved.
- Zero open deals with a past-due close date at audit close.
- Zero second-push or quarter-boundary-push deals without a documented evidence answer.
- Stale-value %, honest-coverage gap, completeness, and next-step rates all improved against baseline toward the agreed target.

Iterate until all four hold. Before quoting any hygiene statistic to stakeholders (including "40-60% of pipeline is stale"), check its credibility flag in [references/evidence-and-benchmarks.md](references/evidence-and-benchmarks.md) - much of the numeric detail in this field comes from vendors selling forecast tooling.

## Optional Integration Note

Skip unless the user names one of these platforms.

- **Salesforce**: the Recycle Bin retains deleted records for only 15 days, one more reason deletion is irreversible in practice; field history tracking must be enabled per field before push counts become reconstructable.
- **Pipedrive**: per-stage "rotting" day thresholds are a native feature and can encode the derived stale thresholds directly.

## Invocation Examples

- "Our pipeline is full of junk before the QBR - half these deals haven't moved in months. Run a hygiene audit and tell me what to close, keep, or push to nurture."
- "Here's a CSV of our open deals with stage history and close-date changes. Flag everything stale, everything that keeps pushing, and every deal missing a next step."
- "Three deals in my commit have pushed their close date twice each. Audit the book for push anomalies and give my managers an exception list to work with reps."

## Reference

- Read [references/detection-rules.md](references/detection-rules.md) when computing baselines and running the rules - the meaningful-activity definition, per-segment median tables, derivations, fallbacks when history is missing, placeholder detection, and dibs-deal detection.
- Read [references/disposition-and-communication.md](references/disposition-and-communication.md) when deciding dispositions and drafting the rollout - the evidence test per disposition, reason-code design, the pipeline amnesty, the reopen-vs-new-record default and the two conditions that flip it, the bulk-versus-conversation split, and the communication plan.
- Read [references/audit-report-examples.md](references/audit-report-examples.md) when shaping the deliverable - one B2B audit, one high-velocity audit, and one audit done wrong.
- Read [references/evidence-and-benchmarks.md](references/evidence-and-benchmarks.md) before citing any number - every threshold and statistic with source and credibility flag, including the vendor-incentive caveat.
