---
name: sales-objection-handling
description: Diagnoses what a sales objection really means and writes rebuttal scripts a rep can say out loud, or calls the deal dead when the objection is a real constraint. Covers price/budget, timing, competitor/incumbent, authority, status-quo, and trust objections for B2B and B2C, with price-specific guidance on value gap vs genuine budget limit and trading instead of discounting. Use whenever the user mentions a price objection, "too expensive", "not interested", "send me some info", "we already use a competitor", stalling, or an objection library, even without the word objection. Do NOT use for discount trade planning (mbfinotti/sales-skills@negotiation-concession-planner) or ROI math (mbfinotti/sales-skills@deal-value-calc).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.8"
---

# Objection Handling

Diagnose what a sales objection really means, then produce spoken-language response scripts - or say plainly that the deal should be disqualified. Works for B2B and B2C, from cold call through negotiation, with dedicated price-objection sequencing.

## The prevention check (run it first)

The strongest research in this field (Neil Rackham's Huthwaite studies) found that objections are more often created by the seller than the buyer, and that preventing them beats rebutting them. Pitching before the need is developed, or leading with features, manufactures price sensitivity.

1. Once the interview tells you where the objection landed, ask what discovery happened before it.
2. If the honest answer is "we pitched before we understood the problem", say so, and recommend mbfinotti/sales-skills@sales-discovery-questions to fix the upstream gap.
3. Then continue - the rep still has to answer the objection in front of them. One check; don't turn this into a discovery session.

## Interview

Ask one question per message. Offer multiple-choice options wherever possible - the user is often answering from a phone between calls. Gather:

1. What are you selling, and to whom? (product, rough price point, buyer persona)
2. B2B, B2C, or consumer high-ticket (auto, solar, home improvement)?
3. Where did the objection land: cold call / discovery / demo / proposal or negotiation / retail or inbound?
4. The prospect's exact words. Verbatim matters - "that's a lot of money" and "we have no budget" are different objections.
5. What has the rep already tried in response?
6. Which proof assets exist: case study, benchmark, reference customer, guarantee, trial? Never invent one.
7. Do you sell in a regulated category - securities, insurance, lending, health/pharma, energy/utilities? (See Ethics and compliance.)
8. By when does this have to land - the call tomorrow, this quarter's pipeline, or next year's team enablement?
9. One-off win or compounding asset: scripts for one rep's live deal, or a framework the whole team adopts and drills?
10. What's the effort ceiling - rehearsal hours available before the next call, and can the rep offer an opt-out, guarantee, or phased start without sign-off?

Re-rank the framework ladder on those answers, and say which answer moved what:

- A call tomorrow promotes the pause, the value/capability split and the ledge, and drops everything costing a quarter of rehearsal.
- A compounding mandate promotes LAARC, the up-front contract and the JOLT play - all three only pay once a team drills them, and all three are wasted on a single deal.
- No authority to offer de-risking deletes the de-risk move from the discount menu below and leaves trading at the top.

## Workflow

1. Run the interview, then the prevention check.
2. Diagnose the objection (next section). Never script before diagnosing.
3. Pick the response mode that matches the diagnosis.
4. Draft the rebuttal set in the output shape below. Apply the price sequencing section to any price objection. For competitor objections: if you can browse the web, verify the competitor's current public pricing and packaging before writing a comparison claim; if you can't, mark every competitor claim "verify before use".
5. Apply the ethics and compliance gate.
6. Run every script through your preferred humanizer skill - mandatory, this is language meant to be spoken. If no humanizer skill is available, do a manual pass: read each line aloud, add contractions, cut anything a person wouldn't actually say on a call.
7. Deliver. If the user is building a reusable library, add the maintenance notes below.

## Diagnose before you script

The stated objection is often not the real one. The same words need opposite responses depending on what's underneath, and a rebuttal aimed at the surface words wastes the rep's turn. Classify first:

| Diagnosis                | What it is                                                         | Tell-tale signs                                                                                                    | Mode                    |
| ------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ----------------------- |
| Reflex brush-off         | Automatic response to being interrupted, not a considered position | Cold call or shop floor, first 30 seconds, generic wording ("not interested", "send me some info", "just looking") | Reflex                  |
| Smokescreen              | A stated objection concealing the real one                         | Vague, shifts when probed, doesn't match the deal's facts                                                          | Probe, then re-diagnose |
| True objection           | A real, specific concern that must be resolved to progress         | Specific, consistent, tied to facts ("your API doesn't cover X", "the CFO capped spend at Y")                      | Considered              |
| Indecision               | Fear of getting it wrong, not preference for the status quo        | Late stage, agrees on value, keeps asking for more information, options, or stakeholders                           | Indecision              |
| Disqualifying constraint | A constraint no script can move                                    | No budget exists at all, no path to authority, no compelling event, hard regulatory bar                            | Disqualify              |

Make the rep ask one diagnostic question before responding. All four cost the same near-zero breath, so the ordering is pure value:

`"what's behind that?" > the price triage > the if-solved test > the confidence question`

- "Can I ask what's behind that?" - opens up almost any objection, and needs no guess about which arena you're in.
- "Is it that the number doesn't fit the budget, or that you're not sure it's worth it?" - the price triage. Splits the single most common objection into its two opposite responses, but only once you know it's about price.
- "If [stated objection] were solved, would you move forward?" - a "no" exposes a smokescreen. Needs a stated objection specific enough to name back.
- "What would you need to see to feel confident this is the right call?" - a specific answer is a true objection; an endless list signals indecision. Slowest to interpret: the tell is in the shape of the answer, not its content.

Before any of that, the magic quarter of a second (Jeb Blount): pause before reacting. The first instinct is to defend, and defending is almost always wrong.

## Response modes

The diagnosis picks the mode, so the four modes are deliberately not ranked against each other - a ranking there would be false precision. The choice of framework _inside_ a mode is ranked, and that ordering is what a rep with limited rehearsal time needs.

Learn the frameworks in this order - value bought per hour of rehearsal:

`pause > value/capability split > LAER > ledge == Mr. Miyagi > gap re-anchor > LAARC > up-front contract > JOLT play > tactical empathy`

Steps, originators, what each costs to learn and what each buys are in [./references/response-frameworks.md](./references/response-frameworks.md) - read it when drafting. Effort there is rehearsal time, live-call composure, and how badly the move fails in unskilled hands; nothing on the ladder is bought, only learned.

What that order starves: tactical empathy and the full JOLT play are the two highest-value entries and lose every round, because each costs a quarter of rehearsal. Promote both when:

- a single deal is worth a large share of the number
- procurement or an adversarial economic buyer is in the room
- no-decision is already the top loss reason

The order is a default, not a law - it shifts with context and with who executes it. Re-rank it against what you already know:

- a team already drilled in one methodology starts from that spine instead of LAER
- a solo founder skips the rungs that only pay once a team drills them
- a transactional motion promotes the ledge to first
- a complex six-figure deal inverts that

### Reflex mode (cold call and retail brush-offs - identical in B2B and B2C)

The goal is the next 30 seconds and the meeting, not the sale. Never argue with a reflex - arguing upgrades it into a real objection.

`ledge, disrupt, ask == Mr. Miyagi > poke the bear`

1. Open with a ledge (Jeb Blount): a pre-memorized neutral line that buys the rep's rational brain recovery time. Blount's full turnaround is ledge, disrupt, ask. An hour to memorise; buys a beat the rep would otherwise spend defending.
2. Or agree and redirect instead of fighting - the Mr. Miyagi Method (30 Minutes to President's Club): absorb the objection, disarm, redirect to selling the meeting, not the product. Their three cold-call buckets - dismissive, situational, existing-solution - each keep that shape with a different redirect. Tied with the ledge: same arena, same rehearsal cost, same failure mode; pick on the rep's temperament, not on merit.
3. Then poke the bear (Josh Braun): "'I'm not interested' isn't an objection." Ask one question that surfaces a problem the prospect may not know they have, instead of pushing. Same hour to learn, but the question only lands with product knowledge a new rep doesn't have yet - that dependency is what ranks it third, not the move itself.
4. One turnaround attempt, at most two. Then take the no gracefully - see Ethics and compliance.

### Considered mode (discovery, demo, proposal)

`LAER > LAARC > up-front contract > tactical empathy`

- LAER - Listen, Acknowledge, Explore, Respond (Carew International). The default spine: an hour to learn, a week of calls before the rep stops answering in the same breath, and it covers every considered objection in any arena.
- LAARC - Listen, Acknowledge, Assess, Respond, Confirm (from the academic professional-selling textbook line). One extra hour on top of LAER for two guardrails: Assess forces "is this the real objection?" before responding, Confirm forces "is it actually resolved?" before moving on. That hour pays only where smokescreens are common or reps declare victory early; elsewhere it buys what LAER already bought.
- Sandler's up-front contract - agree the meeting's outcome up front, and vague stalls never form. Costs a week of habit across the whole team, so it earns its place only under a compounding mandate, never for one call.
- Tactical empathy (Chris Voss / Black Swan Group) - a label and dynamic silence first, a calibrated how/what question second. Sequencing matters: a calibrated question fired before empathy lands as an attack. Last here because it costs a quarter and misfires badly in unskilled hands, first on value when the pushback is adversarial - that's the promotion condition above.

Whichever spine is in play:

- Never respond in the same breath the objection lands. The explore/assess step is what catches smokescreens.
- Attach exactly one proof point per response, matched to the specific concern. Three weak proofs read as desperation.
- Distinguish value objections (buyer unconvinced it's worth it - rebuild the need) from capability objections (can-you-do-X - answer honestly, including "we don't do that") per Neil Rackham's research. Near-zero to learn, which is why it sits second on the ladder.

### Indecision mode (late-stage stalls)

Per The JOLT Effect (Dixon and McKenna, 2022), a large share of lost deals die to buyer indecision - fear of getting it wrong - not preference for the status quo. Adding more value, urgency, or FOMO makes indecision worse. When the diagnosis is indecision, switch modes:

1. Give one clear, confident recommendation - not more options.
2. Limit the exploration: reassure the buyer they already have enough information; stop feeding the research loop.
3. Take risk off the table: opt-out, guarantee, phased rollout, smaller first commitment. De-risk because it answers the actual fear - the win-rate statistics attached to risk-reversal language are vendor-published and correlational, so treat them as a hint, not a law.

### Disqualify (a valid output, not a failure)

When the diagnosis is a real constraint (no budget at all, no path to authority, no compelling event, a hard regulatory bar), say so and stop rebutting. A skill that always produces a comeback teaches reps to push on dead deals.

Output instead:

- a graceful exit script
- a re-entry condition ("when X changes")
- a follow-up date to put in the CRM

## Price objections

Price gets its own treatment because "too expensive" is the most common objection and the most misdiagnosed.

Triage first - the two meanings need opposite responses:

- Value gap: the buyer doesn't yet see enough value to justify the number. Fix the value story, not the price. Use the buyer's own stated goal against the objection (Keenan's Gap Selling): "You said cutting audit prep was the priority this quarter - help me understand how the price outweighs that." Quantifying the gap is mbfinotti/sales-skills@deal-value-calc's job.
- Genuine budget constraint: the money truly isn't available this cycle. No value pitch fixes this. Change the terms, ranked by what each costs the rep against what it recovers: `phased start > smaller scope > later start date > champion enablement > disqualify with a re-entry date`. A phased start needs no new approval and keeps the deal this quarter; a smaller scope shrinks it permanently; a later start date only moves the problem; champion enablement costs a week of the rep's time building someone else's business case; disqualifying is last because it recovers nothing this cycle - but it is the honest answer once none of the four above fit.

Split them with: "Is it that the number doesn't fit this year's budget, or that you're not sure it'd be worth it at that number?"

When price comes up before value is established:

- Don't stonewall. Refusing the number reads as evasive and stacks a trust objection on top of the price one.
- Give an honest range or anchor, then earn the right to add context: "It runs between X and Y depending on scope - can I ask two quick questions so I can tell you where you'd land?"
- The transferable principle from conversation-intelligence research (vendor-published, correlational - treat as a heuristic): discuss price on the first call, after value. Not never, and not in the opening minute.

When they push for a discount, three moves compete. The axes disagree, so read all four lines:

- efficiency: `de-risk > trade > discount` when opt-out or guarantee terms already exist; `trade > de-risk > discount` when they don't, because getting terms approved is a standing job, not a call-prep task
- value: `de-risk > trade > discount`
- effort: `de-risk > trade > discount`
- compliance cost: `de-risk > discount > trade`

- De-risk - an opt-out, guarantee, or smaller first commitment often resolves the fear the discount ask stands in for, and it costs no margin. Highest effort of the three: the terms have to exist and be approved before the call, and a guarantee is a contract term that needs legal sign-off and is hard to withdraw once offered. Deleted from the menu entirely if the interview said the rep can't offer one without sign-off - a de-risk move parked at the bottom reappears mid-call as an unauthorized promise.
- Trade - every reduction gets something back: a longer term, a case study, an intro, a signature date. An hour of rehearsal and the composure to ask; needs only the customer's own permission, so no review is triggered. The default when de-risking isn't available.
- Discount - never conceded unilaterally, and last on efficiency and value. It ranks lowest on effort only in the trivial sense that saying a smaller number takes no rehearsal; it buys a smaller deal, sets the account's floor, and signals the original number was padded. It still needs deal-desk approval, and the precedent carries into the next renewal.

Planning which concessions to trade, and in what order, ahead of a negotiation belongs to mbfinotti/sales-skills@negotiation-concession-planner - hand off rather than improvising a concession ladder here.

Remember the prevention finding: features presented early increase price sensitivity (Rackham). A late "too expensive" is often the bill for a rushed pitch. Weak decision-criteria and economic-buyer work earlier in the deal is the usual root cause - MEDDICC's economic-buyer lens is cost, completion, confidence - and mbfinotti/sales-skills@meddpicc-scorecard scores that; this skill supplies the words in the meantime.

## B2B vs B2C

- B2B: objections often come from a buying committee, so the words the rep hears may be a proxy for an absent stakeholder's concern. "I need sign-off" and "not this quarter" frequently mean "I can't get this through my process", not "I don't want it" - script for the champion's internal battle (a one-pager, talking points for their boss), not just the live call.
- B2C: usually one decision-maker, shorter deliberation, price and trust dominate, and the reflex/emotional share is larger. In retail, "just looking" is a predictable step of the visit, not an objection (Harry Friedman's retail work) - disarm it with a low-pressure opener and let the visit continue.
- Consumer high-ticket (auto, solar, home improvement) sits between the two: a single household with committee-like dynamics ("I need to talk to my partner") and heavy consumer-protection regulation.
- Identical in both, explicitly: the diagnose-before-you-script rule, the reflex brush-off response, and the trade-don't-cave rule on discounts.

## Output shape

Produce a rebuttal set: one entry per objection, each containing:

1. The objection - verbatim, as the prospect says it.
2. What it usually means - the concerns underneath, and which diagnosis each points to.
3. The diagnostic question - the one question that tests which meaning is in play.
4. The response script - spoken language, two to five sentences, contractions, no marketing adjectives.
5. The proof point - which real asset from the interview backs it. Never invented.
6. The hand-back question - the question that returns the conversation to the prospect.
7. If it repeats - what a second occurrence of the same objection means, and what to do (usually: stop rebutting, re-diagnose, or disqualify).

Read [./references/worked-examples.md](./references/worked-examples.md) before writing your first set - including the negative example.

## Ethics and compliance

Hard rules, not style preferences:

- Never manufacture urgency (fake deadlines, fake scarcity), invent social proof, or make any claim the rep can't substantiate. A script with an invented proof point is a lie with better formatting.
- Never build a rebuttal quota - any rule or scorecard requiring N rebuttal attempts before accepting a no. Consumer telemarketing rules require honoring a request to stop; a script that rewards pushing past it makes the script itself the violation.
- A clear "stop calling me" or "take me off your list" ends the conversation. Script the graceful exit, not another angle.
- If the user sells in a regulated category, whole categories of claim are off-limits. Route every script through the firm's compliance review before anyone speaks it, and state that requirement explicitly in the output. Don't enumerate the rules yourself - that is their compliance team's job, not this skill's.
  - Regulated categories: securities, insurance, lending, pharma/health, energy/utilities, a consumer-duty regime.
  - Off-limits claims: guaranteed or predicted returns, unsubstantiated savings figures, implied affiliation with a utility or government body, off-label claims.

## If the output becomes a library

- Date every entry.
- Source responses from real winning calls (call recordings, win/loss notes) instead of invention as soon as any exist.
- Refresh monthly for competitor and pricing entries. A battlecard carrying stale competitor pricing is worse than none - reps stop trusting the whole library.
- If your harness has persistent memory, store the product, personas, proof assets, and diagnosed patterns so later sessions can skip the interview; otherwise tell the user to keep the library in a dated file they own.

Owning and maintaining the library org-wide is beyond this skill's scope - keep this note short in the output.

## Measuring whether it works

`diagnostic-question rate > objections-per-call by rep > no-decision loss rate` - ordered by how fast each one can tell you anything.

- On scored calls, check whether the rep asked a diagnostic question before responding - visible on the next call you score, and the leading indicator that this skill's core habit stuck.
- Track objections-per-call by rep. If the best closers hear materially fewer objections, the problem is upstream sequencing, not rebuttal skill - invest there. Needs a few weeks of calls before the spread means anything.
- Track the no-decision loss rate. A falling rate is the signal the indecision mode is landing, but it needs a quarter of closed deals to move - the most valuable number here and the slowest to arrive.

## Failure modes

- Rebutting a reflex as if it were reasoned. Argument converts a brush-off into a real objection. Ledge, then a question.
- Answering the surface words of a smokescreen. You win the stated objection and the deal still dies. Probe first.
- Adding value, urgency, or FOMO for an indecisive buyer. It reliably makes indecision worse. Switch to indecision mode.
- Feel-Felt-Found ("I know how you feel, others felt the same, they found..."). Formulaic, instantly recognized, and dishonest whenever the "others" are invented. Don't use it.
- The deflect-and-close loop: dodging the first objection without answering, closing again, repeating. A pressure device, not a diagnostic one - and a compliance risk in consumer channels.
- Trashing the competitor. Ask how the incumbent is working instead; a well-placed question beats badmouthing.
- Bluffing a technical or capability answer. The prospect verifies during evaluation, and the trust loss outlives the deal.
- Shipping first-draft scripts. If it reads like an email, nobody can say it. The humanizer pass is not optional.

## References

- mbfinotti/sales-skills@cold-call-opener - the opener itself; this skill starts once pushback lands.
- mbfinotti/sales-skills@sales-discovery-questions - when the prevention check shows discovery was thin.
- mbfinotti/sales-skills@meddpicc-scorecard - deal qualification scoring.
- mbfinotti/sales-skills@deal-value-calc - quantifying the ROI/business case behind a value-gap rebuttal.
- mbfinotti/sales-skills@negotiation-concession-planner - planning concession trades ahead of a negotiation.
- mbfinotti/sales-skills@sales-call-review - scoring a recorded call, including how objections were handled.
- [./references/response-frameworks.md](./references/response-frameworks.md) - named frameworks: steps, originators, and when each fits.
- [./references/worked-examples.md](./references/worked-examples.md) - filled-in rebuttal sets, positive and negative.
