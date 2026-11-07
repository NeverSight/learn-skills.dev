---
name: ub-vuejs
description: Use this skill for Vue component and composable authoring. Apply it when the task involves SFCs, reactivity, watchers, props or emits contracts, template patterns, SSR or hydration primitives, or Vue-core architecture in Vite projects and in Nuxt projects when the main issue is Vue authoring rather than Nuxt runtime behavior.
---

# UB VueJS

## Overview

Use this skill to enforce Vue core best practices for the latest stable release with strict TypeScript and migration-aware legacy handling. Generate only modern patterns for new code and refactor existing legacy patterns incrementally.

Implement against the detected project and runtime truth, but bias component
design toward forward-compatible migration rather than retaining legacy
patterns or outdated guidance by default.

## Load References On Demand

- Read `../ub-authoring/references/authoring-conventions.md` when adjusting routing
  guidance or cross-skill authoring conventions.
- Read `references/vue-modern-patterns.md` for the canonical modern Vue recipes and API usage patterns.
- Read `references/vue-legacy-to-modern-migration.md` for migration mapping, compatibility exceptions, and modernization sequence.

## When Not To Use

- Do not use this skill when the task depends primarily on Nuxt runtime
  behavior, app-directory policy, server routes, or Nitro concerns; co-load or
  defer that to `ub-nuxt` depending on whether Vue authoring remains a
  first-class concern.
- Do not use this skill when the main issue is Tailwind integration or plain
  CSS architecture rather than Vue component logic.

## Core Workflow

1. Detect Vue version family and tooling from `package.json`, lockfiles, `vite.config.*`, `vue.config.*`, and TypeScript config.
2. Confirm the task is Vue core scope (SFCs, reactivity, watchers, SSR and hydration, component contracts). If the task is Nuxt-specific, co-load or defer framework rules to `.agents/skills/ub-nuxt/SKILL.md`.
3. Compare official guidance, repo truth, and observed code reality for
   non-trivial or version-sensitive recommendations.
4. Surface `OFFICIAL_CONFLICT` when authoritative sources, repo truth, or live
   code reality materially disagree on a non-trivial recommendation.
5. Surface `UNVERIFIED` when a non-trivial claim could not be confirmed in
   official sources after targeted research.
6. Implement with strict TypeScript and SFC default `script setup` plus `lang="ts"`.
7. Apply modern Vue patterns from `references/vue-modern-patterns.md`.
8. Reject legacy output and apply migration mapping from `references/vue-legacy-to-modern-migration.md` when updating existing code.
9. Validate behavior with typecheck, lint, and tests available in the target project.

## Version & Research Policy

- Target the latest stable release of Vue.
- Detect the project's actual Vue version from `package.json` and lockfiles.
- Use web search to verify current best practices, API availability, and migration guidance against official Vue documentation.
- Treat repo truth as the gold implementation standard when deciding what can
  actually ship safely in the current project.
- Treat official Vue docs as the preferred guidance baseline for
  forward-looking design and migration-ready patterns.
- If official guidance and repo truth diverge materially on a non-trivial
  recommendation, surface `OFFICIAL_CONFLICT`, implement the repo-safe path,
  and explain the migration path.
- If official sources disagree with each other on a non-trivial
  recommendation, also surface `OFFICIAL_CONFLICT` instead of silently
  collapsing the disagreement.
- If a non-trivial claim cannot be confirmed in official sources after
  targeted research, mark it `UNVERIFIED` or avoid presenting it as settled
  guidance.
- Keep conflict and uncertainty disclosure scoped to non-trivial,
  version-sensitive, or contested guidance rather than trivial edits.
- When the project's installed version is behind latest stable, note the version gap and recommend an upgrade path.
- Do not use pre-release or beta features unless explicitly requested.
- Inspect the host repository's `AGENTS.md` or equivalent instructions when
  present for project-specific version policy and tooling; do not assume it
  contains this catalog's defaults.
- Do not hardcode version numbers in generated guidance — keep recommendations evergreen.

## Freshness Review

- Volatility: high
- Review recommendation: review on touch and during periodic maintenance, targeting a quarterly rhythm when practical.
- Trigger signals: Vue core API additions, hydration or watcher semantics changes, new migration guidance, or repo toolchain changes affecting Vue authoring.
- Enforcement: advisory only; stale Vue guidance should prompt review rather than create automatic blockers.
- Stable core: Composition API, strict TypeScript, and disciplined watcher patterns remain the stable baseline even when ergonomic details change.

## Implementation Rules

### Core Vue and SFC

- Require TypeScript in generated code.
- Default to `script setup` plus `lang="ts"` for SFC authoring.
- Use Composition API and compiler macros for new code.
- Prefer `defineModel()` for component `v-model` contracts in new code.
- Prefer `useTemplateRef()` for string-based template refs.

### Reactivity and Watchers

- Use reactive props destructure in script setup where it improves clarity.
- Watch destructured props with getter sources, never pass the value directly as a watch source.
- Use `MaybeRefOrGetter<T>` and `toValue()` for composables that accept value, ref, or getter inputs.
- Consider `VueUse` (`vueuse.org`, especially `@vueuse/core`) before writing
  bespoke generic composables for browser APIs, events, timers, storage,
  sensors, or async state helpers.
- Register `onWatcherCleanup()` synchronously before any `await` boundary in watcher callbacks.
- Prefer precise getters for watch sources; use numeric `deep` only when necessary.

### SSR and Hydration

- Use `useId()` for SSR-safe ID generation.
- Use lazy hydration strategies for async components when rendering heavy below-the-fold islands.
- Use `data-allow-mismatch` narrowly and document justification for each mismatch type.
- Use `Teleport defer` when the target is created later in the same render tick.

### Performance and Build Hygiene

- Prioritize high-leverage optimizations: stable props, code splitting, large-list virtualization, and controlled deep reactivity.
- Keep compile-time flags intentional and explicit in build configuration.
- Avoid premature micro-optimizations that are not backed by measurements.

## Legacy-Avoidance Guardrails

- Do not generate Options API for new code.
- Do not generate class-style components, mixins, filters, or `this`-centric component logic for new code.
- Do not generate manual `modelValue` and `update:modelValue` boilerplate when `defineModel()` is viable.
- Do not generate `ref(null)` template-ref patterns when `useTemplateRef()` is available and suitable.
- Do not generate watcher code that registers cleanup after an async boundary.

Migration-aware exception policy (see `references/vue-legacy-to-modern-migration.md`):

- Allow temporary legacy retention only when required for bounded compatibility in existing codebases.
- Document each retained legacy pattern, why it is retained, and the exact follow-up modernization path.

Non-goals:

- Do not encode Nuxt-specific directory/runtime policy in this skill; defer to `ub-nuxt`.
- Do not provide deep Tailwind implementation guidance in this skill; defer to `ub-tailwind`.

## Output Requirements

When generating or reviewing code, always include:

1. Environment note: Vue version family, TypeScript state, and key tooling detected.
2. Source truth note: detected project version and toolchain reality, plus any
   material gap versus latest stable guidance.
3. Version note: detected Vue version and whether any pre-release behavior is intentionally excluded.
4. Pattern note: which modern APIs were selected and why.
5. Legacy note: what legacy patterns were removed or intentionally retained with compatibility rationale.
6. Validation note: what checks were run (typecheck, lint, tests, build) and outcomes.
7. Conflict note when relevant: `OFFICIAL_CONFLICT` or `UNVERIFIED` with a
   concise explanation and the implementation consequence.

## Completion Checklist

- Latest stable Vue baseline and TypeScript requirement are enforced.
- New code uses Composition API and script setup with lang ts.
- `defineModel`, `useTemplateRef`, and modern watcher patterns are used where relevant.
- SSR and hydration primitives are used correctly when SSR is in scope.
- No new legacy output is introduced.
- Any retained legacy is explicitly justified with an incremental migration path.
- Nuxt and Tailwind concerns are delegated to their dedicated skills when applicable.
- Any material official-source conflict or unverified non-trivial guidance is
  disclosed explicitly when relevant.
