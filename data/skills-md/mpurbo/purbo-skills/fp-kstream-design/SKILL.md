---
name: fp-kstream-design
description: >
  Kafka Streams topology design using Kafka Stream Algebra (KSA). Use this skill
  when designing, planning, or reviewing a Kafka Streams topology. Triggers:
  "design a topology", "kafka architecture", "stream processing design",
  "how should I model this as streams", "what pattern should I use", "topology review",
  "KSA", "Kafka Stream Algebra", or any request to diagram, plan, or reason about
  a Kafka-based backend service before writing code.
  Do NOT use for implementation, coding, or testing — use fp-kstream-implement for those.
---

# Kafka Topology Design Skill

Design deterministic, replay-safe, cost-efficient Kafka Streams topologies using KSA patterns.

## Required Reading

Before responding, load the shared reference:

```
cat ${SKILL_PATH}/references/KSA.md
```

This is the authoritative source for all patterns, principles, and constraints.

---

## Workflow

### Step 1 — Understand the Problem

Gather from the user (ask if missing):

1. **Source events** — what topics trigger this service?
2. **Enrichment needs** — what data beyond the event itself?
3. **Outputs** — output topics, DB writes, notifications?
4. **Statefulness** — does output depend on past events?
5. **Partition key** — what entity scopes this? (userId, orderId, etc.)

### Step 2 — Select Recipes

Map to KSA recipes (KSA.md §4):

| Problem involves… | Recipe |
|-------------------|--------|
| Cleaning/validating inbound events | 01 — Validation & Normalization |
| Duplicate events from upstream | 02 — Deduplication |
| Splitting events to different consumers | 03 — Routing & Fan-Out |
| Looking up reference data | 04 — Data Enrichment |
| Reference data + historical computation | 05 — Enrichment + Stateful |
| Counting, rate limiting, windowed metrics | 06 — Windowed Aggregation |
| Entity lifecycle (order, payment, KYC) | 07 — Per-Key State Machine |
| Cross-service coordination with rollback | 08 — Saga Orchestrator |
| Building a read model or search index | 09 — CQRS Projection |
| Bug fix replay or data backfill | 10 — Event Replay |

### Step 3 — Compose the Topology

Arrange recipes left to right:

```
Source → [Ingress] → [Enrichment] → [Computation] → [Egress] → Sink
```

Not every stage needed. Only include what the problem requires.

### Step 4 — Draw the Diagram

Produce a Mermaid `flowchart LR` using the KSA symbol legend (KSA.md §3):

- `[TopicName]` — Kafka topic
- `[TopicName*]` — compacted topic (KTable source)
- `(Processor)` — stateless processor
- `{{Processor}}` — stateful processor
- `((Join))` — stream–table join
- `[[Sink]]` — side-effect boundary
- `{Decision?}` — conditional branch

### Step 5 — Declare Policies

For every topology, explicitly document:

1. **Missing-state policy** per join (drop / dead-letter / retry / buffer)
2. **Partition key** and why it aligns with all joins
3. **State store retention** per stateful processor
4. **Sink idempotency** strategy

### Step 6 — Cost Check

Estimate per KSA.md §7.4:

| Factor | Estimate | Red Flag |
|--------|----------|----------|
| State store size/key | value × keys × retention | > 50 GB/instance |
| Changelog overhead | store size × replication | > 100 GB total |
| Repartition count | selectKey/through calls | > 2 on high-volume |
| KTable restore time | topic size / throughput | > 10 minutes |
| Partition count | all internal + output topics | > 500 total |

Multiple red flags → recommend alternatives (KSA.md §7.3).

### Step 7 — Compliance Checklist

Verify against KSA.md §6 before signing off.

---

## Output Format

Always produce:

1. **Summary** — one paragraph describing what the service does
2. **Recipes used** — numbered list of KSA recipe numbers and names
3. **Topology diagram** — Mermaid flowchart LR
4. **State diagram** — Mermaid stateDiagram-v2 (if FSM involved)
5. **Policy table** — missing-state, retention, idempotency decisions
6. **Cost estimate** — back-of-napkin numbers for the heuristic
7. **Compliance** — checklist pass/fail

---

## Anti-Patterns to Flag

| Anti-Pattern | Why It's Wrong | Suggest |
|-------------|----------------|---------|
| HTTP calls inside processor | Breaks replay determinism | KTable enrichment |
| DB queries inside processor | Same as above | Compacted topic |
| No declared missing-state policy | Undeclared behavior = design defect | Ask: "what happens when KTable has no entry?" |
| Partition key mismatch | Join key ≠ partition key | Repartition (flag cost) |
| Unbounded state stores | No TTL = unbounded growth | Ask about retention |
| GlobalKTable for large data | Loads ALL data on EVERY instance | Regular KTable with partition-aligned joins |
| Multiple repartitions on same stream | Each doubles I/O | Redesign key strategy |
| Stateful where stateless suffices | Unnecessary state store overhead | Remove state store |

---

## Conversation Style

- Ask clarifying questions before designing. Problem statements are often incomplete.
- When multiple recipes apply, explain trade-offs and let the engineer choose.
- Always produce a diagram.
- Be explicit about what the topology does NOT handle (scope).
- If the problem is better solved without KStreams, say so (KSA.md §7.3).
