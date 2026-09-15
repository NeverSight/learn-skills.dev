---
name: partner-enablement
description: Sequence the training, content, and certification a B2B partner program needs to make partners self-sufficient sellers - the partner enablement roadmap, not the training content itself. Covers the skills-gap needs assessment, enablement tracks split by partner role and type, certification design and refresh cadence, and a pilot cohort, all designed backwards from the partner's first deal. Also covers B2C analogs (franchise, dealer, ambassador education). Use whenever the user mentions partner enablement, partner certification, channel partner training, a partner onboarding curriculum, or ramping partners to a first deal, even if they never say enablement. Do NOT use for affiliate welcome emails - use mbfinotti/partnerships-skills@affiliate-onboarding-sequence instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.8"
---

# Partner Enablement

Sequence what training, content, and certification partners need to become self-sufficient sellers. This skill architects and orders the enablement roadmap; it never writes the actual training module, battlecard, or exam - those are downstream tactical work.

No canonical partner-enablement methodology exists. Say so plainly rather than invent one. What the field genuinely offers:

- **Established methods are instructional-design methods only**: Kirkpatrick's Four Levels (1959) and Phillips ROI for evaluation, ADDIE and SAM for the build process, 70-20-10 as a heuristic (widely cited, weak empirical base). None is channel-native; applying them to partners is a practitioner adaptation - flag it as such.
- **Everything labeled a "partner enablement framework" or lifecycle model** is PRM-vendor content marketing or proprietary analyst IP (Forrester/Canalys) - internally consistent and often useful, never independent methodology.
- **The best-supported design principle is practitioner consensus, not research**: design backwards from the first deal - minimum viable knowledge to register a qualified opportunity, deeper training as deals progress ("align the learning curve with the earning curve").
- **The strongest analyst-sourced finding** (Forrester channel research): recycling direct-sales content to partners unchanged produces lackluster usage and failed messaging - the field's best-documented failure mode.

## Interview

Ask before designing anything. One question per message; offer multiple-choice options; skip whatever the user already answered.

- Is this B2B channel enablement, or a consumer-facing network - franchise, dealer, retail associate, ambassador/creator? Part of the design genuinely diverges (see B2B and B2C).
- Which partner types are in the program - referral, reseller, SI/implementation, MSP, ISV/tech - and which actually transact?
- What enablement assets exist today, and where did each come from: built for partners, or recycled from direct-sales enablement?
- What sales motion do partners run - refer, resell, implement, manage? Each needs different depth.
- What are the current time-to-first-deal and activation rate (share of signed partners with a registered deal)? "Not tracked" is an answer.
- Does certification already gate anything - tier status, discount, co-sell eligibility, lead flow - or is it a standalone badge?
- What certification burden will partners realistically bear: hours per person, exam fees, certified-headcount requirements? Smaller partners hit headcount walls first.
- Who owns enablement day to day, with what capacity - and does content creation sit elsewhere (product marketing, channel ops)? Fragmented ownership is a documented failure pattern.
- What does the partner get economically for investing the time - margin, services revenue, leads, MDF? Partners ration selling time across vendors.
- What does success mean, and by what date must it land - a first partner deal, a certified cohort, a board slide?
- Do you want a one-off win (one stalled partner selling) or a compounding asset (a curriculum that ramps every partner you sign next year)?
- What is the effort ceiling - enablement hours per week, whose calendar they come off, and how much political capital a certification mandate would cost you internally?

Those last three answers re-rank every option menu in this skill, so ask them before proposing anything:

- A near date promotes: the first-deal path, the deal-registration walkthrough, mined artifacts over partner interviews.
- A compounding mandate promotes: certification, the technical and delivery tracks, the partner-ID join behind the trained-vs-untrained comparison.
- A hard effort ceiling: defers every asset whose build cost runs past a week.

## Workflow

1. Run the Interview; collect every current-state fact the roadmap depends on.
2. Confirm scope: sequence enablement inside a program that already exists. Program structure, tier criteria, and partner scorecards belong to the sibling skills in the Reference section.
3. Run a needs assessment before building anything: interview 5-10 partners split between active and inactive, map each enablement component current-state vs desired-state, and produce a gap document. See [references/needs-assessment.md](references/needs-assessment.md).
4. Choose the sequencing approach before designing to it. Present the three candidates in the ranked order below - highest deals unblocked per hour of enablement build first - say the ranking out loud, recommend the top rung, and wait for the pick. Steps 5-10 build out whichever they choose; offered afterwards, the choice is not a choice.

   | Approach                                 | Build effort                                           | Time to first partner deal     | What it buys                                                                            |
   | ---------------------------------------- | ------------------------------------------------------ | ------------------------------ | --------------------------------------------------------------------------------------- |
   | Minimum-viable first-deal path (default) | a week                                                 | weeks                          | partners transacting while most of the curriculum is still unwritten                    |
   | Certification-first launch               | a quarter, plus sign-off on what the credential claims | a quarter or more              | a defensible capability gate and a tier criterion, before any deal proves one is needed |
   | Comprehensive up-front curriculum        | a standing job                                         | a quarter or more, often never | full coverage of every role and type, at the price of the firehose failure mode         |
   - efficiency: minimum-viable first-deal > certification-first > comprehensive up-front
   - value: comprehensive up-front > certification-first > minimum-viable first-deal
   - effort: comprehensive up-front > certification-first > minimum-viable first-deal
   - compliance cost: certification-first > comprehensive up-front > minimum-viable first-deal

   Certification-first carries the only real exposure of the three. A credential the vendor markets:

   - is a public capability claim partners resell on
   - is gated on legal or brand sign-off
   - is hard to withdraw once partners advertise the badge

   Move off the default only on a condition, not on program size. Certification-first earns its place when customers check credentials before buying, or an unvalidated partner can damage customers.

   The efficiency order starves the comprehensive curriculum: it is first on value and first on effort, so it loses every round to a ratio. A program that only ever computes efficiency never reaches full role coverage at all - it ships the first-deal path and stops. Promote it when the deadline is far enough that no deal is waiting on the curriculum and the effort ceiling is genuinely a standing job.

   Short of that, buy its coverage incrementally as post-first-deal tracks instead of dropping it. When the interview rules a rung out - no economic gate a certification could attach to, or an effort ceiling under a week per asset - strike it from the menu and say it is struck, rather than listing it as a later phase.

   A rung parked at the bottom returns as scope nobody budgeted. Re-rank against what you already know: an existing demo environment, partners who are already technical, or direct-sales collateral that adapts cleanly all cut the top two rows' effort and can move a rung up.

5. Design backwards from the first deal: define the minimum viable knowledge, access, and actions a partner needs to register one qualified opportunity - and size it in partner hours. Everything beyond that path is explicitly post-first-deal training, not a prerequisite. A comprehensive up-front curriculum is the firehose failure mode.
6. Split tracks by partner ROLE (sales rep, solutions architect, delivery consultant, partner marketer, executive sponsor) and by partner TYPE (a referral partner needs a short overview; an implementation partner needs multi-day technical depth). Build them in the ranked order that reference gives - every customer-facing role that exists in the base still gets a track, the ranking only decides which exists first. A role the partner base does not contain is deleted from the audience map and named there as deleted, never scheduled late; a referral-only base has no delivery consultant, and a track left pending for one reappears as a quarter of work nobody planned. See [references/curriculum-architecture.md](references/curriculum-architecture.md).
7. Decide what is enabled before signature vs after: the partner value case and economics come before; product, sales, and technical training come after. Training a partner who has no economic reason to invest is the documented "no value proposition for the partner" pitfall.
8. Decide whether to certify at all, and what each certification gates. Certification can BE a tier criterion - if so, state it and hand the criteria design to `mbfinotti/partnerships-skills@partner-tiering`. See [references/certification-design.md](references/certification-design.md).
9. Set the refresh cadence per asset class, with a named owner per asset - stale content misleads partners more quietly than no content.
10. Plan a pilot cohort: launch the roadmap on a small, deliberately chosen partner group, collect feedback, then scale.
11. Validate the spec section by section per the next section - audience map, first-deal path, tracks, certification, cadence, pilot - revising on pushback before moving on.
12. Check the pass threshold; iterate the roadmap until every check holds.
13. Stop at the approval gate - finalize nothing without the user's explicit approval of the full spec.
14. If your harness has persistent memory, memorize the approved roadmap, its sequencing decisions, and thresholds; otherwise tell the user to store the spec where partner ops can retrieve it.

If you can browse the web, verify any named vendor certification structure before citing it - major programs restructured repeatedly across 2022-2026. Otherwise flag vendor examples as possibly stale.

## Brainstorming the roadmap

Run the design the way channel teams actually run it - discovery before design, socialized before shipped:

- Ask one question per message throughout; never batch questions.
- Start with a listening tour: the 5-10 partner interviews from the needs assessment. If the user cannot run interviews, mine what exists - joint business plans, QBR notes, asset-request logs, support tickets, portal search queries.
- Pull joint-business-planning inputs where they exist: partner goals, resources, obstacles, and any training/certification commitments already made per partner.
- Present the three sequencing approaches at step 4, in step 4's ranked order and with its recommendation stated out loud, before any design step runs. Every ranking in this skill and its references is a default rather than a law: it shifts with the user's deadline, effort ceiling, and who executes the work, so re-rank it against the assets and skills this user already has instead of reciting it.
- Once the user picks a direction, present the spec one section at a time - audience map, first-deal path, tracks, certification, cadence, pilot - and validate each before writing the next.
- Recommend socializing the near-final roadmap through a partner advisory council before any public launch; collecting partner feedback and ignoring it is worse than not asking.
- Validate on the pilot cohort before scaling; expect v1 to be imperfect and plan the iteration window up front.
- Gate finalization on explicit user approval of the assembled spec.

## The Enablement Roadmap Spec

Deliver the engagement as this artifact - a decision record the user hands to partner ops, partner marketing, and the channel chief:

```
ENABLEMENT ROADMAP - <program>, <date>
Audience map    : partner types x roles that need enabling; types/roles excluded, with why
Gap summary     : per enablement component, current state vs desired state (from the
                  needs assessment), ranked by impact per unit of fix effort - not
                  by impact alone, or the quarter-long gaps crowd out the hour-long ones
First-deal path : minimum knowledge + access + actions to register a qualified
                  opportunity, sized in total partner hours; everything else is
                  explicitly post-first-deal
Tracks          : per role x partner type - contents, depth, owner, and per track a
                  build effort (hours / a week / a quarter / a standing job) against
                  what it unblocks, listed in that ratio's order
Pre-signature   : what is enabled before the agreement (value case, economics)
                  vs after (training, portal, deal registration)
Certification   : certify or not, with why; per level - format (exam / lab /
                  outcome validation), burden in hours + fees, what it gates,
                  recertification cadence; tier-criteria design handed to
                  partner-tiering
Refresh cadence : per asset class - owner, review date, retirement rule
Pilot           : cohort size + selection, success criteria, feedback loop,
                  scale trigger
Ownership       : single accountable owner; where content creation sits; internal
                  enablement plan for the vendor's own channel team
KPIs            : from the KPI section, incl. the trained-vs-untrained comparison
                  design and the first review date
```

Rules about the spec itself:

- Every track answers "what's in it for the partner" in economic terms before it lists any content - partners are rational economic actors rationing time across vendors.
- The first-deal path carries a mandatory hours number - a path nobody sized is a firehose in disguise.
- Every asset class carries an owner and a refresh date - unowned content rots into content that misleads.
- The spec sequences and gates; it contains no training content, battlecard copy, or exam questions - those are downstream deliverables built from this roadmap.

## Pass threshold

Ship nothing until all six hold; iterate until they do:

1. **First-deal path fits in hours, not weeks.** If the mandatory pre-selling path exceeds roughly a working day of partner time, it will not be consumed (practitioner consensus, no independent dataset).
2. **No unchanged direct-sales asset anywhere in the plan.** Every asset is either partner-built or explicitly adapted - the recycled-content failure is the best-documented in the field.
3. **Every customer-facing role has a track.** Programs over-invest in sales and neglect technical/delivery roles; a partner who cannot demo or implement will not sell.
4. **Certification gates something economic, or does not exist.** A badge tied to no tier, discount, lead flow, or co-sell priority gets ignored - completion follows economics.
5. **Every asset has an owner and refresh date, and the roadmap names one accountable enablement owner** - even if content creation stays distributed.
6. **Every ordered list in the spec shows the arithmetic under its order.** Each row of the build order, the track list, and the gap ranking carries a build effort in hours, a week, a quarter, or a standing job, against what that row unblocks. Never use a currency figure; it goes stale faster than the ordering it was meant to justify. An order with no ratio beneath it is taste presented as sequencing.

## Diagnosing an existing enablement program

When the user arrives with a running program instead of a blank page, match the symptom they report and work its row. This table is deliberately left unranked: the reader never picks a row - the symptom picks it - so ordering eight diagnoses nobody is choosing between would be false precision. The ordering that does apply lives inside each row, where "Check first" always names the cheapest disqualifying check before the expensive one.

| Symptom                           | Check first                                                                                                                     | Variable at fault                                                                               |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Partners sign but never activate  | Size of the mandatory pre-selling path; whether a partner economic case was ever made                                           | First-deal path too large, or a recruiting/program problem - hand to the program-design sibling |
| Time-to-first-deal above ~90 days | The three usual causes in order: enablement minimum too large; partner manager overloaded; partner signed without qualification | Sequencing, capacity, or recruiting - only the first is an enablement fault                     |
| Certified but inactive partners   | What the certification gates; whether it tests capability or clicks                                                             | Certification-economics link, assessment format                                                 |
| Content unused                    | Origin of the assets (recycled direct-sales?); then portal friction (logins, findability)                                       | Content fit first, distribution second                                                          |
| Partners refuse certification     | Burden (hours, fees, certified-headcount) vs the economic payoff; small-partner headcount walls                                 | Certification burden design                                                                     |
| Partners can't show the product   | Whether a demo environment and demo script exist per track                                                                      | Demo enablement - the most commonly reported gap                                                |
| Stale content losing deals        | Refresh cadence and per-asset ownership                                                                                         | Cadence and ownership, not volume                                                               |
| Only a sales track exists         | Coverage of technical, delivery, and marketing roles                                                                            | Track split by role                                                                             |

## KPIs

Judge the enablement program, not individual partners (partner scorecards, QBRs, and underperformance triggers belong to `mbfinotti/partnerships-skills@partner-performance`):

- **Trained-vs-untrained cohort comparison** on partner-sourced opportunities, time-to-first-deal, and win rate - the one measurement that proves enablement worked rather than merely happened.
- **Certification coverage by role per partner** - not raw certificate counts; 40 sales certs and zero technical certs is a coverage failure hidden by a healthy total.
- **The certified-but-inactive list** - partners who completed training and produced no pipeline; a named failure mode and a coaching queue.
- Time-to-first-deal and activation rate, against the 60-90-day / 30-50% bands - PRM-vendor rules of thumb, no independent dataset exists.
- Content usage and portal engagement as the earliest warning signal - but read low logins as access friction first, apathy second.

Nearly every benchmark in this field is PRM-vendor sourced with undisclosed methodology - carry a reliability flag on any figure you cite. A partner learning platform by default yields only Kirkpatrick Levels 1-2; Levels 3-4 need deal data joined in. See [references/measurement-and-benchmarks.md](references/measurement-and-benchmarks.md).

## B2B and B2C

Identical in both worlds:

- segment learners by role before building anything
- tie certification to recognition and incentives to drive completion
- a learning platform or branded academy as the delivery backbone
- fast new-product training
- the core logic of enabling the person standing in front of the customer

Genuinely different - design for the difference:

- **Train-the-trainer is structural in franchise and dealer networks**: the brand trains the franchisee/general manager, who trains their own staff. B2B SaaS programs rarely formalize this layer; consumer networks cannot function without it.
- **Brand-standard certification carries legal/compliance weight in franchising** - enforced consistency across locations. B2B partner certification has no comparable legal exposure.
- **Coverage is per-site and mandatory in consumer networks** (every location run by certified people) vs B2B's per-organization certified-headcount thresholds.
- **Front-line mindshare**: retail and dealer associates are hourly staff who must be won over with short, motivating micro-content and competitive literacy; B2B partner reps are independent economic actors who need a margin case.
- **Ambassador/creator education is closer to consumer retail than to B2B channel**: short, self-serve, motivation-first, built for high volume at near-zero touch.
- **Contractual leverage**: franchisors can mandate training completion; B2B vendors can only incentivize it.

## Invocation Examples

- "Our partners sign and then never sell. Build the enablement roadmap - 60 partners, mix of resellers and agencies."
- "Design the first-deal path for a new implementation partner and tell me what belongs before signature versus after."
- "Should we certify partners at all? If so, what should certification gate, and how often does it need refreshing?"

## Reference

- See [references/vendor-examples.md](references/vendor-examples.md) for real 2022-2026 vendor program structures decomposed - with a staleness warning.
- See [references/measurement-and-benchmarks.md](references/measurement-and-benchmarks.md) for Kirkpatrick applied to a channel audience, KPI definitions, and benchmark bands with reliability flags.
- See `mbfinotti/partnerships-skills@partner-channel-program` for the overall program structure - motions, tiers, economics envelope, governance; enablement is one component it references.
- See `mbfinotti/partnerships-skills@partner-performance` for partner scorecards, QBR structure, and underperformance triggers - this skill measures whether enablement worked, not whether a partner performs.
