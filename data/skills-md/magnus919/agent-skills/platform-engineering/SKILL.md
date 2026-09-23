---
name: platform-engineering
description: >-
  Use this skill when building or operating internal developer platforms: infrastructure
  as code, CI/CD, container orchestration, service networking, secrets, and
  observability, or when shaping platform products, self-service interfaces,
  adoption evidence, and policy guardrails. Do not use it to define release process,
  promotion, rollout, or rollback policy; use release-engineering for that delivery model.
  Route named-tool configuration and troubleshooting to the corresponding operational
  skill, such as kubernetes or traefik for ingress-controller configuration.
license: MIT
metadata:
  tags: ''
  source_repo: https://github.com/magnus919/hermes-profiles
---

# Platform Engineering

Core methodology and reference library for platform engineering work. This skill does not execute operations itself — it provides the frameworks, patterns, and reference material that a platform-engineer profile loads on demand.

## When to Load

Load this skill when the task involves:

| Trigger | What's Needed |
|---------|---------------|
| Design a CI/CD pipeline | Pipeline structure, GitOps sync strategies, release automation |
| Infrastructure as code plan | Terraform/OpenTofu module patterns, state management, Pulumi/Ansible patterns |
| Container orchestration design | K8s pod lifecycle, Helm chart conventions, Kustomize overlays, Docker Compose; operating a cluster (manifests, RBAC, workloads, upgrades) routes to [kubernetes](../kubernetes/SKILL.md) |
| Service networking / mesh | Traefik/nginx/Caddy config, Tailscale/Headscale ACL, WireGuard, service mesh |
| Observability strategy | Prometheus rules, Grafana dashboards-as-code, Loki logging, tracing; operating the Prometheus/OTel/Loki stack (scrape, rules, retention) routes to [telemetry](../telemetry/SKILL.md), Grafana product work routes to [grafana](../grafana/SKILL.md) |
| Infrastructure execution | Terraform/OpenTofu plan/apply workflow, state backends, drift detection, upgrades — route to [terraform](../terraform/SKILL.md) |
| PostgreSQL operations | Server config review, indexes and query plans, vacuum/bloat, backups/PITR, replication — route to [postgres](../postgres/SKILL.md) |
| Secret management design | Vault, SOPS, External Secrets Operator patterns |
| Cloud architecture assessment | Multi-cloud patterns, provider foundations, cost governance |
| Deployment pipeline review | Delivery-platform architecture; load [release-engineering](../release-engineering/SKILL.md) when defining the release model, promotion gates, rollout, or rollback policy |
| Platform product intake or value case | Applicability, internal-user discovery, outcome contracts, adoption/value evidence, and stop/escalation rules |
| Self-service contract or policy exception | API/outcome contract, guardrail evidence, exception ownership, and escape-hatch review |
| Platform observability ownership | Platform-customer adoption, SLI/SLO publication, response routing, and ownership handoffs |

## When not to use

Use [release-engineering](../release-engineering/SKILL.md) to define release process, promotion, rollout, or rollback policy. This skill builds and operates the delivery platform that implements those decisions.

## Loading Order

```
skill_view('platform-engineering')          # This — methodology index
skill_view('artifact-pyramids')              # Output contract
skill_view('docker-compose')                 # Container lifecycle and Compose (if needed)
skill_view('traefik')                        # Reverse proxy (if needed)
skill_view('tailscale')                      # Mesh networking (if needed)
skill_view('implementation-planning')        # Work breakdown (if needed)
```

Then load domain-specific references from this skill:

```
skill_view('platform-engineering', file_path='references/ci-cd-pipelines.md')
skill_view('platform-engineering', file_path='references/platform-product-evidence.md')
skill_view('platform-engineering', file_path='references/policy-and-observability-ownership.md')
skill_view('platform-engineering', file_path='references/infrastructure-as-code.md')
# ... etc per domain
```

## Reference Files

| Reference | Purpose |
|-----------|---------|
| `references/ci-cd-pipelines.md` | GitHub Actions, GitLab CI, Forgejo CI, Jenkins, CircleCI; GitOps with ArgoCD/Flux; release automation |
| `references/container-orchestration.md` | K8s/k3s, Helm chart conventions, Kustomize overlays, RBAC patterns, Docker Compose production patterns |
| `references/infrastructure-as-code.md` | Terraform/OpenTofu module design, state backends, Pulumi project structure, Ansible roles, CloudFormation/CDK |
| `references/service-networking.md` | Reverse proxy config (Traefik, nginx, Caddy), Tailscale/Headscale ACL, WireGuard topology, service mesh (Istio, Cilium) |
| `references/observability.md` | Prometheus recording rules/alerting, Grafana dashboards-as-code, Loki log aggregation, OpenTelemetry tracing |
| `references/secret-management.md` | HashiCorp Vault auth/policies, SOPS/age encryption in Git, External Secrets Operator, Sealed Secrets |
| `references/cloud-platforms.md` | AWS/GCP/Azure foundational services, multi-cloud design, cost governance, provider abstraction |
| `references/automation-languages.md` | Go CLI patterns, Python SDK integration, Bash bootstrap/conventions for platform tooling |
| `references/release-engineering.md` | Container image lifecycle, artifact versioning strategies, release gate checklists, Helm chart promotion |
| `references/platform-product-evidence.md` | Applicability/intake, platform domain boundaries, outcome/self-service contracts, adoption and value evidence |
| `references/policy-and-observability-ownership.md` | Developer-owned delivery with reusable policy checks, exceptions, observability ownership, and response routing |

## Templates

| Template | When to Use |
|-----------|-------------|
| `templates/golden-path-self-service-portal.md` | Designing a golden path or self-service portal for a developer workflow (scoping, journey, guardrails, escape hatch, metrics) |
| `templates/iac-review-record.md` | Recording a structured review of Terraform/OpenTofu/Pulumi/Ansible modules before they ship |
| `templates/observability-contract.md` | Declaring the metrics/logs/traces contract a service must meet before production traffic |
| `templates/platform-value-record.md` | Recording the platform problem, baseline, adoption assumptions, value model, and stop/escalation decision |
| `templates/platform-exception-record.md` | Reviewing an escape-hatch or policy exception with scope, evidence, expiry, and accountable owner |

## Output Contract

The profile using this skill produces artifact pyramids. The response to any caller is the absolute path to `00-index.md`. See `artifact-pyramids` skill for the specification.

## Design Principles

1. **The platform is a product.** Internal developers are your customers. Their productivity, satisfaction, and cognitive load are the primary metrics.
2. **Golden paths, not golden cages.** Provide paved roads for common workflows but allow escape hatches. Make the right thing easy, not the wrong thing impossible.
3. **Reduce cognitive load.** Abstract infrastructure complexity. Developers should not need to understand Kubernetes internals or Terraform state management to deploy their service.
4. **Everything as code.** Infrastructure, configuration, pipelines, and policies are version-controlled, reviewed, and reproducible. Git is the single source of truth.
5. **Self-service over tickets.** Every manual handoff between teams is a bottleneck. If a developer needs another team to deploy, the platform is incomplete.
6. **Automation is the default.** If a process can be automated, it must be. Manual operations are toil — tax on the organization.
7. **Observability is infrastructure.** Logs, metrics, traces, and dashboards are platform contract, not optional extras. Every service gets them by default.
8. **Security is built in, not bolted on.** Supply chain security, secret management, vulnerability scanning, and policy enforcement are platform responsibilities.
9. **API-first design.** Everything the platform does should be accessible via API — enabling automation, self-service portals, and CLI tools.

## Related Skills

- `artifact-pyramids` — output contract specification
- `docker-compose` — container lifecycle and multi-container Compose orchestration
- `kubernetes` — cluster operations: manifests, RBAC, workloads, Helm, upgrades, troubleshooting
- `terraform` — Terraform/OpenTofu execution: plan/apply workflow, state backends and locking, drift detection, upgrades and refactors
- `telemetry` — Prometheus/OpenTelemetry Collector/Loki stack operations: scrape configs, rules files, retention, HA
- `postgres` — PostgreSQL operations: configuration review, index and query-plan diagnosis, vacuum/bloat, backups/PITR, replication and failover
- `grafana` — Grafana product work: dashboards, panels, data sources, alert rules, contact points, notification policies
- `traefik` — reverse proxy and ingress configuration
- `tailscale` — mesh networking and ACL policies
- `implementation-planning` — work breakdown and dependency ordering
- `mermaid-diagrams` — architecture diagram generation
- `site-reliability-engineering` — sister domain for post-deployment reliability
- `release-engineering` — release process, artifact promotion, readiness, rollout, and rollback policy; this skill owns the delivery platform that implements those decisions
