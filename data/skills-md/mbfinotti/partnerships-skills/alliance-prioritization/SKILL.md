---
name: alliance-prioritization
description: Rank named candidate strategic alliances and technology partnerships by expected value, effort, and risk, to decide where partner-team capacity goes  - must-pass screens, a weighted alliance scorecard with sensitivity analysis, co-innovation and platform-dependency risk checks, a ranked shortlist, and a go/no-go recommendation memo. Covers B2B tech alliances and B2C brand and creator partnerships. Use whenever the user mentions alliance prioritization, partnership ranking, partner shortlisting, or asks which of several named partners deserves investment, even if they never say prioritization. Portfolio-level comparison only. Do NOT use for modeling one partner's P&L  - use mbfinotti/partnerships-skills@partner-economics instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.2"
---

# Alliance Prioritization

Rank specific, named candidate alliances and technology partnerships against each other, and decide which ones the team invests in. No single canonical ranking method owns this discipline - say so plainly rather than invent one. What the evidence actually supports:

- **A dedicated alliance function and structured process** is the field's best-validated success driver: 63% vs 50% alliance success across 1,572 alliances (Kale, Dyer & Singh, 2002). A repeatable prioritization process is part of that function.
- **Complementarity plus compatibility** is the best-validated fit construct: partners different in resources, similar in organizational institutions (Sarkar et al.; Mindruta, Moeen & Agarwal, 2016). Weight these highest.
- **Weighted scorecards are known-fragile machinery**: rank reversal (Belton & Gear, 1983) and arbitrary weights (Dyer, 1990). The fixes - justified weights, sensitivity analysis, must-pass gates kept outside the tradeable score - are mandatory here, not optional polish.
- The famous "50-70% of alliances fail" figure is unsettled: published estimates span 20-80% depending on how failure is defined, and one credible re-analysis puts it at 25-30%. Never quote it as settled fact.

## Interview

Ask before ranking anything. One question per message; offer multiple-choice options; skip whatever the user already answered.

- How many named candidates, and who are they? (Categories instead of names → the ecosystem sibling; a single candidate → the economics sibling.)
- What strategic goal must the ranking serve: pipeline, product-gap fill, market entry, retention, platform presence, brand reach?
- How many alliances can the team actually run - headcount, current load per alliance manager? This number becomes the shortlist cut line.
- What does the existing alliance portfolio look like: active alliances, concentration, redundancy or conflict with the candidates?
- What data exists per candidate: account-overlap data, closed-won history, integration usage, marketplace co-sell records, prior-relationship history?
- Any candidate that is politically protected - an executive relationship, board pressure, a prior tie? Name it now; it gets scored like the rest, visibly.
- Who signs off, and does a gate process or steering committee already exist?
- B2B tech alliances, B2C brand/creator partnerships, or a hybrid list?
- By what date must this ranking land - a board slide next week, a signed alliance this quarter, next year's plan?
- One-off win or compounding asset: a shortlist for this decision only, or a scorecard the team re-runs every portfolio review?
- What is the effort ceiling on the analysis itself - analyst hours available, whose data you can request, whose sign-off you can spend?

Those last three re-order the method choices in Brainstorming the ranking, so ask them before proposing any criteria set.

- A near-term date promotes the speed-to-first-value criteria set and staged gates.
- A compounding mandate promotes the complementarity-led set and segmented weights that survive re-use.
- An effort ceiling under about a day removes the scorecard entirely - rank on gates plus effort-to-first-value and say that is what you did.
- The goal answer carries the same weight: a product-gap or market-entry goal reserves capacity for a deep co-innovation candidate that value-per-effort would otherwise starve.

## Workflow

Every method choice - criteria set, weight distribution, gate strictness, where the capacity line falls - is ranked with its trade-off in Brainstorming the ranking. Open the relevant menu at the step that needs it, put its default and the runner-up to the user, and wait. Never let an assumption harden into the ranking unstated.

1. Run the Interview. Confirm the input is two or more named candidates and one stated strategic goal.
2. Fix the capacity number before scoring anything. A ranking without a cut line decides nothing - every candidate just gets a flattering ordinal.
3. Pre-filter each candidate with the ally-versus-acquire-versus-build test (Dyer, Kale & Singh, 2004): confirm an alliance is even the right mode for the synergy sought. Wrong-mode candidates leave the list here.
4. Run the must-pass gates, staged by default - desk checks across the whole longlist, expensive reviews on survivors only: financial viability, security/compliance posture, legal exposure, brand safety for B2C, and the Gomes-Casseres three-laws screen. A gate failure removes the candidate - a strong logo can never buy its way past a gate. See [references/risk-and-dependency-screens.md](references/risk-and-dependency-screens.md).
5. Build the scorecard for survivors: criteria anchored on resource complementarity and organizational compatibility, weights individually justified in writing, never default-equal. Use account-overlap data as one capped input, not the ranking spine. See [references/scoring-criteria-and-weights.md](references/scoring-criteria-and-weights.md).
6. Score effort alongside value: integration cost, enablement load, alliance-manager hours. Rank candidates on `value ÷ effort > value composite > logo attractiveness` - say that ordering in the memo, because the value column alone is what the room will read otherwise.
7. Score risk explicitly per candidate: relational vs performance risk (Das & Teng), co-innovation and adoption-chain risk (Adner's Wide Lens), and platform-envelopment risk for any candidate whose platform you would build on (Eisenmann, Parker & Van Alstyne).
8. Run the sensitivity analysis: shift each weight ±20% and re-rank. Report which rank positions survive and which flip - a ranking that only holds under one weight set is an opinion wearing a spreadsheet.
9. Draw the capacity line where the summed effort estimates exhaust available alliance-manager months, falling back to the raw headcount number when candidate efforts are comparable. Spend any co-innovation slot reserved before scoring inside that budget, never on top of it - see What the ordering starves. Everything above the line is the shortlist; everything below gets an explicit verdict - hold, recycle, or kill - with a re-entry trigger.
10. Draft a light business case per shortlisted candidate: joint value hypothesis, first-value milestone, effort estimate, risk summary. Deep unit economics hand off to the economics sibling.
11. Where both sides can be convened, pressure-test the top candidates in a joint value proposition workshop; a candidate that cannot articulate joint customer value fails here regardless of score. See [references/gates-and-governance.md](references/gates-and-governance.md).
12. Present the deliverable section by section - gates, scorecard, ranking, sensitivity, shortlist, verdicts - and validate each with the user before drafting the next. Revise on pushback.
13. Issue go/no-go verdicts per candidate - go, conditional-go, recycle, hold, kill - and require explicit user approval of the full memo before finalizing.
14. Check the pass threshold below; iterate the criteria, weights, or gates until every check holds.
15. Set the portfolio review cadence and re-ranking triggers: a candidate's acquisition, a platform policy change, a gate-milestone slip, a new entrant. Rankings decay; date the next review.
16. If your harness has persistent memory, memorize the approved ranking, the weights and their justifications, and each go/no-go verdict so later runs and portfolio reviews start from them.
17. If you can browse the web, verify each candidate's current state - ownership, funding, platform policies, recent incidents - before finalizing; stale candidate facts are a leading cause of dead-on-arrival shortlists. Otherwise flag candidate facts as user-supplied and unverified.

## Brainstorming the ranking

Enter brainstorming mode before scoring anything - never open with a finished table. Run it the way alliance teams actually run candidate selection: a gated debate, not a single answer.

- Ask one question per message throughout; never batch questions.
- Widen the longlist before narrowing it. Source candidates from customer data, overlap reports, marketplace neighbors, and competitor partner directories - inbound requests enter the list but never rank on enthusiasm alone.

### Method choices, ranked

The same discipline the scorecard applies to candidates applies to the method: rank by decision quality bought per analyst hour, never by what is cheapest to run. Open the relevant menu at the step that needs it, put the default and the runner-up to the user with the trade-off, then wait.

**Criteria set** - default: complementarity-led.

- **Complementarity-led**: resource complementarity and organizational compatibility anchor the weights. Costs an hour of criteria design, scored from desk research and closed-won samples the team already holds. Buys the only fit construct with peer-reviewed support, and the ranking most likely to survive the sensitivity re-run.
- **Speed-to-first-value-led**: weights integration effort, prior ties, counterparty alliance readiness. Costs near-zero - every input is already in the team's head. Buys the answer to which alliance ships first, not which one is worth having; the shortlist decays within two quarters.
- **Reach-led**: weights account or audience overlap, market size, brand. Costs a week plus a licensed overlap dataset or audience audit, and RevOps coordination to get it. Buys the least - overlap flags warm accounts with no evidence it predicts alliance success, and market size and brand are the door logo halo walks through. Keep these as capped inputs inside another set rather than a set of their own.
- analyst effort: `reach-led > complementarity-led > speed-to-first-value`
- decision quality, and efficiency alike: `complementarity-led > speed-to-first-value > reach-led`

**Weight distribution** - default: individually justified weights.

- **Individually justified weights**: one written line per weight. Costs an hour, and the justifications double as the memo's audit trail. Kills the arbitrary-weights defect at its source.
- **Type-segmented weight sets**: one set per alliance type when the list mixes technology integrations with co-sell alliances. Costs a few hours more plus a defensible split of the list; buys nothing on a homogeneous list except another sheet to maintain.
- **Formal best-worst method**: preferred over AHP - fewer pairwise comparisons, less rank-reversal exposure. Costs a half-day of structured elicitation per stakeholder and the coordination to convene them. Buys the most defensible weight set on the menu, which is exactly why efficiency starves it - see What the ordering starves for when to promote it anyway.
- **Equal weights**: rejected rather than ranked - near-zero effort, negative value. The format decides instead of the room; this is the documented practitioner failure mode.
- analyst effort: `best-worst > type-segmented > justified > equal`
- decision quality, and efficiency alike: `justified > type-segmented > best-worst > equal`

**Gate strictness** - default: staged.

- **Staged**: desk-checkable gates on the whole longlist (viability signals, public security posture, the three-laws screen), the expensive ones - counsel review of terms, TPRM questionnaire, audience audit - only on survivors. Costs hours across the longlist and a week on the few that reach the expensive tier.
- **Full gate set on every longlist candidate**: costs a week or more, most of it spent on candidates a five-minute check would have removed. Reaches the same shortlist, later. Justified only on a candidate list small enough that staging saves nothing.
- **Gates on finalists only**: costs near-zero up front and is worth less than nothing - scoring and socializing a candidate before its legal or security gate is exactly what makes a gate tradeable, and a candidate the room has already crowned is politically near-impossible to remove.
- analyst effort: `full set > staged > finalists-only`
- decision quality: `staged == full set > finalists-only` - tied because staging changes when the expensive review runs, never what it returns; both remove the same candidates and reach the same shortlist.
- efficiency: `staged > full set > finalists-only`
- compliance cost: `finalists-only > staged == full set` - gating last means roadmap and data have already been shared with a candidate counsel may reject, so the review it triggers arrives after the point where the decision could be reversed cheaply. The other two tie because both put counsel and security in front of a candidate before it is scored or socialized; only the number of candidates reviewed differs, and that is an effort difference, not a reversibility one.

**Where the capacity line falls** - default: effort-sum.

- **Effort-sum line**: cut where the candidates' summed effort estimates exhaust available alliance-manager months. Costs near-zero once step 6 has scored effort. The only line that notices two cheap alliances and one expensive one are not interchangeable.
- **Headcount line**: cut at the capacity number from the Interview. Costs near-zero, and is enough when candidate efforts are comparable - it assumes every alliance costs one manager the same, which is rarely true.
- **Score-gap line**: cut at the biggest break in composite scores. Costs near-zero and buys the least: scores within ~5% are a tie, and the gap moves under any re-weighting, so the line lands wherever the weights happened to fall. Use it to break a tie under an already-fixed capacity number, never as the line itself.
- decision quality, and efficiency alike: `effort-sum > headcount > score-gap` - effort is near-zero for all three, so only what each buys separates them.

Two things here stay deliberately unranked. The must-pass gates are pass/fail and non-tradeable, and the verdicts - go, conditional-go, recycle, hold, kill - are outcomes the evidence assigns, not options an analyst picks between. Ordering either would manufacture exactly the false precision the sensitivity analysis exists to undo.

### What the ordering starves

A value-per-effort ratio always underweights whatever is expensive _and_ strong. Name both instances out loud rather than letting the arithmetic quietly retire them.

- **In the method menu: formal best-worst elicitation.** It produces the most defensible weight set on offer - structured, attributable, least exposed to rank reversal - and loses every efficiency round to justified weights because it costs a half-day per stakeholder plus the coordination to convene them. Promote it when the weights themselves are what the room is arguing about: a sign-off owner who distrusts the sheet, a steering committee that has already reopened one ranking, or a scorecard the team will re-run every portfolio review. It buys agreement on weights, never precision in them.
- **In the candidate list: the deep co-innovation alliance.** A partnership whose value needs both sides to build something loses twice to a quick logo-swap integration - high effort in the denominator, plus a co-innovation discount on value it has not yet been allowed to prove. A portfolio ranked only on the ratio fills with cheap integrations and never places the one bet that changes the product. Promote it when the stated goal is product-gap fill or market entry rather than pipeline, and when the unshipped piece sits on the two parties' own dated roadmaps rather than a third party's. Promote it by reserving a slice of capacity before scoring starts - never by adding points to its composite, which is the false precision the sensitivity analysis exists to undo.

### Re-ranking and deleting against this user

Every ordering above is a default for a team with no unfair advantage, and it shifts with context and with who runs it. Re-rank against what you already know about this user: a licensed account-overlap dataset drops reach-led criteria from a week to an hour (still capped as an input, never the spine); an executive who has already picked a favourite raises the value of justified weights and the sensitivity re-run, because those are the artifacts that survive the argument.

Then delete outright whatever the user's constraints rule out, and say which option you deleted and why. A ruled-out option demoted to the bottom of a menu comes back later as scope somebody re-argues:

- No licensed account-overlap data and no audience-audit budget - delete reach-led criteria. Stripped of the dataset, its remaining inputs are market size and brand, the two the logo halo travels on.
- An executive who has already picked a favourite - delete gates-on-finalists-only. Its one defence is that nobody has committed yet, and somebody has.
- A longlist of two or three candidates - delete staged gates and run the full set on everyone. Staging exists to avoid spending a week on candidates a desk check removes; at that size there is nothing to save.

Then, before anything is presented:

- Name the assumptions out loud before scoring: which candidate the room already wants, which number nobody can evidence, which effort estimate is a guess.
- Argue the strongest case _against_ your own top-ranked candidate before presenting it; logo halo and executive relationships are the documented ways this exercise fools itself.
- Present the deliverable one section at a time - gates, then scorecard, then ranking, then sensitivity, then verdicts - and validate each before drafting the next.
- Gate finalization on the user's explicit approval of the assembled memo.

## The Ranked Shortlist Memo

Deliver the engagement as this artifact - the decision record the user takes to their sign-off owner:

```
ALLIANCE SHORTLIST  - <scope>, <date>
Goal          : strategic goal served + the capacity line and where it came from
Candidates    : N considered; gate failures named, each with the failed gate and evidence
Scorecard     : criteria and weights, one-line justification per weight
Ranking       : full ranked table  - composite score, effort, risk score per candidate
Sensitivity   : which weight shifts reorder the top of the table, and which never do
Shortlist     : candidates above the line, each with verdict and its reasoning
Next gates    : per shortlisted candidate  - first-value milestone, owner, gate date
Below the line: each candidate's verdict (hold/recycle/kill) and its re-entry trigger
Open questions: data that was missing, and what result would change the ranking
```

Three rules govern the memo:

- Every score traces to evidence a reviewer can check - "no shared closed-won accounts in a 40-deal sample" is reviewable, "weak overlap" is not.
- Every quoted benchmark carries a provenance flag - most published partnership statistics come from vendors that profit when the number looks good.
- The open-questions section is mandatory: a ranking with no stated uncertainty has stopped asking.

## Pass Threshold

Ship nothing until all of these hold; iterate until they do:

1. **One criteria set, justified weights.** Every candidate scored on the same criteria; every weight carries a written one-line justification; no equal-weight default anywhere.
2. **Sensitivity-tested.** The ±20% weight-shift re-rank was run; the memo states which positions are stable and which flip.
3. **Gates stayed non-tradeable.** No gate failure was overridden by a high composite score; every gate decision cites evidence.
4. **Shortlist fits capacity.** Shortlist length ≤ the stated capacity number, with effort estimates that sum inside it.
5. **Risk scored, not appended.** Relational, performance, and dependency risk scored per shortlisted candidate and reflected in the ranking, not parked in an annex.
6. **At least one candidate did not make it.** A ranking that greenlights every candidate decided nothing; if all genuinely pass, say so and defend it explicitly.

## KPIs

Judge the prioritization decision itself, six to twelve months out - not the partners' ongoing performance (that belongs to `mbfinotti/partnerships-skills@partner-performance`):

- Share of shortlisted alliances hitting their first-value milestone (first joint deal, integration live, first campaign) by the gate date.
- Partner-sourced and partner-influenced pipeline (B2B) or incremental attributed revenue and brand-lift (B2C) from shortlisted alliances, against the effort spent.
- Gate survival: share of shortlisted candidates that earn "go" at their next gate rather than recycle/kill.
- Ranking churn at the next portfolio review - a reversed top-3 signals weak criteria, not a changed world, unless a named trigger fired.
- Regret log: passed-over candidates that partnered with a competitor and visibly performed. Painful, and the only honest test of the cut line.

## B2B and B2C

Identical in both:

- The stage-gate funnel.
- Must-pass gates kept outside the tradeable score.
- Justified weights plus sensitivity analysis.
- The capacity cut line.
- The memo shape.

Say so when asked. Do not reinvent the method per side.

What genuinely changes - design for it:

| Dimension          | B2B alliance/tech                                          | B2C brand/creator                                               |
| ------------------ | ---------------------------------------------------------- | --------------------------------------------------------------- |
| Ranking currency   | Pipeline, ACV, integration adoption                        | Brand equity, audience, incremental attributed revenue          |
| Core fit construct | Resource complementarity + org compatibility               | Brand fit / attitude congruence (Simonin & Ruth)                |
| Dominant risk      | Channel conflict, platform envelopment, roadmap dependency | Reputational contagion, negative spillover, creator fraud       |
| Key data           | Account overlap, closed-won history, co-sell records       | Audience overlap, brand-lift/incrementality tests, fraud scores |
| Signature gate     | Security/compliance, viability                             | Brand-safety and fraud vetting as pass/fail                     |

Full sourced contrast, hybrid cases, and the evidence-hygiene notes in [references/b2b-vs-b2c-contrast.md](references/b2b-vs-b2c-contrast.md).

## Failure Modes

| Failure                                                        | Fix                                                                                                    |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Logo prestige outranks fit - the famous candidate wins on halo | Weight complementarity + compatibility highest; score the protected candidate visibly, like the rest   |
| Equal weights and false precision                              | Justify every weight in writing; run the sensitivity re-rank                                           |
| Account overlap used as the ranking spine                      | Cap it as one input; the vendor's own network data shows far smaller effects than its survey headlines |
| "Strategic" candidate exempted from measurement                | Every candidate gets a first-value milestone and a gate date, however strategic                        |
| Ranking produced, no capacity line                             | Fix capacity in the Interview; shortlist length ≤ capacity, always                                     |
| Gate failure traded away against a high score                  | Gates live outside the score; a SOC 2 failure is not worth any number of scorecard points              |
| A 0.1 composite gap treated as decisive                        | Scores within ~5% are a tie; break ties with documented judgment, not decimal theater                  |
| Ranking never revisited                                        | Portfolio review cadence plus named re-ranking triggers, dated in the memo                             |

## Invocation Examples

- "We have nine candidate technology alliances and capacity for three. Rank them and tell me which to drop."
- "Leadership wants us to sign a hyperscaler alliance. Score it against the four smaller candidates we already had on the list."
- "Re-run last year's alliance shortlist - two candidates shipped the integrations they promised and one had a down round."

## Reference

- [references/scoring-criteria-and-weights.md](references/scoring-criteria-and-weights.md) - criteria menu, weighting mechanics, the scorecard critique and its fixes, effort scoring, tie-bands.
- [references/risk-and-dependency-screens.md](references/risk-and-dependency-screens.md) - must-pass gate list, Das & Teng risk taxonomy, Adner's two ecosystem risks, platform envelopment, B2C contagion and fraud screens.
- [references/gates-and-governance.md](references/gates-and-governance.md) - stage-gate funnel, verdict vocabulary, joint value proposition workshop format, steering-committee shape, portfolio review cadence.
- [references/worked-examples.md](references/worked-examples.md) - a fully worked ranked shortlist, and a negative example of a logo-collecting scorecard annotated line by line.
- [references/b2b-vs-b2c-contrast.md](references/b2b-vs-b2c-contrast.md) - the sourced B2B/B2C contrast, hybrid cases, and vendor-statistic hygiene.

Sibling skills (same collection):

- `mbfinotti/partnerships-skills@partner-ecosystem` - ranks ecosystem segments and categories; hands its named candidates to this skill.
- `mbfinotti/partnerships-skills@joint-gtm-planning` - planning the joint motion after a candidate earns "go".
- `mbfinotti/partnerships-skills@partner-tiering` - tier criteria inside an existing program; not a candidate-ranking tool.
- `mbfinotti/partnerships-skills@partner-marketplace-strategy` - third-party marketplace listing strategy.
