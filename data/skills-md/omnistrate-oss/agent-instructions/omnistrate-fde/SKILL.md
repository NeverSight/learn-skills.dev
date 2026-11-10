---
name: omnistrate-fde
description: Guide users through onboarding any application onto the Omnistrate platform and turning it into a managed SaaS offering. Covers Docker Compose, Helm charts, Terraform/OpenTofu modules, Kustomize, and mixed stacks, across all deployment models - hosted (your cloud), BYOC (customer cloud accounts, incl. BYO-VPC and PrivateLink), BYOC-K8s (customer-managed Kubernetes, no infra provisioning), and air-gapped/on-prem installers. Also covers monetization - pricing, Stripe end-to-end billing, usage metering export, custom billing dimensions, and cloud-marketplace/Chargebee/Clazar integrations. Use when a customer/ISV wants to onboard, "SaaS-ify", productize, or offer their software as a managed service, asks about BYOC / bring-your-own-cloud / on-prem / air-gapped delivery, or asks how to charge, meter, or bill for it. For Kubernetes operator-based services (CRDs + controller) use omnistrate-operator; for designing an architecture from scratch use omnistrate-sa; for debugging failed instances use omnistrate-sre.
---

# Onboarding Services to Omnistrate

All commands use the `omnistrate-ctl` CLI (alias `omctl`) — install and authenticate with `omnistrate-ctl login` first. An Omnistrate MCP server exposes equivalent tools (`mcp__ctl__*`); use those only if the user explicitly asks to work through MCP.

## Overview

Omnistrate is a control plane that turns your existing artifact — a Docker
Compose file, a Helm chart, a Terraform/OpenTofu module, Kustomize overlays, or
a Kubernetes operator — into a multi-tenant, managed SaaS. For connected
deployment models, Omnistrate handles automatic provisioning, lifecycle
operations (create/modify/stop/backup/restore/upgrade), and metering/billing.
For air-gapped deployments, Omnistrate produces a self-contained installer
artifact; the customer runs and operates it in a disconnected environment. You
bring the artifact; Omnistrate owns the substrate for connected models (node
pools, per-instance namespaces, storage, load balancers, TLS, DNS). Instances
can run in *your* cloud (hosted), in *your customers'* cloud accounts (BYOC), in
*your customers'* own Kubernetes clusters (BYOC-K8s, no infra provisioned by
you), or fully disconnected as an air-gapped installer. This skill is the
router: it runs the intake interview, picks the onboarding method and
deployment model, and drives the phased build-deploy-debug workflow using the
per-topic reference files in this directory.

**Core principle: never write Omnistrate spec YAML, field names, or CLI flags
from memory.** Untrained-knowledge Omnistrate specs are reliably wrong while
looking plausible. Every fragment must be copied from a reference file in this
directory or verified with `omctl docs` (below).

### Verifying spec fields against the platform

`omctl docs` serves the spec reference and the authoritative JSON schema straight
from the platform. **These subcommands need no `omnistrate-ctl login`** (they do make network calls) — use them instead of browsing the docs site or fetching schema URLs.

| Need | Command |
|---|---|
| Every compose tag / `x-omnistrate-*` extension | `omctl docs compose-spec` |
| One compose tag's reference, with examples | `omctl docs compose-spec "x-omnistrate-compute"` |
| Every ServicePlanSpec section | `omctl docs plan-spec` |
| One ServicePlanSpec section | `omctl docs plan-spec "helm chart configuration"` |
| Which JSON schemas can be requested | `omctl docs json-schema` |
| One extension's JSON schema | `omctl docs json-schema x-omnistrate-compute` |
| The whole compose / plan schema | `omctl docs json-schema compose` · `omctl docs json-schema service-plan` |
| `$sys.*` system parameters | `omctl docs system-parameters` |
| Full-text search across all guides | `omctl docs search "byoc privatelink" --limit 15` |
| **Check a finished spec against the schema** | `omctl docs validate --file spec.yaml` |

- Add `-o json` for machine-readable output.
- **Scope the schema.** `json-schema x-omnistrate-compute` is ~6 KB; `json-schema
  compose` is ~92 KB. Pull the one extension you are writing, not the world.
- A tag that matches nothing prints the available-tag list instead of erroring.
  Read that as "the name is wrong — pick from this list", then re-run.
- Compose extensions live under `compose-spec`; Helm / Terraform / Kustomize /
  operator plan fields live under `plan-spec` and the `service-plan` schema.
- The MCP docs-search tools (`mcp__ctl__docs_*`) are an optional alternative only
  when the user has asked to work through MCP.

**Caveats — each one was observed breaking a real agent run. Do not skip.**

- **`docs system-parameters` does not list workflow-context variables.** Its root has only `backup`, `compute`, `deployment`, `deploymentCell`, `id`, `network`, `storage`, `tenant`, `deterministicSeedValue`. `$sys.namespace`, `$sys.instanceId`, `$sys.restore.*`, `$sys.sourceInstanceId` and `$sys.targetInstanceId` are **absent from it but real** — they appear throughout the platform's own workflow examples. Never delete a `$sys.*` path merely because `system-parameters` omits it; confirm with `omctl docs search "workflow context system parameters" --limit 15`.
- **Casing: follow the doc examples.** The platform decodes specs through `encoding/json`, which matches field names case-insensitively, so `awsAccountId` and `AwsAccountId` both build. The generated schema now uses the documented lowerCamel spelling for the blocks that had drifted (`ActionHook`, `Deployment`/`OnPremDeployment`, `configurationOverrides.acceleratorConfiguration`). A few fields are documented UpperCamel and stay that way — `OsFamily`, `GpuClusterID`, and `CustomDNSConfig`'s `TargetKubernetesService`/`TargetName`/`TargetPort`. When in doubt copy the doc example; use the schema to decide whether a field exists at all.
- **Enum coverage is partial.** `tenancyType`, `cloudProvider`, api-param `type`, and action-hook `type`/`scope` now carry `enum` in the schema, so `omctl docs validate` catches a wrong value there. Everything else — storage types (`instanceStorageType`), `cpuArchitecture`, `networkingType` — is still a bare `{"type": "string"}`, so a wrong value passes silently. For those, get legal values from the prose (`omctl docs compose-spec "<tag>"` / `omctl docs plan-spec "<section>"`).
- **Check the finished spec, do not just look fields up.** `omctl docs validate --file spec.yaml` validates a compose spec or ServicePlanSpec against the authoritative schema and reports every violation with its path. Run it before every build — it catches unknown, misplaced and mistyped fields without touching your account, and exits non-zero so it works in a pre-commit hook or CI step. `additionalProperties` errors mask nested ones, so re-run after each fix until it comes back clean.
- **Prose sections are subsets of the schema.** A field missing from a `plan-spec` / `compose-spec` table is not proof it does not exist — cross-check the schema before concluding a field is invalid.
- **The compose schema accepts any `x-*` key** (`patternProperties: {"^x-": {}}`), so schema validation cannot catch a misspelled extension name. Only the `omctl docs compose-spec` tag list can.
- **`docs search` wants prose phrases, not identifiers.** `docs search "api parameter types"` works; `docs search "instanceTypes cloudProvider apiParam required"` returns unrelated pages. Use `--limit 15` — the syntax-bearing sections often rank 8–12, below the prose overview pages.

## Phase 0 — Intake (ALWAYS start here for new onboarding)

Ask these six questions in plain language, **one at a time**, adapting to what
the user already volunteered (skip anything already answered). No Omnistrate
jargon — translate their answers into platform concepts yourself. The target
user is an ISV who has never seen Omnistrate: they describe their product and
their customers' constraints in their own words, and you map those onto the
onboarding method (Decision Matrix) and deployment model (Q2).

**1. What does your product look like today?**
Docker Compose file / Helm chart / Terraform (or OpenTofu) module / Kustomize
overlays / Kubernetes operator (CRDs + controller) / plain container images /
nothing yet.
→ *Operator (CRDs + controller)* hands off to the **omnistrate-operator** skill.
→ *Nothing yet* (needs an architecture designed first) hands off to
**omnistrate-sa**.

**2. Where should instances run?** (multi-select — a service can offer several
models, but **each model becomes its own separate Plan**; never offer to build
a single plan serving multiple deployment models)
- *Your cloud account* → **hosted** deployment.
- *Your customers' cloud accounts* → **BYOC** (`byoaDeployment`). Probe for VPC
  constraints and no-public-egress requirements → **BYO-VPC** / **PrivateLink**.
  **Always ask explicitly: which AWS account config is designated as the
  "Control Plane" account?** The `byoaDeployment` account block uses that AWS
  account config no matter which cloud the customers deploy into (GCP/Azure/
  OCI/Nebius included) — never assume or silently default it
  (`DEPLOYMENT_MODELS_REFERENCE.md` §BYOC, Control Plane account rule).
  Then confirm **prod or dev**: *prod* → ask for the customer's cloud-account
  details (AWS account ID / GCP project ID + number / Azure subscription +
  tenant ID) **and the end-customer email**; *dev* → ask only for the
  cloud-account details — the subscription defaults to your logged-in user.
  Account onboarding flow + per-cloud bootstrap instructions:
  `DEPLOYMENT_MODELS_REFERENCE.md` §BYOC.
- *Your customers' existing Kubernetes clusters, you do NOT provision infra* →
  **BYOC-K8s** (deploys via a dataplane agent; customer owns the cluster). Uses
  the same `byoaDeployment` block — ask the same Control Plane account question.
- *Fully disconnected / no connectivity back to you* → **air-gapped installer**
  (`onPremDeployment`).

**3. Which clouds and regions?** (AWS / GCP / Azure / OCI / Nebius; regions).
For **air-gapped installer only**, also separate artifact production from the
offline install target: `onPremDeployment` currently uses an AWS
artifact-hosting account (`AwsAccountId` + `AWSBootstrapRoleAccountArn`) to
produce the downloadable installer, while the customer workload target is one of
AWS, GCP, Azure, OCI, Nebius, on-prem Kubernetes, or mixed. The target answer
informs installer requirements, hooks, image/chart access, and the runbook, not
a live Omnistrate deployment region.

**4. Operations needs?** Ask based on the deployment model chosen in Q2:
- **Hosted / BYOC / BYOC-K8s:** ask about managed lifecycle needs — backups,
  stop/start, scaling, upgrades. *Noted for later phases — not implemented up
  front.*
- **Air-gapped:** do **not** ask for live Omnistrate lifecycle operations. Ask
  which installer action hooks are needed. There are four supported hook types:
  `VALIDATE`, `PRE_INSTALL`, `POST_INSTALL`, and `BACKUP`. Use `VALIDATE` for
  install/upgrade preflight checks and compatible prerequisite skips,
  `PRE_INSTALL` for setup that must run before Helm, `POST_INSTALL` only for
  commands that must run after Helm succeeds, and `BACKUP` for pre-upgrade
  backup/export steps. Keep image packaging in Q5; do not present it as an
  operational hook.

**5. Artifact access and install-time registry flow?** Ask based on the
deployment model chosen in Q2:
- **Hosted / BYOC / BYOC-K8s:** ask whether any images, Helm charts,
  Terraform/Kustomize sources, or git repos require private access. This
  determines provider-side auth setup.
- **Air-gapped:** do **not** ask only whether the upstream charts/images are
  public or private. Ask which install-time endpoints the installer will use:
  public Helm/image endpoints, customer-accessible private Helm/image
  registries, or a mix. Keep image packaging separate: `INSTALLER_EMBED`
  controls whether images are packed into the installer; it is not a Helm/image
  install source. Capture target registry paths and split image-sync services
  only when source registry, source repository, or source credentials differ.

**6. Monetization?** Ask based on the deployment model chosen in Q2:
- **Hosted / BYOC / BYOC-K8s:** ask how they charge and who handles payment
  (Stripe / cloud marketplace / Chargebee or other billing system / not billing
  yet). Follow up with **"what do you charge for?"** — the built-in dimensions
  are cpu, memory, storage, replica, deploymentCell. Record now, implement in
  phase 6 — never in the first build.
- **Air-gapped:** skip billing/payment intake unless the user explicitly says
  the installer offering needs commercial packaging. The installer setup itself
  is about offline artifact delivery, install-time registry access, hooks, and
  operator runbooks, not live metering or payment collection.

Billing details, when applicable: `BILLING_METERING_REFERENCE.md`.

If the user cannot cleanly place Q2, map their words to a model with the
ISV-phrasing FAQ in `DEPLOYMENT_MODELS_REFERENCE.md` (e.g. "customers want it in
their own AWS" → BYOC; "they run EKS on-prem but allow egress" → BYOC-K8s;
"defense customer, no internet" → air-gapped).

## Deployment Models at a Glance

Intake Q2 selects one or more of these. Details, `deployment:` blocks, and
account-onboarding flows are all in `DEPLOYMENT_MODELS_REFERENCE.md` — this
table is only for steering the interview.

| Model | Runs in… | Who owns infra | Connectivity | Spec block |
|---|---|---|---|---|
| **Hosted** | your (provider) cloud account | you, via Omnistrate | standard control plane | `hostedDeployment` |
| **BYOC** (Account / BYO-VPC / PrivateLink) | the customer's cloud account | customer owns account, you operate | reverse/encrypted channel; PrivateLink = no public exposure | `byoaDeployment` |
| **BYOC-K8s** | the customer's own Kubernetes cluster | customer owns the cluster; you deploy workloads only | cluster opens **outbound** mTLS/gRPC to your control plane | `byoaDeployment` (deploy `--cloud-provider byoc-onprem`) |
| **Air-gapped** | wherever the customer runs the installer | customer runs and operates | **none** — self-contained artifact, no live link | `onPremDeployment` |

Air-gapped plans have no live Omnistrate lifecycle after delivery. The customer
runs the installer and any operational scripts in the disconnected environment.

BYOC-K8s and air-gapped are the pair most often confused — both are "the
customer's own Kubernetes", but the deciding question is **"can that cluster hold
an outbound connection to your control plane?"** Yes → BYOC-K8s. No → air-gapped.
They share almost no mechanics; `BYOC_K8S_REFERENCE.md` has the full
side-by-side table.

BYO-VPC and PrivateLink are BYOC variants selected at customer-account
onboarding, not separate spec blocks (they live within the BYOC plan). A
service can offer several models, but **each deployment model requires its own
separate Plan** — never combine `hostedDeployment` and `byoaDeployment` in one
plan, and never offer a single plan that serves multiple models. For every
`byoaDeployment` plan the account block carries the AWS **"Control Plane"
account** config irrespective of the customer's cloud — asked explicitly at
intake, never defaulted (`DEPLOYMENT_MODELS_REFERENCE.md` §BYOC).

## Decision Matrix

Pick the row for the user's artifact (intake Q1), then check it against the
deployment model (intake Q2) in the constraint table below. **Every** row also
reads `DEPLOYMENT_MODELS_REFERENCE.md` for the `deployment:` block and account
setup.

| Artifact | Spec format | Build command | Guide |
|---|---|---|---|
| Docker Compose | compose + `x-omnistrate-*` | `omnistrate-ctl build --file <compose-file>` | `COMPOSE_ONBOARDING_REFERENCE.md` |
| Helm chart | ServicePlanSpec (`helmChartConfiguration`) | `omnistrate-ctl build -f spec.yaml --spec-type ServicePlanSpec` | `HELM_ONBOARDING_REFERENCE.md` |
| Terraform / Kustomize | ServicePlanSpec (`terraformConfigurations` / `kustomizeConfiguration`) | same | `TERRAFORM_KUSTOMIZE_REFERENCE.md` |
| Operator (CRDs + controller) | ServicePlanSpec (`systemWorkflows`) | same | → **omnistrate-operator** skill (see Companion skills below) |
| Mixed (e.g. terraform infra + helm app) | ServicePlanSpec, multiple services with `dependsOn` | same | `HELM_ONBOARDING_REFERENCE.md` + `TERRAFORM_KUSTOMIZE_REFERENCE.md` |
| Any artifact, air-gapped target | ServicePlanSpec with `onPremDeployment` | same | `DEPLOYMENT_MODELS_REFERENCE.md` §Air-gapped + `ONPREM_INSTALLER_REFERENCE.md` (installer packages Helm releases; non-Helm stacks must first be bundled into chart(s)) |
| Nothing yet (design first) | — | — | → hand off to **omnistrate-sa** |

ServicePlanSpec builds all share `--spec-type ServicePlanSpec`; the compose path
is the exception (plain `omnistrate-ctl build --file <compose-file>`, no `--spec-type`).
Exact flags and skeletons live in the per-format references — do not reconstruct
them here.

If a Helm or Kustomize application pulls charts/images from the provider's
private Amazon ECR across AWS, GCP, Azure, or connected BYOC-K8s, also read
`APPLICATION_PRIVATE_ECR_REFERENCE.md`. Its namespace-Secret flow is not the
generic Compose/private-registry flow.

### Artifact × deployment-model constraints (check before writing any spec)

Artifact and deployment model are **not** freely combinable. The compose path
does not cover every model:

| Deployment model | Compose spec | ServicePlanSpec |
|---|---|---|
| Hosted | ✅ supported | ✅ supported |
| BYOC-Account / BYO-VPC / PrivateLink | ✅ supported | ✅ supported |
| **BYOC-K8s** (`byoc-onprem`) | ❌ **builds but never deploys** | ✅ **required** |
| **Air-gapped** (`onPremDeployment`) | ❌ not a compose path | ✅ **required** |

> **The compose + BYOC-K8s trap.** Nothing fails early. `omctl docs compose-spec`
> documents `byoaDeployment` as a real compose field, `omctl docs validate`
> passes, `omnistrate-ctl build` succeeds, and the generated plan correctly
> reports `tenancy_type: BYOA` with the full resource graph. `instance create`
> is accepted and returns an instance ID. Then the instance sits in `DEPLOYING`
> **with the instance namespace never created at all** — no pods, no Helm
> release, no error surfaced. Observed for 10+ minutes on a healthy cell whose
> agent was connected and whose account was `READY`.
>
> So schema validation cannot protect you here, and neither can a successful
> build. **If intake Q2 selected BYOC-K8s or air-gapped, the artifact must become
> a ServicePlanSpec — convert a compose file to a Helm chart first.** An empty
> instance namespace on `byoc-onprem` is the signature of this mistake; do not
> debug it as a cluster or agent problem.

## Universal Workflow (method-agnostic)

Same workflow phases for every artifact and model. Per-phase commands are named
generically; copy the exact syntax from the format's reference.

**1. Verify accounts / prerequisites.** Confirm the *provider* cloud account is
READY before anything else: `omnistrate-ctl account list` /
`omnistrate-ctl account describe <account-name>`. Extract account IDs,
bootstrap role ARNs, project IDs for the `deployment:` block. For BYOC and
BYOC-K8s, verify the AWS **Control Plane** account config named at intake is
`READY` — its values are what go into `byoaDeployment`, whatever the customer's
cloud — and explain that *customer* accounts are onboarded later, at deploy
time — see `DEPLOYMENT_MODELS_REFERENCE.md` (§BYOC, §BYOC-K8s) for the customer
`account customer create` flows.

**2. Minimal spec, zero parameterization.** Hardcode everything: no API
parameters, no `$var.*`, no autoscaling. For connected models, start with one
cloud/region, create/delete lifecycle only, and get a working deployment before
adding anything. For air-gapped, start with the smallest installer artifact:
minimal `onPremDeployment`, the smallest Helm/image-sync graph, and no optional
action hooks unless required for install. Build the deployment block from
`DEPLOYMENT_MODELS_REFERENCE.md` for the model(s) chosen in Q2 — **one plan per
model**: if several models were chosen, build and stabilize one plan first,
then author a separate plan per remaining model. The service body comes from
the format's reference.
*Exception (from the operator skill): CR-driven specs are parameter-driven from
day one, but still keep the parameter set minimal.*

**3. Build — then a review pit-stop.** The build must succeed before anything
is added.
- Compose: `omnistrate-ctl build --file <compose-file>`.
- Helm/Terraform/Kustomize/mixed: `omnistrate-ctl build -f spec.yaml --spec-type ServicePlanSpec ...`.
- **Pit-stop (required): review before deploying.** The build output prints
  links to the generated product — surface them from the actual output and
  STOP. Have the user review both sides: (a) the **service/plan page**
  (provider side) to sanity-check the generated architecture — resources,
  parameters, endpoints; and (b) the **Customer Portal** ("Access SaaS
  Product") to preview the exact UX their customers will get, including the
  exposed parameters. (`--interactive` builds prompt for Customer Portal
  access directly.) Proceed only after the user confirms, or adjust the spec
  and rebuild.

**4. Deploy one instance or produce the installer artifact.**

For connected models, `instance create` targeting the main resource, then
`instance describe` until RUNNING. For BYOC targets the customer account must be
onboarded and `READY` first — see `DEPLOYMENT_MODELS_REFERENCE.md` §BYOC — then
deploy with `--customer-account-id`. Expect **2–3 iterations** — do not stop at
the first failure. Debug loop, in escalating order:
   1. `omnistrate-ctl instance describe <id> --deployment-status --output json`
      — find the failing resource.
   2. `omnistrate-ctl workflow list --instance-id <id>` then
      `omnistrate-ctl workflow events <workflow-id>` — locate the failed step;
      add `--resource-key` / `--detail` only for that step.
   3. `omnistrate-ctl instance debug <id>` — rendered helm values / terraform
      apply logs / operator CR status (kustomize has no rendered-artifact view:
      use workflow events + the tunnel).
   4. `omnistrate-ctl deployment-cell update-kubeconfig <cell-id> --kubeconfig
      /tmp/kc` + `kubectl logs` / `kubectl get` — live pod state. Never use
      aws/gcloud/az CLIs for cluster access; only the Omnistrate tunnel.
The **omnistrate-sre** skill, if installed, extends this loop with
per-resource-type and per-model failure catalogs.

For air-gapped targets, do not wait for a RUNNING workload through the control
plane. Create the installer instance, wait for installer readiness, download
the artifact, and use `ONPREM_INSTALLER_REFERENCE.md` for installer action hooks
and customer-run diagnostics.

**5. Customization discovery & parameterization.** Once the zero-param instance
is RUNNING for connected models, or the minimal installer artifact is produced
for air-gapped, **proactively inspect** the artifact to recommend a
customer-facing parameter set — do not wait to be asked. For Helm, run
`helm show values` / `helm show readme` (or Artifact Hub); for terraform, read
`variables.tf`; for compose, inspect env vars/images. Classify every relevant
value into three tiers (**Tier 1** recommended customer-facing →
`apiParameters`; **Tier 2** optional/advanced → default to hardcoded; **Tier 3**
platform/ISV-owned → never expose), **present the tier table for approval**, and
also surface external dependencies: when a chart bundles a dependency with a
working default, *suggest* (never force) replacing it with a terraform-managed
RDS/ElastiCache/S3. Then implement approved Tier-1 parameters **one at a time**
— rebuild + redeploy after *each* change for connected models, or rebuild the
installer artifact after *each* change for air-gapped, never batch. See
`HELM_ONBOARDING_REFERENCE.md` §"Customization discovery" and §"External
dependencies", and `TERRAFORM_KUSTOMIZE_REFERENCE.md` §"Managed-service modules".

**6. Production hardening.** Split a prod Plan (accounts differ; spec otherwise
identical), add additional clouds, and additional deployment models (one plan
per model). For air-gapped targets the deliverable is the installer artifact
rather than a running instance — see `DEPLOYMENT_MODELS_REFERENCE.md`
§Air-gapped.
**Billing/metering lands here, not earlier** — and only when monetization was
requested. Implement the path chosen in intake Q6: `pricing` +
`billingProviders` for end-to-end Stripe billing, or the `metering` export (+
your exporter) for marketplaces / non-Stripe providers / custom dimensions. For
`CUSTOM_TENANCY` plans (Helm, operator, Kustomize) the
`omnistrate.com/include-customer-billing: "true"` **pod label** is required or
usage silently bills zero. For air-gapped installer setup, skip billing/metering
unless commercial packaging was explicitly requested. See
`BILLING_METERING_REFERENCE.md`.

**7. Distribute & document.** Release the Plan
(`omnistrate-ctl build ... --release-as-preferred --release-description "..."`),
make the **prod environment Public**, configure the **Customer Portal** (custom
domain via CNAME, SMTP sender email, SSO identity providers), and optionally add
billing. **THEN generate the artifact pair** — `DEPLOYMENT_OVERVIEW.md` +
`deployment-overview.svg` — next to the ISV's spec files. The SVG is produced by
copying the base template `assets/omnistrate-architecture-base.svg` and applying
per-model, id-keyed edits (retitle the boundary, un-hide/label workloads and
managed services, fill customer parameters); the `.md` embeds it. Onboarding is
**not complete** until that pair is generated and the portal path is confirmed
(or, for air-gapped, the installer is delivered). See `DISTRIBUTION_REFERENCE.md`.

## Critical Rules

1. **Never write spec YAML, field names, or CLI flags from memory.** Copy from
   the reference files' verified fragments, or verify with `omctl docs
   compose-spec "<tag>"` / `omctl docs plan-spec "<section>"` for the reference
   and `omctl docs json-schema <type>` for the authoritative schema. Run one of
   these before every extension or field you add. (The MCP docs-search tools
   `mcp__ctl__docs_*` are an optional alternative only on user request.)
2. **Zero-parameterization first** (compose / helm / terraform / kustomize).
   Hardcode everything, get to RUNNING for connected models or produce the
   installer artifact for air-gapped, then parameterize. *Operator-CR exception:*
   CR specs are parameter-driven from day one, set kept minimal.
3. **One change per build-deploy cycle.** Add one parameter or capability, then
   rebuild and redeploy for connected models, or rebuild the installer artifact
   for air-gapped, before the next change.
4. **`defaultValue` is always a quoted string** — even for numeric types.
5. **Never modify the user's original artifact.** Create Omnistrate variants
   (e.g. `-omnistrate.yaml`, a `spec.yaml`) — leave the source untouched.
6. **The deployment model comes from intake Q2 — never silently default.** The
   old "ALWAYS use `hostedDeployment`" rule is gone. Ask Q2, then build the
   `deployment:` block from `DEPLOYMENT_MODELS_REFERENCE.md`.
7. **Field casing is lowerCamel in both compose and ServicePlanSpec.** The platform
   matches field names case-insensitively, so older specs using `AwsAccountId` still
   build, but write lowerCamel (`awsAccountId`, `awsBootstrapRoleAccountArn`) so the
   schema pin and `docs validate` both pass. The exceptions are documented UpperCamel:
   `OsFamily`, `GpuClusterID`, and `CustomDNSConfig`'s `TargetKubernetesService` /
   `TargetName` / `TargetPort`.

## Red Flags — STOP

| Thought | Reality |
|---|---|
| "I declared `endpointConfiguration` / `loadBalancers.https`, so the Helm endpoint is exposed." | Neither creates DNS or routing for chart-created Services. The chart must create an Ingress (TLS via the per-instance `google-public-ca-tls` secret) or a LoadBalancer Service with the `hostname` annotation. Otherwise endpoints stay UNHEALTHY and the instance hangs in `DEPLOYING`. Each endpoint gets its own one-label host. See `HELM_ONBOARDING_REFERENCE.md` → "Exposing endpoints" → "Read this first". |
| "Helm / Terraform / Kustomize isn't supported by this skill." | It is. Use `HELM_ONBOARDING_REFERENCE.md` / `TERRAFORM_KUSTOMIZE_REFERENCE.md`. |
| "This is an operator, I'll write the workflows here." | Hand off to **omnistrate-operator** — it owns `systemWorkflows`. |
| "I'll default to `hostedDeployment`." | Ask intake Q2 first. The model is a decision, not a default. |
| "The user has a compose file and wants BYOC-K8s / air-gapped — the model is orthogonal to the artifact." | It is not. Compose covers hosted and BYOC-*Account* only. BYOC-K8s and air-gapped are ServicePlanSpec-only; convert to a Helm chart first. See §Artifact × deployment-model constraints. |
| "`docs validate` passed and the build succeeded, so the compose spec is fine for BYOC-K8s." | Both pass and it still never deploys — the instance namespace is never created, with no error. Validation cannot catch this. |
| "`instanceTypes` is one entry per cloud provider, so a resource gets one node group." | Compose only. In a **ServicePlanSpec** every entry requests its own node group, same-cloud duplicates included — that is the supported way to back one workload with several machine sizes. Azure pool creation also checks zone placement policy. Never invent a second resource or a shared custom label to get a second node group. See `HELM_ONBOARDING_REFERENCE.md` §Compute: instance types and node groups. |
| "`bestEffort` allows a multi-zone Resource to use one AZ or moves a custom-AZ Resource to another AZ." | It skips unavailable Azure pools per instance type. Multi-zone still needs at least two eligible AZs; custom placement stays in the requested AZ. Read [zonePlacementPolicy](HELM_ONBOARDING_REFERENCE.md#zoneplacementpolicy) when configuring Azure instance types with limited AZ availability. |
| "Pods need custom affinity to reach a resource's second node group." | They don't. Injected affinity keys on `omnistrate.com/resource` — per-*resource*, carried by all its node groups. Don't set `enableInjection: false` to defeat a pin that isn't there; add a `preferred` term if you want to bias placement. |
| "I remember the field name / that ctl flag exists." | Grep the reference files; confirm fields with `omctl docs compose-spec "<tag>"` or `omctl docs json-schema <type>`, and flags with `--help`. |
| "The build rejected an extension I'm sure exists." | Run `omctl docs compose-spec` and match the exact spelling — the platform's error text points there for a reason. |
| "Air-gapped needs an always-on agent phoning home." | No. Air-gapped is a self-contained *installer* artifact — no live control-plane link (`onPremDeployment`). |
| "For air-gapped, I'll ask about stop/start or restore lifecycle." | Don't. Ask which supported action hooks are needed: `VALIDATE`, `PRE_INSTALL`, `POST_INSTALL`, and `BACKUP`. Keep image packaging and registry flow separate. |
| "For air-gapped, I'll ask whether the upstream charts/images are public or private." | Ask which install-time endpoints are used: public Helm/image endpoints, customer private registries/repos, or both. `INSTALLER_EMBED` is image packaging, not an install source. |
| "For air-gapped, I'll ask who handles payment." | Skip billing/payment unless the user explicitly requests commercial packaging for the installer. |
| "BYOC-K8s will provision the customer's nodes." | It won't. The customer owns the cluster and infra; Omnistrate only deploys workloads via the dataplane agent. |
| "I'll add all the parameters, then build once." | One change per build-deploy cycle. Batching hides which change broke it. |
| "I'll add a custom pricing dimension / a `marketplace:` block to the spec." | Neither exists. Only cpu/memory/storage/replica/deploymentCell are billable dimensions; everything else is the metering-export path (`BILLING_METERING_REFERENCE.md`). |
| "A private-ECR application is RUNNING, so registry access is proven." | `RUNNING` alone is insufficient. Check the actual Pod digest and pull-Secret mode, then force a controlled replacement Pod. Do not assume replica count creates a fresh node. See `APPLICATION_PRIVATE_ECR_REFERENCE.md`. |
| "Omnistrate creates the ECR Secret, so it will attach it to every Pod or ServiceAccount." | It will not. Helm hooks and workload Pods must explicitly reference `$sys.deployment.imagePullSecretName`; Kustomize files use `{{ $sys.deployment.imagePullSecretName }}`. This minted path is the application default across AWS, GCP, Azure, and connected BYOC-K8s; do not expose an auth-mode choice to customers. |
| "Billing is set up, so a CUSTOM_TENANCY Helm/operator plan will bill correctly." | Not without the `omnistrate.com/include-customer-billing: "true"` pod label — otherwise it silently bills zero. |
| "I'll parameterize before the first deploy." | Zero-parameterization first (operator-CR excepted). Get to RUNNING for connected models or produce the installer artifact for air-gapped, then parameterize. |

## Reference Files

- **`COMPOSE_ONBOARDING_REFERENCE.md`** — Docker Compose path: `x-omnistrate-*`
  transformation, single vs multi-service (synthetic `noop` root), API
  parameters, compute/storage, load balancers, action hooks, build/debug.
- **`HELM_ONBOARDING_REFERENCE.md`** — Helm ServicePlanSpec:
  `helmChartConfiguration`, `runtimeConfiguration`, values templating, pod
  placement/affinity, multi-service `dependsOn`, endpoints, lifecycle. Includes
  [zonePlacementPolicy](HELM_ONBOARDING_REFERENCE.md#zoneplacementpolicy) for Azure
  Resource AZ selection and per-type pool creation; read it for limited-AZ GPU
  types or mixed instance-type policies.
- **`TERRAFORM_KUSTOMIZE_REFERENCE.md`** — Terraform (`terraformConfigurations`,
  git/local sources, execution identity, state, outputs) and Kustomize
  (`kustomizeConfiguration`, templating, workload affinity), plus combined
  terraform + helm/kustomize patterns.
- **`APPLICATION_PRIVATE_ECR_REFERENCE.md`** — provider private Amazon ECR for
  connected application charts/images across AWS, GCP, Azure, and BYOC-K8s:
  minted namespace credentials, cloud-scoped Helm values, Kustomize overlay
  selection, registry scope, and runtime validation without false fresh-node
  assumptions.
- **`DEPLOYMENT_MODELS_REFERENCE.md`** — the orthogonal `deployment:` block and
  operational flows for hosted / BYOC (BYO-VPC, PrivateLink) / BYOC-K8s /
  air-gapped, plus customer-account onboarding, tenancy, and the ISV-phrasing
  FAQ. Read this for **every** onboarding path.
- **`BYOC_K8S_REFERENCE.md`** — BYOC-K8s depth. **ServicePlanSpec-only: a compose
  spec builds but never deploys on `byoc-onprem`.** Covers **TLS** (the cell
  auto-provisions a publicly-trusted per-instance certificate — public HTTPS is
  one `tls:` block), **rollouts on small clusters** (the single-replica
  `maxSurge`/`maxUnavailable` deadlock), the trust/egress model and the
  customer allowlist, target-cluster prerequisites, the `account customer create
  --cluster-name` install-kit onboarding flow, `--cloud-provider byoc-onprem
  --region on-prem`, endpoints without a cloud LB, storage, native logs,
  operators on customer clusters, day-2 ops, adopted deployment cells, the
  canonical **BYOC-K8s vs air-gapped** disambiguation table, and **trimming the
  amenity footprint** via a `--cloud byoc-onprem` deployment-cell template
  (BYOC-K8s cells only, without touching other clouds) — start with all amenities
  `disable: "true"` and no endpoints in the spec, then add them on request.
- **`ONPREM_INSTALLER_REFERENCE.md`** — air-gapped/on-prem installer setup for
  complex Helm graphs: multiple Helm releases, multiple image registry copy
  services, `INSTALLER_EMBED`, `autoDiscoverImagesTag`, action hooks,
  `parameterDependencyMap`, runtime skips with `skip_resource_deployment`, and
  download/install runbooks.
- **`BILLING_METERING_REFERENCE.md`** — FinOps: choosing end-to-end Stripe
  billing vs custom metering export, `pricing` dimensions, `billingProviders`,
  paywall/quota/invoices, the `metering` bucket export (policy, path layout,
  record schema, `last_success_export.json`, `externalPayerId`), custom
  dimensions + exporter patterns (Clazar recipe), marketplaces, the
  CUSTOM_TENANCY billing pod label, and `omnistrate-ctl cost` insights
  (workflow phase 6).
- **`DISTRIBUTION_REFERENCE.md`** — release states + `--release` /
  `--release-as-preferred` / `--release-description`, prod env visibility, the
  Customer Portal (domain/SMTP/SSO), subscriptions, optional pricing/billing, the
  ordered go-live checklist, per-model customer experience, and the
  `DEPLOYMENT_OVERVIEW.md` + `deployment-overview.svg` artifact pair — the SVG
  edit recipe over the base template in `assets/` (workflow phase 7).
Companion skills — separate installs; this skill is fully usable without them:

- **omnistrate-operator** — CRD + controller onboarding (`systemWorkflows`,
  lifecycle verbs); covers the operator row of the decision matrix. Without it,
  start from the public template:
  https://github.com/omnistrate-community/operator-spec-template.
- **omnistrate-sre** — extends the phase-4 debug loop with per-resource-type
  and per-model failure catalogs.

## Success Criteria

- Build succeeds with the chosen spec format.
- Instance reaches **RUNNING** with all resources healthy — **or**, for
  air-gapped targets, the installer artifact is produced.
- Started with zero parameterization (operator-CR excepted) and completed at
  least one deploy-debug-fix cycle for connected models — or produced the
  minimal installer artifact for air-gapped.
- Every lifecycle/parameter addition validated by a rebuild + redeploy for
  connected models; every air-gapped installer action hook or parameter addition
  represented in the spec and validated by rebuild.
- The deployment model(s) match what the user chose in intake Q2.
- Recommended customization tiers were reviewed with the user (tier table
  presented; approved Tier-1 parameters implemented one per build-deploy cycle).
- The Plan is **released** and the **portal is reachable** (prod env public,
  domain/SMTP/SSO configured) — **or**, for air-gapped, the installer is delivered.
- The **`DEPLOYMENT_OVERVIEW.md`** + **`deployment-overview.svg`** artifact pair
  was generated (the SVG derived from `assets/omnistrate-architecture-base.svg`)
  next to the ISV's spec files.
- Every shipped spec fragment is traceable to a reference, sample, or the docs —
  nothing written from memory.
