---
name: event-volunteers
description: Recruit and organize the volunteer workforce that staffs one edition of a technical event - roster sizing built bottom-up from the posts the schedule needs standing, role definitions with real fit criteria, shift plans with arrival buffers, sign-up and confirmation, the briefing including the code-of-conduct escalation script, a named replacement protocol holding coverage, and recognition for the people who showed up. Use whenever the user mentions how many volunteers an event needs, recruiting or signing up volunteers, volunteer roles or a shift schedule, briefing volunteers, or a volunteer who does not turn up - even if they never say "volunteers". Do NOT use for volunteer care and retention - use samber/dev-event-organizer-skills@event-volunteer-experience instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Volunteers

You staff one edition of an event with people who are not paid to be there. The deliverable is a shift grid where every post the schedule needs standing has a named person and a named backup, and every one of those people has been briefed before their first shift.

The workforce you design is downstream of two documents you do not own:

- **The run of show** - says what has to happen at every hour.
- **The code of conduct** - says who a report can reach.

Read both before counting anybody.

Never size a roster from a volunteer-to-attendee ratio, even when one circulates. Size bottom-up from posts and hours instead (workflow step 3), because the only documented ratio comes from an event that described its own load as past responsible limits.

## Scope ceiling: where this skill stops applying

At the largest professionally-run scale, the workforce this skill designs is replaced by money. Badge and registration desks, security, and AV go to contracted staffing vendors, and no day-of volunteer program exists to run. If the event has an events team on payroll and a staffing budget, this skill is the wrong tool: procure the labour instead, with `samber/dev-event-organizer-skills@event-vendor-sourcing`.

The same ceiling appears one layer up, for the standing organizing team, in `samber/dev-event-organizer-skills@event-team-structure`'s paid-hire gate. Both describe the same transition at roughly the same scale.

## Interview

Ask one question at a time, multiple-choice where it helps. Questions 6-8 exist because the menus below diverge sharply on time-to-effect, durability and effort - their default orderings cannot be picked for the user.

1. What is the event: format, attendee headcount, how many days, how many rooms running at once, and is there a registration or badge desk?
2. Does a run of show or an hour-by-hour schedule exist yet, and does it name the posts someone must be standing at? (If not, step 1 of the workflow builds a provisional post list - it is the only input that produces a defensible headcount.)
3. Who owns volunteers on the standing team: a named lead, or whoever has time? (The standing role itself is defined in `samber/dev-event-organizer-skills@event-team-structure`; this skill is what that person then runs.)
4. Does the event have a code of conduct with a named response team, and are volunteers currently in the reporting path?
5. Which posts will handle attendee personal data, cash or payments, or badge and registration records?
6. What date does the roster have to be closed by, and what fixes it - t-shirt ordering, a badge print run, a briefing session, or just the event date? (A hard date promotes the fast channels.)
7. One-off edition, or a recurring event where this edition's volunteers are next edition's roster? (A compounding mandate promotes the durable rungs: a written catalog, a retained past-volunteer list.)
8. What is the effort ceiling: coordinator hours before the event, whether anyone will coordinate live on the day, budget for t-shirts and food, and whether anything gets maintained between editions?
9. What already exists that the default ordering assumes away?
   - Last edition's volunteer list.
   - A local user group or student chapter that would send a block of people.
   - A registration system that could carry a sign-up flow.
   - A written role catalog.
   - A parent body with its own volunteer pool.

## Scale ladder

Scale, and the formality it forces, changes every mechanic below. A registration desk needs the same people standing at it whether the event is community-run or company-run - a 200-person company-run event needs its own desk staff in exactly the shape a community-run one does. Events sit at three distinct rungs.

- **Informal, network-sourced** (meetup up to a few hundred). Volunteers are a late, ad hoc line item: DevOpsDays' guide surfaces them one month out, after ticket sales and sponsorship, recruited from personal networks in exchange for access. At the bottom of this rung the organizing team _is_ the entire volunteer pool, which is a legitimate answer for a first edition - see `samber/dev-event-organizer-skills@event-first-edition`.
- **Built program** (roughly a thousand attendees upward, multi-room, multi-day). A published role catalog, a sign-up system, fixed shift lengths, a dedicated coordination channel, and lead times measured in weeks:
  - FOSDEM opens sign-up around six to seven weeks out.
  - PyCon US runs its shift claiming behind the conference profile system.
- **Professionally staffed** (see the scope ceiling above). No volunteer workforce.

State which rung a recommendation assumes whenever they differ. The middle rung is where nearly every reader sits, and where both failure directions are live:

- Applying DevOpsDays' one-month, network-only recruitment at conference scale leaves posts empty.
- Building FOSDEM's volunteer site for a 150-person event spends a month of coordinator time on a spreadsheet's worth of work.

## Workflow

1. **List the posts, not the people.** Walk the run of show hour by hour and write down every position someone must be physically standing at: registration, info desk, each room that needs a lead, cloakroom, floaters, setup and teardown, AV support. If no run of show exists yet, build a provisional list from the schedule and flag it for reconciliation when `samber/dev-event-organizer-skills@event-run-of-show` produces the real one. Name the entrance during any public-facing closing session as its own post: without one, a latecomer problem lands on whichever organizer is nearest the door instead of on the roster. Include the event's own emotional high points - an opening keynote, a closing ceremony - in the post list rather than assuming an organizer will informally cover them; a written plan's measurable payoff is that the organizer who would otherwise be running the room gets to watch it instead.
2. **Add the posts the code of conduct requires.** Its response team needs identifiable people reachable during the event. Take that roster requirement as given from `samber/dev-event-organizer-skills@event-code-of-conduct`; this skill recruits and schedules into it, and does not redesign it.
3. **Size the roster bottom-up.** For each post: people needed simultaneously × hours it must be covered ÷ shift length = shift-slots. Sum the slots, divide by the number of shifts one volunteer will actually take (ask this on the sign-up form; do not assume), and add a floater reserve. Published anchors and the worked arithmetic are in [references/sizing-and-shift-planning.md](references/sizing-and-shift-planning.md). Never derive a headcount from attendee count.
4. **Write the role catalog** to the depth the second menu picks, using [references/role-catalog-and-fit-criteria.md](references/role-catalog-and-fit-criteria.md). Give every role a fit criterion, not just a name - FOSDEM's heralding role asks for confidence addressing a room of up to 800 people, and its info desk asks for the ability to handle cash.
5. **Open recruitment** through the channels the first menu picks, with the lead time your rung demands. Publish the role catalog _before_ sign-up opens: people choose a role, not a slot.
6. **Confirm every sign-up individually, by name, against a named coordinator.** A sign-up nobody answered is a name on a list and an empty desk on the day.
7. **Build the shift grid with arrival buffers inside the published times.** Volunteers arrive before their post starts, not when it starts; the buffer is part of the shift, not goodwill. Graduate it for first-timers - PyCon US asks Session Chairs for 15 minutes, or 30 if they are new to the role.
8. **Brief every volunteer before their first shift.** The briefing has non-negotiable content regardless of how informal everything else is: their post's own choreography, who they escalate to and on which channel, and the volunteer-facing code-of-conduct escalation script. Both the built-out source and the thinnest one agree on the last item - DevOpsDays' otherwise one-line treatment still instructs organizers to "Train Staff and Volunteers" so they understand how to handle violations. See [references/briefing-and-coverage-protocols.md](references/briefing-and-coverage-protocols.md).
9. **Publish the coverage protocol**, covering:
   - How to report that you cannot make a shift.
   - How long to wait for a relief who has not arrived.
   - Who to call.
   - One named referent per shift, who owns live direction for that shift's posts - a volunteer taking conflicting instructions from whoever happens to be nearby is a coordination failure this single point of contact exists to remove.
   - The rule that holds the whole grid together: do not leave your post until you have confirmation of a replacement.
10. **Recognize the shift, then hand over the loop.** Apply the third menu for the perks tied to shifts and roles. Everything about bringing the same people back next edition - the alumni list, the retention loop, recognition not tied to a specific shift - belongs to `samber/dev-event-organizer-skills@event-volunteer-experience`.

If your harness has persistent memory, store the post list with its per-post headcounts, the shift length that worked, which posts ran short and at what hour, the no-show rate and how many were replaced, and the names of everyone who finished a shift. The next edition then starts from a real post list and a real roster instead of a blank page.

## Ranked menus

Every ordering below is a default, not a law. It shifts with context and with who executes it. Before presenting any of the three menus, re-rank it against the interview and say which answer moved which option:

- A hard roster deadline (Q6) promotes the channels that fill a roster in days.
- A recurring mandate (Q7) promotes what gets written once and reused.
- An asset the defaults assume away (Q9) can beat the recommended rung outright: last edition's volunteer list turns the top channel into one email, and a local user group willing to send eight people can cover a whole area by itself.

Where the interview rules an option out, delete it from the plan rather than parking it at the bottom. A ruled-out option left on the list reappears as scope at T-2 weeks.

**Briefing depth carries no menu, deliberately.** Ranking it would be false precision: the three components in step 8 cost roughly the same to deliver, and published volunteer briefings, from the most built-out to the thinnest, deliver all three. There is no efficient subset to recommend.

### Recruitment channels

Efficiency: **direct network ask > past-volunteer call-back > registration-gated sign-up form > block partnership with a local group > dedicated volunteer site**.

- value (posts reliably covered): dedicated site > registration-gated form > block partnership == past-volunteer call-back > direct network ask
- effort: dedicated site > block partnership > registration-gated form > past-volunteer call-back > direct network ask
- compliance cost: dedicated site > registration-gated form > past-volunteer call-back > block partnership == direct network ask

**Dominance check: 5 rungs, 10 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Three mechanisms block the ten, and none of them alone would account for the menu:

- Eight pairs fail the ordinary way: the rung ahead on coverage is worse on at least one cost axis.
- One pair fails on compliance alone, and is the one worth stating: the registration-gated form beats a block partnership on value _and_ on effort, and is blocked only because standing up a collection point costs more review than one conversation with a group does.
- The last pair, block partnership against past-volunteer call-back, is tied on value with each rung cheaper on a different cost axis, so neither can be at least equal on both.

None of the three reasons is evidence; the efficiency line rests on the arguments below.

The network ask leads on efficiency because it costs an afternoon of messages and the people who answer already know the organizers, which is most of why they turn up. It caps hard at a dozen or so, which is exactly why the ladder continues.

Both `==` ties are real:

- **Value**: a block partnership and a call-back to past volunteers both convert one conversation into several confirmed people, and both cap at the size of the group on the other end.
- **Compliance cost**: neither stands up a collection point, so the only record either creates is the roster you were keeping anyway.

Compliance cost is a genuine axis here, not filler. Any channel that collects sign-ups collects names, emails, phone numbers and often dietary and t-shirt data about people who are not attendees, which needs a retention rule and someone who owns it before the first form is submitted. A retained past-volunteer list is that same decision made a year earlier and easy to forget.

**Default: a past-volunteer call-back plus a registration-gated sign-up form.** Below roughly 150 attendees, the network ask alone is the whole plan.

**Starved: the dedicated volunteer site** - top of value and top of both cost axes, so efficiency starves it every round. Promote it when:

- There are more rooms than one coordinator can staff by hand.
- Volunteers must self-serve across a multi-day multi-room grid.
- The event recurs and the site is built once and reused.

FOSDEM sits at exactly that condition.

**Deleted, not demoted: an open call with no named coordinator and no confirmation step.** Delete it everywhere. A call for volunteers posted to an announcement channel with nobody answering the replies produces a list of names and an unstaffed desk, and it is indistinguishable from a real channel until the morning of the event.

### Role-catalog depth

Efficiency: **named posts per area > full per-role catalog > catalog plus a per-role training gate > one undifferentiated pool**.

- value: catalog plus training gate > full per-role catalog > named posts per area > undifferentiated pool
- effort: catalog plus training gate > full per-role catalog > named posts per area > undifferentiated pool
- compliance cost: catalog plus training gate > full per-role catalog > named posts per area > undifferentiated pool

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and that is not a pass.** All three axes are the same list, so one mechanism blocks every pair: the deeper catalog buys more and is strictly worse on both cost axes. That covers the pairs against the undifferentiated pool too - it loses on value rather than winning anything for free, and the warning below is about where that cheapness actually lands. The check catches nothing; the ordering is argued.

Named posts per area - registration, information, rooms, setup and teardown, floaters - wins on efficiency because it costs one page and removes the single biggest day-of failure, which is a volunteer standing in a corridor with nothing assigned.

The compliance ordering deserves a warning, because it runs exactly opposite to the exposure each option leaves behind. Writing down that a post handles cash or registration records is what triggers a conversation about who may hold that data.

The undifferentiated pool triggers no conversation at all, and is also the option where a stranger nobody vetted ends up alone with the registration laptop. Cheap on paper, expensive in reality.

**Default: named posts per area**, with the posts identified in Q5 - anything touching payments or registration records - assigned to specific named people rather than open-claimed.

**Starved: the catalog plus a per-role training gate** - top of value and top of both cost axes. Promote it for any post handling money, personal data, or equipment that breaks a session when mishandled. FOSDEM gates precisely that and no more: new info-desk volunteers get trained on the point-of-sale system before handling transactions, which is a five-minute just-in-time gate rather than a training day for everyone.

**Deleted, not demoted: the undifferentiated pool**, at any event where a post handles cash, attendee records, or is the first place a code-of-conduct report lands. It survives only where the organizing team is also the entire volunteer pool.

### Recognition posture

Every rung here is shift-tied. Recognition that lands _after_ the event - a published thank-you naming volunteers, the retained past-volunteer list, the alumni loop - belongs to `samber/dev-event-organizer-skills@event-volunteer-experience` and carries a consent gate this menu does not rank.

Efficiency: **access in exchange for the shift > thanks by name at the end of the shift > feeding them properly > a volunteer t-shirt they keep > shift-linked status perks**.

- value (shifts finished, and people who come back): feeding them properly > access in exchange > t-shirt > shift-linked status perks > end-of-shift thanks by name
- effort: t-shirt > feeding them properly > shift-linked status perks > access in exchange > end-of-shift thanks by name

No compliance-cost axis applies: a t-shirt, a meal, a seat and a spoken thank-you trigger no review and are reversible next edition. Publishing a volunteer's name is the option that would carry that exposure, and it is not on this menu - see the sibling above. The one rung deleted for a different exposure is at the bottom of this section.

Access in exchange for the shift is the mechanism both built-out programmes use, and it costs nothing at an event that is free or not sold out. It has two published shapes worth copying:

- A seat saved in the session you are staffing - PyCon US tells tutorial hosts to sign up for the tutorial they wanted to attend.
- Front-row seats while heralding at FOSDEM - programmatic access traded directly for the room-lead role.

The t-shirt is ranked as recognition but earns its place operationally: it is how an attendee finds a volunteer in a corridor. FOSDEM colour-codes it - orange for general volunteers, green for the video team - which turns a perk into a wayfinding system, and is why it survives a budget cut that a pure perk would not.

**Default: access in exchange, plus food at the post.** Both are near-zero at a free or self-catered event, and both appear at every rung of the ladder.

**Starved: feeding them properly** - it tops the value axis and still loses the top of the order to two near-zero-effort options, because it is a catering line and a headcount the caterer needs weeks in advance. Promote it whenever a shift runs past roughly three hours, covers a mealtime, or falls outside event hours. FOSDEM feeds exactly those cases:

- Drinks and snacks at the info desks for active volunteers.
- Food vouchers for longer shifts.
- Full published meals for the buildup, cleanup and van crews.
- Staff who bring food to a post that cannot be left.

**Deleted, not demoted: a cash stipend.** Paying volunteers changes what the arrangement is, and the status question that follows is not reversible mid-edition once the first payment has gone out. Volunteer programmes at technical events do not pay stipends, and the uniformity of that practice is itself the signal.

## Failure modes

- **Sizing from an attendee ratio.** The only figure in circulation comes from an event's final edition and describes a team already past its limit. Fix: size bottom-up from posts and hours (step 3); the attendee count never enters the arithmetic.
- **Recruiting a month out at conference scale.** DevOpsDays' one-month timing is real and correct - for a network-sourced event of a few hundred. Fix: at the built-program rung, open sign-up six or more weeks out and stage the reminders; the roster deadline is set by t-shirt orders and briefings, not by the event date.
- **A shift grid with no named replacement rule.** The predictable failure is not that someone no-shows, it is that the person on post leaves anyway. Fix: publish the wait-then-escalate protocol and the rule that nobody leaves without confirmation of a replacement (step 9).
- **Volunteers on the code-of-conduct front line without the script.** Any volunteer may be the first person a report reaches, not just the named response team. Fix: brief the five-step escalation script to everyone, including the part that says they are not required to confront anyone.
- **A briefing that omits arrival buffers.** "Your shift starts at 14:00" produces a volunteer who arrives at 14:00, collects a t-shirt, finds the room, and reaches the post at 14:20. Fix: publish the buffer as part of the shift time and graduate it for first-timers.
- **Several people directing the same volunteer during a shift, each unaware of what the other told them.** This is a coordination failure distinct from the confirmation step in Q6/step 9: it happens live, mid-shift, to someone already covering a post. Fix: the coverage protocol names exactly one referent per shift who owns live direction for that post, so a volunteer has a single person to check with rather than whoever happens to walk past.
- **Merging the two "runner" roles.** FOSDEM's Runner is a general-purpose floater waiting in a staging area for task calls; PyCon US's Session Runner is a speaker shepherd working tight fifteen-minute intervals. Same word, different jobs. Fix: name them separately in your own catalog; an event that merges them gets neither.
- **Building the volunteer site for a 150-person event.** Over-investment is a real failure, not just under-investment. Fix: match the rung, and re-read the starved option's promotion condition before building anything reusable.

## Measurement

Measure coverage and briefing, not sign-ups. A sign-up count is the metric most likely to look healthy on an event that is about to run short at 15:00 on Saturday.

- **Post-hours covered, as a share of post-hours the schedule requires.** The only number that answers whether the roster is big enough. Compute it per hour, not as a daily total - a roster that balances across the day still has a hole in it.
- **Share of posts with a named backup.** Distinct from the above and more predictive of a bad afternoon.
- **No-show rate, and the share of no-shows where a replacement was confirmed before the post was left.** The second half is the one the protocol actually controls.
- **Share of volunteers briefed before their first shift, including the escalation script.** Target 100%.
- **Share of shifts that started on time**, measured against published times with the buffer included.

Pass threshold, and iterate until it is met: every post-hour in the schedule covered by a named person with a named backup, and every volunteer briefed on the escalation script before their first shift. Both thresholds are self-set rather than external standards. They are checkable against the grid you built rather than against an industry number, which is what makes them usable anyway.

## Invocation examples

- "How many volunteers do we need for a 400-person one-day conference with three tracks?" → run the interview, then step 3's bottom-up arithmetic; refuse the ratio question and answer with a post list.
- "We're two weeks out and only four people signed up." → the recruitment menu, re-ranked hard by the deadline: past-volunteer call-back and network ask, and cut posts rather than staffing them at half strength.
- "What do we tell volunteers at the briefing?" → step 8 and [references/briefing-and-coverage-protocols.md](references/briefing-and-coverage-protocols.md); the escalation script is not optional at any scale.
- "One of our room volunteers just messaged that she can't come in this afternoon." → the coverage protocol: post it to the coordination channel with post and time slot, and do not release the current person until the replacement is confirmed.

Expected output: a post list with per-post headcounts, a shift grid with arrival buffers and named backups, a role catalog with fit criteria, a sign-up and confirmation plan with dates, a briefing script, and a published coverage protocol.

## Reference

- samber/dev-event-organizer-skills@event-code-of-conduct - the policy, response-team composition, and incident runbook; this skill recruits and schedules into the response team and briefs the escalation script to every general volunteer.
- samber/dev-event-organizer-skills@event-run-of-show - takes this skill's shift plan as input and scripts what staffed posts do during the event; both briefings happen separately.
- samber/dev-event-organizer-skills@event-volunteer-experience - care and retention side after the shift ends; recognition not tied to a specific shift, the alumni loop, and bringing people back next edition.
- samber/dev-event-organizer-skills@event-team-structure - the standing organizing team structure, where Volunteer Lead is a named role; mirrors this skill's scope ceiling.
- samber/dev-event-organizer-skills@event-attendee-experience - staffing the check-in desk, help point, and meal distribution the posts in this roster cover.
- samber/dev-event-organizer-skills@event-first-edition - for a first edition where the founding team is the entire volunteer pool.
