---
name: oss-sponsors-fundraising
description: Designs a maintainer-side open-source sponsorship program - the tier ladder and its pricing for individual and corporate sponsors, rewards that stay deliverable at ten times the sponsor count, funding-goal and sustainability framing, and the invoice-and-entity path a company needs before it can pay. Use whenever a maintainer asks how to get sponsors or funding for a project, sets up or fixes GitHub Sponsors, Open Collective or FUNDING.yml, writes sponsor tiers, rewards or a sponsorship page, wonders why nobody sponsors a widely used project, considers sponsorware, or wants a company to fund maintenance work - even if they only say the project is unsustainable. Not the company side - use samber/developer-relations-skills@oss-sponsors-brand-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# OSS Sponsors Fundraising

You design the sponsorship program of an open-source project: who is being asked, for how much, in exchange for what, through which platform, and how the maintainer stays able to deliver it in two years.

Findings that shape every decision below:

- Salary-shaped income comes from companies, not individuals: GitHub reports that in 2022 "nearly 40% of sponsorship funding came from organizations"; Filippo Valsorda measured typical individual-sponsorship income for a widely depended-on library at under $1,000/month.
- Every reward promised is recurring work for an already stretched maintainer: Tidelift's 2020 survey put burnout at 46% of professional maintainers, 58% for maintainers of widely used projects.

Getting paid also changes what the project can do. Tidelift's 2024 maintainer survey (400+ respondents) found 60% of maintainers unpaid, and paid maintainers 55% more likely to implement critical security and maintenance practices: signed releases with provenance 50% versus 28%, two-factor authentication 76% versus 68%. Use that when the maintainer feels asking for money is impolite.

Figures like these name their source inline or in the reference files; any figure marked **baseline** is this skill's own default, a starting point to argue with, never an industry standard.

If the user is a company deciding which projects to fund and at what tier, this is the wrong side of the table - route them to `samber/developer-relations-skills@oss-sponsors-brand-strategy` and stop.

## Interview

Ask one question at a time, multiple-choice where you can, and stop as soon as you know the project, the goal amount, and the honest delivery capacity. Confirm the rest as you design.

1. Which project, and what is your role - sole maintainer, one of a team, or a company employee maintaining it on work time?
2. What do you want the money to change: buy back hours, cover infrastructure costs, fund a specific deliverable, or replace a salary? Name a monthly number, even a rough one.
3. By what date does that money have to be arriving - this quarter, this year, no deadline?
4. Do you want a one-off win (a funded deliverable, a conference trip, a hardware bill) or a compounding asset that still pays in two years?
5. Who actually uses this - individual developers, companies building products on it, or both? How do you know?
6. Can you name three companies that depend on it, and how you know they do?
7. What is already in place: GitHub Sponsors, Open Collective, Ko-fi, a FUNDING.yml, nothing?
8. What is your effort ceiling: how much sponsor-facing work can you absorb per month, in a bad month - hours, not intentions? Would you sign a commitment you cannot walk back?
9. Do you have a legal entity, or would money come to you personally? Which country?
10. What surfaces do you control, with rough numbers: repository traffic, docs site, newsletter, social following, conference talks?
11. Is anything commercial attached already - paid support, a hosted product, an employer with a claim on the work?
12. What would you refuse to sell at any price?

Answers 3, 4 and 8 re-rank step 2's shape menu - carry them there instead of re-asking:

- Q3, a date inside this quarter: promotes gratitude and visibility, the only shapes that pay before they are finished being built.
- Q4, a compounding mandate: promotes the retainer and the visibility placement, both of which keep paying after the launch push stops.
- Q8, an effort ceiling of a couple of hours in a bad month: deletes the access program.
- Q8, a refusal to sign anything unwalkable: deletes the retainer.

Record the answers. If your harness has persistent memory, store the resulting program brief there; tier prices are effectively permanent on some platforms, and later sessions must not redesign the ladder from scratch.

## Step 1 - Test whether sponsorship is even the right instrument

Sponsorship is one funding instrument among five, opensource.guide's own inventory:

- Employment: open-source time written into a job.
- Individual crowdfunding.
- Project-level corporate sponsorship.
- Commercial revenue: support, hosting, premium features.
- Grants.

Individual sponsorship is also the slowest route to a living wage: the under-$1,000/month figure above is what it typically yields even for a widely depended-on library.

Say this out loud before designing anything:

- Q2 = "replace a salary" and the project has a few hundred users: recommend employment or a commercial tier, with sponsorship as a supplement - even though that is not what this skill builds.
- Q2 = buying back a day a week or covering costs: sponsorship fits well.

Check grants the same way: a project with a research, infrastructure or security angle often clears a grant faster than a hundred $5 sponsors. When it does, run step 1b alongside the rest.

Do not rank those five instruments against each other by efficiency here: a ranking would be false precision over a choice question 2 already made. A salary-replacement goal makes employment dominant whatever it costs to find, an infrastructure or security angle makes a grant dominant, and both verdicts hold at any effort level. The programs inside the grant lane, and the shapes inside sponsorship, do get ranked.

## Step 1b - Run the grant lane

A grant is not a larger sponsor. It is a fixed-term contract with an eligibility gate in front and a reporting duty behind: it ends on a date, and it pays against proof. Run it alongside the sponsorship program, never instead of it.

Qualify before writing. Four gates reject more applications than weak prose does, and interview answer 9 already settles two of them:

- **Licence.** Every program requires a recognised open-source licence, several extending it to documentation and research output.
- **Who can be paid.** Some contract with an individual, some need a legal entity, some pay an organisation only and expect a fiscal sponsor when the project has none.
- **Geography.** The restriction binds the recipient, not the code: residency preferences, national tax residency, sanctions exclusions.
- **Maturity and scope.** Infrastructure funds want a depended-on library and refuse prototypes, prototype funds want new work, science funds want demonstrated use in their own field.

Programs rank by money won per hour of application and compliance work. Five families: **direct** funds paying an individual, **cohort** security funds, **agency** infrastructure funds, **national** innovation funds, **foundation** science grants.

- efficiency: `direct > cohort > agency > national > foundation`
- value (money per award): `foundation > agency > national > direct > cohort`
- effort: `foundation > national > agency > direct > cohort` - a foundation wants a letter of inquiry, an invited proposal and an institutional signature, an agency runs months from application to contract, a direct fund is one form
- compliance cost: `national > foundation > agency > cohort > direct`

What this order starves: the foundation grants, the only ones funding years of named headcount. Promote them when the project already has an institutional home or a fiscal sponsor, and delete them when it has neither.

Write to the committee, not to the sponsor page. Step 5 sells a maintainer's credibility to a reader who already likes the project; a proposal is scored against published criteria by a reviewer reading dozens in a sitting.

- Lead with the dependency, not the story. Prevalence, criticality and who breaks if the project stops are scored criteria.
- Price the work in hours at a named rate, then map those hours to milestones you would accept being paid against, because you will be.
- Answer "why not the existing thing" explicitly. The open forms ask it outright, and a missing answer reads as no landscape research.

Plan the reporting before accepting. A sponsor renews on a thank-you post and churns quietly; a grant-maker withholds payment against a named report on a fixed schedule and reclaims what goes unspent. Charge that admin against the effort ceiling from question 8.

Gates per program, application fields, scoring criteria, post-award duties, and the programs that no longer accept applications are in [references/grant-programs-and-reporting.md](./references/grant-programs-and-reporting.md). Read it before naming a program to the user.

## Step 2 - Brainstorm the program shape, then choose one

Enter brainstorming mode. Sketch **two or three candidate programs** that could hit the stated number, then recommend one and say why the others lose. Get explicit agreement before pricing anything.

The four shapes are ranked by value returned per unit of maintainer effort - effort meaning recurring maintainer hours, obligations that never end, and how hard a published promise is to withdraw. Say the efficiency order out loud rather than leaving it implied by row order. The axes disagree, so read all of them; each line is descending on its own axis, highest first.

- efficiency: `visibility > gratitude > retainer > access`
- value (monthly income the shape can reach): `retainer > access > visibility > gratitude` - visibility overtakes access wherever placement traffic runs to tens of thousands of monthly views
- effort: `access > retainer > visibility > gratitude`
- compliance cost: `retainer > visibility > access == gratitude`

Effort in magnitudes:

- Gratitude: near-zero once the page exists.
- Visibility: about an hour per sponsor for a logo commit and a placement check.
- Access and retainer: both standing jobs.

- **Visibility program.** Company tiers priced against real placement traffic - README, docs site, homepage. Delivery is a logo commit; income scales with the audience the project actually has. Default first shape wherever the docs or README get measurable traffic.
- **Gratitude program.** Low tiers, no perks, one clear ask. Right for a project with many small users and a maintainer with no spare hours, and the base layer underneath any other shape.
- **Retainer program.** A handful of dependent companies pay for named commitments (response times, security triage, upgrade support). Fewest sponsors, largest cheques, most obligation.
- **Access program.** Sponsor-only content, early access, or sponsorware. The best-documented conversion on record and the highest recurring cost - it bolts a content business onto a maintenance job. Right only when an audience already exists.

- Split the two standing jobs on cadence: access ships whether or not anyone asked, while retainer work is triggered by a dependent company's occasional need - which is why the larger cheque also costs fewer hours and ranks above it.
- Justify the compliance tie: neither access nor gratitude commits the project to a named company or puts a third party's brand on its surfaces, and both can be withdrawn from new sponsors in one commit.
- The retainer tops the compliance-cost line: an entity, numbered invoices, tax handling, and a written commitment that is expensive to break. Visibility sits second: a published price is permanent on GitHub Sponsors, and a sponsor logo needs the refusal rule from step 8 before the first one appears.
- What this order starves: the retainer. It is the only shape that reaches salary-shaped income and the only one that obligates real delivery, so it tops the value line and the compliance line at once, and the ratio buries it every round. A maintainer who only ever obeys the efficiency line stays at coffee money permanently.
- Promote the retainer above everything when question 2's answer was "replace a salary", when three dependent companies can be named, and when an entity or fiscal host already exists.
- Delete rather than demote, and say which:
  - No entity and no willingness to use a fiscal host deletes the retainer.
  - No audience beyond the repository (no docs traffic, no newsletter, no talks) deletes access.
  - A README and docs with no countable traffic delete the visibility program, since placement that cannot be measured cannot be priced.
- Most working programs are a gratitude base plus one of the other shapes; recommend a combination only when the maintainer can service both halves.
- This order is a default, not a law: it shifts with context and with who executes it.
- Re-rank it against what you already know about this maintainer before presenting it:
  - An existing newsletter or conference audience promotes access, because the distribution is already built.
  - An employer already paying for the work removes the retainer's premise.
  - A team of three can service a shape a sole maintainer has to delete.

## Step 3 - Build the ladder for two buyers

A ladder serves two buyers that behave nothing alike:

- Individuals pay $5-$25 from their own pocket, decide in seconds, and want gratitude or a personal perk.
- Companies pay from a budget line, need an invoice and a named beneficiary, and want a benefit an approver can defend.

The placement-selling ladders in the reference file (Vue, Sindre Sorhus) put the individual/company boundary near $100/month; treat that split as a **baseline** and move it if the audience says otherwise.

These rules decide most of the ladder - the first four come from the published ladders in the reference file, the last two from GitHub's documentation:

- **Price company placement by the audience it reaches, not by generosity.** "Logo on a README with 20k monthly views" is a media buy an approver can sign off; "gold sponsor" is not. Sindre Sorhus publishes per-placement monthly view counts and prices against them.
- **Name tiers for the buyer.** "The Agency" or "Team" tells a company the tier is theirs; "Platinum" makes them guess - Caleb Porzio's own conclusion after testing his tiers.
- **Never put a partial-perk tier just below the tier that converts.** "If people have the option of paying $1-5/mo. instead of >$14, they will pay the lesser amount" (Porzio). A no-perk gratitude tier _below_ the perk tier is fine and even useful.
- **Expect one tier to carry the program.** In both individual ladders on record, a single tier drives conversion and the others catch generosity above and below it.
- **Treat published prices as permanent.** On GitHub Sponsors a published tier's price can never be edited - only retired and replaced, with existing sponsors left on the old tier. Price for two years from now; the platform ceiling is $12,000/month.
- **Keep the ladder short.** Three to five live tiers as a **baseline**; the platform allows ten published monthly tiers and nobody reads ten.

Reference ladders from Vue, Sindre Sorhus and Caleb Porzio, with prices and exact rewards, are in [references/tier-ladder-examples.md](./references/tier-ladder-examples.md) - including a weak ladder and why it fails. Platform limits, fees, payout and FUNDING.yml mechanics are in [references/platform-mechanics.md](./references/platform-mechanics.md); read it before naming a price or a platform.

## Step 4 - Size every reward against delivery, not appeal

For each reward, ask: what does this cost every month at ten times the current sponsor count? The ten-times multiplier is a **baseline** stress test, not a measured growth rate - it exists because the rewards that convert are exactly the ones that scale into a second job.

Rewards rank the same way shapes do, by what a sponsor buys against what it costs to keep delivering:

- efficiency: `README or docs placement > sponsor badge and thank-you post > early access to releases > private repository or quarterly office hours > monthly calls, priority support, bespoke work`
- value (what makes a company sign and renew): `monthly calls and priority support > private repository or office hours > early access > placement > badge and thank-you post` - for an individual sponsor that line reverses below early access, since the badge and the thank-you are the entire purchase
- effort: the three buckets below, in magnitudes.

- **Near-zero and safe:** name or logo in a `BACKERS.md`, README or docs placement, a thank-you post, a sponsor badge.
- **Bounded but real:** a private repository per tier, quarterly office hours, early access to releases.
- **A second job:** monthly calls, priority support promises, per-sponsor content, bespoke integrations.

What this order starves: the named commitments in that last bucket, which are the only rewards a company will pay retainer money for. Do not promote them into a tier perk - move them out of the ladder entirely and sell them through step 7, where the price matches the obligation.

Cut any reward that fails the ten-times test. Sponsor-only content and sponsorware, release to sponsors first, open-source at a published threshold, are the best-converting rewards on record and the most expensive to keep shipping. The mechanics, the release-trigger rule, and the things that must never be gated (security fixes, the core library, the documentation needed to use it) are in [references/tier-ladder-examples.md](./references/tier-ladder-examples.md).

## Step 5 - Write the ask as a bounded commitment

"Support my work" is not an ask. Every funder, from a $5 sponsor to a grant committee, answers the same five questions (opensource.guide's list):

- Why the project matters.
- What traction proves it.
- Why fund this over the alternative.
- What the money buys.
- How it can legally be disbursed.

Convert the goal into units a reader recognises - one maintenance day a week, the CI and code-signing bill, a named deliverable with a date. Set the first funding goal where it closes this quarter: a completed goal is worth more than an ambitious one stuck at 4% for a year.

Choose the goal type deliberately:

- A sponsor-count goal keeps income private.
- An amount goal publishes monthly revenue permanently and cannot be walked back.

If the user has a build-in-public practice, keep the two consistent.

Write the page in the maintainer's own voice, then run it through your preferred humanizer skill - sponsors buy the maintainer's credibility, and campaign copy spends it.

## Step 6 - Make the ask unavoidable, and the project machine-findable

Sponsorship money arrives through three paths, each needing its own configuration and each worth a different amount for what it costs:

- efficiency: `FUNDING.yml and manifest funding metadata > funding links on the surfaces users already touch > health signals that survive a funder's shortlist`
- value (money the path can route to the project): `health signals > funding links > FUNDING.yml`
- effort: `health signals > funding links > FUNDING.yml` - a Scorecard-driven cleanup is a quarter of work, the links are an hour, the file is near-zero

Do the first two now, in that order. What this order starves is the health-signal work, which is what a corporate fund or foundation program actually reads before allocating; promote it when such a program is the named target, and treat the rest of this section as its prerequisite.

- **The ask people read.** A funding link within two clicks of every surface a user already touches: repository sponsor button, README, docs footer, release notes, CLI or error output where appropriate. A page nobody reaches converts nobody.
- **The graph funders scan.** Sophisticated funders allocate across their dependency tree automatically - Sentry's $500,000 programme reached "95% or greater coverage" of its fundable dependencies at $4-$10 each, and was "likely their first and sole sponsor" for many of them. Being present in that scan costs one file: `.github/FUNDING.yml`, plus package-manifest funding metadata where the ecosystem supports it.
- **The shortlist a program builds.** Corporate funds rank candidates on machine-readable health data before any human looks - OpenSSF Scorecard and Criticality Score, dependent counts, contributor diversity. A missing or dead funding link is a hard filter at that stage, not a low score: an unfundable project is dropped whatever its criticality.

Verify every funding link resolves, and check the org-level fallback (`{owner}/.github`) is not pointing somewhere stale. Dead sponsorship links are common and silently cost the whole channel.

The signals those scanners read, the eligibility rules of employee-nominated funds, and a self-audit pass over them are in [references/funder-scan-and-eligibility.md](./references/funder-scan-and-eligibility.md). FUNDING.yml keys and syntax are in [references/platform-mechanics.md](./references/platform-mechanics.md).

## Step 7 - Open the corporate lane

Individual tiers will not reach a salary-shaped number; the companies that depend on the project will. This lane is a different motion, not a bigger tier.

Companies route money through four mechanisms, each won differently:

- Automatic dependency-share: won by being findable - step 6 already did this.
- Judgement-based strategic sponsorship: won by being visibly load-bearing for that company's product.
- Employee-nominated funds: won by the engineer who already files your issues nominating you.
- Foundation or pledge membership: won by being a foundation's recipient, not by pitching.

Only the second is won by outreach; know which one you are aiming at before writing to anyone.

- efficiency: `dependency-share > employee-nominated funds > strategic sponsorship > foundation membership`
- value (cheque size per company won): `strategic sponsorship > foundation membership > employee-nominated funds > dependency-share`
- effort: `foundation membership > strategic sponsorship > employee-nominated funds > dependency-share` - membership is a quarter or more of process, a strategic pitch is a week per target, a nomination is one message to an engineer who already knows you, and dependency-share is the near-zero file from step 6

Strategic sponsorship is the same shape step 2's ranking starves, arriving one layer down: it is where the retainer-sized cheques live, and the efficiency line buries it every time. Spend the week per target only against companies whose product visibly depends on the project.

The mechanisms and their numbers are in [references/corporate-sponsorship-path.md](./references/corporate-sponsorship-path.md).

Run the outreach for that second mechanism as a sequence:

1. Identify dependent companies from dependency graphs, public repositories, job posts naming the technology, and issues filed from company domains.
2. Address a person with a budget and an exposure - platform lead, staff engineer, head of security - never a generic address.
3. Frame the ask against a budget line that already exists: supply-chain security, marketing reach, or engineering support. Open Source Pledge members commit more than $2,000 per employed developer per year, and that money is looking for legible recipients.
4. Sell named commitments, not goodwill. Valsorda's list of what a company actually buys:
   - Two-factor authentication and mandatory code review.
   - Ecosystem-keeping-up updates.
   - Reliable review and merge timelines.
   - Support on filed issues.
   - Careful handling of security reports.
   - "even a succession plan."
5. Clear procurement before pitching: an entity, a tax form, a numbered invoice and bank details get processed; a donate button does not. Invoiced sponsorships through GitHub carry a $5,000 minimum per invoice, so smaller asks route through a fiscal host instead.
6. Plan the renewal: budgets are annual, so a proof-of-value note mid-cycle is part of the program, not a courtesy.

Check that the payment route also survives, not just that it works today. A fiscal host is itself a continuity risk: the Open Collective Foundation's 2024 dissolution gave its 600+ collectives seven months to move their funds.

When several maintainers share the money, decide who authorises spending before the first payment lands, and separate "paid to keep the lights on" from "paid to decide direction" - the Django Software Foundation funds a Fellowship for triage and administrative work for exactly that reason. A fiscal host's public ledger also exposes each maintainer's compensation; say so before choosing one.

Outreach templates, the one-page prospectus shape, and the payable checklist are in [references/corporate-sponsorship-path.md](./references/corporate-sponsorship-path.md). Entity and host continuity detail is in [references/funder-scan-and-eligibility.md](./references/funder-scan-and-eligibility.md); the full entity/foundation decision belongs to `samber/developer-relations-skills@oss-governance`.

## Step 8 - Write down what money does not buy

Publish these boundaries alongside the tiers, before the first sponsor arrives:

- Sponsorship buys visibility, gratitude and named commitments - never roadmap control or merged pull requests. Contributions are judged on technical merit whether or not the author pays.
- Priority _triage_ can be sold; priority _outcomes_ cannot.
- The sponsor list, the roadmap and the review queue stay separate artefacts.
- A maintainer who declines funding to protect autonomy has made a legitimate choice, not a mistake.

State any conflict-of-interest rule now: which sponsors would be refused, and who decides.

## Step 9 - Measure the program, not the applause

| Question              | Metric                                                           | Ignore                  |
| --------------------- | ---------------------------------------------------------------- | ----------------------- |
| Is it growing?        | Recurring monthly amount, trend over 6 months                    | Cumulative total raised |
| Who is paying?        | Sponsor count split individual vs company                        | Stars, followers        |
| Is it durable?        | Monthly churn; median tier; share of income from the top sponsor | One-time spikes         |
| Does the ask work?    | Conversion from each surface carrying the funding link           | Page views              |
| Was the promise kept? | Funded commitment shipped on time; rewards delivered             | Thank-you replies       |

**Pass threshold (self-set)**, checked at 90 days and then quarterly:

- Recurring monthly income grew versus the previous quarter.
- Every published reward was delivered on time.
- No single sponsor exceeds 50% of income.
- At least one company tier is occupied, if any company depends on the project.

The 50% line comes from freelance client-concentration practice rather than from open-source funding norms; say so if the user treats it as a rule. Failing it is a concentration risk to fix before growing; failing the fourth condition means the corporate lane in step 7 was never really opened.

Diagnose income problems by where the ask fails:

- Income flat while traffic grows: the ask placement is wrong (step 6).
- Ask everywhere and income still flat: the reward is wrong for the buyer (steps 3-4).

## Invocation examples

Typical asks, and where each one enters the workflow:

- _"I maintain a Rust crate with 900k monthly downloads and no funding page - how do I set this up?"_ → interview, then steps 1-6 in order; hold step 7 until dependent companies can be named.
- _"Three funded startups ship our library and nobody sponsors us."_ → steps 6 and 7 first. When usage is proven and income is zero, the ladder is rarely the problem; findability and the absence of a company tier usually are.
- _"Should I release the new CLI to sponsors first for a month?"_ → step 4, then the sponsorware rules in [references/tier-ladder-examples.md](./references/tier-ladder-examples.md).
- _"Rewrite our tiers, the top one is $50."_ → step 3, checked against the weak ladder and its diagnosis in [references/tier-ladder-examples.md](./references/tier-ladder-examples.md).
- _"A sponsor is asking us to prioritise their issue."_ → step 8, and publish the boundary before the next tier goes live.

## Deliverable

Produce a program brief, presented section by section with agreement on each before the next.

```markdown
# Sponsorship program - <project>

## Goal monthly target, what it buys, by when

## Instrument fit why sponsorship, and what else was recommended

## Audience individual vs company mix, named dependent companies

## Ladder tiers, prices, rewards, delivery cost per reward

## Platform where money is received, fees, entity, payout path

## Ask page copy, funding goal and type, surfaces carrying the link

## Corporate lane target list, contact, pitch, paperwork status

## Boundaries what sponsorship does not buy, refusal rules

## Measurement metrics, review date, pass threshold
```

## Common failure modes

- **Publishing a price you will regret.** Unchangeable on the main platform; a $10 top tier caps the program until it is retired and replaced.
- **A ladder for individuals only.** The money is in company tiers, and a company cannot buy a tier that does not exist.
- **Rewards that outgrow the maintainer.** Monthly calls at 12 sponsors are pleasant; at 120 they end the program.
- **A sponsorship page nobody can reach.** No sponsor button, no README link, no FUNDING.yml - invisible to both humans and dependency-graph funders.
- **Selling roadmap influence.** Converts fastest, destroys neutrality, and invites every other user to distrust the review queue.
- **A goal that never moves.** An unreachable first target reads as a project nobody supports; set one that closes this quarter.
- **Gating the project itself.** Sponsorware on convenience is fine; a paywall on the library, its security fixes or its documentation is a licence-adjacent betrayal of the users who got you here.
- **Going quiet after the money arrives.** Sponsors renew on evidence; a silent quarter is a cancelled sponsorship.

## References

- [references/platform-mechanics.md](./references/platform-mechanics.md) - tier and goal limits, fees, invoiced minimums, FUNDING.yml keys, fiscal hosting, dependency-share platforms.
- [references/tier-ladder-examples.md](./references/tier-ladder-examples.md) - three real ladders with prices and rewards, a weak ladder and its diagnosis, sponsorware rules, and a filled example.
- [references/corporate-sponsorship-path.md](./references/corporate-sponsorship-path.md) - the four funding mechanisms, target identification, outreach email (a weak one and a strong one), prospectus shape, payable checklist, renewal note.
- [references/funder-scan-and-eligibility.md](./references/funder-scan-and-eligibility.md) - the health and payability signals funder tooling reads, employee-nominated fund eligibility rules, entity and fiscal-host continuity risk, and a self-audit pass.
- [references/grant-programs-and-reporting.md](./references/grant-programs-and-reporting.md) - eligibility gates and published sizes per grant program, the recurring application fields, published scoring criteria, post-award reporting duties, and the closed programs.
- `samber/developer-relations-skills@build-in-public` for the transparency practice a public revenue goal commits to.
- `samber/developer-relations-skills@readme-optimization` for the README real estate the ask competes for.
- `samber/developer-relations-skills@oss-distribution-strategy` for growing the audience a visibility tier is priced against.
- `samber/developer-relations-skills@devtools-business-model` for whether sponsorship income can substitute for a revenue model at all.
