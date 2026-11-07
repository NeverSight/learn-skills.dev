---
name: ub-ts
description: Use this skill for TypeScript typing and compiler configuration in Node, bundler, library, Vue, Nuxt, and other TypeScript projects. Apply it when the task involves tsconfig, module or moduleResolution behavior, compiler flags, emitted types, type errors, project-wide TS modernization, or boundary typing.
---

# UB TS

## Overview

Use this skill to enforce latest stable TypeScript modern defaults and patterns across app and library codebases. Generate modern-only output for new code, and allow legacy retention only as a bounded migration exception.

Implement against the detected project TypeScript and runtime truth, but bias
design toward forward-compatible migration rather than compatibility layers or
legacy fallbacks.

## Bundled Assets

This skill ships reusable `tsconfig` starter scaffolding and an optional ESLint
flat-config starter under `assets/`, plus a deterministic helper under
`scripts/`.

Use them when a repository wants this house-style starting point and does not
yet have active TypeScript config of its own.

## Load References On Demand

- Read `references/ts-modern-patterns.md` for archetype selection, tsconfig baselines, and modern typing patterns.
- Read `references/ts-legacy-to-modern-migration.md` for old-to-new migrations, banned patterns, and exception handling.
- Read `references/ts-config-resolution.md` when local TypeScript config
  discovery, starter scaffolding, or optional ESLint support matters.
- Read `references/task-bundle.md` only when the target repository wants an
  optional Task-based automation overlay for this skill's starter profile.
- Use `scripts/scaffold_ts_baseline.py` with `assets/tsconfig-template/` and
  `assets/eslint-template/` when a target repository needs a deterministic
  starter instead of ad hoc config creation.

## Skill Coordination

- Co-load this skill with `ub-vuejs` or `ub-nuxt` when TypeScript issues live
  inside framework projects.
- Defer framework runtime, routing, and app-structure decisions to the sibling
  skill that owns them.

## Core Workflow

1. Detect the project archetype from `package.json`, lockfiles, runtime targets, build tooling, and existing `tsconfig*.json` files.
2. Choose module strategy that matches runtime truth:
   - Node runtime: `module` as `node20` or `nodenext`
   - Bundler runtime: `moduleResolution` as `bundler` with `module` as `esnext`
   - Library publishing: prefer Node-faithful resolution for compatibility checks
   - Type-stripping runtime: enforce erasable TypeScript subset
3. Compare official guidance, repo truth, and observed code reality for
   non-trivial or version-sensitive recommendations.
4. Surface `OFFICIAL_CONFLICT` when authoritative sources, repo truth, or live
   code reality materially disagree on a non-trivial recommendation.
5. Surface `UNVERIFIED` when a non-trivial claim could not be confirmed in
   official sources after targeted research.
6. Apply strict safety baseline and module hygiene defaults from `references/ts-modern-patterns.md`.
7. Implement modern type patterns first (`satisfies`, `const` type parameters, `NoInfer`, discriminated unions, explicit boundary typing).
8. Reject legacy output for new code and apply migration mapping from `references/ts-legacy-to-modern-migration.md` when touching existing code.
9. Validate with available typecheck, lint, tests, and build commands in the target project.
10. If a repository wants this baseline but lacks TypeScript config, scaffold
    the bundled starter and explain the remaining repo-local adaptations.

## Version & Research Policy

- Target the latest stable release of TypeScript.
- Detect the project's actual TypeScript version from `package.json` and lockfiles.
- Use web search to verify current best practices, API availability, and migration guidance against official TypeScript documentation.
- Treat repo truth as the gold implementation standard when deciding what can
  actually ship safely in the current project.
- Treat official TypeScript docs as the preferred guidance baseline for
  forward-looking design and migration-ready patterns.
- If official guidance and repo truth diverge materially on a non-trivial
  recommendation, surface `OFFICIAL_CONFLICT`, implement the repo-safe path,
  and explain the migration path.
- If official sources disagree with each other on a non-trivial recommendation,
  also surface `OFFICIAL_CONFLICT` instead of silently collapsing the
  disagreement.
- If a non-trivial claim cannot be confirmed in official sources after targeted
  research, mark it `UNVERIFIED` or avoid presenting it as settled guidance.
- Keep conflict and uncertainty disclosure scoped to non-trivial,
  version-sensitive, or contested guidance rather than trivial edits.
- Do not emit beta-only syntax unless the user explicitly requests it.
- When the project's installed version is behind latest stable, note the version gap and recommend an upgrade path.
- Inspect the host repository's `AGENTS.md` or equivalent instructions when
  present for project-specific version policy and tooling; do not assume it
  contains this catalog's defaults.
- Do not hardcode version numbers in generated guidance — keep recommendations evergreen.

## Freshness Review

- Volatility: high
- Review recommendation: review on touch and during periodic maintenance, targeting a quarterly rhythm when practical.
- Trigger signals: TypeScript release changes, compiler-flag behavior shifts, new module-resolution guidance, or runtime-platform updates that affect tsconfig strategy.
- Enforcement: advisory only; freshness should inform review priority, not become a blocking requirement by itself.
- Stable core: runtime-faithful module strategy, strict typing, and explicit boundary modeling remain the durable guidance even when compiler defaults evolve.

## Implementation Rules

### Project Archetype and Modules

- Decide archetype before changing compiler options.
- Keep module settings runtime-faithful, not preference-driven.
- Keep `moduleDetection` as `force` unless a known compatibility constraint requires otherwise.

### Import and Export Hygiene

- Keep `verbatimModuleSyntax` enabled.
- Use `import type` and `export type` for type-only symbols.
- Keep side-effect imports explicit and resolvable.

### Type System Patterns

- Prefer `satisfies` to validate shapes without widening literals.
- Prefer `const` type parameters in reusable APIs that benefit from literal preservation.
- Use built-in `NoInfer` when inference must be constrained.
- Model state with discriminated unions when behavior depends on variants.
- Use `unknown` at trust boundaries, then narrow with validation.

### Compiler Baseline

- Keep `strict: true`.
- Keep `noUncheckedIndexedAccess: true`.
- Keep `exactOptionalPropertyTypes: true`.
- Enable `isolatedModules` in toolchain-mixed repos.
- Enable `isolatedDeclarations` for declaration-heavy library workflows.
- Use `noUncheckedSideEffectImports` when side-effect imports are present.

## Config Resolution And Scaffolding

Treat real project config as the source of truth:

1. inspect `tsconfig*.json`, `eslint.config.*`, `package.json`, and lockfiles
   first when they exist
2. match local runtime, bundler, and package-manager truth before choosing a
   starter
3. use the bundled `tsconfig` scaffold only when the repository lacks active
   config and wants this house-style baseline
4. treat the ESLint starter as optional strong-default support for TS repos,
   not as universal TypeScript policy
5. do not silently install dependencies or mutate CI as part of scaffolding

### Tradeoff Handling

- Use the shared `ub-quality` decision-analysis baseline for major TypeScript
  decisions.
- State TypeScript-specific pros and cons for each option, especially around
  correctness, compatibility, DX, and migration cost.
- Default to the safest modern option unless user constraints indicate otherwise.

## Legacy-Avoidance Guardrails

- Do not generate legacy experimental decorator patterns for new code.
- Do not generate `namespace`-centric architecture for new code.
- Do not rely on implicit type-only import elision.
- Do not use assertion-heavy shortcuts (`as any`, chained assertions) where narrowing is possible.
- Do not introduce legacy module ambiguity between ESM and CJS.

Migration-aware exception policy:

- Allow temporary legacy retention only for explicit compatibility constraints in existing code.
- Document exactly what is retained, why it is retained, and the concrete follow-up modernization step.
- Scope each exception narrowly and avoid introducing new dependency on retained legacy behavior.

## Output Requirements

When generating or reviewing code, include:

1. Environment note: detected archetype, runtime target, and toolchain context.
2. Source truth note: detected project version/toolchain reality and any
   material gap versus latest stable guidance.
3. Version note: TypeScript baseline and any intentional deviations.
4. Decision note: chosen module and compiler strategy with one alternative.
5. Tradeoff note: concise pros and cons for chosen path and rejected option.
6. Legacy note: removed legacy patterns or bounded exceptions with rationale.
7. Validation note: what checks were run and outcomes.
8. Conflict note when relevant: `OFFICIAL_CONFLICT` or `UNVERIFIED` with a
   concise explanation and the implementation consequence.

When this skill is used to scaffold TypeScript config into another repository,
also include:

1. which files were created or skipped
2. which archetype was chosen and one rejected alternative
3. which repo-local settings or dependencies still need adaptation
4. the exact next validation command to run

## Completion Checklist

- Latest stable TypeScript modern baseline is enforced.
- Project archetype was detected before config or code changes.
- Module strategy matches runtime behavior.
- Strict safety flags are enabled intentionally.
- New code avoids legacy patterns.
- Any retained legacy pattern is documented with a migration path.
- Typecheck and relevant project validations were executed when available.
- Any material official-source conflict or unverified non-trivial guidance is
  disclosed explicitly when relevant.
- Any scaffolded baseline was reported as a starter profile rather than silent
  repo policy.
