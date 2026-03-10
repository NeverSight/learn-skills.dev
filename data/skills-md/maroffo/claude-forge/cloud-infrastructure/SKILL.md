---
name: cloud-infrastructure
description: "AWS/GCP cloud infrastructure: Well-Architected, security, cost, observability. Use when working with Terraform outputs, IAM policies, VPC design, load balancers, or cloud architecture decisions."
compatibility: "Requires AWS CLI or gcloud CLI. Optional: trivy, checkov, infracost."
allowed-tools: [mcp__acp__Read, mcp__acp__Edit, mcp__acp__Write, mcp__acp__Bash]
---

# ABOUTME: AWS/GCP cloud infrastructure patterns and best practices
# ABOUTME: Well-Architected, security, cost optimization, observability

# Cloud Infrastructure (AWS & GCP)

## Quick Reference

```bash
# AWS
aws sts get-caller-identity
aws --profile staging ecs list-services

# GCP
gcloud auth list
gcloud config set project PROJECT_ID

# Security scanning
trivy config . && checkov -d .
```

**See:** `terraform/SKILL.md` | `_PATTERNS.md`

---

## AWS Well-Architected (6 Pillars)

| Pillar | Key Practices |
|--------|---------------|
| **Operational Excellence** | IaC, runbooks, observability, chaos engineering |
| **Security** | Least privilege IAM, GuardDuty/Security Hub, KMS encryption, SCPs |
| **Reliability** | Multi-AZ, auto-scaling, RTO/RPO backups |
| **Performance** | Right-size, caching, serverless, read replicas |
| **Cost** | Reserved/Savings Plans, Spot, tagging |
| **Sustainability** | Optimize utilization, Graviton |

---

## AWS ECS vs EKS

| Factor | ECS | EKS |
|--------|-----|-----|
| Complexity | Lower | Higher (K8s) |
| Multi-cloud | No | Yes |
| Cost | Free control plane | $0.10/hr/cluster |

### ECS Task Definition
```hcl
resource "aws_ecs_task_definition" "app" {
  family                   = "app"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  container_definitions = jsonencode([{
    name   = "app"
    image  = "${var.ecr_repo}:${var.image_tag}"
    healthCheck = { command = ["CMD-SHELL", "curl -f http://localhost/health || exit 1"] }
  }])
}
```

---

## GCP Cloud Run

```yaml
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "100"
    spec:
      containerConcurrency: 80
      containers:
        - image: gcr.io/project/image
          resources: { limits: { cpu: "1", memory: "512Mi" } }
```

---

## Cost Optimization

| Tool | Use |
|------|-----|
| Cost Explorer / Compute Optimizer | AWS analysis |
| Infracost | IaC cost in PRs |
| GCP FinOps Hub | Gemini recommendations |

**Compute:** Reserved (72% savings), Spot (90%), Graviton, auto-scaling
**Storage:** S3 Intelligent Tiering, lifecycle policies
**Networking:** VPC endpoints (avoid NAT costs)

---

## Observability (OpenTelemetry)

**Why OTEL:** Vendor-agnostic, unified traces/metrics/logs

```yaml
receivers:
  otlp: { protocols: { grpc: { endpoint: 0.0.0.0:4317 } } }
processors:
  batch: { timeout: 1s }
exporters:
  awsxray: { region: us-east-1 }
service:
  pipelines:
    traces: { receivers: [otlp], processors: [batch], exporters: [awsxray] }
```

---

## Networking

### AWS VPC Design
```
VPC (10.0.0.0/16)
├── Public → ALB, NAT
├── Private → ECS/EKS, Lambda
└── Isolated → RDS (no internet)
```

### VPC Endpoints
```hcl
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.${var.region}.s3"
}
```

---

## Code Review Checklist

| Category | Checks |
|----------|--------|
| **Security** | No hardcoded secrets, least privilege IAM, KMS encryption, logging enabled |
| **Cost** | Tagged resources, right-sized, auto-scaling |
| **Reliability** | Multi-AZ, health checks, backups |

---

## Resources

**AWS:** [Well-Architected](https://aws.amazon.com/architecture/well-architected/) | [Security Best Practices](https://aws.github.io/aws-security-services-best-practices/)

**GCP:** [Architecture Framework](https://cloud.google.com/architecture/framework)

**Tools:** [Checkov](https://www.checkov.io/) | [Infracost](https://www.infracost.io/) | [OpenTelemetry](https://opentelemetry.io/)
