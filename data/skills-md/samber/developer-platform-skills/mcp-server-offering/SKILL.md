---
name: mcp-server-offering
description: Design a SaaS product's MCP server as a product surface AI agents operate - sizing the build investment, curating a 5-15 workflow-tool agent surface instead of mirroring API endpoints, named write-tool safety patterns (scoped credentials, read-only lockdown, human-in-the-loop approval, risk-tiered server-side gates, dry-run preflight, idempotency and spend caps), remote hosting with OAuth 2.1, versioning the tool surface, MCP registry discoverability, and measuring agent adoption. Use whenever the user mentions MCP, Model Context Protocol, an agent-facing tool surface, exposing a product to AI agents or coding assistants, or MCP write-tool safety - even if they never say "MCP server". Design layer only - code-generation MCP builder skills scaffold what this specifies.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# MCP Server Offering

You are an MCP product-surface designer. Design what a SaaS product exposes to AI agents through an MCP server - which tools, under what safety limits, behind what auth, versioned and measured how - so agents operate the product reliably and the vendor knows whether the investment pays.

This is the design layer. The popular MCP "builder" skills and per-language generators on skills.sh are one altitude below: they scaffold the server code once you know what it should expose. Whether to offer MCP at all is decided one altitude above, by `samber/developer-platform-skills@api-integration-surface-strategy` - this skill starts once MCP is on the roadmap.

## Clarifying questions

Ask these before designing anything; each answer changes a later step. Batch them - this is a tactical design task, not a strategy interview.

1. Demand evidence: has MCP appeared in buyer RFPs or security questionnaires? Are customers or a community-built server already filling the gap? (a community server existing is both a demand signal and a displacement path - see step 6)
2. What existing API surface can the tool set derive from - a stable public REST/GraphQL contract, an internal-only API, or no machine-readable interface at all? (the last case changes the ROI framing - see step 1)
3. Write appetite: is read-only acceptable for launch? Which write actions do agents genuinely need, and which of those are irreversible, financially consequential, or send messages to humans?
4. Hosting posture: a remote endpoint serving many concurrent clients, or a local process beside a developer's own tools? What multi-tenant edge infrastructure already exists?
5. Auth infrastructure: does the product already run an OAuth 2.1-capable authorization server, or would MCP be the first OAuth consumer? (the authorization-server side is `samber/developer-platform-skills@oauth2-provider-design` territory; this skill owns only the MCP resource-server posture)
6. The date the server must land by, whether this is a procurement checkbox or a compounding product surface, and the effort ceiling (engineering hours, ongoing maintenance appetite, reversibility). These answers re-rank both menus below - a hard RFP deadline promotes managed hosting and read-only launch; a compounding mandate promotes the starved options.

## Audience split: agent-consumer type

What changes the design is which kind of agent calls in and how supervised it is:

- **End-user assistant clients** (chat apps, desktop assistants) - a human watches the conversation. Client-side approval prompts work, Markdown responses matter, and an MCP Apps UI (step 8) lands here. The write risk is a confused human approving too fast, not an unattended loop.
- **Enterprise agent fleets** - background agents, often behind the customer's own gateway, sometimes unattended. Server-side enforcement is the only control that holds (the operator can swap clients), attribution and audit matter most, and enterprise-managed authorization and private registry mirrors shape distribution.
- **Developer-tool clients** (IDE and CLI agents) - technically sophisticated callers, tolerant of local stdio transport, discovered through registries and docs rather than sales.

Design for the most demanding type present. A surface safe enough for unattended enterprise fleets serves supervised assistants for free; the reverse is false.

## Workflow

1. Size the build investment.
2. Curate the tool surface.
3. Apply write-tool safety patterns.
4. Choose hosting and auth.
5. Version the tool surface.
6. Publish for discoverability.
7. Measure agent adoption.
8. Roll out in stages.

Each step has a section below, in order.

If your harness has persistent memory, record what this workflow decides:

- The curated tool list, with each tool's risk tier.
- The hosting and auth posture.
- The rollout stage the server currently sits at.
- Every threshold recalibrated against your own telemetry.

A later run then extends a known surface instead of re-deriving it, and the user stops re-explaining the design every session.

## 1. Size the build investment

The honest baseline: for most B2B SaaS vendors an MCP server is defensive positioning that is becoming procurement table stakes - the competitive question has shifted from "supports MCP" to "supports MCP well."

- Only a handful of vendors have published hard first-party impact data. Atlassian's disclosure is the strongest dataset that exists: 5M+ tool calls per working day, roughly a third of them writes, 44% more accurate answers using 48% fewer tokens.
- The citable production-adoption baseline is a Dec 2025 survey of 300 technical leaders putting ~41% of software organizations in limited-to-broad MCP production.
- Only 11-14% of enterprise agentic pilots reach production, and they stall on exactly the identity, audit, and access-control gaps steps 3-4 close.

- One real exception to the defensive framing: a vendor with no public API at all. Roughly half of companies shipping MCP servers had no public REST API - for them MCP is the first machine-readable interface they ever shipped, a genuinely new acquisition channel rather than a defensive duplicate.
- Budget honestly: a demo-grade server is a weekend; a production-grade one is months of work plus a standing maintenance commitment (a simple hand-built API-integration server alone runs an estimated 150-250 hours). This gap is what the hosting menu in step 4 prices.
- The decision rule that overrides everything else: if MCP appears as a hard requirement in actual buyer RFPs, accelerate past the staged timeline (step 8) straight to write tools or UI. Conversely, if tool-call volume stays flat and no RFP demand materializes after two full quarters, treat the server as low-maintenance table stakes and explicitly defer the production build until demand is proven.

Ground every business case in [references/evidence-and-do-not-cite.md](references/evidence-and-do-not-cite.md) - it ranks the evidence by strength and lists the widely-circulated figures that are debunked or unverifiable. Citing one of those poisons the whole case.

## 2. Curate the tool surface

The comprehensive-vs-curated debate is resolved: curated won. Do not present this as an open trade-off.

- The real-world median across 1,412 analyzed servers is 5 tools.
- Tool metadata alone can consume 40-50% of an agent's context window before any work happens.
- The named vendor guidance converges: design top-down from user workflows, never bottom-up from API endpoints; "one server, one job"; 5-15 tools.

- Derive tools from the existing, stable API contract rather than hand-building a parallel surface - every major platform that shipped a hosted server generated it on top of an existing REST or GraphQL API. If the contract isn't stable yet, that's a sequencing problem for the umbrella sibling, not a reason to hand-build.
- Collapse granular endpoints into workflow-level tools (one `upload_file(path, owner)` instead of `get_user()` + `upload_file()`). The agent's question is "what job can I do", not "what endpoints exist".
- Reserve breadth patterns - a generic execute-any-endpoint escape hatch, toolset grouping the client enables selectively, dynamic tool loading - for a proven breadth requirement, never as the default shape.
- Tool descriptions are the single highest-leverage design lever measured: description-only tuning has measurably cut agent error rates with no code change. Write each description for an alien collaborator - when to use the tool, required vs optional parameters, expected output, and how it differs from its near-neighbors. Budget real engineering time here.
- Mistake-proof the parameters (poka-yoke): shape arguments so the wrong call is structurally hard (absolute identifiers over relative ones, enums over free strings), instead of documenting correct usage and hoping.
- Mechanics:
  - Verb-first, service-prefixed snake_case names (`acme_list_invoices`) - the namespace is shared with every other server the agent runs.
  - Honor a `limit` parameter and return cursor/has-more fields, defaulting to 20-50 items.
  - Support JSON and Markdown response formats.
  - Set the read-only/destructive/idempotent annotations honestly, and treat them as hints for clients, never as security controls.
  - Report tool errors inside the result with an actionable message, never as protocol errors leaking internals.
- Give every tool exactly one risk level (step 3). A tool that both reads and irreversibly writes is two tools.

## 3. Apply write-tool safety patterns

Six named patterns, each proven by a specific vendor, detailed in [references/write-safety-patterns.md](references/write-safety-patterns.md). They stack rather than compete, so the ranking orders adoption - which to ship first, never which to ship instead. The axes disagree, so each gets its own line:

- protection: `risk-tiered policy gates > human-in-the-loop approval > scoped credentials == read-only separation > idempotency + spend caps > dry-run preflight`
- effort: `risk-tiered policy gates > human-in-the-loop approval > dry-run preflight > idempotency + spend caps > scoped credentials == read-only separation`
- efficiency (protection per unit of effort): `scoped credentials == read-only separation > risk-tiered policy gates > idempotency + spend caps > dry-run preflight > human-in-the-loop approval`

Human-in-the-loop approval sits second on effort even though building it is a day's work: its real cost is the standing human attention it consumes on every gated call, forever - which is exactly right for the calls that deserve it and unaffordable everywhere else. The scoped-credentials / read-only-separation tie is genuine on all three axes: both are server-side enforcement invisible to a well-behaved agent, both are configuration on the credential model rather than new machinery, and read-only separation is just scoped credentials taken to the extreme.

- **Default rung**: scoped credentials plus a verified read-only mode from day one; human-in-the-loop approval on every contained write; irreversible or deployment-triggering tools disabled by default. The two top-efficiency patterns carry that combination, and approval is affordable alongside them only because early write volume is low - the condition that expires, and the one that promotes the starved option below.
- **Starved option**: risk-tiered server-side policy gates (classify every call as Read Only / Minimal Impact / Contained Write / Critical, then pass, enrich with agent attribution plus async audit, or block before the handler runs). Highest protection and highest build effort at once, so the efficiency order never puts it first and it keeps getting deferred - promote it anyway the moment background agents run unattended, write volume grows past what humans can approve, or the first write incident lands. The vendor that built it did so after an unattended agent closed thousands of tickets.
- The test every pattern must pass: enforcement lives server-side, so **an end user cannot bypass it by switching clients**. Client-side approval prompts and annotation hints fail this test on their own.
- Name the industry gap honestly: undo/rollback is largely absent ecosystem-wide; attribution plus audit trails are the current substitute for true reversibility, not a solved answer.
- This ranking is a default, not a law. Re-rank against question 3's write list and anything you know about the user - a product whose writes send emails or move money promotes dry-run and caps immediately; a pure-analytics product may never need more than the default rung.

## 4. Choose hosting and auth

Three hosting postures, ranked:

- effort: `self-hosted remote > remote managed platform > local stdio`
- value: `self-hosted remote == remote managed platform > local stdio`
- efficiency: `remote managed platform > local stdio > self-hosted remote`

The value tie is genuine: the agent client sees the same OAuth-protected endpoint either way - hosting is invisible to the buyer until a custom server-side policy layer or residency constraint appears, which is precisely the promotion condition.

- **Default rung: remote managed platform.** The protocol shipped four backward-incompatible revisions in its first twenty months; a managed platform absorbs that churn plus the mandatory OAuth machinery, and the economics tilt further toward managed once a few enterprise integrations exist. A hard deadline from question 6 reinforces this rung.
- **Starved option: self-hosted remote.** Highest control and highest effort - months to production-grade plus standing maintenance. Promoted when the MCP server _is_ the product (vertical SaaS, proprietary dataset, regulated workflow - agent access is what customers pay for), when a custom risk-tier policy layer from step 3 must run in your own infrastructure, or when existing multi-tenant edge infrastructure flips the effort line.
- **Step down to local stdio** for developer-tool products operating on the user's own files and processes: single client, near-zero hosting effort, environment-variable credentials, and explicitly exempt from the OAuth requirements below. Rule it out entirely - not just demote it - when the audience is enterprise agent fleets, which consume hosted endpoints.
- This ranking is a default, not a law; re-rank against questions 4-6.

Auth rules for any remote posture (spec revisions are date-stamped and move fast - always verify you're citing the latest one; this section is written against the 2026-07-28 revision):

1. The MCP server is an OAuth 2.1 **resource server**: it validates tokens, it never mints them. Designing the authorization server behind it is `samber/developer-platform-skills@oauth2-provider-design` territory; keep only the MCP-specific posture here.
2. Publish protected-resource metadata (RFC 9728).
   - Require resource indicators (RFC 8707), and reject any token not issued specifically for this server - that is the mechanism stopping a token minted for one MCP server being replayed against another.
   - The 2026-07-28 revision additionally mandates issuer validation (RFC 9207) and rewrites the transport core stateless: design every server instance interchangeable behind a plain load balancer, never session-pinned.
3. Never forward a caller's bearer token to an upstream API - the spec forbids this confused-deputy shape outright. Obtain your own upstream token via token exchange, acting as an OAuth client to the upstream system.
4. Read the compliance statistics as bimodal, never as one number: the often-quoted single-digit OAuth-compliance percentage is dragged down by a long tail of community stdio servers, while vendor-hosted servers default to OAuth 2.1. Implementing it properly is what passes enterprise security review - table stakes for this population, not an above-and-beyond flourish.
5. Hardening floor regardless of posture:
   - Schema-validate every input, and bound sizes and ranges.
   - Sanitize paths.
   - Never leak internal errors to the client.
   - On locally-run HTTP servers, validate the Origin header and bind to localhost (DNS-rebinding protection).

## 5. Version the tool surface

Three layers, versioned separately - treating "MCP versioning" as one decision is the mistake:

1. **Protocol version**: date-based revisions with a formal feature lifecycle (Active → Deprecated → Removed, minimum 12 months between the last two). Track deprecations - the original transport, for instance, entered a grace window early in the protocol's life - and pin exact SDK versions for reproducible builds.
2. **Your server's public API**: ordinary semantic versioning. Renaming or removing a toolset name is a major version - agents key on names for discovery, so a rename breaks them silently. General deprecation machinery is `samber/developer-platform-skills@api-versioning-policy` territory; what stays here is the layer below.
3. **The tool-surface contract itself - names, descriptions, schemas - which no spec standardizes yet.** A tool's description is a compiled interface, not documentation: an analysis of 61,097 catalogued tools found a description wording change measurably alters the model's probability of selecting that tool - a breaking change even when the JSON schema is untouched, and one schema-diff CI cannot catch. Nothing breaks loudly anymore; the agent just adapts, sometimes wrongly.

Discipline for layer 3, since the spec won't impose it:

- Default every change to additive, and alias old tool names instead of renaming.
- Hash the full surface (names + descriptions + schemas) to catch silent drift.
- Run golden-prompt behavioral tests in CI: a fixed set of representative tasks that must still select and call the right tools after any description edit.
- Carry a version marker in the response envelope, and log it on every call.
- Publish a deprecation window of at least 90 days with machine-readable response-header signaling.

Ship a description edit through the same review gate as a code change, never as a docs fix.

## 6. Publish for discoverability

- Publish to the official MCP registry under a DNS-verified reverse-domain namespace. Know what that listing signals: the registry is a metadata catalog with namespace-ownership proof and community moderation - it certifies nothing about security, so don't lean on listing as a trust claim to buyers.
- The official registry is necessary, not sufficient: human developers browse the curated third-party directories, so fan the listing out to them (automation tools exist for the fan-out) rather than stopping at one entry.
- Expect large customers to mirror the registry into private, allowlisted internal catalogs. Your listing's metadata and version history must stay accurate specifically because it gets re-consumed by machines applying policy, not just browsed.
- A first-party server, once published, tends to displace community-built substitutes for the same product rather than compete alongside them - if question 1 surfaced a community server, publishing well is also how you retire the unofficial surface agents currently trust.

## 7. Measure agent adoption

- Instrument tool calls as OpenTelemetry spans (session → tool invocation → downstream operation) rather than a bespoke event schema - the audience for this data in an enterprise deployment is the customer's existing observability stack, not only your dashboard. An auto-instrumenting wrapper beats hand-instrumenting each tool as the surface grows.
- The converged metric set: call volume, success/error rate, per-tool usage, active users, and client distribution (which agent client calls in). The purpose is dual - confirm the server is used at all, and see whether adoption is broad or concentrated.
- Registry listings and package downloads measure install interest, never runtime usage - only in-server telemetry answers the adoption question. Don't let a download count into a business case as a usage figure.
- Assume your telemetry is not the only visibility layer: large customers front your server with their own gateway. Design your metrics to be correlatable (stable tool names, request ids), not exclusive.
- When the data is good, publish it - the strongest ROI evidence in the ecosystem is one vendor's first-party disclosure: call volume, write share, non-technical-user share, enterprise share, retention by cohort, accuracy, and token-efficiency gains. That disclosure shape is the model to match, detailed in [references/evidence-and-do-not-cite.md](references/evidence-and-do-not-cite.md).
- Surfacing per-customer integration failures back to the developers who own them is `samber/developer-platform-skills@integration-error-observability` territory.

## 8. Roll out in stages

Full stage detail, thresholds, and the MCP Apps decision live in [references/rollout-stages-and-thresholds.md](references/rollout-stages-and-thresholds.md). The skeleton:

1. **Read-only launch**: the curated 5-15 tools, OAuth 2.1 from day one, OpenTelemetry from the first call, registry publication. Proceed only on sustained tool-call volume from real agent clients (not demo spikes) with tool-error rate under 2%.
2. **Graduated writes**: risk tiers enforced server-side, approval on contained writes, critical tools disabled by default, scoped credentials, attribution plus async audit, idempotency keys, dry-run where feasible. Expand write scope only on a clean audit trail, zero unattributed writes, and proven approval-flow reliability.
3. **Differentiate**: an interactive MCP Apps UI for the single highest-value workflow (approval screen, filterable dashboard, configuration wizard) - after validating that target customers' security teams accept iframe-rendered third-party UI in their assistant, which is still an open question, not a settled yes. Institutionalize the layer-3 versioning discipline and publish impact metrics.

The RFP-pressure override from step 1 cuts across this sequence in both directions: hard procurement demand accelerates past stages; two flat quarters park the server at stage 1 as maintained table stakes.

## Failure modes

Anti-pattern checklist - each is a direct review finding:

- The comprehensive-mirror trap: one tool per API endpoint. Agents mis-pick among near-duplicates and context drowns in metadata before any work happens.
- A destructive tool that is live-only - no dry-run, no approval gate, no disabled-by-default tier. Community servers have shipped order-cancellation tools that silently email real customers.
- A hand-built parallel surface where a derived one was available - double maintenance and guaranteed drift from the real API contract.
- A tool-description edit shipped as a docs fix, bypassing review and behavioral tests, silently changing which tools agents select.
- Forwarding the caller's bearer token upstream - the spec-forbidden confused-deputy shape.
- Trusting a read-only flag without verifying it: a documented vendor bug shipped write tools despite the flag being set. Test the lockdown, don't configure it and assume.
- Treating tool annotations (read-only/destructive hints) as security controls - they are advisory metadata for clients; enforcement belongs server-side.
- Citing a debunked adoption statistic in the business case - see the do-not-cite list in [references/evidence-and-do-not-cite.md](references/evidence-and-do-not-cite.md).
- A session-pinned server design - the protocol's stateless rewrite made instance-interchangeability the baseline expectation.

## Measurement

Four binary gates - iterate the design until all pass:

- Safety coverage: every write-capable tool carries exactly one risk tier and at least one named pattern from step 3's taxonomy, and every irreversible tool is approval-gated or disabled by default. One uncovered write tool fails the gate.
- Auth conformance (remote servers): protected-resource metadata published, token audience validated, no bearer-token passthrough upstream. Binary per the spec's own MUSTs.
- Evidence hygiene: zero figures from the do-not-cite list in any produced business case or deliverable.
- Curation: the launched surface stays within 5-15 tools unless a proven breadth requirement is documented, with every tool named per step 2's conventions.

The stage-transition thresholds (error rate under 2%, clean audit trail) are based on one vendor's read-only-first practice, not an industry standard - treat them as defaults to calibrate against your own first month, and the adoption metric set from step 7 as trends to baseline, never pass thresholds.

## Invocation examples

- "We have a stable REST API and customers asking for agent access - design our MCP server: which tools do we expose and how do we secure the write ones?"
- "Our MCP server mirrors 60 API endpoints and agents keep calling the wrong tool - redesign the surface."
- "Agents should be able to create and cancel orders through our MCP server - design the safety, approval, and audit model before we ship it."
- "Leadership wants an MCP server because a competitor shipped one - how much should we actually invest and in what order?"

## References

- [references/write-safety-patterns.md](references/write-safety-patterns.md) - the six write-safety patterns with their named vendor implementations, the negative example, and the approval-primitive detail.
- [references/rollout-stages-and-thresholds.md](references/rollout-stages-and-thresholds.md) - the three rollout stages with go/no-go thresholds, and the MCP Apps UI decision.
- [references/evidence-and-do-not-cite.md](references/evidence-and-do-not-cite.md) - adoption/ROI evidence ranked by strength, the disclosure model to match, and the debunked figures never to cite.

See also, same collection:

- `samber/developer-platform-skills@api-rate-limit-policy` - the quota and throttle policy agent traffic runs under, including per-tool and per-credential limits.
- `samber/developer-platform-skills@developer-portal-design` - where the MCP server's docs, connection guide, and credentials live in the developer portal.
