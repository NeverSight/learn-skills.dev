---
name: k3s
description: K3s lightweight Kubernetes — when to use Docker, Compose, K3s, or larger Kubernetes platforms; edge devices, homelabs, Deployments, workers, CronJobs, shared Redis/Valkey, storage, autoscaling, and external secret managers.
---

# K3s — Lightweight Kubernetes

Use this skill when deciding whether to run containers with plain Docker/Compose, K3s, or a larger Kubernetes platform, and when writing K3s manifests for edge devices, homelabs, small production clusters, workers, CronJobs, shared storage, Redis/Valkey, autoscaling, or external secret-manager integration.

K3s is a CNCF-certified, lightweight Kubernetes distribution packaged as a small single binary. It defaults to SQLite for single-server clusters and bundles useful components such as containerd, Flannel CNI, CoreDNS, Traefik ingress, ServiceLB, local-path-provisioner, and a network-policy controller.

Detailed decision matrix and caveats: [`references/decision-and-operations.md`](references/decision-and-operations.md).
Starter manifests:

- [`templates/simple-device.yaml`](templates/simple-device.yaml) — one edge device with host device access.
- [`templates/web-workers-cron-valkey.yaml`](templates/web-workers-cron-valkey.yaml) — web app, multiple worker deployments, CronJob, shared Valkey, PVC.
- [`templates/external-secrets-vault.yaml`](templates/external-secrets-vault.yaml) — External Secrets Operator + Vault-style SecretStore scenario.

## First decision: Docker, Compose, K3s, or bigger Kubernetes?

| Use | Best fit | Why |
|---|---|---|
| One process or one container on one host | Plain Docker + systemd | Lowest cognitive load; easiest logs/restart/backup. |
| 2-10 tightly coupled services on one host | Docker Compose | Simple local stack, networks, volumes, healthchecks. |
| Multiple hosts, self-healing, rolling updates, services, ingress, scheduled jobs | K3s | Kubernetes primitives without full distro overhead. |
| Edge/IoT/ARM/homelab/small production cluster | K3s | Lightweight, batteries included, runs on modest hardware. |
| Multi-region, strict compliance, cloud-native LB/CSI/IAM, many teams | Managed Kubernetes / RKE2 / Talos / OpenShift | Better lifecycle, policy, identity, HA, and support surface. |
| Very large or regulated platform | Managed Kubernetes or full platform stack | Add GitOps, policy, observability, service mesh only when the org can operate them. |

Rule of thumb: **do not choose K3s just because it is fashionable**. Choose it when Kubernetes primitives solve real problems: desired-state reconciliation, rollouts, service discovery, scheduling, autoscaling, CronJobs, shared in-cluster services, or multi-node placement.

## K3s install defaults to know

```bash
# Single-node quick start; review flags before running on real hosts.
curl -sfL https://get.k3s.io | sh -
sudo k3s kubectl get nodes
sudo cat /etc/rancher/k3s/k3s.yaml
```

Before production use:

- Confirm node names are unique; use `--node-name` or `--with-node-id` for recycled/automated hosts.
- Use SSD-backed disks, especially for server/datastore nodes. Avoid SD cards for write-heavy control-plane storage.
- Know default ports: 6443 API, Flannel VXLAN 8472/udp, kubelet 10250, etcd 2379-2380 for HA embedded etcd.
- Do **not** expose Flannel VXLAN/WireGuard ports to the internet.
- For Raspberry Pi, enable cgroups if the OS does not enable memory cgroups by default.

## Scenario ladder

### 1. Simple device / edge node

Use K3s when a single Linux device needs declarative lifecycle, automatic restart, logs, updates, and maybe one host device. Keep it single-node unless remote scheduling actually helps.

Pattern:

- One `Namespace` per app or device group.
- `Deployment` with `replicas: 1`.
- `nodeSelector`/node labels to pin the workload to the node with the device.
- Prefer a Kubernetes device plugin for production fleets. If using `hostPath` device mounts, isolate the namespace and expect `privileged: true` or equivalent device-cgroup permissions.
- `hostPath` only for real host files/devices; keep it narrow.

Copy: [`templates/simple-device.yaml`](templates/simple-device.yaml).

### 2. Small app stack with shared Redis/Valkey

Use K3s when several services should discover each other by DNS, restart independently, and share one in-cluster cache/queue.

Pattern:

- Stateless web/API: `Deployment` + `Service` + `Ingress`.
- Workers: separate `Deployment`s for each queue/function (`email-worker`, `image-worker`, `billing-worker`) so each scales independently.
- Shared Valkey/Redis: `StatefulSet` + `Service` + PVC for single-primary simple cases.
- Scheduled tasks: Kubernetes `CronJob`, not host cron.
- Secrets: external secret manager or sealed/encrypted secret flow; never commit raw Secret YAML.

Copy: [`templates/web-workers-cron-valkey.yaml`](templates/web-workers-cron-valkey.yaml).

### 3. Autoscaled web + separate workers

Use HPA only after metrics are installed and each container has requests. HPA makes poor decisions without requests and metrics.

When HPA owns a Deployment, omit `spec.replicas` from the Deployment manifest; otherwise repeated `kubectl apply` / GitOps reconciliation can reset the replica count that HPA selected.

Pattern:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

For queue workers, CPU is often the wrong metric. Prefer KEDA or external/custom metrics for queue depth when worker count should follow Redis/Valkey, RabbitMQ, SQS, NATS, or Kafka backlog.

### 4. Common storage across nodes

K3s bundles local-path-provisioner, which is great for simple single-node PVCs but **not a shared multi-node storage system**. If pods can move between nodes, choose storage deliberately:

| Storage need | Use |
|---|---|
| Single-node app data | local-path-provisioner PVC; pin pod to node if needed. |
| Multi-node ReadWriteOnce block volumes | Longhorn or cloud CSI. |
| Shared ReadWriteMany files | NFS, Longhorn RWX, Ceph/Rook, or a managed file service. |
| Databases | Prefer managed DB or DB operator; do not casually run critical DBs on local-path. |

### 5. Secret manager scenario

Kubernetes Secrets are base64-encoded and stored unencrypted by default unless encryption at rest is configured. For real secrets, prefer an external secret manager:

- HashiCorp Vault / OpenBao
- AWS Secrets Manager / SSM Parameter Store
- Google Secret Manager
- Azure Key Vault
- 1Password / Bitwarden / Doppler / Infisical, etc.

Common K3s pattern:

1. Install External Secrets Operator with Helm.
2. Give ESO minimal credentials to read only the paths it needs.
3. Create a `SecretStore` or `ClusterSecretStore` for the provider.
4. Create `ExternalSecret` resources that sync provider values into Kubernetes `Secret`s.
5. Mount the resulting Secret into the app by env var or volume.

Copy: [`templates/external-secrets-vault.yaml`](templates/external-secrets-vault.yaml).

## Best practices

- Keep workloads declarative: commit YAML/Helm/Kustomize, not imperative `kubectl run` state.
- Use namespaces by environment or app boundary; do not dump everything into `default`.
- Set `resources.requests` and `resources.limits` for every container.
- Add readiness and liveness probes to every server container.
- Use separate Deployments for separate worker types; do not hide all roles in one container command switch.
- Use Services for stable DNS: `valkey.platform.svc.cluster.local` or simply `valkey` inside the namespace.
- Use `NetworkPolicy` for isolation when workloads are not fully trusted.
- Pin images by version or digest. Avoid `latest`.
- Prefer rolling updates with `maxUnavailable: 0` for small replica counts.
- Back up the datastore and PVCs; K3s control-plane state is not your application data backup.
- For HA K3s, use 3 server nodes with embedded etcd or an external supported database; do not run 2 etcd voters.

## Antipatterns

| Antipattern | Problem | Prefer |
|---|---|---|
| Using K3s for one trivial container | Adds Kubernetes complexity for no benefit | Docker + systemd or Compose. |
| Putting everything in one Pod | Couples unrelated lifecycles and scaling | Separate Deployments; share via Services. |
| One worker Deployment with many queue roles | Cannot scale/roll/debug independently | One Deployment per worker role. |
| Running critical stateful DBs on local-path without backup | Node loss can mean data loss | Managed DB, Longhorn/Ceph/cloud CSI, tested backups. |
| Committing raw `Secret` manifests | Base64 is not encryption | External Secrets / sealed/encrypted secrets. |
| HPA without requests/metrics | Autoscaler is blind or unstable | Install metrics-server, set requests, test HPA. |
| Sharing Redis/Valkey across unrelated tenants | Noisy-neighbor and data isolation risk | Namespace/environment-specific instances or ACLs. |
| Exposing K3s API or Flannel ports publicly | Cluster compromise/network exposure | Private network/VPN/security groups. |
| `hostPath: /` or broad device mounts | Host escape/data destruction risk | Narrow hostPath/device access; node labels. |
| Treating local-path PVCs as portable | They are node-local | Pin pods or install real distributed storage. |

## Validation commands

```bash
# Static sanity checks against a connected cluster/API server. Server dry-run
# catches admission policies such as Pod Security Standards.
kubectl apply --dry-run=server -f templates/simple-device.yaml
kubectl apply --dry-run=server -f templates/web-workers-cron-valkey.yaml

# Offline fallback when no cluster/API server is available. This checks shape,
# not admission policies.
kubectl apply --dry-run=client --validate=false -f templates/simple-device.yaml

# Cluster checks, if connected
kubectl get nodes -o wide
kubectl get storageclass
kubectl get ingressclass
kubectl top nodes      # requires metrics-server
kubectl auth can-i get secrets --as system:serviceaccount:platform-demo:web
```

## Sources

Primary sources used for this skill:

- K3s docs: `https://docs.k3s.io/`
- K3s requirements: `https://docs.k3s.io/installation/requirements`
- Kubernetes Deployments: `https://kubernetes.io/docs/concepts/workloads/controllers/deployment/`
- Kubernetes HPA: `https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/`
- Kubernetes CronJobs: `https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/`
- Kubernetes Persistent Volumes: `https://kubernetes.io/docs/concepts/storage/persistent-volumes/`
- Kubernetes Secret good practices: `https://kubernetes.io/docs/concepts/security/secrets-good-practices/`
- External Secrets Operator: `https://external-secrets.io/latest/`

## Installation

```bash
# Claude Code
cp -r skills/k3s ~/.claude/skills/
```

For claude.ai, upload `SKILL.md` plus the `references/` and `templates/` files, or paste the relevant sections into project knowledge.
