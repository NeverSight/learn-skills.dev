---
name: oss-sponsors-brand-strategy
description: Builds a company's open-source sponsorship portfolio - which projects and maintainers to fund, through which allocation model, at what amount each, and how to prove it worked. Use whenever a company, OSPO, DevRel lead or engineering leader asks which open-source projects to sponsor, how much to budget for open-source funding, whether sponsoring maintainers is worth it, how to run an employee-nominated FOSS fund, how to fund dependencies at scale, how to pick a sponsorship tier on a maintainer's ladder, or how to measure the return on money paid to maintainers - even if they only say they want to give back. Not the maintainer side of raising sponsorship - use samber/developer-relations-skills@oss-sponsors-fundraising. Not event sponsorship.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# OSS Sponsors Brand Strategy

You decide where a company's open-source money goes: what mandate it serves, which projects and maintainers receive it, how much each one gets, and what the company can honestly claim in return.

Hold two facts through every step:

- Sponsorship returns on two axes at once: "brand marketing, and securing our supply chain," in Sentry's David Cramer's words on the Open Source Pledge member page. The two mandates select different projects, so a portfolio that never picks a primary one optimizes for neither.
- Developer audiences read sponsorship as a signal about the company. Money that arrives with expectations of influence costs more trust than it buys.

Route the user elsewhere when this is the wrong table:

- A maintainer looking for sponsors → `samber/developer-relations-skills@oss-sponsors-fundraising`.
- Conference, meetup or hackathon sponsorship tiers → `samber/developer-relations-skills@developer-event-sponsorship`.

Every figure below carries one of two labels:

- **(published)**: a program that ran disclosed it. Figures drift, so re-check before quoting.
- **(self-set)**: this skill offers it as a starting default, never a market rate.

See [references/sourced-numbers.md](./references/sourced-numbers.md) for the source behind each figure. Never present a self-set default to a finance reviewer as a market rate; that is the claim that gets a portfolio sent back.

## Interview

Ask one question at a time, multiple-choice where you can, and stop once you know the mandate, the budget and the ecosystem. Confirm the rest as the portfolio takes shape.

1. Who is asking, and whose budget pays - open-source program office, DevRel/marketing, engineering or security leadership, or a founder?
2. What do you want this money to change: reduce supply-chain exposure, earn reach and credibility with developers, engage your own engineers, or meet a values commitment you have already made publicly? Rank your top two.
3. How much per year, and how many developers do you employ? Is the budget new or moved from an existing line?
4. By what date does this have to be live and showing something - this budget cycle, next one, no deadline?
5. Do you want a one-off win (an announcement, a single funded project, a pledge signature) or a compounding asset that is stronger in three years?
6. What is your effort ceiling: who administers this, for how many hours a month, and would you sign a multi-year agreement you cannot exit early?
7. Do developers buy or choose your product, or do you sell to someone else? (This decides whether reach is a marketing return or an employer-brand return.)
8. Which ecosystems is your stack in, and do you have an SBOM, a lockfile, or a repository I can resolve dependencies from?
9. What is already live - sponsorships, foundation memberships, a public pledge, a one-off donation someone made two years ago?
10. What does finance require: card payment or purchase order only, invoice minimums, vendor onboarding, restricted geographies?
11. Should employees participate - nominating projects, voting, contributing on work time?
12. What are the redlines: licenses, projects run by competitors, projects maintained by your own staff, anything legal has flagged?
13. Who reviews this, and when is your budget decided each year?

Answers 4, 5 and 6 re-rank step 2's model menu; carry them there instead of re-asking:

- Answer 4 (deadline inside this budget cycle): promotes breadth, the only model that goes live without a per-project decision.
- Answer 5 (compounding mandate): promotes depth and foundation membership, both worth more in year three than in year one.
- Answer 6 (effort ceiling of a few hours a month): deletes the employee-nominated fund.
- Answer 6 (refusal to sign a multi-year agreement): deletes foundation membership.

If your harness has persistent memory, store the resulting mandate, budget split and target list. Sponsorships renew annually and the next session must not re-derive the portfolio from scratch.

## Step 1 - Name the mandate before the money

Pick one primary mandate and one secondary. The primary breaks every tie later - which project wins the last $5,000, and which metric decides renewal.

| Mandate                  | Usually owned by        | Default allocation model                                               | What renewal is judged on                                      |
| ------------------------ | ----------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------- |
| Supply-chain assurance   | Engineering or security | Breadth across the dependency graph                                    | Coverage of fundable dependencies; reachability of maintainers |
| Reach and credibility    | DevRel or marketing     | Depth on a few projects your buyers already use                        | Verified placements; referral traffic; unaided mention         |
| Internal engagement      | OSPO or people team     | Employee-nominated fund                                                | Employees contributing; nominations per cycle                  |
| Public values commitment | OSPO or leadership      | Whatever the commitment names - a per-developer floor, foundation dues | The commitment's own terms: floor met, annual report published |

Keep the last two rows apart even though they often share an owner:

- An engagement mandate targets projects your employees already touch.
- A values mandate targets whatever the public commitment named, judged on that commitment's own terms.

Do not rank the mandates against each other. They are four different goals, not four routes to one, and the answer to the interview's second question picks the primary outright - a ratio here would be false precision dressed as analysis. The allocation models in step 2 are routes to whichever mandate wins, and those do get ranked.

Reach behaves differently depending on who buys the product:

- Developers choose or influence the purchase: placement on a project's README, docs or homepage is a media buy and can be priced like one.
- The company sells to non-developers: reach mostly returns employer brand and recruiting. Say that plainly and size the budget against hiring, rather than inflating a marketing case nobody will believe at review time.

## Step 2 - Brainstorm the portfolio shape, then choose one

Enter brainstorming mode before naming a single project:

1. Sketch two or three candidate portfolios, each with its allocation split, the internal work it takes to run, and what it deliberately fails at.
2. Recommend one, and explain why the others lose.
3. Get explicit agreement before building any target list.

The four models - with the numbers real programs published - are in [references/allocation-models.md](./references/allocation-models.md). They are ranked here by value returned per unit of internal effort, effort meaning administrator hours, procurement and legal review, per-project decisions that recur every year, and how hard the commitment is to exit. Say the efficiency order out loud rather than leaving it implied by row order; each line below is descending on its own axis, highest first.

- efficiency: `breadth > depth > foundation membership > employee-nominated fund`
- value (what the model buys at its best): `depth > employee-nominated fund > foundation membership > breadth`
- effort: `employee-nominated fund > depth > foundation membership > breadth`
- compliance cost: `foundation membership > depth > employee-nominated fund > breadth`

Effort in magnitudes:

- Breadth: near-zero once the resolver runs.
- Foundation membership: a quarter of procurement and legal, then near-zero.
- Depth: about a week per project to select, clear and brief, plus a renewal conversation every year.
- Employee-nominated fund: a standing job - a cycle to run, eligibility to check, a vote to administer, a result to communicate.

- **Breadth**: small automatic amounts across the whole dependency graph. Near-zero discovery cost, near-zero visibility. Default first motion unless step 1's mandate table names another one for the primary mandate.
- **Depth**: a short list funded at amounts a maintainer can plan around. Buys the only named maintainer relationship and the only verifiable placement in this menu.
- **Foundation or consortium membership**: dues to an organization that redistributes. Buys governance access, no individual relationship.
- **Employee-nominated fund**: a fixed amount per cycle, nominated and voted internally. Buys engagement and a defensible selection story, targets poorly. This one has a published method to point at - the FOSS Contributor Fund, documented by Duane O'Brien and Mandy Grover (_Investing in Open Source: The FOSS Contributor Fund_, O'Reilly, 2021).

- Read the compliance-cost line as the review triggered and the reversibility spent:
  - Membership: signs a multi-year agreement legal has to review; the company cannot quietly exit.
  - Depth: onboards each maintainer as a supplier (tax forms, sanctions screening, invoiced billing terms); a public sponsorship is embarrassing to drop.
  - Employee-nominated fund: needs a published eligibility and conflict-of-interest rule plus employee disclosure, but no third-party contract.
  - Breadth: card-paid through one platform and reviewed once.
- What this order starves: the employee-nominated fund. It tops the effort line and buys the one return no other model buys at all, so the ratio puts it last every round and a program that only obeys the efficiency line will never have an engaged engineering organization behind it. Promote it above everything when internal engagement is the primary mandate from step 1 - the ratio cannot select it, because the thing it buys does not appear on any other row.
- Delete rather than demote, and say which:
  - Finance that pays only by purchase order against an invoice minimum deletes breadth, unless a fiscal host or platform aggregator can bill the whole motion on one invoice - a $10/month sponsorship never clears a purchase order.
  - No employee participation on work time deletes the nominated fund.
  - No foundation governing anything in the stack deletes membership; joining one for adjacency is dues paid for a room nobody in the company sits in.
- Most working programs run breadth plus one other motion. Recommend a single model only when the budget is too small to split meaningfully.
- This order is a default, not a law; it shifts with context and with who executes it. Re-rank it against what you already know about this company before presenting it:
  - An OSPO already running a nomination cycle promotes the fund, because the standing cost is already paid.
  - A live foundation membership promotes depth inside that foundation's projects.
  - Buyers who are themselves developers promote depth, since placement becomes a media buy rather than a gesture.

## Step 3 - Size the budget

Quote both per-head figures, because they say different things:

- The industry pledge asks members for more than **$2,000 per full-time-equivalent developer per year** (published) - a floor for a company that wants to say it funds open source, not a market rate.
- The one company that published what it actually paid reported **$3,700 per developer**, calling it "quite reasonable compensation for the value we receive" (published - a single self-reported data point).

The gap between them is the argument for going above the floor.

Then split the budget:

- A percentage to breadth.
- A percentage to depth or the nominated fund.
- A reserve of 10-20% (self-set) for opportunistic funding - a maintainer in trouble, an incident response, a project that suddenly becomes load-bearing.

Check the split against payment mechanics before publishing it, since invoiced corporate payments carry minimums that a $10/month sponsorship cannot clear (see step 7).

Decide what counts before you publish a total. A pledge-style program refuses to count four payment categories as open-source funding (published):

- Money to a company-controlled project.
- Software that benefits the payer exclusively.
- A maintainer the company already employs.
- An arrangement returning substantial benefits beyond minimal acknowledgment.

Budgets get padded with all four; count them on a separate line, or the public number will not survive scrutiny.

## Step 4 - Build the candidate list

Do the mechanical half of discovery first - it is cheap, and it usually surprises the room. If your environment can fetch URLs and read the company's manifests:

1. Resolve the full dependency tree, direct and transitive, from a lockfile, an SBOM, or a public dependency-resolution API.
2. Map each package to its source repository, then deduplicate - one maintainer often stands behind a dozen packages.
3. Pull health signals per repository: maintenance activity, contributor count and organizational diversity, release cadence.
4. Discover a funding destination for each: the repository's funding manifest, the owner's org-level fallback, and registry funding metadata.
5. **Verify every funding link resolves** before it enters the list. Funding pages 404 and maintainers leave programs; never carry a funding URL from memory.

Every row of the list is a claim about someone else's project that the company will publish money against. Four rules keep it honest, each one a failure that hand-collected dependency lists produce:

- **Measure, never estimate.** Download counts, maintenance activity and maintainer counts all have APIs. Hand-collected figures have claimed five-plus maintainers for a package whose registry publish rights list one, and zero downloads for a package moving 164 million a week.
- **Score fragility on publish rights, not repository contributors.** They are different populations - fragility depends on who can ship a release, not on who has ever merged a commit - and the contributor graph overstates the count.
- **Mark what you could not assess.** Every candidate resolves to assessed-fine, assessed-flagged, or not-assessable-with-a-reason. Some registries publish no maintainer list at all; a row with missing data is not a clean row.
- **Carry the denominator.** Report "resolved 412 of 470 dependencies; 58 had no source repository", never a bare percentage - coverage of a total nobody defined survives no audit.

The exact endpoints, manifest paths, fallback rules and scoring inputs are in [references/target-discovery-and-scoring.md](./references/target-discovery-and-scoring.md). If your environment cannot browse, ask the user to export a dependency list and work from it, and say which health signals you could not check.

The judgement half has no API: which projects reach the audience you want, on what surface, at what volume. Ask the maintainer for placement traffic when it matters - the maintainers who sell placement usually publish or share those numbers.

## Step 5 - Rank the list, then cut it

Score each candidate on four axes:

- Exposure: how much of your stack depends on it.
- Fragility: how close it is to one person stopping.
- Audience fit: do its users look like your buyers or your future hires.
- Relationship value: would you want this maintainer's phone number during an incident.

The four axes and their mandate weights are self-set; say so, and let the user reweight them. Payability is not a score: a project with no way to receive money is out, however critical, and is instead a candidate for contribution rather than cash.

Then cut hard. A portfolio is only as good as the annual review it can survive; twelve depth sponsorships that get renewed thoughtfully beat forty that get rubber-stamped (self-set). For the breadth motion, report the actionable minimum - the fewest destinations that cover the most dependencies.

Flag the disqualifiers explicitly rather than silently dropping them:

- Vendor-owned projects where the money is a rounding error.
- Projects maintained by your own employees, if you have a conflict-of-interest rule.
- Projects that can only take a support contract when your budget pays one-off.
- Anything with a live conduct or security controversy the brand would attach to.

## Step 6 - Set the amount per target

Take amounts from the maintainer's published ladder, never from a number that felt right. Read what each tier actually grants, then pick the tier that matches the mandate:

- **Supply-chain targets**: the smallest recurring amount is usually correct across many projects; coverage is the goal, not prominence.
- **Reach targets**: pick the tier whose placement is on a surface with real traffic, and price it against that audience. A logo in a backers file nobody opens is not a media buy at any price.
- **Strategic targets**: go above the ladder with a custom or invoiced amount when the project is load-bearing for your product. One program's published depth allocations ran from $1,750 to $15,000 per project per year (published) - the spread is the lesson; depth does not mean uniform.

Check two constraints before promising anything:

- A tier's rewards are recurring work for one person; never request a benefit the maintainer will resent in six months.
- Fund a foundation instead of an individual, when the project's governance already routes money that way.

## Step 7 - Clear procurement before announcing anything

Check the payment path before any target list is final - a portfolio designed around payments finance cannot make is dead on arrival. The figures below come from platform billing documentation and fiscal-host fee schedules; re-check before quoting. Sources and the full rules are in [references/allocation-models.md](./references/allocation-models.md).

- Invoiced corporate billing on the main sponsorship platform has a **$5,000 minimum per invoice**, payable in 30 days, with a 3% service fee and a 3-year agreement term. Below that minimum, the company pays by card or routes money through a fiscal host instead.
- **Switching an organization to invoiced billing cancels its existing sponsorships**, which then have to be re-established. Sequence the switch before the first sponsorship, never after.
- Fiscal hosts take a percentage (commonly 3-10%) and publish a ledger, so every payment is visible.
- Vendor onboarding, tax forms and sanctions screening apply to individual maintainers exactly as they do to suppliers - start that paperwork before you promise a date.
- Whether the spend books as marketing, engineering or charitable giving changes its tax treatment and its approval path. Route that question to the company's finance and legal teams; state the options, never give the answer.

## Step 8 - Publish the policy and the conduct rules

Write these down before the first payment, and publish them where maintainers and employees can read them. An unpublished policy reads as favouritism from the outside.

- Sponsorship buys visibility, sustainability, and a relationship - never roadmap position, merged pull requests, or priority outcomes. Priority triage can be negotiated; priority outcomes cannot.
- No pressure on a maintainer to accept money, to advertise the sponsorship, or to produce gratitude on a schedule.
- Employees who publicly advocate for a project the company funds disclose the relationship.
- State the eligibility and conflict-of-interest rules: which projects qualify, whether employee-owned projects are excluded, who decides, and how a decision is appealed.
- Never shame a project that has no funding link or declines the money. Some maintainers refuse funding deliberately to protect their autonomy.
- Say whether a sponsorship is recurring or one-off. A sponsorship silently dropped at budget close does more relationship damage than one that was never started.

The full policy skeleton and a nomination-process template are in [references/policy-and-measurement.md](./references/policy-and-measurement.md).

## Step 9 - Measure, review, renew

Attribution is weak by nature: nobody clicks a README logo and buys. Measure presence and relationship health instead, per mandate, and refuse to build a last-click case that will not survive its first audit.

| Mandate      | Measure                                                                                                                         | Ignore                           |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| Supply chain | Share of fundable dependencies covered; dormant-dependency count; response time on issues you file                              | Total dollars given              |
| Reach        | Placements live and verified; referral traffic from placement URLs; unaided mentions in developer surveys and community threads | Impressions estimated from stars |
| Internal     | Employees contributing per cycle; nominations submitted; participation rate                                                     | Fund size                        |

**Pass threshold** (self-set), checked at 12 months and then annually:

- Every placement you paid for is live and verified.
- At least 80% of fundable direct dependencies are covered, if supply-chain is the primary mandate.
- Every depth sponsee has at least one documented interaction beyond the payment.
- No policy breach was raised by a sponsee.
- A renewal decision was made for every target before budget close.

Iterate on the portfolio until it passes, then re-run the check each year. On the 80% line, the only company to publish a higher coverage number reported "95% or greater" and described itself as the first to approach 100% (published, self-declared); present anything above 80% as ambitious, not standard.

Publish a short annual report of where the money went. The pledge's published format is the cheapest one to copy (published): the year, the developer count, the total paid, and the amount per recipient. It is the part maintainers and developers actually read, and re-publishing it each year is what turns a one-off into a program.

## Invocation examples

A tier question asked in isolation is usually a mandate question nobody has asked yet. Answer the narrow question the user brought, then say which step of the portfolio it belongs to and offer the rest.

| What the user says                                                | Where to start                               | What comes back                                                                                             |
| ----------------------------------------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| "We have $80k for open source next year. Where should it go?"     | Interview, then step 1                       | The full portfolio brief below                                                                              |
| "Should we sponsor <project> at the $500 or the $2,000 tier?"     | Step 6, after one question about the mandate | The tier that matches the mandate, the surface it lands on, and the traffic question to send the maintainer |
| "Our CTO wants a FOSS fund like the one at <company>. Set it up." | Step 2, then the nomination rules            | The nominated-fund design: amount per cycle, eligibility filters, who nominates, who votes                  |
| "Which of our dependencies can we even pay?"                      | Step 4 only                                  | A verified destination list deduplicated by maintainer, plus the count of dependencies each one covers      |
| "Legal wants to know what we get for this."                       | Step 8 and step 9                            | The policy language on what sponsorship does not buy, and the metrics per mandate                           |

Say what you could not check. "Resolved 412 of 470 dependencies; 58 had no source repository" is a usable answer. A clean-looking list with a silent gap in it is not.

## Deliverable

Produce a portfolio brief, presented section by section with agreement on each before moving on.

```markdown
# Open-source sponsorship portfolio - <company>, <year>

## Mandate primary and secondary, and what breaks ties

## Budget total, per-developer check, split by model, reserve

## Model chosen allocation model(s) and what they deliberately fail at

## Targets ranked table: project, why, exposure, amount, destination, verified

## Amounts per target with the tier it buys and the surface it lands on

## Procurement payment path, minimums, paperwork status, owner

## Policy what sponsorship does not buy, eligibility, conflicts, disclosure

## Measurement metrics per mandate, review date, pass threshold

## Renewal decision date, what would end each sponsorship
```

## Common failure modes

- **Funding the famous project instead of the fragile one.** Nomination votes and gut feel both drift toward projects that already have money; deliberately surface the underserved ones.
- **Announcing before procurement clears.** A promised sponsorship stuck behind vendor onboarding for four months is a broken promise in public.
- **Switching billing after sponsoring.** The switch cancels live sponsorships, and maintainers receive a cancellation email that reads as a withdrawal.
- **Buying a placement nobody sees.** A tier chosen by name rather than by the surface and traffic it grants.
- **Asking for influence.** The fastest way to convert a trust asset into a story about a company buying open-source projects.
- **Sponsoring a dead project.** No commits in eighteen months means the money changes nothing; check maintenance signals before, not after.
- **One-off giving dressed as a program.** A single announcement with no renewal date reads as a marketing stunt to the exact audience it targeted.
- **Unverified funding links.** Paying into a stale destination, or listing a maintainer who left the platform, wastes the budget silently.

## References

- [references/sourced-numbers.md](./references/sourced-numbers.md) - every figure this skill uses, split into published and self-set, each with its source. Read before quoting any number.
- [references/allocation-models.md](./references/allocation-models.md) - the four models with published numbers, a worked budget split, payment mechanics and minimums, and a weak portfolio diagnosed line by line.
- [references/target-discovery-and-scoring.md](./references/target-discovery-and-scoring.md) - dependency resolution and health endpoints, funding-link discovery and verification, the scoring rubric, and a worked shortlist next to the star-ranked one it replaces.
- [references/policy-and-measurement.md](./references/policy-and-measurement.md) - the public policy skeleton, nomination process, annual report shape, a good and a bad outreach note, and the measurement table's layout.
- `samber/developer-relations-skills@oss-sponsors-fundraising` - the maintainer side of the same transaction.
- `samber/developer-relations-skills@developer-event-sponsorship` - conference and hackathon sponsorship.
- `samber/developer-relations-skills@oss-governance` - how a funded project's governance routes money.
- `samber/developer-relations-skills@build-in-public` - publishing the annual report the program produces.
- `samber/developer-relations-skills@open-source-company-strategy` - the company-side gates this funding decision has to clear.
- `samber/developer-relations-skills@devrel-budget-allocation` - the line item this sponsorship program draws against.
