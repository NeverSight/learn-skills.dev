---
name: inspect-perf
description: "Audit source code for semantic performance debt, N+1 queries, memory retention, and concurrency bottlenecks."
disable-model-invocation: true
---

# inspect-perf — Semantic Performance & Resource Efficiency Auditor

## Domain Rubric

### 1. Scope & Tolerability Guardrails (What to Ignore)

- **Mandatory Target Scope**: The user MUST specify an explicit target path (`file`, `directory`, or `subsystem`). If no target scope is provided, halt turn immediately and prompt for scope; forbid speculative full-repository scans.
- **Semantic Debt vs. Micro-Benchmarking**: Confine analysis strictly to structural algorithmic risks, I/O multipliers, and resource retention; ignore sub-microsecond instruction micro-optimizations, compiler inlining nits, or premature caching on cold paths.
- **Governing Reference**: Evaluate performance patterns strictly against `references/performance-rubric.md`.

### 2. Decision Bifurcation: [LOCAL-FIX] vs. [ARCHITECTURAL-REFACTOR]

- `[LOCAL-FIX]` (Localized In-Function Optimization): Algorithmic lookup indexing ($O(1)$ set/map), loop invariant hoisting, or string builder replacement within a single method/file. Route behavior-preserving candidates to `/simplify-audit`; new query limits or altered result semantics require `/changeset`.
- `[ARCHITECTURAL-REFACTOR]` (Systemic Structural Remediation): Decomposing Cartesian joins into Split Queries / DataLoaders, extracting Transactional Outbox to decouple network I/O from database transactions, worker thread offloading, or introducing bounded distributed caches. Route remediation to `/changeset`.

## Canonical Output Contract

```markdown
# Performance Audit Dossier: <Target Scope>

## 1. Executive Summary
- **Target Inspected**: `<directory_or_file_path>`
- **Health Rating**: <OPTIMAL | LOCALIZED_BOTTLENECK | CRITICAL_DEGRADATION>
- **Primary Bottleneck**: <Single-sentence summary of highest-latency or highest-risk resource hazard>

## 2. Load-Bearing Defect Catalog
### [<CRITICAL | MAJOR>] [<LOCAL-FIX | ARCHITECTURAL-REFACTOR>] <Dimension>: `<Target Symbol / Query>`
- **Offending Code**: [<file>#L<N>](file:///path/to/file#L<N>)
- **Violated Rubric**: [<spec_or_dimension>](references/performance-rubric.md#anchor)
- **Smell**: <Observable bottleneck, complexity multiplier, or resource leak description>
- **Action**: <[LOCAL-FIX] Local optimization OR [ARCHITECTURAL-REFACTOR] Separation / batching path>

*(Emit 'No load-bearing performance defects observed across rubric dimensions' if clean)*
```

### Routing

- Local indexing or builder changes whose behavior equivalence can be audited → (via /simplify-audit).
- Changes to result semantics or systemic split-query, outbox, connection-pool, or thread-pool refactorings → (via /changeset).

## Execution Protocol

1. **Intake & Scope Gate**:
   - Ingest target scope (`file`, `directory`, or `subsystem`).
   - **Enforce Scope Gate**: If no explicit scope is provided, halt turn immediately and prompt user: `"Vui lòng chỉ định rõ phạm vi kiểm tra (file, thư mục hoặc subsystem) khi sử dụng /inspect-perf."`
   - Read and ground in `references/performance-rubric.md`.

2. **Scale-Adaptive Pragmatic Audit**:
   - In-Turn Execution (< 10 files or cohesive module): Audit code directly in-turn against rubric dimensions.
   - Subagent Fan-Out (broad multi-package subsystem): Launch concurrent `research` subagents dynamically scaled to partitioned slices or caller-declared budget (Role: `Performance Inspector (<Slice>)`) seeded with slice coordinates, discovered anchors, Domain Rubric, and Output Contract (offload extensive profiling traces to `.agents/scratch/perf-<slice>-dossier.md`).
   - Enforce Section 1 Guardrails: ignore micro-benchmarking noise on non-hot paths; classify every finding explicitly as `[LOCAL-FIX]` or `[ARCHITECTURAL-REFACTOR]`.

3. **Synthesis & Turn-Halt Gate**:
   - Consolidate findings into the Canonical Output Contract with pointers to any offloaded dossiers.
   - Assign definitive Health Rating (`OPTIMAL`, `LOCALIZED_BOTTLENECK`, `CRITICAL_DEGRADATION`).
   - Present completed dossier into conversation stream and halt turn immediately.
