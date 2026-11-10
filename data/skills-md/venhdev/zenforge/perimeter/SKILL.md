---
name: perimeter
description: "Detect raw runtime API bypasses circumventing internal abstractions and codify enforceable boundary constraints."
disable-model-invocation: true
---

# perimeter — Architectural Boundary & Bypass Detection Engine

## Domain Rubric

### 1. Boundary Audit Dimensions

- **Sanctioned Primitives vs. Raw Bypass (Horizontal)**: Identify internal wrappers governing I/O, network clients, resources, or lifecycles; flag call sites bypassing them for raw runtime APIs.
- **Layer & Dependency Directionality (Vertical)**: Trace import graphs across architectural layers (Domain, App, Infra, UI); flag inverted or cross-boundary imports.
- **Resource & Sandbox Hygiene**: Audit storage paths, concurrency pools, and memory buffers; flag unanchored filesystem access or unthrottled resources.
- **Micro-Snippet**:
  ```text
  Banned:   fetch("https://api.domain/orders") // Raw runtime bypass
  Required: appHttpClient.get("/orders")       // Sanctioned primitive with auth & telemetry
  ```

### 2. The Load-Bearing Qualification Gate

Qualify candidate constraints strictly against 3 conditions:
1. *Existing Sanctioned Primitive*: Codebase defines an internal wrapper, base class, or canonical path addressing the boundary.
2. *Empirical Bypass Evidence*: At least one active call site violates the boundary by calling raw APIs directly.
3. *Quantifiable Failure Risk*: Bypass induces architectural drift, resource leaks, memory exhaustion, or security exposure.
- **Negative Boundary**: Confine constraints strictly to load-bearing architectural boundaries with existing internal primitives; never police cosmetic styling, standard utility methods (`Math.*`, collections), or speculative rules lacking active wrappers.

## Canonical Output Contract

```markdown
# Perimeter Report: <Target Subsystem / Scope>

## 1. Executive Verdict
- **Target Inspected**: `<directory_or_package>`
- **Verdict**: <HARDENED | PARTIAL | UNPROTECTED> (<N> active boundaries)
- **Primary Risk**: <Single-sentence technical judgment on highest boundary exposure>

## 2. Qualified Boundary Declarations
*(If HARDENED: 'All architectural boundaries are enforced by active test suites; zero raw bypasses detected.')*

### Boundary: <Constraint Name, e.g., Direct Network Client Bypass>
- **Offending Evidence**: [<file>#L<N>](file:///path/to/file#L<N>) ── <Bypass snippet or call site>
- **Failure Risk**: <Concrete risk: memory leak / auth bypass / architectural drift>
- **Rule**: Required: `<Sanctioned Primitive>` ── Banned: `<Forbidden Raw API>`
- **Enforcement**: Tier: `<Arch Unit Test | AST Linter | Script Guard>` | Whitelist: `<Exempt files | 'None'>`

## 3. Disqualified Invariants (Pruned) *(omit if no candidate patterns pruned)*
- **[PRUNED] <Candidate Pattern>**: <Reason for rejection, e.g., No existing codebase primitive / Trivial style issue>
```

### Routing

- Qualified boundaries need a concrete implementation plan → (via /changeset).
- Boundary tests have an evidence-backed changeset and authorized execution scope → (via /forge).
- Boundary ownership, whitelist exceptions, or architectural trade-offs require human deliberation → (via /clarify).

## Execution Protocol

### Phase 1: Macro Anchor Grounding

1. Ingest target directory or subsystem.
2. Scout architectural anchors (internal wrappers, sanctioned clients, resolvers, base interfaces) to ground boundary baselines.

### Phase 2: Scale-Adaptive Boundary Audit

- *In-Turn Execution* (< 10 files or localized module): Audit call sites against discovered anchors directly in-turn.
- *Subagent Fan-Out* (broad codebase or cross-layer scopes): Launch concurrent `research` subagents dynamically scaled to partitioned slices or caller-declared budget (Role: `Perimeter Reviewer (<Slice>)`), seeded with target slice directory, discovered architectural anchors, Load-Bearing Qualification Gate, path to `references/fitness-functions.md`, and Canonical sub-report contract requiring offending code pointers (`file:///...#L<N>`).

### Phase 3: Codification & Turn-Halt Gate (Fan-in)

1. Reconcile findings into the Canonical Output Contract, moving ungrounded rules to Section 3 (Pruned; omit Section 3 if none).
2. If boundary ownership or whitelist exemptions contain unresolved trade-offs: halt and deliberate (via `/clarify`).
3. Emit the report into the conversation stream and halt turn immediately.
