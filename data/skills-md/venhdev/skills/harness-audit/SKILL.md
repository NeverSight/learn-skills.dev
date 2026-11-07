---
name: harness-audit
description: "Audit test suites and harness infrastructure for flakiness smells, hermetic deficits, and invariant blind spots."
disable-model-invocation: true
---

# harness-audit — Test Suite & Harness Quality Inspector

## Domain Rubric

### 1. The Audit Hierarchy

Inspect target test suites across progressive architectural layers:

1. **Harness Anchor & Foundation Layer**:
   - Inspect the authoritative project harness anchor at `.agents/harness-anchor.md` and follow its `Governing Testing SSOTs` routes to read project testing standards.
   - If missing: Check for legacy test guides (`test/AGENTS.md`, `tests/AGENTS.md`). If found, use as temporary SSOT and advise running `/zenf-init` to establish canonical `.agents/harness-anchor.md`. If absent, mark anchor as `UNGROUNDED` and route to `/zenf-init`.
   - Verify existence on disk of registered hermetic primitives (Deterministic Clock, Storage Sandbox, Fixtures / Factories, Transport / Network Mock, Lifecycle / Cleanup).
2. **Smells & Flakiness Traps**:
   - Evaluate tests against anti-patterns and flakiness traps detailed in `references/test-smells.md`.
3. **Invariant Dimension Blind Spots**:
   - Audit test coverage against invariant dimensions detailed in `references/invariant-dimensions.md`.

### 2. Mandatory Reference Grounding

Before executing audit passes, agents MUST read and ground themselves in:
- `references/test-smells.md` for concrete smell definitions and remedies.
- `references/invariant-dimensions.md` for invariant testing vectors.

### 3. Review Verdicts & Citation Rule

- `PASS`: Harness anchor active; hermetic foundation verified; zero flakiness smells; balanced invariant dimension coverage.
- `WARN`: Infrastructure present but maintenance debt observed (duplicate setup, missing assertion messages).
- `CRITICAL`: Harness anchor absent, foundation missing (no virtual clock/ephemeral storage), or flakiness smells detected (clock leaks, sleeps).
- **Dual-Citation Rule**: Every defect must cite both the offending code pointer (`file:///path/to/test#L<N>`) and the violated invariant/remediation.

## Canonical Output Contract

```markdown
# Harness Audit Report: <Target Scope>

## 1. Executive Verdict
- **Verdict**: <PASS | WARN | CRITICAL>
- **Target Inspected**: <Directory or Test Files>
- **Harness Anchor (SSOT)**: <Cited anchor pointer or 'UNGROUNDED (Missing .agents/harness-anchor.md)'>
- **Flakiness Risk**: <LOW | MEDIUM | HIGH>
- **Summary**: <Single-sentence technical judgment>

## 2. Infrastructure & Anchor Gaps
*(If clean: 'Harness anchor verified; foundational hermetic primitives active.')*
- **[<Anchor / Primitive>] <Gap Title>**: <Deficit description>
   - Impact: <Why this causes flakiness or maintenance debt>
   - Recommendation: <Architecture fix or seed anchor pointer>

## 3. Findings & Invariant Blind Spots
- **[<Smell / Dimension>] <Title>**: <Defect description>
   - Offending Code: [<file>#L<N>](file:///path/to/test#L<N>)
   - Remediation: <Exact architectural correction required>
```

### Routing

- Missing harness anchor requires setup → (via /zenf-init).
- Missing foundational hermetic primitives requiring architectural trade-off deliberation → (via /clarify).
- Discovered gaps or invariant blind spots ready for remediation planning → (via /changeset).
- A supported changeset authorizes localized test remediation and its acceptance criteria/verification → (via /forge).

## Execution Protocol

1. **Grounding & Scope Intake**:
   - Inspect `.agents/harness-anchor.md` if present.
   - Read `references/test-smells.md` and `references/invariant-dimensions.md`.
2. **Scale-Adaptive Audit Dispatch**:
   - *In-Turn Execution* (< 10 test files or localized suite): Inspect test suite against Audit Hierarchy directly in-turn.
   - *Subagent Fan-Out* (broad multi-package test suites): Launch concurrent `research` subagents dynamically scaled to partitioned directories or caller-declared budget, seeding with anchor and reference paths (offload raw test traces to `.agents/scratch/harness-<slice>-dossier.md`).
3. **Synthesis & Turn-Halt Gate (Fan-in)**:
   - Deduplicate findings into the Canonical Output Contract with pointers to any offloaded dossiers.
   - Present completed report into conversation stream and halt turn immediately.
