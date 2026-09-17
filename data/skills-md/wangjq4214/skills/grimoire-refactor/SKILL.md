---
name: grimoire-refactor
description: Orchestrate repository-scale structural improvement and behavior-preserving simplification through coverage tracking, dependency-ordered batches, integration, and measurable acceptance.
disable-model-invocation: true
---

# Purpose

Complete a large refactoring request without confusing a short findings list, isolated branch success, or a smaller file with a simpler codebase. Own coordination and acceptance; keep transformation and verification rules in the responsible skills.

# Scope and authorization

User-selected orchestration over `grimoire-map`, `grimoire-improve`, `grimoire-simplify`, `grimoire-test`, `grimoire-review`, and `grimoire-check`. Load each responsible skill when its stage is used. They remain independently usable. This skill does not replace `grimoire-loop`, which handles general implementation/QA; do not nest mandatory loops.

Discussion or audit-only requests do not authorize code changes. An explicit comprehensive implementation request authorizes reversible internal rewrites within its scope without per-batch approval. Preserve observable behavior and public contracts unless their change was explicitly approved. Ask only for material scope expansion, contract changes, or irreversible actions; do not repeatedly ask the user to pick findings already covered by authorization.

Multi-agent/worktree execution is optional, follows host permission rules, and requires any host-mandated opt-in. This skill is not permission to bypass that requirement. Serial execution must preserve the same coverage and gates. If a required skill is unavailable, disclose the gap and use equivalent explicit steps only when permitted; never report that an unexecuted skill ran.

# Workflow

## 1. Fix the baseline and acceptance criteria

Record scope, authorization, source revision plus dirty-tree fingerprint, baseline validation, and user changes to preserve. Establish a fixed LOC baseline and structural/readability targets using [references/measurement.md](./references/measurement.md).

For comprehensive simplification, default to at least 30% net production-code LOC reduction unless the user specifies otherwise. For bounded or architecture-only work, use the requested target rather than imposing this default. LOC is an independent gate, not permission to remove required behavior or a quota per agent.

Create `.grimoire/refactor/<run-id>/state.json` using [references/coordination.md](./references/coordination.md). Reuse valid prior evidence, not stale success flags.

Completion: Reproducible baseline, explicit gates, and resumable run state exist.

## 2. Map and discover through multiple lenses

Use `grimoire-map` to build or refresh repository navigation. Invoke `grimoire-improve` and `grimoire-simplify` in explicit analyze-only mode for discovery, even when the overall run authorizes implementation: workers must not modify production code before synthesis. Cover responsibility/state, control flow, duplication/dead code, abstractions/dependencies, and cross-module reuse. Omit irrelevant lenses with reasons, not whole unexamined subsystems.

Read-only reviewers may overlap. Require file-level coverage and concrete evidence; index hits are triage, not completed review. Persist module results so a large repository need not fit in one context window.

Completion: Every in-scope module has a discovery disposition; unread or blocked regions remain visible, and cross-module relationships have been examined.

## 3. Synthesize one dependency-ordered plan

Deduplicate findings by root cause and affected contract. Validate proposed deletions and structural findings against actual callers, registrations, tests, and configuration. Group coupled changes into coherent units with owned write paths, read dependencies, preserved contracts, checks, and expected benefit.

Set shared-helper ownership and interfaces before consumer migrations. Schedule dependency cycles and shared-file changes serially or as one atomic unit. Read-only overlap is useful; competing write ownership is not. Top findings may summarize the report but never cap the implementation backlog.

Completion: Every retained finding maps to a work unit or an evidence-backed disposition; ready units have stable prerequisites and nonconflicting ownership.

In audit-only mode, stop here after writing the findings/coverage report and proposed dependency plan. Mark audit completion separately from implementation: inspected requested scope and evidence-backed dispositions suffice; executing units, achieving LOC reduction, and implementation dry passes are not audit gates. Report unread/blocked regions as a partial audit. All proposed benefits remain estimates. For explicitly no-write requests, return the report inline instead of persisting map/run artifacts; use in-memory observations and preserve the same evidence requirements.

## 4. Execute and integrate in waves

Use `grimoire-improve` for responsibility/boundary changes and `grimoire-simplify` for behavior-preserving reduction. Use `grimoire-test` for baseline characterization and changed-risk tests. Workers receive the handoff described in the coordination reference and may not expand their write scope or redefine shared contracts independently.

With subagents, isolate independent writers in worktrees. Follow [references/coordination.md](./references/coordination.md) for base selection, branch preservation, staged integration, and recovery. The coordinator reads actual diffs and test evidence, integrates completed units in dependency order, and reruns affected checks on the combined tree. Refresh dependent work against the new integration base; conflict-free merging is not semantic verification.

Completion: Each integrated unit has current combined-tree evidence; rejected changes are repaired or selectively undone without discarding user work. Agent summaries alone never establish completion.

## 5. Verify the whole and rescan

Run `grimoire-review` against the integrated diff for regressions and cross-module consequences. Run `grimoire-check` against the acceptance criteria, independently from review readiness. Run relevant integration/build/type/lint tests and use `grimoire-test` where missing behavior evidence needs new tests. Preserve their existing classifications; unavailable checks remain unresolved.

Refresh affected map shards and recompute metrics. Rescan the full requested scope for obsolete paths, duplicate helpers, concentrated responsibilities, deep routing, and disconnected documentation. Route new findings back to step 3. After the backlog clears, require two consecutive full-scope discovery passes with no new actionable findings, using different lenses; a code change resets the count. Reuse hash-validated coverage, but revisit cross-module effects. Report any runtime/resource interruption as incomplete with a resumable next unit, not as convergence.

Completion: No actionable in-scope work remains, required checks have evidence, the map matches the integrated tree, and measured acceptance gates are evaluated.

## 6. Report actual outcomes

Write `.grimoire/refactor/<run-id>/report.md`: baseline/final scope and revision, net LOC and category totals, structural changes, coverage, completed/retained/blocked findings, commands/results, and artifact paths. Distinguish complete, incomplete, and blocked. Mark complete only when all required gates pass, including the requested reduction; otherwise state the exact shortfall and evidence. Do not stop merely at 30% if structural work remains, or declare 30% achieved because structural work is finished.

Completion: The user can verify both what changed and what remains, without trusting an agent's completion claim.

# References

- [coordination.md](./references/coordination.md) — persistent work ledger, agent handoff, and worktree integration
- [measurement.md](./references/measurement.md) — stable LOC accounting and anti-gaming acceptance
