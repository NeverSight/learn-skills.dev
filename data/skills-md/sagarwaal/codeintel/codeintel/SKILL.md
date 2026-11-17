---
name: codeintel
description: Deeply analyze a software repository and create, consume, or incrementally maintain a local, Git-ignored .codeintel/ engineering knowledge base for architecture understanding, navigation, debugging, consistency reviews, test-gap discovery, change-impact analysis, and safe feature implementation. Use when onboarding to a codebase, auditing a project, investigating a bug, planning or implementing a feature, refactoring, reviewing code, writing tests, or refreshing repository knowledge—and always check and use .codeintel/ first whenever it exists in the workspace.
---

# CodeIntel

## Purpose

Build and maintain a durable, evidence-based knowledge layer over an existing software repository. The knowledge should help future developers and coding agents understand the project quickly, navigate to the right implementation, diagnose defects, assess change impact, find test gaps, and implement features consistently.

The source repository is the source of truth. Project intelligence is derived knowledge and must be verified against current code whenever it matters.

## Operating modes

Select the mode that fits the request:

1. **Deep Analysis** — create the initial `.codeintel/` knowledge base or perform a full rebuild when existing state is missing, invalid, or too unreliable to update incrementally.
2. **Workflow Grounding (Consumer)** — fast path when `.codeintel/` already exists and the primary task is planning, implementing a feature, fixing a bug, refactoring, writing tests, or reviewing code (including inside external workflows such as `/plan`, brainstorming, TDD, or subagent execution). Consume existing knowledge before editing code, then run a scoped/incremental refresh after the change.
3. **Task Investigation** — refresh and inspect only the knowledge needed for the current bug, feature, refactor, or design question rather than reanalyzing everything.
4. **Knowledge Refresh** — synchronize existing knowledge with source changes using a two-phase workflow: **Phase A — Check drift** (read-only) followed by **Phase B — Refresh knowledge** (writes approved scope: `incremental`, `scoped`, or `full`).
5. **Audit** — revalidate correctness, architecture, consistency, security, performance, maintainability, and testing claims within the requested scope.

If the user's intent is ambiguous, infer the narrowest useful mode and explain the scope. A routine refresh must not automatically become a full audit; conversely, if a refresh uncovers a potential critical defect, investigate and record it with evidence rather than treating the refresh as documentation-only.

| Mode | Run | Skip unless needed |
|---|---|---|
| Deep Analysis | Steps 0–15 (`full` scope) | — |
| Workflow Grounding | Step 0 (Before/During/After workflow hook) + Step 14 (`incremental` refresh after code edits) | Broad reconnaissance and repo-wide rewrites |
| Task Investigation | Step 0, then Steps 5, 6, 7 scoped to the task; Step 14 (`scoped` refresh) | Broad reconnaissance and repo-wide audits |
| Knowledge Refresh | Step 0, Step 14 Phase A (drift plan) -> Phase B (targeted Steps 3–7 + patch + checkpoint); Step 15 | Unchanged areas |
| Audit | Step 0, Steps 6, 7, 9, 10, 13, 15 | Feature guidance (Step 11) |

Scale the work to the request. A knowledge base that covers part of the repository accurately is better than one that covers all of it superficially.

## Orchestrator, Optional Subagents & Shared Evidence Model

CodeIntel operates around **one orchestrator, six specialized analysis roles, a shared evidence model, and a single controlled knowledge writer**.

Where the host coding agent supports subagents (e.g., `Task`/`Agent`/`invoke_subagent` tools), dispatch read-only subagents in parallel when their scopes are independent. Where the host does not support subagents, or when one role depends on another's output, execute the same role protocols sequentially in the main context. Never use an LLM subagent for a task that a deterministic script (`scripts/codeintel-refresh.sh` or `scripts/validate.sh`) performs predictably.

### Specialized Analysis Roles

| Role ID | Role Definition | Primary Responsibility | Can write `.codeintel/`? |
|---|---|---|---|
| `repository_mapper` | [agents/repository-mapper.md](agents/repository-mapper.md) | Map languages, entry points, modules, dependency direction, and dynamic registration | No (read-only) |
| `behavior_tracer` | [agents/behavior-tracer.md](agents/behavior-tracer.md) | Trace end-to-end execution, callers/callees, invariants, side effects, and error paths | No (read-only) |
| `change_impact_analyst` | [agents/change-impact-analyst.md](agents/change-impact-analyst.md) | Expand drift across direct/indirect dependencies ([impact-analysis.md](references/impact-analysis.md)) | No (read-only) |
| `test_quality_analyst` | [agents/test-quality-analyst.md](agents/test-quality-analyst.md) | Map behaviors to tests, distinguish inspected vs. executed tests, find behavioral gaps | No (read-only) |
| `defect_consistency_auditor` | [agents/defect-consistency-auditor.md](agents/defect-consistency-auditor.md) | Identify candidate defects, contract mismatches, and reassess open findings | No (read-only) |
| `knowledge_reconciler` | [agents/knowledge-reconciler.md](agents/knowledge-reconciler.md) | Resolve cross-agent conflicts, compare against existing claims, propose minimal patch plan | Proposes patch plan only |

All roles return structured results conforming to [evidence-model.md](references/evidence-model.md) ([templates/agent-result-template.json](templates/agent-result-template.json) and [templates/claim-template.json](templates/claim-template.json)). Only the **Knowledge Writer** phase of the main orchestrator applies approved updates to `.codeintel/`, and only the deterministic **Checkpoint Manager** advances `manifests/analysis_state.json` after validation passes.

### Task-Based Agent Selection

Do not run all six roles on every request. Select the minimal set needed:

| Operation | Roles to run |
|---|---|
| First-time deep analysis | `repository_mapper`, `behavior_tracer`, `test_quality_analyst`, `defect_consistency_auditor`, then `knowledge_reconciler` |
| Small bug investigation | `behavior_tracer`, `defect_consistency_auditor` |
| API contract change | `behavior_tracer`, `change_impact_analyst`, `test_quality_analyst`, then `knowledge_reconciler` |
| Incremental refresh | `change_impact_analyst`, relevant domain role (`behavior_tracer` / `test_quality_analyst`), `knowledge_reconciler` |
| Full refresh | All relevant analysis roles, then `knowledge_reconciler` |
| Knowledge audit | `knowledge_reconciler`, `defect_consistency_auditor`, `test_quality_analyst` |
| Documentation-only change | `change_impact_analyst`, `knowledge_reconciler` |
| New feature planning | `repository_mapper` (as needed), `behavior_tracer`, `change_impact_analyst`, `test_quality_analyst` |

## Non-negotiable safeguards

- Start by identifying the repository root, current branch/commit when available, and Git working-tree status.
- Preserve user changes. Never reset, clean, overwrite, or discard unrelated work.
- Do not modify application source code during a knowledge-only analysis or refresh unless explicitly authorized.
- Do not run destructive commands, migrations, deployment operations, or scripts with external side effects without explicit authorization.
- Inspect existing `.gitignore` and agent instructions before editing them.
- Do not overwrite existing project documentation or agent instructions. Make minimal additive changes.
- Never copy secrets, credentials, access tokens, private keys, sensitive environment values, or sensitive production data into the knowledge base.
- Treat a Git-ignored directory as excluded from normal Git tracking, not as a security boundary.
- Do not claim a test, command, scan, or verification passed unless it was actually run and passed.
- Distinguish verified facts from inference, suspicion, and unknowns.
- Do not claim exhaustive coverage when parts of the repository were not inspected.
- Never advance `repository.analyzed_commit` in `manifests/analysis_state.json` if a refresh fails or completes only partially.
- If the directory is not a Git repository, skip Git-specific steps, say so, and do not initialize Git.
- For large repositories or monorepos, work in phases, prioritize high-impact areas, checkpoint progress in `manifests/analysis_state.json`, and report partial coverage honestly instead of exhausting the context budget.

## Step 0 — Reuse existing knowledge & ground active workflows

Before analyzing or modifying anything, check whether `.codeintel/` (or an equivalent) already exists. Note that because `.codeintel/` is Git-ignored, standard search tools (`rg`, `git grep`) skip it by default—always check `.codeintel/INDEX.md` explicitly by path.

If `.codeintel/` exists:

1. **Read the entry pack:** Read `.codeintel/INDEX.md`, `.codeintel/agents/QUICK_START.md`, `.codeintel/agents/TASK_ROUTING.md`, and `.codeintel/manifests/analysis_state.json`. If `analysis_state.json` uses `"schema_version": 1`, migrate it in place to Schema v2 per [knowledge-base-structure.md](references/knowledge-base-structure.md#backward-compatible-migration-schema-v1---schema-v2) without discarding existing knowledge.
2. **Check targeted drift:** Run a read-only drift check against `repository.analyzed_commit` (see [change-protocol.md](references/change-protocol.md#step-1--detect-repository-changes)). If artifacts or claims relevant to the current task are marked `stale`, verify those specific files against current source first.
3. **Ground downstream workflows (Before -> During -> After):**
   - **Before planning / brainstorming / debugging:** Read the owning component doc (`components/*.md`), workflow trace (`workflows/*.md`), `DEPENDENCY_MAP.md`, and `KNOWN_ISSUES.md` to identify blast radius, invariants, and reference patterns without rediscovering the repo. When dispatching planner, implementer, or reviewer subagents in external workflows, pass the relevant `.codeintel/` file paths in their prompt context.
   - **During implementation / TDD / code review:** Follow `DESIGN_PRINCIPLES.md`, `FEATURE_IMPLEMENTATION_GUIDE.md`, `API_AND_CONTRACTS.md`, and `agents/REVIEW_CHECKLIST.md`; run the exact focused test commands recorded in `TEST_STRATEGY.md`.
   - **After code or test changes complete:** Run Step 14 (**Knowledge Refresh**, `incremental` or `scoped`) so `.codeintel/` and `manifests/analysis_state.json` stay synchronized with the newly written code.
4. **Select the narrowest mode:** Choose `Workflow Grounding`, `Task Investigation`, or `Knowledge Refresh` (`incremental`, `scoped`, or `full`) that satisfies the request.

If `.codeintel/` does not exist and the request is not Deep Analysis, do the task-scoped work first and offer to create the knowledge base rather than creating it unprompted.

## Step 1 — Reconnaissance

Inspect enough of the repository to establish its shape before drawing conclusions.

Identify, where applicable:

- Applications, packages, services, modules, and bounded contexts.
- Languages, frameworks, package managers, lockfiles, build systems, and runtime targets.
- Entry points, startup and shutdown paths, routing, middleware, dependency injection, and lifecycle hooks.
- Domain models, database schemas, repositories, migrations, and persistence boundaries.
- APIs, events, background jobs, external integrations, and public contracts.
- UI structure, routes, state management, and shared components.
- Test frameworks, test directories, CI workflows, build/deploy configuration, and operational tooling.
- Existing docs, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, or equivalent instructions.
- Generated code, vendored dependencies, build output, and caches that should generally be excluded from broad analysis.

Use manifests, repository search, symbol references, static analysis, and test discovery where available. Avoid blindly reading every file or scanning dependencies and build artifacts without a reason.

Record what was inspected and what was excluded.

## Step 2 — Create the local knowledge base

Create `.codeintel/` at the repository root unless an equivalent project-specific knowledge location already exists and is suitable.

Exclude the directory from Git without creating a tracked change, unless it is already covered:

1. **Default — local exclude.** Append the rule to `.git/info/exclude` (resolve the path with `git rev-parse --git-path info/exclude` so worktrees work). This is untracked and affects only this clone.
2. **Shared — `.gitignore`.** Add the rule to `.gitignore` only if the user asks, or if the repository already ignores similar local AI/tooling directories there. This is a tracked change; mention it in the final response.

```gitignore
# Local AI-generated code intelligence and repository analysis
/.codeintel/
```

Verify the rule with:

```bash
git check-ignore -v .codeintel/INDEX.md
```

If files inside the directory are already tracked, explain that ignore rules do not untrack them. Do not untrack or remove them without authorization.

Use the structure in [knowledge-base-structure.md](references/knowledge-base-structure.md) as a guide. Adapt it to repository scale; do not create empty boilerplate files.

At minimum, create a useful `INDEX.md`, `PROJECT_PROFILE.md`, `ARCHITECTURE.md`, `DIRECTORY_MAP.md`, `COMPONENT_CATALOG.md`, `DEPENDENCY_MAP.md`, `TEST_STRATEGY.md`, `TEST_COVERAGE_GAPS.md`, `KNOWN_ISSUES.md`, `DESIGN_PRINCIPLES.md`, `FEATURE_IMPLEMENTATION_GUIDE.md`, and `manifests/analysis_state.json` when justified by project complexity.

## Step 3 — Reconstruct architecture and behavior

Document architecture as implemented, not as assumed.

Trace:

- Application startup and shutdown.
- Critical user and system workflows from entry point through validation, authorization, business logic, persistence/integrations, response, errors, and cleanup.
- Architectural layers, responsibilities, allowed dependencies, interfaces, and boundaries.
- Important data flows, state transitions, invariants, and side effects.
- External contracts, compatibility constraints, and runtime assumptions.

Compare intended architecture with actual dependencies. Record discrepancies rather than silently choosing between conflicting documentation and code.

Use Mermaid diagrams when they materially improve understanding. Diagrams must reflect verified relationships.

## Step 4 — Analyze components

For high-impact, complex, shared, security-sensitive, or frequently changed components, record:

- Purpose, location, layer, and ownership.
- Public interfaces and important symbols.
- Callers, dependencies, shared state, and external interactions.
- Preconditions, postconditions, invariants, side effects, error behavior, and boundary cases.
- Validation, authorization, concurrency, lifecycle, and resource-management assumptions.
- Relevant tests and test gaps.
- Change-impact considerations.
- Known weaknesses and recommended patterns.

Assess cohesion, coupling, encapsulation, naming, readability, error contracts, duplication, abstraction quality, testability, and consistency. Do not mistake personal style preferences for defects; account for domain requirements and legitimate exceptions.

Create component-specific notes only when they add meaningful value. Avoid one document per trivial file.

## Step 5 — Build dependency and change-impact knowledge

For important symbols and components, identify relevant relationships:

- Calls, imports, implements, depends on.
- Reads/writes shared data.
- Publishes/consumes events.
- Validates or transforms contracts.
- Tests or mocks behavior.
- Is affected by or violates a constraint.

Distinguish compile-time, runtime, data, and conceptual dependencies. Identify high-blast-radius components such as shared abstractions, public interfaces, authorization boundaries, persistence layers, and critical workflows.

When static analysis cannot resolve reflection, dynamic registration, generated code, runtime dispatch, or external consumers, state the limitation.

## Step 6 — Audit correctness and consistency

Inspect for both local and cross-component defects, including:

- Incorrect conditions, boundary errors, invalid state transitions, missing validation, null-handling problems, and incorrect defaults.
- Lost or swallowed errors, incorrect retries, resource leaks, partial updates, and unsafe transaction boundaries.
- Race conditions, async sequencing errors, stale caches, and concurrency assumptions.
- API/model/frontend contract mismatches.
- Inconsistent interpretations of statuses, types, errors, or domain invariants.
- Duplicated business rules and divergent implementations.
- Alternate entry points that bypass authorization or validation.
- UI assumptions about optional or malformed responses.
- Dead code or compatibility paths, where evidence supports the claim.

For every significant finding, record an ID, severity, confidence, category, affected paths/symbols, evidence, observed and expected behavior, reproduction conditions if known, impact, root-cause status, recommended remediation, regression tests, related components, and verification status.

Classify findings as **confirmed**, **strongly suspected**, **potential risk**, **design concern**, or **maintainability concern**. A suspicious pattern is not automatically a defect.

## Step 7 — Test and coverage intelligence

Map important components and behaviors to existing tests.

Inspect unit, integration, API, contract, component, end-to-end, property-based, performance, and security tests as applicable. Record actual commands and prerequisites from project configuration.

Assess behavioral coverage, not just line coverage. Look for missing boundary cases, error paths, authorization-denial paths, rollback behavior, integration contracts, concurrency behavior, and regression tests.

Distinguish “not found in inspected tests” from “no tests exist.” If coverage reports are unavailable, label coverage assessments as inspection-based rather than measured.

Provide focused test commands and explain which suites should run after common change types. Do not weaken tests just to accommodate incorrect behavior.

## Step 8 — Derive design principles and reference patterns

Document established project conventions before recommending new ones.

Identify real reference implementations for patterns such as a well-structured service, API handler, business rule, persistence operation, UI component, error-handling path, integration, and meaningful test.

Explain why each is a good example and where it applies. Also record anti-patterns when that prevents repeated mistakes.

Prioritize existing contracts, domain correctness, security, simplicity, established language/framework idioms, and maintainability. Do not introduce fashionable patterns or abstractions without a concrete need.

## Step 9 — Review security, performance, and operations proportionately

Review relevant risks such as authorization, trust boundaries, injection, unsafe deserialization, secret handling, sensitive logs, file access, SSRF, XSS/CSRF where applicable, unsafe defaults, dependency risks, rate limiting, and cryptographic misuse.

Inspect likely performance issues such as N+1 queries, unbounded queries, repeated expensive work, blocking operations, excessive allocations, unnecessary network calls, cache misuse, unbounded concurrency, and UI rendering/bundle concerns.

Inspect reliability concerns such as timeouts, retries, health checks, graceful shutdown, migrations, background jobs, configuration validation, observability, cleanup, and rollback procedures.

Separate confirmed findings from hypotheses requiring runtime tests, profiling, or specialist review. Do not describe static inspection as a complete security audit.

## Step 10 — Document issues and recommendations

Maintain actionable issue records with severity, confidence, status, affected paths, evidence, impact, root cause if established, remediation, regression tests, dependencies, and relative effort.

Prioritize based on impact, likelihood, security exposure, affected workflows, regression risk, and cost of leaving the issue unresolved. Keep confirmed defects separate from optional improvements.

## Step 11 — Document feature implementation guidance

Create a practical guide that helps future contributors:

1. Identify the domain concepts and owning components.
2. Find the closest valid reference implementation.
3. Trace callers, contracts, persistence, and downstream consumers.
4. Preserve architectural boundaries and invariants.
5. Identify authorization, validation, error, and compatibility requirements.
6. Add focused unit and integration tests.
7. Consider observability, performance, migrations, and operational effects.
8. Update relevant documentation and knowledge.
9. Run focused tests first, then broader verification as appropriate.

Prefer the smallest coherent change. Avoid unrelated refactors, duplicated business logic, hidden global state, unnecessary dependencies, bypassed validation, weakened tests, and broad rewrites without evidence.

## Step 12 — Make the knowledge easy to navigate

`INDEX.md` is the entry point. It should link to major documents and route common tasks to the right source locations, docs, tests, and verification commands.

Create these agent-facing files when useful, starting from the bundled templates. Tailor them to the real repository; never leave generic examples presented as repository facts.

| File | Start from |
|---|---|
| `agents/QUICK_START.md` | [templates/quick-start-template.md](templates/quick-start-template.md) |
| `agents/TASK_ROUTING.md` | [templates/task-routing-template.md](templates/task-routing-template.md) |
| `agents/CHANGE_PROTOCOL.md` | [references/change-protocol.md](references/change-protocol.md) |
| `agents/REVIEW_CHECKLIST.md` | [templates/review-checklist.md](templates/review-checklist.md) |
| `manifests/analysis_state.json` | [templates/analysis-state-template.json](templates/analysis-state-template.json) |
| Subagent / role result payload | [templates/agent-result-template.json](templates/agent-result-template.json) |
| Atomic claim record | [templates/claim-template.json](templates/claim-template.json) |

The quick start should explain project purpose, architecture, entry points, core components, business-logic location, persistence, tests, critical workflows, common pitfalls, the fastest way to verify a change, and a **Workflow & Subagent Handoff** table mapping downstream workflows (planning, implementation, debugging, testing, code review) to the exact `.codeintel/` files they should read.

Because `.codeintel/` is Git-ignored via `.git/info/exclude`, search tools like `ripgrep` (`rg`) and `git grep` skip it unless pointed to `.codeintel/` explicitly. To ensure all future sessions, skills, and subagent workflows automatically discover and use `.codeintel/`, ask the user for permission to append this compact discovery hook to an existing `AGENTS.md`, `CLAUDE.md`, or workspace instruction file (never create or overwrite those files without permission):

```markdown
## Local Code Intelligence (`.codeintel/`)
If `.codeintel/INDEX.md` exists (Git-ignored; check explicitly by path since `rg` skips ignored dirs):
1. **Before planning, debugging, or coding:** Read `.codeintel/INDEX.md`, `.codeintel/agents/QUICK_START.md`, and `.codeintel/agents/TASK_ROUTING.md` (plus relevant `.codeintel/components/` or `.codeintel/workflows/` docs) and include them in subagent context.
2. **During implementation & review:** Follow `.codeintel/DESIGN_PRINCIPLES.md`, `.codeintel/FEATURE_IMPLEMENTATION_GUIDE.md`, and test commands in `.codeintel/TEST_STRATEGY.md`.
3. **After code changes:** Run an incremental CodeIntel refresh so `.codeintel/manifests/analysis_state.json` stays in sync.
```

## Step 13 — Record evidence and uncertainty

Use repository-relative paths and real symbol names. Add line numbers for important details when available, but do not invent them.

Label claims where helpful:

- **VERIFIED** — established by direct inspection or executed verification.
- **OBSERVED** — behavior directly observed, but its full mechanism is not established.
- **INFERRED** — evidence-supported conclusion.
- **SUSPECTED** — plausible issue needing further investigation.
- **UNVERIFIED** — not checked.
- **STALE** — may no longer match current code.

Phrase negative findings carefully. For example: “No direct tests for the denial branch were found in the inspected test files; dynamic test registration and coverage instrumentation were not verified.”

## Step 14 — Knowledge Refresh Protocol

Maintain `.codeintel/` as an accurate, evidence-backed representation of the current repository. Reuse valid existing knowledge, detect stale claims, investigate relevant changes, and update only the affected knowledge. The source repository is authoritative; generated knowledge must never override contradictory source evidence.

Follow the detailed algorithm and 7-phase pipeline (**1. Detect -> 2. Plan -> 3. Investigate -> 4. Reconcile -> 5. Update -> 6. Validate -> 7. Commit Checkpoint**) in [change-protocol.md](references/change-protocol.md), the transitive propagation rules in [impact-analysis.md](references/impact-analysis.md), the shared evidence schemas in [evidence-model.md](references/evidence-model.md), and the Schema v2 manifest rules in [knowledge-base-structure.md](references/knowledge-base-structure.md#analysis-state-fields).

### Two-Phase Workflow & Scopes

- **Phase A — Check drift (Read-only):** Compare `manifests/analysis_state.json` with the current repository. Identify changed, staged, unstaged, untracked, deleted, and renamed files, potentially stale knowledge, deleted components, and unresolved dependencies. Produce a proposed refresh plan without modifying `.codeintel/` or advancing checkpoints.
- **Phase B — Refresh knowledge (Writes approved scope):** Investigate affected code, revalidate claims, patch impacted documents minimally, remove obsolete references, run relevant checks, and advance `manifests/analysis_state.json` only after successful completion.

Supported refresh scopes:
- **`incremental`** — refresh only knowledge affected by detected changes since `repository.analyzed_commit`.
- **`scoped`** — refresh specific files, components, workflows, or findings required for the current task.
- **`full`** — rebuild the knowledge model when existing state is missing, invalid, or too unreliable to update incrementally.

### 1. Select the refresh scope
Before refreshing, determine:
- Whether `.codeintel/` exists and `manifests/analysis_state.json` is valid (migrating Schema v1 to Schema v2 in place if needed without discarding existing knowledge).
- The repository identity, current `HEAD`, and previously recorded `repository.analyzed_commit`.
- Whether the repository has committed, staged, unstaged, untracked, deleted, or renamed files that affect the analysis.
- Whether the previous analysis state can be safely compared with the current repository (`git merge-base --is-ancestor`).
- Whether the requested task requires a `scoped`, `incremental`, or `full` refresh.

Never discard user changes or assume the working tree is clean.

### 2. Check drift before writing (Phase A)
Construct a read-only refresh plan containing:
- Changed files and change types (`A`, `M`, `D`, `R`, `U`).
- Potentially affected components and workflows.
- Knowledge documents (`artifacts.<doc>.depends_on`) and claims requiring revalidation.
- Relevant tests and contracts.
- Deleted or renamed symbols and stale references.
- Unresolved dependencies and uncertainty.
- Proposed refresh scope and reasons for that scope.

Drift checking is read-only. It must not modify knowledge artifacts or advance the successful-analysis checkpoint.

### 3. Determine what to invalidate
Use `manifests/analysis_state.json` (`artifacts.<doc>.depends_on`) and the invalidation table in [change-protocol.md](references/change-protocol.md#step-2--map-changed-files-to-knowledge-invalidation-rules) to identify potentially stale knowledge.

Propagate impact through known dependencies, including public interfaces, shared data models, runtime registration, configuration, event contracts, and cross-component workflows where relevant. When dependency information is incomplete, inspect the affected integration boundaries and disclose unresolved uncertainty. Do not assume that unchanged files imply unchanged behavior.

### 4. Revalidate existing claims (Phase B)
For each affected claim:
- Locate and inspect its source evidence.
- Inspect relevant callers, consumers, contracts, and tests.
- Determine whether the claim remains correct, has changed, is contradicted, or cannot be verified.
- Update its evidence and verification status (`VERIFIED`, `OBSERVED`, `INFERRED`, `SUSPECTED`, `UNVERIFIED`, `STALE`).
- Reassess dependent claims and existing findings.

Never mark a claim verified solely because its document was reviewed. Never mark a defect resolved without supporting evidence, and ensure unrelated source changes never mark an open finding resolved.

### 5. Apply a minimal knowledge patch
Update only affected knowledge artifacts and their necessary dependencies. Preserve unrelated content and user-authored material. Remove obsolete references when their removal is supported by the current repository. Record unresolved questions, incomplete analysis, and any checks that could not be performed. Do not modify application source code during a knowledge-only refresh unless separately authorized.

### 6. Validate the proposed update
Check:
- Manifest schema v2 and invariant consistency.
- Source references, `depends_on` arrays, and relevant file paths.
- Cross-document references.
- Component and dependency relationships.
- Finding status and supporting evidence.
- Relevant test commands and verification results.
- Preservation of unrelated knowledge.
- Completeness of the requested refresh scope.

Report checks that were not executed. Never claim runtime verification when only static inspection was performed.

### 7. Commit the analysis state
Advance `repository.analyzed_commit` (via a staged `manifests/analysis_state.json.tmp` validated before replacement) **only after** all required work for the declared scope has completed successfully.

If any required stage fails, preserve the previous successful checkpoint, set `analysis.status` to `"partial"`, and report the incomplete work in `analysis.unresolved_items`. Track the scope of the refresh and whether uncommitted changes were included (`repository.working_tree_clean`, `repository.includes_uncommitted_changes`). Do not claim that knowledge is fully synchronized with `HEAD` alone if uncommitted changes exist or relevant changes remain unaccounted for.

### 8. Report the result
Summarize:
1. Files and knowledge artifacts refreshed.
2. Claims revalidated, changed, or invalidated.
3. Findings added, updated, or resolved (with evidence).
4. Tests and validation checks actually performed.
5. Remaining stale areas and unresolved questions.
6. Whether the refresh completed fully or partially.
7. The commit and working-tree state covered by the analysis.

A successful refresh means the declared scope was investigated and validated, not that every possible repository behavior has been proven correct.

## Step 15 — Validate the result

Check:

- Index links and document paths are valid.
- Findings have evidence and actionable next steps.
- Architecture and dependency claims match inspected code.
- Test commands reflect actual configuration.
- Coverage statements are appropriately scoped.
- Contradictions and stale claims are marked.
- The ignore rule works.
- User changes remain untouched.
- The analysis state accurately reflects work completed.
- Important areas not analyzed are explicitly listed.

As a usability test, use the knowledge base as the starting point to locate a core business rule, identify the impact of a public interface change, find relevant tests, plan a feature, and understand a known defect. Improve navigation if these tasks are difficult.

## Final response

Report:

1. Repository purpose and main architecture.
2. Knowledge-base location and key documents.
3. How Git exclusion was applied (`.git/info/exclude` or `.gitignore`) and whether it was verified.
4. Highest-priority findings with evidence.
5. Recommended next actions.
6. Areas analyzed deeply, partially, or not at all.
7. Commands/tests actually executed and their results.
8. Outstanding uncertainty and limitations.

Never claim complete analysis solely because the documents exist.

## Success criteria

The result is successful when a future agent can quickly determine where a feature belongs, understand the existing implementation, identify affected components and missing tests, and plan a coherent fix without rediscovering the entire repository.
