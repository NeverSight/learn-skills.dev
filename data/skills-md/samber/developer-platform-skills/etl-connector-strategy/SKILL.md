---
name: etl-connector-strategy
description: Plan a SaaS vendor's presence as a source connector on third-party ETL/ELT platforms - demand validation before any build, platform selection from where customers' data stacks run, a build-path menu (platform-managed listing, vendor-maintained SDK connector, custom open-source tap) ranked by who absorbs the maintenance tax, an extraction-readiness audit of the product API, honest CDC scoping (API sources ship pseudo-CDC, never log-based), certification targets, and a funded maintenance plan. Use whenever the user mentions an ETL or ELT catalog listing, a source connector, data-pipeline integration, or adding CDC - even if they never say "connector strategy". Do NOT use for the vendor's own inbound marketplace - use samber/developer-platform-skills@connector-marketplace-strategy instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# ETL Connector Strategy

You are a data-integration strategist for a SaaS vendor. Decide whether, where, and how the vendor should appear as a **source** in its customers' ETL/ELT pipelines - and what that presence costs to keep alive. Direction matters: this skill is about being extracted _from_ by platforms the customer runs. Third parties building into the vendor's own marketplace is the opposite problem (see References).

Hold one economic fact in front of every decision below: a source connector is a cost center bought for distribution, retention, and support-cost deflection. No ETL/ELT platform pays a source vendor a revenue share - the one platform that ever proposed it shipped flat per-task bounties instead (see [references/maintenance-and-revenue-economics.md](references/maintenance-and-revenue-economics.md)).

## Interview

This is a strategy interview: one question per message, multiple-choice where possible. Each answer gates or re-ranks a later step.

1. Demand evidence - what observed customer pull exists? (a) support tickets asking for a named ETL platform; (b) lost-deal or churn notes citing data-stack incompatibility; (c) customers hand-rolling pipelines against your API, visible in API logs or support load; (d) none yet - internal hypothesis only.
2. Customer stacks - which extraction platforms do your customers' data teams actually run? (a) managed commercial ELT; (b) self-hosted or open-source ELT; (c) open-source-first tap ecosystems; (d) unknown - must be found out before anything else proceeds.
3. Extraction-readiness - does your public API already expose a stable incremental cursor (or reliable `updated_at`), a bulk/backfill path, and a delete signal? (a) all three; (b) cursor only; (c) UI-grade CRUD endpoints only; (d) unsure.
4. Maintenance capacity - who owns the connector in month 13? (a) a named team with standing budget; (b) a side-task on an existing team; (c) nobody yet.
5. Deadline - must catalog presence land by a date (a sales cycle to unblock, a competitive evaluation), or is there none?
6. One-off or compounding - is this a checkbox for one deal, or a standing distribution asset?
7. Effort ceiling - engineering weeks available up front, and hours per month sustainable after launch?

Questions 5-7 re-rank the build-path menu in step 3:

- A hard deadline promotes the platform-managed queue.
- A compounding mandate plus real capacity promotes the SDK rung.
- A near-zero effort ceiling demotes everything except the queue - or the decision not to build yet.

## Customer data-stack maturity

The strategy splits by **which stacks customers' data teams run** - only customers with a warehouse and a data team extract anything, whoever the vendor sells to:

- **Managed-ELT shops** - enterprise-leaning teams on commercial managed platforms. Presence means passing that platform's gated listing review, and the platform's curation is the quality signal buyers read.
- **Self-hosted / open-source ELT shops** - cost-sensitive or data-sovereignty-driven teams. Listing is an open contribution process with a low bar; the optional certification tier is the differentiator.
- **Open-source-first tap ecosystems** - teams composing open-spec taps and targets themselves. The cheapest presence to establish and the fastest to decay unmaintained (see Failure modes).

Interview answer 2 decides which segment is served first. Build where the observed customer stacks are, never where the vendor's engineers would prefer to build.

## Workflow

1. Demand-validation gate.
2. Platform selection.
3. Build-path choice (ranked menu + brainstorm).
4. Extraction-API readiness audit.
5. CDC honesty scoping.
6. Certification path.
7. Maintenance plan.

Each step has a section below, in order. Do not reorder: steps 1-2 supply the evidence steps 3-7 spend.

## 1. Demand-validation gate

- Approve no connector build on hypothesis. Collect named, verifiable evidence: support tickets requesting a platform by name, lost-deal notes citing data-stack mismatch, API logs showing hand-rolled extraction (high-frequency paginated scans from data-team service accounts), security/procurement questionnaires asking about warehouse sync.
- The documented business case clusters around four drivers:
  - Relief of customers' non-core maintenance burden.
  - Distribution through the platform's network of destinations.
  - Competitive table stakes in data-stack evaluations - major catalogs run 500-700+ connectors, and absence reads as a gap, not a neutral fact.
  - Retention/support-cost deflection.
- Keep the business case inside what the quotable evidence actually covers: the strongest rationale (ezCater's "a large investment in a platform that's not part of our core business") comes from a data _consumer_ building its own tap, not from a SaaS vendor instrumenting its own product as a source. Promise the driver, never an ROI figure.
- If evidence is thin, stop here. Recommend improving the raw API or direct-to-storage delivery instead (see References), and name the signal that would reopen this decision (e.g. three named-platform tickets in a quarter, one lost deal citing the gap).
- Route mismatched demand out to the sibling skill it actually fits:
  - "files in our bucket" is bulk data sharing.
  - "live SQL against your data" is SQL access.

## 2. Platform selection

- Follow interview answer 2 - target the platform archetype your customers' evidence names, one platform first, a second only after the first connector's maintenance load is measured.
- The three archetypes gate differently:
  - The curated platform gatekeeps _entry_: a multi-week review that can reject a source outright.
  - The open-contribution platform gatekeeps _labels_: anyone lists, and certification is the earned tier.
  - The open-spec tap ecosystem has no gate at all - and no floor either.
- Read [references/platform-program-tables.md](references/platform-program-tables.md) before committing: it holds the named programs, submission paths, review timelines, release-phase clocks, and support-tier taxonomies per platform, as a dated snapshot to re-verify.
- If answer 2 was "(d) unknown", commission the finding first - a short customer/prospect survey or a pass through integration-request tickets - and suspend the workflow until it lands.

## 3. Build-path choice

The decision axis is who absorbs the maintenance tax - annual upkeep running an appreciable fraction of the original build cost, every year, per connector (vendor-published estimates; the figures and their sources are in step 7). Three paths, ranked:

- effort (descending): `custom outside-platform connector > vendor-SDK connector > platform-managed listing`
- maintenance-tax exposure (descending): `custom (100% yours) > vendor-SDK (split: platform hosts, you fix) > platform-managed (platform absorbs)`
- control over quality and cadence: `custom == vendor-SDK > platform-managed`
- compliance cost (descending): `platform-managed > vendor-SDK > custom` - the managed path triggers the platform's own source review, which can reject outright, and a binding release-phase promotion clock; the SDK path commits you to the platform's contribution terms and update cadence; the custom path triggers no external review and stays fully reversible.
- efficiency: `platform-managed > vendor-SDK > custom`

The `==` tie is genuine: on both the custom and SDK paths, every implementation decision (cursor logic, incremental semantics, update cadence) stays with the vendor; the platform only changes who hosts and distributes the code, not who decides.

- **Default rung: the platform-managed listing.** The platform's request program builds and maintains the connector; the vendor supplies API documentation and a contact. Lowest tax exposure, fastest to a badge. Its real costs:
  - A review gate of weeks that can reject the source outright.
  - Zero control over feature scope and cadence.
  - A fit limited to sources with stable, non-dynamic schemas.
- **Promote to the vendor-SDK connector** when any of these hold:
  - Validated demand justifies standing engineering.
  - The managed queue rejected the source, or the schema is too dynamic for the platform's lightweight path.
  - Control over cursor logic and update cadence is worth owning the tax.

  The vendor writes and maintains the connector on the platform's SDK; the platform hosts and distributes it.

- **The starved option: the custom outside-platform connector** (bespoke pipeline or open-spec tap). Highest control and full platform independence, highest effort and 100% of the tax - it loses every efficiency round. It is promoted anyway when no platform covers the need, or when a strategic customer segment runs open-source-first stacks the commercial platforms don't reach. Carry the decay warning with it (see Failure modes).

This ranking is a default, not a law. Re-rank against interview answers 5-7 and anything else known about the vendor, for example:

- A team already fluent in the platform's SDK language gets the SDK rung nearly free, which moves the effort line.
- An API too custom for the platform's declarative layer deletes the platform-managed rung rather than demoting it.

Then brainstorm before deciding: present 2-3 candidate strategies (each a platform × build-path × resource-scope combination) with trade-offs (time to catalog presence, who owns the tax, control retained) and one argued recommendation. Get an explicit pick from the user before step 4.

## 4. Extraction-API readiness audit

Audit the product API against [references/extraction-readiness-and-cdc.md](references/extraction-readiness-and-cdc.md) before any build starts, and sequence fixes ahead of connector work. This is the single highest-ROI investment in the whole strategy: it cuts build and maintenance cost on every path simultaneously - including every customer's hand-rolled pipeline. The checklist headlines:

- A checkpointable cursor the API guarantees stable across syncs - the property that makes incremental sync possible at all.
- A bulk/backfill endpoint separate from UI-grade CRUD pagination, so first sync doesn't burn the rate limit.
- An explicit delete/change signal - the most common gap; most application APIs return no deletes, so connectors silently miss them.
- Programmatic rate-limit signaling (429 with `Retry-After`).
- Additive versioning with published deprecation/sunset dates. An empirical study of 1,068 API specifications found 87.3% of breaking-change versions shipped with no deprecation notice at all (ICSME 2020) - every unannounced break becomes connector maintenance someone pays for. The source API's own change discipline is `samber/developer-platform-skills@api-versioning-policy` territory; hold it to that skill's notice-window standard.

## 5. CDC honesty scoping

- Never promise "CDC support" as if it were log-based CDC. The boundary is structural, not a maturity gap: log-based CDC reads the internal transaction log of the database being extracted, and no external platform - and no public API - gets that for a multi-tenant SaaS. The platforms' own SaaS-source "CDC" is timestamp-cursor polling under an explicit eventual-consistency model: pseudo-CDC.
- What a SaaS source can honestly ship, in order of completeness:
  1. Timestamp/cursor incremental polling - the practical default.
  2. Webhooks as a freshness supplement, never a backfill substitute - they capture nothing before the connection date.
  3. A vendor-side change/deletion feed - the real upgrade: implement internal CDC yourself and republish it as a stable, versioned API contract.
  4. Periodic full re-import as a reconciliation backstop for what polling structurally misses.
- Write customer-facing language as "incremental sync" with an eventual-consistency framing: state the poll interval and name what it misses - intra-interval overwrites, and hard deletes wherever no deletion feed exists. Ship the deletion feed when customers report missed deletes, not as a launch-day promise.
- Details, the platforms' own wording, and the substitute ladder live in [references/extraction-readiness-and-cdc.md](references/extraction-readiness-and-cdc.md).

## 6. Certification path

- Listing and certification are different bars everywhere:
  - **Listing** - passing the platform's test suite gets a connector listed.
  - **Certification** - optional, earned, and framed around reliability over feature count: "one solid connector is better than two finicky ones." Target it only after the connector holds up in real syncs.
- The certification-grade behaviors to build in from day one regardless:
  - Every supported sync mode integration-tested.
  - Incremental sync wherever the source allows it.
  - Failures that are fast and actionable - never a configuration the platform accepts but that is guaranteed to break.
- Enter a program with its clocks understood: platforms impose release-phase deadlines (e.g. a mandatory promotion window from private preview to beta) that turn a listing into a schedule commitment.
- Certification is paid for in engineering time, not fees: no platform charges a source vendor for the badge - and none pays for it either.
- Where a platform publishes quantitative bars (≥95% sync success, first-response SLAs, update cadence), adopt them as the connector's own SLOs even when the tier doesn't formally require them - they feed step 7's plan. Per-platform bars are in [references/platform-program-tables.md](references/platform-program-tables.md).

## 7. Maintenance plan

- Budget annual upkeep at 15-30% of the original build cost, reaching 50% in mature, high-change phases - vendor-published estimates, so treat them as an order of magnitude, not a quote. Each additional connector adds an independent recurring obligation; nothing amortizes across them.
- Plan against the four documented cost drivers:
  - Authentication changes.
  - Schema drift.
  - Rate-limit shifts.
  - Pricing/compliance overhead.
- Name the owner (interview answer 4) before launch. "A benevolent side-task" is the documented decay path - it is exactly how open-spec tap ecosystems rot (see Failure modes).
- Monitor breakage actively: alert on sync failures and schema-drift errors rather than waiting for customer tickets, because upstream APIs won't warn you (the 87.3% figure from step 4) and marketplace-tier listings carry no platform SLA.
- Justify the spend with support-deflection and retention math, never a revenue line. The documented payoff ranking: support-ticket deflection and retention > competitive-parity distribution > partner co-marketing programs > revenue share - the last essentially does not exist; do not plan around it (see [references/maintenance-and-revenue-economics.md](references/maintenance-and-revenue-economics.md)).

## Deliverable and validation

The output is a connector strategy document covering:

- Demand evidence.
- Platform and build-path decision, with the re-ranked menu shown.
- Extraction-readiness findings and their fix sequence.
- The CDC scoping language customers will see.
- The certification target and its clocks.
- The maintenance budget with a named owner.

Present it section by section and validate each with the user before writing the next. Gate the final document on explicit approval.

If your harness has persistent memory, store the chosen platform and path, the demand evidence, and the interview's re-ranking answers, so later tactical runs (building the connector, writing the listing) start from the decision instead of re-interviewing.

## Failure modes

- **A revenue-share line in the business case.** No platform pays source vendors; the one announced revenue-share model shipped as flat $10-150 per-task bounties. A plan that books connector income will be killed at its first finance review - rewrite the case on deflection and retention.
- **Overpromised CDC.** A "CDC support" checkbox implying log-based completeness fails customer data audits the first time a hard delete goes missing. Scope it as step 5 does, in writing, before marketing touches it.
- **Unmaintained-tap decay.** The open-spec ecosystem's history is the case study: taps of unknowable quality, multiple breaking upstream changes a year, maintainers gone once sponsor attention moved - an open standard solved initial coverage, never ongoing maintenance. Any custom-path plan without a month-13 owner is this failure scheduled in advance.
- **Extraction-hostile API under the connector.** A connector built on UI-grade CRUD pagination produces rate-limited backfills, missed deletes, and flaky incremental syncs - then fails the certification bar for reasons no connector code can fix. Step 4 runs before the build, not after the first support escalation.
- **Building on hypothesis.** A connector shipped without step 1 evidence serves nobody measurable and still bills its 15-30% every year.
- **Mistaking a listing for platform support.** Marketplace-tier connectors are explicitly outside platform support SLAs and may break without notice; only the certified/managed tiers carry the platform's commitment. Know which tier the chosen path lands in.

## Measurement

Gates - iterate the strategy until all pass:

- Demand gate: zero build approvals without named demand evidence attached to the decision; each claimed driver cites at least one verifiable artifact (ticket, lost-deal note, log analysis). Binary.
- Honesty gates: the business case contains no revenue-share income line, and no customer-facing claim says "CDC" without the incremental/eventual-consistency scoping. Binary, checked on the final document.
- Readiness gate: every resource in connector scope passes the extraction-readiness checklist or carries an explicit exclusion note - 100% coverage, no silent skips.

These gates are self-set from the documented record above, not an industry standard.

Trends to watch after launch, baselined from the first quarter:

- Connector-attributed support-ticket deflection.
- Sync success rate against the published ≥95% certification bar.
- The share of new customers connecting through the platform versus the raw API.

## Invocation examples

- "Customers keep asking when we'll be in their ETL platform's catalog - do we build the connector ourselves on the SDK or go through the platform's request program?"
- "Product wants 'CDC support' on our data-sync page - what can we honestly ship as an API-only SaaS, and how do we word it?"
- "Draft the business case for our source-connector investment - what pays for it if there's no revenue share?"

## References

- [references/platform-program-tables.md](references/platform-program-tables.md) - named platform programs, build paths, review gates, release-phase clocks, and support-tier taxonomies (dated snapshot).
- [references/maintenance-and-revenue-economics.md](references/maintenance-and-revenue-economics.md) - build-cost baselines, the maintenance-tax figures and drivers, who absorbs the tax per path, and the revenue-share/co-marketing reality.
- [references/extraction-readiness-and-cdc.md](references/extraction-readiness-and-cdc.md) - the full extraction-friendly API checklist and the honest-CDC substitute ladder with the platforms' own wording.

See also, same collection:

- `samber/developer-platform-skills@api-integration-surface-strategy` - the umbrella choice of which integration surfaces to offer at all; this skill runs after ETL-platform presence is chosen as a surface.
- `samber/developer-platform-skills@connector-marketplace-strategy` - the opposite direction: third parties building connectors into _your_ marketplace; this skill is you building into someone else's catalog.
- `samber/developer-platform-skills@bulk-data-sharing-design` - direct-to-storage file delivery when the demand is "data files in my lake", not "rows synced through my ELT tool".
- `samber/developer-platform-skills@sql-jdbc-access-design` - live SQL/JDBC query endpoints when the demand is interactive querying, not pipeline sync.
- `samber/developer-platform-skills@api-versioning-policy` - the versioning and sunset discipline step 4 demands of the source API.
- `samber/developer-platform-skills@webhook-platform-design` - the webhook surface step 5 uses as a freshness supplement, and the webhook-vs-polling extraction trade-offs.
