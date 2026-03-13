---
name: do-execute
description: >
  Execute an approved plan through structured phases with built-in quality gates.
  Use this skill whenever the user says "plan is approved", "go ahead", "proceed
  with implementation", "let's build this", or otherwise confirms they want to
  start implementing a previously planned task. Also trigger when the user has a
  clear, explicit task that doesn't need planning. Do NOT use when planning is
  incomplete or the user is still exploring approaches — run do-plan first.
argument-hint: "[plan reference or task]"
---

Execute an approved plan through six phases: scope → implement → polish → review → verify → finalize.

## Entry Gate

No approved plan in context → run do-plan first. Never begin execution when planning is incomplete. Never edit the plan file for status tracking.

**"Approved" means explicit user confirmation after `Plan is ready for execution.` — not the readiness declaration itself. If the user has not confirmed, stop and ask.** See do-plan Readiness Declaration for approval definition.

## Depth

Classify at entry. Depth controls fanout per phase, not which phases run — all six always execute.

| Level | Behavior |
|-------|----------|
| `focused` | Main thread handles all phases inline — no subagent dispatch |
| `standard` | Subagent dispatch per phase |
| `deep` | Subagent dispatch per phase with expanded fanout |

## Evidence Levels

See AGENTS.md for E0–E3 definitions. Blocking claims MUST be E2+. Verify claims MUST be E3.

## Phases

**Session ID**: When executing an approved do-plan, reuse the plan's session ID and directory. Otherwise generate per SPINE.md Sessions convention. Append to the session log at each phase boundary (scope, implement, polish, review, verify, finalize) and on re-entry iterations. All output paths below use `<session>` as placeholder.

At `focused` depth, main thread handles every phase inline — no subagent dispatch. The subagent roles below apply to `standard` and `deep` only. Every subagent prompt MUST be self-contained: include scope artifact, files modified, and plan excerpt. Subagents inherit no conversation history.

**Subagent dispatch policy**: Each role uses its specialized agent type. Every dispatch prompt MUST include:
- The exact output file path (`.scratch/<session>/<prescribed-filename>.md`)
- The constraint: "Write your complete output to that path. You may read any repository file. Do NOT edit, create, or delete files outside `.scratch/<session>/`. Do NOT run build commands, tests, or destructive shell commands."

| Phase | Agent type | Rationale |
|-------|-----------|-----------|
| Implement | `@worker` | Read-write implementation — edits project source files per partition |
| Polish | `@analyst` | Advisory-only findings with `[S]`/`[F]` prefixes, no gate authority |
| Review | `@inspector` | Verdict-focused review with `[B]`/`[S]`/`[F]` severity and spec compliance taxonomy |
| Verify | `@verifier` | Adversarial verification — runs commands, read-only for project source |

This is a prompt-level constraint, not a platform-enforced restriction. It is adequate for review workloads where agents have no operational reason to modify source files.

### 1. Scope

Main thread only (all depths). Read the approved plan, classify depth, partition the work.

Output `scope_artifact`:

| Field | Content |
|-------|---------|
| `target_files` | Repo-relative paths for all files in scope |
| `partitions` | Independent vs dependent groupings; colocated files stay together |
| `blocking_questions` | Must be empty before dispatching implement |
| `plan_excerpt` | Compact plan extract for worker consumption |

Ask the user when blocking questions are non-empty. Never carry unresolved questions into implement.

### 2. Implement

Dispatch implementation workers (`@worker` type, `implement` mode): one per partition. Parallel for independent partitions; sequential for dependent. No overlapping writes to the same file.

Output: `files_modified` — repo-relative list of all changed files.

One logical change per worker dispatch. Capture unrelated issues as follow-up tasks, not inline fixes.

Worker self-review before reporting: completeness, naming clarity, YAGNI discipline, tests verify behavior not mocks.

### 3. Polish

Two sub-steps:

1. **Advisory pass**: dispatch analysts **in parallel** (`@analyst` type):

   | Role | Persona | Output |
   |------|---------|--------|
   | `conventions-advisor` | Checks naming against codebase norms; flags deviations from established patterns, not style preferences | `.scratch/<session>/execute-polish-conventions-advisor.md` |
   | `complexity-advisor` | Identifies defensive bloat on trusted paths (NEVER flag auth/authz/validation) and premature abstraction | `.scratch/<session>/execute-polish-complexity-advisor.md` |
   | `efficiency-advisor` | Applies do-polish efficiency lens: reuse opportunities, N+1, missed concurrency, hot-path bloat | `.scratch/<session>/execute-polish-efficiency-advisor.md` |

   The standalone `do-polish` skill provides the same advisory lenses for use outside do-execute.

   **Synthesis**: main thread reads all output files, deduplicates findings, assigns E-levels. Every E2+ finding: action or explicit rejection with rationale. Silent drops prohibited.

2. **Apply**: workers (`@worker` type, `polish-apply` mode) apply synthesis actions from the advisory pass. Apply sub-step skipped when no actions exist.

Output: `polish_findings`, updated `files_modified`.

### 4. Review

Two stages, sequential:

1. **Tests & docs** (conditional): skip when no behavior-changing code AND `docs_impact` is `none`.
   Otherwise:
   - **Tests**: run test suites covering changed behavior; add missing coverage; produce test evidence (command executed + pass/fail + coverage data). Absent test evidence for behavior-changing code is a **blocking finding**.
   - **Docs**: update documentation per `docs_impact` classification. When `customer-facing` or `both`, include changelog entries using `use-writing` skill rules. Absent docs updates when `docs_impact` ≠ `none` is a **blocking finding**.
   Their output is context for stage 2.
2. **Adversarial review**: dispatch inspectors **in parallel** (`@inspector` type). Never skipped. At `focused` depth, run as a single inline pass with all three lenses rather than dispatching separate inspectors.

   | Role | Persona | Output |
   |------|---------|--------|
   | `spec-reviewer` | Validates every plan requirement has a corresponding implementation; flags missing and extra behavior | `.scratch/<session>/execute-review-spec-reviewer.md` |
   | `correctness-reviewer` | Probes for logic errors, edge cases, race conditions, and failure paths — assumes adversarial inputs | `.scratch/<session>/execute-review-correctness-reviewer.md` |
   | `risk-reviewer` | Evaluates security boundaries, performance implications, and scalability; scales depth by risk classification | `.scratch/<session>/execute-review-risk-reviewer.md` |

   **Synthesis**: main thread reads all output files. Deduplicate findings across reviewers. Assign final E-levels and severity buckets per `do-review` skill rules.

Blocking findings (E2+) → produce `re_dispatch_brief` → re-enter polish.
Advisory findings → record; proceed to verify.

Output: `review_findings` with E-levels per finding.

### 5. Verify

Dispatch `@verifier` type. Single verifier instance (all depths). The verifier receives `files_modified`, `review_findings`, and the plan excerpt. All verifier claims MUST be E3 (executed command + observed output). E2- claims are advisory only — never block completion on them.

Output: `verification_result` — PASS, FAIL, or PARTIAL with specifics.

### 6. Finalize

Main thread only. Sole completion authority.

1. Check content gates (see [Content Gates](#content-gates)).
2. Produce learnings as proposals only — never auto-apply. User must explicitly approve any rule, skill, or memory update.
3. Declare completion.

## Re-entry

```
Scope → Implement → Polish → Review → Verify → Finalize
                      ↑         |
                      └─────────┘  blocking review findings
                      ↑
                      └──── verify semantic failure
```

- **Blocking review findings** → re-enter polish (advisory re-runs, workers (`@worker` type, `review-fix` mode) apply fixes).
- **Verify semantic failure** (behavior/spec) → re-enter polish → review → verify.
- **Verify non-semantic failure** (lint, types, build) → workers (`@worker` type, `review-fix` mode) fix → re-verify only. No full loop re-entry.

Each re-entry at polish counts as one iteration. Cap: **5 iterations**. On cap: freeze best state and ask the user for approval to continue.

## Content Gates

Finalize cannot declare completion unless:

- **Tests** for behavior-changing work — with E3 evidence (executed command + pass/fail output)
- **Edge/failure coverage** for risk-bearing work
- **Docs** for user-visible, API, or config changes (`docs_impact` ≠ `none`) — including changelog entries when `docs_impact` is `customer-facing` or `both`

## Completion Declaration

Exact phrases:

- `Implementation complete.`
- `Implementation NOT complete` — followed by specific gaps listed.

## Anti-Patterns

- Skipping phases regardless of depth
- Advisory analyst writing to codebase files during polish (scratch writes are expected)
- Silently dropping E2+ polish findings without action or explicit rejection
- Blocking completion on E2- verifier output
- Making inline main-thread edits when not at focused depth
- Overlapping concurrent writes to the same file
- Auto-applying learnings in finalize
- Skipping tests-and-docs stage without verifying `docs_impact` classification
- Declaring completion without test evidence (E3) for behavior-changing code
