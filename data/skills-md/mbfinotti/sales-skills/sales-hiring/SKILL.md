---
name: sales-hiring
description: Employer-side hiring workflow for SDR/BDR and AE roles, producing an outcome-based scorecard, a structured interview loop with question bank, a scored mock-call work sample, and a 30-60-90 ramp plan with certification gates. Recommends SDR vs AE vs full-cycle from ACV, cycle length and inbound volume, and rests on selection-validity evidence - structured interviews, independent scoring, no brainteasers. Use whenever the user mentions hiring a rep, sales interview questions, a hiring scorecard, a mock call interview, rep onboarding, or a ramp plan, even without the word hiring. Do NOT use for candidate-side prep (mbfinotti/sales-skills@sales-career) or comp plan design (mbfinotti/sales-skills@sales-comp-design).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.2"
---

# Sales Hiring

Build the four artifacts a hiring manager needs to recruit an SDR/BDR or AE with evidence-backed rigor: a role scorecard, a structured interview loop with question bank, a scored mock-call work sample, and a 30-60-90 ramp plan. Structure beats intuition at every stage - the whole skill exists to enforce that.

Label every benchmark output with a short parenthetical naming its source - peer-reviewed, survey, crowdsourced, vendor data, or a named practitioner - and never present a lower tier as a higher one, or a vendor claim as fact.

If the user turns out to be a candidate preparing for a sales interview rather than a hiring manager running one, stop and point them to `mbfinotti/sales-skills@sales-career` - this skill never coaches the candidate.

Out of scope, do not drift into:

- sourcing candidates
- writing or distributing job ads
- running an applicant tracking system
- designing the commission plan as a strategy exercise
- SDR-to-AE promotion mechanics

Compensation appears here only as the published range and the base/variable split and ramp draw that shape the candidate funnel and the ramp.

## Interview

Ask before producing anything. Stop at these ten questions.

- One question per message.
- Offer the multiple-choice options.
- Skip any question the user's message already answers.

Questions 8-10 exist to re-rank the orderings in this skill before the user commits to a path - ask them here, never later.

1. Team stage: (a) first sales hire, founder still selling; (b) hires 2-4, playbook forming; (c) hires 5-30, repeatable playbook exists; (d) 30+, scaling a known model.
2. Role in mind: (a) SDR/BDR; (b) AE; (c) full-cycle rep; (d) not sure - recommend one for me.
3. Pipeline source mix: (a) mostly inbound; (b) mostly outbound; (c) balanced mix.
4. ACV and typical sales-cycle length: (a) under ~$5K, under a month; (b) ~$5-25K, 1-3 months; (c) ~$25-100K, 3-6 months; (d) over ~$100K, 6+ months.
5. Segment: (a) enterprise B2B; (b) high-velocity inside sales (SMB/mid-market B2B); (c) B2C/consumer.
6. Comp philosophy: base-heavy (60:40 or more) or aggressive variable (50:50, uncapped accelerators)? And will you publish the range in the posting?
7. Hiring jurisdiction(s): US (which states, notably NYC/CO/CA/NY/WA/IL), EU (which countries), UK, other - this drives the compliance checks.
8. Deadline: by what date must the offer be signed? (a) this month; (b) this quarter; (c) no hard date.
9. One-off or compounding: a single hire, or the first of several where the scorecard, question bank and rubric get reused? (a) one-off; (b) compounding.
10. Effort ceiling: how many interviewer-hours per candidate can you spend, and do you have a recruiter and an existing trained panel? (a) under ~5 hours, no recruiter, no panel; (b) ~5-15 hours; (c) more, with recruiting support.

## Reading the answers

Every answer above drives an output; use them, don't just record them.

- **Q3 + Q4 decide the role recommendation (Q2), and they flip the ordering.** Default for ACV under ~$25K on cycles under three months with inbound flow (read `>` as "more of this axis"; the efficiency line is the recommendation):
  - efficiency: full-cycle rep > AE only > SDR + AE split
  - value (pipeline generated and revenue closed per hire): SDR + AE split > AE only > full-cycle rep
  - effort (loops to run, ramps to write, handoffs to police, time-to-fill): SDR + AE split > full-cycle rep > AE only
    Above ~$25K ACV on 3-6+ month cycles with an outbound motion, the value line wins and the split leads - one rep cannot both prospect a mapped account list and run six-month deals. **Go/no-go, stated as a deletion:** while inbound volume keeps a closer's calendar full, delete the SDR + AE split from the menu instead of ranking it last, since a ruled-out option parked at the bottom comes back as headcount. Put it back only once AEs show empty-calendar syndrome or the company commits to outbound as a strategy **[survey + practitioner]**. If the user picked a role in Q2 that contradicts this, challenge the pick before proceeding and say why.
- **Q1 decides the candidate profile.**
  - First hire: a founder-led-sales handoff problem. Hire a builder who sells without infrastructure, and treat heavy big-company experience as a risk (the "coin-operated" rep who imports a formula instead of building the company's own). Mark Roberge's regression on his own team found aggression and objection-handling nearly uncorrelated with success; coachability, curiosity, intelligence, and work ethic predicted it (his own single-company regression, not a broader study). For a founder or CEO running this interview personally, SaaStr's repeated framing for the first 2-10 reps is a single gut-check test layered on top of the scorecard, not a replacement for it: would you, the founder, actually buy the product from this person (practitioner opinion).
  - Hires 5-30: a repeatability problem. Profile from the org's own top performers and hire the same rep every time.

  Also warn: doubling the team requires doubling each demand-generation source in proportion, or new hires starve.

- **Q5 sets loop length, work-sample content, predictor weighting, comp split and sourcing** - see B2B and B2C below.
- **Q6 shapes the funnel and the ramp.**
  - Base-heavy splits attract risk-averse candidates and suit reps who start with zero pipeline.
  - Aggressive 50:50 plans with uncapped accelerators self-select confident closers.
  - An unpublished "competitive OTE" repels strong candidates, who read it as a signal the quota is set to fail (practitioner opinion).

  Publishing a range is also legally required in a growing set of jurisdictions (Q7).

- **Q7 triggers the compliance pass** in workflow step 4.
- **Q8 promotes the fast-acting options.** A this-month date:
  - deletes the 5-6 stage enterprise loop
  - promotes the single-loop roles over the SDR + AE split
  - promotes reusing an existing question bank over writing one

  No hard date leaves every default order below in place.

- **Q9 decides whether the work sample stays starved.**
  - One-off: the build amortizes over a single candidate pool, so run the mock call but build it thin - no quarterly rubric refresh, no scorer-training programme.
  - Compounding: the frozen rubric and question bank serve every future hire, which promotes building both properly and first - this is the condition in Selection evidence that overrides the efficiency order.
- **Q10 deletes rungs rather than reordering them.**
  - Under ~5 interviewer-hours per candidate: cut to 3-4 stages and keep only the structured interview and the work sample.
  - No recruiter and no trained panel: every hour in the Selection evidence table becomes the hiring manager's own - re-rank against that, not against a staffed team.

## Workflow

Produce the four artifacts in order. Deliver each one, validate it with the user section by section, then move to the next - never dump all four unreviewed.

1. Run the Interview. Confirm or challenge the role choice using Reading the answers, and state the reasoning in one short paragraph the user can veto.
2. **Artifact 1 - role scorecard.** Build from [references/scorecard-template.md](references/scorecard-template.md). Three parts:
   - a one-sentence mission
   - 3-8 measurable outcomes ranked by importance and quantified (e.g. "$1.2M net-new ACV in year one", "40 SQLs/quarter"), never vague responsibilities
   - 5-7 competencies weighted per segment and team stage

   The scorecard doubles as the interview rubric and the ramp milestone map, so quantify outcomes even when the user resists. Avoid the all-around-athlete profile: narrow, deep competence against these outcomes.

3. **Artifact 2 - interview loop + question bank.**
   - Design the stage sequence for the role and segment: SDR 3-4 stages over days-weeks; AE 4-6 stages; enterprise AE 5-6 stages over weeks, with an inverted funnel (hiring manager in early) when the candidate pool is small and hot.
   - Place the scored work sample at stage 2 or 3, never last. The two placements are identical on value: `value: stage 2-3 == last`, a genuine tie because it is the same instrument, the same rubric and the same score wherever it sits. They separate only on hours: `interviewer hours burned: last > stage 2-3`, at 10+ hours per candidate who cannot sell, plus the extra days of time-to-fill that lose candidates to competing offers. Last placement is therefore deleted from the menu, not ranked below stage 2-3; quality gate 5 enforces it.
   - Write 2-3 behavioral plus 1-2 situational questions per scorecard competency with drill-down probes, from [references/interview-question-bank.md](references/interview-question-bank.md). Delete every brainteaser, "sell me this pen", "greatest weakness" and "are you coachable" - they have no demonstrated predictive value **[peer-reviewed + measured internal analysis at scale]**.
   - Assign each interviewer a competency, and keep the same interviewers and the same questions across all candidates for the role. Structure, not headcount, is what raises validity; panels add no validity over a single trained interviewer (peer-reviewed) - a panel's value is governance, not measurement.
   - Define the scoring mechanics now: every score needs an evidence quote, scores are submitted independently before any debrief, and the final number is combined mechanically with pre-set weights. The hiring manager decides within pre-committed thresholds.
   - If the user wants a personality assessment in the loop, apply the assessment rule below and load [references/assessment-validity-audit.md](references/assessment-validity-audit.md).
   - Run the compliance pass for the Q7 jurisdictions with [references/legal-landscape.md](references/legal-landscape.md): remove salary-history questions everywhere, publish the range, and flag any AI screening tool for bias-audit and high-risk-AI obligations.
4. **Artifact 3 - work-sample design + rubric.** Build from [references/mock-call-design.md](references/mock-call-design.md). Design a mock call where the candidate sells the user's product, not their own:
   - a prep pack sent ahead
   - a hard live scenario
   - one unscripted objection injected mid-call
   - one segment re-run after feedback (the coachability test, replacing the useless self-report question)

   Score on a behaviorally-anchored 0-3 rubric with 5-8 categories, frozen for a quarter, with frame-of-reference training for scorers. Score improvisation and adaptability, never polish. Match content to segment: cold call + objection handling for SDR/high-velocity/B2C, discovery depth + multi-threaded deal strategy + territory plan for enterprise.

5. **Artifact 4 - 30-60-90 ramp plan.** Build from [references/ramp-plan-template.md](references/ramp-plan-template.md).
   - Day 0-30: product/ICP/tooling training ending in a certification gate (a real exam, pass required); shadowing and sandbox mock calls.
   - Day 31-60: live activity with coaching, every call reviewed, first opportunities.
   - Day 61-90: self-sourced pipeline, first deals, forecast accuracy.

   Add:
   - a stepped quota ramp (25/50/75/100% over successive quarters)
   - a non-recoverable draw for AEs in months 1-3
   - a peer buddy distinct from the manager
   - check-ins in Situation-Behavior-Impact form

   Include the early-warning list and the action rule: a hire missing all three 90-day milestones (certification, coached improvement, self-sourced pipeline) needs a decision, not hope - involuntary exits cluster early and the productive window is short (survey).

6. Run the Quality gate below on all four artifacts. Iterate until it passes.
7. If your harness has persistent memory, store the scorecard, the frozen rubric, the loop design and the ramp milestones - later coaching and review sessions start from them. Without memory, tell the user to keep the artifacts as the canonical pack and re-supply them.

## Selection evidence

Two orderings govern the loop and they disagree, so never quote one as if it were the other. Validity says what an instrument buys; efficiency says what to build first with the hours available. Read `>` as "more of this axis"; the efficiency line is the build order.

Validities are corrected operational values (Sackett et al. 2022 correction, peer-reviewed; earlier figures were overstated).

- efficiency: structured interview > job-knowledge exam > reference check > cognitive test > work sample
- value: structured interview > job-knowledge exam > work sample > cognitive test > reference check
- effort: work sample > structured interview > job-knowledge exam > cognitive test == reference check (tied: nothing to build for either, under an hour to run)
- compliance cost: cognitive test > work sample > reference check > job-knowledge exam == structured interview (tied: content-valid instruments whose only exposure is the questions inside them - neither triggers an audit, a consent duty, or third-party data handling)

Rows sit in efficiency order, not validity order:

| Instrument              | Validity      | Build                                                                                                             | Run per candidate                                                                            | What the row costs                                                                                                                                                                  |
| ----------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Structured interview    | .42           | a week - bank, anchors, interviewer training                                                                      | an hour per interviewer                                                                      | Highest validity, and the week is reused by every later hire. Validity climbs with structure (.20 unstructured to .57 highly structured), so the build is what buys the coefficient |
| Job-knowledge exam      | .40           | a week to write                                                                                                   | near-zero, self-marking                                                                      | Your own product cannot be tested pre-hire, so this lands as the day-30 certification gate (Artifact 4) - it buys a ramp decision, not a hire decision                              |
| Reference check         | ~.26 or lower | near-zero                                                                                                         | an hour per finalist                                                                         | Cheap and honest about what it is: a fraud and claim check. Never weight it like an interview or work sample                                                                        |
| Cognitive test          | .31           | near-zero, off the shelf                                                                                          | near-zero                                                                                    | The cheapest row, and the reason cheapness must not lead: near-useless against objective sales (caveat below) and the heaviest compliance load of the five                          |
| Work sample (mock call) | .33           | a week to design, then a standing job - quarterly rubric refresh, frame-of-reference recalibration per new scorer | an hour x two scorers, plus candidate prep hours that cost drop-off and days of time-to-fill | Lowest ratio here, mandatory anyway. Lower adverse impact than cognitive tests, though that gap is overstated in incumbent samples                                                  |

**Deleted from the menu, not ranked last: biodata (empirically keyed), .38 (peer-reviewed).** Empirical keying needs outcome data on hundreds of past hires; no team at Q1 (a)-(c) has it, and a demoted row would silently return as scope.

**What the efficiency order starves: the work sample.** It carries real validity, and it is the only "can do" check in the loop. It is simultaneously:

- the priciest instrument to build
- the only one needing continuous upkeep
- the only one spending the candidate's hours

So a ratio buries it every round. Promote it to first build anyway when any of these hold:

- this is the first sales hire, so no incumbent benchmark exists to calibrate an interview against
- the loop keeps passing candidates who interview well and miss quota
- Q9 answered compounding, which amortizes the build across every future hire

**Default:**

- build the structured interview, then the work sample
- run reference checks on finalists only
- leave the job-knowledge exam in the ramp

Add a cognitive test only with a commitment to validate it against objective sales outcomes, which is a quarter's work on data most teams do not have.

Sales-specific caveat (peer-reviewed): cognitive ability correlates .40 with supervisor ratings but only .04 with objective sales results - it predicts what managers think of reps, not what reps sell. Achievement/conscientiousness shows the inverse pattern (.41 against objective sales), making it the more trustworthy signal to weight. Validate any gate against objective sales outcomes, not performance reviews.

Combine scores mechanically: formula-based combination predicts at .44 versus .28 for experts blending impressions in their heads - holistic judgment burns up to half the validity (peer-reviewed). This is the one choice in the skill needing no ratio: mechanical combination is both the higher-value option and the cheaper one - a weighted sum against an hour of argument. Implement it through independent scoring before the debrief: the loudest voice in the room cannot anchor scores that are already submitted.

**Re-rank before using any ordering above.** Every one is a default, not a law, and each shifts with context and with who executes it:

- a trained interview panel already in place drops the structured interview's build toward zero and moves the work sample to first
- no recruiter turns every hour in the table into the hiring manager's own hour, which shortens the loop and promotes the cheap rows
- a first hire has no top-performer data, which is what promotes the work sample; a thirtieth hire has it, which is the only condition that puts empirical keying back on the menu

**Assessment rule:**

- Treat any commercial sales-personality assessment as unvalidated unless it appears in the Buros Mental Measurements Yearbook with published peer-reviewed criterion validity.
- Never let any assessment gate or veto a candidate.
- Vendor "predictive validity" claims above ~.55 are marketing, not psychometrics - genuine criterion validities rarely exceed .50 even for the best predictors.

The named-vendor audit lives in [references/assessment-validity-audit.md](references/assessment-validity-audit.md).

## B2B and B2C

The shared foundation is identical across enterprise B2B, high-velocity inside sales, and B2C/consumer - no segment gets a pass on rigor because its loop is shorter:

- the written scorecard
- structured interviews
- the scored work sample
- independent scoring before the debrief
- mechanical score combination
- the banned-question list
- the legal constraints

Where the segments genuinely diverge - not ranked, deliberately: Q5 selects the column, so these are a lookup rather than a menu, and ordering options the user cannot choose between would be false precision.

| Dimension           | Enterprise B2B                                                                | High-velocity inside sales                      | B2C/consumer                                                                                              |
| ------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Loop length         | 5-6 stages, several weeks; invert the funnel for scarce talent                | 3-4 stages, days to ~2 weeks                    | 2-4 stages, days; speed wins candidates                                                                   |
| Work-sample content | Mock discovery, multi-threaded deal strategy, territory/30-60-90 presentation | Mock cold call, objection handling              | Mock consumer call end-to-end (the call is often the whole deal), objection handling, script adaptability |
| Predictor weighting | Discovery depth, business acumen, stakeholder navigation                      | Activity resilience, coachability, drive        | Activity resilience, rejection tolerance, drive; compliance discipline where the product is regulated     |
| Comp split          | ~50:50 with large absolute variable                                           | Base-heavy at entry (new reps have no pipeline) | Often commission-heavy with a draw; expect higher washout - budget backfill                               |
| Sourcing            | Proactive headhunting of a small mapped list                                  | Inbound, high-volume funnels, fast screening    | High-volume funnels, fast screening                                                                       |

Flag where the benchmarks come from when working B2C: the published ramp, tenure and attainment numbers skew North American B2B SaaS (survey). Present them to a B2C user as directional, not as their baseline.

## Quality gate

Score the four artifacts against all twelve checks before final delivery. Pass threshold: 12/12 - each check traces to a specific finding, so a miss is an evidence violation, not a style choice. Iterate until every check passes; report the checklist with the artifacts.

1. The scorecard has 3-8 outcomes, every one quantified and ranked (outcome-based scorecard method).
2. The role recommendation (SDR vs AE vs full-cycle) explicitly cites the user's ACV, cycle-length and inbound answers, including the empty-calendar rule where SDRs were requested.
3. Every interview question maps to a named scorecard competency and is behavioral or situational; the identical question set applies to every candidate (structured > unstructured, peer-reviewed).
4. Zero brainteasers, "sell me this pen", "greatest weakness", or "are you coachable" anywhere in the bank.
5. The scored work sample sits at stage 2 or 3 of the loop, never last.
6. The work sample sells the hiring company's product, injects one unscripted objection, and re-runs one segment after feedback as the behavioral coachability test.
7. The work-sample rubric is behaviorally anchored (0-3, 5-8 categories) and declared frozen for a quarter; any conversation-metric anchors are labeled as vendor data, correlational.
8. Interviewers submit independent, evidence-quoted scores before any debrief, and the final combination is mechanical with pre-set weights (mechanical > holistic, peer-reviewed).
9. No assessment gates or vetoes any candidate; any assessment in the loop is labeled per the assessment rule.
10. The posting content states a real base + OTE range; no salary-history question appears anywhere in the loop; jurisdiction flags from Q7 are addressed.
11. The ramp plan contains a day-30 certification gate, a day-60 coached-activity milestone, a day-90 self-sourced-pipeline milestone, a stepped quota ramp, and the missing-all-three action rule.
12. Every benchmark number in all four artifacts carries its evidence label, and no vendor claim is presented as fact.

## Common failure modes

Not ranked, deliberately: every row is a defect with one mandatory fix, and ordering defects by ratio would imply the bottom ones are optional.

| Failure                               | Fix                                                                                                                                  |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Hiring the all-around athlete         | Score narrow, deep competence against the 3-8 outcomes; an impressive-but-mismatched background is a mismatch                        |
| Coin-operated first hire              | For hire #1, weight builder traits over big-logo experience; the imported formula rarely survives contact with the company's motion  |
| Mock call run last                    | Move it to stage 2-3; apply the placement ordering in workflow step 3                                                                |
| Debrief-first scoring                 | Collect written independent scores before anyone speaks; the debrief calibrates, it never originates scores                          |
| One blended gut score                 | Per-competency scores with evidence quotes and mechanical combination; a single average hides the sticking point                     |
| Assessment as gate                    | Apply the assessment rule; unvalidated tools are color at most, and no tool vetoes alone                                             |
| "Competitive OTE", no range           | Publish base + OTE; vagueness filters out exactly the target candidates and violates pay-transparency rules in several jurisdictions |
| Adding SDRs to look grown-up          | Apply the empty-calendar rule; SDRs before AEs are at capacity just adds cost and handoff loss                                       |
| Day-1 overload in the ramp            | Spread orientation across week 1; deep work starts week 2                                                                            |
| Hoping past day 90                    | Missing all three 90-day milestones triggers a decision; late rescue attempts rarely beat the base rates                             |
| Cloning the team or the top performer | Weight the hire toward what the team is missing; different profiles add coverage, not risk                                           |
| Quota set from hope                   | Sanity-check quota against ramp benchmarks in the ramp reference; unattainable year-one numbers drive early regrettable attrition    |

## KPIs

Judge the hire - and this skill's output - after the fact with:

- **Ramp attainment vs the stepped schedule**: percent of the 25/50/75/100 quota steps hit on time, per cohort.
- **Time-to-productivity** vs role benchmarks (SDR ~3.2 months **[survey, 2025 ed.]**; AE 6.2 months, the highest recorded **[survey, 2026 ed.]** - an earlier edition of the same survey read 5.7; use the most recent edition available and treat older ones as trend context, not the baseline).
- **90-day milestone completion**: certification pass, coached-call improvement, self-sourced pipeline - tracked per hire.
- **Attrition, split regrettable vs involuntary**: SDR total attrition averages 39%, nearly two-thirds involuntary, worse below $20M revenue (survey); involuntary exits clustering early usually indict the loop, regrettable exits the ramp or the manager.
- **Loop process KPIs**: time-to-hire vs role norms (SDR 21-35 days; enterprise AE 45-70+ days, practitioner estimate), stage-to-stage drop-off, offer-accept rate.

If you can browse the web or query current market data, refresh comp ranges and ramp benchmarks before quoting them; otherwise label every figure with its edition year and tier, and tell the user to verify locally.

Compensation and legal content in this skill is informational, not legal advice - have counsel and HR review postings, assessment use, and any offer language, especially commission/OTE and guaranteed-vs-variable pay terms.

## Reference

- See [references/scorecard-template.md](references/scorecard-template.md) for the scorecard structure, worked SDR and AE examples, and segment weighting.
- See [references/interview-question-bank.md](references/interview-question-bank.md) for the banned list, per-competency question banks, and the debrief scoring form.
- See [references/mock-call-design.md](references/mock-call-design.md) for the scenario design, the 0-3 rubric with labeled anchors, and anti-gaming countermeasures.
- See [references/ramp-plan-template.md](references/ramp-plan-template.md) for the full 30-60-90 template, certification gates, and ramp benchmarks.
- See [references/assessment-validity-audit.md](references/assessment-validity-audit.md) for the named-vendor validity audit behind the assessment rule.
- See [references/legal-landscape.md](references/legal-landscape.md) for the 2026 jurisdiction-by-jurisdiction compliance table.
- See `mbfinotti/sales-skills@sales-career` for the candidate's side of this table - interview prep, positioning, progression; this skill never coaches candidates.
- See `mbfinotti/sales-skills@sales-comp-design` for the OTE and pay mix an offer positions, and the draw schedule that backs the ramp period.
- See `mbfinotti/sales-skills@sales-org-structure` for the org design that decides which seats exist before recruiting into them - role mix, SDR-to-AE ratio, and management spans.
- See `mbfinotti/sales-skills@sales-quota-setting` for the ramp-relief schedule the 30-60-90 plan's quota expectations key off - this skill sets the certification gates, that one sets what the rep carries at each stage.
- See `mbfinotti/sales-skills@sales-call-review` to score the new hire's live calls during ramp with the same evidence-quoted discipline.
- See `mbfinotti/sales-skills@sales-objection-handling` for objection-handling craft useful when writing mock-call scenarios.
