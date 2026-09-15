---
name: event-volunteer-experience
description: Design what a volunteer gets when they are not standing at a post, and how one edition closes with them - off-duty time they can actually use, the volunteer-specific hospitality top-up on the event's general standard, recognition not tied to a shift, a public thank-you, and the past-volunteer list next edition's recruitment starts from. Use whenever the user mentions looking after volunteers beyond their shift, whether volunteers get to see a talk, a volunteer lounge or volunteer meal, thanking volunteers after the event, or bringing the same volunteers back next edition - even if they never say "volunteer experience". Do NOT use for recruitment, roles, shifts or briefing - use samber/dev-event-organizer-skills@event-volunteers instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Volunteer Experience

You look after the people `samber/dev-event-organizer-skills@event-volunteers` already recruited, in the two windows that skill leaves alone: the hours they are not standing at a post, and the weeks after the event ends.

Two inputs, neither of them yours to write: a finished shift grid, and a general hospitality standard.

Three outputs:

- an off-duty plan a volunteer can actually use
- a volunteer-specific hospitality top-up
- a closed edition - thanked, recorded under a retention rule, and handed to whoever recruits next time

## Where the line is

`samber/dev-event-organizer-skills@event-volunteers` draws the split from its own side. Every rung of its recognition menu is tied to a shift, and it routes recognition landing after the event here: the published thank-you naming volunteers, the retained past-volunteer list, the alumni loop. Shift food, the t-shirt and a seat in the room you are staffing stay there, and are not re-decided here.

Correct that line in exactly one direction, and say so when you do: **off-duty care in this edition is also yours.** That skill speaks to arrival buffers and shift length; it never speaks to what a volunteer does, eats, or sits on while off post.

- **Never re-open roster size, shift length or the sizing arithmetic.** Hand a requirement upstream instead. "Every volunteer needs one continuous block off post" is an input to that skill's bottom-up sizing, not an edit you make here.
- **One rung sits in both menus, and this is the split.** `samber/dev-event-organizer-skills@event-volunteers` carries "thanks by name at the end of the shift" inside its shift-recognition menu: a spoken, in-the-moment thanks its own text excludes from publication ("Publishing a volunteer's name is the option that would carry that exposure, and it is not on this menu"). The published post-event thank-you is yours - a names list, a consent ask, an opt-out. Never let one message serve as both, or the consent gate goes unasked.
- **Never re-decide the catering standard, the dietary and allergen policy, or signage.** `samber/dev-event-organizer-skills@event-hospitality` sets those for every population and you add only the volunteer layer, the same shape `samber/dev-event-organizer-skills@event-speaker-experience` uses for speakers. The hospitality skill's own boundary table hands you the off-duty top-up, with its dietary, allergen and alcohol exposure inherited rather than re-argued, and hands food at the post to `samber/dev-event-organizer-skills@event-volunteers`.
- **Never write a role definition.** Flag a standout volunteer as a candidate and stop; `samber/dev-event-organizer-skills@event-team-structure` owns the role taxonomy and everything that follows an offer.
- **Touch conduct nowhere.** `samber/dev-event-organizer-skills@event-code-of-conduct` owns the policy and the response team, and `samber/dev-event-organizer-skills@event-volunteers` already briefs the escalation script to every volunteer. Volunteer care does not stretch into volunteer safety reporting. A reader who assumes it does writes a second, conflicting script.
- **Your thank-you is outward-facing; the retrospective is not.** `samber/dev-event-organizer-skills@event-debrief` never surveys or writes to participants, so there is no collision. It reviews internally how volunteer ops performed; you write to the volunteers themselves.
- **The alumni loop is yours, and `samber/dev-event-organizer-skills@event-community-building` must mirror that when it is built.** You close out _this_ edition's volunteers - thanks, the retained list, the candidate flag. That skill runs the standing, multi-edition community work the list then sits inside.

  This arbitration rests on `samber/dev-event-organizer-skills@event-volunteers` being shipped and explicitly routing next-edition volunteer material here. The other skill mirrors it from its own side: it scopes its audience to community members who never worked a shift, and runs the alumni loop as a segment inside its surface rather than as a second space.

- **Volunteer feedback is not claimed here.** `samber/dev-event-organizer-skills@event-feedback` segments attendee, speaker and sponsor instruments and is silent on volunteers. A volunteer question set is closer to that skill's job than to this one's, so say so rather than absorbing it.

## Interview

Ask one question at a time, multiple-choice where it helps. Questions 5-7 exist because the menus below diverge on time-to-effect, durability and effort, so nobody can pick those defaults for the user.

1. Would your volunteers otherwise have attended as participants - did they give up a ticket, paid or free, to staff this?
2. Does the shift grid already leave every volunteer at least one continuous block off post, and how long is the event day?
3. What does the venue give you off the programme floor: a room you can hold all day, a corner, or nothing?
4. Does a past-volunteer list already exist from a previous edition, who owns it, and does it have a deletion date?
5. What date does closure have to land by, and what fixes it - next edition's call for volunteers, the retrospective, a venue invoice, or nothing?
6. One-off edition, or a recurring event where this edition's volunteers are next edition's roster?
7. What is the effort ceiling _after_ the event: who is still working the week after, and is there any budget line for volunteers beyond the shift itself?
8. Are any volunteers minors, or on site under someone else's employment or insurance arrangement? (This routes to a review, never to an answer from this skill.)
9. Is there already a standing community space between editions, and who owns it? (This decides how much of the alumni loop is yours at all.)
10. Do returning volunteers take on genuinely different work than first-timers?

## Workflow

1. **Read what the sibling already decided**: the shift grid, the shift-linked perks, and the rule that nobody leaves a post without confirmation of a replacement. None of it is re-opened here.
2. **Take the general hospitality standard as given.** Write down only the delta you are adding for volunteers, so the top-up stays auditable against the standard rather than blurred into it.
3. **Design off-duty time** with the first menu. Express the result as a requirement handed to `samber/dev-event-organizer-skills@event-volunteers`, never as a change you make to the grid.
4. **Set the off-duty hospitality tier** with the second menu, against the space Q3 says you actually have and the standard from step 2.
5. **Close the edition** with the third menu: thank publicly with consent, record the list under a stated owner and deletion date, and flag candidates to the standing team.
6. **Hand the list on.** Next edition's recruitment starts from it. Name who receives it and when, so it is a handoff rather than a file nobody inherits.

Show the user any volunteer-facing message and any published entitlement before it goes out. An off-duty promise the roster cannot fund is worse than no promise, because the volunteer plans their day around it.

If your harness has persistent memory, record per edition:

- which volunteers had a usable block off post and which did not
- what the off-duty top-up actually cost
- who was thanked and who consented to being named
- who said yes to returning
- where the list lives with its deletion date

That record is what makes next edition's loop yours instead of this skill's defaults.

## Ranked menus

Every ordering below is a default, not a law - it shifts with context and with who executes it. Before presenting a menu, re-rank it against the interview and say which answer moved which option.

**The three efficiency orderings, every default rung, every promotion condition and every delete are this skill's own construction, not measured rankings.** Where a named event runs one of these practices, it is cited. No published figure compares the rungs against each other on volunteer return. Treat each ordering as a starting argument to overturn with what you know about your own event, and say so when you present it.

An asset the defaults assume away beats the recommended rung outright: an existing past-volunteer list (Q4) collapses most of the third menu into one email, and a standing community space someone else already owns (Q9) means the alumni half is not even yours to build.

Where the interview rules an option out, delete it from the plan rather than parking it at the bottom. A ruled-out option left on the list reappears as scope.

### Off-duty time

What a volunteer gets to do with the hours they are not on a post. Not the seat in the session they are staffing - that is shift-linked and lives next door.

Efficiency: **off-duty pointer > named personal-attendance blocks > published off-duty entitlement > nothing designed**.

- value (a volunteer who experienced the event, and says yes next edition): named blocks > off-duty pointer > published entitlement > nothing designed
- effort (coordination, and headcount landing on the sibling's arithmetic): named blocks > published entitlement > off-duty pointer > nothing designed

No compliance-cost axis applies: none of these rungs collects data, publishes anything about a person, or triggers a review.

Value and effort run in different orders here, and one inference is what separates them. That inference is this skill's own, not a measured finding:

- The sibling skill plans shifts at 2-3 hours, inside an event day several times longer than one shift.
- Most volunteers therefore already hold off-duty time, without anyone designing it.
- What they lack is knowing what is worth walking into during it.
- A pointer supplies exactly that. An entitlement supplies time they already had.

Q2 is the question that breaks the inference. Where the grid leaves no free block, the entitlement stops being redundant and the order flips.

- **Off-duty pointer** - the default. Give off-duty volunteers a short live note on what is running now and where there is room, reusing the schedule and run of show that already exist. Near-zero effort, and it converts time a volunteer already had.
- **Published off-duty entitlement** - state a minimum block off post inside the published shift plan. Its cost is not writing it. Its cost is the headcount that lands on the sibling's sizing arithmetic. Promote it above the pointer when Q2 says the grid does not already leave every volunteer a continuous block, because a pointer aimed at a volunteer with no free time points at nothing.
- **Named personal-attendance blocks** - the starved option: each volunteer names the sessions they will not miss, and the grid is built around those before shifts are assigned. The 1995 World Wide Web Conference wrote this shape into its own volunteer scheduling policy directly: coordinators built free time around each volunteer's chosen sessions, or assigned that volunteer to work those same sessions instead. PyCon US runs a narrower version tied to one role, where a Tutorial Host who signs up to staff the tutorial they most want to attend secures a seat in it that way. The rung tops value and effort together, so efficiency never picks it. Promote it when Q1 says volunteers gave up a ticket they would otherwise have used and Q6 says the edition recurs. Those are the people for whom "I staffed it and saw none of it" decides next year.
- **Nothing designed** - whatever the grid leaves over. Name it as a choice rather than drifting into it. At a short event with light shifts it is a defensible one.

**Deleted, not demoted: informal permission to slip away from a post when it is quiet.** Delete it from this menu and from the axis lines above. It is the cheapest-looking rung on the page, and it directly contradicts the sibling's published coverage rule that nobody leaves a post without confirmation of a replacement. The failure it produces is not a missed session. It is an unstaffed desk nobody knew was unstaffed.

### Off-duty hospitality tier

The volunteer-specific top-up on the general standard, for time off post. The shift-linked half - food at the desk, vouchers for long shifts, meals for buildup and teardown crews - is already the sibling's and is not repeated here. The general meal line and the quiet room a volunteer uses off-shift are decided by `samber/dev-event-organizer-skills@event-accessibility-inclusion` and `samber/dev-event-organizer-skills@event-attendee-experience`, not here.

Efficiency: **off-duty catering access > volunteer rest space > volunteer social meal > attendee parity only**.

- value (a volunteer who is still functioning late in a long day, and who says yes next edition): rest space > social meal > off-duty catering access > attendee parity only
- effort (rooms, budget lines, headcounts, an evening): social meal > rest space > off-duty catering access > attendee parity only

No compliance-cost axis is derived here. The dietary, allergen and alcohol exposure these rungs carry is the general standard's, already decided in `samber/dev-event-organizer-skills@event-hospitality` and inherited rather than re-argued - deriving it twice is how two skills end up with two policies.

Efficiency diverges from value at the top of this menu: the rest space leads on value, the social meal leads on effort, and the cheapest rung leads on neither yet wins the ratio.

- **Off-duty catering access** - the default, and an off-duty rung before it is a catering one. It covers the volunteer who is away from their post and therefore at the back of the general queue. Hold an allocation for volunteers whose off-post block falls outside the catering window, and give them a queue rule so a short break is not spent standing in line. FOSDEM's published perk is the shift-linked half: volunteers on long shifts can skip queues, and staff bring food to the post or arrange a break. Extending that to time away from the post is this skill's own construction.
- **Volunteer rest space** - a room or corner off the programme floor with seating, water, self-serve snacks, and stated permission to be there while off post. Tops the value axis because it is the only rung that lets someone stop being on. This skill's own construction as a volunteer practice. Promote it above the default when Q2 says the day runs long or across multiple days, or when Q3 says a room is genuinely available.
- **Volunteer social meal** - the starved option: a meal or drinks for volunteers after the last shift. It tops effort and sits second on value, so efficiency never picks it. Promote it when Q6 says the edition recurs, because its whole return lands after this edition is over. DevOpsDays budgets a speakers' dinner with small appreciation gifts as a named expense line. Reading that across to volunteers is this skill's own construction, and it does not carry cleanly: a speaker is an invited guest where a volunteer is labour the event runs on, and that line is budgeted against a speaker roster where the volunteer roster at the same event is usually larger.
- **Attendee parity only** - volunteers eat what attendees eat, on their own time. Legitimate at a short, single-shift event. State it as a decision.

**Deleted, not demoted: repurposing the event's quiet or accessible space as the volunteer break room.** Delete it from this menu and from the axis lines above. It looks free and it is not. That room exists so a person who cannot be around interaction has somewhere to go, and `samber/dev-event-organizer-skills@event-accessibility-inclusion` provisions it for that population. Filling it with off-duty volunteers destroys the exact property it was provisioned for. Borrow a different room, or none.

### Closure and the alumni loop

What happens after the last shift. Recognition and continuity are one menu, not two.

Both are decided in the same week, by the same person, out of the same near-zero budget. Both are measured by the same outcome - a volunteer who comes back - and the status-marker rung cannot exist without the retained list.

Efficiency: **retained past-volunteer list > public thank-you > nomination path > standing alumni channel > returning-volunteer marker**.

- value (volunteers who return, and organizers who emerge): retained list > nomination path > standing channel > public thank-you > returning-volunteer marker
- effort (hours, standing commitment, political capital): standing channel > nomination path > returning-volunteer marker > retained list > public thank-you
- compliance cost (review triggered, reversibility spent): standing channel > retained list > returning-volunteer marker > public thank-you > nomination path

Compliance cost earns its axis here. Every rung except the last holds or publishes personal data about people who are not attendees, and the retained list is the one that persists past the edition it was collected for. That retention duty is inherited from the sibling's sign-up flow, not invented here: apply it to a list that outlives its edition rather than re-deriving the rule.

- **Retained past-volunteer list** - the default, and the load-bearing rung. `samber/dev-event-organizer-skills@event-volunteers` ranks a past-volunteer call-back second on efficiency among recruitment channels and names it in its own default, so without this list that channel structurally does not exist next edition. That is a sibling's published default, not external evidence: it says the list matters, and nobody has measured the payoff. Give it a named owner and a deletion date on the day you create it.
- **Public thank-you** - names and a post, with consent asked before anyone is named. Second on efficiency because it costs an afternoon, and it is the only rung visible to people who did not volunteer, which makes it recruitment surface as well as closure. It reaches everyone who showed up, including the ones you will never see again.
- **Nomination path** - a named route from a standout volunteer to a candidate conversation with the standing team. High value and no data exposure at all. Its cost is coordination and political capital. Raise the flag and hand over: `samber/dev-event-organizer-skills@event-team-structure` owns everything after that. Design the route to fit your own standing team rather than looking for a template to copy. `references/alumni-list-and-handoff.md` borrows DEF CON's own vouching criteria as a starting checklist for what the flag should capture.
- **Standing alumni channel** - a space that keeps the list warm between editions. Tops both effort and compliance cost, so efficiency never picks it, and Q9 may say it is not yours to build at all. Promote it only for a multi-year recurring event with someone already funded to moderate.
- **Returning-volunteer marker** - a status carried across editions. It cannot exist without the retained list, so it never saves the work of the rung above it, and it spends its recognition on people who have already returned: the one group whose return is no longer in question. That is why it sits last on efficiency. **Promotion condition, keyed to Q10**: returning volunteers take on genuinely different work.

**Deleted, not demoted: a formal reward with real cash value** - a raffle prize, a travel grant, a comped ticket to a different event as payment for the shift. Delete it from this menu and from the axis lines above. Once a reward reads as wages, the arrangement is no longer volunteering, and that question is not reversible after the first reward is handed out. This mirrors the sibling's own cash-stipend deletion. TechCrunch runs exactly this shape at its own events: a stated minimum-hours commitment earns a named-dollar-value pass to a different, later event in the same company's portfolio. That is what the deleted rung looks like in practice, and the reason it stays deleted rather than becoming a menu option with guardrails.

A comped ticket offered as an invitation, not as payment, is a different thing. If you offer one, say in writing which it is. No convention ties a comped ticket to the _same_ event's next edition: the named programs that exist run cross-event, inside one organizer's own portfolio, rather than volunteer-this-year-attend-free-next-year at one recurring conference.

## Failure modes

- **Re-opening the shift grid from here.** Every off-duty entitlement is headcount, and headcount is the sibling's arithmetic. Fix: state the requirement, hand it upstream, and let the roster resize.
- **Publishing an off-duty promise the roster cannot fund.** The volunteer plans their day around it and then works through it. Fix: confirm the grid can carry the entitlement before it is published, never after.
- **Reading the pointer as permission to leave a post.** Fix: the pointer addresses volunteers who are already off post. Repeat the replacement-confirmation rule alongside it every time.
- **Spending another population's allocation.** The quiet room, the speaker catering, the sponsor lounge. Fix: budget the volunteer top-up as its own line, however small, or do not offer it.
- **Naming people publicly without asking.** A thank-you post is a publication. Fix: collect consent at sign-up or ask before posting, and offer an opt-out that needs no explanation.
- **Keeping the alumni list forever with no owner.** It stops being a retained list and becomes an inherited liability nobody remembers collecting. Fix: owner and deletion date on day one, renewed deliberately rather than by silence.
- **Answering the minors or insurance question.** Fix: name the review, route to counsel and the insurer, and stop.

## Measurement

No benchmark exists for any of this: no published figure says what share of a volunteer roster should return. Every threshold below is this skill's own, self-set rather than measured, and each becomes meaningful only across editions, against your own previous number.

- **Share of volunteers with at least one continuous block off post** (gate), read off the published grid rather than reported afterwards. If it is not 100%, the entitlement was not funded.
- **Share of volunteers who attended at least one session they chose** (self-set). Meaningful only once the pointer or named blocks are in use. Ask it in a single question at closure.
- **Share of this edition's volunteers who return next edition** (self-set). Record it, and compare it only to your own previous edition.
- **List integrity** (gate): the past-volunteer list exists, has a named owner, and has a deletion date.
- **Consent completeness** (gate): every person named publicly agreed to be named. No exceptions, since the exception is the one that surfaces publicly.

The two self-set shares need a second edition before they say anything. The three gates do not, which is why they carry the pass threshold: check each against the grid and the list you already built, and iterate until all three hold.

## Invocation examples

- "Our volunteers worked all day and saw none of the conference. What do we do next year?" → the off-duty menu, re-ranked by Q1 and Q2. The answer is a requirement handed upstream, not a grid edit.
- "Should we run a volunteer lounge?" → the hospitality menu. The answer depends on Q3 and the length of the day, and it is not the quiet room.
- "How do we thank volunteers after the event?" → the closure menu's default two rungs, plus the consent gate before any name is published.
- "We want the same people back next year." → the retained list first, with an owner and a deletion date, then the handoff to next edition's recruitment.
- "Can we give volunteers a free ticket to next year as a thank-you?" → no convention ties a comped ticket to the same event's next edition. The named programs that exist run cross-event and read as wages, not thanks. Decide which one you are offering, and say so in writing.

Expected output:

- an off-duty requirement handed upstream
- a volunteer-specific hospitality delta written against the general standard
- a closure plan with consent handled
- a retained list with a named owner, a deletion date, and a named recipient for next edition's recruitment

## References

- [references/alumni-list-and-handoff.md](references/alumni-list-and-handoff.md) - retained list structure, owner and deletion date, handoff to recruitment, and candidate flag
- [references/closure-messages.md](references/closure-messages.md) - closure message templates with consent ask and examples

See also, same collection:

- `samber/dev-event-organizer-skills@event-volunteers` - recruits, defines roles, plans shifts, briefs, and owns shift-linked perks. Its shift grid is this skill's input; its past-volunteer call-back channel is what this skill's retained list feeds.
- `samber/dev-event-organizer-skills@event-hospitality` - sets the population-agnostic standard this skill tops up rather than restates.
- `samber/dev-event-organizer-skills@event-team-structure` - receives flagged candidates and owns the role from there.
- `samber/dev-event-organizer-skills@event-accessibility-inclusion` - owns the quiet and accessible space this skill refuses to borrow.
- `samber/dev-event-organizer-skills@event-debrief` - reviews volunteer operations internally; this skill writes to volunteers themselves.
- `samber/dev-event-organizer-skills@event-community-building` - runs standing between-editions community the retained list sits inside, and mirrors this boundary from its own side.
