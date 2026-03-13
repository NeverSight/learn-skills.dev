---
name: cluster-agent-swarm
description: >
  Complete Platform Agent Swarm — A coordinated multi-agent system for Kubernetes and OpenShift 
  platform operations. Includes Orchestrator (Jarvis), Cluster Ops (Atlas), GitOps (Flow), 
  Security (Shield), Observability (Pulse), Artifacts (Cache), and Developer Experience (Desk).
metadata:
  author: cluster-agent-swarm
  version: 1.0.0
  agent_name: Swarm
  agent_role: Platform Agent Swarm (All Agents)
  session_key: "agent:platform:swarm"
  heartbeat: "*/5 * * * *"
  platforms:
    - openshift
    - kubernetes
    - eks
    - aks
    - gke
    - rosa
    - aro
  tools:
    - kubectl
    - oc
    - argocd
    - helm
    - kustomize
    - az
    - aws
    - gcloud
    - rosa
    - jq
    - curl
    - git
---

# Cluster Agent Swarm — Complete Platform Operations

This is the complete cluster-agent-swarm skill package. When you add this skill, you get 
access to ALL 7 specialized agents working together as a coordinated swarm.

## Installation Options

### Install All Skills (Recommended)
```bash
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills
```

This installs all 7 agents as a single combined skill with access to all capabilities.

### Install Individual Skills
Each agent can also be installed separately using GitHub tree path or --skill flag:

```bash
# Using GitHub tree path (recommended)
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/tree/main/skills/orchestrator

# Using --skill flag (if supported by your skills tool)
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills --skill orchestrator

# Available individual skills:
# - orchestrator  (Jarvis - task routing)
# - cluster-ops   (Atlas - cluster operations)
# - gitops        (Flow - ArgoCD, Helm, Kustomize)
# - security      (Shield - RBAC, policies)
# - observability (Pulse - metrics, alerts)
# - artifacts     (Cache - registries, SBOM)
# - developer-experience (Desk - namespaces, onboarding)
# - qmd           (Local hybrid search for markdown notes/docs)
```
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/gitops

# Security - Shield (RBAC, policies, CVEs)
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/security

# Observability - Pulse (metrics, alerts, incidents)
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/observability

# Artifacts - Cache (registries, SBOM, promotions)
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/artifacts

# Developer Experience - Desk (namespaces, onboarding)
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/developer-experience

# QMD - Local Markdown Search (notes, docs, knowledge bases)
npx skills add https://github.com/kcns008/cluster-agent-swarm-skills/skills/qmd
```

---

## The Swarm — Agent Roster

| Agent | Code Name | Session Key | Domain |
|-------|-----------|-------------|--------|
| Orchestrator | Jarvis | `agent:platform:orchestrator` | Task routing, coordination, standups |
| Cluster Ops | Atlas | `agent:platform:cluster-ops` | Cluster lifecycle, nodes, upgrades |
| GitOps | Flow | `agent:platform:gitops` | ArgoCD, Helm, Kustomize, deploys |
| Security | Shield | `agent:platform:security` | RBAC, policies, secrets, scanning |
| Observability | Pulse | `agent:platform:observability` | Metrics, logs, alerts, incidents |
| Artifacts | Cache | `agent:platform:artifacts` | Registries, SBOM, promotion, CVEs |
| Developer Experience | Desk | `agent:platform:developer-experience` | Namespaces, onboarding, support |

---

## Agent Capabilities Summary

### What Agents CAN Do
- Read cluster state (`kubectl get`, `kubectl describe`, `oc get`)
- Deploy via GitOps (`argocd app sync`, Flux reconciliation)
- Create documentation and reports
- Investigate and triage incidents
- Provision standard resources (namespaces, quotas, RBAC)
- Run health checks and audits
- Scan images and generate SBOMs
- Query metrics and logs
- Execute pre-approved runbooks

### What Agents CANNOT Do (Human-in-the-Loop Required)
- Delete production resources (`kubectl delete` in prod)
- Modify cluster-wide policies (NetworkPolicy, OPA, Kyverno cluster policies)
- Make direct changes to secrets without rotation workflow
- Modify network routes or service mesh configuration
- Scale beyond defined resource limits
- Perform irreversible cluster upgrades
- Approve production deployments (can prepare, human approves)
- Change RBAC at cluster-admin level

---

## Communication Patterns

### @Mentions
Agents communicate via @mentions in shared task comments:
```
@Shield Please review the RBAC for payment-service v3.2 before I sync.
@Pulse Is the CPU spike related to the deployment or external traffic?
@Atlas The staging cluster needs 2 more worker nodes.
```

### Thread Subscriptions
- Commenting on a task → auto-subscribe
- Being @mentioned → auto-subscribe
- Being assigned → auto-subscribe
- Once subscribed → receive ALL future comments on heartbeat

### Escalation Path
1. Agent detects issue
2. Agent attempts resolution within guardrails
3. If blocked → @mention another agent or escalate to human
4. P1 incidents → all relevant agents auto-notified

---

## Heartbeat Schedule

Agents wake on staggered 5-minute intervals:
```
*/5  * * * *  Atlas   (Cluster Ops - needs fast response for incidents)
*/5  * * * *  Pulse   (Observability - needs fast response for alerts)
*/5  * * * *  Shield  (Security - fast response for CVEs and threats)
*/10 * * * *  Flow    (GitOps - deployments can wait a few minutes)
*/10 * * * *  Cache   (Artifacts - promotions are scheduled)
*/15 * * * *  Desk    (DevEx - developer requests aren't usually urgent)
*/15 * * * *  Orchestrator (Coordination - overview and standups)
```

---

## Key Principles

- **Roles over genericism** — Each agent has a defined SOUL with exactly who they are
- **Files over mental notes** — Only files persist between sessions
- **Staggered schedules** — Don't wake all agents at once
- **Shared context** — One source of truth for tasks and communication
- **Heartbeat, not always-on** — Balance responsiveness with cost
- **Human-in-the-loop** — Critical actions require approval
- **Guardrails over freedom** — Define what agents can and cannot do
- **Audit everything** — Every action logged to activity feed
- **Reliability first** — System stability always wins over new features
- **Security by default** — Deny access, approve by exception

---

## Detailed Agent Capabilities

### Orchestrator (Jarvis)
- Task routing: determining which agent should handle which request
- Workflow orchestration: coordinating multi-agent operations
- Daily standups: compiling swarm-wide status reports
- Priority management: determining urgency and sequencing of work
- Cross-agent communication: facilitating collaboration
- Accountability: tracking what was promised vs what was delivered

### Cluster Ops (Atlas)
- OpenShift/Kubernetes cluster operations (upgrades, scaling, patching)
- Node pool management and autoscaling
- Resource quota management and capacity planning
- Network troubleshooting (OVN-Kubernetes, Cilium, Calico)
- Storage class management and PVC/CSI issues
- etcd backup, restore, and health monitoring
- Multi-platform expertise (OCP, EKS, AKS, GKE, ROSA, ARO)

### GitOps (Flow)
- ArgoCD application management (sync, rollback, sync waves, hooks)
- Helm chart development, debugging, and templating
- Kustomize overlays and patch generation
- ApplicationSet templates for multi-cluster deployments
- Deployment strategy management (canary, blue-green, rolling)
- Git repository management and branching strategies
- Drift detection and remediation
- Secrets management integration (Vault, Sealed Secrets, External Secrets)

### Security (Shield)
- RBAC audit and management
- NetworkPolicy review and enforcement
- Security policy validation (OPA, Kyverno)
- Vulnerability scanning (image scanning, CVE triage)
- Secret rotation workflows
- Security incident investigation
- Compliance reporting

### Observability (Pulse)
- Prometheus/Grafana metric queries
- Log aggregation and search (Loki, Elasticsearch)
- Alert triage and investigation
- SLO tracking and error budget monitoring
- Incident response coordination
- Dashboards and visualization
- Telemetry pipeline troubleshooting

### Artifacts (Cache)
- Container registry management
- Image scanning and CVE analysis
- SBOM generation and tracking
- Artifact promotion workflows
- Version management
- Registry caching and proxying

### Developer Experience (Desk)
- Namespace provisioning
- Resource quota and limit range management
- Developer onboarding
- Template generation
- Developer support and troubleshooting
- Documentation generation

---

## File Structure

```
cluster-agent-swarm-skills/
├── SKILL.md                    # This file - combined swarm
├── AGENTS.md                   # Swarm configuration and protocols
├── skills/
│   ├── orchestrator/           # Jarvis - task routing
│   │   └── SKILL.md
│   ├── cluster-ops/            # Atlas - cluster operations
│   │   └── SKILL.md
│   ├── gitops/                 # Flow - GitOps
│   │   └── SKILL.md
│   ├── security/               # Shield - security
│   │   └── SKILL.md
│   ├── observability/          # Pulse - monitoring
│   │   └── SKILL.md
│   ├── artifacts/              # Cache - artifacts
│   │   └── SKILL.md
│   └── developer-experience/   # Desk - DevEx
│       └── SKILL.md
│   └── qmd/                    # Local markdown search
│       └── SKILL.md
├── scripts/                    # Shared scripts
└── references/                 # Shared documentation
```

---

## Reference Documentation

For detailed capabilities of each agent, refer to individual SKILL.md files:
- `skills/orchestrator/SKILL.md` - Full Orchestrator documentation
- `skills/cluster-ops/SKILL.md` - Full Cluster Ops documentation
- `skills/gitops/SKILL.md` - Full GitOps documentation
- `skills/security/SKILL.md` - Full Security documentation
- `skills/observability/SKILL.md` - Full Observability documentation
- `skills/artifacts/SKILL.md` - Full Artifacts documentation
- `skills/developer-experience/SKILL.md` - Full Developer Experience documentation
- `skills/qmd/SKILL.md` - QMD local markdown search documentation
