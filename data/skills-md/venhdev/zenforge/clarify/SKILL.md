---
name: clarify
description: "Resolve architectural ambiguities, edge cases, and system trade-offs for proposed features or refactors before implementation planning."
---

# clarify — Architectural Deliberation Engine

## Domain Rubric

### 1. Deliberation Dimensions

Evaluate proposals against 5 core architectural dimensions:

- **Data Contracts & Schemas**: Boundaries, serialization, entity models, and migration compatibility.
- **State & Lifecycle**: Source of truth, mutation paths, concurrency, and persistence.
- **Failure Modes & Resilience**: Error boundaries, partial failure, fallback strategies, and recovery.
- **System Boundaries**: Service responsibilities, dependency blast radius, and external integrations.
- **Non-Functional Guardrails**: Latency, throughput limits, scalability constraints, and security.

### 2. Traversal & Deliberation Guardrails

- **Scope Discipline**: Confine inquiry strictly to high-impact architectural decisions, failure modes, and system invariants; forbid syntax bikeshedding or micro-optimizations.
- **Orthogonal Batching vs. Causal Sequencing**:
  - *Orthogonal (Independent)*: Batch 1–5 independent questions in a single turn to eliminate conversational round-trip latency.
  - *Causal (Branching)*: Isolate branching decisions into strictly one question per turn when downstream options depend directly on the chosen path.
- **Mandatory Recommendation & Fast-Path**: Pair every question with an authoritative technical recommendation and rationale. Support batch fast-path approval (e.g., "accept recommendations" or "approved except Q<N>: [Option]").
- **Root-First Traversal & Pruning**: Resolve highest-impact branching points first; prune obsolete dependent questions immediately upon user response.
- **Autonomous Convergence**: Continue probing until high-impact tensions converge or user prompts to conclude; forbid arbitrary question caps.
- **Convention Pruning**: Adopt standard idioms without prompting when choices have zero cross-module impact.

### 3. Canonical Question Payload Format

```text
### Q<N>: <Architectural Dimension>
Bottleneck: <Single-sentence technical tension or edge-case risk>

• [A] <Option Title> ── Trade-off: <Advantage> vs. <Disadvantage>
• [B] <Option Title> ── Trade-off: <Advantage> vs. <Disadvantage>
• [C] <Option Title> ── Trade-off: <Advantage> vs. <Disadvantage>

Recommendation: [Option] because <Single-sentence technical rationale>
```

## Canonical Output Contract

```markdown
# Architectural Decision Dossier: <Scope / System Slug>

## 1. Scope & Core Constraints
- **Target Boundary**: <Primary subsystem, domain, or integration boundary>
- **Core Dilemma**: <Primary architectural tension or trade-off resolved>
- **Convergence**: <Settled questions: Q1..QN>

## 2. Settled Decisions

### [Q1] <Architectural Dimension> ── <Chosen Option>
- **Bottleneck**: <Operational tension, failure risk, or contract ambiguity addressed>
- **Rationale & Trade-off**: <Core benefit gained> vs. <accepted systemic cost/complexity>
- **Enforced Invariant**: <Concrete non-negotiable rule, contract constraint, or boundary guardrail>

### [Q2] <Architectural Dimension> ── <Chosen Option>
- **Bottleneck**: <Operational tension, failure risk, or contract ambiguity addressed>
- **Rationale & Trade-off**: <Core benefit gained> vs. <accepted systemic cost/complexity>
- **Enforced Invariant**: <Concrete non-negotiable rule, contract constraint, or boundary guardrail>

## 3. Blast Radius
- **Open Decisions**: <Unresolved questions and their impact if the caller concludes deliberation early; omit when none>
- **Impacted Subsystems**: `<Component A>`, `<Component B>`
- **Banned Anti-Patterns**: <Explicitly forbidden workarounds or failure-prone designs>
```

### Routing

- Settled decisions establish a supported direction for file-impact planning → (via /changeset).
- A supplied candidate and direction need empirical proof → (via /spike).
- Remaining choices require an architectural direction decision → (via /architect-decision).

## Execution Protocol

### Phase 1: Surface & Gap Ingestion

1. Inspect proposal and authoritative contracts (via `/ssot`).
2. If requirements conflict with established specifications or ADRs: halt immediately, cite contradiction pointers, and deliberate resolution.
3. If zero architectural ambiguities exist, short-circuit directly to Phase 3; otherwise proceed to Phase 2.

### Phase 2: Deliberation Interview

1. Partition unresolved dilemmas: batch orthogonal questions (max 5) or sequence causal branching decisions (1 per turn), each adhering to Canonical Question Payload Format with recommendation.
2. Present payload and halt turn immediately to await user response.
3. Ingest response (supporting fast-path approval), prune settled branches, and evaluate remaining ambiguities.
4. Repeat until critical architectural vectors converge or user prompts to proceed, then advance to Phase 3.

### Phase 3: Decision Dossier Synthesis

1. Compile settled decisions into the Canonical Output Contract.
2. Deliver the completed `Architectural Decision Dossier` and halt turn immediately.
