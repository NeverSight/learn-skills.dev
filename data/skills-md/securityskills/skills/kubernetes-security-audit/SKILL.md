---
name: kubernetes-security-audit
description: Audit Kubernetes clusters for RBAC excesses, pod security gaps, network policy holes, and supply-chain risks. Use when reviewing cluster configuration or hardening deployments.
---

# Kubernetes Security Audit

Audit a cluster across four layers: workload, identity, network, supply chain.

## Workload Security

- Pod Security Standards: check namespace labels (`pod-security.kubernetes.io/enforce`)
- Privileged pods, `hostPID`/`hostNetwork`/`hostPath` usage — each needs justification
- Containers running as root; `allowPrivilegeEscalation: true`; missing `readOnlyRootFilesystem`
- `securityContext` set at pod and container level; capabilities dropped to minimum set

## RBAC

- Enumerate bindings; find `cluster-admin` subjects — minimize to a named list
- Escalation paths: `bind`/`escalate`/`impersonate` verbs; `create pods` + node privileged, `create pods/exec`
- Service accounts: default SA used by workloads? token automount disabled where unneeded?
- Check for wildcard (`*`) verbs/resources in custom roles

## Network

- NetworkPolicy: default-deny ingress/egress per namespace as the baseline
- Cross-namespace exposure: which namespaces can reach `kube-system`, ingress controllers, databases
- Control plane exposure: API server on public IP? etcd reachable/authenticated?

## Supply Chain

- Image provenance: registry digests pinned (not `:latest`), signature verification (cosign)
- Admission control: image policy, no privileged images from untrusted registries
- Secrets: Kubernetes Secrets at rest (KMS encryption configured), not baked into images or env in manifests committed to git

## Quick Checks

```bash
kubectl get pods -A -o json | jq '[.items[] | select(.spec.containers[].securityContext.privileged==true)]'
kubectl get ns -l pod-security.kubernetes.io/enforce
kubectl auth can-i --list --as=system:serviceaccount:default:default
kubectl get networkpolicy -A
```

## Output

Findings per layer with YAML evidence, risk, and hardening manifests for remediation.
