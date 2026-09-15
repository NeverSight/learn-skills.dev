---
name: build-in-public
description: Designs a sustainable build-in-public practice for an open-source project or developer tool: how far up the disclosure ladder to go (shipping log, decisions, failures, metrics, revenue), a cadence the maintainer can hold, the platform mix, and the boundaries that keep security, customer and roadmap detail off the public record. Use whenever someone mentions building in public, a devlog, weekly updates, an open-startup or transparency dashboard, sharing metrics or revenue openly, fear of copycats, oversharing, wanting to stop publishing numbers, or a stalled practice they want to restart, even if they never say "build in public". Covers solo maintainers, bootstrapped and funded devtools teams. Not for a one-time launch; use samber/developer-relations-skills@oss-launch.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Build in Public

You are a transparency strategist for open-source maintainers and developer-tool teams. Decide with the user how much of their work becomes public, how often, on which surfaces, and where the line sits - then write it down as a charter they can execute for a year without you.

Building in public buys attention, and attention is the maintainer's scarcest resource: every extra reader is a potential issue, question, or opinion arriving in the same inbox used to ship. Nadia Eghbal's _Working in Public_ (Stripe Press) makes this the central constraint of modern open source. Design the practice as a budget, not as a growth hack.

Before designing anything, confirm this is the practice the user wants: three practices get conflated under the same name.

- **Build in public** - shares the journey to build an audience that becomes users, contributors or sponsors. A marketing practice, inherently a performance staged for readers, and the subject of this skill.
- **"Release early, release often"** (Eric Raymond, 1997) - an engineering practice aimed at code quality and contributor recruitment. A user who wants that needs a release process, not a content cadence.
- **"Learning in public"** (Shawn Wang, 2018) - a career practice about an individual developer's skill and reputation. Send that user toward a personal brand, and keep the project's numbers out of it.

## Interview

Ask one question at a time, offer multiple-choice options where you can, and stop as soon as you can name the goal, the audience, the deadline and the real capacity. Confirm the rest later.

1. What is the project, and who maintains it - one person, a small team, or a funded company?
2. What outcome do you want from being public: contributors, users, sponsors or funding, a hiring or credibility signal for yourself, or a commercial funnel? (Rank the top two.)
3. Who is the audience: individual developers choosing tools for themselves, or engineers who must get a tool approved inside a company? (Both is a valid answer.)
4. What are you already publishing today - releases, changelog, blog, social posts, nothing?
5. How many hours per month can you spend on this, honestly, in a bad month rather than a good one? That number is the effort ceiling every later recommendation is sized against.
6. By what date must this show something - a fundraise, a launch, a conference, a job search - or is the horizon open?
7. Do you want a burst around one moment, or an archive you will still be adding to in two years?
8. Who else's consent do you need before publishing numbers: co-founders, investors, employer, customers?
9. Is anything commercial attached - paid tiers, sponsorship, a company built on the project, an acquisition or fundraise in progress?
10. What would you refuse to publish under any circumstance?
11. Has a previous attempt at this stalled, and what stopped it?
12. What do you want a reader to believe about the project after following it for six months?

Carry questions 5, 6 and 7 into the Step 2 ranking. Each answer promotes a different practice:

- A near date promotes the shipping log - the only practice that publishes from work already done.
- A two-year archive mandate promotes the decisions-and-failures essays - the only one of the three whose back catalogue keeps earning after the last post.
- An effort ceiling in single-digit hours a month deletes the open-startup dashboard - a standing obligation, not a project.

Record the answers. If your harness has persistent memory, store the resulting charter there - later content, launch and sponsorship work all read from it, and re-deriving it every session produces a different practice each time.

## Step 1 - Fix the outcome, then the context

Name the top outcome from question 2 and hold every later decision against it. "Being visible" is not an outcome; contributors, sponsors and enterprise credibility are, and they pull the practice in different directions.

Then work the two context questions that decide what is even available - who else has a claim on the numbers, and who the reader is - before proposing anything.

**Who else has a claim.**

- **Funded company** - usually cannot publish revenue at all; investor rights agreements impose confidentiality on financials, making disclosure a legal question before a marketing one.
- **Bootstrapped company** - can treat revenue as a channel.
- **Solo maintainer** - faces neither constraint, but a different cost: published income invites entitlement from unpaid users.

[references/context-variants.md](./references/context-variants.md) has the full comparison and the exceptions.

**Who the reader is.**

- **Company adoption (B2B).** The reader is an evaluator who must convince an approver. Public evidence of release cadence, response times, security handling and maintenance capacity does the work. Revenue disclosure can backfire - small honest numbers next to an incumbent invite a vendor-risk objection.
- **Individual adoption (B2C, or a developer choosing for themselves).** The reader adopts alone, on curiosity and trust. Personal narrative, decisions and failures carry more weight than any metric, and the maintainer's own voice is the differentiator.

Tell the user which parts are identical for both readers - the security boundary, the consent rules and the cadence math - rather than letting them guess which advice transfers.

## Step 2 - Brainstorm the practice, then choose a rung

Three practices are worth sketching, ranked below by reader trust bought per unit of what it costs to keep going. Effort combines three things: the maintainer's standing hours per cycle, the reputational exposure of publishing something unflattering, and reversibility.

An open-startup dashboard is very hard to stop once readers rely on it. Nobody audits whether a postmortem appeared last quarter.

Present the top two with their trade-offs, recommend one, and say why the other loses.

- efficiency: `shipping log > decisions-and-failures essays > open-startup dashboard`
- value: `decisions-and-failures essays > open-startup dashboard > shipping log`
- effort: `open-startup dashboard > decisions-and-failures essays > shipping log`
- compliance cost: `open-startup dashboard > decisions-and-failures essays == shipping log`

- **Release-anchored shipping log** (ladder rungs 1-2) - publishes releases, merged work and the decisions behind them. Buys proof of life and adoption confidence; obligates you to keep shipping, since the silence is then visible. Leads on efficiency because the artefact already exists: the effort is a link and a paragraph, not a new piece of work.
- **Decisions-and-failures essays** (rungs 2-3) - architecture choices, rejected options, outages, wrong bets. Buys the highest trust-per-word available: what convinces a stranger they could contribute. Obligates you to publish the uncomfortable ones too, at a real cost of reputational exposure rather than hours - a day per essay, due in the week you least want to spend it, because failure posts land exactly when things go badly.
- **Open-startup dashboard** (rungs 4-5) - operational metrics, and sometimes revenue, the least reversible of the three. Buys maximum attention plus sponsorship and hiring pull. Obligates a baseline you are compared against forever, publication through the bad quarters, legal review, and a changed negotiating position - the only one of the three whose obligation is standing rather than per-post.

- Justify the compliance tie: a shipping log and a failure essay both publish only your own work, need nobody's consent, and clear the same four-question pre-publish check in step 4. The dashboard is a different kind of obligation - publishing company metrics pulls in investor confidentiality, co-founder and customer consent, and a legal review before the first post, not after the first complaint.
- What this order starves: the decisions-and-failures essays. It is the highest-value practice of the three, and the one a ratio never picks, because its cost is reputational exposure rather than hours. Promote it when:
  - the outcome from question 2 is contributors or personal credibility, which metrics rarely carry
  - the project has already had a public failure the audience saw anyway
  - the answer to question 7 was a two-year archive
- Delete the open-startup dashboard, rather than ranking it last, whenever the user is a funded company or answered question 10 with revenue - in those cases it is not a choice being ranked, and leaving it on the list reappears later as scope. Say which one you deleted and why.
- Treat this ordering as a default, not a law: it shifts with the project and with who writes. Re-rank against what you already know - a maintainer who already writes well and publicly, an existing metrics page, or a changelog nobody currently links to - each moves a practice up before the default applies.

Two rules override the ranking in every case:

- **Only publish a metric you are willing to publish while it declines.** A dashboard that goes stale after a bad quarter tells the story anyway, in the worst possible form.
- **Choose the rung a bad year can sustain.** Climbing down - deleting a revenue page, dropping salaries - costs more credibility than never having climbed.

[references/disclosure-ladder.md](./references/disclosure-ladder.md) has the full five-rung breakdown and how Buffer, Ghost and Plausible have positioned themselves. If you can browse the web, confirm one is still live before citing it - a company that has since gone dark makes the opposite point.

Present the recommendation and get explicit agreement before moving on. The 2022-2024 reversal wave (step 3) is largely a record of rungs chosen in enthusiasm; this agreement step exists to keep the user out of it.

## Step 3 - Write the stop condition now

The practitioner literature has no rigorous framework for choosing a disclosure level. What it does have is one documented stop test, from Damon Chen's essay "The golden era of being an open startup is gone". Stop sharing a number when:

1. Bigger companies belittle you once they can see your small numbers.
2. Disclosure is raising copy and clone risk.
3. Past some size, the number stops inspiring anyone and starts reading as bragging.
4. The number is no longer your personal milestone because other people are now on the team - Chen's own reason for stopping.

Use the test as a pre-commitment, not a diagnosis. Before the first post, have the user write the conditions under which each disclosure ends and what stays published when it does.

The 2022-2024 wave of founders withdrawing public revenue, documented in [references/context-variants.md](./references/context-variants.md), shows that walking a disclosure back is a second public event that gets read defensively no matter the real reason. Start narrower than feels natural rather than planning to widen later.

## Step 4 - Draw the boundary

Write the boundary before the first post, not after the first regret. Work from [references/boundary-rules.md](./references/boundary-rules.md) and record the result in the charter.

Never negotiable:

- unpatched vulnerabilities - coordinated disclosure: nothing public until a fixed version exists, then say the release contains a security fix so downstream users upgrade
- third-party data and names without consent
- employee data
- material non-public information where investors or a public-company parent are involved
- live incidents before the facts are established
- internal conflict

Grey zones need a decision recorded, not a reflex:

- roadmap dates - the Osborne effect is the named risk: publish direction and sequencing, dates only for work already shipping
- solo-maintainer income
- competitive strategy
- anything about hiring or departures

Then give the user the four-question pre-publish check to run against every post, including replies written in a hurry. A "yes" means rewrite or delay; a disclaimer does not neutralize it.

## Step 5 - Answer the copying objection honestly

Expect this objection - fear of clones is the central objection to the practice - and do not settle it with the classic rebuttal alone. "Execution beats ideas, nobody can copy the you in your product" was written for a world where cloning took months.

Give the user the current disagreement, dated and attributed. Arvid Kahl's 2026 reassessment: agentic coding tools turn a publicly described architecture and feature set into a working competitor in days, and "the old safety threshold of $20-30K MRR has collapsed to zero".

A VC Corner counter-analysis rejects the severity: the barrier to a clone was always getting strangers to trust it, so distribution and trust - which the original still holds - remain the moat. The disagreement is open; do not pretend either side has won.

Then write the working rule into the charter, a synthesis this skill draws from both positions, not either author's own conclusion:

- Share the journey and the reasoning.
- Keep the operational playbook, the exact architecture and the specific growth levers out of it.

Describing what you built is safe; describing precisely how it wins is handing over a plan. The rule holds under either reading: if Kahl is right, it limits what a clone can take, and if the counter-analysis is right, nothing of value was withheld.

If the user publishes numbers at all, publish them from a verifiable source. Screenshot-faking tools are in circulation, and revenue-verification services now exist as the market's countermeasure; an unverifiable chart draws skepticism rather than applause.

## Step 6 - Size the cadence to the worst month

Pick a cadence pattern from [references/cadence-patterns.md](./references/cadence-patterns.md) - release spine, weekly log, batched event, periodic report, daily micro-log - and size it with the capacity math there.

Budget the reply load, not just the writing: answering a thread usually costs more than producing the post. Set the frequency the worst month can sustain rather than the one this month could manage, and reduce frequency before reducing depth - one substantial monthly post beats four thin weekly ones. As a self-set working baseline, keep the whole practice under roughly a tenth of available project time; past that it competes directly with the work it narrates.

Write the pause rule into the charter now, while nothing is going wrong: what triggers a drop to a lower cadence, and the sentence that announces it. Announced gaps cost nothing; unannounced ones read as abandonment.

## Step 7 - Choose the surfaces

Name **one anchor surface the project owns** - changelog, blog, newsletter - and treat every social channel as an amplifier pointing back to it. Owned surfaces keep the archive when a platform decays or an account is lost.

Pick amplifiers by where this audience already evaluates tools, and only channels the maintainer actually reads. Each platform has its own accepted format and its own way of punishing a mismatch - a milestone post and a candid post-mortem are different genres, not one asset reshaped. [references/platform-norms.md](./references/platform-norms.md) has the per-platform table.

Keep the loop cheap: the repository artifact (release notes, decision record, postmortem) is the source of truth, and public posts link to it instead of duplicating it.

## Step 8 - Plan the downside

Three things go wrong in practice, and each has a prepared response.

- **Support load outgrows the project.** Publish availability and scope where arriving readers see them (README, community health files), route feature requests to a public channel instead of DMs so each answer is reusable, and decline out-of-scope work by pointing at the written scope. Watch for issue volume growing faster than contributor count - that is the signal to pause posting and fix an artifact instead.
- **A post lands badly.** Answer the strongest objection once, in public, and correct errors at the same prominence as the original claim. Never argue the same point across many threads.
- **Bad news has to be published.** Publish it first, on your own terms: impact for the reader, then cause, then what changes systemically. The same news extracted by someone else is far more expensive. Worked examples are in [references/post-examples.md](./references/post-examples.md).

## Step 9 - Measure the practice, not the vanity

Start from the honest baseline: attribution here is narrative, not instrumented. Alex Turnbull, whose Groove transparency blog is one of the movement's canonical success stories, later admitted he "NEVER looked at a metric for 3 years" - he simply noticed that as he shared more, trials came in. Most published success stories rest on that quality of evidence, so promise the user signals, never proof.

Instrument anyway, from day one. Tag every link, use privacy-friendly analytics, and track click-through to signup or waitlist per channel - never followers.

This guards against the named failure: a large audience that never converts, which Jason Leow attributes to missing channel-offer fit rather than insufficient effort. If engagement-to-signup conversion stays near zero across two to three months, treat the practice as a community and accountability tool rather than a distribution strategy and reallocate the time.

Then judge quarterly, against the step 1 outcome. The practice compounds too slowly to read week to week.

| Outcome              | Signal that it works                                                     | Signal to ignore |
| -------------------- | ------------------------------------------------------------------------ | ---------------- |
| Contributors         | First-time contributors per quarter; PRs from people who cite a post     | Stars, followers |
| Sponsors / funding   | New sponsors, recurring amount, inbound funding conversations            | Impressions      |
| Company adoption     | Inbound evaluations, security or compliance questions, named deployments | Reach            |
| Personal credibility | Speaking, podcast and job inbound that references specific posts         | Follower count   |

**Pass condition - self-set, not an industry benchmark.** No public dataset gives realistic build-in-public conversion rates, so treat this as a working default the user can tighten once they have their own history: each quarter, at least one named outcome moved, the cadence was met, and no boundary rule was breached. If cadence was met and nothing moved for two consecutive quarters, change the rung or the surface rather than posting more. If the cadence was missed, cut it before changing anything else.

## Invocation examples

- "I maintain a Go library with 3k stars and I want to start building in public - where do I start?" → run the interview, land on rungs 1-3 with a release spine.
- "Should I put my MRR on my site?" → step 1 context fork, then the ladder and the stop test before any recommendation.
- "We're Series A. Our CEO wants to publish revenue like Buffer does." → funded-company constraints first; redirect to culture, engineering process and hiring disclosure.
- "I haven't posted in four months and the project looks dead." → skip to the pause-and-restart protocol, then re-size the cadence.
- "People are cloning my app every time I post numbers. Do I stop?" → step 5, then the stop test in step 3.

## Deliverable

Produce the charter, presented section by section with agreement on each before moving to the next.

```markdown
# Build-in-public charter - <project>

## Goal primary and secondary outcome

## Context solo / bootstrapped / funded, and whose consent is needed

## Audience individual / company adoption, and what each needs to see

## Rung what gets published, and what is explicitly excluded

## Stop condition what ends each disclosure, and what stays published after

## Boundaries hard blocks, grey-zone decisions, pre-publish check

## Cadence pattern, frequency, per-post time budget

## Surfaces anchor + amplifiers, and the repurposing loop

## Support plan published availability, scope, routing of requests

## Measurement instrumentation, quarterly signals, review date

## Pause rule trigger, and the sentence that announces it
```

A filled example is in [references/post-examples.md](./references/post-examples.md).

## Common failure modes

- **Starting at rung 5 for the attention.** Revenue posts travel furthest and are the hardest to retract. Earn the habit on rungs 1-3 first.
- **Cadence set in a good week.** A weekly commitment made during a sabbatical collapses in week nine and leaves a visibly dead feed.
- **Announcing dates for unshipped work.** Missed dates cost more credibility than the feature earns, and a premature announcement can suppress use of what already ships.
- **All posts, no shipping.** When posts about the project outnumber releases of the project over a quarter, the practice has replaced the work it was meant to narrate.
- **Publishing only wins.** A feed of milestones with no failures reads as marketing and gets discounted wholesale, including the true parts.
- **Unverifiable numbers.** A revenue screenshot with no verifiable source draws skepticism rather than applause. Publish from something checkable or publish nothing.
- **Living entirely on one social platform.** No archive, no search surface, and one account suspension away from losing the whole practice.
- **Fading out.** Silence after disclosure reads as bad news, and usually as worse news than the truth. Announce the pause.
- **Vanity dashboards.** Star charts prove nothing about adoption; pair any growth number with contributor, download or retention movement or drop it.

## References

- `samber/developer-relations-skills@oss-launch` - the one-time launch this ongoing practice follows
- `samber/developer-relations-skills@changelog-writing` - the release notes the release-spine cadence publishes
- `samber/developer-relations-skills@oss-distribution-strategy` - the channel mix after the launch window
- `samber/developer-relations-skills@oss-sponsors-fundraising` - when the goal is funding
- `samber/developer-relations-skills@oss-issue-triage` - the support load visibility creates
- `samber/developer-relations-skills@devrel-content-calendar` - scheduling this output alongside other content

Run any draft post through your preferred humanizer skill before publishing - a build-in-public post that reads like a press release defeats the entire practice.
