---
name: event-speaker-sourcing
description: Find and qualify speakers for a technical event outside the open call for papers - the proactive channel running alongside or instead of a CFP. Covers program gaps worth filling by invitation, sourcing channels (referral asks, expert and speaker directories, prior-talk review, community scouting), international sourcing by region and language, evidence-based Hot/Warm/Cold/Skip qualification, and a ranked shortlist carrying the "why" behind each name. Use whenever the user mentions finding speakers, a keynote or invited-speaker shortlist, sourcing international or under-represented speakers, or a programme a CFP did not fill - even if they never say "sourcing". Do NOT use to write the invitation - use samber/dev-event-organizer-skills@event-speaker-cold-outreach instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Speaker Sourcing

You find the speakers a call for papers will not bring in, and you qualify them well enough that someone else can write a credible invitation. Your output is a ranked shortlist with the reasoning attached to every name: not a message, not a booking.

You do not act outside this skill's boundary:

- You do not write or send anything to a candidate: personalization, value framing, follow-up cadence and fee negotiation belong to `samber/dev-event-organizer-skills@event-speaker-cold-outreach`.
- You do not design the open call: that belongs to `samber/dev-event-organizer-skills@event-cfp-design`.
- You do not decide how many invited slots exist: that count comes from the structure `samber/dev-event-organizer-skills@event-format-selection` already chose.

Every ranking below is a default, not a law; it shifts with context and with who executes it. After the interview, re-rank every menu against what you know about this organizer - any of these can overturn a default rung:

- A decade-old community network.
- A program chair who already watches conference talks for fun.
- A budget line for travel.
- A hard announcement date.

## Why you were called: two different triggers

State which one applies before sourcing anything; they differ in urgency and in how many names you need.

1. **Supplement to a live CFP.** The open call is on schedule but early volume is thin. This is ordinary, expected practice, not a crisis; the DevOpsDays organizing guide names direct contact as the planned backup: _"Don't be surprised if proposals don't flow in quickly at first… It's good to have a backup plan and contact individual speakers as well."_ You are filling a gap of unknown size, so source against the gaps you can already name and re-check after the call closes.
2. **Replacement of a deleted CFP.** The event is closer than roughly ten weeks, or the call would close inside six weeks of the event; so `samber/dev-event-organizer-skills@event-cfp-design` deletes the open call rather than compressing it and the whole program goes invited. You are sourcing the entire lineup on the shortest possible timeline, which changes the channel ranking: vouched, fast-answering channels beat thorough ones.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 4-6 exist because the menus below diverge sharply on time-to-effect, durability of the payoff, and effort; those defaults cannot be picked for the user.

1. Which trigger above are you in, and how many invited slots need filling, of what kind (keynote, session, workshop, panel seat)?
2. Who owns the event: community conference or vendor/user conference? (This changes what an invitation can honestly offer and who counts as a credible speaker.)
3. What is the event's topic scope, and which specific themes is the program missing today?
4. What is the date the shortlist must be ready, and the date speakers must be confirmed by? (A hard date promotes the fast channels and deletes the slow ones outright.)
5. Is this a one-off edition or a compounding annual asset? (A compounding mandate promotes the slow rungs: community scouting and a speaker pool that outlives this edition.)
6. What is the effort ceiling: organizer hours available for sourcing, who will actually watch recorded talks, and how much of your personal network you are willing to spend on referral asks?
7. Is the program required to reach beyond your own circle - new voices, under-represented speakers, speakers outside your country? If yes, which of those, and is anyone accountable for it?
8. What can the budget honestly cover for an invited speaker: nothing beyond a ticket, travel, lodging, a fee? Say "unconfirmed" if it is unconfirmed; see the honorarium note below.
9. Which assets already exist that should re-rank the menus: past speakers who would refer peers, an archive of last edition's talks, an active community you already moderate, a program chair with a public reputation, prior contact with any candidate?

## Community-run vs vendor/user conference

The split that changes sourcing is who owns the event, the same replacement the rest of this collection argues:

- **Community-run**: an invitation trades on the audience and the peer group, because that is all it has. Credibility comes from the community's own people, and the hard line the collection holds elsewhere applies here too: a sponsor never buys a speaker slot. A sourced name that arrives through a sponsor relationship gets qualified on the same evidence as any other, or it does not enter the shortlist.
- **Vendor/user conference**: content is mostly invited by design, so this skill is the main intake rather than the backup channel. Candidates are weighted toward customers, partners and practitioners who use the vendor's technology, and the invitation can usually carry real budget. The qualification evidence does not change; the candidate pool and the offer do.

Say which pole a recommendation assumes when they differ.

## Workflow

1. Run the interview; fix the trigger (Q1) and the ownership pole (Q2).
2. Name the program gaps before naming any person. Write each gap as a slot brief carrying the theme, the format, the audience level, and what would make this slot a success - plus, where the gap is broad enough to need it, the editorial angle, what the audience should walk away knowing, and two or three open questions worth posing on stage. Sourcing without a brief produces a list of impressive people who do not fit the program.
3. Pick channels from the menu below against the deadline (Q4) and the effort ceiling (Q6). Use at least two; no single channel reaches a whole program (see failure modes).
4. Build a long list, deliberately larger than the number of slots, because qualification culls hard. How much larger has no defensible general answer; see the conversion figure below. Size it from your own past invitations if you have any, and record the ratio you used so the next edition starts from a real number.
5. Qualify each candidate against the slot brief at the depth the menu below sets, recording a source link and a date for every claim. An unqualified name is not a shortlist entry, it is a guess someone else will act on.
6. Score each candidate Hot / Warm / Cold / Skip against fit, evidence strength, and availability, and drop everything that scores Skip.
7. Rank the survivors per slot, not globally: a slot has one brief and the ranking answers "who fills this one first".
8. Write the "why" for every shortlisted name; the specific evidence, not an adjective. This is the input `samber/dev-event-organizer-skills@event-speaker-cold-outreach` personalizes with; a generic reason produces a generic invitation.
9. Check the international and lead-time gates below for any candidate travelling, before the name goes on the list.
10. Decide the review lane for invited proposals and write it into the handoff, then hand the packet to cold outreach.

Present the shortlist slot by slot for validation before any invitation goes out. An invitation is hard to walk back; a name sent by mistake has already been asked.

If your harness has persistent memory, record:

- which channels produced confirmed speakers
- the candidates who declined and why
- the long-list-to-confirmation ratio you actually observed (the one number nobody else can give you, see measurement)
- for a compounding mandate (Q5), keep one running roster of people sourced or invited across editions rather than starting a fresh list each time - a categorical role field (speaker, invited-only, keynote) plus a free-text detail field, so a returning candidate's prior evidence and outcome carry forward instead of being re-qualified from zero

## Sourcing channels

Ranking (default, not a law; Q4, Q6, Q7 and Q9 re-rank it):

- effort (hours per candidate found, coordination, and social capital spent): `community scouting > prior-talk review > referral asks == directory search`
- value (a shortlist you can defend: delivery evidence, reach beyond your own circle, voices no call would surface): `prior-talk review > community scouting > directory search > referral asks`
- compliance cost (review triggered, reversibility spent): `community scouting > directory search > referral asks == prior-talk review`
- efficiency: `referral asks > directory search > prior-talk review > community scouting`

- **Effort tie** (referral asks == directory search): a referral ask and a directory query both cost one action and return names within a day. The difference is who does the retrieval, a person or an index, not what you spend.
- **Compliance tie** (community scouting > directory search > referral asks == prior-talk review): a referral and a recorded talk both work from material a third party volunteered or the candidate published themselves. Neither has you collecting anything the person did not put in public.
- **Why efficiency still leads with referral asks despite trailing on value**: at equal retrieval effort a referral arrives vouched. It skips a qualification rung the directory name still has to pay for, and it triggers no review of retained contact data.

- **Referral asks** (the default): ask past speakers, fellow organizers and community leaders for two or three names each, with the slot brief attached so the answers are usable. Cheapest strong signal available, because a referrer usually attests to delivery quality and reliability in the same sentence. Its ceiling is exactly its weakness: it returns your network's network, which is why it sits last on value and why it can never be the only channel used (see failure modes).
- **Directory search** (the standing infrastructure rung, and the answer to international sourcing): named live directories, their filters and their population limits are in [references/sourcing-channel-evidence.md](references/sourcing-channel-evidence.md). Near-zero effort per query, and it reaches outside your circle, which is why it beats referrals on value despite returning unvouched names that still need qualifying. It carries the higher compliance cost of the two cheap rungs, because you are retaining contact details and because a directory listing is not consent to be pitched (see failure modes).
- **Prior-talk review**: watch recorded talks from other events, or read published slides and transcripts. Top of value, because it produces delivery evidence directly rather than someone's report of it, exactly what the qualification step needs; efficiency ranks it third because it costs real hours per candidate. Promote it one rung ahead of directory search whenever a single slot concentrates the risk (a keynote, an opening talk, a slot the edition is named after), or whenever a promising candidate arrives with no vouch attached.
- **Community scouting** (the starved option): read who answers hard questions in project forums, issue trackers, mailing lists and community chats, and who explains things well there. It tops value alongside prior-talk review, because it is the only channel that reaches people who have never spoken anywhere and are therefore in no directory and on no referral list, and it tops effort too, so efficiency never picks it. It also carries the highest compliance cost: many communities' codes of conduct treat recruiting and solicitation in their spaces as off-limits, so check the space's rules before harvesting names from it, and approach people through their published contact route rather than the community channel itself.
  - Promotion conditions: a stated new-voices or under-represented-speakers goal with someone accountable for it (Q7), a compounding annual mandate (Q5) where the pool you build outlives this edition, or a topic so specific that no directory covers it.

Paid speaker-bureau booking is deleted from this menu, not demoted, whenever the budget cannot confirm a fee (Q8); a bureau's entire mechanism is a negotiated fee, and with no confirmed money it is not a cheap option, it is an unexecutable one. Parked at the bottom of a list it silently returns as scope halfway through sourcing.

## Sourcing internationally

The mechanism is filtering, not searching harder: the directories that publish region and language filters together are the only reliable way to build a genuinely international shortlist rather than an accidental one (mechanics and named examples in the evidence reference). Region alone gives you people you cannot brief in a shared language. Language alone gives you the same country again.

Two gates before an international name enters the shortlist:

- **Travel lead time.** Speakers need roughly four to six weeks to arrange travel or time off. That floor is the minimum, not the target, and it applies broadly to travel; treat it as the earliest a confirmed international speaker could plausibly commit.
- **Visa and entry.** Some routes need months and a formal invitation letter, and processing times swing by passport and destination and change without notice, so check the actual requirement rather than assuming one. If the answer arrives after your confirmation date (Q4), the candidate is a Skip for this edition and a Hot lead for the next one.

Budget honesty binds both: if travel is unconfirmed (Q8), an international candidate is being asked to fund their own trip. Say that in the handoff so the invitation says it too, rather than discovering it during negotiation.

## Qualification depth

Ranking (default, not a law; Q1, Q6, Q8 and Q9 re-rank it):

- effort (per candidate, including coordination and favors owed): `organizer reference > delivery evidence > fit screen`
- value (what the shortlist can be defended with): `organizer reference > delivery evidence > fit screen`
- compliance cost (review triggered, reversibility spent): `organizer reference > delivery evidence == fit screen`
- efficiency: `fit screen > delivery evidence > organizer reference`

**Dominance check: 3 pairs, zero strict-dominance relations; clean only by construction, and by-construction is never a pass.** Value and effort run in one order, so all three pairs fail the same way: the deeper qualification defends the shortlist better and costs strictly more per candidate. Compliance restates that order with the two cheap rungs tied, so it rescues nothing either. The check verifies nothing; the ordering rests on the arguments below.

The compliance tie is genuine: a fit screen and a delivery review both read material the candidate published for exactly this purpose. A reference call does not - it is a discussion about a named person with a third party, so treat it carefully:

- keep it factual
- keep it to what the organizer observed
- never write down an opinion you would not repeat to the candidate

- **Fit screen**: the default first pass over the long list. Does their published work match the slot brief, at the right depth, recently enough? Minutes per candidate, and it is what makes the expensive rungs affordable by shrinking the pool they run on. Where a slot could go to either a practitioner who lived the topic or a vendor pitching a product for it, screen the practitioner first: a vendor-affiliated candidate fills the slot only when no practitioner is available, or completes the discussion as a second voice rather than the only one.
- **Vendor candidates worth tracking rather than sourcing now**: split any vendor-affiliated names the screen turns up into a workshop-or-niche shortlist worth a slot on its own, and a monitor-for-later list that is not this edition's problem. A vendor pitch is not disqualified, it is simply never the default fill.
- **Delivery evidence**: the default for anyone who reaches the shortlist. Ten minutes of a recorded talk, or a talk transcript, or a written piece long enough to show they can structure an argument. Promote every shortlisted candidate to this rung; a name goes to outreach with evidence or it does not go.
- **Organizer reference** (the starved option): ask an organizer who has already hosted them whether the speaker showed up, hit the brief, and handled the room and the audience. It tops both value and effort, so efficiency never picks it, and it is the only rung that predicts reliability rather than talent. The two failure modes of an invited program are a great talk that never gets written and a speaker who cancels late.
  - Promotion conditions: a keynote or headline slot, a candidate who will be paid or flown at real cost, a name you cannot verify any other way, or a second edition where last year's late cancellation is still fresh.

Follower counts and audience-size metrics are deleted from this rubric rather than ranked in it. They measure reach, not the talk, and left anywhere on the page they quietly become the tiebreak between two otherwise equal candidates (see failure modes). If draw genuinely matters for a slot, `samber/dev-event-organizer-skills@event-positioning` owns headliner positioning and can say what draw the program actually needs.

## Scoring and the shortlist

Score every qualified candidate on one scale, then rank within each slot. The four-band scale below borrows the shape sales teams use to score leads; it is a serviceable structure for sorting by evidence strength, and nothing about it is a speaker-sourcing benchmark:

- **Hot**: strong fit against the slot brief, direct delivery evidence, plausibly available on your dates.
- **Warm**: good fit, softer evidence (a written piece but no recorded talk, a referral without a reference), or availability unknown.
- **Cold**: loose fit, or the evidence is thin enough that the invitation would be guessing.
- **Skip**: a disqualifier hit: unavailable on the dates, a conflict with a sponsor or the program's independence, a lead time the calendar cannot absorb, or a code-of-conduct concern.

Every claim in a candidate record carries a source link and the date you checked it, plus a High/Medium/Low confidence label when the claim is inferred rather than stated. Sourcing runs on public channels only:

- no bulk scraping
- no gated-data workarounds
- never infer or target on protected characteristics; source instead from a directory whose members opted into being found for that reason

These guardrails are the same ones that govern sales prospecting, where the legal exposure is identical.

The candidate record template, a worked positive and negative example, and the handoff packet shape are in [references/shortlist-and-qualification-template.md](references/shortlist-and-qualification-template.md).

## Handoff

The packet that leaves this skill contains, per slot:

- the ranked candidates
- the slot brief they were ranked against
- the "why" and its evidence per candidate
- the Hot/Warm/Cold/Skip score
- availability and travel constraints
- what the budget can honestly offer (Q8)
- the intended contact route

It also carries one decision the next skills need: **an invited speaker's proposal cannot go through blind review with the open pool**, because their identity is the entire reason they were invited. `samber/dev-event-organizer-skills@event-talk-selection` asks its organizer to decide the invited lane in advance, so answer it here rather than leaving it to be improvised: state whether the invited talk is confirmed at invitation time and enters the program directly, or whether it is reviewed on its own named track against the same criteria. Write that lane into the packet.

## The two numbers not to invent

Both are unknown, and both invite a plausible-sounding substitute. Tell the user the number is unknown instead.

- **Speaker fees and honoraria.** Community technical events have no standard honorarium rate; organizer guidance warns only that direct payment to speakers "can bring with it complex issues around taxes, visas, and conflict of interest/employment agreements", and goes no further. Two named CFP-driven events do publish a flat per-speaker figure - !!Con's stable "$256 (USD)" and ffconf's "£500" - but they disagree by more than 2x in different currencies and both pay every accepted speaker the same amount regardless of format, which is a different shape from a negotiated invited-speaker fee. Use them as calibration, not a rate card: do not invent a market rate, a per-minute figure, or an "industry standard" for an invited speaker's fee. If the user wants a fee policy, gate every figure on their own budget and their own legal and tax review - `samber/dev-event-organizer-skills@event-cfp-design` treats it the same way, on purpose.
- **Invitation-to-confirmation conversion.** The rate at which invited speakers accept is unknown, so "how many people should I approach for five slots" has no defensible general answer. The lead-generation habit of sourcing two to three times the target count is a sales number, built where the ask, the relationship and the cost of a no all differ. Treat it as a shape for thinking, never as a speaker benchmark, and label it that way if you repeat it - use your own past invitations if you have them, and record this edition's real ratio for the next one.

## Failure modes

- **Sourcing only from your own network.** Referral asks are the efficient default and the whole list comes back looking like last year's, one degree out. The menu's answer is structural: at least two channels, one of which reaches outside your circle.
- **Inviting on fame instead of talk evidence.** A large following predicts attention, not a good session, and it is the easiest signal to mistake for qualification because it is the most visible one. Every shortlisted name carries delivery evidence.
- **Promising money before there is a policy.** A sourcing conversation drifts into "we can probably cover something" and the event has now made an unbudgeted commitment with tax and visa consequences it has not thought about. What the budget covers is fixed at Q8 and written into the handoff, not improvised.
- **Treating a directory listing as consent to be pitched.** Being listed is consent to be found, and each directory states its own contact norms. Use the contact route the person published, follow the directory's rules, and keep the ask specific to a real slot.
- **Sourcing names with no slot brief.** An impressive list nobody can place produces invitations that cannot answer "why me, why this event, why now"; the exact question the invitation has to answer.
- **Sourcing past the confirmation date.** Adding candidates after the point where travel can still be arranged builds a shortlist of people who must decline. The lead-time gate applies at entry, not at outreach.
- **A shortlist with no reasoning attached.** Names handed over without their "why" force outreach to re-do the qualification or write a generic invitation. The evidence is the deliverable, as much as the names are.

## Measurement

- **Source effectiveness**: which channel produced each confirmed speaker, counted per edition. This is the one metric worth carrying, because it is what makes the next edition's channel ranking yours rather than this skill's default.
- **Long-list-to-confirmation ratio** (self-set): candidates sourced per speaker confirmed. Only your own ratio means anything here, so record it across editions rather than comparing against a general figure.
- **Shortlist evidence completeness** (self-set): the share of shortlisted names carrying delivery evidence and a dated source. This one has a real threshold: every name, or the shortlist is not finished.
- **Reach beyond the network** (self-set, only if Q7 set a goal) - the share of confirmed speakers who came from a channel other than referrals. A goal without this count is a stated intention with no feedback.

Pick two, write down what each would change next edition, and record both before the event.

## Invocation examples

- "Our CFP closes in two weeks and we have four talks for a ten-slot program - help me find people to invite."
- "The conference is in nine weeks, we skipped the CFP entirely, build me the whole lineup."
- "We need a keynote on platform engineering who isn't the same three people every European conference books."
- "Find me speakers outside Europe for our Kubernetes day - we can cover travel but not a fee."

Expected output: a slot-by-slot shortlist where each candidate carries:

- the evidence behind their ranking
- a Hot/Warm/Cold/Skip score
- availability and travel constraints
- the honest budget offer
- a contact route
- the invited-review lane

Present it slot by slot for validation, then hand it to cold outreach.

## References

- `samber/dev-event-organizer-skills@event-speaker-experience` - takes over once a sourced speaker confirms, covering travel, briefing, rehearsal, and on-site care.
- `samber/dev-event-organizer-skills@event-accessibility-inclusion` - decides access provisions a sourced speaker may need once they confirm; this skill owns reach into an under-represented pool, never the accommodation that follows.
