---
name: orca-k8s-connector-troubleshoot
description: Diagnoses Kubernetes Connector (K8s Tunnel Client / Helm chart `orca-tunnel`) install and connectivity failures from raw customer input — error text, `helm status`, `kubectl describe`, or pod logs — and walks through step-by-step remediation. Use when a user reports the K8s Connector won't install, won't connect, keeps disconnecting, or the cluster shows connected but no scan data appears.
trigger: When user reports a Kubernetes Connector / K8s tunnel client problem — helm install failures, pod crash-looping or stuck Pending/ImagePullBackOff, tunnel not connecting, TLS/DNS/proxy errors, RBAC or ClusterRoleBinding errors, OpenShift SCC issues, duplicate cluster entries, unauthorized/401 errors reaching the cluster API, or a cluster showing "connected" with no scan data (e.g., "k8s connector won't connect", "tunnel pod is crashlooping", "helm install failed for orca-tunnel", "cluster shows connected but no data", "TLS handshake timeout k8s connector", "unauthorized error from cluster API")
---

# Orca Kubernetes Connector Troubleshooting Skill

Answers: **"Why isn't my Kubernetes Connector installing or connecting, and how do I fix it myself before opening a support ticket?"**

## Background

The Kubernetes Connector (aka K8s Tunnel Client, Helm chart `orca-tunnel`, image `k8s-tunnel-client`) runs entirely on the customer's own cluster. It opens a read-only outbound tunnel (built on `frp`) back to Orca so private and self-managed clusters can be scanned without exposing the cluster's API server to Orca. Because it runs on customer infrastructure, failures are invisible to Orca until the customer reports them. Most of what's covered here can be self-diagnosed from `helm status`, `kubectl describe`, and pod logs alone — that's the point of this skill.

**Quick glossary** (so the categories below don't have to re-explain these every time):
| Term | Means |
|------|-------|
| `frp` | The open-source reverse-proxy library the tunnel is built on. TCP only — if a firewall log shows UDP traffic, that's unrelated noise, not the tunnel. |
| Tunnel target | Orca's server-side record of a specific cluster's tunnel. Can go stale (survive after the customer uninstalls the chart) and is only cleanable by Orca support/on-call. |
| `tunnelId` / `tunnelToken` | The credential pair from Orca's cluster-onboarding screen. Unique per cluster — never reuse one from a different cluster. |
| `cloudVendorId` | The cloud-vendor-specific cluster identifier (format varies by vendor — see the **Connecting Clusters** doc). The single most common typo source in install commands. |
| SCC | OpenShift's Security Context Constraint — its equivalent of a PodSecurityPolicy. |

## Usage

```
/orca-k8s-connector-troubleshoot <paste error, helm status, kubectl describe, or pod logs output>
```

Or natural language:
- "the k8s connector pod is stuck in ImagePullBackOff"
- "helm install for orca-tunnel failed, here's the output: ..."
- "tunnel keeps disconnecting, logs show TLS handshake timeout"
- "cluster shows connected in Orca but no inventory data is showing up"
- "we're getting Unauthorized when the connector reads the cluster API"

## How It Works

1. **Sanity-check** — confirm the Connector is even the right tool for this cluster (Step 1).
2. **Triage** — classify as install-time (chart never deployed successfully) vs. runtime (chart deployed, tunnel/scan not working).
3. **Match** — use the Quick Reference table to jump straight to a category by symptom, or scan the full list.
4. **Remediate or ask** — walk through that category's fix; if the input doesn't clearly match a signature, ask a targeted clarifying question instead of guessing.
5. **Escalate** — if nothing resolves it (including the "known platform limitations" below, which the customer cannot fix themselves), produce a clean handoff summary.

## Step 1: Sanity Check + Triage

**First, confirm the Connector is actually needed.** The single most common avoidable support case is a customer running the K8s Connector on a cluster that's already publicly reachable — it doesn't need a tunnel at all, and fighting connectivity errors on it is wasted effort. Ask: *is this cluster reachable directly (public endpoint), or private/self-managed?* If it's public, the fix is to remove the Connector and let the **Native** connection method handle it instead (see the note in Category 11 below for the correct removal order).

Once you know the Connector is actually the right approach, settle install-time vs. runtime with one command if the customer hasn't already supplied it:

```
kubectl get pods -n <namespace>
helm status <release> -n <namespace>
```

- **Install-time**: `helm install`/`helm upgrade` itself failed, or the pod has never reached a stable `Running` state (`CrashLoopBackOff`, `ImagePullBackOff`, `Pending`, or an error creating the chart's cluster-scoped resources).
- **Runtime**: the chart deployed and the pod has been `Running` at some point, but the tunnel drops, never establishes, or the cluster looks "connected" in Orca yet nothing scans.

If this isn't clear from what the customer gave you, ask before guessing (Step 3).

## Quick Reference: Symptom → Category

Scan for the phrase closest to what the customer reported, then jump to that category for the full fix.

| Symptom | Category |
|---|---|
| `dial tcp ... i/o timeout` / `TLS handshake timeout` in logs | [1. Can't reach the tunnel endpoint](#1-cant-reach-the-tunnel-endpoint-timeout--tls-handshake) |
| `helm install` fails on RBAC objects, or `forbidden`/`Unauthorized` listing cluster resources | [2. RBAC / permission errors](#2-rbac--permission-errors-applying-the-chart) |
| Pod stuck `ImagePullBackOff` / `ErrImagePull` | [3. Image pull failures](#3-image-pull-failures) |
| Pod crash-loops right after install, or `cloud_account not found` at login | [4. Bad `--set` parameters](#4-incorrect-missing-or-malformed---set-parameters) |
| Install succeeds but pod fails on startup with an API compatibility error | [5. Kubernetes version too old](#5-kubernetes-version-incompatibility) |
| Two Orca cluster entries for one physical cluster (self-managed + EKS/AKS/GKE) | [6. Duplicate cluster entries](#6-misuse-of-automationtrue-or-duplicateconflicting-cluster-entries) |
| Pod `OOMKilled`, or `Pending` with insufficient CPU/memory events | [7. Resource constraints](#7-resource-constraints) |
| `helm install` says a secret doesn't exist, but `kubectl get secret` shows it does | [8. Custom namespace issues](#8-custom-namespace-issues) |
| Pod `Running`, but `Unauthorized`/`401` when reading the cluster API | [9. Service-account token expired (K8s 1.30+)](#9-service-account-token-expired-k8s-130) |
| Pod `Running`, tunnel up, but `context deadline exceeded` listing resources | [10. NetworkPolicy blocks API-server egress](#10-networkpolicy-blocks-api-server-egress-causing-context-deadline-exceeded) |
| Tunnel connects then drops on auth/token rejection, or `K8s Tunnel client is unreachable` after re-onboarding | [11. Tunnel drops / stale tunnel target](#11-tunnel-establishes-then-drops-on-authtoken-errors-or-a-stale-tunnel-target) |
| Works with no proxy, breaks once `proxyURL` is set | [12. Proxy misconfiguration](#12-proxy-misconfiguration) |
| `no such host` resolving `tunnelAddr` | [13. DNS resolution failures](#13-dns-resolution-failures) |
| Pod fails to schedule/start, only on OpenShift | [14. OpenShift SCC issues](#14-openshift-specific-scc-issues) |
| Tunnel healthy, cluster shows "connected", but no scan data ever appears | [15. Connected but no scan data](#15-cluster-shows-connected-but-scan-results-never-populate) |
| Cluster disconnects randomly, logs show nothing — and it's public, or it's AKS | [Known Platform Limitations](#known-platform-limitations-not-fixable-by-the-customer) |

## Step 2: Match to a Known Failure Category

Each category below follows the same shape: what it looks like, the one-line fix, why it happens, and the exact steps.

### Install-time categories

#### 1. Can't reach the tunnel endpoint (timeout / TLS handshake)
- **Symptom**: pod logs show repeated `dial tcp ... i/o timeout` or `TLS handshake timeout` from `frpc`; the connector retries with backoff (starts at 15s, doubles up to a 60s cap) but never gets past the first connection attempt.
- **Fix**: allow outbound TCP 443 from the cluster to `tunnelAddr`.
- **Why**: a firewall or NetworkPolicy is blocking that egress path. (If the firewall logs show UDP traffic instead, ignore it — `frp` is TCP-only, so that's unrelated noise, not this issue.)
- **Steps**:
  1. Confirm `tunnelAddr` is copied exactly from the Orca install command (don't reuse one from a different cluster/region).
  2. The tunnel-client image has no `curl` built in — test from a throwaway debug pod instead: `kubectl run tmp-curl --rm -it --image=curlimages/curl -n <namespace> -- curl -v https://<tunnelAddr>:443`.
  3. If that fails, check egress firewall rules / NetworkPolicies allow outbound TCP 443 to Orca's static IP allowlist and to the `tunnelAddr` FQDN specifically (see **Connecting Clusters** doc).
  4. If a corporate proxy is required to reach the internet at all, this is really the **proxy misconfiguration** category — see Category 12.

#### 2. RBAC / permission errors applying the chart
- **Symptom**: `helm install` fails outright (often on the `ClusterRole`/`ClusterRoleBinding`/`ServiceAccount` objects), or the chart installs but pod logs show `forbidden`/`Unauthorized` when listing cluster resources.
- **Fix**: grant the installer cluster-scoped RBAC rights, or fix the deployed `ClusterRole`'s rules.
- **Why**: the identity running `helm install` lacks rights to create cluster-scoped RBAC objects, or the deployed `ClusterRole` (`orca-k8s-collector-role` by default) is missing a resource/apiGroup the connector needs.
- **Steps**:
  1. Confirm the installer has sufficient cluster-scoped rights to create the chart's RBAC objects.
  2. For post-install `forbidden` errors: `kubectl auth can-i --list --as=system:serviceaccount:<namespace>:orca-k8s-collector` and diff against the chart's `clusterRole.rules`.
  3. The `ClusterRole` can be safely narrowed via a values override if company policy requires it (e.g. dropping `secrets` access) — core scanning still works without `secrets` `get`/`list`, though some findings that depend on secret metadata will be reduced. A working no-secrets override, confirmed against a real customer case:
     ```yaml
     # orca-values-no-secrets.yaml
     clusterRole:
       name: "orca-k8s-collector-role"
       rules:
         - apiGroups: [""]
           resources: ["configmaps", "endpoints", "namespaces", "pods", "pods/log",
                       "serviceaccounts", "nodes", "services", "persistentvolumes",
                       "persistentvolumeclaims"]  # "secrets" removed
           verbs: ["get", "list"]
         - apiGroups: ["apps"]
           resources: ["daemonsets", "deployments", "replicasets", "statefulsets"]
           verbs: ["get", "list"]
         - apiGroups: ["networking.istio.io"]
           resources: ["gateways", "sidecars", "virtualservices"]
           verbs: ["get", "list"]
         - apiGroups: ["rbac.authorization.k8s.io"]
           resources: ["clusterroles", "clusterrolebindings", "roles", "rolebindings"]
           verbs: ["get", "list"]
         - apiGroups: ["networking.k8s.io"]
           resources: ["networkpolicies", "ingresses"]
           verbs: ["get", "list"]
         - apiGroups: ["extensions"]
           resources: ["ingresses"]
           verbs: ["get", "list"]
         - apiGroups: ["policy"]
           resources: ["podsecuritypolicies"]
           verbs: ["get", "list"]
         - apiGroups: ["argoproj.io"]
           resources: ["rollouts", "experiments"]
           verbs: ["get", "list"]
         - apiGroups: ["batch"]
           resources: ["jobs", "cronjobs"]
           verbs: ["get", "list"]
     ```
     Apply with `helm install/upgrade -f orca-values-no-secrets.yaml`.

#### 3. Image pull failures
- **Symptom**: pod stuck in `ImagePullBackOff` / `ErrImagePull`.
- **Fix**: allow outbound access to the image registry, or fix `image.pullSecrets`.
- **Why**: outbound access to the registry (`public.ecr.aws` or `ghcr.io`, whichever the install command references) is blocked, or `image.pullSecrets` is missing/wrong for a private mirror.
- **Steps**:
  1. `kubectl describe pod <pod>` to see the exact image/registry being pulled.
  2. Confirm outbound access to that registry hostname; set `image.repository`/`image.pullSecrets` if mirroring internally.
  3. If the install is more than a few chart versions old, also suggest upgrading — recent releases fix both CVEs and unrelated bugs (see Category 9 for a concrete example of a version-lag bug).

#### 4. Incorrect, missing, or malformed `--set` parameters
- **Symptom**: `helm install` succeeds but the pod crash-loops immediately, or logs show a rejection at the `frpc` login step, e.g.:
  ```
  [E] [client/service.go:363] cloud_account not found
  [W] [client/service.go:381] connect to server error: cloud_account not found
  login to the server failed: cloud_account not found. With loginFailExit enabled, no additional retries will be attempted
  ```
- **Fix**: re-copy the exact install command from Orca's cluster-onboarding screen instead of reusing/editing an old one.
- **Why**: one of `tunnelAddr`, `tunnelId`, `tunnelToken`, `clusterName`, `region`, `clusterType`, `cloudVendorId` is missing, blank, or wrong — most commonly `cloudVendorId` pasted as the wrong identifier for the cloud vendor (e.g. a full OCI tenancy OCID instead of just its trailing unique-ID segment, or a cloud-account ID substituted for the real cloud-provider ID) or a `tunnelToken`/`tunnelId` copied from a different cluster's install command.
- **Steps**:
  1. Confirm `clusterType` is one of `eks`/`aks`/`gke`/`k8s`. It auto-detects for EKS/AKS/GKE if omitted, but **self-managed clusters must set it explicitly** (`clusterType=k8s`) — this is a common gap in Terraform-based installs.
  2. Confirm `cloudVendorId` matches the format Orca expects for that vendor (see the **Connecting Clusters** doc's self-managed cluster section for the exact identifier format per vendor).
  3. Prefer `existingSecret` over inline `--set tunnelId=... --set tunnelToken=...` where possible — it keeps credentials out of shell history/CI logs and out of `helm get values` output:
     ```yaml
     apiVersion: v1
     kind: Secret
     metadata:
       name: existing-secret
       namespace: orca-security   # must match the release's namespace
     stringData:
       tunnelId: <tunnelIdValue>
       tunnelToken: <tunnelTokenValue>
     ```
     then `--set existingSecret=existing-secret`.
  4. If credentials may have been compromised or just need rotating without a full reinstall, contact Orca support to rotate the tunnel credentials without a reinstall.

#### 5. Kubernetes version incompatibility
- **Symptom**: the chart installs but the pod fails on startup with an API compatibility error, or specific chart resources fail to apply.
- **Fix**: upgrade the cluster.
- **Why**: cluster is below the connector's minimum supported version (1.16+).
- **Steps**: confirm with `kubectl version`; this needs a cluster upgrade — not something the skill can work around.

#### 6. Misuse of `automation=true`, or duplicate/conflicting cluster entries
- **Symptom**: Orca's cluster list shows two entries for what should be one cluster — a "self-managed" entry and a properly-typed one (EKS/AKS/GKE) — both referencing the same physical cluster.
- **Fix**: delete the stale self-managed row via the delete API — this is self-service, not an escalation.
- **Why**: `automation=true` exists for clusters created by automation that Orca hasn't auto-discovered yet. Setting it (or otherwise onboarding as self-managed) on a cluster that's already visible to Orca through its cloud account — or that a later cloud-account scan auto-discovers — creates a second, duplicate entry. Self-managed rows don't automatically get cleaned up when auto-discovery later finds the same cluster.
- **Steps**:
  1. Before using `automation=true`, confirm the cluster isn't already discoverable under the customer's connected cloud account.
  2. If a duplicate already exists: in Cluster Management, identify the **self-managed** row specifically (filter by cluster name — don't delete the correctly-typed EKS/AKS/GKE row) and note its `cluster_id` and `cloud_account_id`.
  3. This delete is destructive and cannot be undone from the UI — before calling it, confirm the exact `cluster_id`/`cloud_account_id` pair with the user so the correct row is removed. Then call `DELETE /api/cloudaccount/{cloud_account_id}/k8s_cluster/{cluster_id}` (see [delete-specific-k8-cluster](https://docs.orcasecurity.io/docs/en/delete-specific-k8-cluster)). Any role with `kubernetes.write` permission (e.g. org admin) can call this — it soft-deletes the self-managed row and it disappears from Cluster Management immediately.
  4. If the delete doesn't stick, or you're not sure which row is the stale one, escalate (Step 4) with both cluster entries' names/IDs rather than guessing and deleting the wrong one.

#### 7. Resource constraints
- **Symptom**: pod `OOMKilled`, or stuck `Pending` with insufficient-CPU/memory scheduling events.
- **Fix**: free node capacity, or override `resources` in the install command.
- **Why**: node doesn't have enough allocatable CPU/memory for the chart's `resources.requests`/`resources.limits`.
- **Steps**: `kubectl describe pod` for the exact values in effect — don't assume defaults from memory, they change between chart versions. `helm get values <release>` shows what's actually applied.

#### 8. Custom namespace issues
- **Symptom**: `helm install` fails saying a referenced secret doesn't exist, even though `kubectl get secret` shows it exists somewhere in the cluster.
- **Fix**: make sure the secret and the release are in the same namespace.
- **Why**: installing into a non-default namespace needs both `--namespace <ns>` and `--create-namespace` (if new); an `existingSecret` (with `tunnelId`/`tunnelToken` keys) must live in that *same* namespace as the release — a secret created in `default` isn't visible to a release installed into e.g. `orca-security`.
- **Steps**: confirm the `--namespace`/`--create-namespace` flags match where the secret was created; `kubectl get secret <name> -n <namespace>` to check directly.

### Runtime / post-install categories

#### 9. Service-account token expired (K8s 1.30+)
- **Symptom**: pod `Running`, tunnel connects fine, but calls to the cluster's own API fail with `Unauthorized`/`401`, e.g.:
  ```
  {"kind":"Status","apiVersion":"v1","status":"Failure","message":"Unauthorized","reason":"Unauthorized","code":401}
  ```
- **Fix**: upgrade the K8s Connector to the latest chart version.
- **Why**: bound service-account tokens have had an expiry since around Kubernetes 1.21, but many clients kept working past that expiry without the API server rejecting the stale token. Starting around Kubernetes 1.30, the API server began enforcing that expiry and rejecting stale tokens outright. The Connector only gained automatic service-account token rotation in **helm chart v1.0.39 / app v1.0.33** — an older Connector on a 1.30+ cluster will hit this every time its token goes stale.
- **Steps**:
  1. Check the cluster's Kubernetes version (`kubectl version`) and the Connector's chart/app version (`helm list -n <namespace>`, or the image tag via `kubectl describe pod`).
  2. If the cluster is 1.30+ and the Connector predates v1.0.39 (helm)/v1.0.33 (app), upgrade it — this alone resolves the vast majority of these cases.
  3. If it's already on a current version and still failing, collect pod logs (`kubectl logs -n <namespace> $(kubectl get pods -n <namespace> --no-headers -o custom-columns=":metadata.name" | grep tunnel)`) and escalate (Step 4) — this is a narrower case that needs engineering eyes.

#### 10. NetworkPolicy blocks API-server egress causing `context deadline exceeded`
- **Symptom**: pod `Running`, tunnel up, but logs show `context deadline exceeded` when the connector tries to reach the in-cluster API server to list resources.
- **Fix**: confirm NetworkPolicies allow egress from the tunnel pod to the API server's Service IP.
- **Why**: a NetworkPolicy is blocking egress from the tunnel pod to the in-cluster API server, so requests time out. (If it's actually a `forbidden`/`Unauthorized` response rather than a timeout, that's an RBAC issue — see Category 2 instead.)
- **Steps**: check NetworkPolicies applied to the tunnel pod's namespace/labels allow egress to the API server's Service IP/port (typically the `kubernetes` Service in `default`, port 443); temporarily loosening the policy to confirm this is the cause, then scoping it correctly, is the fastest way to verify.

#### 11. Tunnel establishes, then drops on auth/token errors, or a stale tunnel target
- **Symptom**: logs show a successful initial connection, then periodic disconnects citing auth/token rejection; or re-onboarding fails with something like:
  ```json
  "status": ["K8s Tunnel client is unreachable"]
  ```
  referencing a `tunnel_target_id` that should no longer exist.
- **Fix**: if credentials are the issue, confirm `tunnelId`/`tunnelToken` weren't reused from another cluster. If this is a stale entry left over after a delete/re-onboard, escalate — it needs an Orca-side cleanup, but it's a quick one for support to resolve.
- **Why**: usually a `tunnelToken` reused from a different cluster's install, or — if this is a reconnect after a previous tunnel was supposedly deleted — a **stale tunnel target** left over on Orca's side.
- **Steps**:
  1. Confirm the `tunnelId`/`tunnelToken` pair is unmodified from the original install command.
  2. **Check whether this cluster actually needs the Connector at all** — a recurring cause of this exact error is a customer running the Connector on a cluster that's already public. If so, the fix isn't cleanup, it's removing the Connector. `helm uninstall` is destructive — confirm the exact release name and namespace with the user before running it: `helm uninstall <release> -n <namespace>` **first**, then ask Orca to clean up the tunnel target — doing it in the other order just recreates the tunnel entry.
  3. If neither applies and this follows a prior delete/re-onboard, stale-tunnel cleanup is not customer-self-serviceable — escalate (Step 4) with the `tunnel_target_id` (or cluster/tunnel IDs from the error) so support can clear it.

#### 12. Proxy misconfiguration
- **Symptom**: works with no proxy, breaks once `proxyURL` is set; or the environment requires a proxy but none is configured.
- **Fix**: validate the `proxyURL` scheme/credentials, and rule out TLS interception if it still fails.
- **Why**: `proxyURL` follows FRP's URL format — scheme, optional embedded credentials, host, and port — with `http`, `socks5`, and `ntlm` schemes all supported. A wrong scheme, bad credentials, or a proxy allowlist that doesn't include the tunnel endpoint will break the connection.
- **Steps**:
  1. Validate the `proxyURL` scheme and credentials. Supported schemes are `http`, `socks5`, and `ntlm`, each optionally with credentials placed immediately before the host — e.g. a `socks5` proxy with authentication looks like `socks5://[credentials]@proxy.company.com:1080`, and one with no authentication drops the `[credentials]@` segment entirely.
  2. Confirm the proxy itself permits egress to the tunnel endpoint, then re-check pod logs for the specific `frpc` connection error.
  3. **If `proxyURL` is set correctly and the proxy allows the connection but the tunnel still fails on TLS**, ask whether it's a **transparent/TLS-inspecting proxy** — this class of proxy replaces the certificate chain in transit, and the connector will reject the swapped cert since it expects Orca's own certificate. The fix here is a proxy-side exclusion for the tunnel FQDN from TLS inspection, not a Connector-side change.

#### 13. DNS resolution failures
- **Symptom**: logs show `no such host` or similar DNS failures resolving `tunnelAddr`.
- **Fix**: fix cluster DNS resolution for the tunnel FQDN.
- **Why**: cluster DNS (CoreDNS/kube-dns) can't resolve the Orca tunnel FQDN — common in air-gapped or custom-DNS environments.
- **Steps**: from a debug pod in the cluster, resolve `tunnelAddr` directly (e.g. `nslookup`/`getent hosts`); if it fails, check the cluster's DNS config / custom upstream resolvers can reach public DNS or have an internal record for the Orca FQDN.

#### 14. OpenShift-specific SCC issues
- **Symptom**: pod fails to schedule or start, only on OpenShift, with an SCC-related admission error (e.g. "unable to validate against any security context constraint").
- **Fix**: set `--set openshift=true` at install time, and confirm the target SCC exists.
- **Why**: on OpenShift, `openshift: true` must be set at install time. When set, the chart adds an `openshift.io/scc` annotation on the Deployment *and* a `ClusterRole` rule granting `use` on the named SCC (`security.openshift.io` apiGroup, default name `nonroot-v2`, or the `openshiftSCC` override) to the connector's ServiceAccount via the existing `ClusterRoleBinding` — this is the correct, automatic way OpenShift grants an SCC via RBAC, so no manual `oc adm policy` step should be needed. The two most common failure modes instead: (1) `openshift: true` was never set, so the pod falls under the cluster's default `restricted`-type SCC, which typically rejects the chart's pinned `runAsUser`/`fsGroup` (1001); or (2) `openshiftSCC` points at a name that doesn't exist in the target cluster — the RBAC rule applies without error, but pod admission then fails because no matching SCC can be found.
- **Steps**: confirm `openshift: true` was actually set on install (`helm get values <release>`); confirm the named SCC (`openshiftSCC`, default `nonroot-v2`) exists in the cluster (`oc get scc <name>`) and is compatible with the chart's pod/container security context (non-root, all capabilities dropped, read-only root filesystem); if it doesn't exist, either create it or point `openshiftSCC` at an existing compatible SCC.

#### 15. Cluster shows "connected" but scan results never populate
- **Symptom**: tunnel pod healthy, no errors in its logs, Orca console shows the cluster as connected — but no inventory/scan data appears after a reasonable wait.
- **Fix**: check if the cluster's cloud account is BYOC — if so, this is a platform limitation, not a connector bug.
- **Why**: the connector's job (a healthy tunnel) is done at this point — this is almost always an Orca-side scanning/discovery issue, not a connector defect. One specific known case: **BYOC (Bring-Your-Own-Cloud) accounts do not run Kubernetes scanning by design** — a cluster attached to a BYOC cloud account will register and show connected but never get scanned, with no workaround on the customer's side other than attaching the cluster to a standard (non-BYOC) cloud account instead.
- **Steps**: check whether the cluster's associated cloud account is a BYOC account. Otherwise, treat it as an escalation case (Step 4): this can't be diagnosed further from the customer's side.

## Step 3: Ask Clarifying Questions When Input Is Ambiguous

Don't guess a category from a vague report. Ask:
- "Can you share the tunnel pod's logs (`kubectl logs <pod> -n <namespace>`) and `kubectl describe pod <pod> -n <namespace>`?"
- "Is this cluster reachable from outside (public), or private/self-managed? If it's public, it may not need the Connector at all."
- "Is this a managed cluster (EKS/AKS/GKE) or self-managed/on-prem?"
- "Did `helm install`/`helm upgrade` complete successfully, or did the command itself fail?"
- "Has this connector ever worked, or has it never connected since install?"
- "What Kubernetes version is the cluster on, and what Connector chart/app version is installed?"
- "Are you behind a corporate proxy or air-gapped network? If a proxy, is it a transparent/TLS-inspecting one?"
- "Is this cluster on OpenShift?"
- "Was this cluster (or its cloud account) previously onboarded and then removed?"

## Step 4: Escalation / Handoff

If the category can't be resolved from the customer's side — including any of the known platform limitations above — produce a clean handoff summary rather than leaving the customer stuck:

```
=====================================================================
K8S CONNECTOR — SUPPORT HANDOFF
=====================================================================
CLUSTER TYPE       <eks | aks | gke | k8s / self-managed>
CONNECTOR VERSION  <from pod logs / image tag>
K8S VERSION        <from kubectl version>
INSTALL OR RUNTIME <install-time | post-install>
CATEGORY           <matched category, or "unmatched">
WHAT WAS TRIED      <steps already attempted>
RELEVANT IDS        <tunnelId / tunnel_target_id / cluster name, if known>
LOGS ATTACHED       <yes/no — attach kubectl logs + describe output>
=====================================================================
```

## Output Format

```
=====================================================================
K8S CONNECTOR TRIAGE
=====================================================================
STAGE:      <install-time | runtime>
CATEGORY:   <matched category name>
CONFIDENCE: <high | medium — ask clarifying question if medium/low>

QUICK FIX: <one plain-language sentence — the action to take, before any detail>

ROOT CAUSE:
  <one-line explanation>

REMEDIATION:
  1. <step>
  2. <step>
  ...

REFERENCE: <relevant doc section>
=====================================================================
```

If nothing matches confidently, skip straight to Step 3's clarifying questions instead of forcing a category.

## Known Platform Limitations (not fixable by the customer)

Recognize these so the skill doesn't send a customer in circles trying to self-fix something that needs an Orca-side change, or chase a known bug as if it were their own misconfiguration:
- **BYOC accounts don't run Kubernetes scanning** (Category 15) — by design, not a bug.
- **Stale tunnel targets** can block re-onboarding or cause auth drops (Category 11) and require Orca-side cleanup — fast for Orca support to clear; open a ticket.
- **AKS clusters have a known issue with repeated tunnel crashes after control-plane connectivity resets** — if you see this signature, escalate to Orca support rather than continuing to troubleshoot it as a customer-side problem.

Duplicate self-managed/auto-discovered cluster entries (Category 6) are **no longer** in this list — they're now self-service via the delete API in that category.

## Reference Docs

- [Connecting Clusters Using Kubernetes Connector](https://docs.orcasecurity.io/docs/connecting-clusters-using-kubernetes-connector) — install steps, static IP allowlist, self-managed cluster identifier formats, OpenShift deployment notes.
- [Delete a specific K8s cluster](https://docs.orcasecurity.io/docs/en/delete-specific-k8-cluster) — the self-service API for removing a stale/duplicate cluster entry (Category 6).
- Proxy (`proxyURL`) and OpenShift (`openshift`, `openshiftSCC`) install parameters are covered inline in Categories 12 and 14 above — there is no additional dedicated public doc page beyond the **Connecting Clusters** guide linked above.

## Implementation Notes

1. **Validate before launch** against a sample of real past support tickets for the K8s Connector — the categories above were cross-checked against real customer cases, but coverage should be re-confirmed periodically as the connector evolves.
2. **Don't guess when input is ambiguous** — a wrong category sends the customer down the wrong remediation path and erodes trust in the skill faster than admitting uncertainty and asking a follow-up.
3. **Always sanity-check "does this cluster need the Connector at all", then distinguish install-time from runtime** (Step 1) — most of the categories only make sense once you know which side of that line the customer is on, and a surprising number of "connectivity" reports are actually a public cluster that never needed the Connector.
4. **Recognize platform limitations and known bugs as out of customer scope** — don't ask a customer to retry indefinitely against something engineering needs to fix; escalate cleanly instead, citing the tracking ticket when one exists.
5. **Lead every answer with the one-line fix, not the mechanism** — this audience is technical, but still wants the actionable step first and the "why" as backup, not the reverse. Keep the Symptom/Fix/Why/Steps shape for any new category added later.
