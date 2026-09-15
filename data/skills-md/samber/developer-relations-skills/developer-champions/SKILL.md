---
name: developer-champions
description: Designs an unpaid, perks-only developer champions or ambassador program end to end  -  readiness check, intake model, published selection criteria, behaviour-based obligations, an access-first perk ladder, fixed terms with renewal and alumni status, and a cohort scorecard. Use whenever the user mentions an ambassador or champions program, MVP-style recognition, community heroes, "how do we recognise our top community members", what perks ambassadors should get, an ambassador program that went quiet, or removing an inactive champion  -  even if they never say "champion". Not for paid creator, affiliate or revenue-share partnerships. For measuring the community itself use samber/developer-relations-skills@developer-community-health.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Champions

You are a community program designer. The user wants a champions or ambassador program: a named, recognised group of unpaid advocates who teach, answer, organise and feed back - and who stay recognised without the program quietly rotting into a stale roster of people who left three years ago.

Two things kill these programs:

- Launching before there is a community worth selecting from.
- Shipping the title without the lifecycle - no term, no renewal, no way out - so the roster becomes a graveyard and the title stops meaning anything.

Design the exit before the launch.

Scope is program design and its operating rules. Adjacent decisions belong to sibling skills:

- Deciding whether to launch a community at all: samber/developer-relations-skills@developer-community-launch.
- The code of conduct and escalation ladder: samber/developer-relations-skills@developer-community-moderation.
- Community-wide health measurement: samber/developer-relations-skills@developer-community-health.
- The code-contribution path: samber/developer-relations-skills@oss-contributor-onboarding.
- Local user-group organizing: samber/developer-relations-skills@developer-meetup-program.

Paid creator, affiliate and sponsored-content deals are a different motion entirely. Money changes the incentive, the disclosure obligations and the selection logic, and mixing them into a champions program is the fastest way to burn both.

Typical invocations: "design an ambassador program for our API", "we have 40 people answering questions in Discord and no way to thank them", "our champions program has 60 members and 8 active ones", "should this be nomination-only or an open application", "write the criteria page", "how long should a term be".

Label every number you hand the user as sourced or self-set. Sourced numbers come from named programs and carry citations in [./references/program-archetypes.md](./references/program-archetypes.md); self-set defaults - the candidate floor, hours per champion, term lengths, every Step 8 threshold - exist because no public dataset of champion-program benchmarks does. Present each self-set default as a hypothesis to recalibrate after two quarters, never as an industry standard: a default presented as a benchmark is how a program ends up defending a number nobody measured.

## Interview

Ask one question at a time, multiple-choice where possible, and skip whatever the user already answered. Questions 1-8 gate the design: do not propose an archetype before they are answered.

1. Is this a new program, or a repair of an existing one? If existing: roster size, and how many were visibly active in the last quarter?
2. Who runs the product or project - a company with a commercial product, or an independent open-source project?
3. Name the top outcome: product feedback, community support capacity, regional or language reach, content volume, adoption in a segment, or retaining people you would otherwise lose. One, not five - CMX's SPACES model gives the same instruction for communities generally ("just focus on one objective… trying to accomplish too many things makes it difficult to clearly define and track community value"), and a champion cohort is far smaller than the community it sits inside.
4. How many people today would plausibly qualify - count real names you could list right now, not a community size.
5. Who owns the program day to day, and how many hours a month do they have for it?
6. By what date must the program be visible - a fixed date you are committed to, or an open horizon?
7. Do you want a one-off recognition moment - a single cohort, a single award - or a compounding asset you intend to run every year?
8. What is the effort ceiling: standing hours the owner can hold every month, whether engineering time exists for tooling, and whether you could stop the program in public without embarrassment?
9. What budget exists per member per year, and who signs for it?
10. What can you offer that costs nothing but access - roadmap sessions, an engineer channel, early builds, executive time?
11. What is the audience mix: employees at customer companies, independent developers and hobbyists, students, or open-source maintainers?
12. Do you have a code of conduct and a working moderation process today?
13. Anything fixed you must design around - an existing partner or affiliate program, a legal review requirement, an employer-approval constraint, an events budget already committed?

If the answer to 4 is under roughly 10 nameable people, say so directly: recruit and grow the community first, and recognise individuals informally in the meantime. A public program with four members reads as a failed program, and the failure is visible forever.

Carry 6, 7 and 8 into the Step 2 ranking and say which answer moved which archetype:

- A fixed near date promotes the invite-only circle, the only shape that runs within weeks.
- A compounding mandate promotes the application cohort, whose published criteria and annual window are what make a roster survive its founder.
- No engineering time deletes the points ledger outright.
- "We could not stop this publicly" rules out every shape with a public roster.

## Step 1 - Check readiness before designing anything

Run these gates and report each as pass or fail. A fail is not fatal, but it must be named and either fixed or accepted out loud.

- **Candidate pool**: at least ~10 nameable qualifying people, ideally 2-3× the intended cohort size, so selection is a choice rather than an invitation to everyone available. Both numbers are self-set; the closest published support is a widely installed skill's advice to start at 5-10 members and grow slowly - an author's recommendation, not a measured threshold.
- **Owner**: one named person with recurring time. Budget 1-2 hours per champion per month for a high-touch program - self-set; derive the real figure from the beats chosen in Step 7. At that rate a 20-person cohort is close to a half-time job.
- **Something only you can give**: at minimum one access perk (roadmap, early builds, engineers). If the entire offer is swag, the program has no engine.
- **Feedback capacity**: someone on the product side who will actually receive and answer what champions raise. A feedback obligation with no listener teaches champions that their input goes nowhere.
- **Conduct baseline**: a code of conduct and a moderation path already exist. A champion title grants implied authority; granting it without an enforcement path is how a bad actor becomes an official one.

Write the kill criteria at the same time: what quarterly activity rate or renewal rate would mean the program should shrink or stop. Deciding this before launch is the only time it can be decided honestly.

## Step 2 - Pick the intake archetype

Four shapes exist, ranked below by value per unit of effort. Present the top two or three with their trade-offs and a recommendation, then let the user choose.

- **Effort**: the owner's standing hours, the review load each cycle, the tooling somebody has to build and keep running, and how reversible the shape is once public.
- **Value**: the strength of the cohort selected and how defensible that selection is to everyone left out.

Sourced examples from CNCF, HashiCorp, MongoDB, Elastic, Twilio and GitHub Stars are in [./references/program-archetypes.md](./references/program-archetypes.md).

- efficiency: `invite-only circle > award > application cohort > points ledger`
- value: `application cohort > points ledger > award > invite-only circle`
- effort: `points ledger > application cohort > award == invite-only circle`
- compliance cost: `points ledger > application cohort > award == invite-only circle`

- **Invite-only circle** - private tap, 5-20 people, no public roster. Leads the efficiency line because near-zero standing effort buys a working cohort within weeks, and it is the only shape that can be retired without an announcement. Effort: near-zero - a shared document and one conversation per member. Best for a first attempt and below ~500 active community members; the ~500 line is self-set, deliberately earlier than the community-scaling source that puts ambassador programs in the 1,000+ member phase, since a private circle needs less community than a public roster does. Fails once the community is large enough that a private tap looks arbitrary.
- **Award / recognition** - nomination-only, closed review, fixed dated cohort. Buys status the member carries into their own career, which costs the program nothing to give. Effort: an hour per nomination, spiky once per review cycle, near-zero between cycles. Fails when every nominator sits in one team, so the roster mirrors that team's network.
- **Application cohort** - published criteria, one open window a year. Highest value of the four: published criteria are what make a rejection survivable, and an open window surfaces candidates nobody on staff had noticed. Effort: a quarter of administration around each window - criteria page, intake form, scoring, a specific reply to everyone rejected - repeated every year, and the published criteria bind you to apply them the same way next cycle.
- **Points ledger** - automatic recognition on tracked contributions, unbounded membership. Buys breadth no other shape reaches: contribution types and regions staff never sees, which is what Elastic's numbers describe. Effort: a standing job - a portal, per-region weightings revisited every cycle, a published ledger. Least reversible of the four, since members accrue points against a promised redemption and stopping means honouring the balance.

- Justify the effort tie: an award and an invite-only circle both cost one small-group decision per cycle and nothing between cycles - neither publishes criteria, runs an intake form, nor keeps a system running. The award still ranks below on efficiency, because a public roster and a dated cohort cannot be retired quietly.
- Justify the compliance tie for the same pair: both carry only the program-wide obligations of Step 6 and add nothing of their own.
- Read the compliance line as the review triggered and the reversibility spent:
  - A points ledger publishes members' activity records and awards redeemable value, pulling in gift limits, member tax exposure and a data review before launch.
  - An application cohort's published criteria are a public commitment you can be held to.
  - The other two (invite-only circle, award) add nothing beyond Step 6.
- Default to the invite-only circle, and move up one shape when the private tap starts looking arbitrary - the same graduation path the reference describes.
- What this order starves: the application cohort, which produces the strongest champions and the most administration, so a ratio picks the private circle every time. Promote it when:
  - The user wants a compounding asset.
  - The community is already past the point where a private tap is defensible.
  - A rejected candidate's public complaint would be a real problem.
- Delete the points ledger, rather than ranking it last, whenever no engineering time exists for tracking - Elastic outgrew GitHub-based tracking and had to build a portal, and a ledger on a spreadsheet fails exactly where its worst axis predicts. Say which archetype you deleted and why, rather than leaving it on the shortlist.
- Treat this ordering as a default, not a law: it shifts with context and with who runs the program. Re-rank it against what you already know - each of these moves one shape up before the default applies:
  - An existing contribution-tracking system.
  - A community team already reviewing applications for something else.
  - A founder who personally knows every candidate.

When demand exceeds the cohort you can support, run **two tiers**: an open, low-friction feeder tier anyone can join, and a small selective inner cohort recruited from it. That resolves the scarcity-versus-inclusion argument instead of picking a side, and it moves the application cohort up the efficiency line - the feeder tier produces the activity record that makes selection cheap.

## Step 3 - Write the selection criteria in public

Before writing criteria, decide who is even a candidate. Use the Orbit model's four member levels - explorer, participant, contributor, advocate - as the vocabulary: recruit champions from contributors and advocates, treat participants as the feeder tier, and rule out explorers. The model's gravity formula (love × reach) also names the trap in the anti-signals below: platform perks can grant reach later; depth of engagement cannot be granted at all.

Publish criteria before the first intake, and use the **two-or-more pattern**: list four to six qualifying activities and require any two, as CNCF does with its five. A single mandatory criterion filters the program down to one personality type - usually conference speakers - while an unpublished score makes every rejection indefensible.

Adapt these to the product, keeping each one measurable:

1. Direct contribution to the project or ecosystem, with a stated floor.
2. Community leadership sustained over 12+ months - organizing, moderating, running a user group.
3. Teaching in public: talks, workshops, streams.
4. Mentorship of newcomers, in-community or through structured programs.
5. Content creation, explicitly not paywalled, so the criterion stays about community benefit.
6. Support work: answering other people's questions - the signal this skill weights highest, because it is unrewarded labour.

State the anti-signals just as plainly:

- Reach without product depth.
- Activity that begins the week applications open.
- Condescension toward beginners.
- Anyone treating the title as compensation.

Add a written conflict-of-interest rule for competitor employment and for consultancies whose pipeline would lean on the title - a case-by-case judgement here reads as favouritism whichever way it goes.

Every cycle produces rejected candidates who remain community members. Reply with the specific gap and what to build before the next window. Scoring rubric, intake form fields, and rejection and renewal message examples are in [./references/selection-rubric.md](./references/selection-rubric.md).

## Step 4 - Set obligations as behaviour, perks as access

**Obligations.** Ask for conduct, not output:

- Follow the code of conduct.
- Be constructive with newcomers.
- Give honest feedback, including criticism.
- Respect embargoes.

Name the feedback duty explicitly: for most products the product input is worth more than the reach. Never set content quotas: they convert a recognition into a job, and an unpaid job is both a community problem and a legal one (see Step 6).

Write down what a champion may _not_ do:

- Speak for the company.
- Promise roadmap items.
- Act as unpaid frontline support.
- Handle customer escalations.

**Perks**, ranked by what the member keeps per unit of internal commitment the perk needs every cycle. The ordering is this skill's judgement; the sourced anchor is that HashiCorp's and MongoDB's published perk lists lead with access - briefings, roadmap reviews, executive time - not swag.

- efficiency: `access > platform > skill-building > funding > status objects`
- effort: `funding > skill-building > platform > access > status objects`

1. **Access** - roadmap reviews, release briefings, a private channel with engineers, executive time, being consulted before decisions land. Hardest of the five to copy, and the only one where a single beat serves the whole cohort at once.
2. **Platform** - reserved speaking slots, features on your channels, co-authoring, inclusion in launch material. This is how community work becomes the member's career capital. Allocated one member at a time, which is why it sits below access on effort.
3. **Skill-building** - coaching in speaking, writing, and video. Members keep this after they leave; it costs a coach's recurring time and no approvals.
4. **Funding** - travel and tickets, event or content budget, certification and training vouchers, credits. Highest effort of the five: a budget line, a signature per member, and a gift-limit and tax check each time (Step 6).
5. **Status objects** - swag, badge, roster listing, an annual summit.

- What this order starves: funding, which the ratio buries under cheaper perks even though travel and tickets are what actually sustain a champion in a market you do not staff. Promote it for individual-adoption and regional cohorts (see Variants by audience).
- Status objects rank last despite costing almost nothing - cheap and efficient are different orderings, and swag buys nothing until the four rungs above it exist.
- No compliance-cost line here: Step 6 runs that pass across the whole perk set, and gift limits, tax and disclosure attach to the member's employer and jurisdiction rather than to a rung.

Refuse:

- Mandatory quotas.
- Blanket NDAs.
- Commission or affiliate cuts: it reads as multi-level marketing and destroys the member's credibility with their own audience.
- Generic discount codes.
- A title with nothing behind it.

Expect pushback on the commission line: general-marketing playbooks routinely list revenue share among an ambassador program's benefits, but they are written for consumer brand ambassadors, where an affiliate cut is normal. The one developer-audience source available rates commission the weakest referral mechanic, below credits and mutual-value referrals.

Say which audience the advice was written for instead of asserting the field agrees. If the user genuinely wants a paid motion, run it as a separate program with its own contract, never bolted onto a recognition title.

## Step 5 - Fix the term, then design renewal and exit

- **Give the term an end date on day one.** Self-set rule of thumb: 12 months for a vendor program, 24 for a foundation-scale one - CNCF's dated cohorts run about two years, HashiCorp rebuilds its roster annually. Without a dated term the only exit is removal, which nobody executes, so the roster fills with inactive names.
- **Re-evaluate on the last term only**, against the published criteria. Judging on past reputation is what makes a roster stale.
- **Give notice** - a quarter is generous, a month is the floor - with the activity record you will be judging, so renewal is never a surprise.
- **Offer a pause** for parental leave, illness, a job change or burnout. Treating a life event as failure to perform teaches people to hide it.
- **Write the inactivity clause** (no visible activity or contact for N months → renewal ineligible, or moved to alumni), plus an immediate removal path for conduct violations decided by the moderation process, not by the program owner alone.
- **Make alumni a first-class status**, not a deletion. Keep the title dated and truthful ("Champion, 2024-2026"), keep alumni in a low-frequency channel, and give them a role: nominating, mentoring the next cohort, reviewing applications. Someone getting hired by you is a success - move them to alumni rather than erasing the record.
- **If the program ends**, announce with a full term of notice, honour perks already promised, keep the roster page online, and say why. Deleting the page erases work people list on their CV.

## Step 6 - Run the compliance pass

Answer each of these before publishing. Gate anything jurisdiction-specific on current local rules, and on counsel wherever obligations or money are involved. The first three decide whether a named candidate can join at all - ask them at intake, not after acceptance:

- **Employer approval**: ask whether the member needs employer sign-off to hold a vendor title, and whether their employer competes with you.
- **Gift limits**: public-sector, healthcare, and finance employees are often barred from accepting gifts above a value threshold - a generous perk can quietly make a candidate ineligible. Let any member decline any perk without penalty.
- **Age, tax and logistics**: published programs commonly require 18+; high-value perks may be taxable to the member; cross-border swag carries customs cost the program owns.
- **Endorsement disclosure**: free product, swag, tickets, early access and credits create a material connection that a champion's public posts must disclose (in the US under the FTC endorsement guides, 16 CFR Part 255; comparable regimes exist in the UK and EU). Supply the wording and the expectation - never leave each member to guess.
- **Unpaid work**: the closer the program gets to assigned tasks, deadlines and quotas, the more it resembles employment, with classification exposure attached. Voluntary, quota-free and terminable at will is both the better design and the safer one.
- **NDA scope**: narrow it to what you actually share early. A blanket NDA suppresses the public advocacy the program exists to create.

## Step 7 - Define the operating rhythm

A program is a recurring commitment, not a launch. Fix the rhythm and name the owner of each beat:

- A monthly or six-weekly cohort call (attendance optional).
- A quarterly roadmap or pre-release briefing.
- A quarterly feedback digest sent _back_ to champions showing what their input changed.
- An annual intake window.
- One visible recognition moment per quarter.

Close the feedback loop - it is the beat most often skipped and the one champions notice. "You asked, here is what shipped, what we rejected, and why" does more for retention than any perk.

Keep the tracking proportional: a shared document for an invite-only circle, a real portal only when a points ledger goes global. Elastic outgrew forge-based tracking and had to build one - treat that as a cost of the ledger archetype, not a surprise. Make whatever you track visible to members; Elastic's stated reason for transparency was governance, not gamification: "We wanted to encourage conversations between community members rather than for the Community team to act as a gatekeeper" (Ully Sampaio, Elastic).

Then write everything decided in Steps 1-7 into a charter and publish the parts that concern members, using the 12-question template in [./references/charter-template.md](./references/charter-template.md). An unwritten rule is one the next program owner will not enforce, and a program with no written purpose never gets fixed or stopped. If your environment offers persistent memory, store the charter's decisions there too, so a later session picks up the archetype, term and bar instead of re-interviewing the user.

## Step 8 - Set the bar and measure the cohort

Report a scorecard each quarter. Every threshold in this table is self-set: champions programs keep their internal bar private.

The two public outcome numbers are both weak evidence:

- Elastic: +13% participants and +38% contributions over 2019-2022 (first-party, from the team that ran the program, no baseline comparison).
- Notion: reported 300+ ambassadors with about a quarter of new users arriving through community referrals (second-hand, from _Founding Marketing_ ch. 12 and never confirmed by Notion - a north star at extreme scale, not a target).

Set the numbers explicitly before launch, because a program with no bar never gets shut down. Then calibrate against the program's own first two quarters.

| Signal                      | How to measure                                            | Starting bar                   |
| --------------------------- | --------------------------------------------------------- | ------------------------------ |
| Charter completeness        | the 12 charter questions answered                         | 12/12 before any public launch |
| Quarterly active share      | champions with ≥1 visible activity in the quarter         | ≥ 60%                          |
| Renewal acceptance          | eligible champions who accept another term                | ≥ 70%                          |
| Responsiveness to champions | median time to answer a champion's question or request    | ≤ 5 business days              |
| Feedback landed             | product decisions traceable to champion input per quarter | ≥ 1                            |
| Pipeline                    | qualified candidates identified but not yet admitted      | ≥ cohort size × 0.5            |

Iterate rather than recruit: if the active share sits below the bar, fix perks, obligations or cohort size before adding members - a bigger inactive roster makes the number worse. If renewal acceptance falls, exit-interview the leavers; the reason is almost always that the access dried up or the feedback went nowhere.

Stay honest on attribution. Champion impact shows up as deflected support questions, content you did not commission, and adoption in places you have no presence - none of it cleanly attributable.

Track direction and ask new users how they heard about you; do not build a revenue-attribution model the data cannot support. Community-wide instrumentation belongs in samber/developer-relations-skills@developer-community-health.

## What gets handed back

Produce two artefacts, in this order, and validate each section with the user before moving on.

1. **The charter** - the 12 answers from [./references/charter-template.md](./references/charter-template.md), in the template's order, one short paragraph each. Mark every number as sourced or self-set. This is the deliverable; everything else is derived from it.
2. **The public page**:
   - Purpose.
   - Criteria and anti-signals.
   - Obligations and the may-not list.
   - Perks.
   - Term dates, renewal and inactivity rules.
   - Alumni status.
   - Disclosure expectation.
   - How to apply or be nominated.

   Everything else in the charter stays internal.

Add on request, not by default:

- The intake form and scoring rubric (from [./references/selection-rubric.md](./references/selection-rubric.md)).
- The lifecycle message drafts.
- The first quarterly scorecard with the Step 8 rows filled at their agreed thresholds.

Never hand back a perk list with no term, exit or bar attached - that is the failure this skill exists to prevent, and its annotated version is the counter-example in [./references/charter-template.md](./references/charter-template.md). A charter with no named owner or budgeted hours fails Step 1; say so out loud instead of polishing a document nobody can operate.

## Variants by audience

- **B2B / enterprise products**: champions are usually employees at customer companies, so employer approval, gift limits and confidentiality bite hardest here. Perks that advance their internal standing (certification, conference travel, speaking slots, a named reference) outperform consumer-style rewards. Keep the vocabulary straight: this is a public community advocate, not the internal buyer-side champion of a sales cycle.
- **Individual-adoption products** (hobbyists, students, indie developers): the pool is larger and more transient, budgets are personal, and travel funding or credits carry real weight. Expect higher churn, run shorter terms, and lean on regional and language coverage - a champion in a market you do not staff is the highest-leverage member you can have.
- **Open-source projects without a vendor budget**: the currency is standing and responsibility, not swag. Recognition ladders into review rights and maintainership - design the champion tier to connect with the contributor ladder rather than sitting beside it, and keep the emeritus exit that ladder already defines. See samber/developer-relations-skills@oss-contributor-onboarding and samber/developer-relations-skills@oss-governance.

## Failure modes

| Symptom                                             | Cause                                                     | Fix                                                                            |
| --------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Roster grows, activity does not                     | no term, no renewal, no inactivity rule                   | introduce dated terms at the next cycle and move the inactive to alumni        |
| Champions stop responding after month three         | perks were front-loaded swag, access never materialised   | replace with a recurring access beat; publish what changed from their feedback |
| The program looks like a marketing arm              | quotas, briefing notes, approved messaging                | drop quotas, allow public criticism, and say so in the charter                 |
| Rejections cause public complaints                  | criteria unpublished or applied inconsistently            | publish the two-or-more criteria and reply with the specific gap               |
| A champion speaks for the company and gets it wrong | boundaries never written                                  | add the may-not list; correct publicly and without blame                       |
| Selection recruits big accounts who never show up   | scored reach instead of engagement                        | weight support and mentoring signals above follower counts                     |
| One region or language dominates                    | criteria calibrated to one contribution culture           | weight criteria per region, as Elastic did with its points table               |
| Program owner burns out                             | high-touch design at a cohort size the hours cannot cover | shrink the cohort or move to a lower-touch archetype                           |

## Reference

- [./references/program-archetypes.md](./references/program-archetypes.md) for the archetype comparison and sourced benchmarks from six published programs.
- [./references/charter-template.md](./references/charter-template.md) for the 12-question charter template, a filled example, and a counter-example of the version that fails.
- [./references/selection-rubric.md](./references/selection-rubric.md) for the scoring rubric, intake form, and rejection, renewal and offboarding message examples.
- samber/developer-relations-skills@developer-community-launch for upstream community launch decisions.
- samber/developer-relations-skills@developer-community-moderation for escalation and conduct enforcement.
- samber/developer-relations-skills@developer-community-health for measuring community-wide engagement.
- samber/developer-relations-skills@oss-contributor-onboarding for code-contribution pathways in open-source.
- samber/developer-relations-skills@developer-meetup-program for local user-group organizing.
