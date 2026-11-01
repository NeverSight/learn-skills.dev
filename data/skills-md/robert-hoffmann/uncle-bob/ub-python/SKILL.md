---
name: ub-python
description: Use this skill for Python code, typing, tests, and tooling. Apply it when the task involves Python files, pytest, Ruff, mypy or pyright, packaging or environment setup, dataclasses or Pydantic, API or service boundaries, or Python application and repository logic.
---

# UB Python

## Overview

Use this skill to enforce latest stable Python modern defaults, strict typing, boundary validation, and migration-aware legacy handling.

Generate modern patterns for new code and refactor legacy patterns incrementally when touching existing code.

Write against the project's currently supported Python version, but structure code so it can move cleanly toward newer stable releases instead of accumulating compatibility layers.

## When Not To Use

- Do not use this skill for workflow intake, sprint planning, or resumable
  initiative orchestration; defer that to `ub-workflow`.
- Do not use this skill as the primary surface when the main problem is owned
  by a non-Python workflow, documentation, or framework skill.
- Do not use this skill as a generic documentation-normalization layer when the
  main task is Markdown structure or documentation quality rather than Python
  implementation.

## Bundled Assets

This skill ships reusable Ruff scaffolding under `assets/` and a deterministic
helper under `scripts/`.

Use them when a repository wants the same Ruff baseline but does not yet have a
Python lint config of its own.

## Load References On Demand

- Read `../ub-authoring/references/authoring-conventions.md` when adjusting shared routing
  guidance, output structure, or cross-skill authoring conventions.
- Load and apply `references/python-standards.md` for canonical Python rules and toolchain policy.
- Load and apply `references/repository-python-workflows.md` for resolving the
  target repository's actual Python validation and packaging-tooling baseline.
- Load `references/ruff-config-resolution.md` when Ruff config discovery,
  adaptation points, or scaffolding behavior matters.
- Read `references/task-bundle.md` only when the target repository wants an
  optional Task-based automation overlay for this skill's starter profile.
- Use `scripts/scaffold_ruff.py` with `assets/ruff-template/` when a target
  repository needs a deterministic Ruff starter instead of ad hoc config
  rewriting.

## Forward-Compatibility Contract

- Implement for the project's actual supported Python version, runtime, and library floor.
- Bias design toward the next stable upgrade path rather than preserving older-version behavior by default.
- Prefer forward-compatible tools such as `typing_extensions`,
  `collections.abc`, and `abc` when they let the code stay compatible with the
  current repo floor while aligning with newer stable Python direction.
- Add backward-compatibility shims, fallbacks, or bridge code only when an explicit support contract or staged migration plan requires them.
- Do not treat forward-compatibility tools as permission to emit syntax that
  the repo's active Python floor cannot parse or run.

## Core Workflow

1. Detect runtime and tooling truth from project files (`pyproject.toml`, lockfiles, CI, existing configs).
2. Confirm Python scope and version contract before proposing implementation.
3. Compare official guidance, repo truth, and observed code reality for
   non-trivial or version-sensitive recommendations.
4. Surface `OFFICIAL_CONFLICT` when authoritative sources, repo truth, or live
   code reality materially disagree on a non-trivial recommendation.
5. Surface `UNVERIFIED` when a non-trivial claim could not be confirmed in
   official sources after targeted research.
6. Propose at least two viable implementation paths for non-trivial Python work, with concise pros/cons.
7. Choose the simplest path that satisfies correctness, maintainability, and project constraints.
8. Write or adjust tests first for behavior changes.
9. Implement minimal changes to pass tests, then refactor while preserving behavior and boundaries.
10. Run repository-configured validation after modifying Python code, starting with the smallest relevant scope.
11. Report outcomes, bounded exceptions, any conflict or uncertainty disclosures,
    and missing tooling gaps that materially reduce confidence.
12. If a repository wants this Ruff baseline but has no active Ruff config yet,
    scaffold the bundled starter and explain the required repo-local
    adaptations instead of embedding policy in prose.

## Version & Research Policy

- Target the latest stable release of Python for guidance, but implement against the project's actual supported version contract.
- Detect the project's actual Python version from `pyproject.toml`, `.python-version`, lockfiles, and CI configuration.
- Use web search to verify current best practices, API availability, and migration guidance against official Python documentation.
- Treat repo truth as the gold implementation standard when deciding what can
  actually ship without breaking the current project.
- Treat official Python docs as the preferred guidance baseline for
  forward-looking design and migration-ready patterns.
- If official guidance and repo truth diverge materially on a non-trivial
  recommendation, surface `OFFICIAL_CONFLICT`, implement the repo-safe path,
  and explain the forward migration path.
- If a non-trivial claim cannot be confirmed in official sources after targeted
  research, mark it `UNVERIFIED` or avoid presenting it as settled guidance.
- Keep conflict and uncertainty disclosure scoped to non-trivial,
  version-sensitive, or contested guidance rather than trivial edits.
- Do not generate syntax or stdlib behavior only available in unreleased Python versions unless the user explicitly requests it.
- When the project's installed version is behind latest stable, note the version gap, recommend an upgrade path, and prefer patterns that will survive that upgrade cleanly.
- Inspect the host repository's `AGENTS.md` or equivalent instructions when
  present for project-specific version policy and tooling; do not assume it
  contains this catalog's defaults.
- Do not hardcode version numbers in generated guidance — keep recommendations evergreen.

## Freshness Review

- Volatility: high
- Review recommendation: review on touch and during periodic maintenance, targeting a quarterly rhythm when practical.
- Trigger signals: Python release changes, tooling maturity shifts, packaging guidance updates, or repository validation changes that alter the real enforced baseline.
- Enforcement: advisory only; freshness should highlight review targets without
  pretending missing mypy or pytest wiring is automatically a blocker in every
  adopting repository.
- Stable core: strong typing, boundary validation, structured errors, and repository-truth validation remain the durable baseline even when tooling preferences evolve.

## Implementation Rules

### Runtime and Environment

- Use project-local virtual environments and interpreter-explicit commands.
- Prefer `python -m ...` and/or `uv run ...` so command execution matches the intended interpreter.
- Prefer `pathlib.Path` for filesystem operations, with Windows-safe path handling.

### Typing and API Design

- Type annotate non-trivial functions and all public interfaces.
- Prefer modern syntax: `list[str]`, `dict[str, int]`, `X | Y`, `type Alias = ...`.
- Prefer interface types from `collections.abc` (`Iterable`, `Sequence`, `Mapping`, `Callable`) and abstract contracts from `abc` or `Protocol` when concrete mutation behavior is not required.
- Prefer `typing_extensions` for newer typing features when the project's supported version floor does not provide them, or when the backport gives cleaner cross-version semantics and future-upgrade safety.
- Use `Protocol`, `Self`, `override`, `TypeGuard`, `TypeIs`, `Required`, `NotRequired`, `ReadOnly`, `TypeAliasType`, and `assert_never` when they improve correctness and refactor safety.
- Do not invent custom typing compatibility shims when `typing_extensions` already provides the migration path.
- Keep `Any` contained to boundaries and document why when unavoidable.
- In strict public or SDK-facing code, avoid ambiguous constructor overloads
  such as `dict(mapping)` when the source type is a recursive alias or broad
  `Mapping[str, JsonValue]`; prefer typed copy helpers, `{**mapping}`, or
  explicit payload builders so Pyright/Pylance can prove the exact return
  shape.

### Data Modeling and Validation

- Validate boundary data (HTTP, file, env, queue payloads) with Pydantic v2 or explicit manual validation.
- Prefer dataclasses for internal domain containers.
- Dataclass defaults: `@dataclass(slots=True, kw_only=True)` and `field(default_factory=...)` for mutable fields.
- Pydantic v2 defaults: `ConfigDict`, `@field_validator`, `@model_validator`, `model_dump()`.

### Concurrency and Structured Errors

- Prefer `asyncio.TaskGroup` for concurrent async work.
- Handle grouped failures using `ExceptionGroup` and `except*` where relevant.
- Use explicit cancellation and timeout behavior for network or external I/O.

### Packaging and Toolchain Hygiene

- Keep project metadata in `pyproject.toml` and include `[build-system]` for build backend clarity.
- Prefer modern build/install commands (`python -m pip`, `python -m build`) over deprecated `python setup.py ...` command execution.
- Favor standard library first; add dependencies only when they materially improve correctness, maintainability, or DX.

### Post-Edit Validation Contract

- After generating or modifying Python code, run the repository-configured checks that are relevant to the touched scope.
- Minimum expectation: run Ruff when Ruff is configured, run a type checker when mypy/pyright/basedpyright is configured, and run targeted pytest coverage when tests exist or behavior changed.
- Start narrow (`ruff check` on touched files, targeted tests, scoped type checks) and widen only when failures indicate broader impact.
- Fix newly introduced lint/type/test failures before finalizing when they are within the task scope.
- If a configured check cannot be run, state exactly why it was skipped or blocked.

Repository truth note:

- Detect the host repository's actual lint, typecheck, and test baseline before
  presenting a command or gate as established truth.
- `mypy` and `pytest` are often strong recommendations for Python-heavy repos,
  but they should be presented as active gates only when the host repository
  has actually wired them.
- If lint, typecheck, or test expectations are weak or absent, report that gap
  explicitly instead of pretending those checks are already enforced.

### Tooling Gap Warning Policy

- If repository Python tooling for linting, type checking, or testing is missing, weakly configured, or clearly not wired into normal workflows, warn the user explicitly.
- Recommend concrete additions when relevant: Ruff for linting, mypy/pyright for type checking, pytest for tests, and pre-commit or CI wiring for automatic enforcement.
- Treat missing quality gates as a reported risk, not as silent permission to skip validation.

### Error Handling, Logging, and Boundaries

- Fail with specific exceptions and preserve causal chains (`raise ... from err`).
- Log decisions and failures with actionable context, not noise.
- Preserve layered boundaries: presentation -> service -> repository -> data.

## Toolchain Strategy (Primary + Fallback)

- Treat repository-configured tooling as the source of truth. If Ruff, mypy, pytest, pre-commit, or other checks are configured, generate code that satisfies their active rules instead of relying on generic defaults.
- If Ruff, mypy, pytest, pre-commit, or equivalent checks are configured, run the relevant ones after edits instead of stopping at code generation.
- Primary stack: `uv`, `ruff`, `mypy`, `pytest`, `pre-commit`.
- Fallback stack when constraints require it:
  - dependency management: `pip-tools`
  - type checker: `pyright` or `basedpyright`
  - editor feedback: Pylance (Pyright engine) with `python.analysis.typeCheckingMode = "standard"` when team/editor policy prefers standard-mode diagnostics
- Keep one-command check workflows discoverable in project docs/automation when possible.

## Config Resolution And Scaffolding

Treat real tool config as the source of truth:

1. inspect `ruff.toml`, `.ruff.toml`, or `[tool.ruff]` in `pyproject.toml`
   first when they exist
2. inspect task-runner, CI, and package metadata entrypoints before assuming a
   command shape
3. use the bundled Ruff scaffold only when config is absent and the adopting
   repo wants this house style
4. treat the scaffold as a starter that still needs local adaptation for
   target version, include/exclude paths, and first-party package layout
5. do not silently install dependencies or mutate CI as part of scaffolding

## Tradeoff Handling

- Use the shared `ub-quality` decision-analysis baseline for major design or
  tooling choices.
- When Python-specific tradeoffs matter, call out compatibility, policy,
  delivery, and modernization cost explicitly in the option pros/cons.
- Default to the safest modern option unless compatibility, policy, or delivery constraints justify an alternative.
- Document any intentionally deferred cleanup or technical debt retained for compatibility.

## Legacy-Avoidance Guardrails

- Do not generate legacy typing aliases in new code (`Optional`, `Union`, `List`, `Dict`) unless required by compatibility constraints.
- Do not generate Pydantic v1 validator/style APIs in new code.
- Do not introduce new `python setup.py ...` command usage.
- Do not add untyped dict-heavy contracts when typed models are practical.
- Do not preserve support for older Python behavior "just in case" when the project no longer targets it.
- Do not add custom backward-compatibility layers for typing features when `typing_extensions` or the standard library already covers the intended migration path.

Migration-aware exception policy:

- Allow temporary legacy retention only for explicit compatibility constraints in existing code.
- Document exactly what is retained, why it is retained, and the next modernization step.

## Output Requirements

Treat this section as the stable output expectation for non-trivial Python work
in this catalog.

When generating or reviewing Python code, include:

1. Environment note: detected runtime, interpreter strategy, and relevant tooling context.
2. Source truth note: repo version/tooling reality and any material gap versus
   latest stable guidance.
3. Decision note: chosen approach and at least one alternative.
4. Tradeoff note: concise pros/cons for chosen and rejected paths.
5. Legacy note: removed legacy patterns or bounded exceptions with rationale.
6. Validation note: checks run (lint/type/test/build) and outcomes.
7. Tooling gap note: missing or weak lint/type/test enforcement that the user should consider adding or wiring in.
8. Conflict note when relevant: `OFFICIAL_CONFLICT` or `UNVERIFIED` with a
   concise explanation and the implementation consequence.

When this skill is used to scaffold Ruff into another repository, also include:

1. which files were created or skipped
2. which repo-local Ruff settings still need adaptation
3. the exact lint command the target repo should run next

## References

- Core rules and source-backed policy: `references/python-standards.md`
- Repository-specific workflow and validation baseline: `references/repository-python-workflows.md`

## Completion Checklist

- Latest stable Python baseline is enforced intentionally.
- Modern typing and boundary validation are applied where relevant.
- Data model choice (dataclass vs Pydantic v2) is explicit.
- Concurrency and error handling patterns are structured and observable.
- Repository-configured lint/type/test checks were run after edits, or an explicit reason was reported.
- No new legacy output is introduced.
- Missing lint/type/test enforcement was reported when relevant.
- Any retained legacy behavior is documented with a migration path.
- Any material official-source conflict or unverified non-trivial guidance is
  disclosed explicitly when relevant.
- Any scaffolded Ruff starter was reported as a starter profile rather than
  silent repo policy.
