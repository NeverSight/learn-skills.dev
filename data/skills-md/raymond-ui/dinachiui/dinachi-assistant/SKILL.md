---
name: dinachi-assistant
description: Unified Dinachi skill for fast component integration and plan-first generative UI guidance. Use when users ask to initialize/add Dinachi components, build concrete UI features quickly, map ambiguous product requirements to Dinachi recipes, or validate generated UI plans before implementation.
---

# Dinachi Assistant

Use one skill with two explicit modes and one automatic router.

## Mode: build-now

Use when user asks for concrete implementation quickly:

- explicit component asks (`add dialog + form`)
- install/integration asks
- direct code edits using known Dinachi components

Primary references:

- `references/components.md`
- `references/intent-map.md`
- `references/workflows.md` (command generation and verification)
- `references/troubleshooting.md` (setup/import/theme diagnosis)
- `references/maintainer-checklist.md` (monorepo component/docs/template/test updates)

Primary scripts:

1. `scripts/suggest-components.mjs --json "<prompt>"` (when component names are ambiguous)
2. `scripts/audit-skill.mjs` (maintainer consistency checks)
3. `scripts/validate-skill.mjs` (skill folder sanity checks)

Maintainer scope:

- When changing Dinachi itself in this monorepo, use `references/maintainer-checklist.md`.
- Treat `packages/components/src/<slug>` as source of truth and keep CLI templates/docs in sync.

## Mode: plan-first

Use when user intent is broad/ambiguous or generative:

- "make a good settings flow"
- "design a configurable admin experience"
- "generate a workflow UI from intent"

Primary references:

- `references/components.registry.json`
- `references/policies.json`
- `references/intent.schema.json`
- `references/recipe.schema.json`
- `references/question-policy.json`

Primary scripts:

1. `scripts/resolve-intent.mjs --json "<prompt>"`
2. If `status=clarify`, run `scripts/clarify-question.mjs --json '<GuidanceDecision JSON>'`
3. If `status=resolved`, run `scripts/plan-recipe.mjs --json '<GuidanceDecision JSON>'`
4. Validate with `scripts/validate-recipe.mjs --json '<UIRecipe JSON>'`

Only proceed to implementation when `ValidationReport.valid` is true.

## Mode: auto-router

Route automatically with:

`scripts/route-mode.mjs --json "<prompt>"`

Routing policy:

1. `build-now` when prompt contains explicit Dinachi slugs or direct install/add verbs.
2. `plan-first` when prompt is broad, qualitative, or design-oriented without concrete component selection.
3. If uncertain, choose `plan-first`.

## Shared Contracts

The plan-first pipeline uses:

- `IntentEnvelope`: `{ request_id, intents, ambiguities, confidence }`
- `GuidanceDecision`: `{ status, reason, question?, options?, candidates? }`
- `UIRecipe`: `{ recipe_id, goal, layout, components, actions, bindings, states }`
- `ValidationReport`: `{ valid, errors, warnings, fixes }`

## Operating Rules

1. Use `references/components.registry.json` as the source of truth for allowed Dinachi slugs and capabilities.
2. Keep hard guards minimal and safety-focused.
3. Keep warnings advisory; do not block on warnings alone.
4. Prefer fast path (`build-now`) for concrete requests.
5. Prefer reliable path (`plan-first`) for ambiguous or system-level requests.
