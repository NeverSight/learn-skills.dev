---
name: fable-eco
description: "Provision curated capabilities, manage reproducible capability locks, verify host integrations, and compile capability execution contracts for routed get-fable work. Use when discovering machine capabilities, managing eco profiles, planning capability installations, repairing ecosystem health, or preparing capability-aware execution contracts — even if the user does not explicitly say \"fable-eco\" (e.g. \"install eco capabilities\", \"run eco discover\", \"repair ecosystem\", \"explain capability run\"). Do NOT use as an independent task router (use get-fable)."
version: 1.0.0
pack: system
inputs:
  - routing_decision
  - project_binding
requires:
  - catalog_metadata
produces:
  - install_plan
  - execution_contract
  - capability_receipt
gates:
  - deterministic_resolution
  - transaction_journal_committed
  - health_check_passed
fallback: fable-plan
mutatesWorkspace: false
parallelSafe: true
neural_links:
  precursors:
    - get-fable
    - fable-discover
  continuations:
    - fable-execute
    - fable-verify
  lateral_peers:
    - fable-config
    - fable-run
  recovery: fable-recover
---

# Fable Eco

Curated capability distribution and execution-control subsystem for get-fable.

## Purpose

Bridge the gap between fragmented developer tool installation and disciplined agentic capability activation. `fable-eco` enforces the architectural principle of "install many, activate few": it provisions curated AI engineering capabilities (code graph indexers, review helpers, browser tools, testing runners) transactionally with immutable pinned versions and compiles task-bounded execution contracts for routed get-fable tasks under explicit least-privilege policy.

## When to Use

- Discovering local machine runtimes, compilers, package managers, and coding host configurations without side effects.
- Resolving, planning, installing, updating, or rolling back curated ecosystem capabilities.
- Managing project capability bindings in `.fable/eco.json` to declare required capabilities, profiles, and minimum contract versions.
- Diagnosing or repairing ecosystem integrity, lockfiles, journals, or broken symlinks with non-mutating doctor checks.
- Compiling deterministic capability execution contracts for agent tasks based on lifecycle routing decisions.

## When NOT to Use

- High-level lifecycle task routing or state management (use `get-fable`).
- Purely internal code authoring without external capability requirements (use `fable-execute`).
- Driving test-first red-green-refactor loops (use `fable-tdd`).
- Diagnosing repeated execution failures or broken test harnesses (use `fable-recover`).

## Inputs

- `routing_decision`: Structured routing decision from `fable_core::RoutingDecision` containing selected skill, task shape, and intent.
- `project_binding`: Optional workspace binding from `.fable/eco.json` declaring active profiles, pinned capabilities, and policy overrides.
- `catalog_layers`: Multi-layer capability manifests across official distribution, team repositories, or local directories.
- `machine_facts`: Observed system runtimes, OS platform, package managers, and host configuration state.

## Expected Outputs

- `install_plan`: Topological Directed Acyclic Graph (DAG) of installation operations with rollback classifications.
- `lockfile`: Cryptographically hashed `.fable/eco.lock` with SHA-256 digests and provenance metadata.
- `execution_contract`: Task-bounded manifest exposing only authorized tools, environment variables, and execution limits.
- `capability_receipt`: Structured record documenting host configuration edits, installed versions, and active ownership.

## Procedure

1. **Discovery**: Run non-mutating probes to discover machine facts, installed runtimes, existing capability versions, and host configuration files.
2. **Catalog Loading & Validation**: Ingest capability and profile manifests across official, team, and local catalog layers, enforcing semantic schema validation.
3. **Deterministic Resolution**: Build dependency and conflict graphs, resolve transitive capability requirements, and detect incompatibilities or missing prerequisites.
4. **Plan Generation**: Construct an execution plan outlining all file copies, download extractions, environment updates, and health checks before applying any mutation.
5. **Transactional Provisioning**: Execute operations inside a staging sandbox with a write-ahead journal (`.fable/eco-journal.json`), verifying checksums and atomic commit.
6. **Health Verification**: Run post-installation health probes for each installed capability to prove operational readiness.
7. **Receipt & Lock Sealing**: Update `.fable/eco.lock` and write host configuration ownership receipts.
8. **Contract Compilation**: For routed tasks, filter installed capabilities against the routing decision and policy rules to compile an execution contract.

## Decision Rules

- Plan before mutation: Never perform file modifications, downloads, or configuration edits without a verified pre-execution plan.
- Immutability on stable channel: Stable capabilities must resolve to immutable git commits or cryptographically hashed release archives (reject `main` or `HEAD`).
- Monotonic permission layering: Project policies can only restrict capabilities; project policies cannot override machine-wide deny rules.
- Least privilege capability activation: Expose only the specific capabilities required by the current lifecycle phase and task shape.
- Rollback on failure: If a health check or installation step fails during provisioning, trigger automated rollback using the transaction journal.

## Tool Policy

- Execute discovery and resolution natively via the high-performance `fable-eco` Rust crate.
- Use atomic filesystem staging and copy operations with strict path traversal prevention (`..` escapes prohibited).
- Execute read-only probes without altering system files or environment state.
- Validate all incoming manifests against canonical JSON Schema definitions in `schemas/eco/`.

## Evidence Requirements

- Discovery results must include structured machine facts (OS, architecture, runtimes, package managers, hosts).
- Installation plans must list all operations with explicit `id`, `kind`, `depends_on`, and `rollback_class`.
- Execution contracts must specify exact capability IDs, permitted tools, network policies, and enforcement grades.
- Completed operations require passing post-install health check evidence before lockfile persistence.

## Failure Handling

- When transaction staging fails or an unexpected crash occurs, classify journal state (`Clean`, `RecoverableRollback`, `RecoverableCommit`, `Corrupted`) and recover.
- If a required runtime or dependency is unavailable on the host machine, mark the capability as degraded or incompatible and report remediation steps.
- In case of conflicting capability requirements, halt resolution and output conflicting capability chains.

## Completion Criteria

- All selected capabilities successfully staged, verified, and committed without unhandled errors.
- Target host configuration files patched cleanly with verified ownership tags.
- Post-install health checks pass with exit code 0 and valid output.
- Deterministic `.fable/eco.lock` generated and synchronized with workspace state.
