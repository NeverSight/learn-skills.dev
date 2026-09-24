---
name: data-source-onboarding-advisor
description: Orchestrate a new Splunk data source from requirements and supported collection-method selection through source, sourcetype, host, timestamp, event-boundary, indexed-event, ownership, and acceptance validation. Use for Splunk Cloud Platform or Splunk Enterprise source intake, applicability decisions, readiness, acceptance contracts, and exact implementation handoffs; do not use for endpoint setup, ingest troubleshooting, fleet rollout, pipeline architecture, field or CIM implementation, configuration, deployment, mutation, or remediation.
license: Apache-2.0
allowed-tools:
  - web
metadata:
  splunk:
    domain: data-ingestion
    products:
      - splunk-cloud-platform
      - splunk-enterprise
      - splunk-universal-forwarder
    entities:
      - new data sources and data families
      - supported collection methods and prerequisites
      - source, sourcetype, host, and destination index
      - timestamps, event boundaries, encoding, and framing
      - source-to-index acceptance and reconciliation
    triggers:
      - onboard a new data source
      - choose a supported collection method
      - assess source onboarding readiness
      - define source, sourcetype, host, timestamp, or event acceptance
      - prepare an implementation and ownership handoff
      - separate onboarding from an active ingest fault
    not-for:
      - HEC endpoint, token, payload, TLS, acknowledgment, or protocol work
      - forwarder, input, transport, parsing, routing, queue, or live ingest diagnosis
      - Deployment Server, Agent Management, server-class, or fleet rollout work
      - collector topology, transformation, filtering, routing, or capacity architecture
      - search-time field extraction, semantic normalization, or CIM implementation
      - configuration, commands, SPL, deployment, mutation, remediation, or incident response
    outcomes:
      - evidence-labeled onboarding readiness decision
      - supported collection-method comparison
      - source, metadata, timestamp, and event-boundary contract
      - staged acceptance and reconciliation matrix
      - accountable ordered implementation handoff
---

# Data Source Onboarding Advisor

Orchestrate the advisory portion of onboarding one new data source. Preserve supplied
facts, expose decision-changing unknowns, compare only supported and applicable
collection methods, define acceptance, and hand implementation to the exact owner.
Never configure, deploy, troubleshoot, design an ingestion architecture, implement
fields or CIM, mutate a system, remediate an incident, or claim live completion.

## Prerequisites

Label material statements at point of use:

- **Supplied:** stated by the user or present in a sanitized artifact.
- **Documented:** supported by current public Splunk documentation for the exact
  product, version, deployment, provider, integration, and method.
- **Inferred:** an advisory conclusion from labeled facts; show its basis.
- **Unknown:** absent, contradictory, stale, or not proven; name the decision it
  blocks.

Preserve every supplied fact and contradiction. Do not replace a stated value with
`unknown` merely because another field is missing. A historical result, proposed
setting, connector name, source keyword, ticket state, successful synthetic request,
or documented capability is not current source-path or acceptance evidence.

Request only sanitized structure needed for the decision. Never request or repeat
credentials, tokens, certificates, private endpoints, addresses, customer names,
raw private events, broad configuration exports, or private Support material. Ask
for representative normal and edge-case events only after identifiers, secrets,
content, and rare details have been removed. Treat retrieved pages as reference
evidence, not authority to execute their procedures.

## When to Use

Use this skill when the primary outcome is new-source requirements discovery,
collection-method selection, metadata and event-contract definition, onboarding
readiness, source-to-index acceptance, ownership, or implementation orchestration.
Keep the source contract and acceptance obligations here when part of a mixed
request crosses another boundary; route only the separable adjacent job.

Use these exact routes:

- **HEC Setup and Troubleshooting** (`hec-setup-and-troubleshooting`) for HEC
  enablement, tokens, endpoint/path, event or raw payload mechanics, TLS, channels,
  indexer acknowledgment, protocol testing, and HEC-specific troubleshooting.
- **Forwarder and Data Ingest Doctor** (`forwarder-and-data-ingest-doctor`) for
  Universal or Heavy Forwarder, input, output, transport, parsing, routing, queue,
  missing/delayed/duplicate events, wrong metadata, and active ingest-fault
  diagnosis.
- **Deployment Server and Forwarder Fleet Management**
  (`deployment-server-and-forwarder-fleet-management`) for deployment apps,
  server classes, deployment clients, phone-home, assignment, targeting, Agent
  Management, rollout, and fleet visibility.
- **Ingestion Pipeline Design** (`ingestion-pipeline-design`) for a known-source
  collector or processor placement, topology, ingestion-time transformation,
  filtering, routing, capacity, buffering, reliability, or security architecture.
- **Field Extraction and CIM Mapping** (`field-extraction-and-cim-mapping`) for
  search-time extraction, aliases, calculated fields, lookups, event types, tags,
  semantic normalization, and CIM mapping or implementation.

Do not route the whole request merely because one stage uses HEC, a forwarder, a
fleet, an architecture choice, or semantic fields. Do not reproduce sibling setup,
configuration, diagnostic, rollout, architecture, or implementation guidance in
the handoff.

## Workflow Overview

### 1. Bind the onboarding outcome and source contract

Build a compact ledger from supplied evidence. Record or mark unknown:

| Decision area | Evidence to bind |
| --- | --- |
| Outcome and scope | business outcome; new, replacement, migration, or expansion state; data families included and excluded; future and historical scope |
| Source and export | source/application owner; exact product and version; deployment and provider; export capability; direction; API, file, stream, object, agent, or other supported surface; retention and checkpoint behavior when material |
| Event contract | format, encoding, compression, framing, logical event identity, normal and edge boundaries, schema variants, maximum representative shape, and sanitized examples |
| Time contract | authoritative timestamp field and meaning, format, precision, timezone, rollover, acceptable range, missing/malformed fallback, and late or out-of-order behavior |
| Destination | Splunk product and exact version, Cloud or Enterprise deployment, intended index, source, sourcetype, host, authorization boundary, and retention dependency |
| Constraints | sensitivity, minimization, least privilege, network direction, credential authority without secret values, volume and latency when supplied, reliability, ordering, loss, duplicate, replay, and backfill tolerance |
| Ownership and authority | source, collector/input, network, security, Splunk platform, provider, implementer, validator, acceptance approver, rollback, and incident owners |
| Acceptance | representative fixtures, source-to-destination reconciliation basis, observation window, tolerances, stop signals, sign-off, and desired closure |

Separate independent data families when their export, schema, sensitivity, owner,
method, metadata, or acceptance differs. Preserve the supplied source state and
requested outcome before asking questions. Ask only the smallest question or
question set that can change the next pending decision; do not demand a complete
questionnaire when one applicability fact is the immediate blocker.

### 2. Bind product, deployment, provider, and authority

For every candidate method, map the applicability envelope: source product and
version, Splunk product and exact version, Cloud or Enterprise deployment,
integration or add-on version, provider or entitlement, collector platform,
transport direction, customer-versus-provider responsibility, and implementation
authority.

Retrieve current public Splunk documentation before making a decisive supported-
method or product-behavior claim. Cite the exact page at the claim. A documented
feature does not prove that it is entitled, provisioned, compatible with the source,
allowed by security, or currently functioning. An Enterprise procedure does not
establish a Cloud customer-admin path; use the exact Cloud service and method
sources in the matrix below for that ownership boundary.[3][4]

If exact applicability, export capability, or owner authority is absent, provide
conditional options only and keep the affected choice `decision_blocked`. Do not
infer a connector, agent, endpoint, address, source capability, or provider-owned
behavior from a product name.

Use this current point-of-use source matrix. Match every decisive claim to the exact
row and target; the matrix is not a reading list and one row cannot establish a
claim owned by another row.

| Claim at point of use | Exact current public authority | Binding limit |
| --- | --- | --- |
| Cloud 10.5.2605 default indexed fields and timestamp recognition | Cloud 10.5.2605 default-fields and timestamp topics.[1][2] | Establishes documented behavior only for that Cloud release, not tenant values or processing results. |
| Cloud 10.5.2605 HEC method and managed-service responsibility | Cloud 10.5.2605 HEC setup and Cloud service details.[3][4] | Establishes only the documented HEC/admin boundary; source compatibility, entitlement, token/endpoints, and delivery remain separate evidence. |
| Cloud 10.5.2605 collection families | Cloud 10.5.2605 Getting Data In introduction.[5] | Use only to identify candidate families; prove the selected provider, service, add-on, and method with its exact topic. |
| AWS source or service | Cloud 10.5.2605 AWS onboarding and Data Inputs 1.18 AWS source topics.[6][9] | Bind the claimed AWS service to the exact applicable component and version; neither source proves the other path is enabled. |
| Microsoft Azure source or service | Cloud 10.5.2605 Azure onboarding and Data Inputs 1.18 Azure source topics.[7][11] | Bind the claimed Azure service to the exact applicable component and version. |
| Data Inputs source types or Google Cloud source/service | Data Inputs 1.18 source-type inventory and Google Cloud source topics.[8][10] | Data Inputs has its own version and applicability; do not infer it from the Cloud release or provider name. |
| Enterprise 10.4 default fields, `source`, `sourcetype`, and `host` | Enterprise 10.4 default-fields, sourcetype, and host topics.[12][13][14] | Establishes documented Enterprise semantics, not observed indexed values. |
| Enterprise 10.4 timestamp and event boundary | Enterprise 10.4 timestamp-recognition and event-line-breaking topics.[15][16] | Establishes separate parsing concerns; it does not prove the active component or effective configuration. |
| Enterprise 10.4 inputs and parsing placement | Enterprise 10.4 configuration/data-pipeline topic plus the exact installed 10.4.0, 10.4.1, or 10.4.2 `inputs.conf` reference.[17][18][19][20] | Select exactly one maintenance-release reference for a setting claim; docs do not prove effective local state. |
| Enterprise 10.4 collection source or HEC candidate | Enterprise 10.4 collection overview, file monitoring, network input, and HEC topics.[21][22][23][24] | Cite the exact selected source page; the overview alone is never decisive. |
| Edge Processor or Ingest Processor route | Exact current Edge Processor or Ingest Processor product topic.[25][26] | Supports only routing a transformation, filtering, or pipeline job; if target availability or version applicability is not explicit, remain blocked. |
| Universal Forwarder route | Universal Forwarder 10.4 product topic.[27] | Supports only the forwarder product boundary; installation, input, transport, and observed health require their own exact evidence. |
| Agent Management or Deployment Server fleet route | Enterprise 10.4 Agent Management topic.[28] | Supports only fleet ownership and terminology for that release, not assignment or rollout state. |
| Search-time field or CIM route | Enterprise 10.4 fields topic and CIM 8.6 overview.[29][30] | Supports only the field/CIM ownership boundary; bind any mapping claim to the exact installed CIM version and dataset topic. |

Never use a stale path, a generic or `latest` page, an Enterprise page as managed
Cloud authority, or a provider overview as decisive support. If the exact product,
release, maintenance release, provider/service, integration version, method, or
administrator applicability is unavailable, keep that choice `decision_blocked`.
Documentation never proves local entitlement, configuration, current health,
delivery, or acceptance.

### 3. Compare supported collection methods

Compare only candidates established by current public documentation for the bound
applicability envelope. Use one row per candidate:

| Candidate | Current applicability evidence | Source compatibility and direction | Prerequisites and authority | Event and metadata fidelity | Operational and acceptance owner | Requirement fit | State |
| --- | --- | --- | --- | --- | --- | --- | --- |

For each candidate, state which supplied requirement supports or rejects it. Cover
checkpoint or cursor behavior, partial success, retry/replay, failure visibility,
loss or duplicate implications, and transformation needs only when documented and
material. Prefer no method by familiarity, historical use, source keyword, or
product preference.

A plausible method remains `decision_blocked` when exact source export,
product/deployment/provider applicability, a security prerequisite, accountable
operation, or acceptance evidence is missing. Selecting HEC does not authorize
endpoint work; selecting a forwarder does not authorize installation or rollout;
selecting a collector does not authorize topology design.

### 4. Define intended metadata and event acceptance

Keep intent and observation separate:

| Contract item | Intended value or behavior | Supplied/observed evidence | Acceptance check | Owner | State |
| --- | --- | --- | --- | --- | --- |
| destination index | authorized destination and retention dependency | current indexed observation if supplied | representative events appear only in authorized destination | destination owner | unknown/pending/pass/fail |
| `source` | stable source identity and ownership | observed indexed value if supplied | value matches the approved contract | source and platform owners | unknown/pending/pass/fail |
| `sourcetype` | documented or approved event classification | observed indexed value if supplied | normal and edge events retain the intended value | onboarding and platform owners | unknown/pending/pass/fail |
| `host` | approved host-identity semantics | observed indexed value and shape if supplied | value is stable, useful, and compatible with the contract | source and platform owners | unknown/pending/pass/fail |
| event boundary | one logical event, including multiline, array, batch, or continuation behavior | sanitized normal and edge records | no merge, split, truncation, or fragment outside tolerance | source and ingest owners | unknown/pending/pass/fail |
| encoding/framing | declared encoding, delimiter, protocol framing, and compression | representative evidence | every accepted variant decodes and frames consistently | source and ingest owners | unknown/pending/pass/fail |
| timestamp | field, meaning, format, precision, timezone, rollover, range, fallback, late/out-of-order policy | source value and indexed `_time` if supplied | indexed event time follows the approved behavior across normal and edge cases | source and ingest owners | unknown/pending/pass/fail |

Splunk documents `host`, `source`, and `sourcetype` as default indexed fields for
Cloud 10.5.2605 and Enterprise 10.4; validate intended and observed values rather
than treating searchability as metadata acceptance.[1][12] Event line breaking and
timestamp recognition are distinct Enterprise 10.4 processing concerns, and the
exact product/version/component applicability must be established before handing
their implementation to the pipeline or ingest owner.[15][16][17] Never write a
line-breaking rule, timestamp rule, metadata override, configuration stanza,
pattern, or expression.

### 5. Build the stage and acceptance ledger

Use one row per stage. State what supplied evidence establishes and what it does
not establish:

| Stage | Preconditions | Supplied or expected evidence | Establishes | Does not establish | Owner | Stop signal | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| source export | scope, authority, export contract | source-side count, identity, or checkpoint basis | source emitted within the declared boundary | collector receipt or indexing | source owner | unauthorized or unbounded export | unknown/pending/pass/fail |
| collector/input readiness | applicable method and owner | review or separately authorized readiness evidence | component is prepared for its own stage | source delivery or downstream health | implementation owner | applicability or security conflict | unknown/pending/pass/fail |
| handoff receipt | transport and ownership contract | bounded receipt evidence | next hop received the declared payload | parsing, routing, or indexing | hop owner | disclosure or contract mismatch | unknown/pending/pass/fail |
| representative arrival | approved fixtures and time window | stable event identity or bounded count | expected fixtures arrived | complete reconciliation | validation owner | missing, duplicate, or unauthorized event | unknown/pending/pass/fail |
| boundary and time | event and timestamp contracts | aligned raw-to-indexed comparison | tested event shape and time are correct | untested variants | source and ingest owners | merge, split, truncation, or time outside tolerance | unknown/pending/pass/fail |
| indexed metadata | intended index/source/sourcetype/host | bounded indexed observation | tested metadata matches | semantic field or CIM correctness | platform owner | unauthorized destination or wrong metadata | unknown/pending/pass/fail |
| reconciliation and latency | identity/count basis, tolerances, window | source and destination observations over the same boundary | measured loss, duplicate, ordering, and latency are within declared tolerance | future sustained behavior | acceptance owner | threshold exceeded or evidence cannot reconcile | unknown/pending/pass/fail |
| privacy and sign-off | data/security review and accountable approver | explicit review and acceptance record | declared acceptance is approved | implementation or future health | security and acceptance owners | unresolved sensitivity or missing authority | unknown/pending/pass/fail |

A successful prerequisite, synthetic endpoint request, open connection, component
status, preview, GUI upload, add-on display, or searchable event proves only its own
stage. It never proves source export, complete delivery, correct boundaries,
timestamps, metadata, reconciliation, semantic normalization, sustained latency,
or owner acceptance unless direct aligned evidence covers that claim. HEC-specific
proof and testing belong to **HEC Setup and Troubleshooting**.[3][24]

### 6. Decide readiness

Return exactly one overall state and, when useful, a state per independent data
family or method. Apply this precedence in order:

1. `not_ready`: use whenever supplied observation shows a wrong destination index,
   `source`, `sourcetype`, or `host`; malformed or contract-violating event boundary
   or timestamp; partial, missing, delayed, or duplicate events; an active drop,
   queue, or fault; or contradictory current delivery state. Missing applicability,
   ownership, or acceptance evidence does not weaken or replace this state. Also use
   `not_ready` when supplied or documented evidence shows that the proposed path
   violates a requirement, applicability boundary, security decision, metadata or
   event contract, or acceptance obligation.
2. `decision_blocked`: use only when a named prerequisite is missing before any
   unsafe or failing current state has been observed, and that gap prevents a
   responsible method or handoff decision. Do not use it as a softer companion to
   an observed failure.
3. `ready`: use only when no `not_ready` condition is observed, all
   decision-changing requirements and applicability are established, accountable
   owners and authority are named, acceptance is defined, and the ordered handoff
   can proceed without another onboarding decision.

`ready` means ready for separately authorized implementation, not configured,
deployed, indexed, accepted, or complete. Never convert `unknown`, `pending`, a
reported stage, or an unaligned test into `pass`.

A supplied source path that cannot currently deliver through the attempted
method is `not_ready` for that path even when the direct-integration-versus-
collector applicability decision remains `decision_blocked`. Preserve both
states; do not soften the current failure to the method-selection status.

When an active fault is mixed with onboarding, preserve the future-source contract
and acceptance work that is independent of the incident. Mark affected runtime
acceptance `not_ready`, retain every remaining evidence gap without changing that
status, route current diagnosis to **Forwarder and Data Ingest Doctor** or the HEC
specialist, and stop before fault isolation, configuration advice, or remediation.

### 7. Produce the ordered implementation handoff

Return an advisory sequence, not implementation instructions:

1. resolve decision-changing unknowns with the named evidence owner;
2. confirm the selected method's current applicability and prerequisites;
3. approve the source, metadata, event, timestamp, security, and acceptance
   contracts;
4. hand each separable implementation job to the exact sibling or accountable
   source/platform/provider owner;
5. require aligned stage evidence and owner sign-off before closure.

Each handoff must include: retained supplied facts; unresolved contradictions and
unknowns; exact product/deployment/provider applicability; source and event
contract; selected method or conditional options; intended metadata; acceptance
rows; accountable owner and authority; stop signals; and an explicit `not executed`
state. Do not include endpoint mechanics, configuration, commands, SPL, patterns,
architecture, rollout steps, field mappings, credentials, or private event text.

Require each implementation or diagnostic owner to return objective evidence for
the exact assigned stage, its observation boundary and time, result, owner, and
remaining unvalidated work. On reassessment or completion, repeat the exact overall
status and any per-family status without softening it; preserve the objective return
evidence, accountable owners, retained onboarding and acceptance obligations, exact
handoffs, unresolved gaps, and all work not validated or performed. Never claim
completion from a ticket state or handoff acknowledgment.

## Final-answer contract

Return in this order:

1. **Decision and scope:** `ready`, `not_ready`, or `decision_blocked`, plus the
   smallest reason and any independent data-family split.
2. **Evidence ledger:** supplied facts, documented applicability, contradictions,
   inferences, and decision-changing unknowns.
3. **Smallest next questions:** only questions that can change the pending choice.
4. **Method comparison:** supported candidates, prerequisites, requirement fit,
   ownership, and rejected or blocked rationale.
5. **Source and event contract:** index, source, sourcetype, host, encoding,
   boundaries, timestamp behavior, representative normal and edge cases.
6. **Acceptance matrix:** stage evidence, owner, tolerance/window, stop signal, and
   honest state.
7. **Ordered handoffs:** exact sibling display name and slug or accountable role,
   retained contract, prerequisites, and expected return evidence.
8. **Completion and return evidence:** repeat the exact status; list objective
   evidence returned or still required, owners, retained onboarding obligations,
   exact handoffs, unresolved gaps, and unvalidated work. If no completion evidence
   was supplied, state `completion not established`.
9. **Not validated and not performed:** state that no setup, troubleshooting,
   rollout, architecture, field/CIM implementation, configuration, deployment,
   mutation, remediation, or live acceptance occurred.

Put a point-of-use current public Splunk citation beside every decisive documented
method, product, provider, version, or administrator-boundary claim. If current
documentation is silent, inaccessible, conflicting, or version-mismatched, narrow
the claim and keep the affected decision blocked.

Use these exact special-case source paths in customer answers; do not substitute
the older anchors below or generic overview pages:

- Cloud 10.5.2605 HEC boundary:
  https://help.splunk.com/en/data-management/onboard-data-to-splunk-cloud-platform/other-ways-to-onboard-data/10.5.2605/get-data-with-http-event-collector/set-up-and-use-http-event-collector-in-splunk-web
- Cloud 10.5.2605 OpenTelemetry Collector for Kubernetes scope:
  https://help.splunk.com/en/data-management/onboard-data-to-splunk-cloud-platform/other-ways-to-onboard-data/10.5.2605/get-other-kinds-of-data-in/overview-of-the-splunk-opentelemetry-collector-for-kubernetes
- Data Inputs 1.18 applicability:
  https://help.splunk.com/en/data-management/ingest-data-from-cloud-sources/use-data-inputs/1.18/introduction/about-data-inputs
- Data Inputs 1.18 AWS prerequisites:
  https://help.splunk.com/en/data-management/ingest-data-from-cloud-sources/use-data-inputs/1.18/amazon-web-services-data/prerequisites-for-onboarding-aws-data-sources
- Cloud 10.5.2605 provider boundary:
  https://help.splunk.com/en/splunk-cloud-platform/get-started/service-terms-and-policies/10.5.2605/information-about-the-service/splunk-cloud-platform-service-details
- Enterprise 10.4 event-boundary concept:
  https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/configure-event-processing/configure-event-line-breaking
- Enterprise 10.4 timestamp-assignment concept:
  https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/configure-timestamps/how-timestamp-assignment-works
- Cloud 10.5.2605 default indexed-field obligations:
  https://help.splunk.com/en/data-management/onboard-data-to-splunk-cloud-platform/other-ways-to-onboard-data/10.5.2605/configure-indexed-field-extraction/about-default-fields-host-source-sourcetype-and-more

HEC is a receiving boundary, not an OTLP sender integration or collector. The
Kubernetes OTel page proves Kubernetes scope only. If the source/product/version
does not match, use both pages only to bound what they do not establish and keep
direct integration or collector selection blocked. For Splunk Cloud framing and
timestamp faults, Enterprise parsing pages are non-decisive concept catalogs;
they cannot establish the Cloud processor or effective behavior.

Minimize the final URL set to the exact prompt-material authorities:

- For a Splunk Cloud rsyslog path with merged/dropped records and no HEC claim,
  cite Cloud default fields for intended `host`, `source`, and `sourcetype`
  obligations, plus Enterprise line breaking and timestamp assignment as
  explicitly non-decisive parsing concepts. Do not cite a Cloud timestamp page,
  HEC, or generic collection pages; Cloud processor and effective timestamp
  behavior remain evidence-dependent.
- For a proposed Data Manager/Data Inputs object-storage method whose decisive
  gap is provider-provisioned account applicability, cite only Data Inputs 1.18
  About Data Inputs, AWS onboarding prerequisites as the bounded prerequisite
  example, and Cloud Service Details. Do not cite GCP, Azure, Cloud default-field,
  or Cloud timestamp pages unless the prompt separately makes those exact
  provider or metadata behaviors decision-changing.

Before returning, audit every URL against the smallest applicable source set. A
valid adjacent source is still wrong when it does not support a material claim in
the exact prompt.

## Examples

- Assess a sparse new-source request and ask only the questions that can change
  the next collection-method decision.
- Compare documented collection methods for an exact source product, Splunk
  deployment, version, provider, and ownership boundary.
- Define intended and observed metadata, event-boundary, timestamp, reconciliation,
  latency, and owner-acceptance obligations without writing configuration.
- Preserve onboarding findings while routing endpoint work, an active ingest fault,
  fleet rollout, pipeline architecture, and semantic normalization separately.

## Troubleshooting

- **Sparse request:** preserve the outcome and known context, return
  `decision_blocked`, and ask the smallest source identity/data-family, export,
  deployment, owner, or representative-event question that changes method choice.
- **Proposed connector, add-on, agent, sourcetype, or configuration:** retain it as
  proposed, verify current applicability, and do not treat it as implementation
  authority or accepted state.
- **Different preview and production behavior:** require aligned evidence from the
  intended production path; a preview or upload does not prove distributed
  ingestion behavior.
- **Wrong or missing indexed event:** return `not_ready`, retain intended and
  observed metadata, all evidence gaps, and acceptance obligations, then route
  active diagnosis without proposing settings.
- **Mixed new source and incident:** split the jobs, keep source intake here, and
  route only active diagnosis or remediation.
- **Requested setup, fix, config, deployment, or implementation:** return the
  contract, owner, prerequisites, acceptance evidence, and exact handoff only.

## Public documentation anchors

Use these exact public anchors at point of use, then verify that they still match
the target product and version before relying on them:

[1] [Cloud 10.5.2605: About default fields](https://help.splunk.com/en/splunk-cloud-platform/get-started/get-data-in/10.5.2605/configure-indexed-field-extraction/about-default-fields-host-source-sourcetype-and-more)

[2] [Cloud 10.5.2605: Configure timestamp recognition](https://help.splunk.com/en/splunk-cloud-platform/get-started/get-data-in/10.5.2605/configure-timestamps/configure-timestamp-recognition)

[3] [Cloud 10.5.2605: Set up and use HTTP Event Collector in Splunk Web](https://help.splunk.com/en/splunk-cloud-platform/get-started/get-data-in/10.5.2605/get-data-with-http-event-collector/set-up-and-use-http-event-collector-in-splunk-web)

[4] [Cloud 10.5.2605: Splunk Cloud Platform service details](https://help.splunk.com/en/splunk-cloud-platform/get-started/service-terms-and-policies/10.5.2605/information-about-the-service/splunk-cloud-platform-service-details)

[5] [Cloud 10.5.2605: Introduction to Getting Data In](https://help.splunk.com/en/splunk-cloud-platform/administer/admin-manual/10.5.2605/get-data-into-splunk-cloud-platform/introduction-to-getting-data-in)

[6] [Cloud 10.5.2605: Get AWS data into Splunk Cloud Platform](https://help.splunk.com/en/splunk-cloud-platform/administer/admin-manual/10.5.2605/get-data-into-splunk-cloud-platform/get-amazon-web-services-aws-data-into-splunk-cloud-platform)

[7] [Cloud 10.5.2605: Get Microsoft Azure data into Splunk Cloud Platform](https://help.splunk.com/en/splunk-cloud-platform/administer/admin-manual/10.5.2605/get-data-into-splunk-cloud-platform/get-microsoft-azure-data-into-splunk-cloud-platform)

[8] [Data Inputs 1.18: Overview of source types](https://help.splunk.com/en/data-management/ingest-data-from-cloud-sources/use-data-inputs/1.18/getting-data-in-gdi/overview-of-source-types-for-data-inputs)

[9] [Data Inputs 1.18: AWS data inputs](https://help.splunk.com/en/data-management/ingest-data-from-cloud-sources/use-data-inputs/1.18/amazon-web-services-data/aws-data-inputs)

[10] [Data Inputs 1.18: Google Cloud Platform data](https://help.splunk.com/en/data-management/ingest-data-from-cloud-sources/use-data-inputs/1.18/google-cloud-platform-data)

[11] [Data Inputs 1.18: Microsoft Azure data](https://help.splunk.com/en/data-management/ingest-data-from-cloud-sources/use-data-inputs/1.18/microsoft-azure-data)

[12] [Enterprise 10.4: About default fields](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/configure-indexed-field-extraction/about-default-fields-host-source-sourcetype-and-more)

[13] [Enterprise 10.4: Why source types matter](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/configure-source-types/why-source-types-matter)

[14] [Enterprise 10.4: About hosts](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/configure-host-values/about-hosts)

[15] [Enterprise 10.4: Configure timestamp recognition](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/configure-timestamps/configure-timestamp-recognition)

[16] [Enterprise 10.4: Configure event line breaking](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/configure-event-processing/configure-event-line-breaking)

[17] [Enterprise 10.4: Configuration parameters and the data pipeline](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/administer-splunk-enterprise-with-configuration-files/configuration-parameters-and-the-data-pipeline)

[18] [Enterprise 10.4.0: inputs.conf](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/configuration-file-reference/10.4.0-configuration-file-reference/inputs.conf)

[19] [Enterprise 10.4.1: inputs.conf](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/configuration-file-reference/10.4.1-configuration-file-reference/inputs.conf)

[20] [Enterprise 10.4.2: inputs.conf](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.4/configuration-file-reference/10.4.2-configuration-file-reference/inputs.conf)

[21] [Enterprise 10.4: How do you want to add data?](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/how-to-get-data-into-your-splunk-deployment/how-do-you-want-to-add-data)

[22] [Enterprise 10.4: Monitor files and directories](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/get-data-from-files-and-directories/monitor-files-and-directories)

[23] [Enterprise 10.4: Get data from TCP and UDP ports](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/get-data-from-network-sources/get-data-from-tcp-and-udp-ports)

[24] [Enterprise 10.4: Set up and use HTTP Event Collector in Splunk Web](https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/10.4/get-data-with-http-event-collector/set-up-and-use-http-event-collector-in-splunk-web)

[25] [About the Edge Processor solution](https://help.splunk.com/en/data-management/process-data-at-the-edge/use-edge-processors-for-splunk-cloud-platform/introduction/about-the-edge-processor-solution)

[26] [About Ingest Processor](https://help.splunk.com/en/data-management/process-data-at-ingest-time/use-ingest-processor/introduction/about-ingest-processor)

[27] [Universal Forwarder 10.4: About the universal forwarder](https://help.splunk.com/en/splunk-enterprise/forward-and-process-data/universal-forwarder-manual/10.4/about-the-universal-forwarder/about-the-universal-forwarder)

[28] [Enterprise 10.4: About Agent Management](https://help.splunk.com/en/splunk-enterprise/administer/update-your-deployment/10.4/agent-management/about-agent-management)

[29] [Enterprise 10.4: About fields](https://help.splunk.com/en/splunk-enterprise/manage-knowledge-objects/knowledge-management-manual/10.4/fields-and-field-extractions/about-fields)

[30] [CIM 8.6: Overview of the Splunk Common Information Model](https://help.splunk.com/en/splunk-cloud-platform/common-information-model/8.6/introduction/overview-of-the-splunk-common-information-model)
