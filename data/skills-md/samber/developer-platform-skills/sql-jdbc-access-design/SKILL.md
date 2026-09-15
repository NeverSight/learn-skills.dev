---
name: sql-jdbc-access-design
description: Design customer-facing SQL access to a product's data - a JDBC/ODBC endpoint, warehouse share, or hosted query surface. Covers the architecture gate by scan frequency (zero-copy share, replicated copy, per-tenant compute isolation), engine-level tenant isolation with secure views and row-level security, an additive-only schema-stability contract enforced in CI, BI-tool connectivity and driver certification, query governance and cost caps, short-lived credential issuance, and the pricing shape. Use whenever the user mentions JDBC, ODBC, SQL access for customers, connecting Tableau or Power BI to product data, or pricing a SQL add-on - even if they never say "SQL access". Do NOT use for bulk file delivery - use samber/developer-platform-skills@bulk-data-sharing-design instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# SQL / JDBC Access Design

You are a data-platform product designer. Design how a SaaS product exposes its own hosted data to its customers through live SQL - a warehouse share, a read endpoint, or a JDBC/ODBC handle a BI tool connects to - so the surface is isolated, stable, governed, and priced before the first customer connects.

The stakes are asymmetric: an API bug returns a wrong response, but an isolation bug on a live SQL handle returns another customer's rows, and a runaway customer query lands on your infrastructure bill.

The demand side, in a16z's framing: applications are increasingly rebuilt warehouse-native, so governed SQL access is becoming a product category, not a niche feature - analyst positioning for the "why now", not evidence for any implementation choice below.

## Clarifying questions

Ask these before designing anything; each answer changes a later step. Batch them - this is a tactical design task, not a strategy interview.

1. Which problem is this actually? These get conflated under "data sharing", but only one is this skill's full scope:
   - (a) sharing data with partner _organizations_ - reuses the sharing mechanics here.
   - (b) isolating compute per tenant _inside_ your own product's analytics - an internal architecture concern that this skill's isolation menu touches but pricing and BI sections don't.
   - (c) giving _your customers_ a queryable SQL endpoint to their own data - this skill's full scope.
2. Where does the data live today: a cloud warehouse (Snowflake, Databricks, BigQuery), an OLTP database, a self-managed OLAP cluster? (decides which architecture rungs are nearly free)
3. Scan-frequency evidence: will a typical customer run ad-hoc queries a few times a week, or park a dashboard on it that re-scans many times a day? How large are the tables scanned? (this gates the architecture - see step 2)
4. Tenancy: how many customer accounts, what size spread, and is the store pooled or already siloed per tenant?
5. Which SQL consumers do customers actually demand: Tableau/Power BI/Looker, `psql` and notebooks, or an embedded app or agent issuing queries? (drives the BI-connectivity budget)
6. Schema exposure: raw operational tables, or a curated mart layer? (raw exposure makes every internal refactor a customer-breaking change - see step 4)
7. Pricing intent: free feature, gated to a higher tier, or a metered add-on - and who should pay the query compute? (see step 8; also ask the standard re-ranking trio - ship date, one-off vs compounding, effort ceiling)

If your harness has persistent memory, store the design's settled decisions (architecture rung with its promotion condition, isolation mechanism and identity function, schema-stability contract and what counts as breaking, credential ladder position, governance caps, pricing shape) so later runs - a new consumer type, a schema change, a repricing - start from the design instead of re-deriving it.

## Consumer type and scan frequency

Two splits do the work:

- **Consumer type:**
  - A _BI analyst_ behind Tableau or Power BI needs a certified driver, stable column names, and predictable types - they never see your docs, only their tool's connection dialog.
  - A _data engineer_ with `psql`, dbt, or a notebook tolerates rough edges but pushes the largest queries.
  - An _embedded app or agent_ issues high-frequency machine-generated queries that no human reviews - the strongest case for hard cost caps, since nobody notices a pathological query pattern until the bill.
- **Scan frequency.** The same table read twice a week and the same table under a forty-viewer morning dashboard want different architectures (step 2). Frequency, not company size, is the economic variable.

Design for the most demanding consumer type present, and gate the architecture on measured or honestly-estimated scan frequency - never on the org chart of who bought the product.

## Workflow

1. Confirm the problem and inventory the consumers.
2. Gate the architecture on scan economics.
3. Enforce tenant isolation in the engine.
4. Publish a schema-stability contract.
5. Design BI connectivity and driver distribution.
6. Configure query governance and cost caps.
7. Issue credentials.
8. Choose the pricing shape.

Each step has a section below, in order. Steps 3 and 6 must both pass their gates before any customer gets a handle; everything else can stage.

## 1. Confirm the problem and inventory the consumers

- Settle question 1 explicitly and write the answer down. "Data sharing", "multi-tenant isolation", and "customer SQL access" name overlapping but distinct architectures, and a design that answers the wrong one ships the wrong isolation primitive.
- List the concrete consumers (question 5) with their expected query shape: dashboard refresh, ad-hoc exploration, scheduled extract, agent traffic. This list is the input to every ranked menu below.
- State the boundary for the reader: this surface serves _live queries_. If the consumer actually wants periodic files or their own warehouse fed, hand off to the bulk-delivery sibling skill (see References) before designing anything here.

## 2. Gate the architecture on scan economics

Three architectures, ranked. Scan frequency and where the data already lives decide which one wins - not taste.

- efficiency: `zero-copy share > replicated copy or read endpoint > per-tenant compute isolation`
- effort: `per-tenant compute isolation > replicated copy or read endpoint > zero-copy share`
- value: `per-tenant compute isolation > zero-copy share > replicated copy or read endpoint`

- **Default rung: zero-copy warehouse sharing** - when the data already lives in a shared cloud warehouse and customers scan infrequently. The share is a metadata grant, not a copy: lowest build cost, always-fresh data, governance stays centralized at the source. The cost model is the catch: live access is paid per query scan (plus cross-region egress), so the economics hold only while scans stay infrequent.
- **Step to a replicated copy or dedicated read endpoint** when scan frequency inverts the arithmetic.
  - One lakehouse practitioner's heuristic (Alex Merced - treat it as one practitioner's rule of thumb, not a benchmark): a copy is paid once per refresh, live access once per query.
  - At roughly 20 scans/day on a ~200 GB table, the egress of live re-scanning costs more per month than a replicated copy costs per year.
  - A dashboard forty people load every morning is past this line. Two analysts querying twice a day are not.
  - The price of this rung: staleness to the last refresh, and a second copy of the data (including its PII) to govern.
  - Never point the replica at the live operational schema directly - see step 4.
- **Promote to per-tenant compute isolation** - each tenant gets its own query engine (a per-tenant instance over shared storage, fronted by one endpoint). This is the starved option:
  - Highest value: noisy neighbors eliminated by construction, a runaway query's blast radius capped at one tenant, clean per-tenant cost attribution.
  - Highest effort: an engine fleet to build and operate, so it loses every efficiency round.
  - Two conditions promote it anyway: arbitrary customer-authored SQL at dashboard-or-agent frequency across many tenants, or a shared cluster whose worst-case query already threatens the product itself.
  - PostHog hit both, judged unbounded customer queries against its shared cluster "basically untenable", and rebuilt on per-organization engines behind a Postgres wire-protocol endpoint (see [references/vendor-case-studies.md](references/vendor-case-studies.md)).

This ranking is a default, not a law. Re-rank against the interview:

- Already on Snowflake/Databricks/BigQuery makes zero-copy nearly free (which is why it's the default at all).
- An OLTP-only stack with no warehouse deletes the zero-copy rung entirely rather than demoting it.
- A hard ship date promotes whichever rung your platform gives you today.
- Agent consumers or a compounding-asset mandate promote the isolation rung despite its effort.

## 3. Enforce tenant isolation in the engine

Isolation must live in the query engine, never in application code. An app-layer `WHERE tenant_id = ?` filter is a named failure class for this surface: with an external SQL handle there is no application layer left to intercept the query, so one missed filter - ever, anywhere - leaks another customer's rows. Engine-level policies make a query that omits the filter return nothing instead.

- On a warehouse share, expose only secure/dynamic views that join a private base table to a private entitlement table filtered on the _caller's identity as the engine sees it_ - Snowflake's `current_account()`, Databricks Delta Sharing's `current_recipient()`. The base and mapping tables never enter the share.
- **The NULL-context trap**: `CURRENT_ROLE()` and `CURRENT_USER()` return `NULL` inside a secure view once it crosses an account-to-account share. A policy written against them silently matches nothing - or worse, everything, depending on the predicate's shape. Only the share-aware identity functions are safe across a share boundary.
- Treat recipient-property _partition filtering_ as a performance optimization, never as access control - Delta Sharing documents it as best-effort. Hard isolation comes from the dynamic-view predicate alone.
- On Postgres-family engines, use row-level security with `FORCE ROW LEVEL SECURITY`, and inject tenant identity into the session context server-side from a verified token - never from client-supplied input. RLS has four well-documented failure modes (policy recursion, missing `WITH CHECK`, permissive-policy OR-composition, owner-privileged view bypass) plus performance rules; work through [references/rls-failure-mode-catalog.md](references/rls-failure-mode-catalog.md) before writing any policy.
- Verify isolation from the consumer's side, not the provider's: run probe queries as another tenant (a second test account, or the warehouse's simulated-consumer session mode) and require zero foreign rows. This is a gate (see Measurement), re-run on every policy change.

## 4. Publish a schema-stability contract

The moment a customer's dashboard queries your tables, your schema is an API: columns are fields, tables are endpoints, their dashboards are clients. The asymmetry versus API versioning is that schema changes often happen _accidentally_ - a source-system update, a readability rename - and propagate downstream with no deprecation header to warn anyone.

- Never expose the live operational schema. Serve a curated mart layer replicated from the system of record, so internal schema churn stops at the replication boundary instead of landing in customer dashboards.
- Adopt the additive-only rule: add columns and tables freely; never rename, retype, or drop in place. Evolve via expand/contract:
  1. Add the new column.
  2. Deprecate the old one in the docs.
  3. Migrate consumers.
  4. Remove only when nothing depends on it.

  Amplitude's event schema is a shipped existence proof: it only ever adds tables and columns as new event types arrive, staying backward-compatible by construction.

- Enforce the contract in CI, not by convention. A contract that only lives in a doc is a hope:
  - dbt model contracts (1.5+) fail the run on a breaking column change.
  - The open-source `datacontract` CLI validates a contract against a PR before merge.
- Write the contract in four parts, because a BI dashboard, a dbt job, and an embedded app each depend on a different subset:
  - Schema: columns, types, nullability.
  - Quality: completeness thresholds.
  - Freshness: refresh SLA.
  - Availability: uptime/latency.
- When a breaking change is genuinely unavoidable, it exits through deprecation machinery with notice periods - the versioning sibling skill governs that; this contract defines what counts as breaking.

## 5. Design BI connectivity and driver distribution

BI-tool support is a certification tax, not a one-time integration - budget it as ongoing engineering, and let question 5 decide how much of it you buy.

- The cheapest rung, when your engine allows it: speak an existing wire protocol. A Postgres wire-protocol endpoint gets every BI tool, `psql`, and every ORM for free, because they all ship a Postgres driver - this is exactly why PostHog fronted its per-tenant engines with one. It costs you dialect fidelity: you support the Postgres dialect and nothing exotic.
- A custom dialect is the anti-pattern this rung exists to avoid: PostHog names its own HogQL as a reason direct exposure was a non-starter - "not a language that's already widely supported" means every BI tool integration starts from zero.
- Shipping your own driver means:
  - A spec-compliant Type-4 JDBC driver with _accurate_ SQLSTATEs (Tableau warns that a generic error instead of SQLSTATE 28000 for bad credentials breaks connector behavior).
  - Signed per-tool connector packages with certificates that expire and must be renewed.
  - Per-tool certification programs whose policies route first-line connectivity support back to you, not to the BI vendor.

  Details and the certification requirements per tool: [references/bi-connectivity-and-credentials.md](references/bi-connectivity-and-credentials.md).

- Publish a connection-setup page per supported client. An undocumented connection string is a support ticket per customer:
  - URL template.
  - Driver class or download.
  - TLS requirement stated explicitly rather than left to client defaults.
  - Auth method.

## 6. Configure query governance and cost caps

None of the warehouse cost controls are on by default; every one must be configured before GA, per external warehouse or engine. This differs from API rate limiting in enforcement primitive: you are capping compute seconds and spend on a long-running engine, not counting requests at a gateway. Design it here, and keep request-style limits (connection counts, queries/minute at the endpoint) consistent with the API sibling skill's policy.

- Per-query circuit breaker: a statement timeout so one runaway query dies instead of running all night, plus a queued-statement timeout so queries don't wait indefinitely for a slot.
- Concurrency cap per tenant or workload, so one customer's parallel dashboard refresh can't occupy a shared engine.
- A spend cap distinct from the timeout: a resource monitor (or your engine's equivalent budget alarm) that suspends the warehouse when its credit budget is hit. The timeout bounds one query; the monitor bounds the month.
- **The reader-account trap**: when you provision consumer accounts whose compute bills to _you_ (Snowflake reader accounts, or any provider-pays posture from step 8), their warehouses can consume unlimited credits charged to your account by default. A resource monitor on every such account is the single most important cost-control step of this surface, not optional hardening.
- The escalation signal: a tenant that regularly queues others or trips monitors moves to isolated or larger compute; never raise the shared cap for everyone to accommodate one tenant.

## 7. Issue credentials

The industry is retiring static database passwords - Snowflake enforces this through a staged deprecation schedule that moves all service users onto key-pair, OAuth, PAT, or workload identity - so design credential issuance on that trajectory rather than grandfathering passwords in.

Preference order: short-lived token > managed secret > static password; inline credentials in a connection string are the anti-pattern no documented path should show.

- Service accounts and automation: key-pair auth signing short-lived JWTs, so no password ever crosses the network; mark machine identities as service-type to close the password fallback.
- BI tools: OAuth (authorization-code with PKCE for desktop tools) so the BI tool never stores a database password. Caveat: token-refresh support varies by client - a BI tool that can't hold a refreshable token degrades to a key-pair or PAT service account, so the ordering must degrade gracefully rather than assume OAuth everywhere.
- Scope every credential to the tenant's own data by construction (the entitlement mapping from step 3), enforce TLS as a stated requirement, and give customers self-service revocation. Key formats, rotation UX, and secret hygiene follow the credential sibling skill; specifics for this surface live in [references/bi-connectivity-and-credentials.md](references/bi-connectivity-and-credentials.md).

## 8. Choose the pricing shape

Package SQL access as a paid tier or add-on, never a free feature. The shipped precedents (Stripe Sigma, Heap Connect, Mixpanel Data Pipelines) show customers pay for exactly this capability, and a price is itself a governance control on a surface that is expensive to over-serve. Three shapes, ranked:

- efficiency: `flat add-on or tier gate > consumption / volume-tiered > provider-pays-compute passthrough`
- effort: `consumption / volume-tiered > provider-pays-compute passthrough > flat add-on or tier gate`
- value: `consumption / volume-tiered > provider-pays-compute passthrough > flat add-on or tier gate`

- **Default rung: the flat add-on or tier gate** (Heap Connect, Mixpanel's shape) - SQL access unlocks at a higher plan or as a fixed-price add-on. Near-zero billing engineering; the gate itself throttles casual abuse. Its risk is the unbounded heavy user whose compute costs exceed the flat price - acceptable only with step 6's caps in place.
- **Promote to consumption / volume-tiered** when your own cost exposure is consumption-based or customer data volumes span orders of magnitude. This is the starved option:
  - Highest value: revenue tracks cost, so no customer is quietly unprofitable.
  - Highest effort: metering, tier tables, overage logic, so it loses the efficiency round until one of those two conditions holds.
  - Meter on a business unit the buyer already understands (Stripe Sigma tiers on monthly charge volume with unmetered queries), never on warehouse credits a non-technical buyer can't predict.
  - Sigma also shows the metric is revisable: it changed its own pricing model after shipping.
- **Provider-pays-compute passthrough** is less a free choice than the posture that arrives with reader accounts and marketplace listings: you pay the compute, then invoice cost plus margin. Take it only with a resource monitor on every account (step 6) - and note the consumer-pays alternative exists at the same rung: HubSpot's Snowflake share bills compute to the customer's own account, gated to its top tier.

This ranking is a default, not a law - re-rank against question 7 and the interview trio:

- A compounding-asset mandate promotes the consumption rung early, since retrofitting a meter under a shipped flat price is a customer-facing repricing.
- A hard ship date holds the flat gate, which is the only rung that needs no billing engineering.

Pricing precedents with their point-in-time figures: [references/vendor-case-studies.md](references/vendor-case-studies.md) - verify current pricing before quoting any of them to a customer.

## Failure modes

Anti-pattern checklist - each is a direct audit finding:

- Tenant isolation implemented as an application-layer `WHERE` clause instead of engine policy.
- A shared-view policy written against `CURRENT_ROLE()`/`CURRENT_USER()` (NULL across shares) instead of the share-aware identity functions.
- Partition filtering trusted as access control.
- Customer SQL admitted onto the shared production cluster - the PostHog "untenable" scenario.
- The live operational schema exposed directly, so internal refactors break customer dashboards.
- A rename or retype shipped in place instead of expand/contract, with no CI contract to catch it.
- A reader account (or any provider-pays compute) with no resource monitor.
- A custom query dialect where a standard wire protocol was available.
- Schema-per-tenant chosen for isolation, collapsing under connection pooling and DDL migrations past a few hundred tenants.
- Isolation verified only from the provider's side, never probed as a consumer.
- RLS-specific traps (recursion, missing `WITH CHECK`, OR-composition, view bypass): the full catalog with fixes is in [references/rls-failure-mode-catalog.md](references/rls-failure-mode-catalog.md).

## Measurement

- Isolation gate: probe queries executed as another tenant (simulated-consumer session or a second test account) return zero foreign rows, across every shared view and policy - binary, before GA and after every policy or schema change.
- Schema gate: zero breaking changes reach the customer-facing schema past the CI contract check; a breaking change that ships is a gate failure even if no customer noticed.
- Cost gate: every external compute handle has a statement timeout, a concurrency cap, and a spend cap before the first customer connects - audited as a checklist, pass/fail per handle.
- Trends to baseline from the first month, not thresholds: connectivity support tickets per new connection, per-tenant query cost against price paid, freshness-SLA adherence. A customer-facing data surface carries a categorically higher reliability bar than an internal dashboard - a failure here is a support ticket and a churn risk, so trend regressions get triaged like product incidents.

Iterate until all three gates pass; they are gates, not aspirations. The trends steer pricing and architecture revisits afterwards.

## Invocation examples

- "Our customers keep asking to plug Tableau into their data in our product - design the SQL access surface, we're on Snowflake."
- "We want to sell direct SQL access as an Enterprise add-on. What architecture and pricing shape, given most customers would park dashboards on it?"
- "Review our plan to expose read replicas of our production Postgres to customers - what breaks?"

## References

- `samber/developer-platform-skills@etl-connector-strategy` - being a source connector on other people's ETL platforms; this skill is the customer querying you directly.
- `samber/developer-platform-skills@api-integration-surface-strategy` - the umbrella decision of whether SQL access should be offered at all, among the other integration surfaces.
- `samber/developer-platform-skills@api-auth-key-management` - key formats, rotation UX, and secret hygiene for API credentials; step 7 applies the same discipline to database handles.
- `samber/developer-platform-skills@api-versioning-policy` - deprecation machinery and notice periods; step 4's contract defines what counts as breaking for the schema, that skill governs how a breaking change is announced and retired.
- `samber/developer-platform-skills@api-rate-limit-policy` - request-counting limits at the API gateway; step 6 caps compute and spend on a query engine instead, and the two published policies must not contradict each other.
