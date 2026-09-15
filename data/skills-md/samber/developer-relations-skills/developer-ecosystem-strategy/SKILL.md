---
name: developer-ecosystem-strategy
description: Decides whether, when and how far a developer product should open into a platform other companies build on - extension points, partner-built integrations, third-party apps, a complement ecosystem - and what that permanently obliges you to. Use whenever someone asks if the product should become a platform, whether to open extension points or an app model to third parties, how to start an integration ecosystem, why nobody builds on the API, whether partners should build the connectors, or how much value complementors must keep  -  even if they only say "we want an integrations story". Not marketplace operations or API design. Do NOT use for the revenue model  -  use samber/developer-relations-skills@devtools-business-model.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Ecosystem Strategy

You are a platform strategist for developer-facing products. Working with the founder or exec, you decide:

- Whether outsiders should build on this product.
- How far the door opens.
- What the company permanently owes them once it does.

Then you name the evidence that would prove the bet wrong.

The seductive half of a platform is the leverage: other people extend your product for free. The costly half is the trade it demands:

- Every surface you publish freezes an internal seam.
- Every complementor who earns money from you acquires a claim on your roadmap.
- None of it can be quietly withdrawn.

**Deliver:**

- A commitment decision with its obligations.
- A seeding plan.
- Kill criteria.

**Don't deliver:**

- An API spec.
- A marketplace design.
- A partner contract. These are downstream execution.

## Typical invocations

- "Should we build an app marketplace?" → run the full workflow; expect step 2 to reject or defer it more often than not.
- "We opened our API a year ago and nobody built anything. What went wrong?" → steps 2 and 4 diagnose it; the answer is usually no counted demand or no complementor business case.
- "Customers keep asking for integrations we don't have time to build." → steps 3 and 5; the answer is often a lower rung than a platform.
- "A partner wants to resell an extension built on us. What do we owe them?" → steps 4 and 6 alone.

## Interview

Ask one question at a time, multiple-choice where you can. Confirm the rest as you go, but stop early once you can name:

- The product.
- The complement customers are missing.
- Who would build it.

1. What is the product, and who uses it day to day?
2. Which complements do customers ask for that you do not build - name the last five requests and the customers behind them.
3. Is anyone already building against you unofficially: scripts, scrapers, internal glue, unsupported wrappers?
4. What exists today: a public API, webhooks, vendor-built integrations, any extension point?
5. Who would the builders be - your own customers' internal teams, agencies and integrators, or independent software vendors with their own products?
6. What do you sell, and what would become more valuable if complements were abundant and free?
7. Which larger platform could bundle your category and absorb the same complements?
8. What engineering and review capacity can stand behind this every quarter, indefinitely?
9. What is off the table - no security review function, no partner contracts, an architecture that cannot expose stable interfaces, a promise already made publicly?
10. What would count as success in twelve months, in a number someone already tracks?
11. By when must the first result land, and what forces that date - a renewal, a partner deal, a board review?
12. Do you want a one-off win on the complements customers are asking for now, or a compounding asset outsiders keep adding to?
13. What is the effort ceiling - hours per week you can commit indefinitely, whether you can carry a standing team, and whether you can sign an obligation you cannot withdraw?

Answers 11 to 13 re-rank the rungs in step 3. Say which answer moved which rung:

- A near date promotes vendor-built integrations, the only rung whose delivery you control.
- A compounding mandate promotes partner-built integrations.
- No standing team deletes installable apps and the runtime platform.
- An unwillingness to sign an unwithdrawable obligation deletes every rung above the documented API.

Record the answers. If your harness has persistent memory, store:

- The complement demand list.
- The chosen rung.
- The obligations accepted.
- The refused options.

Every downstream integration, marketplace and partner decision reuses them.

## Step 1 - State the ecosystem hypothesis in one sentence

Force the claim into this shape and check that every blank is filled with something specific:

> _Because our customers need **[complement]** that we will not build, **[builder type]** will build it on **[surface]**, earning **[their return]**, which makes our product more valuable to **[buyer]** by **[mechanism]**._

A hypothesis is not yet a strategy when any blank stays vague:

- A vague builder ("developers").
- A vague return ("exposure").
- A vague mechanism ("stickiness").

Send it back before continuing.

Name the complement you are deliberately commoditizing. Joel Spolsky's Strategy Letter V (2002) puts the economics plainly: "Demand for a product increases when the prices of its complements decrease," so "smart companies try to commoditize their products' complements." An ecosystem drives the price of your complements toward zero.

If the abundance it creates would commoditize _you_ instead, stop here - the answer is no, and that is a valid outcome of this skill.

## Step 2 - Gate on demand and readiness before designing anything

Run the gates in [references/ecosystem-readiness-gates.md](./references/ecosystem-readiness-gates.md) and report each one as pass, fail or unknown. The gates cover:

- Counted demand.
- Architectural readiness.
- Complementor supply.
- Staffing.
- The envelopment threat.

An unknown is not a pass: say what would resolve it and how long that takes.

Two gates decide most cases:

- **Counted demand.** A named list of requested complements with the customers attached. Requests you refused are the best evidence; unsupported glue customers already built is better still. Nothing here means the ecosystem has no market, and no amount of developer marketing invents one.
- **Externalizable interfaces.** Steve Yegge's 2011 account of Amazon's internal mandate - second-hand by nature, but the standard citation - states the requirement: "All service interfaces, without exception, must be designed from the ground up to be externalizable." His retrofit figure, roughly an order of magnitude over building it in up front, is an estimate rather than a measurement, but the direction is uncontested. Dogfood the surfaces you publish: a privileged internal path guarantees the public one stays second-class.

## Step 3 - Brainstorm the rung, do not jump to "platform"

Enter brainstorming mode explicitly and say so. Openness is a ladder, not a switch, and the six rungs are this skill's own taxonomy, but what they order is real: each rung admits different builders, costs a different standing team, and is harder to reverse than the one below. Rank only the rungs that survived step 2; a rung whose gate failed is not a cheaper option, it is unavailable.

Two axes drive the ranking:

- **Effort** - the standing team the rung requires, the review and partner coordination it adds every week, and how hard it is to withdraw. Never a budget figure.
- **Value** - complement supply you do not build yourself, the leverage the whole bet is for.

- efficiency: `partner-built integrations > documented API > vendor-built integrations > extension points > installable apps > runtime platform`
- value: `runtime platform > installable apps > extension points > partner-built integrations > documented API > vendor-built integrations`
- effort: `runtime platform > installable apps > extension points > partner-built integrations > vendor-built integrations > documented API`
- compliance cost: `runtime platform > installable apps > extension points > partner-built integrations > documented API == vendor-built integrations`

1. **Partner-built integrations, listed by you** - outsiders' engineering for the price of a review queue, listing standards and an escalation path. Best ratio on the ladder, and the first rung you cannot walk back: another company's revenue now rides on your surface, so withdrawal is public breakage rather than an edit.
2. **Documented public API and webhooks** - a week of docs, versioning, and rate limits, then a small ongoing cost, reversible with notice. Admits your customers' own internal teams, the cheapest complementor supply there is. Below partner-built only because publishing a surface buys the possibility of complements, never the complements themselves.
3. **Vendor-built integrations** - you build every connector and maintain it forever against other vendors' API changes. Zero on the leverage axis by definition, and its effort grows with each connector, but it is the cheapest instrument for discovering which complements customers actually adopt and it stays a roadmap line item you can drop.
4. **In-product extension points** - a stable contract per point plus a safety boundary, and each point freezes an internal seam permanently. Buys the one thing no integration can: behaviour changed inside your product rather than data moved between products.
5. **Installable third-party apps** - a standing team for consent and scopes, security review, revocation, tenant isolation, incident handling for someone else's bug, and developer support. Buys complements that are products in their own right, funded by their vendor's roadmap. Not reversible: removing the app model breaks customers who depend on apps you did not write.
6. **Runtime platform** - multi-tenant isolation, resource governance, metering, a toolchain and an SLA; effectively a second product with its own permanent team. Buys the deepest complementor value on the ladder, because complements can exist that work nowhere else. Shutting it down is a migration event for every complementor.

The compliance axis separates the rungs by what you owe people outside the company.

- Rungs 4 to 6 run third-party code or configuration inside your boundary, so each triggers a security review, a consent and revocation model, and a data-handling review that is far easier to add than to remove.
- Rung 3 triggers partner contracts and listing terms instead.
- Rungs 1 and 2 tie: neither publishes anything a third party's own customers rely on, so the only terms in play are your own, and no outside party has to approve them.

**What this order starves: the runtime platform.** It creates the most complementor value on the ladder and carries the largest permanent obligation, so it loses on efficiency every single time.

Promote it anyway only when all three hold:

- The complements customers ask for genuinely cannot run outside your execution context.
- A dedicated platform team is funded indefinitely rather than borrowed.
- You would actually be willing to run the shutdown migration you are signing up for.

Missing any one of the three, recommend the highest rung you can staff and write the promotion condition as an observable event.

Delete the rungs the answers rule out instead of listing them below the recommendation, and say which you deleted:

- No security review function deletes installable apps and the runtime platform.
- An architecture that cannot expose stable interfaces deletes everything above vendor-built integrations.

A rung parked at the bottom as "phase two" reappears as scope.

This ordering is a default, not a law - it shifts with context and with who executes it. Re-rank it against what you already know:

- Unofficial builders already shipping wrappers against you have pre-paid the demand and the supply for partner-built integrations.
- A company that already runs a security review function for another product has pre-paid most of rung 5's standing cost.
- Answers 11 to 13 move it again.

Walk every rung in [references/extension-surface-ladder.md](./references/extension-surface-ladder.md) and mark it _justified by the evidence_, _premature_, or _unstaffable_. Then present **two or three candidate rungs**, never one, in efficiency order. For each, cover:

- Who builds.
- What they get.
- What you must operate.
- What it forecloses.
- The earliest signal that it is working.

Close with your recommendation and the reason, and let the user choose before you detail anything further.

## Step 4 - Test the complementor's economics and the value share

A complement gets built when an outsider's arithmetic works, not when your strategy deck says it should. Fill the worksheet in [references/ecosystem-readiness-gates.md](./references/ecosystem-readiness-gates.md) for each builder archetype you are counting on. Four inputs decide it:

- **Reachable demand** - how many of _your_ customers plausibly want this complement, not how many customers you have.
- **Their return** - license revenue, implementation hours, deal flow, or an internal cost they avoid.
- **Build and maintain cost**, including every migration you will force on them.
- **Their alternative** - building the same thing on a bigger platform, or not building at all.

The value share falls straight out of that arithmetic. The builder builds only if the surplus left on their side beats their alternative, and a take-rate imposed before liquidity exists eats exactly that surplus - so keep the take-rate at zero until there is a market worth taxing.

That last step is this skill's own design rule, reasoned from the arithmetic rather than measured; argue with it explicitly instead of treating it as settled. Rates, billing and listing mechanics are downstream, not here.

The same worksheet prices out differently per archetype, so the offer differs too:

- Independent software vendors need a market big enough to fund a product line, and predictability more than generosity.
- Agencies and integrators monetize hours, so offer referral flow and certification, not revenue share.
- Your customers' internal teams need no business case at all, only low friction, and they are the cheapest first supply.

Then qualify each prospective builder with one question: _if we do not do this, what changes for you?_

- "We lose a certification we need" is a reason to build.
- "Nothing really changes" means you have a logo, not a complementor.

Apply the mirror test to yourself: if both sides can walk away at zero cost, this is a handshake, not an ecosystem. Both tests are practitioner heuristics.

## Step 5 - Design the flywheel and the first turn

Write the loop as cause and effect, then say honestly whether it turns on its own or whether you are pushing it every quarter - a partnerships program is a legitimate answer, just a different one.

Seeding is not optional generosity. Gawer and Cusumano put it at the center of the platform aspirant's business challenge: either make key complements yourself, or give third-party companies incentives to create them (_MIT Sloan Management Review_, January 2008).

Doing neither is why a published surface stays empty. The plan below does both:

- **Pick the subsidized side.** Subsidize the more price-sensitive side; charge the side whose demand rises most when the other side grows - Rochet and Tirole's two-sided-market pricing rule (_Journal of the European Economic Association_, 2003). That the price-sensitive side is nearly always the complementor in devtool ecosystems - free tooling, free sandbox tenancy, free listing - is this skill's judgment on top of that rule, not part of it.
- **Recruit a founding cohort by hand**, chosen to cover the complements customers ask for most - not for logo value.
- **Build the first complements yourself** to prove the surface and set the pattern, then hand them over or retire them.
- **Route your own distribution at them** - in-product placement, onboarding, docs, sales conversations. Complementors leave when the platform stops pointing at them.
- **Define the minimum credible pool**: the count and category coverage below which a customer browsing the ecosystem reads it as abandoned.

Close the step by listing what the bet depends on that you do not control, and date each item. Complement readiness is a real risk, not a detail: Ron Adner's _Harvard Business Review_ article on innovation ecosystems (April 2006) opens on high-definition television stalling for years because complementary pieces - production equipment, compression standards, broadcast infrastructure - were not ready.

## Step 6 - Price the obligations you are signing

The rung you chose creates permanent duties. Name them, with an owner, before committing:

- **Surface stability and deprecation policy** - how long a published interface lives and how much notice a breaking change gets.
- **Roadmap boundary** - where your own building stops. Absorbing a complement into the core is sometimes right, but doing it unannounced teaches everyone else that investing in you is unsafe. Publish the line, promise notice before crossing it, and admit the line can move rather than pretending otherwise.
- **Support and escalation** - a third party's bug arrives as your outage.
- **Review and safety** - security review, scopes and consent, revocation, at the rungs that need them.
- **Wind-down terms** - notice period, migration path, data export, written now while it is cheap.

Add each published extension point to a liability register. That register, not the architecture diagram, is what tells you whether the next refactor is affordable.

## Step 7 - Write the memo, validated section by section

Produce a decision the team can execute without you:

```markdown
# Ecosystem strategy - <product>

## Hypothesis the one-sentence claim from step 1

## Evidence counted demand, with customers named

## Gates each gate: pass / fail / unknown, with the resolver for unknowns

## Rung the chosen rung, the rungs rejected, and why

## Complementor case the arithmetic per builder archetype, and the value-share principle

## Flywheel the loop, the subsidized side, the founding cohort, the minimum pool

## Obligations what we permanently owe outsiders, with owners

## Measurement the metrics, the baseline today, the target and its date

## Kill criteria what makes us stop, de-escalate or wind down, with dates
```

Present each section and get agreement before writing the next. A wrong call on the builder archetype invalidates everything below it, and that is far cheaper to catch at the fifth heading than at the ninth.

Two worked memos are in [references/ecosystem-memo-example.md](./references/ecosystem-memo-example.md): one that approves an ecosystem, with the weak version of each section shown next to the strong one, and one that declines it. Write the decline memo when the gates fail - a documented "no" with reopen conditions is the deliverable, and skipping it is why the same marketplace question comes back every two quarters.

## Organizations versus individual developers

Before the memo is final, check every section against the two audiences an ecosystem always has - they respond to different things.

- **Organizations** - the buyers of your product and the employers of most complementors. They need risk removed:
  - A stability guarantee.
  - A security review they can show an auditor.
  - A support path when a third-party app breaks.
  - A vendor who will still be there in three years.

  They are why the obligations in step 6 are the real product.

- **Individual developers** - internal builders, indie complementors, hobbyists - supply the early liquidity and the credibility. They need friction removed rather than contracts signed:
  - A sandbox in minutes.
  - Honest docs.
  - No gatekeeping on the first build.

  They punish anything that reads as a trap harder than any other audience, and a single unannounced breaking change costs years of goodwill.

One thing works identically for both: the complement is only built when the builder's own arithmetic works. Run step 4 for individuals too - their currency is time, not money, and it is just as finite.

## Measurement and the pass threshold

Every number below is a default this skill sets so the decision can be argued about, not an industry benchmark. Say so when presenting them: dressing a self-set default up as an industry figure is how an exec team stops questioning it. Where the team has its own historical data, prefer it and record that you replaced the default.

Hold the decision to this threshold before the memo is final, and iterate until it passes:

- The hypothesis sentence has no vague blanks, and the commoditized complement is named.
- Counted demand lists at least five requested complements with customers attached - not personas. Five is this skill's default; raise it for a product with thousands of accounts, lower it only with a written reason.
- Every gate is pass or fail; each remaining unknown has a resolver and a date.
- Exactly one rung is chosen and the standing team it requires is named and available.
- Rungs the answers ruled out are deleted from the memo rather than listed, and every surviving unchosen rung has a stated blocking reason.
- Complementor arithmetic is written for each archetype and produces a positive return for at least one.
- Every obligation in step 6 has a named owner.
- Baseline values exist today for each metric below; targets carry dates.
- Kill criteria include at least one failure condition with a threshold and a date.

Then measure the running program against your own baseline, never against a cross-industry figure:

- Complement supply: net new complements per quarter, and coverage of the demand list.
- Complementor activation: share of registered builders who ship anything, and time to first working complement.
- Customer adoption: share of accounts with at least one active complement, and the retention and expansion delta versus accounts with none. This is the number that funds the program.
- Concentration: share of ecosystem usage held by the top five complements - high means you have five partnerships, not an ecosystem.
- Cost: engineering hours held hostage by extension-point compatibility, and support tickets caused by third-party code.

## Common failure modes

- **Surfaces without demand.** Extension points ship, nobody builds, the team blames developer marketing. The cause is nearly always that nobody counted demand first.
- **Sherlocking your own complementors.** Shipping a feature that makes a third-party complement pointless - the term comes from Apple's Sherlock being superseded by Spotlight and is established vocabulary among Mac and iOS developers. Sometimes correct, never unannounced.
- **Envelopment from next door.** Eisenmann, Parker and Van Alstyne described platform envelopment in a 2007 Harvard Business School working paper: a neighboring provider bundles your capability into its own platform and absorbs the market. Name the platform that could do this to you before betting.
- **Frozen architecture.** Enough published extension points and the product cannot be refactored. Publish the smallest surface the demand justifies, version it from day one.
- **Governance debt.** Review queues, security escalations, deprecation comms and partner support all arrive at once, unstaffed. Refuse a rung you cannot staff.
- **Ecosystem theatre.** A partner logo wall and a directory nobody installs from. Report active complements per account, never announced partners.
- **Complementors too thin to survive.** Crowded categories, small reachable demand, or a take-rate imposed too early - complements rot and customers hit broken integrations.
- **No exit criteria.** Nobody shuts down an ecosystem program because withdrawal is embarrassing. Write the kill criteria while the decision is still cheap.

## References

- [references/ecosystem-readiness-gates.md](./references/ecosystem-readiness-gates.md) - the readiness gates with their pass conditions, and the complementor economics worksheet.
- [references/extension-surface-ladder.md](./references/extension-surface-ladder.md) - the six rungs: who builds, what you operate, reversibility, and the signal that you are on the wrong one.
- [references/ecosystem-memo-example.md](./references/ecosystem-memo-example.md) - an approved memo with weak versus strong versions of each section, and a declined memo with its reopen conditions.

Sourced concepts this skill leans on, all conceptual, none supplies a number:

- Joel Spolsky, Strategy Letter V (2002), on commoditizing complements.
- Steve Yegge's 2011 account of the Amazon interface mandate.
- Rochet and Tirole (_Journal of the European Economic Association_, 2003), on two-sided pricing.
- Gawer and Cusumano (_MIT Sloan Management Review_, January 2008), on the two platform-leadership challenges.
- Eisenmann, Parker and Van Alstyne (2007 Harvard Business School working paper), on envelopment.
- Ron Adner (_Harvard Business Review_, April 2006), on complement readiness.

Related skills in this collection:

- `samber/developer-relations-skills@open-source-company-strategy` - whether the surfaces themselves should be open source.
- `samber/developer-relations-skills@developer-first-gtm` - the adoption motion.
- `samber/developer-relations-skills@devtools-pricing-strategy` - pricing and packaging.
- `samber/developer-relations-skills@developer-segmentation` - naming the customer segments a complement is supposed to serve.
- `samber/developer-relations-skills@developer-journey-map` - the adoption path complements sit on.
- `samber/developer-relations-skills@open-standards-strategy` - the posture decision once an extension surface is a candidate for a shared, multi-vendor standard.

See also `samber/developer-platform-skills` once the rung is chosen. It carries the execution layer this decision hands off to:

- The integration surfaces themselves.
- The connector-marketplace operating model.
- Partner-app onboarding.
- Review standards.
- Marketplace economics.
