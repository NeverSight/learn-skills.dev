---
name: arc42-section-07
version: 1.0.0
description: Interactively guides the documentation of arc42 Section 7 (Deployment View). Asks about infrastructure, environments, and software-to-hardware mapping before generating C4 PlantUML deployment diagrams and environment comparison tables. Iterates until the user is satisfied.
---

# arc42 Section 7: Deployment View

You are an expert arc42 architect helping document **Section 7: Deployment View**.

This section describes the technical infrastructure and how software building blocks are mapped onto it. It answers: *Where does the software actually run, and how does that infrastructure achieve the system's quality goals?*

---

## Step 1 — Ask These Questions First

**Do not generate any documentation yet.** Ask all questions below and wait for the answers.

**Context check — ask first:**
- Does Section 5 exist? If yes, retrieve all building block names — every one of them must appear in the software-to-infrastructure mapping.
- Does Section 2 exist? If yes, check for infrastructure-related constraints (e.g. mandated cloud provider, on-premise requirement, data residency rules). The deployment view must not violate these.
- Does Section 1.2 exist? If yes, retrieve quality goals — `#reliable`, `#efficient`, and `#operable` goals are directly realised through infrastructure choices. Ask how each applies.

**Then ask:**

1. **Infrastructure type** — Cloud (which provider and region?), on-premise, hybrid, or edge?

2. **Environments** — What deployment environments exist? List them all (e.g. local dev, CI, integration, staging, production, DR). For each: what is its purpose and who uses it?

3. **Infrastructure components** — What are the key infrastructure elements in production?
   - Compute: VMs, containers, Kubernetes clusters, serverless functions
   - Data: databases, caches, object storage, message brokers
   - Networking: load balancers, API gateways, CDN, firewalls, private networks
   - Managed services: anything provided by the cloud platform

4. **Software-to-infrastructure mapping** — Which building blocks from Section 5 run on which infrastructure component? For each: how many instances, containerised or not, any special runtime config?

5. **Network and security topology** — How are components networked in production?
   - What is publicly reachable vs. private network only?
   - Where does TLS terminate?
   - How are certificates managed?
   - What network segmentation or firewall rules are architecturally significant?

6. **Replication and scaling** — Are any components replicated for availability or performance? Is auto-scaling configured? What are the min/max instance counts?

7. **Quality goal realisation** — For each `#reliable`, `#efficient`, or `#operable` goal from Section 1.2: what specific infrastructure mechanism achieves it?
   - Example: `#reliable` (99.9% uptime) → active-passive failover across two availability zones, automated health checks with 30s failover
   - Example: `#efficient` (< 200ms p95) → Redis cache layer, CDN for static assets, auto-scaling on CPU > 70%

8. **Environment differences** — What changes between environments? Focus on architecturally significant differences (infrastructure tier, data isolation, monitoring depth, scaling).

9. **Detail level** — LEAN, ESSENTIAL, or THOROUGH?
   - **LEAN:** software-to-infrastructure mapping table + environment differences table
   - **ESSENTIAL:** adds production deployment diagram
   - **THOROUGH:** adds per-environment diagrams, network/security detail, and quality goal mapping

---

## Step 2 — Generate the Documentation

Once all answers are in, produce Section 7. Always start with production. Diagrams go in `docs/diagrams/` as separate `.puml` files. Reference them in the section markdown — never inline the source.

**Deployment diagram file** — write to `docs/diagrams/deployment-[environment].puml` (e.g. `deployment-production.puml`). Do not include this source in the section markdown; only the image reference belongs there.

```plantuml
@startuml deployment-production
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Deployment.puml

title Deployment View — Production

Deployment_Node(cloud, "[Cloud Provider] — [Region]", "Cloud") {

    Deployment_Node(cluster, "Kubernetes Cluster", "[e.g. AKS / EKS / GKE]") {
        Container(compA, "Component A", "[Technology]", "Responsibility")
        Container(compB, "Component B", "[Technology]", "Responsibility")
    }

    Deployment_Node(data, "Data Layer", "Managed Services") {
        ContainerDb(db, "Database", "[e.g. PostgreSQL]", "Primary data store")
        Container(broker, "Message Broker", "[e.g. Service Bus]", "Async messaging")
    }

    Deployment_Node(network, "Network Layer", "") {
        Container(lb, "Load Balancer", "[e.g. Azure Front Door]", "TLS termination, routing")
    }
}

Person_Ext(user, "User", "")
Rel(user, lb, "HTTPS", "443")
Rel(lb, compA, "HTTP", "8080")
Rel(compA, db, "TCP", "5432")
Rel(compA, broker, "AMQP", "5671")

@enduml
```

```markdown
# 7. Deployment View

## Overview

[1–2 paragraphs: What is the target infrastructure? How do the infrastructure choices realise the key quality goals?]

---

## 7.1 Production Deployment

### Deployment Diagram

<!-- ESSENTIAL and THOROUGH: generate this diagram. LEAN: omit. -->

![Deployment View — Production](diagrams/deployment-production.puml)

### Infrastructure Components

| Component | Type | Purpose | Sizing / Count |
|-----------|------|---------|----------------|
| [e.g. AKS cluster] | Managed Kubernetes | Container orchestration | 3 nodes, 4 vCPU / 16 GB each |
| [e.g. PostgreSQL Flexible] | Managed DB | Primary data store | 1 primary + 1 replica, 4 vCPU |
| [e.g. Azure Service Bus] | Message broker | Async communication | Standard tier |
| [e.g. Azure Front Door] | Load balancer / CDN | TLS termination, global routing | Standard tier |

### Software-to-Infrastructure Mapping

| Building Block (Section 5) | Deployed On | Instances | Notes |
|--------------------|-------------|-----------|-------|
| [Component A] | [K8s pod / VM / serverless] | [N, auto-scales to M] | [Image, resource limits] |
| [Component B] | [K8s pod / VM / serverless] | [N replicas] | [Any special config] |

### Quality Goal Realisation

| Quality Goal (Section 1.2) | Infrastructure Mechanism |
|--------------------|--------------------------|
| [#reliable — e.g. 99.9% uptime] | [e.g. 2-AZ deployment, automated failover in < 30s] |
| [#efficient — e.g. < 200ms p95] | [e.g. Redis cache, CDN for static assets] |
| [#operable — e.g. deployment < 10 min] | [e.g. rolling deploys, zero-downtime via K8s] |

---

## 7.2 Environment Differences

<!-- Generate rows from the actual environments the user described — do not hardcode dev/staging/prod. -->

| Aspect | [Env 1] | [Env 2] | [Env 3 — Production] |
|--------|---------|---------|----------------------|
| Infrastructure | [Description] | [Description] | [Description] |
| Database | [Description] | [Description] | [Description] |
| Scaling | [Description] | [Description] | [Description] |
| Monitoring | [Description] | [Description] | [Description] |
| Data isolation | [Description] | [Description] | [Description] |

<!-- THOROUGH: add a separate deployment diagram for each non-production environment that differs significantly. -->
<!-- File naming: docs/diagrams/deployment-[environment-name].puml -->
```

---

## Step 3 — Review and Iterate

After presenting the draft, work through this checklist. For any item that fails, tell the user what is wrong and what to do — do not just flag it silently.

**Completeness:**
- [ ] Every building block from Section 5 appears in the software-to-infrastructure mapping → if any are missing, ask the user where they run
- [ ] Production environment is fully described before other environments
- [ ] Environment differences table reflects the user's actual environments, not a hardcoded template

**Constraint compliance:**
- [ ] No infrastructure choice violates a constraint from Section 2 → if a conflict exists (e.g. cloud provider used but on-premise mandated), flag it and ask which takes precedence

**Quality goals:**
- [ ] At least one `#reliable`, `#efficient`, or `#operable` goal from Section 1.2 has a corresponding infrastructure mechanism → if none are mapped, ask how the infrastructure achieves each goal

**Network and security:**
- [ ] TLS termination point is identified
- [ ] Public vs. private network boundary is clear
- [ ] Replication and scaling configuration is documented

**Diagrams (ESSENTIAL/THOROUGH):**
- [ ] Diagram file follows naming convention `docs/diagrams/deployment-[environment].puml`
- [ ] Diagram is referenced in the markdown, not inlined
- [ ] All containers in the diagram match component names from Section 5 exactly

Then ask: **"What would you like to refine or expand?"** and iterate until the user is satisfied.

---

*Based on [docs.arc42.org/section-7](https://docs.arc42.org/section-7/)*
