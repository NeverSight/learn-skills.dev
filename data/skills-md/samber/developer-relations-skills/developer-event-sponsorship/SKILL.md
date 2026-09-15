---
name: developer-event-sponsorship
description: Builds a developer-event sponsorship plan - which conferences, meetups and hackathons to sponsor, at which tier, with which on-site activation, and how to prove the money worked. Use whenever a DevRel lead, developer marketer or founder mentions sponsoring a conference, booth cost, a sponsorship tier or package negotiation, splitting an event budget across events, hackathon sponsorship, or event ROI - even if they only ask "is this booth worth it". Do NOT use for organizing your own event (samber/developer-relations-skills@developer-meetup-program), getting a talk accepted (samber/developer-relations-skills@conference-cfp-submission), or sponsoring open-source projects.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Event Sponsorship

You decide where a company's developer-event money goes: which events, at what depth, doing what on site, and what the company can honestly claim in return.

Read every package line by line, because tier names carry no meaning across events. A "Gold" at a foundation mega-conference and a "Gold" at a volunteer-run community day differ on the only things that matter: whether contact data exists, whether a stage slot is for sale, which surfaces are sold separately.

Developers read a sponsorship as a statement about the company. Trade-show behavior at a community event costs more credibility than the logo buys - that trade governs every activation choice in step 6.

Route the user elsewhere when this is the wrong table:

- Running their own meetup, conference or hackathon → `samber/developer-relations-skills@developer-meetup-program`, or see-also `samber/dev-event-organizer-skills` for the organizer craft.
- Getting a talk accepted → `samber/developer-relations-skills@conference-cfp-submission`.
- Funding open-source projects and maintainers → `samber/developer-relations-skills@oss-sponsors-brand-strategy`.
- Splitting the whole DevRel budget across pillars → `samber/developer-relations-skills@devrel-budget-allocation`.

## Interview

Ask one question at a time, multiple-choice where you can. Stop once you know the objective, the budget and the staffing ceiling; confirm the rest as the plan takes shape.

1. Who is asking, and whose budget pays - DevRel, developer marketing, field marketing, engineering, or a founder?
2. What should this money change: awareness in a new ecosystem, product adoption, sales pipeline, partner/ecosystem relationships, or engineering recruiting? Rank your top two.
3. Who buys your product - a developer paying with a card, a developer who champions it to a buyer, or a buyer who never touches it?
4. Who must be in the room: which roles, seniority, ecosystems and regions? Name the person you want your staff talking to.
5. How much per year, and is that the fee only or everything (travel, swag, staff time)? When is the budget decided?
6. What is your effort ceiling: how many people can you send who can debug a stranger's code, how many days each across the year, and who answers the follow-up in the two weeks after each event?
7. By what date must the result be visible - a board review, a funding round, a launch? This is not the contract deadline; ask for both.
8. Do you want a one-off win at one event this year, or a presence that compounds across editions?
9. Which events are already on the table - names, dates, deadlines, quoted tiers? Which did you sponsor before, and what happened?
10. What baseline data exists: web analytics, signup attribution, CRM, past event reports?
11. What are the constraints - data-protection rules on collected contacts, recruiting goals, brand rules, geographies, competitors you would rather not stand beside?
12. Who signs, and what is the earliest contract deadline you are facing?

Questions 6-8 decide the rankings in steps 3, 4 and 6, so ask them before recommending anything and say which answer moved which option:

- A near date for the result promotes the meetup and community rungs in step 4 and the help-desk booth in step 6, and deletes the workshop outright - a quarter of preparation does not fit inside a deadline two months out. It also promotes buying an add-on at an event already contracted over adding a new event.
- A compounding mandate promotes the ecosystem-anchored portfolio in step 3, the repeated event over the one-and-done, and the workshop in step 6.
- A low effort ceiling deletes the workshop and the side event, caps step 3 at the shapes one team can staff, and makes the booth's full hall hours the binding constraint on how many events the year can hold.

If your harness has persistent memory, store the objective, the annual budget split, the per-event thresholds and the post-event verdicts. Sponsorships renew annually; the next session must not re-derive the portfolio from scratch.

## Step 1 - Fix one primary objective

A sponsorship serves one primary mandate. Everything downstream (event choice, tier, activation, metric) is decided by it, and a plan that keeps two primaries produces a report nobody can act on.

This objective table draws on Phil Leggetter's AAARRRP goal mapping, which places events and conference talks in the Awareness/Acquisition family - a corrective to pipeline-first sponsorship pitches.

This table carries no efficiency ranking, deliberately: the objective is a mandate handed to you, not an option chosen for its ratio, and ranking the rows would tell a recruiting team to chase pipeline. Every ranking further down is computed against whichever row lands here.

| Objective  | What the money buys                                         | Primary metric                                                                   | Events that fit                                             |
| ---------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Awareness  | first contact with an ecosystem that does not know you      | branded search, direct traffic and unaided mention lift vs. a pre-event baseline | large horizontal conferences, student hackathons            |
| Adoption   | hands on the product during the event                       | activations from the event cohort still active at 30/60/90 days                  | workshop-friendly events, hackathons, ecosystem conferences |
| Pipeline   | qualified conversations with people who can buy or champion | conversations → opportunities → influenced pipeline                              | practitioner and enterprise-heavy conferences               |
| Ecosystem  | partner and integration conversations                       | partner conversations that reached a scheduled next meeting                      | vendor-neutral foundation events, ecosystem summits         |
| Recruiting | candidate contact                                           | candidates entering the hiring funnel                                            | student hackathons, language-community conferences          |

Who buys changes both the objective and the measurement:

- **Developer-purchased products (self-serve, card payment, individual or team plan)** behave like consumer marketing. Success is measurable in-product (event-specific signup URL, promo credit, activation curve) and the follow-up is a product invitation, not a sales sequence. Awareness and adoption are the realistic mandates.
- **Enterprise-sold products** hinge on a conversation that outlives the event by two to four quarters. The attendee is often a champion, not a signer, so pipeline claims must ride on the CRM, and the event's contribution is influence rather than source.
- **Both motions in one company** need the objective set per event, not per year: the hackathon is awareness, the enterprise conference is pipeline. Say which is which in the plan.

## Step 2 - Qualify every candidate event

Headcount is the least informative number in a prospectus. Demand this evidence before pricing anything, and treat an organizer who cannot supply it as the answer:

1. Audience composition - role mix, seniority, company size, buying influence. Not a total.
2. Geography and travel mix.
3. Track record - prior editions, returning-sponsor rate, and last edition's post-event report with actual numbers.
4. Sponsor density and which competitors have already committed.
5. Exactly what the package includes (see step 4).
6. Program balance - technical content versus sponsor content.
7. Follow-up rights - whether contact data exists at all, and under which consent.

Organizers who run a healthy event already publish most of this. The PSF's PyCon US 2026 prospectus prints attendee count, job-function split (53.9% developer), industry split and company-size bands before it prints a price - that is the evidence standard to hold every organizer to, not an unusual courtesy.

Score each event against the objective rather than against other events' prices. [references/event-scorecard.md](./references/event-scorecard.md) holds the weighted scorecard, a worked example of a strong and a weak event scored side by side, and the request email that extracts the evidence above.

Walk away on:

- unverifiable demographics
- a first-time organizer making large promises
- a prospectus that sells sponsor benefits harder than the attendee experience
- an attendee list offered as a deliverable
- deadline pressure arriving before the audience data does

## Step 3 - Brainstorm the portfolio, then choose one

Size the envelope before drawing the shortlist. One published reference point exists: events took a mean 41.1% of DevRel program budget in _State of Developer Relations 2024_ (DevRel.Agency, September 2024), the largest of four categories. Use it only as evidence that events historically dominate DevRel spend - 47 respondents answered that question and their shares sum to 104.5% - never as a target to hit.

Then enter brainstorming mode before committing to any single event. Sketch **two or three candidate portfolios** for the year, each with its allocation split, the staffing it consumes, and what it deliberately fails at. Recommend one, explain why the others lose, and get explicit agreement before negotiating anything.

Four shapes are worth drawing from, ranked by value per unit of effort. Effort is staff-days across the year, travel overhead, preparation reusable between events, and follow-up capacity after each one - never the fee. Value is qualified conversations that continue after the event, plus the recognition carried into the next edition.

- efficiency: ecosystem-anchored > flagship-led > farm-team > regional spread
- value: flagship-led > ecosystem-anchored > farm-team > regional spread
- effort: regional spread > farm-team > flagship-led == ecosystem-anchored

No compliance-cost line at this altitude: contracts, consent and code-of-conduct obligations are signed per event in step 4, and a portfolio shape commits to none of them.

- **Ecosystem-anchored** - every event sits inside one technology community. Leads the efficiency line because the demo, the staff brief, the prepared answers and the follow-up relationships are built once and reused at every event; credibility compounds fast. Effort: a quarter of preparation, then a standing job for whoever owns that community. Fails the moment the strategy needs a second ecosystem.
- **Flagship-led** - one deep sponsorship plus small presences elsewhere. Buys the most conversations and the strongest recognition of any shape, because depth of presence is what a developer audience notices. Effort: a quarter of preparation and a standing job for the week itself. Fails at geographic coverage, and starts cold everywhere the flagship is not.
- **Farm-team** - student hackathons for long-horizon awareness plus one practitioner conference for near-term proof. Two objectives and two metrics on one budget, which is also its cost: two follow-up motions and two measurement systems, each paid in full. Effort: the preparation of the flagship shape, doubled, and two owners.
- **Regional spread** - many small local events. Cheap per event, good for a field team, and the only shape that reaches developers who never travel. Effort: travel overhead multiplied by the event count, with follow-up fragmented across as many owners. Rarely reaches decision-makers.

- Justify the effort tie: flagship-led and ecosystem-anchored concentrate the same people on the same preparation for the same total number of days. The ecosystem shape spreads those days across more editions without adding any, which is why it wins on efficiency and not on effort.
- Default to ecosystem-anchored, and move to flagship-led when one event demonstrably holds the audience the objective names, or when recognition inside a single ecosystem is already established and the mandate is to be seen beyond it.
- What this order starves: the regional spread, the only shape that gives a field team local coverage. Promote it when go-to-market is regional and the staff already live in those cities - a team travelling nowhere new turns its worst axis, travel overhead, into near-zero.
- Delete the farm-team, rather than ranking it last, whenever one person owns event measurement: two objectives with one owner produce one metric and two excuses.
- Re-rank against what you already know about this team: an ecosystem where the company is already a known name, a staff roster clustered in one region, or an existing workshop curriculum all move a shape up before the default order applies.

Keep a slice of the annual budget unallocated - 15-25% is this skill's default, not an industry figure - because the best-fit event is rarely the one visible in January.

## Step 4 - Choose the model and the tier

Read the prospectus for three clauses before looking at the price:

- what contact data the sponsor receives
- how a stage slot is obtained
- which surfaces are sold separately

Package models return different amounts of qualified conversation per staff-day, which is the one axis a price sheet never shows. Effort below is people on site × days plus the preparation and follow-up the model generates; compliance cost is the review a model triggers and how little of it can be undone once signed.

- efficiency: meetup / user group > community conference > foundation or large vendor conference > hackathon > in-kind
- value (qualified conversations that continue): foundation or large vendor conference > hackathon > community conference > meetup / user group > in-kind
- effort: hackathon > foundation or large vendor conference > community conference > meetup / user group > in-kind
- compliance cost: foundation or large vendor conference > hackathon > in-kind > community conference > meetup / user group

| Package model                               | What money buys                                                                                                                                       | What it never buys                                     | Effort                                                                                                     | How to win there                                                                                              |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Meetup / user group                         | one evening in front of a small, high-intent local audience                                                                                           | scale                                                  | an hour of preparation, one evening, local staff                                                           | sponsor a series rather than one night; let the host keep editorial control                                   |
| Community / volunteer conference            | presence among peers, a table, passes, a brief timed pitch                                                                                            | attendee contact data, badge scanning, purchased talks | two technical people for the length of the event; opt-in follow-up only, so the follow-up list stays small | send people who help; capture interest by opt-in only; submit to the CFP separately                           |
| Foundation / large vendor conference        | booth space, passes, consented badge-scan data, à-la-carte surfaces (wi-fi, lanyard, scholarships, activation zones), published multi-event discounts | main-stage session slots, editorial content            | a standing job for several people across several days, plus the follow-up that scan volume creates         | buy a lower tier plus the one add-on that reaches your audience; logo size scales with price, surfaces do not |
| Hackathon                                   | mentorship access, a prize track, workshop slots, product placement in what gets built                                                                | judging outcomes, guaranteed adoption                  | a standing job across nights and a weekend, judging included                                               | frame the prize around the problem, not the product; staff the crunch hours                                   |
| In-kind (credits, hardware, infrastructure) | reach at low cash cost for an early-stage vendor                                                                                                      | predictable visibility                                 | near-zero on site, a week spent pinning deliverables in writing                                            | pin every deliverable in writing; in-kind visibility drifts unless specified                                  |

- Read the efficiency line as ordering models, not events: it decides where a marginal staff-day goes when two candidate events both survived step 2.
- What this order starves: the foundation or large vendor conference - top on value, second on effort, so a ratio picks the meetup every time, and a year of meetups never reaches an ecosystem that does not know you. Promote it when the objective is awareness in a new ecosystem, or when the buyers you named in the interview travel to one event and no other.
- Delete in-kind, rather than ranking it last, unless the company is early-stage and cash-constrained. Elsewhere it buys visibility nobody committed to, at the price of a contract negotiation with no money in it.
- Read the compliance line as the review triggered and the reversibility spent:
  - a large conference's contract is signed a quarter ahead and cannot be unwound, and its consented badge data needs a data-protection review before anyone may use it
  - a hackathon's prize rules and judging criteria are published and fixed the moment entries open
  - a community conference asks you to sign its sponsor code of conduct and holds no data at all
  - a meetup is a handshake
- This ranking is a default, not a law, and it shifts with who executes it. Re-rank when the team already attends an event for other reasons, when the product demos badly in five minutes, or when a local user group is run by someone the company already works with.

Inside a chosen event the tier is its own menu. Efficiency: lower tier plus the one add-on that reaches your audience > cheapest tier clearing the booth price floor > logo-only tier > top tier.

Effort scales with what a tier obliges you to staff rather than with what it costs: ten passes and a large booth are a staffing commitment, and a booth nobody can staff for the full hall hours is worth less than a workshop. Check for eligibility-gated startup or end-user tiers before picking a rung, since they are the same product cheaper, for reasons unrelated to audience quality.

Work back from the calendar: three mechanics are decided there rather than at the negotiating table.

- Contract and add-on deadlines: large events close roughly a quarter out - KubeCon NA 2026 required signed contracts by 14 August for a November event - so put the decision in the fiscal quarter before the event it affects.
- Multi-event discounts: check for published ones before inventing an ask, since some marketplaces fix them rather than negotiate them (CNCF: 3% for one event, 5% for two signed together, 8% for three or more).
- Branded surfaces: move early, since the best ones sell out months ahead and are the cheap half of the lower-tier-plus-add-on play.

Where published prices exist, read them before accepting a quote. [references/published-price-ladders.md](./references/published-price-ladders.md) carries the two 2026 prospectuses that print full price lists, the booth price floor they reveal, what a hands-on slot really costs, and the tier-name comparison trap to avoid.

## Step 5 - Negotiate

Packages move, especially for early commitment, multi-event or multi-year deals, off-peak editions, growing events, and sponsors who bring something the organizer wants (a workshop, a mentor pool, a scholarship fund).

The asks compete for one budget that is not money: the number of things an organizer says yes to before the conversation turns. Spend it in this order.

- efficiency: previous edition's post-event report > extra staff passes > timing of lead-data delivery > placement on a specific high-traffic surface instead of a generic logo tier > a workshop or demo-theatre slot > permission to publish content from the event > a written attendance estimate with a remedy if the event undershoots badly
- value (qualified conversations that continue): workshop or demo-theatre slot > high-traffic surface > extra staff passes > lead-data timing > permission to publish > attendance remedy > post-event report

The report leads because it costs nothing to ask, arrives before signature, and can still cancel the deal. What this order starves is the attendance remedy and the workshop slot, the two hardest asks.

Make the remedy your first ask at any first edition, where an unmet estimate is the whole risk. Make the workshop your first ask whenever step 6 chose it. The ordering sequences the asks; it never shortens the list.

Never buy a keynote's content, a judging outcome, an attendee list the attendees never consented to, or an implied speaking slot at an event that runs a CFP. None of these is a gray area to probe in negotiation: each is an ethics failure, and each becomes a story that travels faster than the sponsorship does.

## Step 6 - Design the on-site activation

Spend commits immediately after this choice, so brainstorm **two or three activation options** for the chosen tier, name the trade-off in each, recommend one, and validate it before anything is bought.

Value here is qualified developer conversations that continue after the event, never badge scans. Effort is staff-days on site, preparation before it, follow-up capacity after it, and opportunity cost - the same two engineers cannot run a workshop and staff a booth.

- efficiency: help-desk booth > prize track > side event > workshop
- value: workshop > help-desk booth > side event > prize track
- effort: workshop > side event > help-desk booth > prize track
- compliance cost: prize track > side event > help-desk booth == workshop

Effort in magnitudes:

- the booth costs an hour of preparation and then a standing job for the hall hours
- the prize track costs a week to frame and procure, and borrows mentoring hours you were staffing anyway
- the side event costs a week of guest-list and venue work plus an evening that also costs you the next morning
- the workshop costs a quarter of preparation and takes your two best engineers off the floor for its whole slot

- Default to the booth as a help desk: technical staff who debug a stranger's code, a demo the attendee drives, a quick win within reach (the five-minute bar is this skill's default). That pattern is practitioner convention, not a measured result - but it is the behavior developer audiences reward, and the pitch-first booth is the one they punish.
- Justify the compliance tie: a booth and a workshop each collect contact details under one consent line, reviewed once and reused all year, and trigger nothing else. The prize track tops that axis because prize promotions are regulated in some jurisdictions, judging criteria are published and fixed once entries open, and prize value can be reportable. A side event you host carries the venue contract, the alcohol, and a code of conduct the conference organizer is not enforcing on your behalf.
- What this order starves: the workshop and the side event, the two deepest engagements available and the two most staff-intensive, so a ratio picks the booth every round. Promote the workshop when a curriculum already exists - that alone collapses its preparation from a quarter to a week and moves it to the top of the efficiency line. Promote it too when the product cannot show a win in five minutes and the booth's whole premise fails. Promote the side event when the objective is ecosystem and the twenty names already sit in the CRM, or when the team was travelling to this event anyway, which drops its marginal cost to the evening alone.
- Delete rather than demote:
  - the prize track at any event with no build phase
  - the workshop where the package sells no hands-on slot or nobody can be spared for its preparation
  - both the workshop and the side event when only one person is travelling, since a team of one can staff exactly one thing
- The scholarship or diversity fund sits off this ladder on purpose. It buys goodwill and stage-level thanks and produces no conversations by design, so it has no value on this axis and ranking it would be false precision. Choose it deliberately as an awareness or employer-brand purchase, or leave it out.

[references/activation-playbooks.md](./references/activation-playbooks.md) details each activation in that order - staffing rhythm per event type, the staff brief, and a positive/negative example pair of booth conversations.

Two rules bind every activation. Staff conversations toward the qualification bar defined in step 7 rather than toward badge count. And where a live demo is part of the activation, design its failure plan with `samber/developer-relations-skills@developer-live-demo-design` - a booth demo fails in front of the exact person you were trying to convince.

## Step 7 - Build the measurement plan before signing

Cost the sponsorship fully - fee, add-ons, booth build, shipping, swag, prizes, travel and accommodation per person, and loaded staff time for preparation, travel, on-site days and follow-up. Staff time is the line most teams omit and the line that most often doubles the total.

Then fix the threshold **before** signing: a target cost per qualified conversation, plus a minimum conversation count that makes the trip worth staffing. Derive the target from the current blended acquisition cost rather than from the sponsorship fee.

Only one unit survives comparison across a hackathon, a community day and a mega-conference: the qualified conversation - someone who has the problem, holds or influences the decision, and agrees to a named next step. Define the bar and the next step before the event and brief every staffer on both.

Route each logged conversation to the team that can use it, and name the destination in the log. Mary Thengvall's DevRel Qualified Lead (2019) gives the routing table:

| Conversation type            | Route to     |
| ---------------------------- | ------------ |
| Case-study material          | Marketing    |
| Feedback and beta candidates | Product      |
| Bugs                         | Engineering  |
| Partner interest             | Partnerships |
| Candidates                   | Recruiting   |
| Buyers                       | Sales        |

Most booth conversations are not sales leads, and defaulting them all to sales is what fills a CRM with records nobody works.

[references/sponsorship-roi-model.md](./references/sponsorship-roi-model.md) holds the cost worksheet, the metric definitions per objective, and the tracking mechanics (event-specific URLs and codes, baseline capture, consented capture where scanning does not exist, the conversation log shape). It also covers the 30/60/90 windows and a worked calculation with the same event judged well and badly.

## Step 8 - Review, then renew, renegotiate or drop

Run the review within two weeks, while the conversation log is still accurate, and write the verdict down where next year's budget cycle will find it:

- **Renew** - threshold met, staffing sustainable, audience unchanged.
- **Renegotiate** - right audience, wrong package: drop a tier and buy the add-on that produced the conversations, or trade the booth for a workshop.
- **Drop** - audience mismatch, or the same outcome is reachable elsewhere for less.

These three carry no efficiency ranking: the verdict is read off the threshold set in step 7, not chosen for its ratio. Ranking them would let the cheapest verdict win an argument the data already settled.

Judge a first edition against awareness-stage expectations and reserve the pipeline verdict for the second, since recognition and relationships compound across editions. That patience is not a license to renew an event that has missed its threshold twice.

## Pass threshold

The plan is finished when every event on it carries:

- one primary objective
- a fully loaded cost
- a target cost per qualified conversation
- a minimum conversation count
- a named owner for the follow-up

An event that cannot be given a threshold cannot be judged and should not be signed - say that out loud instead of softening it.

After the event, the sponsorship passes when it met its threshold on its own primary metric. Missing it triggers step 8's renegotiate or drop, not a search for a secondary metric that happens to look better.

## Invocation examples

- "Should we sponsor KubeCon next year?" → run the interview, then steps 1-2 on that single event, and answer with a threshold or a decline, never with a maybe.
- "We have €60k for developer events in 2027, what should we do with it?" → steps 1-3, deliver two or three candidate portfolios with the allocation split, recommend one.
- "They quoted us Gold at $18k, is that worth it?" → step 4 against the line items and `references/published_price_ladders.md`, then step 7's fully loaded cost before any verdict.
- "We're sponsoring a hackathon in six weeks, what do we do there?" → steps 6-7 only; the event is bought, so design the activation, the qualification bar and the tracking.
- "Was last year's conference worth it?" → step 8, using whatever cost and conversation data exists; if no threshold was set, say the question cannot be answered honestly and fix it for the next one.

## Failure modes

| Symptom                                 | Cause                                              | Fix                                                     |
| --------------------------------------- | -------------------------------------------------- | ------------------------------------------------------- |
| Big attendance, no useful conversations | event chosen on headcount, not composition         | re-qualify on role mix and buying influence (step 2)    |
| Booth ignored                           | non-technical staff, pitch-first posture           | staff with engineers, lead with help (step 6)           |
| Leads that never convert                | swag-for-scan capture with no qualification bar    | define the bar pre-event; capture fewer, better records |
| No verdict at renewal time              | no threshold and no baseline set before signing    | fix both in step 7, before the contract                 |
| Repeated one-off sponsorships           | portfolio never designed, events bought reactively | run step 3 once a year and keep a reserve               |
| Community backlash                      | trade-show mechanics at a community event          | read the three prospectus clauses in step 4 first       |
| Missed the good events                  | contracts close a quarter ahead of the event       | map deadlines during the interview, not after           |

## Output shape

Produce two artifacts:

- **Portfolio plan** - the year's events in a table (event, date, objective, model and tier, fully loaded cost, threshold, owner), the allocation split, the unallocated reserve, and the shortlist of events deliberately declined with the reason.
- **Per-event one-pager** - objective, audience evidence, package line items, negotiated extras, activation plan, staffing roster and rhythm, tracking setup, threshold, and the post-event verdict once it exists.

Templates for both are in [references/event-scorecard.md](./references/event-scorecard.md) and [references/sponsorship-roi-model.md](./references/sponsorship-roi-model.md).

## References

- [references/event-scorecard.md](./references/event-scorecard.md) - weighted qualification scorecard, worked strong/weak examples, organizer evidence request, portfolio plan template.
- [references/sponsorship-roi-model.md](./references/sponsorship-roi-model.md) - cost worksheet, metric definitions, tracking mechanics, worked ROI calculation, per-event one-pager template.
- [references/activation-playbooks.md](./references/activation-playbooks.md) - five activation types, staffing rhythms, staff brief, positive/negative booth examples, follow-up sequences.
- [references/published-price-ladders.md](./references/published-price-ladders.md) - sourced 2026 tier and add-on prices, the booth price floor, the tier-name comparison trap, and how to build your own yearly band table.
- See `samber/developer-relations-skills@conference-cfp-submission` for winning a stage slot the sponsorship cannot buy.
- See `samber/developer-relations-skills@developer-live-demo-design` for any demo that runs live at the booth or in a sponsored workshop.
- See `samber/developer-relations-skills@developer-meetup-program` for running your own recurring event instead of sponsoring someone else's.
- See `samber/developer-relations-skills@oss-sponsors-brand-strategy` for sponsoring open-source projects and maintainers.
- See `samber/developer-relations-skills@devrel-budget-allocation` for the split between events and the other DevRel pillars.
- See `samber/developer-relations-skills@devrel-metrics` for the program-level measurement framework these event metrics roll up into.
