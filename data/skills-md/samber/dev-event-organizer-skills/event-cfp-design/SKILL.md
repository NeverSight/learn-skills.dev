---
name: event-cfp-design
description: Design a technical event's call for papers - the published call, not the selection behind it. Covers the CFP open/close timeline worked back from the event date, submission form fields, which session formats the call offers, the anonymization posture (named, opt-in, or mandatory blind review), review criteria published in the call itself, stated speaker benefits, per-person submission caps, first-time-speaker support, and the CFP tooling capabilities to look for. Use whenever asked to open or write a CFP, set a CFP deadline, design a talk submission form, decide on blind review, or state speaker perks in a call for proposals. Do NOT use to review or score submissions - use samber/dev-event-organizer-skills@event-talk-selection.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event CFP Design

You design the call for papers of a technical event: the public artifact a prospective speaker reads, the form they fill, and the timeline both sides commit to.

You do not:

- Score or select the submissions - the rating grid, review committee, and notifications belong to `samber/dev-event-organizer-skills@event-talk-selection`.
- Recruit speakers outside the CFP - that parallel channel belongs to `samber/dev-event-organizer-skills@event-speaker-sourcing`.

The session formats the call offers are an input, chosen upstream by `samber/dev-event-organizer-skills@event-format-selection`.

Every recommendation below is a default, not a law - it shifts with context and with who executes it. After the interview, re-rank every menu in this skill against what you know about this organizer: an existing mentor pool, a distributed international community, a tool already paid for, or a hard program-announcement date can each overturn a default rung.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 4-6 exist because the menus below diverge sharply on time-to-effect, durability of the payoff, and effort - the default rankings cannot be picked for the user.

1. What is the event date, and which structure was chosen - shape, track count, session-format mix? If no structure exists yet, route to `samber/dev-event-organizer-skills@event-format-selection` first: a CFP cannot offer formats nobody has picked.
2. Who owns the event: community conference (open CFP fills the program) or vendor/user conference (mostly invited content, the CFP fills a slice)?
3. Is this the first CFP or a repeat? If a CFP has run before: how many submissions for how many slots, and what complaints did speakers or reviewers raise?
4. How many weeks remain until the program must be announced? (A hard date gates the timeline menu - below the floor, the open CFP is deleted, not compressed.)
5. Is this edition a one-off or a compounding annual asset? (A compounding mandate promotes the slow, trust-building rungs: blind review, mentorship, published criteria that hold year over year.)
6. What is the effort ceiling: review committee headcount, organizer hours, and who will sustain CFP promotion across the open window?
7. What can the budget honestly promise speakers - the free-ticket floor only, travel reimbursement or grants, anything more? Unconfirmed money never goes in the call.
8. Is speaker diversity a stated goal, and is there capacity for active outreach beyond posting the call?
9. Which assets already exist that should re-rank the menus: past accepted proposals to publish, a volunteer mentor pool, an international speaker community with visa lead times, a CFP tool already in use?

## Community vs vendor conference

The submitter is a developer either way. What changes CFP design is who owns the event (the same split `samber/dev-event-organizer-skills@event-format-selection` argues):

- **Community conference** - the CFP is the program's main intake; sourced norms are explicit sales-pitch bans and "no speaker spots can be bought by sponsors: not ever - period" (DevOpsDays organizing guide). Everything sourced in this skill comes from this pole.
- **Vendor/user conference** - content is mostly invited and organized around the vendor's architecture (per swyx); the CFP, where one exists, fills a community slice of an otherwise curated program. The menus below still apply to that slice, but the timeline couples to the vendor's launch calendar, not only to speaker travel.

Say which pole a recommendation assumes when they differ.

## Workflow

1. Run the interview; fix the ownership pole (Q2).
2. Take the offered formats from the chosen structure (Q1): the call offers exactly the session formats the structure needs - no more, no fewer. Give each format its own submission type with its own fields; a broader menu than one "talk" slot is sourced practice (PyCon US offers talks, tutorials, Spanish-language charlas, and posters - the charla being a concrete non-English inclusion mechanism).
3. Set the timeline from the menu below, working back from the event date and the program-announcement date (Q4).
4. Design the submission form from the form-depth menu and [references/submission-form-catalog.md](references/submission-form-catalog.md); set the per-person submission cap (the one sourced example: PyCon US caps at three proposals per person).
5. Write the review criteria into the call itself - the published-criteria section below - and decide the anonymization posture from its menu; state the posture, and when identity enters review, in the call.
6. State speaker benefits explicitly in the call: the sourced floor and the honesty rules below. Never publish a perk the budget hasn't confirmed (Q7).
7. Pick the first-time-speaker support rung from its menu.
8. List the tooling capabilities the chosen design needs (form fields, scheduling, review modes, messaging) from the catalog reference - capabilities first, tool second.
9. Plan promotion for the whole open window (see the promotion section - thin by design, and honest about it).
10. Close and hand off: the call states when submitters hear back; submissions go to `samber/dev-event-organizer-skills@event-talk-selection`, the invited-speaker channel runs in parallel via `samber/dev-event-organizer-skills@event-speaker-sourcing`, and the accepted program lands in `samber/dev-event-organizer-skills@event-schedule-design`.

Present the assembled call section by section (timeline, form, criteria, benefits) for validation before it goes public - a published CFP is a promise to strangers, and quiet edits after launch burn trust.

If your harness has persistent memory, record the chosen timeline anchors, posture, cap, published criteria, and - most importantly - the measurement thresholds that would revise each choice next edition.

## CFP timeline

Ranking (default, not a law - Q4, Q8, Q9 re-rank it):

- effort (calendar runway + promotion sustained across the window): `long window > standard window > floor-compressed`
- value (reach, under-represented outreach time, early demand signal, international travel lead): `long window > standard window > floor-compressed`
- efficiency: `standard window > floor-compressed > long window`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks all three pairs: whichever rung leads on value costs strictly more, and no rung is ever at least equal on value while costing less. No third axis is printed that could block or rescue a pair. The check catches nothing; the ordering rests entirely on the argument below.

The sourced floor (DevOpsDays organizing guide): "open your CFP as soon as possible, and close it at least 6-8 weeks before your event." Keep the call "open for at least a month" and "at least 2 weeks to consider proposals and fill in any gaps." The reason is the speaker's calendar, not the organizer's: "People will usually need at least 4-6 weeks to arrange for travel or time off."

- **Standard window** - the default: open roughly two months, close 8+ weeks before the event, review inside the gap. Fits a repeat edition with a known audience.
- **Floor-compressed** - the minimum the source allows: ~4 weeks open, close at 6-8 weeks out, 2 weeks of review - about 10-12 weeks from open to event, total. Legitimate under a hard date; nothing below it is.
- **Long window** - the starved option: DevOpsDays' own master timeline anchors CFP launch at T-7.5 months, submission voting at T-4.5, program launch at T-3.5 - roughly a three-month review-to-launch runway. Highest reach and the only rung with room for mentorship pairing and visa lead times, but it loses every efficiency round because its real cost is not calendar - it is promotion sustained for months (see failure modes). Promotion conditions: a first edition using CFP volume as a pre-sales demand read (hand that read to `samber/dev-event-organizer-skills@event-market-fit`), international speakers, or a mentorship program that needs room before close.

Below the floor - an event closer than ~10 weeks, or a close date inside 6 weeks of the event - the open CFP is deleted, not demoted: speakers cannot arrange travel inside the sourced 4-6 weeks, so the program goes invited via `samber/dev-event-organizer-skills@event-speaker-sourcing`.

## Submission form depth

Ranking (default, not a law):

- effort (speaker friction + form build + per-submission review time): `extended > standard > minimal`
- value (review discriminating power + program-balance and logistics data): `extended > standard > minimal`
- efficiency: `standard > minimal > extended`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort run in one order, so all three pairs fail identically: the rung ahead on value is the rung that costs more. Nothing else is printed to block or rescue a pair. The efficiency line rests on the arguments below, not on a passed check.

- **Standard** - the default: title, an abstract capped near 100 words, a separate "why me" context field, the format pick, intended audience level, bio, optional prior-talk links. The abstract/context split is the load-bearing choice: it lets reviewers score topic quality and speaker fit separately instead of untangling one text box (per swyx's CFP advice - title weighted "twice as important as your abstract", short abstract, a distinct context field worth using). Field-by-field detail, sourced examples, and a negative example live in [references/submission-form-catalog.md](references/submission-form-catalog.md).
- **Minimal** - title, abstract, bio. Near-zero effort keeps it second on efficiency, but its cheapness is partly false economy: every dropped field is paid back in review-time guesswork and follow-up email. Acceptable for a meetup-scale call or a small invited-plus-CFP hybrid.
- **Extended** - the starved option: adds per-format conditional fields, recording/consent checkboxes, a travel-grant request folded into the form (per PyCon US), and a structured outline. Promotion conditions: a grant program exists (an in-form checkbox beats a separate application process), the structure offers formats with genuinely different requirements, or the committee is large enough to use the extra structure.

## Anonymization posture

Ranking (default, not a law):

- effort (review-process discipline + speaker instructions + two-phase mechanics): `mandatory blind > opt-in anonymous > named review`
- value, submission-side equity and trust: `mandatory blind > opt-in anonymous > named review`
- value, program-shaping data during review (name recognition, local/out-of-town balance, speaker-fit reads): `named review > opt-in anonymous > mandatory blind`
- efficiency: `named review > opt-in anonymous > mandatory blind`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** One mechanism blocks all three pairs, and it is not the usual one: the two value axes are exact reverses of each other, so whichever rung leads on equity trails on program-shaping data, and no rung can be at least equal on both. Effort is never reached in any pair. The check finds nothing here - the efficiency line rests on the argument below.

The two value axes genuinely disagree - that disagreement is the decision, and the evidence sits on both sides. Per swyx: "blind CFP review is important for some level of equity... In my experience, most CFP's are NOT blind." PyCon US is the at-scale counter-example that actually runs it: "During initial review, proposal author information is not displayed to reviewers".

- **Named review** - the de facto field default per swyx's observation, and the default here for a small first CFP where a 2-3 person committee hand-tunes program balance. Only honest with published criteria doing the fairness work the anonymity isn't.
- **Opt-in anonymous** - the tooling default (two of the three example platforms in the catalog reference ship anonymization as an optional mode). Treat it as a platform capability, not a fairness posture: a pool mixing named and anonymous submissions is not reviewed on one footing.
- **Mandatory blind** - the starved option: top of equity value and top of effort, so efficiency never picks it. Its real costs, from the PyCon implementation: review runs two-phase (identity must enter before the program is final - balance, travel, the name-recognition read), and speakers must be instructed to self-police identifying details out of titles and free text, because the platform hides the author field, not what the author wrote. Promotion conditions: equity as a stated goal (Q8) plus committee capacity for a two-phase process. If promoted, publish the mechanics in the call including exactly when identity enters, or you've built blind-review theater (see failure modes).

## Published review criteria

Write the criteria into the call itself. The sourced template is DevOpsDays' six content-policy points, stated openly to speakers (verbatim in [references/published-call-evidence.md](references/published-call-evidence.md)):

- No sponsor-bought speaker spots, ever.
- New content favored over already-published material.
- Local/out-of-town speaker balance.
- New speakers actively favored.
- Bold subjects encouraged.
- Tool/product-specific talks routed to open space rather than rejected.

The call redirects vendor pitches to the format that fits them, which only works if the structure chose an open-space block upstream.

Honesty check before publishing: per swyx, organizers optimize a program to "sell tickets, have a great content mix, and sell next year's tickets, in roughly that order." If name recognition and topic mix will in fact shape selection - they will - the criteria must not pretend otherwise. Publish criteria you will actually apply, and let the community-pole hard line ("not ever - period") carry the one non-negotiable.

## Speaker benefits stated in the call

- The published floor: "at minimum, all speakers should receive a free event ticket" (DevOpsDays organizing guide). State it explicitly; a call silent on perks reads as a call with none.
- Travel: reimbursement is "a good use of funds if available" with a documented caveat worth repeating to organizers - direct payment "can bring with it complex issues around taxes, visas, and conflict of interest/employment agreements." If running grants, reuse PyCon US's policy shape: grants framed as enabling attendance rather than rewarding quality, capped at one per accepted proposal, with an explicit ask that speakers who can afford to attend self-select out of the limited pool.
- Honorarium: no industry norm exists, but two named community events now publish a fixed figure in their own call: !!Con states a flat "$256 (USD)" honorarium for every speaker, unchanged across its 2018-2024 editions; ffconf (UK) states "£500 honorarium" alongside full travel, hotel, and meals. The two amounts don't converge on a rate - treat them as calibration points, not a market rate or "industry standard". If the user wants an honorarium policy, show these two figures, then gate the actual number on their own budget and legal/tax review.
- The rule that binds all three: the call states exactly what speakers get, and nothing the budget hasn't confirmed.

## First-time-speaker support

Ranking (default, not a law):

- effort (setup + per-speaker time): `proposal mentorship > worked examples > encouragement copy`
- value (submissions from new voices that survive review): `proposal mentorship > worked examples > encouragement copy`
- efficiency: `worked examples > encouragement copy > proposal mentorship`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and that is never a pass.** Value and effort share one ordering, so the same mechanism blocks every pair: the higher-value rung is strictly the costlier one. No further axis exists to change that in any pair. The check verifies nothing; argue with the ratios below.

- **Worked examples** - the default: publish past accepted proposals as calibration; PyCon US points first-timers at prior years' proposals. A first edition has no archive - fall back one rung and let the published criteria plus a well-split form do the calibrating.
- **Encouragement copy** - near-zero effort, always included, never sufficient alone: a stated "favor new speakers" line is itself one of the sourced published criteria.
- **Proposal mentorship** - the starved option: a structured pre-submission pairing program, separately timed alongside the CFP. PyCon US's Proposal Mentorship is a documented example of the mechanism. Promotion conditions: a volunteer mentor pool exists (Q9) and the window is long enough to pair mentors before close - which couples this rung to the long-window timeline.

## Promotion

No conference organizer or CFP platform has published a channel-by-channel breakdown of where submissions actually came from - say that plainly rather than inventing a ranked channel menu. Three things are sourced and load-bearing (verbatim in [references/published-call-evidence.md](references/published-call-evidence.md)):

- Sustain promotion across the whole open window, not just at open - the long-window rung's cost lives here.
- A concrete sequencing pattern (Write the Docs): write the announcement, post it to the blog, tweet a link to the post, then wait one to two hours before the mass email - the delay lets the community catch errors before the wider list sees them.
- The equity warning (DevOpsDays): "under-represented people in tech are much less likely to respond to your CFP." If diversity is a goal (Q8), reach actively into those communities; the open call alone will not do it. Two sourced mechanisms for that active reach: a maintained list of named community groups with a template outreach email (`jlengstorf/awesome-speaker-diversity`), and PyCon 2010's own categorized CFP-distribution target list as a concrete precedent for the same move at conference scale.

## Failure modes

- **Unstated criteria.** A rubric exists but the call doesn't publish it - rejections read as arbitrary, and next year's submission pipeline pays for it. The sourced practice is six criteria in the call itself.
- **Perk promises without policy.** Travel or honorarium language published before budget confirmation, walking into the sourced taxes/visas/conflict-of-interest trap. The call states the confirmed floor and stops.
- **Blind-review theater.** Mandatory blind announced, but identity leaks unmanaged in free text, or quietly re-enters for program shaping with no published phase boundary. Publish the mechanics or pick named review.
- **The stale long window.** A CFP opened at T-7.5 months with one announcement and no sustained promotion sits silent through the middle of its window. A long window is a promotion commitment, not just an early open date.
- **A CFP below the floor.** Closing inside 6 weeks of the event, or open under a month, asks speakers to defy the sourced 4-6 week travel reality. Delete the open call; go invited.
- **One text box for everything.** An abstract that must carry topic, outline, and "why me" at once can't be scored on any of them - the split form exists so review can separate topic quality from speaker fit.
- **A call offering the wrong formats.** Formats in the call that the chosen structure doesn't have (or missing ones it does) create submissions nobody can schedule. The format menu is an input from upstream, not a CFP-time decision.
- **Reading oversubscription as failure.** Turning away most submissions is the normal state of a healthy CFP (see measurement) - the fix for volume is review capacity, not a narrower call.

## Measurement

Documented benchmarks are stated; everything else is a threshold you set before the CFP opens.

- **Submissions-to-slot ratio**: PyCon US 2025 accepted 15% of 938 proposals - roughly 6.5:1. Swyx's benchmark puts an established conference's pool at 200 to 800-1,200 applicants, making 8-30x oversubscription normal at a popular single-track event. As a pre-launch demand read, even 2-3:1 on a first CFP is a strong signal - that go/no-go reading belongs to `samber/dev-event-organizer-skills@event-market-fit`.
- **First-time-submitter share**: DjangoCon Europe 2024 drew 174 proposals from 138 submitters, 51 of them first-time speakers - submitter diversity as a vibrancy signal, not just volume.
- **Off-policy share**: the fraction of submissions the published criteria already exclude (vendor pitches in the curated pool) - a high share means the criteria aren't landing in the call.
- **Submission timing**: where in the window submissions arrive; a dead middle argues the promotion plan, not the window length, failed.

Pick 2-3, write down the revision each would trigger next edition, and record both before the event.

## Invocation examples

- "Our first DevOps conference is in nine months - set up the CFP end to end."
- "Write the CFP page for our two-day community conference: timeline, form, criteria, perks."
- "Should our CFP be anonymous? We got flak last year about the same names being picked."
- "The event is in ten weeks and we have no talks yet - can we still run a CFP?"

Expected output: a CFP design brief with:

1. The timeline worked back from the event date, with open/close/notify anchors.
2. The form field list per offered format, plus the submission cap.
3. The published criteria text.
4. The anonymization posture, with its mechanics as the call will state them.
5. The speaker-benefits statement.
6. The promotion and outreach notes, with the sourced equity warning.
7. The handoff plan to selection, sourcing, and scheduling.

Presented section by section for validation before the call goes public.

## References

- [references/submission-form-catalog.md](references/submission-form-catalog.md) - field-by-field catalog with examples, the four-format PyCon menu, the submission cap, tooling capability checklist with named example platforms, and a positive/negative form example.
- [references/published-call-evidence.md](references/published-call-evidence.md) - the DevOpsDays timeline and six criteria verbatim, speaker-benefit and travel-grant language, the anonymization evidence on both sides, first-time-speaker mechanisms, the under-represented-response warning and two sourced outreach mechanisms, a sourced promotion sequencing pattern, and the oversubscription benchmarks.

See also, same collection:

- `samber/dev-event-organizer-skills@event-format-selection` - chooses the structure whose session formats this call offers.
- `samber/dev-event-organizer-skills@event-talk-selection` - reviews and selects what this call brings in: rating grid, committee, bias control, notifications.
- `samber/dev-event-organizer-skills@event-speaker-sourcing` - the parallel invited-speaker channel, and the fallback when the timeline deletes the open CFP.
- `samber/dev-event-organizer-skills@event-speaker-experience` - delivers the benefits this call promised, including the recording policy stated per session format; it never re-opens the honorarium question this skill leaves as a stated gap.
- `samber/dev-event-organizer-skills@event-schedule-design` - lays the accepted program into the track structure downstream.
- `samber/dev-event-organizer-skills@event-market-fit` - owns the demand reading of CFP oversubscription this skill's measurement defers to.
