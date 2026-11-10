---
name: omnistrate-operator
description: Use when onboarding a Kubernetes operator-based service (CRDs + controller, e.g. CloudNativePG, Strimzi, KubeAI, ECK) onto the Omnistrate platform; when writing or reviewing an Omnistrate ServicePlanSpec with systemWorkflows; or when an operator/Helm+CR deployment must become a managed SaaS offering with create/modify/stop/backup/restore lifecycle. For Docker-Compose services use omnistrate-fde; for debugging failed instances use omnistrate-sre.
---

# Onboarding Kubernetes Operators to Omnistrate

All commands use the `omnistrate-ctl` CLI (alias `omctl`) — install and authenticate with `omnistrate-ctl login` first. An Omnistrate MCP server exposes equivalent tools (`mcp__ctl__*`); use those only if the user explicitly asks to work through MCP.

## Overview

An operator integration is a **ServicePlanSpec** (NOT a Docker-Compose spec — no
`x-omnistrate-*` tags). Omnistrate owns the substrate: node pools, per-instance
namespace, storage, load balancers, TLS, DNS. The operator owns the application.
The spec's job is to map Omnistrate lifecycle verbs (create, modify, stop,
delete, backup, restore, ...) onto Kubernetes custom-resource manipulations,
expressed as Argo-workflow DAGs under `systemWorkflows`.

**Core principle: never write spec YAML from memory.** Untrained-knowledge
Omnistrate specs are reliably wrong in structure, field names, and variable
syntax while looking plausible. Every block you write must be copied from a
known-good example (see Canonical Examples) or verified with `omctl docs` (below).

### Verifying spec fields against the platform

An operator integration is a ServicePlanSpec, so `plan-spec` and the
`service-plan` schema are your references — **not** `compose-spec`. These
subcommands need no `omnistrate-ctl login`, though they do make network calls.

| Need | Command |
|---|---|
| Every ServicePlanSpec section | `omctl docs plan-spec` |
| The operator CRD section | `omctl docs plan-spec "operator crd"` |
| Helm chart config for the operator deployment | `omctl docs plan-spec "helm chart configuration"` |
| The authoritative ServicePlanSpec schema | `omctl docs json-schema service-plan` |
| `$sys.*` system parameters | `omctl docs system-parameters` |
| Full-text search across all guides | `omctl docs search "systemWorkflows" --limit 15` |
| **Check the finished spec** | `omctl docs validate --file spec.yaml` |

`systemWorkflows`, `customWorkflows`, `successCondition` and `outputParameters`
have no `plan-spec` heading of their own — they are defined in the
`service-plan` schema. Pull it and read the definitions directly. **Start with the
`$ref` + key list**: `$defs` names are not spec key names (the root is
`CustomServicePlanSpec`, `services[]` is `ResourceConfiguration`), so without this
first step you will not know which definition to open.

```bash
# 1. discover the root definition and the full $defs index — always do this first
omctl docs json-schema service-plan -o json | jq -r '.["$ref"], (.["$defs"]|keys[])'

# 2. the workflow container: this is where you learn the Argo body nests under
#    `workflow:` and that `outputParameters` is a sibling MAP, not a list
omctl docs json-schema service-plan -o json | jq '.["$defs"].CreateWorkflowConfiguration, .["$defs"].CustomWorkflowConfiguration'

# 3. the verb keys (additionalProperties:false, so this list is exhaustive)
omctl docs json-schema service-plan -o json | jq '.["$defs"].SystemWorkflowsConfiguration'

# 4. the DAG itself
omctl docs json-schema service-plan -o json | jq '.["$defs"].WorkflowSpec, .["$defs"].Template, .["$defs"].DAGTemplate, .["$defs"].DAGTask, .["$defs"].Arguments'

# 5. the CR config and the apply task
omctl docs json-schema service-plan -o json | jq '.["$defs"].OperatorCRDConfiguration, .["$defs"].ResourceTemplate'

# 6. which parent uses a definition? (disambiguates look-alike defs such as
#    WorkflowOutputParameterSpec vs systemWorkflows.outputParameters)
omctl docs json-schema service-plan -o json | jq -r --arg d WorkflowOutputParameterSpec \
  '[paths(scalars) as $p | select(getpath($p)=="#/$defs/"+$d) | ($p|map(tostring)|join("."))][]'
```

**The Argo body goes under `create.workflow:`, not directly under `create:`.**
`CreateWorkflowConfiguration` allows only `{outputParameters, workflow, workflowFile}`.
Reading `WorkflowSpec` alone will mislead you into putting `entrypoint`/`templates`
one level too high — this is the single most common structural mistake here.

**`docs system-parameters` does NOT cover workflow-context variables.** Its root
has only `backup`, `compute`, `deployment`, `deploymentCell`, `id`, `network`,
`storage`, `tenant`, `deterministicSeedValue`. `$sys.namespace`, `$sys.instanceId`,
`$sys.restore.*`, `$sys.sourceInstanceId` and `$sys.targetInstanceId` are **real but
absent from it** — they are used throughout the platform's own operator examples.
Never remove one because `system-parameters` omits it. For those, use
`omctl docs search "Backup and Restore Workflow Context" --limit 15`.

**Start every operator session with `omctl docs search "Kubernetes Operators" --limit 10`** —
it returns the whole operator build guide: the lifecycle-verb table, a complete
create-workflow example, the minimal plan shape, and the backup/restore context.
Nothing else in the toolset gives you a copyable end-to-end workflow.

Also note: no `enum` is emitted anywhere in the schema, so api-param `type:` values
and `cloudProvider` values must come from the prose
(`omctl docs search "parameter types" --limit 15`), and a wrong value will pass
schema validation silently.

A tag that matches nothing prints the available-tag list and warns on stderr —
read that as "wrong name, pick from this list". The MCP docs-search tools
(`mcp__ctl__docs_*`) are an optional alternative only on user request.

## When to Use

- "Integrate operator X with Omnistrate" / "offer X as managed SaaS" where X is
  operator-managed (CNPG, Strimzi, ECK, KubeAI, RabbitMQ operator, ...)
- Writing/extending a ServicePlanSpec: `systemWorkflows`, `customWorkflows`,
  `operatorCRDConfiguration`, `helmChartConfiguration`
- Adding lifecycle verbs (stop/start, backup/restore, failover) to an existing
  operator-backed plan

**Not this skill:** compose/helm/terraform/kustomize onboarding → `omnistrate-fde` (the universal onboarding router); architecture
design from scratch → `omnistrate-sa`; deployed-instance failure debugging →
`omnistrate-sre`.

## Decision Guide (answer these before writing YAML)

**1. How do the operator and its CRDs install?**

CRDs are cluster-scoped Kubernetes objects. Regardless of how the operator
itself is scoped, CRDs install once per deployment cell via a custom amenity —
never owned by a per-instance chart (the second instance would conflict).

| Operator scoping | Pattern |
|---|---|
| Cluster-scoped (one controller serves all namespaces, e.g. CNPG) | Deployment-cell amenity: the full operator chart as a `customAmenities` entry (`type: Helm`) applied via `omnistrate-ctl deployment-cell` config — operator and CRDs install once per cell |
| Namespace-scoped (controller watches only its own namespace, e.g. KubeAI) | **Hybrid:** CRDs via a deployment-cell amenity (`type: KubernetesManifest`, or a crds-only Helm amenity); the operator itself as a sibling service with `helmChartConfiguration` (chart `crds.enabled=false`) that the CR service `dependsOn` — chart installs per instance |

**Deprecated:** installing operator charts via
`operatorCRDConfiguration.helmChartDependencies`. Do not add chart entries
there in new specs — keep `helmChartDependencies: []` purely as the marker
that declares the service an operator-CRD resource. Older specs (including
Omnistrate's public operator spec template) still carry chart entries; copy
their workflow anatomy, not their install method.

**2. Can readiness be gated on the CR's status?**

- CR has reliable status fields (phase/conditions/readyReplicas) →
  `successCondition`/`failureCondition` on the apply task, and workflow-level
  `outputParameters` reading `$tasks.<task>.resource.status.*`.
- Nothing waitable (e.g. scale-to-zero autoscaling: 0 replicas at create) → NO
  `successCondition`, and therefore **NO `outputParameters` at all** —
  referencing `$tasks.X.resource.*` without a successCondition fails the
  workflow render. Surface state via live CR reads instead.

**3. How does traffic reach it?**

- TCP protocol (databases) → `loadBalancers.tcp` + a tiny internal proxy
  service (socat) that bridges LB ports to the operator's Services
- HTTP → `loadBalancers.https` with `targetKubernetesServiceName` **pinned to
  the chart/operator-created Service name** — omit it and Omnistrate
  synthesizes a backend from the resource key, which never exists
- Stable client endpoints (writer/reader) → `endpointConfiguration`
- **Neither `endpointConfiguration` nor `loadBalancers.*` creates DNS for
  chart/operator-created Services.** Something in the cluster has to produce a
  record: an Ingress host, a `type: LoadBalancer` Service with the `hostname`
  annotation, or `internal-hostname` on a ClusterIP Service. Otherwise
  endpoints stay UNHEALTHY and the instance hangs in `DEPLOYING` with all pods
  Running. Give each endpoint its own host, one label deep under
  `instance-<id>`, to match the per-instance wildcard cert. See the FDE skill's
  `HELM_ONBOARDING_REFERENCE.md` → "Exposing endpoints" → "Read this first".

## Workflow

**Phase 0 — Gather facts.** CRD group/version/kind; the status fields the
operator actually writes (get a live CR or read its API reference); Helm chart
coordinates; operator scoping (question 1 above); the operator-native
quiesce mechanism for stop/start (e.g. CNPG `cnpg.io/hibernation` annotation);
verify cloud accounts (`omnistrate-ctl account list` / `omnistrate-ctl account describe <account-name>`).

**Phase 1 — Minimal spec.** Header (`name`, `tenancyType: CUSTOM_TENANCY`,
`deployment.hostedDeployment` with real account values — field casing matters:
`awsBootstrapRoleAccountArn`; a BYOC offering is a **separate plan/spec** with
a `byoaDeployment` block instead — one plan per deployment model, never
`hostedDeployment` and `byoaDeployment` together in one plan. The
`byoaDeployment` values are the AWS account designated as the **"Control
Plane" account** — ask the user which account that is; it is an AWS account
config irrespective of the customer's cloud), one CR service, operator install per decision 1,
`systemWorkflows` with **create and delete only**. Declare only the API
parameters the CR manifest genuinely needs — unlike compose onboarding, the CR
is parameter-driven from day one, but keep the set minimal and hardcode
everything else. Single cloud provider.

**Phase 2 — Build, deploy, debug until RUNNING.**
```bash
omnistrate-ctl build -f spec.yaml --spec-type ServicePlanSpec \
  --product-name "<name>" --environment Dev --environment-type Dev \
  --release-as-preferred
omnistrate-ctl instance create --service "<name>" --plan "<plan>" \
  --environment Dev --cloud-provider aws --region <region> \
  --resource <crResourceKey> --param '<json>' --output json
omnistrate-ctl instance describe <instance-id> --output json
```
Iterate build → deploy → fix; expect 2-3 cycles. For failures: `instance
describe <id> --deployment-status`, then `workflow list` / `workflow events`
for the failed step, then live CR/pod state via `deployment-cell
update-kubeconfig` + kubectl (never cloud-provider CLIs for cluster access).
The `omnistrate-sre` skill, if installed, provides the full systematic
debugging workflow.

**Phase 3 — Add lifecycle verbs one at a time**, re-building and re-deploying
after each: `modify` (re-apply CR with new `$var` values), `stop`/`start`
(operator-native quiesce via `action: patch`),
`backup`/`restore`/`deleteBackup` (+ `capabilities.backupConfiguration`),
`failover`, then provider-defined `customWorkflows`. Syntax for each verb and
its context variables: see the reference.

**Phase 4 — Networking and endpoints** per decision 3.

**Phase 5 — Production.** Split dev/prod twin specs that differ ONLY in
`deployment` accounts and the metering bucket (state this in a header comment
and keep them in sync); add `metering`, `billingProviders`, per-cloud
`instanceTypes` via `apiParam`, node-affinity pinning to Omnistrate-managed
nodes, billing if the ISV monetizes (`pricing` + `billingProviders` for Stripe,
or the `metering` export for marketplaces / non-Stripe / custom dimensions —
**plus the `omnistrate.com/include-customer-billing: "true"` pod label, required
on `CUSTOM_TENANCY`**; see the FDE skill's `BILLING_METERING_REFERENCE.md`),
BYOA variants if offered (a **separate BYOC plan/spec** — one plan per
deployment model — whose `byoaDeployment` carries the AWS **"Control Plane"
account** values; ask the user which AWS account config is designated
Control Plane; required irrespective of the customer's cloud; onboard each
customer account with `omnistrate-ctl account customer create`,
then deploy instances with `--customer-account-id`).

> **Targeting a customer-managed cluster (BYOC-K8s, `--cloud-provider byoc-onprem`)?**
> Four assumptions break: CRD install is a cluster-scoped change on infrastructure
> you don't own; the customer may already run the same operator; there is no cloud
> load balancer and no cloud StorageClass; and operator backups need a
> customer-supplied object store. Read **§11** of
> `OPERATOR_ONBOARDING_REFERENCE.md` before designing the install path, and the
> FDE skill's `BYOC_K8S_REFERENCE.md` for the deployment model itself.

## Critical Rules

1. **`systemWorkflows` is the lifecycle mechanism.** `template`,
   `supplementalFiles`, `readinessConditions`, `outputParameters` directly
   under `operatorCRDConfiguration` are DEPRECATED — do not use them, do not
   invent JSONPath readiness polling. Readiness lives in `successCondition`;
   outputs live in workflow-level `outputParameters`.
2. **Stop/start/delete do nothing you didn't author.** There is no platform
   magic that scales down an operator's CR — write the workflow (delete = CR +
   secrets teardown; stop = the operator's own hibernation/pause mechanism).
3. **One Kubernetes resource per workflow template.** Argo
   `resource: action: apply` applies only the FIRST document of a multi-doc
   manifest (confirmed live — the rest silently vanish). N resources = N
   templates = N dag tasks.
4. **No successCondition ⇒ no outputParameters.** The task captures no live
   resource object, so any `$tasks.X.resource.*` reference fails the render.
5. **Declare every parameter on the resource that `instance create` targets.**
   A param declared only on a dependency service is silently dropped at create.
   Same key on two services = one shared instance value.
6. **The param that names the CR (`metadata.name`) must be
   `modifiable: false`** — otherwise modify re-applies under a new name and
   orphans the old CR. Prefer `{{ $sys.instanceId }}` as the CR name.
7. **`defaultValue` is always a quoted string**, even for Float64. **Never
   name a parameter `replicaCount`:** the platform overrides a parameter with
   that key during `start` (observed rendering as 1), so a start re-creates a
   1-member cluster. Use a product-specific key (`memberCount`, `brokerCount`).
8. **Only documented variables exist**: `$sys.*`, `$var.*`, `$func.*` — the
   real vocabulary is tabled in the reference (`$sys.instanceId`,
   `$sys.namespace`, `$sys.deploymentCell.region`, ...). `$sys.id` does not
   exist. Concatenation requires `{{ }}`.
9. **Thread every template input explicitly.** Workflow `arguments.parameters`
   → entrypoint template `inputs` → dag task `arguments` → leaf template
   `inputs`. Verbose, but any skipped hop renders empty.
10. **Optional nested YAML in a CR** (args lists, env maps, nodeSelector):
    inject as a pre-composed, pre-indented block parameter that collapses when
    empty — Argo templating has no conditionals.
11. **Operator-created pods do NOT inherit Omnistrate placement.** Omnistrate
    schedules only the containers it creates itself. Every pod template the
    operator stamps out from your CR must carry node affinity pinning it to
    the instance's Omnistrate-managed node group (`omnistrate.com/managed-by`,
    region, instance type, `omnistrate.com/resource` — exact block in
    reference §8), or pods land on system/shared nodes or fail to schedule.
    GPU node groups additionally need the extended-resource request and the
    `nvidia.com/gpu` taint toleration. Cells mix arm64 and amd64 nodes:
    single-arch operator images without placement fail with `no match for
    platform in manifest` — verify the operator's CRD actually forwards a
    placement field BEFORE onboarding (some operators have none; that's a
    vendor gap, see reference §8).

## Red Flags — STOP, you are hallucinating

| Thought | Reality |
|---|---|
| "I know the Omnistrate spec schema from training" | You know a plausible-looking wrong one. Copy from a canonical example. |
| "readinessConditions will gate RUNNING" | Deprecated. Use `successCondition` on the apply task. |
| "Stop will just scale the workload down" | Only if you author a stop workflow using the operator's quiesce mechanism. |
| "I'll put all the manifests in one apply task" | Only the first doc applies. Split them. |
| "Outputs are templated strings on the resource" | Outputs are workflow `outputParameters` from `$tasks.*.resource.status.*`, gated on successCondition. |
| "The operator's pods will schedule fine by default" | Omnistrate places only containers it creates. Pin operator-created pods to the managed node group via CR affinity (reference §8). |
| "I'll install the operator via helmChartDependencies" | Deprecated. Cluster-scoped → cell amenity; namespace-scoped → hybrid (amenity CRDs + sibling service). |
| "This ctl flag probably exists" | Verify with `--help` before using it; verify spec fields with `omctl docs json-schema service-plan`. |
| "I know the plan-spec section name for systemWorkflows" | There isn't one. Read `$defs.SystemWorkflowsConfiguration` out of `omctl docs json-schema service-plan`. |

## Canonical Examples & Reference

Full syntax — spec skeleton, operator/CRD install patterns, every lifecycle
verb with context variables, apiParameters, system-variable table, networking,
node placement/affinity, troubleshooting: **OPERATOR_ONBOARDING_REFERENCE.md**
(this directory). The reference embeds complete, copyable blocks distilled
from working production specs (CNPG/postgres, KubeAI/vLLM) — start from those.

Public sources to verify against:
- Omnistrate operator spec template —
  https://github.com/omnistrate-community/operator-spec-template — a full
  CNPG lifecycle example (create/modify/start/stop/addCapacity/removeCapacity/
  delete/backup/restore/deleteBackup/failover + customWorkflows). NOTE: it
  still installs CNPG via the deprecated `helmChartDependencies`; copy its
  workflow anatomy, not its install method.
- The live ServicePlanSpec schema and reference, straight from the platform:
  `omctl docs json-schema service-plan`, `omctl docs plan-spec "<section>"`,
  `omctl docs search "<query>"` (see "Verifying spec fields" above). Prefer these
  over the docs site — no login needed, and they are never stale.
  The MCP docs-search tools (`mcp__ctl__docs_*`) are an optional alternative only
  when the user has asked to work through MCP.

## Success Criteria

- Build succeeds; instance reaches RUNNING with the CR reconciled by the
  operator (verify via live CR status, not just instance status)
- Every declared lifecycle verb exercised at least once against a live
  instance (modify, stop→start, delete leaves nothing orphaned in the
  namespace)
- For data services, **data verified around every verb**, not just instance
  status: load a known dataset and record its checksum, run an external writer
  that logs every client-acknowledged write, and after each operation re-read
  the dataset (checksum unchanged) and check that every acknowledged write is
  present. Verbs that legitimately lose data (e.g. backup-then-release stop)
  must have that window measured and documented.
- Anything exposed to the internet is **port-scanned from outside** after
  create: only the intended ports answer (repeat each probe several times —
  a leak through some nodes answers only part of the time)
- Dev and prod specs differ only in accounts + metering bucket
