---
name: inspect-deps
description: "Audit and test dependency version upgrades in an isolated worktree with before/after trade-off analysis."
disable-model-invocation: true
---

# inspect-deps — Isolated Dependency Upgrade & Trade-off Auditor

## Operating Invariants

- **Isolated Worktree Boundary**: Always stage and execute version upgrades inside a dedicated Git worktree (`chore/deps-<slug>`) via `/worktree`; forbid mutating root workspace files during dependency experiments.
- **Evidence-Backed Verification**: Every proposed upgrade must be verified by native typecheck, linter, and full test suites before recommending merge.
- **Zero Hallucinated Targets**: Target versions must exist on official registries; evaluate breaking changes against concrete changelogs rather than assumptions.

## Domain Rubric

1. **Target Selection (Best Fit vs. Latest Available)**:
   - *Best Fit (Recommended)*: Latest minor/patch release, or a mature major release with high ROI (fixes CVEs, supports new OS/runtime platform features like Node LTS, Android/iOS SDKs).
   - *Beyond Best Fit (Bleeding Edge)*: RC/Alpha builds or unproven majors that introduce high API churn without clear architectural benefits.
2. **ROI & Breaking Change Evaluation**:
   - Assess whether migration costs (file changes, test repairs, API rewrites) justify the benefits (security patches, perf gains, unblocking platform APIs). If ROI is low, keep the current locked version.

## Canonical Output Contract

````markdown
# Dependency Audit & Upgrade Report: <Target Scope>

## 1. Upgrade Matrix
| Package | Before | Target | Verdict | Verification |
|---|---|---|---|---|
| `<pkg>` | `<v_old>` | `<v_target>` | <DIRECT | MIGRATED | RETAINED> | <PASS (N tests) | FAILED> |

## 2. Best-Fit Target & Justification
- **`<pkg>` (Target: `<ver>`)**: <Why this version is the sweet spot: compatibility, bugfixes, CVE elimination, or runtime readiness>.

## 3. High-Break Trade-off & ROI Analysis
- **Candidate**: `<pkg>` ➔ `<bleeding_edge_ver>`
- **Breaking Seams**: <Affected APIs, config changes, or downstream impact>.
- **Worth the Breaking Change?**: <YES | NO>. <Explicit justification: why taking or declining the migration cost makes engineering sense>.
````

### Routing

- Merge verified worktree back to target branch → (via /worktree).
- Discard experiment and prune dirty worktree → (via /sweep).
