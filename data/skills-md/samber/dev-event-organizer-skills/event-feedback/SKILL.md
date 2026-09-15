---
name: event-feedback
description: Design and run participant-feedback collection for one edition of a technical event - what gets asked, who answers it, through which channel, when it goes out, and what goes back to respondents. Covers format-adapted question sets (meetup pulse, conference satisfaction and return intent, hackathon team dynamics, mentors, judging fairness, project continuation), attendee, speaker and sponsor segmentation, in-room versus emailed collection against real response-rate data, survey length, anonymity and free text. Use whenever asked what to put in a post-event survey, when to send it, how to fix a response rate nobody answered, how to survey a hackathon, or what to do with the answers. Do NOT use for the team's own retrospective - use samber/dev-event-organizer-skills@event-debrief.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Feedback

You design and run the collection of feedback _from_ the people who came: attendees, speakers, sponsors, and - at a hackathon - mentors and judges. You own the instrument, the channel, the timing, the response-rate tactics, and what goes back to respondents. You close with findings someone else acts on.

**You never look inward.** `samber/dev-event-organizer-skills@event-debrief` runs the organizing team's own retrospective, and states the boundary from its side: this skill collects from participants, and its summary is _"an input here, and the direction never reverses"_.

It holds identically from this side. You do not run the post-mortem, and you do not analyse the team.

Four more things arrive already owned. Collect for them; do not decide for them.

| Sibling                        | Owns                                                                                                                                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `event-market-fit`             | The demand verdict - what participants _did_ (return rate, renewal, sellout), never blended with what they _said_. You hand findings over as one qualitative input, never a go/no-go. |
| `event-continuous-improvement` | Cross-edition trends. You produce one edition's findings; comparing to last year's is the easiest scope to absorb by accident.                                                        |
| `event-speaker-experience`     | What a speaker receives, and when - the envelope. You design the instrument that produced the ratings - the questions.                                                                |
| `event-sponsor-fulfillment`    | Writes the ROI report _to_ the sponsor. You collect the sponsor's verdict _from_ them - opposite directions, same week.                                                               |

## What the field actually publishes about this

Organizer guides name the practice in one line each. DevOpsDays: "surveying...is optional, but strongly recommended". MLH: "email attendees and sponsors a post-event survey". Neither designs the instrument, so the question set, the timing, and the response-rate target are yours.

The event-industry research ecosystem does publish response-rate bands, a survey-length effect, and satisfaction thresholds, all with real sample sizes: [references/response-rate-evidence-and-timing.md](references/response-rate-evidence-and-timing.md). Communities do publish findings, among them WordPress, KubeCon, MLH, PyCon, and Write the Docs: [references/publishing-and-findings-handoff.md](references/publishing-and-findings-handoff.md).

The question craft comes from customer-discovery interviewing, and half of it does not carry over. Keep the two rules: non-leading phrasing, and "what they did, not what they would hypothetically do". Drop the purchase commitment those rules were built to extract: the event has already happened, and nothing is being sold.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6 to 8 exist because the menus below diverge sharply on time-to-effect, durability, and effort; the defaults cannot be picked for the user without them.

1. What format, how many participants, and **has the event already happened, or is the day still being planned?** The second half decides whether an entire collection channel is still available.
2. Which roles actually exist, and which do you need to hear from? Ask which exist before which you want.
3. What decision is waiting on these answers, and who makes it? A question with no decision behind it gets cut in step 4.
4. What did you promise about anonymity, and does anything judge a named person's performance? Changes both instrument and channel.
5. How can you reach each role, and how were addresses collected (registration, ticketing, sponsor contract, badge scan)? You need the consent basis, not just the list.
6. When must findings be in someone's hands? That date is this skill's deadline.
7. One-off or recurring, does a prior edition's response rate exist to compare, is a public recap already planned?
8. Effort ceiling: hours available after the event, who reads and analyzes, can the run of show still change?
9. Roughly what share of the budget do sponsors fund?

## Event format and a captive moment

A recruiting-driven or vendor-run event adds talent-pipeline questions to the sponsor module: interview conversions, cost per hire. Never include those by default at a community event. That is one conditional module, not a split running through the whole skill.

Otherwise, ask an enterprise-buyer attendee and a hobbyist-meetup attendee the same things, in the same words, on the same timing. Two axes genuinely change the output:

- **Format** changes the instrument: a hackathon survey keeps the conference core and adds team formation, mentor availability, judging fairness, tooling quality, and project continuation - first-class measures in academic hackathon instruments. A meetup usually justifies one question and a box.
- **Whether a captive moment still exists** changes the channel, moving response rate by a multiple, not a few points. A closing plenary, session-end break, or demo day puts everyone in one room with the experience fresh; a dispersed audience has no such moment, and no email craft recovers the difference. When the channel is email, `event-attendee-email-sequences` owns the send's copy and cadence; this skill owns only the question set.

## Workflow

1. Run the interview. Pick the channel rung first if the day is still being planned - that choice has a deadline the others do not.
2. **Start from the decision, not a question bank**: for each Q3 decision, write the question whose answer would change it. What survives is the instrument; the rest is curiosity - the cheapest way to hit the length rung.
3. **Pick the format-adapted question set**: core by format, plus role modules for roles that actually exist (Q2). Sets, closed/open balance, worked pairs: [references/question-sets-by-format-and-role.md](references/question-sets-by-format-and-role.md).
4. **Cut to the depth rung**: delete every question with no named decision behind it. A very short instrument more than doubles the median response rate of a long one (largest available study). Say the trade to the user.
5. **Set anonymity before the channel** (§ Anonymity and free text) - it deletes channel rungs, so decide it first.
6. **Field within 24-48 hours**, reminder days later - strong practitioner consensus, no controlled test exists for technical events. Cadence: [references/response-rate-evidence-and-timing.md](references/response-rate-evidence-and-timing.md).
7. **For a hackathon, plan the second instrument now**: main survey at demo day, a separate short follow-up 1-2 weeks later on whether teams kept working. A second survey, not a delayed first one.
8. **State the response rate beside every finding.** Work it out per role before reading a single answer: every number that follows inherits its confidence.
9. **Read results as findings, not a score.** Group free text into themes with counts, and never average satisfaction with return intent.
10. **Close the loop with respondents** at the chosen rung - the one step that pays into next edition.
11. **Hand findings over and stop**: whole summary to `event-debrief`, qualitative read to `event-market-fit`, per-speaker material to `event-speaker-experience`, sponsor verdicts to `event-sponsor-fulfillment`.

If your harness has persistent memory, record per edition:

- The instrument as fielded.
- The channel and send dates.
- The response rate per role.
- The headline numbers.
- The themes, with their counts.
- What was promised about anonymity.
- What went back to respondents.

Next edition then opens with a comparable instrument instead of a fresh invention - and a response rate has no meaning at all until there is a second one beside it.

Every ranking below is a default, not a law; it shifts with context and with who executes it. Where a constraint deletes a rung, strike it from that menu's axis lines too - a rung surviving in the ordering survives in the reader's head and returns as scope.

Re-rank all three menus against what you already know about this event:

- A team that already runs an in-room poll during the day buys the channel menu's top rung for almost nothing.
- An event whose audience is one Slack community reaches people through a channel none of these rungs assume.
- An organizer who has published findings twice already has the third menu's starved option as a habit rather than a project.

## Collection channel

Ranked menu - responses actually collected, per unit of setup and coordination. Value rests on **measured figures**:

- Emailed surveys: **10-30%** response rate.
- In-room capture: **40-60%** response rate.
- An incentive: lifts emailed response by **roughly half again**.
- In-room completion: **85-95%**. A different quantity from response rate - the share who finish once they have started.

Compare channels on response rate only. Sources, sample sizes, and the vendor-versus-research tiering: [references/response-rate-evidence-and-timing.md](references/response-rate-evidence-and-timing.md). Ratios, not point figures, are what transfers.

- effort (setup, day-of coordination, prize administration): `email plus reminders plus an incentive > in-room capture > email plus reminders > single email`
- value (responses collected, and collected while memory is fresh): `in-room capture > email plus reminders plus an incentive > email plus reminders > single email`
- efficiency: `email plus reminders > in-room capture > single email > email plus reminders plus an incentive`
- compliance cost (review triggered, reversibility spent): `email plus reminders plus an incentive > single email == email plus reminders > in-room capture`

Value and effort disagree: the incentive costs more than a channel move and buys less. In-room capture dominates the incentive rung outright, with a higher response rate at both ends of its band and lower effort, and efficiency ranks it above accordingly.

Efficiency still leads with email plus reminders, a free lift for one scheduled send. Never credit that lift with the 85-95% completion figure, which counts finishers, not responders.

Compliance does not copy effort. An incentive draw needs an identifier attached to a response, turning an anonymous rating of a named speaker into a permanent link. The two email rungs tie because exposure attaches to the list, not to the number of sends; in-room capture through an anonymous code carries the least.

- **Single email** - one send to the registration list after the event.
- **Email plus reminders** - one reminder days later, at most one final one. More produces fatigue, not responses.
  - Route the send through any small sub-group channel the respondent already belongs to, a project team's own chat or a track's channel, instead of or alongside the general list. A peer channel carries trust and a shared memory of the event that a cold broadcast must build from nothing, and it costs no extra rung: the ask still goes out once, through a different pipe. This is this skill's own convention, not a measured figure to set beside the sourced bands above.
- **Email plus reminders plus an incentive** - a prize draw. Event-specific prizes outperform generic gadgets.
- **In-room capture** - a code at session end, a plenary prompt, a demo-day form. Needs a line in the run of show.

**Default: email plus reminders.** Promote to in-room capture when Q1 says the day is still being planned, the format has a captive moment, and Q8 says the run of show can take one more line - all three.

**Starved option: the incentive** - first on effort and compliance cost, second on value. Promote only when Q7 shows a prior rate at or below the band floor and the day is already over.

When Q1 says the event already happened, **delete in-room capture** - record it for next edition instead. When anonymity is required, **delete the incentive rung**: a draw needs an identity, anonymity forbids one.

## Instrument depth

Ranked menu - findings you can act on, per unit of design and analysis time. Every ordering here is judgment; the length-versus-response-rate trade underneath it is measured.

- effort (drafting, fielding per role, reading and analysis): `full role-segmented instrument > core plus one role module > short core > single-question pulse`
- value (decisions the answers actually change): `full role-segmented instrument > core plus one role module > short core > single-question pulse`
- efficiency: `short core > core plus one role module > single-question pulse > full role-segmented instrument`

No dominance check backs this ordering. Value and effort run in the same order, so no rung could ever have violated one, and the check catches nothing: clean only by construction, not a pass. The efficiency ordering therefore carries its own weight, on three claims.

- **Short core buys the whole event's verdict**, from the largest sample the length evidence allows.
- **Every rung above it buys narrower answers from fewer people**, at several times the analysis cost.
- **The response-rate penalty lands on effort and efficiency, never on value.**

No compliance-cost axis here. The exposure is third-party personal data in free text, and it arrives as a step at the first open-ended question rather than climbing rung by rung. An axis would be tied rungs dressed as an ordering, so § Anonymity and free text carries it as a rule instead.

- **Single-question pulse** - one rating, one open box. Honest for a meetup of a few dozen.
- **Short core** - 3-5 questions: satisfaction/return intent, one content question, one operations question, one open "what should we change".
- **Core plus one role module** - core to everyone, plus a module for the single role whose decision is worth the most (sponsor renewal, speaker return-and-refer).
- **Full role-segmented instrument** - per-role instrument for every role, plus the hackathon layer (team dynamics, mentors, judging fairness, tooling, continuation) and its separate outcome follow-up.

**Default: short core.** Add one role module when Q3 names a decision owned by a specific role due before next edition. Move to full instrument when Q1 says hackathon - those questions exist nowhere else.

**Starved option: full role-segmented instrument** - first on value and effort, last on efficiency. **Promotion condition, keyed to Q1 or Q9**: a hackathon, or where sponsors fund most of the budget.

When Q2 shows no sponsors and no formal speaker slate, **delete the role module and the full instrument** - modules for roles that do not exist read as thoroughness and produce nothing.

## Anonymity and free text

Decide this before the channel, because it deletes rungs from that menu.

**The promise:**

- **Turn anonymity on whenever the instrument asks about judging fairness, mentor quality, inclusion, or a named individual's performance.** The reason is mechanical, not ethical: a participant who suspects the judge will read their name gives you an unusable rating.
- **Anonymous and confidential are different promises.** Say which one you are making, in the instrument itself.

**The free text:**

- **Free text will name people.** Decide who reads raw responses, what reaches the named person, and what never leaves the team. `event-speaker-experience` owns the speaker pass-through rule; any code-of-conduct allegation leaves immediately for `event-code-of-conduct`'s pipeline and is never a survey finding.
- **Ask for publication consent at collection time or not at all.** A verbatim quote cannot be retro-consented once the respondent is anonymous, which deletes the public rung below.
- **Convert free text to structured choices once volume outgrows reading.** One published precedent did this after 2,867 responses and said so publicly.

## Closing the loop with respondents

Ranked menu - next edition's response rate and the trust that produces it, per unit of drafting and exposure. The mechanism is documented: a practitioner sustaining response rates in the eighties and nineties attributes it to always acting on feedback, so participants believe answering is worth it.

- effort (drafting, review, sign-off): `public findings post > you-said-we-changed note > acknowledgement > nothing back`
- value (belief that answering changes something, which is what next edition's rate is made of): `you-said-we-changed note > public findings post > acknowledgement > nothing back`
- efficiency: `you-said-we-changed note > acknowledgement > public findings post > nothing back`
- compliance cost (review triggered, reversibility spent): `public findings post > you-said-we-changed note > acknowledgement`; publishing nothing carries none.

Value and effort disagree at the top: the public findings post reaches a far larger audience, but most of that audience never answered the survey. The lift comes from a respondent seeing their own answer move something, so the you-said-we-changed note dominates the post on both axes at once, higher value at lower effort, and efficiency ranks it above accordingly.

Publishing nothing sits last on efficiency despite costing nothing: zero return on zero effort never wins a ratio.

- **Nothing back** - findings go to the team; respondents hear no more.
- **Acknowledgement** - a short thank-you with the headline number and confirmation answers were read.
- **You-said-we-changed note** - acknowledgement plus 2-3 findings being acted on and what changes. A few lines' marginal cost, since the findings already exist by step 9.
- **Public findings post** - numbers and themes published openly, ideally with a note on what the survey design itself got wrong.

**Default: the you-said-we-changed note.** Promote to public when Q7 says the event compounds for several more editions and a recap is already planned. `event-debrief` owns publication and its code-of-conduct sign-off; you supply only the survey half.

**Starved option: public findings post** - first on effort and compliance cost, second on value, third on efficiency. Promote when the event must prove something to a constituency that never answers surveys.

For a private or NDA-bound event, or where publication consent was not requested at collection time, **delete the public findings post** - the material is not yours to publish.

## Re-ranking against the interview answers

Say which answer moved which option, per menu, rather than silently reordering. Full Q1-Q8 breakdown against all three menus: [references/interview-answer-reranking.md](references/interview-answer-reranking.md).

Two moves are easy to miss:

- A decision due within days (Q3) promotes in-room capture even outside Q1's own conditions.
- A compounding event with a recap already planned (Q7) is the only path that promotes the public findings post.

## Failure modes

- **Building from a question bank.** Ten plausible questions produce ten unowned answers and a halved response rate. Start from the decision.
- **Asking hypotheticals.** "Would you attend a workshop day?" collects imagination; "which sessions did you go to?" collects behaviour. Keep the phrasing craft; drop the purchase commitment it was built to extract.
- **Averaging everything into one score.** Satisfaction, return intent, and operations answer three different questions; blending produces a number nobody can explain.
- **Reading twelve responses as a verdict.** A low response rate usually means the collection failed, not that attendees were indifferent.
- **Emailing a week later.** Consensus converges on 24-48 hours; the further out, the more rate lost.
- **Promising anonymity and running a prize draw.** The draw needs an identity - pick one before fielding.
- **Passing a free-text complaint straight to the named person.** `event-speaker-experience` owns what a speaker receives; the code-of-conduct pipeline owns allegations. Neither is a finding to forward on instinct.
- **Collecting and never reporting back.** The failure that compounds: respondents who hear nothing do not answer next year.
- **Surveying a hackathon like a conference.** Team formation, mentors, judging fairness, and tooling are the substance of that format; a conference core alone measures its catering.

## Measurement

Response-rate figures come from the event-research and vendor ecosystem, heterogeneous and mostly undisclosed - credible enough to set a floor, not clean enough as a standard: [references/response-rate-evidence-and-timing.md](references/response-rate-evidence-and-timing.md).

Two pass thresholds, iterate until each holds:

- **Zero unowned questions** (gate, checked before fielding) - every question maps to a named decision and a named person from Q3. This skill's own bar, set by judgment and measured nowhere. Re-read the draft question by question; attach an owner or cut the question.
- **Response rate at or above the published band floor** (gate, checked after fielding) - roughly one in ten emailed, four in ten in-room. The floor is anchored to the bottom of a published band, which makes it a measured anchor rather than a measured threshold. Below it, treat the collection as failed and act: send the reminder, shorten the instrument, move the channel. Never read the audience as indifferent.

Signals to record, not targets:

- **Response rate per role** - one blended number hides a sponsor set where two of six answered.
- **Return intent** - below roughly two-thirds is an early warning; hand the trend to `event-continuous-improvement`.
- **Completion vs. start rate** - where people abandon flags which question was too long or vague.
- **Whether and how fast respondents heard back** - the single best predictor of next edition's rate.

## Invocation examples

- "Our conference finished yesterday - what do we actually put in the attendee survey, and when do we send it?"
- "We ran a hackathon and the usual conference survey feels wrong. What should we be asking instead?"
- "We emailed 400 attendees and got 18 responses. What went wrong and can we still fix it?"
- "Should the speaker survey be different from the attendee one, or just longer?"
- "One of the free-text answers is a complaint about a specific speaker. What do we do with it?"
- "Do we publish the survey results, and what happens if they're bad?"

Expected output:

- An instrument sized to a chosen depth rung, with every question tied to a named decision.
- A channel and a send schedule with a reminder cadence.
- A stated anonymity posture and a free-text handling rule.
- Findings grouped into themes with their counts and the response rate stated beside them.
- A decision on what goes back to respondents.
- Hand-offs to the debrief, demand, speaker and sponsor siblings, with every claim labelled as published evidence or this skill's own judgment.

## References

- [references/question-sets-by-format-and-role.md](references/question-sets-by-format-and-role.md) - core question sets per format including the hackathon layer, the attendee/speaker/sponsor modules with the recruiting-driven conditional, the closed-versus-open balance rule, the anonymity guidance, and worked good-and-bad question pairs.
- [references/response-rate-evidence-and-timing.md](references/response-rate-evidence-and-timing.md) - every response-rate and satisfaction figure with its source, sample size and credibility classification, the send-timing consensus and why it is unproven, the reminder cadence, and the incentive evidence.
- [references/publishing-and-findings-handoff.md](references/publishing-and-findings-handoff.md) - the published-report precedents with their sample sizes, the findings summary's shape, and what each receiving sibling is handed.

Other sibling skills referenced throughout: `event-debrief`, `event-market-fit`, `event-speaker-experience`, `event-sponsor-fulfillment`, `event-code-of-conduct` (see body above) - plus `samber/dev-event-organizer-skills@event-run-of-show`, which owns the day and the one line that makes in-room capture possible.
