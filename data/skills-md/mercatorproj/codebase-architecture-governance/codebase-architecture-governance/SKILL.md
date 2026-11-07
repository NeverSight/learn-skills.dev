---
name: codebase-architecture-governance
description: Analyze and improve a software project's module boundaries, dependency direction, file organization, code duplication, oversized modules, and unnecessary indirection. Use when a repository has become hard to navigate, files are proliferating, responsibilities are scattered, or a safe architecture/refactoring plan is needed. Supports analysis-only recommendations and incremental implementation across languages and frameworks.
metadata:
  version: 1.0.0
  license: MIT
  topics: [architecture, refactoring, code-organization, dependencies, codex]
---

# Codebase Architecture Governance

## Mission

Make a codebase easier to understand, change, test, and extend by clarifying responsibility, ownership, and dependency direction. Reduce accidental complexity without pursuing a simplistic target such as the fewest files, shortest files, or the most fashionable folder structure.

A successful result has:
- one authoritative implementation for each business rule;
- one clear owner for each important state and domain concept;
- understandable, intentional module boundaries;
- dependencies that point in stable directions;
- few unnecessary wrappers, compatibility layers, duplicated schemas, and cross-module hops;
- tests that protect important behavior and architecture constraints;
- a migration plan that can be applied and reviewed in small, reversible batches.

## When to use this skill

Use this skill when asked to:
- reorganize or modularize a codebase;
- reduce code sprawl, file count, or architectural complexity;
- decide whether files should be split, merged, moved, kept, or deleted;
- define frontend/backend module boundaries;
- establish a target folder structure or dependency rules;
- audit duplicated business logic, compatibility facades, pass-throughs, or circular dependencies;
- plan a safe refactor without changing product behavior;
- create repository architecture guidance or architecture tests.

## Modes of operation

Determine the requested mode from the user’s instruction.

1. **Assessment mode (default):** inspect and report; do not modify source files.
2. **Plan mode:** prepare a staged migration plan with file-level actions and validation commands.
3. **Implementation mode:** make changes only when explicitly asked. Work in small batches, preserve behavior, run available checks, and report exact paths changed.
4. **Architecture-only mode:** focus on boundaries and dependency direction; do not assume the user wants code cleanup or file deletion.

If the repository is unavailable, do not pretend to have inspected it. Offer a general target model or ask for the repository/archive only when actual source-level findings are required. Clearly distinguish source-backed facts, inferences, and recommendations.

## Core rules

1. **Understand before restructuring.** Read repository instructions, architecture docs, package manifests, entrypoints, test setup, build/packaging configuration, and representative code before recommending structural changes.
2. **Use evidence.** Base file-level claims on imports, exports, call sites, symbol references, tests, configuration, runtime discovery, and packaging. A filename, age, file size, or zero obvious imports is not sufficient proof.
3. **Separate facts from hypotheses.** Label findings as `confirmed`, `likely`, or `needs investigation`; include paths and symbols/lines when available.
4. **Preserve behavior by default.** Structural refactoring should not silently change domain rules, persisted data, public APIs, request/response contracts, user-visible flows, or error semantics.
5. **Do not over-fragment.** Split a module only when it contains genuinely distinct responsibilities, lifecycles, owners, or test seams. Do not create files merely to reach a line-count target.
6. **Do not over-consolidate.** Do not combine distinct domains just to reduce directories or files. A small file with a stable interface may be valuable.
7. **Establish ownership.** Every domain entity, mutable state, validation rule, conversion rule, and business operation should have a clearly identifiable authoritative owner.
8. **Constrain shared code.** Shared/common/utils modules may depend on stable lower-level primitives, not on feature-specific modules. Do not use `shared` as a dumping ground for uncertain ownership.
9. **Separate policies from mechanisms.** Business decisions belong in domain/application logic; HTTP, CLI, UI, storage, AI provider, and platform-specific details belong behind adapters or infrastructure boundaries.
10. **Trace indirect references.** Check dynamic imports, lazy routes, reflection, plugin registries, string-based module paths, dependency injection, generated code, test fixtures, CLI entrypoints, package exports, and deployment rules.
11. **Protect high-risk areas.** Concurrency, persistence, schema migration, algorithms, streaming, drag/drop, collision detection, undo/redo, and state synchronization need tests and small changes before restructuring.
12. **Make changes only within authorization.** A request for recommendations is not permission to edit. Never delete data, migration history, lockfiles, required generated code, or reference material blindly.
13. **Prefer reversible batches.** Avoid combining folder moves, API redesign, behavior changes, and mass renames in one step.
14. **Fit the repository.** Treat example structures in this skill as patterns, not mandatory directories. Reuse existing sound boundaries rather than rewriting names for aesthetic consistency.

## Vocabulary

Use these concepts consistently in the report:

- **Domain/module:** a cohesive capability with a clear responsibility and controlled interface.
- **Feature module:** a product capability that groups UI, local state, commands, and feature-specific types.
- **Application/use-case layer:** orchestration that coordinates business operations, transactions, and state transitions.
- **Domain/core layer:** business concepts, rules, and algorithmic capabilities that should not depend on delivery mechanisms.
- **Adapter/interface layer:** HTTP, CLI, desktop IPC, MCP, message queue, or other external entrypoints.
- **Infrastructure:** persistence, filesystem, network clients, provider SDKs, clocks, logging, and other technical implementations.
- **Facade/compatibility layer:** a wrapper or re-export maintained to preserve an API or hide implementation details.
- **Canonical path/API:** the intended import or invocation path after migration.
- **State owner:** the single module responsible for changing and validating a particular mutable state.

## Workflow

### Phase 1 — Establish repository context

Inspect the repository root and identify:
- languages, frameworks, package/workspace boundaries, and build systems;
- repository instructions such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, and architecture docs;
- runtime entrypoints, application startup, public exports, and external adapters;
- core data models, persistence formats, APIs, generated assets, and migrations;
- tests, lint/type-check/build commands, and architecture tests;
- high-risk areas and existing conventions worth preserving.

Use the repository's actual commands from its manifests and docs. Do not invent commands. Record tests/checks that could not be run and why.

Deliver a short baseline summary and state the scope and evidence limitations.

### Phase 2 — Map the current architecture

Create a current-state map before suggesting a new one. Show:
- major modules and what each appears to own;
- entrypoints and the application services they call;
- core data models and who creates, changes, validates, persists, and serializes them;
- shared dependencies and cross-cutting utilities;
- circular dependencies, dependency-direction violations, and duplicated paths where evidenced.

Prefer a simple Mermaid diagram when it makes relationships easier to understand. Use separate diagrams for different concerns rather than one unreadable graph:
- a context/container or high-level module map;
- a dependency diagram for important modules;
- a sequence/activity diagram for a critical runtime flow, only when the flow itself matters.

Do not produce diagrams as decoration. Every diagram must answer a specific reader question.

### Phase 3 — Define module responsibilities and ownership

For each major module, write a one-sentence responsibility statement. Then identify:
- what it owns;
- what it exposes publicly;
- which modules it may depend on;
- which modules must not depend on it;
- which rules/state it must not duplicate;
- how it is tested.

A healthy boundary typically has high internal cohesion, a small stable interface, and low coupling to unrelated modules.

Use **business capabilities first**, then organize files by responsibility within a capability. Organizing only by technical file type (`components/`, `utils/`, `types/`, `services/`) may be suitable for small projects, but in a large product it can scatter one feature across many unrelated directories. Prefer feature-first organization where it improves locality, while keeping genuinely shared primitives in a constrained shared layer.

### Phase 4 — Choose suitable target boundaries

Adapt to the observed stack. Do not force a universal architecture onto every project.

#### General backend pattern

A useful logical dependency direction is:

`Interfaces/adapters → Application/use cases → Domain/core`

`Infrastructure implementations` are called through explicit interfaces or injected dependencies where beneficial. Domain/core should not import HTTP frameworks, UI code, provider SDKs, or filesystem details.

Possible responsibility allocation:
- **Domain/core:** entities, value objects, invariants, domain rules, deterministic algorithms.
- **Application/use cases:** orchestrate domain operations, authorization/confirmation policies, transactions, validation sequence, and result handling.
- **Infrastructure:** persistence, files, networking, model/provider clients, clocks, logging.
- **Interfaces/adapters:** HTTP/MCP/CLI/UI bridge, input/output mapping, transport-specific error handling.

Avoid adding an abstract `domain/` or `application/` layer if it merely renames existing code and creates no useful boundary. A well-contained existing core can keep its established name.

#### General frontend pattern

Separate:
- app shell and routing;
- feature modules and their local UI/state/commands/types;
- application-level orchestration shared across features;
- shared UI primitives, transport clients, and stable cross-feature contracts.

A large frontend may use a structure such as:

```text
src/
  app/                 # bootstrap, router, shell
  features/
    <capability>/      # UI, local model/state, commands, feature API
  application/         # cross-feature workflows and orchestration
  shared/
    ui/                # generic UI primitives only
    api/               # transport/client primitives
    contracts/         # intentionally shared contracts
    utils/             # pure, genuinely generic utilities
```

This is illustrative, not a required migration target. Feature modules must not form circular dependencies. Shared modules must not import feature modules. Move a type or helper to `shared` only if it is genuinely shared and ownership is unambiguous.

#### AI/agent/workflow systems

When present, distinguish intent/input parsing, context or memory, reconciliation/decision support, workflow orchestration, and business execution. The agent may propose or request confirmation, but must not become a second implementation of business rules. Preserve meaningful workflow checkpoints for confirmation, retry, observability, and recovery.

#### Visualization/editing systems

For complex editors, distinguish UI composition, domain/editor state, rendering/scene lifecycle, interaction state machines, commands/history, and persistence/commit behavior. Do not split stateful interactions by arbitrary line count. Identify a single owner for selection, drag state, candidate placement, commit, undo/redo, and resource disposal.

#### Algorithmic or data-heavy systems

Separate domain contracts, input normalization, algorithm implementation, orchestration, and serialization/adapters. Preserve deterministic behavior, constraints, identifiers, units, rotations, ordering rules, and numerical tolerances. Do not let transport or file-format concerns leak into the algorithm core.

### Phase 5 — Audit files and modules

Classify each candidate as one of:

- `KEEP`: responsibility and boundary are sound.
- `SPLIT`: one module mixes distinct responsibilities or lifecycles.
- `MERGE`: neighboring files have the same cohesive responsibility and excessive pass-through between them.
- `MOVE`: ownership is clear but the file is in the wrong module.
- `MIGRATE-THEN-REMOVE`: compatibility export/facade can be removed after callers migrate and public uses are checked.
- `DELETE`: evidence shows it is obsolete or unused, including non-static references checked where relevant.
- `INVESTIGATE`: the available evidence cannot safely determine an action.
- `ADD-BOUNDARY`: add a small interface, owner module, or test boundary because current responsibilities are entangled.

For every non-trivial candidate, record:
- path or module;
- current responsibility;
- proposed action and target owner;
- evidence (references, symbols, tests, or observed duplication);
- confidence (`confirmed`, `likely`, `needs investigation`);
- risk (`low`, `medium`, `high`);
- prerequisites and validation command/test;
- rollback or compatibility note where useful.

Never classify a file as deletable based only on its size, name, timestamp, or absence of obvious static imports. Zero reference search results are evidence, not proof, if runtime discovery is possible.

### Phase 6 — Inspect dependencies and duplication

For high-value candidates, trace:
- imports and re-exports in both directions;
- call sites and state mutation points;
- duplicated schemas, types, validation, conversions, and state transitions;
- dependency cycles and upward dependencies;
- public exports, API routes, plugin/registry discovery, reflection, lazy imports;
- tests, fixtures, scripts, build, packaging, deployment, and documentation references;
- ownership of persistent data and cross-module contracts.

Prefer a language-aware symbol/reference tool or AST analysis when available. Use repository-wide text search as a first pass. Explain what search cannot prove.

### Phase 7 — Prioritize work by value and risk

Common high-value order (adapt based on evidence):
1. clarify public entrypoints and module ownership;
2. identify repeated business rules, schema drift, and multiple state owners;
3. remove confirmed obsolete artifacts and debug outputs;
4. converge compatibility exports and pass-throughs toward canonical APIs;
5. merge scattered implementations of one responsibility;
6. move modules to their owning feature/domain;
7. split truly multi-responsibility files with tests around the boundary;
8. address circular dependencies and add architecture checks;
9. update diagrams and developer documentation.

A large file is a **review signal**, not an automatic split request. An extra file is worthwhile if it creates a stable interface, isolated lifecycle, clearer ownership, or a useful test seam. Removing a tiny file is worthwhile only if it eliminates real indirection without weakening a boundary.

### Phase 8 — Create an incremental migration plan

Use small batches with a clear invariant:
1. establish or record the baseline;
2. add or improve focused tests around the behavior to preserve;
3. choose one module/concern;
4. migrate callers to one canonical API;
5. consolidate or move implementation;
6. remove obsolete indirection only after reference checks;
7. run focused tests and inspect the diff;
8. run type checks/lint/build and the wider suite at milestones;
9. update architecture documentation;
10. record unresolved items and rollback steps.

Do not mix a directory-wide rename, public API redesign, business-rule changes, and data migration in one batch. When a behavior change is required, separate and document it explicitly.

### Phase 9 — Add architectural guardrails

Recommend enforceable constraints where valuable, for example:
- feature modules cannot import one another except through approved public APIs;
- `shared` cannot import from `features`;
- domain/core cannot import transport or UI packages;
- interfaces/adapters call application services rather than duplicate use cases;
- only one module owns writes to a particular state or persisted entity;
- compatibility imports are deprecated and have an explicit removal path;
- critical invariants are tested at the appropriate layer.

Use the project's existing test/lint/import tooling. Do not add a heavyweight framework when a small test or lint rule is sufficient.

## Risk guidance

Usually lower risk after verification:
- stale screenshots, local debug outputs, abandoned profiler files;
- pure re-export files with callers migrated;
- duplicate pure utility functions with equivalent tests;
- documentation links and folder labels.

Usually medium risk:
- moving feature-local modules;
- merging validation/conversion logic;
- changing public import paths;
- splitting presentation from orchestration;
- refactoring agent workflow subdomains.

Usually high risk:
- persisted schemas or file formats;
- IDs and cross-stage relationships;
- auth/permissions or confirmation behavior;
- concurrent/streaming state, retries, persistence, undo/redo;
- optimization algorithms and numerical constraints;
- drag/drop/collision/3D interaction state machines;
- plugin-loaded or dynamically discovered modules.

Risk depends on actual references and tests; do not assume a category is always safe.

## Required output formats

### For an architecture assessment
1. **Executive diagnosis:** top causes of complexity, not just symptoms.
2. **Current-state map:** major modules, entrypoints, core data/state owners, dependency direction.
3. **Responsibility map:** each major module’s job, public interface, and forbidden dependencies.
4. **Proposed target structure:** illustrative tree aligned to existing stack and current code.
5. **Module/file decision table:** action, evidence, confidence, risk, proposed destination, validation.
6. **Dependency rules:** explicit allowed and forbidden directions.
7. **Phased migration sequence:** small, reversible batches with prerequisites.
8. **Behavioral invariants:** flows, contracts, and state transitions that must not change.
9. **Validation plan:** actual available tests/checks and success criteria.
10. **Unknowns:** unresolved items that need source tracing or user decision.

### For a file-pruning request
Use the file classifications in Phase 5 and include reference-tracing evidence. Clearly distinguish “candidate to inspect” from “safe to delete.”

### For implementation
Summarize the scope before editing if the change is large, then work in small batches. At the end report:
- files added/moved/changed/deleted;
- responsibility/ownership changes;
- tests and commands run with outcomes;
- tests/checks that could not run;
- behavior intentionally changed, if any;
- remaining risks and rollback options.

Be specific to the actual repository. Avoid generic advice that is not tied to paths, symbols, constraints, or observed relationships.

## Definition of done

The task is complete when:
- each major module has a clear responsibility and owner;
- important data/state has a single authoritative owner;
- dependency directions and public interfaces are understandable;
- duplicate implementations and compatibility paths have an explicit decision;
- deletions are backed by evidence rather than guesses;
- the migration is split into reviewable batches;
- critical behavior is covered by tests or explicitly marked as unverified;
- validation results and evidence limitations are honestly reported;
- architecture docs reflect the resulting design.

## Supporting references

Use these supporting files when preparing deliverables:
- `references/module-map-template.md` — current/target module responsibility map.
- `references/file-audit-template.md` — file-by-file action and evidence matrix.
- `references/refactor-plan-template.md` — phased migration checklist.
