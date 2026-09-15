---
name: event-speaker-cold-outreach
description: Write and sequence the cold invitation to a speaker a shortlist already picked - the message, not the search. Covers what a first invitation must disclose up front (event basics, honest budget and travel terms, the answer deadline, how you found them), personalization built from the shortlist's own "why", ranked first-touch channels, follow-up cadences that add a new angle instead of bumping, and the fee conversation where speakers have no rate card. Use whenever the user mentions writing a speaker invitation, pitching a keynote candidate, following up on an unanswered invitation, or a speaker who asks for a fee - even if they never say "outreach". Do NOT use to find or qualify candidates - use samber/dev-event-organizer-skills@event-speaker-sourcing instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Speaker Cold Outreach

You write the invitation and run it to an answer. Your input is the packet `samber/dev-event-organizer-skills@event-speaker-sourcing` hands you - ranked candidates, the evidence-backed "why" behind each name, a Hot/Warm/Cold/Skip score, availability and travel constraints, the honest budget line, the contact route, and the invited-review lane. Your output is a confirmed speaker with terms agreed in writing, or a recorded no.

This skill's boundaries:

- Not sourcing or qualifying candidates: a name that arrives without its "why" goes back to sourcing, because the "why" is the message.
- Not the open call design: `samber/dev-event-organizer-skills@event-cfp-design` owns that.
- Not the invited-proposal review: `samber/dev-event-organizer-skills@event-talk-selection` owns that lane, and the packet already states which one applies.
- Not what happens after a yes: briefing, travel and on-site care belong to `samber/dev-event-organizer-skills@event-speaker-experience`.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 4-6 exist because the menus below diverge sharply on time-to-effect, durability and effort - those defaults cannot be picked for the user.

1. What does the sourcing packet contain for this slot: ranked candidates, the slot brief they were ranked against, each one's "why" and its evidence, the Hot/Warm/Cold/Skip score, availability and travel constraints, the honest budget line, the published contact route, and the invited-review lane? Anything missing goes back to sourcing rather than getting invented in the message.
2. Who owns the event: community conference or vendor/user conference? This changes what the invitation can honestly offer.
3. Which slot is this, and how many candidates are queued behind it? Decide now whether you approach them one at a time or in parallel - see failure modes, because two yeses for one slot are a worse problem than one no.
4. By what date do you need an answer, and what is the last date a yes is still usable once travel is counted? A hard date promotes the fast rungs and deletes the long cadence outright.
5. One-off edition, or a compounding annual program? A compounding mandate promotes the expensive personalization rungs: a candidate who declines this year with the relationship intact is next year's first call.
6. What is the effort ceiling: who actually writes these invitations, how many hours, and how much of your own name you are willing to spend on referral asks and personal introductions?
7. What can the budget honestly cover, phrased as a sentence you are willing to put in the first email - nothing beyond a ticket, travel, lodging, a fee? If it is unconfirmed, "unconfirmed" is what goes in the email.
8. What is negotiable if the answer is "yes, but": date, slot length, format, remote delivery, travel dates, a companion ticket, recording terms? Fix that list before the first message, never during the negotiation.
9. Who has authority to agree a fee or a condition, and is that person you? If not, name them and the turnaround, because a candidate waiting on your internal approval is a candidate cooling.

## Community-run vs vendor/user conference

What changes the invitation is who owns the event, the same replacement the rest of this collection argues:

- **Community-run** - the invitation trades on the audience and the peer group, because that is genuinely all it has. Budget is usually thin, which makes the honesty rule load-bearing rather than polite: an invitation that stays vague about money is asking someone to block a weekend on a guess. A sponsor never buys a speaker slot, so a candidate arriving through a sponsor relationship gets invited on the same terms as anyone else or not at all.
- **Vendor/user conference** - invitation is the main intake rather than the backup channel, budget is usually real, and the ask can carry a fee and full travel. The offer changes; nothing about the disclosure rules or the cadence does. Published organizer guidance is written for the community pole, so treat every vendor-pole adjustment here as judged rather than established practice.

Say which pole a recommendation assumes whenever they differ.

## Workflow

1. Run the interview. Confirm the packet is complete (Q1) and fix the pole (Q2), the answer date (Q4), the honest budget line (Q7) and the negotiable list (Q8).
2. Check the travel gate before writing anything. If the candidate has to travel and your answer date sits inside the four-to-six-week floor, you are about to send an invitation that can only be declined. Say so in the message rather than letting them discover it, or move to a candidate who does not travel.
3. Pick the first-touch channel from the menu below, per candidate, against the published contact route in the packet.
4. Pick the personalization depth from the menu below, tiered by the candidate's Hot/Warm/Cold score - effort scales with fit.
5. Write the invitation against the disclosure list below, then cut it to length. Every message-craft constraint - the five-part structure, the word cap, the banned vocabulary, the subject-line rules - is in [references/invitation-message-craft.md](references/invitation-message-craft.md), each with its transposition labelled.
6. Run the invitation past a humanizer pass in your preferred humanizer skill before sending. A model-shaped invitation to a practitioner who reads model-shaped email all day is the fastest way to be ignored.
7. Send through the chosen channel, one candidate per slot per thread. Never let two candidates for the same slot see each other.
8. Follow up on the cadence menu below, respecting its cap. Every touch carries something the last one did not; honor an opt-out the moment it arrives, mid-sequence, not at the next scheduled touch.
9. Run the fee-and-conditions conversation off the honest-budget line when the answer is "yes, but" - see below, and the scripted shapes in [references/cadence-and-fee-conversation.md](references/cadence-and-fee-conversation.md).
10. Close the loop: confirm a yes in writing with every agreed term, or record a no with its reason and ask for a referral. Then hand off or move to the next candidate.

Show the user the drafted invitation before it goes out. An invitation cannot be unsent, and a candidate asked by mistake has already been asked.

If your harness has persistent memory, record per candidate:

- the channel used
- the angle each touch carried
- the answer and its date
- the reason behind any decline
- any condition you agreed

That record is what makes next edition's outreach yours rather than this skill's defaults.

## What the first invitation must state

The first message is incomplete without every one of these.

- **Event basics** - size, location, dates. A speaker cannot evaluate an invitation without knowing when and where.
- **How you found them**, in the first line - their talk at X, their post on Y, a colleague's referral. This is simultaneously the strongest personalization available and the consent-respecting move, which is why it is one instruction and not two: a directory listing or a public profile is consent to be _found_, never consent to be pitched.
- **The specific angle**, drawn from the packet's "why" - the candidate's own recent work, not a compliment about their reputation.
- **Why this slot, this audience, this stage** - the differentiator aimed at a speaker's incentive (a peer audience, a room worth being seen in, a topic they have been trying to get a hearing for), not at the organizer's need.
- **Honest terms, up front** - what the budget covers, including when the answer is "nothing beyond a ticket" or "unconfirmed", plus the confirmation deadline. Silence on money reads worse to a speaker than to a sponsor - a sponsor expects a negotiation, a speaker is being asked to block a calendar.
- **A low-friction, specific ask** - a proposed next step, never an open-ended "let me know."
- **No links, attachments, or images in the first email.** Corporate phishing filters auto-trash mail carrying them, and a speaker's work address is exactly that kind of inbox. The CFP page, the program and your logo all wait for the second touch.

## First-touch channel

Per candidate, the route the first message travels.

Every ranking below is a default, not a law. After the interview, re-rank all three menus against what you know about this organizer. Any of these can overturn a default rung:

- a program chair the candidate already knows
- a referrer willing to make the introduction
- a confirmed travel budget
- a conference you and the candidate are both attending next month

Ranking (default, not a law - Q3, Q4 and Q6 re-rank it):

- effort (per candidate contacted: coordination, social capital spent, travel, your own hours): `in-person ask > referrer-relayed intro > direct email == published DM`
- value (a considered answer, not merely a reply): `in-person ask == referrer-relayed intro > direct email > published DM`
- compliance cost (review triggered, reversibility spent): `direct email == published DM > in-person ask > referrer-relayed intro`
- efficiency: `referrer-relayed intro > direct email > published DM > in-person ask`

- **Effort tie:** an email and a DM are the same act - one composed message to a route the person published. The channel changes the character limit, not the work.
- **Value tie:** both top rungs arrive through a relationship rather than through an inbox, one carrying a third party's vouch and the other your physical presence, and neither has to survive the unread-mail filter that actually kills the two written rungs.
- **Compliance tie:** the same act seen from the other side - unsolicited written contact to a named individual, with contact details retained and a message that cannot be unsent, is consent and e-marketing territory (GDPR, CAN-SPAM and kin) whichever pipe carries it.

- **Referrer-relayed introduction** - the default wherever the path exists: the person who referred the candidate, or a mutual contact, forwards the ask or makes the introduction. Cheapest strong rung, because a vouch arrives attached and you contact nobody until the candidate answers. Exhaust it per candidate before anything colder, though it exists for only part of any shortlist.
- **Direct email to a published address** - the default everywhere else, and the rung every message-craft rule in this skill was written for. Beats the DM on value because email is where a considered answer gets written, while a DM invites a fast reflexive one to a request that needs a calendar check and often an employer's sign-off (a judged ordering, not a measured one).
- **Published DM or social contact route** - the right rung when it is the only route the candidate published, which is common for candidates sourced by community scouting. Same effort and same compliance exposure as email, lower value, so efficiency puts it below.
- **In-person ask** - the starved option: ask at an event you are both attending. It ties for the top of value and tops effort outright, so efficiency never picks it. Promotion conditions: a keynote or headline slot where a no costs the program most, a candidate who has already let a written approach go unanswered, or a conference you are both attending anyway before the answer date (Q4).
- **Deleted, not demoted: guessed or scraped addresses, and the candidate's community space as a contact route.** A guessed work address is not a cheap last resort, it is out. So is soliciting inside a project forum, chat or issue tracker: many community codes of conduct treat recruiting and solicitation in their spaces as off-limits, the breach is public, and it cannot be walked back. Use the contact route the person published instead; parked at the bottom of a menu, both quietly return as scope when the shortlist runs thin.

## Personalization depth

How much of the invitation is about this specific person. Ranking (default, not a law - Q5 and Q6 re-rank it):

- effort (minutes per invitation, and whose minutes): `program-shaped ask > fresh-work personalization > sourced-"why" > slot-brief line`
- value (a reply that engages with the actual offer instead of declining politely): `program-shaped ask > fresh-work personalization > sourced-"why" > slot-brief line`
- compliance cost (review triggered, reversibility spent): `fresh-work personalization == program-shaped ask > sourced-"why" == slot-brief line`
- efficiency: `sourced-"why" > fresh-work personalization > slot-brief line > program-shaped ask`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks all six pairs: the deeper ask buys a better reply and costs strictly more minutes.

The compliance axis re-orders the menu and rescues nothing, because a dominance relation needs value ≥ _and_ every cost ≤, and the effort half is already lost in every pair. The check catches no misordering; the efficiency line rests on the arguments below.

Both compliance ties are genuine and split the menu cleanly in half:

- **The two deep rungs** go past the shortlist's recorded evidence into fresh research on a named individual, where the line between "read their public work" and "assembled a file on them" is yours to hold.
- **The two shallow rungs** use only what sourcing already recorded and dated for exactly this purpose.

Efficiency inverts the value order at the top for one reason worth stating: the sourced-"why" is already paid for. Sourcing bought that evidence to qualify the candidate, and re-using it costs you one sentence.

- **Slot-brief line** - the floor: name the specific slot, theme and audience, with nothing candidate-specific. Cheapest, and it sits below fresh-work on efficiency anyway, because cheap and efficient are different orderings - a generic invitation sent to someone you chose specifically throws away the qualification that got them onto the list.
- **Sourced-"why" personalization** - the default for every candidate: open on the specific evidence the packet recorded, the talk or the post or the project, and connect it to the slot. Costs a sentence and returns most of what deeper research would.
- **Fresh-work personalization** - read what they published this month, past the packet's evidence, and open on that instead. Promote every Hot candidate to this rung, and every candidate for a slot that concentrates the program's risk.
- **Program-shaped ask** - the starved option: restructure the invitation around a talk only this person could give, naming the gap in the program their work fills, effectively co-designing the slot before they answer. It tops both value and effort, so efficiency never picks it. Promotion conditions: a keynote, a candidate who declined a previous edition, a compounding annual mandate (Q5) where the relationship outlives this slot, or a slot no shortlisted candidate quite fits.
- **Deleted, not demoted: the merge-field blast to the whole shortlist.** One template, one mail-merge, every candidate at once. It is not the bottom rung of this menu; it is the thing that makes the entire shortlist worthless, and it is one slip away from the CC failure mode below.

## Follow-up cadence

After the first touch, how many times and how spaced. Ranking (default, not a law - Q4 and Q6 decide this menu almost alone):

- effort (touches written, threads tracked, and how long the slot stays held open): `long-runway cadence > three-touch angle cadence > single ask`
- value (answers recovered from silence, including a no you can act on): `long-runway cadence > three-touch angle cadence > single ask`
- compliance cost (review triggered, reversibility spent): `long-runway cadence > three-touch angle cadence > single ask`
- efficiency: `three-touch angle cadence > single ask > long-runway cadence`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and that is not a pass.** All three axes run in one order, so a single mechanism blocks every pair: the cadence that recovers more answers is strictly worse on both cost axes.

Compliance restates the effort order rather than re-ordering it, so it cannot rescue a pair either. The check verifies nothing here; argue with the ratios below.

The compliance axis needs no ties: it tracks touch count directly. Every additional unsolicited message to somebody who has not replied is more exposure, not less - silence is not consent to keep writing, and no touch can be recalled.

- **Single ask, then stop** - send once and read silence as a no. Its whole cost is one message, and it frees the slot the same day for the next candidate.
- **Three-touch angle cadence** - the default: Day 0, Day 3 _only if you have new information_, Day 7 with a genuinely fresh hook, then stop. Disciplined enough for a volunteer organizer and short enough that the slot does not rot behind it.
- **Long-runway cadence** - the starved option: one to two weeks between touches, capped at three, tightening to three or four days as the answer date closes in. It tops value and effort together, so efficiency never picks it - yet it is the only cadence shaped for the candidate who has to get an employer's sign-off and arrange travel, which is most invited speakers.
  - Promotion conditions: a candidate who needs internal approval, an international candidate inside the four-to-six-week travel window, or a slot with no viable next candidate behind it.
  - Efficiency ranks it below even the single ask: its real cost is not the touches, it is the weeks a slot stays held open behind someone who may never answer, and an open slot is the scarcest thing in an invited program.
- **Deleted, not demoted: the bump.** "Bumping this up", "did you see my email", the same pitch reformatted - deleted here rather than ranked. Never bump; always add an angle. In a community whose members talk to each other, a bumped invitation costs the event's name more than the slot is worth.

Rotate a genuinely new angle into every touch:

- a confirmed co-speaker
- a program detail that landed since
- a specific audience question their work answers

The full angle table is in [references/cadence-and-fee-conversation.md](references/cadence-and-fee-conversation.md).

## The fee and conditions conversation

A sponsor negotiation has a rate card behind it. A speaker invitation has nothing equivalent - there is no published price, no tier, and no norm. What you have instead is the honest-budget line fixed at Q7, and it is fixed _before_ the first message, stated _in_ it, and not rediscovered under pressure.

- **When the candidate names a fee**, you have no market rate to check it against, and inventing one is the single most tempting failure in this skill. Two named community events publish a flat per-speaker honorarium - !!Con's stable "$256 (USD)" and ffconf's "£500" - but both pay a fixed amount to every accepted CFP speaker alike, which is a different shape from a negotiated invited-speaker fee; treat them as calibration for what a small honorarium looks like, never as a rate to counter-offer with. Answer from your own budget and your own authority (Q9), and route any actual payment through whoever handles the event's money and contracts. Direct payment to speakers can bring complex issues around taxes, visas, and conflict of interest or employment agreements, so involve them rather than routing payment yourself.
- **When money is not available, trade conditions instead** - the list fixed at Q8, never improvised. None of these is a convention of event practice: they are ordinary concessions with a real cost to you and real value to them, which is the only test a concession has to pass.
  - travel dates that let them add a personal day
  - a shorter or longer slot
  - remote delivery
  - a co-speaker seat
  - a companion ticket
  - recording and publication terms
  - the time of day their session runs
  - an introduction to someone in the audience they want to meet
- **Never promise what you cannot deliver** - the pitch-killer that damages an event longest, because the candidate finds out after they have already said yes.
- **Escalate rather than stall.** If the ask exceeds your authority, say who decides and by when. A candidate waiting on an unexplained silence is cooling, and the cadence menu has no rung for "waiting on us."

## Closing the loop

- **On a yes**, confirm in writing the same day, then hand the confirmed speaker to `samber/dev-event-organizer-skills@event-speaker-experience`:
  - slot, date, time, length, format
  - what the event pays and - explicitly - what it does not
  - the travel and lodging terms
  - the recording terms
  - the review lane the packet stated (`samber/dev-event-organizer-skills@event-talk-selection` needs that answer, not a guess)
- **On a yes-with-conditions**, agree only from the Q8 list, then confirm exactly as above with the condition written into it.
- **On a no**, record the reason. That reason is worth more than the slot: it feeds `samber/dev-event-organizer-skills@event-speaker-sourcing`'s channel record and next edition's shortlist. Ask whether they would suggest someone else - a referral is the cheapest strong signal in the sourcing menu, and a declining candidate is unusually well placed to give one, but never re-approach the same person for the same slot.
- **On silence past the cadence cap**, treat it as a no, move to the next candidate, and release the slot. A slot held open out of hope is the most expensive thing in this workflow.

## Failure modes

- **CCing two candidates for the same slot.** Both see they were second choice, or worse, both see each other. One candidate per thread, always.
- **Running parallel threads for one slot without deciding what happens on two yeses.** Sequential asks cost time; parallel asks cost a retraction. Pick at Q3, and if you go parallel, know in advance which second yes you can honestly place elsewhere.
- **Treating a directory listing or a public profile as consent to be pitched.** It is consent to be found. Use the route they published, say how you found them, and keep the ask tied to a real slot.
- **Hiding the budget until late.** A candidate who blocks travel time and then learns nothing is covered will decline, tell people, and not answer next year. The budget line goes in the first message even when the answer is "nothing" or "unconfirmed".
- **Bumping without new information.** Deleted from the cadence menu for a reason; it converts a pending answer into a remembered annoyance.
- **Inviting without the sourcing "why".** An invitation that cannot answer "why me, why this event, why now" is a form letter to someone you specifically chose. Send it back to sourcing rather than writing around the gap.
- **Links, attachments or images in the first email.** Auto-trashed unread by corporate filters. Everything visual waits for touch two.
- **Inventing a speaker fee, a market rate or an "industry standard".** Saying "I don't have a benchmark, here is our budget" is the honest and stronger move.
- **Inviting inside the travel window without saying so.** The four-to-six-week travel floor is the earliest a travelling candidate could plausibly commit; an invitation arriving under it is functionally a request to decline unless you name the constraint yourself.
- **Promising a slot, a format or a fee you do not control.** See Q9 - check your authority before the sentence, not after.

## Measurement

Acceptance rate, reply rate and time-to-answer are all self-set here: quote your own numbers rather than importing a sales figure, and expect them to mean something only across editions.

- **Invitation-to-acceptance rate** (self-set) - accepted over sent, per slot type. Edition two turns this into the only speaker-outreach benchmark you will ever have that is actually about your event.
- **Time-to-answer by channel** (self-set) - days from first touch to any answer, split by channel. This is what re-ranks the first-touch menu for you.
- **Decline-reason capture** - the one metric with a real threshold: every decline carries a recorded reason, or the next edition's sourcing repeats the mistake that produced it.
- **Slot-holding time** (self-set) - days a slot spends behind an unanswered candidate. A number nobody tracks, and the one that quietly decides whether a program fills.

Pick two, write down what each would change next edition, and record both before the event.

## Invocation examples

- "Write the invitation to the keynote candidate at the top of our shortlist - we can cover travel but no fee."
- "Our first invitation went out nine days ago with no answer. What do we send now, if anything?"
- "A speaker we invited came back asking for €2,000. We have no budget line for fees - how do I answer?"
- "We have three candidates for one slot and six weeks until the program is announced. How do I approach them?"

Expected output: a drafted invitation carrying the packet's "why", the honest budget line and the answer deadline, plus a per-candidate plan covering:

- the channel and cadence, with the angle each follow-up will carry
- the negotiable list fixed in advance
- the written confirmation or the recorded decline that closes the loop

## References

- [references/invitation-message-craft.md](references/invitation-message-craft.md) - the five-part message structure, the length cap and banned vocabulary, subject-line rules, the full disclosure checklist, and a worked positive and negative invitation.
- [references/cadence-and-fee-conversation.md](references/cadence-and-fee-conversation.md) - the three cadences touch by touch with an angle table, the close-out message, the fee-and-conditions conversation scripts against the honest-budget line, the concession list with its costs, and the yes/no confirmation shapes.

See also, same collection:

- `samber/dev-event-organizer-skills@event-speaker-sourcing` - produces the packet this skill consumes; hand every decline reason back to it.
- `samber/dev-event-organizer-skills@event-speaker-experience` - takes over the moment a candidate says yes: briefing, travel, rehearsal, on-site care.
- `samber/dev-event-organizer-skills@event-talk-selection` - owns the invited-proposal review lane the confirmation message has to state.
- `samber/dev-event-organizer-skills@event-cfp-design` - the open call this channel supplements or replaces; carries the same honest-budget posture on honoraria.
- `samber/dev-event-organizer-skills@event-sponsor-outreach` - the same cadence and objection shape aimed at sponsors, where a rate card exists and the honest-budget line does not.
- `samber/dev-event-organizer-skills@event-positioning` - owns what the lineup says about the event, which is what an invitation to a headline candidate is really selling.
