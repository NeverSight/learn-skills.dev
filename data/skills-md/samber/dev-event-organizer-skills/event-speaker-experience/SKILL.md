---
name: event-speaker-experience
description: Run the speaker-side experience from the moment a speaker confirms through to the thank-you after their talk - collecting bio, headshot, A/V needs and travel details against a deadline ladder, a single named point of contact, the pre-event briefing and slide deadline, tech check and green room, documented recording consent and its per-format opt-out asymmetry, and post-event follow-up. Use whenever the user mentions what to send an accepted speaker, a green room, speaker travel or hotel, a tech check, recording consent, a speakers' dinner, or supporting a first-time speaker - even if they never say "speaker experience". Do NOT use before acceptance - inviting is samber/dev-event-organizer-skills@event-speaker-cold-outreach.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Speaker Experience

You take care of a speaker who has already said yes. Your input is the acceptance email `samber/dev-event-organizer-skills@event-talk-selection` has just sent, and specifically its closing line: "What you get: {the perks exactly as the call stated them}. What we need next: {confirmation, bio, headshot, slide deadline, travel or A/V details}." You start there.

Your output is a speaker who arrives knowing what happens when, delivers without an equipment surprise, agreed in writing to whatever was recorded, and hears from you after the event.

What this skill does not do:

- **Promise terms**: you do not decide what a speaker is promised. `samber/dev-event-organizer-skills@event-cfp-design` set the perks and left the honorarium open. You deliver whatever was promised and never invent a figure nobody confirmed.
- **Decline or waitlist messages**: not your ground - that belongs to `samber/dev-event-organizer-skills@event-talk-selection`, and those speakers never enter your scope.
- **Sourcing, inviting or selecting**: you do none of it.
- **Population-agnostic fundamentals**: you add only the speaker-specific layer on top of `samber/dev-event-organizer-skills@event-hospitality`, and you hand timing needs upstream rather than writing a schedule yourself.

Every ranking below is a default, not a law - it shifts with context and with who executes it. After the interview, re-rank all three menus against what you know - each of the following overturns a default rung:

- A venue with a house A/V technician.
- A returning speaker who already knows the drill.
- An organizer who books travel for a living.
- A recording pipeline that already exists.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 4-6 exist because the menus below diverge sharply on time-to-effect, durability and effort - those defaults cannot be picked for the user.

1. Where are you in the sequence: acceptance emails just went out, the event is weeks away, or it is next week? This fixes what is still changeable and what is now a communication problem.
2. How many speakers, across how many session formats, and how many are travelling - domestically or internationally?
3. What exactly was promised, and where: in the call, in the acceptance email, in any individual invitation? List each term. You deliver those. You never re-open them here.
4. For each material you need, what is the last date it can still be used - programme print, badge print, slide upload, venue equipment order? Work the deadlines back from those dates rather than from the event date.
5. One-off edition, or a recurring event where this year's speakers are next year's referrals and returning names?
6. What is the effort ceiling: who is the speaker contact, how many hours a week do they have, and is there a budget line for speaker expenses at all?
7. What is your recording and publication intent per session format, and where exactly were speakers told about it?
8. Who is speaking for the first time, or for the first time at this scale? Ask rather than assume - a senior engineer's first conference talk is still a first talk.
9. What does the venue actually give you: a green room or not, a house A/V technician or a volunteer with an adapter, a confidence monitor or not?
10. Is any speaker presenting material their employer restricts, or otherwise sensitive?

## Community-run vs vendor/user conference

What changes the work is who owns the event, the same replacement the rest of this collection argues:

- **Community-run** - the budget is thin and the labour is volunteer, so care is bought with attention rather than money: a named contact who answers, a packet that answers the question before it is asked, a dinner if the budget stretches. A free ticket is the floor, and anything above it was a promise somebody made deliberately.
- **Vendor/user conference** - travel, lodging and a production crew are usually real, which moves the risk from "can we afford this" to "did anyone tell the speaker". Bigger machinery hides the speaker's own experience more easily: the packet and the named contact matter more here, not less.

Say which pole a recommendation assumes whenever they differ, and treat every vendor-pole adjustment as judged rather than established practice.

## Workflow

1. **Read the acceptance packet** - the accepted proposal, the perks exactly as the call stated them, and the "what we need next" list. If anything promised there cannot be delivered, escalate it now to whoever promised it. A term quietly downgraded between acceptance and arrival is the failure a speaker tells other speakers about.
2. **Name the point of contact before the first message** - one person or a pair handling all speaker communications from confirmation through the event. One name, one address, one stated response window. Split the pre-event and on-site roles only if team size forces it, and introduce the second person by name in advance if you do.
3. **Turn "what we need next" into a dated collection ladder**, each item pinned to the last date it is usable (Q4), not to the event date. The full item list, the per-item deadline logic and the reminder shapes are in [references/material-collection-and-deadlines.md](references/material-collection-and-deadlines.md).
4. **Send the speaker packet** - one document, one link, everything a speaker needs before they need it:
   - Their slot, the room, the format and length.
   - The deadlines from step 3.
   - The recording policy for their format.
   - Travel and reimbursement mechanics.
   - On-site arrival instructions.
   - The contact from step 2.
   - Whether the deck is collected right after the talk for redistribution to attendees, if that is this event's practice - tell the speaker before they build it, not while they are still on stage.
5. **Collect A/V requirements early enough to act on them.** The date that matters is the last date the venue can still add something, not the day before - an adapter, a second microphone, a wired network drop, an audio feed for a demo. Ask what the talk does, not just what the laptop is: a live demo, an audio clip, a hardware prop and an internet dependency each fails differently.
6. **Brief the speaker on what to expect**, at the depth the care menu sets. Where an established orientation course exists for your event's community, recommending it is close to free and carries more weight than your own briefing paragraph. Structure a written brief as an outcome, not a topic reminder: the state you want the room in when the talk ends, plus the specific bad habit this slot should counter (a rushed opening act, over-claiming what a tool replaces, whatever this programme's own recurring failure is) - naming the failure mode is what a slot-and-subject reminder never does.
7. **Hold the slide deadline as a real checkpoint**, not a suggestion. State what happens if it slips, and be honest if the answer is nothing.
8. **Run the pre-event cadence** from the menu below, per speaker rather than as one broadcast.
9. **On site: host, tech check, green room** - the host from step 2 meets the speaker, walks them to their room, runs the tech check on the actual stage equipment, and knows where they are before their slot. The operating detail is in [references/onsite-speaker-care.md](references/onsite-speaker-care.md). The minute-by-minute conduct of the day belongs to `samber/dev-event-organizer-skills@event-run-of-show`, and speaker timing needs are an input you hand to it.
10. **Close the loop after the event**: thank-you, feedback delivered while it still matters, the recording link when it exists, and a retention pass that deletes the travel documents you no longer need. See [references/recording-consent-and-followup.md](references/recording-consent-and-followup.md).

Show the speaker-facing packet and any deadline change to the user before it goes out. A deadline moved by mistake is a deadline you cannot re-tighten.

If your harness has persistent memory, record per edition:

- Which materials arrived late, and after which reminder.
- Which A/V requests the venue could not meet.
- The consent answer per speaker and format.
- Who said yes to returning.

That record is what makes next edition's ladder yours rather than this skill's defaults.

## Speaker-care depth

What you add on top of what was promised. Anything the call or the invitation already committed to is delivered, never ranked - this menu starts above that line. Ranking (default, not a law - Q2, Q5 and Q6 re-rank it):

- effort (hours, standing availability, coordination, money spent): `travel and lodging concierge > speakers' dinner and gifts > named point of contact > written speaker packet > linked orientation course`
- value (a speaker who arrives prepared and on time, and who comes back or refers a peer): `named point of contact > travel and lodging concierge == speakers' dinner and gifts > written speaker packet > linked orientation course`
- compliance cost (review triggered, reversibility spent): `travel and lodging concierge > speakers' dinner and gifts == named point of contact > written speaker packet == linked orientation course`
- efficiency: `named point of contact > written speaker packet > linked orientation course > speakers' dinner and gifts > travel and lodging concierge`

- **Value tie**: genuine - each buys the same single outcome (the speaker's sense that the event carries what it asked them to take on) by a different route, and which one dominates depends entirely on whether that speaker is travelling.
- **First compliance tie**: genuine too - both rungs retain a little personal data past the event that nobody has decided to delete, a mobile number in one case and a dietary or allergy answer in the other, and the second sits under health-data rules in several jurisdictions.
- **Last tie**: the honest zero - a document and a link to somebody else's course collect nothing.

- **Named point of contact** - the default and the floor: a person or a pair handling all speaker communications. Highest value per hour in the menu because it removes the failure every other rung is also trying to remove - a speaker with a question and nobody to ask. Move up one rung as soon as you pass roughly five speakers or any deadline that must land on a single day: past that, the contact spends their hours re-answering the same question by hand.
- **Written speaker packet** - one document carrying slot, deadlines, logistics, recording policy and the contact. Costs an afternoon once and is reused every edition, which is why it sits second on efficiency despite sitting fourth on value.
- **Linked orientation course** - recommend an existing course for accepted speakers rather than writing one. Near-zero effort, real value where the community has one, and nothing to maintain.
- **Speakers' dinner and small appreciation gifts** - a real budgeted expense line, not a nice-to-have somebody improvised. Promote it whenever Q5 says the edition recurs: it is the rung that turns a speaker into next year's referral, and its return lands entirely after this edition is over.
- **Travel and lodging concierge** - the starved option: book and pay for flights and hotel on the speaker's behalf rather than reimbursing. It ties for the top of value and tops both effort and compliance cost outright, so efficiency never picks it. Promote it for any international speaker, for any speaker who cannot front the cost of a flight - reimbursement quietly filters your lineup by who has a spare month of salary - and wherever a visa letter is needed. Handle the documents it requires under a stated retention limit. See step 10.
- **Deleted, not demoted: improvised per-speaker care with nothing written down.** Warm messages in a private channel, deadlines that live in one organizer's head, terms agreed verbally. It looks like the friendliest rung on the menu and it is the one that drops a commitment, because nothing outside one person's memory says what was promised. Parked at the bottom it comes back as "we know our speakers personally." It is out.

## Recording-consent posture

How a speaker agrees to being recorded and published, and when. Ranking (default, not a law - Q1 and Q7 re-rank it):

- effort (forms built, chasing, coordination with whoever runs the cameras): `granular per-format consent > day-of signed release > consent collected at acceptance > consent bundled into submission > no recording`
- value (a publishable recording nobody has to take down, and a speaker who knew what they agreed to): `granular per-format consent > consent bundled into submission == consent collected at acceptance > day-of signed release > no recording`
- compliance cost (review triggered, reversibility spent): `day-of signed release > consent bundled into submission == consent collected at acceptance > granular per-format consent > no recording`
- efficiency: `consent bundled into submission > consent collected at acceptance > granular per-format consent > no recording > day-of signed release`

- **Value tie**: genuine - both produce a written record before anyone books a camera, which is the only property that decides whether the video can be published. They differ only in which form carried it.
- **Compliance tie**: the same fact from the other side - identical licence, identical personal data in a recorded likeness and voice, differing only in the date on the record.

- **Consent bundled into the submission form** - the default: by submitting, the speaker grants the licence, and there is no separate day-of form. Cheapest strong rung because the form already exists. Its ceiling is that an invited speaker never filled it in. Move up one rung the moment any speaker was invited rather than submitted, or a session format was added after the call closed.
- **Consent collected at acceptance** - state the licence and the opt-out in the acceptance packet and record the answer per speaker. Same exposure as bundling, one extra step, and it is the only rung that covers invited speakers.
- **Granular per-format consent** - the starved option: the speaker chooses recording, live streaming and publication separately, and the room's crew holds a per-session list. It tops effort and value together, so efficiency never picks it. Yet PyCon US's recording policy is already per-format, offering an opt-out for Talks and Charlas and stating plainly that "you cannot opt-out of recording for lightning talks" - so this is a real posture and not a refinement somebody invented. **Promotion conditions, keyed to Q10**: speakers present employer-restricted or sensitive material, your formats genuinely differ, or an opt-out has to be honoured at the door rather than in a spreadsheet.
- **Day-of signed release** - collect signatures on the morning. Efficiency ranks it below not recording at all, because it costs real coordination on the busiest day and still risks exactly the failure it exists to prevent: a speaker who declines at 09:00 leaves you a booked camera, a gap in the record, and a decision to make in a corridor.
- **No recording** - a legitimate posture, not a failure. It costs nothing, removes the exposure entirely, and loses the archive. Choose it deliberately rather than by drifting into it.
- **Deleted, not demoted: recording on the assumption that silence is consent.** Publish first and handle complaints later. It is not a cheap rung: a published video cannot be unpublished from the copies people already have, and the speaker discovers your policy at the same moment their employer does.

## Pre-event communication cadence

How often a confirmed speaker hears from you before the event. No compliance-cost axis here: none of these rungs collects or transfers anything the packet did not already. Ranking (default, not a law - Q2 and Q6 re-rank it):

- effort (messages written, threads tracked, calls scheduled): `per-speaker check-in call > milestone cadence > packet plus two checkpoints > single packet at acceptance`
- value (materials arriving on time, and surprises found while they can still be fixed): `per-speaker check-in call > milestone cadence > packet plus two checkpoints > single packet at acceptance`
- efficiency: `packet plus two checkpoints > milestone cadence > single packet at acceptance > per-speaker check-in call`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks all six pairs: the cadence that surfaces more surprises costs strictly more messages, threads and calls.

With no compliance axis printed, nothing else can block or rescue a pair. The check catches no misordering. The efficiency line rests on the arguments below.

- **Packet plus two checkpoints** - the default: the packet at acceptance, a reminder at the materials deadline, a logistics note 48 hours out. Two messages buy most of what six do. Move up to the milestone cadence for the individual speakers Q2 and Q8 flag - international travel, a first talk, non-standard A/V - rather than for the whole roster.
- **Milestone cadence** - a message at each real checkpoint: confirmation, materials due, slide deadline, one week out, 48 hours out, the morning of. More work, and it catches the moved flight and the changed title.
- **Single packet at acceptance** - send everything once and answer questions if they come. Efficiency puts it below the milestone cadence anyway, because the hours it saves are dwarfed by one A/V surprise discovered on stage.
- **Per-speaker check-in call** - the starved option: a scheduled call with each speaker two to three weeks out. It tops value and effort together, so efficiency never picks it - it is also the only rung that reliably surfaces the thing a speaker will not put in writing, an anxiety about the room or a demo they have quietly stopped trusting. Promote it for keynotes, for first-time speakers, and for any session the programme cannot afford to have go wrong.
- **Deleted, not demoted: the one broadcast thread with every speaker CC'd.** It leaks each speaker's address to all the others, and a personal deadline addressed to twenty people reads as somebody else's problem. Use a per-speaker thread or a proper mailing tool.

## First-time speakers after acceptance

Speaker mentorship programmes work on proposal drafts and close before acceptance decisions are made - they belong to the call for papers, not to you. A first-time speaker's highest-anxiety moment starts the day they are accepted, and the weeks after that are rarely anybody's job. Everything below is a default worth trying rather than established conference practice:

- **Ask rather than infer** (Q8). "Is this your first talk at this size?" in the packet, with a stated reason: it changes what you offer, not how you judge the talk.
- **Offer a rehearsal slot at a real time**, with a real person listening - not "let us know if you want to practise." An open offer is declined by exactly the people who need it.
- **Offer the room.** Access to the actual stage, the actual clicker and the actual confidence monitor before the doors open removes more fear than any advice does.
- **Say what the room will be like**: audience size, whether questions happen, who introduces them, what the timing signals look like, and what happens if a demo fails.
- **Own the organizer's half of rehearsal only** - booking the room, providing a listener, coordinating the timing. What goes in the talk is the speaker's own work. Point them at `samber/developer-relations-skills@tech-talk-outline` for the content and rehearsal side rather than coaching it here.

## Failure modes

- **Promising at invitation what this stage cannot deliver.** Travel "probably covered", a fee nobody approved, a slot length that later shrinks. The speaker finds out after they have already blocked the time, and they tell other speakers. Escalate at step 1, never at the venue.
- **No single point of contact.** Three organizers answer a speaker in three threads, or nobody does. One person or a pair handles all speaker communications - the cheapest strong rung in this skill.
- **Collecting A/V needs too late to act on them.** A requirement learned the day before is not collected, it is discovered. Pin the ask to the venue's own ordering deadline.
- **Recording without a documented consent.** A camera in the room is not agreement, and neither is silence. Every published recording needs a record naming the format, the licence and the opt-out answer - including the formats where you offer no opt-out, which then has to be stated plainly in advance.
- **Leaving first-time speakers unsupported after acceptance.** Mentorship closes at the proposal stage, so assuming somebody else's programme covers this window is how it stays uncovered.
- **Treating accessibility and dietary answers as trivia.** They were asked for a reason and they have a delivery deadline like any other material.
- **Keeping passports, tickets and payment details after the event.** Travel handling collects the most sensitive data in this skill. Delete on a stated schedule rather than when someone remembers.
- **Discovering a speaker's arrival time on the day.** It belongs in the cadence, not in a corridor conversation.

## Measurement

Everything below is self-set except the two completeness gates, and only becomes meaningful across editions.

- **Material completeness at the deadline** (gate) - every accepted speaker has bio, headshot, final title, A/V requirements and travel details recorded by the date each becomes unusable, or the ladder in step 3 is wrong.
- **Consent-record completeness** (gate) - every published recording has a record naming the session format, the licence and the opt-out answer. No exceptions, since the exception is the one that surfaces publicly.
- **A/V surprises discovered on stage** (self-set) - count them. The target is zero, and the useful number is which category recurs.
- **Time from event to recording published, and to the speaker being told** (self-set) - set your own, publish it in the packet, and be measured against your own promise rather than an invented industry norm.
- **Returning and referring speakers** (self-set) - only meaningful if Q5 says the edition recurs, and the single best read on whether any of this worked.

Pick two, write down what each would change next edition, and record both before the event.

## Invocation examples

- "Acceptance emails went out yesterday for eleven speakers. What do I send them, and what do I need back by when?"
- "Three of our speakers are flying in. Do we book their travel or reimburse it?"
- "We want to publish the talks on YouTube. What do we need from speakers, and when do we ask?"
- "One of our speakers has never given a conference talk before. What do we offer without being patronising?"
- "What actually goes in a green room, and who staffs it?"

Expected output:

- A dated material-collection ladder with an owner per item.
- The speaker packet's contents.
- A per-speaker cadence.
- A recording-consent posture with its record fields.
- An on-site host plan.
- The post-event follow-up sequence.

Carry anything promised earlier through unchanged, and label every judged or self-set element as such.

## References

- `samber/dev-event-organizer-skills@event-talk-selection` - sends the acceptance email this skill starts from.
- `samber/dev-event-organizer-skills@event-cfp-design` - set the speaker benefits and perks this skill delivers.
- `samber/dev-event-organizer-skills@event-hospitality` - the population-agnostic fundamentals this skill layers on.
- `samber/dev-event-organizer-skills@event-run-of-show` - owns the day-of minute-by-minute document. Hand it your speakers' timing needs.
- `samber/dev-event-organizer-skills@event-schedule-design` - owns the grid. Hand it arrival windows and back-to-back conflicts.
- `samber/developer-relations-skills@tech-talk-outline` - the speaker's own side of preparing and rehearsing a talk, where this skill deliberately stops.
