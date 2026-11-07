---
name: deploy-adk-on-google-cloud
description: >-
  Select, implement, adapt or audit deployment of Python Google ADK agents on
  Cloud Run, Agent Runtime or GKE, including identity, packaging, browser
  validation, recovery and owned-resource cleanup. Use for ADK hosting
  decisions and deployment lifecycle work. Do not activate for general
  Kubernetes administration, non-ADK applications, canary, rollback or eval
  gates of later releases (adk-release-engineering), measured performance
  tuning (optimise-adk-on-google-cloud), telemetry and alerts
  (adk-agent-observability), FastAPI routes and process shape
  (adk-fastapi-backend), prompt-only changes (adk-agent-instructions owns
  prompt wording), or RAG and memory design without a deployment task.
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "3"
  last-tested: "2026-09-16"
  verified-against: "google-adk 2.8.0 live deployments 2026-09-14; 2.12.0 scaffold and api_server source read 2026-10-22"
  version: "2026.10.28"
---

# Deploy ADK on Google Cloud

Produce a deployment design, focused implementation or evidence-based audit that fits the existing project. Keep Cloud Run, Agent Runtime and GKE as modes of this one skill. The outcome includes an explicit resource and identity plan, meaningful verification and a separate cleanup procedure.

## Inspect before choosing

1. Read the project's instructions, dependency declarations and lockfiles, configuration templates, deployment definitions and tests. Establish the requested outcome: recommend, implement, review, deploy, recover or clean up. Preserve existing customisations and package management. When `agents-cli-manifest.yaml`, `deployment_metadata.json` or `deployment/terraform/` is present, the project is an Agents CLI project: keep its generated server, its Terraform ownership and its `agents-cli deploy` conventions, and consult the installed `google-agents-cli-deploy` skill for the command flags, the generated infrastructure and which fields Terraform owns; if it is not installed, report it as missing, name `uvx google-agents-cli setup` (which installs the Agents CLI skills) as the setup step, and continue from the project's own files.
2. Run `python "$SKILL_DIR/scripts/inspect_project.py" --project /path/to/project` using an available Python 3.11+ interpreter ([interpreters](references/operating-rules.md#helper-scripts-and-interpreters)). Substitute the actual paths; a GCP project ID for its planned read-only commands goes in `--gcp-project`, never `--project`. This is a bounded, offline inventory; it neither loads `.env` values nor executes project code or cloud commands. Inspect files outside its reported coverage manually. Read [compatibility.md](references/compatibility.md) when assessing versions, interpreting its output or changing an SDK integration.
3. Check the selected environment's Python and installed distribution versions as well as declared pins. Use package metadata without importing agent code. Record conflicts and uncertain compatibility. Preserve the target's versions; a different version requires contract validation, not an automatic upgrade or downgrade.
4. Locate the existing agent export, server factory, model/backend selection, tool effects, session/artefact services, user-authentication boundary and build context. Record configuration **keys and provenance**, keeping secret values out of reports. A root `.env` does not replace nested configuration. Treat hosting, inference, session storage and build locations separately.
5. Establish the operator, build, runtime and caller identities; on GKE add node and Kubernetes service-account identities. CLI login, ADC, ADC quota project and deployed workload identity are distinct. Discover project/billing/API access with explicitly scoped reads; denied access is unknown state, not proof of absence.

Inspection is complete when the current architecture, constraints, version status, missing prerequisites and intended scope are recorded. Missing credentials do not block local implementation or a reviewable plan.

## Choose the mode

| Workload requirement | Mode and reference |
| --- | --- |
| Managed HTTP service, custom web/API integration or control of the container | [Cloud Run](references/cloud-run.md). Choose native ADK deployment for an uncustomised server, or a custom container for an existing server and runtime requirements. |
| ADK package fits managed agent hosting and platform sessions | [Agent Runtime](references/agent-runtime.md). Legacy CLI/API identifiers still include `agent_engine` and `reasoningEngines`. |
| Existing Kubernetes platform or requirements needing Kubernetes controls | [GKE](references/gke.md). Prefer adapting the existing workload; a fresh cluster is an explicit infrastructure decision. |
| The deployment includes a browser frontend, static assets or streamed runs through a CDN or Firebase Hosting | Add [frontend hosting](references/frontend-hosting.md) to the chosen mode |
| Request asks which platform to choose | Compare only the relevant modes against HTTP integration, existing operations, state, identity, network and lifecycle needs. Deliver a recommendation without provisioning. |

These choices are not a maturity ladder. Keep the user's selected platform unless evidence shows a blocking requirement. Load only the selected mode's reference; read another when comparing alternatives. Self-hosting an open-weights model on an Agent Platform endpoint is model serving, not an ADK hosting mode: when the request includes it, consult the installed Google skills `agent-platform-deploy` and `agent-platform-inference` (from google/skills) for that part. The same applies to any `google/skills:<name>` a ticket lists as supporting: it operates the Google product, and this skill still decides what the deployment needs. If one is not installed, give the user `npx skills@latest add google/skills --skill <name>` (a restart of the coding agent loads it), invent none of its instructions, finish the local work, and record the product step in the ticket's Evidence as an execution-scope prerequisite.

## Implement or adapt

1. Present a short plan with the affected files, retained interfaces and validation steps. Read [lifecycle.md](references/lifecycle.md) before preparing provisioning, recovery or deletion. The plan must separate local code changes, cloud reads, mutations and paid tests.
2. Make the smallest coherent change. Reuse the existing agent and tools; do not replace the application with a support-ticket demonstration. Preserve package manager, locks, test framework, ports and naming conventions where compatible.
3. Prepare an allowlisted source package, explicit model/backend configuration, workload identity, authenticated access and selected state services. Review generated native-ADK files as well as authored files. Bind the application to the container's configured port and provide cheap health checks that do not call a model.
4. Prepare a data-only ownership journal or extend the existing lifecycle system: exact target, source fingerprint, original resource identities and IAM baseline, submitted operation IDs and created identities. On repeats, reconcile state before submitting more work. Use the lifecycle reference for uncertain outcomes and concurrency.
5. Complete the implementation and offline checks before asking for approval of a concrete cloud action. Production changes such as external state, user authorisation, IAP, distributed locking and release promotion need their own implementation and tests; historical lab success does not validate them.

When the request includes production users, durability, scaling or release operations, read the relevant sections of [production.md](references/production.md) for implementation decisions and acceptance tests. For a concrete failure, use [troubleshooting.md](references/troubleshooting.md) to separate provider, application and test-harness problems before retrying. These references add depth when needed; a small deployment edit does not require implementing every production extension.

## Permission boundary

<!-- shared:consequential-operations-brief -->
Inspection is read-only, and code generation authorises no deployment, paid
call or live test. Before any consequential operation (an API, billing or
quota change, a billable resource, a secret, IAM, a data migration, a
deployment, a deletion, or a paid or destructive test), read
[consequential operations](references/operating-rules.md#consequential-operations),
present the exact scope and limits, obtain explicit approval and end the turn
to wait for it. Cleanup is a separate confirmed operation on resources this
workflow created.
<!-- /shared:consequential-operations-brief -->

Never infer approval from elapsed time, a budget balance or a previous campaign; a command run in the same turn as its approval request was not approved, and irreversible deletion needs a typed confirmation naming the resource.

## Validate and report

Read [validation.md](references/validation.md) for the relevant acceptance checks, evidence levels and retry cases. Always run applicable local tests first. Check real tool output and final grounded text, not just HTTP status. Verify session recall explicitly; health does not prove model access or persistence.

For live work, use an approved isolated target and synthetic data. Record the submitted model/build/control work, deployed identity and cleanup result. An accepted timeout requires reconciliation; automatic replay can repeat tool effects. Completed deletion must be safe to repeat and independently checked within the caller's visibility.

Finish with files changed, commands actually executed, labelled test results, exact versions, manual steps and remaining uncertainty. Name retained resources and retention/visibility limits. Do not claim production readiness, cross-user authorisation, absence of all future charges, or coding-agent compatibility beyond the evidence.

<!-- shared:evidence-labels-brief -->
Label each result with its tier (`offline`, `local`, `live` or `release`) and
outcome (`pass`, `fail`, `blocked` or `not run`) as
[evidence labels](references/operating-rules.md#evidence-labels) defines them;
earlier, vendor and documentation-only results are `historical`,
`vendor-measured` or `guidance`, never this session's evidence.
<!-- /shared:evidence-labels-brief -->

Independent community project; not affiliated with or endorsed by Google.
