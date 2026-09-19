---
name: stelow-product-open-source
description: The Open Source Paradox — delivering value by giving up control. Explores business models, organizational structures, and strategies for competing in an open-source world.
metadata:
  frequency: rare
  category: product
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
disable-model-invocation: true
---

# The Open Source Paradox: Delivering Value by Giving Up Control

## The Problem of the Proprietary Code Approach

The belief that value resides in the secrecy of code creates constant friction:
- The customer needs to trust a "black box"
- High cost to acquire customers (convincing that the secret solution is better)
- Slow feedback cycle and isolated development
- Software creation itself (especially low complexity) is becoming a commodity — with good developers and advanced AI, replicating features is faster than ever

## The Alternative Perspective

**The product is not the code — it's the living system.** The strategy shifts from protection to **curation**. Open source becomes the ideal vehicle for this, accelerating distribution and building trust — which become the true differentials, harder to replicate.

*Analogy*: publishing the recipe for a complex dish. The recipe (the code) can be copied. Other restaurants can even use the recipe. But the value of the original restaurant lies in the consistency of execution, in the atmosphere, in the trust that customers have, and — perhaps most importantly — in the **evolution of the menu**. The free recipe didn't cannibalize the business; it **created the market**.

## Business Models with Open Source

**Open-core**: the core software (which solves the problem for most users) is open and free. Monetization comes from "premium" closed-source features that solve corporate niche problems (advanced security, integrations, administration tools).

**Managed Hosting (Software as a Service)**: sell convenience. "You can host this yourself, configure, update, worry about security. Or you can pay us a monthly fee to do it all for you." Examples: WordPress.com (vs. WordPress.org), GitLab.

**Consulting, Support, and Training**: the software is 100% free, but using it at scale requires deep knowledge. The company that created it sells that knowledge in the form of technical support, consulting, and training. Example: Red Hat on top of Linux.

**Alternative Licenses (Fair Code, Source Available)**: hybrid models. Example: n8n — open source but with a license that restricts commercial use by third parties who want to offer n8n as a competing direct service. Attempt to have open source transparency without the risk of predatory competition.

**Paid Access to Repositories or Builds**: works like a "sponsorship" model, where companies pay to have access to more stable builds or private repository with priority fixes.

## Sustenance via Sponsorship

Goodwill doesn't pay rent. Sponsorship — money given to keep the project alive, not to buy features — can fund maintenance full-time, but only when designed as a system, not as a tip jar left to chance.

**How the money moves**: **GitHub Sponsors** (monthly or one-time tiers, sponsor button via `FUNDING.yml`, zero platform fee on personal accounts); **Open Collective** with a fiscal host (~10% fee, every transaction public — companies strongly prefer this traceability, and GitHub Sponsors payouts can route through it); **Patreon / Ko-fi** for fan subscriptions outside GitHub; **Tidelift** for enterprise maintenance commitments (security response, release cadence) in exchange for recurring payouts; **direct corporate sponsorship** (logo on README/docs — Vue.js peaked above $20k/month on Open Collective; TanStack's partner model funds salaries).

**What sponsors actually buy**: maintenance health, not an SLA. Never promise support response times inside a sponsorship tier — sponsorship ≠ support contract. What converts companies is a public roadmap plus a budget ("this $20k funds the 12-month roadmap"), followed by published spend reports proving it.

**Design tiers by persona, not by metal**: individual / freelancer / agency / enterprise, each with a fair expectation attached (an agency at $250/month is buying one billable hour — the code saves them far more). Keep the entry tier meaningful ($9–14/month, not $1–5): if people can pay almost nothing, most will. This is the Caleb Porzio (Livewire/Alpine.js) playbook: sponsorware first, then sponsor-exclusive screencasts — from ~$40k to >$100k/year in months, past $1M total.

**Sponsorware**: release something new exclusively to sponsors until a public threshold (sponsor count or monthly total), then open-source it to everyone. Funds the work without betraying openness — Sushi earned ~$11k/year in two days; Nuno Maduro replicated it with Pest. The guarantee to open-source must be public from day one, or it reads as a paywall.

**Honest numbers**: SerenityOS reached ~$4.2k/month and break-even in Sweden on pure donations; komorebi made ~$12k in all of 2025 and its author still needs a day job. Voluntary individual sponsorship rarely pays a full salary — treat it as one layer (see Combining Models), and court companies early: they have the budget and a selfish interest in your survival.

## Education as a Moat (Courses and Workshops)

*Analogy*: the recipe is free, but the cooking class is packed. Nobody pays for what they can read — they pay to learn faster, with the chef, alongside peers, with a team that "gets it" on Monday morning.

**The thesis**: your documentation is distribution. People arrive hungry for knowledge; sell the learning curve, not the code. One non-negotiable rule: the free docs stay best-in-class — paid material is the level above, never the missing manual.

**Formats**: **sponsor-exclusive screencasts** (recurring revenue via GitHub Sponsors tiers — the Livewire engine: free basics in the docs, advanced series behind sponsorship); **full courses** (build an email list with free content, go dark, launch — the classic launch-week-plus-long-tail formula: Laracasts for Laravel, Vue School / Vue Mastery for Vue, TestDriven.io for Django); **in-company workshops and training days** (the Red Hat / Linux Foundation / CNCF end of the spectrum — enterprises pay for teams to learn fast); **certification** where the ecosystem is big enough.

**Why it compounds the moat**: courses and workshops deepen exactly the layers competitors can't fork — brand trust, community, and the judgment of what to teach next (a curriculum is curation, like the code). Graduates become contributors; contributors become sponsors.

⚠️ **The treadmill**: education is SaaS with the worst churn — revenue stalls when content stops. And AI now answers from your docs without visiting them (Tailwind's 2025 traffic collapse is the cautionary tale: docs-SEO alone is a fragile funnel). Diversify the funnel — newsletter, community, workshops — and price accessibly (a modest annual plus a one-time option) so lower-income regions aren't locked out.

## Organizational Structures for Open Source Projects

**For-Profit Organizations and Venture Capital (VC)**: massive distribution and trust generated by open source can be the basis for accelerated growth. ⚠️ Pressure for quick financial return can conflict with building a long-term business and community interests.

**Foundations or Non-Profit Associations**: in Brazil, projects can be maintained by association or foundation, supported by donations from companies and the community. Reinforces trust that the project serves the public interest.

**Other Structures**:
- *Platform cooperativism*: the users and developers themselves own the platform
- *Steward-ownership*: the company cannot be sold as an asset. Profits are reinvested in the purpose, and voting control remains in the hands of "guardians" committed to the mission.

## How to Protect Yourself from Competition with Open Source

1. **The Brand and Trust**: people tend to trust the original creators. The brand becomes synonymous with authenticity and quality.
2. **Distribution and the Ecosystem**: a competitor can copy the code, but not the community — network of users, contributors, plugins, and integrations.
3. **The Wisdom of System Evolution**: ability to evolve the system with **discipline to keep it simple**. A competitor can copy today's features, but not the criteria that will define tomorrow's product.
4. **Defining the Market Standard**: a successful project can become the practical standard in its category. The switching cost to a competing tool becomes very high due to the established ecosystem.

## Combining Models: Suggesting a Mix from Context

No single model carries most projects. Sponsorship is goodwill but volatile; education is recurring but demands content; hosting and open-core pay enterprise money but only fit some architectures. **The sustainable pattern is a stack of two or three layers, each covering another's weakness.**

Before recommending, gather context — never prescribe blindly:
- **Project type**: library/devtool, hostable service, or end-user app?
- **Audience**: individual developers, teams, enterprises, or the general public?
- **Distribution**: stars, downloads, doc traffic — is there an audience yet?
- **Team**: solo maintainer or a team that can sell and deliver?
- **Enterprise-only surface**: are there features only companies need (SSO, audit, batch, priority builds)?

**Starter mixes by archetype**:
- *Popular devtool, solo, high doc traffic* → sponsorship + screencasts/courses + logo placements (the Livewire playbook).
- *Hostable service or infrastructure* → managed hosting or open-core as the engine, sponsorship for goodwill, education as the onboarding funnel.
- *Niche but critical dependency with enterprise users* → direct corporate sponsorship via Open Collective + support contracts; Tidelift where eligible.
- *Early project, low traction* → don't monetize yet. Distribution first — run the Internal Library experiment; nothing converts without reach.
- *Community or civic project* → foundation/association + donations + paid workshops for institutions.

**Output contract**: given the context above, propose the mix (which layers, in which order), name what each layer pays for, and scope the first reversible experiment. Revisit the mix when the context changes — a library that becomes infrastructure earns a hosting layer it didn't deserve at birth.

## Experiments for Those Who Want to Explore This Path

- **Internal Library Experiment**: transform a useful (but not-critical) internal component into an open source project to learn the dynamics.
- **"Paid Convenience" Experiment**: offer a small layer of paid convenience on an existing project (installer or premium documentation).
- **Minimum Open-Core Experiment**: release a "core" version of a product and see if this drives interest in the paid version with advanced features.
- **Sponsor Button Experiment**: add `FUNDING.yml`, three persona-based tiers, and a one-line ask in the README/docs ("If this saves you or your company time, consider sponsoring maintenance"). Run 30 days; measure profile clicks → sponsor conversion before investing in perks.
- **Docs-Funnel Screencast Experiment**: publish 5 free videos inside the docs plus 3 sponsor-only advanced ones. Measure sponsor conversion per thousand doc visitors before committing to a full course.

## Completeness contract

The host validates these minima — never submit fewer:

- Openness thesis, moat design, and experiment scope.
- At least 600 words and 3 headings.

## Examples

### Example: devtool considering open-sourcing the core

**Input:** "Should we open-source our parser?"

**Steps:**
1. Name what openness buys (adoption, contributions, trust) vs risks (competitor capture).
2. Pick the protection layer (license, hosted moat, trademark).
3. Propose the smallest reversible experiment (one repo, not the company).

**Output:** Openness thesis + moat design + experiment scope.

### Example: solo maintainer choosing a mix

**Input:** "I maintain a parser library solo, 8k stars, steady doc traffic, no enterprise-only features."

**Steps:**
1. Classify context (library, individual-dev audience, some distribution, solo, no enterprise surface).
2. Rule out what doesn't fit (no open-core surface, no hosting story).
3. Propose the mix: sponsorship base + screencast series as the engine, logo placements later.
4. Scope the first experiment (Sponsor Button, 30 days).

**Output:** Layered mix + sequencing + first experiment + revisit trigger (e.g. "add workshops when in-company requests appear").

## Edge Cases

### Competitor already forked similar work
- License choice matters more than timing; address capture explicitly.
### Team fears support burden
- Scope community surface (discussions, not SLAs); openness ≠ free support.
### No community shows up
- Distribution precedes community; the experiment failed at reach, not at openness.
### Sponsors churn silently
- Diversify across individuals and companies; never depend on one whale; sponsorship is a layer, not the salary.
### Sponsorware reads as paywalling
- Threshold and open-source guarantee public from day one; the release happens on the metric, not on mood.
### Course revenue stalls when content stops
- Price for the treadmill (annual + one-time options); repurpose workshop material into evergreen content.
### AI answers from your docs without visiting them
- The Tailwind lesson: docs-SEO alone is a fragile funnel. Build direct channels (newsletter, community, workshops) alongside search traffic.

## Entry (mode detection)

When this skill loads, check for the stelow workflow marker:

```bash
if [ -n "$STELOW_WORKFLOW" ] && [ -n "$STELOW_STATE" ]; then
  echo "stelow: workflow mode (state=$STELOW_STATE)"
else
  echo "stelow: standalone mode (no STELOW_WORKFLOW marker)"
fi
```

In **standalone mode** (no marker), run the existing skill body unchanged.
In **workflow mode**, skip to `### Workflow slice` and emit a complete
`## Hand-off (workflow mode)` block at the end. See
`../stelow-workflow-entry/SKILL.md` for the full marker protocol.

## Hand-off (workflow mode)

```
stage          : shape
description    : Shape stage. Define appetite, hill chart, rabbit holes.
status         : <done|partial|blocked>
artifacts      : <paths created or modified>
next-candidate : critique
gate           : none
rework-on      : shape
```

Workflow mode: emit the above Hand-off block verbatim, then stop. The
router skill consumes the next-candidate field and calls
`scripts/stelow advance <next-candidate>` to move state forward.

### Workflow slice

Workflow mode for the **shape** stage. Standalone behavior lives in
the rest of this file (unchanged). Summary:

> Shape stage. Define appetite, hill chart, rabbit holes.

Primary actions (per stages.yaml): `read, write`. Run only the actions that
produce the artifacts promised in `## Hand-off`; skip anything that does
not advance the workflow.

