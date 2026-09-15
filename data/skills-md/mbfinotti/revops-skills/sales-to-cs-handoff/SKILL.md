---
name: sales-to-cs-handoff
description: Design the sales-to-CS handoff process after a deal closes - what data transfers, when, in what artifact, and who is accountable - producing a handoff spec with a gated closed-won trigger, a required handoff packet, timing SLAs, a kickoff meeting pattern, and a CS acceptance/rejection step. For RevOps and Sales Ops designing and enforcing the process, not a CSM running one handoff. Use whenever the user mentions sales to CS handoff, post-close transition, closed-won to kickoff, handoff accountability, "the CSM starts from zero", or "customers repeat themselves after signing" - even if they never say "handoff". Covers B2B high-touch through PLG/self-serve and B2C subscription. Do NOT use for account health scoring - use mbfinotti/revops-skills@customer-health-score instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.6"
---

# CS Handoff

Design the process that moves a customer from the seller who won them to the owner who keeps them. Lincoln Murphy's diagnosis frames the stakes: "Customers hate three things: surprises, uncertainty, and repeating themselves" - and a poor handoff delivers all three before the customer's first call with CS. He attributes customers ghosting during onboarding "100% of the time" to a poorly designed - or not-designed-at-all - sales handoff process.

The design job has six decisions:

- The trigger event and its gate.
- The required data set.
- The artifact it travels in.
- The timing clocks.
- The meeting pattern.
- An accountability chain with an explicit acceptance step.

The named canon, where it genuinely helps:

- **Winning by Design's Bowtie Model** places Commit at the center of one continuous revenue lifecycle - the handoff is the seam between its two halves, not the end of a funnel.
- **Murphy's Desired Outcome** (Goal + Appropriate Experience) defines what must transfer: the customer's actual goal _and_ the experience they need to feel successful, not just contract terms.
- **Murphy's touch-level segmentation** sets coverage by what a segment needs, never by what it pays.
- **Kristi Faltorusso's "10 Essentials"** checklist is the best-known practitioner inventory of the information that must move ("If you are aligned on all of these details, you will be set up to have a productive partnership kickoff").
- **Time to First Value** (TTFV, Murphy) is the clock that starts ticking at the handoff moment.

Boundaries, stated because readers expect them here:

- Not employee/new-hire onboarding - ramping a new internal hire is a different job entirely.
- Not the drafting of a single recap email.
- Not the post-kickoff onboarding curriculum or 90-day success plan - this skill's job ends when the customer is successfully received by the post-sale owner and the first-value clock is running.
- Not health scoring or churn-signal discovery (sibling skills own those), though early-life churn is a legitimate outcome measure for handoff quality.
- Not pipeline-stage redesign - closed-won entry criteria are a gating input here, taken as given.

## Interview

Ask before designing. One question per message; offer multiple-choice answers where possible. Skip anything already answered.

- Which motion(s), and the segment mix? (a) sales-led enterprise/high-touch, (b) mid-market, (c) high-volume SMB, (d) PLG/self-serve, (e) B2C subscription - often several at once.
- Who exists post-sale? (a) dedicated named CSM, (b) pooled CS, (c) implementation/onboarding team then CSM, (d) no human - automated lifecycle only.
- How many closed-won deals per month, per segment? (Decides how heavy the artifact and meeting pattern can afford to be.)
- Today, how long from closed-won to kickoff (or first lifecycle touch)? Is it even measured?
- What does the CRM actually capture at closed-won today - enforced required fields, call recordings, free-text notes only?
- Is the AE compensated or held accountable past close (clawback, onboarding milestone, required intro)? This decides how much the process can ask of sales.
- Who can block or accept a handoff today? Has CS ever rejected one?
- What breaks today - customers repeating themselves, ghosting, kickoff delays, CSMs doing archaeology in old email threads?
- By when must the improved handoff be live - this quarter's closes, or next fiscal year? A hard date promotes the wiring and the live kickoff and defers the packet document.
- One-off fix, or a compounding asset? A compounding mandate promotes the acceptance step, whose reject codes only start rewriting the packet from the second quarter on.
- The effort ceiling: how many customer-success hours per handoff can the receiving team actually spend, and does CS have the standing to reject a rep's work? A low hour ceiling deletes the packet document and the internal sync; no standing deletes the acceptance step until a manager sponsors it.

## Ceremony, Ranked

Five things a handoff process can buy, ranked by retention bought per hour of customer-success time. Build down the list and stop where the segment's hour ceiling runs out. The axes disagree, which is the point - the strongest rung and the cheapest rung are not the same rung.

- efficiency: wiring > live customer kickoff > internal sync > acceptance step > per-deal packet document
- value: live customer kickoff > internal sync > wiring > per-deal packet document > acceptance step
- effort (CS hours per handoff): per-deal packet document > live customer kickoff == internal sync > acceptance step > wiring

| Rung                                                                                                      | What it costs                                                                                                      | What it buys                                                                                                          |
| --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| **Wiring**: must-block field gate on structured CRM fields, plus an assignment rule with a fallback owner | A one-off configuration pass of days; near-zero per handoff after that                                             | Context exists at all and every handoff carries a name - kills both the repeat-yourself complaint and the archaeology |
| **Live customer kickoff** with a visible transfer of ownership                                            | About an hour of the receiver's time, plus scheduling against the customer's calendar; one attempt, not repeatable | The ghosting fix - the customer leaves the call knowing who owns them now                                             |
| **Internal sync** before any customer contact                                                             | About an hour across two internal calendars                                                                        | Commitments and nuance surface before the customer tests them                                                         |
| **Acceptance step** with reason codes                                                                     | Minutes of receiver time per deal, plus the political capital to let CS reject a rep's work                        | Proves the packet was read; reject codes compound into a better packet definition each quarter                        |
| **Per-deal packet document** plus recordings review                                                       | Hours per handoff, split between rep and receiver                                                                  | Fidelity structured fields cannot carry - realized only where implementation spans teams                              |

The `==` on effort is real: kickoff and sync each cost about an hour of the receiver's time. What separates them is coordination and reversibility, not hours - the kickoff runs against the customer's calendar and gets one attempt, which is why efficiency ranks it above the sync where raw hours cannot.

Default rung: wiring plus the live kickoff, in every segment where a human receives the customer.

- Add the internal sync when more than one internal team delivers, or when commitment-related reject codes keep recurring.
- Add the packet document only when implementation genuinely spans teams.

What this order starves: the full high-touch ceremony - packet document, internal sync, line-by-line commitments review - loses every efficiency round, because its value concentrates in the few deals that would otherwise have failed loudly while the average deal shows no return. Promote it whole, ratio ignored, when:

- Losing one account would visibly dent the segment's renewal base.
- Services or an SOW ship with the deal.
- Regulated data requirements are in play.

Delete a rung, never demote it.

- Above SMB volume, per-deal acceptance is deleted and replaced by the sampling audit in [references/segment-variants.md](references/segment-variants.md).
- In PLG/self-serve and B2C, both meetings and the packet document are deleted outright - no human receives the customer, so ranking human ceremony there is fiction.

A rung parked at the bottom of the list comes back later as scope.

This ordering is a default, not a law: it shifts with volume, with who executes it, and with what the Interview surfaced.

- AEs compensated past close make the sync and the packet cheap to demand and move both up.
- A CS team that has never rejected a handoff cannot start with the acceptance step whatever its ratio says.
- Call recording already auto-captured raises the packet document by stripping most of its cost.

Re-rank against those answers before proposing anything.

## Workflow

1. Run the Interview; collect every answer before designing.
2. Define the trigger and its gate. Take closed-won entry criteria from the stage definitions as given input - do not redesign stages here.
   - **Trigger**: the closed-won event as the CRM records it.
   - **Gate**: the set of blocking conditions (required packet fields complete, required attachments present) without which the handoff must not fire.
3. Define the required data set from [references/handoff-packet-fields.md](references/handoff-packet-fields.md). Give every field a named supplier and a named consumer, and cut any field nobody reads at kickoff - an unread field is gate friction with no return. Fill in this order, by retention bought per minute of rep time: auto-captured call recordings > goal and success definition > commitments made during the sale > commercial terms > stakeholders with sentiment > technical requirements > marketing engagement history.
   - Recordings lead because tooling fills them at near-zero rep cost and they carry the nuance no field does.
   - Engagement history costs a rep nothing to skip and almost nobody opens it.
   - Must-block the top four.
   - Leave the rest optional, and promote technical requirements to must-block in any segment where integrations or an SOW routinely exist.
4. Choose the artifact per segment. Never chat threads or email as the artifact of record - context that lives there does not travel and cannot be gated.
   - Structured CRM fields for every human motion.
   - A system event payload for automated ones.
   - The per-deal packet document only under the promotion condition in Ceremony, Ranked - it is the bottom rung, not the default.
5. Set the two clocks: closed-won to internal handoff, and internal handoff to external kickoff held (or first automated touch). Defaults per segment in [references/slas-and-kpis.md](references/slas-and-kpis.md).
6. Design the meeting pattern where a human motion exists, taking both meetings and their build order from Ceremony, Ranked. Both are common practice, not a named framework.
   - **Internal sync**: the rep briefing the post-sale owner before any customer contact.
   - **Kickoff**: sales introducing that owner live.

   The visible transfer is what the kickoff buys, because, as Murphy puts it, "Sales STILL holds the keys to the relationship" until the customer knows who owns them now.

7. Assign accountability: a named owner for every step, and - wherever volume leaves room for per-deal review - CS explicitly accepts or rejects each handoff against the gate. Above SMB volume, the sampling audit replaces this step entirely.
   - Rejects bounce back to the rep with a reason code and a re-submission clock.
   - They never sit in limbo with the customer waiting.
8. Wire escalation.
   - SLA breaches and repeat rejects escalate to named manager roles.
   - Suspected bad-fit deals route to the sales/CS alignment forum rather than being absorbed - "Bad fit is not a Customer Success problem" (Sixteen Ventures).
9. Instrument the KPIs from [references/slas-and-kpis.md](references/slas-and-kpis.md), measured from CRM timestamps and reason codes, not from memory.
10. Emit the spec (next section) section by section for user validation; ground it in the matching worked example from [references/worked-examples.md](references/worked-examples.md).
11. Pilot on one segment for a full cycle of deals, review weekly, then roll out. Review reject reason codes and KPI misses monthly - recurring reject reasons are the packet definition telling you it is wrong.
12. If your harness has persistent memory, memorize the approved spec - gate, packet fields, clocks, acceptance rules, owners - so later revisions and per-segment extensions start from it instead of re-interviewing. Without memory, tell the user to keep the spec document as the standing input for future runs.

## B2B and B2C

The core mechanics are identical in both, and say so when asked. They apply unchanged from enterprise B2B to consumer subscriptions:

- A gated trigger.
- A defined data set.
- An artifact of record.
- Two clocks.
- An accountable receiver.

What genuinely differs is whether a human receives the customer:

- **Sales-led B2B**: the transfer is relationship-heavy - live meetings, a named owner, discovery intel and stakeholder context dominating the packet.
- **PLG/self-serve and B2C subscription**: there is often no human handoff by design - Murphy argues no-touch customers "should just be left alone", because over-serving them with human touch is itself a bad experience. The handoff is a system-to-system event (a CRM or billing state change) that triggers automated lifecycle onboarding, and the design question becomes which signals trigger which automated motion, and who owns exceptions - typically pooled, reactive CS or a growth/lifecycle-marketing owner rather than a CSM. The gate becomes data completeness on the account record; an activation event stands in for the kickoff.

Full per-segment treatment in [references/segment-variants.md](references/segment-variants.md).

## The Handoff Spec

Deliver every engagement as this artifact - a document RevOps can enforce and both teams can be held to. Fully worked versions live in [references/worked-examples.md](references/worked-examples.md).

```
HANDOFF SPEC - <company>, <date>, v<n>
Scope      : segments covered | explicit non-goals (onboarding curriculum, health scoring)
Trigger    : closed-won event definition + gate (blocking fields, required attachments)
Packet     : fields by category -> supplier -> consumer | must-block vs optional
Artifact   : where the packet lives per segment (CRM record, doc, event payload)
Clocks     : closed-won -> internal handoff | -> kickoff held (or first auto touch), per segment
Meetings   : internal sync + customer kickoff pattern per segment | or automated motion map
Acceptance : who accepts | reject reason codes | bounce protocol | re-submission clock
Escalation : SLA-breach path | repeat-reject path | bad-fit path
Automation : events fired at trigger (owner assignment, sequence enrollment, task creation,
             removal from sales sequences)
KPIs       : gate completeness % | both clocks | first-submission acceptance % | TTFV |
             early-life churn (outcome only)
Governance : process owner | acting owners per step | review cadence | change log location
```

## Objective and Pass Threshold

No standards body publishes handoff thresholds; these floors are this skill's starting conventions - calibrate them against the org's own baseline before treating them as law, and iterate the spec until all of them hold:

- **Gate completeness**: at least 95% of closed-won deals pass the gate complete on first submission.
- **Acceptance**: CS accepts at least 90% of handoffs on first submission.
- **Clocks**: internal handoff within 1 business day of closed-won; kickoff held within the segment SLA (default 10 business days for high-touch; first automated touch within the hour for self-serve).
- **Outcomes watched, not target-managed**: TTFV median measured and not worsening; early-life churn (first 90 days) tracked as the handoff's downstream outcome.

Read the failures diagnostically:

- Completeness near 100% with low acceptance means the gate checks the wrong fields.
- High acceptance with late kickoffs means the problem is scheduling or capacity, not data.

Definitions and instrumentation in [references/slas-and-kpis.md](references/slas-and-kpis.md).

## Common Failure Modes

| Symptom                                                 | Root cause                                    | Fix                                                                                                        |
| ------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Customer repeats context to every new face              | Packet not written, or written and never read | Gate blocks unwritten packets; acceptance step proves they were read                                       |
| Customer ghosts during onboarding                       | No visible transfer of ownership              | Live introduction at kickoff; sales stays engaged until CS accepts                                         |
| CSM does archaeology in email threads                   | Free-text notes are the only artifact         | Structured fields plus linked call recordings; chat/email never the record                                 |
| Promises surface after signature                        | No commitments field in the packet            | Capture every commitment (timeline, SLA, training, roadmap) as a must-block field; review at internal sync |
| CS accepts everything to keep the peace                 | Acceptance gate is theater                    | Reason-coded rejects, tracked and reviewed, with no penalty for rejecting                                  |
| Gate gamed with "N/A" in every field                    | Completeness measured as non-empty            | Spot-audit packet quality monthly; reject codes catch junk at acceptance                                   |
| Handoff fires into a pooled queue and vanishes          | No named receiver per handoff                 | Assignment rule with a fallback owner on every trigger                                                     |
| Self-serve volume forced through the enterprise process | One process designed for the largest deal     | Segment variants; automate everything below the human-touch line                                           |
| Bad-fit customers blamed on onboarding                  | No shared definition of a qualified customer  | Route to the sales/CS alignment forum; fix upstream in stage criteria                                      |

## Invocation Examples

- "Our CSMs start from zero on every new account and customers complain about repeating themselves - design a real sales-to-CS handoff process."
- "We close 60 deals a month across mid-market and self-serve; kickoffs happen anywhere from 3 days to 5 weeks after signature. Build the handoff spec with SLAs and an acceptance gate."
- "We're pure PLG with pooled CS - what does a handoff even mean for us, and what should trigger what?"

## Reference

- Read [references/handoff-packet-fields.md](references/handoff-packet-fields.md) when defining the data set - the field-by-field packet, grouped by category, with why each field transfers and who supplies it.
- Read [references/segment-variants.md](references/segment-variants.md) when the org spans motions - how trigger, artifact, timing, meetings, and ownership change from enterprise to B2C subscription.
- Read [references/slas-and-kpis.md](references/slas-and-kpis.md) when setting clocks and instrumentation - SLA defaults, the acceptance gate mechanics, reason codes, KPI definitions, and the review cadence.
- Read [references/worked-examples.md](references/worked-examples.md) when shaping the deliverable - a filled spec, a filled packet, and a negative example with its cost.
- See `mbfinotti/revops-skills@pipeline-stage-definition-audit` for the closed-won entry criteria this skill's gate builds on - stages are its output, this skill's input.
- See `mbfinotti/revops-skills@crm-data-governance` for who owns and maintains the fields the packet depends on once the process is live.
- See `mbfinotti/revops-skills@customer-health-score` for health scoring that starts from the packet this skill defines.
- See `mbfinotti/revops-skills@customer-churn-signals` for churn signals that emerge after the handoff - the first baseline is set from the packet this skill defines.
- See `mbfinotti/revops-skills@revenue-leakage` for quantifying what unmanaged handoff gaps cost - that skill finds the leak, this one closes it.
- See `mbfinotti/revops-skills@lead-routing` for assignment-rule patterns when picking the post-sale owner from a pool - the routing logic transfers directly.
