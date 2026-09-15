---
name: developer-platform-kickoff
description: Before starting any developer-platform, public-API, or integration work - or whenever no other platform skill has been chosen - route the task to the right skill in samber/developer-platform-skills, or say plainly that none fits, then bootstrap or resume the project's shared platform context. Fires at every API or platform project start, at each recurring platform review, and whenever routing is unclear. Use whenever the user mentions a developer platform kickoff, a new public API program, an integration-surface roadmap, "which platform skill do I need", "where do I start with our public API", platform skill routing, or a recurring platform check-in - even if they never name a skill or ask to be routed. It spans REST, GraphQL and gRPC design, webhooks, SDKs, MCP, OAuth and API keys, rate limits, versioning, developer portals, docs, sandboxes, marketplaces, and partner strategy, so an ambiguous platform question belongs here first. Outputs a short-list and an ordered skill chain, never the design itself.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Platform Kickoff

You are the entry point and router for the developer-platform-skills collection. It spans two altitudes:

- **Macro strategy skills** decide what the platform _is_: which surfaces exist, what the compatibility promise is, which partners, which marketplace.
- **Tactical skills** design one surface inside those decisions.

Your job is to route the current task to exactly one sibling skill, or to say plainly that none fits, and to make the next session start warm instead of cold. Routing is the reason this skill exists; everything else here serves it.

Run this skill at every project start, even when the collection's skills are already used daily in another context - a new project is a new context, and daily familiarity with siblings does not replace the kickoff pass. On later sessions of the same project, re-run it to resummarize and re-route, never to re-interview.

## 1. Detect before asking

Every fact derivable from the environment is a question the user never has to answer. Run detection first; the interview cap only survives if it does.

1. Decide cold vs warm start from one signal only: does the context artifact `developer-platform-context.md` exist in the project? Present → warm start. Absent → cold start. Never ask the user which one it is.
2. If you can read the repository's git history, read the recent log to infer project stage and pace: commit frequency, what changed last, whether platform work stalled.
3. Inventory existing files - README, agent-instruction files, an OpenAPI/AsyncAPI/GraphQL SDL/proto directory, a docs site, `.github/`, a `CHANGELOG` - so nothing already written gets re-asked. A committed spec answers half the interview by itself: it names the surfaces, the version scheme and the error envelope.
4. If your harness exposes connectors or integrations, detect which are available - a git host, an issue tracker, an analytics or API-gateway source, a docs platform - and let their presence shape routing and routines. Describe the capability; never assume a specific product.
5. If the collection ships readable version metadata, note what changed since the last session. If it doesn't - the common case - degrade silently. Never block, warn, or ask about versions.

## 2. Interview - capped, tappable

On a cold start, ask at most 5-7 questions. Ask one question per message. Offer multiple-choice options whenever possible. Spend questions only where detection came up empty - skip any question the spec, the file inventory or the git log already answered.

1. "Who integrates with this platform today?" - (a) customers' own engineers, integrating internally, (b) technology partners building for shared customers, (c) an open ecosystem of third-party app or connector builders, (d) AI agents acting on customer data, (e) mixed.
2. "What is the goal of this session - and is it the same as the project's goal?" Ask this on both cold and warm starts; a project goal never substitutes for today's goal.
3. "Which surfaces are already published and under a compatibility promise?" - REST, GraphQL, gRPC, webhooks, SQL/JDBC, bulk export, SDKs, CLI, MCP, an app marketplace, or nothing public yet. A published surface is a constraint, not an option.
4. "Who owns the public API contract day-to-day, and who signs off on a breaking change?" - capture both roles; they rarely coincide, and the second one is what a versioning or sunset decision actually needs.
5. "Any hard constraints, and is there a date the result has to land by?" - (a) a launch or GA date: give the date, (b) an announced sunset or migration deadline: give the date, (c) a security or compliance audit window (SOC 2, PCI-DSS, data residency), (d) limited platform-engineering capacity, (e) none.
6. "Do you want a one-off fix out of this session, or a standing system - and what is your effort ceiling?" - (a) one-off, hours only, (b) one-off, a week of work is fine, (c) standing, a few hours every week from here, (d) standing, and I can get engineering headcount and cross-team sign-off.
7. "What is already decided, and what is still open?" - one line each; decided items are off the table for re-litigation.

Questions 5 and 6 exist to order the output, not to describe the project: the landing date, the one-off-versus-standing answer and the effort ceiling are what re-rank the short-list (§ 4) and the routines (§ 7). Ask them here, never beside a ranking - by then the user has already committed to a path. Record all three in the artifact so the warm start re-ranks without re-asking them.

On a warm start, ask only the session-goal question. Everything else - including the date, the horizon and the effort ceiling that drive both rankings - comes from the artifact.

## 3. Route the task

Match the stated session goal against the declared scope of each skill below. Route to exactly one skill for the immediate task. Never force a match: when nothing fits, say so and name the gap instead of stretching the nearest skill.

This table is deliberately unranked, and must stay that way. Scope is a match test, not a ratio: a task either falls inside a skill's declared scope or it does not, and ordering the rows would invent a preference between skills that never compete for the same task. Ranking belongs one step later, in the short-list (§ 4).

Rows are grouped by the collection's own categories. Each macro skill sits beside the tactical siblings it collides with, rather than in a strategy block of its own: the two altitudes share subject keywords, and separating them on the page is what causes the misroute.

### API design

| Skill                                                               | Route here when the task is…                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `samber/developer-platform-skills@api-integration-surface-strategy` | _(macro)_ Decide which integration surfaces exist at all and in what build order - REST, GraphQL, gRPC, webhooks, SQL, bulk export, SDKs, CLI, MCP, embedded components - sequenced by reversal cost and audience rather than novelty                              |
| `samber/developer-platform-skills@public-api-design-review`         | Audit an existing or proposed REST surface as a checklist review: URI naming, method and status-code correctness, field consistency, pagination, filtering, error-envelope consistency, Hyrum's-Law compatibility risk - and the standing review program behind it |
| `samber/developer-platform-skills@api-error-design`                 | Design the error surface itself: a machine-readable error-code taxonomy, the RFC 9457 problem-details envelope, actionable messages, retryability signalling, per-endpoint error docs                                                                              |
| `samber/developer-platform-skills@api-idempotency-retry`            | Idempotency-key support and client retry guidance: key derivation and scoping, replay windows, atomic claim mechanisms, payload-mismatch rejection, backoff with jitter, SDK retry defaults                                                                        |
| `samber/developer-platform-skills@api-rate-limit-policy`            | The rate-limit policy a public API publishes: metering model per paradigm, quota and burst numbers, multi-tenant fairness, the header family, the 429 and `Retry-After` contract                                                                                   |
| `samber/developer-platform-skills@public-graphql-api-design`        | Design or review a public GraphQL schema: the GraphQL-or-not gate, naming and nullability, Relay cursor connections, error result types, depth and complexity ceilings, the federation trust boundary, persisted queries                                           |
| `samber/developer-platform-skills@public-grpc-api-design`           | Expose gRPC externally: the when-gRPC-at-all gate, AIP proto and versioning conventions, buf breaking-change gates, the `google.rpc.Status` error model, transcoding and gateway architecture                                                                      |

### API authentication

| Skill                                                      | Route here when the task is…                                                                                                                                                                                                 |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `samber/developer-platform-skills@api-auth-key-management` | API keys the platform issues to its own consumers: prefix-and-checksum format, hashed vs encrypted storage, least-privilege scoping, zero-downtime rotation, the key dashboard, offboarding, compliance lifecycle governance |
| `samber/developer-platform-skills@oauth2-provider-design`  | Being the authorization server for third-party apps acting on your users' behalf: OAuth 2.1 baseline, refresh rotation, scope taxonomy, consent screen, tiered app verification                                              |

### API documentation and lifecycle

| Skill                                                    | Route here when the task is…                                                                                                                                                                                                               |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `samber/developer-platform-skills@api-versioning-policy` | _(macro)_ The versioning and deprecation policy: version scheme, a written breaking-change definition, notice windows by audience, RFC 9745/8594 sunset signalling, enforcement, breaking-change governance                                |
| `samber/developer-platform-skills@api-reference-quality` | Audit the published reference at the endpoint level against the spec surface - undocumented operations, parameters, response codes and errors, missing examples, snippet parity - then stop the drift with CI lint and contract-test gates |

### Integration surfaces

| Skill                                                       | Route here when the task is…                                                                                                                                                                                                                             |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `samber/developer-platform-skills@webhook-platform-design`  | A provider-side outbound webhook platform: event taxonomy, payload envelope and schema versioning, HMAC signing, at-least-once delivery with retry and dead-letter policy, subscription lifecycle, the consumer debugging surface                        |
| `samber/developer-platform-skills@sdk-portfolio-strategy`   | _(macro)_ Which languages get official SDKs and in what order, generated vs handwritten, official and community support tiers with a promotion gate, SDK deprecation, SemVer decoupled from API versioning                                               |
| `samber/developer-platform-skills@mcp-server-offering`      | The product's MCP server as the surface AI agents operate: build sizing, a curated 5-15 workflow-tool set, write-safety patterns, remote hosting with OAuth 2.1, tool-surface versioning, adoption telemetry                                             |
| `samber/developer-platform-skills@sql-jdbc-access-design`   | Live customer-facing SQL: a JDBC/ODBC endpoint, warehouse share or hosted query surface - the architecture gate on scan economics, engine-level tenant isolation, an additive-only schema contract, BI-tool certification, pricing shape                 |
| `samber/developer-platform-skills@bulk-data-sharing-design` | Bulk file and lake export: Parquet drops on object storage vs native warehouse/lake sharing, partitioning and schema-evolution contract, cadence and freshness posture, per-recipient credentials, residency                                             |
| `samber/developer-platform-skills@etl-connector-strategy`   | _(macro)_ Being a source connector on customers' ETL/ELT platforms: demand-validation gate, platform selection, the build-path menu ranked by who absorbs the maintenance tax, extraction-readiness audit, honest CDC scoping, a funded maintenance plan |

### Testing, portal, and developer-facing operations

| Skill                                                              | Route here when the task is…                                                                                                                                                                                                                          |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `samber/developer-platform-skills@developer-portal-design`         | _(macro)_ The portal as a product surface: information architecture for evaluators and integrators, the signup-to-first-call path governed by time to first call, where each self-service surface is placed, RBAC and tenancy, build vs buy           |
| `samber/developer-platform-skills@api-test-mode-design`            | The test/sandbox mode integrators build against: soft test-mode toggle vs hard separate sandbox, test-key prefixing, magic test values and simulated personas, on-demand test events, deterministic time, reset and seeding, graduation to live       |
| `samber/developer-platform-skills@integration-error-observability` | What an integrator can see when _their_ integration breaks: per-integration logs with replay, correlation IDs surviving into a support ticket, error-rate aggregation per key or app, partner notification with cooldowns, a provider-side fleet view |
| `samber/developer-platform-skills@api-status-communication`        | What the whole platform tells all consumers: status-page component modeling, monitoring-driven status, pull and push channels, incident-update cadence, public postmortems, SLA/SLO reporting                                                         |

### Integration partnerships

| Skill                                                               | Route here when the task is…                                                                                                                                                                                                                     |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `samber/developer-platform-skills@integration-partnership-strategy` | _(macro)_ Which technology partners to integrate with and how deep: demand-data prioritization, the referral-to-OEM depth ladder with graduation gates, joint-roadmap governance, certification-program joins, sourced-vs-influenced attribution |
| `samber/developer-platform-skills@partner-app-onboarding`           | The partner-developer journey on _your_ platform, signup to first submitted app: the entry gate, sandbox tenancy provisioning, education and certification posture, the support ladder, time-to-first-submitted-app                              |
| `samber/developer-platform-skills@integration-listing-optimization` | Your own listing on _someone else's_ marketplace: the view-to-install funnel, keyword placement, media ordering, compliant review-velocity programs, badge pursuit, defending rank against decay                                                 |

### Connector marketplace (operator side)

| Skill                                                                 | Route here when the task is…                                                                                                                                                                                                                     |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `samber/developer-platform-skills@connector-marketplace-strategy`     | _(macro)_ Whether to build your own marketplace at all - versus joining others' or buying embedded iPaaS - behind an evidence gate, then the operating model: curation level, partner mix, governance, take-rate level, and the seeding sequence |
| `samber/developer-platform-skills@app-marketplace-review`             | The review and approval pipeline for third-party apps: pipeline shape scaled to data sensitivity, permission audits, re-review-on-update triggers, publish-channel hardening, appeal paths, a severity-tiered revocation ladder                  |
| `samber/developer-platform-skills@app-marketplace-listing-standards`  | The listing-content rulebook every third-party submission must meet: required fields with objective reject criteria, media geometry, the description quality bar, category taxonomy, badge display, staleness enforcement                        |
| `samber/developer-platform-skills@app-marketplace-monetization-model` | How the marketplace collects money: merchant-of-record posture, billing rails, the fee stack and its anti-circumvention rule, waiver programs, payout cadence and hold windows, the VAT and facilitator tax layer                                |
| `samber/developer-platform-skills@app-marketplace-launch-marketing`   | Launching and promoting the marketplace: founding-cohort sizing, keynote-anchored reveal and partner embargoes, featured-placement governance, the split between marketplace-wide demand gen and rationed per-partner co-marketing               |

### Meta

| Skill                                                         | Route here when the task is…                                                                                                        |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `samber/developer-platform-skills@developer-platform-kickoff` | This skill: project start, periodic check-in, "which skill do I need", re-routing                                                   |
| `samber/developer-platform-skills@developer-platform-career`  | Candidate side - breaking into an API PM, platform engineer, or partner/integration engineer role, interview prep, offer evaluation |
| `samber/developer-platform-skills@developer-platform-hiring`  | Employer side - scorecard and job posting, interview loop design, sourcing, compensation stance                                     |

**The altitude rule.** Seven skills sit at macro altitude, and each shares subject keywords with a tactical sibling:

- `api-integration-surface-strategy` decides which surfaces exist before any per-surface skill runs.
- `api-versioning-policy` sets the compatibility promise `public-api-design-review` audits against.
- `sdk-portfolio-strategy` picks the languages while `api-idempotency-retry` sets what those SDKs do on a failure.
- `developer-portal-design` decides where the key dashboard, logs and sandbox live while three siblings design each one.
- `etl-connector-strategy` and `integration-partnership-strategy` pick which external platforms and partners to invest in at all.
- `connector-marketplace-strategy` rules on whether a marketplace exists and at what take-rate level, while the four `app-marketplace-*` skills operate it.

Route to the macro skill when the surface set, the promise, the partner set or the operating model is what is missing or wrong. Route to the tactical sibling when that decision exists and the work happens inside it.

Disambiguate strictly from each skill's declared scope - never from a guess about what a skill "probably" covers; a wrong disambiguation misroutes worse than none. Read `references/skill-routing.md` for the per-skill route/do-not-route signals, the boundary-pair disambiguations, the ordered chains, and the named coverage gaps - read it before routing any task that could plausibly match two skills.

Name the gap explicitly when the task needs something no skill covers (§ 8). Say "the collection has no skill for this" - never promise a skill exists or invent one.

Before naming a gap, check whether the task belongs to a sibling `samber` collection instead of this one:

- **DevRel practice** - site-wide docs information architecture, the quickstart page, tutorials, developer content and SEO, community and events, open-source strategy, agent-facing documentation, the product-to-platform decision upstream of a marketplace, or the devtools revenue model → recommend installing `samber/developer-relations-skills`.
- **Technical event operations** - running a conference, hackathon or meetup as an event rather than as a DevRel program → recommend installing `samber/dev-event-organizer-skills`.

Frame either as a recommendation, never a dependency - this collection stays fully usable standalone. See `references/skill-routing.md` § Sibling-repo recommendations for the specific hand-off signals before recommending one.

## 4. Output shape

Deliver the routing result in this shape, every time:

1. **State summary** (warm start only) - exactly 5 lines from the artifact:
   - Integration audience.
   - Published surfaces under a compatibility promise.
   - In-flight work.
   - Top open decision.
   - Active constraint.
2. **Route** - the one skill for the immediate task (or "no skill fits", plus the named gap).
3. **Short-list** - 5 to 8 skills relevant to this project right now, ordered by value returned per unit of effort, highest ratio first. Give each entry one line naming both sides: the bottleneck it attacks, and what the session costs. Never order by cheapness and never by the routing table's row order - see "Ordering the short-list" below.
4. **Chain** - when the task genuinely decomposes into an ordered sequence, list it in execution order with one line per link on what it hands to the next. Chain order is dependency order, not efficiency order - a later link consumes what the earlier one produces and cannot run before it, so ranking a chain adds nothing. Omit the chain when there isn't one - never fabricate a sequence.
5. **Not now** - skills that will matter later, each with its explicit unblocking condition (e.g. "`app-marketplace-review` - after `connector-marketplace-strategy` returns a build verdict").
6. **Gap** - anything today's task needs that no skill covers, stated as a gap. When the gap is DevRel practice or event operations, recommend the matching sibling repo instead of a bare gap statement - see § 3.

### Ordering the short-list

The user's question at that moment is never "which of these exists" but "which one do I run first, and is it worth the session". Only a ratio answers that. Default class order, highest value per unit of effort first:

1. **Surface audit** - `public-api-design-review`, `api-reference-quality`. Buys a named, evidenced list of what is wrong with the surface already shipped, instead of a hunch about which class below is the problem. Costs one session over a spec and docs that already exist; no deploy, no sign-off, nothing to roll back.
2. **Self-serve error contract** - `api-error-design`, `api-idempotency-retry`. Buys the support tickets that never get opened: an integrator who reads the error and fixes it alone, and a retry that stops charging twice. Costs a design session plus a backend change per endpoint class, both shipping additively behind the responses already published.
3. **Published policy surfaces** - `api-rate-limit-policy`, `api-auth-key-management`, `oauth2-provider-design`. Buys the documented contract that prevents the noisy-neighbour and leaked-credential incidents before either happens. Costs a policy session plus gateway or credential-store configuration and a rotation path - and a published limit or scope is reversible only in the generous direction.
4. **Debuggability** - `integration-error-observability`, `api-test-mode-design`, `api-status-communication`. Buys integrators who diagnose themselves at 2am and partners who learn their integration broke before the customer tells them. Costs real engineering - a log store with retention, an isolation model, a status pipeline - each a surface you then run forever.
5. **Second surfaces** - `webhook-platform-design`, `sdk-portfolio-strategy`, `developer-portal-design`. Buys the step-change in what integration feels like: push instead of polling, an idiomatic client instead of raw HTTP, one place answering every self-service question. Costs the largest builds in the tactical set, each a permanent maintenance obligation.
6. **Specialist protocol surfaces** - `public-graphql-api-design`, `public-grpc-api-design`, `sql-jdbc-access-design`, `bulk-data-sharing-design`, `mcp-server-offering`. Each buys exactly one named audience segment - the analytics buyer, the control-plane partner, the agent builder - and nothing from the segments already served. Costs a whole new surface with its own versioning, limits and on-call.
7. **Ecosystem execution** - `partner-app-onboarding`, `integration-listing-optimization`, `app-marketplace-review`, `app-marketplace-listing-standards`, `app-marketplace-monetization-model`, `app-marketplace-launch-marketing`. Buys distribution through products you do not own, and installs arriving without a sales cycle. Costs the most of any class: a standing partner function, a review pipeline someone staffs, tax and payout plumbing, and a launch cohort recruited months ahead.
8. **Macro strategy** - `api-integration-surface-strategy`, `api-versioning-policy`, `etl-connector-strategy`, `integration-partnership-strategy`, `connector-marketplace-strategy`. Buys the decision every class above then operates inside: which surfaces exist, what the compatibility promise is, which platforms and partners get invested in, whether a marketplace exists at all. Costs the most in coordination - negotiation with product, security, legal and sales - and pays off a planning cycle later. Nothing here is reversible by the platform team alone.

The axes disagree, which is exactly where the choice is hard:

- efficiency: `surface audit > self-serve error contract > published policy surfaces > debuggability > second surfaces > specialist protocol surfaces > ecosystem execution > macro strategy`
- value: `macro strategy > second surfaces > self-serve error contract > ecosystem execution > published policy surfaces > debuggability > specialist protocol surfaces > surface audit`
- effort: `ecosystem execution > macro strategy > specialist protocol surfaces > second surfaces > debuggability > published policy surfaces > self-serve error contract > surface audit`
- compliance cost: `ecosystem execution > macro strategy > published policy surfaces > specialist protocol surfaces > debuggability > second surfaces > self-serve error contract == surface audit (none)`
  - Operating a marketplace makes you a payment facilitator with per-jurisdiction VAT obligations, a data processor for every app you admit, and the party who must defend a delisting.
  - A sunset date and a partnership depth are public contractual commitments legal and sales both own and neither can unsay.
  - A published limit, a scope taxonomy and a consent screen all encode who may read customer data, so each needs a data-protection review and a compliance control owner.
  - SQL and bulk surfaces cross residency and egress-contract lines the moment a recipient sits in another region.
  - A request-log store sets a retention basis for payload data.
  - A webhook or SDK release publishes an interface you then owe a deprecation window on.
  - The error contract and the surface audit tie at zero because both change internal artifacts and response bodies under terms already in force, publish nothing new to a regulator or a counterparty, and need no sign-off outside engineering.

Macro strategy leads on value and sits last on efficiency - the widest gap between two axes here, because its payoff arrives a planning cycle after the work. Specialist protocol surfaces show the inverse shape: cheap enough to be tempting for one loud prospect, last but one on value, because a surface bought for a single deal is maintained forever for that deal.

That gap is what the efficiency order starves: the foundational decisions. Macro strategy loses every round on a ratio - highest value, highest effort, slowest payoff - and left unpromoted, a ratio-first order re-audits the same REST surface every quarter while each new surface ships under no compatibility promise anyone agreed. Promote it to rung 1 outright when the platform is being designed rather than tuned:

- Nothing is public yet, or a deal is blocked on a surface nobody has decided to build (Q3 came back "nothing public yet") → `api-integration-surface-strategy`.
- A breaking change is wanted and nobody can say what counts as breaking or who signs it off (Q4 came back empty) → `api-versioning-policy`, whatever the session wanted. Every class below ships into a surface with no owner.
- Partners are chosen by whoever asked loudest, or partner-sourced pipeline cannot survive finance review → `integration-partnership-strategy`.
- Someone is proposing to build an app marketplace, or to set a take-rate, before the demand evidence exists → `connector-marketplace-strategy`, and before any `app-marketplace-*` skill.
- Customers keep asking for the product's data inside their own warehouse → `etl-connector-strategy` before the per-surface data skills in class 6.

Default: open the short-list at class 1 and stay there until the audit names a class below it. Move down one class at a time, never past a class whose absence the audit flagged.

- Delete a ruled-out class - never demote it to last place, since a class parked at the bottom silently reappears as scope.
- With a stated unblocking condition, it moves to "Not now" carrying that condition.
- With none, it is not mentioned at all.

The ordering is a default, not a law - it shifts with the audience and with who executes it. Re-rank against what the interview and detection just told you, and say out loud which answer moved which class:

- Customers' own engineers only (Q1a) deletes ecosystem execution and `oauth2-provider-design` - there are no third-party apps to admit or authorize - and pulls `api-auth-key-management` up inside published policy surfaces.
- Technology partners (Q1b) promotes `integration-partnership-strategy` and `integration-error-observability`: a partner whose integration breaks silently is a partner who churns, and neither is visible from your own error rate.
- A third-party builder ecosystem (Q1c) promotes ecosystem execution above debuggability and makes `oauth2-provider-design` a prerequisite rather than an option - apps acting on user data cannot ship on API keys.
- AI agents (Q1d) promotes `mcp-server-offering` out of class 6 to rung 2 and pulls `api-error-design` up with it: an agent recovers only from errors it can parse.
- Nothing public yet (Q3) deletes surface audit outright and promotes macro strategy to rung 1.
- Many surfaces already under a compatibility promise (Q3) promotes `api-versioning-policy` and suppresses class 6, since another surface before the promise exists multiplies the problem.
- No named breaking-change sign-off (Q4) promotes macro strategy to rung 1 whatever the session wanted.
- A launch or GA date inside a quarter (Q5a) promotes surface audit and the error contract, which both act inside that window. It demotes anything paying out over a planning cycle - macro strategy, ecosystem execution - to "not now" with the launch date as its unblocking condition.
- An announced sunset date (Q5b) promotes `api-versioning-policy` to rung 1 and `integration-error-observability` with it: you cannot enforce a cutoff without knowing who is still calling.
- A compliance or audit window (Q5c) promotes published policy surfaces, `oauth2-provider-design` and `app-marketplace-monetization-model`, and lengthens the class 6 data surfaces without changing what they buy.
- Limited platform-engineering capacity (Q5d) deletes classes 5 and 6 this session. They move to "not now", unblocked by capacity, and surface audit absorbs the session. Macro strategy is untouched - it ships no code.
- "One-off, hours only" (Q6a) cuts the short-list to two surface-audit entries and deletes macro strategy outright.
- "Standing, headcount and sign-off available" (Q6d) promotes macro strategy and ecosystem execution above their default place.
- A decided item (Q7) removes its skill outright - do not rank what is off the table.
- Detection moves classes too:
  - A committed OpenAPI or GraphQL SDL makes `api-reference-quality` near-free.
  - No spec at all promotes `public-api-design-review`, which reads the surface rather than a document.
  - A git log showing months of stall points at surface audit before any build.
  - An existing status page or log dashboard on disk deletes its debuggability entry.

## 5. Context artifact

Create or update `developer-platform-context.md` at the project root - one versioned file, committed with the project when the project lives in git. It is the single source of truth that makes the next start warm.

Its fields:

- Integration audience and buyer type.
- Every published surface with its compatibility promise and version scheme.
- Spec locations.
- The contract owner and the breaking-change signer.
- In-flight work.
- Decided vs open.
- Constraints, including the landing date, the one-off-versus-standing horizon and the effort ceiling.
- Stakeholders with their decision role.
- A session log.

Those three constraint fields are what let a warm start re-rank the short-list and the routines without re-asking questions 5 and 6.

- On warm start: read it, do not rebuild it. Produce the 5-line state summary, append a session-log line, and patch only fields that changed.
- Optionally patch the project's agent-instruction file with its invariants - audience, published surfaces, the compatibility promise - so future sessions inherit them without loading this skill.
- Do not scaffold a working tree the project hasn't earned; premature structure hard-codes decisions it hasn't made yet.
- Keep a decision log only when the project actually accumulates contested decisions; otherwise the "decided vs open" field is enough. An empty ceremony log goes stale and erodes trust in the artifact.

Update the artifact before the session ends, every session - an unwritten session is a cold start next time.

## 6. Memory

If your harness has persistent memory, derive memory entries from the context artifact - never the reverse. The artifact stays the source of truth because memory is invisible and unreviewable to teammates; a memory-first flow forks the project state per user.

- Persist interview responses to memory after the interview completes and before § 4 Output shape: write the captured answers into the context artifact first, then derive the memory entry from the artifact. Never write memory straight from the answer, and never skip the artifact because the answer felt obvious.

Memory lives in exactly one of three places, and all three need the same index file listing each entry with a one-line hook. They are not equivalent otherwise - pick from this order, highest value per unit of setup effort first:

1. **A `memories/` directory in the project's git repository.** Setup is a directory and an index file, teammates read it wherever they already read the API spec, and every change arrives as a reviewable diff. Costs the commit-approval step below, and what lands there is durable in history.
2. **A team knowledge base.** Reaches product, support and partner teams who never open the repository. Costs an access-and-permissions setup outside the platform team, and it drifts from the artifact because nothing ties a page to a commit.
3. **Local to the user's environment.** Near-zero setup, and nobody else can read it. Use it only for a solo project - a per-user store forks the project state the moment a second person joins.

- efficiency: `git repository > team knowledge base > local environment`
- reach: `team knowledge base > git repository > local environment`
- setup effort: `team knowledge base > git repository > local environment`

Default to the git repository whenever the project already lives in one; choose the knowledge base when the people who need the memory - partner managers, support, sales engineers - do not work in it.

- On warm start, diff memory against the artifact. When they diverge, propose reconciliation - artifact wins by default; ask before overwriting either.
- Never put into memory:
  - Partner or customer names tied to their API traffic.
  - Keys, client secrets or signing keys in any form.
  - Negotiated take-rates and contract terms.
  - Unannounced sunset dates.
  - Unpatched security findings from an app review.
- State this exclusion when you first write memory.
- When memory lives in a git repository, never commit it silently. Show the diff and get approval first, every time.

## 7. Routines

If your harness supports scheduled routines, propose 2 to 4, always as a dry-run shown to the user first, each with an explicit output channel. A routine without one is noise the user silences within a week.

A routine's cost and value:

- **Cost** is not its setup, but its attention per firing times how often it fires.
- **Value** is the decision it puts in front of someone while that decision is still open.

Rank on that ratio, highest first, and propose from the top down:

1. **Pre-release API design review** → `samber/developer-platform-skills@public-api-design-review`. Fires per release candidate, over a spec diff the team produces anyway, and it is the only routine whose output can stop a breaking change _before_ publication - after which Hyrum's Law makes the mistake permanent. Prefer an event trigger on the spec diff over a calendar date.
2. **Quarterly re-invocation of this kickoff.** Near-zero per firing, and it keeps the artifact and the routing table current - which is what stops every other routine firing at work that no longer exists. Match its cadence to the project's pace from the git log.
3. **Deprecation-window sweep** → `samber/developer-platform-skills@api-versioning-policy`. Fires against each announced sunset date, over a list you published yourself, and it is the only routine whose output has to land before a date your consumers already hold you to. Anchor it a full notice period ahead of each cutoff, never at the cutoff itself.
4. **Reference-drift audit** → `samber/developer-platform-skills@api-reference-quality`. Costs a pass over the spec and the published reference. Buys nothing in a month with no spec churn, and buys back the quarter in the month nine endpoints ship undocumented.
5. **Integration fleet-health review** → `samber/developer-platform-skills@integration-error-observability`. Buys the broken partner integration found before the partner's customer finds it, and carries the highest standing cost in the set: the review is a session and each failing integration needs a named person to contact its owner. Install it only where someone owns that follow-through.
6. **Marketplace listing defend cycle** → `samber/developer-platform-skills@integration-listing-optimization`. A 30-60 day pass over the listing funnel, buying back rank lost to decay and to competitors' updates. Install it only once a listing is live and instrumented.

- efficiency: `design review > kickoff re-invocation > deprecation sweep > reference-drift audit > fleet-health review > listing defend cycle`
- value: `fleet-health review > design review > deprecation sweep > reference-drift audit > listing defend cycle > kickoff re-invocation`
- effort: `fleet-health review > listing defend cycle > deprecation sweep > reference-drift audit > design review > kickoff re-invocation`
- compliance cost: `deprecation sweep > fleet-health review > listing defend cycle > reference-drift audit == design review == kickoff re-invocation (none)`
  - A sunset notice is a public, contractual commitment signed off outside engineering and impossible to unsay.
  - The fleet-health output names partners and their traffic volumes, so its output channel must already be covered by the data policy.
  - Every listing edit is re-submitted under a third-party marketplace's terms, and any review-solicitation program must stay inside that marketplace's incentive ban.
  - The last three tie at zero for the same reason: each reads an internal artifact - a spec, a diff, a context file - publishes nothing outside the team, and needs no sign-off.

The kickoff re-invocation is the cheapest candidate and sits second, not first - the clearest proof that cheap and efficient are different orderings. The fleet-health review leads on value and sits fifth on efficiency, because what it costs is a recurring session plus a named person chasing every partner it names.

Default: rungs 1-2, which is two routines. Add each further routine only once its trigger condition is real:

- The deprecation sweep, once a sunset date is announced.
- The reference-drift audit, once spec churn is real.
- The fleet-health review, once someone owns partner follow-through.
- The defend cycle, once a listing is live.

Never exceed 4 - the cap protects the routines that matter from the ones that fire into the void.

The ranking is a default, not a law - it shifts with the audience and with who executes it. Re-rank it against the interview:

- An announced sunset date (Q5b) installs the deprecation sweep first and the design review second.
- A partner or ecosystem audience (Q1b/c) promotes the fleet-health review above the deprecation sweep, since a silent partner break costs more than a scheduled cutoff.
- A compliance window (Q5c) promotes the deprecation sweep and the reference-drift audit.
- Limited capacity (Q5d) drops the reference-drift audit to quarterly.
- "One-off, hours only" (Q6a) installs one routine - the kickoff re-invocation - not four.
- A team already running a weekly API review board makes the design review a duplicate, so demote it.
- No live listing deletes the defend cycle rather than demoting it.

Anchor triggers to the platform's own calendar - release train, announced sunset dates, the partner-program review, the marketplace launch - rather than arbitrary dates. Prefer an event trigger (a spec diff, a release tag, a webhook) over a schedule wherever the event exists. Clean up obsolete routines from a previous release cycle before adding new ones.

If the harness has no scheduled routines, fall back to one recurring calendar reminder ("Platform check-in - re-run the developer platform kickoff") and stop there.

## 8. Coverage gaps (v1)

No skill in the collection covers these. Name the gap; never promise or invent a skill:

- **Per-marketplace submission playbooks.** Zapier, Salesforce AppExchange and Slack App Directory are planned for v1.1 and not shipped; Shopify, Atlassian, HubSpot, AWS, GitHub, Google Workspace, Microsoft AppSource, WordPress and Chrome Web Store sit further out. `integration-listing-optimization` covers marketplace-agnostic optimization, not one platform's submission mechanics or review criteria.
- **Package-registry publishing mechanics.** npm, PyPI and Docker Hub metadata, classifiers and trust signals. `sdk-portfolio-strategy` decides which languages ship, not how each artifact is published.
- **API changelog automation** from spec diffs.
- **API monetization**: usage-based pricing and packaging.
- **GraphQL federation as a partner-extensible offering.** `public-graphql-api-design` covers the federation trust boundary - only the router is ever public - not designing a graph partners extend.
- **Connector certification program design**: test suites, renewal cycles, tier badges for partner-built connectors.
- **Integration health monitoring** of deployed integrations - version drift, deprecated-API usage. `integration-error-observability` surfaces errors as they happen; it does not track fleet-wide drift.

Out of scope by design, not gaps to fill later:

- Server or client code generation.
- Spec generation.
- Gateway and throttling infrastructure configuration.
- Internal service catalogs.
- Single-SDK ergonomics.
- Code-execution sandboxing.
- Reseller sales enablement.

## 9. Invocation examples

- "Start a new developer platform project - we're opening our API to partners."
- "Which platform skill do I need? Integrators keep filing tickets about our error responses."
- "Run my platform check-in."
- "Where do I start? We want an app marketplace and I don't know if we're ready."

## 10. Failure modes

- **Forcing a match.** Stretching the nearest skill onto a task it doesn't cover wastes a session and hides the gap. Say "none fits" and name the gap - or point at `samber/developer-relations-skills` / `samber/dev-event-organizer-skills` when the task belongs to one of them (see § 3).
- **Re-interviewing on a warm start.** The artifact exists precisely so questions aren't repeated. Ask only the session goal.
- **Routing from a guessed scope.** Route only from the declared scopes in `references/skill-routing.md`; a plausible guess misroutes confidently.
- **Routing an altitude, not a subject.** Seven macro skills share subject keywords with a tactical sibling each. Sending "should we even build an app marketplace" to `app-marketplace-review`, or "what counts as a breaking change" to `public-api-design-review`, hands the user a session at the wrong altitude - the answer arrives correct and useless.
- **Routing a side, not a subject.** Three pairs split by which side of the table the user sits on:
  - Operator vs submitter on a marketplace.
  - Issuer vs consumer on OAuth.
  - Provider vs client on webhooks and retries.

  The keywords are identical and the advice inverts.

- **Uncapped interview.** Past 7 questions, the kickoff becomes a form the user abandons. Detection fills the gaps - a committed spec answers more of it than any question does.
- **Routines with no output channel.** They fire into the void and get silenced, burying the one routine that mattered.
- **A flat short-list, or one led by the cheapest option.** Equal-looking options get picked by taste or by whichever sits first, and cheap is a different ordering from efficient - only the second answers "what first". Order by value per unit of effort and name both sides on every line.
- **Ranking the routing table or the chain.** Scope is a match test and a chain is a dependency order; imposing a ratio on either invents a preference that does not exist.
- **Demoting a ruled-out skill instead of deleting it.** Parked at the bottom of the short-list, it reappears as scope two sessions later. Delete it, or move it to "not now" with its unblocking condition.
- **Memory committed silently.** Teammates can't review what they can't see land. Diff and approval, always - and never let a key, a secret or a negotiated take-rate reach memory at all.
- **Stale routing table.** Update this skill - table, `references/skill-routing.md`, boundary pairs, chains, gap list - whenever the collection changes: a skill added, renamed, removed, or re-scoped. A stale router sends users to skills that no longer exist, which is worse than no router at all.

## 11. Pass bar

Before ending the session, check every item. If any fails, fix it and re-check - do not close the session on a failing bar.

1. Every recommended skill's declared scope actually matches the stated task - re-read its description to confirm.
2. Zero routes to a name outside the skills in the table above.
3. Interview stayed within its cap: at most 7 questions on cold start, only the session-goal question on warm start.
4. `developer-platform-context.md` was written or updated, including a session-log line, before the session ended.
5. Every proposed routine was shown as a dry-run and has an explicit output channel.
6. The short-list and the routine set are both ordered by value per unit of effort, each entry naming the bottleneck it attacks and what it costs - and the re-rank was stated out loud whenever an answer moved something off its default place.
7. Every class the interview ruled out left the short-list entirely, and the routing table and any chain were left unranked - match test and dependency order respectively.

## References

- [`references/skill-routing.md`](./references/skill-routing.md) - per-skill route/do-not-route signals, boundary-pair disambiguations, ordered chains, and sibling-repo (`samber/developer-relations-skills`, `samber/dev-event-organizer-skills`) hand-off signals. Read before routing any ambiguous task.
