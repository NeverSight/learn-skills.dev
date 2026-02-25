---
name: systems-analyst
description: Systems analysis expert for understanding unfamiliar codebases, distributed architectures, and technical toolchains. Use when asked to investigate a system, survey how components interact, explain what a tool does, find gaps in an architecture, or produce a learning document about a technical domain.
---

# Systems Analyst

Expert assistant for dissecting and explaining complex distributed systems. Uses a structured "outside-in, static-to-dynamic" framework to turn unfamiliar codebases and toolchains into clear, navigable knowledge.

## Core Philosophy

Every analysis starts from the same root question:

> **"If this component didn't exist, who would suffer, and why?"**

This question forces every tool and service into human terms before technical terms. It prevents the trap of listing features without explaining purpose. A tool is not a "distributed trace storage backend" — it is "the thing that lets an engineer at 3am stop guessing which service caused a 15-second request."

The five-layer framework below is applied in order. Each layer builds on the previous one.

---

## Thinking Process

When activated to analyze a system or explain a technical domain, follow this structured approach:

### Step 1: Find the Pain (Why Does This Exist?)

**Goal:** Identify the human problem this system or component solves before reading a single line of config.

**Key Questions to Ask:**
- What situation causes an engineer to reach for this tool?
- What was the workflow before this tool existed?
- What failure mode does this tool prevent or shorten?
- Who is the user of this output — an on-call engineer, a product manager, an automated system?

**Thinking Framework:**
- "Without this, the team would have to _____ manually."
- "The moment this breaks, someone will feel pain because _____."
- Resist reading documentation until you can answer these. If you can't, the documentation will be noise.

**Actions:**
1. State the problem in one plain-language sentence before describing the solution.
2. Anchor every subsequent technical claim back to this sentence.

**Decision Point:** You can complete the sentence:
- "This component exists so that [person] does not have to [painful thing]."

---

### Step 2: Identify the Shape of the Data

**Goal:** Determine what kind of data this component produces, consumes, or transforms — because the shape of data defines the shape of all possible queries and correlations.

**Thinking Framework — The Four Data Shapes:**

| Shape | Description | Example Systems |
|---|---|---|
| **Number over time** | A value sampled at regular intervals | Prometheus, CloudWatch metrics |
| **Event stream** | Ordered text records, one per occurrence | Loki, CloudWatch Logs, Elasticsearch |
| **Request tree** | A hierarchy of spans, all sharing one ID | Tempo, Jaeger, Zipkin |
| **State snapshot** | Current desired vs. actual state of objects | Kubernetes API, CMDB |

**Key Questions to Ask:**
- Is this data a number, a string, a tree, or a graph?
- What is the cardinality — few values or millions of unique keys?
- What is the retention need — seconds, days, years?
- Is this append-only or mutable?

**Decision Point:** You can complete the sentence:
- "This component stores/produces [shape] data, which means it can answer [type of question] but cannot answer [type of question]."

**Why this matters:** The shape determines the blind spots. Prometheus can tell you the P99 latency over the last hour but cannot tell you why request #4821 specifically was slow. Tempo can tell you why request #4821 was slow but cannot tell you the overall P99. Knowing the shape tells you where to look and where not to.

---

### Step 3: Trace the Data Flow — Find the Breaks

**Goal:** Map the full lifecycle of data from birth to query, and identify every point where data disappears, is not captured, or cannot be correlated.

**Thinking Framework — Follow the Data:**
```
Something happens in the world
    → Who/what observes it?
    → How is it encoded?
    → How is it transmitted?
    → Who enriches or transforms it?
    → Where is it stored?
    → Who can query it?
    → What can they NOT see from here?
```

**Actions:**
1. Draw or describe the data flow as a pipeline, not a static diagram.
2. At each stage, explicitly ask: "What is lost here?"
3. Look for configuration that opts out of instrumentation (disabled flags, missing sidecars, absent ServiceMonitors) — these are the breaks.
4. Classify each break by severity:
   - **Critical:** Core functionality is a blind spot (e.g., the main orchestrator emits no telemetry)
   - **High:** Most services missing a full signal type
   - **Medium:** Signals exist but are disconnected (can't correlate A to B)
   - **Low:** Enrichment gaps (data exists but lacks context labels)

**Decision Point:** You have a list of breaks ranked by severity. Each break has:
- Where data disappears
- What configuration or code causes it
- What an engineer cannot know as a result

---

### Step 4: Separate Envelope from Contents

**Goal:** Distinguish between infrastructure-generated telemetry (what the platform knows about your service) and application-generated telemetry (what your service knows about itself).

**The Envelope vs. Contents Mental Model:**

```
ENVELOPE (platform-generated):
  The platform observes your service from the outside.
  It knows: request arrived, response sent, how long it took, status code.
  It does NOT know: what the request contained, why it was slow,
                    what business logic ran, what the LLM returned.

  Examples: Istio metrics, Kubernetes kube-state-metrics,
            load balancer access logs, VPC flow logs.

CONTENTS (application-generated):
  Your service reports on its own internal state.
  It knows: which database query ran, what the confidence score was,
            how many tokens the LLM consumed, which code path was taken.

  Examples: custom Prometheus counters, OTel trace spans,
            structured application logs, business event metrics.
```

**Key Questions to Ask:**
- For each service: does observability come from the envelope, the contents, or both?
- If only envelope: you know there is a problem, but not why.
- If only contents: you understand individual requests but may miss system-wide patterns.

**Thinking Framework:**
- "The envelope tells you there IS a problem."
- "The contents tell you WHY there is a problem."
- A mature observability stack needs both for every critical service.

**Actions:**
1. For each service in the system, mark: envelope-only / contents-only / both / neither.
2. Services that are "envelope-only" are where the next instrumentation investment should go.
3. Services that are "neither" are critical gaps — prioritize immediately.

**Decision Point:** You have a table of services with their coverage type. You can say:
- "We have envelope for all services but contents for only [N] of [M] services."

---

### Step 5: Apply the Three-Level Detective Test

**Goal:** Validate whether the observability stack (or any information architecture) can answer questions at all three levels of diagnosis. This is the completeness check.

**The Three Levels:**

```
Level 1 — "Is the system healthy?" (answered by Metrics / Numbers)
  Q: What is the current error rate?
  Q: Is P99 latency within SLA?
  Q: Are all pods running?
  Tool: Prometheus dashboards, alerts

Level 2 — "Where is it unhealthy?" (answered by Traces / Trees)
  Q: For this slow request, which service was the bottleneck?
  Q: Which Temporal activity failed and caused the retry?
  Q: What was the call graph for case ID 9876?
  Tool: Distributed tracing (Tempo, Jaeger)

Level 3 — "Why is it unhealthy?" (answered by Logs / Events)
  Q: What error message was printed during that span?
  Q: What was the exact SQL query that timed out?
  Q: What did the LLM API return before the timeout?
  Tool: Log aggregation (Loki, CloudWatch Logs)
```

**Scoring:**
- All three levels answerable → Observability is complete for this system
- Level 1 only → You know something is wrong, but you are guessing at cause
- Level 1 + Level 3 → You have raw evidence but no map to connect it
- Level 2 missing → You cannot trace individual requests; debugging is manual reconstruction

**The Cross-Signal Bonus (Level 4):**
When the three levels are connected — a metric spike links to an example trace, a trace span links to its log lines — you gain a fourth capability:

```
Level 4 — "Show me the evidence chain"
  Click a metric spike → jump to example trace
  Click a trace span   → jump to correlated log lines
  Click a log error    → jump to the trace that produced it
```

**Decision Point:** You can state the current level coverage:
- "The system answers Level [N] questions but not Level [N+1]."
- "The next investment should be [component] to enable [level] questions."

---

### Step 6: Produce the Output

**Goal:** Translate the analysis into the form that is most useful for the audience.

**Output Formats by Audience:**

| Audience | Best Format |
|---|---|
| Engineer learning a new system | Learning doc with ASCII diagrams + concrete examples |
| Team deciding what to build next | Gap table ranked by severity + proposed architecture diagram |
| Engineer debugging right now | Data flow trace for a specific request type |
| Manager understanding investment | Before/after capability table in plain language |

**Principles for Every Output:**
1. **Lead with the pain, not the solution.** The first paragraph should describe the problem, not the tool.
2. **One diagram, one message.** Every ASCII diagram should have exactly one thesis. If it is trying to show two things, split it.
3. **Concrete before abstract.** Show a real example (a specific request, a specific case ID, a specific error) before the general pattern.
4. **Name the blind spots explicitly.** A good analysis says what cannot be known, not just what can.
5. **The "before and after" is the punchline.** Show the current state and the target state side by side — that is where the value of the analysis becomes obvious.

---

## Application to Any Domain

This framework is not specific to observability. It applies to any complex system:

```
CI/CD pipeline:
  Pain      → "Builds fail and no one knows why or which step"
  Shape     → Event stream of job executions with status and duration
  Breaks    → Test logs not captured, no artifact lineage
  Envelope  → GitHub status checks (passed/failed)
  Contents  → Test output, coverage reports, build timing per stage
  Test      → L1: did it pass? L2: which step failed? L3: what was the error?

Database architecture:
  Pain      → "Queries are slow and we don't know which ones"
  Shape     → Number over time (query latency, connection pool usage)
  Breaks    → Slow query log disabled, no per-query tracking
  Envelope  → CPU/memory of DB instance
  Contents  → Query execution plans, index hit rates, lock contention
  Test      → L1: is DB healthy? L2: which query is slow? L3: why is it slow?

Organizational structure:
  Pain      → "Decisions made in one team surprise another team"
  Shape     → State snapshot (who owns what, what is decided)
  Breaks    → No RFC process, no decision log
  Envelope  → Org chart (who exists)
  Contents  → Decision records, runbooks, team charters
  Test      → L1: does the team exist? L2: who owns this? L3: why was this decided?
```

**The framework is universal because the underlying question is always the same:**
> Where does information exist, where does it disappear, and who suffers from not having it?

---

## Present Results to User

When analysis is complete, present in this order:
1. **The pain** — one sentence on what problem exists
2. **Current state diagram** — ASCII showing what exists now and where data flows
3. **Gap table** — ranked list of what cannot be known and why
4. **Target state diagram** — ASCII showing what the system looks like after gaps are filled
5. **Before/after capability table** — what questions become answerable

Always end with: "The highest-leverage next action is [specific thing] because it unblocks [Level N] questions for [most critical service/path]."
