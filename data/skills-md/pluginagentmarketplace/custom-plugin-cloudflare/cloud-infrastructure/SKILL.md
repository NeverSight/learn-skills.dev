---
# ═══════════════════════════════════════════════════════════════════════════
# SKILL: Cloud Infrastructure
# Version: 2.0.0 | Updated: 2025-01
# ═══════════════════════════════════════════════════════════════════════════
name: cloud-infrastructure
description: Cloud platforms (AWS, Cloudflare, GCP, Azure), containerization (Docker), Kubernetes, Infrastructure as Code (Terraform), CI/CD, and observability.

# ACTIVATION TRIGGERS
triggers:
  - aws
  - kubernetes
  - docker
  - cloud
  - terraform
  - devops
  - ci-cd
  - cloudflare
  - gcp
  - azure

# SKILL PARAMETERS
parameters:
  platform:
    type: string
    enum: [aws, gcp, azure, cloudflare, multi-cloud]
    required: true
  focus:
    type: string
    enum: [compute, containers, iac, cicd, monitoring]
    required: false

# OUTPUT SPECIFICATION
outputs:
  architecture:
    type: object
  services:
    type: array
  learning_path:
    type: array

# RELIABILITY
retry:
  max_attempts: 3
  backoff: exponential

# OBSERVABILITY
observability:
  log_level: info

level: advanced
prerequisites:
  - linux-basics
  - networking-basics

sasmp_version: "1.3.0"
bonded_agent: 01-core-paths
bond_type: PRIMARY_BOND
---

# Cloud Infrastructure Skill

## Quick Reference

| Platform | Market | Best For | Learning |
|----------|--------|----------|----------|
| **AWS** | 32% | Everything | 3-6 mo |
| **Azure** | 24% | Microsoft stack | 3-6 mo |
| **GCP** | 11% | Data, ML | 3-6 mo |
| **Cloudflare** | Edge | CDN, Workers | 2-4 wk |

---

## Learning Paths

### AWS
```
[1] IAM + VPC (1-2 wk)
 │  └─ Roles, policies, networking
 │
 ▼
[2] Compute: EC2, Lambda (2-3 wk)
 │
 ▼
[3] Storage: S3, EBS (1-2 wk)
 │
 ▼
[4] Database: RDS, DynamoDB (2-3 wk)
 │
 ▼
[5] Containers: ECS, EKS (3-4 wk)
 │
 ▼
[6] Monitoring: CloudWatch (1-2 wk)
```

### Docker & Containers
```
[1] Docker Basics (1 wk)
 │  └─ Images, containers, Dockerfile
 │
 ▼
[2] Multi-stage Builds (1 wk)
 │  └─ Optimization, layer caching
 │
 ▼
[3] Docker Compose (1 wk)
 │  └─ Multi-container apps
 │
 ▼
[4] Registry & Security (1 wk)
    └─ Push/pull, scanning, non-root
```

### Kubernetes
```
[1] Pods & Deployments (2 wk)
 │
 ▼
[2] Services & Networking (1-2 wk)
 │
 ▼
[3] ConfigMaps & Secrets (1 wk)
 │
 ▼
[4] Helm Charts (2 wk)
 │
 ▼
[5] Production Patterns (ongoing)
    └─ HPA, PDB, resource limits
```

### Terraform (IaC)
```
[1] Resources & State (1 wk)
 │
 ▼
[2] Variables & Outputs (1 wk)
 │
 ▼
[3] Modules (1-2 wk)
 │
 ▼
[4] Remote State (1 wk)
 │
 ▼
[5] Workspaces & Environments (1 wk)
```

---

## Kubernetes Quick Reference

| Resource | Purpose | Example |
|----------|---------|---------|
| **Pod** | Smallest unit | Single container |
| **Deployment** | Manage replicas | Web app |
| **Service** | Network access | ClusterIP, LoadBalancer |
| **Ingress** | HTTP routing | Path-based routing |
| **ConfigMap** | Configuration | Environment variables |
| **Secret** | Sensitive data | Credentials |
| **StatefulSet** | Stateful apps | Databases |

---

## Terraform Structure

```
project/
├── main.tf           # Resources
├── variables.tf      # Inputs
├── outputs.tf        # Outputs
├── providers.tf      # Provider config
├── versions.tf       # Version constraints
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── rds/
└── environments/
    ├── dev.tfvars
    ├── staging.tfvars
    └── prod.tfvars
```

---

## CI/CD Pipeline Template

```yaml
# GitHub Actions
name: CI/CD
on:
  push:
    branches: [main]
jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: docker build -t app .
      - name: Test
        run: docker run app pytest
      - name: Push
        run: docker push registry/app:${{ github.sha }}
      - name: Deploy
        if: github.ref == 'refs/heads/main'
        run: kubectl set image deployment/app app=registry/app:${{ github.sha }}
```

---

## Monitoring Stack

```
┌─────────────────────────────────────────┐
│         OBSERVABILITY STACK              │
├─────────────────────────────────────────┤
│  Metrics:  Prometheus → Grafana         │
│  Logs:     Loki / ELK                   │
│  Traces:   Jaeger / Tempo               │
│  Alerts:   Alertmanager → PagerDuty     │
└─────────────────────────────────────────┘
```

---

## Troubleshooting

```
Container not starting?
├─► docker logs <container>
├─► Check port conflicts
├─► Check image name/tag
└─► Check resource limits

Pod in CrashLoopBackOff?
├─► kubectl describe pod <name>
├─► kubectl logs <pod>
├─► Check resource limits
├─► Check probes configuration
└─► Check image pull secrets

Terraform apply fails?
├─► terraform plan first
├─► Check state lock
├─► terraform import existing
└─► Restore state from backup

High cloud bill?
├─► Enable cost alerts
├─► Right-size instances
├─► Use spot instances
├─► Delete unused resources
└─► Storage lifecycle policies
```

---

## Common Failure Modes

| Symptom | Root Cause | Recovery |
|---------|------------|----------|
| Pod CrashLoopBackOff | App error or OOM | Check logs, increase limits |
| ImagePullBackOff | Wrong image or auth | Verify image, check secrets |
| Terraform drift | Manual changes | Import or terraform apply |
| Slow deploys | Large images | Multi-stage builds, layer caching |

---

## Best Practices

### Docker
- Use multi-stage builds
- Run as non-root user
- Use .dockerignore
- Pin base image versions
- Scan for vulnerabilities

### Kubernetes
- Set resource requests/limits
- Use readiness/liveness probes
- Store config in ConfigMaps
- Use namespaces for isolation
- Enable network policies

### Terraform
- Use remote state (S3, GCS)
- Lock state file
- Use modules for reuse
- Plan before apply
- Tag all resources

---

## Next Actions

Specify your cloud platform and focus area for detailed guidance.
