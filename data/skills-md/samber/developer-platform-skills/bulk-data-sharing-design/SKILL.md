---
name: bulk-data-sharing-design
description: Design bulk file and lake export as a B2B product surface - the two-camp choice between Parquet file-drops on object storage and native warehouse/lake sharing (Snowflake shares, Delta Sharing, linked datasets), the partitioning and schema-evolution contract across batches, delivery cadence and freshness commitments (full dump vs incremental vs CDC vs streaming), shared-bucket security with per-recipient credentials, egress cost allocation, and cross-border data residency. Use whenever the user mentions bulk export, data dumps to S3, Parquet, Snowflake shares, Delta Sharing, or export freshness SLAs - even if they never say "bulk data sharing". Do NOT use for live SQL endpoints - use samber/developer-platform-skills@sql-jdbc-access-design instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Bulk Data Sharing Design

You are a data-platform product designer. Design how a SaaS product hands its customers their own data in bulk - as files on object storage, as a native warehouse or lake share, or as a stream - so a customer's data team can join it against the rest of their business without building a scraper against your API.

The motivating precedent: before Stripe shipped Data Pipeline, a customer wanting Stripe data in a warehouse either built a custom API pipeline (Stripe's own estimate: months of work, hundreds of thousands of dollars) or bought a third-party ETL sync with incomplete coverage. A vendor-run bulk surface is the third option - full coverage by construction, and every vendor studied sells it as a premium feature.

## Clarifying questions

Ask these before designing anything; each answer changes a later step. Batch them - this is a tactical design task, not a strategy interview.

1. Customer warehouse landscape: what share of target accounts already run a shareable warehouse or lakehouse (Snowflake, Databricks, BigQuery), and does one platform dominate? (picks the camp - see step 1)
2. What data, at what volume and volatility: append-only events, or mutable records with updates and deletes? (drives cadence and delete semantics)
3. Freshness demand, sourced from actual buying customers: is day-old data fine, or do they need hours or minutes? What did they say, not what sounds ambitious?
4. Compliance regimes and regions: EU personal data in scope? Any customers in countries with data-localization mandates (e.g. China's PIPL, Russia, India)?
5. Pricing intent: enterprise-tier gate, usage-priced add-on, or bundled into an existing paid plan? If the plan is "free feature", flag it now - see Failure modes.
6. Recipient clouds: one of AWS/GCP/Azure, or a mix? (drives the credential and encryption mapping)
7. Delivery ceiling: by when must the first export land, is this a one-off enterprise deal-closer or a compounding platform surface, and how much data-engineering effort can you spend? (re-ranks both menus below - a hard deadline promotes the low-effort rungs, a compounding mandate promotes the table-format and CDC investments)

If your harness has persistent memory, store the design's settled decisions so later runs (a new dataset, a cadence upgrade, a residency review) start from the design instead of re-deriving it. Store:

- Chosen camp
- Partition and file-size contract
- Cadence rung, with its promotion condition
- Credential model
- Cost-allocation split
- Residency posture

## Data-stack maturity

The design splits by the customer's data-stack maturity:

- **Warehouse-resident consumers** - already live in Snowflake, Databricks, or BigQuery. A native share serves them with zero copies, zero egress, and no schema drift on load; handing them raw files forces them to rebuild ingestion you could have skipped.
- **Bucket-only consumers** - no shareable warehouse; they run Spark, Athena, DuckDB, or ML pipelines against object storage. Partitioned Parquet in a bucket is the only shape they can consume.

Design for the mix you actually have, not the sophisticated end. Stripe ships both camps side by side - warehouse shares for the first group, raw Parquet to S3/GCS/Azure Blob for the second - rather than picking one.

## Workflow

1. Choose the camp - file-drop, native share, or both.
2. Specify the file-layout and partitioning contract.
3. Set the delivery cadence and the freshness posture.
4. Design the security and credential model.
5. Allocate egress, storage, and compute cost.
6. Write the schema-evolution contract.
7. Settle compliance and residency.
8. Stage the rollout.

Each step has a section below, in order.

## 1. Choose the camp

Two architectural camps ship in production, plus one outlier:

- effort: `streaming push > Parquet file-drop > native warehouse/lake share`
- value: `native share > file-drop > streaming push` (for warehouse-resident consumers; flips to `file-drop > native share` when consumers are bucket-only)
- efficiency: `native share > file-drop > streaming push`

- **Default rung: native warehouse/lake sharing** - Snowflake Secure Data Sharing, Databricks Delta Sharing, BigQuery linked datasets - whenever a meaningful share of target accounts concentrate on one warehouse platform (roughly 30-40%+ on one platform; that threshold is self-set, not a vendor-published number). Nothing is copied, so there is no egress bill, no storage duplication, and no schema drift introduced by a load job. This is the camp Stripe, HubSpot, and Salesforce all chose for their warehouse-resident customers. The effort line above assumes the data already lives in a share-capable warehouse or lakehouse - if it doesn't, getting it there is the real cost, and that flips the effort ordering.
- **Universal fallback rung: Parquet file-drops on object storage** - Hive-partitioned Parquet in a bucket, the shape every consuming engine reads. The default when no warehouse concentration exists, and the second surface to ship even when one does, because it also serves ML backfills and raw-file use cases the share can't.
- **Deleted, not demoted: the native share when question 1 finds no warehouse-resident accounts at all.** A share needs a share-capable destination on the recipient's side; with none, this is not a slower rung but an unreachable one. Strike it rather than leaving it at the bottom, where "we'll add Snowflake sharing too" reappears as scope in every roadmap review. Re-promotion trigger: target accounts concentrating on one shareable platform.
- **Starved option: real-time streaming push** - highest freshness, highest effort, loses every efficiency round. Promote it only when the exported data is genuinely event-shaped, consumers demand sub-minute delivery, and they accept the durability trade-off: Braze Currents, the one real-world example (Avro, not Parquet), states plainly that events can't be replayed - a consumer whose endpoint was down recovers nothing from the provider.

This ranking is a default, not a law. Re-rank against question 1's answer and anything else you know about the user: a provider whose data already sits in Databricks gets Delta Sharing nearly free; a customer base of ML teams with no warehouse makes the file-drop the only rung that matters; an event-analytics product with streaming-native consumers is the one context that promotes the starved option.

Protocol-level detail - how Delta Sharing vends pre-signed URLs so the sharing server never proxies bytes, and how one tenant-partitioned table backs every recipient's share without per-tenant copies - lives in [references/vendor-case-studies.md](references/vendor-case-studies.md).

## 2. Specify the file-layout and partitioning contract

For the file-drop camp, the layout is the contract. Write it down; don't let the export job's incidental output become what customers depend on.

- Pick partition keys by what the consumer will filter on, never by how your internal schema is organized - date for event data, plus tenant scoping. Use Hive-style paths (`year=2026/month=08/day=30/`), capped at 2-3 levels of low-cardinality keys; never partition on a high-cardinality key like user ID.
- State target file and row-group sizes in the contract (roughly 256-512 MB files), and run compaction - the small-files problem is measured, not theoretical (an AWS benchmark cut a 40-second query to under 10 by compacting).
- Default to Parquet over CSV/JSON: AWS's own numbers show Parquet unloads up to 2x faster and up to 6x smaller than text.
- Register the schema in a catalog (Glue, Iceberg REST, Hive Metastore) rather than leaving consumers to infer it from files.
- Graduate from raw partitioned Parquet to a table format (Iceberg, Delta, Hudi) only when the export needs atomic multi-file commits, time-travel, or in-place schema evolution - not before; raw Parquet is cheaper to operate when those guarantees aren't needed.

Concrete numbers, the compaction trigger, and the format trade-offs live in [references/file-layout-and-access-control.md](references/file-layout-and-access-control.md).

## 3. Set the delivery cadence and the freshness posture

The cadence ladder - build complexity rises monotonically, operating cost at scale falls:

- effort to build: `streaming push > log-based CDC > micro-batch incremental > scheduled full-dump`
- operating cost at scale: `scheduled full-dump > micro-batch incremental > log-based CDC`
- freshness: `streaming push > log-based CDC > micro-batch incremental > scheduled full-dump`
- efficiency: `scheduled full-dump > micro-batch incremental > log-based CDC > streaming push`

- **Default rung: scheduled full-dump.** Idempotent overwrite, no delete-tracking, simplest to operate. Stripe's full load every 3 hours is the concrete reference cadence. The cost: every cycle re-transfers the whole dataset regardless of how little changed.
- **Promote up the ladder** when the full-dump's bandwidth/compute bill exceeds CDC's build cost, or a customer freshness requirement the dump interval can't meet. Adopting CDC commits the design to upsert-by-primary-key dedup, explicit delete tombstones, and a periodic full-scan reconciliation job - missed deletes are the named CDC gotcha, since a delete that never emits a change event is invisible downstream.
- Streaming push sits at the top with the non-replayability trade-off from step 1.

This order is a default too. Re-rank it against what the team already has: an in-house group that has run log-based CDC before (Debezium and its snapshot-to-log handoff) buys the CDC rung far cheaper than the ladder assumes, and that experience promotes it well before the cost curve would.

Separately from the rung, publish an explicit freshness posture - one of three, and say which:

1. **Fixed cadence** - Stripe: a full load every 3 hours, unconditional.
2. **Best-effort target** - Amplitude: "aims to export five million events per hour", explicitly variable under shared load.
3. **Contractual SLA** - Fivetran: 99.9% uptime, penalty-backed.

"Best-effort hourly" and "99.9% SLA" look similar on a pricing page and carry completely different support-escalation and legal consequences. A surface that never states which posture it makes has made the best-effort promise in the customer's mind and the no-promise position in its own.

## 4. Design the security and credential model

- Never proxy the bytes through your own servers. Every production sharing mechanism - Delta Sharing, Snowflake, BigQuery - vends short-lived signed URLs or scoped temporary credentials so the recipient reads object storage directly; your service does authorization and URL-signing, and throughput scales with the storage layer.
- Issue per-recipient credentials, never shared or static keys: cross-account roles with an external ID on AWS, SAS tokens on Azure, and one KMS grant per recipient so revoking one customer never touches another.
- Isolate recipients along the maturity ladder, moving up only as tenant count forces it: `dedicated bucket per tenant > shared bucket with prefix isolation > per-recipient access points > broker-minted short-term credentials`.
- Encrypt with customer-manageable keys (CMEK/SSE-KMS); rotation must not require re-encrypting historical data, and per-file encryption is the finer-grained option when one bucket serves recipients with different trust levels.
- Pin the access-review cadence to the credential TTL - expiration is the enforcement point, not per-request ACL checks.

Mechanics per cloud, the AWS isolation ladder, and the token-lifecycle details live in [references/file-layout-and-access-control.md](references/file-layout-and-access-control.md).

## 5. Allocate egress, storage, and compute cost

Three cost layers; name who pays each, in writing, before launch:

1. **Infrastructure cost allocation follows the camp.**
   - File-drop: the customer pays everything - their bucket, their reprocessing compute. Segment's model: customers own and pay AWS directly, down to the transform cluster Segment runs inside the customer's own account.
   - Warehouse share: nothing is copied, so nobody pays storage duplication, and the consumer pays only query compute. Snowflake's model; HubSpot tells customers outright they owe all Snowflake costs incurred reading the share.
2. **Egress is the decisive line item.** Cross-region and cross-cloud transfer can contribute up to 70% of total data-transfer cost (Snowflake's own published figure - a vendor number, and one that flatters the optimizer it sells); same-region is typically free.
   - Know which side of the share eats it: in cross-region native sharing the _provider_ can end up paying egress that scales with consumer query volume (a caveat raised by a competitor source - weight accordingly, but the economics are real).
   - Snowflake shipped an Egress Cost Optimizer (GA 2025-04-15) precisely because of this: replicate once, pay egress on increments only. The up-to-96% savings figure is a vendor claim, though one customer, RavenPack, reports a 14-fold cost reduction.
3. **What you charge is independent of who pays infrastructure.** Every vendor studied prices bulk export as an enterprise-tier or usage-priced add-on: there is no observed free-tier precedent for this feature class.
   - Stripe bills a subscription keyed to transaction count.
   - Braze gates behind an enterprise contract.
   - HubSpot gates behind its top tier.

## 6. Write the schema-evolution contract

The export's schema is an API contract whose breaking changes ship silently - a source-system rename propagates into the customer's dashboards with no deprecation header. Treat it with API-versioning discipline:

- Add-only posture: append new nullable columns at the end; never rename, remove, or retype in place. Renames break Parquet consumers outright (column names are the identifiers); the correct move is add-new-plus-deprecate-old.
- Keep column ordering and types consistent across every batch - engines' predicate pushdown and by-name column matching both depend on it.
- Register every schema version in the catalog and validate the written schema against the documented contract before a delivery counts as successful, so drift raises an alert instead of a customer ticket.
- Frame the full commitment as a four-part data contract, because a BI dashboard, an ML pipeline, and a dbt job each depend on a different subset:
  - Schema: columns, types, nullability.
  - Quality: completeness thresholds.
  - Freshness: the step-3 posture.
  - Availability.
- When a breaking change is genuinely unavoidable, run it like an API deprecation: announced window, parallel old-and-new columns or paths, dated removal. Sibling `samber/developer-platform-skills@api-versioning-policy` owns that notice-period machinery; this contract defines what counts as breaking for files and tables.

## 7. Settle compliance and residency

Cross-border transfer of personal data has teeth: Schrems II added a mandatory Transfer Impact Assessment on top of Standard Contractual Clauses, and Meta's €1.2B fine (2023) was specifically for cross-border transfer failures. Remote access counts as a transfer - a support engineer in a non-EEA office querying an EEA customer's export is the same regulated event as a file copy.

Prefer the architectural fix over the paperwork path, in this order:

1. **Region-pin from day one** - EU data in EU buckets/shares eliminates the transfer question at the source. Segment deprecated its EU Data Lakes product rather than retrofit compliance onto a US-region design; region selection is a day-one setting in every major platform for this reason, and retrofitting it is what the Segment case says it is: sometimes cheaper to kill the product.
2. **Regionalized CMEK** - a key that never leaves the region closes the "ciphertext moved, but it's unreadable" loophole regulators don't accept.
3. **Pseudonymized replicas** - strip or tokenize identifying fields before any copy leaves its home region.
4. **Localization mandates are hard blockers, not paperwork** - China's PIPL and similar laws can forbid the transfer outright; Stripe simply does not offer Data Pipeline in India, citing data localization. "Not offered in region X" is a legitimate, precedented design outcome.

Full legal-mechanism ordering (adequacy → SCC/BCR + TIA → derogations) and the pattern details live in [references/compliance-and-residency.md](references/compliance-and-residency.md).

## 8. Stage the rollout

Deliver the design as a staged plan, not a single launch (thresholds here are self-set, not vendor-published figures):

1. Native warehouse share for the dominant warehouse platform, if question 1 found concentration.
2. Parquet-on-object-storage file drop as the universal fallback - partitioned, cataloged, per-recipient credentials.
3. Cadence upgrades (incremental/CDC) only when full-dump cost or a customer freshness requirement forces them.
4. Premium gating and the published freshness posture - priced as an enterprise tier or add-on from day one.
5. Build vs partner: buy or partner for standard delivery paths (the warehouse's own sharing primitive, an established movement vendor); build in-house only for what no vendor covers. Fivetran itself - with a working prototype in hand - acquired Census (May 2025) rather than build reverse ETL internally, because read-path and write-path data movement are different engineering problems. Revisit the choice when a vendor's usage pricing crosses the fully-loaded cost of roughly 1-2 data engineers.

Region pinning (step 7) is cross-cutting: bake it into stages 1-2, never bolt it on at stage 4.

## Failure modes

Anti-pattern checklist - each is a direct review finding:

- **Silent schema drift**: a rename or type change ships to the export because nothing validates batches against a documented contract. The costliest failure in this domain - the break lands in the customer's dashboards, not your logs.
- **Egress bill shock**: cross-region sharing launched without knowing which party pays per-byte egress, discovered on the first invoice at 70%-of-transfer-cost scale.
- **Cross-border violation**: one global bucket for engineering simplicity, which silently commits you to SCC/TIA paperwork for every EU customer - or to a Meta-scale finding.
- **Free-tier giveaway**: bulk export bundled free, against a feature class where every vendor studied gates it behind a premium tier - margin surrendered that tier repricing can't easily claw back.
- **Proxied bytes**: export downloads routed through your API servers, making your fleet the throughput ceiling and the egress payer at once.
- **Small-files decay**: no compaction, thousands of tiny files, consumer queries slow to a crawl - the measured 4x penalty.
- **CDC without delete reconciliation**: deletes that never emit events accumulate as phantom rows in every customer's copy.
- **Static shared credentials**: one key for all recipients, so a single leak or offboarding rotates everyone.
- **Streaming without the replay warning**: consumers discover during their first outage that missed events are gone; if you ship a non-replayable stream, the contract must say so as loudly as Braze does.

## Measurement

Four binary gates; iterate the design until all four pass:

1. **Contract completeness**: every export surface has a written data contract covering schema (columns, types, nullability) and an explicit freshness posture (fixed cadence, best-effort, or SLA - named as such). A surface with an implicit schema or an unstated posture fails.
2. **Cost allocation named**: for each shipped delivery model, who pays storage, compute, and egress is written down, including the cross-region case. Any unattributed egress path fails.
3. **Residency coverage**: every regulated region present in the customer base has a documented posture - region-pinned, legal-mechanism-documented, or explicitly not offered. An EU customer on an unpinned global bucket with no documented SCC/TIA fails.
4. **Premium gating**: bulk export sits behind a paid tier or add-on, or the design records an explicit, argued decision to break the industry-wide precedent.

Trends to watch after launch, never pass thresholds:

- Share of deliveries meeting the stated freshness posture.
- Consumer-reported schema-break incidents (target direction: zero).
- Egress cost per recipient per month.

## Invocation examples

- "Our enterprise customers keep asking to get their data into Snowflake - design a bulk export surface, and tell me whether to build file drops or a native share."
- "Design the Parquet layout and schema-evolution rules for our S3 data export so customer dashboards stop breaking when we change columns."
- "We want to sell a data export add-on: what cadence can we promise, who pays the egress, and what do we do about our EU customers?"

## References

- [references/vendor-case-studies.md](references/vendor-case-studies.md) - the vendor comparison table (Stripe, Segment, Amplitude, Braze, HubSpot, Fivetran) and the sharing-platform landscape (Snowflake, Delta Sharing, BigQuery, Iceberg REST Catalog, Salesforce Zero Copy, AWS Data Exchange), with Delta Sharing protocol mechanics and the build-vs-partner evidence.
- [references/file-layout-and-access-control.md](references/file-layout-and-access-control.md) - partitioning and compaction numbers, table-format graduation triggers, the multi-tenant isolation ladder, and per-cloud credential/encryption mechanics.
- [references/compliance-and-residency.md](references/compliance-and-residency.md) - GDPR transfer mechanics, Schrems II/TIA, the architectural pattern ordering, and the localization-mandate cases.

See also, same collection:

- `samber/developer-platform-skills@api-integration-surface-strategy` - the umbrella decision that chooses bulk files/shares as a surface at all; this skill designs the surface once chosen.
- `samber/developer-platform-skills@etl-connector-strategy` - being a source connector on other people's ETL platforms (Fivetran, Airbyte); this skill is you delivering the data yourself.
- `samber/developer-platform-skills@api-auth-key-management` - API credential issuance and rotation; the per-recipient bucket credentials here (cross-account roles, KMS grants, short-lived tokens) apply the same lifecycle principles to storage access.
