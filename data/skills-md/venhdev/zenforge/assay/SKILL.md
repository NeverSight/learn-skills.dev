---
name: assay
description: "Evaluate changesets, task breakdowns, or code diffs for scope bloat, architectural drift, and regression risks."
disable-model-invocation: true
---

# assay — Mutation Review & Adversarial Quality Engine

## Domain Rubric

### 1. Review Dimensions

Inspect mutation artifacts against 4 structural dimensions:

- **Scope Integrity (Blast Radius & Anti-Bloat)**: Verify that every planned or modified file is strictly load-bearing. Flag accidental formatting, cosmetic churn, unrelated refactoring, speculative files, or lingering dead code left unpruned after replacement.
- **Contract & Spec Fidelity (Anti-Drift)**: Reconcile changes against governing specifications, SSOT documents, and established interfaces. Flag undocumented behavioral changes or broken contracts.
- **Structural Cohesion & Slicing**: Verify modular encapsulation without leaky abstractions. For tasks, verify true vertical slicing (end-to-end capability) over horizontal layer fragmentation.
- **Operational Hygiene & Safety**: Expose unhandled edge cases, resource leaks, lingering debug probes (`[DEBUG-<hex>]`), unredacted secrets, or unpurged transient scratch/task files.

### 2. Review Verdicts

- `PASS`: Zero structural or contract defects; blast radius is minimal and strictly load-bearing; ready for execution or commit.
- `CONDITIONAL`: Minor defects observed (accidental churn, missing edge test, localized bloat); actionable remediation provided to unblock.
- `FAIL`: Critical defects detected (contract violation, unauthorized blast radius, fake vertical slice, regression risk); reject and halt.

### 3. Anti-Hallucination & Grounding Guardrails

- **Dual-Citation Rule**: Cite both the offending code pointer (`file:///path/to/code#L<N>`) and the violated specification or interface contract (`file:///path/to/spec#L<M>`) for every reported `Contract & Spec Fidelity` defect; never claim drift without an authoritative specification citation.
- **Multi-Layer Contract Grounding**: Ground mutations against 3 authoritative layers: explicit specifications/tasks, structural code interfaces/schemas, and baseline test invariants; evaluate strictly on Scope Integrity and Hygiene when marked `UNGROUNDED` without inventing unstated requirements.

## Canonical Output Contract

```markdown
# Assay Report: <Target / Scope Name>

## 1. Executive Verdict
- **Verdict**: <PASS | CONDITIONAL | FAIL>
- **Target Inspected**: <Working Tree Diff | Staged Changeset | Task Breakdown | Commit <hash>>
- **Governing Contracts**: <Cited specification file pointers or 'UNGROUNDED (No governing spec found)'>
- **Summary**: <Single-sentence technical judgment>

## 2. Findings & Actionable Remediations
*(If PASS: 'No defects observed across scope integrity, contract fidelity, structural cohesion, and operational hygiene.')*

- **[<Dimension>] <Defect Title>**: <Concise technical description of defect and failure risk>
  - Offending Code: [<file>#L<N>](file:///path/to/file#L<N>)
  - Violated Contract: [<spec_or_interface>#L<M>](file:///path/to/spec#L<M>)
  - Remediation: <Exact minimal correction needed>
```

### Routing

- Verdict is PASS; the unapplied changeset/task is supported by evidence and execution scope is authorized → (via /forge).
- Scope or structural defects; re-stage the Changeset Tree → (via /changeset).
- Contract drift or ungrounded tensions → (via /clarify).

## Execution Protocol

### Phase 1: Scope & Contract Grounding

1. Ingest target mutation artifact (uncommitted diff, staged changeset, `.agents/tasks/`, or commit range).
2. Trace and ground governing boundaries across the codebase per Multi-Layer Contract Grounding guardrails.

### Phase 2: Scale-Adaptive Adversarial Review

1. Evaluate mutation scope scale:
   - *In-Turn Review* (localized diff of < 10 files, or single task card): Audit mutations directly in-turn against review dimensions.
   - *Subagent Fan-Out* (multi-package changesets or broad PR diffs): Launch concurrent `research` subagents dynamically scaled to partitioned slices or caller-declared budget (Role: `Mutation Reviewer (<Target Slice>)`). Seed each with:
     - Allocated diff slice and target file pointers.
     - Discovered governing contracts and invariant baselines.
     - The Dual-Citation Rule and Canonical Output Contract (offload extensive proof traces to `.agents/scratch/assay-<slice>-dossier.md`).

### Phase 3: Synthesis & Turn-Halt Gate (Fan-in)

1. Reconcile and deduplicate subagent findings into the Canonical Output Contract with pointers to any offloaded dossiers.
2. Compute the definitive Executive Verdict (`PASS` only if all slices pass; downgrade to `CONDITIONAL` or `FAIL` based on highest defect severity).
3. Emit the report into the conversation stream and halt turn immediately.

