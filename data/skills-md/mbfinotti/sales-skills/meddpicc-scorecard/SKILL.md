---
name: meddpicc-scorecard
description: Scores one deal against the eight MEDDPICC elements on an evidence ladder - unknown, assumed, stated, validated - with a scorecard, a verdict band, and the single next action that closes the biggest gap. Full MEDDPICC for complex deals, a lightweight subset for small ones, covering B2B and considered high-ticket B2C. Use whenever the user mentions MEDDPICC, MEDDIC, BANT, deal qualification, "score this opportunity", "is this deal real", or deal-review prep, even without naming a framework. Do NOT use for stakeholder mapping (mbfinotti/sales-skills@deal-champion-mapping), note-level risk scanning (mbfinotti/sales-skills@deal-red-flags), or transcript grading (mbfinotti/sales-skills@sales-call-review).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.9"
---

# MEDDPICC Scorecard

Score one described deal against the eight MEDDPICC elements and say plainly what is missing, what is assumed rather than validated, and what the rep should go validate next.

The largest field study available (Ebsta x Pavilion 2023 benchmark, 3.2M opportunities across 364 companies) found:

- 61% of methodology-adopting companies chose MEDDPICC.
- Only 15% of opportunities were fully qualified.
- Only 5% of companies scored confidence per criterion.

The acronym is everywhere; the discipline is rare - that gap is "MEDDPICC theatre", and this scorecard is built to prevent it.

The whole scorecard runs on one axis: **evidence, not presence**. A letter is never scored on whether the rep can name something; it is scored on whether the buyer has done something observable to prove it.

The skill scores one deal at a time, gathers no new information itself, and grades only what the user reports, then tells them what to go validate next.

Two confidence distinctions run throughout and belong in the output:

- Whether a rule is published by the methodology or set by this skill.
- Whether a figure is an independent measurement or a **vendor claim**, a vendor's own correlational number never independently replicated.

## Interview

Ask questions under these constraints:

- One question per message.
- Multiple-choice answers wherever possible.
- Skip anything the deal description already answers.

Two rounds:

Deal frame (right-sizing inputs, always first):

1. B2B, or considered high-ticket B2C (real estate, automotive, solar, remodel, private education, financial advisory - not impulse retail)?
2. Rough deal size (contract value or ACV), and how many people on the buying side are involved?
3. What stage is the deal at, how long has it been open, and who set the expected close date - the buyer or the rep?
4. Does the buyer's side involve formal procurement, security review, or legal redlines?
5. Does your team mandate its own MEDDPICC definitions or scale (second C, Implicate vs. Identify, weighting)? If yes, use theirs and note the mapping in the output.
6. By what date must this scorecard change something - this week's forecast call, the next deal review, or nothing dated?
7. Do you want a one-off read on this deal, or a re-scored record that compounds across reviews?
8. What is your effort ceiling before that date: how many buyer asks you can make, and how much of your champion's internal credit you can spend?

Questions 6-8 re-rank the next actions, not the scoring; which answer moves which action is in Closing the biggest gap.

Evidence collection (only for elements that survive right-sizing), one element per message:

9. For this element: what do you know, and what buyer-side artefact or event backs it - an email, a recorded call, a document you have seen, an intro that was made, a date or number the buyer supplied? "The buyer seems positive" is an answer; it scores accordingly.

## Workflow

1. Run the deal-frame interview questions before any element questions.
2. Right-size (next section). Confirm the element list with the user before scoring anything.
3. Collect, per scored element, the rep's claim and the buyer-side evidence behind it.
4. Score each element on the 0-3 evidence ladder (Scoring section).
5. Challenge every 2 and 3: which artefact or event justifies it? No artefact named → drop the score to 1 and record why. Apply this anti-inflation rule without exception - self-scoring optimism is the documented failure the rule corrects - score levels need objective definitions, or an optimist and a pessimist grade the same deal differently.
6. Apply the two gates, compute the total, band the deal.
7. Name the single biggest gap: a failed gate first; otherwise the gap that buys the most verdict change per unit of effort (Closing the biggest gap).
8. Attach a next action to every element below 3, ordered by that same ratio. Single out the top one, phrased as a buyer-visible test - an ask the buyer either performs or refuses, so the answer is evidence either way.
9. Run the Quality gate; iterate until it passes.
10. Deliver the scorecard using [references/scorecard-template.md](references/scorecard-template.md).
11. If your harness has persistent memory, store the scorecard, its date, and each score's justifying artefact so the next run can re-score and show deltas - deals decay, so re-score at every deal review. Otherwise, end with a short recap the user can paste into their own deal record.

If you can browse the web, you may verify public facts a score depends on (the named Economic Buyer still holds the role; the competitor cited still sells the product); otherwise rely on the user's report and mark those facts "user-reported".

## Right-size before scoring

Full MEDDPICC on every deal is over-engineering; scoring the wrong list is the first inflation. Which letters survive is itself a ranked menu - what scoring the letter costs against the verdict information it returns:

- value on a small deal (verdict change per letter scored): Champion > Implicate the Pain == Metrics > Decision Process > Competition > Decision Criteria > Paper Process
- effort (rep time plus the buyer questions the letter costs, most expensive first): Paper Process > Decision Process > Decision Criteria > Competition > Metrics == Implicate the Pain == Champion

Drop from the low-value, expensive end inward: Paper Process leaves first (the first element dropped in lightweight practice), then Decision Criteria, then Competition.

- Pain == Metrics: they are one answer from two directions: the costed consequence and the number the buyer owns arrive in the same sentence.
- Metrics, Pain and Champion tie at the cheap end and never drop: on a small deal each is a single question, and any two of them are unreadable without the third.
- Economic Buyer sits on neither line: it is a gate, and on small deals it merges into Champion instead of being dropped.

Fit bands:

- Roughly $100K+ contract value, 5+ stakeholders, formal procurement/security/legal path: score all 8.
- ~$25K-$100K, 2-5 stakeholders: drop Paper Process, unless procurement is known to be involved.
- Below ~$25K, 1-2 deciders, no procurement: Metrics + Implicate the Pain + Champion, adding Decision Process if any multi-step approval exists. Here the Economic Buyer and Champion usually collapse into one person - score them as one letter and say so.
- High-ticket B2C: see the B2B and B2C section; right-size aggressively.

Never score an element that was right-sized out; the denominator shrinks with the element list, and a dropped element earns no next action either.

## The eight elements and their evidence bar

| Element            | What it means (this skill's chosen definition)                                      | Validated (3) looks like                                               | Assumed (1) looks like                                  |
| ------------------ | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------- |
| Metrics            | The quantified outcome the buyer expects, as a number they own                      | A figure the buyer supplied in their own words                         | "They want efficiency"; a rep-built ROI never confirmed |
| Economic Buyer     | The one person with discretionary spend authority and veto                          | A held meeting with the named EB confirming the case                   | "My contact says the CFO is on board"                   |
| Decision Criteria  | The technical, economic, and relationship standards used to compare options         | Criteria the buyer wrote down or confirmed, proof mapped               | A feature list or RFP sheet treated as neutral criteria |
| Decision Process   | Who decides what, in what order, by when (technical validation + business approval) | A mutual action plan the buyer co-edited                               | A close date the rep invented; "they said Q3"           |
| Paper Process      | Everything between verbal yes and signature: legal, procurement, security           | A mapped path with named owners and timelines                          | "Procurement is just a formality"                       |
| Implicate the Pain | The problem made costed and owned; the cost of inaction                             | Buyer states the specific costed consequence of not solving            | A surface pain with no cost attached                    |
| Champion           | Power + personal stake + sells internally when you're absent                        | The contact has acted: EB intro, shared criteria, presented internally | A friendly contact who hasn't and maybe can't act       |
| Competition        | Every alternative: rivals, internal build, other initiatives, inertia               | Buyer articulates the alternatives; a win plan positions against each  | "We're the only one they're looking at"                 |

Contested definitions - this skill's positions, to be overridden by the user's team standard when one exists:

- The second C is Competition, including inertia/do-nothing (the methodology publisher's official position); some teams use Compelling Event or Closing instead.
- A compelling event is a thread running through every element, not its own letter; its honest absence is deal intelligence, never something to manufacture.
- Pain means Implicate the Pain: identify the problem, indicate its broader impact, implicate the buyer in the costed consequence.
- The optional "P for Partner" variant is not scored here.

Per-letter evidence exemplars, red flags, and the questions that move a letter up the ladder are in [references/element-evidence-bar.md](references/element-evidence-bar.md) - read it before scoring.

## Scoring

The evidence ladder, per element:

| Score | RAG   | Label     | Bar                                                                                                 |
| ----- | ----- | --------- | --------------------------------------------------------------------------------------------------- |
| 0     | Red   | Unknown   | No information at all                                                                               |
| 1     | Red   | Assumed   | The rep believes it; no buyer-side evidence                                                         |
| 2     | Amber | Stated    | The buyer said it - in a meeting, call, or email                                                    |
| 3     | Green | Validated | The buyer demonstrated it: an intro made, a document seen, a date committed, a number they supplied |

Where the scale comes from: the red/amber/green convention comes from Andy Whyte's book, confirmed as the book's own core scoring mechanism rather than one option among several. The 0-3 evidence ladder is a documented practitioner variant rather than official methodology doctrine, and this skill adopts it and defines each rung precisely above. Per-letter weighting is configurable and practice-dependent, never canonical - this skill weights all elements equally and says so in the output; if the user's team weights differently, use theirs.

Aggregate: total = sum of element scores; percentage = total / (3 × elements scored). Bands:

- **≥80% and both gates passed - Forecast-ready.** Evidence supports committing the deal (anchor: a documented practitioner threshold of 20+/24). Still re-score at every review.
- **55-79% - Real but gapped.** The deal is live but not commit-grade; work the listed gaps before forecasting it.
- **30-54% - Under-qualified.** Not forecastable. Late-stage deals in this band are a coaching trigger (a documented sub-16/24 late-stage trigger).
- **<30% - Not qualified.** Re-qualify from discovery or disqualify. Disqualification is a valid outcome of this skill, not a failure.

Gates - two letters cap the verdict regardless of total. The emphasis on both letters is the methodology's; the cap mechanic is this skill's, not published doctrine:

- Champion ≤1 → verdict capped at Under-qualified. "No Champion, no deal".
- Economic Buyer = 0 → verdict capped at Under-qualified. A champion unwilling or unable to introduce the EB is a major red flag that also questions whether the champion is real.

Place borderline scores with the sourced maturity ladders:

- Metrics: M1 (outcomes delivered for other customers) → M2 (personalized to this prospect) → M3 (validated post-go-live). A buyer-confirmed M2 scores a 3. A recited M1 scores a 1.
- Champion: Contact → Coach → Champion.
- Economic Buyer: unknown → Access (intro committed, not held) → Sponsorship (met, case confirmed). Access scores a 2. Sponsorship scores a 3.

Never present vendor outcome claims ("18% higher win rates / 24% larger deals / 26% shorter cycles", "forecast accuracy to 95%") as expected results - unreplicated vendor claims; the quarantine list is in [references/vendor-claim-quarantine.md](references/vendor-claim-quarantine.md).

## Closing the biggest gap

Every element below 3 generates a next action, and they all compete for one scarce thing: the asks this rep can make of this buyer before the next checkpoint. Rank them by verdict change bought per unit of effort.

Effort here is never money. It is:

- Rep hours.
- Calendar latency.
- How much of the champion's internal credit the ask spends.
- Whether a refused ask can be re-asked.

The eight candidate asks:

- Champion test
- EB meeting
- Pain cost
- Buyer's metric
- Decision-process plan
- Criteria write-down
- Paper-process map
- Do-nothing probe

The ordering below is this skill's, not published doctrine; effort is stated as orders of magnitude rather than figures.

- value (how much closing it moves the band): champion test > EB meeting > pain cost == buyer's metric > decision-process plan > paper-process map > do-nothing probe > criteria write-down
- effort (most expensive first): EB meeting > paper-process map > decision-process plan > criteria write-down > champion test == pain cost == buyer's metric == do-nothing probe
- efficiency (the default order to work): champion test > pain cost == buyer's metric > do-nothing probe > decision-process plan > criteria write-down > EB meeting > paper-process map

Magnitudes, never figures:

- Near-zero: champion test, pain cost, buyer's metric, do-nothing probe - one question on a call already in the diary.
- An hour to draft plus a week waiting for the buyer to return it: decision-process plan, criteria write-down.
- A week and a second introduction: paper-process map.
- A week or more of calendar, plus the champion's credit to arrange it, and it cannot be un-asked: EB meeting.

The champion test leads on value because it is the ask that produces the others: a champion who acts books the EB meeting, and one who refuses is a coach, which caps the deal anyway. The four near-zero asks tie on effort because none needs a new meeting, a new document, or a second introduction.

What this order starves: the EB meeting and the paper-process map. The two highest-value asks in the deal sit at the bottom of the efficiency line every round, because the element that most changes the verdict is usually the most expensive to validate. Promote them anyway when:

- Economic Buyer scores 0. The gate caps the verdict, so no other validation can lift the band - the EB meeting goes first regardless of ratio.
- The deal is late-stage, procurement is known, or a verbal yes is close. The paper-process map goes first; after the yes it is no longer a cheap fix, it is a stall.

Delete, never demote:

- An element right-sized out has no next action at all.
- An effort ceiling that forbids spending the champion's credit removes the EB meeting and the procurement introduction from the menu, rather than parking them at the bottom where they silently return as scope.
- A team standard that replaces the second C with Compelling Event deletes the do-nothing probe with it.

Say in the scorecard which asks you deleted and why.

Re-rank on what you already know, and record which answer moved which ask:

- A checkpoint inside the week (interview Q6) promotes the near-zero asks and demotes the EB meeting and the paper-process map - neither lands in time.
- A compounding record (Q7) promotes the decision-process plan and the paper-process map; both leave an artefact that keeps scoring at every re-score, which a one-off answer does not.
- A ceiling of one buyer ask (Q8) collapses the menu to the top of the efficiency line.
- A champion who has already acted once makes the EB meeting far cheaper than this order assumes - promote it.
- A team-mandated methodology or weighting (Q5) overrides the ordering outright; use theirs.

This order is a default, not a law. It shifts with the deal and with who executes it: a rep with a standing relationship to the economic buyer pays near-zero for a meeting that costs a first-year rep a week and a favour.

## Invocation and expected output

Typical invocations:

- "Score this deal against MEDDPICC: 200-seat rollout at a logistics company, $180K ACV, proposal stage - here's what we know."
- "MEDDPICC check before Thursday's deal review. Ask me your questions one at a time."
- "Is this deal real? Single-founder buyer, $9K contract, says he'll sign this month."

Deliver one scorecard (full fill-in template in [references/scorecard-template.md](references/scorecard-template.md)):

```
MEDDPICC SCORECARD - <deal>, <date>, elements scored: <list>
Per element  : score 0-3 + RAG, the claim, the evidence artefact
               (or "none - score dropped"), the next action and what it
               costs, best ratio first
Gates        : Champion / Economic Buyer status; cap applied or not
Total        : X/<max> (NN%), band, one-line verdict in forecast terms
Biggest gap  : one element, why it beat the others on verdict change per
               unit of effort, and the buyer-visible test that closes it
Deferred     : the high-value asks the order starved, what would promote
               them, and any ask deleted by a constraint
Challenged   : every score knocked down, and why
Definitions  : second-C / Pain choices used; weighting (equal by default)
Re-score     : the event or date that triggers the next scoring pass
```

## B2B and B2C

- MEDDPICC is B2B-native: its own publisher positions it for mid-market and enterprise B2B, and consumer selling is outside the methodology's stated scope. Everything below about B2C is a structural analogy rather than established practice; say so in every B2C scorecard you produce.
- Identical in both, explicitly:
  - The evidence axis.
  - The 0-3 ladder.
  - The anti-inflation rule.
  - The gates.
  - The workflow.
  - The quality gate.
  - Only the cast changes.
- High-ticket considered B2C mapping, all of it analogy:
  - Economic Buyer → whoever controls the money and holds veto: spouse or partner, a financing parent, the lender whose approval gates the purchase.
  - Champion → the enthusiastic household member selling the skeptical one when the salesperson is absent.
  - Decision Process → who must agree, in what order: viewing, inspection, second opinion.
  - Paper Process → financing approval, inspection, appraisal, contingencies, closing.
  - Competition → rival options plus the powerful "do nothing / wait".
  - Metrics → quantified household stakes: monthly payment, resale value, energy savings.
  - Pain → the costed and emotional price of the status quo.
- Right-size B2C aggressively: usually Metrics + Pain + Champion + Paper Process as financing; a full eight-letter scorecard on a household purchase is process theatre. Paper Process is the one letter that inverts the drop order here - an unstarted loan application, not an unmapped procurement path, is what actually stops a household purchase, so the starved ask is promoted by default in B2C.
- A worked B2C adaptation is in [references/worked-examples.md](references/worked-examples.md).

## Quality gate

Score the drafted scorecard against all nine checks. Pass threshold: 9/9. Iterate - fix and re-check - until nothing fails.

1. Every scored element carries a claim, a score, and either a named artefact/event or an explicit "none".
2. No 2 or 3 stands without its artefact; every knocked-down score appears under Challenged with the reason.
3. The element list matches the right-sizing decision, and the denominator matches the element list.
4. Both gates were checked; any cap applied is stated in the verdict line.
5. The biggest gap is exactly one element; the scorecard says why it beat the others on verdict change per unit of effort, or which promotion condition overrode the ratio; and its next action is a buyer-visible test, not rep homework ("update the deal record" fails; "ask the champion to book the EB meeting this week" passes).
6. Every element below 3 has a next action, ordered by that same ratio, with the starved asks named under Deferred; no action is attached to a 3.
7. The band's meaning is stated in forecast terms, not as a grade.
8. The chosen definitions (second C, Pain) and the weighting are stated, with a note to align with the team's own standard if one exists.
9. Every rule the scorecard leans on is marked as published methodology or as this skill's own, and no vendor claim appears as an expected outcome.

These nine checks are deliberately unranked: the threshold is 9/9, so there is no first one to run and no last one to skip, and an order here would only invite trading one away.

## KPIs and measurement

- Per deal, the scorecard worked if:
  - At least one score was knocked down for missing evidence.
  - The top next action is a buyer-visible test.
  - Re-scores move - a score that never changes usually means nobody talked to the buyer that week.
- Across deals, the measures are ranked too - value is how much a measure can prove the rubric wrong, effort is how long you wait before it says anything:
  - value: band vs. realized outcome > commit-to-close forecast accuracy > no-decision loss rate > slipped-deal count
  - effort: band vs. realized outcome > commit-to-close forecast accuracy > slipped-deal count == no-decision loss rate
    Slippage and no-decision rate tie at near-zero because both are already columns in any pipeline report. Read them weekly, but they only ever hint.

    Band vs. realized outcome is the starved measure - a standing job that pays out only after a full quarter of closed deals - and the sole one that can falsify the rubric, so instrument it from day one anyway. Late-stage slippage bleeds win rate fast (as relative lifts).
- Adoption check: if scorecards get filled but forecast accuracy does not move, the evidence definitions are too loose. That is MEDDPICC theatre - fields completed to satisfy a manager rather than to qualify - the exact documented failure this skill exists to prevent.

## Common failure modes

| Failure                                                                                  | Fix                                                                                                                                  |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Happy ears - buyer politeness read as validation                                         | Demand the artefact; politeness is not an event                                                                                      |
| Self-scoring inflation - optimism graded as evidence                                     | The anti-inflation rule: no named artefact, no 2 or 3                                                                                |
| Presence, not evidence - "we have a champion" scored green                               | Score what the person has done, not that they exist                                                                                  |
| Coach mistaken for champion                                                              | Test with an ask - EB intro, internal criteria, presenting to the committee; hesitation means coach                                  |
| Feature list or RFP mistaken for decision criteria                                       | Criteria count only when buyer-confirmed and covering technical, economic, and relationship dimensions                               |
| Paper process discovered after the verbal yes                                            | Score it early on large deals; "procurement is just a formality" is a 1                                                              |
| Inertia ignored as competition                                                           | "Do nothing" is the most common winner; no do-nothing analysis caps Competition at 2                                                 |
| Score used as a report card, not an action generator                                     | Every gap gets a next action, ordered by verdict change per unit of effort; the real output is the ranked to-do list, not the number |
| Biggest gap picked on value alone - the EB meeting chosen the day before a forecast call | Rank by ratio, not importance; promote a starved ask only on its stated condition                                                    |
| Single-threaded deal scoring green                                                       | One contact supplying the evidence for every letter is itself fragility - flag it on the scorecard                                   |
| Over-qualifying small deals                                                              | Right-size first; all eight letters on a $9K single-decider deal is process theatre                                                  |

## Reference

- [references/element-evidence-bar.md](references/element-evidence-bar.md) - per-letter definitions, evidence exemplars, assumption red flags, ladder-climbing questions.
- [references/scorecard-template.md](references/scorecard-template.md) - the fill-in-ready scorecard.
- [references/worked-examples.md](references/worked-examples.md) - a full B2B enterprise scorecard, an annotated early-stage negative example, and a high-ticket B2C adaptation.
- [references/vendor-claim-quarantine.md](references/vendor-claim-quarantine.md) - the circulating MEDDPICC figures that are vendor marketing, and how to handle them.
- mbfinotti/sales-skills@sales-discovery-questions - generates the interview questions; this skill only grades what came back.
- mbfinotti/sales-skills@deal-value-calc - builds the ROI/business case behind Metrics; here the buyer's number is only checked as evidence.
- mbfinotti/sales-skills@sales-hiring - ramp acceleration via shared qualification language.
