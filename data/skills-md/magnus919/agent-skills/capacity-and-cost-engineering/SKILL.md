---
name: capacity-and-cost-engineering
description: >-
  Model technical capacity, unit cost, and budget constraints connected to
  demand, performance, and reliability decisions. Use when projecting capacity
  from growth forecasts, sizing for peak events, designing cost-aware scaling
  policies, defining budget thresholds or quota/rate-limit enforcement, running
  or planning load/soak tests as capacity evidence, resolving SLO-cost tradeoffs,
  or modeling multi-tenant demand distributions, hot-tenant skew, pooled or siloed
  headroom, fairness evidence, and tenant-variable unit cost. Do NOT use for
  financial P&L statements, fundraising scenarios, or SaaS metrics (route to
  financial-modeling); for infrastructure implementation or cloud-resource
  provisioning (route to platform-engineering); or for generic cloud-cost tips
  and universal utilization targets — this skill does not prescribe fixed savings
  rates or one-size-fits-all thresholds.
license: MIT
compatibility: Platform-agnostic methodology. No runtime dependency.
metadata:
  tags: capacity-engineering, cost-engineering, unit-economics, load-testing,
    capacity-planning, budget-controls, quota-management, rate-limiting,
    cost-performance-tradeoffs, scaling-models, utilization-modeling,
    multi-tenant-capacity, tenant-unit-cost
---

# Capacity and Cost Engineering

Connect demand, performance, reliability, and spend into defensible capacity and cost decisions. This skill models technical capacity, calculates unit cost at the infrastructure level, defines budget and quota controls, requires load/soak evidence for capacity claims, and makes cost-performance tradeoffs explicit — producing evidence that feeds [production-readiness](../production-readiness/SKILL.md) launch decisions and constrains or supports [site-reliability-engineering](../site-reliability-engineering/SKILL.md) SLO choices.

## Connected dimensions

Demand (traffic and growth), performance (latency and throughput), reliability (SLOs and error budgets), and spend (cost) are treated as **connected dimensions** — a change in any one dimension affects the others. The skill's core method is tracing the connection:

| Dimension | Capacity impact | Cost impact |
|-----------|----------------|-------------|
| Demand (traffic, growth rate) | Drives compute, storage, network requirements | Drives baseline and projected spend |
| Performance (latency, throughput target) | Constrains resource headroom per request | Tighter targets increase unit cost |
| Reliability (SLO, error budget) | Requires redundancy, over-provisioning, or isolation | Higher SLOs increase cost non-linearly |
| Spend (budget, cost constraint) | Caps capacity; may force degraded-mode operation | Limits what SLO/performance targets are achievable |

A capacity decision that changes one dimension without modeling the others is incomplete. Every capacity model, unit-cost calculation, and budget decision in this skill must name at least one connection to another dimension with evidence or an explicit assumption.

## Loading Guide

Load this skill when the task involves any of:

| Trigger | What to load |
|---------|-------------|
| Project capacity from a growth forecast | `SKILL.md` + `templates/capacity-model.md` |
| Size capacity for a peak event (launch, Black Friday, seasonal) | `SKILL.md` + `templates/capacity-model.md` + `templates/load-soak-test-plan.md` |
| Calculate unit cost and connect to SLO or demand decisions | `SKILL.md` + `templates/unit-economics-record.md` |
| Define a budget threshold, spending alert, or hard cap | `SKILL.md` + `templates/budget-quota-decision.md` |
| Design quota or rate-limit enforcement in operational context | `SKILL.md` + `templates/budget-quota-decision.md` |
| Plan or review a load/soak test as capacity evidence | `SKILL.md` + `templates/load-soak-test-plan.md` |
| Resolve an SLO-cost tradeoff or cost-constrained reliability decision | `SKILL.md` + `templates/slo-cost-tradeoff-record.md` |
| Review a cost anomaly or attribute cost to services/teams | `SKILL.md` + `templates/unit-economics-record.md` |
| Model multi-tenant demand, skew, fairness, or tenant-variable unit cost | `SKILL.md` + `references/multi-tenant-capacity-and-unit-cost.md` + `templates/tenant-capacity-model.md` |
| Understand ownership boundaries with adjacent skills | `SKILL.md` + `references/discovery-brief.md` |

## Working method

### 1. Model demand and capacity

Start with the demand signal: current traffic, growth rate, and any known peak events. Translate demand into capacity requirements using a capacity model that connects:

- **Demand units** (requests/second, concurrent users, GB ingested, messages/second) to
- **Capacity units** (vCPUs, memory GB, storage GB, IOPS, network throughput, provisioned throughput units) through
- **Utilization targets** (maximum sustainable utilization per resource, stated with rationale — never a universal percentage without context).

A capacity model is incomplete without a stated utilization target, the evidence for that target (why 70% and not 85%?), and the scaling trigger that fires when utilization approaches the target.

Use the **capacity model template** (`templates/capacity-model.md`) which captures demand assumptions, capacity-unit mapping, utilization targets with rationale, scaling triggers, and a projection over the relevant horizon. The template requires fields for assumptions, evidence source, ownership, and tradeoffs.

### 2. Calculate unit cost

Unit cost is the cost of serving one unit of demand — cost per request, cost per user per month, cost per GB stored, cost per provisioned capacity unit. Unit cost connects infrastructure spend to product and reliability decisions.

Calculate unit cost as:

```
unit cost = total cost of capacity / number of demand units served
```

Both numerator and denominator must be measured over the same period, with the same scope (service, team, or platform), and with the same allocation method stated (direct resource cost, attributed shared cost, or fully loaded cost including overhead).

The **unit-economics record template** (`templates/unit-economics-record.md`) requires: the unit definition, the cost numerator with allocation method, the demand denominator with measurement source, the resulting unit cost, a cost-per-SLO comparison (what happens to unit cost at 99.9% vs 99.99%?), and an assumptions/evidence/ownership/tradeoffs section. The template includes a structured field for the unit-cost calculation formula.

For a multi-tenant service, do not use a fleet average as the only unit. Load
`references/multi-tenant-capacity-and-unit-cost.md` and distinguish platform
baseline cost from tenant-variable cost, then report a distribution of tenant
costs or resource consumption. A tenant's variable unit cost may depend on
request mix, storage, background work, burst shape, placement, and tier
entitlements. Shared-cost allocation is an explicit modeling choice, not a
claim that every tenant consumes an equal share.

### 3. Define budget and quota controls

Budget controls are spending limits with operational consequences — spending alerts at thresholds, hard caps that prevent further spend, and the operational behavior when a cap is hit (degrade, throttle, or stop). Quota and rate-limit enforcement are the mechanisms that implement budget controls at the request or resource level.

Budget controls operate at three levels:

| Level | Mechanism | Operational consequence |
|-------|-----------|------------------------|
| **Alert** | Spending threshold notification | No automated action; triggers review |
| **Soft cap** | Throttling, degraded mode, reduced provisioning | Service continues at reduced capacity |
| **Hard cap** | Rate limiting, quota enforcement, resource denial | Requests above cap are rejected |

Budget controls must specify what happens at each threshold — the operational behavior, the user-facing impact, and the owner accountable for responding. A budget threshold without a defined operational consequence is incomplete.

The **budget/quota decision template** (`templates/budget-quota-decision.md`) captures: budget owner, period, thresholds (alert/soft/hard), quota or rate-limit configuration, enforcement mechanism, operational behavior at each threshold, cost attribution method, anomaly detection triggers, and approval record.

### 4. Require load/soak evidence

**Load and soak test evidence is required for capacity decisions.** A capacity model alone — without observed system behavior under representative load — is insufficient evidence for a capacity claim or a scaling policy.

- A **load test** exercises the system at a target throughput (e.g., expected peak + 20% headroom) for a defined duration and measures latency, error rate, and resource utilization.
- A **soak test** exercises the system at a sustained load over an extended period (hours to days) and detects slow leaks (memory, file descriptors, connection pools, disk growth) that a short load test misses.

The **load/soak test plan template** (`templates/load-soak-test-plan.md`) captures: test objective, target throughput with rationale, duration, environment (must be representative — a dev-environment test is not sufficient), success criteria (latency percentiles, error rate, resource utilization), data collection plan, and the evidence record. The template distinguishes a component-level benchmark from an end-to-end test; a capacity decision must state which boundary was exercised.

Modeling without test evidence, or testing without a model, is incomplete. Both are required.

For multi-tenant claims, the evidence must exercise representative tenant
profiles together, including ordinary tenants, high-demand tenants, bursty
tenants, and relevant tier or placement variants. A single-tenant benchmark or
fleet-average test cannot establish protection against hot tenants, partition
skew, or fairness behavior.

### 5. Resolve SLO-cost tradeoffs

An SLO-cost tradeoff arises when the cost of meeting an SLO at projected demand exceeds the budget, or when a budget constraint forces a lower SLO than the team would otherwise target. This is a structured decision, not an implicit acceptance.

The **SLO-cost tradeoff record template** (`templates/slo-cost-tradeoff-record.md`) captures: the SLO under discussion, current cost to meet it, projected cost at demand forecast, alternative SLO with cost comparison, degradation path if the lower SLO is chosen, error budget impact, accountable owner, and approval record. The template requires surfacing the tradeoff with evidence (cost projection, load-test data) and ownership (who decides and who is accountable).

## Scenarios

### Growth scenario

Demand is growing predictably (e.g., 15% month-over-month). The question: when does current capacity become insufficient, and what does it cost to stay ahead of growth?

Guidance:
1. Project demand forward using the growth rate, with confidence intervals.
2. Model capacity at current utilization targets; identify the resource that saturates first.
3. Calculate the cost of incremental capacity at each scaling step.
4. Define the scaling trigger — the utilization threshold at which provisioning must begin (lead time matters).
5. Record assumptions (growth rate stability, no step-change events, current utilization pattern holds) and evidence sources.

### Peak scenario

A known event will drive traffic well above baseline (product launch, Black Friday, seasonal peak). The question: how much capacity is needed for the peak, what does it cost, and is the cost justified?

Guidance:
1. Model peak demand separately from baseline — peak shape (height, duration, ramp), not just the peak number.
2. Size capacity for the peak, not the average. Include headroom.
3. Run a load test at the projected peak throughput before the event. A model without load evidence is insufficient.
4. Define the post-peak scale-down plan and its trigger — capacity that persists after the peak incurs unnecessary cost.
5. If peak capacity cost exceeds budget, model a degraded peak alternative (which functions shed, what users experience).

### Degraded scenario

A dependency fails or a resource constraint forces operation below full capacity. The question: what does the system look like in degraded mode, what capacity is needed for the core path, and what does degraded operation cost?

Guidance:
1. Tier functions: core (must preserve) vs enhancing (can shed). Route degradation-path design to [resilience-and-recovery](../resilience-and-recovery/SKILL.md).
2. Model capacity for core-path-only operation — what resources are freed by shedding enhancing functions.
3. Calculate the cost of degraded operation (may be lower than full operation, or higher if failover resources activate).
4. Define the maximum degraded-operation window — how long degraded mode can persist before escalation.
5. Ensure the degraded capacity model is exercised in a game day or chaos test (route to resilience-and-recovery for exercise design).

### Cost-constrained scenario

A budget constraint prevents provisioning to the ideal capacity or SLO target. The question: what is the best achievable reliability and performance within the budget, and who decides?

Guidance:
1. Start from the budget constraint — state the cap explicitly (monthly, quarterly, annual).
2. Model the capacity that the budget can purchase at current unit costs.
3. Calculate the SLO and performance targets that capacity can support.
4. Compare to the unconstrained ideal: what SLO, latency, and throughput are being traded away.
5. Produce an SLO-cost tradeoff record with an accountable owner. Cost optimization must not degrade reliability, privacy, or user outcomes — if the budget cannot support an acceptable SLO, the decision is escalated, not silently accepted.

**Cost optimization must not justify degrading reliability, privacy, or user outcomes.** If a cost constraint forces a choice between budget and these non-negotiables, the tradeoff is escalated to an accountable owner with the evidence — it is never silently accepted as an optimization.

## When not to use

This skill does **not** provide generic cloud-cost tips (reserved instances, spot instances, "turn off unused resources," "right-size," savings plans). Those are platform-specific implementation tactics that belong in [platform-engineering](../platform-engineering/SKILL.md) references or cloud-provider documentation, not in a capacity-and-cost methodology skill. This skill owns the *decision framework* and *evidence standard* for capacity and cost — not a list of cost-cutting tips.

This skill does **not** prescribe universal utilization targets. A utilization target of 70% for a latency-sensitive service with spiky traffic is not the same as 85% for a batch-processing pipeline with predictable load. Every utilization target must be stated with context, rationale, and the evidence that supports it. "Target 70% utilization" without context is not a capacity decision — it is a guess.

This skill does **not** permit cost optimization to justify degrading reliability, privacy, or user outcomes. These are non-negotiable constraints. A cost-constrained scenario that would violate them must be escalated, not optimized around.

## Routing table

| When the task involves... | Route to... |
|---|---|
| P&L, fundraising, SaaS metrics (ARR/churn/NDR), pricing strategy | [financial-modeling](../financial-modeling/SKILL.md) |
| Infrastructure implementation, autoscaling, cloud provisioning, cost-allocation tags | [platform-engineering](../platform-engineering/SKILL.md) |
| SLO definition, error budget policy, incident command, on-call operations | [site-reliability-engineering](../site-reliability-engineering/SKILL.md) |
| Demand measurement, traffic forecasting instrumentation, tracking plans | [product-analytics-and-measurement](../product-analytics-and-measurement/SKILL.md) |
| Launch decisions, cross-domain evidence assembly, go/no-go/defer/exception | [production-readiness](../production-readiness/SKILL.md) |
| Portfolio capacity allocation, bet sequencing, roadmap tradeoffs | [product-roadmapping-and-portfolio](../product-roadmapping-and-portfolio/SKILL.md) |
| Degradation-path design, recovery verification, RTO/RPO decisions, game days | [resilience-and-recovery](../resilience-and-recovery/SKILL.md) |
| Statistical modeling of demand, time-series forecasting, causal inference on growth drivers | [data-scientist](../data-scientist/SKILL.md) |
| Cost data pipeline implementation, spend-data ETL, cost-dashboard data models | [data-engineering](../data-engineering/SKILL.md) |
| End-to-end tenant semantics, control/application planes, tenancy choice, lifecycle, or billing handoffs | [multi-tenant-saas-architecture](../multi-tenant-saas-architecture/SKILL.md) |
| Tenant isolation threats, authorization, privileged support, or security controls | [secure-software-engineering](../secure-software-engineering/SKILL.md) |
| General architecture boundaries, topology, or decomposition decisions | [software-architecture](../software-architecture/SKILL.md) |

## File map

| Path | Loaded when |
|---|---|
| [references/discovery-brief.md](references/discovery-brief.md) | Understanding ownership boundaries and routing rules with adjacent skills |
| [templates/capacity-model.md](templates/capacity-model.md) | Building a demand-to-capacity projection with utilization targets and scaling triggers |
| [templates/unit-economics-record.md](templates/unit-economics-record.md) | Calculating unit cost and connecting it to SLO or demand decisions |
| [templates/budget-quota-decision.md](templates/budget-quota-decision.md) | Defining budget thresholds, quota limits, rate-limit enforcement, and operational consequences |
| [templates/load-soak-test-plan.md](templates/load-soak-test-plan.md) | Designing or reviewing a load or soak test as capacity evidence |
| [templates/slo-cost-tradeoff-record.md](templates/slo-cost-tradeoff-record.md) | Resolving an SLO-cost tradeoff with evidence, accountability, and approval |
| [references/multi-tenant-capacity-and-unit-cost.md](references/multi-tenant-capacity-and-unit-cost.md) | Modeling tenant distributions, skew, pooled/siloed headroom, tier promises, admission, fairness evidence, and cost allocation |
| [templates/tenant-capacity-model.md](templates/tenant-capacity-model.md) | Recording tenant profiles, partition behavior, headroom, quota/admission evidence, and tenant-variable unit cost |
| [references/source-index.md](references/source-index.md) | Public provenance and original-writing boundary for this methodology |
