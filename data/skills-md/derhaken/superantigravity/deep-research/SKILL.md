---
name: deep-research
description: Use when a task requires gathering information from external sources, researching unfamiliar technologies, validating technical approaches, or answering questions that need current web knowledge before implementation
---

# Deep Research

## Overview

Systematic multi-source research before acting on unknowns. Never guess when you can verify.
Plan your searches, execute in parallel where possible, synthesize before concluding.

## When to Use

- Starting work on an unfamiliar library, framework, or API
- Validating a technical approach before committing
- Answering questions that require current information
- Comparing options or evaluating trade-offs
- Verifying security practices or compatibility

## The Process

**1. Plan searches first**
Before searching, list the specific questions you need to answer.
Identify 3-5 targeted search queries that cover different angles.

**2. Execute searches in parallel**
Run multiple searches simultaneously where possible.
Prefer official documentation and primary sources over secondary.

**3. Evaluate source quality**
- Official docs > tutorials > blog posts > forums
- Recent (within 1-2 years) > older for fast-moving tech
- Multiple sources agreeing > single source

**4. Synthesize findings**
Reconcile conflicting information. Note gaps.
Present a clear answer with confidence level and key sources.

**5. Flag uncertainty**
If research is inconclusive, say so explicitly.
"I found X but couldn't verify Y — recommend checking Z."

## What Counts as a Key Claim

A claim is "key" if any of the following are true:

- **(a) It directly informs a technical decision** — the claim is the basis for choosing one
  approach over another (e.g., "Redis supports atomic operations" → informs whether Redis
  can safely handle concurrent session writes)
- **(b) It contradicts a common assumption** — the claim overturns something a developer
  would naturally assume to be true (e.g., "Node.js cluster mode does NOT share Redis
  connections automatically")
- **(c) The implementation depends on it being correct** — if the claim is wrong, the
  implementation breaks or has to be redesigned (e.g., "Redis TTL is per-key, not per-value")

Key claims require at least 2 corroborating sources. Non-key claims require 1.

## Conflict Resolution Rule

When same-level sources conflict (e.g., two official docs, or two well-regarded tutorials):

1. Note the conflict explicitly: "Sources conflict on this point."
2. State both positions clearly: "Source A says X. Source B says Y."
3. Flag the affected finding as medium confidence maximum — do not present conflicting
   information as high confidence regardless of source quality.
4. Recommend resolution: "Recommend testing this directly" or "Check the changelog between
   these versions."

Do not silently pick one side of a conflict and present it as settled.

## Research Quality Checklist

- [ ] Searched official documentation first
- [ ] Found at least 2 corroborating sources for key claims
- [ ] Checked publication dates for currency
- [ ] Noted any contradictions between sources
- [ ] Stated confidence level in findings

**Minimum pass threshold: 4 out of 5 items must be checked to proceed.**

If fewer than 4 items are checked, do not act on the findings. Gather more sources first.
State explicitly: "Research quality check: 3/5. Gathering additional sources before proceeding."

## Error Path: Sources Inaccessible

If all sources are inaccessible (no internet connection, rate limiting, paywalled content,
or search returning no results):

1. State this explicitly: "I cannot access external sources for this research (reason: [no
   internet / rate limited / all results paywalled])."
2. Note what you know from training data: "Based on my training data (cutoff: [date]), here
   is what I know about this topic: [summary]."
3. Flag confidence as low: "Confidence: low — this is based on training data only, not
   current sources."
4. Recommend user verify independently: "Recommend verifying against current official
   documentation before acting on this."

Do not present training-data knowledge as researched knowledge. They are different things.

## Red Flags

| Thought | Reality |
|---------|---------|
| "I already know this" | Knowledge has a cutoff. Verify before acting. |
| "One source is enough" | Single sources miss context. Find corroboration. |
| "I'll research later" | Unknowns discovered mid-implementation cost more. Research first. |
| "The docs are probably right" | Docs lag implementation. Check issues/changelogs too. |
| "These sources conflict but one seems more credible" | Conflicts cap confidence at medium. State both. |

## Output Format

Present research as:
1. **Question answered**
2. **Finding** (the answer)
3. **Confidence** (high/medium/low)
4. **Sources** (URLs or doc sections)
5. **Caveats** (what you couldn't verify)

## Worked Example

The following is a complete research session demonstrating correct application of this skill.

---

**Question:** Is Redis suitable for storing user sessions in a Node.js app handling 10k
concurrent users?

---

**Step 1: Planned queries**

Before searching, listed specific questions to answer:
- What is Redis's recommended use case for session storage?
- What are the concurrency limits or performance benchmarks for Redis under load?
- How does the Node.js Redis client (ioredis / node-redis) handle connection pooling at scale?
- Are there known issues with Redis session storage at 10k+ concurrent users?
- What are the alternatives and how do they compare?

Queries to run:
1. "Redis session storage Node.js best practices 2024"
2. "Redis performance benchmark 10000 concurrent connections"
3. "ioredis connection pooling Node.js cluster"
4. "Redis vs in-memory session storage Node.js"
5. "Redis official docs: data types, TTL, persistence"

---

**Step 2: Hypothetical source findings**

Source A — Official Redis documentation (redis.io):
Redis is explicitly recommended for session storage. Supports key expiry via TTL for
automatic session cleanup. Single-threaded event loop handles ~100k operations/second on
typical hardware. Recommends connection pooling for high-concurrency Node.js apps.

Source B — Node.js best practices guide (github.com/goldbergyoni/nodebestpractices):
Redis is listed as the standard recommendation for session storage in Node.js. Notes that
connect-redis (Express session adapter) is stable and widely used. Warns that Node.js
cluster mode requires all workers to share the same Redis instance — sessions stored
in-process will not work across workers.

Source C — Benchmark article (medium.com, published 2023, author with Redis certifications):
Benchmarks Redis at 80k-120k GET/SET operations per second on a t3.medium AWS instance.
10k concurrent users generating ~1k session reads/writes per second would consume roughly
1-1.5% of capacity. Flags that network latency (not Redis throughput) is the bottleneck
at this scale. Recommends connection pooling with a pool size of 10-20 connections for
a Node.js app at this scale.

---

**Step 3: Source quality evaluated**

- Source A (official Redis docs): Tier 1. High weight.
- Source B (Node.js best practices repo, 80k+ GitHub stars): Tier 2, high-quality secondary.
- Source C (Medium benchmark article, 2023): Tier 3. Useful data, but methodology not fully
  disclosed. Treat as corroborating, not primary.

No conflicts detected between sources. All three agree Redis is appropriate for this use case.
The Node.js cluster warning from Source B is a key claim (contradicts what developers might
assume) — flagged for inclusion.

Key claims check:
- "Redis supports session storage with TTL" — key claim, 2 sources agree (A + B). Verified.
- "10k concurrent users is well within Redis capacity" — key claim, 2 sources agree (A + C). Verified.
- "Cluster mode requires shared Redis instance" — key claim, 1 source (B). Contradicts common
  assumption. Flag as needing confirmation but include with note.

Research quality checklist:
- [x] Searched official documentation first
- [x] Found at least 2 corroborating sources for key claims
- [x] Checked publication dates for currency (2023-2024)
- [x] Noted any contradictions between sources (none found)
- [x] Stated confidence level in findings

Score: 5/5. Proceed.

---

**Step 4: Synthesis with confidence**

- Redis suitability for session storage: **High confidence**. Official docs + best practices
  guide + benchmark all confirm. Well within performance envelope.
- Performance at 10k concurrent users: **High confidence**. 10k users generating ~1k ops/sec
  is ~1% of Redis capacity on modest hardware.
- Node.js cluster mode caveat: **Medium confidence**. One source (Node.js best practices).
  Credible source but only one. Include with caveat.
- Connection pool sizing recommendation (10-20): **Medium confidence**. Single benchmark
  article, methodology not fully disclosed.

---

**Step 5: Final output**

**Question answered:** Is Redis suitable for storing user sessions in a Node.js app at 10k
concurrent users?

**Finding:** Yes. Redis is the standard recommendation for Node.js session storage and is
well within capacity for 10k concurrent users. At ~1k session operations per second (assuming
typical session read/write patterns), Redis on modest hardware operates at roughly 1-1.5% of
its throughput capacity. Use ioredis or node-redis with connection pooling (10-20 connections
recommended). If using Node.js cluster mode, all workers must share the same Redis instance —
in-process session storage will not work across cluster workers.

**Confidence:** High (suitability and scale). Medium (cluster mode caveat, pool size tuning).

**Sources:**
- redis.io official documentation — session storage, TTL, connection management
- github.com/goldbergyoni/nodebestpractices — Node.js session storage recommendations
- Medium benchmark article (2023) — Redis throughput benchmarks on AWS t3.medium

**Caveats:** Cluster mode caveat confirmed by one source only — verify against current
ioredis documentation. Pool size recommendation comes from a single benchmark; tune based
on observed connection wait times in your environment.

---

## Integration Contract

Output from this skill is consumed by:

- **brainstorming skill** (feasibility phase): research findings inform whether a proposed
  approach is viable before ideation continues
- **architecture-design skill** (options evaluation): findings populate the trade-off analysis
  for each architectural option
- **confidence-check skill** (context score): successful research raises Context dimension
  score by establishing verified understanding of the technical landscape
