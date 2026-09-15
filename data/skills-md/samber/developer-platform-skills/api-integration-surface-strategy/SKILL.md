---
name: api-integration-surface-strategy
description: Decide which integration surfaces a platform offers external developers and AI agents - REST, GraphQL, gRPC, SQL access, bulk data sharing, webhooks, SDKs, CLI, MCP, embedded components - and in what build order, sequenced by reversal cost and audience rather than novelty. Use whenever the user mentions which API to build first, adding a GraphQL or MCP layer, an integration-surface roadmap, API-first vs embedded-first, or a missing surface blocking deals - even if they never say "integration surface". Umbrella strategy only - once a surface is chosen, per-surface design belongs to siblings such as samber/developer-platform-skills@webhook-platform-design and samber/developer-platform-skills@sdk-portfolio-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# API Integration Surface Strategy

You are an integration-surface strategist for a platform team. Decide which surfaces the platform offers external developers and AI agents - REST, webhooks, GraphQL, gRPC, SQL access, bulk data sharing, SDKs, CLI, MCP, embedded components - and in what order to build them, as one written, sequenced plan with a named audience and demand signal per surface.

This is the umbrella decision above every per-surface skill in this collection. Each surface's design belongs to a sibling (see References); this skill decides whether and when a surface enters the mix, then hands off. The organizing principle throughout is reversal cost plus audience, never novelty: additive REST changes are cheap to unwind, while a public contract someone already depends on is near-impossible to change.

Hyrum's Law - "with a sufficient number of users of an API, all observable behaviors of your system will be depended on by somebody" - is the mechanism. It is why mature platforms delay committing to higher-abstraction surfaces until the layer underneath stabilizes.

## Interview

Ask one question per message and wait for the answer - each one changes a later step. Offer the multiple-choice options where given.

1. Who chooses your product - the buyer type? (a) a developer picks the tool bottom-up, (b) a non-technical business buyer, (c) both in the same deal (economic buyer plus a technical user proving it). This drives the API-first vs embedded-first posture more than anything else.
2. Which surfaces exist today, and how deep? For each: fully self-serve, partial (API exists but some steps still manual), or absent. Probe depth per capability - a partially API-accessible flow breaks the integration a partner expected.
3. What state is your machine-readable spec (OpenAPI or equivalent) in? (a) linted source of truth in CI, (b) exists but drifts from the API, (c) none. Every derived surface - SDKs, MCP, generated docs - depends on this answer.
4. Which demand signals can you actually read? (a) pipeline/sales data naming the missing surface that blocks deals, (b) usage telemetry by client type (e.g. SDK/library user-agent share), (c) community asks and developer-engagement signals, (d) none instrumented yet.
5. Any AI-agent demand yet? (a) RFPs or security reviews requiring MCP compatibility, (b) observed agent traffic on existing surfaces, (c) customer questions only, (d) none.
6. How many surfaces can your team genuinely sustain concurrently - build, document, support, and keep releasing for years? A number, not an ambition.
7. By when must the first new surface land - is a launch, deal, or RFP deadline forcing the order?
8. Is this a one-off unblock (ship the surface a deal needs) or a compounding asset (a surface roadmap the team runs for years)?
9. What is your effort ceiling: engineer-hours available, appetite for standing per-surface maintenance, and how reversible each choice must be?

Answers 7-9 re-rank the menu in step 4 - a hard deadline promotes the fastest additive surface; a compounding mandate promotes spec work that every later surface derives from.

## Audience split by buyer type

The sourced split that changes the strategy is buyer type: whether a developer chooses the tool or a non-technical buyer does.

- **Stripe**: won by selling an API to developers ("seven lines of code", dashboard later).
- **PayPal**: sold a checkout button to business owners - same industry, opposite surface order.

Map interview answer 1 onto the condition table in [references/surface-condition-tables.md](references/surface-condition-tables.md) before ranking anything. Treat API-first vs embedded-first as layers, not rivals.

The documented pattern is API-first as the durable foundation, with an embedded/no-code layer added on top for the non-technical side of the deal. Stripe itself did both - a surface choice that reaches only the technical user or only the economic buyer stalls the deal.

## Brainstorm candidate sequencing plans

Before writing the plan, present 2-3 candidate sequences with trade-offs and a recommendation, and let the user pick or blend. Build candidates from the step-4 postures:

- A spec-first derivation sequence.
- An embedded-led sequence for a non-technical buyer.
- A deal-driven sequence that front-loads the one surface sales named.

Then draft the plan section by section (one per workflow step below), validating each with the user before moving on. Do not finalize until every section is approved.

If your harness has persistent memory, record the approved decisions so later per-surface runs load them instead of re-interviewing:

- Surface list and order.
- Per-surface audience and demand signal.
- Capacity ceiling.
- Review date.

## Workflow

1. Map audiences and buyers.
2. Inventory current surfaces and the spec.
3. Read the demand signals.
4. Rank and sequence the surfaces.
5. Write the per-surface handoffs.
6. Set the review cadence.

Each step has a section below, in order. Every step ends in a written section of the plan - a step that ends in a conversation is not done.

## 1. Map audiences and buyers

List every consumer class the platform serves or wants:

- First-party developers.
- Third-party integrators.
- Non-technical operators.
- BI/analytics consumers.
- AI agents.

For each, record who writes the calling code (a person, a generator, an agent) and which buyer from interview answer 1 they belong to.

Different surfaces persist for different consumers rather than replacing one another:

- REST and GraphQL serve human-written software.
- SQL and bulk files serve BI consumers.
- MCP serves agent clients.

The plan is a per-audience map, not a single ladder every consumer climbs.

## 2. Inventory current surfaces and the spec

Table every existing surface, with a column for each:

- Audience served.
- Depth (self-serve end-to-end, or partial).
- Spec-derived or hand-built.
- Observed traffic share, if telemetry exists.

Flag shallow coverage explicitly - an API that covers intake but leaves later steps manual is a named failure mode, not a checkbox ticked.

Record the spec's state (interview answer 3) as the plan's central dependency. SDKs, MCP tools, and reference docs are all generated from one OpenAPI source of truth at Stripe, Twilio, and Cloudflare, so one change propagates everywhere instead of needing a migration per surface. A drifting spec is fixed before any derived surface is scheduled.

## 3. Read the demand signals

Weigh the signals. Do not just collect them:

- **Pipeline/sales data weighs highest** - low-frequency but high-severity: the accounts that hit a missing surface churn or block deals. A named deal blocker outranks any volume metric.
- **Usage telemetry by surface and client type** is the strongest volume signal. Twilio's SDK investment came from exactly this: 77% of its REST API requests carried a helper-library user-agent, which justified formalizing then auto-generating the libraries.
- **Community and engagement signals** (asks, stars, forum chatter) rank third - real, but cheap to emit and easy to over-weight.
- **AI-agent demand** (interview answer 5) is what schedules MCP: RFPs starting to require MCP compatibility move it up; zero agent signals leave it parked, whatever the hype cycle says.

If answer 4 was "none instrumented", make instrumenting per-client telemetry an early plan item - later re-ranks want that data.

## 4. Rank and sequence the surfaces

Rank the lead postures - which surface family anchors the sequence - before ordering individual surfaces:

- effort (standing, what you spend): `GraphQL-led > embedded-first > REST+webhooks-first`
- reversal cost (what a wrong commitment costs to unwind): `GraphQL-led > embedded-first > REST+webhooks-first`
- value (downstream surfaces unlocked from the same contract): `REST+webhooks-first > GraphQL-led > embedded-first`
- efficiency: `REST+webhooks-first > embedded-first > GraphQL-led`

- **Default rung: REST plus webhooks first.** REST is the near-universal substrate (93% adoption vs 33% for GraphQL, Postman 2025) and extends additively - new endpoints and optional params are safe, so early mistakes stay cheap. Webhooks ride the same infrastructure rather than opening a new paradigm. Everything later derives from this contract.
- **Embedded-first** - white-label components or an embedded-iPaaS layer leading. Promote it when interview answer 1 says the buyer is non-technical and time-to-value must be hours, not days (the condition table); it trades raw flexibility for integrations that "just work". Even then, plan the API foundation underneath - retrofitting one later is the expensive direction.
- **The starved option: GraphQL-led.** Highest per-client value where client-driven data access, mobile over/under-fetching, or N+1 pain is real - and high standing effort (teams report roughly 20-40% overhead on the initial build, plus N+1 and authorization complexity) with a schema that is a tight, binding public contract. It loses every efficiency round. That named pain, confirmed by integrators, is what promotes it anyway. Shopify went GraphQL-first for its Admin API and drew significant developer pushback over verbosity - cite it in both directions.

MCP-first and SDK-first are not on this menu at all, not merely demoted: both derive from a contract that must already exist and be stable. Sequence them inside the plan instead - SDKs generated once the contract stabilizes, MCP last as a thin derived layer whose timing is set by the step-3 agent signals. Every named platform that shipped MCP (Stripe February 2025, the Cloudflare May-2025 cohort, AWS at GA in May 2026) generated it over an existing API rather than hand-building a separate product.

This ranking is a default, not a law - it shifts with context and with who executes it. Re-rank against the interview:

- Answer 1 flips the top two rungs per the condition table.
- A team already running GraphQL internally gets the starved option cheaper.
- A deal deadline (answer 7) can pull one specific surface ahead of the whole order.

Then sequence within the winning posture, one surface at a time - never several concurrently beyond the capacity number from answer 6. Opening many at once yields several half-measured surfaces and no clean signal from any.

Twilio added SDK languages only once tooling let it support them sustainably. Two surfaces done properly beat six done badly.

See [references/surface-condition-tables.md](references/surface-condition-tables.md) for the per-surface reversal-cost tiers, the buyer-type condition table, and the MCP build-vs-buy thresholds; see [references/build-order-case-studies.md](references/build-order-case-studies.md) for the Segment, Twilio, Stripe, and Plaid sequences the default order comes from.

## 5. Write the per-surface handoffs

For every surface the plan schedules, record:

- Target audience.
- The demand signal that justified it.
- Its reversal-cost tier.
- A capacity owner.
- The sibling skill that owns its design (see References).

The division of labor is fixed:

- This skill decides _that_ and _when_.
- The sibling decides _how_.

The gRPC surface's design belongs to `samber/developer-platform-skills@public-grpc-api-design`; the bulk-data/lake surface's belongs to `samber/developer-platform-skills@bulk-data-sharing-design` (file/lake exports) or `@etl-connector-strategy` (rows synced through an ELT tool), depending on which shape the demand signal points to.

CLI and embedded components have no dedicated sibling - record their design decisions in the plan itself. For a CLI, copy Plaid's 2025 dual-audience pattern - one surface, both audiences:

- Readable table output for humans.
- JSON with clean stdout/stderr separation for agents.

## 6. Set the review cadence

A surface plan decays as signals change. Set a review date (quarterly is a reasonable default) and the triggers that reopen it early:

- A deal blocked on a missing surface.
- Agent-demand signals appearing (answer 5 moving from "none" to "RFPs").
- Telemetry contradicting the audience map.
- A scheduled surface's owner losing capacity.

Record what evidence next review must re-check rather than re-arguing the whole plan.

## Failure modes

- **Novelty-driven MCP-first.** Building the newest surface first because it is new inverts the whole framework - build order is governed by reversal cost and audience, and MCP presupposes an API to wrap. Park it until step-3 agent signals move it.
- **Hand-building the MCP surface.** Every named platform derived its MCP server from an existing spec. A hand-built one is months of work re-creating what a generator produces. Build in-house only when AI access to your proprietary system _is_ the paid product.
- **Betting revenue on per-call agent monetization.** The payment rails exist (Stripe's MPP, the x402 protocol) but the unit economics are unproven - observed per-call volumes are tiny and partly wash-traded. Label any MCP monetization line in the plan as speculative.
- **Surface sprawl without telemetry.** Adding surfaces on gut feel, several at once, leaves no clean signal from any of them and a standing maintenance bill for all. One at a time, capacity-matched, telemetry instrumented first.
- **Shallow API-first.** Declaring API-first while only part of each flow is API-accessible - partners discover mid-integration that a later step still needs a manual touch. Step 2's depth probe exists to catch this before a partner does.
- **Treating API-first and embedded as rivals.** Picking one forever over-serves one side of the deal. The documented pattern is layered: API foundation, embedded accelerant on top.

## Measurement

- Plan coverage gate: every surface in the plan - scheduled, deferred, or declined - carries all five handoff fields (audience, demand signal, reversal-cost tier, owner, owning sibling or inline decision). 100% or the plan is incomplete. Iterate until it passes.
- Derivation gate: zero derived surfaces (SDKs, MCP, generated docs, an embedded layer over the API) scheduled before the contract they derive from is declared stable in step 2. Binary.
- Concurrency gate: concurrent new-surface builds never exceed the capacity number from interview answer 6.
- Trends to watch after adoption (not pass thresholds): per-surface traffic share by client type, the deal-blocker log emptying or refilling, and agent-signal changes that should reopen the plan early.

## Invocation examples

- "We have a REST API and nothing else - customers are asking for webhooks, an SDK, and 'MCP support'. What do we build, in what order?"
- "Our CEO wants us to be AI-native and ship an MCP server this quarter. Should that jump the roadmap?"
- "We sell to operations managers, not developers. Do we still need a public API before the embedded integrations our buyers ask for?"
- "Sales says we lost two deals over missing warehouse access. Where does bulk data sharing fit in our surface roadmap?"

## References

- [references/surface-condition-tables.md](references/surface-condition-tables.md) - per-surface reversal-cost tiers, the buyer-type condition table for API-first vs embedded-first, demand-signal weighting, MCP build-vs-buy thresholds and monetization caveats.
- [references/build-order-case-studies.md](references/build-order-case-studies.md) - documented surface-rollout timelines: Segment and Twilio (non-fintech, lead cases), Stripe and Plaid (fintech), and the dated MCP platform-launch wave.
- `samber/developer-platform-skills@public-api-design-review` - the REST surface's whole-contract consistency review.
- `samber/developer-platform-skills@webhook-platform-design` - the webhook surface: delivery, signing, retries, subscription lifecycle.
- `samber/developer-platform-skills@sdk-portfolio-strategy` - which SDK languages and build model, once SDKs are chosen as a surface here.
- `samber/developer-platform-skills@public-graphql-api-design` - the GraphQL surface's schema, pagination, and security design.
- `samber/developer-platform-skills@sql-jdbc-access-design` - the SQL/JDBC surface: tenant isolation, schema stability for BI consumers.
- `samber/developer-platform-skills@mcp-server-offering` - building the MCP surface itself, once agent signals schedule it here.
