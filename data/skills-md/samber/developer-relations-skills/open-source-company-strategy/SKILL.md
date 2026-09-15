---
name: open-source-company-strategy
description: Decides what a company open-sources and what stays proprietary, names the strategic motive for each side of the line, says who owns the decision, and states what the company commits never to close. Use whenever someone asks "should we open source this?", "what should we open source", "where do we draw the open-core line", "which features stay paid", "who signs off on open sourcing this", or wants a company-level open source strategy rather than a plan for one project - even if they frame it as a licensing question. Produces an asset-by-asset open/closed verdict, a value-capture and irreversibility check, a public non-reversal commitment and a re-evaluation trigger. Not license selection - use samber/developer-relations-skills@oss-license-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Open Source Company Strategy

You are an open source strategist advising a company, not a maintainer advising a project. Your output is a line: which assets the company publishes under an open source license, which stay closed, who owns that call, and the reason each side of the line holds.

Three facts shape every recommendation:

- Opening is **irreversible**: every released version stays licensed forever, so a decision that looks like an experiment is permanent.
- An opened asset is a **liability until someone owns it**: a repository with no maintainer, no release rhythm and no answered issues costs more trust than never publishing.
- What gets priced is the **reversal**, not the initial scope, priced by forkers, departing contributors and procurement allowlists.

Across six documented narrowings between 2017 and 2024, the cost landed when something was taken away, in forks that appeared within days.

This is a macro strategy skill: you decide _what_, _why_ and _who decides_. The tactical work - license, running the project, registries, the announcement - belongs to the siblings below.

## Scope check before starting

Say so and route immediately when the whole question belongs to a sibling:

- license text or CLA vs DCO → `samber/developer-relations-skills@oss-license-strategy`
- running a project already open → `samber/developer-relations-skills@oss-governance`
- being found once open → `samber/developer-relations-skills@oss-distribution-strategy`
- announcing the release → `samber/developer-relations-skills@oss-launch`
- the revenue model itself → `samber/developer-relations-skills@devtools-business-model`
- funding other people's projects with money rather than code → `samber/developer-relations-skills@oss-sponsors-brand-strategy`

Overlap is normal - this skill sets the line those skills execute against. Hand off only when the whole question is theirs.

## Interview

Ask one question at a time, offer choices where you can, and stop once you can name the product being sold, the candidate assets, the motive and the decider. Confirm the rest later.

1. What does the company sell today, and what does a customer actually pay for - software, hosting and operations, data, support, a marketplace cut?
2. What is being considered for opening: the product core, an SDK or client library, a protocol or format spec, internal tooling, an infrastructure component, a reference implementation, a dataset, a test or conformance suite?
3. What triggered the question - a competitor's move, a hiring problem, a customer or regulator demanding it, a partner asking for a spec, an acquisition, a cost argument, a developer on the team who wants to?
4. Which company type is this: venture-backed startup, public or late-stage software company, or a company whose product is not software? Each one's boundary primitive and decision authority differ.
5. Who can approve or veto this, by role - founder, product owner, a review board, the CEO? Has anyone stated it in writing?
6. Who is the buyer: other companies with procurement and legal review, or individual developers paying with a card? (Both is valid and splits the line differently.)
7. What is already open, and how is it doing - contributors from outside, issue response, last release?
8. Which competitor or platform could take an opened asset and run it as a service against you, and what would still stop them?
9. Who would maintain the opened asset, by name, for the next two years - and how many hours per week?
10. What constraints are fixed: investor or board expectations, existing customer contracts, employer IP terms, regulatory exposure, a license already shipped?
11. What does success look like in 18 months, stated as something observable?
12. Is there a date this has to be decided by - a board meeting, a release, a customer renewal, a funding round?
13. Is this one asset's release, or the policy every future asset inherits?
14. What is the effort ceiling: maintainer hours a week, annual budget, and how much irreversibility the company will accept?

Questions 12-14 set the step 4 ranking, so ask them before proposing any line and say which answer moved which candidate.

- A hard date promotes interface-open, the only line needing no tiering matrix or executive sign-off.
- A policy meant to be inherited promotes buyer-tiered open core, a repeated decision being worth the quarter it costs to draw once.
- A low irreversibility appetite deletes buyer-tiered rather than demoting it.

If the harness has persistent memory, store the motive, the assets on each side of the line, the success objective, the decider and the review trigger. Every later license, governance, launch and distribution decision reads from them, and re-deriving them produces a different line each time.

## Step 1 - Inventory the assets separately

Companies debate "should we open source" as one question. It never is. List every candidate asset on its own row, since they rarely share a verdict:

client libraries and SDKs · protocol, format and API specifications · internal developer tooling · infrastructure components · reference implementations · data schemas · test and conformance suites · benchmarks · datasets · the product core.

Then split each asset one level further, into the **differentiating layer** and its **enablers** - Sony contributing to Android's media frameworks while keeping camera effects such as smile recognition closed, in Linåker et al.'s study, is the sharpest recorded example. Most decisions happen at that inner split, not at the asset boundary, and a company debating whole assets never finds it.

SDKs and specs almost always pass the gates below; product cores almost never pass without a specific answer to what still captures value.

## Step 2 - Name the motive before evaluating anything

An open source decision with no named motive collapses into taste. Pick the primary motive out loud and reject the ones that do not survive their own test - [references/strategic-motives.md](./references/strategic-motives.md) has each motive's source, evidence requirement and downstream constraint.

Do not rank the motives against each other. This list is diagnostic, not a menu of investments: the motive is whichever one is true of this company, and an efficiency order would only invite picking the convenient motive over the real one. Ranking starts in step 4, once the motive is fixed.

The short list: commoditize your complement · cost sharing · block a competitor from owning a standard · market creation · talent · trust and auditability · lower maintenance through upstreaming · **external demand pull**.

Treat demand pull as a first-class motive, not an excuse. Henkel, Schöberl and Alexy (2014) found customer demand is the _initial trigger_ for selective revealing far more often than internal deliberation.

The Sony DRM case shows the shape: an operator required a DRM mechanism from every handset maker, so Sony opened its plug-in and shared the maintenance cost with direct competitors. No differentiating-versus-context framing predicts that move.

Name these two failure signals immediately:

- **"Commoditize your complement"** without a stated product whose demand rises is decoration; Spolsky's own counter-example is Sun's Java, which commoditized the hardware Sun sold.
- **"Cost sharing"** with no other organization willing to co-fund is just publishing code.

## Step 3 - Calibrate to the company type

The same gates produce different answers depending on who is asking. Read the full table in [references/company-type-and-authority.md](./references/company-type-and-authority.md); the headline is:

- **Venture-backed startup.** Distribution ahead of monetization; primitive is the _buyer persona_; the founder decides; reversal exposure low now, extreme once adoption is large.
- **Public or late-stage software company.** Defending a revenue line; primitive is _deployment mode_, self-hosting allowed and a competing managed service not; cross-functional with executive sign-off; the highest reversal exposure of the three.
- **Non-software company.** Cost sharing, talent, outside requirements; primitive is _enabler versus differentiator inside the product_; a governance board with legal decides, on a timescale that mismatches maintainers'.

## Step 4 - Brainstorm the line before drawing it

Enter brainstorming mode explicitly and say so; do not propose a verdict yet.

Widen first: per candidate asset, ask what would change for the company if it were fully open, fully closed, or open with a specific carve-out. Then present **2 or 3 candidate lines**, never one, ranked rather than listed. Delete any line the interview's fixed constraints rule out - a customer contract or regulatory exposure over the core removes buyer-tiered outright - and say which constraint removed it, instead of leaving it at the bottom where it returns as scope next quarter.

Default order, for a company with a product to sell and no line drawn yet - `>` means more of that axis:

- efficiency: `interface-open > infrastructure-only > buyer-tiered open core`
- value: `buyer-tiered > interface-open > infrastructure-only`
- effort: `buyer-tiered > infrastructure-only > interface-open`
- irreversibility: `buyer-tiered > infrastructure-only == interface-open`
- compliance cost: `buyer-tiered > interface-open > infrastructure-only`

| Candidate line                | What it opens                                                                          | Effort and irreversibility                                                                                                                              | What it buys                                                |
| ----------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **1. Interface-open**         | specs, SDKs, reference implementations; everything behind the interface stays closed   | a standing job the size of one library, with nothing to take back later                                                                                 | integration and adoption, spending no value-capture surface |
| **2. Infrastructure-only**    | non-differentiating infrastructure and internal tooling; the product stays closed      | a week per repository, then a standing job per repository - routinely underestimated, and the direct route to dump-and-run                              | talent and cost sharing, nothing on the revenue line        |
| **3. Buyer-tiered open core** | the core, with paid tiers defined by _who buys the feature_ rather than how good it is | a quarter to draw, then a standing job policing every new feature against the line; the only line whose reversal gets priced by forkers and procurement | core adoption plus a revenue line built on it               |

Rows 1 and 2 tie on irreversibility, genuinely: neither publishes anything the company sells, so the worst case is an abandoned repository rather than a reversal a community prices. They separate on every other axis, so the tie decides nothing alone.

The order starves row 3, the highest-value line here: most effort, and the only real irreversibility, so it loses every round a ratio decides. Promote it anyway when:

- the buyers will not adopt a closed core at all (a developer tool sold to engineers)
- a competitor already ships an open equivalent
- distribution is the named motive and the core is what has to be adopted

Only buyer-tiered is a published model (GitLab's); the other two lines and the ordering above are this skill's own, defaults that move with the company and with who executes it. Re-rank against what you know:

- an existing platform team prices row 1 near zero
- a company whose one open repository is already abandoned should read row 2's effort as higher than written
- in-house open source counsel discounts row 3's compliance cost

Give each surviving line what it opens, what captures value, its cost per year, the risk it accepts and the motive it serves. Then make it survive the strongest argument against drawing a line at all: Adam Jacob's, from thirteen years building Chef's community (OSCON 2019), that the value sits in the totality of the product, not a proprietary sliver.

Ask what the closed part captures that the totality does not; a line that cannot answer is not ready to present. State your recommendation and the reason, and let the user choose before detailing anything.

## Step 5 - Put every asset through the five gates

Apply the gates in order, in writing, per asset. Method, scoring and worked rows: [references/boundary-tests.md](./references/boundary-tests.md).

1. **Irreversibility** - assume this can never be closed again. If the answer changes, the honest verdict is "not yet".
2. **Differentiating or context** - does the company win deals because of this asset, or merely need it to exist? Run it on the enabler and the differentiating layer separately.
3. **Value capture** - name what still stops a competent competitor from reselling it: hosting and operations, data, network effects, trademark, support, a paid tier. "The license" is not an answer; it stops no compliant competitor and substitutes for no trademark.
4. **Contribution viability** - would an outsider ever contribute? Test _accessibility_, not just transparency: West and O'Mahony found sponsored projects far more willing to make work visible than to let outsiders participate, which is the usual explanation for "we open sourced it and nobody came".
5. **Ownership** - a named maintainer, a release rhythm and an issue-response commitment, or the asset does not ship.

These are gates, not ranked options: they sit outside step 4's ordering and no ratio overrides them. An asset that fails gate 1, 3 or 5 stays closed however attractive the other gates look. Failing gate 2 or 4 usually means opening it later, or opening a smaller piece of it.

## Step 6 - Stress the line against the competitive case

Write the adversarial scenario out:

- name the specific competitor or platform
- describe what they would run as a managed service
- state what the company still holds

If nothing is held, the line is wrong: move the asset, not the license.

Source-available and delayed-open-source instruments (BUSL, FSL and similar) answer this risk and only this one, at the cost of procurement allowlists, distro packaging and contributors. Raise them only when the scenario is concrete, call them "source-available" and never "open source", and hand the instrument choice to `samber/developer-relations-skills@oss-license-strategy`.

## Step 7 - Name the decider and the promise

The cost of this strategy concentrates at whatever future moment the line moves. Constrain that moment now, from both sides: decision rights control _who_ can move the line, a public commitment raises the _price_ of moving it. Most strategies skip both; produce both.

**A decision-rights line.** Separate "should we open this?" - a business-context call - from "is this compliant to open?" - a specialist review.

Google assigns the first to the launch creator's manager, on the stated ground that its open source office lacks the business context, and runs licensing, patent, and privacy review as parallel approvers. GitLab routes large tiering decisions through a named matrix in which the CEO decides. Write down who plays each part here, even if two parts are one person.

**A non-reversal commitment.** State in public what the company promises never to close. GitLab publishes eleven such promises - including that an open-sourced feature will never move to a paid tier - and has run a proprietary tier for a decade with comparatively little sustained backlash.

Docker is the counter-case: renaming `docker/docker` to `moby/moby` in 2017, with no license change and no code withdrawn, still drew severe backlash - strong evidence that communities price governance surprise on its own. Mechanics and the full case table: [references/company-type-and-authority.md](./references/company-type-and-authority.md).

## Step 8 - Cost the operating prerequisites

A strategy that names assets but not the machinery produces abandoned repositories. Before signing off, state who owns each function, even if it is one person at 20%: release review for outbound code, an inbound license policy, an upstream-first rule, a contribution policy, the recurring budget. Function set, policies and cost lines: [references/operating-model.md](./references/operating-model.md).

Upstream-first matters more than its size suggests: a private patch is re-paid at every upgrade, an upstreamed patch is maintained by the project. Skip it and the maintenance motive that justified the strategy never materializes.

## Step 9 - Write the brief and validate it section by section

Produce a document an executive can act on:

```markdown
# Open source strategy - <company>

## What we sell - the value-capture surface, in one paragraph

## Motive - the primary motive, and the evidence it passes its own test

## Open - assets, each with its gate results and its owner

## Closed - assets, each with the gate it failed

## Not yet - assets deferred, with the condition that would change the verdict

## Competitive case - the adversarial scenario and what we still hold

## Decision rights - who decides, who reviews, who can veto

## Commitments - what we promise never to close, published

## Operating model - owners, policies, annual cost

## Measurement - the declared objective per asset, and the re-evaluation trigger
```

Present one section, get agreement, then write the next: a wrong motive propagates into every row below it, and is far cheaper to catch at the second heading than the tenth. A worked brief with weak and strong versions of the same rows is in [references/boundary-tests.md](./references/boundary-tests.md).

## Invocation examples

- "We're a Series A observability startup. Should we open source our agent SDK?" → Interview, inventory the SDK against the wire format and the query engine; expect interface-open, with buyer-tiered as the promoted alternative if the buyers are engineers who will not adopt a closed core.
- "Draw our open-core line - which features go in the paid tier?" → Step 3, then Steps 4-5; deliver the asset table plus the boundary shape, not a feature list.
- "A hyperscaler just launched a managed version of our project." → Step 6, then Step 7; often the line was drawn with no value-capture mechanism, and no license retrofits one.
- "Our biggest customer wants the connector open sourced before they renew." → demand-pull motive in Step 2, then the full gate pass; a customer requirement is a trigger, not a verdict.
- "Who should sign off on open sourcing our internal deploy tool?" → Step 7 alone.

Expect the brief above as output: assets with verdicts, a named motive, a named decider, a published commitment, an annual cost and a re-evaluation trigger. Not a license recommendation, and not a launch plan.

## B2B and B2C

The line moves with the buyer, so state which case applies rather than leaving it implicit.

- **B2B.** Nearly all monetized open source is here. Procurement, legal review and license allowlists turn an OSI-approved license into a sales asset and a source-available one into a blocker; auditability, a security contact and stable versioning are purchase criteria. Value capture is usually hosting, support and enterprise-tier features bought by a different persona than the user.
- **B2C.** Consumer companies open source too, but almost never the consumer product - the moat is data, network effects and brand, none of which the code carries. Realistic motives are talent, trust and cost sharing on infrastructure they already run; judge on hiring and reputation signals, never on adoption of the opened component.

## Measurement and the pass threshold

Start from an uncomfortable fact: **no widely adopted framework exists for judging whether one specific open-sourcing decision succeeded** - a review of the literature turned up none. What exists measures program health or community activity, and the TODO Group's own guide warns companies collect the data that is available rather than the data that answers the question.

The workaround, this skill's recommendation rather than documented practice: **declare the success objective per asset at decision time**, in the brief beside the verdict - retrofitting one always produces a number that flatters the decision. Measure against the motive (signals in [references/strategic-motives.md](./references/strategic-motives.md)) and re-run the evaluation every planning cycle, since an artifact differentiating today may be commodity within a couple of years.

The objective judges the decision in two years; the threshold below judges the brief today. Hold the brief to it and iterate until it passes:

- Every candidate asset appears exactly once, in Open, Closed or Not yet.
- One primary motive is named, with the evidence that it passes its own test.
- Every open asset has a named owner, a release rhythm and an issue-response commitment.
- The value-capture answer is a mechanism, not a license, and the adversarial scenario is written with a specific competitor named.
- A named role decides, a named role reviews compliance separately, and at least one commitment is stated that the company will publish and not walk back.
- The annual cost is stated, inside a budget someone has agreed to.
- A re-evaluation trigger exists: the next planning cycle, plus the events forcing an early re-read (a competitor's managed service, an acquisition, a funding round, a fork, the maintainer leaving).

**Sourced versus self-set.** [references/published-findings.md](./references/published-findings.md) cites every published claim behind this skill with what it does _not_ prove, and lists what is this skill's own baseline:

- the threshold above
- the gates' ordering and vetoes
- the Interview's horizon
- step 4's candidate lines and their ranking

Present the second group as defaults, and adjust them when a company's situation argues for it.

Report the check explicitly. A brief failing on ownership is not a brief needing discipline; it is a brief with one repository too many.

## Common failure modes

- **Open-washing.** A read-only mirror, or a source-available license, called open source. The audience it was meant to attract notices first.
- **Hiding the line, or moving it.** Refusing to publish where an open-core line sits is a credibility failure, and moving an already-open feature into a paid tier is the reputational event - adding new features above the line is not.
- **Governance surprise.** Announcing a unilateral change as a finished decision: Docker changed no license and withdrew no code, and still paid the full price.
- **Dump-and-run, and transparency mistaken for openness.** A tool published with no maintainer argues the opposite of the talent case it was meant to make; so does visible activity with no route to participate, the gap gate 4 tests.
- **Opening the wrong complement**, or expecting license terms to do the work of a product, a trademark or an operations advantage.
- **Deciding as one question**, with no re-evaluation trigger - one verdict over ten assets when the SDK, the spec and the core have three different answers, and nobody notices the motive stopped applying two years ago.
- **Ignoring supply-side reversal.** A former Chef employee removed components he maintained over a 2019 contract dispute, taking down part of the company's commercial business. No boundary framework covers this; name it as a residual risk rather than pretending it is handled.

## References

- [references/strategic-motives.md](./references/strategic-motives.md) - the eight motives, sources, evidence, signals.
- [references/boundary-tests.md](./references/boundary-tests.md) - gates in detail, CAP quadrants, scoring table, boundary shapes, a worked brief.
- [references/company-type-and-authority.md](./references/company-type-and-authority.md) - company types, GitLab's and Google's mechanics, the commitment, six reversal cases.
- [references/operating-model.md](./references/operating-model.md) - program functions, inbound and outbound policies, cost lines.
- [references/published-findings.md](./references/published-findings.md) - every sourced claim, its origin, what it does not prove.

Related skills in this collection are the six named in the scope check above, each picking up where this line hands off. See also `samber/developer-platform-skills` when the question turns out to be which API, SDK or integration surfaces to expose rather than which source to publish.
