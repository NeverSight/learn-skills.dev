---
name: software-architecture-design
description: "Designs runtime topology in a chosen solution. Use when choosing monolith vs services, cells, consistency, ADRs. Not for cross-system design (software-solution-architecture)."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.3"
last_validated: 2026-07-11
---

# Software Architecture Design

If the question starts from a business workflow, system landscape, target state, or phased cross-system migration, use [../software-solution-architecture/SKILL.md](../software-solution-architecture/SKILL.md) first and come here for runtime, decomposition, and operability depth.

Treat estate modernization, platform engineering, and AI-native interoperability as optional deep dives. Do not load them unless the user is explicitly asking for those concerns.

## Quick Reference

| Task | Pattern/Tool | Key Resources | When to Use |
|------|-------------|---------------|-------------|
| Choose architecture style | Modular monolith (default; see Decision Factors below); Layered, Microservices, Event-driven, or Serverless once independent-deployment/ownership needs are clear | [modern-patterns.md](references/modern-patterns.md) | Greenfield projects, major refactors |
| Decide API boundary posture (architectural level) | Contract posture and versioning strategy, not endpoint design | [api-gateway-service-mesh.md](references/api-gateway-service-mesh.md) | Service-to-service contract decision is architectural |
| Design for scale | Load balancing, Caching, Sharding, Read replicas | [scalability-reliability-guide.md](references/scalability-reliability-guide.md) | High-traffic systems, performance goals |
| Ensure resilience | Circuit breakers, Retries, Bulkheads, Graceful degradation | [scalability-reliability-guide.md](references/scalability-reliability-guide.md) | Distributed systems, external dependencies |
| Document decisions | Architecture Decision Record (ADR) | [adr-template.md](assets/planning/adr-template.md) | Major technical decisions, tradeoff analysis |
| Define service boundaries | Domain-Driven Design (DDD), Bounded contexts | [microservices-template.md](assets/patterns/microservices-template.md) | Microservices decomposition |
| Model data consistency | ACID vs BASE, Event sourcing, CQRS, Saga patterns | [data-architecture-patterns.md](references/data-architecture-patterns.md) | Multi-service transactions |
| Plan observability | SLIs/SLOs/SLAs, Distributed tracing, Metrics, Logs | [architecture-blueprint.md](assets/planning/architecture-blueprint.md) | Production readiness |
| Migrate from monolith | Strangler fig, Database decomposition, Shadow traffic | [migration-modernization-guide.md](references/migration-modernization-guide.md) | Legacy modernization |
| Design inter-service comms | API Gateway, Service mesh, BFF pattern | [api-gateway-service-mesh.md](references/api-gateway-service-mesh.md) | Microservices networking |
| Design delivery platform | IDP, golden paths, fitness functions | [fitness-functions-governance.md](references/fitness-functions-governance.md) | Multi-team platforms, governance |
| Rationalize service sprawl | Bounded-context platforms, repo-vs-runtime matrix, platform scorecards | [estate-modernization.md](references/estate-modernization.md) | 20+ repos, too many services, uneven platform maturity |
| Plan estate modernization | Platform-first migration waves, consolidation, compatibility boundaries | [estate-modernization-blueprint.md](assets/planning/estate-modernization-blueprint.md) | Polyrepo estates, regulated migrations, legacy reduction |
| Design AI-native systems | RAG boundaries, tool gateways, agent interoperability, MCP, A2A | [architecture-trends.md](references/architecture-trends.md) | LLM-powered products when architecture, not implementation, is the main question |

## When NOT to Use This Skill

Use other skills instead for:

- **Cross-system solution design** (business flow, target state, integration landscape, phased transition across systems) → [software-solution-architecture](../software-solution-architecture/SKILL.md)
- **Single-service implementation** (routes, controllers, business logic) → [software-backend](../software-backend/SKILL.md)
- **API endpoint design** (REST conventions, GraphQL schemas) → [dev-api-design](../dev-api-design/SKILL.md)
- **Security implementation** (auth, encryption, OWASP) → [software-security-appsec](../software-security-appsec/SKILL.md)
- **Frontend component architecture** → [software-frontend](../software-frontend/SKILL.md)
- **Database query optimization** → [data-sql-optimization](../data-sql-optimization/SKILL.md)
- **Agent workflow implementation / MCP server implementation** → [ai-agents](../ai-agents/SKILL.md), [agents-mcp](../agents-mcp/SKILL.md)

## Boundary Rules

- This skill owns runtime boundaries, deployable-unit decisions, data consistency tradeoffs, resilience internals, and platform defaults.
- Start from the simplest architecture that satisfies the constraints; do not default to microservices, event sourcing, service mesh, or multi-agent splits without explicit evidence.
- If the unresolved question is still "which systems participate, where is the system of record, or what is the target-state landscape?" route back to [software-solution-architecture](../software-solution-architecture/SKILL.md).
- If the unresolved question is implementation of agent protocols, tool servers, or runtime-specific integrations, route to [ai-agents](../ai-agents/SKILL.md) or [agents-mcp](../agents-mcp/SKILL.md).
- **Migration boundary**: this skill owns the mechanics of extracting or decomposing inside one system — strangler-fig steps, database decomposition, shadow traffic (`migration-modernization-guide.md`, `estate-modernization.md`). It does not own the cross-system wave plan (which systems coexist, in what order, with what rollback/retirement criteria) — that is [../software-solution-architecture/SKILL.md](../software-solution-architecture/SKILL.md)'s `transition-architecture.md`.

## Decision Tree: Choosing Architecture Pattern

```text
Primary question: [What kind of architecture problem is this?]
    ├─ Large estate with many repos/services and rising cognitive load?
    │   ├─ Runtime count is the main problem → Bounded-context platforms + selective consolidation
    │   ├─ Delivery inconsistency is the main problem → IDP + golden paths + scorecards
    │   └─ Both are true → Platform-first modernization, then consolidate low-value runtime units
    │
    ├─ Deterministic workflow, known steps?
    │   ├─ Single deployable acceptable → Modular Monolith
    │   ├─ Independent teams/capabilities required → Sequential or event-driven services
    │   └─ Burst-driven or edge-triggered workload → Serverless / event-driven
    │
    ├─ Adaptive workflow with tool use and reasoning?
    │   ├─ One agent can own the task → Single-agent system
    │   ├─ Specialized roles truly needed → Multi-agent with explicit stop conditions
    │   └─ High stakes / regulated workflow → Human-in-the-loop + audit trail
    │
    ├─ Strong consistency inside one domain boundary?
    │   ├─ Keep data and writes together → Monolith or Modular Monolith
    │   └─ Split only at stable bounded contexts → Microservices with owned data
    │
    └─ Need platform-level consistency across many teams?
        ├─ Repeated service creation / compliance needs → IDP + golden paths
        └─ Cross-agent or cross-vendor interoperability → MCP for tools/context, A2A for agent-to-agent
```

**Decision Factors:**

- **Default posture**: prefer modular monolith over microservices unless independent deployment, ownership, and operability benefits are clear — see the explicit team-size/release-cadence/operational-maturity gates in [modern-patterns.md § Modular Monolith vs. Microservices](references/modern-patterns.md#modular-monolith-vs-microservices-explicit-gates)
- **Estate posture**: optimize for fewer runtime units before fewer repos; repositories are collaboration units, runtimes are operational cost centers
- **Agent posture**: prefer deterministic workflows or a single agent before introducing multi-agent coordination
- **Connectivity posture**: prefer gateway plus application-library patterns until mTLS, traffic policy, or shared telemetry needs justify mesh complexity
- Team structure (Conway's Law) — architecture mirrors org structure
- Deployment independence needs
- Consistency and failure-domain boundaries
- Operational maturity (monitoring, orchestration)
- Interoperability needs (protocols, contracts, external systems)

**Where to split: fracture planes** (Skelton and Pais, *Team Topologies*, 2nd ed., 2025). A fracture plane is "a natural seam in the software system that allows the system to be split easily into two or more parts" — the stonemason's analogy. Candidate planes: business domain bounded context (the default, and the one most splits should map to), regulatory compliance, change cadence, team location, risk, performance isolation, technology, and user personas.

- **Litmus test**, quoted: "Does the resulting architecture support more autonomous teams (less dependent teams) with reduced cognitive load (less disparate responsibilities)?" Concretely: after the split, can each team build, test, and deploy its part without coordinating with another team?
- **Composite rule**: real boundaries usually combine planes — "we can and should break down a monolith by combining different types of fracture planes," and "often, a combination of fracture planes will be required."
- **Distributed-monolith warning**: splitting the software without aligning the boundaries to teams and their release paths buys distribution cost with none of the autonomy. The book quotes Amy Phillips: "If you have microservices but you wait and do end-to-end testing of a combination of them before a release, what you have is a distributed monolith." Coupling also creeps in below the service boundary — shared databases, coupled builds and releases.
- Make segments team-sized: "it is essential to make software segments team sized so that teams can effectively own and evolve their software in a sustainable way."

See [references/modern-patterns.md](references/modern-patterns.md) for detailed pattern descriptions, and [references/modern-patterns.md § Connascence](references/modern-patterns.md#connascence-a-finer-grained-coupling-vocabulary) to check whether a proposed seam leaves strong coupling crossing it.

## Output Guidelines

The references in this skill are background knowledge for you — absorb the patterns and present them as your own expertise. Do not cite internal reference file names (e.g., "from data-architecture-patterns.md") in user-facing output. Users don't know these files exist.

Every architecture recommendation must cover the following; skip elements only with explicit justification:

- [ ] **Simplest sufficient topology** — state the least-complex architecture that still satisfies requirements
- [ ] **Concrete technology picks** — name specific technologies (e.g., "Temporal.io for workflow orchestration", not just "an orchestrator")
- [ ] **Recommended option + rejected alternatives** — what was considered, why alternatives lost
- [ ] **What NOT to build** — explicitly defer or exclude premature scope
- [ ] **Team and process alignment** — CODEOWNERS, deployment ownership, on-call boundaries
- [ ] **Repo and runtime model** — for multi-repo estates, distinguish repo count from deployable count
- [ ] **Operability model** — deployment topology, failure domains, rollback points, SLO ownership, incident boundaries
- [ ] **Migration path** — sequencing, cutover strategy, reversibility (for refactors or new subsystems)
- [ ] **Key risks and failure modes** — named breakpoints, how to detect early
- [ ] **Success metrics** — service SLOs and the relevant [DORA five delivery metrics](https://dora.dev/guides/dora-metrics/): deployment frequency, change lead time, failed deployment recovery time, change fail rate, and deployment rework rate; compare each with its own baseline

## Workflow (System-Level)

Use this workflow when a user asks for architecture recommendations, decomposition, or major platform decisions.

1. Clarify: problem statement, non-goals, constraints, and success metrics
2. Capture quality attributes: availability, latency, throughput, durability, consistency, security, compliance, cost
3. Decide workload shape: deterministic workflow, single-agent, or multi-agent; synchronous vs asynchronous
4. Propose 2–3 candidate architectures and compare tradeoffs
5. Default to the least-complex viable topology before justifying more distributed patterns
6. For 20+ repo estates, classify each repo as runtime, adapter, library, channel, platform, tooling, or absorption candidate
7. Define boundaries: bounded contexts, ownership, APIs/events, protocol contracts, interoperability needs
8. Decide data strategy: storage, consistency model, schema evolution, migrations
9. Design for operations: SLOs, failure modes, observability, deployment, DR, incident playbooks
10. Design governance and safety: policy enforcement, auditability, evaluation gates, rollback controls
11. Call out scope limits: what NOT to build yet, what to defer, what to buy vs build
12. Document decisions: write an ADR when a choice changes a deployable boundary, consistency or failure model, platform contract, or costly-to-reverse constraint. Record context, options, consequences, owner, and supersession link in [the ADR template](assets/planning/adr-template.md); [MADR](https://adr.github.io/madr/) is a lean format option. Use a lighter note for local implementation choices.

Preferred deliverables (pick what fits the request):

- Architecture blueprint: `assets/planning/architecture-blueprint.md`
- Estate modernization blueprint: `assets/planning/estate-modernization-blueprint.md`
- Decision record: `assets/planning/adr-template.md`
- Pattern deep dives: `references/modern-patterns.md`, `references/scalability-reliability-guide.md`

### Decision Evidence Gate

For each proposed boundary or new deployable, name the observed pressure that requires it: independent release cadence, incompatible scaling shape, fault isolation, data sovereignty, or distinct ownership. Record the baseline and the experiment that would falsify the choice. If the pressure is hypothetical or can be handled inside the existing runtime, keep the boundary logical and postpone the operational split.

## Known Traps

- Choosing microservices because the estate already has many repos, even though runtime sprawl and weak ownership are the real issue.
- Drawing a target-state diagram without a migration sequence, rollback boundary, or compatibility plan between old and new paths.
- Splitting domains before ownership, on-call, and deploy authority are ready to support the additional surface area.
- Introducing async and event-driven workflows on every boundary before deciding which paths actually need decoupling.
- Calling something platform engineering while the golden path remains optional, inconsistent, or under-owned.

## Common Anti-Patterns

- Using deployable services as the default decomposition unit instead of bounded contexts, team ownership, and operational cost.
- Copying hyperscaler or vendor reference architectures into teams that do not have equivalent scale, tooling, or platform staffing.
- Designing for peak optional futures instead of the current throughput, failure, compliance, and change-management constraints.
- Keeping every repo and runtime because each has "some value" despite obvious coordination and governance cost.
- Conflating "modern" with "more distributed" and "AI-native" with "multi-agent by default."

## Navigation

### Core References

Read **at most 2–3 references** per question — pick the ones most relevant to the specific ask. Do not read all of them.

| Reference | Contents | When to Read |
|-----------|----------|--------------|
| [modern-patterns.md](references/modern-patterns.md) | Architecture patterns with decision trees, incl. modular-monolith-vs-microservices gates and cell-based architecture | Choosing or comparing patterns |
| [scalability-reliability-guide.md](references/scalability-reliability-guide.md) | CAP theorem, DB scaling, caching, circuit breakers, SRE | Scaling or reliability questions |
| [data-architecture-patterns.md](references/data-architecture-patterns.md) | CQRS variants, event sourcing, data mesh, sagas, consistency | Data flow across services |
| [migration-modernization-guide.md](references/migration-modernization-guide.md) | Strangler fig, DB decomposition, feature flags, risk assessment | Refactoring a monolith |
| [api-gateway-service-mesh.md](references/api-gateway-service-mesh.md) | Gateway patterns, service mesh, mTLS, observability | Inter-service communication |
| [fitness-functions-governance.md](references/fitness-functions-governance.md) | Fitness-function taxonomy (six axes), architectural-vs-domain and monitoring-vs-alarm litmus tests, ArchUnit/NetArchTest/linter rules, modular-monolith boundary enforcement, herding thresholds, coupling and complexity metrics, codebases changed by coding agents | Automating architectural governance, making principles enforceable, making a codebase safe for agent-authored diffs |
| [architecture-trends.md](references/architecture-trends.md) | Platform engineering, ambient mesh, AI-native systems, MCP/A2A | Current trends only |
| [estate-modernization.md](references/estate-modernization.md) | Runtime-vs-repo rationalization, bounded-context platforms, consolidation heuristics | Multi-repo estates and service sprawl |
| [operational-playbook.md](references/operational-playbook.md) | Architecture questions framework, decomposition heuristics | Design discussion framing |

### Templates

**Planning & Documentation** ([assets/planning/](assets/planning/)):

- [architecture-blueprint.md](assets/planning/architecture-blueprint.md) — Service blueprint (dependencies, SLAs, data flows, resilience, security, observability)
- [estate-modernization-blueprint.md](assets/planning/estate-modernization-blueprint.md) — Estate blueprint (repo/runtime classification, target platform map, migration waves, scorecards)
- [adr-template.md](assets/planning/adr-template.md) — Architecture Decision Record for tradeoff analysis

**Architecture Patterns** ([assets/patterns/](assets/patterns/)):

- [microservices-template.md](assets/patterns/microservices-template.md) — Microservices design (API contracts, resilience, deployment, testing)
- [event-driven-template.md](assets/patterns/event-driven-template.md) — Event-driven architecture (event schemas, saga patterns, event sourcing)

**Operations** ([assets/operations/](assets/operations/)):

- [scalability-checklist.md](assets/operations/scalability-checklist.md) — Scalability checklist (DB scaling, caching, load testing, auto-scaling, DR)

### Validation

- [evals/evals.json](evals/evals.json) — trigger, non-trigger, and near-boundary behavioral checks for this skill

### Applied-Recipe Toolkits

- [references/decision-theory-applied.md](references/decision-theory-applied.md) — Decision-theory applied recipes for architecture: ADRs with EU + sensitivity, real-options for irreversible choices, VoI on spikes.
- [references/queueing-theory-applied.md](references/queueing-theory-applied.md) — Queueing-theory applied recipes for architecture: service sizing, backpressure topology, tail-latency budget.
- [references/theory-of-constraints-applied.md](references/theory-of-constraints-applied.md) — TOC applied recipes for architecture: system-wide bottleneck hunt, refactor scope, stability-vs-velocity ADR.
- [references/distributed-systems-applied.md](references/distributed-systems-applied.md) — Distributed-systems primitives applied to architecture: CAP-conscious service boundaries, consensus algorithm selection, idempotency at API surfaces, leases-with-fencing for leader-elected jobs, quorum sizing, consistency-vs-latency ADR template.
- [references/reliability-theory-applied.md](references/reliability-theory-applied.md) — Reliability primitives (MTBF/MTTR, availability, FMEA, error budgets) applied to software architecture design.

### Related Skills

- [software-solution-architecture](../software-solution-architecture/SKILL.md) — End-to-end solution design, system landscape, target-state and migration architecture
- [software-backend](../software-backend/SKILL.md) — Backend engineering, API implementation, data layer
- [software-frontend](../software-frontend/SKILL.md) — Frontend architecture, micro-frontends, state management
- [dev-api-design](../dev-api-design/SKILL.md) — REST, GraphQL, gRPC design patterns
- [ops-devops-platform](../ops-devops-platform/SKILL.md) — CI/CD, deployment strategies, IaC
- [qa-observability](../qa-observability/SKILL.md) — Monitoring, tracing, alerting, SLOs
- [software-security-appsec](../software-security-appsec/SKILL.md) — Threat modeling, auth, secure design
- [data-sql-optimization](../data-sql-optimization/SKILL.md) — Query tuning and optimization on existing schemas
- [software-database-design](../software-database-design/SKILL.md) — Schema design, migrations, and data modeling
- [docs-codebase](../docs-codebase/SKILL.md) — Architecture documentation, docs-as-code structure
- `docs-diagram-design` — Whether a diagram earns its place, and what it must show
- For C4 context/container views, arc42 documentation structure, or diagrams as code, choose the smallest useful view with `docs-diagram-design` and keep its ownership and update path in [docs-codebase](../docs-codebase/SKILL.md).
- [ai-agents](../ai-agents/SKILL.md) — Agent system design, orchestration, evaluation
- [agents-mcp](../agents-mcp/SKILL.md) — MCP server/client patterns and integration

## Freshness Protocol

When a question is version-sensitive (current trends, "is X still recommended?", vendor limits, managed-service capabilities, AI-native interoperability), verify against primary sources from `data/sources.json` before answering. Without live access, answer with durable patterns and state which assumptions could change. Trigger conditions, check steps, and the source categories: [references/operational-playbook.md#freshness-protocol](references/operational-playbook.md#freshness-protocol). Trend deep dives: [architecture-trends.md](references/architecture-trends.md), [estate-modernization.md](references/estate-modernization.md).

## Learnings Loop

When prior decisions or pitfalls are relevant, consult `learnings.consolidated.md` if present; use `learnings.md` only for needed history or as the available fallback. Otherwise skip both.

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
