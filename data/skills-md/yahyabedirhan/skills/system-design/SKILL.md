---
name: system-design
description: Design, explain or redesign a system at the level of services, data stores, APIs and scale, through the system design delivery framework. Use when designing a new backend or distributed system, explaining or documenting an existing one, redesigning or scaling one, or choosing a database, cache, queue or protocol.
---

# System design

Follow the **delivery framework** in every session, whether the design is new, explained or redesigned, so the user always finds the same things in the same places. The user decides what the session is for; the framework sets how the answer is laid out. Keep the design in the conversation unless the user asks for it to be written somewhere, and then use the stages as its sections.

To design inside one service's codebase, at the level of its modules, classes and folders, use `/low-level-design` instead.

## Flow

1. **Read what the session is for** from the request and its context, and restate it in one line before starting, so a misreading costs one reply.
   - **Invoked inside a project with no instructions:** explain that project's current design.
   - **When the purpose is unclear:** ask what the user wants to do with the design, whether the system exists, and whether they want only an explanation.
2. **Work through the delivery framework** below, stage by stage, reading a concept reference when a stage reaches its concept.
3. **Present every stage and revise it with the user** until they are satisfied.

The purpose decides how the stages are walked. The cases below are common, not a complete list; a session can mix them or move from one to another.

- **Designing a new system:** write a complete first draft through every stage.
- **Explaining an existing system:** walk it through the stages as it is, without changing it.
  - Build each stage from the evidence. Start from an existing design document and check it against the code. In the code, read the routes and handlers, jobs and consumers, schemas and migrations, connection and deploy config, and calls to other services. The user's description is evidence too. Cite the file, section or message behind each claim.
  - Mark requirements read from the code **inferred**. Mark what the evidence can't show, such as traffic, data sizes, incidents or why a choice was made, **unknown**, and ask about it rather than filling it in, so a guess never passes for a fact.
  - In place of the deep dives, explain each concept the design relies on, such as its cache, its sharding or its consistency choice: what it is, why it matters here, and the trade-off the design made.
  - Record weaknesses as observations, not proposals, because the session explains the system without changing it. Answer follow-up questions by walking a request or a failure through the design.
- **Redesigning an existing system:** explain it first and get the user's agreement that the explanation is right. Then redesign through the same stages, keeping each existing component unless the problem lies in it. Present the new design's trade-offs as options, and show every changed stage as a before/after `diff`.
- **Deciding one thing,** such as "Postgres or DynamoDB here?": answer it as one deep dive, naming the parts of the design it touches and the requirement behind it.

## The delivery framework

```text
Requirements → Core entities → API → [Data flow] → High-level design → Deep dives
```

The stages come in this order because each builds on the one before it: the API serves the requirements, the high-level design serves the API, and the deep dives make the high-level design meet the non-functional requirements. Go back to an earlier stage when a later one exposes a gap.

### Requirements

**Functional requirements** are the core features, as "users should be able to..." statements. A real system has hundreds of features; keep the in-scope list to about three, because every item on it is something the design must then satisfy.

**Non-functional requirements** are the qualities the system must have, as "the system should be..." statements, each stated for this system and quantified where possible: "search results under 500 ms", not "low latency". Pick the 3-5 that most constrain this design from this checklist:

- **Consistency or availability** under a network partition, decided per feature ([cap-theorem.md](references/cap-theorem.md)). Settle this first, because it decides which stores fit.
- **Scalability**: bursty traffic, peak events, and the read/write ratio, which says which side must scale.
- **Latency**, especially for requests that need real computation, such as search and feeds.
- **Durability**: how bad losing data is, a social post against a bank transfer.
- **Security**: data protection and access control.
- **Fault tolerance**: redundancy, failover and recovery.
- **Compliance**: legal and regulatory constraints.
- **Environment**: device, memory or bandwidth limits, such as mobile clients on poor networks.

**Estimates:** work out users, QPS or storage only where the number changes a decision, such as whether a top-K counter fits in one in-memory heap or must be sharded. Do the arithmetic at the point in the design where a choice depends on it ([numbers-to-know.md](references/numbers-to-know.md)).

Show requirements as short lists: functional, non-functional, and out of scope with reasons.

### Core entities

The things the API exchanges and the stores persist, as a short first draft with clear names (for Twitter: User, Tweet, Follow). Ask who the actors are and whether they overlap, and which resources each functional requirement needs. Leave fields for the high-level design, where a request shows which ones matter.

### API

The contract with the system's users, usually one endpoint per functional requirement. Use the core entities as resources. Use REST by default, GraphQL for diverse clients with different data needs, and RPC for internal, performance-critical calls. Design real-time features, such as WebSockets or SSE, after the core API. Take the current user from the auth token, never from the request body ([api-design.md](references/api-design.md)).

Show entities and endpoints as short lists or tables.

### Data flow

For a data-processing system, a numbered list of steps from input to output (a web crawler: fetch seed URLs, parse HTML, extract URLs, store data, repeat).

### High-level design

Lay out the components (clients, load balancers, services, databases, caches, queues) and how they interact, endpoint by endpoint, until the design satisfies the whole API. Include only what the functional requirements need.

- Say how data flows through the system for each request, from the API call to the response, and what state changes where.
- When a request reaches a store, write the fields that matter beside it: the ones the design depends on, not the obvious ones ([data-modeling.md](references/data-modeling.md), [database-indexing.md](references/database-indexing.md)).
- When a part looks like it needs a cache or a queue, note it for the deep dives and move on.

Show the design as a component flow (`client -> LB -> API -> Postgres`), a request or a failure as a numbered walk through the components with the state it changes, and stores as a table of what each holds, who writes it, and its key or shard key.

### Deep dives

Meet each non-functional requirement, remove bottlenecks and single points of failure, and handle edge cases. Add caches, queues and other complexity here and not earlier, because a design that adds them early rarely reaches a complete, working whole. Name each problem, with numbers when it's about scale, then its options and their trade-offs. Twitter's scale leads to horizontal scaling, caching and sharding; its fast feeds lead to fanout-on-read against fanout-on-write. Choose the deep dives yourself, and let the user redirect them toward what they care about.

Each default in *Defaults first* has a reference that says when to move off it: the store in [data-modeling.md](references/data-modeling.md), the API in [api-design.md](references/api-design.md), transport and real-time in [networking-essentials.md](references/networking-essentials.md), the cache in [caching.md](references/caching.md), scale in [sharding.md](references/sharding.md) and [numbers-to-know.md](references/numbers-to-know.md), and async work in [common-patterns.md](references/common-patterns.md).

Show the options side by side, each with its gain and cost, and a redesign or revision as a before/after `diff` of the flow or the list that changed.

## Defaults first

Start each choice from its default, because the most common failure in system design is complexity added before it is needed: PostgreSQL as the store, REST for the API, TCP and HTTP polling for transport and real-time, no cache and then Redis cache-aside, one bigger database with replicas and then hash sharding, and synchronous work. Move off a default only for a named requirement, with numbers when the case is about scale. Typical over-design: a queue at 5k writes per second, sharding at 100 GB, a WebSocket where polling would do, a cache in front of an indexed lookup.

When the design adopts a specific technology (Kafka, DynamoDB, Elasticsearch), research it in its documentation before relying on its details: its limits, its guarantees, and how it fails.

## Working with the user

Load `/show-me` and present every stage visually, with prose only for the reasons behind choices.

- Keep one current version of the design and revise it.
- When feedback changes one part, carry the change through every part it affects.
- Open each revision with what changed and why, as a before/after of the parts that moved, including parts that changed only because of a change elsewhere.
- Leave a point the user settled as it is unless they reopen it.

Ask only what the code, the existing design documents and the user's earlier answers can't settle, one question at a time; decide the rest and say what you decided.

## References

### Concepts and technologies

Each covers one concept: what it is, why it matters, its trade-offs, and when to choose which kind of technology.

| Reference | Covers |
|---|---|
| [networking-essentials.md](references/networking-essentials.md) | TCP and UDP, HTTP, REST, gRPC, SSE, WebSockets, WebRTC, load balancing, regions, failure handling |
| [api-design.md](references/api-design.md) | REST, GraphQL, RPC, resources, pagination, idempotency, versioning, auth |
| [data-modeling.md](references/data-modeling.md) | Database models, schema design, normalization |
| [database-indexing.md](references/database-indexing.md) | B-tree, LSM, hash, geospatial and inverted indexes, composite indexes |
| [caching.md](references/caching.md) | Where to cache, cache patterns, eviction, what goes wrong |
| [sharding.md](references/sharding.md) | Shard keys, distribution strategies, hot spots, cross-shard work |
| [consistent-hashing.md](references/consistent-hashing.md) | The hash ring, virtual nodes, hot keys |
| [cap-theorem.md](references/cap-theorem.md) | Consistency against availability, consistency levels |
| [numbers-to-know.md](references/numbers-to-know.md) | Hardware and component capacities, over-design they prevent |
| [common-patterns.md](references/common-patterns.md) | Real-time updates, long-running tasks, contention, scaling reads and writes, large blobs, multi-step processes, proximity |

---

Source: Hello Interview, [Delivery Framework](https://www.hellointerview.com/learn/courses/system-design/lesson/orientation/delivery).
