---
name: revenue-leakage
description: Trace where deals and revenue silently exit one specific funnel and size the loss in recoverable (never gross) dollars - untracked steps, unworked leads, manual handoffs, mid-funnel stalls, paper-process drops, billing and renewal misses - separating real leaks from healthy disqualification and data-capture gaps. Use whenever the user mentions revenue leakage, funnel drop-off, a leaky funnel, deals disappearing, unworked leads, handoff gaps, "where are we losing deals", or "why did pipeline vanish" - even if they never say "leakage". Covers B2B sales-led and B2C/self-serve/PLG, one funnel instance at a time. Takes stage definitions as given - to audit those, use mbfinotti/revops-skills@pipeline-stage-definition-audit instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.2"
---

# Revenue Leakage

Trace where records and dollars silently exit one specific funnel instance, prove each loss is real, size the recoverable amount, and rank the fixes by owner.

- **Lifecycle lens:** Winning by Design's Bowtie (winningbydesign.com/bowtie). Leakage spans acquisition through onboarding, renewal, and expansion, not just the sales stages - most teams over-inspect the top and never reconcile the back half.
- **Late-stage leak:** MEDDPICC's "Paper Process" element (meddicc.com/meddpicc) names the classic late-stage leak - deals that die between verbal yes and signature.
- **Working method:** process mining applied to the funnel's own event log, the approach Celonis popularized. Reconstruct the process from timestamps as it actually ran, never from the documented flowchart.

## Ground Rules

- Trace, never redesign. The stage set, routing rules, scoring model, and handoff processes are inputs. If one of them is the defect, say so in one line and route to the matching skill in Reference - do not rebuild it here.
- The deliverable is a leak register, never a hygiene checklist. Stale-deal counts, missing fields, and push counts are input signals for locating leaks; reporting them as the finding is a different skill's job (`mbfinotti/revops-skills@sales-pipeline-hygiene`). Leakage asks where records and dollars exited without an accounted-for reason, and what that is worth.
- Nothing is a leak until it passes the three-way classification below. Counting healthy disqualification as leakage is the most common false finding in this genre. Mistaking a data-capture gap for a funnel drop is the second most common.
- Size the recoverable amount, never the gross. Presenting the gross pipeline value of stalled deals as "leaked revenue" is the standard way these reports lose credibility with finance.
- Stay on one funnel instance for one period and one entry cohort. Program-level patterns across teams, funnels, or quarters are out of scope.
- Label every numeric threshold with its provenance: published practice, practitioner consensus, or derived from the user's own data. Never present a vendor heuristic as an industry constant.
- Warn off the circulating speed-to-lead statistics below - the vendor pages carrying them cite nothing:
  - "respond in 5 minutes = 100x more likely"
  - "21x more likely to qualify"
  - "average B2B response time is 42 hours"
  - "38% of leads never reply"
  - the "391% / 60-second rule"

  The HBR 2011 paper "The Short Life of Online Sales Leads" (Oldroyd, McElheran, Elkington) is real and citable as evidence that response latency matters, but the specific multipliers commonly attached to it were not verifiable. Measure the user's own response-time-vs-conversion curve and derive the threshold from that.

## The Conservation Test

Every record that enters a funnel step must leave it through exactly one countable outcome:

- **advanced**
- **closed-lost with a recorded reason**
- **disqualified/recycled with a recorded reason**
- **still open inside that step's expected dwell window**

Build the reconciliation per transition:

```
entered  =  advanced + lost(reason) + disqualified(reason) + still-open(in window)  +  residual
```

Every non-zero residual demands an explanation. Before anything is called a leak, run the three-way classification on it:

1. **Real leak** - the record was viable and stopped moving for a process, system, or ownership reason (never contacted, never accepted, stalled past window, never invoiced). Only these get sized and ranked.
2. **Healthy disqualification** - the record left for a legitimate reason and the exit was recorded. Not a leak. A funnel with zero disqualification is not healthy; it is unfiltered.
3. **Data-capture gap** - the record actually progressed but the system never recorded it: an untracked step, work living in an inbox or spreadsheet, a missing timestamp, a conversion completing in a system that never writes back. The drop is in the data, not the funnel; the fix is instrumentation, and "fixing the funnel" here fixes nothing.

**Untracked-step detection is the signature move.** For every pair of adjacent systems or owners, ask what happens in between and whether a human does it by hand. Any step performed in an inbox, spreadsheet, or chat thread has no timestamp and therefore no measurable drop-off - treat every such step as a suspected leak site until instrumented or proven pass-through. A step that produces no records carries no measurable leak; name it as an instrumentation gap instead of guessing a number.

## B2B and B2C / Self-Serve

- **B2B sales-led:** leak sites are human action points - respond, route, accept, advance, chase signature. A rep-owned pipeline exists, so residuals attach to owners.
- **B2C / self-serve / PLG:** most of the funnel has no rep-owned pipeline; the mechanism is technical rather than human - trial and checkout step drops, payment failure and dunning gaps, involuntary churn, auto-renewal misses. Involuntary churn runs 20-40% of total subscription churn (Baremetrics, citing Paddle research), and 2-5% for B2B SaaS specifically (Baremetrics' own platform data - vendor-aggregated, not an independent study).
- **Identical across both, apply without modification:** the conservation reconciliation itself, the three-way classification, the recoverable-dollar sizing rule, and the rule that an untracked step cannot be measured until instrumented. Only the leak-site catalog and the evidence types differ.

## Interview

Ask before analyzing. One question per message; multiple-choice where possible; skip anything already answered.

- Which funnel and motion: B2B sales-led, sales-assisted PLG, pure self-serve/B2C? One funnel instance only - which one?
- What triggered this investigation: a number that dropped, a board question, deals that vanished, a gut feeling?
- What are the funnel's steps as actually operated (not the official diagram), and which system holds each segment of the record trail - marketing tool, sales system, billing system, spreadsheets?
- What can actually be exported or queried: stage-change history with timestamps, owner history, closed-lost and disqualification reason codes, billing/invoice records, payment-failure events?
- Where do manual steps live today - which handoffs happen through an inbox, a spreadsheet, or a chat message?
- Who owns each funnel segment, and who owns the spaces between segments?
- Which period and entry cohort should the analysis cover? (One cohort, followed forward - never a mixed-vintage snapshot.)
- Average deal or subscription value, and the historical step-to-step conversion rates if known?
- What unexplained residual per transition are you willing to sign off on? The Pass Threshold gates on this number and it has to be yours, not this skill's. A common working bar is 5% of entering records per transition - a practitioner figure, not a published standard. Take 5% only as a placeholder when no better basis exists, and tighten it from the funnel's own reconciliation history as soon as one run produces that history.
- By what date must the recovered revenue actually land - this quarter's close, a board date, no fixed deadline? (A hard date deletes process redesign from this round's register and leads with alerts, routing fallbacks, and rework of the records already leaked.)
- Do you want a one-off recovery of the records that already leaked, or a fix that stops the leak recurring? (One-off promotes rework; compounding promotes alerts, routing fallbacks, and recovery sequences.)
- What is the effort ceiling - analyst hours only, engineering capacity available, or a cross-team process change on the table?
  - Analyst-only deletes instrumentation and redesign fixes.
  - Engineering capacity promotes recovery sequences and instrumentation.
  - A cross-team mandate is what makes process redesign rankable at all.

## Workflow

1. Run the Interview; fix the funnel, period, and entry cohort; confirm the scope boundary (trace, not redesign).
2. Map the funnel as actually operated: every step, system, owner, and handoff - including the manual ones. Mark every untracked or hand-performed step as a suspected leak site. Use [references/leak-site-inventory.md](references/leak-site-inventory.md) as the checklist of sites to probe so none is skipped.
3. If you can query the funnel's systems directly, build the conservation reconciliation per transition from the event history; otherwise derive it from exports and record samples the user provides, and mark every transition you could not reconcile as unmeasured rather than assuming it is clean.
4. Classify every non-zero residual with the three-way test, attaching evidence per record group: timestamps, owner history, reason codes, or their absence. An unclassifiable residual stays labeled "unexplained" - never promote it straight to "leak".
5. Size each confirmed real leak in recoverable dollars per [references/sizing-recoverable-revenue.md](references/sizing-recoverable-revenue.md), with a confidence tag on every figure.
6. Build the leak register (schema in Output Shape), ranked by recoverable dollars per unit of fix effort - never by dollars alone - using the fix-class ordering in [references/sizing-recoverable-revenue.md](references/sizing-recoverable-revenue.md), re-ranked against the deadline, one-off-vs-compounding, and effort-ceiling answers from the Interview. Delete a fix class the user's constraints rule out rather than demoting it, and say which constraint deleted it. Data-capture gaps get their own section with an instrumentation fix, not a dollar figure.
7. Emit the report one section at a time for user validation, grounded in the matching example from [references/worked-examples.md](references/worked-examples.md).
8. Check the Pass Threshold; iterate until it holds or every remaining gap is explicitly named as uninstrumented with a scheduled fix.
9. If the harness has persistent memory, store the funnel map, the instrumentation gaps, and the agreed residual baselines so the re-check starts from them; otherwise put all three in the report's final section so the user can paste them into the next run.

## Output Shape

Every threshold and dollar figure carries a provenance or confidence tag.

```
REVENUE LEAKAGE REPORT - <funnel>, <cohort/period>, <date>
Funnel map       : steps -> systems -> owners; manual/untracked steps flagged
Reconciliation   : per transition - entered / advanced / lost(reason) /
                   disqualified(reason) / open-in-window / residual (% of entered)
Leak register    : rank | site | evidence | classification | records affected |
                   recoverable $ (confidence) | owner | fix | fix class
                   (fix class carries the effort behind the rank; ranking basis
                   and any deleted fix class stated above the register)
Disqualification : volume left for recorded, legitimate reasons (not leakage)
Capture gaps     : untracked steps + records that progressed unrecorded;
                   instrumentation fix per gap, no dollar figure
Recoverable total: sum of register, by confidence band; never a gross figure
Re-check         : residual baselines agreed, re-run date, gaps scheduled
```

## Pass Threshold

- The unexplained residual at every reconciled transition is below the tolerance agreed with the user upfront - a common working bar is 5% of entering records per transition (practitioner working bar, not a published standard; derive a tighter one from the funnel's own history).
- Every leak register entry carries evidence, a classification, a recoverable figure with confidence tag, an owner, a fix, and that fix's class.
- Every unreconciled transition and untracked step is explicitly named as uninstrumented with a scheduled instrumentation fix - never silently omitted.
- The analysis covers exactly one entry cohort followed forward; no snapshot counts mixed with cohort flows.

Iterate until all four hold. Where instrumentation must be built before a transition can be reconciled, the report says so and schedules the re-run - that is a passing outcome; a guessed number is not.

## Common Failure Modes

| Defect                                                   | Consequence                                                                   | Fix                                                                                               |
| -------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Mixing cohort vintages (snapshot counts vs cohort flows) | Residuals are arithmetic noise; leaks invented or hidden                      | One entry cohort followed forward; compare like periods only                                      |
| Counting healthy disqualification as leakage             | Inflated findings; sales stops trusting the report                            | Three-way classification before anything is called a leak                                         |
| Mistaking a capture gap for a funnel drop                | "Fix" targets a funnel that isn't broken; nothing improves                    | Check for progression evidence in adjacent systems first                                          |
| Double-counting a record that leaks twice                | Recoverable total exceeds reality; credibility lost                           | Each record counts once, at its first unexplained exit                                            |
| Sizing gross pipeline value as recoverable               | Finance discounts the whole report                                            | Recoverable = records x value x onward conversion from that point                                 |
| Blaming reps for a systems defect                        | Political fight, no fix; the leak persists                                    | Attach residuals to process/system owners, not individuals, unless owner history proves otherwise |
| Guessing a number for an untracked step                  | A fabricated figure anchors the whole ranking                                 | Name it uninstrumented; instrument first, measure next run                                        |
| Deliverable drifts into a hygiene checklist              | Duplicates the hygiene skill; the "what is it worth" question goes unanswered | Every finding must state records affected and recoverable dollars or an instrumentation fix       |

## KPIs

- Track per re-run:
  - unexplained residual share per transition (trending to the agreed tolerance)
  - recovered dollars against the sized recoverable figure per fixed leak
  - share of funnel steps with timestamps (instrumentation coverage)
  - time from leak confirmation to fix ownership
- Recovered-vs-sized is the honesty check on the sizing method itself: if actual recovery consistently lands far under the sized figure, tighten the onward-conversion assumptions before the next report.
- Never report "leaks found" as the success metric - it rewards inflating the register.

## Invocation Examples

- "Our marketing team swears they sent sales 400 qualified leads last quarter and sales says they got 250. Where are we losing deals and what is it costing us?"
- "Trial signups are steady but paid conversions dropped 20% and nobody can say where in the funnel it happens. Trace the leak."
- "Deals keep disappearing between verbal commit and signed contract, and renewals seem to just lapse. Find the leakage and tell me what's actually recoverable."

## Reference

- Read [references/leak-site-inventory.md](references/leak-site-inventory.md) when mapping the funnel - the catalog of leak sites from entry to involuntary churn, with detection signals and evidence to pull per site.
- Read [references/sizing-recoverable-revenue.md](references/sizing-recoverable-revenue.md) when sizing and ranking - the recoverable-dollar formula, onward-conversion estimation, confidence tags, and ranking rules.
- Read [references/worked-examples.md](references/worked-examples.md) when shaping the deliverable - one B2B reconciliation, one self-serve/PLG reconciliation, and one report done wrong.
- See `mbfinotti/revops-skills@sales-forecast-diagnostic` when the presenting symptom is a wrong forecast number rather than vanished records.
- See `mbfinotti/revops-skills@lead-routing` when a leak site turns out to need the assignment logic redesigned.
- See `mbfinotti/revops-skills@lead-scoring` when a leak site turns out to need the score redesigned.
- See `mbfinotti/revops-skills@sales-to-cs-handoff` when the fix for a handoff leak is designing the sales-to-CS handoff itself.
