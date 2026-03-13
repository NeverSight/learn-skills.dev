---
name: infrastructure-coder
description: >-
  Infrastructure-as-Code: Terraform, Kubernetes, Docker. Generate, review,
  cost-compare, security-scan. Use for IaC work. NOT for CI/CD
  (devops-engineer), application code, or actual pricing.
argument-hint: "<mode> <requirements>"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Infrastructure Coder

Generate, review, and analyze Infrastructure-as-Code. Terraform/OpenTofu modules, Kubernetes manifests, Dockerfiles.

**Scope:** IaC generation and analysis only. NOT for CI/CD pipelines (devops-engineer), application code, cloud console operations, or actual cost calculation.

## Canonical Vocabulary

| Term | Definition |
|------|-----------|
| **module** | A self-contained Terraform/OpenTofu unit with variables, resources, and outputs |
| **manifest** | A Kubernetes YAML resource definition |
| **chart** | A Helm package containing templated K8s manifests |
| **stage** | A Docker build stage in a multi-stage Dockerfile |
| **resource** | A cloud infrastructure primitive (instance, bucket, network, etc.) |
| **misconfiguration** | A security or reliability issue in IaC (open ports, missing encryption, no limits) |
| **cost-relative** | Comparison between resource types/tiers, NOT absolute dollar pricing |
| **hardening** | Applying security best practices to reduce attack surface |
| **drift** | Difference between declared IaC state and actual infrastructure |
| **blast radius** | How many dependent resources would be affected by a change |

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `terraform <requirements>` | Generate Terraform/OpenTofu modules |
| `kubernetes <requirements>` / `k8s <requirements>` | Generate K8s manifests and Helm charts |
| `docker <requirements>` | Optimize Dockerfiles (multi-stage, caching, security) |
| `review <file-or-path>` | Audit IaC for correctness and best practices |
| `cost <config-or-path>` | Cost-relative estimation (compare resource types) |
| `security <config-or-path>` | Security scan for IaC misconfigurations |
| Empty | Show mode menu with examples |

## Mode: Terraform

Generate production-ready Terraform/OpenTofu modules.

### Terraform Steps

1. Parse requirements — identify resources, provider, region, dependencies
2. Run `uv run python skills/infrastructure-coder/scripts/terraform-module-scanner.py <path>` on any existing `.tf` files to understand current state
3. Generate module structure:
   - `main.tf` — resource definitions
   - `variables.tf` — input variables with descriptions, types, defaults, validation
   - `outputs.tf` — useful outputs for downstream consumption
   - `versions.tf` — required providers and version constraints
4. Apply patterns from references/terraform-patterns.md

### Generation Rules

- Always pin provider versions with `~>` constraints
- Use `for_each` over `count` for named resources
- Tag all resources with `Name`, `Environment`, `ManagedBy = "terraform"`
- Use data sources for existing infrastructure, never hardcode ARNs/IDs
- Separate state per environment using workspaces or backend config
- Reference references/cloud-equivalents.md for multi-cloud alternatives

## Mode: Kubernetes

Generate Kubernetes manifests or Helm charts.

### Manifest Steps

1. Parse requirements — identify workload type, scaling, networking, storage
2. Run `uv run python skills/infrastructure-coder/scripts/k8s-manifest-validator.py <path>` on existing manifests
3. Generate manifests with best practices:
   - Resource limits and requests on every container
   - Health checks (liveness, readiness, startup probes)
   - Security context (non-root, read-only root filesystem, drop capabilities)
   - Pod disruption budgets for HA workloads
   - NetworkPolicies for pod-to-pod communication

### Helm Charts

4. For Helm charts: parameterize environment-specific values, use `values.yaml` defaults
5. Apply patterns from references/kubernetes-patterns.md

## Mode: Docker

Optimize Dockerfiles for size, build speed, and security.

1. Run `uv run python skills/infrastructure-coder/scripts/dockerfile-analyzer.py <path>` on existing Dockerfile
2. Parse JSON output for issues and optimization opportunities
3. Apply optimizations:
   - Multi-stage builds separating build and runtime
   - Order layers by change frequency (dependencies before source)
   - Use specific base image tags (never `latest`)
   - Distroless or Alpine for runtime images
   - Non-root USER directive
   - COPY specific files, avoid COPY . .
   - Combine RUN commands to reduce layers
   - Use .dockerignore
4. Reference references/dockerfile-guide.md for detailed patterns

## Mode: Review

Audit IaC files for correctness, best practices, and reliability.

### Analysis Pipeline

1. Identify file type (Terraform, K8s manifest, Dockerfile, Helm chart)
2. Run the appropriate analysis script:
   - `.tf` files: `terraform-module-scanner.py`
   - K8s YAML: `k8s-manifest-validator.py`
   - Dockerfile: `dockerfile-analyzer.py`
3. Multi-pass analysis (adapted from honest-review pipeline):
   - **Pass 1 — Correctness**: syntax, valid references, API version compatibility
   - **Pass 2 — Best practices**: patterns from reference files, anti-patterns
   - **Pass 3 — Reliability**: failure modes, blast radius, recovery paths

### Findings Report

4. Present findings grouped by severity (Critical / Warning / Info)
5. For each finding: file location, issue description, recommended fix
6. Reference references/security-hardening.md for security-specific checks

## Mode: Cost

Cost-relative comparison between resource configurations. NOT absolute pricing.

1. Identify resources in the configuration
2. Reference references/cloud-equivalents.md for cross-cloud mapping
3. Compare configurations on relative axes:
   - Instance families: compute-optimized vs memory-optimized vs general-purpose
   - Storage tiers: standard vs infrequent-access vs archive
   - Network: inter-region vs intra-region vs same-AZ
   - Managed vs self-hosted trade-offs
4. Present as relative comparison table (e.g., "~2x cost of...", "comparable to...")
5. Reference references/cost-comparison.md for tier mappings

Output relative comparisons only. Never state dollar amounts — pricing changes constantly and varies by contract.

## Mode: Security

Scan IaC for security misconfigurations.

1. Run the appropriate analysis script for file type
2. Check against references/security-hardening.md checklist:
   - **Network**: open security groups, public subnets, missing NACLs
   - **Encryption**: unencrypted storage, missing TLS, plaintext secrets
   - **Access**: overly permissive IAM, missing MFA, wildcard policies
   - **Containers**: privileged mode, root user, host networking, latest tags
   - **Secrets**: hardcoded credentials, API keys in config, missing vault integration
3. Classify findings by severity:
   - **Critical**: exploitable without authentication, data exposure
   - **High**: requires some access but significant impact
   - **Medium**: defense-in-depth violation, potential escalation path
   - **Low**: informational, hardening recommendation
4. Present findings with CIS/cloud-specific benchmark references where applicable

## Dashboard

After any review, cost, or security scan, render an IaC overview dashboard.

1. Collect all findings and resource inventory
2. Inject as JSON into `templates/dashboard.html`:
   ```json
   {
     "view": "iac-overview",
     "resources": [...],
     "findings": [...],
     "dockerfile_layers": [...],
     "cost_comparison": [...]
   }
   ```
3. Copy template to a temporary file, inject data, open in browser

## Reference Files

Load ONE reference at a time. Do not preload all references.

| File | Content | Read When |
|------|---------|-----------|
| `references/terraform-patterns.md` | Module patterns, state management, provider config | Terraform mode |
| `references/kubernetes-patterns.md` | Resource patterns, Helm conventions, scaling | Kubernetes mode |
| `references/dockerfile-guide.md` | Multi-stage builds, layer optimization, distroless | Docker mode |
| `references/cloud-equivalents.md` | AWS/GCP/Azure resource mapping | Cost mode, multi-cloud generation |
| `references/security-hardening.md` | IaC security checklist by category | Security mode, Review mode |
| `references/cost-comparison.md` | Relative cost tiers and trade-offs | Cost mode |

| Script | When to Run |
|--------|-------------|
| `scripts/dockerfile-analyzer.py` | Docker mode, Review mode (Dockerfiles) |
| `scripts/terraform-module-scanner.py` | Terraform mode, Review mode (.tf files) |
| `scripts/k8s-manifest-validator.py` | Kubernetes mode, Review mode (K8s YAML) |

| Template | When to Render |
|----------|----------------|
| `templates/dashboard.html` | After review, cost, or security scan |

## Critical Rules

1. Never state absolute dollar pricing — use relative comparisons only ("~2x", "comparable to")
2. Always pin versions — provider versions, base image tags, chart versions. Never `latest`
3. Never generate IaC with hardcoded secrets — use variables, vault references, or secret managers
4. Always include resource limits in K8s manifests — CPU, memory requests and limits
5. Always run the appropriate analysis script before review/security mode output
6. Never skip security context in K8s — non-root, read-only root FS, dropped capabilities
7. Tag all cloud resources — Name, Environment, ManagedBy at minimum
8. Use `for_each` over `count` in Terraform for named resources
9. Never generate overly permissive IAM policies — principle of least privilege
10. Always include health checks in K8s manifests — liveness, readiness probes
11. Present review findings grouped by severity — Critical before Info
12. Load ONE reference file at a time — do not preload all references into context
13. Refuse CI/CD pipeline requests — redirect to devops-engineer skill
14. Refuse application code requests — this skill is IaC only
15. Refuse absolute cost estimation requests — explain why relative comparison is provided instead
