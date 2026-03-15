---
name: architecture-design
description: Use when designing new systems or significant features, evaluating architectural trade-offs, choosing between structural approaches, or when a task requires understanding system-wide design before writing code
---

# Architecture Design

## Overview

Design before you build. Architecture decisions are expensive to change.
Understand constraints, explore options, validate trade-offs, then decide.

## When to Use

- Starting a new system or significant new component
- Evaluating whether to build vs. use existing solutions
- Making decisions that will affect multiple parts of the system
- Choosing between fundamentally different structural approaches
- Designing APIs, data models, or service boundaries

## Constraints Checklist (gather before proposing options)

Complete this checklist before presenting any architectural options. Do not propose options
without knowing the constraints — options that ignore constraints are not options, they are
guesses.

- [ ] **Scale:** users / requests / data volume per day
- [ ] **Consistency:** eventual vs. strong (specify which operations require which)
- [ ] **Latency:** acceptable p50 and p99 in milliseconds
- [ ] **Team:** size, existing stack, deployment platform
- [ ] **Cost:** hard budget ceiling if any

**Termination criterion:** Proceed when 4 out of 5 items are checked, OR when the user
explicitly says "don't know" or "doesn't matter" for the remaining unchecked items.

If fewer than 4 items are known and the user has not dismissed the unknowns, ask before
proceeding. Unknown constraints produce designs that must be redesigned later.

## The Process

**1. Understand constraints**
Before proposing anything, gather the checklist above.
Record what is known and what is assumed.

**2. Identify core trade-offs**
Every architecture has trade-offs. Name them explicitly:
- Consistency vs. availability
- Simple vs. scalable
- Build vs. buy
- Monolith vs. services
- Synchronous vs. asynchronous

**3. Propose 2-3 options**
Never present only one option. For each:
- Describe the approach in 2-3 sentences
- List pros and cons
- State the constraints it satisfies (and which it doesn't)
- Give a complexity estimate

**4. Recommend with reasoning**
State your recommendation clearly.
Explain WHY given the specific constraints.
Don't hedge everything — make a call.

**5. Document the decision**
Record: what was decided, what was rejected, and why.
This is the most important thing to write down.

## Open Questions Resolution Process

After completing the output, list any open questions that remain. For each open question,
assign it to exactly one of:

- **(user):** only the user can answer this (business requirements, organizational constraints,
  budget decisions). **Do not proceed if any user-assigned question is unanswered.**
- **(deep-research skill):** answerable by researching current technical documentation,
  benchmarks, or compatibility information
- **(implementation discovery):** answerable only by building a spike or prototype; acceptable
  to proceed and revisit

If a user-assigned question is blocking, state it clearly: "I need your answer on [question]
before I can finalize this design."

## Uncertainty Guidance

When constraints are unavailable, do not refuse to proceed — proceed transparently:

1. State your assumption explicitly: "I am assuming [X] because [reason]."
2. Design for the stated assumption: produce a complete design based on it.
3. Document that the design must be revisited: "If actual [constraint] differs significantly
   from this assumption, revisit [specific aspect of the design]."

Assumptions are acceptable. Hidden assumptions are not.

## Patterns Composition Guidance

When combining patterns, follow these composition rules:

**REST + event-driven:** Use REST for synchronous CRUD operations (user requests a resource,
expects an immediate response). Use events for async side effects (notifications, audit logs,
cache invalidation, search index updates). Do not use events for operations where the caller
needs an immediate, consistent result.

**CQRS + event-driven:** Commands (writes) emit events. Query models are rebuilt from events.
Acceptable eventual consistency window must be defined before adopting this — if users expect
to see their own writes immediately, event lag will cause visible bugs.

**Repository pattern + any persistence layer:** The repository interface is defined by the
domain, not the database. Changing the underlying storage should not require changing the
domain logic.

## Architecture Principles

**YAGNI** — Don't build for hypothetical future needs.
**Simple first** — The simplest thing that could work is usually right.
**Explicit over implicit** — Clear dependencies beat magic.
**Stateless where possible** — Stateful systems are harder to scale and reason about.
**Fail fast** — Validate inputs at boundaries, not deep in the call stack.

## Common Patterns Reference

| Pattern | Use When |
|---------|----------|
| REST API | CRUD over resources, external-facing APIs |
| Event-driven | Decoupling producers/consumers, async workflows |
| CQRS | Read/write loads differ significantly |
| Repository pattern | Abstracting data access from business logic |
| Circuit breaker | Calling unreliable external services |
| Saga pattern | Distributed transactions across services |
| BFF (Backend for Frontend) | Multiple clients with different data needs |

## Output Format

Present as:
1. **Constraints** — what must be true
2. **Options** — 2-3 approaches with trade-offs
3. **Recommendation** — clear choice with reasoning
4. **Decision record** — what was decided and what was rejected
5. **Open questions** — what still needs to be resolved, each assigned to (user | deep-research skill | implementation discovery)

## Worked Example

The following is a complete design session demonstrating correct application of this skill.

---

**Scenario:** "Design a notification service for a SaaS app"

---

**Constraint gathering**

Checklist filled:
- [x] **Scale:** 5,000 active users. Approximately 50,000 notifications per day (mix of in-app
  alerts, email digests, and real-time activity updates). Peak load: ~500 notifications per
  minute during business hours.
- [x] **Consistency:** Eventual. Users can tolerate a notification arriving 1-5 seconds after
  the triggering event. No financial or compliance requirement for guaranteed delivery.
- [x] **Latency:** In-app notifications: p50 < 500ms, p99 < 2s acceptable. Email: best-effort,
  no hard SLA.
- [x] **Team:** 2 backend engineers. Existing stack: Node.js, PostgreSQL, AWS (EC2 + RDS).
  No Kubernetes. No existing message queue infrastructure.
- [ ] **Cost:** Not specified. (User said "don't know.")

4/5 checked, user dismissed remaining item. Termination criterion met. Proceeding.

---

**Trade-offs identified**

Primary tension: **sync vs. async delivery**

- Synchronous delivery (within the same request that triggers the notification) is simple
  but couples notification latency to the main request path. A slow email provider slows down
  the user-facing action.
- Asynchronous delivery (decouple via queue or polling) is more resilient but adds
  infrastructure and operational complexity.

Secondary tension: **reliability vs. simplicity**

- Guaranteed delivery requires persistent queues, acknowledgement, and retry logic.
- Best-effort delivery (acceptable given no compliance requirement) allows simpler
  implementations.

---

**Option A: Direct DB polling**

The application writes notification records to a PostgreSQL `notifications` table when events
occur. A background worker process polls the table every 2 seconds for undelivered notifications
and dispatches them via email/in-app channels. Marks records as delivered after successful send.

Pros:
- No new infrastructure — PostgreSQL already exists
- Trivially debuggable: notification state is a table row
- Survives process restarts without losing notifications
- 2 engineers can own and operate it without specialist knowledge

Cons:
- Polling introduces up to 2 seconds of added latency (acceptable given p99 < 2s requirement)
- PostgreSQL write load increases slightly (append-only `notifications` table)
- Does not scale beyond ~50k-100k notifications/day without query optimization

Constraints satisfied: scale (5k users, 50k/day), consistency (eventual), team (no new infra),
cost (zero marginal cost).
Constraints not satisfied: would need redesign above ~100k notifications/day.

Complexity estimate: Low. 1 database table, 1 background worker process, 1-2 days to implement.

---

**Option B: Message queue + workers**

Introduce a message queue (AWS SQS or RabbitMQ). Application services publish notification
events to the queue. A pool of worker processes consumes the queue and dispatches notifications.
Queue provides durability, retry, and dead-letter handling.

Pros:
- Scales to 1M+ notifications/day without re-architecture
- Decoupled: notification workers fail independently of the main app
- Built-in retry and dead-letter queue for failed deliveries

Cons:
- New infrastructure: queue service must be provisioned, monitored, and operated
- Local development requires running a queue locally (Docker or mock)
- Adds operational surface area for a 2-engineer team
- 1-2 weeks to implement correctly including error handling and DLQ monitoring

Constraints satisfied: scale (headroom to 1M+/day), consistency (eventual).
Constraints not satisfied: team (adds infra burden); cost (SQS has per-message cost at volume).

Complexity estimate: High. New infrastructure dependency, operational runbook required.

---

**Option C: Webhooks / Server-Sent Events (client-pull)**

Instead of pushing notifications, serve a `/notifications` SSE endpoint. The frontend
subscribes on load and receives events in real time. Email notifications sent synchronously
within the triggering request.

Pros:
- No background worker or queue required
- Real-time in-app delivery without polling

Cons:
- SSE connections held open per active user (connection management overhead)
- Does not handle offline users (notifications missed if user is not connected)
- Email sent synchronously degrades main request performance if email provider is slow
- Not suitable when guaranteed delivery is needed for offline users

Constraints satisfied: latency (real-time when connected).
Constraints not satisfied: consistency (offline users miss notifications), reliability
(no guaranteed delivery).

Complexity estimate: Medium. SSE implementation is straightforward; offline delivery gap
is a product-level deficiency.

---

**Recommendation: Option A**

Given the constraints — 5k users, 50k notifications/day, 2-engineer team, no compliance
requirement for guaranteed delivery, no message queue infrastructure — Option A (DB polling)
is the correct choice.

Rationale:
- The scale is well within what PostgreSQL can handle as a notification backing store.
- The 2-second polling interval satisfies the p99 < 2s requirement.
- The team avoids introducing and operating new infrastructure.
- The implementation is observable (table rows), debuggable, and reversible.
- If the app grows to 500k+ notifications/day, migrate to Option B at that point. Do not
  build for that scale now (YAGNI).

---

**Decision record**

Decided: Option A — DB polling with PostgreSQL `notifications` table and background worker.

Rejected: Option B (message queue) — premature complexity. No current requirement justifies
the operational burden for a 2-engineer team at this scale.

Rejected: Option C (SSE/webhooks) — does not provide guaranteed delivery for offline users.
Acceptable only if the product accepts "notifications are best-effort and only visible when
logged in," which was not stated.

---

**Open questions**

- Should failed email deliveries be retried? If yes, how many times and with what backoff?
  Assign to: **(user)** — product decision. Do not proceed with email implementation until
  answered.
- Which email provider (SendGrid, SES, Postmark)? Assign to: **(user)** — depends on
  existing vendor relationships and cost.
- Does the PostgreSQL polling query need a partial index on `(delivered_at IS NULL)`?
  Assign to: **(implementation discovery)** — measure query time after table has 100k rows,
  add index if needed.
