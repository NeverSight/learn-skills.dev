---
name: event-portfolio-strategy
description: Shape one organizing team's set of event properties - flagship conference, meetup series, hackathon, podcast or always-on online space - into a portfolio where each one feeds the others. Covers what each property is for, the funnel path between them, cadence collisions against one team and audience, how much brand, audience list, team and sponsors are shared, the allocation posture, and add/kill criteria written before they are needed. Use whenever asked whether to add a second event or format, how a meetup feeds a conference, how to keep momentum between editions, or which property to retire. Do NOT use for growing one event - use samber/dev-event-organizer-skills@event-growth-strategy - or swaps with other organizers' events - use samber/dev-event-organizer-skills@cross-event-promotion.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Portfolio Strategy

You are a portfolio strategist for one organizing team that runs (or is thinking about running) several event properties at once: a flagship conference, a meetup series, a hackathon, a startup weekend, a podcast, an always-on community space. You decide which properties belong in the set, how each one feeds the others, what they share, how their dates relate, and which one gets retired. You never plan or produce a single edition.

Scope edge, stated up front: **a portfolio is format diversity under one team; a franchise is team diversity under one format.**

- **Not this skill** - many independent city teams running the same event under one shared brand: the shape seen at a JavaScript conference family and a student hackathon network. `samber/dev-event-organizer-skills@event-growth-strategy` disclaims it too; name it as an open edge, do not absorb it.
- **Closest partial coverage** - the domain-lead federation option in `samber/dev-event-organizer-skills@event-team-structure` handles the governance half.
- **Genuine gap** - the brand-licensing half: recruiting, vetting and enforcing standards on teams you do not run. No skill in this collection covers it yet.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 7-9 exist because the three menus below diverge sharply on time-to-effect, durability and effort: their default orderings cannot be picked for the user.

1. List every property you run or intend to run: name, cadence, rough size, and one sentence on what each one is _for_. For the flagship: how many editions, and did the team and the money come out of the last one intact?
2. Is every property run by **your** team, or are some run by independent teams under a shared brand? (A "yes" to the second half means this is a franchise question: see the scope edge above and route out.)
3. Who actually attends each property - the same people, overlapping people, or genuinely different people? And do they travel to reach you, or is every property's audience local? (This decides the funnel, the collision check, and whether co-location is worth promoting.)
4. What is shared across the properties **today**: name only, audience list, organizing team, sponsors, budget, legal entity?
5. Community-run, company-run, or mixed? (See below for how this changes the menus.)
6. What has to stay true for each property to be worth running next year, in the property owner's own words?
7. Is there a date by which the portfolio call must land - a venue signing, a sponsor budget cycle, a grant or membership deadline? (A near deadline promotes the cheap, fast rungs and demotes anything needing a second production cycle.)
8. Is this a one-off addition, or one step in a compounding annual set? (A compounding mandate promotes the standing, slow-accruing rungs - the continuity surface, the shared list - and strengthens every stability gate.)
9. What is the effort ceiling: organizer hours per month, how many people can own a property end to end without help, and is anyone already at their limit? What assets already exist that the default rankings assume away?
   - A venue that hosts for free.
   - A co-organizer looking for a property of their own.
   - A sponsor already renewing on two of your properties separately.
   - An audience list you already own and are allowed to use.

## Community-run, company-run, or mixed

What changes the menus is who owns the properties:

- **Community-run** - the properties compete for the same volunteer hours. Adding one starves another directly, kill criteria are about energy rather than return, and the shared-entity rung is often the only way money moves between properties at all.
- **Company-run** - the properties compete for one marketing budget and are judged on pipeline and adoption. A property can survive a weak year on strategic grounds and die instantly when its budget owner leaves. Cross-property sponsor packaging is largely moot since the company is its own sponsor: wire the KPIs through `samber/dev-event-organizer-skills@corporate-event-strategy` and present these substitutions as reasoned stand-ins, never as established practice.
- **Mixed** - a community meetup and a company-funded conference under one team. Worth naming as its own pole because it is the one case where the shared-entity rung stops being optional: whose brand, whose list, and whose money each property uses has to be written down before a sponsor, a member or a tax authority asks. A reasoned pole rather than an observed one.

## Workflow

1. Run the interview. Apply the franchise test (Q2) before anything else: a set of independent teams under one brand is not a portfolio, and every menu below will give the wrong answer for it.
2. Inventory the properties. One row each: cadence, size, audience, rough cost, the single person who owns it end to end, and what it is _for_ in one sentence. A property whose purpose nobody can state in one sentence is the first kill candidate, before any other criterion is applied.
3. Name the funnel, pair by pair. For each ordered pair of properties, write what actually carries a person from the first to the second, and mark it _exists_ or _aspirational_. A portfolio with no _existing_ path between any two properties is a set of separate events sharing a logo; fix that before adding anything. The cheapest real mechanic, wherever two properties run close enough in time: a single slide promoting property B placed inside the deck of property A while A is still running. The highest-intent audience for B is physically in the room for A, and the mechanic costs one slide, not a campaign.
4. Check cadence collisions against **one team** and **one audience**, in that order - the team constraint binds first. Lay the properties on a twelve-month calendar and mark each property's _build-up window_, not just its date: the six weeks before a conference is when its team is unavailable, and that is where collisions actually happen. Flag any two properties whose build-up windows overlap, and flag separately any two whose audiences are the same people within one quarter.
5. Decide the shared-infrastructure set (menu 2 below). Do this before composition: what you can share determines what a new property would actually cost.
6. Decide the cadence posture (menu 3 below), then re-run step 4's calendar against it.
7. Decide composition (menu 1 below): what to add, if anything. Hard gate: nothing gets added while the flagship is unstable, meaning fewer than two completed editions, or a last edition the team or the budget did not come out of intact (Q1). An unstable flagship plus a new property is two weak properties, not a portfolio.
8. Write the allocation posture: how organizer hours and money split across the properties, and what visibly breaks first when one starves another. Treat this as a question set the team answers for itself, never as a formula:
   - Which property loses its owner first?
   - Which property's quality drop would be noticed by attendees soonest?
   - Which one are the sponsors actually paying for?

   Route the money modelling to `samber/dev-event-organizer-skills@event-budget`.

9. Write add/kill criteria per property, in advance and dated. Write the team's own: a named metric, a floor value, and the number of consecutive editions below it that trigger a retirement conversation. A criterion written after a property starts failing is a negotiation, not a criterion.
10. When the composition call is contested inside the team, enter brainstorming mode instead of recommending:
    - Two or three candidate portfolio shapes, each with trade-offs and a recommendation.
    - Questions asked one at a time.
    - Each section of the plan validated before the next.

    Never emit a portfolio plan the team has not walked through section by section.

If your harness has persistent memory, record:

- The property inventory, with each purpose sentence and owner.
- The funnel paths, marked exists or aspirational.
- The shared-infrastructure rung chosen, and the ones rejected.
- The cadence posture and the allocation posture.
- Every add/kill criterion, with its date.

Next year's portfolio call then starts from this team's own history rather than from generic cases.

## Portfolio composition

What to add to the set, if anything. Ranking below is a default, not a law.

- effort (hours, coordination, whether the commitment ever ends): `standalone second format > low-cadence small format > recurring media property > co-located add-on > continuity surface`
- value (audience carried across the gaps, plus audience the flagship cannot reach): `standalone second format > low-cadence small format > continuity surface > recurring media property > co-located add-on`
- efficiency: `continuity surface > low-cadence small format > co-located add-on > recurring media property > standalone second format`
- compliance cost (review triggered, reversibility lost): `standalone second format > co-located add-on > recurring media property > continuity surface`. The low-cadence small format carries none in the common case - a hosted room and an open invitation sign nothing.

Re-rank against the interview:

- A near deadline (Q7) promotes the continuity surface and the co-located add-on, the only rungs needing no second production cycle.
- A compounding mandate (Q8) promotes the continuity surface and the low-cadence format, and demotes the co-located add-on, which buys nothing between editions.
- A co-organizer looking for a property of their own, or a venue hosting for free (Q9), promotes the standalone second format past its normal position.

- **Continuity surface** - the default rung: one always-on, non-event property that holds the audience between editions (a chat space, a list, a publishing surface), near-zero to start, and the only rung that directly answers the momentum-between-editions problem. A hackathon network acquired an always-on developer community platform that demonstrates the pattern: a participant's work becomes "permanent, searchable, and useful to the next person" for the next cohort. Animating it is `samber/dev-event-organizer-skills@event-community-building`'s job, not this skill's; this skill only decides _whether it belongs in the portfolio_.
- **Low-cadence small format** - a monthly or quarterly meetup under the same brand, feeding the flagship. A community conference organizing guide recommends it bluntly: "No local meetup? No problem! Start one. Even if it's once a quarter, it starts building up an audience, and you get a sense of who is out there." Move up to it from the continuity surface once the surface has an audience and the gap between editions is still visibly cold. Its highest-value use is as an R&D and pipeline surface rather than a separate program: run a hands-on session on whatever is newly relevant to the flagship's own subject as soon as it emerges, and the meetup produces both a tested content idea and a warm audience for the flagship at once, ahead of anything the flagship's own planning cycle could source that fast.
- **Co-located add-on** - a second program inside the flagship's existing venue and dates: a workshop day, a co-located mini-summit. This pattern bundles several co-branded conferences into one regional edition sharing venue, week and sponsors. Bounded effort - one extra program per edition, no new date, venue or travel decision - but it buys nothing during the other eleven months, which is why it ranks below the meetup despite costing less.
- **Recurring media property** - a podcast, newsletter or video series on its own cadence, reaching past the room and past the city with no capacity ceiling. It ranks below the co-located add-on on efficiency because its cost never ends and its value only accrues across many issues: a property that stops publishing reads as dead, which is worse than never having started. Whether it converts listeners into attendees is unmeasured - treat any conversion rate as self-set, and never attach a figure to the claim.
- **Standalone second format on its own date** - the starved option: a hackathon, a startup weekend, a second conference line. Highest value on the menu, since it reaches an audience the flagship structurally cannot (students, beginners, builders rather than listeners) and creates a second sellable moment for sponsors, but it loses every efficiency round because it is a full second production cycle. Promote it only when all three hold:
  - The flagship has run at least two stable editions.
  - A distinct audience keeps asking for something the flagship's format cannot host.
  - A _different_ person can own it end to end.

  The flagship's own lead taking a second property is how both properties get worse.

A second property under its own name with no announced relationship to the flagship, no shared list and no cross-promotion path is deleted from this menu, not ranked last. The portfolio's entire value is the funnel between properties; an unlinked property is a separate event that competes with your own flagship for the same team's hours while returning none of the compounding. Parked at the bottom, it comes back the moment a co-organizer wants their own brand.

## Shared-infrastructure depth

What the properties share. Cumulative: each rung assumes the ones above it. Ranking below is a default, not a law.

- effort (setup, coordination, legal and consent work, reversibility): `one entity and budget > cross-property sponsor package > shared team and playbook > shared audience list > shared brand only`
- value (funnel paths that actually work, money moved between properties, cost taken off the next property): `shared audience list > cross-property sponsor package > shared team and playbook > one entity and budget > shared brand only`
- efficiency: `shared audience list > shared brand only > shared team and playbook > cross-property sponsor package > one entity and budget`
- compliance cost (review triggered, reversibility lost): `one entity and budget > cross-property sponsor package > shared audience list > shared team and playbook`. Shared brand alone carries none.

Re-rank against the interview:

- A mixed community/company portfolio (Q5) promotes the shared entity out of the basement, since that case needs the money boundary written down before anything else.
- A sponsor already renewing on two properties separately (Q9) promotes the cross-property package.
- A hard deadline (Q7) demotes both the package and the entity, the two rungs that cannot be done quickly.

- **Shared brand only** - one name, one visual system, one page listing every property. Near-zero effort, thinnest value, and second on efficiency for exactly that reason: recognition transfers between properties at almost no cost. It is a floor, not a portfolio.
- **Shared audience list** - the default rung and the highest-value one: one audience record spanning the properties, so an attendee of any property can be reached about another. This _is_ the funnel; without it, step 3's paths are all aspirational. Consent has to be carried per property, not assumed across them.
- **Shared team and playbook** - the same organizing people plus shared operational assets: code of conduct, vendor list, venue relationship, templates. It is what makes the third property cheaper than the second. It carries a compliance cost most teams miss: a code of conduct spanning properties means a ban on one carries to the others, and that has to be written down before it is first used, not during the incident. Once tooling is shared across properties, name what each storage system is _only_ for and archive whatever no longer matches - photos in one place, decks and credentials in another, nothing left scattered because the second property assumed it could reuse the first one's ad hoc folder.
- **Cross-property sponsor package** - the starved option: one sponsor conversation and one deal covering several properties. **This rung is untested**: co-located conferences do share a venue, a week and a sponsor pool, but that is not the same as one deal written across several properties, and neither organizers selling such a bundle nor sponsors asking for one is established practice.
  - Never present a bundle as standard practice, and never quote a bundled price as normal.
  - Promote it only when the same sponsor already renews on two of your properties separately, so the bundle formalizes an existing relationship rather than inventing one, and when one person can own fulfilment across all of them.
  - Treat the first bundle as a test with a named fallback to per-property deals, and route the pricing to `samber/dev-event-organizer-skills@event-sponsor-pricing`.
- **One entity and budget** - a single legal and financial container carrying every property, letting a profitable conference cross-subsidize a free meetup. Real, and the only way that cross-subsidy is clean - but the highest effort and the least reversible thing on the menu, which is why it loses every efficiency round for a team that does not need it yet.

Carrying one property's attendee list into another property's marketing without that property's own consent is deleted from this menu, not demoted. It is the cheapest-looking version of the highest-value rung, and consent scoped per property is a design requirement of that rung rather than an expensive variant of it. Parked at the bottom, it reappears the week before a launch deadline.

## Cadence orchestration

How the properties' dates relate across the year. Ranking below is a default, not a law.

- effort: `fixed multi-year rotation > co-location > seasonal waves > anchor-and-spread > opportunistic`
- value (audience served without collision, and a team that survives the year): `anchor-and-spread > co-location > seasonal waves > fixed multi-year rotation > opportunistic`
- efficiency: `anchor-and-spread > seasonal waves > co-location > fixed multi-year rotation > opportunistic`
- compliance cost: only the two postures that pre-commit a venue carry any - `fixed multi-year rotation > co-location`. Anchor-and-spread, seasonal waves and opportunistic sign nothing beyond what each property signs anyway.

Re-rank against the interview:

- An audience that travels to reach you (Q3), or a shared venue and crew that can carry two programs on one setup (Q9), both promote co-location out of its starved position.
- A team already at its limit (Q9) promotes seasonal waves, the only posture that deliberately buys recovery stretches.

- **Anchor-and-spread** - the default: fix the flagship's date first, then place every other property in the gaps at even intervals. Cheapest posture that both prevents collisions and keeps the year continuous, which are the two things the portfolio exists to do. Mostly a calendar exercise, repeated once a year.
- **Seasonal waves** - cluster the properties into two or three concentrated waves with deliberately quiet stretches between. A foundation demonstrates this approach by running roughly 67 events a year in quarterly waves rather than a flat calendar. Its real value for a small team is the quiet stretches: it is the only posture that treats recovery as a scheduling decision instead of hoping for it.
- **Co-location** - the starved option: two or more properties deliberately landing on the same venue and dates. At scale, one regional edition of a flagship bundles several co-branded conferences into one venue and week - high value (one travel decision, one setup, one sponsor moment) but high effort, since it concentrates every property's peak staffing on a single weekend. Promote it when the audience travels to reach you, or when the same booking and the same crew genuinely carry both programs without a second setup.
- **Fixed multi-year rotation** - slots fixed years ahead, the way one flagship rotates China, North America and Europe on a published annual cycle. Buys predictability that attendees and sponsors plan around, but the predictability only pays across many editions or many regions, and the forward commitment cannot flex when the team's capacity changes.
- **Opportunistic** - no posture: each property's owner picks their own date when they are ready. It looks free and is not. Its ratio is worse than its near-zero effort suggests, because the collisions it produces cost the audience and the team more than the coordination it avoids - which is the first failure mode below.

Running two properties on adjacent days in different venues, without sharing the booking or the crew, is deleted from this menu, not ranked last. It is co-location's promise - one trip, one weekend - with none of its mechanism: the audience is asked to choose or to attend both, and the team runs two full setups inside 48 hours. Parked at the bottom, it returns every time two owners each want their own venue on the same busy weekend.

## Failure modes

- **Two properties for the same audience in the same quarter.** The audience does not have two evenings and two ticket budgets in eight weeks; the team does not have two build-ups. Step 4's calendar exists for this, and it fails most often through the _build-up_ overlap rather than the dates themselves.
- **Adding a property before the flagship is stable.** The stability gate in step 7 is the one hard gate in this skill. A shaky flagship plus a new property produces two weak properties and one exhausted team, and the flagship is the one that was working.
- **Treating a franchise as a portfolio.** Independent teams under one shared brand need recruitment, vetting and distributed standards enforcement - none of which any menu here provides. Recognising the shape early saves the team from applying composition logic to a governance problem.
- **Selling a cross-property sponsor package as established practice.** Present the first bundle as a test with a fallback, never as how this is normally done, and never attach a bundled price presented as a market rate.
- **A property surviving because nobody wrote a kill criterion.** Properties do not die of low attendance; they die of a conversation nobody scheduled. A criterion written in advance, with a floor and a number of editions, is what turns that into a decision instead of an argument about someone's baby.
- **Reaching for a kill criterion when the real problem is a stale concept.** A flagship losing energy is not always a portfolio question - check whether the property's own theme or format has simply run out of freshness before retiring it as a property. That renewal decision belongs to whichever skill owns the property's own format, not to this one; this skill only decides whether the property still belongs in the set.
- **A continuity surface that quietly becomes a fourth property.** An always-on space with no owner and no moderation plan is not the cheap rung it looked like - it is an unstaffed property with a code of conduct attached.
- **Mistaking a shared logo for a funnel.** Step 3 marks each path _exists_ or _aspirational_ precisely because a portfolio page listing four properties looks identical whether or not anyone ever moves between them.

## Measurement

Every threshold below is self-set, so declare each floor in advance rather than reading a number back from a first year and calling it a target.

- **Cross-property carry rate** - share of one property's attendees who appear at another property within twelve months. The single number that says whether this is a portfolio or a set. Self-set floor, per pair, declared before the year starts.
- **Gap coverage** - longest stretch of the year with no touchpoint of any kind. The continuity surface's whole job is shrinking this.
- **Single-owner coverage** - properties with exactly one named person who can run them end to end. A property with zero is already failing; a person owning two is the collision the calendar will not catch.
- **Criteria written** - properties with an add/kill criterion on paper, dated, before the season starts.

One pass threshold, and it is structural rather than numeric: **every property in the inventory has a purpose sentence, a named owner and a written kill criterion - zero exceptions.** A portfolio plan with any property missing any of the three is not done, whatever its carry rate looks like.

Three questions stay the team's own to answer:

- Allocation, and what breaks first.
- Add/kill criteria, with stated reasons.
- Whether cross-property sponsor packaging is sold or wanted.

The workflow hands them a question set at those points rather than a number - do not fill them with invented figures.

## Invocation examples

- "We run a monthly meetup and an annual conference. Should we add a hackathon next year?"
- "Our conference sells out but the audience disappears for eleven months. What property fixes that?"
- "We have four events and one exhausted team - which one do we kill?"
- "Can we sell one sponsorship covering the meetup, the conference and the podcast?"

Expected output: the portfolio plan described under Measurement, delivered section by section for validation:

- The property inventory, with purposes and owners.
- The funnel map, marked exists or aspirational.
- The collision calendar.
- The shared-infrastructure rung chosen, with the rungs rejected.
- The cadence posture.
- The allocation posture.
- The composition decision.
- Per-property add/kill criteria, with dates.

## References

- [references/portfolio-case-record.md](references/portfolio-case-record.md) - the three real multi-property portfolios behind every rung, what each one does and does not demonstrate, and the three decisions a team has to make for itself.
- [references/inventory-funnel-and-kill-criteria.md](references/inventory-funnel-and-kill-criteria.md) - worked shapes for the property inventory, the pairwise funnel map, the build-up collision calendar, the kill-criteria template, and the sponsor-bundle test, with a negative example for each.

See also, same collection:

- `samber/dev-event-organizer-skills@event-format-selection` - picks the format of a property this skill decides to add.
- `samber/dev-event-organizer-skills@event-market-fit` - validates demand for a new property before composition assumes it exists.
- `samber/dev-event-organizer-skills@event-date-selection` - picks each property's actual date inside the cadence posture chosen here.
- `samber/dev-event-organizer-skills@event-marketing-plan` - runs the acquisition campaign per property, inside the calendar this skill fixes.
