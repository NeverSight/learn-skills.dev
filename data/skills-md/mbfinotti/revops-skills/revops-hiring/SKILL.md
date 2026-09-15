---
name: revops-hiring
description: Build the complete hiring packet for a RevOps or Sales Ops role - archetype and level decision, outcome scorecard, interview stage map with a competency question bank and anchored rating scales, a work-sample exercise with rubric and debrief, and a 30-60-90 ramp plan branched on seniority and archetype. For the hiring manager or founder recruiting the hire. Use whenever the user mentions hiring a RevOps manager, sales ops interview questions, a RevOps take-home exercise, a scorecard for a first ops hire, or a 30-60-90 for a new ops hire - even if they never say "hiring packet". Does not source candidates or post jobs. Do NOT use for a candidate's own interview prep - use mbfinotti/revops-skills@revops-career instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.7"
---

# RevOps Hiring

Build the packet a hiring manager needs to recruit a RevOps or Sales Ops person: role definition, interview loop, scorecard, work sample, ramp plan.

The frame is the scorecard tradition of Geoff Smart and Randy Street's _Who: The A Method for Hiring_ - a mission, 3-8 ranked measurable outcomes, then competencies. It applies to the archetypes practitioners actually recognize:

- RevOps Co-op's five career tracks: analyst, systems administrator, enablement, deal desk, project manager.
- Compressed for hiring into three profiles: systems, analyst, strategist.

Two decisions come before any packet exists:

- Whether to open a requisition at all rather than take a fractional operator or a scoped agency project.
- Which archetype - because most failed RevOps hires are an archetype mismatch, not a competence failure.

This is the hirer's side only. It does not source candidates, post jobs, or track applicants, and it reports published compensation bands with source and date as scoping input - it never writes offer letters or gives legal or HR compliance advice; those need HR/legal review.

The candidate side - preparing for and landing a RevOps role - is the mirror-image sibling `mbfinotti/revops-skills@revops-career`. Onboarding a _customer_ after closed-won is `mbfinotti/revops-skills@sales-to-cs-handoff`, a different job entirely.

## Interview

Ask before designing. One question per message; offer multiple-choice answers where possible. Skip anything already answered.

- What stage and size is the company? (a) pre-Series A / under 25 people, (b) Series A-B / 25-150, (c) Series C+ / 150+, (d) not venture-track - describe.
- What does the GTM team look like - roughly how many sales reps, marketers, and CS people?
- Is this the first dedicated ops hire, or joining an existing ops team? If existing: who is on it and what do they own?
- Which pain is driving the hire? (a) admin and ticket backlog - capacity, (b) nobody trusts the reporting or the forecast - analytics, (c) problems that cross team boundaries - process and alignment, (d) several of these.
- How mature is the stack? (a) CRM barely configured, (b) CRM plus marketing automation working but messy, (c) full GTM stack including a data warehouse and BI.
- What budget and level is the req funded at - and is that number negotiable if the market says it is too low?
- Who will this hire report to, and who is the executive sponsor?
- Who is on the interview panel, and how many rounds can you realistically run?
- By when must this be solved? (a) a dated event forces it inside a quarter - board meeting, quota reset, migration, (b) this fiscal year, (c) open. A hard date inside a quarter deletes the senior in-house options: the search alone outlasts the deadline.
- Do you want a one-off fix or a compounding capability? A one-off promotes fractional and agency; a compounding mandate promotes the in-house hire, and is the only answer that justifies its first two quarters.
- What is your effort ceiling - how many manager hours per week you have, whether panelists are available, whether headcount is actually approved, and whether you could unwind this in a month if it went wrong? A freeze or unapproved headcount deletes the requisition options outright; low tolerance for irreversibility promotes the contract ones.

## Workflow

1. Run the Interview; collect every answer before designing anything.
2. Decide whether to open a requisition at all, using the ranked profile-choice test in [references/role-archetypes-and-leveling.md](references/role-archetypes-and-leveling.md). By value returned per hour you spend: `fractional operator > scoped agency project > in-house specialist > in-house strategist`, with the in-house rows routed by pain - reporting-trust to the analyst, admin backlog to the systems specialist, cross-boundary process to the strategist - and pain confined to one function routed out of RevOps entirely to Sales, Marketing, or CS Ops. Delete the options the Interview answers rule out rather than ranking them last, and name which you deleted. Re-rank the rest against what you already know about this company: an agency already retained, an in-house recruiter, a fifth ops hire versus a first. Only an in-house outcome makes the rest of this workflow apply - then name the archetype and level in writing before drafting anything else.
3. Gate the req: lock the reporting line and a VP-or-C-level executive sponsor in writing - practitioners call sponsorship the single biggest predictor of first-hire success - and pressure-test the budget against the published bands in the same reference. Quote every band with its source and date. RevOps Co-op's warning applies: "It's better to fight for more money to hire an experienced professional than [to] work with the money you have and fail your new hire."
4. Write the role definition as a scorecard - one-line mission, 3-8 ranked outcomes with dates that are objective and observable, then competencies - and turn its must-haves into a requirements matrix. Sketch what "good" looks like even roughly; RevOps Co-op: "Your job is to sketch out what 'good' could look like - even if it's just a napkin drawing." Score experience level-relative - overqualified and underqualified both score low - and make a vendor certification a must-have only for a systems archetype at a company standardized on that platform. Requirements-matrix rules:
   - Write around problems, not tools.
   - Cap must-haves at 5-7 and weight them to sum to 100%.
   - Keep nice-to-haves as additive bonus points.
   - Hold disqualifiers in a separate checklist rather than as negative points inside the score.
5. Define 4-6 competencies and build the question bank from [references/competencies-and-question-bank.md](references/competencies-and-question-bank.md): 2-3 behavioral and 1-2 situational questions per competency with follow-up probes, domain failure modes as hard-to-fake probes, and red/green answer pairs as scoring anchors.
6. Map the loop as a stage table - stage, interviewer, competencies assessed - with each competency owned by exactly one stage and each panelist assigned a lane. Keep it tight: Matthew Volm (CEO, RevOps Co-op) argues for one roughly two-hour take-home and "keep it to 3 rounds max".
7. Fix the scoring discipline before anyone interviews. Write an anchored rating scale carrying a behavioral description of what each anchor point looks like for this specific role - a bare number is banned - and require every submitted score to cite evidence, a quote or a concrete example. Interviewers score independently before any discussion, disqualifying signals are recorded separately from the score, and the recommendation is weighted by confidence, not fit alone: "insufficient data" is a valid output, and no single score overrides the loop.
8. Design the work sample from [references/work-sample-design.md](references/work-sample-design.md). Pick the format from the ranked menu there - `live mock > paid take-home > unpaid take-home` on signal per hour spent, with the unpaid row carrying both the drop-off of your best candidates and a real compliance cost, and the eight-hour unpaid exercise deleted rather than demoted. Then build:
   - A prompt that looks like a real defect, not a project.
   - A hard time cap.
   - A rubric written before the first submission.
   - A debrief plan - the debrief carries more signal than the artifact.
9. Build the ramp plan from [references/ramp-plan-template.md](references/ramp-plan-template.md): pre-start, Day 1, Week 1, then 30/60/90 - branched on seniority and archetype, with the week-one access list, ticket-queue protection, honest milestone expectations, and closing watch areas.
10. Emit the packet (next section) section by section for user validation, grounding each section in the matching example from [references/worked-examples.md](references/worked-examples.md).
11. Iterate the packet until every item in Pass Threshold holds.
12. If your harness has persistent memory, memorize the approved packet - archetype, level, competencies, stage map, thresholds, ramp branches - so screening runs and the eventual ramp start from it instead of re-interviewing. Without memory, tell the user to keep the packet document as the standing input for future runs.

## The Hiring Packet

Deliver every engagement as this artifact. Fully worked versions live in [references/worked-examples.md](references/worked-examples.md).

```
HIRING PACKET - <company>, <role>, <date>, v<n>
Profile choice  : ranked options with the ordering stated | options deleted + why | recommendation
Role definition : archetype + level | mission | 3-8 ranked outcomes with dates | competencies
Requirements    : must-haves weighted to 100% | nice-to-haves as bonus | disqualifier checklist
Comp input      : published band quoted with source + date | flag: offer terms need HR/legal
Stage map       : stage -> interviewer -> competencies assessed (each owned by exactly one stage)
Question bank   : per competency - behavioral + situational + follow-up probes | red/green anchors
Scorecard       : anchored scale per competency | cited evidence per score | confidence rating
Work sample     : prompt + time cap + paid/unpaid call | rubric (written first) | debrief agenda
Debrief rules   : independent pre-scores | disqualifiers separate | confidence-weighted decision
Ramp plan       : pre-start, Day 1, Week 1, 30/60/90 | seniority + archetype branches |
                  week-one access list | watch areas
```

## B2B and B2C

The hiring process is identical across segments - scorecard, loop, work sample, ramp - and say so when asked. What genuinely changes is which competencies carry weight, which metrics the role owns, which stack the candidate must know, and what the interview probes.

- **B2B enterprise**: the role owns pipeline coverage, win rate, deal velocity, net revenue retention, forecast accuracy, territory and quota; the stack is CRM, sales engagement, revenue intelligence, CPQ - weight quote-to-cash depth, territory and comp design, and forecast-cadence judgment.
- **B2C and e-commerce**: the role owns CAC, conversion rate, average order value, purchase frequency, churn, and cohort-modeled LTV.
- **PLG**: activation, product-qualified leads, free-to-paid conversion, expansion signals - RevOps Co-op notes that in PLG "using funnel stages as a proxy for a team's effectiveness [becomes] nonsensical".

Directional vendor-report benchmarks for PLG, labeled directional and not authoritative:

- Activation: 25-40% of signups within 7-14 days.
- Free-to-paid: roughly 2-5% freemium, 15-25% free trial.
- PQL users convert around three times higher.
- Only about a quarter of PLG companies actually use PQLs.

PLG and consumer RevOps therefore demand analytics-engineering-adjacent skills - strong SQL, hands-on data-warehouse work, a transformation layer - and interviews should probe product-signal fluency over territory design.

- Deal desk is close to a B2B-only archetype; consumer subscription rarely has one.
- Its billing and payments complexity has no B2B analogue.
- Pure B2C subscription usually lacks the expansion pathway that pushes B2B net retention above 100%.

## Pass Threshold

Iterate until every item holds. Each item below is either sourced from practitioner guidance or this skill's own convention.

- Archetype and level are named in writing, and the reporting line plus executive sponsor are locked, before the role definition is drafted - no sponsor, no req (sourced).
- The role definition names problems and outcomes, not tools, and caps must-haves at 5-7 (sourced).
- 4-6 competencies; every question maps to exactly one; every competency is owned by exactly one interview stage (sourced).
- Every anchor point carries a role-specific behavioral description, and every submitted score cites a quote or concrete example (sourced); a bare number fails this check.
- The loop runs at most 3 rounds plus one take-home of about two hours, three-hour ceiling if unpaid (sourced).
- The work-sample rubric exists before the first submission; its numeric point values follow this skill's own convention.
- The ramp plan branches on both seniority and archetype, ends with watch areas, and sets the honest milestone timeline - early wins in 60-90 days, revenue-level outcomes at 12+ months (sourced).
- Every compensation figure in the packet carries its source and date; no invented bands, no figures for geographies the sources do not cover (self-set).
- Every option menu the packet presents - profile choice, work-sample format, question selection - states its ordering out loud, deletes ruled-out options instead of demoting them, and names one re-ranking against this company's own context (self-set).

## Common Failure Modes

Ranked by how much of this table each prevention removes, best ratio first: `committed executive sponsor > archetype diagnosis > stage map and independent scoring > defended ramp calendar`. The first two cost a conversation each and pre-empt the top four rows before the req opens; the rest are loop and onboarding discipline that only start paying once those two hold.

| Symptom                                                 | Root cause                                                       | Fix                                                                                                       |
| ------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Impressive hire, CRM cleaner, forecast still shaky      | Archetype mismatch - a systems admin hired for a process problem | Rerun the profile-choice test; the problem "was never the software; it was the revenue motion"            |
| Hire spends months in meetings, then quits              | Unclear mandate - three executives each think they own the hire  | Write the charter, outcomes, and single sponsor before the req opens                                      |
| Every improvement becomes a negotiation                 | No executive sponsor                                             | Do not open the req until a VP or C-level sponsor is committed in writing                                 |
| First 90 days eaten by the ticket queue                 | No defended calendar or mandate                                  | Protect ramp time explicitly; make ticket-queue capture a named watch area                                |
| Panelists all ask the same questions                    | No stage map                                                     | One competency, one stage; assign each panelist a lane                                                    |
| Debrief converges on the first confident voice          | Scores shared before being written                               | Independent scoring before discussion; spend debrief time where scores diverge                            |
| Strong candidate rejected over a missing certification  | Vendor cert set as a must-have                                   | Certs are table stakes, not predictors - nice-to-have unless systems archetype on a standardized platform |
| Polished interviewer, weak on the job                   | Loop rewards polish over method                                  | Work sample plus red/green method anchors; the weak and strong answers differ in method, not confidence   |
| Best candidates decline the take-home                   | Long unpaid exercise selects for uncommitted hours               | Cap at 2-3 hours, consider paying, and move the signal to the debrief                                     |
| Good hire pushed out at month six for no revenue impact | Unrealistic timeline                                             | Set honest milestones up front - "Anyone promising revenue impact in 30 days is selling you something"    |

## Invocation Examples

- "We're a 40-person Series A B2B SaaS, the CRM is a mess and nobody trusts the forecast - help me scope and hire our first RevOps person."
- "I have a RevOps analyst req open on an existing five-person ops team - build the interview loop, the scorecard, and a take-home that actually tests the job."
- "Our new Director of Revenue Operations starts in three weeks - write the 30-60-90 ramp plan."

## Reference

- Read [references/role-archetypes-and-leveling.md](references/role-archetypes-and-leveling.md) when diagnosing the archetype, picking the level, scoping a first hire versus an Nth hire, or pressure-testing the budget against published salary bands.
- Read [references/competencies-and-question-bank.md](references/competencies-and-question-bank.md) when defining competencies, writing questions and probes, or building the anchored scorecard and requirements matrix.
- Read [references/work-sample-design.md](references/work-sample-design.md) when designing the exercise - time and payment norms, synthetic-dataset construction, the grading rubric, and the debrief.
- Read [references/ramp-plan-template.md](references/ramp-plan-template.md) when writing the ramp plan - the pre-start-to-90-day skeleton with seniority and archetype branches and watch areas.
- Read [references/worked-examples.md](references/worked-examples.md) when shaping the deliverable - one full positive packet and one negative example with its cost spelled out.
- See `mbfinotti/revops-skills@revops-career` for the mirror-image candidate side - preparing for, positioning toward, and progressing in a RevOps role.
- See `mbfinotti/revops-skills@sales-to-cs-handoff` for onboarding a customer after closed-won - a different job this skill does not cover.
- See `mbfinotti/revops-skills@lead-scoring`, `mbfinotti/revops-skills@sales-forecast-diagnostic`, and `mbfinotti/revops-skills@pipeline-stage-definition-audit` for the domain depth behind the interview probes - the failure modes those skills fix are the material candidates are probed on.
