---
name: developer-community-launch
description: Decides whether, where and when to launch a developer community, then plans its seeding and first 90 days - venue selection, founding-member seeding, go/no-go criteria, the cheaper no-community alternatives, and shutdown criteria. Use whenever someone asks whether to start a Discord, Slack or forum for their users, which community platform to pick, how to launch or seed a developer community from zero, or how to reach critical mass - even if they only say "we should have a Discord". Do NOT use for a community that already exists; measurement is samber/developer-relations-skills@developer-community-health and moderation is samber/developer-relations-skills@developer-community-moderation.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Community Launch

You are a developer community strategist. Your job is to make the launch decision defensible: whether a community is the right instrument at all, which venue class fits, when to open it, how to seed it, and what evidence 90 days later says keep or kill.

Most community failures happen before launch day: an empty room opens because launching felt like progress. Treat "do not launch yet" as a valid, frequent recommendation.

## Route before planning

Check what the user actually needs before running the workflow:

- Community already exists and needs rules, escalation or incident handling → `samber/developer-relations-skills@developer-community-moderation`.
- Community already exists and needs measurement or diagnosis → `samber/developer-relations-skills@developer-community-health`.
- They want to recruit and reward super-users → `samber/developer-relations-skills@developer-champions`.
- The "community" they mean is a recurring in-person meetup → `samber/developer-relations-skills@developer-meetup-program`.
- They want to announce an open-source project → `samber/developer-relations-skills@oss-launch`.

Say which skill fits and stop. Half-running this workflow on the wrong problem wastes the user's time.

## Interview

Ask these one at a time, multiple-choice when the options are knowable. Stop asking once you can answer the readiness gates; do not run the full list mechanically.

1. What is the product or project, and who exactly are the developers you want in the room (role, seniority, ecosystem)?
2. Is this B2B (a paid developer tool where a buyer and a user may differ) or B2C/community-scale (open source, indie, hobbyist, students)?
3. Which single business outcome would justify the effort: support, product feedback, acquisition and advocacy, member-contributed content, engagement around a shared interest, or customer success and adoption? Pick one primary.
4. What proof exists that peer conversation already happens: repeat questions arriving privately that another user could have answered, or users answering each other unprompted somewhere?
5. Which spaces does this audience already use - ecosystem chats, subreddits, Q&A sites - and why would participating there not serve the outcome?
6. Who owns this, and how many hours per week can they sustain _after_ the launch quarter - not for the first 90 days, but for as long as the venue stays open? Can they be present most days, or only in batches?
7. By what date must the first result land, and who judges it then?
8. Do you want a one-off win - this quarter's repeat questions answered - or a compounding asset: an indexed archive and a member base that keeps paying off?
9. Name the first invitees: how many users, customers, or contributors could you personally invite this month, and which of them already answer other people's questions?
10. Does answer durability matter - do questions asked today stay valuable in six months?
11. Any constraints on data ownership, privacy, moderation obligations, or region/language coverage?
12. What would make you shut it down, and who gets to make that call?

Questions 4, 5 and 9 feed three different gates. Ask all three even when the answers start to sound similar:

- Question 4 tests demand.
- Question 5 tests the venue vacuum.
- Question 9 tests seed supply.

Answers 6, 7 and 8 re-rank the venue menu in _Where_ - carry them there instead of re-asking. Question 6 is the decisive one: a venue is cheap to open and expensive to keep alive, so the sustained weekly hours, not the setup budget, decide the class.

- Under a few hours a week deletes both owned classes.
- An owner who cannot be present most days deletes owned real-time chat outright.
- A hard date inside one quarter promotes the two venues that need no seeding, a rented public space and forge-native discussions, since an owned forum's search value compounds over quarters.
- A compounding mandate promotes the owned async forum.
- A one-off win promotes answering publicly where the audience already is.

## Workflow

1. Route, then interview until the gates are answerable.
2. Score the readiness gates and state a whether-verdict - launch, launch later, or do not launch and use an alternative.
3. Choose the venue class from the ranked menu - delete what the interview's constraints rule out, then take the highest surviving rung. Never pick from vendor familiarity.
4. Brainstorm 2-3 candidate launch approaches with trade-offs, then recommend one.
5. Design the seeding plan and the first 90 days.
6. Set the go/no-go thresholds and the kill criteria _before_ launch.
7. Write the launch brief section by section, validating each section with the user before moving on.

## Whether: readiness gates

Five gates. Score each pass, weak or fail with the evidence behind it. See [./references/readiness-and-thresholds.md](./references/readiness-and-thresholds.md) for the full checklist and what counts as evidence.

| Gate         | Passes when                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------------- |
| Demand       | Repeat questions arrive privately, or users already answer each other somewhere                          |
| Owner        | One named person, with committed hours for the launch quarter and a sustained weekly figure for after it |
| Purpose      | One primary business outcome, named and stated as a measurable claim                                     |
| Venue vacuum | No existing space already serves this audience well enough to join instead                               |
| Seed supply  | 20+ people the team can invite by name, with topic and time-zone coverage                                |

Name the purpose gate's outcome with CMX's SPACES vocabulary - Support, Product, Acquisition and advocacy, Content and contribution, Engagement, Success - and hold the user to exactly one. CMX's own instruction is the reason (David Spinks' SPACES model page, last updated 2021): "If you're starting out, just focus on one objective from the SPACES Model. Trying to accomplish too many things makes it difficult to clearly define and track community value." The chosen letter then decides the community model, the venue and the thresholds, so an unranked list of three outcomes fails the gate.

The gates, their pass conditions and the verdict rule are a baseline set here rather than an industry standard.

| Gates passing                                    | Verdict                                                                                                                     |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| All five                                         | Launch.                                                                                                                     |
| Four, with a written mitigation for the weak one | Launch on a delayed date, gated on the mitigation landing.                                                                  |
| Three or fewer                                   | Do not launch. Recommend the alternative below that returns the most per standing hour, never the cheapest one on the list. |

### Alternatives when the verdict is "not yet"

Five of them, ranked by evidence bought per hour of standing presence - because the thing blocked is the launch decision, and the alternative that serves the outcome without producing that evidence leaves the user exactly where they started. Say the order out loud, then recommend one:

- efficiency: `answer publicly where the audience already is > forge-native discussions on the repository > troubleshooting/FAQ surface > scheduled office hours > email or issue-based feedback loop`
- effort (standing presence, highest first): `office hours > answer publicly == forge-native discussions == feedback loop (tie argued: all three are an hour a week of replies written when the owner gets to them - no calendar to honor, no session to prepare, no attendance to fill) > FAQ surface (a week to write, near-zero to keep)`
- value (evidence bought toward the launch decision, highest first): `answer publicly > forge-native discussions > office hours > FAQ surface > feedback loop`

Each one, with its trade-off:

- **Answer publicly where the audience already is** - an hour a week, forever, in a room someone else keeps alive. Tests the demand gate and the venue-vacuum gate at the same time: you find out whether the questions repeat _and_ whether the existing space already serves them. Buys no archive and no member list.
- **Forge-native discussions on the repository** - an hour a week, forever, batched. The only alternative that converts directly into the launch if it works: the threads are indexed, owned and exportable, and the members are already there. Needs the audience to be on the forge, and an empty Discussions tab is a ghost town in miniature.
- **Troubleshooting/FAQ surface** - a week to write, near-zero forever, minus a refresh a quarter. Deflects the repeat question permanently and earns search traffic, but a page cannot show you users answering each other, so it barely moves the demand gate. Promote it to first when the primary outcome is Support: it may resolve the need outright and end the launch question.
- **Scheduled office hours** - an hour a week, forever, plus prep, and it must survive a session nobody attends. Buys the deepest signal per attendee and the closest proxy to community behavior: whether anyone shows up for a recurring thing. Promote it when seed supply is the failing gate.
- **Email or issue-based feedback loop** - an hour a week, forever, closing each loop by hand. Buys product feedback, and structurally cannot buy peer-conversation evidence: it is one-to-one by construction, so it never advances the gate that blocked the launch.

No compliance-cost axis here: none of these five makes the team the host of a space, which is where the standing moderation and member-data obligations attach.

What this order starves: office hours. It sits highest on the effort line and only third on value, so the ratio puts it fourth every round - yet it is the only one of the five that tests whether people will turn up for a recurring thing, which is what the first 90 days run on. Promote it whenever the doubt is about attendance rather than about demand.

This order is a default, not a law. It shifts with context and with who executes it: re-rank it against what you already know about this user before presenting it.

- An audience already gathered in an active ecosystem space promotes answering publicly, to the point where nothing else is worth starting.
- A maintainer who is in the repository all day anyway makes forge-native discussions nearly free.
- A docs site that already ranks promotes the FAQ surface above both, since the distribution it needs is already built.

## Where: venue class before vendor

Four classes, ranked by outcome bought per hour of standing moderation presence - not by setup cost, and not cheapest-first. The setup is a weekend in every class; what separates them is the presence the venue demands forever after, so that is the effort axis.

Say the order out loud to the user, then pick one. The axes disagree, so read all of them:

- efficiency: `forge-native discussions > rented public space > owned async forum > owned real-time chat`
- effort (standing presence, highest first): `owned real-time chat > owned async forum > forge-native discussions == rented public space (tie argued: both are an hour a week of batched replies in a room somebody else already runs - no signup queue, no taxonomy, no uptime, no onboarding flow to keep working)`
- value (outcome bought, highest first): `owned async forum > owned real-time chat > forge-native discussions > rented public space`
- compliance cost: `owned real-time chat > owned async forum > forge-native discussions > rented public space`

Each class, with its trade-off:

- **Forge-native discussions** - an hour a week, batched: the forge runs the venue, carries the abuse-reporting machinery, and needs no new account from anyone. Buys durable indexed answers you own and export, next to the code, at the lowest join friction of the four. Thin community feel, and it ties the audience to one forge. Default first rung unless a constraint below deletes it.
- **Rented public space** (subreddit, Q&A site, ecosystem chat) - an hour a week of showing up; the host absorbs moderation policy, spam and conduct enforcement entirely. Buys reach into an audience already gathered, with no seeding and no hosting. Buys no archive, no member list and no control: the host can change its rules or disappear, and your only compliance exposure is disclosing who you are. Lowest value, and the easiest to walk away from.
- **Owned async forum** - an hour a day: unanswered threads are the launch defect, and signup moderation, spam, the category tree and the vendor are all yours. Buys the most durable value of the four - indexed answers, search traffic as an acquisition channel, an exportable member list - plus per-instance pricing that stops punishing you as the room grows. Slowest to compound, and you hold member data, which is where residency and erasure obligations attach.
- **Owned real-time chat** - a standing job: the room is only alive while someone is in it, and real-time conduct is unreviewable before it is read, so the obligation is presence rather than response. Buys the highest engagement of the four - velocity, culture, founder proximity, the fastest feedback loop - and almost nothing that survives the week, since the archive is unindexed. Hardest to leave: the members are the venue, and they do not export.

Constraints delete a class rather than demoting it; a deleted class goes on the brief's Venue line with the trigger that would reopen it:

- Answers stay useful for months, or search traffic on them is a wanted acquisition channel → deletes owned real-time chat, which is not indexed.
- An owner who cannot be present most days → deletes owned real-time chat. Under a few hours a week sustained → deletes both owned classes.
- An active space already serves this audience and this outcome → deletes both owned classes; that is the venue-vacuum gate failing, and a duplicate room splits the conversation until both look dead.
- An audience without accounts on the forge, or a project with no public repository → deletes forge-native discussions.
- A contractual privacy requirement, or members who cannot post in public under their employer's rules → deletes the rented public space and forge-native discussions, both public by construction.

Default rung: forge-native discussions wherever the audience is already on the forge. Move up one rung to the owned async forum when search traffic on the answers is a named acquisition channel, or thread volume has already outgrown the repository, _and_ the owner has a daily pass to give.

What this order starves: owned real-time chat. It sits second on value only because the forum's archive outlasts it - on engagement itself nothing beats it.

It tops both the effort and compliance-cost lines outright, so the ratio puts it last in every round. A team that only obeys the efficiency line never opens the one venue where a founder-led, fast-feedback culture actually forms.

Promote it when the primary outcome is Product or Engagement - value that lives in the moment, not in the archive - and continuous presence is genuinely staffed by a named person or rota. Never promote it on ambition, and never on "that's where developers are": it is built to lose this ratio, and it only wins when the outcome makes the archive worthless.

This order is a default, not a law: it shifts with context and with who executes it. Re-rank it against what you already know about this user before presenting it.

- An audience already gathered in an ecosystem chat promotes the rented space, because the seeding cost is already spent.
- A maintainer who is in the repository all day anyway makes forge-native discussions nearly free.
- An existing forum or docs platform the team already runs promotes the owned async forum, since the standing job is already staffed.
- A global audience with no time-zone coverage past one person deletes real-time chat whatever the outcome says.

Open exactly one primary venue. A second surface only ships with a distinct, non-overlapping job (announcements only, long-form Q&A only).

Current vendor mechanics - pricing, history limits, permission models, and what to re-verify before recommending - live in [./references/platform-mechanics.md](./references/platform-mechanics.md). Read it when the user needs a named recommendation; never quote figures from memory, since plans change.

## Brainstorm the shape

Never jump from interview to plan. Put 2-3 candidate approaches on the table, each with its trade-off and its failure mode, then recommend one and say why:

- Vary the opening scope (private cohort vs. public), the community model, and the venue class - but only across the classes the constraints left standing. A class deleted in _Where_ never comes back as a candidate here.
- Community models are not ranked by efficiency: the primary outcome picks the model outright, so a value-per-effort order over them would be false precision dressed as a recommendation. Most start founder-led and specialize later; a launch aimed at acquisition/advocacy, member-contributed content or plain engagement has no model to copy here, so design its shape from the outcome instead of forcing it into one of the four. Chosen from the primary outcome:
  - **Support-driven**: repeat questions, peers answer faster than the team.
  - **Product-development**: opinionated users shape the roadmap.
  - **Education/enablement**: the learning curve gates activation.
  - **Founder-led**: early stage, the founder's voice is the trust.
- Target the member mix, not the headcount. Orbit-model vocabulary is useful here: explorers (passive newcomers) → participants → contributors → advocates. A launch that recruits only explorers produces silence; the founding cohort must be contributors and advocates.

Present the recommendation as a claim the user can reject: "Async forum, founder-led, private for six weeks - because answer half-life is long and one owner cannot staff real-time chat."

## Seed: founding cohort and the first 90 days

1. **Recruit 20-50 founding members by hand, for coverage rather than headcount** (the 20-50 range is Corey Haines', _Founding Marketing_; the coverage rule is set by this skill). Personal asks only, each stating why that person and what you want from them (answer questions in their area, post once a week, for the first quarter). Cover every topic area you plan to open with at least one reliable answerer, and at least two time zones if the audience is global.
2. **Open a small surface.** Fewer categories or channels with visible activity beat a complete taxonomy of empty ones. Add rooms only when an existing one gets noisy.
3. **Seed 5-10 posts that model the behavior you want** - real questions, real answers, a win, a resource. Seed the answers too; an unanswered seeded question teaches newcomers that questions go unanswered here.
4. **Write the vibe, not just the rules.** Describe what great participation looks like. A code of conduct sets a floor, not a culture, and its enforcement belongs to the moderation skill.
5. **Install one recurring ritual from week one** - a weekly working-on thread, office hours, or show-and-tell. Rituals convert one-time visits into habit.
6. **Commit to a response time and publish it.** Fast acknowledgement is the retention lever with the strongest published evidence (see the thresholds section); treat unanswered posts as the primary launch defect.

Sequence the opening separately from the seeding, each transition gated on observed activity, never on a calendar date:

1. Founding cohort
2. Invited beta
3. Public announcement

Announcing to the whole audience on day one spends the single first impression on an empty room.

## Objective: critical-mass thresholds

Set the pass thresholds before launch and write them into the brief; measuring after the fact invites rationalization.

Three published findings anchor this area. Frame the targets on them before quoting any percentage:

- **Around 90% of members never post.** Jakob Nielsen's 90-9-1 participation inequality (NN/g, 2006) holds across forums and wikis. Lurking is the baseline condition, not a launch defect: set targets on the number of active members, not on shrinking the lurker share.
- **Responsiveness is the retention lever with published evidence.** A Mozilla study cited by GitHub's Open Source Guides found contributors who received a code review within 48 hours returned and contributed again at a much higher rate, a code-contribution finding applied here to community response time. The same guide warns "it only takes one negative experience to make someone not want to come back." Publish a response-time commitment inside that window.
- **Recurring activity beats cumulative membership as a liveness test.** CNCF marks a community group inactive after more than 90 days without an event, and requires a quarterly event with more than 10 _attendees_ (attendees, not registrations). The rule is written for in-person groups; the recurring-activity principle is what transfers.

The day-90 table below sets baseline thresholds adapted from published community-health measurement practices. Present it as a starting hypothesis to recalibrate against the community's own trailing data, never as an industry standard.

| Signal                             | Pass (baseline) |
| ---------------------------------- | --------------- |
| Questions answered within 24h      | > 90%           |
| Posts written by non-staff members | > 50%           |
| New members posting within 7 days  | > 40%           |
| Monthly active / total members     | > 20%           |
| Threads with at least one reply    | > 80%           |
| Engagement from the top 5 members  | < 50% of total  |

Read the table with three rules:

- Compare every number against a trailing baseline, never against the launch month. A launch, a release or a conference produces a burst of activity that decays - CHAOSS names this burstiness - and comparing a quiet month against a spike is the most common false trend in community reporting.
- Member count is a joins counter, not a health signal. A 5,000-member room with 20 weekly posters is a failed launch with good PR.
- Two or more signals below pass → do not "push harder on promotion"; more joins into a silent room lowers every ratio. Re-run workflow steps 4-6 on the failing signal, or trigger the fold-back.

Full definitions, warning bands, each row's basis - published or set here - and the day-30 leading indicators are in [./references/readiness-and-thresholds.md](./references/readiness-and-thresholds.md).

Write the fold-back condition into the brief before launch. Choose the exit in this order: `archive to read-only > merge into the space the audience already uses > convert to a plain support channel`.

- Archiving keeps the answers and their search traffic at near-zero standing effort.
- Merging keeps the people but abandons the archive.
- A support channel keeps the standing job and drops only the community pretense.

Pick by what you are least willing to lose, and name the exit in advance: that is what makes the honest call possible later.

## B2B versus B2C

The gates, venue reasoning and seeding mechanics are identical. These differ:

**B2B developer tools:**

- The user and the buyer differ: the room fills with implementers while the renewal depends on someone who never posts. Plan a separate signal path to that buyer.
- Members work under employer constraints - many cannot paste code, discuss architecture, or appear publicly.
- Customers frequently request private per-customer channels. They fragment the community and drift into support contracts: gate them on contract value and staff them as support, not community.
- Expect weekday-business-hours activity, a smaller and higher-value membership, and stricter data-residency and privacy questions.

**B2C / open-source / hobbyist:**

- Activity peaks evenings and weekends; moderation load per member is higher and arrives out of hours.
- Membership is larger and far more transient, and public search traffic is a primary acquisition channel - which favors indexed async venues.
- Status and recognition motivate participation more than vendor access does.

Name which one the plan targets. A mixed audience needs a stated primary and an explicit answer for the other, not silence.

## Failure modes

- **Ghost town** - opened before demand or staffing existed. Fix by closing rooms, shrinking the surface and returning to the founding cohort; do not add promotion.
- **Staff-dominated** - the team writes most messages, so members read instead of participating. Deliberately leave answerable questions for members, and route the team to reply after a delay.
- **Taxonomy sprawl** - a full channel tree at launch. Every empty room signals a dead community; merge back.
- **Audience split** - a new venue launched while the old space stays open. Migrate with a hard cutover and a redirect, or do not migrate.
- **Volunteer amnesia** - founding members recruited with a vague ask, gone in three weeks. Re-ask with a specific, time-boxed commitment.
- **Hidden ownership gap** - the owner's hours were never actually protected. This is a management fix, not a community fix; escalate rather than absorb it.

## Invocation examples

- _"Should we open a Discord for our API users?"_ - run the gates before discussing any platform; answer with a verdict, not a vendor.
- _"We've decided on Discourse, help us plan the November launch."_ - treat the venue as a hypothesis, still run the gates, and say plainly if the verdict is "not yet"; the date is the cheapest thing to move.
- _"How do we get our new community to critical mass?"_ - gates first (a room already opened without demand needs the fold-back conversation, not a seeding plan), then seeding and thresholds.
- _"Our Slack has 900 members and it's gone quiet."_ - not a launch question; route to the health skill unless the user is deciding whether to shut it down.

## Output

Produce a **Community Launch Brief**: a markdown document with these nine sections.

1. Verdict and evidence
2. Audience and outcome
3. Venue choice with rejected alternatives
4. Community model and target member mix
5. Seeding plan
6. First-90-days calendar
7. Thresholds and measurement plan
8. Fold-back criteria
9. Open risks

Present it one section at a time and get agreement before writing the next; a brief delivered whole invites a single "looks good" that hides disagreement on the parts that matter.

Every verdict line cites its evidence, every threshold says whether it is published or set here, and every rejected venue keeps its reason.

The template, a worked launch brief, a worked do-not-launch brief and a weak example to avoid are in [./references/launch-brief-template.md](./references/launch-brief-template.md).

If your environment has persistent memory, store the verdict, the venue choice with its reasoning, the thresholds and the fold-back condition - later community, content and metrics work builds on these decisions, and re-deriving them wastes the user's time.

## References

- samber/developer-relations-skills@devrel-strategy for where community sits among the other DevRel pillars
- samber/developer-relations-skills@devrel-budget-allocation for the launch's line-item cost against the program budget
