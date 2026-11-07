---
name: architecture-decision-framework
description: How to decide architecture and technology from REQUIREMENTS, not trends. Use when choosing between modular monolith vs microservices, SQL vs NoSQL, serverless vs containers, queues vs workflows, or evaluating trade-offs and operational complexity.
when_to_use: |
  - monolith vs microservices
  - SQL vs NoSQL
  - serverless vs containers / Kubernetes
  - queue vs workflow engine
  - evaluating trade-offs or operational complexity
license: MIT
metadata:
  version: "0.11"
  category: system-design
compatibility: OpenCode, Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, Windsurf, Cline
---

# Architecture Decision Framework

Never memorize stacks. **Derive architecture from requirements.** The goal is not to recommend a
technology — it is to teach the agent *how to decide*.

## Decision order (never reverse)

```
Problem → Business Goals → Users → Functional Reqs → Non-functional Reqs
       → Constraints → Architecture → Infrastructure → Technologies → Implementation
```

## Questions before every decision

- What problem are we solving? What if we choose nothing?
- What breaks / scales / becomes expensive / fails first?
- Can we simplify or postpone this decision? Can it be replaced later?
- How difficult is migration?

## The five constraints

Every decision balances these; raising one usually lowers another. Perfect solutions do not exist.

| Constraint | Trades against |
|---|---|
| Performance | Cost, complexity |
| Reliability | Speed of delivery |
| Scalability | Simplicity |
| Developer Experience | Control |
| Cost | Everything above |

## Engineering trade-offs (every recommendation must include)

**Why · Advantages · Disadvantages · Hidden complexity · Operational burden · Scaling limits ·
Migration strategy · Alternatives.** Never recommend without trade-offs.

## Start small (default)

```
Single Repository → Single Deployment → Single Database → Single Backend → Simple Infrastructure
```

Split systems only after **measurable pain** exists.

## Modular monolith first

Default to a **modular monolith**, not microservices: simpler deployment, shared transactions,
less networking, simpler debugging, lower cost, less infra, faster generation. Most startups should
stay here for years.

## Extract services only when…

- Independent scaling · independent deployment · separate ownership
- Different technology · resource isolation · regulatory isolation

Never extract because *"microservices are modern."*

## Microservice checklist

Create a service only if YES to at least four:

- Independent deployment? · Independent scaling? · Different team owns it?
- Different runtime? · Different database? · Different SLA? · Independent failure desirable?

Otherwise keep it in the monolith.

## Choice shortcuts

| Need | Choose |
|---|---|
| Relationships, joins, transactions, financial consistency | **PostgreSQL** (SQL) |
| Flexible schema, rapid iteration, nested docs | Document DB (MongoDB) |
| Many systems react to one action | **Event-driven** (publish, don't call 10 syncs) |
| User can't wait | **Background job / queue** |
| Task spans minutes, needs retries/checkpoints/approval | **Workflow engine** (Temporal, Trigger.dev, Inngest) |
| Expensive + frequently read + rarely updated | **Cache (Redis)** intentionally |
| Keyword + semantic search | **Hybrid search** |
| User uploads | **Object storage** (metadata in DB, file in S3/R2) |

## Cost & operational awareness

- Estimate monthly / scaling / operational / engineering / migration cost. Cheapest service ≠
  cheapest architecture.
- Before adding Kafka/K8s/ES/Redis/etc., justify the operational burden. Every YES needs a reason.
- Prefer replaceable technologies; hide implementations behind interfaces (rule of replacement).

## Architecture review (pre-implementation)

- Can new engineers / the AI understand it? Can components scale and fail independently?
- Can services recover, data migrate, infra/deployment change? If not — improve the architecture.

## Architecture decision tree

```
Need an architecture decision?
  ↓
Requirements clear? → NO → Stop. Gather requirements.
  ↓ YES
Small team / MVP? → YES → Modular Monolith
  ↓ NO
Independent scaling/deploy/ownership? → YES → Extract a service
One action triggers many systems? → Event-Driven
Task spans minutes or needs retries? → Workflow Engine
Added infra (Kafka/K8s/ES)? → Justify operational cost or skip
```

## Anti-patterns

- ❌ Choosing tech because it is trending or a creator uses it
- ❌ Microservices / Kubernetes for an MVP
- ❌ Starting at "Enterprise" scale
- ❌ Recommending tools without stating trade-offs
- ❌ Reversing the order: technology → architecture
- ❌ Ignoring operational complexity of added infrastructure

## Architecture prompts

- What problem am I actually solving?
- Can this be simpler or postponed?
- Can this be replaced later, and how hard is migration?
- What breaks / scales / fails first?
- Does this add unnecessary coupling?
