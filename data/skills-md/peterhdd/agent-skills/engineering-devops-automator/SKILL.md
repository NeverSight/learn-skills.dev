---
name: engineering-devops-automator
description: "Automate infrastructure provisioning, CI/CD pipelines, and cloud operations for reliable deployments. Use when you need Terraform infrastructure-as-code, Docker containerization, blue-green or canary deployments, monitoring and alerting setup, log aggregation, disaster recovery planning, secrets management, cost optimization, or multi-environment configuration with tools like Vault, ELK, Loki, or AWS."
metadata:
  version: "1.1.1"
---

# DevOps & Infrastructure Guide

## Overview
This guide covers infrastructure automation, CI/CD pipeline development, deployment strategies, monitoring, and cloud operations. Use it when provisioning infrastructure, building pipelines, setting up observability, managing secrets, or planning disaster recovery.

## First 10 Minutes

- Inventory the delivery surface before proposing changes: CI config, infrastructure directories, runtime manifests, Dockerfiles, and observability config.
- Run the existing validation commands before editing anything. If the repo has no validation path for infra changes, add one as part of the task.
- Use `scripts/analyze_deployment_risk.py` on the repo root to summarize CI, Docker, Terraform, and Kubernetes signals before proposing rollout changes.
- Identify the rollback path for the current deploy system. If you cannot explain how to revert the change in under 5 minutes, the rollout plan is incomplete.

## Refuse or Escalate

- Refuse "just push it" requests when there is no rollback path, no health signal, or no way to test the change outside production.
- Escalate before changing production state if the plan includes database replacement, Terraform destroys, state moves, certificate rotation, or security group broadening without a compensating control.
- Escalate when the repo mixes multiple deployment systems and ownership boundaries are unclear. Untangling that is a separate task.
- Do not recommend Kubernetes by default. If the workload is a single service with simple networking and predictable scale, stay with the simpler runtime.

## Infrastructure Decision Rules

### Provisioning
- Use Terraform with remote state (S3 + DynamoDB lock) so every resource is version-controlled and safe from concurrent modifications.
- Use Terraform workspaces or directory-per-environment layout with shared modules to catch drift between staging and production.
- Use the same Terraform modules as production with variable overrides -- never create infrastructure via cloud console.

### CI/CD Pipelines
- Structure as discrete stages (lint, test, build, scan, deploy) with explicit dependencies so security failures block deployment.
- Deployment strategy: **blue-green** for zero-downtime + instant rollback, **canary** for gradual traffic shifting with metric-based promotion, **rolling** when simplicity matters and brief mixed-version traffic is acceptable.
- Automate any manual step performed more than twice; delete the manual runbook entry to prevent drift.

### Containerization
- Use multi-stage Docker builds with distroless or Alpine final images to minimize attack surface.
- CI must run Trivy (or equivalent) and fail on CRITICAL/HIGH findings before merge.

### Monitoring and Reliability
- Instrument the four golden signals (latency, traffic, errors, saturation); alert on symptoms, not causes.
- Every alert must link to a runbook; alerts without runbooks get deleted or converted to dashboard metrics within one sprint.
- Enforce structured JSON logging; ship to centralized system (ELK, Loki) with compliance-aligned retention.
- Configure liveness probes for 30-second restart; set PodDisruptionBudget for availability during disruptions.

### Disaster Recovery
- Automate failover with runbooks tested quarterly; an untested DR plan is no plan.

### Cost Optimization
- Review cloud utilization monthly; downsize any instance averaging below 20% CPU over 14 days.

### Secrets Management
- Store secrets in Vault or AWS Secrets Manager with automated rotation (max 90-day TTL); inject at runtime.
- Never commit secrets to source control or bake them into images.

### Network Security
- Default all security groups and NACLs to deny-all inbound; open only required ports/CIDRs; prune monthly.

### Compliance
- Generate automated audit logs recording deployer, commit SHA, and approval; store immutably for retention period.

### Incident Response Protocol
- **Severity 1 (site down, data loss risk)**: Assemble incident team within 5 minutes. First action: mitigate (rollback, failover, scale up), not diagnose. Communicate status to stakeholders within 15 minutes. Post-mortem within 48 hours.
- **Severity 2 (degraded performance, partial outage)**: On-call engineer responds within 15 minutes. Check: recent deploys (rollback if <1 hour old), infrastructure alerts (CPU, memory, disk), dependency health (downstream services, databases). Communicate status within 30 minutes.
- **Severity 3 (minor issue, workaround exists)**: Log the issue, create a ticket, fix in next sprint. No immediate response required.
- **Rollback decision**: If the issue started after a deploy within the last 4 hours, rollback first, investigate second. If the issue is not correlated with a deploy, escalate to the relevant service team.
- **Communication template**: "We are aware of [impact description]. [X users / Y% of traffic] are affected. We are [current action]. Next update in [time]."

### Cost Estimation Formulas
- **Compute (EC2/GCE)**: `monthly_cost = instance_hourly_rate * 730 * instance_count`. Reserved instances save 30-60% for steady-state workloads (commit for 1 year).
- **Storage (S3/GCS)**: `monthly_cost = storage_GB * $0.023 + requests * $0.0004 (GET) or $0.005 (PUT)`. Enable lifecycle policies: move to Infrequent Access after 30 days, Glacier after 90 days.
- **Database (RDS/Cloud SQL)**: `monthly_cost = instance_hourly_rate * 730 + storage_GB * $0.115 + IOPS_provisioned * $0.10`. Multi-AZ doubles the instance cost.
- **Data transfer**: First 1GB/month free. $0.09/GB out to internet. Inter-AZ: $0.01/GB each direction. Cross-region: $0.02/GB. Data transfer is the hidden cost — monitor it.
- **Kubernetes (EKS/GKE)**: `cluster_cost = control_plane ($73/month EKS) + node_instance_costs + data_transfer`. Spot/preemptible nodes save 60-90% for fault-tolerant workloads.
- **Rule of thumb**: If cloud bill >$5k/month, hire a FinOps review. If >$50k/month, automate cost anomaly detection with AWS Cost Anomaly Detection or similar.

### Service Selection Decision Trees
- **Compute**: Lambda/Cloud Functions if <15 min execution, <10GB memory, and request-driven. ECS/Cloud Run for containerized services with consistent traffic. EKS/GKE only if running >10 services with complex networking requirements.
- **Database**: RDS PostgreSQL for <10TB relational. DynamoDB for key-value at >100k QPS. ElastiCache Redis for caching and session storage. Aurora if you need PostgreSQL compatibility with automatic multi-AZ failover.
- **Queue/Messaging**: SQS for simple async jobs. SNS + SQS for fan-out. EventBridge for event routing with filtering rules. Kafka (MSK) only for streaming >10k msg/sec with replay.
- **Storage**: S3 for objects. EFS for shared filesystem (NFS). EBS for block storage (database volumes). Choose storage class based on access frequency.
- **CDN**: CloudFront for AWS-native. Cloudflare for multi-cloud or DDoS-heavy. Use CDN for all static assets and any API response cacheable for >5 seconds.

## Self-Verification Protocol
After any infrastructure or pipeline change, verify:
- **Terraform**: Run `terraform plan` and read every line of the diff. If the plan shows any `destroy` or `replace` on a production resource, stop and verify intent.
- **CI/CD pipeline**: Trigger a full pipeline run on a non-production branch. Verify every stage passes. Check that security scan gates actually block on findings (deliberately introduce a known CVE to test).
- **Monitoring**: After setting up alerts, trigger each alert manually (spike CPU, kill a health check, fill disk). Verify the alert fires within the expected time window and reaches the correct channel.
- **Disaster recovery**: After configuring backups, perform a restore to a test environment. Verify data integrity. If you cannot restore, you do not have backups — you have a false sense of security.
- **Secrets**: Verify no secrets appear in: CI/CD logs (mask variables), Docker image layers (`docker history`), Terraform state (use `sensitive = true`), or git history (`git log -p | grep -i password`).

## Failure Recovery
- **Terraform state drift**: Run `terraform plan` to see the drift. If drift is in a non-critical resource, run `terraform apply` to reconcile. If drift is in a critical resource (database, load balancer), investigate who/what changed it manually and reconcile carefully. Never blindly `terraform apply` when state shows unexpected changes.
- **CI/CD pipeline broken**: Check the last successful run. Diff the pipeline config between last success and current failure. Common causes: expired secrets/tokens, dependency version bump, runner image update, or rate limiting from a registry.
- **Container OOM-killed in production**: Check `kubectl describe pod` for the OOM event. Increase memory limits if under-provisioned. If memory usage grows linearly over time, the application has a memory leak — fix the app, not the limits.
- **Certificate expiry**: Automate renewal with cert-manager (Kubernetes) or ACM (AWS). Set alerts for 30, 14, and 7 days before expiry. If expired: renew immediately, check all services using the cert, verify they pick up the new cert (may need pod restart).
- **Disk full**: Identify what filled it: logs (rotate and compress), Docker images (prune unused), database WAL (check replication lag), or temp files. Fix the root cause; expanding the disk is a temporary measure.

## Scripts

- `scripts/validate_dockerfile.sh` -- Check a Dockerfile against common best practices: multi-stage builds, USER instruction, HEALTHCHECK, no latest tags, COPY over ADD, and .dockerignore presence. Run with `--help` for usage.
- `scripts/check_services.sh` -- Check TCP connectivity and HTTP response for a list of host:port pairs. Reports status, latency, and HTTP status code. Run with `--help` for usage.

## Code Examples

See [CI/CD Pipeline Guide](references/cicd-pipeline.md) for a full GitHub Actions pipeline with security scanning, container build, and blue-green deployment with smoke tests.

See [Infrastructure & Monitoring Guide](references/infrastructure.md) for Terraform (launch template, ASG, ALB, CloudWatch alarm) and Prometheus configuration with alert rules.

## Workflow

### Step 1: Infrastructure Assessment
- Audit existing infrastructure, deployment process, and monitoring gaps.
- Map application dependencies and scaling requirements.
- Identify security and compliance requirements for the target environment.

### Step 2: Pipeline Design
- Design CI/CD pipeline with security scanning integration.
- Plan deployment strategy (blue-green, canary, rolling).
- Create infrastructure as code templates.
- Design monitoring and alerting strategy.

### Step 3: Implementation
- Set up CI/CD pipelines with automated testing.
- Implement infrastructure as code with version control.
- Configure monitoring, logging, and alerting systems.
- Create disaster recovery and backup automation.

### Step 4: Optimization and Maintenance
- Monitor system performance and optimize resources.
- Implement cost optimization strategies.
- Create automated security scanning and compliance reporting.
- Build self-healing systems with automated recovery.

## Deliverables

- Deployment strategy with explicit rollback steps, health gates, and ownership.
- Infrastructure change summary listing stateful resources, blast radius, and approval points.
- CI/CD plan covering lint, test, build, scan, deploy, and post-deploy verification.
- Monitoring and alert checklist tied to the changed services, not a generic dashboard wishlist.

## References

- [CI/CD Pipeline Guide](references/cicd-pipeline.md) -- GitHub Actions pipeline with security scanning, container build, and blue-green deployment.
- [Infrastructure & Monitoring Guide](references/infrastructure.md) -- Terraform (launch template, ASG, ALB, CloudWatch alarm) and Prometheus configuration.
- [Kubernetes Patterns](references/kubernetes.md) -- Production Deployment, HPA, PDB, ConfigMap/Secret mounting, Ingress with TLS, CronJob, and Helm values.
- [Docker Best Practices](references/docker.md) -- Multi-stage Dockerfiles (Node.js, Python, Go), .dockerignore, Docker Compose, and Trivy scanning.
- [Monitoring & Observability](references/observability.md) -- Structured logging, Prometheus metrics, Grafana dashboard, alert rules, OpenTelemetry tracing, and health checks.
- [Incident Triage](references/incident-triage.md) -- Repo-first production incident flow, rollback decision tree, and evidence capture checklist.
- [Deployment Rollback Guide](references/deployment-rollbacks.md) -- Canary, blue-green, rolling, schema-change, and feature-flag rollback patterns.
