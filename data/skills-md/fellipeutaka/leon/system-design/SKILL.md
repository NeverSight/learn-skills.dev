---
name: system-design
description: Design or evolve a system's architecture from requirements to a scaled, fault-tolerant design. Use when designing a backend or feature that must scale, choosing a database, removing a bottleneck, picking sync vs async communication, adding cache, queues, or real-time push, deciding monolith vs microservices, or practising a system design interview.
---

# System Design

Every component in a design exists because a requirement put it there, and every component costs something. Work the steps in order: each one ends on a completion criterion, and the next step builds on what it produced. The references are pattern catalogs; open the one a step points at when the design reaches that branch.

## Steps

### 1. Requirements

- **Functional**: the 2–4 core actions users take (actor + verb + noun: "users upload files"). Name what is out of scope.
- **Non-functional**, each with a number: daily and peak-concurrent users, read:write ratio, data size and retention, latency target (p99), availability, file or payload size limits, and problem-specific constraints (fairness, anti-bot, resumable uploads, ordering).
- **Consistency per data type**: money, inventory, and uniqueness need strong consistency; likes, feeds, and catalogs tolerate staleness. Decide per module, sometimes per query.

When the user gives no numbers, ask for them; when they can't say, state assumptions and label them as such.

**Done when** every non-functional requirement carries a number or a labelled assumption, and each data type has a consistency stance.

### 2. Back-of-envelope

Compute only the numbers that drive a decision, and write the decision beside each one.

| Quantity        | Formula                                                                        |
| --------------- | ------------------------------------------------------------------------------ |
| Average rate    | daily count ÷ 86,400 (≈ 10⁵)                                                   |
| Peak rate       | average × peak factor (state it; 3–10× is typical, event spikes far higher)    |
| Reads           | writes × read:write ratio                                                      |
| Rows            | daily writes × 365 × retention years                                           |
| Storage         | rows × average size × replication factor (× renditions/versions)               |
| Bandwidth       | requests/s × payload size (egress usually dominates cost for media)            |
| Open connections| peak concurrent users on push features ÷ connections per node = node count     |
| Identifier size | smallest k with alphabetᵏ ≥ total identifiers ever issued                      |

Examples of the link: 35 writes/s → one relational primary is plenty; 365 billion rows over ten years → a partitioned store; 150 TB/day of uploads → bytes must bypass app servers. When no number would change a decision, skip the step and say why.

**Done when** each computed number names the decision it drives.

### 3. Entities, API, database

- Derive entities from the nouns of the functional requirements. Split **blob from metadata**: bytes live in object storage; owner, size, type, status, and object key live in the database.
- One endpoint per functional requirement. Take identity from the auth token, never the request body. Flag protocol details that shape the architecture (301 vs 302, payload limits, long-lived responses).
- Choose the database from step 2's numbers and step 1's consistency stances → [DATA.md](references/DATA.md).

**Done when** every functional requirement has an endpoint and every entity has a home store with a reason.

### 4. Naive design, then break it

Draw the simplest design that satisfies the functional requirements end to end. Then attack it with the **worst case** for each non-functional requirement: the largest file, the peak spike, the hottest key, a node dying mid-operation, a network partition between two writes. Intuitive designs fail here; finding where is the point of the step.

**Done when** you have a list of concrete failures, each tied to the requirement it violates.

### 5. Fix each failure on the ladder

Fix each failure with the **cheapest rung** that solves it, and write the trade-off it adds next to the component.

1. Better query, index, or data structure; the right tool for the access pattern (a search engine for search).
2. Cache, CDN, or a precomputed read model.
3. Vertical scaling.
4. Horizontal scaling of a stateless tier behind a load balancer.
5. Read replicas.
6. Async work: queues, workers, events.
7. CQRS, partitioning (sharding).
8. Service split, multi-region.

A higher rung earns its place by **necessity**: name the symptom the lower rungs left unsolved. Two moves sit off the ladder: when demand vastly exceeds what can ever be served (fixed ticket supply), throttle demand instead of scaling to it; and buy commodity capabilities (waiting rooms, transcoding, managed search) instead of building them.

| Failure looks like                                                         | Open                                          |
| -------------------------------------------------------------------------- | --------------------------------------------- |
| Server overloaded, single server, spikes, slow jobs in requests, global latency | [SCALING.md](references/SCALING.md)       |
| DB overloaded, slow queries, search, data too big, IDs, large files, double-booking | [DATA.md](references/DATA.md)         |
| Writes to two systems, derived stores drift, sync call chains, ordering, duplicates | [DISTRIBUTED.md](references/DISTRIBUTED.md) |
| Slow or failing dependencies, cascading failures, retries, overload         | [RESILIENCE.md](references/RESILIENCE.md)     |
| History is lost on update, audit or temporal queries, many views of the same facts | [EVENT-SOURCING.md](references/EVENT-SOURCING.md) |
| Team or codebase boundaries, monolith vs microservices                     | [STYLES.md](references/STYLES.md)             |
| Clients need server updates without refreshing                             | [REALTIME.md](references/REALTIME.md)         |

To see the whole method applied to a known problem, read [CASE-STUDIES.md](references/CASE-STUDIES.md).

**Done when** every failure from step 4 has a fix with its trade-off written down.

### 6. Hunt single points of failure

Walk every component and ask what happens when it dies, slows down, or is partitioned away: the load balancer itself, the database primary, the cache, the ID generator, the broker, the region. Answer with redundancy plus failover, and state the data-loss window (asynchronous replication can drop the last writes on failover). A cache that dies should degrade to the database, guarded against a thundering herd.

**Done when** every component has a failure answer.

### 7. Verify against requirements

Build the table: requirement → component(s) → trade-off accepted. Then check the claims end to end: every derived store (cache, search index, read model) has a sync path and a stated staleness; every at-least-once path ends in an idempotent consumer; every component traces back to a requirement.

**Done when** every requirement is mapped, every component is justified, and no consistency claim rests on an unverified path.

## Principles

- **Trade-off.** Every choice pays with something: latency, consistency, cost, operational load, team complexity. A design without stated trade-offs hasn't been examined.
- **Source of truth.** Each fact has one authoritative store. Caches, search indexes, and read models are derived: disposable, rebuildable, fed by CDC or an outbox rather than a dual write.
- **Necessity.** Microservices, event-driven architecture, CQRS, sharding, and WebSockets enter when a named symptom demands them, scoped to the part of the system that has the symptom. A single server with one database is a correct design when the numbers allow it.
- **Hot path.** Keep heavy work off the request: large bytes go straight to object storage, slow jobs go to a queue, expensive aggregations are precomputed.
- **Fundamentals over brands.** Justify a tool by the property it provides (partitioned writes, inverted index, durable log); any tool with that property fits.

## Interview mode

When the design is for an interview: ask for numbers in step 1, keep steps 1–3 to roughly the first quarter of the time, and spend the bulk on the deep dives the problem actually tests (large uploads, ID generation, ordering, contention). Say each trade-off aloud as you choose.
