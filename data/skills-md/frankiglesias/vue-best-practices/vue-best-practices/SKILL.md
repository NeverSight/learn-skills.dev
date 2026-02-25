---
name: vue-best-practices
description: This skill should be used when the user asks to review, refactor, debug, or optimize Vue 3 code for performance, correctness, SSR hydration, reactivity stability, request concurrency, TypeScript safety, or bundle size.
---

# Vue Best Practices

Use this skill as a rulebook for fixing common Vue 3 anti-patterns in production apps.

## Workflow

1. Open `AGENTS.md`.
2. Select only the relevant rule files from `rules/`.
3. Apply the smallest safe change that resolves the issue.
4. Re-check behavior and run the project's lint, test, and build checks.

## Repository Guardrails

- Use Vue 3 Composition API with `<script setup lang="ts">`.
- Follow the existing state-management pattern already used by the project (Vuex, Pinia, etc.).
- Do not create new global components.
- Do not add comments unless the user explicitly asks for them.
- Do not import Vue compiler macros (`defineProps`, `defineEmits`, `defineExpose`, `withDefaults`) from `vue`.
- Match ESLint style defaults in this repo: semicolons, single quotes, trailing commas for multiline, 2-space indent.

## Output Expectations

- Explain which rules were applied and why.
- Prefer composables and pure utilities over ad-hoc component logic.
- Keep changes incremental; avoid broad rewrites unless asked.
