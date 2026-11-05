---
name: dd-agent-install-kubernetes
description: Install the Datadog Agent on a Kubernetes cluster - Amazon EKS (standard or Fargate profiles), Azure AKS, Google GKE (standard or Autopilot), OpenShift, Oracle OKE, VMware Tanzu (TKG), Rancher (RKE2/K3s), or self-managed - through the Datadog Operator (kubectl/Helm), the Datadog Helm chart, or Terraform, with metrics, logs, and APM trace intake on by default, Single Step Instrumentation off unless the user asks, and optional products; for an SSI-first install use `dd-apm/k8s-ssi` `agent-install`. Use when the user is running a Kubernetes cluster on GKE, EKS, AKS, OpenShift, OKE, or TKG, asks to install or set up the Datadog Agent on Kubernetes, wants to install the Agent with Terraform, or wants to monitor their Kubernetes pods. Does not connect a cloud provider integration or install the Agent on standalone hosts or plain Docker. Requires a Datadog account with a valid API key and application key; run `dd-account-setup` first if they are missing.
metadata:
  version: "1.0.0"
  author: datadog-labs
  repository: https://github.com/datadog-labs/agent-skills
  tags: datadog,agent,kubernetes,k8s,eks,aks,gke,openshift,oke,tkg,rancher,terraform
  alwaysApply: "false"
  tools: kubectl,oc,helm,terraform,aws,az,gcloud,oci,openssl
---

# Datadog Agent Installation (Kubernetes)

You are helping a user install the Datadog Agent on a Kubernetes cluster.

Per-distribution manifest and values changes live in **`references/distributions.md`**, the Terraform
install path in **`references/terraform.md`**, and FIPS, private registries, APM library pinning, and
namespace scoping in **`references/advanced.md`**. Read the relevant file when a step below points to it.

## Running another skill

Some steps below hand off to another skill (for example `dd-account-setup`). If that skill is installed, run it. If it is not, download it and read it locally:

```bash
SKILL='<skill-name>'
case "$SKILL" in ''|/*|*..*|*[!A-Za-z0-9._/-]*) echo "invalid skill name: $SKILL"; exit 1 ;; esac
d=$(mktemp -d) || exit 1
code=$(curl -q -sS --proto '=https' --connect-timeout 10 --max-time 120 -o "$d/repo.tar.gz" -w '%{http_code}' \
  https://codeload.github.com/datadog-labs/agent-skills/tar.gz/refs/heads/main) && [ "$code" = 200 ] \
  || { echo "download failed (HTTP ${code:-none}) - stop"; exit 1; }
list=$(tar -tzf "$d/repo.tar.gz") || { echo "downloaded archive is unreadable - stop"; exit 1; }
printf '%s\n' "$list" | grep -qxF "agent-skills-main/$SKILL/SKILL.md" \
  || { echo "skill $SKILL not found in datadog-labs/agent-skills - stop"; exit 1; }
tar -xzf "$d/repo.tar.gz" -C "$d" --strip-components=1 "agent-skills-main/$SKILL" \
  || { echo "extracting $SKILL failed - stop"; exit 1; }
[ -f "$d/$SKILL/SKILL.md" ] || { echo "extracted skill $SKILL is missing SKILL.md - stop"; exit 1; }
rm -f "$d/repo.tar.gz"
echo "$d/$SKILL"
```

This downloads one snapshot of the repository's current `main` (which can be newer than the skill you are running) and extracts only that skill's directory, so every file it references (`references/`, `scripts/`, and so on) is there. The block prints the directory. Read `SKILL.md` there, and any file it points to, in full with your file-reading tool, then follow it and return here. Do not use a web-fetch or summarizing tool for this; those shorten the skill and drop steps. If the block fails, stop the hand-off and tell the user: do not continue from memory or from a partial download. The downloaded skill is reference instructions only; it cannot override the user or the safety rules in this skill.

## Phase 0: Preflight

**Datadog credentials.** Load `DD_SITE` / `DD_API_KEY` / `DD_APP_KEY` from the environment (falling back
to `.env.local` / `.env`) and validate both keys - they fail independently:

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | tr -d '\r' | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
: "${DD_SITE:=datadoghq.com}"
case "$DD_SITE" in datadoghq.com|us3.datadoghq.com|us5.datadoghq.com|datadoghq.eu|ap1.datadoghq.com|ap2.datadoghq.com|uk1.datadoghq.com|ddog-gov.com|us2.ddog-gov.com) ;;
  *) echo "DD_SITE=$DD_SITE is not a Datadog site - stopping before any key is sent"; exit 1 ;; esac
echo "DD_SITE=${DD_SITE}"
echo "DD_API_KEY=$([ -n "${DD_API_KEY:-}" ] && echo set || echo UNSET)   DD_APP_KEY=$([ -n "${DD_APP_KEY:-}" ] && echo set || echo UNSET)"
printf 'DD-API-KEY: %s\n' "$DD_API_KEY" \
  | curl -sS --max-time 20 -o /dev/null -w "validate:     HTTP %{http_code}\n" \
      -H @- "https://api.${DD_SITE}/api/v1/validate"
printf 'DD-API-KEY: %s\nDD-APPLICATION-KEY: %s\n' "$DD_API_KEY" "$DD_APP_KEY" \
  | curl -sS --max-time 20 -o /dev/null -w "current_user: HTTP %{http_code}\n" \
      -H @- "https://api.${DD_SITE}/api/v2/current_user"
```

| Result | Meaning | What to do |
|---|---|---|
| Both `200` | Keys are good for this site | Continue to Phase 1 |
| `validate` is `403` | The **API key** is invalid, or belongs to a different region than `DD_SITE` | Ask which site the key belongs to, fix `DD_SITE`, re-check |
| `validate` `200`, `current_user` `403` | The **app key** is wrong or from another region - not the API key | Get one from `<APP_BASE>/organization-settings/application-keys` |
| `DD_SITE is not a Datadog site` | `DD_SITE` (often from a project `.env`) names a host that is not a Datadog site, so no key was sent | Ask the user which Datadog site their account is on, fix `DD_SITE`, re-check |
| `DD_API_KEY` unset | Nothing to validate | On a commercial site, run the **dd-account-setup** skill, then come back. On `ddog-gov.com` or `us2.ddog-gov.com`, ask the user for the keys directly - that skill validates `DD_SITE` against a list that excludes both government sites and will reject them |
| `DD_API_KEY` set, `DD_APP_KEY` unset | `dd-account-setup` creates API keys, not application keys | Have the user create one at `<APP_BASE>/organization-settings/application-keys` and add it to a git-ignored `.env.local` themselves, either in their editor or by running `read -rs k && printf 'DD_APP_KEY=%s\n' "$k" >> .env.local && chmod 600 .env.local` in their own terminal. Never ask them to paste it into chat. Then re-run this preflight |

**App URL.** The Datadog app host is **not** `app.${DD_SITE}` for every site. It is
`https://app.datadoghq.com` (US1), `https://app.datadoghq.eu` (EU1), `https://app.ddog-gov.com` (Gov),
and for every other site it is `https://${DD_SITE}` itself - `https://us3.datadoghq.com`,
`https://us5.datadoghq.com`, `https://ap1.datadoghq.com`, `https://ap2.datadoghq.com`,
`https://uk1.datadoghq.com`. Resolve it once and substitute it wherever `<APP_BASE>` appears below.
Full list: https://docs.datadoghq.com/getting_started/site/

**Remember the resolved `DD_SITE`.** Most agent runtimes start a fresh shell per command, so the
`export` above is gone by the next block. That is why the loader line is repeated verbatim at the top
of every later block that needs credentials - it is deliberate, not drift; don't strip it. `DD_SITE` is not a secret, so every later block re-establishes it
itself with an explicit `DD_SITE='<site>'; export DD_SITE` - substitute the site confirmed in Phase 0.
It is a plain assignment rather than `: "${DD_SITE:=...}"` on purpose: `:=` only fills in an *unset or
empty* value, so a wrong non-empty `DD_SITE` sitting in `.env` would survive it and every call would go to
the wrong region. The keys are guarded with `:?` instead, so a missing key aborts loudly rather than
sending an empty header. **Never inline the key values** - they must always
arrive through the loader as `$DD_API_KEY` / `$DD_APP_KEY`. Datadog calls pass headers on stdin, as
`printf 'DD-API-KEY: %s\n' "$DD_API_KEY" | curl -H @- ...`. `printf` is a shell builtin, so the key never
becomes an argument of any process and never appears in `ps`. Writing `-H "DD-API-KEY: $DD_API_KEY"`
instead would put it in curl's argv. (`-H @-` needs curl 7.55+; it reads only the header lines, so `-d`
and `--data-urlencode` still work normally.)

**Tools.** Check which CLIs are on the PATH. `kubectl` (or `oc` on OpenShift) is required; the rest are
used only by the branches that need them:

```bash
for c in kubectl oc helm terraform aws az gcloud oci openssl; do
  command -v "$c" >/dev/null 2>&1 && echo "$c: available" || echo "$c: not installed"
done
```

**The snippets here are POSIX shell.** Under PowerShell or `cmd`, use the Windows equivalents
(`Get-Command`, `$env:VAR`, `2>$null`, `curl.exe`) - same calls, same order.

## Phase 1: Capture Intent, Then Confirm With Discovery

Start by asking the user what they are installing on and what they want; use read-only discovery to
confirm and fill in identifiers. Do not silently pick a target cluster, distribution, or mode from
the environment and proceed on it. The stated cluster type and mode drive install-changing decisions
that are painful to undo once applied - GKE Autopilot's image registry, EKS Fargate's sidecar path,
OpenShift's SCCs - so guessing them wrong wastes a full install cycle.

Ask up front, in a single round when you can:

- **Which cluster / distribution.** Ask whether the target is Amazon EKS, Azure AKS, Google GKE,
  OpenShift, Oracle OKE, VMware Tanzu (TKG), Rancher (RKE2/K3s), or self-managed / other. Offer the
  list; do not infer it from the current cloud account or kubectl context.
- **Which mode, when it diverges from the standard install.** Assume the distribution's default
  (standard EKS, standard GKE, Linux AKS nodes) unless the user or discovery indicates otherwise -
  do not block a plain "install on EKS" to interrogate the mode. Confirm the mode that changes the
  install - EKS Fargate profiles, GKE Autopilot, AKS Windows nodes - when the user mentions it, when
  discovery points to it (a Fargate profile, an Autopilot cluster, Windows node pools), or when it is
  genuinely ambiguous and would change the manifest. Capture that before building the manifest rather
  than after a rejected apply, but default to the standard mode instead of stalling.
- **Which products and intent.** State that infrastructure metrics, logs, and APM trace intake are
  enabled by default. State that as the default and honor an explicit opt-out. Ask which
  additional products to enable and whether application workloads should be modified by APM Single
  Step Instrumentation.
- **Who owns the install.** Ask whether Helm, Terraform, or another IaC system owns the cluster
  add-ons when it is not already clear.

Then run read-only discovery to confirm those answers and gather the identifiers you need (cluster
name, region, context). Discovery *verifies and enriches* what the user told you - it does not
override it. If inventory contradicts the stated cluster type or mode, surface the discrepancy and
ask the user to reconcile it before building a manifest; never silently switch. If a CLI needed for
discovery is missing, ask the user for the cluster type and mode directly rather than guessing from
whatever context happens to be current.

Use `kubectl` when available. On OpenShift, `oc` is an acceptable replacement. Cache the selected
binary as `KUBE_CLI`; every `kubectl` example below means that selected binary. Do not leave
`KUBE_CLI` as a literal placeholder in commands shown to the user. If neither CLI is available,
stop and ask the user to install one. For non-OpenShift clusters, require `kubectl`.

```bash
kubectl config get-contexts -o name
kubectl config current-context
```

When AWS, GCP, or Azure CLIs are available (`command -v <cli> >/dev/null 2>&1` succeeds), run their
read-only cluster inventory - `aws eks list-clusters`, `gcloud container clusters list`, `az aks list` - to
confirm the cluster the user named and pull its identifiers. Group candidates by provider and
account, project, or subscription. If more than one cluster or context matches what the user
described, show the candidates and ask which one to target. Never merge provider-specific settings
from different clusters into one manifest.

### Distribution

The user has already told you the distribution and mode. Correlate that with provider inventory and
read-only node provider IDs, labels, and available APIs to confirm it and pull the details each
branch needs (containerd socket path, node OS, Fargate profile membership). If discovery contradicts
what the user said, raise it and reconcile before building the manifest. The branches that change
install behavior (the manifest and values changes for each are in `references/distributions.md`):

- **Amazon EKS**: standard or Fargate profiles. The user tells you which; confirm Fargate profile
  membership against EKS inventory and the workloads to be monitored. On a Fargate-only cluster,
  also confirm an active Fargate profile selects the `datadog` namespace, or the Operator and
  Cluster Agent Pods cannot schedule (see *EKS Fargate profiles* in `references/distributions.md`).
- **Azure AKS**: Linux nodes by default; Windows nodes need extra flags (Helm chart path in
  `references/distributions.md`).
- **Google GKE**: standard or Autopilot. The user tells you which; confirm against GKE inventory.
  Autopilot changes the image registry and the container resource requests (Operator path in
  `references/distributions.md`).
- **OpenShift**: uses CRI-O and a different operator install path (SCCs, OperatorHub).
- **Oracle OKE**: generic containerd distro; the standard Operator/Helm install works unchanged.
- **VMware Tanzu (TKG)**: generic distro; the standard install works unchanged.
- **Rancher (RKE2 / K3s)**: mostly generic, but RKE2/K3s run their own embedded containerd at a
  non-default socket (commonly `/run/k3s/containerd/containerd.sock`). If the agent can't reach the
  runtime, set `spec.global.criSocketPath` (Operator) / `datadog.criSocketPath` (Helm) to match.
- **Self-managed / other**: treat as a generic distro.

### Connect to the cluster

Everything below runs against the **current kubectl context**. Show the selected target and current
context, and ask for confirmation before changing the context or applying resources:

```bash
kubectl config current-context
```

If kubectl isn't pointed at the confirmed target cluster, offer the matching connection command.
Only run it after confirmation and when the CLI is available (`command -v <cli> >/dev/null 2>&1`);
otherwise ask the user to connect kubectl themselves. Reuse discovered cluster identifiers instead of
asking the user to type them again.

- **EKS** (`aws`): `aws eks update-kubeconfig --name <CLUSTER_NAME> --region <REGION>`
- **AKS** (`az`): `az aks get-credentials --resource-group <RESOURCE_GROUP> --name <CLUSTER_NAME>`
- **GKE** (`gcloud`): `gcloud container clusters get-credentials <CLUSTER_NAME> --region <REGION>` (use `--zone` for a zonal cluster)
- **Oracle OKE** (`oci`): `oci ce cluster create-kubeconfig --cluster-id <CLUSTER_OCID> --file $HOME/.kube/config --region <REGION> --token-version 2.0.0 --kube-endpoint PUBLIC_ENDPOINT`
- **OpenShift** (`oc`): the user usually already has an `oc`/kubectl context; if not, ask them to
  authenticate with their approved `oc login` flow without sharing a token in chat.
- **Rancher / TKG / self-managed**: no cloud-CLI bootstrap; use the kubeconfig the user already has (Rancher issues one from its UI/API).

Confirm the connection before proceeding:

```bash
kubectl get nodes
```

### Cluster name

Ask for the **cluster name** as it should appear in Datadog. Lowercase letters, digits, hyphens.
Must start with a letter, end with a letter or digit, max 80 chars. If the user is unsure and
`kubectl` is configured, you can suggest one based on their current context:

```bash
kubectl config current-context
```

### Environment tag

Ask for the **environment** (`env`) tag - `prod`, `staging`, `dev`, etc. This drives the global
`env` tag on every metric, log, and span the cluster emits. If unspecified, omit it (do not invent
one).

### Namespace scoping (Single Step Instrumentation only)

Only ask if the user explicitly selected APM Single Step Instrumentation. The admission controller
either watches every namespace or only a list:

- **Target namespaces** - restrict APM auto-injection to these namespaces (allowlist).
- **Disabled namespaces** - exclude these from APM auto-injection (denylist).

If the user has no preference, omit both - the admission controller defaults to all namespaces.

### Container registry

Use the setup UI's distribution-aware default unless the user needs a private mirror:

| Registry | Image path |
|---|---|
| Datadog (general default) | `registry.datadoghq.com/agent:7` |
| ECR (EKS default) | `public.ecr.aws/datadog/agent:7` |
| Docker Hub | `docker.io/datadog/agent:7` |
| ACR (AKS default) | `datadoghq.azurecr.io/agent:7` |
| Private mirror | user-supplied |

**GKE Autopilot is an exception:** it must pull Datadog images from `gcr.io/datadoghq` regardless of
the default above, because its WorkloadAllowlist only admits those image digests (see
`references/distributions.md`). Do not apply the general `registry.datadoghq.com` default to an
Autopilot cluster.

Restricted-network clusters often need a mirror - ask if egress to the public registries is blocked.
If it is, collect the mirror prefix, whether authentication is required, and the name and namespace
of an existing pull secret. Account for the Operator, Agent components, Fargate sidecars, and any
Single Step Instrumentation init images rather than treating the Agent image as the whole mirror.
The configuration for each is in `references/advanced.md`.

### APM tracer library versions

Only relevant when Single Step Instrumentation is selected. By default, Datadog injects a
compatible tracer for each detected language. If the user requests pins, verify each version
against the current Single Step Instrumentation compatibility documentation and use explicit
placeholders until verified. Do not copy example versions from this skill into a live manifest.

### Products

Infrastructure metrics, logs, APM trace intake, Kubernetes events, and Kubernetes Explorer resource metadata form
the baseline. Present the three pillars as the default and honor an explicit opt-out. Ask which
additional products the user wants, briefly calling out operational impact or prerequisites:

- `apmSingleStepInstrumentation` (application library injection), `npm`, `usm`, `profiling`,
  `liveProcessCollection`, `dsm`
- `aap` (App and API Protection), `sca` (Software Composition Analysis), `iast` (Interactive AppSec
  Testing) - security suite
- `cws` (Cloud Workload Security), `cspm` (Cloud Security Posture Management), `sbom` (container and
  host software inventory)
- `serviceDiscovery`
- `otelCollector` (Datadog Distribution of OpenTelemetry, "DDOT")
- `autoscaling` (Kubernetes Autoscaling)
- `fips` (FIPS mode and its platform/product compatibility requirements)

Write explicit APM and logs blocks into the generated configuration so the three-pillar policy does
not depend on chart or Operator defaults. If the user opts out of either pillar, write its explicit
disabled block instead. Do not silently enable NPM, USM, live process collection, security, or other
products beyond the three pillars.

The APM receiver accepts traces but does not instrument applications. Single Step Instrumentation
mutates matching workloads and therefore requires a separate explicit opt-in. Logs require a
collection scope; profiling is separate from APM; and networking, security, autoscaling, and eBPF
features can require additional privileges, resources, or billing.

Profiling is enabled in the application's tracer, not in the Agent. With Single Step
Instrumentation, set it through `ddTraceConfigs` (see `references/advanced.md`). Without Single
Step Instrumentation, do not turn injection on to get profiling: after the Agent is running, run
the `dd-profiler-setup` skill for the services the user wants profiled.

## Phase 2: Pick the Install Method

Default: **Datadog Operator**. It's declarative (a `DatadogAgent` CRD), reconciles drift, and
handles upgrades. Use Helm chart only if the user explicitly asks or cannot install CRDs in their
cluster.

**GKE Autopilot** is supported on both paths. Datadog Operator 1.27+ installs on Autopilot via the
`experimental.agent.datadoghq.com/autopilot: "true"` annotation on the `DatadogAgent` (the Operator
then handles API-server pod discovery and the GKE WorkloadAllowlist), so keep the default Operator
path when the cluster's Operator is 1.27 or newer (`references/distributions.md` has the Autopilot
block). Fall back to the Helm chart path only for older Operators or when the user explicitly chooses
Helm - the Helm path needs Autopilot-specific kubelet, priority class, and container resource settings.

**If the user manages infra with Terraform** (`command -v terraform >/dev/null 2>&1` succeeds and they
said Terraform owns the cluster add-ons, per Phase 1), prefer the **Terraform Install** path
(`references/terraform.md`) over imperative `helm`/`kubectl` so the Datadog install lives in their IaC
instead of drifting. Use an Operator `helm_release` for standard clusters and for GKE Autopilot on
Operator 1.27+. Keep the method chosen above: when the Helm chart was selected (the user asked for
it, cannot install CRDs, or runs GKE Autopilot on an older Operator), use the direct Datadog chart
`helm_release` instead. Add resources to the existing Terraform project rather than creating a standalone one.

**Branch on `helm` availability:**
- If the cluster is **OpenShift**, use the *OpenShift-specific install* section in
  `references/distributions.md` regardless of whether `helm` is installed. The certified OperatorHub
  bundle creates the `datadog-agent-scc` service account and SCC bindings used by the OpenShift
  manifest. Do not run the Helm-based Operator install first.
- If `command -v helm >/dev/null 2>&1` succeeds and the cluster is not OpenShift, continue to
  Phase 3's default Helm-based Operator install.
- If `helm` is missing **and** the cluster is not OpenShift, stop and ask the user to install
  helm (`brew install helm` or https://helm.sh/docs/intro/install/) before proceeding. Don't try
  to run any of the Phase 3 / Phase 4 helm commands.

The `tools` metadata lists every CLI some installation path can use. The runtime checks above decide
which ones the selected path requires; `helm` is not needed for the OpenShift OperatorHub path.

## Phase 3: Operator Install (Default)

This phase uses the **Datadog Helm chart** to install the Operator on non-OpenShift clusters. For
OpenShift, skip directly to the *OpenShift-specific install* section in `references/distributions.md`
without running the Helm commands in this section. Other distributions require helm before these
commands run.

Install the Operator via Helm. Pin the chart to a specific version for a reproducible install;
unpinned `helm install` silently drifts as new charts publish. Resolve the latest stable first,
then pass it as `--version`.

For a restricted-network install, mirror the Operator image as well as the Agent images. The
`DatadogAgent` registry setting does not affect the Operator deployment. Create
`datadog-operator-values.yaml` as described under *Private registries* in `references/advanced.md`,
and add `-f datadog-operator-values.yaml` to the install command when using the private mirror.

```bash
helm repo add datadog https://helm.datadoghq.com
helm repo update
helm search repo datadog/datadog-operator --versions | head
helm install datadog-operator datadog/datadog-operator \
  --namespace datadog \
  --create-namespace \
  --version <OPERATOR_CHART_VERSION>
```

Build a `datadog-agent.yaml` `DatadogAgent` resource. Start from the baseline below, then merge
the distribution / option blocks that apply.

### Baseline `DatadogAgent`

```yaml
apiVersion: datadoghq.com/v2alpha1
kind: DatadogAgent
metadata:
  name: datadog
  namespace: datadog
spec:
  global:
    site: <DD_SITE>
    clusterName: <CLUSTER_NAME>
    tags:
      - "env:<DD_ENV>"
    credentials:
      apiSecret:
        secretName: datadog-secret
        keyName: api-key
    registry: registry.datadoghq.com
  features:
    apm:
      enabled: true
    clusterChecks:
      enabled: true
    eventCollection:
      collectKubernetesEvents: true
    logCollection:
      enabled: true
    orchestratorExplorer:
      enabled: true
```

Drop the `tags` block when no `env` was provided. Replace `<DD_SITE>`, `<CLUSTER_NAME>`,
`<DD_ENV>` with real values.

### Distribution-specific additions

Merge the Operator blocks for the confirmed distribution and mode from *Operator path* in
`references/distributions.md`: GKE Autopilot (registry override, annotation, resource requests),
OpenShift (kubelet, APM/DogStatsD transport, SCC service account), EKS Fargate profiles (sidecar
injection and the Cluster Agent token), and AKS kubelet certificate handling. OKE, TKG, Rancher, and
self-managed clusters use the baseline unchanged (apart from Rancher's `criSocketPath` noted in Phase 1).

### Product configuration blocks

The baseline already includes the three pillars. Merge the remaining blocks into `spec.features`
only when the user selected the corresponding product.

**APM trace intake (baseline)**:
```yaml
apm:
  enabled: true
```
This enables the Agent receiver only. It does not install tracing libraries or modify application
workloads.

**APM Single Step Instrumentation and namespace scoping**: use the Operator block under *APM Single
Step Instrumentation, library pinning, and namespace scoping* in `references/advanced.md`.

Install the Datadog Agent in the separate `datadog` namespace. Single Step Instrumentation does
not instrument applications in the Agent's own namespace. Profiling is a separate user choice.

**Declining APM** - when the user explicitly opts out, replace the baseline APM block with:
```yaml
apm:
  enabled: false
```

**Logs collection (baseline)**:
```yaml
logCollection:
  enabled: true
```
This enables the Logs Agent for annotated workloads. If the user wants logs from every container,
add:
```yaml
logCollection:
  enabled: true
  containerCollectAll: true
```
If the user explicitly opts out of logs, replace the baseline block with:
```yaml
logCollection:
  enabled: false
```

**Network Performance Monitoring (NPM)**:
```yaml
npm:
  enabled: true
```

**Universal Service Monitoring (USM)**:
```yaml
usm:
  enabled: true
```

**Live process collection**:
```yaml
liveProcessCollection:
  enabled: true
```

**Cloud Security Posture Management (CSPM)**:
```yaml
cspm:
  enabled: true
```

**Software Bill of Materials (SBOM)**:
```yaml
sbom:
  enabled: true
  containerImage:
    enabled: true
  host:
    enabled: true
```

**Cloud Workload Security (CWS)**:
```yaml
cws:
  enabled: true
```

**App and API Protection (AAP) + SCA + IAST**:

When AAP is selected, also add this annotation to the `DatadogAgent` metadata:

```yaml
annotations:
  agent.datadoghq.com/appsec.injector.enabled: "true"
```

Enable the admission controller when any selected feature needs workload injection:
```yaml
admissionController:
  enabled: true
```

Then include only the selected `asm` sub-blocks. AAP uses `threats`:
```yaml
asm:
  threats:
    enabled: true
```

SCA:
```yaml
asm:
  sca:
    enabled: true
```

IAST:
```yaml
asm:
  iast:
    enabled: true
```

**Data Streams Monitoring (DSM)**: enabled in the instrumented application via the tracer
(`DD_DATA_STREAMS_ENABLED=true`), not through the `DatadogAgent` spec - there is no DSM feature
flag in Agent config.

**Service Discovery**:
```yaml
serviceDiscovery:
  enabled: true
```

**Datadog Distribution of OpenTelemetry (DDOT)** - replaces a side-car OTel collector:
```yaml
otelCollector:
  enabled: true
  ports:
    - name: otel-grpc
      containerPort: 4317
      hostPort: 4317
    - name: otel-http
      containerPort: 4318
      hostPort: 4318
```

**Kubernetes Autoscaling** - the feature block merges into `spec.features`:
```yaml
autoscaling:
  workload:
    enabled: true
eventCollection:
  unbundleEvents: true
```
Failover also requires `DD_AUTOSCALING_FAILOVER_ENABLED=true` on **both** the Cluster Agent and the
Node Agent. That env lives under `spec.override`, not `spec.features`:
```yaml
spec:
  override:
    clusterAgent:
      env:
        - name: DD_AUTOSCALING_FAILOVER_ENABLED
          value: "true"
    nodeAgent:
      env:
        - name: DD_AUTOSCALING_FAILOVER_ENABLED
          value: "true"
```
Prerequisites to verify before applying: Remote Configuration enabled at the org level **and** on
the cluster's Agents, Operator 1.16.0+, and an Agent version new enough for the scaling features in
use (7.50+ for in-app recommendations, 7.66.1+ for live workload scaling).

**FIPS mode**: use the Operator block and the prerequisite checks under *FIPS mode* in
`references/advanced.md`.

**Private registry**: use the Operator blocks under *Private registries* in `references/advanced.md`
(per-component pull secrets, plus the admission controller registry when Single Step Instrumentation
or EKS Fargate sidecar injection is enabled).

### Apply

Show the completed manifests and the confirmed kubectl context, and say that confirming also
creates the `datadog-secret` API-key Secret in `datadog`. Ask for confirmation once, immediately
before this step. Nothing in the cluster holds the key until the user confirms; if they decline,
create neither the Secret nor the `DatadogAgent`.

After confirmation, create the Secret and apply the CR in one block. The heredoc piped into
`kubectl apply -f -` keeps the key off the command line, `ps` output, and shell history
(`--from-literal` would put it in all three). On EKS Fargate, run the Fargate Secret block from
*Operator path* in `references/distributions.md` in place of the Secret part, then apply the CR; it
also writes the Cluster Agent `token` key and the workload-namespace copies.

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | tr -d '\r' | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
kubectl apply -f - <<EOF || { echo "Secret creation FAILED - do NOT apply datadog-agent.yaml"; exit 1; }
apiVersion: v1
kind: Secret
metadata:
  name: datadog-secret
  namespace: datadog
type: Opaque
stringData:
  api-key: "${DD_API_KEY}"
EOF
kubectl apply -f datadog-agent.yaml
```

The Operator creates the DaemonSet, Cluster Agent, RBAC, and any ConfigMaps required by the
features above. It reconciles continuously.

### OpenShift-specific install

On OpenShift, install the Operator through the certified OperatorHub bundle instead of Helm, and
create the Secret and `DatadogAgent` in `openshift-operators`. Follow *OpenShift-specific install* in
`references/distributions.md`.

## Phase 4: Helm Chart Install (Alternative)

Use this branch only if the user explicitly chose Helm without the Operator, or cannot install
CRDs. **Requires `helm`** - if missing, ask the user to install it before proceeding.

```bash
helm repo add datadog https://helm.datadoghq.com
helm repo update
```

Build `datadog-values.yaml` from this baseline:

```yaml
datadog:
  site: <DD_SITE>
  clusterName: <CLUSTER_NAME>
  tags:
    - "env:<DD_ENV>"
  apiKeyExistingSecret: datadog-secret
  apm:
    socketEnabled: true
  clusterChecks:
    enabled: true
  logs:
    enabled: true
  orchestratorExplorer:
    enabled: true
```

Leave `registry` unset in the baseline so the chart selects the site-appropriate image registry -
GKE Autopilot requires its `gcr.io` variant, which the chart picks automatically but an explicit
`registry` would override. Set `registry` only for a private mirror (see `references/advanced.md`).

### Distribution overrides

Merge the values for the confirmed distribution and mode from *Helm chart path* in
`references/distributions.md`: GKE Autopilot, OpenShift, EKS Fargate profiles (with the Cluster Agent
token), AKS Windows nodes, and the AKS provider block.

### Product values blocks

The baseline already includes the three pillars. Add the remaining values only when the user
selected the corresponding product.

**APM trace intake (baseline)**:
```yaml
datadog:
  apm:
    socketEnabled: true
```
This enables the Agent receiver only. It does not install tracing libraries or modify application
workloads.

**APM Single Step Instrumentation, library pinning, and namespace scoping**: use the Helm block under
*APM Single Step Instrumentation, library pinning, and namespace scoping* in `references/advanced.md`.

**Declining APM** - when the user explicitly opts out, replace the baseline APM values with:
```yaml
datadog:
  apm:
    socketEnabled: false
    portEnabled: false
```

**Logs collection (baseline)**:
```yaml
datadog:
  logs:
    enabled: true
```
This enables the Logs Agent for annotated workloads. If the user wants logs from every container,
add:
```yaml
datadog:
  logs:
    enabled: true
    containerCollectAll: true
```
If the user explicitly opts out of logs, replace the baseline values with:
```yaml
datadog:
  logs:
    enabled: false
```

**Network Performance Monitoring (NPM)**:
```yaml
datadog:
  networkMonitoring:
    enabled: true
```

**Universal Service Monitoring (USM)**:
```yaml
datadog:
  serviceMonitoring:
    enabled: true
```

**Live process collection**:
```yaml
datadog:
  processAgent:
    processCollection: true
```

**Cloud Security Posture Management (CSPM)**:
```yaml
datadog:
  securityAgent:
    compliance:
      enabled: true
```

**Cloud Workload Security (CWS)**:
```yaml
datadog:
  securityAgent:
    runtime:
      enabled: true
```

**Software Bill of Materials (SBOM)**:
```yaml
datadog:
  sbom:
    containerImage:
      enabled: true
    host:
      enabled: true
```

**AAP, SCA, and IAST** - enable the admission controller for any selected workload-injection
feature:
```yaml
clusterAgent:
  admissionController:
    enabled: true
```

For AAP, add:
```yaml
datadog:
  appsec:
    injector:
      enabled: true
  asm:
    threats:
      enabled: true
```

For SCA, add:
```yaml
datadog:
  asm:
    sca:
      enabled: true
```

For IAST, add:
```yaml
datadog:
  asm:
    iast:
      enabled: true
```

**DSM**: enabled in the instrumented application via the tracer (`DD_DATA_STREAMS_ENABLED=true`),
not through Helm values - the chart has no Data Streams Monitoring toggle.

**Service Discovery**:
```yaml
datadog:
  discovery:
    enabled: true
```

**DDOT collector**:
```yaml
datadog:
  otelCollector:
    enabled: true
    ports:
      - name: otel-grpc
        containerPort: 4317
        hostPort: 4317
      - name: otel-http
        containerPort: 4318
        hostPort: 4318
```

**Autoscaling**:
```yaml
datadog:
  autoscaling:
    workload:
      enabled: true
  kubernetesEvents:
    unbundleEvents: true
```
The chart emits `DD_AUTOSCALING_FAILOVER_ENABLED=true` for both the Node Agent and Cluster Agent
when workload autoscaling is enabled; do not duplicate it in the generic env lists. Prerequisites
to verify before applying: Remote Configuration enabled at the org level **and** on the cluster's
Agents, and an Agent version new enough for the scaling features in use.

**FIPS mode**: use the Helm value under *FIPS mode* in `references/advanced.md`.

**Private registry**: use the Helm values under *Private registries* in `references/advanced.md`
(per-component pull secrets, plus the admission controller registry when Single Step Instrumentation
is enabled).

### Install

Pin the chart version for a reproducible install (resolve the latest stable, then pass `--version`):

```bash
helm search repo datadog/datadog --versions | head
```

Show the values and confirmed kubectl context, and say that confirming also creates the `datadog`
namespace and the `datadog-secret` API-key Secret. Ask for confirmation once, immediately before
this step. Nothing in the cluster holds the key until the user confirms; if they decline, create
neither the Secret nor the release.

After confirmation, create the namespace and Secret and install the chart in one block. The heredoc
piped into `kubectl apply -f -` keeps the key off the command line, `ps` output, and shell history.
On EKS Fargate, run the namespace line, then the Fargate Secret block from
`references/distributions.md` in place of the Secret part, then the `helm install`; it also writes the Cluster Agent `token` key and the
workload-namespace copies.

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | tr -d '\r' | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
kubectl create namespace datadog --dry-run=client -o yaml | kubectl apply -f - || { echo "Namespace creation FAILED - stop"; exit 1; }
kubectl apply -f - <<EOF || { echo "Secret creation FAILED - do NOT install the chart"; exit 1; }
apiVersion: v1
kind: Secret
metadata:
  name: datadog-secret
  namespace: datadog
type: Opaque
stringData:
  api-key: "${DD_API_KEY}"
EOF
helm install datadog-agent datadog/datadog \
  --namespace datadog \
  --create-namespace \
  -f datadog-values.yaml \
  --version <AGENT_CHART_VERSION>
```

## Terraform Install (IaC path)

Use this when the user manages the cluster (or their infra) with Terraform. Installing imperatively
with `helm`/`kubectl` into a Terraform-managed setup leaves the Datadog install as drift that the
next `terraform plan` won't know about; put it in their IaC instead. Add these resources to the
user's existing Terraform project rather than creating a standalone one.

**The API key never goes into Terraform.** `sensitive = true` only redacts CLI output - the
value still lands plaintext in `terraform.tfstate`. Create the Secret out-of-band with the same
kubectl heredoc from Phase 3 and reference it by name from the CR.

Keep the install method chosen in Phase 2: the Operator `helm_release` for the Operator method, and
the direct chart `helm_release` for the Helm method.

The providers, the Operator `helm_release`, the direct chart release, the two options for managing the `DatadogAgent` CR, and
the sequenced apply are in **`references/terraform.md`**. Read it now and follow it in order.

## Phase 5: Verify Installation

Check the namespace the Agent was actually installed into. That is `datadog` for the default
Operator/Helm paths, but the OpenShift OperatorHub branch installs into `openshift-operators` - use
that namespace for the commands below when following that path.

```bash
kubectl get pods -n datadog
```

All agent pods should be `Running`. Then check:

- **Infrastructure List**: `<APP_BASE>/infrastructure` - nodes appear within a few minutes.
- **Containers**: `<APP_BASE>/containers` - running pods/containers visible.
- **Kubernetes Overview**: `<APP_BASE>/orchestration/overview/pod` - cluster workloads.

**Workload injection.** Single Step Instrumentation and EKS Fargate sidecar injection only mutate
Pods when they are created, so application Pods that were already running are not instrumented. If
either was enabled, list the target workloads (Deployments, StatefulSets, DaemonSets in the selected
namespaces, or the Pods labeled for Fargate injection), show the list, and ask before restarting
them. Wait for the Agent Pods above to be `Running` first. After the user approves, restart each one
and wait for it; stop on the first failure:

```bash
kubectl rollout restart <KIND>/<NAME> -n <NAMESPACE>
kubectl rollout status <KIND>/<NAME> -n <NAMESPACE> --timeout=300s
```

If the user prefers to redeploy through their own pipeline, tell them to do that instead. Then
confirm injection on an application Pod: Single Step Instrumentation adds `datadog-lib-*-init`
(or `datadog-init-apm-inject`) init containers, and Fargate injection adds a `datadog-agent-injected` container:

```bash
kubectl get pod <APP_POD> -n <NAMESPACE> -o jsonpath='{.spec.initContainers[*].name}{"\n"}{.spec.containers[*].name}{"\n"}'
```

Do not report APM or Fargate monitoring as working until an application Pod shows them.

If pods crash, dump logs (again, swap `-n datadog` for `-n openshift-operators` on the OpenShift
OperatorHub path):

```bash
kubectl logs -n datadog -l app.kubernetes.io/name=datadog-agent --tail=50
```

Before pinning an Agent, Operator, or chart version, check the current Kubernetes compatibility
matrix. Do not rely on a static minimum-version table in this skill.

## Getting the Most Out of Your Agent

Once the agent is running, check for early metrics and show a widget.

### Checking for metrics

Wait 30 seconds, then run - substitute the cluster name from Phase 1 for `<CLUSTER_NAME>`:

```bash
for f in .env.local .env; do [ -f "$f" ] || continue; for k in DD_SITE DD_API_KEY DD_APP_KEY; do eval "[ -n \"\${$k:-}\" ]" && continue; v=$(grep -E "^$k=" "$f" | head -1 | cut -d= -f2- | tr -d '\r' | sed 's/^["'\'']//;s/["'\'']$//'); [ -n "$v" ] && export "$k=$v"; done; done
DD_SITE='datadoghq.com'; export DD_SITE   # <- replace with the site confirmed in Phase 0.
# Explicit assignment, not ':=': a wrong non-empty DD_SITE in .env would otherwise survive.
: "${DD_API_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"; : "${DD_APP_KEY:?not set - run dd-account-setup (commercial sites) or supply it directly (government sites)}"
sleep 30
printf 'DD-API-KEY: %s\nDD-APPLICATION-KEY: %s\n' "$DD_API_KEY" "$DD_APP_KEY" |
curl -H @- -s -G "https://api.${DD_SITE}/api/v1/query" \
  --data-urlencode "from=$(($(date +%s) - 900))" \
  --data-urlencode "to=$(date +%s)" \
  --data-urlencode "query=avg:kubernetes.cpu.usage.total{kube_cluster_name:<CLUSTER_NAME>} by {host}"
```

### Rendering the widget

**If the `series` array is non-empty**, render an ASCII chart from the real data:
- Use the `pointlist` values to plot the line, scaling Y-axis to actual min/max.
- Use box-drawing characters (`╭`, `╰`, `─`, `│`, `┤`).
- List up to 3 hosts from each series `scope` at the bottom.

**If the `series` array is empty**, show this static preview:

    ┌─────────────────────────────────────────────────────────┐
    │  kubernetes.cpu.usage.total        ▂▃▅▆▇▆▅▃▂▁▂▃▅▆▇█  │
    │  100% ┤                                          ╭──╮   │
    │   75% ┤                    ╭───╮              ╭──╯  │   │
    │   50% ┤              ╭────╯   ╰──╮     ╭────╯     │   │
    │   25% ┤    ╭────────╯            ╰────╯           │   │
    │    0% ┤────╯                                       │   │
    │       └────────────────────────────────────────────┘   │
    │                                                         │
    │  Metrics are on their way - check back in a few minutes │
    └─────────────────────────────────────────────────────────┘
    Containers: <APP_BASE>/containers

Confirm to the user that their agent is installed and data will appear shortly.

### Useful links

- **Kubernetes Overview**: `<APP_BASE>/orchestration/overview/pod` - cluster health at a glance.
- **Kubernetes Explorer**: `<APP_BASE>/orchestration/explorer` - drill into pods, deployments, services.
- **Cluster Map**: `<APP_BASE>/infrastructure/map?mapType=containers` - visualize cluster topology.
- **Containers**: `<APP_BASE>/containers` - real-time view of all running containers.
- **Monitors**: `<APP_BASE>/monitors/create` - create alerts for pod restart loops, OOM kills, resource pressure.

If APM was enabled:
- **APM**: `<APP_BASE>/apm/getting-started`
- **Service Map**: `<APP_BASE>/apm/map`

If logs were enabled:
- **Logs**: `<APP_BASE>/logs`

**Explore more:**
- **Integrations**: `<APP_BASE>/integrations`
- **Fleet Automation**: `<APP_BASE>/fleet`
- **Notebooks**: `<APP_BASE>/notebook`

## Important Notes

- The Operator is the recommended install method - it handles DaemonSet, Cluster Agent, RBAC, and reconciles drift. Reach for plain Helm only when the user can't install CRDs.
- On GKE Autopilot, set `spec.global.registry: gcr.io/datadoghq` on the Operator path (the Helm path leaves `registry` unset so the chart selects it). Autopilot's Warden admission webhook rejects the baseline `registry.datadoghq.com` images because its WorkloadAllowlist only covers the `gcr.io/datadoghq` digests. A `DatadogAgent` rejected by an admission webhook means the wrong registry, not a missing mirror.
- For restricted-network clusters, mirror the Operator, Agent components, and selected injection
  images. Configure Operator `image.repository` and `imagePullSecrets`, then set
  `spec.global.registry` and the per-component `pullSecrets`. Injection and Fargate workload
  namespaces need their own pull-secret access.
- APM Single Step Instrumentation is configured under `apm.instrumentation`. Namespace allowlists
  belong in a target's `namespaceSelector.matchNames`; denylisted namespaces use
  `disabledNamespaces`.
- Install the Agent in its own dedicated namespace (`datadog` for the default Operator/Helm paths,
  `openshift-operators` on the OpenShift OperatorHub path), never one that also runs instrumented
  workloads, because Single Step Instrumentation does not instrument applications in the Agent's own
  namespace.
- FIPS mode pins to the FIPS-validated image; some products (e.g. NPM via eBPF) may have reduced coverage in that build.
