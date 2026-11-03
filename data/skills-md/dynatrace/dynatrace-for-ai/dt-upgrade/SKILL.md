---
name: dt-upgrade
description: >
  Guide users through Dynatrace upgrade from classic/2nd-gen to 3rd-gen.
  Assess tenant readiness, run tracking queries, identify migration actions
  for dashboards, entity queries, IAM, management zones, OpenPipeline,
  service detection, logs, K8s, RUM, synthetic, alerting.
  Includes cloud integration migration (AWS, Azure, GCP) from classic
  to new (Smartscape on Grail): connection discovery, metric mapping,
  and cutover.
  Keywords: upgrade, migrate, classic, gen3, phase2, phase3, readiness,
  cloud integration, AWS, Azure, GCP, classic connection, new connection,
  Smartscape on Grail, fleet management, Site Reliability Guardian (SRG),
  classic pipeline, log processing pipeline, bizevents pipeline,
  pipeline upgrade, classic processing rules,
  ActiveGate, authToken, auth token,
  DynaKube, dynatrace-operator, classicFullStack, Platform token,
  enable RUM on Grail, RUM migration, mobile RUM, web RUM, Experience Vitals.
license: Apache-2.0
---

# Dynatrace Upgrade Skill

Help users assess and execute their Dynatrace upgrade from classic/2nd-generation to 3rd-generation platform concepts.

## Overview

The Dynatrace upgrade transitions environments from classic (2nd-gen) features to 3rd-generation equivalents. A phase is a property of an environment, not of a customer:

- **Phase 1** -- Hybrid default. Gen2 and gen3 UI side by side, classic apps enabled, nothing removed. Where most existing customers are today.
- **Phase 2** -- New environments only (SaaS 331+). Removes 32 classic apps, 21 APIs, management zones, and auto-tagging. **No in-place upgrade from Phase 1** -- Phase 2 is only available at environment creation.
- **Phase 3** -- Opt-in gen2 retirement. Removes 50 apps, 45 APIs, API tokens, entity IDs, and all remaining classic concepts. Per environment and **permanent** -- everything must be migrated before the opt-in.

Establish which phase an environment is in before assessing it. See [overview.md](references/overview.md) for the full phase detail, removal lists, and the paths into Phase 3.

## Data Types

When assessing upgrade readiness, tracking data falls into these categories:

- **Classic Usage** -- Tracks individual usage events of legacy features (views, queries, API calls)
- **Classic Configuration** -- Lists classic config objects that may need migration
- **Readiness Status** -- Per-item pass/fail compatibility check for Phase 3
- **New Usage** -- Tracks adoption of gen3 replacements

## Operating Workflow

This skill drives the upgrade end to end: scope it, plan it, execute it, verify it. Follow the stages below for any request that changes tenant configuration.

> **Hard gate:** do not write a configuration to environment, POST an object, delete a classic object, or start executing a plan until you have told the user what you intend and they have said yes. The artifacts scale with the size of the job. However, the approval is always required.

**Classify the request first and say which tier you picked**, so the user can override it:

- **Question** — a readiness assessment or a "what replaces X" question. No configuration changes. Run the area's tracking queries, report findings, done.
- **Single task** — a limited upgrade task scoped to one item in the Reference Index. Ask the questions that matter, present the approach in chat, get a yes, then execute with a todo list. No spec or plan file.
- **Program** — three or more areas, a cross-cutting change, or a full tenant upgrade. Full stages below with written spec and plan.

When torn between two tiers, take the heavier one. Discovering hidden scope mid-engagement upgrades the tier — say so and step up.

**Read `references/upgrade-workflow.md` before a Program-tier engagement**, and whenever you need the spec template, the plan task structure, or the per-object-type verification steps.

### Stage 1 — Scope

**Validate access and tooling before the first query.** Run `dtctl doctor` — it checks config validity, current context, environment reachability, token retrieval, and API authentication in one command. Then confirm the context points at the *intended* environment (`dtctl config current-context`): running an upgrade against the wrong tenant is the worst failure this skill can cause. If dtctl is not configured, stop and ask which environment to target rather than guessing from a URL in the conversation. Report what you verified, and against which environment, before moving on.

Then establish tenant context and run the discovery queries before asking detailed questions: never plan a migration for an area with no classic usage. Ask clarifying questions one at a time, preferring multiple choice. Establish which objects are still needed at all — abandoned classic config should be deleted, not migrated. Present the scope and approach, then **stop and wait for an explicit yes**. Program tier writes the spec to `docs/dt-upgrade/YYYY-MM-DD-<topic>-spec.md`, self-reviews it, and has the user review it before planning.

### Stage 2 — Plan

One task per migration unit, each naming its reference file, its exact objects, its dependencies, and ending in something the user can review. Bite-sized steps with the actual queries and field mappings written out — "map the fields appropriately" and "handle edge cases" are plan failures, not steps. Self-review against the spec for coverage, placeholders, and task order, then save to `docs/dt-upgrade/YYYY-MM-DD-<topic>-plan.md`.

### Stage 3 — Execute

Reread the plan critically and raise concerns *before* starting. One task at a time, one todo per task, checkpoint with the user between tasks. Stop and ask on any blocker — a missing permission, a field with no gen3 equivalent, an unclear step. Never invent a configuration value to keep moving, and never delete a classic object before its replacement is verified working.

### Stage 4 — Verify

**Evidence before claims.** If you have not run the check in this message, you cannot say it passed. Use every check the object type supports:

1. **Reference cross-check** — walk the generated config field by field against the area's reference file. Always.
2. **User review** — show the config and name every non-mechanical decision you made. Always.
3. **Tracking query** — re-run the area's queries and paste the output.
4. **Pre-write validation** — only where the area's reference documents one, using exactly the command it names.

**Do not assume a dry run exists.** `dtctl apply --dry-run` is a client-side preview only: it reports success without contacting the API, even for a schema that does not exist. For most object types there is no server-side validation before the real write, so checks 1 and 2 are the primary verification, not a fallback. Never describe a client-side parse as validation, and "the API accepted it" is not evidence that the config does what the classic object did.

### Stage 5 — Wrap up

Re-run the readiness scan for the areas touched, then report migrated / remaining / blocked with the evidence and the artifact paths, and offer the next steps. Wait for the user to choose.

### When something breaks

Find the root cause before changing anything: read the full error including the response body, reproduce it, check what changed, and compare the broken object against a working one field by field. Form one hypothesis, test one change. **After three failed attempts, stop** and bring it to the user — three failures usually means the approach is wrong, not that the fourth fix is the right one.

**On `401` or `403`, suspect the credential before the request.** The surface decides the credential: Platform API (`<env>.apps.dynatrace.com/platform/`) takes a platform token (`dt0s16.*`) or OAuth; classic API (`<env>.live.dynatrace.com/api/`) takes an access token (`dt0c01.*`); Account Management (`api.dynatrace.com`) takes neither — only account OAuth client credentials exchanged for a short-lived (~5 min) bearer.

Only a **subset** of classic APIs is proxied through the Platform API. dtctl reaches that subset via browser login or a platform token; for the rest there is no dtctl path — call the `.live` host directly with an access token. That is expected in upgrade work, not a misconfiguration. dtctl does not support `api.dynatrace.com` and cannot use account OAuth client credentials at all — its browser login is a different flow entirely.

Name the exact missing scope and hand it back to the user — a credential gap is a blocker, not something to retry. Never echo a token value. See [upgrade-workflow.md](references/upgrade-workflow.md#credentials-suspect-them-first-on-401-and-403) for the surface map and triage table.

### Git, when present

Check `git rev-parse --is-inside-work-tree` once, at the start of execution. Not a repository: skip all git steps and never suggest `git init`. A repository: offer a working branch, and commit after each task passes verification. **Never push, never open a pull request, never force-push** — integration with a remote is the user's decision, outside this skill.

### Red flags

| Thought | Reality |
|---|---|
| "The mapping is obvious, I'll just write the config" | The reference exists because the mapping has exceptions. Read it for every task. |
| "They asked for the upgrade, so applying it is approved" | Approval to plan is not approval to apply. Show the config first. |
| "The API accepted it, so it is correct" | Accepted means well-formed, not equivalent to the classic object. |
| "I'll clean up the classic objects while I'm here" | Deleting before the replacement is verified is unrecoverable. Separate task, separate approval. |
| "The plan grew but I'm nearly done" | Hidden scope upgrades the tier. Say so and step up. |
| "The branch is green, I'll push it" | Never. No push, no PR, no exceptions. |

## Reference Index

### General

| File | Description |
|---|---|
| [overview.md](references/overview.md) | Upgrade phases, data types, general prerequisites and planning checklist |
| [upgrade-workflow.md](references/upgrade-workflow.md) | Scope/plan/execute/verify stages, spec and plan templates, verification checks, credential and API-surface triage, debugging, git handling |

### Shared

Cross-cutting utilities reused by multiple upgrade references.

| File | Description |
|---|---|
| [metric-transpiler.md](references/shared/metric-transpiler/metric-transpiler.md) | Convert classic 2G metric selectors/expressions to Grail DQL via the `/api/v2/metrics/transpile` API |

### Platform

| Classic Concept | Gen3 Replacement | Reference |
|---|---|---|
| Dashboards Classic, Data Explorer, Metrics, Reports | Dashboards, Notebooks | [dashboards-classic.md](references/platform/dashboards-classic/dashboards-classic.md) |
| 2nd gen entity queries | Smartscape / raw data enrichment | [entity-queries.md](references/platform/entity-queries/entity-queries.md) |
| IAM 2nd gen roles | IAM default policies | [iam-2nd-gen-roles.md](references/platform/iam-2nd-gen-roles/iam-2nd-gen-roles.md) |
| 2nd gen role grants scoped to a management zone | IAM policies on enriched fields/tags, or Grail bucket permissions | [mz-permission-scopes.md](references/platform/iam-2nd-gen-roles/mz-permission-scopes.md) |
| Management Zones | Segments / IAM policies / Grail buckets | [management-zones.md](references/platform/management-zones/management-zones.md) |
| Autotagging | Source-side / central / OpenPipeline primary tags | [autotagging.md](references/platform/autotagging/autotagging.md) |
| Custom devices (entity API) | Smartscape API | [custom-devices.md](references/platform/custom-devices/custom-devices.md) |
| SNMP custom device monitoring; ICMP/TCP `MULTI_PROTOCOL` monitors with `targetFilter` (dynamic entity lookup) | SNMP extension (`com.dynatrace.extension.snmp`) autodiscovery; `NETWORK_AVAILABILITY` monitors with static host targeting (dtctl/Settings API) or `MULTI_PROTOCOL` monitors with explicit `targetList` (Environment API v2) | [custom-devices-synthetic.md](references/platform/custom-devices/custom-devices-synthetic.md) |
| Classic alerting and problem notifications (metric events, disk rules, AWS anomaly detection, process availability, alerting profiles, notification integrations) | DQL-based anomaly detectors, edge-side detectors, Workflow notifications | [alerting-and-problem-notifications.md](references/platform/alerting-and-problem-notifications/alerting-and-problem-notifications.md) |
| Classic pipeline (Logs, Business events) | OpenPipeline pipelines | [classic-pipeline.md](references/platform/classic-pipeline/classic-pipeline.md) |
| Classic credential vault API (`/api/v2/credentials`, `@dynatrace-sdk/client-classic-environment-v2`) | Platform Credential Vault API (`/platform/credential-vault/v1/`, `@dynatrace-sdk/client-credential-vault`) | [credential-vault.md](references/platform/credential-vault/credential-vault.md) |

### Edge Data Platform

| Classic Concept | Gen3 Replacement | Reference |
| ---|---|---|
| Classic cloud integrations (AWS/Azure/GCP) | Fleet Management App | [classic-cloud-integrations.md](references/edge-data-platform/classic-cloud-integrations/classic-cloud-integrations.md) |
| Network-zones enforcement | -- | [network-zones.md](references/edge-data-platform/network-zones/network-zones.md) |
| ActiveGate authentication enforcement (Phase 3) | -- | [activegate-auth-tokens.md](references/edge-data-platform/activegate-auth-tokens/activegate-auth-tokens.md) |
| Cloud telemetry enrichment | Central settings for ingest enrichment and primary Grail tags | [cloud-telemetry-enrichment.md](references/edge-data-platform/cloud-telemetry-enrichment/cloud-telemetry-enrichment.md) |
| Dynatrace Operator (version, token type, deployment mode, operand artifacts) | Dynatrace Operator 1.10.0+ with Platform token and supported OneAgent deployment mode | [dynatrace-operator.md](references/edge-data-platform/dynatrace-operator/dynatrace-operator.md) |
| EF2 extensions below Smartscape2 minimum version; monitoring configs below required version or with management-zone scope | Extension OpenPipeline entity extraction (Smartscape2); monitoring config migration | [ef2-entity-extraction.md](references/edge-data-platform/extensions/ef2-entity-extraction.md) |
| DT Plugins (EF1), custom only | EF2 extension via Hub or custom rebuild | [plugins-ef1.md](references/edge-data-platform/extensions/plugins-ef1.md) |

### Application Observability

| Classic Concept | Gen3 Replacement | Reference |
|---|---|---|
| Log v2 | Logs on Grail | [log-v2.md](references/application-observability/log-v2/log-v2.md) |
| Classic Full Service Detection (SDv1) Rules | -- | [classic-service-detection-rules.md](references/application-observability/classic-service-detection-rules/classic-service-detection-rules.md) |
| SDv1 Global Failure Detection Rules | -- | [global-failure-detection-rules.md](references/application-observability/global-failure-detection-rules/global-failure-detection-rules.md) |
| Request Attributes | -- | [request-attributes.md](references/application-observability/request-attributes/request-attributes.md) |
| Global Request Naming Rules | -- | [global-request-naming-rules.md](references/application-observability/global-request-naming-rules/global-request-naming-rules.md) |
| Service-specific Request Naming Rules | -- | [service-specific-request-naming-rules.md](references/application-observability/service-specific-request-naming-rules/service-specific-request-naming-rules.md) |
| Calculated Service Metrics | OpenPipeline span metric extraction, where the definition can be expressed on spans | [calculated-service-metrics.md](references/application-observability/calculated-service-metrics/calculated-service-metrics.md) |
| External Services (database, opaque, and third-party) | Service App | [external-services.md](references/application-observability/external-services/external-services.md) |
| Messaging/Queues and Screens | -- | [messaging-queues.md](references/application-observability/messaging-queues/messaging-queues.md) |
| Attribute Masking Configs (OTEL ingest pipeline) | -- | [attribute-masking-configs.md](references/application-observability/attribute-masking-configs/attribute-masking-configs.md) |

### Infrastructure Observability

| Classic Concept | Gen3 Replacement | Reference |
|---|---|---|
| Classic disk anomaly detection | Disk Edge | [classic-disk-anomaly-detection.md](references/infrastructure-observability/classic-disk-anomaly-detection/classic-disk-anomaly-detection.md) |
| Classic host availability alerting (`builtin:anomaly-detection.infrastructure-hosts`, connection lost and graceful shutdown) | Custom alerts from the Infrastructure & Operations app templates (nothing configured by default in Phase 3) | [classic-host-availability-alerting.md](references/infrastructure-observability/classic-host-availability-alerting/classic-host-availability-alerting.md) |
| VMware ActiveGate integration | VMware Extension | [vmware-activegate-integration.md](references/infrastructure-observability/vmware-activegate-integration/vmware-activegate-integration.md) |
| CloudFoundry ActiveGate integration | CloudFoundry Extension | [cloudfoundry-activegate-integration.md](references/infrastructure-observability/cloudfoundry-activegate-integration/cloudfoundry-activegate-integration.md) |
| Classic Maintenance Windows | Gen3 Maintenance Windows | [classic-maintenance-windows.md](references/infrastructure-observability/classic-maintenance-windows/classic-maintenance-windows.md) |
| Classic maintenance windows scoped to synthetic monitors (`SYNTHETIC_TEST`, `SYNTHETIC_TEST_STEP`, `HTTP_CHECK`, `HTTP_CHECK_STEP`, `SYNTHETIC_LOCATION`, `EXTERNAL_SYNTHETIC_TEST`, `EXTERNAL_SYNTHETIC_TEST_STEP` entity types) | Gen3 Maintenance Windows with `dt.smartscape.http_monitor`, `dt.smartscape.browser_monitor`, `primary_tags.<key>`, `dt.security_context`, or segment filters | [classic-maintenance-windows-synthetic.md](references/infrastructure-observability/classic-maintenance-windows/classic-maintenance-windows-synthetic.md) |
| Classic Database monitoring | Database Observability | [classic-database-monitoring.md](references/infrastructure-observability/classic-database-monitoring/classic-database-monitoring.md) |
| Classic Network monitoring | Infrastructure Observability extensions | [classic-network-monitoring.md](references/infrastructure-observability/classic-network-monitoring/classic-network-monitoring.md) |
| Classic Windows Service monitoring | OS Services monitoring | [classic-windows-service-monitoring.md](references/infrastructure-observability/classic-windows-service-monitoring/classic-windows-service-monitoring.md) |
| Classic OneAgent process connection monitoring | OneAgent network connection monitoring | [classic-process-connection-monitoring.md](references/infrastructure-observability/classic-process-connection-monitoring/classic-process-connection-monitoring.md) |
| Kubernetes Telemetry Enrichment | Central enrichment config | [kubernetes-telemetry-enrichment.md](references/infrastructure-observability/kubernetes-telemetry-enrichment/kubernetes-telemetry-enrichment.md) |
| Inferred hosts (process-in-container, no host agent) | No Gen3 equivalent — install OneAgent in INFRASTRUCTURE or DISCOVERY mode | [inferred-hosts.md](references/infrastructure-observability/inferred-hosts/inferred-hosts.md) |

### Cloud Automations

| Classic Concept | Gen3 Replacement | Reference |
|---|---|---|
| SRG with classic SLO reference | SRG with DQL objectives | [srg-classic-slo.md](references/cloud-automations/srg-classic-slo/srg-classic-slo.md) |

### Application Security

| Classic Concept | Gen3 Replacement | Reference |
|---|---|---|
| Vulnerabilities App | Updated vulnerability monitoring | [vulnerabilities-app.md](references/application-security/vulnerabilities-app/vulnerabilities-app.md) |

### Digital Experience

| Classic Concept | Gen3 Replacement | Reference |
|---|---|---|
| 3rd-party monitor integration (`POST /api/v1/synthetic/ext/tests`) | Grail-native events ingest API (`POST /platform/ingest/custom/events/external.tests`) | [ext-monitors-migration.md](references/digital-experience/ext-monitors-migration/ext-monitors-migration.md) |
| Enable RUM on Grail — bulk frontend enablement (web, mobile; inventory, classify, enable, validate) | RUM on the latest Dynatrace | [enable-rum-on-grail.md](references/digital-experience/enable-rum-on-grail/enable-rum-on-grail.md) |
| RUM Anomaly detection | Frontend health alerts | [rum-anomaly-detection.md](references/digital-experience/rum-anomaly-detection/rum-anomaly-detection.md) |
| Classic action and session property capturing, and classic user tagging (user tag rules on a web application) | Event and session property capturing, config-less properties; a user tag becomes `user.identifier`, set by `dynatrace.identifyUser()` or by an OpenPipeline rule — there is no Gen3 setting for it | [classic-action-session-properties.md](references/digital-experience/classic-action-session-properties/classic-action-session-properties.md) |
