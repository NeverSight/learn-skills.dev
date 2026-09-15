---
name: event-marketing-plan
description: Build the attendee-acquisition plan for a technical event - audience segments mapped to channels, the campaign-calendar spine (a ticketed event's percent-of-ticket-sales ladder or a free event's percent-of-attendance-goal curve), campaign moments pinned to pricing and program dates fixed elsewhere, budget allocated across the channel mix, funnel targets per phase, and each channel routed to the sibling that executes it. Use whenever asked to plan how to fill an event, run a ticket-sales or registration campaign, choose promotion channels, split promotion budget, or set registration targets by date. Do NOT use for the email copy itself - use samber/dev-event-organizer-skills@event-attendee-email-sequences - or ticket prices - use samber/dev-event-organizer-skills@event-ticket-pricing.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Marketing Plan

You build the acquisition plan that fills a technical event: which audience segments get reached through which channels, at what weight, on what dates, against what per-phase targets. This is the umbrella plan. It decides _when and how much_ each channel gets and hands the channel's own content to the sibling that owns it.

Four inputs arrive already decided. Do not re-derive them:

- **The message** - `samber/dev-event-organizer-skills@event-positioning` supplies the promise and the audience definition every channel's copy carries.
- **The demand read** - `samber/dev-event-organizer-skills@event-market-fit` supplies whether there is an audience at all, and is diagnostic where this plan is prescriptive.
- **The dates** - `samber/dev-event-organizer-skills@event-ticket-pricing` sets the price points and the early-bird cutoff. Those cutoffs are fixed calendar moments this plan reacts to; this skill never moves one to make a campaign more convenient.
- **Two channels' deal mechanics** - `samber/dev-event-organizer-skills@cross-event-promotion` and `samber/dev-event-organizer-skills@event-media-partnerships` own how those barter deals are sourced and structured. This plan only weights and schedules them.

Two organizer guides ground this plan:

- DevOpsDays' organizer guide names five acquisition channels and calls a mailing list "a powerful tool for ticket sales".
- MLH's organizer guide catalogs campus tactics and publishes a signup-to-attendance drop-off rate.

Both publish checkpoint numbers for total registrations, and both stop there: the funnel as a whole carries published figures, a single channel's yield in registrations does not. So when presenting the plan, say which targets are which:

- Whole-funnel checkpoints: published.
- Channel value ordering: your judgement.
- Per-channel targets: set from scratch.

Every ranking below is a default, not a law: it shifts with context and with who executes it. After the interview, re-rank both menus against what you already know about this organizer. Each of these overturns a default rung:

- An existing large mailing list.
- An organizer with a popular newsletter or podcast.
- A single-campus audience.
- A sponsor who bundles ad credits.
- A volunteer team with zero content-production capacity.

## Interview

Ask one question at a time, multiple-choice where possible.

Questions 4 and 7-9 exist because the channel and budget menus diverge sharply on time-to-effect, durability and effort; the default order cannot be picked for the user. Q4 carries the deadline axis: doors are the hard date. A short runway between announcement and doors promotes fast-acting rungs (paid ads, a partner's next send) over slow ones (building a list from zero, local relationship-building), which cannot repay inside one compressed cycle.

1. Ticketed (paid) or free registration? This picks the calendar spine, and it is the single most consequential answer in the interview.
2. Community-run or company/vendor-run? The channel economics differ (see the next section).
3. What is the target number - expected paid ticket sales, or an attendance goal? For a ticketed event, ask for expected sales **net of sponsor, speaker, organizer and volunteer comps**; those tickets never had to be sold.
4. Which dates are already fixed: announcement, early-bird close, CFP close, speaker announcement, full-agenda announcement, doors? Collect them before planning anything.
5. Where does the target audience already read, listen and gather - which lists, communities, meetups, campuses, employers? Name real properties; this settles the channel weights and breaks the value ties below.
6. What does the event already own: a mailing list and its size, social accounts and their reach, a prior edition's own sales curve, an existing partner roster?
7. Is there a cash acquisition budget at all, and who approves it? A community event funded ~80%+ by sponsorship spends acquisition money against catering, not against a marketing line.
8. One edition's push, or a compounding asset across editions? A compounding mandate promotes the slow rungs (list building, local presence, partner relationships) that a single edition never repays.
9. What is the effort ceiling - organizer hours per week, who writes, who shows up in person?
10. Is the edition in person, online-only, or hybrid?

## Community-run vs company-run

The buyer of a conference ticket is an individual developer whose employer often pays, so every event straddles employer-funded and self-funded attendance. The axis that actually changes the plan is who owns the event - the same axis this collection's positioning and sponsor skills argue:

- **Community-run** - the community-run organizer guides define the checkpoints and channel taxonomy used here. Acquisition is mostly owned and barter channels because cash competes with the event's own costs, and reciprocal-visibility swaps replace paid placement.
- **Company/vendor-run** - the community organizer guides are written for community events, so extrapolate rather than cite them at this pole. Expect a real budget line, a marketer who owns it, paid channels that a community event cannot reach, and media properties routing vendor promotion through commercial ad inventory rather than barter. The calendar spines still apply unchanged; only the budget posture moves.

Say which pole the plan assumes before allocating anything.

## Pick the calendar spine - never blend the two

Two calendar spine types exist. They measure **different denominators** and belong to structurally different events. Averaging them, or carrying a checkpoint from one into the other, produces targets that are wrong in both directions.

- **Ticketed conference → percent of expected ticket sales** (DevOpsDays organizing guide). Checkpoints sit at named marketing moments, not fixed calendar offsets, because sales spike at announcements. The risk being managed is under-selling.
- **Free event → percent of the attendance goal** (MLH hackathon organizer guide). Checkpoints sit at fixed offsets (2 weeks, 1 week) and the target exceeds 100% on purpose. The risk being managed is no-shows, not under-selling.

Full checkpoint ladders, the worked numbers behind both, and the phase-target method: [references/calendar-spines-and-phase-targets.md](references/calendar-spines-and-phase-targets.md).

This choice is deliberately not ranked. The two spines are not competing options with different value per unit of effort - they are descriptions of two different demand shapes, and the event's revenue and no-show structure picks one outright. Ranking them would be false precision: the "more efficient" spine is simply the one measuring the wrong thing for that event.

For the in-between case - a nominal-fee event, or a free event with a hard capacity cap - pick the spine by the failure you actually fear: unsold seats or empty seats. Run it as the plan's only target line. Read the other spine's checkpoint as a secondary sanity check that never enters a target.

## Workflow

1. Run the interview. Fix the spine (Q1), the pole (Q2), the target number net of comps (Q3), and the fixed dates (Q4).
2. Restate the message and the demand read from `samber/dev-event-organizer-skills@event-positioning` and `samber/dev-event-organizer-skills@event-market-fit` in one paragraph each. If either is missing, stop and route there first - a channel plan for an undefined audience allocates effort at random.
3. Map audience segments to channels from the Q5 answers, then weight them with the ranked menu below. Name the segment each channel is bought for.
   - One segment can need several channels.
   - One channel can serve several segments.
4. Lay the spine's checkpoints on the calendar, then pin every fixed date from Q4 onto it. Work backward from doors, not forward from today. Earliest anchor: **T-7 months, "ensure marketing is off and running"** (DevOpsDays organizer guide).
5. Allocate budget with the posture menu below. The percentage allocation table comes from B2B / B2C SaaS conventions, not from event-industry practice. Say so explicitly when showing it, so nobody reads a borrowed convention as an events standard.
6. Set funnel targets per phase against the spine's checkpoints, never against a straight line. Method and worked example: [references/calendar-spines-and-phase-targets.md](references/calendar-spines-and-phase-targets.md).
7. Route each channel to the sibling that executes it (see References). Hand over the weight, the phase, and the dates. Do not write the sibling's content here.
8. Re-forecast at each checkpoint against the plan's own line, and diagnose a miss before reacting to it (see Measurement).

If your harness has persistent memory, record for each edition:

- The spine chosen and why.
- The target net of comps.
- The channel weights, with the segment each was bought for.
- The fixed dates.
- The budget posture.
- Each checkpoint's planned-vs-actual.

The next edition's plan starts from a real prior curve instead of a blank calendar, which is exactly what the pace-index method needs.

## Channel mix

Ranked menu: value returned per unit of organizer effort, drawn from DevOpsDays' five-channel visibility taxonomy and MLH's campus and social tactic catalog. The value ranking is judgement rather than a measured benchmark. Re-rank it against what this organizer already owns.

Channel taxonomy, quotes from the guides, campus-scale tactics and the owned/earned/paid framing: [references/channel-menu-and-budget-allocation.md](references/channel-menu-and-budget-allocation.md).

- effort (organizer hours, coordination, recurrence): `local and campus engagement > partner channels > own social presence > paid ads == pre-event press > own mailing list > comms hub`
- value (registrations bought, judged not measured): `own mailing list > local and campus engagement == partner channels > own social presence > paid ads > pre-event press > comms hub`
- efficiency: `own mailing list > comms hub > partner channels > paid ads > local and campus engagement > own social presence > pre-event press`
- compliance cost (review triggered, reversibility lost): `paid ads > own mailing list > partner channels`

The other four channels carry no compliance cost of their own: posting on your own accounts, showing up at a meetup, publishing a link hub and pitching a local outlet touch no consent record, no signed agreement and no spend approval.

Both ties are argued:

- **Effort tie** (paid ads == pre-event press): a paid-ads run and a press pitch are each a few hours of setup or writing followed by waiting on someone else's system. Neither is a standing job the way social posting is.
- **Value tie** (local engagement == partner channels): both put the event in front of an audience someone has already assembled and that already trusts the assembler. The difference is whether an organizer shows up in person or a partner's channel does it for them, not how much reach is bought.

Compliance cost is real on exactly three rungs:

- **Paid ads** need an ad account in the organization's name, platform ad-policy review and someone authorized to commit the spend.
- **Own mailing list** carries consent exposure: a list collected for one edition, mailed for the next, without a documented opt-in, is the one acquisition asset that can force a deletion the event cannot undo.
- **Partner channels** carry logo-licensing and delivery terms, handled in `samber/dev-event-organizer-skills@cross-event-promotion` and `samber/dev-event-organizer-skills@event-media-partnerships`.

Each channel in full:

- **Own mailing list** - announcements of ticket availability, early-bird offers, agenda releases, countdowns. DevOpsDays' guide: "Keep emails informative and limit their frequency to maintain engagement." Worth building from zero if the event has none. Where last edition's registration form recorded who said they were not available that year, re-contact that specific segment at this edition's announcement - a "not available last time, are you free now" ask converts a list segment other channels never reach.
- **Comms hub** - one page centralizing every channel, shareable by QR code (DevOpsDays organizer guide). One-time build. It converts reach the other channels create rather than creating reach itself, which is why it sits low on value and high on efficiency at once. This plan owns the page; `samber/dev-event-organizer-skills@event-comms-channels` supplies the per-channel roster (name, job, owner, hours) it publishes.
- **Partner channels** - cross-event swaps, media and community partners, developer-ambassador programs. Executed by `samber/dev-event-organizer-skills@cross-event-promotion` and `samber/dev-event-organizer-skills@event-media-partnerships`; this plan sets their weight and phase.
- **Paid ads** - targeted social ads. MLH's guide describes them as "cheap and effective" for campus audiences (note: that claim is specific to campus scale, not general).
- **Local and campus engagement** - meetups, local employers, business associations (DevOpsDays); in-class pitches, tabling, flyering, student groups and departments, plus the "at least 3 schools within 6 hours" invitation rule (MLH). Treat business-support networks/incubators and named school contacts as two separate referrer pools rather than one undifferentiated local list - they run on different outreach cadences and are worth tracking apart so each pool's own conversion stays legible.
- **Own social presence** - regular posting across the event's accounts, varying times. Weighted below its intuitive place on purpose: DevOpsDays' guide names the problem directly, "with the dispersal of tech communities from Twitter, a lot of community events are struggling to reach people."
- **Pre-event press** - school paper, local outlets, community media (MLH). A lighter ask than a press campaign; a real one belongs to `samber/dev-event-organizer-skills@event-press-relations`.

Where to start:

- **Default rung**: own mailing list plus comms hub, with own social presence running underneath as the baseline.
- **Promotion condition**: add partner channels once Q5 names properties whose audience genuinely matches, and add paid ads only after one owned channel shows a tracked referral signal worth amplifying, never as the first move against a soft checkpoint.

**The starved option is local and campus engagement**: high value, highest effort, so efficiency never picks it. Promote it anyway in two cases:

- A first edition with no list to mail, where the top rung is simply empty.
- A geographically concentrated audience (one campus, one metro), where in-person presence reaches a share of the target no owned channel can.

The organizer guides argue for it directly. DevOpsDays states "avoid the misconception that a great agenda alone will attract attendees. Actively promote your event," and MLH treats flyering and in-class pitches as core rather than optional.

**Delete condition, keyed to Q10**: for an online-only edition, delete the in-person half of local engagement rather than demoting it - the meetup and community relationships survive online, the tabling and flyering do not. A deleted rung cannot quietly reappear as scope in week three.

## Budget allocation posture

Ranked menu - registrations bought per unit of money-handling and approval effort. Postures and the percentage table behind the full spread: [references/channel-menu-and-budget-allocation.md](references/channel-menu-and-budget-allocation.md).

- effort (planning, approvals, reconciliation, monitoring): `full spread > concentrated bet > fixed test budget > barter-only`
- value (reach bought, judged): `concentrated bet == full spread > fixed test budget > barter-only`
- efficiency: `barter-only > fixed test budget > concentrated bet > full spread`
- compliance cost: `full spread == concentrated bet > fixed test budget`

Barter-only carries no compliance cost of its own: its exposure is the partner agreement, owned by the two partner-channel skills named above.

Both ties are argued:

- **Value tie** (concentrated bet == full spread): both deploy the same money and buy comparable total reach. The spread hedges channel uncertainty, the bet compounds one channel's learning. They differ in variance, not in expected value.
- **Compliance cost tie** (full spread == concentrated bet): both cross whatever threshold triggers treasurer or finance sign-off and an ad account held in the organization's name, while a capped test budget usually clears under one organizer's own discretion.

Each posture in full:

- **Barter-only** - everything through owned channels and reciprocal-visibility swaps. No cash, no approvals.
- **Fixed test budget** - one capped amount, one paid channel, one measurable question.
- **Concentrated bet** - the bulk of available cash into the single highest-confidence channel.
- **Full spread** - a balanced percentage allocation across paid, content, partner and testing lines (not an event-industry standard; derived from SaaS marketing practice).

Where to start:

- **Default rung**: barter-only plus a fixed test budget, for a community-run event.
- **Promotion condition**: move to a concentrated bet when a checkpoint misses _and_ one channel already shows a tracked referral signal worth scaling. A miss alone is a reason to diagnose, not to spend.

**The starved option is the full spread** - its effort and approval load mean efficiency never picks it. Promote it for a company-run event with a standing marketing budget line and a marketer who owns reporting on it: there, the spread's hedging is worth its overhead, and the overhead is someone's actual job.

Where there is no cash at all - no acquisition line and no discretionary float - delete the three spending postures rather than parking them at the bottom. Barter-only is then the whole menu, and a rung nobody can fund does not get to reappear as a plan B the first time a checkpoint misses.

## Failure modes

- **Blending the two spines.** "200% of goal" and "40-50% of expected sales" are percentages of different denominators, one of an attendance goal and one of net-of-comps expected sales. Averaging them, or carrying MLH's 2-weeks-out rule onto a paid conference, sets a target that is unreachable or trivially met and tells you nothing either way. Pick one spine, state which, and keep the other out of the target line.
- **Setting the early-bird date here.** The cutoff arrives fixed from `samber/dev-event-organizer-skills@event-ticket-pricing`. Moving it to smooth a campaign changes the price ladder and the event's revenue, and the pricing skill's own checkpoint no longer means what it measured. Plan around the date. If it genuinely must move, route the decision back rather than absorbing it.
- **Doing a sibling's job.** Writing the announcement email, designing the registration page, or building the social content calendar inside this plan produces a second, competing version of work the sibling owns. Hand over weight, phase and dates. Stop there.
- **Treating the free-event drop-off as universal.** The 30-50% signup-to-attendance drop-off is MLH's, for free hackathons, and it is exactly why that spine targets 200%. A paid ticket has its own, much smaller no-show behavior, and its rate is self-set per event. Never apply the free-event over-registration multiple to a paid conference.
- **Presenting the budget percentages as an event standard.** They come from SaaS marketing practice, not from event-industry benchmarking. Shown unlabeled, they read as an event-industry standard the reader will defend to a board that has no reason to accept them. Label them explicitly.
- **Reading launch week as demand.** The announcement spike measures reach, not demand. Week two is when the campaign pattern becomes readable. A quiet middle is the normal shape of the curve, not a failure signal.
- **Starting marketing when the program is locked.** DevOpsDays' guide warns directly: "avoid the misconception that a great agenda alone will attract attendees." The documented earliest start point is T-7 months, well before most programs finalize.

## Measurement

Channel attribution is the honest weak point: **the whole-funnel checkpoints carry published benchmarks, every channel-level target is yours to set.** Published event figures measure the funnel, not a channel's contribution to it, so a per-channel number is only ever as good as the tracked link behind it. Before launching, write down what each signal would trigger.

- **Checkpoint hit or miss against the chosen spine**: the only externally grounded target line in the plan. Ladders and figures: [references/calendar-spines-and-phase-targets.md](references/calendar-spines-and-phase-targets.md).
- **The execution-vs-demand discriminator** (ticketed spine): roughly 40-50% of expected sales one month out is on track. A team that skipped or delayed its visibility push lands nearer 25-30% at the same point (DevOpsDays). A miss in that band is a marketing-execution problem, not proof of missing demand - diagnose before concluding, because the two have opposite fixes. Before reading a shortfall as weak demand, check three communication causes specifically: program or speaker announcements that ran later than planned, a theme narrow enough to exclude part of the intended audience, and messaging that never actually said who is welcome - the last of these is a funnel problem worth naming outright rather than a vague "we should promote more" diagnosis.
- **Pace index against the event's own prior curve**: tickets-to-date divided by curve-expected, times 100. Above 100 is running hot, below 100 is a gap with a size and a deadline attached. It needs a prior curve, which is why step 8's memory record matters.
- **Per-channel referral signal**: a distinct tracked link or registration code per channel, decided before launch because it cannot be added retroactively. A channel at zero across two editions loses its weight next edition. Where a partner channel serves several distinct closed communities (a school, a professional group), give each its own code rather than one shared partner-channel code: it tracks which specific community actually converts, and it reads to that community as an invitation made for them rather than a generic discount.
- **Funnel demographics beyond headcount** (self-set, judged not a benchmark): role mix, geography, and one figure most plans skip - whether registering costs the attendee something real beyond the ticket price, such as time off work the next business day. A signup form that only asks role checkboxes filters cheaply but excludes anyone who fits no listed label; if that trade-off is made deliberately, invest the effort saved into messaging (who is welcome, what a typical attendee looks like) rather than leaving the exclusion unaddressed, and widen the checkbox list from the first edition rather than patching it in later once a gap is visible.
- **Self-reported source on the registration form**: "how did you hear about us" undercounts owned channels and double-counts whatever the registrant saw last. Useful only as a cross-check against tracked links, never as the primary attribution.
- **Reach-versus-conversion split** (self-set diagnostic): healthy traffic to the registration page with low conversion points at the price or the page, not at the channel mix - route to `samber/dev-event-organizer-skills@event-ticket-pricing` or `samber/dev-event-organizer-skills@event-landing-page` rather than buying more reach.

## Invocation examples

- "We're running a 400-person paid DevOps conference in October - build the marketing plan: channels, calendar and targets."
- "Our free hackathon needs 500 attendees. Registrations open in three months. What should the campaign look like and how many signups do we need by when?"
- "We're a month out and sitting at 28% of expected ticket sales. Is this a demand problem or did we under-market?"
- "We have €2,000 for promotion and a volunteer team of four. Where should it go?"

Expected output:

- The chosen spine, named with its reason.
- The target, net of comps.
- An audience-to-channel map with weights and the segment each channel is bought for.
- A dated campaign calendar with every fixed date pinned onto the spine's checkpoints.
- A budget posture with allocation.
- Per-phase funnel targets.
- A routing list naming which sibling executes each channel.

## References

- [references/calendar-spines-and-phase-targets.md](references/calendar-spines-and-phase-targets.md) - both checkpoint ladders in full, a worked calendar for each spine, the net-of-comps calculation, and the per-phase target method.
- [references/channel-menu-and-budget-allocation.md](references/channel-menu-and-budget-allocation.md) - the channel taxonomy, campus-scale tactics, the owned/earned/paid framing, the four budget postures, and the percentage allocation table.

Channel executors (route each channel to the appropriate sibling):

- `samber/dev-event-organizer-skills@event-social-media` - owns the platform mix, content calendar and amplification kits inside the social channel.
- `samber/dev-event-organizer-skills@event-landing-page` - owns the registration funnel's on-page conversion; this plan drives traffic to it.
- `samber/dev-event-organizer-skills@event-attendee-email-sequences` - writes the emails whose send moments this plan's calendar places.
- `samber/dev-event-organizer-skills@event-comms-channels` - owns channel selection methodology and voice consistency; this plan consumes that choice rather than re-deriving it.
