---
name: iac-scan-kube-linter
description: Run KubeLinter to lint Kubernetes YAML and Helm charts for security best practices. Checks pod security, resource limits, network policies, and RBAC.
---

# Kubernetes Linting with KubeLinter

You are a security engineer linting Kubernetes manifests and Helm charts using **KubeLinter** for security best practices.

## When to use

Use this skill when asked to lint or review Kubernetes YAML manifests or Helm charts for security issues.

## Prerequisites

- KubeLinter installed (`brew install kube-linter` or download binary)
- Verify: `kube-linter version`

## Instructions

1. **Identify the target** — Determine the K8s manifests or Helm chart directory.
2. **Run the scan:**
   ```bash
   kube-linter lint <path> --format json > kubelinter-results.json
   ```
   - Specific file: `kube-linter lint deployment.yaml --format json`
   - Helm chart: `kube-linter lint ./charts/myapp --format json`
   - List available checks: `kube-linter checks list`
   - Exclude checks: `kube-linter lint . --exclude no-read-only-root-fs --format json`
3. **Parse the results** — Read JSON output and present findings:

```
| # | Check | Object | File | Message | Remediation |
|---|-------|--------|------|---------|-------------|
```

4. **Summarize** — Provide total issues, specific YAML fixes for each finding.

## Key KubeLinter Checks

| Check | Description |
|-------|-------------|
| `run-as-non-root` | Containers should not run as root |
| `no-read-only-root-fs` | Set readOnlyRootFilesystem: true |
| `drop-net-raw-capability` | Drop NET_RAW capability |
| `no-extensions-v1beta` | Don't use deprecated API versions |
| `dangling-service` | Services without matching pods |
| `default-service-account` | Don't use default service account |
| `writable-host-mount` | Host path mounted as writable |
| `privilege-escalation-container` | allowPrivilegeEscalation not set to false |
| `unset-cpu-requirements` | CPU limits/requests not set |
| `unset-memory-requirements` | Memory limits/requests not set |
| `sensitive-host-mounts` | Mounting sensitive host paths |
