---
name: simplify-audit
description: "Audit code simplification opportunities across scoped code, stage behavior-preserving changesets when justified, and route architectural decisions to design."
disable-model-invocation: true
---

# simplify-audit — Simplification Audit & Changeset Staging

## Domain Rubric

### Input & Boundary

Receive a file, function, module, subsystem, or repository scope. Inspect the target, governing contracts, call sites, and relevant checks; keep all work read-only. Scope width determines inspection depth, not an automatic redesign route.

Read [references/simplify-rubric.md](references/simplify-rubric.md) before evaluating candidates. Preserve semantics, error handling, ownership, and public contracts. Propose only changes whose equivalence is grounded; route unresolved architectural choices rather than silently expanding the design.

For broad input, identify cohesive slices and report what was inspected and what remains. Stage only sufficiently understood, suitably low-risk slices, including necessary cascades; never claim whole-repository coverage from a sample.

### State

- `PASS`: No worthwhile simplification breaches the rubric in the inspected scope; report briefly and end.
- `STAGED`: A concrete, behavior-preserving simplify changeset is ready for review, supported by equivalence evidence or applicable references and acceptance criteria.
- `UNRESOLVED`: Evidence, risk, or design decisions prevent reliable staging; report concise findings and the gap.

## Canonical Output Contract

````markdown
# Simplification Audit: <Scope> · <PASS | STAGED | UNRESOLVED>

<Short-to-medium conclusion; rubric-based opportunities and inspected coverage.>
Basis: <Equivalence evidence, governing contracts, checks/references; omit for a clean report.>
Gap: <Uninspected scope or unresolved decision; omit if none.>

<!-- STAGED only: -->
# Changeset: Simplify <Slice>

Acceptance: <Behavior and contracts that must remain unchanged.>

```text
|-- <subsystem>/
|   `-- <file>
|       `-- [UPDATE] <Rubric-based simplification and retained invariant>.
`-- <deep/path/to/caller>
    `-- [UPDATE] <Necessary behavior-preserving cascade; omit if none>.

Summary: <N> files affected (<C> created, <U> updated, <M> moved, <D> deleted).
```
````

For `PASS` or `UNRESOLVED`, omit the entire changeset, acceptance block, and file summary. This is one audit artifact with conditional staging, not a mandatory pair of reports.

### Routing

- The embedded changeset is supported and authorized; carry equivalence evidence and acceptance criteria → (via /forge).
- Behavior-preserving staging requires resolving requirements or trade-offs → (via /clarify).
- Simplification requires an architectural direction decision → (via /architect-decision).

## Execution Protocol

1. Ground the scope and apply the rubric. Audit localized work directly. For a broad multi-layer scope, pre-scout anchors and delegate grounded slices to workers seeded with boundaries, contracts, the local rubric path, and a findings/evidence/risk sub-report contract; consolidate rather than producing a directory inventory.
2. If clean, deliver `PASS` and end. If a reliable slice exists, embed its changeset and deliver `STAGED`; halt for authorization and keep implementation outside this skill. An embedded tree does not require `(via /changeset)`.
3. If architectural ownership, contracts, or trade-offs must change, report `UNRESOLVED` with the design gap. Broad scope alone is not a design blocker.
4. Finish at report, staging, or design handoff; keep refactor implementation outside this skill.
