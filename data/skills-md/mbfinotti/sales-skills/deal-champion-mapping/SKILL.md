---
name: deal-champion-mapping
description: Builds an evidence-graded stakeholder map for one active deal from titles, call notes, email and meeting activity, and CRM contact roles, naming the likely champion, economic buyer, and blockers, each with a confidence level tied to observed behaviour rather than title. Covers B2B buying committees and high-consideration B2C households. Use whenever the user mentions a champion, economic buyer, power map, deal org chart, multi-threading, single-threaded risk, or "who actually decides", even without the word stakeholder. Do NOT use for qualification scoring (mbfinotti/sales-skills@meddpicc-scorecard) or scanning notes for general risk (mbfinotti/sales-skills@deal-red-flags).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.11"
---

# Champion Mapping

Turn what is already known about an account - contact list with titles, call notes, email and meeting activity, CRM contact roles - into a stakeholder map. The map:

- Names the likely champion, the economic buyer, and the blockers or detractors.
- Grades every assignment by the strength of its evidence.
- States what is still unproven.
- Attaches the next concrete action that proves or disproves it.

The role definitions come from MEDDICC (champion, economic buyer) and Challenger (Mobilizer, Blocker) as named sources; this skill identifies and tests the people - it never scores the deal against any acronym.

Confidence labels used throughout:

- **verified** - confirmed at a named source.
- **second-hand** - documented only via another publisher.
- **vendor-data** - a vendor's own correlational platform dataset, never independently replicated.
- **inference** - this skill's own reasoning rather than a cited claim.

No vendor correlation here is causal, ever.

## Interview

Ask before mapping. One question per message; offer multiple-choice answers when possible; skip anything the user's data already answers.

- B2B, or high-consideration B2C? (B2C here means considered household purchases - remodeling, solar, private school, financial products - not impulse retail.)
- Deal size and segment? (Transactional / mid-market / enterprise - this sets the coverage benchmark and how much committee to expect.)
- What contact data exists? (Contact list with titles, call notes or transcripts, email/meeting activity, CRM contact-role fields - paste or attach whatever is available.)
- What stage is the deal in? (Early discovery, evaluation, proposal, procurement/paper process - later stages demand more proven roles.)
- Does the team run a sales methodology (MEDDICC/MEDDPICC, Challenger, Miller Heiman, other)? The map will use its vocabulary where it matters.
- Industry or regulatory context? (Regulated buyers add compliance and legal seats to the committee by default.)
- Does the product touch customer data? (If yes, assume a security reviewer exists whether or not one has appeared - **inference** from practitioner consensus that security can veto after everyone else approves.)
- What is already known about the org - reporting lines, prior deals at this account, who bought last time?
- Who is the current primary contact, and why them? (The answer often reveals whether the deal is single-threaded.)
- By what date must the next assignment be proven - close date, board meeting, budget cycle? (A hard date promotes the near-zero, same-week asks and deletes anything whose latency exceeds it, starting with the co-built business case.)
- One-off win, or a compounding asset - is this account also a reference, an expansion base, a logo the team will resell against? (A compounding mandate promotes the slow, high-value plays: the co-built case, an executive sponsor, a cultivated second champion.)
- What is the effort ceiling - how much of the contact's political capital can this deal spend, how many rep hours, and can a refused ask be survived? (A low ceiling, or a contact who has already spent capital once, holds the ladder at its cheap rungs and deletes the proof-of-concept.)

## Workflow

1. Run the Interview; collect the contact data before assigning any role.
2. Inventory the evidence. For each contact, separate three piles: observed behaviour (what they demonstrably did), stated claims (what they said about themselves or the process), and title/org inference. These piles are the evidence tiers below - never mix them.
3. Assign a candidate role to each contact from the taxonomy, grading each assignment with the evidence rubric. Contacts with contradictory or empty evidence get "unknown", not a guess.
4. Test the champion candidate: list which capital-costing asks have been made, what the follow-through was, and which rung of the ask ladder to run next - named as a rung, with the reason it was promoted or held.
5. Name the economic buyer, or explicitly flag "EB unknown" with the discovery action that would surface them. If the champion has deferred EB access, classify the deferral (four readings below) and run its countermove; where the evidence names no reading, run them in the section's order.
6. Hypothesize blockers by function from the taxonomy below, in its efficiency order - explicitly including at least one function not yet on any call, and deleting the functions this deal genuinely has no seat for.
7. Run the coverage check against segment benchmarks; flag single-threading as a coverage gap. (A full red-flag review of the deal notes belongs to the deal-red-flags skill, not here.)
8. Note champion risk: is there a second champion candidate, an executive sponsor, exposure to a job change or reorg?
9. Assemble the map per [references/stakeholder-map-template.md](references/stakeholder-map-template.md); run the Quality gate; iterate until every item passes.
10. Deliver with refresh triggers: the map is a living artifact, re-walked at every stage change, new stakeholder appearance, or champion job-change signal - not a one-time deliverable (**second-hand**, Miller Heiman practitioner discipline via published syntheses).
11. If your harness has persistent memory, memorize the map, the evidence behind each assignment, and the open next actions - the next run starts from proven ground instead of re-deriving it. Otherwise hand the user the map file to keep and re-supply.

## Role taxonomy

One-line definition and the distinguishing test for each. Full framework disagreements (Miller Heiman's Coach vs MEDDICC's Champion, Challenger's title-rejection) in [references/evidence-and-benchmarks.md](references/evidence-and-benchmarks.md).

| Role                      | Definition                                                                                                                                                               | Distinguishing test                                                                                        |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| Champion                  | "A person who has power, influence, and, subsequently, credibility within the customer's organization and who is willing and able to assist you" (**verified**, MEDDICC) | Spends internal political capital: passes a capital-costing ask with follow-through                        |
| Coach / informant         | Helpful, shares process and politics, but lacks power or won't spend capital                                                                                             | Gives information; hedges or defers when asked for an EB introduction                                      |
| Cheerleader               | Enthusiastic, takes every meeting, no organisational pull                                                                                                                | Cannot move budget or override anyone's preference; enthusiasm is the only evidence                        |
| Sponsor                   | Senior, lends name and authority to the deal                                                                                                                             | Endorses but does not do the internal selling work or build the case                                       |
| Mobilizer (Challenger)    | Defined by consensus-building disposition, not title (**verified** as Challenger's taxonomy)                                                                             | Responds to insight with hard questions and drives internal change                                         |
| Economic buyer            | "The power to say yes when others say no, and say no when others say yes" (**verified**, MEDDICC)                                                                        | Can release discretionary or unbudgeted funds for this purchase                                            |
| Budget holder             | Owns a budget line                                                                                                                                                       | May not have authority to redirect it to this purchase                                                     |
| Signatory                 | Signs the contract                                                                                                                                                       | May be a delegate executing the EB's decision - never conflate the two (**second-hand**, MEDDICC guidance) |
| Approver                  | Required sign-off in the process (procurement, legal, security)                                                                                                          | Gate-keeps the paper process; not the value-based decision-maker                                           |
| Blocker                   | Objects on risk, competing priorities, or politics                                                                                                                       | Surfaces objections openly; can be addressed or co-opted                                                   |
| Detractor / anti-champion | Actively works to defeat the deal, often silently                                                                                                                        | Rarely on any call; visible only through second-order effects (stalls, resurfaced objections)              |

## Evidence tiers and confidence

Grade every role assignment by the strongest evidence supporting it:

- Behaviour under cost beats behaviour.
- Behaviour beats claims.
- Claims beat titles.

| Tier                     | Evidence                                                        | Example                                                                                                    |
| ------------------------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1 - Behaviour under cost | The contact did something that cost effort or political capital | Arranged the EB meeting; forwarded the business case; defended the deal in a meeting the rep didn't attend |
| 2 - Low-cost behaviour   | Observable but cheap actions                                    | Fast replies, meeting attendance, sharing non-sensitive information                                        |
| 3 - Stated claim         | What they said, uncorroborated                                  | "I'm the decision maker"; "I'll champion this internally"                                                  |
| 4 - Title inference      | Role guessed from title, department, seniority                  | "VP of the function that owns this category, so probably the EB"                                           |

Confidence rules (**inference**, this skill's rubric):

- **High**: at least one Tier-1 item, consistent with the rest of the evidence.
- **Medium**: Tier-2 or Tier-3 evidence corroborated by a second independent item.
- **Low**: a single uncorroborated item, or anything Tier-4.
- Title alone is the weakest tier and never yields more than Low - a title can suggest a hypothesis, never confirm a role.
- Missing or contradictory inputs widen uncertainty: cap confidence at Low and mark the role "unknown" rather than defaulting to the typical org chart.
- Company size bends title inference: at small companies function leaders buy directly; at 1,000+ employees the same title often sits two levels from the budget (**second-hand**, published qualification-prompt heuristic).

## The champion test

A champion is proven by an ask that costs them internal capital, and by follow-through - not by warmth. "No Champion, no deal" (**verified**, MEDDICC). The four canonical asks below are a ladder, not a list, ranked on two axes:

- **Effort** - the contact's own political capital, plus calendar latency and reversibility. A refused ask spends standing they may not get back.
- **Value** - evidence strength about whether this person is genuinely a champion.

- effort: co-built case > EB introduction > criteria share > forwardable email
- value: co-built case > EB introduction > criteria share > forwardable email
- efficiency: criteria share > forwardable email > EB introduction > co-built case
- compliance cost: criteria share (under a formal RFP or public procurement, asking for competing bids can disqualify the bid) > forwardable email == EB introduction == co-built case (genuinely equal at zero: none touches a policy, a contract clause, or a sign-off)

Effort and value rank identically, which is why row order can be neither: the strongest proof is also the ask most likely to be refused. Run the ladder in efficiency order.

| Rung | Ask                                                                                                           | Contact's effort                                         | Evidence bought                                                                              |
| ---- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 1    | Share internal evaluation criteria, competing vendors, or budget                                              | An hour, plus a norm quietly broken                      | Tier 1: they took a real risk for you, and the competitive picture arrives in the same move  |
| 2    | Forward a rep-written summary internally, or call a customer reference                                        | Near-zero, same day                                      | Weak Tier 1: their name is now attached to you internally - proves willingness, not standing |
| 3    | Arrange a meeting with the economic buyer or an executive sponsor                                             | A week of calendar latency; visible standing spent       | Tier 1, plus the deal's single most diagnostic answer - and the EB meeting itself            |
| 4    | Co-build - not just receive - the internal business case, and present it at a meeting the rep does not attend | An exec-review cycle; publicly staked, hard to walk back | The strongest evidence available: they defended the deal in a room you could not enter       |

Progress the ladder one rung at a time:

- Default to rung 1 with an untested contact.
- Climb exactly one rung each time the previous one passes with follow-through inside its stated timeframe.
- Never repeat a passed rung: a second cheap ask buys no new evidence, and repeating one is how a map stays at Medium confidence for a whole quarter.

Rung 4 is what the efficiency order starves: highest value, worst ratio, last every round, and a collection that only ever computes efficiency never runs it. Promote it anyway when any of these hold:

- Rung 3 has passed, or is structurally impossible (the EB does not meet vendors).
- The decision has moved into a committee the rep cannot attend.
- A competitor is in the room and the map's only remaining risk is whether this contact defends you there.

Delete, do not demote, an ask the deal's constraints rule out; a ruled-out ask parked at the bottom silently reappears as scope.

- Delete rung 1 on a formal RFP or public-sector deal.
- Delete rung 4 before the evaluation stage: a discovery-stage deal has no committee meeting to present at.

This order is a default, not a law. It shifts with segment, stage, and with who executes it: a rep with existing executive relationships pays far less for rung 3 than a first-time seller into the account.

Re-rank against what is already known about this deal:

- An existing relationship with the EB deletes rung 3 (the introduction is already paid for).
- A contact who has already spent capital once starts at the rung above the one they passed.
- A deal too early for a committee holds at rungs 1-2.

Re-rank against the Interview answers too, and say which answer moved which rung.

The diagnostic behind rung 3: "if your Champion is unwilling or unable to introduce you to the EB, this could be a signal that they aren't a true Champion, and you have work to do" (**verified**, MEDDICC). Nate Nasralla's forward-commitment test secures rung 2's proof live during discovery: "if I write you a short email with the summary that we've been working on, are you willing to forward this along?" (**verified**) - the commitment itself, then the follow-through, are both evidence.

Reading the response: follow-through within the stated timeframe is Tier-1 evidence - upgrade. Hedging or deferral twice on capital-costing asks downgrades the contact from champion to coach on the map; do not rest the deal on their strength. (A circulating "40% of supposed champions fail this test" figure is practitioner folklore with no traceable methodology - illustrative only.)

MEDDICC's published warning flags a contact is not a champion (**verified**):

- Lack of information sharing.
- Resistance to making introductions.
- Absence of internal advocacy.
- Limited organizational access.
- Reluctance during internal pushback.

Re-test through the cycle, not once at qualification.

## Economic buyer discovery

"The Economic Buyer is unlikely to raise their hand and tell you they're the EB. It is your job to identify them" (**verified**, MEDDICC). Distinguish EB from budget holder, signatory, and approver per the taxonomy - the EB is the one who could fund this even unbudgeted. Role-identifying questions (this skill's whole allowance of questions - full discovery sets belong to the sales-discovery-questions skill):

- "Who had to approve the last solution you bought like this?"
- "Who is the budget holder for this type of purchase - and could they redirect budget to it?"
- "If everyone else said yes and one person could still say no, who is that?"

**When the champion defers EB access** - one of the most diagnostically loaded events in a deal. Four standard readings, each with its countermove (**second-hand**, practitioner consensus across MEDDICC-derived sources).

Diagnose the reading from evidence rather than picking it, so the ranking below is deliberately narrow: it decides only which countermove to run first when the evidence does not say which reading applies. Ranking a diagnosis the evidence already named would be false precision.

- efficiency (EB access bought per rep hour and per unit of the contact's capital): EB-ready one-pager > decision-path probe > compelling-event revisit > re-run the champion test
- value (what it settles): re-run the champion test > decision-path probe > EB-ready one-pager > compelling-event revisit

| Reading                                                        | Countermove                                                                             | Effort                                                   | Odds it opens the door                                                                             |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Fears losing control or being exposed as lacking authority     | Value exchange: a short, EB-ready business case that makes them look good presenting it | An hour of rep time; near-zero contact capital           | Good - and it is the only play that also helps under readings 1 and 3, which is what puts it first |
| Protecting a relationship, or the real decision sits elsewhere | Give them a reason the EB will want the meeting; probe the actual decision path         | An hour, on the next call already booked                 | Moderate on access, high on information - it returns the map's biggest unknown either way          |
| No active deal - no urgency                                    | Revisit the compelling event; if none, the map is not the problem                       | An hour, and the deal may end on the call                | Low on access - but a negative answer saves a quarter of misdirected effort                        |
| Not a true champion - no standing to secure the meeting        | Re-run the champion test one rung up; downgrade to coach if it fails again              | A week of latency, and the contact's capital spent again | Low - it settles the map rather than opening the door                                              |

Last resort: multithread to the EB through another path. It ranks last on every axis, and what puts it there is irreversibility rather than hours. Going around the champion can destroy trust and convert the champion into a detractor, the single act on this map that turns an asset into a liability (**second-hand**, consistent across practitioner sources).

Delete it outright from a single-threaded deal instead of holding it in reserve: with one real relationship there is nothing left to sell to when it fails. A give-to-get softens the ask instead: trade something the contact wants for the introduction, stated as a condition up front (**verified**, Jason Bay's pattern).

## Blocker taxonomy

Hypothesize blockers by function, not by who has shown up. The recurring pattern in the literature: deals die to a single silent detractor in security, legal, or finance who was never mapped and never on a call (**second-hand**, synthesis of practitioner sources). Table synthesized from the same research base, rows ordered by efficiency - veto risk removed per unit of work, not by seniority or by how loud the function is.

- effort: technical POC > political realignment > ROI model in their numbers > security pack == compliance pack > procurement, legal and incumbent plays (equal at near-zero: each is one send of material you already own)
- efficiency: legal > security == compliance > procurement > economic > incumbent loyalist > political > technical
- compliance cost: compliance/residency commitments > legal redlines > everything else (near-zero) - a residency option or a bespoke clause conceded to clear one review binds every renewal after it, and is the only play here you cannot quietly reverse

Security and compliance tie on both lines because they are the same job - producing an evidence pack - aimed at a different reviewer: an hour when the pack exists, a quarter when it must be built from scratch.

| Blocker                      | Signal and motivation                                                   | Veto power                            | Neutralise / co-opt                                      | Effort                                                                          |
| ---------------------------- | ----------------------------------------------------------------------- | ------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Legal                        | DPA/MSA redlines; liability, data rights                                | Blocks on unacceptable clauses        | Pre-empt with standard terms                             | Near-zero: send the standard paper before they ask                              |
| Security / InfoSec           | Questionnaire, certification review; data isolation, compliance posture | Can veto after everyone else approves | Certifications, architecture docs, SSO                   | An hour if the pack exists; a quarter to build one                              |
| Compliance / privacy         | Data-residency and regulatory review; audit mandates                    | Veto on residency/compliance          | Compliance briefs; residency options                     | An hour if the pack exists; a quarter to build one                              |
| Procurement                  | Appears at paper-process stage; price, terms, vendor risk               | Controls contract terms and timeline  | Engage early; give champion negotiation cover            | Near-zero, but only if run before the paper stage                               |
| Economic (CFO, budget owner) | TCO/ROI questions; controls funding; cost and opportunity cost          | Blocks funding if ROI unproven        | ROI model in their own numbers; business case in dollars | A week - and it needs the champion's capital to get their numbers               |
| Incumbent loyalist           | Advocates status quo; switching cost, sunk relationship                 | Rallies for "do nothing"              | Cost-of-inaction framing; contain rather than convert    | Near-zero to produce, but conversion rarely lands - budget for containment only |
| Political                    | Competing initiative, turf; status, control, rival project              | Informal; can rally opposition        | Align to their agenda; executive sponsor                 | A week or more, and unwinnable if their rival project is funded                 |
| Technical (CTO, architect)   | "We need to run this through IT"; integration cleanliness, standards    | Veto authority, rarely budget         | Surface early; technical validation, POC                 | A quarter of engineering time on both sides                                     |

The proof-of-concept is what this order starves: it produces the strongest technical proof and has the worst ratio on the table, and it is the only play that also spends the buyer's engineering time and the champion's capital to schedule. Promote it when either holds:

- The technical reviewer holds the real veto and has stated an integration objection the documents cannot answer.
- The product's differentiation is only visible inside the buyer's own environment.

Delete rows this deal rules out rather than carrying them low:

- The compliance/privacy row for an unregulated buyer whose product touches no personal data.
- The whole legal/security/compliance/procurement block for B2C households (see the template's adaptation).

A row parked at the bottom returns as unplanned scope at the paper stage.

Watch the seniority mismatch: mapping over-indexes on the executive (the CISO) while the person who runs the actual review (the security architect) holds informal veto over anything that doesn't integrate cleanly (**second-hand**). The most dangerous detractor is often not on any call - the map must contain hypotheses about absent people, not just observations about present ones. Re-rank the plays against what this account already gives you: an existing security-review pass from a prior deal, an in-house solutions architect, or a compliance pack already written for another buyer all move their row up.

## Coverage check

- Benchmarks by segment (**vendor-data** and practitioner heuristics, correlational, not targets): roughly 4-7 engaged contacts mid-market, ~10 for $50K-$250K, 11-17+ for strategic enterprise. Gartner's survey puts the median buying group at 6-10 decision makers (**verified** as Gartner's figure, 2017, n=750).
- Single-threading is a coverage gap on this map: one real relationship means the deal dies with one departure. Treat any single-threaded deal over $50K as structurally behind - multithreaded deals over $50K win at materially higher rates in Gong's 1.8M-deal analysis (its "130%" lift is **vendor-data**, correlational). Flag the gap here; the deal-red-flags skill owns the broader review.
- Count relationships, not names: "whether you're actually protected in a deal - or just have multiple email addresses and one real relationship" (**verified** quote, 30MPC/Gong report).
- The Challenger counter-current, stated so the map isn't read as "more contacts = better": CEB's data shows purchase likelihood _falls_ as buying-group size grows (81% at one decision maker, 55% at two, mid-30s at six) because consensus gets harder (**verified** as CEB's published claim). More stakeholders makes buying harder; multithreading is how a seller _manages_ buying-group complexity, not a force that causes winning. Add contacts to cover real roles, never to inflate a count.

## Champion risk

- Roughly 20% of B2B contacts change jobs in a year (**vendor-data**, a job-change-alerting vendor citing a professional-network analysis) - a multi-month deal resting on one champion is structurally fragile, and most departures are silent.
- The map must answer three questions:
  - Is there a second champion candidate being cultivated?
  - Is there an executive sponsor whose commitment survives a mid-level departure?
  - Would a job change be detected within days (alerting) or discovered at the next ghosted email?
- On a champion-departure signal: activate the redundancy candidate immediately, lean on the executive sponsor for continuity - and note the departure is also an opportunity at the champion's next company.

## B2B and B2C

High-consideration B2C runs the same multi-role logic under different names: consumer theory's household decision-making unit (**verified**, Schiffman & Kanuk / AMA academic taxonomy).

- **initiator** - raises the need
- **influencer** - shapes criteria
- **decider** - holds authority
- **buyer** - executes the purchase
- **user** - consumes
- **gatekeeper** - controls information flow

Mapping onto this skill's roles (**inference**, analytic transfer, not empirically measured equivalence):

- decider ≈ economic buyer
- gatekeeper ≈ the administrative/procurement screen
- influencer ≈ technical evaluator
- user ≈ end user
- the enthusiastic spouse who sells the other is the champion
- the skeptical parent, in-law, or co-signer is the silent detractor
- "do nothing" is as real a competitor in a kitchen renovation as in enterprise software

Works identically for both:

- The evidence tiers.
- The champion test (an ask that costs the enthusiastic partner effort - "will you walk your spouse through this quote before Thursday?").
- The deferral readings.
- Confidence rules.
- The quality gate.

Say so on the map rather than leaving it implicit.

Does not transfer:

- No procurement, legal, or security veto function, no written paper process, and no CRM tooling.
- Power maps become informal intuition.
- Roles shift per purchase (the decider for the car may be a mere influencer for the school).
- Family emotional dynamics are not captured by influence/sentiment scoring.

Drop those rows from the template; keep everything else.

## Invocation and expected output

Typical invocations:

- "Here's the contact list and my call notes for the Meridian deal - who's my champion, who actually signs off, and who's going to block this?"
- "Map the stakeholders on this opportunity; my main contact is great but I can't tell if she's a champion or just friendly."
- "We sell home solar; the husband booked the consult and loves it - map the household before I send the proposal."

Deliver one stakeholder map (full template in [references/stakeholder-map-template.md](references/stakeholder-map-template.md)):

```
STAKEHOLDER MAP - <account>, <deal size/segment>, <stage>, <date>
Per stakeholder : name, title, assigned role, evidence tier + the evidence itself,
                  confidence, gap still unproven, next action to prove/disprove
Champion test   : asks made, follow-through observed, next ask + its rung and why
Economic buyer  : named + evidence, or "unknown" + the surfacing action
Blockers        : >=1 hypothesis per plausible function, incl. people not yet on calls
Coverage        : engaged-contact count vs segment benchmark; single-thread flag
Champion risk   : redundancy candidate, executive sponsor, job-change exposure
Refresh trigger : what event forces the next re-walk of this map
```

## Common failure modes

| Failure                                                     | Fix                                                                                                                                                         |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mistaking responsiveness for power                          | Fast replies are Tier 2; the contact who takes every meeting may have zero organizational pull - grade by capital spent, not warmth                         |
| Assigning champion by title                                 | Title is Tier 4, capped at Low; a champion is proven by a passed capital-costing ask, nothing less                                                          |
| Mapping only who is on calls                                | The most dangerous detractor never joins one; force blocker hypotheses for absent functions                                                                 |
| Treating the map as a one-time artifact                     | Re-walk at every stage change, new stakeholder, or job-change signal; unmet roles and unreadable stances are the most valuable items on it                  |
| Going around the champion to reach the EB                   | Run the deferral countermoves in their ranked order first; the bypass converts champions into detractors, and is deleted outright on a single-threaded deal |
| Reaching for the biggest ask, or repeating the cheapest one | Climb the ask ladder one rung at a time from rung 1; a rung already passed buys no new evidence, and rung 4 needs its promoting condition stated            |
| Conflating EB with signatory or budget holder               | The signatory may be a delegate; the budget holder may lack redirect authority; test for "yes when others say no"                                           |
| Counting email addresses as coverage                        | Multiple contacted names with one real relationship is still single-threaded                                                                                |
| Reading a stated claim as proof                             | "I'm the decision maker" is Tier 3; corroborate with behaviour before raising confidence past Medium                                                        |

## Quality gate

Score the drafted map against all eight. Pass threshold: 8/8. Iterate until nothing fails.

1. Every named stakeholder carries a role, an evidence tier with the actual evidence cited, a confidence level, and a next action.
2. No High-confidence assignment rests on title alone; no champion is High-confidence without a passed capital-costing test, and the next ask names its rung plus why that rung and not the one above.
3. The economic buyer is named with evidence, or explicitly flagged unknown with the surfacing action - never silently omitted.
4. At least one blocker/detractor hypothesis exists, and at least one names a function not yet present on any call.
5. The coverage count is compared to the segment benchmark and single-threading is flagged if present.
6. Champion risk is answered: redundancy candidate, executive sponsor, and detection method each addressed (or honestly marked absent).
7. Every vendor statistic on the map is labeled correlational; no stated claim is presented as proven behaviour.
8. A refresh trigger is stated - the map declares when it goes stale.

## KPIs and measurement

- Per refresh, the map worked if:
  - Next actions from the prior version were executed and their assignments proved or disproved (an assignment that never moves off Tier 3-4 across two refreshes is a gap, not a fact).
  - The champion passed a new capital-costing ask.
  - No stakeholder appeared at proposal stage who wasn't at least hypothesized earlier.
- Across deals, track the share of maps where the EB was engaged before the proposal/solution-presented stage - top performers engage the EB early far more often in Ebsta/Pavilion's multi-million-opportunity analyses (**vendor-data**, correlational, platform-selection bias applies) - and the share of losses attributable to an unmapped detractor. Falling unmapped-detractor losses is the honest success signal.

Optional integration note:

- CRM contact-role fields seed Tier-4 hypotheses.
- Conversation-intelligence transcripts supply the Tier-1/Tier-2 behavioural evidence.
- Job-change alerting feeds the champion-risk row.

All three are categories - any tool of the class works, and the map functions with none of them.

## Reference

- [references/stakeholder-map-template.md](references/stakeholder-map-template.md) - fill-in-ready map template with B2C adaptations
- [references/worked-examples.md](references/worked-examples.md) - complete worked B2B map and an annotated naive counter-example
- [references/evidence-and-benchmarks.md](references/evidence-and-benchmarks.md) - buying-committee size figures, multithreading data with caveats, framework disagreements on role definitions, misquotation warnings
- `mbfinotti/sales-skills@meddpicc-scorecard` for scoring the deal against MEDDPICC criteria
- `mbfinotti/sales-skills@sales-discovery-questions` for building the discovery question set
- `mbfinotti/sales-skills@deal-red-flags` for the general red-flag review of deal notes
