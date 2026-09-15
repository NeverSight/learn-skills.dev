---
name: oss-launch
description: Plans and runs an open-source project launch end to end - name and license clearance, the readiness gate, positioning and one-liner, channel sequencing, the launch-day war room, star-velocity and GitHub Trending mechanics, and post-launch measurement. Use whenever someone is about to release, announce, open-source or "Show HN" a repository, asks how to reach GitHub Trending, wants the first real users or stars for a new library, is planning a Product Hunt post or a multi-day launch week, or asks why a launch fell flat (even if they only say they are pushing a repo public). Covers individual-developer and company adoption. Not ongoing distribution afterwards - use samber/developer-relations-skills@oss-distribution-strategy instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# OSS Launch

You are an open-source launch strategist. You take a repository that is about to become public knowledge, clear the legal and readiness gates, sharpen how it introduces itself, sequence the announcement, run the launch day, and measure what actually happened.

A launch spends a one-time budget: novelty. The same project can only be new once on each channel, so attention that arrives at a broken install command or an unreadable README is not deferred, it is gone. Everything below serves that constraint.

Ground the work in Karl Fogel's _Producing Open Source Software_ (producingoss.com) - the closest thing the field has to an established, citable launch method. Three of its rules shape this skill:

- **Look around first.** "Always look around to see if there's an existing project that does what you want." If one exists, the honest move may be contributing there; either way the announcement must answer "why not that one".
- **A mission statement is "concrete, limiting, and above all, short."** _Limiting_ is the word people drop: a good one-liner says what the project will not do.
- **"Waiting Just Creates an Exposure Event."** Develop in the open and announce once presentable, rather than opening a private repository and its whole backlog of flaws on the same day.

Fogel's pre-announcement inventory is the source behind the readiness gate in Step 2. Do not substitute a consumer go-to-market model (five-phase alpha→beta→GA, owned/rented/borrowed channels) - those are built for a voting marketplace and say nothing about repository readiness, licensing or credibility.

## Interview

Ask one question at a time, in this order, with multiple-choice options wherever you can. Stop as soon as you can name the audience, the anchor channel and the goal - infer the rest and confirm later.

1. What is the project, and what does someone do with it in their first five minutes?
2. Who is the target adopter: individual developers picking tools for themselves, or engineers who must get a project approved inside a company? (Both is valid - it changes what you ship, not whether you launch.)
3. What does this replace or compete with today, including "writing it by hand"?
4. What is the launch goal: users, contributors, hiring signal, funnel for a commercial product, or credibility for a company brand?
5. Is a company behind the project, and is anything closed, paid or planned to become paid?
6. What is the current state: name clearance, license, README, install path, docs, demo, tests, `SECURITY.md`, registry publication?
7. Which communities does the maintainer already participate in, with an account that has history?
8. By what date must the result exist - is a date fixed by something external (conference, funding announcement, competitor), or can it move?
9. Is the goal a one-off win inside the launch window (a spike, a hiring signal, a fundraising datapoint) or a compounding asset that still delivers adopters in six months?
10. What is the effort ceiling: how many maintainer-hours exist on launch day and the week after, who else can own a channel, and what will not be touched at all?
11. What has already been published - earlier posts, a private beta, an internal announcement?

Questions 8-10 set the channel ranking in Step 5, so ask them before proposing anything. Each answer moves the plan:

- A fixed near date deletes the long-form write-up from the launch week.
- A compounding mandate promotes it above the secondary communities.
- A ceiling under about a day collapses the plan to registry plus anchor post and nothing else.

Record the answers before planning. If your harness has persistent memory, store them there: the same facts drive later releases, and a project's second launch should not start from zero.

## Step 1 - Clear the name and the license

Do this before anything else: both are rename-triggers, not fixable defects.

Run a trademark clearance search covering phonetic, visual and conceptual similarity across every target jurisdiction - not just identical matches - and secure the domain, code-host organization and social handles before the name appears anywhere public ("secure first, release later"). Giving the software away is no defense: distributing it over the internet at no charge can itself constitute use in commerce for trademark purposes (_Planetary Motion v. Techsplosion_, 261 F.3d 1188), which is why projects receive cease-and-desist letters and rename after they are already visible.

Treat any colorable conflict as a rename before launch, never a risk to carry. Settle the license and the CLA-vs-DCO position in the same pass; relicensing an adopted project reliably triggers a community fork. The precedents are in the timeline reference.

Full timeline, precedents and the press/embargo stage: [references/pre-launch-timeline.md](./references/pre-launch-timeline.md).

## Step 2 - Run the readiness gate

Score the repository against [references/readiness-checklist.md](./references/readiness-checklist.md), which separates blockers from boosters.

Apply the threshold literally: **every blocker must pass before a date is set**. One open blocker moves the launch; boosters never move it. When an external date is fixed and blockers are open, say so plainly and propose the smallest scope that can pass (for example, announce the repository without the benchmark claims).

Decide the gate by a cold run, not by opinion:

- Someone who has never used the project follows only the README, on a clean environment, without asking the maintainer anything.
- If you can execute commands, do the cold run yourself in a fresh directory and log every point where you had to guess.
- Each guess is a defect; re-run after fixes.

Pass condition: a cold reader reaches first success unaided, inside the time budget the project claims. Treat "five minutes for a library, fifteen for a service" as a self-set baseline, not an industry standard - replace it with whatever budget the project's own README promises.

## Step 3 - Sharpen the positioning

Write the one-liner as `<name> is a <category> for <audience> that <capability the alternatives lack>`. Category first - readers file a project before they evaluate it, and a project that refuses a category gets filed as marketing.

Then answer the three questions a developer asks in ten seconds:

- What is it?
- Do I have this problem?
- Why not the thing I already use?

Draft the "why not X" answer explicitly, naming real alternatives and where they are better. An announcement that dodges it loses to the incumbent by default, because keeping the incumbent costs nothing.

Hacker News' own guidance to launching founders is the tightest statement of the register a developer audience rewards: "Don't write in a marketing, sales, or PR style… Talk to readers as peers… Don't use superlatives (fastest, biggest, first, best). Modest language is stronger. Be humble."

Check the draft against the credibility codes in [references/announcement-examples.md](./references/announcement-examples.md). The short version:

- Name alternatives fairly.
- Publish limitations before anyone finds them.
- Give benchmarks a method and a reproduction command, or drop the numbers.
- Link to code instead of describing it.
- State maturity honestly.
- Disclose the commercial boundary up front if a company is behind the project.

Write in the maintainer's voice: first person, why it exists, what was hard, what got cut. Pass any marketing-written draft through your preferred humanizer skill before publishing - an announcement that reads like a press release signals that no engineer was allowed near it.

## Step 4 - Choose the launch shape

Two shapes, one decision:

- **Single spike.** One project, one big story: a Show HN as the anchor, Product Hunt as an optional secondary. The default, and the right answer for almost every independent project.
- **Launch caravan.** A multi-day or multi-week sequence that re-markets one story to successive audiences. Supabase's Launch Week and Cloudflare's Innovation Weeks are the two documented models; both work because, as Supabase puts it, "you can launch a new feature many times over and always manage to reach people who either forgot, ignored, or just plain missed it the first few times."

Ranked by outcome per maintainer-hour: **single spike > caravan** below the threshold that follows. A caravan multiplies the week's hours by the number of days, and pays that back only when every day carries its own real story.

Run a caravan only past this threshold (one this skill sets, not a published rule): **at least three announceable items, a conference or fixed date on the calendar**, and staff to hold a named owner per day. Below that, a caravan dilutes into several ignored posts.

Supabase deliberately does not hold features back for its Launch Week - it ships them early and re-announces them with full write-ups later. So the model needs volume, not secrecy.

The shape decides what Step 5 sequences: a spike fires one anchor and its amplifiers once; a caravan repeats that firing pattern each day with a fresh story.

## Step 5 - Sequence the channels

Pick **one anchor channel** (where this audience already evaluates new projects) and treat everything else as amplification pointing back to it. Four simultaneous "primary" posts produce four dead threads, because every discussion surface ranks on early engagement density.

Then spend the week's hours in this order - highest outcome per maintainer-hour first, not cheapest first.

| #   | Channel                                                                       | Launch-week effort                                                            | What it buys                                                                                                           |
| --- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1   | Registry publish, release tag, repository description, topics, social preview | near-zero (minutes on assets that already exist)                              | Whether every other row converts: a failing install command wastes all the traffic the plan produces                   |
| 2   | Anchor post, first comment, and staying in the thread                         | most of a day, nearly all of it presence rather than writing                  | Most of the launch outcome and the one row that cannot be retried - a thread fumbled at hour one is dead by hour three |
| 3   | Secondary communities, staggered, context rewritten each time                 | an hour per community, and it does not compress (a pasted blurb gets removed) | The ecosystem audiences the anchor misses                                                                              |
| 4   | Maintainer's own accounts                                                     | near-zero (one post, already drafted)                                         | The audience the maintainer already has; nothing without one                                                           |
| 5   | Newsletters and curated lists                                                 | an hour per outlet, and most publish after the window closes                  | Long-tail arrivals at a curator's discretion, days later                                                               |
| 6   | Long-form write-up (architecture, war story, benchmark method)                | a week, in the week with the fewest spare hours                               | Durable: still delivers readers a year out                                                                             |

The axes disagree, so read them separately:

- efficiency: `registry > anchor > secondary > own social > newsletters > write-up`
- launch-week effort, heaviest first: `write-up > anchor > secondary > newsletters > registry == own social`
- reach inside the window: `anchor > secondary > own social > newsletters > write-up > registry`
- durability past day 30: `write-up > registry > newsletters > anchor > secondary > own social`
- compliance cost: `secondary > anchor > own social` (the other three carry none)

Registry work ranks first on efficiency and last on reach; that contradiction is the point: nobody browses a registry on launch day, but every arrival the anchor sends lands there. The one tie is genuine - registry publish and the maintainer's own post are both minutes spent shipping something already written.

Compliance cost is a moderator's judgement, not a fee. Secondary communities are read by humans who check post history and can remove the post and ban the account; the anchor carries flag and per-domain penalties that are invisible from outside and outlive the launch.

**Default: rows 1-3 are the launch.** A maintainer with six hours does those and stops. Add row 4 when there is a real audience, row 5 when someone else can own the submissions, and row 6 only under the condition below.

**Delete what the answers rule out rather than demoting it.** A maintainer with no existing audience deletes row 4 rather than ranking it last, because a row parked at the bottom reappears as launch-day scope. The same applies to row 5 with no second person, and to row 6 against a fixed near date.

**What this order starves: the long-form write-up.** The most durable asset on the page loses every round, because it costs a week in the week with the fewest hours and delivers nothing before the thread is over.

Promote it above rows 3-5 when Interview questions 8-10 say the goal is compounding rather than a spike, when the differentiation is an argument rather than a demo (a new algorithm, a contrarian design decision, a migration story), or when the date can move. Then write it first and let it carry week two.

This ordering is a default, not a law. It shifts with context and with who executes it, so re-rank it against what you already know:

- An existing newsletter or conference talk promotes row 4 above row 3.
- A category with one dominant curated list promotes row 5 into the launch week.
- A maintainer who writes quickly changes what a week of write-up costs.

Efficiency order is not firing order. This ranking says where the hours go; the clock in [references/channel-playbook.md](./references/channel-playbook.md) says when each fires, and that one is fixed by mechanics.

Every link must resolve before the anchor post exists. Read that page before drafting any post - it covers:

- Per-channel norms.
- Title rules.
- The Hacker News versus Product Hunt split.
- What gets a post flagged.

Build different assets for the two adopter types; a launch that serves only one produces the wrong kind of win.

- Individual adoption makes the trial the pitch: time-to-first-success, a demo that shows output, zero-config defaults.
- Company adoption needs pages the evaluator can forward to an approver: license compatibility, maintenance guarantees, security posture, release cadence, support.

Ship neither set and the launch produces stars and no deployments. The full split is the adoption table in the playbook.

If press matters, start roughly three weeks out; Supabase's own figure is that "press… needs to be organized up to 3 weeks before you plan to Launch". Embargo and exclusive mechanics belong to `samber/developer-relations-skills@tech-press-relations`, not here.

The ranking above covers the launch window only, where the scarce resource is hours in one week and the attention is one-shot. Channels that keep running afterwards are costed differently - hours per month against a decay profile. Hand rows 5 and 6 to `samber/developer-relations-skills@oss-distribution-strategy` once the window closes instead of re-costing them here.

## Step 6 - Stand up the war room and run the day

Build the run of show from [references/launch-day-runbook.md](./references/launch-day-runbook.md):

- Pre-flight checks.
- The posting hour, chosen from the anchor audience's geography.
- The first comment that supplies context.
- The response rotation.
- Who watches what.

Staff it on GitLab's model, the only complete openly published launch-day playbook. Four pieces generalize to any project:

- One named DRI per channel.
- A stated response cadence rather than "as needed".
- An escalation path to the engineer who can answer.
- An explicit rule on who may speak with authority.

Its tone rule is the whole posture in three words: "conveying without convincing".

Two rules carry most of the outcome:

- Post the maintainer's own top-level comment immediately: who you are, why it exists, what is interesting under the hood, what it does not do yet.
- Stay in the thread for several hours and answer everything, including hostile comments, without defensiveness.

Availability is the only variable you fully control after publishing.

Keep a triage lane open in parallel: a broken install path found in hour one is worth fixing and shipping the same hour, and saying so in the thread converts critics faster than any argument.

One kind of comment bypasses the rotation entirely: a security report, or anything shaped like one.

1. Stop discussing it publicly.
2. Point the reporter at `SECURITY.md`.
3. Open a private advisory.
4. Patch on a private branch.
5. Publish the advisory crediting them.

Coordinated disclosure only works if that contact path exists before launch day; that is why it is a blocker in Step 2, not a reaction.

## Step 7 - Concentrate velocity, never manufacture it

Discovery surfaces sample flow, not stock. GitHub Trending ranks stars gained inside a window (today / this week / this month) and filters by language, so a project's language page is a far smaller pool than the global page and the realistic target for a first launch. The selection formula is unpublished - treat any reverse-engineered version as folklore and never promise a trending placement.

That is why concentration beats spreading: the same effort compressed into one day produces the slope these surfaces reward, while a week of drip produces none.

The other half of the same mechanic is a hard boundary: never solicit votes, stars or comments, and never coordinate them. Hacker News states that asking for upvotes gets submissions, accounts and whole domains penalized, and Product Hunt weights votes for authenticity rather than counting them raw.

The penalties are invisible from outside, so a team can run the play and never learn why the post died. Asking colleagues to "go look" is fine; asking anyone to upvote or star is not. Say the difference out loud to the team before launch day.

## Step 8 - Measure honestly

Capture the baseline the evening before:

- Stars, unique visitors and cloners.
- Registry downloads for the last full week.
- Docs sessions.
- Open issues, contributor count and referrers.

Traffic panels keep only a short rolling window, so an uncaptured baseline is unrecoverable.

Then read three windows (a conventional split, not a standard) and let the day-30 numbers decide:

- Day 1 measures attention.
- Day 7 measures trial.
- Day 30 measures adoption.

Metric definitions, target-setting method and the funnel-stage diagnosis table are in [references/measurement-plan.md](./references/measurement-plan.md).

Treat stars as the loudest and least meaningful signal. An issue opened by a stranger who clearly read the docs outranks a hundred of them; the pairing to watch is star growth against unique cloners and downloads. A spike in the first with no movement in the others means the announcement travelled, and the project did not.

Set targets as multiples of the project's own pre-launch baseline. The absolute numbers that circulate for launch-day stars per hour, front-page thresholds or day-1 download lift trace back to single anecdotes and launch-consultancy claims; say so rather than adopting one as a target.

## Invocation examples

- _"We're open-sourcing our internal feature-flag service next month. Can you plan the launch?"_ → Full interview, then the launch plan below, with Step 1 flagged as urgent because a month is inside the trademark-clearance window.
- _"Review my Show HN title and first comment before I post."_ → Skip to Steps 3 and 6; rewrite both against the credibility codes and return a weak/strong diff.
- _"How do I get on GitHub Trending with a Rust crate?"_ → Step 7 plus Step 5; name the language page as the realistic target and refuse to promise placement.
- _"Our launch got 40 stars and died. What went wrong?"_ → Skip to Step 8; run the funnel-stage diagnosis before proposing any relaunch.
- _"We have five features shipping and a conference keynote in six weeks."_ → Step 4 caravan branch; produce a per-day sequence with a named owner per day.

## Expected output

Produce a launch plan the maintainer can execute without you:

```markdown
# Launch plan - <project>

## Verdict go / go with reduced scope / not ready (blockers listed)

## Clearance name, trademark, license, CLA/DCO status

## Positioning one-liner, why-not-X, three claims we can defend

## Audience individual / company adoption, and the assets each needs

## Shape single spike or caravan, with the reason

## Channels anchor + amplifiers ranked by outcome per hour, then the firing clock, a DRI each, and the rows deleted with the reason

## Run of show hour-by-hour for launch day, including the first comment

## Measurement baseline snapshot, day-1/7/30 targets, tracking method

## Risks what could flag, break or overwhelm us, and the response
```

Present it section by section and get agreement on each before moving to the next - a positioning error propagates into every post if you write them all first.

## Common failure modes

- **Announcing before the name is cleared.** A rename after public visibility costs the URL, the search history and the announcement itself. Clear it in Step 1 or accept that risk explicitly.
- **Launching to a fixed external date with blockers open.** Reduce scope instead; broken install commands become the top comment and outrank the project in search for years.
- **A flat launch read as bad luck.** Localize it by funnel stage before relaunching anywhere - see the diagnosis table in the measurement reference. Only "wrong channel" justifies a relaunch; the rest justify fixing the artifact.
- **Reposting a dead thread immediately.** Aggregators bury duplicates. Hacker News allows a small number of reposts only when a story "has not had significant attention in the last year or so" and separately runs a second-chance pool moderators use to re-surface good submissions that missed. Mailing them once is the sanctioned recovery path; resubmitting is not.
- **Nobody home.** A launch posted before a meeting-heavy day dies in the comments. Move it.
- **Winning the wrong audience.** Individual-developer channels for an enterprise-shaped project produce applause and no adoption; check the day-30 numbers, not the day-1 ones.
- **Burnout in week one.** An over-performing launch lands on a team of one or two, already fragile. Tidelift's maintainer surveys (2020, 2022) put burnout at 46% of professional maintainers, rising to 58% on widely-used projects - with almost 60% having quit or considered quitting a project. Agree the triage trigger (issue templates, thread locks, a temporary contribution freeze) and a response SLA you can hold before launch day, not while drowning.

## References

- [references/pre-launch-timeline.md](./references/pre-launch-timeline.md) - 8-weeks-out staged sequence: trademark, license, press, war room, freeze.
- [references/readiness-checklist.md](./references/readiness-checklist.md) - blockers, boosters, cold-run protocol.
- [references/channel-playbook.md](./references/channel-playbook.md) - per-channel norms, HN vs Product Hunt, title rules, what gets flagged.
- [references/launch-day-runbook.md](./references/launch-day-runbook.md) - hour-by-hour run of show, DRI model, first-comment and response patterns.
- [references/announcement-examples.md](./references/announcement-examples.md) - weak vs strong one-liners, titles, comparison tables, first comments.
- [references/measurement-plan.md](./references/measurement-plan.md) - baseline capture, day-1/7/30 metrics, flat-launch diagnosis.

Related skills in this collection:

- `samber/developer-relations-skills@readme-optimization` - the README the launch points at.
- `samber/developer-relations-skills@developer-quickstart-guide` - the first-success path the gate tests.
- `samber/developer-relations-skills@oss-license-strategy` - the license and CLA/DCO decision Step 1 assumes is settled.
- `samber/developer-relations-skills@tech-press-relations` - embargo and briefing mechanics.
- `samber/developer-relations-skills@oss-distribution-strategy` - the channel mix after the launch window closes.
- `samber/developer-relations-skills@open-source-company-strategy` - the boundary decision on what gets open-sourced, settled before this launch is planned.
