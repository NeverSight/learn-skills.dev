---
name: event-landing-page
description: Build a technical event's public front door and the small site around it - the page shape for the funding model (a ticketed event's single-CTA hero, or a free event's stats hero with no registration to sell), the section set, a date-gated CTA state machine so Propose renders only during the CFP window and Register only inside the registration window, the accessibility target, and the event structured data. Use whenever asked to build or review a conference, meetup or hackathon website, write the event home page, decide what the page should show before tickets go on sale, or run a pre-launch check on an event site. Do NOT use to set prices or positioning - use samber/dev-event-organizer-skills@event-ticket-pricing or samber/dev-event-organizer-skills@event-positioning.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Landing Page

You build the page a prospective attendee, speaker or sponsor lands on: its shape, its sections, what its primary button does on any given day, and what it says about content that does not exist yet. This is channel execution, not strategy. Almost everything the page says was decided upstream.

Four things arrive already decided. Do not re-derive them, and do not argue against them:

- **The campaign weight, phases and dates** - `samber/dev-event-organizer-skills@event-marketing-plan` owns the channel mix, the calendar spine and the per-phase targets. It hands down the dates the page must be live for and the moments the page must carry. Never move a date.
- **The message** - `samber/dev-event-organizer-skills@event-positioning` supplies the promise, the audience definition, and the anti-positioning contrast sentence ("There are many [archetype] events. This is not one of them."). Carry that sentence verbatim. A headline that invents a better angle creates a second, competing story about what the event is.
- **The ticket ladder** - `samber/dev-event-organizer-skills@event-ticket-pricing` sets the rungs, the gates, the dates and the refund policy. Present the ladder as it arrives. Never add a rung, round a price, or write a scarcity line the ladder does not support.
- **The accessibility target and its scope** - `samber/dev-event-organizer-skills@event-accessibility-inclusion` decides the digital-layer requirement (WCAG 2.2, level AA) and which surfaces are in scope. Implement it on this page. Never choose the target.

Two boundaries sit on your border, and both are easy to absorb by accident:

- **The CFP page and its submission form belong to `samber/dev-event-organizer-skills@event-cfp-design`.** Link out to the call. Do not design the form fields or the timeline.
- **The emails that fire after someone registers belong to `samber/dev-event-organizer-skills@event-attendee-email-sequences`.** Own the page and the path up to the button, then say what happens after it rather than writing it.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 8-10 exist because the three menus below diverge sharply on time-to-effect, durability and effort; without those answers, no default ordering can be picked for the user. Question 11 feeds the compliance-cost axis on the third menu.

1. What did the marketing plan hand down: the campaign phases, and every fixed date - announcement, CFP open and close, speaker reveal, agenda release, on-sale, early-bird close, doors? If nothing was handed down, stop and route to `samber/dev-event-organizer-skills@event-marketing-plan` first; a page with no campaign calendar under it has no way to know what to show.
2. What is the funding model: priced, nominal, or free-to-attend with no registration at all? This decides the page's shape more than any other answer (see the branch below).
3. What are the positioning statement and the anti-positioning contrast sentence, word for word?
4. Is there a CFP, what are its open and close dates, and is the call on track for submissions or running short?
5. What does the ticket ladder look like - the rungs, what gates each one, and on what dates?
6. What accessibility target did the sibling set, and which surfaces did it put in scope?
7. First edition or recurring - and does a past-edition archive actually exist: photos, talk recordings, a speaker list, sponsor logos?
8. What is the doors date, and how many weeks of runway before the first campaign moment the page must be live for?
9. One edition's page, or a site meant to persist and be rebuilt each edition from the same structure?
10. Who builds and maintains this, for how many hours across the whole campaign - and can they change what the page shows on a date without a developer touching it?
11. What photo opt-out did the past edition's badges carry, and what do the speaker agreements permit for republishing its photographs and talk recordings?

## Funding model

Who buys and who pays come apart on a conference ticket: an individual developer buys it, and an employer usually reimburses it. `samber/dev-event-organizer-skills@event-ticket-pricing` already splits its ladder on that, so an invoice rail reaches this page as a rung to present rather than as a page-shape decision.

The split leaves exactly one trace here: a short, linkable block the visitor forwards to whoever approves their travel budget. That is one section in the section set, not a branch.

What changes the whole page is **whether there is anything to buy**. Two published conference sites anchor the poles:

- **Priced or nominal** - PyCon US 2026 puts a hero with the name, dates and location above a single "Register Today!" button linking straight into the ticketing flow, followed by venue details and a conference-breakdown timeline. Exactly one primary action competes for attention anywhere on the page; no secondary CTA fights it. A ticketed, capacity-constrained conference is the closest this domain gets to the SaaS single-CTA rule being legitimate.
- **Free-to-attend, no registration** - FOSDEM 2026 has **no CTA at all**, because there is nothing to register for. Its hero substitutes scale and credibility signals for a value proposition - "8000+ hackers", "65 devrooms", "1013 lectures" - with the dates and location, then goes straight to the schedule, the video archive, news, sponsors and the venue. Its footer groups the practical cluster (accessibility, code of conduct, during-the-event, health policy) as its own block rather than scattering those links through the nav.

Forcing a "Register Now" button onto a page with nothing behind it is the wrong transfer from the SaaS rule. The free-event hero is a different shape, not a degraded version of the priced one. Read the funding model off Q2, which reads it off `samber/dev-event-organizer-skills@event-ticket-pricing`; never re-decide it here.

## Workflow

1. Run the interview. Fix the dates, the message, the ladder and the accessibility target from Q1-Q6 before designing anything.
2. Branch on the funding model. A free, no-registration event skips every registration mechanic below rather than emptying it.
3. Restate the positioning statement and the anti-positioning sentence. Every headline below inherits both, unchanged. Where `samber/dev-event-organizer-skills@event-positioning` has genuinely refreshed the promise for this edition, show the old headline struck through beside the new one: a returning visitor reads a real pivot faster that way than from a rewritten paragraph. Use that device only for a pivot already decided, never as a substitute for deciding one.
4. Choose the page shape with the first menu. Whether the site is one page or ten decides which of the following steps have anywhere to put their output.
5. Build the section set for the chosen shape. Published section orders per funding model, the hero field list, and a negative example: [references/page-shape-and-section-set.md](references/page-shape-and-section-set.md). Write the FAQ against the procedural anxieties an applicant or attendee carries about this event's own mechanics: what it means to enter, when teams form, what happens if a rule is misunderstood. Skip the generic "what is this event" questions the rest of the page already answers.
6. Wire the date-gated CTA state machine with the second menu, then write the transition table: which CTA is on screen between which two dates. Table, the no-code fallback, and the structured-data block: [references/cta-state-machine-and-structured-data.md](references/cta-state-machine-and-structured-data.md).
7. Decide the reveal posture for every section whose content does not exist yet, with the third menu. This is a per-section decision, not one setting for the whole page.
8. Implement the accessibility target the sibling decided, in the build rather than after it: [references/digital-accessibility-implementation.md](references/digital-accessibility-implementation.md).
9. Emit the structured-data block - a machine-readable name, description, dates, URL, image and location. Field list in the same reference as step 6.
10. Run the pre-launch gate in Measurement. All four binary checks pass, or the page does not go live.
11. Hand the post-click path to `samber/dev-event-organizer-skills@event-attendee-email-sequences` and the tracked per-channel links back to `samber/dev-event-organizer-skills@event-marketing-plan`. Say what you are handing over; do not write the emails.

If your harness has persistent memory, record the section set with the funding model that justified it, the CTA transition table with its real dates, which sections were withheld and why, and the accessibility scope. A recurring event rebuilds from that record instead of from a blank page, and next edition's dates are the only thing that actually changed.

Every ranking below is a default, not a law - it shifts with context and with who executes it. Re-rank all three menus against what you already know about this organizer: an existing site that persists across editions, a designer already on the team, a page nobody can edit without a developer, a badge photo opt-out most attendees took, an event that sells out on announcement. Each menu below names which interview answer moves which of its options.

## Page shape

Ranked menu - questions a visitor gets answered per unit of build and upkeep effort. The rungs, the three orderings, the default and its promotion conditions are this skill's own construction, not measured thresholds. **Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean by construction rather than by adjudication, and by-construction is never a pass.**

Value and effort share one ordering, so one mechanism blocks all six pairs: the shape that answers more questions costs strictly more to build and keep, and no rung is ever at least equal on value while costing less. No third axis is printed here. The check can catch no misordering, so the efficiency line rests entirely on the arguments below rather than on anything it survived.

- effort (build hours, content to write, upkeep across the campaign): `full multi-page site > front door plus the program set > front door plus practical annexes > one page`
- value (questions answered, plus URLs other people can link to): `full multi-page site > front door plus the program set > front door plus practical annexes > one page`
- efficiency: `front door plus practical annexes > one page > front door plus the program set > full multi-page site`

- **One page** - a single scrolling page: name, dates, location, the positioning sentence, one CTA, the practical facts. Everything else is an anchor link.
- **Front door plus practical annexes** - the same front door, plus Location, Code of Conduct and Accessibility as their own addressable pages. The jump in value is not about length: an anchor is not an address. A code of conduct and an accessibility statement get cited by third parties, forwarded to employers, and pointed at by the siblings that wrote them. None of that works against a fragment on a scrolling page.
- **Front door plus the program set** - adds Program and Speakers as their own pages, with a page per talk and per speaker once the content is real.
- **Full multi-page site** - the whole DevOpsDays set as separate pages: welcome, program, speakers, sponsor, registration, propose, location, contact, diversity, conduct.

**Default rung: front door plus practical annexes.** **Promotion condition** (Q1 and Q4): move to the program set the moment the program is real - talks accepted, speakers confirmed - because the reveal is a dated campaign moment and it needs somewhere to land. Do not build those pages ahead of the content; that is what the third menu is for.

**The starved option is the full multi-page site** - top on value, top on effort, so efficiency never picks it. Promote it in two cases:

- Q9 says the site persists and gets rebuilt each edition, so the structure is paid for once and amortized across editions the way a per-year content directory is.
- A sponsorship agreement contracts a logo placement and a sponsor page becomes a fulfilment item owned by `samber/dev-event-organizer-skills@event-sponsor-fulfillment`, not an optional rung.

When Q10 says one volunteer with a handful of hours and no way to edit the page on a date, **delete the two upper rungs outright and strike them from the axis lines above** rather than leaving them as aspirations. A ten-page site with four empty pages is worse than one honest page, and a rung parked at the bottom of a menu reappears as scope in week three.

## CTA posture

Ranked menu - visitors who take the action actually available today, per unit of setup and date-discipline effort. The rungs, the four orderings, the default and its promotion conditions are this skill's own construction, not measured thresholds. This one needed adjudication: one rung is dominated outright (contact-only beats the persistent button row on value at identical effort), and the efficiency line honours that.

- effort (setup, plus the discipline to keep it correct as dates pass): `dual gated row > single date-gated primary > notify-me capture > persistent multi-CTA == contact only`
- value (the visitor takes the one action open right now, and the page never sends anyone at a closed door): `dual gated row > single date-gated primary > notify-me capture > contact only > persistent multi-CTA`
- efficiency: `single date-gated primary > dual gated row > notify-me capture > contact only > persistent multi-CTA`
- compliance cost (review triggered, reversibility spent): `notify-me capture > every other rung`; the capture is the only one that collects personal data, so it needs a consent basis, a privacy notice and a deletion path before it ships. The four link-only rungs carry none.

The effort tie is argued: what costs effort on this menu is date-conditional logic, and neither the contact link nor a row of permanent buttons has any. Both are static markup written once and never touched again. They are equal in work and very unequal in value, which is exactly why contact-only outranks the button row on efficiency.

- **Contact only** - an organizer contact link and nothing else. In the DevOpsDays template this link is unconditional and present at every phase (`layouts/partials/events/cta.html`); it is also the honest whole menu for an event with nothing open yet.
- **Notify-me capture** - an email field so the announcement has somewhere to land before anything is for sale. Content Marketing World's landing page is a published example: a prominent notify-me box and sign-up section for the stretch before registration opens. `samber/dev-event-organizer-skills@event-marketing-plan` backs the rung from the other side, ranking the owned mailing list above every other channel and calling it worth building from zero.
- **Single date-gated primary** - at most one primary button on screen at a time, whose target switches by date: Propose during the CFP window, Register inside the registration window, and when both are open the CFP link demotes to text. PyCon US shows the single-action half of this shape, with exactly one action competing for attention.
- **Dual gated row** - Propose and Register render as independent buttons, each gated on its own dates, plus the unconditional Contact. This is literally what the DevOpsDays template does: Propose renders only between `cfp_date_start` and `cfp_date_end`, Register only when registration is explicitly open or the current date sits inside the registration window and it has not been closed.
- **Persistent multi-CTA** - Register, Propose, Sponsor and Newsletter all sitting on the page for the whole campaign. Its one merit is that nothing is ever missing; its cost is that half the buttons are lies on any given day.

**Default rung: the single date-gated primary.** **Promotion condition** (Q4 against Q5): move to the dual row when the CFP window and the registration window genuinely overlap _and_ speakers are as scarce as attendees - a first edition, or an undersubscribed call.

**The starved option is the dual gated row** - top on value, top on effort, so efficiency never picks it. Promote it when either holds:

- The two windows overlap for more than a couple of weeks, since a CFP demoted to a text link for a month is a CFP nobody sees.
- `samber/dev-event-organizer-skills@event-cfp-design` reports the call running short of submissions, because speaker acquisition is then the binding constraint rather than ticket sales.

When Q2 says free-to-attend with no registration, **delete the notify-me capture, the single date-gated primary and the dual row outright, and strike all three from the axis lines above.** There is no gated action to hang on any of them.

**Delete the persistent multi-CTA too, from this menu and from the axis lines above, wherever the program is invited rather than called for.** With Register and Newsletter already gone, a row carrying only Propose and Sponsor is the dual row under another name; with no call either, it is a row of one. Contact-only plus the schedule and news links is then the whole menu, and the FOSDEM hero carries the credibility signals a button would have carried.

## Content-reveal posture

Ranked menu, applied **per section** rather than once for the whole page - what a visitor learns per unit of effort about content that is not real yet. The rungs, the four orderings, the default and its promotion conditions are this skill's own construction, not measured thresholds. Adjudicated: three dominance relations, all honoured below.

- effort (writing, asset production, and the upkeep of coming back): `substitute with the archive > published thin > named with a date > omit entirely == "coming soon" placeholder`
- value (the visitor can decide, and the page makes no promise it breaks): `substitute with the archive > named with a date > omit entirely > published thin > "coming soon" placeholder`
- efficiency: `omit entirely > named with a date > substitute with the archive > published thin > "coming soon" placeholder`
- compliance cost (review triggered, reversibility spent): `substitute with the archive > every other rung`; republishing past attendees' photographs and past speakers' recordings needs the consent the badge-carried photo opt-out owned by `samber/dev-event-organizer-skills@event-accessibility-inclusion` and the speaker agreements actually granted, and a recording republished without it cannot be un-published. The four text-only rungs carry none.

The effort tie is argued: omitting a section and pasting "coming soon" into it are both one-time near-zero acts with nothing to maintain, and both end in the same later edit. The difference between them is a decision, not work - which is why one of them dominates the other outright.

- **Omit entirely** - the section is absent from the page and from the nav until its content exists. The live 2026 DevOpsDays city page keeps its Program, Speakers and Sponsors rows wrapped in HTML comments while Dates, Location, Register, Propose, Diversity and Contact stay live. This is the organizers' own answer, and it is the default.
- **Named with a date** - a heading plus the date its content lands, and nothing else. It answers the visitor's real question, which is usually not "who is speaking" but "when will I know enough to book a flight". Only use a date that comes off the CFP timeline or the talk-selection schedule and that you will actually hit.
- **"Coming soon" placeholder** - a heading with a dateless promise. It costs the same as omitting, advertises an absence, and answers nothing.
- **Published thin** - the section goes live with whatever partial content exists: three speakers of twenty, a draft grid marked draft. It gets screenshotted and circulated in the state you published it.
- **Substitute with the archive** - the top of the value axis: replace the not-yet-real section with last edition's evidence, meaning photographs, talk recordings, who spoke, which sponsors backed it. Nothing else on this menu turns an absence into a reason to attend. The DevOpsDays template carries exactly this, as an impressions video from the previous year plus a list of every past edition, and it is the honest event-scale replacement for the "10,000+ teams" social proof a SaaS page uses and an event does not have.

**Default rung: omit entirely**, matching the DevOpsDays template's own handling. **Promotion condition** (Q1 and Q8): move to named-with-a-date for the one or two sections whose absence actually blocks the decision the visitor came to make - normally the program, and normally when travel, visas or budget approval have deadlines of their own that land before your reveal date.

**The starved option is substituting with the archive** - top on value, top on effort, so efficiency ranks it third. Promote it when either holds:

- Q7 says the archive already exists, because the marginal effort collapses to selecting and publishing rather than producing.
- The visitor's real question is "what is this event like" rather than "who is speaking", which is the question a program section never answers anyway.

When Q7 says first edition, **delete the archive rung outright and strike it from all four axis lines.** There is nothing to substitute.

Left on the menu, it gets satisfied with stock photographs of a generic conference audience, which is the same lie as a "coming soon" placeholder with a bigger budget. Say instead what the event is for, who is organising it, and what is decided. A first edition's honest hero is the promise and the people, not borrowed atmosphere.

## Failure modes

- **Overriding what a sibling already decided.** Rounding a ticket price to look cleaner, moving a CFP deadline to fit the layout, inventing an early-bird cutoff, or replacing the positioning sentence with a better angle in the hero. Each creates a second source of truth: one attendees screenshot, or a competing story about what the event is. Present what arrived; route a genuine change back to the sibling that owns it.
- **A Register button with nothing behind it.** The single-dominant-CTA rule is real for a ticketed event and meaningless for a free one. FOSDEM's page has no CTA because there is nothing to register for, and a button that opens a page saying "registration is not open yet" costs more trust than the empty space would have.
- **A stale CTA after its window closes.** A Propose button still live a week after the CFP closed sends a speaker to a closed form, which is the single failure the date-gating exists to prevent. If nothing on the site can change on a date, use the manual transition checklist in the CTA reference and put its dates in the campaign calendar.
- **Importing an A/B testing plan.** A CRO skill's own author puts the floor at roughly 1,000 sessions or 30 conversions in the window; below that, the data cannot separate a real problem from noise, and first-principles friction should be ranked instead. An event page structurally never reaches that, even at campaign peak, and a single edition has no second run to iterate against. Rank the page against the pre-launch gate instead of testing it.
- **Importing the SaaS section order.** Its Problem → Solution → Features → Testimonials → Pricing spine assumes a pain-point narrative and tiered software plans. An event page's job is identity and program facts, and the published orders in the reference are what real conference sites use.
- **Borrowed social proof.** The SaaS "10,000+ teams" line assumes a customer base a first or small edition does not have. Named speakers, real sponsor logos and last edition's archive are the honest substitutes.
- **Bolting accessibility on after launch.** A registration flow that cannot be completed by keyboard is a person who does not attend, and no on-site provision rescues that. It is also far cheaper to build than to retrofit, and the retrofit never gets scheduled.
- **Absorbing the CFP form or the confirmation emails.** Both sit one click from the page and belong to siblings. Link out; hand over.

## Measurement

Two refusals come first, because everything after them depends on why they are refusals.

- **This skill quotes no conversion rate for an event landing page.** The available figures are SaaS and paid-traffic numbers with no event framing, and quoting one here would dress it up as event evidence. If a user asks what a good conversion rate is for an event page, say that the published rates describe SaaS and paid-traffic funnels rather than event pages, instead of handing over one they will defend to a board.
- **Section order, hero length and CTA count follow observed practice, not a standard.** The reference records three concrete section sets from real events; every ordering judgment here is reasoned from those, and says so where it goes beyond them.

Because of the first refusal this skill sets **no numeric conversion threshold**. An imported rate would be false precision, and the reader would optimise against a number that means nothing here.

A binary pre-launch gate replaces it. The four checks below are this skill's own construction, not a published standard, and each one is settled by a single person in an afternoon rather than by a measurement nobody can take. **All four pass, or the page does not go live:**

1. **Every CTA transition has a date, and each one fired.** Walk the transition table against the campaign calendar. A transition with no owner and no date is a transition that does not happen.
2. **What, who, when, where and what it costs are answerable in one screen on a phone**, without scrolling and without reading a paragraph. Verify by handing it to someone who has never seen the event, not by rereading it yourself.
3. **The structured-data block validates and carries the real dates, location and URL.** Machine-checkable, and the one item on this list a script can confirm.
4. **The registration flow completes with the keyboard alone**, end to end, including any date picker and the payment step. This is `samber/dev-event-organizer-skills@event-accessibility-inclusion`'s target, not an extra bar this skill invented.

Beyond the gate, three things are worth tracking, and all three are self-set, not benchmarked:

- Which per-channel tracked link brought each visitor - you create the links, `samber/dev-event-organizer-skills@event-marketing-plan` reads them.
- Whether any section on the page is currently promising content past its stated date.
- For a recurring event, which sections the next edition rebuilt unchanged, since those are the ones worth turning into a persistent structure.

## Invocation examples

- "We announced our 400-person infra conference last week and the site is one page with a Register button that goes nowhere. What should be on it right now?"
- "Our CFP closes Friday and tickets go on sale two weeks later - what does the home page do in between?"
- "The event is free and there's no registration at all. Everyone keeps telling me I need a call to action. Do I?"
- "First edition, no speakers confirmed yet, page needs to be live Monday. What goes on it and what do I leave off?"
- "Review our conference site before we launch the campaign."

Expected output: the page shape with the answer that justified it, the section set with each section's reveal posture and reason, a CTA transition table with real dates and a named owner per transition, the structured-data block, the accessibility scope with who implements it, and the pre-launch gate run item by item - with every self-set element labelled as such.

## References

- samber/dev-event-organizer-skills@event-marketing-plan - owns the campaign phases, dates and channel weight this page executes within.
- samber/dev-event-organizer-skills@event-positioning - supplies the message and the anti-positioning sentence the page carries verbatim.
- samber/dev-event-organizer-skills@event-ticket-pricing - sets the ladder this page presents, with its gates, dates and refund policy.
- samber/dev-event-organizer-skills@event-cfp-design - owns the call, its form and its timeline; this page links out to it and gates the link on its dates.
- samber/dev-event-organizer-skills@event-accessibility-inclusion - decides the digital-layer target and scope this page implements, owns the accessibility page's content, and owns the badge-carried photo and recording opt-out the archive rung depends on.
- samber/dev-event-organizer-skills@event-attendee-email-sequences - owns what happens after the button, starting with the confirmation.
