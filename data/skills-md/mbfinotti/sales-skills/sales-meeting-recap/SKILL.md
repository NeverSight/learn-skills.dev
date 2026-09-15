---
name: sales-meeting-recap
description: Turns raw sales call notes into a structured recap email with agreed next steps - every action item carrying an owner, a date, and a deliverable - plus mutual close plan (mutual action plan) items when the deal warrants one. Restates the buyer's pain in their own words and never invents a commitment the notes don't contain. Covers complex B2B committee deals and transactional or B2C motions. Use whenever the user mentions a recap email, follow-up after a sales call, next steps email, post-call summary, or a mutual action plan, even without the word recap. Do NOT use for judging how the call went (mbfinotti/sales-skills@sales-call-review).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.4"
---

# Meeting Recap

Convert the user's call notes into two artifacts: a recap email the buyer will ratify by replying, and mutual close plan items when the deal is complex enough to warrant a shared plan. The organizing rule is Armand Farrokh's (30MPC): a recap email answers exactly two questions - "Did you make it clear what the prospect needs to do next?" and "Did you remind them why they agreed to take action?" Everything else is decoration, and "nothing should get in the way of what we want them to do."

Second rule: the recap is champion-enablement content. A buying group gives any single vendor only around 5-6% of its purchase time (Gartner 2017 B2B buyer survey), so the email does most of its selling in rooms the rep never enters - write it to be forwarded.

Scope boundaries:

- Work only from notes, transcripts, or descriptions the user supplies.
- Never score or critique how the call was run - that belongs to `mbfinotti/sales-skills@sales-call-review`.
- The post-sale handoff from sales to customer success is out of scope entirely.

## Interview

Ask one question per message; offer multiple-choice options; skip anything the notes or context already answer.

1. Who was on the call - names and roles on both sides? Which buyer contacts should receive the recap?
2. B2B or B2C? Buying committee, or a single decision-maker?
3. Deal stage: first connect, discovery, demo, proposal, or negotiation?
4. Rough deal size and expected cycle length? This sets the recap's weight and whether a close plan pays off.
5. What was actually agreed on the call - commitments, owners, dates, exactly as stated?
6. Is the next meeting booked with a calendar invite? If not, was a specific date discussed?
7. Does a mutual close plan already exist for this deal, or should this call seed one?
8. By when must the recap land - within the hour, today, or is tomorrow acceptable? A same-hour answer promotes the short recap and deletes anything needing a working session.
9. One-off win or compounding asset: this deal's follow-up only, or a pattern repeated across the pipeline? Compounding promotes the close plan and the automated sequence; one-off promotes the hand-written recap alone.
10. Effort ceiling: how many minutes per recap, across how many live deals? A tight ceiling deletes the full mutual action plan and caps the recap at one screen.

Every ordering below is a default, not a law - it shifts with the deal, with the pipeline, and with who executes it. Re-rank each one against these answers and against what you already know about the user: a rep running dozens of small deals, a single strategic pursuit, and a CRM that already auto-drafts recaps each invert a different ordering. Delete the options their constraints rule out rather than parking them at the bottom, where they quietly reappear as scope.

## Anti-fabrication rule

The load-bearing guard. A recap containing a commitment the buyer never made destroys the shared record it exists to create.

- Never invent a commitment, owner, date, quote, attendee, or decision the notes do not contain.
- Treat a gap as output, not as something to fill: list missing owners, dates, and unconfirmed items in an "Open gaps" block and ask the user.
- Mark any step the buyer did not explicitly agree to as "proposed - confirm before sending".
- Reuse the buyer's own words for the pain, verbatim - their phrasing, their numbers. Never translate their language into marketing copy (practitioner rule: "confirmation, not summary").

## The recap email

30MPC's 3-step recap email (Armand Farrokh):

1. **Lead with next steps** - action items at the very top, each with an owner and a date; make the buyer's own items visually unmissable.
2. **Recap problems, not features** - restate the pain in the prospect's own words, never a list of capabilities.
3. **Keep it short and skimmable** - the whole email fits on one phone screen.

### What earns space on the one screen

One phone screen is the whole budget, so these elements compete for it. Ranked by value per rep minute, best ratio first:

1. **Dated next-steps block at the top** - near-zero extra minutes, part of the recap email already being written. Buys the only thing separating a call from progress: something the buyer must do, by a date.
2. **The buyer's pain in their own words** - near-zero when the notes caught the quote, one more pass through the transcript when they did not. Buys the forward: it is the line that survives the champion's internal debrief.
3. **A send list across the committee** - minutes per deal to find and justify the contacts, redone from scratch on the next deal. Buys the largest measured effect in this section: single-threading is the dominant structural failure, closed-won deals carry 67% more contacts, and multithreading lifts win rates ~130% on $50K+ deals (Gong Labs; sample disclosed, method proprietary).
4. **A closing ratification question** - one line, "Anything I missed?". Buys a reply, and a reply turns the recap into an agreed record.
5. **A subject under 50 characters, next-step-anchored** - one line, plain: "Next steps - Acme + Yourco". Buys the open and nothing past it; 1-4 words performs best (Gong).
6. **The one attachment the buyer asked for** - near-zero to attach, longer when it must be produced first. Buys credibility on a single asked-for item. Never list attachments as action items.

- value: next-steps block > pain in their words > send list > ratification question > subject line > attachment
- effort: send list > attachment > next-steps block == pain quote == ratification question == subject line - those four tie at genuinely near-zero, each being one line or one paste written in the same pass as the email itself

The ratio starves the send list: it is the only row costing real minutes per deal, so a minutes ceiling cuts it first. Promote it regardless of ratio the moment the notes name more than one buyer stakeholder - there is no cheaper substitute for a contact who was never emailed.

Deleted, not demoted. Keep these out of the draft entirely, since they lose on every axis:

- A capability or feature recap (step 2 forbids it).
- Full meeting minutes (a different artifact).
- Rapport prose like "wonderful to connect", which reads as automation.

Unranked on purpose, because they cost nothing and apply to every recap:

- Cap bullets at ~4, max two lines each (30MPC).
- Write plain text that any email client renders as-is - no markdown syntax, headers, or asterisk-bold.

**When to send.** value: within hours of the call > later the same day > next morning > multi-day. Effort is identical at every rung - same email, same minutes - so nothing trades against speed. Send before the buyer's internal debrief, always (timing norm).

Filled strong and negative examples: [references/recap-email-examples.md](references/recap-email-examples.md).

## What makes a next step real

- Real = **Owner + Date + Deliverable**, plus a calendar invite for any meeting. Missing any part means a nice conversation, not progress (practitioner definition).
- Reject "circle back", "next week", "soon", "ASAP" as dates. The forced choice defeats vagueness: "Thursday or Friday?" (technique).
- Assign one named owner per item - a person, never a team.
- Activity is not advancement: extra demos and reference calls without confirmed movement through the buyer's decision process are not progress (MEDDICC).
- When the notes show no committed next step, do not manufacture one. Flag it, and prescribe 30MPC's 5 Minute Drill for the next touch (framework): "Do you wanna buy?", "When do you wanna buy?", "How do you wanna buy?" - commitment, timeline, then the recommended multi-step path.

## Mutual close plan

Three rungs answer "how much plan does this deal need". Ranked by value per rep minute, best ratio first:

1. **A booked next meeting, no plan** - near-zero minutes, and the only rung that scales across a whole pipeline. Buys what most deals actually need: somewhere for momentum to live. Default rung.
2. **Two or three seeded milestones inside the recap** - a few extra minutes on top of the recap, one deal at a time. Buys an early look at the paper process and at least one buyer-owned step, without asking the buyer to co-own a document yet.
3. **A full mutual action plan** - an hour to build, then a standing job to keep current through every call until go-live. Buys coordination a committee deal gets no other way: dated, owned milestones through security review, legal and procurement.

- value: full plan > seeded milestones > booked meeting
- effort: full plan > seeded milestones > booked meeting
- efficiency: booked meeting > seeded milestones > full plan (the axes agree on the first two lines and invert on the third - that inversion is the whole point)

The efficiency order starves the full plan: it is the most expensive rung per deal and loses every ratio round, yet it is the only thing that holds a complex deal together. Promote it regardless of ratio when a buying committee, a multi-call cycle, or procurement or security review sits in the path - roughly $50K+ ACV (threshold reasoning: the multithreading payoff is measured on $50K+ deals). Below that line, delete rungs 2 and 3 from the output rather than offering them: a plan left on the menu for a single-decision-maker deal comes back as scope the rep never had minutes for.

- 30MPC's editorial position, quoted: "If your sales process involves more than a 1-call close...you should be using Mutual Action Plans on every deal." (Treat the rung ladder above as the practical friction-versus-control judgment on top of that stance.)
- Build it as a shared document co-owned by the rep and a buyer project lead; the irreducible columns are milestone, owner (buyer and seller), and date (Salesforce Salesblazer).
- Work backwards from the buyer's compelling event or go-live date - never the seller's quarter-end.
- Extend past signature to onboarding and first measured value, so the plan doesn't read as a device to extract a contract.
- Surface the Decision Process and Paper Process early (MEDDICC / MEDDPICC, Andy Whyte): security review, DPA, MSA redlines, procurement. "60% of deals are lost to inertia" (MEDDICC-published stat).
- Never dump a full plan on a buyer who hasn't agreed to co-own it: enter rung 3 through rung 2, then ask for a working session and sign-off (Salesforce tactic).
- Evidence honesty: the circulated MAP win-rate uplifts ("26%", "57-200%") are vendor self-reports with no disclosed methodology and obvious selection bias. Directional at best - never present them as fact.

Column layout, milestone taxonomy, the Salesforce 5-part structure, and co-ownership tactics: [references/mutual-close-plan.md](references/mutual-close-plan.md).

## B2B and B2C

Identical in both, explicitly:

- Same-day timing.
- Owner + Date + Deliverable.
- The anti-fabrication rule.
- Buyer's-own-words pain.
- Plain-text formatting.
- The humanizer pass.
- The Quality gate.

Consumer-sales follow-up practice (real estate, med spas, automotive, gyms, financial advisory) converges independently on the same two disciplines this skill applies to B2B: reply within about two hours of the call, and personalize to what the buyer actually said rather than a generic template - the same-day timing and buyer's-own-words rules above are not a B2B convention stretched onto B2C, they hold natively in both.

Four recap weights, listed lightest to heaviest. The ranking is the pair of efficiency lines below, not this list order - which weight wins per rep minute inverts with who is executing:

1. **Automated lifecycle sequence** - a week to build once, then near-zero minutes per deal, and it is the only option that covers a whole pipeline at once. Buys coverage, never the buyer's own words.
2. **Short recap** - minutes per deal, one deal at a time. Three to five sentences, one next step with a real date, no close plan. Fits transactional, self-serve, single-decision-maker, and B2C motions including high-ticket consumer (solar, real estate, financial advisory).
3. **Full recap to multiple contacts** - tens of minutes per deal. Buys the multithreaded, forwardable record a committee deal runs on.
4. **Full recap plus mutual close plan** - an hour, then a standing job. Buys coordination through the buyer's paper process.

- value per deal: full recap + plan > full recap > short recap > automated sequence
- effort per deal: full recap + plan > full recap > short recap > automated sequence (the sequence is last only because its cost is paid once, up front, not per deal)
- efficiency, a rep running dozens of small deals: automated sequence > short recap > full recap, with the plan deleted outright
- efficiency, a single strategic pursuit: full recap + plan > full recap > short recap, with the sequence deleted outright

Default weight:

- B2B committee deal: the full recap, promoted to full recap plus plan under the close-plan conditions above.
- Transactional, self-serve, and B2C motions: the short recap.

Reserve the human recap for deals worth the minutes - in high-velocity motions it is often replaced by automated lifecycle sequences entirely (carve-out for transactional sales).

## Workflow

1. Run the Interview; skip answered questions.
2. Parse the notes: agreed commitments with owner/date/deliverable as stated, the buyer's pain in their words, decisions, open questions, and stakeholders mentioned but absent from the call.
3. Apply the Anti-fabrication rule: separate agreed from proposed; collect every gap.
4. Pick the recap weight from B2B and B2C, then draft with the 3-step structure, spending the one screen in the ranked order above.
5. Pick the close-plan rung. At rung 2 or 3, and only if the buyer signalled willingness to co-own it, draft or update milestones per [references/mutual-close-plan.md](references/mutual-close-plan.md); at rung 1, state in the output which rung you chose and why.
6. If your harness can create calendar events or send email, offer to book the next meeting and place the draft - never send without explicit approval. Otherwise deliver text the user can paste.
7. Optional integration note: if your environment connects to a CRM, a call-recording platform, or an AI notetaker, offer to pull the transcript as input and log the recap as an activity - pulled content is still just notes, under the same anti-fabrication rules.
8. Run the draft through your preferred humanizer skill. Raw first-draft output is never final.
9. Run the Quality gate; redraft until every check passes.
10. Deliver the output shape below. If your harness has persistent memory, store the deal's open action items and plan state so the next recap starts from live state instead of a blank page.

## Invocation and expected output

- "Here are my notes from the Acme demo - draft the recap email."
- "Turn this discovery call into a follow-up with next steps and start a mutual action plan."
- "Quick post-call summary for a small deal, single contact."

```
SUBJECT     : under 50 characters, next-step-anchored
RECAP EMAIL : plain text; next steps first (Owner - Deliverable - Date,
              buyer items highlighted), pain in the buyer's own words,
              attachments named, closing ratification question
CLOSE PLAN  : chosen rung, plus new or updated milestones (milestone |
              buyer owner | seller owner | date) at rung 2 or 3
OPEN GAPS   : missing owners/dates, unconfirmed commitments marked
              "proposed - confirm before sending", questions for the user
SEND LIST   : who receives the email and why (multithreading check)
```

## Quality gate

Pass threshold: every check, no exceptions. Redraft and re-check until nothing fails. Deliberately unranked: these are pass/fail gates, not options traded against each other, so ordering them would only imply the cheap ones are skippable.

1. 100% of action items carry Owner + Date + Deliverable - zero vague dates ("next week", "soon").
2. The next meeting has a real calendar date and an invite, or the output flags the gap and prescribes the 5 Minute Drill.
3. Email fits one phone screen, under ~200 words (short-motion recap: 3-5 sentences).
4. Subject line under 50 characters.
5. The buyer's stated pain appears verbatim in their own words; no feature list anywhere.
6. Every commitment traces to the notes, or is marked "proposed - confirm before sending"; gaps are listed, never filled.
7. On committee deals, at least one action is buyer-owned - or the seller-only imbalance is flagged as a risk.
8. The send list covers the relevant buyer contacts, or states why a single recipient is right.
9. The draft went through the humanizer pass.

## KPIs

Instrument in this order - value per unit of setup effort, best ratio first:

1. **Next-step-set rate**: % of open opportunities with a scheduled, calendar-booked next step. A count the CRM already holds, and the only metric here with a pass mark - practitioner benchmark ~80%. Below that, fix this before any close-plan rollout (recommendation). Start here.
2. **Multithreading rate**: buyer contacts engaged per deal. Also already in the CRM (direction solid, magnitudes are marketing - Gong).
3. **Recap reply rate** - per-deal tracking to set up once, then near-zero. A reply ratifies the record; track it per deal stage.
4. **Stage conversion and slipped-deal rate** on deals with vs. without a dated next step - one pipeline report answers both.
5. **Sales-cycle length** - a full quarter of data before it says anything. Context for the stakes: 40-60% of qualified B2B deals end in no decision (Dixon and McKenna, The JOLT Effect, 2.5M conversations) - next-step discipline attacks exactly that.

- value: next-step-set rate > sales-cycle length > stage conversion == slipped-deal rate > multithreading rate > recap reply rate (those two tie because they are the same pipeline query over the same window, and neither moves before the other)
- effort: sales-cycle length > stage conversion == slipped-deal rate > recap reply rate > next-step-set rate == multithreading rate (this pair ties at near-zero: both are counts the CRM already stores, read from the same report)

The order starves sales-cycle length - a quarter of waiting kills its ratio every round. Promote it anyway when the question is whether to roll recap discipline out across a team; nothing cheaper produces that evidence. And never measure close-plan success by vendor win-rate uplift claims: instrument your own before/after comparison.

## Failure modes

Rows are defect-and-fix pairs, not competing options - each fix is the only fix, so there is nothing to rank.

| Failure                                        | Fix                                                                        |
| ---------------------------------------------- | -------------------------------------------------------------------------- |
| "Circle back next week" as a next step         | Owner + Date + Deliverable, or list it under Open gaps                     |
| Every action owned by the seller               | Surface buyer-owned steps from the notes; flag the imbalance if none exist |
| Feature dump instead of the buyer's pain       | Their problem, their words, verbatim                                       |
| No calendar invite for the next meeting        | Real date plus invite, or flag and prescribe the 5 Minute Drill            |
| Recap sent to one contact on a committee deal  | Build the send list; single-threading is the top structural failure        |
| Commitments the buyer never made               | Anti-fabrication rule; mark "proposed - confirm before sending"            |
| Full close plan dumped on an unconsulted buyer | 2-3 agreed milestones, then a working session and sign-off                 |
| Recap sent the next morning                    | Same day, within hours, before their internal debrief                      |
| Markdown formatting in the email body          | Plain text only                                                            |
| A recap the length of meeting minutes          | One phone screen; minutes are a different artifact                         |

## References

- [references/recap-email-examples.md](references/recap-email-examples.md) - a strong filled example, a negative example annotated defect by defect, and a short-motion B2C variant.
- [references/mutual-close-plan.md](references/mutual-close-plan.md) - columns, milestone taxonomy, the Salesforce 5-part structure, when to introduce, buyer co-ownership tactics, and a worked micro-example.
- `mbfinotti/sales-skills@meddpicc-scorecard` - qualifies the deal; this skill's close plan operationalizes its Decision Process and Paper Process elements.
- `mbfinotti/sales-skills@deal-champion-mapping` - identifies who the recap should be written through and who belongs on the send list.
- `mbfinotti/sales-skills@deal-red-flags` - a missing dated next step or a seller-only plan surfaced here is an input signal there.
- `mbfinotti/sales-skills@deal-value-calc` - builds the forwardable business case; the recap carries its numbers into the buyer's internal debrief.
