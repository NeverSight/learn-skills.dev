---
name: event-attendee-email-sequences
description: Design and write the attendee email arc for a technical event - the sequence, the cadence, and the actual copy. Covers the dated arc from announcement to post-event follow-up, a sourced reminder cadence with per-segment caps rather than a SaaS drip, the know-before-you-go email, role and registration-state segmentation, consent and list hygiene, and a humanizer pass before anything sends. Use whenever asked to write an event announcement email, registration confirmation, week-before or day-before reminder, know-before-you-go, day-of or post-event follow-up, or to decide how many emails to send and when. Do NOT use for overbooking, waitlists or seat release - use samber/dev-event-organizer-skills@event-no-show-management.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Attendee Email Sequences

You design and write the emails a technical event sends its attendees. Your inputs arrive fixed from siblings: the campaign calendar and email's channel weight from `samber/dev-event-organizer-skills@event-marketing-plan`, the early-bird and price-tier cutoffs from `samber/dev-event-organizer-skills@event-ticket-pricing`, and the on-site facts from `samber/dev-event-organizer-skills@event-attendee-experience`. Your output is a dated send map plus the copy for every email on it.

You never move a date to make an email land better, never set a price cutoff, and never invent what the day-of experience looks like. Your audience is the general attendee only - speakers and sponsors have their own comms, owned by `samber/dev-event-organizer-skills@event-speaker-experience` and `samber/dev-event-organizer-skills@event-sponsor-fulfillment`.

**The sharpest boundary is no-shows.** A reminder sequence exists to fight them.

- **You own:** the sequence's design and copy, in full.
- **`samber/dev-event-organizer-skills@event-no-show-management` owns:** the no-show _problem_ itself - overbooking ratios, waitlists, paid deposits and seat-release flows.
- **When a user asks "how do we stop no-shows":** answer with the reminder emails, and route the structural fix there in the same breath.
- **This boundary is one-sided:** that sibling ships, but it was written from this side only and has not been agreed from its side - say so rather than implying an agreed handoff.

## The sourced cadence

The reminder sequence you design should be much thinner than SaaS marketing norms - roughly 2 to 4 sends across the whole pre-event arc, segmented by list membership. Say that plainly whenever a user expects a longer sequence. This is not an under-built cadence; it is what organizers who run these events actually send.

Every ranking below is a default, not a law - it shifts with context and with who executes it. Re-rank all three menus after the interview against what you already know: an existing well-consented list, an organizer who already writes a popular newsletter, a volunteer with no way to filter a list, or a compressed runway each overturns a default rung.

## Core principles

**SaaS lifecycle drips are rejected structurally.** Welcome, onboarding, re-engagement and win-back sequences assume an ongoing subscription and branch on per-recipient behaviour (opened, clicked, went quiet). An event arc is fixed, dated, and ends on one day. Every send moment here is a calendar date, never a behavioural trigger, and the branching mechanic needs marketing-automation tooling a volunteer-run event does not have.

**Cold-email subject-line science is rejected entirely.** Its tactics (2-4 lowercase words, no first-name token, "look like a colleague, not a vendor") exist to disguise a sender so an unsolicited message beats a stranger's spam filter. That inverts here: your recipient registered and is hunting for the email that tells them where to check in.

Name the event and the date plainly.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-effect, durability and effort - those defaults cannot be picked for the user.

1. What does the marketing plan hand you: which calendar spine, what channel weight email carries, and the fixed dates (announcement, agenda release, doors)? Take all of it as given.
2. Is there a list at all, and where did each address come from - a ticket purchase, a form with an explicit opt-in box, last year's attendees, an existing community list? Answer per source, not in aggregate.
3. Ticketed or free - and is there registration at all? A no-registration event has no list to sequence.
4. Community-run or company/vendor-run? This changes the consent posture and what the list may later be used for, not the arc.
5. Which dated cutoffs must an email react to: early-bird close, price-tier change, capacity cap, CFP close? Those dates arrive fixed; you write the email that lands against them.
6. What is the last date each send can still work? Doors, minus the week-before and day-before offsets, is fixed - a compressed runway deletes the upper rungs of the sequence-depth menu outright rather than compressing them.
7. One edition, or a list you intend to still own in three years? A compounding mandate promotes the consent-heavy and win-back rungs, because a list that survives an audit is the asset, not this edition's sends.
8. Who writes and sends these, how many hours do they have, and can they filter a list per send? A team that cannot produce a filtered list has no segmentation rungs above the role split.
9. What does the on-site day actually look like - check-in location and hours, badge policy, quiet room, dietary mechanics, accessibility provisions? Take this from `samber/dev-event-organizer-skills@event-attendee-experience`; never invent it to fill a section.
10. Who else receives email about this event (speakers, sponsors, volunteers, judges), and who owns those sends? You write the attendee variant only.
11. What is the rough split of first-timers versus returning attendees, and how many attendees travel internationally? Decides whether the attribute-segments rung is worth the list work.

## Community-run vs company/vendor-run

An attendee whose employer pays often needs something forwardable to a manager - dates, cost, and what the company gets - which is a _variant of the announcement email_, not a different arc.

Every other send is identical, because the recipient is an individual developer either way and the day-of information does not care who paid. Keep the forwardable justification paragraph as a named option.

What actually changes the work is two orthogonal axes:

- **Registration posture (ticketed / free-with-registration / no registration).** Decides whether the arc exists at all.
  - A free event carries a sourced 30-50% signup-to-attendance drop-off, which makes the reminder cadence load-bearing rather than courteous.
  - A no-registration event (FOSDEM's published posture: "There is no registration. Just turn up!") has no list. The identity-consistent output is the practical information published once on the event's own page plus one announcement, not a sequence with nothing to gate entry into it.
  - State that as the right answer for that posture, never as a shortfall.
- **Community-run vs company/vendor-run.** A community event's list is an organizer-held asset with one purpose; a vendor event's list usually flows into a marketing database with a second life. The published practice behind this skill is community-side, so treat every vendor-pole adjustment as a judgment call and say which pole a recommendation assumes whenever they differ.

## The arc

Fixed and dated. Each row is one email with one job. Nothing here branches on behaviour.

| Send                      | Fires on                                                                           | Its one job                                     |
| ------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------- |
| Announcement              | the plan's announcement date                                                       | it exists, it is dated, here is where to look   |
| Registration confirmation | on registration (transactional)                                                    | prove it worked, say what arrives next and when |
| Agenda / speaker release  | the plan's agenda-release date                                                     | give the undecided a concrete reason            |
| Last call                 | `samber/dev-event-organizer-skills@event-ticket-pricing`'s cutoff, a day before it | one dated fact, no manufactured urgency         |
| Know-before-you-go        | roughly one week before doors                                                      | everything needed to arrive prepared            |
| Day-before nudge          | the evening before                                                                 | the one thing: when and where                   |
| Post-event thank-you      | 1-3 days after                                                                     | thanks, recordings, and the feedback handoff    |

A live, checkable figure counts as the dated fact the last-call row asks for - "already 70% of seats taken" is not manufactured urgency if it is true at send time, unlike a countdown with nothing behind it. The same rule runs the other direction for the day-of send: open with the social proof that already exists ("we are sold out") before repeating the logistics, rather than burying it under the practical details the reader has already seen once.

The email-by-email breakdown - trigger, required contents, what each must _not_ carry, and its segment - is in [references/arc-and-send-map.md](references/arc-and-send-map.md).

## Workflow

1. Run the interview. Fix the spine and dates (Q1), the list's consent provenance per source (Q2), the registration posture (Q3), the cutoffs you react to (Q5) and the runway (Q6).
2. Restate the handed-down inputs back to the user before writing anything - dates, email's channel weight, the message and positioning - the way `samber/dev-event-organizer-skills@event-social-media` restates them for its own channel. Re-deriving any of them is how two channels end up disagreeing on the same event's dates.
3. Map the fixed arc above onto those dates. Every send gets a date and one job, or it does not exist.
4. Pick the sequence depth, the reminder cadence and the segmentation depth from the three menus below, in that order.
5. Write each email to its single job. The craft rules - subject and preview text, the five-part body, formatting, banned moves - are in [references/email-craft-and-worked-copy.md](references/email-craft-and-worked-copy.md).
6. Build the know-before-you-go email against the sourced 14-section structure in [references/know-before-you-go-email.md](references/know-before-you-go-email.md), pulling every on-site fact from Q9 rather than inventing one.
7. Apply the role split at the week-before send. Write the attendee variant; hand the speaker, sponsor and volunteer variants to the siblings that own those audiences.
8. Check the whole plan against the sourced caps. If any segment is over, cut a send rather than justifying it.
9. Run every drafted email through a humanizer pass in your preferred humanizer skill. A model-shaped email to a room of developers reads as model-shaped, and this is the one channel where the sender's own voice is the credibility.
10. Run the consent and list-hygiene check below. A send that fails it does not go out, whatever the calendar says.
11. Show the user the full send map plus every draft before anything is scheduled. An email cannot be unsent, and a wrong date in a reminder produces a room of people arriving on the wrong day.
12. Hand the post-event survey itself to `samber/dev-event-organizer-skills@event-feedback` - you write the email that carries it, never the instrument inside it.

If your harness has persistent memory, record the dated send map, which list each send went to and where those addresses came from, the cadence caps you held to, the subject lines used, and anything that drew replies or complaints. That record is what makes next edition's arc yours rather than this skill's defaults.

## Sequence depth

How much of the arc you actually build. Ranking (default, not a law - Q6 and Q8 re-rank it):

- effort (emails written, sends coordinated, list work per send): `full arc > core arc > confirmation plus know-before-you-go > confirmation only`
- value (a full room, and the people in it arriving prepared): `full arc > core arc > confirmation plus know-before-you-go > confirmation only`
- efficiency: `core arc > confirmation plus know-before-you-go > full arc > confirmation only`
- compliance cost (review triggered, reversibility lost): the full arc alone carries any; the other three rungs mail only people who registered for this edition. The full arc's win-back mails a prior edition's list, which needs a documented per-address opt-in and sign-off before it goes out - the one send here whose mistake cannot be taken back.

This menu is **clean by construction, not by care**: value and effort run in the same order, so no rung dominates another and any efficiency ordering is admissible. Do not read that as a pass - it means the ordering below rests entirely on the argument attached to each rung, with no dominance check available to catch a mistake. The other two menus each carry a real dominance constraint, and each says where.

- **Confirmation only** - one transactional confirmation at registration, nothing else. Near-zero effort, and it leaves undone the one job only email can do: telling a registered person where and when to show up. Its efficiency ratio is two near-zero numbers divided by each other, which is why it sits last rather than first.
- **Confirmation plus know-before-you-go** - two sends. Cheap, and it buys most of the arrival value, because the week-before email is what determines whether people reach the right building at the right hour.
- **Core arc** - the default: announcement, confirmation, know-before-you-go, day-before nudge, post-event thank-you. Five sends, none branching. It adds the announcement - the send that carries the own mailing list, which the marketing plan ranks first on both value and efficiency across every acquisition channel the event owns - plus a post-event send at almost no marginal cost.
- **Full arc** - the starved option: core plus agenda release, last call against the pricing cutoff, and a prior-year win-back. It tops value and effort together, so efficiency never picks it. **Promotion conditions**: a dated early-bird cutoff worth reacting to (Q5), a prior-year attendee list that exists and is consented (Q2), and someone whose actual job includes writing these (Q8) - all three, not any one.
- **Deleted, not demoted: the behaviourally-branched drip.** Five to ten nurture sends on one list with open/click conditional logic. It is not a heavier rung of this menu; it is a different mechanic for a different relationship, and parked at the bottom it silently returns as scope the first time someone asks for "a proper sequence".
- **Conditional delete.** On a free event with no registration, delete every rung of this menu and the axis lines above it: publish the practical information on the event's own page and send one announcement to whatever list already exists. There is nothing to sequence.

## Reminder cadence

How many reminder passes, spaced how. Every rung keeps the week-before send and differs only in which further pass it adds on top: nothing, the day-before nudge, the registration follow-up, or all four sourced passes at once. The whole menu sits inside MLH's sourced caps; the top rung _is_ the ceiling, not permission to exceed it. Ranking (default, not a law - Q3 and Q8 re-rank it):

- effort (sends composed, lists filtered per send, coordination): `full sourced ceiling > two-pass registration follow-up > week-before plus day-before > single week-before`
- value (bodies in the room on the day): `full sourced ceiling > week-before plus day-before == two-pass registration follow-up > single week-before`
- efficiency: `week-before plus day-before > single week-before > two-pass registration follow-up > full sourced ceiling`
- compliance cost (review triggered, reversibility lost): `full sourced ceiling > two-pass registration follow-up`; the week-before and day-before sends go to registered attendees about the event they registered for and carry none. The ceiling's win-back reuses a prior edition's list, the one reuse § Consent names as irreversible; the follow-up mails people who have _not_ registered, which is promotional rather than transactional and needs its own recorded opt-in per address.

The `==` is genuine and worth the sentence: the day-before nudge converts an already-registered person into someone who turns up, while the registration follow-up converts an interested person into a registration that still faces the sourced 30-50% drop-off. Comparable expected bodies in the room, bought from opposite ends of the funnel. That tie plus the effort gap is what forces the day-before pair above the follow-up on efficiency - the one dominance constraint this menu carries, and it is respected.

- **Single week-before reminder** - one send, one week out, split by role. MLH's own minimum, and the send its guide treats as the essential one.
- **Week-before plus day-before** - the default: the know-before-you-go at one week, then a short evening-before nudge carrying one fact. **Promotion condition**: add the two-pass registration follow-up on top when the registration curve is behind its checkpoint on the plan's spine - a capacity problem, not a cadence preference.
- **Two-pass registration follow-up** - MLH's capped "1 or a maximum of 2" follow-ups to people who have not registered, cross-referenced against the registered list so no registrant is asked to register. Costs real list work per send, which is why efficiency puts it below the cheaper pair it ties with on value.
- **Full sourced ceiling** - the starved option: all four sourced passes at once (registration follow-up capped at two, prior-year win-back, one engagement update, the week-before role split). Tops value and effort, so efficiency never picks it. **Promotion conditions**: a free event where the drop-off is the binding constraint (Q3), a consented prior-year list (Q2), and someone who owns list filtering (Q8).
- **Deleted, not demoted: the countdown chain.** Seven days, three days, two days, tomorrow, this morning. It exceeds every sourced cap, it is the exact behaviour MLH's anti-spam instruction names, and each send trains the recipient to stop opening the one that matters.
- **Conditional delete.** When the audience is a single standing community list with no separate registration step - a recurring meetup where the list _is_ the audience - delete the two-pass registration follow-up and the full sourced ceiling from this menu and from the axis lines above. There is no "not yet registered" segment to write to.

## Segmentation depth

Who gets which version. Ranking (default, not a law - Q8 and Q10 re-rank it):

- effort (list filtering per send, copy variants written, tooling required): `attribute segments > registration-state segments > role split at the week-before send > one list one send`
- value (each recipient gets the one instruction that applies to them): `attribute segments > role split at the week-before send == registration-state segments > one list one send`
- efficiency: `role split at the week-before send > registration-state segments > one list one send > attribute segments`
- compliance cost (review triggered, reversibility lost): attribute segments alone carry any; the other three rungs slice a list you already hold and add none beyond its own consent record. Dietary and accessibility flags are health-adjacent personal data, so holding them per recipient is a retention, access and deletion decision - and a field once collected cannot be un-collected.

The `==` is genuine: both rungs remove a wrong-message-to-wrong-person error of comparable size. The role split stops an attendee's check-in time being buried under sponsor load-in instructions; registration-state stops "register now" landing on someone who already paid. One error at the door, one at the top of the funnel.

Because the role split costs less to produce, it dominates registration-state outright - and efficiency respects that, which is the one dominance constraint here.

- **One list, one send** - everyone receives the same email. Near-zero effort, and everyone does still get the know-before-you-go, which is why it is not last on efficiency.
- **Role split at the week-before send** - the default and MLH's sourced minimum: attendees, speakers, sponsors, volunteers and judges each get their own check-in instruction. You write the attendee variant only. **Promotion condition**: add registration-state segments the moment the event has both a registered list and an open registration window.
- **Registration-state segments** - registered / not yet registered / last year's attendees, filtered manually per send. MLH assumes exactly this: a filtered list, not behavioural tooling.
- **Attribute segments** - the starved option: first-timer vs returning, local vs travelling, workshop ticket vs conference only, dietary and accessibility flags. Tops value and effort, so efficiency never picks it. **Promotion conditions, keyed to Q11**: a large first-timer share where orientation is a stated goal, or international attendees whose visa-letter and travel lead times differ enough that one email cannot serve both.
- **Deleted, not demoted: behavioural segments.** Opened, clicked, did not open. It needs tooling the pole this collection sources from does not have, and it targets a per-recipient behaviour when every send moment here is a fixed date.
- **Conditional delete.** When the only tool is a plain announce list with no per-recipient filtering, delete registration-state and attribute segments from this menu and from the axis lines above. Keep the role split by maintaining separate lists per role and sending to each.

## Consent and list hygiene

The mailing list is the event's highest-value acquisition channel and the one asset whose loss cannot be undone. A list collected for one edition and mailed for the next without a documented opt-in is the single exposure in this whole skill that can force a deletion the event never recovers from.

- **A ticket purchase is not consent to be marketed to.** It is consent to receive what the transaction requires: the confirmation, the practical information, and the changes to it. Anything promotional needs its own recorded opt-in, taken at the moment the address was collected.
- **Record provenance per address, not per list** - which form, which edition, which box was ticked, and when. Q2 asks this per source for that reason. A merged list whose provenance is "we think most of them opted in" is not auditable.
- **Every non-transactional send carries a working unsubscribe**, honoured immediately rather than at the next scheduled send.
- **Announce a second, differently-branded automated email before it arrives.** The sourced devopsdays email does exactly this, warning attendees a week ahead that a separate tool would email them about the code of conduct. An unannounced email from a name the recipient does not recognise reads as phishing and gets reported, which costs the sending domain more than the email was worth.
- **The rules differ by jurisdiction and by list.** Consent, retention and unsubscribe obligations for an attendee list are a real compliance question, not a style preference - check the current rules for where your attendees are, and get sign-off before reusing a prior edition's list.

## Failure modes

- **Importing a SaaS drip cadence.** Five to ten sends with behavioural branching, dropped onto a dated arc. It roughly triples the sourced organizer norm and needs tooling the event does not have. The cadence is thin on purpose.
- **Exceeding the sourced caps because the room is not full.** A soft registration curve is a diagnosis for the marketing plan, not a licence for a fifth reminder. More sends to a list that is already ignoring you converts a soft curve into a burned list.
- **A know-before-you-go missing the code of conduct or the accessibility line.** Both are in the sourced structure, and both are exactly the information that decides whether someone attends at all. Omitting them is not a length trade-off.
- **Treating consent as implied by the ticket purchase.** See above; this is the one failure with an irreversible outcome.
- **Solving no-shows here.** Writing overbooking ratios, waitlist mechanics or deposit rules into the reminder plan. Answer with the reminder emails, then route to `samber/dev-event-organizer-skills@event-no-show-management`.
- **Moving a date so an email lands better.** The announcement, agenda release and early-bird cutoff arrive fixed. An email that wants a different date is an email written to the wrong date.
- **Inventing the on-site facts.** Check-in location, badge policy, quiet room, dietary mechanics - all of it belongs to `samber/dev-event-organizer-skills@event-attendee-experience`. A confidently wrong check-in time in a reminder is worse than no reminder.
- **Writing the speaker or sponsor variant of the week-before email.** The role split is yours; the other roles' content is not.
- **Borrowing cold-email subject-line tactics.** Lowercase two-word subjects and hidden sender identity, aimed at a recipient who is searching their inbox for your event's name.
- **Shipping raw model output.** A first draft that skipped the humanizer pass reads as one, in the one channel where the organizer's own voice is the product.
- **Announcing nothing about the second automated email.** The recipient reports it as phishing, and the report lands on your sending domain.

## Measurement

**Treat any published open-rate or click-rate figure as a rough sanity floor, never a target.** Most figures you will find are marketing-industry averages blending unrelated senders and audiences with the post-registration sends this skill covers, and importing one as a pass/fail bar is how a healthy send gets declared a failure. The closest available figure sits at 21-30% open rate and 2.1-3% click-through rate, and even that one predates a since-2021 measurement shift and blends promotional sends with the confirmation, reminder and post-event sends this skill actually writes; no reply-rate figure exists at all. Sourcing and the full caveats: [references/open-click-benchmark-evidence.md](references/open-click-benchmark-evidence.md). Refuse a hard target built on any of this, say why, and measure the two things that are actually binary here plus a few self-set signals.

Two binary gates, both checkable before sending:

- **Know-before-you-go completeness** - every section of the sourced 14-section structure is either present or explicitly noted as not applying to this event. Iterate until this passes; a partial pass is a fail.
- **Cap compliance** - no segment receives more sends than the sourced caps allow. Count per segment, not per list.

Self-set signals, meaningful only across editions:

- **Desk questions the email already answered** - count at check-in, by question. The cheapest and most honest measure of whether the know-before-you-go worked, and this skill's own construction rather than anything sourced.
- **Late arrivals of dietary and accessibility requests** - replies to the pre-event email asking for something that needed two weeks' notice mean the email asked too late, not that people were careless.
- **Unsubscribes and complaints per send** - the only real cadence guardrail available. Any rise is the caps being exceeded, whatever the calendar said.
- **Day-of arrival timing against the stated check-in window** - a crowd at the wrong hour is an email problem before it is a desk problem.

Pick two of the self-set signals, write down what each would change next edition, and record both before the event.

## Invocation examples

- "Write the week-before email for our 300-person conference - first edition, we have no idea what to put in it."
- "How many emails should we send between now and the event? Registration opened six weeks ago and we're at half capacity."
- "Draft the last-call email for the early-bird deadline on Friday."
- "We collected emails at last year's event. Can we mail that list about this one?"
- "Our free meetup gets 40% no-shows. What should the reminder emails say?"

Expected output: a dated send map with one job per email, the chosen cadence stated against the sourced caps, the segment each send goes to, humanized copy for every email including a complete know-before-you-go, a consent check per address source, and an explicit routing of anything structural to the sibling that owns it.

## References

- [references/arc-and-send-map.md](references/arc-and-send-map.md) - every send in the arc: trigger date, its one job, required contents, what it must not carry, its segment, and the no-registration collapse.
- [references/know-before-you-go-email.md](references/know-before-you-go-email.md) - the sourced 14-section structure in its real order, which sections are conditional, adaptation rules for smaller events, and the completeness checklist the measurement gate uses.
- [references/email-craft-and-worked-copy.md](references/email-craft-and-worked-copy.md) - subject and preview-text rules, the five-part body shape, mobile formatting, the humanizer checklist, and worked positive and negative copy for the last-call and day-before emails.
- [references/open-click-benchmark-evidence.md](references/open-click-benchmark-evidence.md) - the one named-organizer open/click benchmark found, why it falls short of a target figure, and what was checked and confirmed absent.
- `samber/dev-event-organizer-skills@event-marketing-plan` - the umbrella. Hands down the calendar spine, email's channel weight and every fixed date; also the source of the consent discipline this skill enforces.
- `samber/dev-event-organizer-skills@event-ticket-pricing` - owns the early-bird and price-tier cutoffs the last-call email reacts to and never sets.
- `samber/dev-event-organizer-skills@event-attendee-experience` - the source of truth for every on-site fact the pre-event and day-of emails describe.
- `samber/dev-event-organizer-skills@event-no-show-management` - owns the no-show problem's structural fixes; this skill's reminder cadence is one input into that model, not a substitute.
- `samber/dev-event-organizer-skills@event-feedback` - owns the post-event survey instrument this skill's final email carries.
- `samber/dev-event-organizer-skills@event-code-of-conduct` - owns the content the code-of-conduct section of the know-before-you-go email links to.
