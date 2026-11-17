---
name: kubernetes-security
description: Harden a Kubernetes cluster's data plane and control plane. Covers Pod Security Standards (Restricted, Baseline, Privileged), RBAC with least privilege, NetworkPolicy default-deny, secrets management without raw env vars, admission controllers (Kyverno, OPA Gatekeeper), image scanning, and audit logging. Invoke when provisioning a new cluster, inheriting one, or before adding a new tenant to a shared cluster.
---

# Kubernetes Security

A pragmatic baseline for a single Kubernetes cluster running a small-team workload. Skews toward "I have a cluster and need it to not be the cause of an incident" — not a full CIS Benchmark for regulated environments. Most managed-K8s providers ship sensible defaults at the control-plane layer; the data-plane (your workloads) is where the work is.

## When to invoke

- Provisioning a new cluster
- Inheriting a cluster with no documented hardening
- Before adding a new tenant / team / workload to a shared cluster
- After a K8s security advisory affecting your version
- Periodic re-audit (quarterly)
- Multi-tenant SaaS where customer workloads share infrastructure

## Step 1 — Cluster baseline

Before workload hardening, the cluster itself.

```bash
# What version? Is it supported?
kubectl version --short
# K8s has a ~14-month support window. Unsupported = unpatched CVEs.

# Who can reach the API?
kubectl cluster-info
# For managed clusters, check the provider's "API endpoint" access setting:
# - Private endpoint, restricted CIDRs, or behind a bastion is correct
# - "Public, open to 0.0.0.0/0" is a finding

# Audit log enabled?
# For EKS/GKE/AKS: check the cluster's "audit logging" / "control-plane logging" setting
# Self-hosted: --audit-log-path on the API server
```

Patterns:

- **Restrict the API endpoint.** Public + open is the worst default. Use private endpoint + bastion, or public + CIDR allowlist + IAM auth at minimum.
- **Enable control-plane audit logging.** Without it, an incident has no record. Ship to a log destination outside the cluster (so a compromise cannot wipe its own audit trail).
- **Pin to a supported version**, automate patching to within the support window.
- **Encrypt etcd at rest.** Default-on for EKS, GKE, AKS. Self-hosted: configure `--encryption-provider-config`.

## Step 2 — Pod Security Standards

Since K8s 1.25, **Pod Security Admission** is built-in. There are three policy levels:

| Level | What it allows | When to use |
|---|---|---|
| **Privileged** | Everything | System namespaces only (kube-system, ingress controllers that need it) |
| **Baseline** | No privileged escalation, no host networking, no hostPath | Default for most workloads |
| **Restricted** | The above plus: non-root user, read-only root filesystem, drop all capabilities, seccomp profile | Production application workloads |

Apply per namespace:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/audit: restricted
```

`enforce` rejects non-compliant pods. `warn` returns a warning to the user. `audit` logs to the audit log.

For workloads that cannot meet `restricted` (legacy containers needing root), use `baseline` and document why. Anything in `privileged` mode is a finding unless it's a known infrastructure component.

Common adjustments to make existing workloads `restricted`-compliant:

```yaml
# In the pod spec
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault

# Per container
containers:
- name: app
  securityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    capabilities:
      drop: [ALL]
    runAsNonRoot: true
```

Anything writable (cache, temp) goes to an `emptyDir` volume; the root filesystem stays read-only.

## Step 3 — RBAC and ServiceAccounts

The single most common K8s misconfiguration: every workload running as the `default` ServiceAccount of its namespace, which often has more rights than the workload needs.

```bash
# What can the default ServiceAccount in 'production' do?
kubectl auth can-i --list --as=system:serviceaccount:production:default -n production

# What ServiceAccounts have cluster-admin or near-admin rights?
kubectl get clusterrolebindings -o json \
  | jq -r '.items[] | select(.roleRef.name == "cluster-admin") | "\(.metadata.name) -> \(.subjects | map(.name) | join(","))"'
```

Patterns:

- **One ServiceAccount per workload.** Don't use `default`.
- **`automountServiceAccountToken: false`** on workloads that don't talk to the K8s API. Most don't.
- **Bind to a Role (namespace-scoped) before a ClusterRole** — `ClusterRoleBinding` should be rare and justified.
- **Avoid `*` verbs and `*` resources** in Role rules.
- **Audit `system:authenticated` and `system:anonymous`** — these should have minimal permissions, never cluster-admin.

Example tight Role:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["app-config"]
  verbs: ["get"]
```

The resource name pin matters — `verbs: [get]` on all configmaps is too broad if the workload only reads one.

## Step 4 — NetworkPolicy (default-deny)

By default, every pod can talk to every other pod, in any namespace. That's a flat network — one compromised workload pivots freely.

```yaml
# Default-deny ingress AND egress in a namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

Then explicitly allow what's needed:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-allow
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes: [Ingress, Egress]
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:                            # DNS
    - namespaceSelector: {}
      podSelector:
        matchLabels:
          k8s-app: kube-dns
    ports:
    - protocol: UDP
      port: 53
```

**NetworkPolicy requires a compatible CNI** (Calico, Cilium, Weave, Antrea, AWS VPC CNI with policy enabled). If the CNI ignores NetworkPolicy, the manifests are decoration.

## Step 5 — Secrets management

K8s `Secret` objects are base64-encoded, not encrypted at the application level. At rest in etcd they are encrypted only if you configured encryption. They are still accessible to anyone with `get secrets` in the namespace.

Patterns, from worst to best:

1. **Env vars from `kind: Secret`** — workable but secrets leak via `kubectl describe pod`, env-dumping logs, child processes
2. **Mounted as files via volume** — better; not in env, lifecycle is the pod
3. **External secret manager via CSI driver / External Secrets Operator** — secrets stay in Vault / AWS Secrets Manager / GCP Secret Manager, K8s only sees references
4. **Workload Identity / IRSA** — workload assumes a cloud IAM role directly, no secret crosses K8s at all

Standard tooling:

- **External Secrets Operator** (external-secrets.io) — syncs from cloud secret managers
- **SealedSecrets** (Bitnami) — encrypt secrets in the repo with a cluster-specific key; the controller decrypts at apply time
- **SOPS + age** — encrypted secrets in Git, decrypted at apply time via a Flux/Argo plugin
- **HashiCorp Vault** with the Vault Agent injector

For new clusters, prefer External Secrets + a cloud secret manager. SOPS is a good fit for GitOps-heavy teams.

## Step 6 — Admission controllers

Policy-as-code that blocks non-compliant resources at API time. Two common choices:

- **Kyverno** — K8s-native syntax, easier learning curve
- **OPA Gatekeeper** — Rego policies, more flexible, used at scale

Baseline policies worth enforcing:

- Reject images from non-allowlisted registries
- Reject images tagged `:latest` (only digests or version tags allowed)
- Reject containers without `runAsNonRoot: true` (catches workloads that slipped past PSS)
- Reject NetworkPolicy-less namespaces in production
- Require resource limits (CPU/memory) on every container
- Reject `hostNetwork: true`, `hostPID: true`, `hostIPC: true` outside of audited exceptions

```yaml
# Kyverno example — require resource limits
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resources
spec:
  validationFailureAction: enforce
  rules:
  - name: validate-resources
    match:
      any:
      - resources:
          kinds: [Pod]
    validate:
      message: "Resource limits are required."
      pattern:
        spec:
          containers:
          - resources:
              limits:
                memory: "?*"
                cpu: "?*"
```

## Step 7 — Image hygiene

- **Scan every image before it lands in the cluster.** Trivy, Grype, or your registry's built-in scanner. See [`docker-container-security`](../docker-container-security/SKILL.md).
- **Pull by digest, not tag.** `myapp@sha256:abc123...` is immutable; `myapp:v1.2.3` can be repushed.
- **Use a private registry** for app images; the public Docker Hub is a supply-chain surface.
- **Enable registry-side admission** that rejects unsigned / unscanned images. Sigstore / cosign for signing; Kyverno or Gatekeeper for enforcement.

## Step 8 — Cluster + control-plane hygiene

- **kubeconfigs are credentials.** Treat them like SSH private keys. Rotate on team change. Scope per-user.
- **No long-lived static admin token.** Use SSO (cloud provider's OIDC) or short-lived tokens.
- **Don't `kubectl exec` in production casually.** It bypasses normal audit logging in some setups. Configure cluster audit policy to capture exec events explicitly.
- **`kubectl proxy`** opens the API to localhost without auth — never on a shared dev machine.
- **Restrict who can create resources in `kube-system`** — that namespace's pods can compromise the cluster.

## Step 9 — Multi-tenancy (if applicable)

If multiple teams or customers share a cluster, hard isolation is hard. Options:

- **Namespace per tenant** + strict RBAC + NetworkPolicy + ResourceQuotas — minimum bar
- **vCluster / Capsule** — virtual clusters inside one cluster, more isolated but operational overhead
- **Cluster per tenant** — strongest isolation, highest cost

A single-cluster multi-tenant setup with shared nodes is **soft isolation**. Container escape and kernel CVEs can cross tenants. For security-sensitive multi-tenancy, run separate node pools per tenant or move to per-tenant clusters.

## Common findings on inherited clusters

Walk this list against any cluster you're auditing:

- API endpoint open to `0.0.0.0/0`
- Pod Security Admission not configured (or only at `audit`, not `enforce`)
- Workloads using `default` ServiceAccount
- ClusterRoleBindings to `cluster-admin` for human accounts or generic ServiceAccounts
- No NetworkPolicy in any namespace (flat network)
- CNI does not support NetworkPolicy (manifests present but ineffective)
- Secrets in env vars throughout
- Images pulled by `:latest`
- No image scanning
- No admission controller
- Containers running as root (`runAsUser: 0` or unspecified)
- `privileged: true` on application workloads
- `hostNetwork: true` or `hostPath:` volumes outside system pods
- Audit logging disabled or sent only to the cluster itself
- kubeconfigs for `cluster-admin` shared on multiple machines
- etcd backups absent or unencrypted

## Quick audit script

```bash
#!/usr/bin/env bash
echo "=== Cluster version ==="
kubectl version --short

echo "=== PSS labels per namespace ==="
kubectl get ns -o json | jq -r '.items[] | "\(.metadata.name)\t\(.metadata.labels // {} | to_entries | map(select(.key | startswith("pod-security.kubernetes.io"))) | from_entries)"'

echo "=== ServiceAccounts with cluster-admin ==="
kubectl get clusterrolebindings -o json | jq -r '.items[] | select(.roleRef.name == "cluster-admin") | "\(.metadata.name)\t\(.subjects // [] | map("\(.kind):\(.namespace // "-"):\(.name)") | join(", "))"'

echo "=== Namespaces without NetworkPolicy ==="
for ns in $(kubectl get ns -o jsonpath='{.items[*].metadata.name}'); do
  count=$(kubectl get networkpolicy -n "$ns" 2>/dev/null | grep -c -v NAME)
  [ "$count" -eq 0 ] && echo "$ns"
done

echo "=== Pods running as root ==="
kubectl get pods -A -o json | jq -r '.items[] | select(.spec.securityContext.runAsNonRoot != true and (.spec.containers[]?.securityContext.runAsNonRoot // false) != true) | "\(.metadata.namespace)/\(.metadata.name)"' | head -30

echo "=== Pods using :latest ==="
kubectl get pods -A -o json | jq -r '.items[] | "\(.metadata.namespace)/\(.metadata.name)\t\(.spec.containers[].image)"' | grep ':latest' | head -30
```

## Checklist

- [ ] K8s version is supported; auto-patching within the window
- [ ] API endpoint restricted (private or CIDR-allowlisted)
- [ ] Control-plane audit logging on, shipped off-cluster
- [ ] etcd encryption at rest
- [ ] Pod Security Standards: `restricted` enforced in app namespaces
- [ ] Every workload has a dedicated ServiceAccount with minimal RBAC
- [ ] `automountServiceAccountToken: false` for workloads not calling K8s API
- [ ] Default-deny NetworkPolicy in every namespace; explicit allows
- [ ] CNI supports NetworkPolicy enforcement
- [ ] Secrets via External Secrets / SealedSecrets / Vault, not raw `kind: Secret` in env
- [ ] Image scanning before admission
- [ ] Images pinned by digest or version, not `:latest`
- [ ] Admission controller (Kyverno / Gatekeeper) enforcing baseline policies
- [ ] No `privileged`, `hostNetwork`, `hostPID`, `hostIPC` in app workloads
- [ ] kubeconfigs scoped per user, rotated on offboarding
- [ ] Multi-tenancy strategy documented (or single-tenant explicitly)

## What this skill will not do

- Replace a full CIS Kubernetes Benchmark for regulated environments
- Help compromise a cluster you do not own
- Recommend `privileged: true` or `hostNetwork: true` for application workloads
