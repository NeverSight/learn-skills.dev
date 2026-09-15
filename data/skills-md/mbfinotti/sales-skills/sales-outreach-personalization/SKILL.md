---
name: sales-outreach-personalization
description: Turns prospect signals into 2-3 ranked personalization angles for outreach, each pairing a dated, sourced signal with the problem it implies, a one-line hook, the ask it justifies, and a confidence/recency label. Covers B2B and B2C signals and 1:1 vs 1:few vs 1:many effort tiers, and never invents a signal. Use whenever the user mentions personalization, a trigger event, a funding round, a new hire or job change, a product launch, review mining, or "find a reason to reach out", even without the word personalize. Do NOT use for drafting the message - subject lines (mbfinotti/sales-skills@cold-email-subject-line-tester), openers (mbfinotti/sales-skills@cold-call-opener), and cadence (mbfinotti/sales-skills@sales-outbound-sequence) live elsewhere.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.9"
---

# Outreach Personalization

Turn the signals a user supplies (or can verify) about a prospect into 2-3 concrete personalization angles. An angle is a reason to reach out, not a message: the finished email, subject line, call opener, and touch cadence belong to neighboring skills (see References). The hardest rule here is negative - a fabricated signal is worse than no angle at all, because it destroys trust the moment the prospect checks.

**Scope boundaries.** Never write body copy, subject lines, call scripts, or sequences. A one-line hook is in scope; a drafted paragraph is not.

Hand the chosen angle to:

- `mbfinotti/sales-skills@cold-email-subject-line-tester` for subjects
- `mbfinotti/sales-skills@cold-call-opener` for phone openers
- `mbfinotti/sales-skills@sales-outbound-sequence` for cadence

## Interview

- Ask one question per message, offering multiple-choice options.
- Skip anything context already answers.
- If your harness has persistent memory and a prior run stored this user's answers, confirm instead of re-asking.

1. Who is the prospect: a named person at a company (B2B), or a consumer/segment (B2C)?
2. What do you sell, in one plain sentence, and to whom? Refuse a feature list - one sentence.
3. Which signals do you already have? Offer the taxonomy categories as choices: funding/financial, leadership/role change, hiring, product/launch news, tooling change, their content or talks, community/review activity, mutual connection - or for consumers: purchase, browsing, lifecycle, loyalty events.
4. For each signal: where did it come from, and when? Source and date decide confidence.
5. Target channel: email, phone, social DM, or (B2C) a triggered lifecycle message? Take the answer as given - this skill deliberately does not rank channels against each other, because channel and touch mix are the cadence sibling's call and a second ordering here would contradict it.
6. Account tier: 1:1 strategic account, 1:few segment, or 1:many volume?
7. By when must this land - this week, this quarter, or no fixed date?
8. One-off win on this prospect, or a compounding asset you will reuse across the whole segment?
9. Effort ceiling: how many minutes per prospect, and can you spend someone else's time (a mutual connection's intro, a colleague's sign-off)?
10. Any known consent or suppression constraints on this prospect or list?

Answers 7-9 re-order everything below them, so ask them before proposing an angle, not after. See Ranking the signals you have for which answer moves which option.

## Anatomy of an angle

Every angle ships with all five parts. A missing part means the angle is not done.

- **Signal**: the observed fact, with its source and date. Paraphrase what was actually seen; quote sparingly.
- **Inference**: "therefore this person likely faces X right now." One sentence, hedged in proportion to the evidence.
- **Hook**: one line the user can drop into their own message, referencing the signal in plain speech.
- **Ask it justifies**: the specific next step this angle earns. A hiring surge justifies a different ask than a champion changing jobs.
- **Label**: confidence (verified / single-source / user-asserted / inferred) plus recency (days or weeks since the signal).

## Signal taxonomy

Classify every supplied signal into one category before ranking; category determines the typical inference and freshness window. When you are choosing what to go looking for - rather than sorting what you were handed - work the categories in efficiency order: replies bought per minute of sourcing, not raw signal strength.

- **Efficiency**: hiring == leadership change > product and launch news > community and review activity > tooling change > public content and speaking > funding and financial
- **Effort** (minutes to source, tool access you must work around the absence of, and whose attention it spends): community and review monitoring (a standing job to watch the venues buyers post in) > mutual connection activated (an hour, and it spends someone else's calendar) == flagship talk watched end to end (an hour) == tooling change without a detection service (an hour of guessing; near-zero with one) == funding round qualified down to what it actually funds (an hour) > hiring == leadership change == product/launch == a single post (near-zero - one dated lookup on a page the account publishes about itself)
- **Value** (positive replies and meetings): community and review activity == relationship and mutual connection > leadership change > hiring == tooling change > public content > product and launch news > funding and financial
- **Compliance cost** (the review it triggers and what it costs to reverse): B2C behavioural signals (a marketing-consent check before every send; an unwanted send cannot be unsent) > community and review activity (a venue-norm judgement - a public post turned into an uninvited DM costs standing on the platform and with the buyer) > everything on the public professional record (near-zero)

**Ties, and why they are real ties:**

- Hiring and leadership change: both are one dated lookup on a page the account publishes about itself, and both imply the same class of problem - a team changing shape - so neither buys more per minute.
- Community activity and a mutual connection: equal on value because both replace your inference with something the prospect, or someone they trust, has already said.
- The three "an hour" items: equal because an hour is the smallest magnitude worth asserting; a finer ordering between them would be invented.

Default: run hiring and leadership change on every account - one lookup each, live on most accounts. Promote community and review activity as soon as you know the venue your buyers actually post in; that standing cost is paid once for the whole segment, never per prospect.

What this order starves: the **mutual-connection angle**, the highest-value signal here and the only one whose cost lands on someone else's calendar, so it loses every efficiency round.

Promote it anyway when:

- The account is named and strategic.
- The deal is big enough that one warm intro outruns a quarter of cold touches.
- A cold attempt on that prospect has already failed.

Deleted, not demoted: **third-party-sourced consumer behavioural data**. B2C angles run on first-party data and the marketing consent attached to it, so purchased or scraped consumer signals never enter this ranking - do not park them at the bottom as a fallback.

This order is a default, not a law: it shifts with the segment and with who executes it. Re-rank it against what you already know about the user.

- A technology-detection or funding database already licensed drops those two categories to near-zero effort and promotes them.
- A named list of thirty accounts makes the mutual-connection angle affordable.
- An SDR with a daily dial quota cannot carry a standing monitoring cost at all - drop community activity out of their order entirely.

**B2B categories:**

- Hiring and job postings
- Leadership and role changes
- Product and launch news
- Community and review activity
- Technology and tooling changes
- Public content and speaking
- Relationship and mutual-connection signals
- Funding and financial events

**B2C categories:**

- Purchase behaviour
- Lifecycle stage
- Browsing and engagement
- Loyalty and advocacy

Full category-by-category detail (what to look for, where each surfaces, what it costs to source, what it usually implies, how fast it goes stale) lives in [references/signal-taxonomy.md](references/signal-taxonomy.md).

## The relevance test

Run every candidate signal through the **"so what?" test** - Armand Farrokh's second of his "4 Questions" at 30 Minutes to President's Club (30MPC). Read the fact from the prospect's seat and ask: "so what does that mean for me?"

- **Pass**: the honest answer names a problem or opportunity the user's offer addresses.
- **Fail**: the answer is "nothing" - the fact is merely interesting. "You went to X university" and a bare "congrats on the round" both fail.

Companion principle, also from 30MPC: personalization must be attached to the problem. An observation that does not lead into the reason for reaching out is decoration, not an angle.

Discard failures. Record them in the output's Discarded list with a one-line reason, so the user sees the work.

## Ranking the signals you have

The efficiency order in Signal taxonomy governs the search - what to go looking for with the minutes you have. This rubric governs the shortlist - which of the signals already in hand get shipped. Sourcing cost is spent by the time a signal reaches this stage, so the only cost left to weigh is what the angle costs to act on.

Score every signal that survived the relevance test, 0-2 on each axis:

- **Recency**: this month beats this quarter beats this year. Always note the date; an undated signal caps at 1.
- **Specificity**: a concrete, dated action by this person or account beats a trend about their industry or role.
- **Connection**: how directly the inferred problem maps to what the user actually sells.
- **Cost to act**: 2 when the angle is yours to send today; 1 when it needs a tool, a data pull, or a verification round trip; 0 when it spends someone else's time or needs a consent check first.

Use the total to cut, never to order. A 7 and a 6 are not a real difference, and ranking two survivors against each other by score is false precision - the reply decides that. Keep the top 2-3, and output fewer rather than pad: two strong angles beat two strong plus one filler.

Re-rank against the interview answers, and name which answer moved what:

- A hard date promotes the near-zero categories and the 1:few tier, and demotes anything costing a standing job or another person's calendar.
- A compounding-asset mandate promotes exactly those slow options: a monitored venue and a documented trigger stack are paid once and reused on every prospect after.
- A low effort ceiling deletes the 1:1 tier for this run rather than demoting it - say so out loud, and template instead.

**Tie-breakers:**

- Match signal altitude to seniority - Jason Bay's rule, published via 30MPC: executives respond to company-level, strategic signals; managers respond to personal and team-level context.
- Apply "First is Best" (30MPC / Jason Bay) at scale: pre-rank the segment's likeliest trigger types, then use the first one research actually confirms instead of digging indefinitely for a "better" one.

## Anti-fabrication rule

This is the load-bearing guard. Everything else in this skill is negotiable against context; this is not.

- Never invent a signal, a date, a quote, a name, or a detail. No exceptions, including "plausible" ones.
- Cite source and date for every signal. Write "date unavailable" rather than guessing a date.
- Mark every inference as inference. Never promote a guess into an observed fact.
- Thin evidence: say so, and output one angle - or zero, plus the shortest list of what would unlock one (a recent event, a piece of their content, a prior interaction). Ask the user; never fill the gap.
- Never build an angle on special-category or sensitive personal data - health, financial hardship, religion, politics, sexuality - even when a public post reveals it.

## Effort tiering

Decide the tier in the interview; it sets how much research time each prospect gets and the depth of angle to aim for.

- **Efficiency** (meetings booked per hour of research): 1:few > 1:many > 1:1
- **Effort**: 1:1 (an hour per account, every account, every time) > 1:few (a week of segment research once, then near-zero per prospect) == 1:many (that same one-time pass, plus a standing job to keep B2C trigger data live)
- **Value** (per prospect reached): 1:1 > 1:few > 1:many

1:few and 1:many tie on effort because the expensive part of both is the same one-time segment pass; what separates them is where the payoff lands, not what they cost.

Ranked, best ratio first:

- **1:few**: a segment of similar prospects. One shared inference per segment, plus one light per-prospect variable (their specific role, post, or event). The default rung.
- **1:many**: volume outreach or B2C lifecycle. Personalize at segment/persona level: Jeb Blount's "because statement" (Sales Gravy, with Chris Beall) - one researched, pattern-based reason-for-contact sentence serving the whole list.
- **1:1 deep-dive**: named strategic accounts, high deal value. Individual-level signals; verify each one at its source; all five anatomy parts bespoke.

Move up to 1:1 when the account list is short and named and one meeting repays a day of research. What moves you down to 1:many is the templating rule at the end of this section.

What this order starves: **1:1 deep-dive** - the highest value per prospect and the highest effort, so it loses every efficiency round and a rep who only ever computes ratios never runs it.

Promote it anyway for:

- A named strategic account.
- A multi-stakeholder deal.
- A prospect a templated tier has already failed on.

The ROI test in [references/effort-tiering-and-benchmarks.md](references/effort-tiering-and-benchmarks.md) (meetings booked per hour of research, by tier) tells you afterwards which way you were wrong.

This ranking is a default, not a law; it shifts with the segment and with who executes it. Re-rank it against the user's own position:

- An already-licensed enrichment or intent platform makes 1:few cheaper still.
- A thirty-account named list makes 1:1 affordable.
- An SDR against a daily activity quota is effectively capped at 1:many whatever the deal size says.

Researched calibration, attributed honestly:

- Jeb Blount (Sales Gravy) caps first-touch research at 2-3 minutes per prospect; beyond that, research becomes procrastination dressed as diligence.
- 30MPC: with a segment's triggers pre-documented, a personalized email takes under 3 minutes. Their editorial rule: "Personalize the ones that matter. Template the rest."
- Kyle Coleman's 5x5x5 method, published by Lavender (a vendor): 5 minutes research plus 5 minutes writing, roughly 30 personalized emails a day. Vendor-published - treat as directional.
- Gong (vendor-published, its own platform data): the average rep sends ~344 cold emails per booked meeting. Personalization lift claims range from 50-250% (Lavender, citing Salesloft - vendor-published) up to 5x (Gong data, cited by 30MPC). The direction is consistent across sources; the magnitudes are marketing.

Templating is the correct answer, not a compromise, when:

- Deal or customer value is low.
- The segment is large and uniform.
- A time-capped search finds no fresh individual signal.
- The motion is B2C lifecycle at scale.

See [references/effort-tiering-and-benchmarks.md](references/effort-tiering-and-benchmarks.md) for tier definitions and the full benchmark attribution table.

## B2B and B2C

The angle anatomy, the so-what test, the 0-2 scoring rubric, and the anti-fabrication rule are identical for B2B and B2C - apply them unchanged. The category efficiency order is not: B2C runs on its own order (see references/signal-taxonomy.md), because every one of its categories carries the same consent cost and the ordering falls to timing instead.

The regimes diverge on four points:

- **Consent basis**: B2B angles lean on public professional activity. B2C behavioural data (purchases, browsing, lifecycle events) exists only inside a direct customer relationship and the marketing consent attached to it. Never mine a stranger's personal posts to personalize consumer outreach.
- **Signal sources**: B2B reads the public professional record: company news, careers pages, professional profiles, talks, reviews. B2C reads first-party data the business already holds: purchase history, on-site behaviour, lifecycle stage, loyalty activity.
- **Channel and cadence**: a B2B angle ships as an individually sent message. A B2C angle usually ships as an automated triggered flow (abandoned cart, replenishment window, milestone): the angle becomes a segment trigger plus a message variant, not a hand-written line.
- **Scale**: B2C is 1:many by default. "Personalization" there means the right trigger, timing, and dynamic fields - not per-person research.

## Workflow

1. Run the Interview. Confirm prospect, offer, signals with sources and dates, channel, and tier before anything else.
2. Inventory the supplied signals. If you can browse the web, verify each volatile fact (date, role, event, wording) at its source; otherwise label unverified items "user-asserted" and proceed.
3. Optional integration note: if your environment connects to a data-enrichment, intent, or CRM platform (for example a funding database or a professional-network sales tool), pull additional signals from it - never as a substitute for verification.
4. Classify each signal using [references/signal-taxonomy.md](references/signal-taxonomy.md).
5. Apply the so-what test. Discard failures with a one-line reason each.
6. Score survivors on the rubric in Ranking the signals you have. Keep the top 2-3 - or fewer, per the anti-fabrication rule.
7. Write each angle in the five-part anatomy. Hedge inference language to match the confidence label.
8. Run the hook lines through your preferred humanizer skill. A hook that reads templated defeats its own purpose; raw first-draft output is never final.
9. Run the Self-check gate below. Iterate until every shipped angle passes.
10. Deliver the output shape below, including the Discarded list, and hand off to the drafting sibling for the chosen channel.
11. If your harness has persistent memory, record the segment's stack-ranked trigger list and which angles won replies - later runs skip straight to ranking.

## Expected output

```
## Angles for [prospect / segment]

### Angle 1 - [signal category]
- Signal: [fact] ([source], [date])
- Inference: [therefore they likely face X right now]
- Hook: "[one line in plain speech]"
- Ask it justifies: [specific next step]
- Label: [confidence] / [recency]

### Angle 2 - ...
(2-3 angles total; fewer if evidence is thin - say why)

### Discarded
- [signal] - [failed so-what / stale / no connection to offer]

### Next step
Hand the chosen angle to [cold-email-subject-line-tester | cold-call-opener | sales-outbound-sequence].
```

Filled good and bad examples - including the tempting-but-wrong ones - live in [references/angle-examples.md](references/angle-examples.md).

## Self-check gate and KPIs

Gate before returning output. Every shipped angle must:

- Cite a real, dated signal (or a verified source plus "date unavailable").
- Pass the so-what test.
- Fail the swap test: it could not be sent verbatim to a different prospect.
- Hedge its inference to match its confidence label.
- Carry a hook that survived the humanizer pass.

Iterate until all pass. Fewer angles beats a failing third.

Field KPIs, once angles ship:

- Reply rate and positive-reply rate on personalized sends versus a control template.
- Meeting-booked rate (B2B).
- Triggered-flow click and conversion versus a generic blast (B2C).

Judge angles on positive replies and meetings, never opens - privacy proxies inflate opens.

## Failure modes

- **Fake compliment as an angle** ("love what you're building!"): no signal, no inference - discard.
- **Funding congratulations with no consequence attached**: the round alone fails so-what; the pressure it creates is the angle.
- **"Saw you went to X university."**: personal trivia disconnected from the problem; practitioners flag it as the canonical bad opener.
- **Stale signal presented as fresh**: a 9-month-old post reads as scraped; date every signal and let recency scoring demote it.
- **Over-researching low-value accounts**: Jeb Blount's warning, research past the 2-3 minute cap is procrastination - drop the account to a templated tier instead.
- **Obviously AI-generated pseudo-personalization**: templated phrasing around a merge field. The humanizer pass and swap test exist for this.
- **Creepy over-familiarity**: quoting deep personal detail or non-public data. Reference only what they made public or gave the business directly.
- **Padding to three**: two real angles plus one filler reads weaker than two real angles.
- **Signal dump**: ranked shortlist of 2-3, never an inventory of everything found.

## Compliance note

General practice, not legal advice - this skill asserts no legal conclusions; verify against primary sources with your own counsel.

- Honor opt-outs, do-not-contact requests, and suppression lists before any send; keep a working unsubscribe path on email.
- Reference only data the prospect made public or gave the business directly - never data they would be surprised you hold.
- Never use special-category or sensitive personal data as an angle (see Anti-fabrication rule).
- Regimes to check for your jurisdictions and channels: GDPR/ePrivacy (EU/UK), CAN-SPAM (US), CASL (Canada), CCPA/CPRA (California). Their consent and opt-out rules differ materially.

This list is unranked on purpose - which one binds is decided by where the prospect sits, not by which is cheapest to satisfy, so ordering them would be false precision.

## References

- `mbfinotti/sales-skills@sales-discovery-questions` - what to ask once an angle earns the meeting.
- [references/signal-taxonomy.md](references/signal-taxonomy.md) - B2B and B2C signal categories: sources, typical inferences, freshness windows, interpretation principles.
- [references/angle-examples.md](references/angle-examples.md) - filled good and bad angle examples in the output format.
- [references/effort-tiering-and-benchmarks.md](references/effort-tiering-and-benchmarks.md) - tier definitions, when templating wins, benchmark table with attributions.
